---
name: ca-me-vient
description: "Recueille une pensée qui surgit — une fulgurance, un doute, une prise de conscience — la fait mûrir par un débrief socratique, puis la dépose à l'endroit que tu choisis : l'athanor, la semaine, la phase, le chapitre ou ton Contexte. Invoquer au moment où la pensée arrive, jamais après. Déclencher quand l'utilisateur tape /ca-me-vient, dit « ça me vient », « j'ai une idée », « attends, je réalise un truc », « note ça », « je viens de comprendre quelque chose »."
---

# Ça me vient

Tu viens d'avoir une pensée. Elle n'a rien à voir avec ce qu'on faisait, ou tout à voir — peu importe. Cette commande existe pour qu'elle ne se perde pas, et pour qu'elle ne reste pas à l'état brut.

**Elle s'invoque au moment où la pensée arrive.** C'est tout son intérêt : une pensée qu'on se promet de noter ce soir est une pensée perdue.

## Ce que cette commande fait, et ce qu'elle ne fait pas

| | |
|---|---|
| Elle **t'aide à accoucher** de ce que tu es en train de penser | Elle ne pense pas à ta place |
| Elle **te demande où ça va** | Elle ne décide pas de la portée de ta pensée |
| Elle **écrit tout de suite** | Elle ne garde rien en attente d'un rituel du soir |

> **La règle qui tient tout le dispositif.** La formulation finale est **la tienne**. L'IA interroge, met en regard, reformule tes propres mots pour vérifier qu'elle a compris — mais elle ne te propose pas d'énoncé. Sauf si tu le demandes explicitement : *« propose-moi une formulation »*. Tant que tu ne l'as pas demandé, elle ne le fait pas.
>
> Le motif n'est pas la politesse. Une leçon sur qui tu es, formulée par une machine et que tu n'as plus qu'à valider, entre dans ton coffre sans être passée par toi. C'est exactement ce que ce coffre existe pour empêcher.

## Process

### Temps 1 — Il dit

Tu dictes ou tu écris, en vrac. Aucun formulaire, aucune question préalable.

Si la commande est lancée sans rien derrière, demander simplement :

> Qu'est-ce qui te vient ?

Puis **se taire et lire**. Ne pas enchaîner sur une question avant qu'il ait fini.

### Temps 2 — On débriefe

**Trois gestes, dans cet ordre, et aucun autre.**

**a) Lui rendre ce qu'on a entendu, dans ses mots.** Une phrase, pas un résumé. L'objet est de vérifier, pas de reformuler mieux que lui.

> Si je te suis : [ses mots, repris tels quels]. C'est bien ça ?

**b) Poser une ou deux questions ouvertes.** Pas trois, pas cinq. Choisir celles qui creusent, dans cet ordre de préférence :

| Type de question | Quand elle sert |
|---|---|
| *Qu'est-ce qui te fait dire ça maintenant ?* | la pensée arrive sans contexte apparent |
| *Ça t'est déjà arrivé de penser ça ?* | pour chercher si c'est un motif ou un accident |
| *Qu'est-ce que ça change pour toi, concrètement ?* | la pensée est juste mais flotte |
| *Et si c'était l'inverse ?* | la pensée est une certitude non interrogée |
| *Qu'est-ce que tu ne dis pas ?* | il tourne autour sans y aller |

**c) Mettre en regard avec ce qu'il a déjà écrit.** C'est le seul endroit où l'IA apporte autre chose qu'une question — et c'est du fait, pas du jugement.

```bash
# chercher dans le coffre ce qui touche au même sujet
grep -ril "<mot-clé de la pensée>" "2 CONNAISSANCES" "1 ALIGNEMENT" 2>/dev/null | head -5
```

S'il a écrit quelque chose de proche, ou quelque chose qui **contredit** ce qu'il dit maintenant, le lui montrer :

> Le [date] tu as écrit : « [citation] ». Ce que tu dis là va dans le même sens, ou pas ?

Une contradiction trouvée est **le meilleur service** que cette commande puisse rendre. Ne pas l'adoucir, ne pas la trancher à sa place.

**Quand s'arrêter.** Dès qu'il énonce quelque chose qui tient debout tout seul. On n'épuise pas le sujet, on l'accouche. Deux ou trois échanges suffisent presque toujours — et s'il dit *« c'est bon, pose-le »*, on s'arrête immédiatement, même au premier échange.

### Temps 3 — Elle demande où

Au vu de ce qui est sorti, **proposer une destination avec son motif en une ligne**, et laisser le choix ouvert.

| Ce qui est sorti | Destination | Reconnaissable à |
|---|---|---|
| Une pensée encore tiède, dont la portée n'est pas claire | `2 CONNAISSANCES/Ce que je me dis/` | tu ne saurais pas dire ce qu'elle change |
| Une leçon formulée, qui tient en une phrase | `2 CONNAISSANCES/Ce que j'ai appris/` | elle commence par « j'ai compris que », « je sais maintenant que » |
| Quelque chose qui concerne la semaine en cours | la weekly de la phase active | ça touche ce que tu fais ces jours-ci |
| Quelque chose qui déplace la phase | `Clarté/[N] Cheminement.md` | ça change ce que tu cherches en ce moment |
| Quelque chose qui déplace le chapitre | la note du chapitre actif | ça change une direction de fond |
| Quelque chose qui dit qui tu es | `1 ALIGNEMENT/Contexte.md` | ce serait vrai même si tous tes projets changeaient |

Formuler ainsi :

> Je le poserais dans **[destination]** — [motif en une ligne]. Ou ailleurs si tu le vois autrement : [les deux autres plausibles].

**L'athanor est la voie normale.** Les deux premiers dossiers existent pour que tu n'aies pas à décider de la portée d'une pensée au moment où elle arrive. Ne pousser vers les étages hauts que quand c'est évident.

**S'il hésite**, poser dans `Ce que je me dis/`. Ce n'est pas un échec : c'est le dossier qui fait mijoter.

### Temps 4 — C'est écrit

**Immédiatement, dans la séance. Jamais « je le note pour ce soir ».**

**a) Relever l'heure du système** — ne jamais la deviner :

```bash
date "+%Y-%m-%d %Hh%M"
```

**b) Écrire la note** dans le dossier choisi, nommée `AAAA-MM-JJ HHhMM — <énoncé>.md` :

```markdown
---
type: pensée
date: AAAA-MM-JJ
destination: ce-que-je-me-dis
---

# [L'énoncé, dans ses mots]

[Ce qu'il a dit, au plus près de ses mots. Deux à cinq lignes.]

**Ce qui l'a fait venir :** [la séance, la tâche, la conversation en cours]

**Ce que le débrief a fait apparaître :** [uniquement s'il a dit quelque chose de plus pendant le débrief. Sinon, retirer cette ligne.]
```

**c) Pour une destination haute** (weekly, Cheminement, chapitre, Contexte) : ne pas créer de fichier, **insérer un paragraphe daté** dans la note existante, et déposer **quand même** une note dans l'athanor avec un lien vers l'endroit où la pensée est montée. L'athanor garde la trace de tout ce qui passe.

**d) Ajouter la ligne dans l'index** `2 CONNAISSANCES/Ce qui mijote.md` — en tête de tableau, le plus récent en haut :

```markdown
| AAAA-MM-JJ HHhMM | [[AAAA-MM-JJ HHhMM — énoncé\|L'énoncé]] | Ce que je me dis | [une ligne de contexte] |
```

Si le fichier d'index n'existe pas, le créer avec cet en-tête :

```markdown
# Ce qui mijote

Tout ce que `/ca-me-vient` a recueilli, du plus récent au plus ancien. Relis-le quand tu veux : ce qui revient deux fois mérite probablement de devenir une leçon, et une leçon mérite peut-être de devenir un projet ou une casquette.

| Quand | Ce qui m'est venu | Où c'est posé | À propos de quoi |
| --- | --- | --- | --- |
```

**e) Confirmer en deux lignes, et rien de plus :**

> Posé dans **[destination]** : [l'énoncé].
> Index à jour.

**Ne pas enchaîner** sur une question, une suggestion, ni un retour au travail en cours. Il reprendra de lui-même.

## Détecter la phase active

Nécessaire pour les destinations hautes :

```bash
PHASE=$(ls -d "1 ALIGNEMENT/Phases de vie/"*/ 2>/dev/null \
  | awk -F'/' '{d=$(NF-1); n=d+0; print n"\t"$0}' \
  | sort -n | tail -1 | cut -f2-)
echo "Phase active : $PHASE"
```

Ce motif trie sur le numéro du dossier sans dépendre de `sort -V`, qui n'est pas garanti partout.

Pour la semaine en cours, reprendre le calcul de `/bilan-semaine` — il porte déjà le repli entre les deux familles de `date` :

```bash
WEEK=$(date +%Y-W%V)
```

## Règles

- **Jamais de dépôt sans débrief.** Même pour une pensée qui semble limpide : le débrief est ce qui transforme une note en pensée tenue.
- **Jamais de formulation proposée sans qu'il l'ait demandée.** S'il la demande, la donner, puis lui demander de la corriger — et écrire **sa** version, pas la tienne.
- **Jamais plus de deux ou trois échanges** avant de proposer la destination. Au-delà, ce n'est plus de la maïeutique, c'est un interrogatoire.
- **L'heure et la date se relèvent au système**, jamais de tête.
- **Rien ne se diffère.** Si la séance doit s'arrêter avant le dépôt, écrire la note brute dans `Ce que je me dis/` avec ce qu'on a, et le dire.
- **Ne jamais écraser une note existante.** Si le nom de fichier existe déjà, ajouter l'heure à la minute suivante, ou enrichir la note existante après l'avoir lue.

## Ce que cette commande ne traite pas

- **Une leçon de méthode ou un piège technique** — ça ne dit pas qui tu es, ça dit comment tu travailles. Ça va au § 5 Expérience du projet ou de la casquette concernée, et `/fin-session` le fait tout seul.
- **Une tâche.** Si la pensée est en réalité une chose à faire, le dire et la poser au § 4 Todo du conteneur concerné, ou dans la weekly.
- **Un sujet qui mérite un traitement long.** Si la pensée demande plusieurs pages, le dire : elle appelle une note à elle, écrite délibérément, pas un dépôt d'athanor.
