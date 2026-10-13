"""
edge_tts_speak.py — Lecture TTS via les voix neuronales Microsoft Edge (gratuit, sans cle).

Memes modes d'usage que piper_tts.py et fish_tts.py :
  1. python edge_tts_speak.py "Texte"
  2. echo "Texte" | python edge_tts_speak.py --stdin
  3. python edge_tts_speak.py --file <path>
  4. python edge_tts_speak.py --kill
  5. Stop hook : payload JSON sur stdin (lit si tts_enabled existe)

Voix supportees (selection via ~/.claude/hooks/tts_edge_voice) :
  - denise (defaut) : fr-FR-DeniseNeural, feminine
  - eloise          : fr-FR-EloiseNeural, feminine
  - vivienne        : fr-FR-VivienneMultilingualNeural, feminine
  - henri           : fr-FR-HenriNeural, masculine
  - remy            : fr-FR-RemyMultilingualNeural, masculine

Le service renvoie du MP3 : il est decode par soundfile (libsndfile) puis joue
par sounddevice, sans binaire externe ni fichier temporaire persistant.

NOTE : ce moteur passe par le reseau — le texte sort de la machine. Il est donc
interdit pour toute donnee de sante (MemorIA, ASRC). Pour de l'offline strict,
c'est piper_tts.py qui reste le moteur souverain.
"""

import sys
import os
import re
import io
import json
import asyncio
import subprocess
from pathlib import Path

# --- Configuration ---
# Le coffre est portable : le dossier des hooks se deduit du fichier
# lui-meme, jamais d'un chemin ecrit en dur. (Portage du 13/10/2026 depuis
# le poste de Rodrigue, ou cette ligne designait son propre profil et
# n'aurait donc rien trouve ailleurs.)
HOOKS_DIR = Path(__file__).parent.resolve()
FLAG_FILE = HOOKS_DIR / "tts_enabled"

VOICE_FILE = HOOKS_DIR / "tts_edge_voice"  # contient : denise / eloise / vivienne / henri / remy

EDGE_VOICES = {
    "denise":   "fr-FR-DeniseNeural",
    "eloise":   "fr-FR-EloiseNeural",
    "vivienne": "fr-FR-VivienneMultilingualNeural",
    "henri":    "fr-FR-HenriNeural",
    "remy":     "fr-FR-RemyMultilingualNeural",
}
DEFAULT_VOICE = "denise"

MAX_CHARS = 50000
CHUNK_TARGET = 1500

CREATE_NO_WINDOW = 0x08000000


def _verrou_de_session(prefixe):
    """Le fichier verrou de LA FENETRE appelante.

    Pose le 23/09/2026. Avant, un seul fichier par moteur retenait un seul PID :
    deux fenetres sur le meme moteur s'ecrasaient donc mutuellement le leur, et
    /m dans l'une tuait le son de l'autre. TTS_SESSION_ID est pose par
    tts_worker.py et par tts_dispatch.py. Sans lui -- appel manuel en ligne de
    commande -- on retombe sur le nom historique, qui n'a pas disparu.
    """
    sid = os.environ.get("TTS_SESSION_ID", "").strip()
    sid = "".join(c for c in sid if c.isalnum() or c in "-_")[:128]
    if not sid:
        return HOOKS_DIR / ("%s.lock" % prefixe)
    return HOOKS_DIR / ("%s.%s.lock" % (prefixe, sid))

def resolve_voice() -> str:
    """Retourne le ShortName Microsoft pour la voix de la session appelante.

    TTS_SESSION_VOICE est pose par tts_dispatch.py d'apres l'etat de la fenetre.
    Le fichier global ne sert plus que de repli hors session.
    """
    name = DEFAULT_VOICE
    de_la_session = os.environ.get("TTS_SESSION_VOICE", "").strip().lower()
    if de_la_session in EDGE_VOICES:
        return EDGE_VOICES[de_la_session]
    try:
        if VOICE_FILE.exists():
            n = VOICE_FILE.read_text(encoding="utf-8").strip().lower()
            if n in EDGE_VOICES:
                name = n
    except OSError:
        pass
    return EDGE_VOICES[name]


def _naissance(pid):
    """L'heure de naissance d'un processus, ou None s'il n'existe plus.

    Windows reattribue les numeros de processus. Un verrou abandonne -- lecture
    tuee de force, machine qui a bronche -- finit donc par designer un innocent.
    Constate le 23/09/2026 : le verrou portait le numero d'un processus sans
    rapport, qu'une commande d'arret aurait tue. Le couple (numero, heure de
    naissance), lui, est unique.
    """
    try:
        import ctypes
        from ctypes import wintypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        k = ctypes.windll.kernel32
        h = k.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if not h:
            return None
        try:
            creation = wintypes.FILETIME()
            reste = (wintypes.FILETIME(), wintypes.FILETIME(), wintypes.FILETIME())
            ok = k.GetProcessTimes(h, ctypes.byref(creation), ctypes.byref(reste[0]),
                                   ctypes.byref(reste[1]), ctypes.byref(reste[2]))
        finally:
            k.CloseHandle(h)
        if not ok:
            return None
        return (creation.dwHighDateTime << 32) | creation.dwLowDateTime
    except Exception:
        return None


def _poser_verrou(chemin):
    """Inscrit notre numero de processus et notre heure de naissance."""
    chemin.write_text("%d %s" % (os.getpid(), _naissance(os.getpid()) or 0),
                      encoding="utf-8")


def _pid_du_verrou(chemin):
    """Le PID a tuer, ou None si le verrou ne designe plus la bonne lecture."""
    try:
        morceaux = chemin.read_text(encoding="utf-8").strip().split()
        pid = int(morceaux[0])
    except (OSError, ValueError, IndexError):
        return None
    attendue = int(morceaux[1]) if len(morceaux) > 1 and morceaux[1].isdigit() else 0
    if not attendue:
        # Verrou au format d'avant le 23/09/2026 : il ne porte qu'un numero, donc
        # il ne prouve rien. On refuse de tuer sur cette seule foi.
        return None
    if _naissance(pid) != attendue:
        return None            # processus disparu, ou numero recycle : on n'y touche pas
    return pid


def extract_prose(text: str) -> str:
    """Filtre le Markdown pour ne garder que la prose lisible."""
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
    """Decoupe sur frontieres naturelles (paragraphes/phrases/espaces)."""
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
        sentences = re.split(r"(?<=[.!?\u2026])\s+", p)
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
    """Tue toute lecture audio en cours via le PID stocke dans le lock file."""
    verrou = _verrou_de_session("edge_tts")
    if not verrou.exists():
        return
    pid = _pid_du_verrou(verrou)
    if pid is None:
        # Verrou orphelin, ou numero recycle par un processus etranger.
        # On nettoie, et surtout on ne tue rien.
        try:
            verrou.unlink()
        except OSError:
            pass
        return
    try:
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            capture_output=True,
            creationflags=CREATE_NO_WINDOW,
        )
    except (ValueError, OSError):
        pass
    try:
        _verrou_de_session("edge_tts").unlink()
    except OSError:
        pass


async def synth_mp3(text: str, voice: str) -> bytes:
    """Appelle le service Edge et retourne le MP3 complet du chunk."""
    import edge_tts
    buf = bytearray()
    communicate = edge_tts.Communicate(text, voice)
    async for item in communicate.stream():
        if item["type"] == "audio":
            buf.extend(item["data"])
    return bytes(buf)


def speak(text: str):
    """Synthese Edge par chunk + lecture sounddevice."""
    text = (text or "").strip()
    if not text:
        return
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS].rsplit(" ", 1)[0] + "."

    chunks = split_into_chunks(text)
    if not chunks:
        return

    kill_previous()
    _poser_verrou(_verrou_de_session("edge_tts"))

    try:
        import sounddevice as sd
        import soundfile as sf

        voice = resolve_voice()
        stream = None
        try:
            for chunk_text in chunks:
                mp3 = asyncio.run(synth_mp3(chunk_text, voice))
                if not mp3:
                    continue
                data, samplerate = sf.read(io.BytesIO(mp3), dtype="float32", always_2d=True)
                if data.size == 0:
                    continue
                if stream is None:
                    stream = sd.OutputStream(
                        samplerate=samplerate,
                        channels=data.shape[1],
                        dtype="float32",
                    )
                    stream.start()
                stream.write(data)
        finally:
            if stream is not None:
                stream.stop()
                stream.close()
    finally:
        try:
            _verrou_de_session("edge_tts").unlink()
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

    # Mode hook Stop : payload JSON sur stdin
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
            sys.stderr.write(f"edge_tts_speak erreur: {type(exc).__name__}: {exc}\n")
        sys.exit(0)
