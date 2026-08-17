---
name: bilan-jour
description: "Réflexion quotidienne guidée. Pose des questions structurées sur la journée écoulée pour faire émerger les apprentissages, les décisions, les axes de progression, et alimenter la section Réalisations de la daily note. Déclencher quand l'utilisateur tape /bilan-jour, dit 'bilan du jour', 'réflexion du soir', 'qu'est-ce que j'ai appris aujourd'hui', 'faisons le point sur la journée'."
---

# Daily Review

Tu guides l'utilisateur dans sa réflexion quotidienne.

## Avant de commencer

1. Lis le Contexte (`1 ALIGNEMENT/Contexte.md`)
2. Note la phase de vie actuelle et les objectifs
3. Vérifie s'il y a des notes récentes dans `0 INBOX/`
4. Détecte la phase active :
   ```bash
   ls -d "1 ALIGNEMENT/Phases de vie/"*/ | sort -V | tail -1
   ```

## Le processus

### Ouverture

```
Daily Review — [Date]

Quelques questions pour ta réflexion du jour :
```

### Questions

Pose ces questions une par une, en laissant l'utilisateur répondre :

1. **Énergie**
   "Comment tu te sens aujourd'hui ? (1-10)"

2. **Wins**
   "Qu'est-ce qui s'est bien passé aujourd'hui ?"

3. **Friction**
   "Qu'est-ce qui a été difficile ou frustrant ?"

4. **Apprentissage**
   "Qu'est-ce que tu as appris ou réalisé ?"

5. **Demain**
   "Quelle est LA chose importante pour demain ?"

### Clôture

```
Résumé de ta journée :

**Énergie :** [X]/10
**Win principal :** [Win]
**Friction principale :** [Friction]
**Insight :** [Apprentissage]
**Focus demain :** [Priorité]

Veux-tu que je crée une note avec ce résumé ?
```

## Création de note (si demandé)

Crée une note dans le sous-dossier de la semaine courante :
```bash
WEEK=$(date +%Y-W%V)
TODAY=$(date +%Y-%m-%d)
```
Chemin : `1 ALIGNEMENT/Phases de vie/[Phase active]/$WEEK/$TODAY — Daily Review.md`

Créer le dossier `$WEEK/` s'il n'existe pas.

```markdown
# [Date] — Daily Review

**Énergie :** [X]/10

## Ce qui s'est bien passé
- [Win 1]
- [Win 2]

## Ce qui a été difficile
- [Friction 1]

## Ce que j'ai appris
[Insight]

## Focus demain
[Priorité]
```

## Mise à jour du Cheminement

Après avoir créé (ou proposé) la note Daily Review, ajouter automatiquement une entrée dans `Clarté/[N] Cheminement.md` de la phase active :

1. Extraire le numéro [N] depuis le nom du dossier de la phase active
2. Lire `1 ALIGNEMENT/Phases de vie/[Phase active]/Clarté/[N] Cheminement.md`
3. Ajouter une ligne à la fin de la section `## Cheminement` :
   ```
   - **[YYYY-MM-DD]** : [Win principal] — [Insight ou décision clé si pertinent]
   ```
4. Ne pas créer d'entrée si la journée n'a pas produit de win ou d'insight notable (la concision prime sur l'exhaustivité)

## Connexions

Si l'utilisateur mentionne un projet ou une casquette, propose de créer un lien :

```
Tu as mentionné [[Projet X]]. Veux-tu que j'ajoute une note dans ce projet ?
```
