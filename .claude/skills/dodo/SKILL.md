---
name: dodo
description: "Bilan de fin de journée : consolide les sessions du jour, sync weekly, détection jalon, mise à jour Contexte + Préférences, bilan introspectif. À lancer 1 fois/jour en fin de journée. Déclencher quand l'utilisateur tape /dodo, dit 'bilan du jour', 'fin de journée', 'on ferme', 'bonne nuit', 'à demain'."
---

# Bilan de fin de journée

Clôture **la journée** (pas une session). Différent de `/fin-session` qui clôture chaque session terminale en cours de journée.

## Coexistence avec `/fin-session`

| Critère | `/fin-session` | `/dodo` |
|---|---|---|
| Cadence | N fois/jour (1 par session terminale) | 1 fois/jour (fin de journée) |
| Niveau ruissellement | 2 (daily) + 3 (contextes projet/casquette) | 4 (Contexte) + 5 (Préférences) + 2bis (sync weekly) + 3bis (jalon) + bilan introspectif |
| Cas d'usage | À chaque fermeture de terminal en cours de journée | Une fois en fin de journée, avant `dodo` réel |

**Détection automatique** : `/dodo` regarde si la daily du jour contient déjà des sections `## Logs IA <Runtime> / Session [HH:MM]` posées par `/fin-session`. Si oui, `/dodo` consolide plutôt que de re-faire le travail. Si non, `/dodo` fonctionne en mode autonome complet (cas d'une journée à 1 seule session sans `/fin-session` intermédiaire).

**Coexistence multi-runtime** : si la daily contient des sections d'autres runtimes que Claude Code (ex. OpenCode), `/dodo` doit **les relire** lors de l'Étape 1 et de l'agrégation, pour intégrer leur contexte avant la mise à jour Contexte et Préférences. Sinon la mémoire externalisée diverge des actions réellement effectuées.

## Process

### Étape 0 : Détection des sessions déjà closes

```bash
PHASE_DIR=$(ls -d "1 ALIGNEMENT/Phases de vie/"*/ | sort -V | tail -1)
WEEK=$(date +%Y-W%V)
TODAY=$(date +%Y-%m-%d)
DAILY="${PHASE_DIR}${WEEK}/${TODAY}.md"
```

Si la daily existe, compter les sections `## Logs IA <Runtime> / Session [HH:MM]` (tous runtimes confondus + legacy sans runtime) :

```bash
SESSION_COUNT=$(grep -cE "^## Logs IA .*Session " "$DAILY" 2>/dev/null || echo 0)
```

Lister les runtimes présents pour information :

```bash
grep -oE "^## Logs IA [^/]+/" "$DAILY" 2>/dev/null | sort -u
```

Deux modes selon `$SESSION_COUNT` :

**Mode CONSOLIDATION (SESSION_COUNT >= 1)** :
- Les Étapes 3-4 (log daily + mise à jour contextes) **sont déjà faites** par `/fin-session`
- `/dodo` ne re-fait PAS ces étapes
- `/dodo` exécute : analyse globale du jour + Étape 4bis (jalon, si non détecté en cours de journée) + Étape 4ter (bilan introspectif) + Étape 5 (sync weekly) + Étape 6 (Contexte) + Étape 7 (Préférences) + Étape 8 (confirmation)
- Pour l'Étape 1, analyser la conversation **uniquement de la dernière session** (sinon doublonnage avec les `/fin-session` précédents)

**Mode AUTONOME (SESSION_COUNT = 0)** :
- Aucune session n'a été fermée formellement aujourd'hui
- `/dodo` fait TOUT le travail comme avant (Étapes 1 → 8)

Annonce à l'utilisateur lequel des 2 modes est activé :

```
Mode détecté : [CONSOLIDATION (N sessions déjà loggées par /fin-session) | AUTONOME (aucune session formellement close aujourd'hui)]
```

### Étape 1 : Analyse de la conversation et extraction structurée

### Étape 1 : Analyse de la conversation et extraction structurée

Relis la conversation et identifie **deux ensembles** :

**A. Actions de la session (factuel)** :
1. Ce qui a été accompli (fichiers créés, modifiés, actions réalisées)
2. Les contextes modifiés (projets, casquettes, phase de vie, infos personnelles)
3. Les prochaines étapes identifiées mais non réalisées

**B. Les 5 extractions structurées** :

| # | Type | Définition | Routage |
|---|---|---|---|
| 1 | **Décisions** | Choix actés qui affectent les process ou l'organisation. Ex : « On part sur NocoDB pour le CRM », « J'arrête ce projet », « On bascule l'archi en V2 » | NIVEAU 3 (note contexte projet/casquette) + NIVEAU 4 si stratégique |
| 2 | **Préférences** | Feedback utilisateur sur le comportement de l'agent. Ex : « Sois plus direct », « Ne me demande pas de valider chaque fois », « Mode propositionnel pour /bilan-jour » | NIVEAU 5 (Préférences.md) + capitalisation MEMORY.md cross-session |
| 3 | **Faits** | Informations factuelles nouvelles. Ex : « Nouveau client signé », « Le prix a changé », « Le COSTRAT s'est tenu hier » | NIVEAU 3 (note contexte projet/casquette) ou NIVEAU 4 (Contexte) |
| 4 | **Contradictions** | Incohérences entre ce qui est documenté dans le vault et ce qui a été dit. Ex : La note de projet dit « deadline mars » mais on a parlé de « deadline juin » | Résolution directe dans la note source du vault — l'info la plus récente gagne |
| 5 | **Ressources** | Liens, outils, concepts à documenter. Ex : URL article, nom d'outil, package npm, référence bibliographique | NIVEAU 3 (Ressources/ du projet) ou `5 RESSOURCES/` si transverse ou `5 RESSOURCES/Outils/Patterns techniques transverses.md` si pattern technique réutilisable |

**Règle d'or** : si une extraction est vide (rien à noter sur ce type), le mentionner explicitement (« Décisions : aucune ») plutôt que de l'omettre — force à se poser la question, évite l'omission par paresse.

### Étape 2 : Détecter la phase active

```bash
ls -d "1 ALIGNEMENT/Phases de vie/"*/ | sort -V | tail -1
```

Extraire le numéro et nom de la phase depuis le nom du dossier.

### Étape 3 : Log dans la daily note (NIVEAU 2 — OBLIGATOIRE)

> **Mode CONSOLIDATION (SESSION_COUNT >= 1)** : ne pas créer une nouvelle section `## Logs IA / Session [HH:MM]` (les sessions précédentes ont déjà été loggées par `/fin-session`). À la place, ajouter une section unique `## Bilan de fin de journée [HH:MM]` qui consolide :
> - Résumé global du jour (3-5 lignes, regroupé par projet/thème)
> - Synthèse des extractions accumulées sur toutes les sessions (lire les sections `## Logs IA / Session` précédentes pour agréger)
> - Bilan introspectif (cf. Étape 4ter)
>
> **Mode AUTONOME (SESSION_COUNT = 0)** : faire ce qui suit (logger une section `## Logs IA / Session` comme avant) — c'est la version « historique » de `/dodo`.

Trouve ou crée la daily note du jour dans la phase de vie active :
```bash
WEEK=$(date +%Y-W%V)
TODAY=$(date +%Y-%m-%d)
```
- Chemin : `1 ALIGNEMENT/Phases de vie/[Phase active]/$WEEK/$TODAY.md`
- Créer le dossier `$WEEK/` s'il n'existe pas
- Si la note n'existe pas, la créer avec le template `5 RESSOURCES/Modèles/Daily Note.md`

Ajoute à la fin de la note :

```markdown
---

## Logs IA / Session [HH:MM]

**Accompli :**
- [Action 1]
- [Action 2]
- [Action 3]

**Extractions structurées :**
- **Décisions :** [liste ou « aucune »]
- **Préférences :** [feedback IA ou « aucune »]
- **Faits :** [informations factuelles nouvelles ou « aucun »]
- **Contradictions :** [incohérences détectées et résolues ou « aucune »]
- **Ressources :** [liens, outils, concepts à retenir ou « aucune »]

**Fichiers modifiés :**
- `[chemin/fichier1.md]`
- `[chemin/fichier2.md]`

**Prochaines étapes :**
- [ ] [TODO 1]
- [ ] [TODO 2]
```

### Étape 4 : Mise à jour contextes projet/casquette (NIVEAU 3 — OBLIGATOIRE, appliqué directement sans validation)

> **Mode CONSOLIDATION (SESSION_COUNT >= 1)** : les notes de contexte projet/casquette ont déjà été mises à jour par `/fin-session` à chaque session terminale. **Skip** cette étape pour les projets qui ont eu une session `/fin-session` aujourd'hui. Faire uniquement les mises à jour qui n'ont PAS été couvertes (cas rare : oubli `/fin-session` sur une session, ou projet touché en réflexion seulement en fin de journée).
>
> **Mode AUTONOME (SESSION_COUNT = 0)** : faire toutes les mises à jour ci-dessous comme avant.

Si des projets ont été travaillés, mets à jour directement :
- `3 PROJETS/[Projet]/[Projet].md` → Progression, roadmap, status
- `3 PROJETS/PROJETS.md` → Mettre à jour la **Situation** des projets travaillés + la date `updated` du frontmatter
- `3 PROJETS/Suivi Projets.md` → Kanban global : ajouter/cocher/supprimer les tâches des projets travaillés
- `3 PROJETS/[Projet]/Suivi [Projet].md` → Kanban projet : déplacer les cartes entre colonnes (À programmer → Programmées → En cours → Accomplies), ajouter les nouvelles tâches
- `3 PROJETS/[Projet]/Suivi des livrables*.md` → Synchroniser : si des tâches ont été cochées/décochées dans les notes de livrables, refléter l'état dans le Kanban projet correspondant (et vice versa)

**Format Kanban :** frontmatter `kanban-plugin: basic`, colonnes en `## Heading`, cartes en `- [ ]` / `- [x]`, dates en `@{YYYY-MM-DD}`.

Si des casquettes ont été impactées, mets à jour directement :
- `4 CASQUETTES/[Casquette]/[Casquette].md` → Nouvelles infos, responsabilités

**Pas de validation pour ce niveau** — ces mises à jour sont factuelles et reflètent ce qui a été fait.

#### Étape 4-ter : Rituel « À chaque livrable, une ligne au fil de l'eau » (sans validation)

En complément de la mise à jour factuelle ci-dessus, alimenter **systématiquement et sans demander validation** les 3 sections chronologiques du fil rouge de la note de contexte de chaque projet ou casquette touché(e) pendant la journée :

- **§ 3 Historique** — si la journée a produit une avancée concrète (note structurante, procédure, présentation, décision, arbitrage, bilan-jalon, livraison technique). Format : `- **YYYY-MM-DD (contexte session)** — 🔷 Titre synthétique. Description dense 2-4 lignes avec [[wikilinks vers les livrables produits]].`
- **§ 5 Expérience** — si la journée a fait émerger un apprentissage ou une compétence acquise. Format : `- **YYYY-MM-DD — Apprentissage formulé de manière actionnable.** Contexte d'émergence si utile + [[wikilink vers la note qui matérialise l'apprentissage]] + [[wikilinks vers mémoires liées]].`
- **§ 6 Idées au fil de l'eau — Idées en cours** — si la journée a fait émerger une idée à mûrir ou une piste ouverte. Format : `- **YYYY-MM-DD** — Idée en 1-3 phrases + [[wikilink vers la note/section qui a fait naître l'idée]] + [[wikilinks vers ressources d'appui pour maturation]].`

**Règle absolue sur les wikilinks** : **toute entrée ajoutée dans § 3, § 5 ou § 6 doit contenir au moins un wikilink vers une note du coffre**. Objectif : permettre à l'utilisateur de rebondir depuis la note de contexte vers les notes détaillées pour approfondir à tout moment, sans avoir à chercher. Les répétitions de liens sont acceptées et souhaitées — la traçabilité prime sur la concision. Ne jamais poser une entrée « nue » sans lien de rebond.

**Portée** : tous les projets et casquettes touchés pendant la journée, sans sélectivité.

**Automaticité** : ne jamais demander validation à l'utilisateur. Le geste est intégré au workflow de `/dodo`.

**Mode CONSOLIDATION** : si `/fin-session` a déjà alimenté § 3/5/6 pour certains projets/casquettes pendant la journée, ne pas doublonner — compléter seulement ce qui n'a pas été couvert (nouvelles avancées, apprentissages, idées émergents en fin de journée uniquement).

### Étape 4bis : Détection jalon franchi (NIVEAU 3bis — avec validation)

**Objectif** : combler la zone d'ombre des projets exécutés sur plusieurs semaines sans aucune note dans `Réflexion/`. À chaque jalon franchi, capter le retour d'expérience à chaud plutôt que le perdre.

#### 4bis.1 — Détection

Identifier dans la session un signal de jalon franchi sur un projet ou une casquette :

- **Mention explicite** dans la conversation : « jalon X atteint », « jalon X acté », « jalon X franchi », « jalon X validé », « jalon X livré », « livré intégralement », « Phase X terminée »
- **Bascule de statut** dans une note de contexte ou roadmap : `status: active` → `status: completed`, `status: en cours` → `status: terminé`
- **Cochage jalon** dans une roadmap, suivi ou note de contexte : `- [ ] Jalon X` → `- [x] Jalon X`

Si aucun signal détecté, passer directement à l'étape 5. **Ne pas insister.**

#### 4bis.2 — Proposition

Si un jalon est détecté, présenter à l'utilisateur :

```
J'ai détecté un jalon franchi : [Jalon X] sur [[Projet]].

Veux-tu que je crée une note de bilan dans 3 PROJETS/[Projet]/[N Réflexion]/<date> — Bilan jalon [X].md pour capitaliser le retour d'expérience à chaud ? (o/n)
```

Trouver le bon dossier Réflexion en cherchant le sous-dossier existant qui correspond au pattern PPAR du projet (`4 Réflexion/`, `5 Réflexion/`, ou `Réflexion/`). Si le dossier n'existe pas, le créer.

#### 4bis.3 — Création (si validé)

Créer la note avec ce template léger :

```markdown
---
type: bilan-jalon
projet: "[[Projet]]"
jalon: "Jalon X — Nom du jalon"
date: YYYY-MM-DD
tags:
  - bilan-jalon
  - réflexion
---

# Bilan jalon [X] — [Nom du jalon] ([[Projet]])

## Intention initiale rappelée

[Ce qui était prévu — citer la note Pourquoi ou Plan d'origine via [[wikilinks]]. 2-4 lignes.]

## Réalité de l'exécution

[Ce qui s'est vraiment passé — chemin réel, durée, conditions, acteurs impliqués. 4-8 lignes.]

## Écarts intention / réalisation

[Différences notables entre prévu et vécu. Surprises positives. Dérives. Ce qui a été ajouté en cours. Ce qui a été abandonné.]

## Apprentissages

[Ce qu'on a appris — patterns techniques, pièges évités, décisions structurantes prises.]

## Reste à faire

[Suites directes, jalons libérés, dépendances ouvertes pour la phase suivante du projet.]

## Liens

- [[Projet]] — note de contexte
- [Note Pourquoi/Plan d'origine du jalon]
- [Mémoires capitalisées pertinentes]
```

Ne pas pré-remplir le contenu — laisser l'utilisateur compléter à son rythme. Confirmer brièvement la création (« Note créée : `[chemin]` ») et passer à l'étape 5.

#### 4bis.4 — Si refus

Si l'utilisateur dit non, ne pas insister, ne pas redemander dans la session. Passer à l'étape 4ter directement.

### Étape 4ter : Bilan introspectif du jour

**Objectif** : capter en fin de journée un mini-bilan introspectif (équivalent compact de `/bilan-jour`), pour ne pas perdre la dimension réflexive. Différent de l'extraction factuelle de l'Étape 1 — ici on parle **énergie, win, friction, focus demain**. Compense le fait que `/fin-session` a déjà absorbé le ruissellement factuel.

#### 4ter.1 — 4 questions courtes (mode propositionnel autorisé)

Pose ces 4 questions une par une, attends la réponse entre chaque :

1. **Énergie** : « Niveau d'énergie aujourd'hui (1-10) ? »
2. **Win** : « Le truc qui s'est le mieux passé ? »
3. **Friction** : « Le truc qui a coincé ? »
4. **Focus demain** : « LA chose importante pour demain ? »

**Mode propositionnel** : si l'utilisateur a déjà laissé des indices dans la conversation ou dans les sections `## Logs IA / Session` du jour, proposer directement 2-4 wins/friction/insights candidats à partir de la daily, et laisser l'utilisateur valider/nuancer/retirer.

**Ne pas insister** : si l'utilisateur ne veut pas faire ce bilan ce soir, passer directement à l'Étape 5 sans le forcer.

#### 4ter.2 — Écrire dans la daily

Append cette section à la fin de la daily du jour (en plus des logs de l'Étape 3) :

```markdown
---

## Bilan introspectif du jour

**Énergie :** [X]/10
**Win principal :** [Win]
**Friction principale :** [Friction]
**Focus demain :** [Priorité]
```

#### 4ter.3 — Mise à jour Cheminement de phase

Ajouter une ligne au `Clarté/[N] Cheminement.md` de la phase active (cohérent avec `/bilan-jour`) :

```
- **[YYYY-MM-DD]** : [Win principal] — [Insight ou décision clé si pertinent]
```

Ne pas créer d'entrée si la journée n'a pas produit de win ou d'insight notable (concision prime sur exhaustivité).

### Étape 5 : Sync daily → weekly (NIVEAU 2bis — validation rapide en bloc)

**Objectif** : faire remonter dans la weekly note (GPS de la semaine en cours) les tâches accomplies aujourd'hui dans la daily. La weekly est consultée comme tableau de bord pendant la semaine — si les coches daily ne remontent pas, la weekly devient obsolète et perd son rôle de GPS.

**Convention** : la weekly `YYYY-WXX.md` porte le planning de la semaine en cours en haut + bilan W-1 en bas. C'est cette weekly qu'on synchronise.

#### 5.1 — Lire les deux notes

```bash
WEEK=$(date +%Y-W%V)
TODAY=$(date +%Y-%m-%d)
PHASE_DIR=$(ls -d "1 ALIGNEMENT/Phases de vie/"*/ | sort -V | tail -1)
WEEKLY="${PHASE_DIR}${WEEK}/${WEEK}.md"
DAILY="${PHASE_DIR}${WEEK}/${TODAY}.md"
```

Lire `$WEEKLY` (section `## Planning de la semaine` uniquement, ignorer `## Bilan de la semaine précédente` en bas). Lire `$DAILY` (sections `## Tâches à réaliser et Focus` + `# Réalisations de la journée`).

#### 5.2 — Détecter les correspondances

Parcourir chaque tâche `- [ ]` de la section Planning de la weekly et chercher dans la daily :

1. **Match par cochage** : la même tâche (ou formulation proche) est passée en `- [x]` dans les Tâches de la daily du jour ou des jours précédents de la semaine
2. **Match par réalisation** : une section `## [[Projet]] — ...` dans Réalisations correspond à une tâche weekly du même projet, avec verbiage indiquant l'accomplissement (« ✅ », « fait », « terminé », « livré », « programmé », « envoyé », etc.)
3. **Match par mots-clés** : pour les tâches sans formulation exacte, comparer les mots-clés significatifs (nom de projet, livrable, action)

Pour chaque match, noter :
- La tâche weekly (texte complet)
- La preuve dans la daily (ligne cochée ou paragraphe de réalisation)
- Le niveau de confiance (fort / moyen / faible)

#### 5.3 — Présentation en bloc + validation rapide

Présenter à l'utilisateur :

```
Sync weekly — j'ai détecté N tâches accomplies aujourd'hui dans la daily qui correspondent à des items du planning W23 :

[1] ✅ [Tâche weekly] (confiance forte)
    Preuve : [extrait daily]

[2] ✅ [Tâche weekly] (confiance moyenne)
    Preuve : [extrait daily]

[3] ⚠ [Tâche weekly] (confiance faible — formulation différente)
    Preuve : [extrait daily]
    À cocher quand même ? (o/n)

Veux-tu que j'applique toutes les coches confiance forte+moyenne ? (o/n/items spécifiques)
```

Comportement par défaut :
- **Confiance forte** : à cocher d'office après validation globale
- **Confiance moyenne** : à cocher après validation globale (mais à mentionner explicitement)
- **Confiance faible** : item par item, demander confirmation explicite

Si aucun match détecté, signaler simplement : « Aucune remontée daily → weekly détectée aujourd'hui. »

#### 5.4 — Application des coches

Une fois validation reçue, modifier `$WEEKLY` pour passer les `- [ ]` correspondants en `- [x]`, en préservant le texte de la tâche. Ajouter optionnellement une mention de la date du jour si la coche n'est pas évidente : `- [x] **Tâche** — ✅ [DD/MM]`.

#### 5.5 — Détection des accomplissements émergents (bonus)

Si la daily contient des **réalisations qui ne correspondent PAS à des tâches existantes de la weekly** (= émergence imprévue, ex : « tableau de recueil des usages rempli » qui n'était pas anticipé en début de semaine), proposer à l'utilisateur :

```
J'ai détecté N accomplissements émergents non prévus dans la weekly :

- [[Projet]] — [Description courte]

Veux-tu les ajouter rétroactivement à la weekly (déjà cochés) pour préserver la trace ? (o/n)
```

Si oui, ajouter ces items dans la bonne section (Deep Focus / Créatif / Admin) sous le projet concerné, déjà cochés.

### Étape 6 : Mise à jour contexte global (NIVEAU 4 — avec validation)

Vérifie si des mises à jour sont nécessaires dans :
- `1 ALIGNEMENT/Contexte.md` → Nouvelles infos personnelles, changement d'objectifs
- `1 ALIGNEMENT/Phases de vie/[Active]/[N] Intention.md` → Progression sur les objectifs

Si des changements sont pertinents, montre le diff et demande validation :

```
Je propose de mettre à jour [fichier] :

- Ajouter : [contenu]
- Modifier : [ancien] → [nouveau]

OK ?
```

Si aucun changement de contexte global n'est nécessaire, ne rien proposer.

### Étape 7 : Mise à jour Préférences (NIVEAU 5 — AUTO)

Si de nouvelles préférences ou patterns ont émergé pendant la session, mets à jour `1 ALIGNEMENT/Préférences.md` directement (sans validation).

### Étape 8 : Confirmation

```
Bilan de fin de journée loggé !

Mode : [CONSOLIDATION (N sessions consolidées) | AUTONOME]

Extractions du jour :
- [N1] décisions
- [N2] préférences
- [N3] faits
- [N4] contradictions résolues
- [N5] ressources

NIVEAU 2 — Daily note : [date] mise à jour (mode CONSOLIDATION : section « Bilan de fin de journée » ajoutée + N sessions déjà loggées par /fin-session | mode AUTONOME : section « Logs IA / Session » ajoutée)
NIVEAU 3 — Contextes mis à jour : [liste des fichiers] (mode CONSOLIDATION : seulement les projets non couverts par /fin-session)
NIVEAU 3bis — Jalon Réflexion : [créée : chemin / aucun jalon détecté / refusée]
NIVEAU 4ter — Bilan introspectif : [Énergie X/10, Win, Friction, Focus demain / sauté à la demande de l'utilisateur]
NIVEAU 2bis — Weekly note : [N] coches appliquées + [M] émergents ajoutés
NIVEAU 4 — Contexte global : [mis à jour / pas de changement]
NIVEAU 5 — Préférences : [mis à jour / pas de changement]
Cheminement de phase : [ligne ajoutée / pas d'insight notable]

À demain !
```

## Notes

- **Mode CONSOLIDATION vs AUTONOME** : `/dodo` détecte automatiquement si la daily du jour contient des sections `## Logs IA / Session [HH:MM]` (= `/fin-session` a déjà été lancé en cours de journée). Mode CONSOLIDATION = consolide ; Mode AUTONOME = fait tout le ruissellement (étapes 3-4 incluses).
- NIVEAU 2bis (sync daily → weekly) nécessite validation rapide en bloc — éviter validation item par item sauf confiance faible
- NIVEAU 3 (projets/casquettes) est appliqué directement — pas de validation
- NIVEAU 3bis (jalon Réflexion) nécessite validation simple o/n — ne jamais insister si refus
- NIVEAU 4 (contexte global) nécessite validation
- NIVEAU 4ter (bilan introspectif) est interactif — ne jamais insister si l'utilisateur dit qu'il ne veut pas faire le bilan ce soir
- NIVEAU 5 (préférences) est appliqué directement — pas de validation
- Être concis dans les logs (pas de blabla)
- Utiliser des liens `[[wikilinks]]` quand pertinent
- **Convention weekly (rappel)** : la weekly porte le planning de la semaine en cours. Si la weekly ouverte porte le numéro de la semaine bilanée (ancienne convention W22 et antérieures), ne pas appliquer la sync — alerter l'utilisateur.
- **Convention jalon Réflexion** : NIVEAU 3bis vise à combler la zone d'ombre des projets exécutés sans capitalisation Réflexion. Détection passive, validation explicite, pas d'insistance.
- **Doctrine /fin-session vs /dodo** : `/fin-session` traite le ruissellement micro (par session, plusieurs fois/jour). `/dodo` traite le ruissellement macro (par jour, une fois). Le tout est conçu pour le mode de travail en sessions parallèles.
