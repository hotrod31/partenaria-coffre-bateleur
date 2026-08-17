# Phases de vie — Cycle court (2 à 12 semaines)

Une phase de vie est une **période thématique** d'exécution opérationnelle, à l'intérieur d'un chapitre.

## Cycle

- **Durée typique** : 2 à 12 semaines (max 3 mois)
- **Une seule phase active à la fois**
- **Nommage** : `N Nom de la phase/` (ex : `3 Structurer mon offre/`)
- Le `N` est le numéro d'ordre dans la vie, pas dans le chapitre — il s'incrémente sur toute ta trajectoire

## Structure d'une phase

```
N Nom de la phase/
├── Clarté/                     ← Notes structurelles (séparées du journaling)
│   ├── N Intention.md          ← L'intention de la phase (status: active/completed)
│   ├── N Cheminement.md        ← Trajectoire vivante (auto-alimentée par /bilan-jour)
│   └── N Bilan.md              ← Bilan de fin (à créer quand la phase se termine)
├── YYYY-WXX/                   ← Sous-dossiers de semaine
│   ├── YYYY-MM-DD.md           ← Daily notes
│   └── YYYY-WXX.md             ← Weekly note de la semaine
└── [autres notes ponctuelles]  ← Réflexions structurantes de la phase
```

## Cheminement — note vivante

Le fichier `Clarté/N Cheminement.md` se peuple automatiquement au fil des commandes :

- **`/bilan-jour`** ajoute une ligne datée
- **`/bilan-semaine`** ajoute un bloc hebdomadaire

Ne l'édite pas manuellement sauf pour corriger. C'est la trace vivante de ta phase.

## Cycle d'une phase

1. **Ouverture** — via `/nouvelle-phase-vie [Nom]`
2. **Vie de la phase** — journaling quotidien, weekly reviews, notes structurantes
3. **Clôture** — bilan écrit dans `N Bilan.md`, `status: completed` sur l'intention, ouverture de la phase suivante

## Lien avec le chapitre

Chaque phase référence son chapitre via un wikilink dans le frontmatter de `N Intention.md` :

```yaml
---
status: active
chapitre: "[[YYYY-MM - Nom du chapitre]]"
---
```

## Règle non négociable

**Tout le journaling va dans la phase active.** Pas de daily note en dehors d'une phase active.

Voir aussi : [`../Chapitres/README.md`](../Chapitres/README.md)
