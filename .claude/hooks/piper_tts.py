"""
piper_tts.py — Lecture TTS via Piper en local (souverain, gratuit, 100 % offline).

Ce script est exécuté par le hook Stop de Claude Code après chaque réponse de l'IA.
Il lit les flags dans le même dossier pour déterminer si le mode vocal est actif,
quelle voix utiliser, et joue la réponse via Piper si tout est OK.

Modes d'usage :
  1. Hook Stop : payload JSON sur stdin (lit si tts_enabled existe)
  2. python piper_tts.py "Texte"                (lecture directe)
  3. echo "Texte" | python piper_tts.py --stdin (lecture depuis stdin)
  4. python piper_tts.py --file <path>           (lecture depuis fichier)
  5. python piper_tts.py --kill                  (arrête toute lecture en cours)

Voix supportées (sélection via `tts_piper_voice` dans ce dossier) :
  - jessica (défaut) : UPMC speaker 0, féminine chaleureuse
  - pierre           : UPMC speaker 1, masculine
  - siwis            : Siwis mono-speaker, féminine neutre

Prérequis Python :
  pip install piper-tts sounddevice
"""

import sys
import os
import re
import json
import subprocess
import platform
from pathlib import Path

# --- Configuration self-contained ---
# Tous les chemins sont relatifs au dossier de ce script.
HOOKS_DIR = Path(__file__).parent.resolve()
FLAG_FILE = HOOKS_DIR / "tts_enabled"
LOCK_FILE = HOOKS_DIR / "piper_tts.lock"

VOICE_DIR = HOOKS_DIR / "piper" / "voices"
VOICE_FILE = HOOKS_DIR / "tts_piper_voice"  # contient l'identifiant de voix : jessica / pierre / siwis

# Mapping identifiant → (fichier .onnx, speaker_id ou None pour mono-speaker)
PIPER_VOICES = {
    "jessica": (VOICE_DIR / "fr_FR-upmc-medium.onnx", 0),
    "pierre":  (VOICE_DIR / "fr_FR-upmc-medium.onnx", 1),
    "siwis":   (VOICE_DIR / "fr_FR-siwis-medium.onnx", None),
}
DEFAULT_VOICE = "jessica"

MAX_CHARS = 50000
CHUNK_TARGET = 1500

IS_WINDOWS = platform.system() == "Windows"
CREATE_NO_WINDOW = 0x08000000 if IS_WINDOWS else 0


def resolve_voice():
    """Retourne (model_path, speaker_id) selon le contenu de tts_piper_voice."""
    name = DEFAULT_VOICE
    try:
        if VOICE_FILE.exists():
            n = VOICE_FILE.read_text(encoding="utf-8").strip().lower()
            if n in PIPER_VOICES:
                name = n
    except OSError:
        pass
    return PIPER_VOICES[name]


def extract_prose(text: str) -> str:
    """Filtre le Markdown pour ne garder que la prose lisible à voix haute."""
    lines = text.split("\n")
    paragraphs = []
    current = []
    in_code_block = False

    def flush():
        if current:
            paragraphs.append(" ".join(current))
            current.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            flush()
            continue
        if in_code_block:
            continue
        if stripped.startswith("|"):
            continue
        if re.match(r"^[-*_]{3,}$", stripped):
            continue
        if re.match(r"^={3,}$", stripped):
            continue
        if not stripped:
            flush()
            continue
        cleaned = re.sub(r"^#{1,6}\s+", "", line)
        cleaned = re.sub(r"\*{1,3}([^*\n]+)\*{1,3}", r"\1", cleaned)
        cleaned = re.sub(r"`[^`\n]+`", "", cleaned)
        cleaned = re.sub(r"\[([^\]\n]+)\]\([^)\n]+\)", r"\1", cleaned)
        cleaned = re.sub(r"\[\[([^\]\n]+)\]\]", r"\1", cleaned)
        cleaned = re.sub(r"^[-*+]\s+", "", cleaned)
        cleaned = cleaned.strip()
        if cleaned:
            current.append(cleaned)
    flush()
    return "\n\n".join(paragraphs)


def split_into_chunks(text, target=CHUNK_TARGET):
    """Découpe sur frontières naturelles (paragraphes/phrases/espaces)."""
    text = (text or "").strip()
    if not text:
        return []

    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    buf = ""

    def push_buf():
        nonlocal buf
        if buf:
            chunks.append(buf)
            buf = ""

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        if len(p) <= target:
            if buf and len(buf) + 1 + len(p) > target:
                push_buf()
            buf = (buf + " " + p).strip() if buf else p
            continue

        push_buf()
        sentences = re.split(r"(?<=[.!?…])\s+", p)
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            if len(s) > target:
                push_buf()
                while len(s) > target:
                    cut = s[:target].rsplit(" ", 1)[0]
                    if not cut:
                        cut = s[:target]
                    chunks.append(cut)
                    s = s[len(cut):].strip()
                if s:
                    buf = s
                continue
            if buf and len(buf) + 1 + len(s) > target:
                push_buf()
            buf = (buf + " " + s).strip() if buf else s

    push_buf()
    return chunks


def kill_previous():
    """Tue toute lecture audio en cours via le PID stocké dans le lock file."""
    if not LOCK_FILE.exists():
        return
    try:
        pid = int(LOCK_FILE.read_text().strip())
        if IS_WINDOWS:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                capture_output=True,
                creationflags=CREATE_NO_WINDOW,
            )
        else:
            subprocess.run(["kill", "-9", str(pid)], capture_output=True)
    except (ValueError, OSError):
        pass
    try:
        LOCK_FILE.unlink()
    except OSError:
        pass


def speak(text: str):
    """Streaming Piper local + sounddevice."""
    text = (text or "").strip()
    if not text:
        return
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS].rsplit(" ", 1)[0] + "."

    chunks = split_into_chunks(text)
    if not chunks:
        return

    kill_previous()
    LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")

    try:
        import sounddevice as sd
        from piper import PiperVoice
        from piper.config import SynthesisConfig

        model_path, speaker_id = resolve_voice()
        if not model_path.exists():
            # Modèle absent — silence, l'utilisateur doit lancer /vocal-setup
            return

        voice = PiperVoice.load(str(model_path))
        syn_config = SynthesisConfig(speaker_id=speaker_id) if speaker_id is not None else None
        sample_rate = voice.config.sample_rate

        stream = sd.RawOutputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )
        stream.start()
        try:
            for chunk_text in chunks:
                for audio_chunk in voice.synthesize(chunk_text, syn_config=syn_config):
                    pcm = audio_chunk.audio_int16_bytes
                    if pcm:
                        n = len(pcm) - (len(pcm) % 2)
                        if n > 0:
                            stream.write(pcm[:n])
        finally:
            stream.stop()
            stream.close()
    except ImportError:
        # piper-tts ou sounddevice non installés — silence
        return
    finally:
        try:
            LOCK_FILE.unlink()
        except OSError:
            pass


def read_stdin_utf8() -> str:
    raw = sys.stdin.buffer.read()
    if not raw:
        return ""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


def main():
    args = sys.argv[1:]

    if args and args[0] == "--stdin":
        text = read_stdin_utf8().strip()
        speak(text)
        return

    if args and args[0] == "--file":
        if len(args) < 2:
            return
        path = args[1]
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except OSError:
            return
        if path.lower().endswith((".md", ".markdown")):
            text = extract_prose(text)
        speak(text)
        return

    if args and args[0] == "--kill":
        kill_previous()
        return

    if args:
        text = " ".join(args).strip()
        speak(text)
        return

    # Mode hook Stop : payload JSON sur stdin, lit si tts_enabled existe
    if not FLAG_FILE.exists():
        return

    raw_text = read_stdin_utf8()
    if not raw_text:
        return

    try:
        payload = json.loads(raw_text)
    except ValueError:
        return

    text = payload.get("last_assistant_message") or ""
    if not text:
        return

    prose = extract_prose(text)
    if not prose:
        return

    speak(prose)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        if sys.argv[1:]:
            sys.stderr.write(f"piper_tts erreur: {type(exc).__name__}: {exc}\n")
        sys.exit(0)
