---
name: initialisation
description: Déploie le squelette du coffre PartenarIA à partir du fichier d'introspection intime du bateleur. Prend le chemin d'un fichier en argument (`.md`, `.txt`, `.pdf`, `.docx`). Lit la matière libre-form guidée par les 7 sections du guide d'introspection, extrait sémantiquement les éléments et génère automatiquement Contexte.md, Préférences.md, premier chapitre, première phase de vie, première semaine et première daily. Configure aussi Obsidian pour pointer vers la nouvelle phase. Déclencher quand l'utilisateur tape /initialisation <chemin>, dit « initialise mon coffre », « pose le squelette », « déploie mon coffre bateleur ».
---

# /initialisation — Déploiement du coffre Bateleur

## Rôle

Tu déploies le squelette du coffre PartenarIA d'un bateleur qui vient de franchir le seuil du Fou. Le bateleur t'a fourni le chemin d'un fichier d'introspection intime (rédigé selon le guide `PartenarIA — Ton introspection`, 7 sections/17 questions, format libre 5000-10000 mots).

Ton geste est un **rite d'initiation technique** : tu poses les fondations sur lesquelles le bateleur va construire sa relation avec toi. Sois précis, sobre, respectueux.

## Doctrine de confidentialité

**Le contenu de la note d'introspection est confidentiel.** Il passe par toi pendant l'extraction (flux technique automatisé) mais **ne doit jamais être révélé dans le rapport final ni dans aucune trace visible** :

- Ne cite jamais de valeurs extraites dans les messages user
- Ne crée aucun fichier de log intermédiaire
- Le rapport final est **strictement factuel** (liste des fichiers créés, pas leur contenu)
- Le bateleur doit pouvoir partager ton rapport final en visio sans rien révéler de son intime

## Arguments

- **Chemin du fichier d'introspection** (obligatoire) — absolu ou relatif à la racine du coffre
- Formats acceptés : `.md`, `.txt`, `.pdf`, `.docx`

Si aucun argument n'est fourni : demander le chemin au bateleur, une seule fois, avec un message clair.

## Flux d'exécution (6 étapes)

### Étape 1 — Validation de l'entrée

1. Vérifier que le fichier existe
2. Vérifier que l'extension est supportée (`.md`, `.txt`, `.pdf`, `.docx`)
3. Si extension non supportée : arrêter avec message clair
4. Si fichier introuvable : arrêter avec message clair

### Étape 2 — Lecture (et conversion si nécessaire)

- **`.md` / `.txt`** : lecture directe avec le tool Read
- **`.pdf`** : lecture native via le tool Read (Claude Code gère les PDF)
- **`.docx`** : conversion via Bash `markitdown "<chemin>"` (nécessite `pip install markitdown` — cf. README du coffre) puis lecture du markdown produit

**Compter les mots du contenu extrait.** Si moins de 500 mots :

> Ton fichier d'introspection contient environ N mots. Le guide `PartenarIA — Ton introspection` en recommande 5000-10000 pour que la matière soit suffisante. L'initialisation va se poursuivre, mais plusieurs sections de ton Contexte.md contiendront des placeholders `[à compléter]` que tu pourras remplir plus tard.

L'initialisation continue quand même — le bateleur assume.

### Étape 3 — Extraction sémantique

Analyse le contenu pour identifier les éléments correspondant aux **7 sections du guide** :

| Section guide | Questions | Ce que tu cherches |
|---|---|---|
| S1 Ancrage et provenance | Q1-Q2 | Fil rouge du parcours (intime, pas CV), 2-3 expériences structurantes |
| S2 Rupture consommée | Q3-Q4 | Évidences du milieu d'origine rompues, geste concret ou rupture intérieure |
| S3 Étoile du Nord | Q5-Q6 | Vision profonde du monde/vie/sens, voix propre à porter |
| S4 Blessure et problème du monde | Q7-Q8 | Problème du monde touchant profondément, blessure/épreuve qui a rendu sensible |
| S5 Urgence et action | Q9-Q11 | Ce qui rend la démarche urgente maintenant, contribution envisagée, croisée des chemins |
| S6 Discipline et itération | Q12-Q14 | Disciplines installées (méditation, sport, journaling…), capacité à recommencer, réception de la critique |
| S7 Attente et engagement | Q15-Q17 | Attentes précises envers PartenarIA, chef-d'œuvre incarné imaginé, empêchements possibles |
| MBTI (optionnel) | fin du fichier | Type + traits reconnus + traits rejetés |

**Règle stricte** : si une section n'est pas traitée dans le fichier, tu insères un placeholder `[à compléter — Q_X du guide d'introspection non renseignée]` dans la section correspondante du fichier généré. Tu n'inventes rien.

### Étape 4 — Micro-interaction (unique question méta)

Pose au bateleur une **seule question** :

> Comment veux-tu nommer cette première phase de vie ? (2-5 mots, format libre — ex : « Découverte », « Retrouver mon corps », « Cadrer mon activité ». Elle durera 2-12 semaines.)

Récupère la réponse. Nettoie-la (retire les caractères problématiques pour un nom de dossier). Note-la comme `<NOM_PHASE>`.

Récupère aussi la **date du jour** et la **semaine ISO courante** via Bash :

```bash
date +%Y-%m-%d       # ex: 2026-08-17
date +%Y-W%V         # ex: 2026-W34
date +%Y-%m          # ex: 2026-08
```

Note les valeurs comme `<TODAY>`, `<WEEK>`, `<YEAR_MONTH>`.

### Étape 5 — Génération des 7 fichiers cibles

**Règle d'idempotence** : avant chaque Write, vérifier si le fichier existe déjà. Si oui, arrêter le flux et signaler au bateleur : « Le fichier X existe déjà. Ton coffre semble déjà initialisé. Je m'arrête pour ne rien écraser. »

Génère dans cet ordre :

**a) `1 ALIGNEMENT/Contexte.md`** — 6 sections alignées sur le guide :

```markdown
# Contexte — [Prénom ou "Bateleur"]

## Moi
[Identité, provenance, fil rouge du parcours intime, expériences structurantes — extrait de S1]

## Ma Vision
[Vision du monde et étoile du Nord, voix propre à porter dans le monde — extrait de S3]

## Mes Ruptures
[Évidences du milieu d'origine rompues, geste concret ou rupture intérieure — extrait de S2]

## Ma Blessure et le problème du monde
[Problème du monde qui te touche, blessure/épreuve qui t'y a rendu sensible — extrait de S4]

## Ma Discipline
[Disciplines déjà installées, capacité d'itération — extrait de S6]

## Mes Attentes PartenarIA
[Ce que tu attends techniquement, relationnellement, intérieurement — extrait de S7]
```

Si `<Prénom>` n'est pas identifiable dans le fichier, utiliser `Bateleur`.

**b) `1 ALIGNEMENT/Préférences.md`** — 4 sections :

```markdown
# Préférences

## Style de communication
Tutoiement institué entre toi et moi. Accents français toujours. Direct et concis.
[Ajouter d'autres éléments extraits si présents dans l'introspection — sinon laisser tel quel]

## Réception de la critique
[Extrait de Q14 — comment tu reçois la critique quand elle vient de quelqu'un que tu respectes]

## Disciplines installées
[Extrait de Q12 — quelles routines structurent déjà ton quotidien]

## Rythme et cadre de travail
[À compléter au fil de tes premières sessions]
```

**c) `1 ALIGNEMENT/Chapitres/<YEAR_MONTH> - <intention-initiale-courte>.md`** — premier chapitre :

Le nom de fichier `<intention-initiale-courte>` est extrait de S3 (voix propre / étoile du Nord), 3-6 mots. Ex : `2026-08 - Fonder ma pratique du coaching.md`.

```markdown
---
status: active
période: [YEAR_MONTH] → [YEAR_MONTH + 6-12 mois]
---

# [YEAR_MONTH] - [Intention initiale]

## Intention stratégique
[Extrait développé de S3 — vision profonde et voix propre]

## Objectifs macro
[Extrait de S10 — contribution envisagée. Décliner en 3-5 objectifs macro si formulables, sinon placeholder]

## Contraintes
[À compléter au fil de ton cheminement]

## Engagements personnels
[À compléter au fil de ton cheminement]
```

**d) `1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/Clarté/1 Intention.md`** :

```markdown
---
status: active
chapitre: "[[YEAR_MONTH - <intention-initiale-courte>]]"
période: [TODAY] → [TODAY + 6 semaines par défaut]
---

# 1 <NOM_PHASE>

## Intention de la phase
[Extrait de S5 — urgence + contribution envisagée, formulé comme intention opérationnelle de 2-12 semaines]

## Focus principal
[À préciser lors de ta première session /hello]

## Ce que je veux voir advenir
[3-5 objectifs concrets, extraits de S10 si possible, sinon placeholder]
```

**e) `1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/Clarté/1 Cheminement.md`** :

```markdown
# 1 Cheminement — <NOM_PHASE>

Trajectoire vivante de la phase. Se peuple automatiquement via `/bilan-jour` et `/bilan-semaine`. Ne pas éditer manuellement sauf pour corriger.

---
```

**f) `1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/<WEEK>/<WEEK>.md`** — première weekly :

Utiliser le template `5 RESSOURCES/Modèles/Weekly Note.md`. Remplacer les placeholders `{{date:YYYY-[W]WW}}` par la valeur de `<WEEK>` et renseigner le frontmatter `phase` et `chapitre`.

**g) `1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/<WEEK>/<TODAY>.md`** — première daily :

Utiliser le template `5 RESSOURCES/Modèles/Daily Note.md`. Remplacer `{{date:YYYY-MM-DD}}` par `<TODAY>`.

### Étape 6 — Configuration Obsidian

Mettre à jour **3 fichiers de config** pour que les plugins periodic-notes et calendar sachent où créer les futures dailies/weeklies.

Utiliser Edit sur ces fichiers pour renseigner le chemin exact `1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>` :

**a) `.obsidian/daily-notes.json`** — remplacer `"folder": ""` par `"folder": "1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>"`

**b) `.obsidian/plugins/periodic-notes/data.json`** — remplacer `daily.folder` et `weekly.folder` (les 2 valeurs vides) par `"1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>"`

**c) `.obsidian/plugins/calendar/data.json`** — remplacer `"weeklyNoteFolder": ""` par `"weeklyNoteFolder": "1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>"`

### Étape 7 — Rapport de fin (factuel, sans révéler de contenu)

Émettre exactement ce message (adapter uniquement les chemins) :

```
✓ Coffre initialisé.

7 fichiers créés :
  • 1 ALIGNEMENT/Contexte.md
  • 1 ALIGNEMENT/Préférences.md
  • 1 ALIGNEMENT/Chapitres/<YEAR_MONTH> - <intention>.md
  • 1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/Clarté/1 Intention.md
  • 1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/Clarté/1 Cheminement.md
  • 1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/<WEEK>/<WEEK>.md
  • 1 ALIGNEMENT/Phases de vie/1 <NOM_PHASE>/<WEEK>/<TODAY>.md

3 fichiers de config Obsidian mis à jour :
  • .obsidian/daily-notes.json
  • .obsidian/plugins/periodic-notes/data.json
  • .obsidian/plugins/calendar/data.json

Ton coffre est prêt.

Prochaine étape : lance /hello quand tu veux commencer ta première session.
```

**Aucune autre information sortie**. Pas d'extrait, pas de commentaire, pas de résumé de ton introspection.

## Règles de conception (à respecter absolument)

1. **Silence sur le contenu** — ne cite jamais de valeurs extraites dans ce que tu affiches à l'utilisateur
2. **Une seule question au bateleur** — le nom de sa première phase de vie, rien d'autre
3. **Aucune invention** — si une section du guide n'est pas traitée, placeholder `[à compléter — Q_X ...]`
4. **Idempotence stricte** — si un fichier cible existe déjà, arrêter net et signaler, jamais écraser
5. **Dates système** — toujours via commande Bash `date`, jamais inférer
6. **Nom de phase** — reprendre exactement ce que le bateleur a saisi (nettoyage minimal pour compatibilité dossier)
7. **Aucun log intermédiaire** — n'écrire aucun fichier autre que les 7 cibles + les 3 configs Obsidian
