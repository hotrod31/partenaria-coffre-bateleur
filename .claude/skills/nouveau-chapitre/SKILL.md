---
name: nouveau-chapitre
description: "Clôturer le chapitre actuel et en ouvrir un nouveau (cycle long, 6-12 mois). Réalise le bilan du chapitre précédent, définit l'intention, le triple ancrage, les objectifs macro et les engagements personnels du nouveau chapitre. Déclencher quand l'utilisateur tape /nouveau-chapitre, dit 'nouveau chapitre', 'nouvelle année de vie', 'grande bascule', 'nouveau cycle long'."
---

# Nouveau Chapitre

Transition vers un nouveau chapitre de vie.

**Concept :** un chapitre est un cycle long (plusieurs mois) qui donne la vision stratégique. Il se décline en phases de vie courtes (2-12 semaines) dans le coffre.

## Argument

$ARGUMENTS = Nom du nouveau chapitre (ex: "2027 - Fonder ma pratique du coaching")

## Process

### Étape 1 : Identifier le chapitre actuel

Scanne le dossier `1 ALIGNEMENT/Chapitres/` pour trouver le chapitre avec `status: active` dans son frontmatter.

Si aucun chapitre actif n'est trouvé, c'est le tout premier — passer directement à l'étape 3.

### Étape 2 : Clôturer le chapitre actuel

**Lis le chapitre actuel** pour comprendre les intentions et objectifs initiaux.

**Pose des questions pour le bilan :**

```
Avant d'ouvrir le nouveau chapitre, faisons le bilan de "[Nom chapitre actuel]".

1. Comment résumerais-tu ce chapitre en quelques phrases ?
2. Quels sont les accomplissements majeurs ?
3. Quelles leçons structurantes en tires-tu ?
4. Où en es-tu sur les objectifs macro initiaux ?
5. Qu'est-ce qui a changé dans ta vision ou ta stratégie ?
6. Qu'est-ce qui se reporte dans le nouveau chapitre ?
```

**Ajoute une section "Bilan" à la fin du chapitre actuel** avec les réponses.

**Marque le chapitre comme terminé :** Change `status: active` en `status: completed` dans le frontmatter.

### Étape 3 : Créer le nouveau chapitre

**Crée le fichier** `1 ALIGNEMENT/Chapitres/[Nom].md`

**Pose des questions pour définir le chapitre :**

```
Définissons ton nouveau chapitre "[Nom]".

1. Quelle est la période estimée de ce chapitre ? (début → fin, plusieurs mois)
2. Quelle est ton intention stratégique pour ce chapitre ?
3. Dans quel scénario ou stratégie s'inscrit-il ?
4. Quel est le triple ancrage (si applicable) — opérationnel, créatif, systémique ?
5. Quels sont tes objectifs macro du chapitre ?
6. Quels engagements personnels veux-tu poser pour la période ?
```

**Structure du chapitre** (frontmatter + sections) :

```markdown
---
status: active
type: chapitre
periode: [Période estimée]
---

# [Nom du chapitre]

**Période :** [Date début] → [Date fin] ([X] mois)
**Statut :** Actif

---

## Intention du chapitre

[Intention stratégique long terme]

---

## Triple ancrage

1. **Opérationnel** — [...]
2. **Créatif** — [...]
3. **Systémique** — [...]

---

## Objectifs macro du chapitre

[Objectifs majeurs regroupés par thème]

---

## Engagements personnels

[Engagements perso de la période — voyages, santé, famille, finances]

---

## Phases de vie du chapitre

Ce chapitre se décline en phases courtes (2-12 semaines) dans le coffre du coffre :

- *Les phases seront créées au fur et à mesure via `/nouvelle-phase-vie`*

---

## Point d'étape

*À remplir au fil du chapitre — vision bottom-up, les jalons émergent de l'exécution des phases courtes.*
```

### Étape 4 : Mettre à jour le Contexte du coffre

Dans `1 ALIGNEMENT/Contexte.md`, mets à jour la section "Chapitre actif" avec :
- Le nom du nouveau chapitre
- La période
- L'intention principale
- Les 2-3 ancrages majeurs

### Étape 5 : Mettre à jour le CLAUDE.md du vault

Dans `CLAUDE.md` (racine du coffre), mets à jour la section "Chapitre actif" si elle existe avec les mêmes informations.

### Étape 6 : Proposer de lancer `/nouvelle-phase-vie`

Un nouveau chapitre appelle généralement une première phase de cadrage. Propose à l'utilisateur de lancer `/nouvelle-phase-vie` pour définir la première phase courte.

### Étape 7 : Confirmation

```
Chapitre "[Ancien nom]" clôturé (status: completed).
Chapitre "[Nouveau nom]" créé et actif.

Fichiers créés/modifiés :
- 1 ALIGNEMENT/Chapitres/[Ancien nom].md (status: completed + bilan)
- 1 ALIGNEMENT/Chapitres/[Nouveau nom].md (nouveau)
- 1 ALIGNEMENT/Contexte.md (section Chapitre actif)
- CLAUDE.md (si pertinent)

Pense à lancer `/nouvelle-phase-vie` pour définir la première phase courte du nouveau chapitre.
```

## Notes

- Un chapitre dure plusieurs mois (typiquement 6 à 12 mois, mais flexible)
- Les objectifs du chapitre sont macro — les livrables concrets sont portés par les phases courtes
- Approche bottom-up : les jalons émergent de l'exécution des phases, pas fixés à l'avance dans le chapitre
- Un seul chapitre peut être actif à la fois
- Toujours demander confirmation avant de créer/modifier les fichiers
