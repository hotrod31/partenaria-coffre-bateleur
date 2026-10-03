---
name: fin
description: "Clôture d'une session terminale en cours de journée : log + propagation contextes + création note détaillée si pertinent. Ruissellement micro, distinct du bilan jour /dodo. Détecte automatiquement le runtime (Claude Code, OpenCode, ou IA externe) pour tagger correctement le log dans la daily note."
---

# Clôture de session terminale (mutualisé Claude Code / OpenCode)

Clôture **une session terminale** (terminée parce que l'idée/tâche est close), pas la journée entière. Conçue pour le mode de travail en sessions parallèles : 1 session par idée, N sessions par jour.

Skill mutualisé : fonctionne dans **Claude Code** et **OpenCode** (et IA externe en fallback). Le runtime est détecté automatiquement et étiqueté dans le log de la daily note.

## Quand utiliser ce skill

- À la fin de **chaque session terminale** quand l'idée/tâche est close et que tu vas fermer le terminal
- **Plusieurs fois par jour** si tu travailles en sessions parallèles
- **AVANT** de fermer le terminal de cette session (sinon le contexte est perdu)

## Quand NE PAS utiliser ce skill

- **En fin de journée** : utilise `/dodo` qui fait le bilan jour + les niveaux supérieurs (sync daily→weekly, Contexte, Préférences, détection jalon)
- **Si la session n'a rien produit de notable** : pas besoin de logger un vide
- **Si la session est en cours et tu vas la reprendre** : ferme juste le terminal, tu reprendras le contexte à la réouverture

## Distinction avec `/dodo`

| Critère | `/fin` | `/dodo` |
|---|---|---|
| Cadence | N fois/jour (1 par session) | 1 fois/jour (fin de journée) |
| Niveau ruissellement | 2 (daily) + 3 (contextes projet/casquette) | 4 (Contexte) + 5 (Préférences) + 2bis (sync weekly) + 3bis (jalon) + bilan introspectif |
| Bilan introspectif | Non | Oui (1-2 questions) |
| Détection sessions déjà closes | Non applicable | Oui — skip les niveaux 2-3 déjà faits par `/fin` |

## Process

### Étape 0 : Détection du runtime

**Toujours** exécuter en premier pour étiqueter correctement le log :

```bash
if [ "$CLAUDECODE" = "1" ]; then
  RUNTIME="Claude Code"
elif [ "$OPENCODE" = "1" ]; then
  RUNTIME="OpenCode"
else
  RUNTIME="IA externe"
fi
echo "Runtime détecté : $RUNTIME"
```

Stocker la valeur de `$RUNTIME` pour usage dans les Étapes 5 et 7.

### Étape 1 : Analyse rapide de la conversation

Relis la conversation de la session et identifie :

**A. Actions de la session** :
- Ce qui a été accompli (1-3 actions concrètes)
- Fichiers créés ou modifiés (chemins absolus)
- Prochaines étapes identifiées mais non réalisées

**B. 5 extractions simplifiées** :

| Type | Définition |
|---|---|
| **Décisions** | Choix actés qui affectent process/organisation |
| **Préférences** | Feedback IA reçu pendant la session |
| **Faits** | Informations factuelles nouvelles |
| **Contradictions** | Incohérences vault détectées et résolues |
| **Ressources** | Liens, outils, concepts à documenter |

**Règle de simplification (vs `/dodo`)** : mentionne seulement les extractions qui ont un contenu réel. **Pas de « aucune » obligatoire pour les vides** — saute l'item simplement. Si la session est purement technique sans aucune extraction notable, ne pas afficher la section Extractions du tout.

### Étape 2 : Détection technicité réutilisable

Si la session a porté sur une **procédure technique** (debug, fix, install, configuration, refactor, méthode), arbitre **AVANT** de logger :

**Question à se poser** : cette technicité est-elle :
- **Spécifique à un projet ponctuel** → ira dans la note de contexte projet
- **Réutilisable dans plusieurs projets / contextes futurs** → mérite une note dédiée

Présente à l'utilisateur :

```
La session a porté sur une technicité.

Résumé : [3-5 lignes synthétisant le pattern / la procédure]

Veux-tu :
a) Ajouter une trace dans la note de contexte du projet [[Projet X]] (section Historique ou Expérience)
b) Créer une note procédure réutilisable dans `5 RESSOURCES/Processus/[Stack ou domaine].md`
c) Capitaliser comme pattern transverse dans `5 RESSOURCES/Outils/Pièges et patterns techniques.md` (le créer s'il n'existe pas encore — un coffre neuf ne le contient pas)
d) Rien créer en plus, garder seulement le log session

Choix ?
```

Si choix a/b/c : créer la note ou faire la mise à jour. Récupérer le wikilink pour le log session (Étape 5).

Si choix d : passer à l'Étape 3.

### Étape 3 : Détection contenu structuré (Option C — toujours validation)

Si la session a produit du **contenu structuré** (analyse, brainstorming, décision argumentée, réflexion développée, arbitrage long), présente un brouillon de note à l'utilisateur :

```
Cette session a produit du contenu structuré.

Brouillon de note proposé :
- Titre : [Titre suggéré]
- Type : [bilan / réflexion structurée / décision / analyse comparative / arbitrage / ...]
- Extrait (3-5 lignes) : [teaser du contenu]
- Emplacement suggéré : [chemin proposé selon la nature]

Veux-tu :
- Oui, crée à l'emplacement suggéré
- Oui, mais ailleurs : [tu précises]
- Non, garde seulement dans le log session
```

Si validation positive : créer la note + récupérer le wikilink pour le log session (Étape 5).

Si refus : pas de note, le contenu reste capturé dans le log session.

### Étape 4 : Détection phase active

```bash
PHASE_DIR=$(ls -d "1 ALIGNEMENT/Phases de vie/"*/ 2>/dev/null | awk -F'/' '{d=$(NF-1); n=d+0; print n"	"$0}' | sort -n | tail -1 | cut -f2-)
WEEK=$(date +%Y-W%V)
TODAY=$(date +%Y-%m-%d)
HHMM=$(date +%H:%M)
```

Chemin daily : `${PHASE_DIR}${WEEK}/${TODAY}.md`

Si la note n'existe pas, la créer à partir du template `5 RESSOURCES/Modèles/Daily Note.md`. Créer le dossier `${WEEK}/` s'il n'existe pas.

### Étape 5 : Log dans daily note (Option A — section par session)

**Append** cette section à la fin de la daily (ne pas remplacer les sections existantes, ne pas toucher au reste de la note). Remplacer `$RUNTIME` par la valeur détectée à l'Étape 0 (`Claude Code`, `OpenCode`, ou `IA externe`) :

```markdown
---

## Logs IA $RUNTIME / Session [HH:MM]

**Accompli :**
- [Action 1]
- [Action 2]

**Extractions :** (uniquement les types non vides)
- Décisions : [contenu]
- Préférences : [contenu]
- Faits : [contenu]
- Contradictions : [contenu]
- Ressources : [contenu]

**Fichiers modifiés :**
- `[chemin/fichier1.md]`
- `[chemin/fichier2.md]`

**Note détaillée créée :** [[wikilink]] (si Étape 3 a produit une note)

**Procédure / pattern capitalisé :** [[wikilink]] (si Étape 2 a produit une note)

**Prochaines étapes :**
- [ ] [TODO 1]
- [ ] [TODO 2]
```

**Format** : si une catégorie est vide (Extractions, Fichiers modifiés, Notes créées, Prochaines étapes), **ne pas l'afficher** plutôt que d'écrire « aucune ». Gain de lecture.

### Étape 6 : Mise à jour notes de contexte (NIVEAU 3, sans validation)

Pour chaque projet ou casquette concerné par la session, met à jour directement la note de contexte :

- `3 PROJETS/[Projet]/[Projet].md` → Progression, statut, roadmap, décisions actées
- `4 CASQUETTES/[Casquette]/[Casquette].md` → Nouvelles infos, responsabilités

Mises à jour factuelles uniquement (pas d'analyse, pas de bilan — ça c'est pour `/dodo`).

**Pas de validation** — cohérent avec NIVEAU 3 de `/dodo`.

#### Étape 6bis : Rituel « À chaque livrable, une ligne au fil de l'eau » (sans validation)

En complément de la mise à jour factuelle ci-dessus, alimenter **systématiquement et sans demander validation** les 3 sections chronologiques du fil rouge de la note de contexte de chaque projet ou casquette touché :

- **§ 3 Historique** — si la session a produit une avancée concrète (note structurante, procédure, présentation, décision, arbitrage, bilan-jalon, livraison technique). Format : `- **YYYY-MM-DD (contexte session)** — 🔷 Titre synthétique. Description dense 2-4 lignes avec [[wikilinks vers les livrables produits]].`
- **§ 5 Expérience** — si la session a fait émerger un apprentissage ou une compétence acquise. Format : `- **YYYY-MM-DD — Apprentissage formulé de manière actionnable.** Contexte d'émergence si utile + [[wikilink vers la note qui matérialise l'apprentissage]] + [[wikilinks vers mémoires liées]].`
- **§ 6 Idées au fil de l'eau — Idées en cours** — si la session a fait émerger une idée à mûrir ou une piste ouverte. Format : `- **YYYY-MM-DD** — Idée en 1-3 phrases + [[wikilink vers la note/section qui a fait naître l'idée]] + [[wikilinks vers ressources d'appui pour maturation]].`

**Règle absolue sur les wikilinks** : **toute entrée ajoutée dans § 3, § 5 ou § 6 doit contenir au moins un wikilink vers une note du coffre**. Objectif : permettre à l'utilisateur de rebondir depuis la note de contexte vers les notes détaillées pour approfondir à tout moment, sans avoir à chercher. Les répétitions de liens sont acceptées et souhaitées — la traçabilité prime sur la concision. Ne jamais poser une entrée « nue » sans lien de rebond.

**Portée** : tous les projets (dossier `3 PROJETS/`) et toutes les casquettes (dossier `4 CASQUETTES/`).

**Automaticité** : ne jamais demander validation à l'utilisateur. Le geste est intégré au workflow de `/fin`.

### Étape 6ter : La mention d'intériorité — une ligne, et rien de plus

Cette séance a peut-être laissé passer quelque chose qui parle de **qui tu es**, et non de ce que tu as fait. Si c'est le cas, cette étape te le rappelle — **sans te poser de question**.

**Les neuf signaux.** Liste fermée. Si aucun n'est présent, **ne rien dire du tout** et passer à l'Étape 7.

| | Signal |
|---|---|
| 1 | Tu as parlé de quelqu'un **en tant que personne**, pas en tant que rôle |
| 2 | Tu as arbitré avec une raison **non technique** — « ça ne me ressemble pas », « je ne veux pas devenir ça » |
| 3 | Tu es **revenu sur une décision passée** et tu as dit ce que tu en penses maintenant |
| 4 | Tu as exprimé une gêne, une lassitude ou un élan **sur le fond** du travail, pas sur son exécution |
| 5 | Tu as **contredit ou nuancé** quelque chose que tu as écrit ailleurs |
| 6 | Tu as formulé une **règle générale sur la vie, le métier, les gens** |
| 7 | Tu as **réfléchi sur l'intelligence artificielle** — ce qu'elle est, ce qu'elle fait aux gens |
| 8 | Tu as parlé **du coffre lui-même**, du dispositif, de la relation de travail |
| 9 | Une **réflexion spontanée** que tu as énoncée comme telle — « je me disais que… » |

**Hors périmètre, sans exception** : une leçon de méthode, une préférence d'outil, un piège technique. Ceux-là sont déjà traités aux Étapes 2 et 6 — ils vont au § 5 Expérience du conteneur, et ils coulent tout seuls.

**La forme de la mention, exactement :**

```
Au passage : « [citation, au plus près de tes mots] ».
Pour le reprendre : /ca-me-vient
```

**Trois interdits, et ils font tout le dispositif :**

- **Aucune question.** Ni « tu veux le garder ? », ni « je le note ? ». Une mention, pas une sollicitation.
- **Aucune écriture.** Cette étape n'écrit rien, nulle part. Ce qui n'est pas repris est perdu, et c'est assumé : une pensée qu'on se promet de traiter plus tard ne se traite jamais.
- **Aucune leçon.** Citer le fait, jamais ce qu'il signifie. Si la leçon est déjà formulée dans la mention, il ne reste plus qu'à l'approuver — et une conclusion sur qui tu es entre dans ton coffre sans être passée par toi.

S'il y a plusieurs faits, les citer **tous ensemble**, en une seule mention de deux ou trois lignes.

### Étape 7 : Confirmation

```
Session [HH:MM] loggée (runtime : $RUNTIME).

Extractions :
- [N1] décision(s)
- [N2] préférence(s)
- [N3] fait(s)
- [N4] contradiction(s) résolue(s)
- [N5] ressource(s)

Fichiers actualisés :
- daily du jour : section `## Logs IA $RUNTIME / Session [HH:MM]` ajoutée
- [Projet].md / [Casquette].md : mis à jour
- Note détaillée créée : [chemin si applicable]
- Procédure capitalisée : [chemin si applicable]

À la prochaine session !
```

## Règles

- **Concision** : log court, pas de blabla, structures listes
- **Wikilinks** : utiliser `[[wikilinks]]` généreusement
- **Pas de « aucune »** obligatoire — sauter les vides
- **Pas de bilan introspectif** dans ce skill (c'est `/dodo` qui le porte)
- **Toujours valider** la création de notes nouvelles (Étapes 2 et 3) — l'utilisateur choisit
- **Niveau 3 sans validation** — les contextes projet/casquette sont mis à jour directement
- **Étiquetage runtime** : le `$RUNTIME` détecté à l'Étape 0 doit apparaître textuellement dans le titre de section (`## Logs IA Claude Code` / `## Logs IA OpenCode` / `## Logs IA IA externe`)

## Convention pour `/dodo`

`/dodo` (bilan jour) détecte les sections `## Logs IA <Runtime> / Session [HH:MM]` déjà présentes dans la daily du jour (Claude Code, OpenCode, IA externe + modèle, etc.). Si présentes, `/dodo` **ne re-fait pas** les Étapes 3-4 (déjà accomplies par `/fin`) et bascule directement sur :
- Bilan introspectif rapide (1-2 questions)
- NIVEAU 2bis (sync daily → weekly)
- NIVEAU 3bis (détection jalon franchi)
- NIVEAU 4 (Contexte)
- NIVEAU 5 (Préférences)
