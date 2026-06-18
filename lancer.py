"""
BRAS DROIT IA — Lanceur Principal
Menu central pour accéder à tous les agents de l'entreprise.

Usage : python lancer.py
"""

import os
import sys
import subprocess


def verifier_cle():
    if not os.environ.get("GEMINI_API_KEY"):
        print("\n⚠️  Clé API manquante.")
        print("   Tape dans ton CMD : set GEMINI_API_KEY=ta_cle")
        print("   Puis relance : python lancer.py\n")
        return False
    return True


def lancer(script, args=""):
    cmd = f"python {script} {args}".strip()
    os.system(cmd)


def afficher_stats():
    try:
        from memoire import charger_memoire
        m = charger_memoire()
        clients = len(m.get("clients", {}))
        interactions = len(m.get("interactions", []))
        demandes = m.get("stats", {}).get("total_demandes", 0)
        print(f"  Clients en mémoire : {clients}  |  Interactions : {interactions}  |  Demandes traitées : {demandes}")
    except Exception:
        print("  Mémoire vide — première utilisation.")


MENU = """
  ┌─────────────────────────────────────────────────┐
  │         BRAS DROIT IA — AgentClaude Solutions   │
  └─────────────────────────────────────────────────┘

  AGENTS DISPONIBLES :

  [1]  Orchestrateur Autonome    ← Tout déléguer à l'IA
  [2]  Agent Commercial          ← Prospects, propositions, emails
  [3]  Agent Veille              ← Marché IA et concurrents
  [4]  Agent Facturation         ← Factures et relances paiement
  [5]  Agent Recrutement         ← CV, fiches poste, entretiens
  [6]  Agent Professeur          ← Formation et apprentissage
  [7]  Usine de Migration        ← Moderniser du code legacy
  [8]  Suite Sécurité            ← Audit et protection données

  [9]  Voir stats & mémoire
  [0]  Quitter
"""


if __name__ == "__main__":
    if not verifier_cle():
        sys.exit(1)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(MENU)
        afficher_stats()
        print()
        choix = input("  Ton choix → ").strip()

        if choix == "0":
            print("\n  À bientôt !\n")
            break
        elif choix == "1":
            lancer("orchestrateur.py")
        elif choix == "2":
            lancer("agent_commercial.py")
        elif choix == "3":
            lancer("agent_veille.py")
        elif choix == "4":
            lancer("agent_facturation.py")
        elif choix == "5":
            lancer("agent_recrutement.py")
        elif choix == "6":
            lancer("agents.py")
        elif choix == "7":
            fichier = input("\n  Fichier à migrer → ").strip()
            lancer("usine_migration_logicielle.py", fichier)
        elif choix == "8":
            fichier = input("\n  Fichier à auditer → ").strip()
            lancer("securite.py", fichier)
        elif choix == "9":
            from memoire import charger_memoire, lister_clients
            print("\n  ── CLIENTS ──")
            lister_clients()
            m = charger_memoire()
            print(f"\n  ── STATS ──")
            print(f"  Total demandes traitées : {m.get('stats', {}).get('total_demandes', 0)}")
            for agent, count in m.get('stats', {}).get('agents_utilises', {}).items():
                print(f"  {agent} : {count} utilisations")
            input("\n  [Entrée pour revenir au menu]")
        else:
            print("  Choix invalide.")
            input("  [Entrée pour continuer]")
