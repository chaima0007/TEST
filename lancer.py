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
    python = "py" if os.system("py --version >nul 2>&1") == 0 else "python"
    cmd = f"{python} {script} {args}".strip()
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
  [9]  Agent Référence           ← Index et doc de tous tes projets
  [10] Agent Juridique           ← Contrats, CGV, RGPD, NDA
  [11] Agent Support Client      ← SAV 24/7, FAQ, onboarding
  [12] Agent Chef de Projet      ← Planification, risques, rapports
  [13] Agent Guide               ← Sait toujours ce qu'il faut faire ensuite
  [14] Agent Watchdog            ← Surveillance 24h/24 de tous les agents
  [15] Agent Fantôme             ← Audit silencieux, zéro trace
  [16] Agent Commandant          ← Fait travailler tous les agents en équipe
  [17] Agent Résolveur           ← Résout les problèmes de manière ultra-pro
  [18] Agent CRM                 ← Pipeline commercial lead → client → CA
  [19] Agent Email               ← Cold outreach + séquences + propositions
  [20] Dashboard CEO             ← Vue exécutive revenus, KPIs, alertes
  [21] Mémoire Session           ← Se souvient de tout ce qu'on a fait ensemble
  [22] Agent Autopilot           ← Cerveau autonome — analyse et agit seul
  [23] Agent Growth              ← Growth hacking — 0 à 10 clients en 90 jours
  [24] Agent Empire              ← Vision 5 ans — expansion et domination
  [25] Agent TITAN               ← 20 experts + 50 simulations — zéro erreur

  ── NOUVEAUX AGENTS BUSINESS & ADMINISTRATIF ──────────────
  [26] Comptable Belge           ← TVA, BCE, INASTI, déductions, factures légales
  [27] Agent Financement         ← Innoviris, Hub Brussels, subventions, pitch
  [28] Agent Tarification        ← Pricing, ROI client, packages, upsell
  [29] Agent Marque              ← Branding, storytelling, LinkedIn, positionnement
  [30] Agent Mental              ← Coach entrepreneurial, blocages, routine fondatrice
  [31] Auditeur Financier        ← Simulation ONEM + Caelum, seuil optimal, conformité

  ── AGENTS STRATÉGIE & RÉSILIENCE ─────────────────────────
  [32] Red Team Architect        ← Black Swan, stress tests, plan de continuité
  [33] Flux Économique           ← Vélocité capital, DSO, Revenue/Hour, frictions
  [34] Synthèse Exponentielle    ← Unifie tous agents → décision stratégique unique

  ── DIRECTIVE MAÎTRE — VISION EMPIRE & SINGULARITÉ ────────
  [35] Stratège Croissance       ← Scalabilité, levier exponentiel, passage paliers
  [36] Asset Builder             ← Transformer revenus en actifs durables
  [37] Analyste Convergence      ← Conformité légale + expansion empire simultanée

  ── FLOTTE DOMINATION EUROPÉENNE ──────────────────────────
  [38] Architecte Singularité    ← Concevoir l'avantage concurrentiel inégalable
  [39] Sniper Goulots            ← Identifier et éliminer tous les blocages
  [40] Maître Vélocité Capital   ← Optimisation capital ≥ 10x en 90 jours
  [41] Simulateur Black Swan     ← Scénarios catastrophe + plans de survie
  [42] Stratège Premiers Principes ← Décisions fondamentales sans biais
  [43] Orchestrateur Symbiose    ← Synergie maximale entre tous les agents
  [44] Chasseur Marchés Émergents ← Détection opportunités avant la concurrence
  [45] Gardien Playbook          ← Mémoire institutionnelle + décisions validées
  [46] Expert Conformité Offensif ← Légalité belge = avantage compétitif
  [47] Influence Systémique      ← Positionnement autorité IA en Belgique

  ── ARCHITECTURE LOCALE AUTONOME (OLLAMA) ─────────────────
  [48] Ingénieur Code Autonome   ← Dev, debug, optimisation code (sans tokens)
  [49] Testeur Simulation QA     ← Tests en boucle, logs d'erreurs, correctifs auto
  [50] Analyste BD Légales       ← Corpus juridiques → JSON/SQL structuré

  ── SYSTÈME DE CONSCIENCE ─────────────────────────────────
  [51] Gardien Cohérence         ← Détecte les dérives, aligne l'empire, mémoire vive
  [52] Synthétiseur Réalité      ← Ground Truth : compresse, vérifie, débiaise la flotte

  ── PROTOCOLE DOMINATION TOTALE ───────────────────────────
  [53] Chasseur Inefficacité     ← Lean : éliminer toute perte de temps et d'argent
  [54] Capteur Signaux Faibles   ← Valide les opportunités réelles avant la concurrence
  [55] Architecte Talents        ← Ressources (agents + skills) pour chaque opportunité
  [56] Force de Vente            ← Offensive marché ciblée, MEDDIC, closing
  [57] Optimiseur Décisions      ← Résultat final : X% parts de marché, profit net

  ── CAPITAL STRATÉGIQUE DE L'EMPIRE ──────────────────────
  [58] Architecte Réputation     ← The Anchor : valeur perçue, preuve sociale, crédibilité
  [59] Analyste Valeurs Adjacentes ← Marchés voisins où Caelum est imbattable
  [60] Stratège Auto-Obsolescence ← Concevoir le produit qui tuera ton produit actuel
  [61] Maître Culture Interne    ← Standards d'excellence, alignement, mindset empire
  [62] Historien Empire          ← Log-Keeper : décisions → protocoles de réussite

  [s]  Voir stats & mémoire
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
            lancer("agent_reference.py")
        elif choix == "10":
            lancer("agent_juridique.py")
        elif choix == "11":
            lancer("agent_support_client.py")
        elif choix == "12":
            lancer("agent_chef_projet.py")
        elif choix == "13":
            lancer("agent_guide.py")
        elif choix == "14":
            lancer("agent_watchdog.py")
        elif choix == "15":
            lancer("agent_fantome.py")
        elif choix == "16":
            lancer("agent_commandant.py")
        elif choix == "17":
            lancer("agent_resolveur.py")
        elif choix == "18":
            lancer("agent_crm.py")
        elif choix == "19":
            lancer("agent_email.py")
        elif choix == "20":
            lancer("agent_dashboard_ceo.py")
        elif choix == "21":
            lancer("agent_memoire_session.py")
        elif choix == "22":
            lancer("agent_autopilot.py")
        elif choix == "23":
            lancer("agent_growth.py")
        elif choix == "24":
            lancer("agent_empire.py")
        elif choix == "25":
            lancer("agent_titan.py")
        elif choix == "26":
            lancer("agent_comptable_belge.py")
        elif choix == "27":
            lancer("agent_financement.py")
        elif choix == "28":
            lancer("agent_tarification.py")
        elif choix == "29":
            lancer("agent_marque.py")
        elif choix == "30":
            lancer("agent_mental.py")
        elif choix == "31":
            lancer("agent_auditeur_financier.py")
        elif choix == "32":
            lancer("agent_red_team.py")
        elif choix == "33":
            lancer("agent_flux_economique.py")
        elif choix == "34":
            lancer("agent_synthese_exponentielle.py")
        elif choix == "35":
            lancer("agent_stratege_croissance.py")
        elif choix == "36":
            lancer("agent_asset_builder.py")
        elif choix == "37":
            lancer("agent_convergence.py")
        elif choix == "38":
            lancer("agent_architecte_singularite.py")
        elif choix == "39":
            lancer("agent_sniper_goulots.py")
        elif choix == "40":
            lancer("agent_maitre_velocite.py")
        elif choix == "41":
            lancer("agent_simulateur_black_swan.py")
        elif choix == "42":
            lancer("agent_premiers_principes.py")
        elif choix == "43":
            lancer("agent_symbiose.py")
        elif choix == "44":
            lancer("agent_chasseur_marches.py")
        elif choix == "45":
            lancer("agent_gardien_playbook.py")
        elif choix == "46":
            lancer("agent_conformite_offensive.py")
        elif choix == "47":
            lancer("agent_influence_systemique.py")
        elif choix == "48":
            lancer("agent_ingenieur_code.py")
        elif choix == "49":
            lancer("agent_testeur_qa.py")
        elif choix == "50":
            lancer("agent_analyste_legal.py")
        elif choix == "51":
            lancer("agent_gardien_coherence.py")
        elif choix == "52":
            lancer("agent_synthetiseur_realite.py")
        elif choix == "53":
            lancer("agent_chasseur_inefficacite.py")
        elif choix == "54":
            lancer("agent_capteur_signaux.py")
        elif choix == "55":
            lancer("agent_architecte_talents.py")
        elif choix == "56":
            lancer("agent_force_de_vente.py")
        elif choix == "57":
            lancer("agent_optimiseur_decisions.py")
        elif choix == "58":
            lancer("agent_architecte_reputation.py")
        elif choix == "59":
            lancer("agent_valeurs_adjacentes.py")
        elif choix == "60":
            lancer("agent_auto_obsolescence.py")
        elif choix == "61":
            lancer("agent_culture_interne.py")
        elif choix == "62":
            lancer("agent_historien_empire.py")
        elif choix == "s":
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
