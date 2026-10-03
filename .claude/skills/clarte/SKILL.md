---
name: clarte
tags: vision
description: "Tableau de bord actualisé du portefeuille de projets et casquettes de l'utilisateur : vue de pilotage instantanée, backlogs, blocages, urgences, chapitre actif, phase active, décisions récentes. Données factuelles uniquement, pas de suggestions. Déclencher quand l'utilisateur tape /clarte, demande 'tableau de bord', 'vue de pilotage', 'cockpit', 'dashboard', 'où en est-on', 'état des projets', 'situation', 'panorama', 'vue d'ensemble' des projets."
---

# Clarté — Tableau de bord actualisé

Affiche une vue de pilotage complète et actualisée de tous les projets, en relisant les sources de vérité avant d'afficher.

## Process

### Étape 1 : Relire les sources de vérité

Lire en parallèle :
1. **Les notes de contexte de tes projets et de tes casquettes** — `3 PROJETS/<X>/<X>.md` et `4 CASQUETTES/<X>/<X>.md`. Leur § 3 Historique dit ce qui s'est passé, leur § 4 Todo ce qui reste, leur § 5 Expérience ce que tu en as appris. **C'est là que vit la mémoire du coffre, et nulle part ailleurs** — il n'existe aucun fichier de mémoire séparé, et c'est voulu : une mémoire tenue à côté des notes diverge de ce qu'elles disent
2. **Chapitre actif** — scanner `1 ALIGNEMENT/Chapitres/*.md` et lire celui qui a `status: active`
3. **Les backlogs** — le § 4 Todo de la note de contexte de chaque projet et de chaque casquette active. C'est là que vivent les tâches ouvertes, et il n'y a pas d'autre endroit
4. `3 PROJETS/PROJETS.md` — vue sommaire des projets
5. **Découverte dynamique des projets de dev** dans le dossier `WORKSPACE` de l'utilisateur (`$HOME/WORKSPACE` — à adapter selon ton organisation). On exclut automatiquement les coffres Obsidian (dossiers contenant `.obsidian/`) puisqu'ils sont déjà couverts par les étapes 2-4 ci-dessus :
   ```bash
   find "$HOME/WORKSPACE" -maxdepth 2 -name "CLAUDE.md" \
     -not -path "*/node_modules/*" \
     -not -path "*/.git/*" | while read f; do
       if [ ! -d "$(dirname "$f")/.obsidian" ]; then
         echo "$f"
       fi
     done
   ```
   Lire chaque `CLAUDE.md` détecté pour connaître l'état.
6. Détecter la phase active :
   ```bash
   ls -d "1 ALIGNEMENT/Phases de vie/"*/ 2>/dev/null | awk -F'/' '{d=$(NF-1); n=d+0; print n"	"$0}' | sort -n | tail -1 | cut -f2-
   ```
7. Lire la daily note du jour si elle existe : `1 ALIGNEMENT/Phases de vie/[Phase active]/YYYY-WXX/YYYY-MM-DD.md`

### Étape 2 : Identifier les blocages et urgences

Depuis les § 4 Todo et les notes de contexte :
- Tâches avec dates dépassées ou proches (cette semaine)
- Projets marqués comme bloqués (mot-clé "bloquant")
- Dépendances non résolues

### Étape 3 : Afficher le tableau de bord

```
TABLEAU DE BORD — [Date du jour, format : Samedi 27 juin 2026 (W26)]
Chapitre : [Nom du chapitre actif] ([Période])
Phase : [N] [Nom de la phase active] ([Période courte])

PROJETS DE DÉVELOPPEMENT (code)
| Projet | État | Prochaine action | Échéance |
|--------|------|------------------|----------|
| ... | ... | ... | ... |

PROJETS DE PILOTAGE (notes/audit/formation)
| Projet | État | Prochaine action | Échéance |
|--------|------|------------------|----------|
| ... | ... | ... | ... |

BLOCAGES
- [Projet] : [raison du blocage]

URGENCES CETTE SEMAINE
- [ ] [Tâche urgente] — [Projet] — [date]

DÉCISIONS RÉCENTES
- [2-3 décisions les plus récentes depuis la méta-mémoire]
```

### Étape 4 : Mettre à jour la méta-mémoire

Mettre à jour silencieusement le fichier `tableau-de-bord.md` dans le dossier mémoire du projet avec les données actualisées.

## Règles

- Ne rien demander à l'utilisateur — afficher directement
- Données factuelles uniquement, pas de suggestions
- Séparer projets de dev et projets de pilotage
- Mettre en évidence les blocages et urgences
- Concis : une ligne par projet, pas de paragraphes
- Français avec accents
- Tutoiement institué entre toi et ton IA-partenaire (posture PartenarIA)
