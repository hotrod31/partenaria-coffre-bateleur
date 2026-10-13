---
name: vocal
description: "Allume la lecture vocale de CETTE fenêtre avec ta voix par défaut — celle que tu as choisie à l'écoute, à l'installation. Retaper la commande l'éteint. Déclencher quand l'utilisateur tape /vocal, dit 'lis-moi tes réponses', 'active la voix', 'mets la voix', 'parle-moi' sans nommer de voix."
---

# /vocal — ta voix, celle que tu as choisie

Allume la lecture vocale de **cette fenêtre** avec **ta voix par défaut** — celle que tu as retenue en écoutant les échantillons, le jour de l'installation.

**Retaper `/vocal` éteint la lecture de cette fenêtre.**

> 🔷 **Portée : cette fenêtre de terminal, et elle seule.** Les autres ne sont pas touchées.

## Logique à exécuter

Lance via Bash, et **affiche la sortie telle quelle** :

```bash
python .claude/hooks/tts_bascule.py --defaut
```

## Notes

- La voix par défaut est écrite dans `tts_voix_defaut`. **Pour la changer, il suffit d'utiliser une commande nommée** — `/vocal-pierre` par exemple — et ce choix devient la nouvelle voix par défaut.
- Si aucune voix par défaut n'a été posée, c'est **Jessica** *(féminine chaleureuse, 100 % locale)*.
- Pour le silence immédiat : **`/vocal-stop`**.
- Les voix nommées : **réseau** `/vocal-denise`, `/vocal-eloise`, `/vocal-vivienne`, `/vocal-henri`, `/vocal-remy` — **100 % local** `/vocal-jessica`, `/vocal-pierre`, `/vocal-siwis`.
