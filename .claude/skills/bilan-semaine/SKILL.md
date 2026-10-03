---
name: bilan-semaine
description: "Weekly review — bilan rétrospectif W-1 + GPS planning W (note nommée d'après la semaine en cours)"
---

# Weekly Review

Génère la note weekly de la **semaine en cours** (= la semaine qui vient de démarrer ou qui va démarrer), structurée en **GPS prospectif** (planning haut) + **bilan rétrospectif** de la semaine qui s'achève (bas).

> **Convention de nommage** : la weekly `YYYY-WXX.md` porte le planning de la semaine WXX en haut, et le bilan rétrospectif de la semaine W-1 en bas. L'icône « cette semaine » de Periodic Notes ouvre la weekly de la semaine en cours, qui devient le GPS opérationnel. À lancer le **dimanche soir ou lundi matin**.

## Process

### Étape 1 : Lire le contexte
Lis `1 ALIGNEMENT/Contexte.md` pour comprendre la situation de l'utilisateur.

### Étape 2 : Détecter la phase active et les semaines

```bash
PHASE_DIR=$(ls -d "1 ALIGNEMENT/Phases de vie/"*/ 2>/dev/null | awk -F'/' '{d=$(NF-1); n=d+0; print n"	"$0}' | sort -n | tail -1 | cut -f2-)
PHASE_NAME=$(basename "$PHASE_DIR")

# Si lancé dimanche soir : la semaine "en cours" est celle qui démarre lundi
# Si lancé lundi matin : la semaine en cours est aujourd'hui
TODAY=$(date +%u)  # 1=lundi, 7=dimanche
if [ "$TODAY" -ge 6 ]; then
  # Samedi ou dimanche : on prépare la semaine qui démarre lundi
  CURRENT_WEEK=$(date -v+1d -v-Mon +%Y-W%V 2>/dev/null || date -d "next monday" +%Y-W%V)
  PREV_WEEK=$(date +%Y-W%V)
else
  # Lundi à vendredi : semaine en cours
  CURRENT_WEEK=$(date +%Y-W%V)
  PREV_WEEK=$(date -v-7d +%Y-W%V 2>/dev/null || date -d "7 days ago" +%Y-W%V)
fi
echo "Phase: $PHASE_NAME"
echo "Semaine planifiée (GPS): $CURRENT_WEEK"
echo "Semaine bilanée (rétro): $PREV_WEEK"
```

**Demander confirmation à l'utilisateur** sur la semaine planifiée si on est dimanche soir (cas limite).

### Étape 3 : Lire le bilan de la semaine précédente

Lire la weekly de la semaine précédente (`$PREV_WEEK/$PREV_WEEK.md`) dans la phase active. Elle contient le planning W-1 + le bilan W-2. On extrait :
- Toutes les tâches `- [ ]` non cochées du planning W-1 → carry-forward dans le planning W
- Pas de bilan rétro à extraire ici — celui-ci sera produit fraîchement à partir du brain dump (étape 5)

Si la note précédente n'existe pas, passer cette étape et générer une note vierge.

### Étape 4 : Scanner l'activité de la semaine écoulée

```bash
find . -type f -name "*.md" -mtime -7 2>/dev/null | grep -v ".git" | head -50
```

Scanner en particulier `3 PROJETS/`, `4 CASQUETTES/`, `0 INBOX/`. Présenter un résumé rapide de ce qui a bougé.

### Étape 5 : Brain dump bilan W-1

Poser la question :
> Comment s'est passée la semaine $PREV_WEEK ? Qu'est-ce qui a avancé, qu'est-ce qui a bloqué, qu'est-ce qui a émergé ? Donne aussi un score d'énergie 0-10 par jour si tu peux.

Attendre la réponse. Extraire les éléments clés (Avancé / Bloqué / Émergent / Énergie).

### Étape 6 : Brain dump planning W

Poser la question :
> Quelles sont tes priorités pour la semaine $CURRENT_WEEK ? Que veux-tu faire avancer ?

### Étape 7 : Organiser le planning W par énergie

Classer toutes les tâches (carry-forward + nouvelles) en 3 catégories :

- **Deep Focus** : travail technique, écriture longue, apprentissage profond, réflexion stratégique
- **Créatif** : contenu, design, idéation, vidéos, présentations, brainstorming
- **Admin** : emails, compta, organisationnel, logistique, réunions, rangement

Grouper par projet/casquette à l'intérieur de chaque catégorie. Présenter la classification et attendre validation.

### Étape 8 : Priorités top 3

Demander :
> Quelles sont tes 3 priorités absolues de la semaine $CURRENT_WEEK ?

### Étape 9 : Générer la weekly note

Créer `$CURRENT_WEEK/$CURRENT_WEEK.md` dans la phase active (dans le sous-dossier de semaine) avec cette structure :

```markdown
---
type: weekly
week: $CURRENT_WEEK
phase: "[[N Nom de la phase]]"
chapitre: "[[Nom du chapitre actif]]"
---
# $CURRENT_WEEK (DD — DD mois)

> [Pitch en 1-2 phrases de la dynamique de la semaine, contexte des jalons en cours]

---

## Planning de la semaine

### Priorités (top 3)

1. [Priorité 1]
2. [Priorité 2]
3. [Priorité 3]

---

### Deep Focus

#### [[Projet ou Casquette]]
- [ ] Tâche

---

### Créatif

#### [[Projet ou Casquette]]
- [ ] Tâche

---

### Admin

#### [[Projet ou Casquette]]
- [ ] Tâche

---

### Questions ouvertes

- ...

### Prochaines échéances

- **Date** — événement

---

## Bilan de la semaine précédente — [[$PREV_WEEK]]

> Source intégrale dans [[$PREV_WEEK]]. Synthèse en rappel ci-dessous.

### Énergie $PREV_WEEK

- Lun DD : **N/10** — résumé
- ...
- **Moyenne pondérée : N,N/10** — caractérisation

### Avancé

- ...

### Bloqué / Friction

- ...

### Émergent / Structurel

- ...

---

## Liens

- [[N Intention]] — intention de la phase active
- [[N Cheminement]] — historique vivant de la phase
- [[$PREV_WEEK]] — bilan complet de la semaine précédente
- [[Nom du chapitre actif]] — chapitre stratégique
```

### Étape 10 : Mise à jour du Cheminement

Après avoir généré la weekly note, ajouter une synthèse dans `Clarté/[N] Cheminement.md` de la phase active :

1. Extraire le numéro [N] depuis le nom du dossier de la phase active
2. Lire `1 ALIGNEMENT/Phases de vie/[Phase active]/Clarté/[N] Cheminement.md`
3. Ajouter un bloc hebdomadaire à la fin de la section `## Cheminement` :
   ```
   **[$PREV_WEEK] — [DD au DD mois]**
   - [Avancée principale]
   - [Blocage ou pivot si pertinent]
   - [Décision ou insight clé]
   ```
4. S'appuyer sur la section « Bilan de la semaine précédente » de la nouvelle weekly comme source

### Étape 11 : Confirmation

Afficher un résumé :
- Semaine planifiée : $CURRENT_WEEK
- Semaine bilanée : $PREV_WEEK
- Nombre de tâches carry-forward
- Nouvelles tâches ajoutées
- Répartition Deep Focus / Créatif / Admin
- Top 3 priorités

## Output Style

- En français
- Concis, pas de blabla
- Interactif (attend les réponses)
- Pas d'emojis
- Rappel à l'utilisateur en fin de génération : **« Le GPS W$CURRENT_WEEK est en ligne. Coche les tâches au fur et à mesure de la semaine. Relance `/bilan-semaine` dimanche prochain pour basculer sur W+1. »**

## Notes

- **Convention de nommage** : la weekly porte le numéro de la semaine qu'elle PLANIFIE (= la semaine en cours). Le bilan rétrospectif de W-1 est en BAS de cette même note, pour lecture autosuffisante.
- **Pourquoi cette convention ?** L'icône « cette semaine » de Periodic Notes ouvre la weekly correspondante = directement le GPS opérationnel.
- **Cas d'usage** : à lancer dimanche soir (pour préparer la semaine du lundi) ou lundi matin (si on n'a pas eu le temps dimanche).
