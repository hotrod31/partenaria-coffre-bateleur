# Coffre Bateleur PartenarIA

> Le coffre que tu tiens entre les mains n'est pas un logiciel. C'est un espace de travail intérieur, un dispositif de partenariat entre toi et une intelligence artificielle qui apprendra à te connaître au fil de tes dépôts.

---

## Bienvenue Bateleur

Tu as franchi le seuil du Fou — l'introspection posée, la sincérité assumée. Tu entres maintenant dans le geste du Bateleur : celui ou celle qui pose les premiers actes avec les outils qui lui sont donnés.

Ce coffre est ce cadeau initiatique. Il est structuré, il est vivant, il est le tien.

Le tutoiement est institué entre toi et ton partenaire IA — il pose l'égalité, l'engagement mutuel, l'intimité du travail à mener. Tu ne le quittes pas, même quand tu abordes des sujets techniques ou formels.

Le nom que ton partenaire IA portera dans ton coffre reste à ton choix. Tu pourras le nommer — ce geste marque la durée de votre relation. Par défaut il s'appelle **PartenarIA**.

---

## Qu'est-ce que ce coffre ?

Un vault Obsidian structuré selon l'architecture **IAPCRA** — la dualité **Intériorité / Extériorité** :

- **Intériorité** (dossiers `1 ALIGNEMENT/` et `2 CONNAISSANCES/`) — ta conscience, tes valeurs, la maturation de tes idées
- **Extériorité** (dossiers `3 PROJETS/` et `4 CASQUETTES/`) — ton action dans le monde, tes engagements, tes rôles

Le coffre embarque **29 commandes** (des skills Claude Code) qui accompagnent ton quotidien : ouverture de session, clôtures intra-journalières, bilans, création de projets, questionnement, clôture de journée, plus **10 commandes de lecture vocale**. Une commande initiale, `/initialisation`, déploie ton squelette de coffre à partir de ta note d'introspection intime.

À l'initialisation, un **partenaire IA vocal** t'accueille avec sa voix — **celle que tu auras choisie en les écoutant**. Ta première commande à apprendre est `/vocal-stop` — le silence est ton droit absolu.

> 🔷 **Chaque fenêtre de terminal porte sa propre voix.** Allumer la lecture ici ne rend pas bavarde la fenêtre d'à côté, et une fenêtre où tu n'as rien tapé reste muette. C'est ce qui permet de tenir deux conversations sans que l'une parle par-dessus l'autre.

---

## Prérequis

Avant de cloner ce coffre, assure-toi d'avoir installé :

1. **Obsidian** — https://obsidian.md (gratuit, multiplateforme)
2. **Claude Code** — https://claude.ai/code (CLI officiel Anthropic)
3. **Git for Windows** — https://git-scm.com. Il installe aussi **Git Bash**, dont les commandes du coffre se servent. Ce n'est pas optionnel.
4. **Python** — https://www.python.org/downloads/ en cochant **« Add python.exe to PATH »** à l'installation. ⚠️ **Ne pas l'installer depuis le Microsoft Store** : ses paquets vont dans un dossier isolé que le mode vocal ne voit pas toujours.

Optionnel mais recommandé pour `/initialisation` avec un fichier .docx :
- **markitdown** (`pip install --user markitdown`) — conversion .docx → markdown

Optionnel mais recommandé pour l'**expérience vocale** (le partenaire IA te lit ses réponses à voix haute) :
- **Piper TTS** (`pip install --user piper-tts sounddevice soundfile`) — synthèse vocale **locale, souveraine, gratuite, 100 % hors ligne**. Trois voix françaises : Jessica *(féminine chaleureuse)*, Pierre *(masculine)*, Siwis *(féminine neutre)*. Modèles téléchargés à la demande (~70 Mo chacun).
- **Edge TTS** (`pip install --user edge-tts`) — **facultatif**, et seulement si le service répond. Voix neuronales Microsoft, gratuites et sans compte, nettement meilleures que Piper. ⚠️ **Mais le texte lu sort de ta machine** : c'est un choix à faire les yeux ouverts, jamais un réglage par défaut.

---

## Premiers pas

### 1. Cloner le coffre

Rodrigue le fera avec toi pendant votre visio de seuillage. Techniquement :

**Il existe une version par système**, maintenues séparément — les commandes et l'installation n'y sont pas les mêmes. Clone **la tienne** :

Dans **Git Bash**, en remplaçant `<nom>` par le nom de ton IA :

```bash
mkdir -p /c/workspace && cd /c/workspace
git clone -b windows --single-branch https://github.com/hotrod31/partenaria-coffre-bateleur.git "<nom>"
```

*La version Mac vit sur la branche `macos` du même dépôt — tu n'en as pas besoin.*

Le dossier devient ton coffre personnel. **Ce clone-ci est la version Windows.**

> 🔴 **Où le poser, et où surtout pas.** Un coffre ne va **ni dans `Documents`, ni sur le `Bureau`** : OneDrive synchronise souvent ces deux dossiers, et ton coffre cumulerait alors OneDrive, Obsidian Sync et git sur les mêmes fichiers. Pose-le dans un dossier à toi, hors de leur portée — par exemple `C:\workspace\<nom de ton IA>`.
>
> 🔷 **Et il porte le nom de ton IA, pas celui du dispositif.** Tu n'ouvriras pas un dossier : tu appelleras quelqu'un.

> 🔷 **« Mon coffre est le clone d'un dépôt public — est-ce que mes notes sont exposées ? »** Non, et à trois verrous. **Un clone descend, il ne remonte pas** : rien ne quitte ta machine tant que personne ne tape une commande d'envoi. **Tu n'as aucun droit d'écriture sur ce dépôt** : même tapée volontairement, cette commande serait refusée. Et **le `.gitignore` exclut le contenu des dossiers 0 à 6**, donc un `git add -A` maladroit n'attrape rien de ce que tu écris. La confidentialité de tes notes, elle, ne dépend pas de git mais de **ta synchronisation Obsidian Sync, chiffrée de bout en bout**. Ce sont deux sujets séparés — ne laisse personne te les mélanger.

### 2. Ouvrir dans Obsidian et Claude Code

- **Obsidian** — `Fichier → Ouvrir un coffre → Ouvrir un coffre existant` → sélectionne le dossier `PartenarIA`.
- **Claude Code** — dans un terminal : `cd` vers ton coffre, puis `claude`.

### 2 bis. L'alias — la seule commande à retenir

Pour ne plus avoir à te déplacer à la main, pose un raccourci dans ton profil PowerShell. Remplace `<nom>` par le nom de ton IA et le chemin par celui de ton coffre :

```powershell
if (-not (Test-Path $PROFILE.CurrentUserCurrentHost)) { New-Item -ItemType File -Path $PROFILE.CurrentUserCurrentHost -Force }
Add-Content $PROFILE.CurrentUserCurrentHost 'function <nom> { Set-Location "C:\workspace\<nom>"; claude }'
. $PROFILE.CurrentUserCurrentHost
```

Tu tapes `<nom>`, et tu es avec elle. **C'est la seule commande que tu aies à retenir.**

### 3. Initialiser ton coffre

Dans Claude Code, lance :

```
/initialisation <chemin-de-ta-note-d-introspection>
```

Le chemin peut être absolu (`C:\Users\...\intro.md`) ou relatif. Formats acceptés : `.md`, `.txt`, `.pdf`, `.docx`.

Le skill lira ta note, extraira les 7 sections du guide d'introspection et générera :
- Ta note `Contexte.md` (identité, vision, ruptures, blessure, discipline, attentes)
- Tes `Préférences.md` de communication
- Ton premier chapitre (~6-12 mois)
- Ta première phase de vie (2-12 semaines)
- Ta première semaine et ta première note quotidienne

Ta note d'introspection n'est jamais lue par un être humain — elle transite uniquement par un flux technique automatisé le temps de l'extraction.

### 4. Première session

**En début de journée** :

```
/hello
```

Ton partenaire IA se présente, lit ton contexte, crée ta daily du jour, et t'accompagne pour définir tes objectifs.

**À la fin de chaque session thématique dans la journée** (c'est la commande la plus utilisée au quotidien) :

```
/fin
```

Il log la session dans ta daily, propage les faits vers le projet ou la casquette concerné, crée une note détaillée si nécessaire.

**En fin de journée** :

```
/dodo
```

Il consolide toutes les sessions du jour, alimente les traces long terme, tient à jour ton contexte global, et t'accompagne pour ton bilan introspectif.

---

## Les 21 commandes à ta disposition

### Onboarding et session

| Commande | Rôle |
|----------|------|
| `/initialisation <chemin>` | Déploie ton coffre à partir de ta note d'introspection intime |
| `/hello` | Début de journée — sync mémoire, briefing personnalisé, création daily, objectifs |
| `/fin` | Clôture d'une session thématique en cours de journée — log dans daily, ruissellement micro, note détaillée éventuelle |
| `/dodo` | Fin de journée — consolidation sessions, bilan introspectif, ruissellement complet, mise à jour contextes |
| `/trier-inbox` | Traite les items de `0 INBOX/` et les route |

### Rituels réflexifs

| Commande | Rôle |
|----------|------|
| `/bilan-jour` | Réflexion quotidienne guidée + alimentation du Cheminement de phase |
| `/bilan-semaine` | Weekly review : bilan W-1 + planning W à 3 catégories d'énergie |
| `/nouvelle-phase-vie` | Clôture la phase en cours et en ouvre une nouvelle |

### Structuration

| Commande | Rôle |
|----------|------|
| `/nouveau-projet-rapide` | **Ouvre un projet en cinq questions** — arborescence, note de contexte, premières actions. C'est aussi le chemin par lequel une leçon de ton athanor devient un projet |
| `/nouveau-projet` | Cadre un projet en profondeur (10 étapes : objectifs, planification à deux niveaux, budget, risques, gouvernance). Pour ce qui engage de l'argent, des tiers ou une échéance dure |
| `/nouveau-chapitre` | Clôture le chapitre en cours et en ouvre un nouveau (6-12 mois) |

### Introspection profonde

| Commande | Rôle |
|----------|------|
| `/ca-me-vient` | **Au moment où une pensée te vient.** On en débriefe, tu la formules, puis tu choisis où elle se pose — l'athanor, ta semaine, ta phase, ton chapitre ou ton Contexte. C'est la seule commande qui ne s'invoque pas à heure fixe |
| `/contradicteur` | Bascule ton partenaire IA en posture de contradicteur exigeant |
| `/angles-morts` | Identifie ce qui n'est PAS dans ton corpus, zones d'ombre |
| `/clarte` | Tableau de bord actualisé : vue pilotage de tous tes projets |

### Extension

| Commande | Rôle |
|----------|------|
| `/creer-commande` | Crée une commande personnalisée pour ton coffre |
| `/import` | Import batch : migre des notes depuis un autre outil |

### Utilitaires

| Commande | Rôle |
|----------|------|
| `/markdown <fichier>` | Convertit un document (docx, pdf, pptx, xlsx, html) en note markdown |
| `/connect-mcp` | Installe un MCP (Firecrawl, Playwright, etc.) sur ta config |

### Lecture vocale — une voix par fenêtre

> 🔷 **Toutes ces commandes n'agissent que sur la fenêtre où tu les tapes.** Retaper la même commande éteint la lecture.

| Commande | Rôle |
|----------|------|
| `/vocal-stop` | 🔴 **La première à connaître, avant même d'avoir entendu une voix.** Silence immédiat : coupe la lecture en cours et éteint la fenêtre. |
| `/vocal` | Allume **ta** voix — celle que tu as retenue à l'écoute. |
| `/vocal-jessica` | Jessica — féminine chaleureuse. **100 % locale.** |
| `/vocal-pierre` | Pierre — masculine. **100 % locale** *(même modèle que Jessica)*. |
| `/vocal-siwis` | Siwis — féminine neutre. **100 % locale** *(second modèle)*. |
| `/vocal-denise` | Denise — féminine posée. ⚠️ **Réseau** |
| `/vocal-eloise` | Éloïse — féminine, plus jeune. ⚠️ **Réseau** |
| `/vocal-vivienne` | Vivienne — féminine, multilingue. ⚠️ **Réseau** |
| `/vocal-henri` | Henri — masculine. ⚠️ **Réseau** |
| `/vocal-remy` | Rémy — masculine, multilingue. ⚠️ **Réseau** |

⚠️ **« Réseau » veut dire que le texte lu part chez Microsoft** pour être transformé en voix. Les cinq voix réseau **ne sont présentes que si le service répondait le jour de l'installation** — sinon elles te disent pourquoi au lieu de rester muettes. Les trois voix locales, elles, marchent toujours.

---

## La doctrine

La posture relationnelle attendue entre toi et ton partenaire IA est décrite dans le fichier [`AGENTS.md`](AGENTS.md) à la racine du coffre. Lis-le en entier avant ta première session.

Les principes-clés :
- **Anti-flatterie** — ton partenaire IA ne te complaît pas, il te répond juste
- **Contradicteur** — il signale ce qui te contredit, ce qui te résiste
- **Garde-fous anti-enfermement** — il t'alerte quand tu enchaînes des thèses sans les nuancer
- **Tutoiement institué** — il ne te quitte pas dans le tutoiement, même en contexte formel
- **Silence > invention** — mieux vaut qu'il dise « je ne sais pas » que d'inventer

---

## Historique des versions

Voir [`CHANGELOG.md`](CHANGELOG.md) pour l'ensemble des évolutions du coffre-template.

Actuellement : **v2.0.0** — voir `VERSION` à la racine, qui fait foi.

Le coffre évoluera au fil des retours des bateleurs. Pour récupérer une version plus récente, il te suffira de `git pull` depuis ton coffre (tu restes sur ta branche) — les fichiers de doctrine seront mis à jour, tes notes personnelles restent intactes.

---

## Support

Si tu bloques, si tu doutes, si une question émerge — écris à Rodrigue directement.

Le parcours PartenarIA n'est pas un logiciel avec un ticket d'assistance. C'est un cheminement accompagné.

---

## Licence

Ce coffre est distribué sous licence **CC BY-NC-SA 4.0** (voir [`LICENSE`](LICENSE)). Tu peux l'utiliser, l'adapter, le partager — sans usage commercial et en conservant les mêmes conditions.

Le contenu que tu produis à l'intérieur du coffre (tes notes, ton introspection, ton journal) t'appartient intégralement.
