---
name: clarte
tags: vision
description: "Tableau de bord actualisé du portefeuille de projets et casquettes de l'utilisateur : vue de pilotage instantanée, kanban global, blocages, urgences, chapitre actif, phase active, décisions récentes. Données factuelles uniquement, pas de suggestions. Déclencher quand l'utilisateur tape /clarte, demande 'tableau de bord', 'vue de pilotage', 'cockpit', 'dashboard', 'où en est-on', 'état des projets', 'situation', 'panorama', 'vue d'ensemble' des projets."
---

# Clarté — Tableau de bord actualisé

Affiche une vue de pilotage complète et actualisée de tous les projets, en relisant les sources de vérité avant d'afficher.

## Process

### Étape 1 : Relire les sources de vérité

Lire en parallèle :
1. **Méta-mémoire du coffre** — fichier `memory/MEMORY.md` du dossier Claude Code du workspace (Claude Code sait où le trouver via sa convention interne : `~/.claude/projects/<workspace-slug>/memory/MEMORY.md`)
2. **Chapitre actif** — scanner `1 ALIGNEMENT/Chapitres/*.md` et lire celui qui a `status: active`
3. `3 PROJETS/Suivi Projets.md` — Kanban global (tâches en cours par projet)
4. `3 PROJETS/PROJETS.md` — vue sommaire des projets
5. **Découverte dynamique des projets de dev** dans le dossier `WORKSPACE` de l'utilisateur (typiquement `$HOME/WORKSPACE` sur macOS/Linux, `%USERPROFILE%\WORKSPACE` sur Windows — à adapter selon ton organisation). On exclut automatiquement les coffres Obsidian (dossiers contenant `.obsidian/`) puisqu'ils sont déjà couverts par les étapes 2-4 ci-dessus :
   ```bash
   find "$HOME/WORKSPACE" -maxdepth 2 -name "CLAUDE.md" \
     -not -path "*/node_modules/*" \
     -not -path "*/.git/*" | while read f; do
       if [ ! -d "$(dirname "$f")/.obsidian" ]; then
         echo "$f"
       fi
     done
   ```
   Équivalent PowerShell :
   ```powershell
   Get-ChildItem -Path "$HOME/WORKSPACE" -Depth 2 -Filter "CLAUDE.md" -File |
     Where-Object { -not (Test-Path "$($_.Directory.FullName)/.obsidian") -and $_.FullName -notmatch "node_modules|\.git" }
   ```
   Lire chaque `CLAUDE.md` détecté pour connaître l'état.
6. Détecter la phase active :
   ```bash
   ls -d "1 ALIGNEMENT/Phases de vie/"*/ | sort -V | tail -1
   ```
7. Lire la daily note du jour si elle existe : `1 ALIGNEMENT/Phases de vie/[Phase active]/YYYY-WXX/YYYY-MM-DD.md`

### Étape 2 : Identifier les blocages et urgences

Depuis le Kanban global et la méta-mémoire :
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
