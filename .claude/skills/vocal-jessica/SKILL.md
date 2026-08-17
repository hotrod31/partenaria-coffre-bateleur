---
name: vocal-jessica
description: "Bascule le mode vocal sur la voix Jessica (Piper local, féminine chaleureuse, modèle fr_FR-upmc-medium speaker 0). Souverain, gratuit, 100 % offline. Déclencher quand l'utilisateur tape /vocal-jessica, dit 'voix Jessica', 'active la voix féminine chaleureuse', 'passe en vocal Jessica'."
---

# /vocal-jessica — Bascule voix Jessica (Piper local)

Active ou bascule le mode vocal en utilisant **Jessica** — voix féminine chaleureuse, TTS souverain via Piper local (modèle `fr_FR-upmc-medium` speaker `0`).

## Logique

1. **Si mode actif ET voix courante = jessica** → **désactiver** le mode vocal. Répondre : `Mode vocal désactivé.`
2. **Si mode actif ET autre voix** → **switcher** vers Jessica. Répondre : `Mode vocal basculé sur Jessica.`
3. **Si mode inactif** → **activer** avec Jessica. Répondre : `Mode vocal activé — Jessica.`

## Implémentation

Utiliser Bash pour manipuler les 2 fichiers flags dans `.claude/hooks/` du coffre :

```bash
HOOKS=".claude/hooks"
FLAG="$HOOKS/tts_enabled"
VOICE="$HOOKS/tts_piper_voice"
TARGET="jessica"

CURRENT_VOICE=""
if [ -f "$VOICE" ]; then
  CURRENT_VOICE=$(tr -d '[:space:]' < "$VOICE")
fi

if [ -f "$FLAG" ] && [ "$CURRENT_VOICE" = "$TARGET" ]; then
  rm -f "$FLAG"
  echo "Mode vocal désactivé."
elif [ -f "$FLAG" ]; then
  printf "%s" "$TARGET" > "$VOICE"
  echo "Mode vocal basculé sur Jessica."
else
  touch "$FLAG"
  printf "%s" "$TARGET" > "$VOICE"
  echo "Mode vocal activé — Jessica."
fi
```

Vérifier ensuite si le modèle est présent :

```bash
if [ ! -f ".claude/hooks/piper/voices/fr_FR-upmc-medium.onnx" ] && [ -f "$FLAG" ]; then
  echo ""
  echo "⚠ Modèle Jessica absent. Téléchargement (~63 MB)..."
  python .claude/hooks/download_voice.py jessica
fi
```

## Notes

- Piper = TTS open source MIT, 100 % CPU local. Latence ~1-2 s pour une phrase courte. Aucun appel réseau.
- Modèle mutualisé : `fr_FR-upmc-medium.onnx` contient à la fois Jessica (speaker 0) et Pierre (speaker 1) — un seul fichier .onnx pour ces deux voix.
- Autres voix : `/vocal-pierre` (masculine), `/vocal-siwis` (féminine neutre), `/vocal-stop` (désactive).
- Le hook Stop dans `.claude/settings.local.json` lit automatiquement chaque réponse Claude Code quand le mode est actif.

## Prérequis

- Python 3.x
- `pip install piper-tts sounddevice` (installés automatiquement au premier `/initialisation`)
