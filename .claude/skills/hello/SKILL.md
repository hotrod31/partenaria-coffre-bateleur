---
name: hello
description: "Début de session : sync mémoire, lecture du Contexte et des Préférences, détection de la phase de vie active et du chapitre, bilan automatique de la veille, lecture de la daily note du jour, briefing personnalisé avec prénom, suggestions d'actions du jour. Déclencher quand l'utilisateur tape /hello, dit 'bonjour', 'bjr', 'salut', 'on commence', 'on attaque', 'briefing', 'début de session', ou ouvre l'outil pour la première fois de la journée."
---

# Welcome — Début de session

Synchronise le contexte, lit la mémoire, et donne un briefing personnalisé pour démarrer la session.

## Process

### Étape 1 : Lire le contexte

**Lire dans cet ordre :**

1. `1 ALIGNEMENT/Contexte.md` — Extraire le prénom de l'utilisateur (champ **Nom** ou première ligne)
2. `1 ALIGNEMENT/Préférences.md` — Décisions récentes, prochaines étapes, contexte projets

### Étape 2 : Détecter la phase active

```bash
ls -d "1 ALIGNEMENT/Phases de vie/"*/ | sort -V | tail -1
```

Équivalent PowerShell si le shell est PowerShell :
```powershell
Get-ChildItem -Path "1 ALIGNEMENT/Phases de vie" -Directory | Sort-Object Name | Select-Object -Last 1
```

Extraire le numéro et nom de la phase depuis le nom du dossier.

### Étape 3 : Lire le contexte de phase

1. **Intention de la phase** : Extraire le numéro [N] depuis le nom du dossier de la phase active (premier caractère numérique), puis lire `1 ALIGNEMENT/Phases de vie/[Phase active]/Clarté/[N] Intention.md` (contient un champ `chapitre:` dans le frontmatter)
2. **Chapitre actif** : Depuis le champ `chapitre:` de l'intention, lire le fichier correspondant dans `1 ALIGNEMENT/Chapitres/[Nom].md` pour récupérer la vision long terme (intention, triple ancrage, objectifs macro)
3. **Inbox** : compter les items de `0 INBOX/`
4. **Activité récente** : compter les notes `.md` modifiées dans les dernières 24h sous la phase active

### Étape 3b : Bilan automatique de la veille

Exécuter la logique de `/bilan-veille` **silencieusement** :

1. Calculer le sous-dossier de semaine du jour et vérifier le jour de la semaine via une commande système (ne jamais calculer mentalement) :
   ```bash
   WEEK=$(date +%Y-W%V)
   TODAY=$(date +%Y-%m-%d)
   DAY_EN=$(date +%A)
   ```
   Mapper `$DAY_EN` en français : Monday→Lundi, Tuesday→Mardi, Wednesday→Mercredi, Thursday→Jeudi, Friday→Vendredi, Saturday→Samedi, Sunday→Dimanche.
   Chemin de la daily note du jour : `1 ALIGNEMENT/Phases de vie/[Phase active]/$WEEK/$TODAY.md`
2. Vérifier si la daily note du jour existe. Si non, la créer à partir du template `5 RESSOURCES/Modèles/Daily Note.md` (remplacer `{{date}}` par YYYY-MM-DD, compléter le titre "# Objectifs de la journée du" avec la date). Créer le dossier `$WEEK/` s'il n'existe pas.
3. Vérifier si la section `# Bilan de la journée précédente` est déjà remplie. Si oui, passer.
4. Trouver la daily note précédente (la plus récente avant aujourd'hui dans les sous-dossiers `YYYY-WXX/` de la phase active).
5. Extraire la section `# Réalisations de la journée` de cette note.
6. Si elle contient du texte, rédiger un résumé succinct (3-6 lignes, style télégraphique, regroupé par projet, avec [[wikilinks]]) et l'insérer sous `# Bilan de la journée précédente`.
7. Ne pas afficher de confirmation séparée — le briefing mentionnera que le bilan a été inséré.

### Étape 4 : Lire et analyser la daily note du jour

1. **Déterminer le chemin** : `1 ALIGNEMENT/Phases de vie/[Phase active]/YYYY-WXX/YYYY-MM-DD.md` où `YYYY-WXX` est le sous-dossier de la semaine courante et `YYYY-MM-DD` est la date du jour
2. **Lire la note** si elle existe (elle devrait exister après l'étape 3b)
3. **Extraire les éléments clés** :
   - **Bilan de la veille** : résumé en 1-2 lignes (chercher les sections qui parlent d'hier, de la veille, ou du bilan)
   - **Objectifs déclarés pour la journée** : liste des tâches ou objectifs mentionnés (chercher les sections objectifs, tâches, plan, todo)
   - **État santé/routines** : ce qui a été fait le matin (sport, marche, méditation, sommeil, douleurs...)
   - **Notes et réflexions** : insights, idées, réflexions notables dictées pendant la marche
4. **Si la note n'existe pas ou est vide** : noter "Pas de daily note détectée pour aujourd'hui" et passer à l'étape suivante normalement

### Étape 4b : Mettre à jour PROJETS.md

Lire `3 PROJETS/PROJETS.md` et mettre à jour la section **Situation** de chaque projet mentionné dans Préférences.md ou dans la daily note. Mettre à jour la date `updated` dans le frontmatter.

Ne pas tout réécrire — modifier uniquement les lignes "Situation" et "Points critiques" si des changements ont eu lieu depuis la dernière session.

### Étape 4c : Mettre à jour les Kanbans

**Sources de tâches :** notes de contexte projet (prochaines étapes), PROJETS.md (points critiques), daily note du jour, **notes de suivi de livrables** (`3 PROJETS/[Projet]/Suivi des livrables*.md` — les tâches cochées dans ces notes doivent être reflétées comme accomplies dans le Kanban, et les tâches non cochées comme programmées ou en cours).

**Kanban global** (`3 PROJETS/Suivi Projets.md`) :
- Format Obsidian Kanban : frontmatter `kanban-plugin: basic`, colonnes en `## [Nom Projet]`, cartes en `- [ ]` / `- [x]`
- Une colonne par projet, montrant uniquement les tâches **programmées** et **en cours**
- Ajouter les nouvelles tâches identifiées, cocher les tâches accomplies depuis la dernière session
- Supprimer les tâches accomplies du Kanban global (elles sont dans les Kanbans projet)

**Kanbans projet** (`3 PROJETS/[Projet]/Suivi [Projet].md`) :
- 4 colonnes : `À programmer`, `Programmées`, `En cours`, `Accomplies`
- Déplacer les cartes entre colonnes selon l'avancement
- Ajouter les nouvelles tâches dans la colonne appropriée
- Les dates sont au format `@{YYYY-MM-DD}` après la description de la carte

Ne mettre à jour que les Kanbans des projets effectivement travaillés pendant la session.

### Étape 5 : Composer le briefing

Utiliser le prénom extrait du Contexte :

```
Bonjour [Prénom],

[Date du jour — format : Samedi 27 juin 2026 (W26) — OBLIGATOIRE : utiliser $DAY_EN converti en français, ne jamais deviner le jour de la semaine]

**Chapitre actif :** [Nom du chapitre] ([Période])
> [Intention du chapitre en 1 ligne]

**Phase actuelle :** [N] [Nom de la phase] ([Période courte])
**Intention :** [Résumé de l'intention en 1 ligne]

**Vault status :**
- Inbox : X items
- Activité 24h : X notes modifiées

**Mémoire dernière session :**
- [Décisions récentes depuis les notes de contexte — 2-3 items max]
- [Prochaines étapes depuis les notes de contexte]

**Ta daily note du jour :**
- Bilan hier : [résumé du bilan de la veille extrait de la note]
- Objectifs déclarés : [liste des objectifs/tâches extraits]
- Routines ce matin : [X/Y accomplies — détails]
- Notes : [insights ou réflexions notables]
[Si pas de daily note : "Pas de daily note détectée pour aujourd'hui — tu peux en créer une pour poser tes objectifs"]

**Suggestion du jour :**
[Suggestion contextuelle — basée prioritairement sur la daily note si elle existe]
```

### Suggestions contextuelles

**Règle de priorité : la daily note prime.** Quand la daily note contient des objectifs, ceux-ci priment sur les notes de contexte projet pour les suggestions du jour (la daily note est plus fraîche et plus spécifique).

**Si la daily note existe et contient des objectifs :**
- La suggestion principale reprend le premier objectif déclaré ou le plus important
- Si la note mentionne un blocage, un problème ou une douleur, la suggestion doit en tenir compte (ex: "Tu as mentionné [problème] — veux-tu qu'on s'y attaque ?")
- Les objectifs de la daily note remplacent les suggestions génériques par jour de la semaine

**Si pas de daily note (fallback sur le comportement existant) :**
- **Lundi :** "Nouvelle semaine — bon moment pour revoir tes projets actifs"
- **Mercredi :** "Mi-semaine — as-tu avancé sur ton intention principale ?"
- **Vendredi :** "Fin de semaine — pense à faire un `/bilan-semaine`"
- **Weekend :** "Temps de repos — peut-être un peu de lecture ou de mouvement ?"

**Toujours applicable (indépendamment de la daily note) :**
- **Si inbox > 5 :** "Ton inbox déborde un peu — `/trier-inbox` peut aider"
- **Si inbox = 0 :** "Inbox vide, parfait"

### Étape 6 : Actions rapides

Proposer 2-3 actions basées sur le contexte. **Si la daily note existe, les actions reprennent les tâches prioritaires déclarées dans la note :**

```
**Actions rapides :**
1. [Tâche prioritaire de la daily note OU action notes de contexte si pas de daily note]
2. [Deuxième tâche de la daily note OU action basée sur la phase/intention]
3. [Action contextuelle : /bilan-jour, /brainstorming, /trier-inbox, ou /bilan-semaine le vendredi]
```

Si la daily note mentionne des tâches spécifiques, les reformuler en actions claires et directes plutôt que proposer des actions génériques.

## Style

- Concis
- En français
- Pas de superflu
- Actionnable
- Utiliser le prénom de l'utilisateur
- OBLIGATOIRE : écrire en français correct avec tous les accents (é, è, ê, à, ù, ç, î, ô, etc.)
- Ne jamais produire du texte sans accents — c'est du français, pas du ASCII
- Tutoiement institué entre toi et l'utilisateur
