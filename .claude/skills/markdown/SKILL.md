---
name: markdown
description: "Convertit un document (docx, pdf, pptx, xlsx, html, etc.) en note markdown dans le coffre via markitdown, avec wikilink vers le fichier source. Usage : /markdown <chemin du document>"
argument: source_path
---

# Commande /markdown

Tu convertis un document (Word, PDF, PowerPoint, Excel, HTML, audio, etc.) en note markdown dans le coffre en utilisant **markitdown** (Microsoft, https://github.com/microsoft/markitdown). La note conserve un **wikilink Obsidian** vers le fichier source pour que l'utilisateur puisse rouvrir l'original depuis Obsidian.

## Paramètres

- **Chemin source** : `$ARGUMENTS`
- **Destination** : **même dossier que le source si dans le coffre, sinon `0 INBOX/`** (cf. V1.1 ci-dessous)
- **Outil de conversion** : `markitdown` (installé globalement, Python 3.13)

## Conventions arbitrées (V1.1 — 06/06/2026)

1. **Si le source est HORS du coffre** → copie du source dans `0 INBOX/` + note convertie dans `0 INBOX/` (wikilink valide). Cas typique : docx reçu par mail dans Downloads.
2. **Si le source est DANS le coffre** → pas de copie, **la note convertie va dans le même dossier que le source**. Cas typique : transcription Upmeet déjà rangée dans `4 Ressources/` d'un projet → la version markdown va dans `4 Ressources/` aussi.
3. **Cas particulier du source dans `0 INBOX/`** → note convertie reste dans `0 INBOX/` (cohérent avec la règle 2, c'est juste un sous-cas).
4. La destination est **affichée explicitement dans la confirmation finale** pour que l'utilisateur puisse la déplacer s'il le souhaite.

> Évolution V1 → V1.1 : la V1 (05/06/2026) plaçait systématiquement la note convertie dans `0 INBOX/`, ce qui cassait le rangement existant quand le source était déjà dans un projet. V1.1 fait suivre la note au source. Idée d'évolution V1.2 future : si le sous-dossier source est `4 Ressources/` mais que le contenu converti ressemble à un CR ou une action, proposer un dossier alternatif (`3 Action/`). À voir à l'usage.

## Formats supportés par markitdown

| Format | Extension(s) | Notes |
|---|---|---|
| Word | `.docx` | Texte + structure conservée |
| PDF | `.pdf` | OCR non inclus — PDF scanné = pauvre |
| PowerPoint | `.pptx` | Slides en sections, notes incluses |
| Excel | `.xlsx`, `.xls` | Tableaux convertis en tables markdown |
| HTML | `.html`, `.htm` | Conversion via markdownify |
| Audio | `.mp3`, `.wav`, `.m4a` | Transcription via speech recognition |
| Texte | `.txt`, `.csv`, `.json`, `.xml` | Conversion directe |
| Images | `.jpg`, `.png` | OCR via Azure Document Intelligence (config requise) |
| Archives | `.zip` | Décompresse et convertit le contenu |
| Notebooks | `.ipynb` | Cellules + outputs |

## Instructions

### 1. Valider le chemin source

- Récupère le chemin depuis `$ARGUMENTS` (peut être Windows `C:\...` ou Unix `/c/Users/...`).
- Normalise le chemin (`cygpath -u` si nécessaire pour Bash, ou garde Windows tel quel).
- Vérifie que le fichier existe (`test -f`).
- Si le fichier n'existe pas, affiche une erreur claire et stoppe.
- Extrais le nom du fichier source (avec extension) et le nom sans extension.

### 2. Déterminer si le fichier est dans le coffre

Détecter dynamiquement la racine du coffre (utiliser `pwd` ou détecter le dossier contenant `AGENTS.md`). Si le chemin source absolu commence par cette racine, le fichier est **dans** le coffre. Sinon, il est **hors** du coffre.

### 3. Déterminer la destination de la note convertie + gérer la copie si source hors coffre

#### Cas A — Fichier dans le coffre

- **Pas de copie** du fichier source.
- **Destination de la note convertie = dossier du source** (V1.1).
  - Source `0 INBOX/doc.docx` → note dans `0 INBOX/`
  - Source `3 PROJETS/MonProjet/5 Ressources/doc.docx` → note dans `3 PROJETS/MonProjet/5 Ressources/`
  - Source `4 CASQUETTES/MaCasquette/5 Ressources/doc.docx` → note dans `4 CASQUETTES/MaCasquette/5 Ressources/`
- Wikilink : `[[<nom du fichier complet avec extension>]]` (Obsidian résout automatiquement par nom dans tout le coffre).

#### Cas B — Fichier hors du coffre

- **Destination de la copie source** : `0 INBOX/<nom du fichier complet avec extension>`.
- Copie le fichier source vers cette destination (`cp`).
- Si le nom existe déjà dans `0 INBOX/`, ajoute un suffixe `-2`, `-3`, etc. avant l'extension.
- **Destination de la note convertie** : `0 INBOX/` (à côté de la copie source).
- Wikilink : `[[<nom du fichier copié avec extension>]]`.

### 4. Convertir avec markitdown

Lance markitdown sur le fichier (source si dans le coffre, copie si hors coffre) :

```bash
python3 -m markitdown "<chemin du fichier à convertir>" > /tmp/markitdown_out.md 2>/tmp/markitdown_err.log
```

- Si la conversion échoue (exit code ≠ 0), affiche le contenu de `/tmp/markitdown_err.log` à l'utilisateur et stoppe.
- Si la sortie est vide ou trivialement courte (< 20 caractères), alerte l'utilisateur (souvent : PDF scanné sans OCR, image illisible, audio sans audio reconnaissable).

Lis le contenu converti depuis `/tmp/markitdown_out.md`.

### 5. Construire le nom de la note markdown

Format : `<préfixe-date> <nom-fichier-source-sans-extension>.md`

- **Préfixe-date** : la date du jour au format `YYYY-MM-DD - ` (avec espace après le tiret).
- **Exception** : si le nom du fichier source commence DÉJÀ par une date au format `YYYY-MM-DD` (regex `^\d{4}-\d{2}-\d{2}`), n'ajoute pas de préfixe (sinon on aurait `2026-06-06 - 2026-06-05 - Doc.md`, redondant).
- Nettoie le nom : remplace les caractères incompatibles Windows (`<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`) par `-`.
- Tronque à 100 caractères max (extension `.md` comprise) si nécessaire.

Exemples :
- Source `GERONTOPOLE 2026-06-05.docx`, conversion 2026-06-06 → note `2026-06-06 - GERONTOPOLE 2026-06-05.md`
- Source `2026-06-05 - Réunion ESEA.docx` → note `2026-06-05 - Réunion ESEA.md` (date préservée, pas de double préfixe)
- Source `Compte rendu Q1 2026.pdf` → note `2026-06-06 - Compte rendu Q1 2026.md`

### 6. Construire le contenu de la note markdown

```markdown
---
type: import
source: "[[<nom du fichier source avec extension>]]"
source-format: <extension sans le point>
source-path-original: "<chemin absolu original avant copie, vide si fichier déjà dans le coffre>"
date_import: <YYYY-MM-DD du jour>
tool: markitdown
tags:
  - import
  - markitdown
---

# <Titre court — nom du fichier source sans extension>

> Conversion automatique du document **[[<nom du fichier source avec extension>]]** via markitdown le <YYYY-MM-DD du jour>. Cliquer le wikilink pour ouvrir l'original.

---

<contenu markdown converti par markitdown>
```

### 7. Écrire la note dans le coffre

Crée le fichier `<dossier destination>/<nom-note>.md` avec le contenu ci-dessus (outil Write).

Le `<dossier destination>` est celui déterminé à l'étape 3 :
- Cas A (source dans le coffre) = dossier du source
- Cas B (source hors coffre) = `0 INBOX/`

Si le nom de note existe déjà dans le dossier de destination, ajoute un suffixe `-2`, `-3`, etc. avant `.md` (cohérent avec le suffixe de la copie source si applicable).

### 8. Confirmer à l'utilisateur

Affiche un message synthétique :

```
Note créée : <dossier destination>/<nom-note>.md
Source : <nom du fichier source> (<dans le coffre | hors coffre, copié dans 0 INBOX/>)
Format détecté : <extension>
Longueur convertie : <nombre de caractères ou lignes>
Règle V1.1 appliquée : <dossier source = dossier note | source hors coffre → INBOX>
```

Si la conversion a produit un contenu très court ou suspect (PDF scanné sans OCR, audio muet), signale-le explicitement.

## Notes techniques

- **markitdown gère les images embarquées** dans les docx/pptx en les référençant comme `![](image_path)`, mais ne les extrait pas par défaut. Pour cette V1, on garde le markdown brut sans extraction d'images.
- **OCR sur images / PDF scannés** = nécessite Azure Document Intelligence (config supplémentaire, non activée). PDF texte natif fonctionne directement.
- **Audio** = la transcription Speech Recognition de markitdown est de qualité limitée. Pour des transcriptions de qualité, préférer un outil dédié (Whisper local, service de transcription) puis importer le résultat texte.
- **Sortie en français** : markitdown préserve la langue du document source. Si l'original est en français, la sortie l'est aussi (accents inclus).

## Cas d'usage typiques

| Cas | Exemple | Commande | Destination note (V1.1) |
|---|---|---|---|
| Word reçu par mail dans Downloads | Compte-rendu de réunion | `/markdown ~/Downloads/CR-reunion.docx` | `0 INBOX/` (+ copie source dans INBOX) |
| PDF de référence technique | Doc de spec | `/markdown ~/Downloads/spec.pdf` | `0 INBOX/` (+ copie source dans INBOX) |
| Slides reçues d'un confrère | Présentation PowerPoint | `/markdown "~/Downloads/Présentation.pptx"` | `0 INBOX/` (+ copie source dans INBOX) |
| Excel partagé | Tableau de bord | `/markdown "~/Downloads/tableau.xlsx"` | `0 INBOX/` (+ copie source dans INBOX) |
| HTML archivé | Article web sauvegardé | `/markdown ~/Downloads/article.html` | `0 INBOX/` (+ copie source dans INBOX) |
| Document déjà dans `0 INBOX/` | Transcription brute | `/markdown "0 INBOX/transcription.docx"` | `0 INBOX/` (même dossier) |
| Document déjà rangé dans un projet | Doc déposé dans Ressources d'un projet | `/markdown "3 PROJETS/MonProjet/5 Ressources/doc.docx"` | `3 PROJETS/MonProjet/5 Ressources/` (même dossier) |
| Document dans une casquette | Doc dans une casquette | `/markdown "4 CASQUETTES/MaCasquette/5 Ressources/doc.docx"` | `4 CASQUETTES/MaCasquette/5 Ressources/` (même dossier) |

## En cas d'erreur

- **`markitdown: command not found`** → markitdown n'est pas installé. Lance `pip3 install --user 'markitdown[all]'`. Si Homebrew refuse l'installation (« externally-managed-environment », PEP 668), ajoute `--break-system-packages` ou installe dans un environnement virtuel.
- **Sortie vide ou très courte** → souvent PDF scanné sans OCR (texte présent visuellement mais pas extractible). Alerte l'utilisateur, propose une alternative manuelle (capture + OCR séparé).
- **Erreur d'encodage** → markitdown s'attend à UTF-8 en sortie. Si caractères corrompus, vérifier `chcp` (CP1252 Windows par défaut). Forcer `PYTHONIOENCODING=utf-8` dans le shell avant l'appel.
- **Fichier source verrouillé** (Office ouvert) → fermer le fichier dans Office, retenter.
