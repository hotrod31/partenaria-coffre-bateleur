---
name: angles-morts
description: "Posture contradicteur outillée sur les dernières décisions prises ou les projets actifs. Identifie ce qui n'est PAS dans le corpus, les zones d'ombre, les contradictions internes, les angles non examinés. Garde-fou anti-enfermement réflexif. Déclencher quand l'utilisateur tape /angles-morts, dit 'trouve mes angles morts', 'ce que je ne vois pas', 'zones d'ombre', 'contradictions internes'."
---

# /angles-morts — Posture contradicteur outillée

Active la **posture contradicteur exigeante** (doctrine PartenarIA, cf. `AGENTS.md`) outillée par une lecture profonde des notes du coffre. Identifie ce qui **n'est pas** dans le corpus mais devrait y être, les **contradictions internes** entre décisions, les **zones d'ombre** non examinées, et les angles ratés par effet de tunnel.

C'est le garde-fou contre l'enfermement réflexif quand on construit avec soi-même.

## Usage

```
/angles-morts <décisions|projet|période>
```

Exemples :

```
/angles-morts 3 dernières décisions
/angles-morts Nom du projet actif
/angles-morts décisions du chapitre actif
/angles-morts 30 derniers jours
```

## Méthodologie

### Phase 1 — Récolte large

Pour qu'il y ait de la matière à contredire, **élargir** la récolte en lisant en profondeur :

1. **Notes du projet ou décisions ciblées** :
   - Utiliser Grep pour trouver les notes du projet (`3 PROJETS/<Projet>/**/*.md`) ou du chapitre actif
   - Filtrer par période si demandée (via `find -mtime` ou date dans le frontmatter)
   - Lire les 10-15 notes les plus pertinentes

2. **Notes doctrinales et intentions** :
   - Lire l'intention du chapitre actif et de la phase active
   - Lire les décisions dans `2 CONNAISSANCES/` qui touchent au sujet

3. **Notes de contexte et backlogs** :
   - Lire `3 PROJETS/PROJETS.md` pour l'état d'ensemble, et le § 4 Todo des projets concernés
   - Lire les notes de contexte des projets concernés

4. **Lecture du AGENTS.md** :
   - Rappel des indicateurs d'enfermement réflexif (voir section « Posture relationnelle »)

### Phase 2 — Lecture ciblée

Lire 10-15 notes en profondeur. Identifier les décisions actées, les raisonnements affichés, les hypothèses non-explicitées.

### Phase 3 — Synthèse contradictrice

**Posture** : contradicteur exigeant mais documenté. Pas de critique sans fondement, mais ne pas adoucir non plus. Le but est de **protéger l'utilisateur contre lui-même** quand il pourrait tomber dans une chambre d'amplification.

Structure de la réponse :

1. **Rappel factuel du périmètre** (3 lignes) — décisions/projets/période examinés
2. **3 à 6 angles morts identifiés**, chacun sous la forme :

   ### Angle mort N° X : nom court

   - **Ce que le corpus dit** : 2-3 lignes citant `[[wikilinks]]`
   - **Ce qu'il ne dit pas (ou pas assez)** : la zone d'ombre, l'argument absent, la voix manquante
   - **Pourquoi c'est un angle mort** : signal d'alerte (effet de tunnel, biais de confirmation, accommodation, enfermement)
   - **Question à se poser** : 1 question précise et exigeante adressée à l'utilisateur

3. **Contradictions internes** entre décisions/notes — quand deux raisonnements documentés dans le corpus sont en tension non résolue. Citer les 2 sources et nommer la tension.
4. **Indicateurs d'enfermement à surveiller** — si le corpus montre des signes d'enfermement (3 thèses non nuancées de suite, refus de contradiction consécutive, accord trop rapide sans examen), les nommer explicitement.

**Règles non négociables** :
- Pas de complaisance : si tout est aligné, le dire et noter que c'est suspect (un sujet où on n'a aucun angle mort = on n'a pas vraiment regardé)
- Citer `[[wikilinks]]` pour chaque assertion sur le corpus
- Ne pas inventer d'angles morts pour faire nombre — minimum 3 si pertinents, sinon en signaler moins
- Distinguer angle mort cognitif (l'utilisateur ne le voit pas) de zone d'ombre factuelle (corpus ne le porte pas)

## Réponse à la vraie question source

*« Quels sont les angles morts que tu ne vois pas sur les trois dernières décisions que tu as prises ou les trois derniers projets que tu as pris ? »*

Cette commande est conçue exactement pour cette question. C'est la commande la plus exigeante de l'arsenal — elle mobilise la doctrine relationnelle anti-flatterie et la posture contradictrice.

## Commande sœur

`/contradicteur` — bascule de posture sans matière du corpus (posture pure). `/angles-morts` est `/contradicteur` outillé par le corpus.
