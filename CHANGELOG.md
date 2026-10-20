# Historique des versions — Coffre Bateleur PartenarIA

Toutes les évolutions notables du coffre-template, du plus récent au plus ancien.

Convention SemVer allégée : `vMAJOR.MINOR.PATCH`
- **MAJOR** : rupture de structure (ex : refonte IAPCRA, ajout d'une couche)
- **MINOR** : nouveau skill embarqué, nouveau template, évolution notable
- **PATCH** : correction ou épuration ciblée sur un skill existant

---

## v1.1.2 — 2026-10-20 — branche `main`

**Tes notes ne peuvent plus partir dans un dépôt, même par maladresse. Et le `.env` que la doctrine promettait d'exclure l'est enfin.**

Ton coffre est le clone d'un dépôt public. Un clone descend, il ne remonte pas : rien n'en sort tant que personne ne tape une commande d'envoi, et personne d'autre que l'auteur du template n'a le droit d'écrire dans ce dépôt. Le risque était donc théorique. Mais **« théorique » n'est pas « nul »**, et le jour où un bateleur se crée son propre dépôt, c'est lui qui décide de sa visibilité.

### Les dossiers 0 à 6 n'exposent plus que la doctrine

- **`.gitignore`** — le contenu des sept dossiers du coffre est désormais exclu en bloc, avec une **liste fermée d'exceptions** : les douze fichiers de doctrine du template, nommés un par un. Un `git add -A` tapé sans regarder n'ajoute plus rien de personnel — vérifié sur dix fichiers de test, de la daily note au `.env` en passant par une archive de données.
- 🔴 **`.gitignore` n'a aucun effet sur un fichier déjà suivi par git.** C'est ce qui rend l'exclusion sans danger : les douze fichiers de doctrine restent suivis et **continuent d'arriver par `git pull`**. Contrepartie assumée, écrite dans le fichier : ajouter un *nouveau* fichier de doctrine dans ces dossiers côté template demande désormais de l'inscrire en exception, ou de faire `git add -f`.

### Une promesse qui n'était pas tenue

- 🔴 **`AGENTS.md` dit au bateleur de ranger ses clés API dans un `.env` local, « déjà exclu par `.gitignore` ». Il ne l'était pas.** Aucune des trois branches n'excluait ce fichier — seuls `venv/` et `env/`, qui sont des dossiers Python et n'ont rien à voir. La doctrine affirmait une protection que le fichier n'implémentait pas, ce qui est pire que ne rien promettre. `.env` et `.env.*` sont maintenant exclus, `.env.example` reste versionnable.

---

## v1.1.1 — 2026-08-17

### Voix par défaut selon consonance du nom du coffre

Le skill `/initialisation` détermine automatiquement la voix du premier cri (Jessica féminine ou Pierre masculin) en analysant la consonance du prénom identifiable dans le nom du coffre saisi par le bateleur.

**Nouvelle étape 2b** :
1. Extraire le prénom candidat dans `<NOM_COFFRE>` (ignorer les mots génériques : « Coffre », « Mon », « PartenarIA », « Vault »).
2. Analyser la consonance du prénom :
   - Terminaisons féminines (`-a`, `-e`, `-ette`, `-elle`, `-ine`, `-ie`, `-ia`, `-ah`, `-anne`, etc.) ou prénom connu féminin → Jessica
   - Terminaisons masculines (`-o`, `-us`, `-in`, `-en`, `-c`, `-l`, `-r`, `-t`, `-d`, etc.) ou prénom connu masculin → Pierre
   - Ambigu (Camille, Dominique, ou aucun prénom identifiable) → **Jessica par défaut** (règle : dans le doute, féminin)
3. Utiliser cette voix à l'étape 7b pour configurer les flags Piper et lors du premier cri.

**Exemples** :
- « Elsa » → Jessica ✓
- « Marc » → Pierre ✓
- « PartenarIA Sarah » → Jessica ✓ (prénom extrait)
- « Coffre Rodrigue » → Pierre ✓
- « Mon Coffre » → Jessica ✓ (ambigu, défaut féminin)
- « Camille » → Jessica ✓ (épicène, défaut féminin)

Le bateleur peut toujours changer via `/vocal-jessica`, `/vocal-pierre`, `/vocal-siwis`, `/vocal-stop`.

Aucune question supplémentaire posée au bateleur — respect de la règle « 2 questions max au bateleur ».

---

## v1.1.0 — 2026-08-17

### Feature majeure — Mode vocal Piper local

Le partenaire IA parle. À l'initialisation, la voix **Jessica** (féminine chaleureuse, Piper local, 100% souverain, aucun appel réseau) est activée par défaut. Le premier cri est lu à voix haute.

**Nouveaux fichiers embarqués** :
- `.claude/hooks/piper_tts.py` — engine TTS Piper, appelé par le hook Stop après chaque réponse Claude Code. Lit les flags pour déterminer si le mode est actif et quelle voix utiliser. Streaming direct via `sounddevice` (multiplateforme, mais testé Windows uniquement en v1.1.0).
- `.claude/hooks/download_voice.py` — utilitaire de téléchargement des modèles `.onnx` depuis Hugging Face (`rhasspy/piper-voices`).
- `.claude/settings.local.json` — hook Stop configuré pour déclencher `piper_tts.py` après chaque réponse.

**4 nouveaux skills** :
- `/vocal-stop` — désactive le mode vocal, tue toute lecture en cours (silence immédiat). **La première commande que le bateleur apprend.**
- `/vocal-jessica` — bascule sur Jessica (féminine chaleureuse). Voix par défaut à l'initialisation.
- `/vocal-pierre` — bascule sur Pierre (masculine, même modèle UPMC).
- `/vocal-siwis` — bascule sur Siwis (féminine neutre, modèle Siwis distinct).

**Évolution `/initialisation`** :
- Étape 7b ajoutée : installation `piper-tts sounddevice` via pip, téléchargement du modèle Jessica si absent (~63 MB), activation des flags Piper.
- Le rapport final mentionne le mode vocal actif et rappelle `/vocal-stop`.
- Fallback gracieux si Piper indisponible (message clair, pas de blocage).

**Prérequis nouveau** : Python 3.x + `pip install piper-tts sounddevice`. Documenté dans le README.

**Doctrine** : le silence est un droit absolu. `/vocal-stop` marche toujours, sans blocage possible. Le mode vocal est activé par défaut pour installer d'emblée le partenariat vocal, et la première commande apprise par le bateleur est celle qui le désactive — un geste doctrinal fort (« j'ai le pouvoir d'instituer le silence »).

**Total skills embarqués** : 17 → **21**.

### Portée v1.1.0 vs v1.2.0

- v1.1.0 = **Windows-first** (testé Windows). Le code Python `piper_tts.py` est théoriquement multiplateforme (sounddevice fonctionne sur Mac/Linux) mais aucun test réalisé sur ces OS. Fallback sur `kill -9` au lieu de `taskkill` pour non-Windows.
- v1.2.0 (à venir) : validation macOS/Linux, ajustements si nécessaire.

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
