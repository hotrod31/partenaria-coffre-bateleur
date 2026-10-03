---
name: bilan-jour
description: "Prépare ton bilan du jour à ta place, en lisant ce que la journée a laissé comme traces, puis te demande une seule chose — ta note d'énergie — et quelques arbitrages groupés avant d'écrire. Mode propositionnel : il propose un bilan rédigé, il ne te fait pas passer un questionnaire. Déclencher quand l'utilisateur tape /bilan-jour, dit « bilan du jour », « réflexion du soir », « faisons le point sur la journée », « qu'est-ce que j'ai appris aujourd'hui »."
---

# Bilan du jour

**Le principe, et c'est tout le skill.** En fin de journée, on n'a pas l'énergie de répondre à cinq questions. Donc **tu fais le travail avant de parler** : tu lis ce que la journée a laissé comme traces, tu rédiges le bilan, et tu ne demandes que ce que tu ne peux pas savoir.

> 🔴 **Mode propositionnel, sans exception.** Tu proposes un bilan **déjà écrit**. Tu ne poses pas de question ouverte, tu ne déroules pas de questionnaire. Les seules prises de parole demandées sont une note d'énergie et des arbitrages fermés, tous présentés **en une seule fois**.

## Avant de dire un mot — préparer

### 1. Situer

```bash
PHASE=$(ls -d "1 ALIGNEMENT/Phases de vie/"*/ 2>/dev/null \
  | awk -F'/' '{d=$(NF-1); n=d+0; print n"\t"$0}' \
  | sort -n | tail -1 | cut -f2-)
WEEK=$(date +%Y-W%V)
TODAY=$(date +%Y-%m-%d)
echo "Phase : $PHASE"
echo "Daily : ${PHASE}${WEEK}/${TODAY}.md"
```

### 2. Lire toute la matière de la journée

| Source | Ce qu'on y cherche |
|---|---|
| **La daily du jour, en entier** | les objectifs posés le matin, les réalisations, et **toutes** les sections `## Logs IA / Session` — c'est là que vit le détail |
| `2 CONNAISSANCES/Ce qui mijote.md` | les pensées déposées aujourd'hui par `/ca-me-vient` |
| Les notes de contexte touchées aujourd'hui | ce qui a avancé, et ce qui est resté ouvert |
| La weekly de la phase | ce qui était prévu pour cette semaine |

**Lire la daily en entier, pas son titre ni son début.** Une journée à six séances a son fait le plus important dans le log de la quatrième.

### 3. Rédiger le bilan, avant de parler

Composer, en interne :

- **Le win principal** — pas une liste, le fait qui compte. Ce qui est passé d'un état à un autre.
- **La friction principale** — ce qui a résisté, coûté du temps, ou échoué.
- **L'apprentissage** — s'il y en a un. **Une journée sans leçon est le cas normal** : ne rien inventer pour remplir la ligne.
- **Le focus de demain** — déduit de ce qui reste ouvert, pas inventé.
- **Les points d'arbitrage** — uniquement là où le doute est réel. Zéro, un ou deux. Jamais cinq.

## Le processus

### Temps 1 — Ouvrir, et ne demander qu'une chose

```
Bilan du jour — [date]

J'ai lu ta journée. Avant de te montrer ce que j'en retiens :
**ton énergie aujourd'hui, de 1 à 10 ?**
```

C'est la seule donnée que tu ne peux pas déduire des traces. Rien d'autre ne se demande ici.

**S'il répond autre chose que son énergie** — un commentaire, un fait de plus — l'intégrer et continuer. Ne pas redemander le chiffre.

### Temps 2 — Montrer le bilan, et grouper les arbitrages

Présenter le bilan **rédigé**, puis les arbitrages **tous ensemble**, en une seule prise de parole :

```
Voilà ce que je retiens du [date] :

**Énergie** [X]/10
**Win** — [le fait, en une ou deux lignes]
**Friction** — [ce qui a résisté]
**Apprentissage** — [la leçon, ou « rien de neuf aujourd'hui »]
**Demain** — [ce qui reste ouvert et qui compte]

Deux choses à trancher :
1. [point d'arbitrage, formulé en question fermée]
2. [point d'arbitrage]

Tu corriges ce que tu veux, et j'écris.
```

**Si rien n'est à trancher, ne rien demander** — dire que le bilan est prêt et attendre son feu vert, rien de plus.

**Les arbitrages sont fermés.** *« J'ai mis la panne du matin comme friction principale plutôt que le retard du livrable — tu le vois comme ça ? »* est un arbitrage. *« Qu'est-ce qui a été difficile aujourd'hui ? »* est un questionnaire, et c'est exactement ce que ce skill existe pour éviter.

### Temps 3 — Écrire, sans redemander

Dès qu'il a validé ou corrigé, **écrire tout de suite**. Ne pas demander *« veux-tu que je crée la note ? »* — c'est le but de la commande.

**a) La note de bilan** : `${PHASE}${WEEK}/${TODAY} — Bilan du jour.md`

```markdown
# [Date] — Bilan du jour

**Énergie :** [X]/10

## Le win
[Le fait qui compte, dans ses mots quand il les a donnés.]

## La friction
[Ce qui a résisté.]

## Ce que j'ai appris
[La leçon. Retirer cette section si la journée n'en a pas produit.]

## Demain
[Le focus.]
```

**b) La ligne de Cheminement** — dans `${PHASE}Clarté/[N] Cheminement.md`, à la fin de la section `## Cheminement` :

```
- **[AAAA-MM-JJ]** : [le win] — [l'apprentissage, s'il y en a un]
```

Extraire `[N]` du numéro du dossier de phase. **Ne pas écrire de ligne si la journée n'a produit ni win ni apprentissage notable** — un Cheminement rempli de lignes creuses ne se relit pas.

**c) Confirmer en deux lignes**, et s'arrêter là :

```
Bilan écrit : [[AAAA-MM-JJ — Bilan du jour]]
Cheminement à jour.
```

## Le cas où il n'y a rien à lire

Si la daily du jour est vide ou quasi vide — pas de log, pas de réalisation —, **tu n'as pas de matière, et il ne faut pas la fabriquer**. Le dire, et poser alors **deux questions, pas cinq** :

```
Ta daily du jour est vide, je n'ai rien à te proposer.

Deux questions, et j'écris :
- ton énergie, de 1 à 10 ?
- qu'est-ce qui a compté aujourd'hui ?
```

C'est le seul cas où ce skill questionne. Il est l'exception, pas le mode normal.

## Règles

- **Jamais de questionnaire.** Une note d'énergie, des arbitrages fermés groupés, et c'est tout.
- **Jamais « veux-tu que je crée la note ? »** — la note est la raison d'être de la commande.
- **Lire la daily en entier**, sections `## Logs IA` comprises, avant toute synthèse.
- **Ne rien inventer pour remplir une section.** Une journée sans apprentissage, sans friction ou sans win existe. Retirer la section plutôt que l'orner.
- **Ne jamais deviner la date ni l'heure** — les relever au système.
- **Ne pas écraser la note de bilan si elle existe déjà** : la lire, puis la compléter.
- **Ce qui relève de qui tu es ne se traite pas ici.** Si le bilan fait affleurer une pensée sur toi — pas sur ta journée —, le signaler en une ligne et renvoyer à `/ca-me-vient`. Ne pas la formuler, ne pas la déposer.
