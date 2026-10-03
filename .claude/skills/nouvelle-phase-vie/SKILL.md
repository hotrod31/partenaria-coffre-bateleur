---
name: nouvelle-phase-vie
description: "Clôturer la phase actuelle et en ouvrir une nouvelle (2-12 semaines, max 3 mois). Réalise le bilan de la phase précédente, crée l'intention et le cheminement de la nouvelle phase, la rattache au chapitre actif, et bascule les chemins Obsidian. Déclencher quand l'utilisateur tape /nouvelle-phase-vie, dit 'nouvelle phase', 'changement de cap', 'on passe à autre chose', 'clôturer la phase'."
---

# Nouvelle Phase de Vie

Transition vers une nouvelle phase de vie avec bilan de la précédente.

**Important :** les phases de vie sont courtes (2 à 12 semaines, max 3 mois). Elles s'inscrivent dans un **chapitre** (cycle long) défini au niveau workspace dans `1 ALIGNEMENT/Chapitres/`.

## Argument

$ARGUMENTS = Nom de la nouvelle phase (ex: "Lancement business", "Transition", "Focus créatif")

## Process

### Étape 1 : Identifier la phase actuelle

Scanne le dossier `1 ALIGNEMENT/Phases de vie/` pour trouver la phase avec le numéro le plus élevé.

Structure attendue :
```
1 ALIGNEMENT/Phases de vie/
├── Phases de vie.md
└── 1 Ma première phase/
    ├── Clarté/
    │   ├── 1 Intention.md
    │   ├── 1 Cheminement.md
    │   └── 1 Bilan.md
    ├── YYYY-WXX/
    │   └── YYYY-MM-DD.md  (daily notes)
    └── YYYY-WXX.md        (weekly notes)
```

### Étape 2 : Identifier le chapitre actif

Scanne le dossier `1 ALIGNEMENT/Chapitres/` pour trouver le chapitre avec `status: active` dans son frontmatter. Récupère le nom du chapitre — il sera référencé dans le frontmatter de la nouvelle intention.

Si aucun chapitre actif n'est trouvé, proposer à l'utilisateur de lancer `/nouveau-chapitre` d'abord.

### Étape 3 : Créer le bilan de la phase actuelle

**Lis l'intention de la phase actuelle** : `1 ALIGNEMENT/Phases de vie/[Phase actuelle]/Clarté/[N] Intention.md` pour comprendre les objectifs initiaux.

**Pose des questions pour le bilan :**

```
Avant de passer à la nouvelle phase, faisons le bilan de "[Nom phase actuelle]".

1. Comment résumerais-tu cette phase en quelques phrases ?
2. Quelles leçons as-tu apprises ?
3. Quels ont été tes moments préférés ?
4. Où en es-tu sur tes objectifs ?
   - [Objectif 1 de l'intention] : ?
   - [Objectif 2 de l'intention] : ?
5. Qu'aimerais-tu améliorer pour la prochaine phase ?
```

**Crée le fichier bilan** `Clarté/[N] Bilan.md` dans le dossier de la phase actuelle avec le template `5 RESSOURCES/Modèles/Bilan Phase de vie.md`.

**Marque l'intention comme terminée :** Change `status: "active"` en `status: "completed"` dans `Clarté/[N] Intention.md`.

### Étape 4 : Créer la nouvelle phase

**Calcule le nouveau numéro :** numéro actuel + 1

**Crée les dossiers :**
- `1 ALIGNEMENT/Phases de vie/[N] [Nom]/`
- `1 ALIGNEMENT/Phases de vie/[N] [Nom]/Clarté/`

**Pose des questions pour l'intention :**

```
Maintenant, définissons ton intention pour "[Nom nouvelle phase]".

Cette phase s'inscrit dans le chapitre "[Nom chapitre actif]".

1. Quelle est la période exacte de cette phase ? (début → fin, max 3 mois)
2. Quelle est ton intention principale pour cette phase ?
3. Décris ta journée idéale pendant cette période.
4. Quels sont tes objectifs principaux (livrables ou décisions attendus) ?
5. Que fais-tu quand tu es surchargé ? dispersé ? fatigué ? dans le flow ?
```

**Vérifier la durée :** si la période dépasse 3 mois, proposer à l'utilisateur de découper la phase en plusieurs phases plus courtes.

**Crée le fichier intention** `Clarté/[N] Intention.md` avec le template `5 RESSOURCES/Modèles/Phase de vie.md`.

**Crée le fichier cheminement** `Clarté/[N] Cheminement.md` avec le template `5 RESSOURCES/Modèles/Cheminement Phase de vie.md` (remplacer "N Nom de la phase" par le nom réel de la phase).

**Frontmatter attendu pour l'intention :**
```yaml
---
status: active
chapitre: "[[Nom du chapitre actif]]"
---
```

### Étape 5 : Mettre à jour Phases de vie.md

Ajoute la nouvelle phase dans le tableau de `1 ALIGNEMENT/Phases de vie/Phases de vie.md` et mets à jour la section "Phase actuelle".

### Étape 6 : Mettre à jour Contexte

Mets à jour la section "Phase de Vie Actuelle" dans `1 ALIGNEMENT/Contexte.md` avec :
- Le nouveau nom de phase
- La nouvelle période
- Le nouveau focus
- Le chapitre dans lequel elle s'inscrit

### Étape 7 : Proposer la bascule des notes périodiques Obsidian

À ce stade, la nouvelle phase est créée et la phase précédente clôturée. Les icônes daily/weekly d'Obsidian pointent encore vers la phase précédente.

**Appeler la commande dédiée `/bascule-notes-periodiques`** qui :
1. Détecte automatiquement la phase active (qui est maintenant la nouvelle)
2. Affiche les chemins actuels et les chemins cibles
3. Demande confirmation à l'utilisateur (NON silencieux)
4. Applique la bascule si validé sur `.obsidian/daily-notes.json` (core) et `.obsidian/plugins/periodic-notes/data.json` (communautaire)

Si l'utilisateur refuse la bascule à ce stade, ce n'est pas bloquant — il pourra relancer `/bascule-notes-periodiques` plus tard.

### Étape 8 : Confirmation

```
Phase [N-1] "[Ancien nom]" clôturée.
Phase [N] "[Nouveau nom]" créée, rattachée au chapitre "[Nom chapitre actif]".

Fichiers créés/modifiés :
- 1 ALIGNEMENT/Phases de vie/[N-1] .../Clarté/[N-1] Bilan.md
- 1 ALIGNEMENT/Phases de vie/[N-1] .../Clarté/[N-1] Intention.md (status: completed)
- 1 ALIGNEMENT/Phases de vie/[N] .../Clarté/[N] Intention.md
- 1 ALIGNEMENT/Phases de vie/[N] .../Clarté/[N] Cheminement.md
- 1 ALIGNEMENT/Phases de vie/Phases de vie.md
- 1 ALIGNEMENT/Contexte.md
- [si bascule confirmée] .obsidian/daily-notes.json
- [si bascule confirmée] .obsidian/plugins/periodic-notes/data.json

⚠️ Si la bascule des notes périodiques a été appliquée : **fermer complètement Obsidian** (Cmd+Q, ou clic droit sur son icône du Dock puis « Quitter ») puis rouvrir. Cmd+R NE SUFFIT PAS — le community plugin Periodic Notes ne relit son data.json qu'au démarrage complet de l'app, sinon il continue à créer les notes dans l'ancienne phase (bug observé 2026-06-01). Vérification après restart : Paramètres → Periodic Notes → Note Folder doit afficher la nouvelle phase.
```

## Notes

- Toujours demander confirmation avant de créer les fichiers
- Le bilan peut être fait de manière interactive ou complété plus tard
- Si c'est la première phase, pas de bilan à faire
- Durée cible : 2 à 12 semaines, jamais plus de 3 mois — si besoin de plus, découper en plusieurs phases
- Une phase de vie s'inscrit toujours dans un chapitre workspace (vision long terme)
