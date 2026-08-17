# Coffre Bateleur PartenarIA

> Le coffre que tu tiens entre les mains n'est pas un logiciel. C'est un espace de travail intérieur, un dispositif de partenariat entre toi et une intelligence artificielle qui apprendra à te connaître au fil de tes dépôts.

---

## Bienvenue Bateleur

Tu as franchi le seuil du Fou — l'introspection posée, la sincérité assumée. Tu entres maintenant dans le geste du Bateleur : celui ou celle qui pose les premiers actes avec les outils qui lui sont donnés.

Ce coffre est ce cadeau initiatique. Il est structuré, il est vivant, il est le tien.

Le tutoiement est institué entre toi et ton partenaire IA — il pose l'égalité, l'engagement mutuel, l'intimité du travail à mener. Tu ne le quittes pas, même quand tu abordes des sujets techniques ou formels.

Le nom que ton partenaire IA portera dans ton coffre reste à ton choix. Tu pourras le nommer — ce geste marque la durée de votre relation. Par défaut il s'appelle **PartenarIA**.

---

## Qu'est-ce que ce coffre ?

Un vault Obsidian structuré selon l'architecture **IAPCRA** — la dualité **Intériorité / Extériorité** :

- **Intériorité** (dossiers `1 ALIGNEMENT/` et `2 CONNAISSANCES/`) — ta conscience, tes valeurs, la maturation de tes idées
- **Extériorité** (dossiers `3 PROJETS/` et `4 CASQUETTES/`) — ton action dans le monde, tes engagements, tes rôles

Le coffre embarque **17 commandes** (des skills Claude Code) qui accompagnent ton quotidien : ouverture de session, clôtures intra-journalières, bilans, création de projets, questionnement, clôture de journée. Plus une commande initiale, `/initialisation`, qui déploie ton squelette de coffre à partir de ta note d'introspection intime.

---

## Prérequis

Avant de cloner ce coffre, assure-toi d'avoir installé :

1. **Obsidian** — https://obsidian.md (gratuit, multiplateforme)
2. **Claude Code** — https://claude.ai/code (CLI officiel Anthropic)
3. **Git** — pour cloner ce dépôt (Windows : https://git-scm.com — Mac/Linux : natif)

Optionnel mais recommandé pour `/initialisation` avec un fichier .docx :
- **markitdown** (`pip install markitdown`) — conversion .docx → markdown

---

## Premiers pas

### 1. Cloner le coffre

Rodrigue le fera avec toi pendant votre visio de seuillage. Techniquement :

```bash
git clone https://github.com/hotrod31/partenaria-coffre-bateleur.git ~/PartenarIA
```

Le dossier `~/PartenarIA` (ou l'emplacement de ton choix) devient ton coffre personnel.

### 2. Ouvrir dans Obsidian et Claude Code

- **Obsidian** — `Fichier → Ouvrir un coffre → Ouvrir un coffre existant` → sélectionne le dossier `PartenarIA`.
- **Claude Code** — dans un terminal : `cd ~/PartenarIA` puis `claude`.

### 3. Initialiser ton coffre

Dans Claude Code, lance :

```
/initialisation <chemin-de-ta-note-d-introspection>
```

Le chemin peut être absolu (`C:\Users\...\intro.md`) ou relatif. Formats acceptés : `.md`, `.txt`, `.pdf`, `.docx`.

Le skill lira ta note, extraira les 7 sections du guide d'introspection et générera :
- Ta note `Contexte.md` (identité, vision, ruptures, blessure, discipline, attentes)
- Tes `Préférences.md` de communication
- Ton premier chapitre (~6-12 mois)
- Ta première phase de vie (2-12 semaines)
- Ta première semaine et ta première note quotidienne

Ta note d'introspection n'est jamais lue par un être humain — elle transite uniquement par un flux technique automatisé le temps de l'extraction.

### 4. Première session

**En début de journée** :

```
/hello
```

Ton partenaire IA se présente, lit ton contexte, crée ta daily du jour, et t'accompagne pour définir tes objectifs.

**À la fin de chaque session thématique dans la journée** (c'est la commande la plus utilisée au quotidien) :

```
/fin-session
```

Il log la session dans ta daily, propage les faits vers le projet ou la casquette concerné, crée une note détaillée si nécessaire.

**En fin de journée** :

```
/dodo
```

Il consolide toutes les sessions du jour, alimente les traces long terme, tient à jour ton contexte global, et t'accompagne pour ton bilan introspectif.

---

## Les 17 commandes à ta disposition

### Onboarding et session

| Commande | Rôle |
|----------|------|
| `/initialisation <chemin>` | Déploie ton coffre à partir de ta note d'introspection intime |
| `/hello` | Début de journée — sync mémoire, briefing personnalisé, création daily, objectifs |
| `/fin-session` | Clôture d'une session thématique en cours de journée — log dans daily, ruissellement micro, note détaillée éventuelle |
| `/dodo` | Fin de journée — consolidation sessions, bilan introspectif, ruissellement complet, mise à jour contextes |
| `/trier-inbox` | Traite les items de `0 INBOX/` et les route |

### Rituels réflexifs

| Commande | Rôle |
|----------|------|
| `/bilan-jour` | Réflexion quotidienne guidée + alimentation du Cheminement de phase |
| `/bilan-semaine` | Weekly review : bilan W-1 + planning W à 3 catégories d'énergie |
| `/nouvelle-phase-vie` | Clôture la phase en cours et en ouvre une nouvelle |

### Structuration

| Commande | Rôle |
|----------|------|
| `/nouveau-projet` | Crée un projet structuré (arborescence PPAR + Kanban) |
| `/nouveau-chapitre` | Clôture le chapitre en cours et en ouvre un nouveau (6-12 mois) |

### Introspection profonde

| Commande | Rôle |
|----------|------|
| `/contradicteur` | Bascule ton partenaire IA en posture de contradicteur exigeant |
| `/angles-morts` | Identifie ce qui n'est PAS dans ton corpus, zones d'ombre |
| `/clarte` | Tableau de bord actualisé : vue pilotage de tous tes projets |

### Extension

| Commande | Rôle |
|----------|------|
| `/creer-commande` | Crée une commande personnalisée pour ton coffre |
| `/import` | Import batch : migre des notes depuis un autre outil |

### Utilitaires

| Commande | Rôle |
|----------|------|
| `/markdown <fichier>` | Convertit un document (docx, pdf, pptx, xlsx, html) en note markdown |
| `/connect-mcp` | Installe un MCP (Firecrawl, Playwright, etc.) sur ta config |

---

## La doctrine

La posture relationnelle attendue entre toi et ton partenaire IA est décrite dans le fichier [`AGENTS.md`](AGENTS.md) à la racine du coffre. Lis-le en entier avant ta première session.

Les principes-clés :
- **Anti-flatterie** — ton partenaire IA ne te complaît pas, il te répond juste
- **Contradicteur** — il signale ce qui te contredit, ce qui te résiste
- **Garde-fous anti-enfermement** — il t'alerte quand tu enchaînes des thèses sans les nuancer
- **Tutoiement institué** — il ne te quitte pas dans le tutoiement, même en contexte formel
- **Silence > invention** — mieux vaut qu'il dise « je ne sais pas » que d'inventer

---

## Historique des versions

Voir [`CHANGELOG.md`](CHANGELOG.md) pour l'ensemble des évolutions du coffre-template.

Actuellement : **v1.0.0** (17 août 2026) — première version distribuable.

Le coffre évoluera au fil des retours des bateleurs. Pour récupérer une version plus récente, il te suffira de `git pull` depuis ton coffre — les fichiers de doctrine seront mis à jour, tes notes personnelles restent intactes.

---

## Support

Si tu bloques, si tu doutes, si une question émerge — écris à Rodrigue directement.

Le parcours PartenarIA n'est pas un logiciel avec un ticket d'assistance. C'est un cheminement accompagné.

---

## Licence

Ce coffre est distribué sous licence **CC BY-NC-SA 4.0** (voir [`LICENSE`](LICENSE)). Tu peux l'utiliser, l'adapter, le partager — sans usage commercial et en conservant les mêmes conditions.

Le contenu que tu produis à l'intérieur du coffre (tes notes, ton introspection, ton journal) t'appartient intégralement.
