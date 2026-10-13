---
name: vocal-stop
description: "Coupe la lecture vocale de CETTE fenêtre de terminal, et rend le silence immédiat même si une voix est en train de parler. Les autres fenêtres ne sont pas touchées. Déclencher quand l'utilisateur tape /vocal-stop, dit 'arrête la voix', 'coupe', 'tais-toi', 'silence', 'plus de voix'."
---

# /vocal-stop — le silence, tout de suite

Coupe la lecture vocale de **cette fenêtre**. Et coupe aussi la lecture **en cours** : si une voix parle, elle s'arrête au milieu de sa phrase.

> 🔴 **C'est la première commande à connaître, avant même d'avoir entendu une voix.** Le silence est un droit absolu — jamais négociable, jamais retardé, jamais conditionné à quoi que ce soit.

> 🔷 **Portée : cette fenêtre.** Si c'est la fenêtre d'à côté qui parle, celle-ci n'a rien à couper et te le dira.

## Logique à exécuter

Lance via Bash, et **affiche la sortie telle quelle** :

```bash
python .claude/hooks/tts_stop.py
```

Réponds avec la phrase qu'il renvoie, en rétablissant les accents :
« Silence. Mode vocal désactivé pour cette fenêtre. » / « Mode vocal déjà désactivé pour cette fenêtre. »

## Notes

- Le silence vient **d'abord**, le réglage ensuite. Et il passe par le dispatcher, qui coupe **les deux moteurs** : une lecture peut être en cours sur Piper alors qu'Edge est devenu l'actif.
- **Ton choix de voix n'est pas perdu.** Rallumer avec n'importe quelle commande `/vocal-*` retrouve la voix que tu avais.
- Pour rallumer : **réseau** *(qualité supérieure)* `/vocal-denise`, `/vocal-eloise`, `/vocal-vivienne`, `/vocal-henri`, `/vocal-remy` — **100 % local** `/vocal-jessica`, `/vocal-pierre`, `/vocal-siwis`.
