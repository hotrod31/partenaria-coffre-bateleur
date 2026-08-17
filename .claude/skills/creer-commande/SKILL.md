---
name: creer-commande
tags: meta
description: Accompagne l'utilisateur à créer une commande maison pour son coffre Obsidian + Claude Code, sans qu'il ait besoin de compétences techniques. Consulte d'abord la Bibliothèque de commandes pour éviter de réinventer une commande existante, puis capture l'intention et le rituel étape par étape en langage clair, puis génère le fichier de la commande. Déclencher quand l'utilisateur dit « crée une commande », « je voudrais automatiser », « j'ai un rituel que je répète », « fais-moi une nouvelle commande », « je veux un raccourci pour... », ou nomme un besoin d'automatisation dans son coffre.
---

# Créer une commande

> **Note de vocabulaire.** Dans cette communauté PartenarIA, on parle de **commande**. Techniquement, dans Claude Code, ce que tu crées ici s'appelle un **skill** — c'est exactement la même chose, on l'appelle simplement « commande » parce que c'est plus parlant en français. Si tu cherches un jour de l'aide en ligne, tape *skill Claude Code* et non pas *commande Claude Code*.

## Ce que fait cette commande

Cette commande t'accompagne pas à pas pour transformer un **rituel que tu répètes** en une commande maison que tu pourras invoquer par son nom (`/nom-de-ta-commande`). Tu n'as pas besoin de savoir coder ni de connaître les outils techniques — tu décris ce que tu veux, je m'occupe du reste.

Elle est faite pour créer des **commandes simples** — c'est-à-dire des commandes qui font une seule chose de bout en bout et produisent un livrable clair. Pour orchestrer plusieurs commandes en une seule (une **méta-commande**), une autre commande dédiée sera livrée plus tard : `creer-meta-commande`.

## Ce que tu vas obtenir en fin de course

- Un fichier `.claude/skills/[nom-de-ta-commande]/SKILL.md` dans ton coffre, prêt à l'usage.
- Une invocation testable immédiatement : `/nom-de-ta-commande`.
- Un ajout optionnel dans la Bibliothèque de commandes pour partager avec les autres membres.

---

## Processus

### Étape 1 — Capture d'intention

Pose ces questions **une par une**, attends chaque réponse, ne les groupe pas :

1. **Quel est ton objectif final ?** — Décris le **livrable concret** que la commande doit produire. Exemples : « une note de préparation d'un débrief avec une soignante », « un fichier PowerPoint pour ma prochaine réunion CA », « le classement automatique des captures de mon inbox par projet ». Reste concret : *pas* « je veux gagner du temps », *oui* « je veux un document Word structuré en 5 sections avec les mêmes titres à chaque fois ».
2. **Quand veux-tu l'utiliser ?** — Chaque matin ? Une fois par semaine ? À la fin de chaque réunion ? À la demande, quand tu en as besoin ?
3. **Quelle est la douleur principale de ce rituel aujourd'hui ?** — Ce qui te casse le plus les pieds quand tu le fais à la main. Cette réponse va nourrir le cœur de la commande.

**Règle d'or à ce stade** : si l'utilisateur répond vaguement (« ben, je fais ça comme je peux »), reformule avec un cas d'entretien : *« Imagine que ce soir tu dois former quelqu'un à faire ça à ta place. Qu'est-ce que tu lui dirais concrètement de faire, dans quel ordre ? »* Les rituels tacites sortent avec cette reformulation.

### Étape 2 — Recherche dans la Bibliothèque PartenarIA

**Avant** de partir sur la création d'une commande neuve, vérifier si une commande équivalente existe déjà et peut être adaptée.

1. Ouvrir le fichier `5 RESSOURCES/Bibliothèque de commandes.md` du coffre.
2. Parcourir le tableau à la recherche de mots-clés cohérents avec l'objectif capté à l'étape 1.
3. **Si une commande existante correspond** — même approximativement — la présenter à l'utilisateur :
   - Nom, description, cas d'usage
   - Lien vers le fichier source
   - Proposer : « veux-tu qu'on parte de cette commande et qu'on l'adapte à ton usage, plutôt que de partir d'une page blanche ? »
   - Si oui → passer directement à l'étape 4 (Génération) en adaptant le contenu.
   - Si non ou si l'adaptation serait trop lourde → continuer à l'étape 3.
4. **Si aucune commande existante ne correspond** — continuer à l'étape 3.

*Note V1* — la recherche se limite à la Bibliothèque locale. Dans une version future, une branche recherche étendue (web via Firecrawl) pourra être ajoutée.

### Étape 3 — Description accompagnée du rituel

Cette étape est le cœur du travail. Prendre le temps.

**Sous-étape 3a — Les étapes du rituel, une par une.**

Demander à l'utilisateur de décrire son rituel étape par étape, **comme s'il formait quelqu'un** ce soir. Pour chaque étape, capter :

- **Ce qu'on fait concrètement** — l'action, en langage simple.
- **À quoi on fait attention** — le critère de qualité, ce qui distingue une étape bien faite d'une étape bâclée.
- **Ce qui peut mal tourner** — le piège éventuel à éviter.

Nombre indicatif : **3 à 6 étapes**. Si l'utilisateur en propose plus, proposer de regrouper. Si moins de 3, creuser pour faire surgir les implicites (« qu'est-ce que tu fais juste avant / juste après ce que tu as décrit ? »).

**Ne PAS demander à l'utilisateur** :
- Quels outils techniques utiliser (Python, API, script bash…) — il n'a pas la compétence, ce n'est pas son travail.
- Quel format technique le fichier doit prendre.
- Comment invoquer un LLM en interne.

**Sous-étape 3b — Logiciels externes utilisés (exception explicite).**

Poser une seule question ciblée : « ton rituel touche-t-il à un logiciel que tu utilises déjà (Word, PowerPoint, Excel, Photoshop, Canva, un site web précis…) ? Si oui lequel, et pour faire quoi ? »

Si l'utilisateur mentionne un logiciel externe qui nécessite un script pour être manipulé (ex : PowerPoint → génération .pptx ; Excel → lecture/écriture .xlsx ; conversion PDF ; scraping d'un site web…) — **c'est à toi (moi, l'assistant) d'aller chercher via Firecrawl** les patterns techniques nécessaires (bibliothèque Python, exemple de code, référence de doc) et de les embarquer dans la commande finale de manière invisible pour l'utilisateur.

Exemples de recherches Firecrawl à déclencher :
- « python-pptx create presentation programmatically »
- « openpyxl write formatted excel file »
- « pdf conversion python docx to pdf »

Le résultat de la recherche vient nourrir le corps du fichier SKILL.md, pas l'interaction avec l'utilisateur.

**Sous-étape 3c — Exemples concrets (indispensable).**

Demander : « peux-tu me montrer 1 ou 2 exemples de sorties de ce rituel que tu trouves excellentes ? Et si tu en as, 1 exemple raté et pourquoi il l'était ? »

Si l'utilisateur n'a pas d'exemples sous la main : chercher dans ses notes existantes ou lui proposer de compléter la commande plus tard. Ne pas bloquer la création.

**Stocker les exemples fournis VERBATIM** dans la commande — mot pour mot, sans reformulation. Ce sont eux qui donnent le « goût » spécifique de l'utilisateur à l'IA.

### Étape 4 — Choix et validation du nom

Le nom du fichier de la commande doit respecter des contraintes techniques :

- **Uniquement des lettres minuscules et des tirets.**
- **Pas d'accents** (é, è, à, ç…).
- **Pas d'espaces, pas de majuscules, pas de caractères spéciaux.**
- Exemples valides : `preparer-debrief`, `note-de-reunion`, `plan-tournee-aromatherapie`.
- Exemple invalide : `Préparer débrief` → à corriger en `preparer-debrief`.

Si l'utilisateur propose un nom invalide, corriger silencieusement et lui montrer la version valide : « le fichier s'appellera `preparer-debrief` (sans accents et sans espaces, c'est une contrainte technique) — mais toi tu pourras l'appeler *préparer débrief* dans nos échanges, ça marchera pareil ».

### Étape 5 — Génération du fichier

Créer le fichier `.claude/skills/[nom-valide]/SKILL.md` avec cette structure :

```markdown
---
name: [nom-valide]
description: [Description qui explique ce que la commande fait ET dans quels contextes l'utiliser. Doit être un peu « poussante » — l'IA a tendance à sous-déclencher les commandes. Inclure explicitement les phrases-types de déclenchement. Longueur : 200-400 caractères.]
---

# [Titre lisible avec accents et espaces]

[1-2 phrases : ce que fait la commande et dans quel contexte l'utiliser.]

## Ce que tu vas obtenir

[Description du livrable final, concret.]

## Processus

### Étape 1 — [Nom de l'étape en langage naturel]

[Instructions à l'IA, à l'impératif. Expliquer le POURQUOI de chaque instruction, pas juste le quoi. Éviter les MUSTs en majuscules — préférer des explications posées.]

### Étape 2 — ...

## Exemples

**Exemple bien fait :**
> [Exemple verbatim de l'utilisateur, copié mot pour mot]

Pourquoi c'est bon : [ce que l'utilisateur a dit sur pourquoi il aimait ce résultat]

**Exemple raté (si applicable) :**
> [Exemple verbatim]

Pourquoi c'était raté : [explication de l'utilisateur]

## Règles à respecter

- [Règles issues de la conversation avec l'utilisateur, formulées en langage clair]
- [...]

## Ce qu'il ne faut PAS faire

- [Anti-patterns issus des « pièges » captés à l'étape 3]
- [...]
```

**Sur la description (champ frontmatter)** : c'est le mécanisme qui décide si la commande se déclenche ou pas quand l'utilisateur parle. Elle doit inclure :
- Ce que fait la commande.
- Les phrases-types qui doivent la déclencher (« déclencher quand l'utilisateur dit ... ou ... »).
- Un ton légèrement poussant (Claude a tendance à sous-déclencher).

**Frontmatter** : uniquement `name` et `description`. Ne pas ajouter `allowed-tools`, `license`, `compatibility` sauf demande explicite — ça surcharge inutilement.

**Longueur du corps** : viser sous 300 lignes pour une commande simple. Si le rituel demande plus, c'est probablement une méta-commande — proposer à l'utilisateur d'attendre la sortie de `creer-meta-commande`.

### Étape 6 — Test immédiat + ajout à la Bibliothèque

1. **Annoncer la création** à l'utilisateur : « ta commande `/[nom]` est créée. On la teste maintenant sur un cas réel ? »
2. **Si oui** — proposer à l'utilisateur d'invoquer sa nouvelle commande sur un cas concret et observer le résultat ensemble.
3. **Ajustement** — si le résultat n'est pas satisfaisant, remonter avec l'utilisateur ce qui n'a pas marché et modifier la commande en direct (ajouter un exemple, préciser une étape, retirer une consigne trop rigide).
4. **Proposer d'ajouter à la Bibliothèque PartenarIA** — « veux-tu que j'ajoute cette commande à la Bibliothèque de commandes pour que les autres membres puissent en profiter ? » Si oui → éditer `5 RESSOURCES/Bibliothèque de commandes.md` pour ajouter une ligne : nom · description · fichier · niveau · cas d'usage.

---

## Règles

- **Toujours consulter la Bibliothèque PartenarIA à l'étape 2** avant de démarrer une création neuve — inutile de réinventer la roue.
- **Ne jamais demander à l'utilisateur les outils techniques** à utiliser dans sa commande. C'est le travail de l'assistant de choisir et de rechercher via Firecrawl si nécessaire.
- **Exemples verbatim** — copier mot pour mot ce que l'utilisateur donne comme exemples. Sa formulation encapsule son goût.
- **Nom fichier sans accent, sans majuscule, sans espace** — corriger silencieusement.
- **Frontmatter minimal** — `name` + `description` uniquement.
- **Description « pushy »** — inclure explicitement les phrases-types qui doivent déclencher la commande.
- **Toujours proposer un test immédiat** en fin de création — sans test, la commande reste théorique.
- **Toujours proposer d'ajouter à la Bibliothèque** en fin de test réussi — c'est ce qui alimente l'écosystème PartenarIA.

## Ce que cette commande NE FAIT PAS

- Elle ne crée pas de **méta-commande** (orchestration de plusieurs commandes simples). C'est le rôle de `creer-meta-commande` (à venir).
- Elle ne cherche pas encore de commandes existantes **hors** de la Bibliothèque locale — pas de recherche GitHub ni web à ce stade. Cette branche sera ajoutée en V2 quand tous les membres PartenarIA auront Firecrawl installé et un accès au repo GitHub PartenarIA.
- Elle ne propose pas de **tests automatiques** (assertions, benchmark, évaluation quantitative) — c'est réservé aux commandes destinées à la production à grande échelle. Ici, le test se fait à la main sur un cas réel.
- Elle ne demande pas à l'utilisateur de choisir entre « skill » et « fiche » — elle produit toujours une commande exécutable.

## Références

- **Skill officiel Anthropic `skill-creator`** — https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md (source d'inspiration principale : structure Capture Intent → Interview → Draft → Test, anatomie du skill, principe de progressive disclosure, description pushy).
- **[[Bibliothèque de commandes]]** — le catalogue des commandes créées par toi dans ton coffre.
- **`AGENTS.md`** — la doctrine PartenarIA qui définit la posture relationnelle IA-utilisateur.
