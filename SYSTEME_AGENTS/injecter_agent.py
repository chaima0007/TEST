"""
INJECTION SOUVERAINE — Charge un agent .md et l'injecte dans Gemini
Usage : py injecter_agent.py 13        (agent numéro 13 = GUIDE)
        py injecter_agent.py TITAN     (cherche par nom)
        py injecter_agent.py --list    (liste tous les agents)
"""
import os
import sys
import glob

DOSSIER = os.path.dirname(os.path.abspath(__file__))


def lister_agents():
    fichiers = sorted(glob.glob(os.path.join(DOSSIER, "[0-9][0-9]_*.md")))
    print(f"\n  {'#':>3}  {'Fichier':<30} {'Nom'}")
    print(f"  {'─'*55}")
    for f in fichiers:
        nom = os.path.basename(f)
        num = nom[:2]
        label = nom[3:-3].replace("_", " ")
        print(f"  {num:>3}  {nom:<30} {label}")
    print()


def charger_agent(identifiant: str) -> tuple[str, str]:
    """Retourne (nom_agent, contenu_md)."""
    if identifiant.isdigit():
        pattern = os.path.join(DOSSIER, f"{identifiant.zfill(2)}_*.md")
    else:
        pattern = os.path.join(DOSSIER, f"*{identifiant.upper()}*.md")

    fichiers = glob.glob(pattern)
    if not fichiers:
        raise FileNotFoundError(f"Agent '{identifiant}' introuvable dans {DOSSIER}")

    chemin = fichiers[0]
    nom = os.path.basename(chemin)[3:-3].replace("_", " ")
    with open(chemin, "r", encoding="utf-8") as f:
        return nom, f.read()


def dialoguer_avec_agent(nom: str, contenu: str):
    """Lance une session de dialogue avec l'agent chargé."""
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("\n[ERREUR] GEMINI_API_KEY manquante. Lance installer.bat d'abord.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    print(f"\n{'═'*65}")
    print(f"  AGENT SOUVERAIN : {nom}")
    print(f"  Identité chargée depuis SYSTEME_AGENTS/")
    print(f"  Tape 'quit' pour quitter")
    print(f"{'═'*65}\n")

    historique = []

    while True:
        try:
            question = input(f"  Toi → ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Session terminée.")
            break

        if question.lower() in ("quit", "exit", "0", "q"):
            print("\n  Session terminée.")
            break
        if not question:
            continue

        historique.append({"role": "user", "parts": [{"text": question}]})

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=historique,
                config=types.GenerateContentConfig(
                    system_instruction=contenu,
                    temperature=0.3,
                    max_output_tokens=2000,
                ),
            )
            reponse_texte = response.text or ""
            historique.append({"role": "model", "parts": [{"text": reponse_texte}]})
            print(f"\n  {nom} →\n")
            print(reponse_texte)
            print()
        except Exception as e:
            print(f"\n  [Erreur API] {e}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "--list":
        lister_agents()
        identifiant = input("  Numéro de l'agent → ").strip()
    else:
        identifiant = sys.argv[1]

    try:
        nom, contenu = charger_agent(identifiant)
        dialoguer_avec_agent(nom, contenu)
    except FileNotFoundError as e:
        print(f"\n  ❌ {e}")
        lister_agents()
