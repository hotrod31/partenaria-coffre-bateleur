"""
tts_bascule.py - Allume, eteint ou change la voix de LA FENETRE appelante.

Appele par les commandes /vocal-* :

    python tts_bascule.py <moteur> <voix> "<Nom affiche>"

Trois cas, un seul message en sortie :

    meme moteur ET meme voix deja actifs  ->  on eteint
    une autre voix est active             ->  on bascule
    rien n'est actif                      ->  on allume

POURQUOI UN SCRIPT, ET PAS DU BASH RECOPIE DANS CHAQUE COMMANDE. Il y a huit
voix. Huit copies d'une meme regle divergent : la premiere correction oubliee
quelque part, et deux commandes ne se comportent plus pareil. Ici la regle
vit a un seul endroit.

Portee : CETTE fenetre de terminal, et elle seule. Les autres ne sont pas
touchees. Hors session, on retombe sur les fichiers partages.
"""

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


DEFAUT_FICHIER = HOOKS_DIR / "tts_voix_defaut"
DEFAUT_SECOURS = ("piper", "jessica", "Jessica")


def lire_defaut():
    """La voix par defaut, choisie a l'ecoute le jour de l'installation.

    Format du fichier : "moteur:voix". Jessica en secours : c'est la
    meilleure voix de Piper en francais, et elle est 100 % locale -- donc
    elle marche toujours, meme sans reseau.
    """
    try:
        brut = DEFAUT_FICHIER.read_text(encoding="utf-8").strip().lower()
    except OSError:
        return DEFAUT_SECOURS
    if ":" not in brut:
        return DEFAUT_SECOURS
    moteur, voix = brut.split(":", 1)
    moteur, voix = moteur.strip(), voix.strip()
    if moteur not in tts_session.MOTEURS or not voix:
        return DEFAUT_SECOURS
    return (moteur, voix, voix.capitalize())


def ecrire_defaut(moteur, voix):
    """Le dernier choix explicite devient la voix par defaut.

    Ainsi /vocal rejoue toujours ce que l'on a demande en dernier, sans
    avoir a reglerquoi que ce soit.
    """
    try:
        DEFAUT_FICHIER.write_text("%s:%s" % (moteur, voix), encoding="utf-8")
    except OSError:
        pass


def main():
    args = sys.argv[1:]

    if args and args[0] == "--defaut":
        moteur, voix, nom = lire_defaut()
        memoriser = False
    elif len(args) >= 2:
        moteur = args[0].strip().lower()
        voix = args[1].strip().lower()
        nom = args[2] if len(args) > 2 else voix.capitalize()
        memoriser = True
    else:
        print("usage : tts_bascule.py <moteur> <voix> [nom affiche]")
        print("        tts_bascule.py --defaut")
        return 1

    if moteur not in tts_session.MOTEURS:
        print("Moteur inconnu : %s" % moteur)
        return 1

    # Un moteur demande mais pas installe : on le dit, et on ne pose rien.
    # Mieux vaut un refus clair qu'une fenetre qu'on croit bavarde et qui
    # reste muette sans raison visible.
    moteurs_fichiers = {"piper": "piper_tts.py", "edge": "edge_tts_speak.py"}
    if not (HOOKS_DIR / moteurs_fichiers[moteur]).exists():
        print("Le moteur %s n'est pas installe dans ce coffre." % moteur)
        return 1

    # Le marqueur d'indisponibilite d'Edge. Pose par l'installateur quand le
    # service Microsoft refusait la connexion le jour de l'installation : la
    # bibliotheque n'est alors pas installee, et activer une voix Edge
    # produirait une fenetre qu'on croit bavarde et qui reste muette.
    # Ce marqueur n'est PAS versionne -- le fichier du moteur, lui, reste en
    # place, pour qu'une reinstallation n'ait rien a retelecharger.
    if moteur == "edge" and (HOOKS_DIR / "tts_edge_indisponible").exists():
        print("Les voix Edge ne sont pas disponibles sur cette installation.")
        print("")
        print("Le service de synthese de Microsoft refusait la connexion le jour")
        print("de l'installation (erreur 403). Ce n'est pas un defaut de ton")
        print("coffre : c'est une coupure cote Microsoft, qui se repare souvent")
        print("d'elle-meme en quelques jours.")
        print("")
        print("En attendant, les voix 100 % locales fonctionnent :")
        print("  /vocal-jessica   feminine chaleureuse")
        print("  /vocal-pierre    masculine")
        print("  /vocal-siwis     feminine neutre")
        print("")
        print("Pour reessayer Edge plus tard : relancer Installer-Voix.ps1")
        return 1

    sid = tts_session.session_id_courante()

    if sid is None:
        # Repli hors session : les anciens fichiers partages.
        actuel_moteur, actuel_voix = tts_session.etat_global()
        if actuel_moteur == moteur and actuel_voix == voix:
            tts_session.desactiver_global()
            resultat = "eteint"
        else:
            etait_actif = actuel_moteur is not None
            tts_session.activer_global(moteur, voix)
            resultat = "bascule" if etait_actif else "allume"
        portee = " (hors session : reglage partage)"
    else:
        actuel_moteur, actuel_voix = tts_session.etat_session(sid)
        if actuel_moteur == moteur and actuel_voix == voix:
            tts_session.desactiver(sid)
            resultat = "eteint"
        else:
            etait_actif = actuel_moteur is not None
            tts_session.activer(sid, moteur, voix)
            resultat = "bascule" if etait_actif else "allume"
        portee = ""

    # Un choix explicite devient la voix par defaut, pour que /vocal rejoue
    # toujours le dernier souhait. Une extinction ne l'efface pas : on garde
    # la voix pour la prochaine fois.
    if memoriser and resultat != "eteint":
        ecrire_defaut(moteur, voix)

    if resultat == "eteint":
        print("Mode vocal desactive pour cette fenetre." + portee)
    elif resultat == "bascule":
        print("Mode vocal bascule sur %s." % nom + portee)
    else:
        print("Mode vocal active - %s." % nom + portee)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.stderr.write("tts_bascule erreur : %s: %s\n" % (type(exc).__name__, exc))
        sys.exit(1)
