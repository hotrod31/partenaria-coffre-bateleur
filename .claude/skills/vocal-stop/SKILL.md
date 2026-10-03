---
name: vocal-stop
description: "Désactive le mode vocal — le partenaire IA cesse de lire ses réponses à voix haute. Rend aussi le silence immédiat si une lecture est en cours. Déclencher quand l'utilisateur tape /vocal-stop, dit 'arrête la voix', 'stop la voix', 'silence', 'coupe la voix', 'plus de voix'."
---

# /vocal-stop — Désactive le mode vocal

Désactive complètement le mode vocal du partenaire IA. Aucune réponse ne sera plus lue à voix haute jusqu'à ce que tu réactives avec `/vocal-jessica`, `/vocal-pierre` ou `/vocal-siwis`.

Tue aussi toute lecture audio en cours (silence immédiat).

## Implémentation

```bash
HOOKS=".claude/hooks"
FLAG="$HOOKS/tts_enabled"

# Tuer toute lecture en cours (silence immédiat)
python3 .claude/hooks/piper_tts.py --kill 2>/dev/null || true

# Désactiver le flag
if [ -f "$FLAG" ]; then
  rm -f "$FLAG"
  echo "Mode vocal désactivé. Silence."
else
  echo "Mode vocal déjà désactivé."
fi
```

## Notes

- Le fichier `tts_piper_voice` reste inchangé — si tu réactives ensuite avec une commande `/vocal-*`, la voix précédemment choisie est restaurée.
- Pour réactiver : `/vocal-jessica`, `/vocal-pierre`, ou `/vocal-siwis`.
- Le mode vocal est toujours **désactivable à tout moment** — c'est ton droit absolu, jamais bloqué par le système.
