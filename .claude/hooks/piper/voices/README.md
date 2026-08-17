# Modèles Piper

Ce dossier contient les modèles vocaux Piper (`.onnx` + `.onnx.json`) téléchargés à la demande.

**Ne pas committer les `.onnx`** (ils sont dans le `.gitignore` — ~60 MB chacun).

## Modèles pris en charge

| Fichier | Voix associée(s) | Taille |
|---|---|---|
| `fr_FR-upmc-medium.onnx` | Jessica (speaker 0) + Pierre (speaker 1) | ~63 MB |
| `fr_FR-siwis-medium.onnx` | Siwis (mono-speaker) | ~60 MB |

## Téléchargement manuel

Si tu veux forcer un téléchargement :

```bash
python .claude/hooks/download_voice.py jessica    # ou pierre (même modèle UPMC)
python .claude/hooks/download_voice.py siwis
python .claude/hooks/download_voice.py --all      # les deux modèles
```

Le téléchargement se fait automatiquement au premier `/vocal-jessica` (ou `/vocal-pierre`, `/vocal-siwis`) si le modèle est absent, et lors de `/initialisation`.

## Source

Modèles hébergés par [rhasspy/piper-voices sur Hugging Face](https://huggingface.co/rhasspy/piper-voices) — Piper TTS, licence MIT.
