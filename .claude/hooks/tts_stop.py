"""
tts_stop.py - Le silence, pour CETTE fenetre, tout de suite.

Appele par /vocal-stop. Deux gestes, dans cet ordre, et l'ordre compte :

  1. couper la lecture EN COURS -- via tts_dispatch.py --kill, qui coupe LES
     DEUX moteurs. Une lecture peut etre en cours sur piper alors qu'edge est
     devenu l'actif ; n'en couper qu'un laisserait l'autre parler.
  2. rendre la fenetre muette -- en retirant sa fiche de session.

Le silence d'abord, le reglage ensuite : quelqu'un qui tape /vocal-stop veut
que ca s'arrete maintenant, pas apres une ecriture de fichier.

Le choix de voix n'est PAS efface. Rallumer avec une commande /vocal-*
retrouve la voix precedente.
"""

import subprocess
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(HOOKS_DIR))
import tts_session  # noqa: E402

for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    # 1. le silence immediat
    dispatch = HOOKS_DIR / "tts_dispatch.py"
    if dispatch.exists():
        try:
            subprocess.run([sys.executable, str(dispatch), "--kill"],
                           timeout=20, capture_output=True)
        except Exception:
            pass   # un echec de coupure ne doit pas empecher l'extinction

    # 2. rendre la fenetre muette
    sid = tts_session.session_id_courante()
    if sid is None:
        moteur, _voix = tts_session.etat_global()
        if moteur is None:
            print("Mode vocal deja desactive. (hors session : reglage partage)")
            return 0
        tts_session.desactiver_global()
        print("Silence. Mode vocal desactive. (hors session : reglage partage)")
        return 0

    moteur, _voix = tts_session.etat_session(sid)
    if moteur is None:
        print("Mode vocal deja desactive pour cette fenetre.")
        return 0

    tts_session.desactiver(sid)
    print("Silence. Mode vocal desactive pour cette fenetre.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.stderr.write("tts_stop erreur : %s: %s\n" % (type(exc).__name__, exc))
        sys.exit(1)
