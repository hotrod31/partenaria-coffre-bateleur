---
name: import
description: "Import batch : migrer toutes les notes de _Import/ en une fois"
---

# Import Batch — Migration rapide

Tu vas analyser toutes les notes dans `_Import/`, créer un plan d'import global, poser 2-3 questions de clarification, puis exécuter le transfert en batch.

**Objectif :** Vider `_Import/` rapidement sans validation note par note.

## Étape 1 : Analyse globale

1. **Scanne tout le dossier** `_Import/` (récursif, sous-dossiers inclus)
2. **Détecte les patterns** :
   - Dossiers thématiques (ex: "Marketing/", "Projets/", "Notes de lecture/")
   - Types de notes (ex: "TODO-*.md", "Book - *.md", dates dans les noms)
   - Taille et contenu (notes vides, très courtes < 100 chars, très longues > 5000 chars)
   - Dates de modification (anciennes > 1 an, récentes < 3 mois)

3. **Catégorise automatiquement** :
   - **3 PROJETS/** → Notes avec "projet", "TODO", "deadline", objectifs clairs, récentes
   - **4 CASQUETTES/** → Notes documentant un rôle (business, santé, création, etc.)
   - **5 RESSOURCES/** → Notes de lecture, références, documentation, templates, guides
   - **6 ARCHIVES/** → Notes obsolètes (> 1 an, projets terminés, info dépassée)
   - **0 INBOX/** → Impossible à catégoriser automatiquement (très rares, < 5%)

4. **Identifie les irrélevants** → Archive direct :
   - Notes vides ou quasi-vides (< 50 caractères)
   - Notes "test", "untitled", "brouillon"
   - Fichiers systèmes (`.md` générés automatiquement par exports)
   - Notes datant de plus de 2 ans sans contenu substantiel

## Étape 2 : Présenter le plan

```
J'ai scanné [X] notes dans _Import/.

**Plan d'import :**

→ 3 PROJETS/ ([X] notes)
  - [Liste des notes clés, max 5 exemples]

→ 4 CASQUETTES/ ([X] notes)
  - [Liste des notes clés, max 5 exemples]

→ 5 RESSOURCES/ ([X] notes)
  - [Liste des notes clés, max 5 exemples]

→ 6 ARCHIVES/ ([X] notes)
  - [Liste, dont X notes irrelevantes → archive direct]

→ 0 INBOX/ ([X] notes)
  - [Notes ambiguës à traiter manuellement plus tard]

**Durée estimée :** [X] secondes
```

## Étape 3 : Questions de clarification (2-3 max)

Pose UNIQUEMENT si nécessaire :

**Question 1 (si détection de patterns ambigus) :**
```
J'ai détecté [X] notes dans un dossier "Marketing/".
Tu veux :
a) Les mettre dans une casquette "Marketing" (rôle ongoing)
b) Les mettre en ressources (références)
c) Décider au cas par cas (je liste)
```

**Question 2 (si détection de notes anciennes mais riches) :**
```
J'ai [X] notes datant de 2020-2022 avec du contenu riche.
Tu veux :
a) Tout archiver (trop vieux)
b) Garder comme ressources (encore utile)
c) Je te montre la liste et tu décides
```

**Question 3 (si détection de doublons potentiels) :**
```
J'ai détecté des notes qui se ressemblent :
- "Idées YouTube.md" et "Idées vidéos.md"
- "Projet site.md" et "Refonte site web.md"

Tu veux :
a) Je les garde toutes séparées
b) Je les archive toutes sauf la plus récente
c) Je te montre les doublons et tu décides
```

## Étape 4 : Exécution batch

Une fois validé :

1. **Transfert massif** — Déplace toutes les notes selon le plan (pas de validation individuelle)
2. **Création des dossiers manquants** — Si une casquette n'existe pas, la créer
3. **Nettoyage** — Supprimer les dossiers vides dans `_Import/`
4. **Logs** — Créer un fichier `0 INBOX/Import Log [DATE].md` avec le détail de ce qui a été fait

## Étape 5 : Récapitulatif

```
Import terminé en [X] secondes !

**Résumé :**
- [X] notes → 3 PROJETS/
- [X] notes → 4 CASQUETTES/
- [X] notes → 5 RESSOURCES/
- [X] notes → 6 ARCHIVES/ (dont [X] irrelevantes)
- [X] notes → 0 INBOX/ (à traiter manuellement)

Le dossier _Import/ est vide.

**Log complet :** `0 INBOX/Import Log [DATE].md`
```

## Règles de classement automatique

### → 3 PROJETS/
**Critères détectables :**
- Mots-clés : "projet", "TODO", "deadline", "objectif", "livrable", "milestone"
- Structure : listes de tâches, roadmaps, dates futures
- Récent : modifié dans les 6 derniers mois
- Contexte : liés à un projet actif de l'utilisateur (check `1 ALIGNEMENT/Contexte.md`)

**Exemples :**
- "Projet refonte site.md"
- "TODO lancement produit.md"
- "Roadmap Q1 2026.md"

### → 4 CASQUETTES/
**Critères détectables :**
- Documente un rôle/domaine : Marketing, Santé, Création, Business, etc.
- N'a pas de deadline
- Documentation ongoing (process, méthodes, templates par rôle)
- Mots-clés : "guide", "process", "méthode", nom d'un rôle

**Exemples :**
- "Process création vidéo.md"
- "Marketing — Stratégie contenu.md"
- "Santé — Routine quotidienne.md"

### → 5 RESSOURCES/
**Critères détectables :**
- Notes de lecture : "Book -", "Article -", "Cours -"
- Références : guides, documentation, templates génériques
- Inspiration : idées, concepts, frameworks
- Mots-clés : "notes", "résumé", "référence", "template", "guide"

**Exemples :**
- "Book - Atomic Habits.md"
- "Notes formation marketing.md"
- "Framework OKR.md"

### → 6 ARCHIVES/
**Critères détectables (archive automatique si) :**
- Date : modifié il y a plus de 2 ans ET pas de contenu riche
- Taille : < 50 caractères (quasi-vide)
- Noms irrelevants : "test", "untitled", "brouillon", "tmp", "backup"
- Projets terminés : contient "terminé", "fini", "archivé", "abandonné"
- Obsolète : référence à des dates passées (ex: "TODO 2019")

**Exemples :**
- "test.md" (vide)
- "Projet 2019.md" (ancien)
- "Notes à supprimer.md"

### → 0 INBOX/ (exceptions)
**Seulement si impossible à catégoriser :**
- Note très courte (<100 chars) mais récente et non-vide
- Contenu ambigu sans contexte
- Nécessite décision humaine

**Rares : < 5% du total**

## Principes de décision

**1. En cas de doute : Archive**
Mieux archiver une note et la ressortir plus tard que polluer le système avec des notes inutiles.

**2. Batch over perfection**
On vise 95% de précision, pas 100%. Les 5% ambigus vont en inbox, l'utilisateur triera plus tard.

**3. Utilise le contexte utilisateur**
Lis `1 ALIGNEMENT/Contexte.md` pour savoir :
- Ses projets actifs → Notes liées = PROJETS
- Ses casquettes → Notes liées = CASQUETTES
- Sa phase de vie → Hors phase = ARCHIVES

**4. Détection de patterns**
Si tu vois un dossier "Marketing/" avec 20 notes → propose de créer la casquette "Marketing" et tout y mettre.

**5. Log tout**
Crée `0 INBOX/Import Log [DATE].md` avec la liste complète des transferts pour que l'utilisateur puisse vérifier après coup.

## Format du log

```markdown
# Import Log — [DATE] [HEURE]

## Résumé
- Total : [X] notes traitées
- Projets : [X]
- Casquettes : [X]
- Ressources : [X]
- Archives : [X]
- Inbox : [X]

## Détail par destination

### 3 PROJETS/
- `_Import/Projet site.md` → `3 PROJETS/Refonte site/Refonte site.md`
- `_Import/TODO lancement.md` → `3 PROJETS/Lancement produit/TODO.md`
...

### 4 CASQUETTES/
- `_Import/Marketing/*.md` (12 notes) → `4 CASQUETTES/Marketing/`
...

### 5 RESSOURCES/
- `_Import/Book - Atomic Habits.md` → `5 RESSOURCES/Book - Atomic Habits.md`
...

### 6 ARCHIVES/
- `_Import/test.md` → `6 ARCHIVES/test.md` (irrelevant)
- `_Import/Projet 2019.md` → `6 ARCHIVES/Projet 2019.md` (obsolète)
...

### 0 INBOX/
- `_Import/idée.md` → `0 INBOX/idée.md` (ambigu)
...

## Fichiers créés
- `4 CASQUETTES/Marketing/Marketing.md` (note de contexte générée)
- `3 PROJETS/Refonte site/Refonte site.md` (note de contexte générée)

## Remarques
[Observations, doublons détectés, suggestions pour l'utilisateur]
```
