# Historique des versions — Coffre Bateleur PartenarIA

Toutes les évolutions notables du coffre-template, du plus récent au plus ancien.

Convention SemVer allégée : `vMAJOR.MINOR.PATCH`
- **MAJOR** : rupture de structure (ex : refonte IAPCRA, ajout d'une couche)
- **MINOR** : nouveau skill embarqué, nouveau template, évolution notable
- **PATCH** : correction ou épuration ciblée sur un skill existant

---

## v1.0.4 — 2026-08-17

### Évolution majeure du skill `/initialisation`

Le rapport de fin comprend maintenant un **premier cri du partenaire IA** — un message de salutation et de présentation adressé au bateleur, qui pose la relation dès la fin de l'initialisation.

**Trois versions du message**, routées automatiquement selon le tempérament du bateleur détecté à partir de sa note d'introspection :

- **SYMBOLIQUE** — présentation baptismale (métaphores, quête, miroir, compagnon d'exécution) pour un bateleur au registre contemplatif/spirituel
- **ÉQUILIBRÉ** — présentation moyenne pour un bateleur au registre mixte
- **FACTUEL** — présentation opérationnelle (missions listées, ton direct) pour un bateleur au registre pragmatique

Le tempérament est détecté par 4 signaux croisés : registre lexical dans les réponses S3/S7, structure des réponses (contemplative vs structurée), discipline installée (Q12), chef-d'œuvre imaginé (Q16). Fallback ÉQUILIBRÉ si les signaux sont mixtes.

### Autres évolutions

- **Salutation temporelle** : « Bonjour » avant 18h, « Bonsoir » à partir de 18h (détection Bash `date +%H`).
- **Extraction du prénom** : le skill cherche le prénom du bateleur dans la Section 1 du fichier d'introspection (fil rouge du parcours) pour l'utiliser dans la salutation. Fallback sur le nom du coffre si non identifiable.
- **Aucun message après la présentation** : la présentation IA se suffit à elle-même. Pas de « À demain », pas de rappel /hello. Le premier cri se pose et se tait.

Le skill passe de 8 à 9 étapes internes (ajout de l'étape 4b : extraction prénom + détection tempérament).

**Respect absolu de la confidentialité** : seuls le prénom (identité) et le tempérament (registre d'expression) sont mobilisés — jamais le contenu de la matière d'introspection.

---

## v1.0.3 — 2026-08-17

### Correctifs plugins Obsidian (issus du test coffre Teillus)

- **Plugin Commander** : v0.5.5 → **v0.5.8**. La v0.5.5 avait un bug de rendu qui cassait les icônes SVG des autres plugins dans la ribbon (icônes cliquables mais invisibles). La v0.5.8 corrige.
- **Plugin periodic-notes** : v0.0.17 → **v1.0.0 stable**. Le rendu des icônes weekly/daily ne fonctionnait plus correctement avec les versions récentes d'Obsidian (1.13+). Le manifest de la release GitHub 1.0.0 contient encore `"version": "0.0.17"` par erreur du mainteneur — corrigé localement dans le manifest embarqué.

Sans ces mises à jour, les bateleurs voyaient certaines icônes de la ribbon vides ou manquantes après ouverture du coffre dans Obsidian.

---

## v1.0.2 — 2026-08-17

### Correctifs (issus du premier test end-to-end)

- **Plugin Calendar** : ajout de `main.js` (141 KB, version 1.5.10, téléchargé depuis la release officielle GitHub `liamcain/obsidian-calendar-plugin`). Sans ce fichier, le plugin était installé mais ne pouvait pas se charger — l'icône Calendar dans la ribbon Obsidian n'apparaissait pas.
- **Skill `/initialisation`** : ajout d'une **première question au bateleur** en début de flux (avant la lecture du fichier d'introspection) — « Quel nom veux-tu donner à ton coffre ? ». Le nom est utilisé pour :
  - Le titre du `Contexte.md` généré (« # Contexte — Nom du coffre »)
  - Une **proposition de renommage du dossier physique** en fin de rapport (procédure détaillée pas-à-pas : fermer Obsidian + Claude Code, renommer via l'explorateur, rouvrir).

Le flux passe de 6 à 8 étapes. Deux questions posées au bateleur au total (nom du coffre + nom de la première phase de vie).

---

## v1.0.1 — 2026-08-17

### Correctif

- Ajout de README de méthode dans `6 ARCHIVES/`, `5 RESSOURCES/Outils/` et `5 RESSOURCES/Processus/` pour que ces dossiers structurels soient présents dès le clone (Git ne track pas les dossiers vides).

---

## v1.0.0 — 2026-08-17

Première version distribuable du coffre-template Bateleur.

### Contenu embarqué

- **Structure IAPCRA** complète (0 INBOX, 1 ALIGNEMENT, 2 CONNAISSANCES, 3 PROJETS, 4 CASQUETTES, 5 RESSOURCES, 6 ARCHIVES)
- **17 skills Claude Code** : `initialisation`, `hello`, `fin-session`, `dodo`, `trier-inbox`, `bilan-jour`, `bilan-semaine`, `nouvelle-phase-vie`, `nouveau-projet`, `nouveau-chapitre`, `contradicteur`, `angles-morts`, `clarte`, `creer-commande`, `import`, `markdown`, `connect-mcp`
- **Config Obsidian** pré-embarquée avec 10 plugins : periodic-notes, calendar, obsidian-kanban, obsidian-excalidraw-plugin, advanced-canvas, cmdr, editing-toolbar, obsidian-style-settings, omnisearch, url-into-selection
- **7 templates markdown** dans `5 RESSOURCES/Modèles/` : Daily Note, Weekly Note, Projet, Casquette, Phase de vie, Bilan Phase de vie, Réflexion
- **Doctrine PartenarIA** embarquée dans `AGENTS.md`
