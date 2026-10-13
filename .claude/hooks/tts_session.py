"""
tts_session.py - La lecture vocale, fenetre par fenetre.

CE QUI EST EN JEU. Sans ce fichier, un seul drapeau `tts_enabled` commandait
TOUTES les fenetres de terminal ouvertes : allumer la voix ici la rendait
bavarde la-bas, et l'eteindre la-bas te rendait muet ici. Avec plusieurs
conversations ouvertes en parallele, c'est inutilisable.

Ici, CHAQUE FENETRE PORTE SA PROPRE VOIX. Une fenetre ou tu n'as rien tape
reste muette, et `/vocal-stop` n'y coupe rien.

L'etat d'une fenetre vit dans sessions/<identifiant>.json :

    {"engine": "piper", "voice": "jessica"}

  fiche absente  ->  cette fenetre est muette
  fiche presente ->  elle lit, avec ce moteur et cette voix

REPLI HORS SESSION. Quand l'identifiant de fenetre n'est pas fourni -- appel
a la main depuis un terminal, runtime qui ne le pose pas -- on retombe sur
les anciens fichiers partages (tts_enabled, tts_engine, tts_piper_voice,
tts_edge_voice). Ce repli garde les appels manuels fonctionnels ; il n'est
pas le chemin normal.

Rien de ce que ce fichier ecrit n'est versionne : voir .gitignore.
"""

import json
import os
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.resolve()
SESSIONS_DIR = HOOKS_DIR / "sessions"

# Les fichiers du repli hors session, ceux d'avant le 13/10/2026.
FLAG_GLOBAL = HOOKS_DIR / "tts_enabled"
ENGINE_GLOBAL = HOOKS_DIR / "tts_engine"
VOIX_GLOBALE = {
    "piper": HOOKS_DIR / "tts_piper_voice",
    "edge": HOOKS_DIR / "tts_edge_voice",
}

MOTEURS = ("piper", "edge")
MOTEUR_DEFAUT = "piper"
VOIX_DEFAUT = {"piper": "jessica", "edge": "denise"}


def session_id_courante():
    """L'identifiant de la fenetre appelante, ou None hors session.

    Trois noms acceptes : Claude Code pose le premier, et les deux autres
    permettent de forcer la main depuis un script ou un autre runtime.
    """
    for var in ("CLAUDE_CODE_SESSION_ID", "TTS_SESSION_ID", "OPENCODE_SESSION_ID"):
        val = os.environ.get(var, "").strip()
        if val:
            return val
    return None


def _assainir(session_id):
    """Un identifiant ne doit jamais pouvoir sortir du dossier sessions/.

    Sans ce filtre, un identifiant contenant ../ ferait ecrire la fiche
    n'importe ou sur le disque.
    """
    return "".join(c for c in str(session_id) if c.isalnum() or c in "-_")[:128]


def fiche(session_id):
    return SESSIONS_DIR / ("%s.json" % _assainir(session_id))


def etat_session(session_id):
    """Rend (moteur, voix) pour cette fenetre, ou (None, None) si muette."""
    chemin = fiche(session_id)
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return (None, None)
    moteur = str(donnees.get("engine", "")).strip().lower()
    voix = str(donnees.get("voice", "")).strip().lower()
    if moteur not in MOTEURS:
        return (None, None)
    if not voix:
        voix = VOIX_DEFAUT[moteur]
    return (moteur, voix)


def activer(session_id, moteur, voix):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    fiche(session_id).write_text(
        json.dumps({"engine": moteur, "voice": voix}, ensure_ascii=False),
        encoding="utf-8")


def desactiver(session_id):
    """Rend la fenetre muette en retirant sa fiche. Sans effet si deja muette."""
    try:
        fiche(session_id).unlink()
    except OSError:
        pass


def etat_global():
    """Le repli : (moteur, voix) des fichiers partages, ou (None, None)."""
    if not FLAG_GLOBAL.exists():
        return (None, None)
    moteur = MOTEUR_DEFAUT
    try:
        lu = ENGINE_GLOBAL.read_text(encoding="utf-8").strip().lower()
        if lu in MOTEURS:
            moteur = lu
    except OSError:
        pass
    voix = VOIX_DEFAUT[moteur]
    fichier = VOIX_GLOBALE.get(moteur)
    if fichier is not None:
        try:
            lu = fichier.read_text(encoding="utf-8").strip().lower()
            if lu:
                voix = lu
        except OSError:
            pass
    return (moteur, voix)


def activer_global(moteur, voix):
    FLAG_GLOBAL.touch()
    ENGINE_GLOBAL.write_text(moteur, encoding="utf-8")
    fichier = VOIX_GLOBALE.get(moteur)
    if fichier is not None:
        fichier.write_text(voix, encoding="utf-8")


def desactiver_global():
    try:
        FLAG_GLOBAL.unlink()
    except OSError:
        pass


def resoudre():
    """Ce que la fenetre appelante doit jouer : (moteur, voix) ou (None, None).

    C'est la fonction que le hook Stop interroge. Une fenetre sans fiche est
    muette -- elle ne retombe PAS sur le reglage global, sinon une fenetre
    qu'on vient de faire taire se remettrait a parler.
    """
    sid = session_id_courante()
    if sid is None:
        return etat_global()
    return etat_session(sid)
