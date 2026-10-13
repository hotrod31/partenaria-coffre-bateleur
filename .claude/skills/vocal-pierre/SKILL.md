---
name: vocal-pierre
description: "Active la voix Pierre (masculine, moteur piper) pour CETTE fenêtre de terminal uniquement — les autres sessions ne sont pas touchées. Retaper la commande éteint la lecture de la fenêtre. Déclencher quand l'utilisateur tape /vocal-pierre, dit 'voix Pierre', 'passe en Pierre', 'lis-moi ça avec Pierre'."
---

# /vocal-pierre — la voix Pierre, pour cette fenêtre seulement

Fait lire tes réponses à voix haute par **Pierre** — masculine. Moteur : **piper**.

> 🔷 **Portée : cette fenêtre de terminal, et elle seule.** Chaque fenêtre porte sa propre voix. Une fenêtre où tu n'as rien tapé reste **muette**, et l'éteindre ici ne fait pas taire celle d'à côté. C'est ce qui permet de travailler à deux conversations sans que l'une parle par-dessus l'autre.

**Retaper `/vocal-pierre` éteint la lecture de cette fenêtre.** Même geste pour allumer et pour éteindre.

## Logique à exécuter

Lance via Bash, et **affiche la sortie telle quelle** :

```bash
python .claude/hooks/tts_bascule.py piper pierre "Pierre"
```

Le script tranche seul entre les trois cas selon ce qui est déjà actif dans cette fenêtre. Réponds avec la phrase qu'il renvoie, en rétablissant les accents :

| État de départ | Ce que tu réponds |
| --- | --- |
| lecture active, déjà sur Pierre | « Mode vocal désactivé pour cette fenêtre. » |
| lecture active, autre voix | « Mode vocal basculé sur Pierre. » |
| fenêtre muette | « Mode vocal activé — Pierre. » |

## Notes

- ✅ **100 % local, aucun appel réseau.** Rien de ce que tu dis ou écris ne sort de ta machine.
- Qualité en dessous des voix Edge : c'est le prix de la souveraineté.
- Le modèle (**fr_FR-upmc-medium.onnx**, ~70 Mo) se télécharge **au premier usage**, pas à l'installation. Le premier appel peut donc prendre une minute.
- **Toute la logique vit dans `tts_bascule.py`**, et la résolution d'état dans `tts_session.py` — une seule copie pour les huit voix, pour qu'elles ne divergent pas.
- Pour le silence immédiat pendant une lecture : **`/vocal-stop`**. C'est la première commande à connaître, avant même d'avoir entendu une voix.
- Les autres voix : **réseau** `/vocal-denise`, `/vocal-eloise`, `/vocal-vivienne`, `/vocal-henri`, `/vocal-remy` — **100 % local** `/vocal-jessica`, `/vocal-siwis`
