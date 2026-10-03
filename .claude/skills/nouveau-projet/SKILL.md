---
name: nouveau-projet
tags: projet, rituel, réflexion
description: "Crée un nouveau projet structuré dans le coffre : arborescence PPAR (Pourquoi/Plan/Action/Réflexion/Ressources), note de contexte dont le § 4 Todo fait office de backlog, notes de planification (objectifs SMART, budget, risques, gouvernance). Méthodologie conversationnelle rigoureuse en 10 étapes : identification, alignement, validation SMART, décomposition en étapes, actions/acteurs/ressources, budget, risques, gouvernance, récapitulatif, génération. Templates markdown embarqués, aucune dependance externe. Declencher quand l'utilisateur tape /nouveau-projet, dit « créé un nouveau projet », « demarrons un projet », « cadrage projet », « lance un projet »."
---

# nouveau-projet — Créer un projet structuré (méthodologie 10 étapes)

Cette commande accompagne l'utilisateur pour cadrer et créer un nouveau projet dans son coffre Obsidian. Le processus est **conversationnel** : l'assistant guide l'utilisateur étape par étape, challenge ses réponses, pose les questions qu'il ne se pose pas, et ne passe à l'étape suivante que quand l'étape en cours est validée.

Ce n'est pas une commande de génération rapide — c'est un rituel de définition sérieux qui peut prendre 30 min à 2h selon la profondeur du projet.

> 🔀 **Il existe une version resserrée : `/nouveau-projet-rapide`.** Cinq questions, quelques minutes, une seule note produite. **Vérifier en ouvrant que c'est bien de celle-ci qu'il a besoin** — la version longue ne se justifie que si le projet engage de l'argent, des tiers, ou une échéance qu'on ne peut pas rater. Si ce n'est pas le cas, le dire une fois et proposer la version rapide. Un cadrage en dix étapes abandonne à la sixieme ne laisse rien derriere lui. Au bout du rituel, le projet est **complètement cadre** : objectifs validés SMART, étapes découpées, acteurs identifiés, budget estimé, risques anticipés, gouvernance définie.

## Ce que tu vas obtenir

Une **arborescence PPAR** (Pourquoi / Plan / Action / Réflexion / Ressources) posee dans le coffre :

```
<dossier-projet>/
├── <NomProjet>.md                     Note de contexte (6 sections)
├── 1 Pourquoi/
│   └── Objectifs <NomProjet>.md       Objectifs SMART justifiés
├── 2 Plan/
│   ├── Planification <NomProjet>.md   Étapes + actions + ressources + jalons
│   ├── Budget <NomProjet>.md          Grille budgétaire
│   ├── Risques <NomProjet>.md         Tableau des risques + plans B
│   └── Gouvernance <NomProjet>.md     Communication + procédures + contrats
├── 3 Action/
├── 4 Réflexion/
└── 5 Ressources/
```

Toutes les notes sont pre-remplies avec les données collectées pendant l'interview.

## Ton role

Tu es un **chef de projet experimente** et un **sparring partner exigeant**. Tu :

- Suis rigoureusement la méthodologie ci-dessous, dans l'ordre.
- Ne passes jamais à l'étape suivante sans validation explicite de l'utilisateur.
- Challenges les réponses vagues, les incoherences, les angles morts.
- Poses les questions que l'utilisateur ne se pose pas.
- Proposes des perspectives alternatives quand c'est pertinent.
- Notes les questions sans réponse immediate (elles seront consignees dans les notes).
- Restes direct, concis, sans flatterie.

## Convention PPAR (structure de dossier)

Ce skill impose une convention de sous-dossiers pour le projet :

| Dossier | Role |
|---|---|
| `1 Pourquoi/` | Le sens et l'alignement du projet — objectifs, valeurs, ancrage |
| `2 Plan/` | Ce qui est prevu — étapes, budget, risques, gouvernance, roadmap visuelle |
| `3 Action/` | Ce qui se fait — suivi operationnel, notes terrain, workflows, comptes-rendus |
| `4 Réflexion/` | Bilans et retex — mesure des ecarts entre prevu et vecu, notes structurees |
| `5 Ressources/` | Materiel de référence — templates, documents, liens, medias |

Cette convention n'est pas negociable dans ce skill (c'est ce qui rend le projet lisible et reutilisable). Un utilisateur qui veut une autre structure peut copier-coller les notes générées dans son organisation propre.

---

## Processus — les 10 étapes du rituel

### Étape 0 — Lieu du projet

Demander à l'utilisateur ou créer le projet dans son coffre :

```
Dans quel dossier veux-tu créer ce projet ?
Exemples courants : `3 Projets/`, `Projects/`, `Work/Clients/`.
Donne-moi le chemin (relatif au coffre ou absolu).
```

Vérifier via `ls` que le dossier existe. S'il n'existe pas, demander confirmation avant `mkdir -p`.

Enregistrer `[BASE_PATH]` = chemin absolu du dossier parent choisi.

### Étape 1 — Identification du projet

Demander :

1. **Nom du projet** (ex : « Refonte site vitrine », « Migration serveur prod »).
2. **Description courte** (1-2 phrases).
3. **Échéance** (date exacte ou estimee).
4. **Contexte et enjeux** — pourquoi ce projet maintenant ?

Enregistrer : nom, description, échéance, contexte.

### Étape 2 — Vérification d'alignement (optionnelle mais recommandee)

Si l'utilisateur a un fichier de contexte / vision / valeurs dans son coffre (a demander explicitement), lire ce fichier et croiser :

- Ce projet est-il coherent avec la vision d'ensemble ?
- Y a-t-il un risque de dissonance avec les valeurs annoncees ?
- Est-il compatible avec la charge existante (regarder les autres projets en cours) ?

Signaler les tensions detectees. **Ne bloque jamais la création du projet** — c'est l'utilisateur qui décide. Signale, questionne, mais respecte sa décision.

### Étape 3 — Validation SMART des objectifs

Demander à l'utilisateur ses **objectifs pour le projet**.

Pour chaque objectif, valider les 5 critères SMART :

- **S — Spécifique** : « Etre riche » → vague. « Avoir un revenu net mensuel de 15 000 euros » → spécifique.
- **M — Mesurable** : « Etre mince » → non mesurable. « Peser 75 kilos » → mesurable.
- **A — Aligné** : coherent avec les valeurs et la vision de l'utilisateur.
- **R — Réaliste** : faisable en l'état des ressources et connaissances actuelles.
- **T — Temporel** : porte une échéance claire.

Pour chaque critère non validé, aider l'utilisateur à reformuler. Une fois les 5 critères OK → l'objectif est SMART, passer au suivant.

Enregistrer chaque objectif avec ses 5 justifications SMART.

### Étape 4 — Planification Niveau 1 (Étapes)

Decomposer le chemin vers les objectifs en **étapes** (grands paliers intermediaires). Pour chaque étape :

1. **Nom de l'étape**
2. **Objectif de l'étape** (distinct du livrable)
3. **Échéance**
4. **Entrees / declencheurs** (temporels, evenementiels, livraisons de l'étape precedente)
5. **Sorties / livrables** (tangibles)
6. **Sequencage** (dépendances, parallelisme possible)

Pour chaque étape, définir **1 jalon** : moment de mesure, ce qu'on mesure, qui mesure, décision au jalon.

Rappel à l'utilisateur : *chaque étape peut être decoupee en sous-étapes avec la même logique (fractal).*

### Étape 5 — Planification Niveau 2 (Actions, tâches, acteurs, ressources)

Pour **chaque étape** définie au Niveau 1 :

**5.1 — Actions** : décomposer en actions (plus petite unite de travail significative). Pour chaque action : nom, objectif, tâches (si complexe), séquençage.

**5.2 — Acteurs** : pour chaque action, identifier qui exécute (humain, système, co-création), qui contrôle, et si acteur externe, quel type de relation.

**5.3 — Ressources** : matérielles (équipement, locaux), logicielles (outils, licences), immatérielles (compétences, formations nécessaires).

**5.4 — Estimation budgétaire unitaire** : pour chaque ressource, coût estimé ou fourchette. Si l'utilisateur ne sait pas, noter dans la liste des éléments à chiffrer.

### Étape 6 — Grille budgétaire

Consolider un tableau structure :

```
| Étape | Action | Poste de coût | Type | Montant estimé |
|-------|--------|---------------|------|----------------|
```

Avec totaux par action, par étape, total projet.

Demander à l'utilisateur de valider le budget global. Les postes sans montant restent marques « à chiffrer ».

### Étape 7 — Analyse des risques

Aider l'utilisateur a identifier les risques :

- Retards (dépendances, disponibilite des acteurs)
- Dépassement budgétaire
- Défaillance d'un acteur clé
- Dépendance externe non maîtrisée
- Compétence manquante
- Évolution du contexte (marché, réglementation, technologie)

**Pose les questions que l'utilisateur ne se pose pas** :

- *Que se passe-t-il si [acteur X] n'est plus disponible ?*
- *Et si le budget est depasse de 30 % ?*
- *Quelle est ta dependance la plus fragile ?*

Evaluer chaque risque : probabilité (Faible/Moyenne/Elevee), impact (Faible/Moyen/Eleve), criticité (P × I).

Pour chaque risque **critique** (proba ET/OU impact élevé), définir un plan B. Si l'utilisateur n'a pas la réponse, **consigner la question dans la note** comme point ouvert. Le but n'est pas d'avoir toutes les réponses, c'est d'avoir toutes les questions.

### Étape 8 — Gouvernance opérationnelle

**8.1 — Communication** : plateformes (email, chat, videoconf), fréquence des points d'avancement, matrice de communication, canal urgences.

**8.2 — Procédures et transmission** : ou sont documentees les procédures, qui les maintient à jour.

**8.3 — Contractualisation** (si acteurs externes) : type de relation, livrables, conditions, points juridiques a anticiper.

### Étape 9 — Récapitulatif et validation finale

Presenter un récapitulatif complet :

```
PROJET : [Nom]
ECHEANCE : [Date]
OBJECTIFS : [Liste SMART validée]
ETAPES : [N étapes avec jalons]
ACTIONS : [N actions identifiees]
ACTEURS : [Liste]
BUDGET : [Total estimé + postes à chiffrer]
RISQUES CRITIQUES : [N risques critiques identifiés]

NOTES QUI SERONT GÉNÉRÉES :
- <NomProjet>.md                        Note de contexte racine
- 1 Pourquoi/Objectifs <NomProjet>.md   Objectifs SMART
- 2 Plan/Planification <NomProjet>.md   Étapes + actions
- 2 Plan/Budget <NomProjet>.md          Grille budgétaire
- 2 Plan/Risques <NomProjet>.md         Tableau risques + plans B
- 2 Plan/Gouvernance <NomProjet>.md     Communication + procédures

ARBORESCENCE :
<BASE_PATH>/<NomProjet>/
├── <NomProjet>.md
├── 1 Pourquoi/
├── 2 Plan/
├── 3 Action/
├── 4 Réflexion/
└── 5 Ressources/
```

Demander : *« Tout est bon ? je crée l'arborescence et je génère toutes les notes ? »*

### Étape 10 — Génération

Une fois la validation obtenue :

**10.1 — Créer l'arborescence PPAR** :
```bash
mkdir -p "<BASE_PATH>/<NomProjet>/1 Pourquoi"
mkdir -p "<BASE_PATH>/<NomProjet>/2 Plan"
mkdir -p "<BASE_PATH>/<NomProjet>/3 Action"
mkdir -p "<BASE_PATH>/<NomProjet>/4 Réflexion"
mkdir -p "<BASE_PATH>/<NomProjet>/5 Ressources"
```

**10.2 — Générer les notes à partir des gabarits du coffre** :

Les gabarits vivent dans `5 RESSOURCES/Modèles/`, **et nulle part ailleurs**. Le skill n'embarque aucune copie : un gabarit recopie dans le skill divergerait de celui que le bateleur ouvre à la main, et c'est celui du coffre qui ferait alors autorite sans que personne le sache.

Pour chaque note à produire :

1. **Lire** le gabarit dans `5 RESSOURCES/Modèles/`
2. **Remplir** chaque section avec la matiere collectee pendant l'interview — les gabarits portent des indications entre crochets, qui se remplacent par le contenu reel
3. **Écrire** dans le dossier cible, et **retirer les blocs d'exemple non utilisés** plutôt que les laisser vides

| Gabarit | Cible |
|---|---|
| `Modèles/Projet.md` | `<NomProjet>.md` (racine du projet) |
| `Modèles/Projet — Objectifs.md` | `1 Pourquoi/Objectifs <NomProjet>.md` |
| `Modèles/Projet — Planification.md` | `2 Plan/Planification <NomProjet>.md` |
| `Modèles/Projet — Budget.md` | `2 Plan/Budget <NomProjet>.md` |
| `Modèles/Projet — Risques.md` | `2 Plan/Risques <NomProjet>.md` |
| `Modèles/Projet — Gouvernance.md` | `2 Plan/Gouvernance <NomProjet>.md` |

**Ce qui se substitue dans tous les gabarits** :
- `{{title}}` — le nom du projet
- Le frontmatter : renseigner `deadline` avec l'échéance, et `projet` avec le wikilink du projet dans les cinq notes filles
- Les indications `[entre crochets]` — les remplacer par la matiere reelle, ou supprimer la ligne si elle ne s'applique pas

⛔ **Deux gabarits ne se remplissent que s'ils ont lieu d'être** :
- **Gouvernance** — seulement si le projet implique d'autres personnes. Un projet porte seul n'a pas de gouvernance, et en produire une est du remplissage.
- **Budget** — seulement si le projet engage de l'argent. Sinon, ne pas créer la note.

Le dire à l'utilisateur plutôt que produire une note vide : *« ton projet ne mobilise ni argent ni tiers, je ne crée ni budget ni gouvernance — on les ajoutera si ca change. »*

**10.3 — Explication à l'utilisateur** :

Une fois généré, expliquer l'usage de chaque dossier :

```
Ton projet est créé. Voici comment utiliser chaque dossier :

**1 Pourquoi/** — Tes objectifs SMART validés. Référence stable.
**2 Plan/** — Tout ce qui concerne le plan : étapes, budget, risques, gouvernance.
**3 Action/** — Documente ici le suivi des actions au moment ou elles sont realisees.
**4 Réflexion/** — Bilans de jalons, comptes-rendus, mesure des ecarts entre prevu et vecu.
**5 Ressources/** — Materiel de référence, templates, documents, liens, medias.

Le § 4 Todo de la note de contexte est le backlog du projet : c'est lui qui suit l'execution des actions. **Ne jamais créer de fichier de suivi separe** — un backlog qu'on ne voit pas en ouvrant la note du projet affiche des échéances qui n'ont jamais eu lieu, avec l'apparence de la rigueur.
La section 6 « Réflexion / Idées au fil de l'eau » de la note de contexte accueille les idées emergentes.
```

## Regles

- **Jamais d'étape sautee** — La méthodologie se deroule dans l'ordre.
- **Validation explicite** — Chaque étape necessite un « oui » de l'utilisateur avant de passer à la suite.
- **Pas de complaisance** — Si un objectif n'est pas SMART, le dire. Si un risque est ignore, insister.
- **Notes des questions sans réponse** — Si l'utilisateur ne sait pas, noter la question. Ne jamais bloquer.
- **Accents francais dans toutes les notes générées** (le SKILL.md est en ASCII pour compatibilite technique, mais les contenus produits doivent avoir les accents).
- **Wikilinks** — Utiliser des `[[wikilinks]]` dans les notes générées pour les références croisees.
- **Pas d'emojis** dans les notes générées, sauf demande explicite.

## Ce qu'il ne faut PAS faire

- Decider à la place de l'utilisateur.
- Bloquer la création pour des raisons d'alignement ou de charge (signale, il decide).
- Générer l'arborescence avant la validation finale (étape 9).
- Inventer des informations que l'utilisateur n'a pas fournies.
- Produire des notes vides — chaque note contient au minimum les informations recoltees.
- Sauter des étapes pour aller plus vite.
- Modifier la structure PPAR (Pourquoi/Plan/Action/Réflexion/Ressources) — c'est la convention imposee par ce skill.

## Exemple d'usage typique

L'utilisateur invoque `/nouveau-projet`.

- Étape 0 : projet créé dans `~/Coffre/3 Projets/`
- Étape 1 : « Refonte site vitrine », deadline 30/09/2026
- Étape 2 : vérification d'alignement — pas de contexte fourni, on saute
- Étape 3 : 2 objectifs SMART validés
- Étapes 4-5 : 3 étapes, 8 actions, 4 acteurs identifiés
- Étape 6 : budget de 12 000 € consolide
- Étape 7 : 3 risques critiques avec plans B
- Étape 8 : gouvernance définie (Slack + reunion hebdo)
- Étape 9 : récapitulatif validé
- Étape 10 : arborescence creee + 7 notes générées

Duree totale : ~90 min de dialogue. Le projet est complètement cadre.

---

## Références techniques (invisibles pour l'utilisateur)

### Structure du skill

```
nouveau-projet/
└── SKILL.md
```

Aucun gabarit embarque. Les six vivent dans `5 RESSOURCES/Modèles/` :
`Projet.md`, `Projet — Objectifs.md`, `Projet — Planification.md`,
`Projet — Budget.md`, `Projet — Risques.md`, `Projet — Gouvernance.md`.

Le bateleur peut donc les ouvrir, les lire et les modifier sans entrer
dans `.claude/` — et il n'existe qu'une seule version de chacun.

### Dépendances

- Aucune dependance externe — le skill utilise uniquement les outils Read/Write/Edit du runtime.
- Pas de Python requis pour ce skill.

### Complémentarité avec d'autres commandes

**Dans le coffre, et disponibles tout de suite :**

- `/nouveau-projet-rapide` — la version resserrée, cinq questions. **À proposer si le projet n'engage ni argent ni tiers.**
- `/fin` — alimente au fil de l'eau les § 3, 4, 5 et 6 de la note de contexte, à chaque séance.
- `/clarte` — le tableau de bord de tous les projets, lu depuis leurs § 4 Todo.
- `/ca-me-vient` — si une pensée surgit pendant le cadrage et qu'elle ne concerne pas le projet.

**Pas embarquées dans le coffre, et installables depuis la bibliothèque** `ressources.partenaria.fr` :

- `/deck-projet` — un résumé exécutif du projet en markdown.
- `/tableau-projet` — un tableau HTML imprimable.
- `/gantt` et `/roadmap` — des frises temporelles.

⛔ **Ne pas les proposer tant que le bateleur ne les a pas installées.** Elles produisent des livrables de présentation, utiles quand un projet se montre à des tiers — ce qui n'est pas le cas courant, et surtout pas celui d'un premier projet.
