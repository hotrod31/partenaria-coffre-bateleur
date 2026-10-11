---
name: vocal-siwis
description: "Bascule le mode vocal sur la voix Siwis (Piper local, féminine neutre, modèle fr_FR-siwis-medium mono-speaker). Souverain, gratuit, 100 % offline. Déclencher quand l'utilisateur tape /vocal-siwis, dit 'voix Siwis', 'active la voix féminine neutre', 'passe en vocal Siwis'."
---

# /vocal-siwis — Bascule voix Siwis (Piper local)

Active ou bascule le mode vocal en utilisant **Siwis** — voix féminine neutre, TTS souverain via Piper local (modèle `fr_FR-siwis-medium`, mono-speaker).

## Logique

1. **Si mode actif ET voix courante = siwis** → **désactiver** le mode vocal. Répondre : `Mode vocal désactivé.`
2. **Si mode actif ET autre voix** → **switcher** vers Siwis. Répondre : `Mode vocal basculé sur Siwis.`
3. **Si mode inactif** → **activer** avec Siwis. Répondre : `Mode vocal activé — Siwis.`

## Implémentation

Utiliser Bash pour manipuler les 2 fichiers flags dans `.claude/hooks/` du coffre :

```bash
HOOKS=".claude/hooks"
FLAG="$HOOKS/tts_enabled"
VOICE="$HOOKS/tts_piper_voice"
TARGET="siwis"

CURRENT_VOICE=""
if [ -f "$VOICE" ]; then
  CURRENT_VOICE=$(tr -d '[:space:]' < "$VOICE")
fi

if [ -f "$FLAG" ] && [ "$CURRENT_VOICE" = "$TARGET" ]; then
  rm -f "$FLAG"
  echo "Mode vocal désactivé."
elif [ -f "$FLAG" ]; then
  printf "%s" "$TARGET" > "$VOICE"
  echo "Mode vocal basculé sur Siwis."
else
  touch "$FLAG"
  printf "%s" "$TARGET" > "$VOICE"
  echo "Mode vocal activé — Siwis."
fi
```

Vérifier ensuite si le modèle est présent :

```bash
if [ ! -f ".claude/hooks/piper/voices/fr_FR-siwis-medium.onnx" ] && [ -f "$FLAG" ]; then
  echo ""
  echo "⚠ Modèle Siwis absent. Téléchargement (~60 MB)..."
  python .claude/hooks/download_voice.py siwis
fi
```

## Notes

- Modèle Siwis distinct du modèle UPMC (Jessica/Pierre) — 60 MB à télécharger en plus si tu veux essayer Siwis.
- Autres voix : `/vocal-jessica` (féminine chaleureuse), `/vocal-pierre` (masculine), `/vocal-stop` (désactive).
