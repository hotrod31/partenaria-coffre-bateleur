---
name: vocal-pierre
description: "Bascule le mode vocal sur la voix Pierre (Piper local, masculine, modèle fr_FR-upmc-medium speaker 1). Souverain, gratuit, 100 % offline. Déclencher quand l'utilisateur tape /vocal-pierre, dit 'voix Pierre', 'active la voix masculine', 'passe en vocal Pierre'."
---

# /vocal-pierre — Bascule voix Pierre (Piper local)

Active ou bascule le mode vocal en utilisant **Pierre** — voix masculine, TTS souverain via Piper local (modèle `fr_FR-upmc-medium` speaker `1`).

## Logique

1. **Si mode actif ET voix courante = pierre** → **désactiver** le mode vocal. Répondre : `Mode vocal désactivé.`
2. **Si mode actif ET autre voix** → **switcher** vers Pierre. Répondre : `Mode vocal basculé sur Pierre.`
3. **Si mode inactif** → **activer** avec Pierre. Répondre : `Mode vocal activé — Pierre.`

## Implémentation

Utiliser Bash pour manipuler les 2 fichiers flags dans `.claude/hooks/` du coffre :

```bash
HOOKS=".claude/hooks"
FLAG="$HOOKS/tts_enabled"
VOICE="$HOOKS/tts_piper_voice"
TARGET="pierre"

CURRENT_VOICE=""
if [ -f "$VOICE" ]; then
  CURRENT_VOICE=$(tr -d '[:space:]' < "$VOICE")
fi

if [ -f "$FLAG" ] && [ "$CURRENT_VOICE" = "$TARGET" ]; then
  rm -f "$FLAG"
  echo "Mode vocal désactivé."
elif [ -f "$FLAG" ]; then
  printf "%s" "$TARGET" > "$VOICE"
  echo "Mode vocal basculé sur Pierre."
else
  touch "$FLAG"
  printf "%s" "$TARGET" > "$VOICE"
  echo "Mode vocal activé — Pierre."
fi
```

Vérifier ensuite si le modèle est présent :

```bash
if [ ! -f ".claude/hooks/piper/voices/fr_FR-upmc-medium.onnx" ] && [ -f "$FLAG" ]; then
  echo ""
  echo "⚠ Modèle Pierre absent. Téléchargement (~63 MB)..."
  python3 .claude/hooks/download_voice.py pierre
fi
```

## Notes

- Modèle mutualisé avec Jessica : `fr_FR-upmc-medium.onnx` contient les deux speakers. Si Jessica a été téléchargée avant, aucun re-téléchargement nécessaire.
- Autres voix : `/vocal-jessica` (féminine chaleureuse), `/vocal-siwis` (féminine neutre), `/vocal-stop` (désactive).
