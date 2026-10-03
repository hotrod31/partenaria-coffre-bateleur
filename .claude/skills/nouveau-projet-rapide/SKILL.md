---
name: nouveau-projet-rapide
description: "Ouvre un projet en cinq questions et quatre minutes : l'arborescence, la note de contexte, et les premières actions. Version resserrée de /nouveau-projet — sans budget, sans analyse de risques, sans gouvernance. C'est aussi le chemin par lequel une leçon de ton athanor devient un projet. Déclencher quand l'utilisateur tape /nouveau-projet-rapide, dit « ouvre-moi un projet vite », « je veux juste cadrer ça rapidement », « un projet simple », ou veut transformer une leçon en projet."
---

# Nouveau projet — version rapide

Cinq questions, et le projet existe. **Pas de budget, pas d'analyse de risques, pas de gouvernance** — ces trois-là vivent dans `/nouveau-projet`, et ils ne servent que quand le projet engage de l'argent, des tiers, ou une échéance qu'on ne peut pas rater.

## Laquelle des deux prendre

| | `/nouveau-projet-rapide` | `/nouveau-projet` |
|---|---|---|
| Durée du cadrage | quelques minutes | une bonne demi-heure |
| Questions | 5 | 10 étapes |
| Notes produites | **1** — la note de contexte | **jusqu'à 6** — contexte, objectifs, planification, et selon le projet budget, risques, gouvernance |
| Pour quoi | un projet que tu portes seul, dont tu vois l'issue | un projet avec de l'argent, des tiers, une échéance dure, ou plusieurs mois devant |
| Exemples | « reprendre la course », « refaire mon site », « publier mes dix premiers articles » | « ouvrir mon activité », « lancer une formation payante », « déménager l'atelier » |

> **Dans le doute, prends celle-ci.** Un projet cadré en quatre minutes et qui avance vaut mieux qu'un cadrage en dix étapes jamais terminé. Et si en cours de route tu réalises qu'il faut la version longue, elle reprend ce qui est déjà écrit — rien n'est perdu.

## Process

### Question 0 — Est-ce vraiment un projet ?

**Un projet a une fin.** Si ce dont tu parles n'en a pas, c'est une **casquette** — un rôle que tu tiens dans la durée.

| | A une fin | Alors |
|---|---|---|
| **Projet** | oui | `3 PROJETS/<Nom>/` — et il se clôt un jour |
| **Casquette** | non | `4 CASQUETTES/<Nom>/` — et elle se revoit à une cadence, pas à une date |

Si c'est une casquette, le dire et demander confirmation avant de continuer : la structure est la même, le dossier et le vocabulaire changent.

**Si la demande vient d'une leçon de l'athanor** — `2 CONNAISSANCES/Ce que j'ai appris/` — la lire en entier avant de poser la question suivante, et **la citer** au § 1 de la note de contexte. C'est ce qui donne au projet sa raison d'être, et c'est le passage que le cycle rate le plus souvent : une leçon qu'on ne décide jamais d'habiter reste un commentaire sur sa propre vie.

### Question 1 — Qu'est-ce que c'est ?

> Comment tu l'appelles, et c'est quoi en une phrase ?

Récupérer le nom — propre pour un dossier, sans `< > : " / \ | ? *` — et la description courte.

### Question 2 — Pourquoi maintenant ?

> Pourquoi maintenant, et pas dans six mois ?

C'est la question d'alignement, et elle remplace à elle seule l'étape 2 de la version longue. Si la réponse est faible, le dire — un projet sans raison de commencer maintenant est un projet qui s'arrêtera au premier obstacle.

**Relier au chapitre et à la phase en cours**, s'ils existent :

```bash
PHASE=$(ls -d "1 ALIGNEMENT/Phases de vie/"*/ 2>/dev/null \
  | awk -F'/' '{d=$(NF-1); n=d+0; print n"\t"$0}' \
  | sort -n | tail -1 | cut -f2-)
grep -l "status: active" "1 ALIGNEMENT/Chapitres/"*.md 2>/dev/null
```

Si le projet ne sert ni le chapitre ni la phase, **le signaler une fois** — sans l'empêcher. Un projet peut légitimement sortir du cadre ; ce qui ne l'est pas, c'est de ne pas le savoir.

### Question 3 — À quoi on verra que c'est fait ?

> Quand ce projet sera fini, qu'est-ce qui existera qui n'existe pas aujourd'hui ? Et pour quand ?

Deux choses : **l'issue visible** et **l'échéance**.

- Si l'issue n'est pas vérifiable de l'extérieur — « me sentir mieux organisé » —, demander ce qui le prouverait. Pas pour faire du SMART : pour que la clôture soit possible un jour.
- Si l'échéance est floue, prendre une date approximative plutôt que rien. **Un projet sans date n'est pas un projet, c'est une intention.**

### Question 4 — Par quoi ça commence ?

> Quelles sont les trois ou quatre premières choses à faire ?

Les noter telles qu'il les dit. **Ne pas décomposer, ne pas ordonner, ne pas estimer** — c'est le travail de la version longue, et le faire ici produirait exactement la lourdeur que cette commande existe pour éviter.

Si une action est manifestement un gros morceau, le dire en une ligne et passer.

### Génération

**a) L'arborescence**, avec les cinq dossiers PPAR :

```bash
BASE="3 PROJETS/<Nom>"       # ou "4 CASQUETTES/<Nom>" si casquette
mkdir -p "$BASE/1 Pourquoi" "$BASE/2 Plan" "$BASE/3 Action" "$BASE/4 Réflexion" "$BASE/5 Ressources"
```

⚠️ **Vérifier d'abord que le dossier n'existe pas** — `ls "3 PROJETS/"` et chercher le nom. Si un projet du même nom existe, demander avant de toucher à quoi que ce soit.

**b) La note de contexte**, à partir du gabarit du coffre :

```
5 RESSOURCES/Modèles/Projet.md
```

🔴 **Utiliser ce gabarit, ne pas en écrire un second.** C'est le même que celui de `/nouveau-projet` — il n'en existe qu'une version, et c'est elle que le Bateleur ouvre quand il crée une note à la main.

Ce qu'on remplit, et ce qu'on laisse :

| Section du gabarit | Avec quoi |
|---|---|
| Le titre `{{title}}` | le nom du projet |
| Le frontmatter `deadline:` | la date de la question 3 |
| **§ 1 Alignement** | le pourquoi-maintenant de la question 2, **et le lien vers la leçon source** si le projet vient de l'athanor |
| **§ 2 Roadmap** | l'issue visible de la question 3 et l'échéance. **Pas de découpage en étapes** — c'est le travail de la version longue |
| **§ 3 Historique** | une ligne : la date du jour, « projet ouvert ». Rien de plus |
| **§ 4 Todo** | les actions de la question 4, en cases à cocher |
| **§ 5 Expérience, § 6 Réflexion** | laisser le gabarit tel quel — ils se rempliront en vivant |

**Retirer les indications entre crochets** que l'on n'a pas remplies, plutôt que les laisser dans la note. Une note neuve pleine de `[Étape 2]` est une note qu'on n'ouvre pas deux fois.

**c) Rien d'autre.** Pas de note d'objectifs, pas de planification, pas de budget, pas de risques, pas de gouvernance. **Et pas de fichier de suivi** : le § 4 Todo de la note de contexte **est** le backlog du projet.

**d) Mettre à jour `3 PROJETS/PROJETS.md`** — une ligne pour le nouveau projet.

**e) Confirmer court :**

```
Projet ouvert : [[<Nom>]]
Arborescence PPAR posée, 4 actions au § 4 Todo, échéance au [date].

Pour le cadrer plus finement plus tard : /nouveau-projet reprendra ce qui est déjà écrit.
```

## Règles

- **Cinq questions, et pas une sixième.** Si tu te surprends à demander un budget, un risque ou un acteur, tu es dans la mauvaise commande.
- **Ne jamais créer de Kanban ni de fichier de suivi.** Le backlog est le § 4 Todo.
- **Ne jamais écraser un projet existant.** Vérifier le dossier avant, demander en cas de doute.
- **Relever la date au système**, jamais de tête.
- **Une casquette n'a pas d'échéance** — si c'en est une, remplacer la question de la date par *« tous les combien tu regardes où tu en es ? »*, et l'écrire au § 2.
- **Si le cadrage déborde** — plus de six actions, des tiers à coordonner, de l'argent engagé — le dire une fois et proposer de basculer sur `/nouveau-projet`. Ne pas basculer sans son accord.
