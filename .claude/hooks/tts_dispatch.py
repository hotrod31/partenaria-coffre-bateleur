"""
tts_dispatch.py - Point d'entree du hook Stop. Choisit le moteur, passe la main.

Son travail, et rien d'autre :
  1. demander a tts_session.py ce que LA FENETRE appelante doit jouer
  2. si elle est muette, sortir sans bruit
  3. sinon, lancer le bon moteur en lui posant la voix dans TTS_SESSION_VOICE

Deux moteurs :

  piper  - 100 % local, aucun appel reseau. Le moteur souverain.
           Voix : jessica (defaut), pierre, siwis
  edge   - voix neuronales Microsoft, gratuites et sans cle, mais LE TEXTE
           SORT DE LA MACHINE. Qualite tres superieure a piper.
           Voix : denise, eloise, vivienne, henri, remy
           Installe seulement si le service repondait a l'installation.

POURQUOI UN DISPATCHER PLUTOT QU'UN APPEL DIRECT AU MOTEUR. Le hook Stop vit
dans settings.local.json, qui est VERSIONNE dans le depot. Le changer a chaque
bascule de moteur creerait un conflit au premier `git pull`. Ici le fichier
settings ne bouge jamais : c'est l'etat de la fenetre qu'on ecrit, et il
n'est pas suivi par git.

Usage :
  python tts_dispatch.py              (hook Stop : charge utile JSON sur stdin)
  python tts_dispatch.py "Texte"
  echo "Texte" | python tts_dispatch.py --stdin
  python tts_dispatch.py --file <chemin>
  python tts_dispatch.py --kill       (silence immediat, sur les deux moteurs)
"""

import os
import subprocess
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(HOOKS_DIR))
import tts_session  # noqa: E402

MOTEURS = {
    "piper": HOOKS_DIR / "piper_tts.py",
    "edge": HOOKS_DIR / "edge_tts_speak.py",
}


def script_du_moteur(nom):
    """Le script du moteur demande, ou piper en repli, ou None si rien.

    Un moteur demande mais absent retombe sur piper : mieux vaut une voix
    moins belle qu'un silence qu'on mettra une semaine a comprendre.
    """
    chemin = MOTEURS.get(nom)
    if chemin is not None and chemin.exists():
        return chemin
    repli = MOTEURS["piper"]
    if repli.exists():
        if nom != "piper":
            sys.stderr.write(
                "tts_dispatch : moteur '%s' demande mais absent, repli sur piper\n" % nom)
        return repli
    return None


def relayer(script, args, entree, voix=None):
    env = os.environ.copy()
    if voix:
        # Les deux moteurs lisent cette variable avant tout fichier : c'est
        # elle qui porte la voix PROPRE A CETTE FENETRE.
        env["TTS_SESSION_VOICE"] = voix
    try:
        proc = subprocess.Popen(
            [sys.executable, str(script)] + list(args),
            stdin=subprocess.PIPE, env=env)
        proc.communicate(input=entree)
        return proc.returncode or 0
    except Exception as exc:
        sys.stderr.write("tts_dispatch : %s\n" % exc)
        return 1


def main():
    args = sys.argv[1:]

    # --kill ne regarde ni l'etat ni le moteur actif : on veut le silence, et
    # une lecture peut etre en cours sur l'autre moteur.
    if args and args[0] == "--kill":
        code = 0
        for chemin in MOTEURS.values():
            if chemin.exists():
                code = relayer(chemin, ["--kill"], b"") or code
        return code

    # On lit toujours stdin, meme pour ne rien faire ensuite : laisser le
    # tuyau du hook plein bloquerait l'appelant.
    entree = b""
    if not args or args[0] == "--stdin":
        try:
            entree = sys.stdin.buffer.read()
        except Exception:
            entree = b""

    moteur, voix = tts_session.resoudre()

    # Hook Stop sur une fenetre muette : on sort sans bruit. C'est le cas
    # NORMAL d'une fenetre ou personne n'a tape /vocal-*.
    if not args and moteur is None:
        return 0

    if moteur is None:
        moteur, voix = "piper", tts_session.VOIX_DEFAUT["piper"]

    script = script_du_moteur(moteur)
    if script is None:
        sys.stderr.write("tts_dispatch : aucun moteur installe dans ce coffre\n")
        return 1

    return relayer(script, args, entree, voix)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.stderr.write("tts_dispatch erreur : %s: %s\n" % (type(exc).__name__, exc))
        sys.exit(1)
