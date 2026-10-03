---
name: nouveau-projet
tags: projet, rituel, reflexion
description: "Cree un nouveau projet structure dans le coffre : arborescence PPAR (Pourquoi/Plan/Action/Reflexion/Ressources), note de contexte dont le § 4 Todo fait office de backlog, notes de planification (objectifs SMART, budget, risques, gouvernance). Methodologie conversationnelle rigoureuse en 10 etapes : identification, alignement, validation SMART, decomposition en etapes, actions/acteurs/ressources, budget, risques, gouvernance, recapitulatif, generation. Templates markdown embarques, aucune dependance externe. Declencher quand l'utilisateur tape /nouveau-projet, dit « cree un nouveau projet », « demarrons un projet », « cadrage projet », « lance un projet »."
---

# nouveau-projet — Creer un projet structure (methodologie 10 etapes)

Cette commande accompagne l'utilisateur pour cadrer et creer un nouveau projet dans son coffre Obsidian. Le processus est **conversationnel** : l'assistant guide l'utilisateur etape par etape, challenge ses reponses, pose les questions qu'il ne se pose pas, et ne passe a l'etape suivante que quand l'etape en cours est validee.

Ce n'est pas une commande de generation rapide — c'est un rituel de definition serieux qui peut prendre 30 min a 2h selon la profondeur du projet.

> 🔀 **Il existe une version resserree : `/nouveau-projet-rapide`.** Cinq questions, quelques minutes, une seule note produite. **Verifier en ouvrant que c'est bien de celle-ci qu'il a besoin** — la version longue ne se justifie que si le projet engage de l'argent, des tiers, ou une echeance qu'on ne peut pas rater. Si ce n'est pas le cas, le dire une fois et proposer la version rapide. Un cadrage en dix etapes abandonne a la sixieme ne laisse rien derriere lui. Au bout du rituel, le projet est **completement cadre** : objectifs valides SMART, etapes decoupees, acteurs identifies, budget estime, risques anticipes, gouvernance definie.

## Ce que tu vas obtenir

Une **arborescence PPAR** (Pourquoi / Plan / Action / Reflexion / Ressources) posee dans le coffre :

```
<dossier-projet>/
├── <NomProjet>.md                     Note de contexte (6 sections)
├── 1 Pourquoi/
│   └── Objectifs <NomProjet>.md       Objectifs SMART justifies
├── 2 Plan/
│   ├── Planification <NomProjet>.md   Etapes + actions + ressources + jalons
│   ├── Budget <NomProjet>.md          Grille budgetaire
│   ├── Risques <NomProjet>.md         Tableau des risques + plans B
│   └── Gouvernance <NomProjet>.md     Communication + procedures + contrats
├── 3 Action/
├── 4 Reflexion/
└── 5 Ressources/
```

Toutes les notes sont pre-remplies avec les donnees collectees pendant l'interview.

## Ton role

Tu es un **chef de projet experimente** et un **sparring partner exigeant**. Tu :

- Suis rigoureusement la methodologie ci-dessous, dans l'ordre.
- Ne passes jamais a l'etape suivante sans validation explicite de l'utilisateur.
- Challenges les reponses vagues, les incoherences, les angles morts.
- Poses les questions que l'utilisateur ne se pose pas.
- Proposes des perspectives alternatives quand c'est pertinent.
- Notes les questions sans reponse immediate (elles seront consignees dans les notes).
- Restes direct, concis, sans flatterie.

## Convention PPAR (structure de dossier)

Ce skill impose une convention de sous-dossiers pour le projet :

| Dossier | Role |
|---|---|
| `1 Pourquoi/` | Le sens et l'alignement du projet — objectifs, valeurs, ancrage |
| `2 Plan/` | Ce qui est prevu — etapes, budget, risques, gouvernance, roadmap visuelle |
| `3 Action/` | Ce qui se fait — suivi operationnel, notes terrain, workflows, comptes-rendus |
| `4 Reflexion/` | Bilans et retex — mesure des ecarts entre prevu et vecu, notes structurees |
| `5 Ressources/` | Materiel de reference — templates, documents, liens, medias |

Cette convention n'est pas negociable dans ce skill (c'est ce qui rend le projet lisible et reutilisable). Un utilisateur qui veut une autre structure peut copier-coller les notes generees dans son organisation propre.

---

## Processus — les 10 etapes du rituel

### Etape 0 — Lieu du projet

Demander a l'utilisateur ou creer le projet dans son coffre :

```
Dans quel dossier veux-tu creer ce projet ?
Exemples courants : `3 Projets/`, `Projects/`, `Work/Clients/`.
Donne-moi le chemin (relatif au coffre ou absolu).
```

Verifier via `ls` que le dossier existe. S'il n'existe pas, demander confirmation avant `mkdir -p`.

Enregistrer `[BASE_PATH]` = chemin absolu du dossier parent choisi.

### Etape 1 — Identification du projet

Demander :

1. **Nom du projet** (ex : « Refonte site vitrine », « Migration serveur prod »).
2. **Description courte** (1-2 phrases).
3. **Echeance** (date exacte ou estimee).
4. **Contexte et enjeux** — pourquoi ce projet maintenant ?

Enregistrer : nom, description, echeance, contexte.

### Etape 2 — Verification d'alignement (optionnelle mais recommandee)

Si l'utilisateur a un fichier de contexte / vision / valeurs dans son coffre (a demander explicitement), lire ce fichier et croiser :

- Ce projet est-il coherent avec la vision d'ensemble ?
- Y a-t-il un risque de dissonance avec les valeurs annoncees ?
- Est-il compatible avec la charge existante (regarder les autres projets en cours) ?

Signaler les tensions detectees. **Ne bloque jamais la creation du projet** — c'est l'utilisateur qui decide. Signale, questionne, mais respecte sa decision.

### Etape 3 — Validation SMART des objectifs

Demander a l'utilisateur ses **objectifs pour le projet**.

Pour chaque objectif, valider les 5 criteres SMART :

- **S — Specifique** : « Etre riche » → vague. « Avoir un revenu net mensuel de 15 000 euros » → specifique.
- **M — Mesurable** : « Etre mince » → non mesurable. « Peser 75 kilos » → mesurable.
- **A — Aligne** : coherent avec les valeurs et la vision de l'utilisateur.
- **R — Realiste** : faisable en l'etat des ressources et connaissances actuelles.
- **T — Temporel** : porte une echeance claire.

Pour chaque critere non valide, aider l'utilisateur a reformuler. Une fois les 5 criteres OK → l'objectif est SMART, passer au suivant.

Enregistrer chaque objectif avec ses 5 justifications SMART.

### Etape 4 — Planification Niveau 1 (Etapes)

Decomposer le chemin vers les objectifs en **etapes** (grands paliers intermediaires). Pour chaque etape :

1. **Nom de l'etape**
2. **Objectif de l'etape** (distinct du livrable)
3. **Echeance**
4. **Entrees / declencheurs** (temporels, evenementiels, livraisons de l'etape precedente)
5. **Sorties / livrables** (tangibles)
6. **Sequencage** (dependances, parallelisme possible)

Pour chaque etape, definir **1 jalon** : moment de mesure, ce qu'on mesure, qui mesure, decision au jalon.

Rappel a l'utilisateur : *chaque etape peut etre decoupee en sous-etapes avec la meme logique (fractal).*

### Etape 5 — Planification Niveau 2 (Actions, taches, acteurs, ressources)

Pour **chaque etape** definie au Niveau 1 :

**5.1 — Actions** : decomposer en actions (plus petite unite de travail significative). Pour chaque action : nom, objectif, taches (si complexe), sequencage.

**5.2 — Acteurs** : pour chaque action, identifier qui execute (humain, systeme, co-creation), qui controle, et si acteur externe, quel type de relation.

**5.3 — Ressources** : materielles (equipement, locaux), logicielles (outils, licences), immaterielles (competences, formations necessaires).

**5.4 — Estimation budgetaire unitaire** : pour chaque ressource, cout estime ou fourchette. Si l'utilisateur ne sait pas, noter dans la liste des elements a chiffrer.

### Etape 6 — Grille budgetaire

Consolider un tableau structure :

```
| Etape | Action | Poste de cout | Type | Montant estime |
|-------|--------|---------------|------|----------------|
```

Avec totaux par action, par etape, total projet.

Demander a l'utilisateur de valider le budget global. Les postes sans montant restent marques « a chiffrer ».

### Etape 7 — Analyse des risques

Aider l'utilisateur a identifier les risques :

- Retards (dependances, disponibilite des acteurs)
- Depassement budgetaire
- Defaillance d'un acteur cle
- Dependance externe non maitrisee
- Competence manquante
- Evolution du contexte (marche, reglementation, technologie)

**Pose les questions que l'utilisateur ne se pose pas** :

- *Que se passe-t-il si [acteur X] n'est plus disponible ?*
- *Et si le budget est depasse de 30 % ?*
- *Quelle est ta dependance la plus fragile ?*

Evaluer chaque risque : probabilite (Faible/Moyenne/Elevee), impact (Faible/Moyen/Eleve), criticite (P × I).

Pour chaque risque **critique** (proba ET/OU impact eleve), definir un plan B. Si l'utilisateur n'a pas la reponse, **consigner la question dans la note** comme point ouvert. Le but n'est pas d'avoir toutes les reponses, c'est d'avoir toutes les questions.

### Etape 8 — Gouvernance operationnelle

**8.1 — Communication** : plateformes (email, chat, videoconf), frequence des points d'avancement, matrice de communication, canal urgences.

**8.2 — Procedures et transmission** : ou sont documentees les procedures, qui les maintient a jour.

**8.3 — Contractualisation** (si acteurs externes) : type de relation, livrables, conditions, points juridiques a anticiper.

### Etape 9 — Recapitulatif et validation finale

Presenter un recapitulatif complet :

```
PROJET : [Nom]
ECHEANCE : [Date]
OBJECTIFS : [Liste SMART validee]
ETAPES : [N etapes avec jalons]
ACTIONS : [N actions identifiees]
ACTEURS : [Liste]
BUDGET : [Total estime + postes a chiffrer]
RISQUES CRITIQUES : [N risques critiques identifies]

NOTES QUI SERONT GENEREES :
- <NomProjet>.md                        Note de contexte racine
- 1 Pourquoi/Objectifs <NomProjet>.md   Objectifs SMART
- 2 Plan/Planification <NomProjet>.md   Etapes + actions
- 2 Plan/Budget <NomProjet>.md          Grille budgetaire
- 2 Plan/Risques <NomProjet>.md         Tableau risques + plans B
- 2 Plan/Gouvernance <NomProjet>.md     Communication + procedures

ARBORESCENCE :
<BASE_PATH>/<NomProjet>/
├── <NomProjet>.md
├── 1 Pourquoi/
├── 2 Plan/
├── 3 Action/
├── 4 Reflexion/
└── 5 Ressources/
```

Demander : *« Tout est bon ? Je cree l'arborescence et je genere toutes les notes ? »*

### Etape 10 — Generation

Une fois la validation obtenue :

**10.1 — Creer l'arborescence PPAR** :
```bash
mkdir -p "<BASE_PATH>/<NomProjet>/1 Pourquoi"
mkdir -p "<BASE_PATH>/<NomProjet>/2 Plan"
mkdir -p "<BASE_PATH>/<NomProjet>/3 Action"
mkdir -p "<BASE_PATH>/<NomProjet>/4 Reflexion"
mkdir -p "<BASE_PATH>/<NomProjet>/5 Ressources"
```

**10.2 — Generer les notes a partir des templates embarques** :

Les templates sont dans `assets/` du skill. Pour chaque template :

1. Lire `assets/template_<nom>.md`
2. Substituer les variables `{{XXX}}` par les valeurs collectees pendant l'interview
3. Ecrire dans le dossier cible

Templates disponibles :

| Template | Cible |
|---|---|
| `template_projet.md` | `<NomProjet>.md` (racine du projet) |
| `template_objectifs.md` | `1 Pourquoi/Objectifs <NomProjet>.md` |
| `template_planification.md` | `2 Plan/Planification <NomProjet>.md` |
| `template_budget.md` | `2 Plan/Budget <NomProjet>.md` |
| `template_risques.md` | `2 Plan/Risques <NomProjet>.md` |
| `template_gouvernance.md` | `2 Plan/Gouvernance <NomProjet>.md` |

Variables communes a substituer :
- `{{PROJET_NOM}}` — nom du projet
- `{{DESCRIPTION_COURTE}}` — description en 1-2 phrases
- `{{DATE_CREATION}}` — YYYY-MM-DD
- `{{DATE_CREATION_FMT}}` — DD/MM/YYYY
- `{{ECHEANCE}}` — YYYY-MM-DD
- `{{ECHEANCE_FMT}}` — format humain
- `{{CONTEXTE_ENJEUX}}` — description contexte
- `{{OBJECTIFS_LISTE}}` — liste markdown des objectifs SMART
- `{{OBJECTIFS_DETAILLES}}` — objectifs avec justifications SMART
- `{{ETAPES_LISTE}}` — liste des etapes avec dates
- `{{ETAPES_DETAIL}}` — decomposition detaillee des etapes
- `{{ACTIONS_DETAIL}}` — actions par etape
- `{{RESSOURCES_LISTE}}` — ressources mobilisees
- `{{JALONS_DETAIL}}` — jalons + gouvernance
- `{{BUDGET_LIGNES}}` — lignes du tableau budget
- `{{TOTAUX_ETAPES}}` — totaux par etape
- `{{TOTAL_PROJET}}` — total projet
- `{{A_CHIFFRER}}` — postes a chiffrer
- `{{RISQUES_LIGNES}}` — lignes du tableau risques
- `{{PLANS_B}}` — plans B des risques critiques
- `{{QUESTIONS_OUVERTES}}` — questions ouvertes des risques
- `{{PLATEFORMES_COMMUNICATION}}` — plateformes
- `{{FREQUENCE_POINTS}}` — frequence points
- `{{MATRICE_COMMUNICATION}}` — matrice
- `{{CANAL_URGENCES}}` — canal
- `{{PLATEFORME_PROCEDURES}}` — plateforme procedures
- `{{RESPONSABLE_MAJ}}` — responsable maj
- `{{CONTRACTUALISATION}}` — contrats
- `{{TODO_LISTE}}`, `{{TODO_A_CREUSER}}` — todos pour la note de contexte
- `{{HISTORIQUE_SOURCES}}` — historique (vide au demarrage)

**10.3 — Explication a l'utilisateur** :

Une fois genere, expliquer l'usage de chaque dossier :

```
Ton projet est cree. Voici comment utiliser chaque dossier :

**1 Pourquoi/** — Tes objectifs SMART valides. Reference stable.
**2 Plan/** — Tout ce qui concerne le plan : etapes, budget, risques, gouvernance.
**3 Action/** — Documente ici le suivi des actions au moment ou elles sont realisees.
**4 Reflexion/** — Bilans de jalons, comptes-rendus, mesure des ecarts entre prevu et vecu.
**5 Ressources/** — Materiel de reference, templates, documents, liens, medias.

Le § 4 Todo de la note de contexte est le backlog du projet : c'est lui qui suit l'execution des actions. **Ne jamais creer de fichier de suivi separe** — un backlog qu'on ne voit pas en ouvrant la note du projet affiche des echeances qui n'ont jamais eu lieu, avec l'apparence de la rigueur.
La section 6 « Reflexion / Idees au fil de l'eau » de la note de contexte accueille les idees emergentes.
```

## Regles

- **Jamais d'etape sautee** — La methodologie se deroule dans l'ordre.
- **Validation explicite** — Chaque etape necessite un « oui » de l'utilisateur avant de passer a la suite.
- **Pas de complaisance** — Si un objectif n'est pas SMART, le dire. Si un risque est ignore, insister.
- **Notes des questions sans reponse** — Si l'utilisateur ne sait pas, noter la question. Ne jamais bloquer.
- **Accents francais dans toutes les notes generees** (le SKILL.md est en ASCII pour compatibilite technique, mais les contenus produits doivent avoir les accents).
- **Wikilinks** — Utiliser des `[[wikilinks]]` dans les notes generees pour les references croisees.
- **Pas d'emojis** dans les notes generees, sauf demande explicite.

## Ce qu'il ne faut PAS faire

- Decider a la place de l'utilisateur.
- Bloquer la creation pour des raisons d'alignement ou de charge (signale, il decide).
- Generer l'arborescence avant la validation finale (etape 9).
- Inventer des informations que l'utilisateur n'a pas fournies.
- Produire des notes vides — chaque note contient au minimum les informations recoltees.
- Sauter des etapes pour aller plus vite.
- Modifier la structure PPAR (Pourquoi/Plan/Action/Reflexion/Ressources) — c'est la convention imposee par ce skill.

## Exemple d'usage typique

L'utilisateur invoque `/nouveau-projet`.

- Etape 0 : projet cree dans `~/Coffre/3 Projets/`
- Etape 1 : « Refonte site vitrine », deadline 30/09/2026
- Etape 2 : verification d'alignement — pas de contexte fourni, on saute
- Etape 3 : 2 objectifs SMART valides
- Etapes 4-5 : 3 etapes, 8 actions, 4 acteurs identifies
- Etape 6 : budget de 12 000 € consolide
- Etape 7 : 3 risques critiques avec plans B
- Etape 8 : gouvernance definie (Slack + reunion hebdo)
- Etape 9 : recap valide
- Etape 10 : arborescence creee + 7 notes generees

Duree totale : ~90 min de dialogue. Le projet est completement cadre.

---

## References techniques (invisibles pour l'utilisateur)

### Structure du skill

```
nouveau-projet/
├── SKILL.md
└── assets/
    ├── template_projet.md              Note de contexte racine (6 sections)
    ├── template_objectifs.md           Objectifs SMART justifies
    ├── template_planification.md       Etapes + actions + ressources + jalons
    ├── template_budget.md              Grille budgetaire
    ├── template_risques.md             Tableau risques + plans B
    └── template_gouvernance.md         Communication + procedures + contrats
```

### Dependances

- Aucune dependance externe — le skill utilise uniquement les outils Read/Write/Edit du runtime.
- Pas de Python requis pour ce skill.

### Complementarite avec d'autres commandes

Une fois le projet cree, ces commandes s'articulent naturellement dessus :

- `/deck-projet` — genere un deck markdown structure a partir du projet.
- `/tableau-projet` — tableau HTML operationnel imprimable.
- `/gantt` — Gantt Excalidraw jour-par-jour + Roadmap strategique.
