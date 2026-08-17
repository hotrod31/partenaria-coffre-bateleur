"""
download_voice.py — Télécharge un modèle Piper .onnx (+ .json config) depuis Hugging Face.

Usage :
  python download_voice.py jessica     # télécharge le modèle UPMC (mutualisé jessica/pierre)
  python download_voice.py pierre      # idem (même modèle)
  python download_voice.py siwis       # télécharge le modèle Siwis
  python download_voice.py --all       # télécharge tous les modèles

Les modèles sont stockés dans le sous-dossier `piper/voices/` de ce dossier.
Taille : UPMC ~63 MB, Siwis ~60 MB.
"""

import sys
import urllib.request
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.resolve()
VOICE_DIR = HOOKS_DIR / "piper" / "voices"

# Repository officiel Piper sur Hugging Face
BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR"

MODELS = {
    "upmc": {  # fr_FR-upmc-medium — utilisé par jessica ET pierre (multi-speaker)
        "onnx": "upmc/medium/fr_FR-upmc-medium.onnx",
        "json": "upmc/medium/fr_FR-upmc-medium.onnx.json",
        "size": "~63 MB",
    },
    "siwis": {  # fr_FR-siwis-medium — utilisé par siwis (mono-speaker)
        "onnx": "siwis/medium/fr_FR-siwis-medium.onnx",
        "json": "siwis/medium/fr_FR-siwis-medium.onnx.json",
        "size": "~60 MB",
    },
}

VOICE_TO_MODEL = {
    "jessica": "upmc",
    "pierre": "upmc",
    "siwis": "siwis",
}


def download_file(url: str, dest: Path):
    """Télécharge un fichier depuis une URL vers un chemin local."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Téléchargement : {url}")
    print(f"  Destination    : {dest}")
    urllib.request.urlretrieve(url, dest)
    size_mb = dest.stat().st_size / (1024 * 1024)
    print(f"  ✓ OK ({size_mb:.1f} MB)")


def download_model(model_key: str) -> bool:
    """Télécharge un modèle (onnx + json) si absent. Retourne True si téléchargé, False si déjà présent."""
    if model_key not in MODELS:
        print(f"Modèle inconnu : {model_key}")
        return False

    model = MODELS[model_key]
    onnx_path = VOICE_DIR / Path(model["onnx"]).name
    json_path = VOICE_DIR / Path(model["json"]).name

    if onnx_path.exists() and json_path.exists():
        print(f"Modèle {model_key} déjà présent ({model['size']}) — skip.")
        return False

    print(f"Téléchargement du modèle {model_key} ({model['size']})...")
    try:
        download_file(f"{BASE_URL}/{model['onnx']}", onnx_path)
        download_file(f"{BASE_URL}/{model['json']}", json_path)
        print(f"✓ Modèle {model_key} installé.")
        return True
    except Exception as exc:
        print(f"✗ Erreur téléchargement modèle {model_key} : {exc}")
        # Nettoyage des fichiers partiels
        for p in (onnx_path, json_path):
            if p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass
        return False


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    VOICE_DIR.mkdir(parents=True, exist_ok=True)

    if args[0] == "--all":
        for model_key in MODELS:
            download_model(model_key)
        return

    voice_name = args[0].lower()
    if voice_name not in VOICE_TO_MODEL:
        print(f"Voix inconnue : {voice_name}. Voix valides : {', '.join(VOICE_TO_MODEL.keys())}")
        sys.exit(1)

    model_key = VOICE_TO_MODEL[voice_name]
    download_model(model_key)


if __name__ == "__main__":
    main()
