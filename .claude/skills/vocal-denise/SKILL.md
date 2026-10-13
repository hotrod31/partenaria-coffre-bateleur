---
name: vocal-denise
description: "Active la voix Denise (féminine, posée, moteur edge) pour CETTE fenêtre de terminal uniquement — les autres sessions ne sont pas touchées. Retaper la commande éteint la lecture de la fenêtre. Déclencher quand l'utilisateur tape /vocal-denise, dit 'voix Denise', 'passe en Denise', 'lis-moi ça avec Denise'."
---

# /vocal-denise — la voix Denise, pour cette fenêtre seulement

Fait lire tes réponses à voix haute par **Denise** — féminine, posée. Moteur : **edge**.

> 🔷 **Portée : cette fenêtre de terminal, et elle seule.** Chaque fenêtre porte sa propre voix. Une fenêtre où tu n'as rien tapé reste **muette**, et l'éteindre ici ne fait pas taire celle d'à côté. C'est ce qui permet de travailler à deux conversations sans que l'une parle par-dessus l'autre.

**Retaper `/vocal-denise` éteint la lecture de cette fenêtre.** Même geste pour allumer et pour éteindre.

## Logique à exécuter

Lance via Bash, et **affiche la sortie telle quelle** :

```bash
python .claude/hooks/tts_bascule.py edge denise "Denise"
```

Le script tranche seul entre les trois cas selon ce qui est déjà actif dans cette fenêtre. Réponds avec la phrase qu'il renvoie, en rétablissant les accents :

| État de départ | Ce que tu réponds |
| --- | --- |
| lecture active, déjà sur Denise | « Mode vocal désactivé pour cette fenêtre. » |
| lecture active, autre voix | « Mode vocal basculé sur Denise. » |
| fenêtre muette | « Mode vocal activé — Denise. » |

## Notes

- ⚠️ **Ce moteur passe par le réseau.** Le texte de la réponse sort de ta machine pour être transformé en voix par Microsoft. C'est gratuit et sans compte, mais **ce n'est pas souverain**. Pour une lecture qui ne quitte jamais ta machine : `/vocal-jessica`, `/vocal-pierre`, `/vocal-siwis`.
- Qualité nettement au-dessus de Piper, et **aucun modèle à télécharger**.
- 🔴 **Ces voix ne sont présentes que si le service répondait le jour de l'installation.** S'il ne répondait pas, le moteur n'a pas été installé et cette commande te le dira franchement au lieu de rester muette.
- **Toute la logique vit dans `tts_bascule.py`**, et la résolution d'état dans `tts_session.py` — une seule copie pour les huit voix, pour qu'elles ne divergent pas.
- Pour le silence immédiat pendant une lecture : **`/vocal-stop`**. C'est la première commande à connaître, avant même d'avoir entendu une voix.
- Les autres voix : **réseau** `/vocal-eloise`, `/vocal-vivienne`, `/vocal-henri`, `/vocal-remy` — **100 % local** `/vocal-jessica`, `/vocal-pierre`, `/vocal-siwis`
