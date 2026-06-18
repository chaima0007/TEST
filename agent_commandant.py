"""
AGENT COMMANDANT — Fait travailler tous les agents en équipe
Chef d'orchestre opérationnel : délègue, coordonne, suit les résultats.
Niveau cabinet de conseil international.

Usage : python agent_commandant.py
"""

import os
import sys
import json
import subprocess
from datetime import datetime
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# Registre complet des agents avec leurs capacités
REGISTRE_AGENTS = {
    "agent_commercial.py": {
        "role": "Ventes & prospection",
        "capacites": ["générer prospects", "rédiger propositions", "relances clients", "pipeline ventes"],
        "priorite": 1,
    },
    "agent_facturation.py": {
        "role": "Finance & trésorerie",
        "capacites": ["créer factures", "relances paiements", "tableau trésorerie", "rapport financier"],
        "priorite": 1,
    },
    "agent_support_client.py": {
        "role": "Service client",
        "capacites": ["répondre tickets", "FAQ", "onboarding", "satisfaction client"],
        "priorite": 1,
    },
    "agent_chef_projet.py": {
        "role": "Gestion de projet",
        "capacites": ["WBS", "standup report", "analyse risques", "rétrospective"],
        "priorite": 1,
    },
    "agent_kpi.py": {
        "role": "Analytics & KPIs",
        "capacites": ["tableau de bord", "alertes performance", "prédictions business"],
        "priorite": 1,
    },
    "agent_veille.py": {
        "role": "Intelligence marché",
        "capacites": ["veille concurrentielle", "tendances marché", "opportunités"],
        "priorite": 2,
    },
    "agent_seo.py": {
        "role": "Référencement & contenu",
        "capacites": ["mots-clés", "articles blog", "audit SEO", "plan contenu"],
        "priorite": 2,
    },
    "agent_strategie.py": {
        "role": "Stratégie & croissance",
        "capacites": ["analyse Porter", "expansion", "pitch investor", "plan stratégique"],
        "priorite": 2,
    },
    "agent_reputation.py": {
        "role": "Image & communication",
        "capacites": ["gestion avis", "crise réputation", "LinkedIn", "communication"],
        "priorite": 2,
    },
    "agent_juridique.py": {
        "role": "Juridique & conformité",
        "capacites": ["contrats", "CGV", "RGPD", "NDA"],
        "priorite": 2,
    },
    "agent_recrutement.py": {
        "role": "RH & recrutement",
        "capacites": ["fiches poste", "analyse CV", "entretiens", "onboarding"],
        "priorite": 3,
    },
    "agent_formation_equipe.py": {
        "role": "Formation & développement",
        "capacites": ["plan formation", "IDP", "certifications", "compétences"],
        "priorite": 3,
    },
    "agent_bienetre_equipe.py": {
        "role": "Bien-être & culture",
        "capacites": ["burnout prevention", "rituels équipe", "énergie collective"],
        "priorite": 3,
    },
    "securite.py": {
        "role": "Sécurité & protection",
        "capacites": ["audit sécurité", "détection secrets", "OWASP", "score sécurité"],
        "priorite": 1,
    },
    "agent_innovation.py": {
        "role": "Innovation & R&D",
        "capacites": ["brainstorm", "scénarios futurs", "disruption", "nouvelles idées"],
        "priorite": 3,
    },
    "agent_oracle.py": {
        "role": "Prédictions & anticipation",
        "capacites": ["prédictions business", "signaux faibles", "black swans"],
        "priorite": 2,
    },
    "agent_comptable.py": {
        "role": "Comptabilité & fiscalité",
        "capacites": ["bilan", "TVA", "CIR", "rapport investisseur"],
        "priorite": 1,
    },
    "agent_data.py": {
        "role": "Data science",
        "capacites": ["analyse CSV", "segmentation", "prévisions", "corrélations"],
        "priorite": 2,
    },
    "agent_partenariats.py": {
        "role": "Partenariats & réseau",
        "capacites": ["identifier partenaires", "programme revendeurs", "négociation"],
        "priorite": 2,
    },
    "agent_watchdog.py": {
        "role": "Surveillance système",
        "capacites": ["vérifier agents", "rapport santé", "alertes pannes"],
        "priorite": 1,
    },
    "agent_fantome.py": {
        "role": "Sécurité silencieuse",
        "capacites": ["audit sans trace", "détection intrusion", "intégrité agents"],
        "priorite": 1,
    },
}


def charger_memoire():
    try:
        if os.path.exists("memoire_entreprise.json"):
            with open("memoire_entreprise.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*60}\n  {label}\n{'═'*60}\n")
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=3000),
    )
    reponse = ""
    try:
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


# ─────────────────────────────────────────────────────────────
# 1. BRIEFING OPÉRATIONNEL — Qui fait quoi maintenant
# ─────────────────────────────────────────────────────────────

def briefing_operationnel():
    memoire = charger_memoire()
    clients = list(memoire.get("clients", {}).keys())
    tickets = [t for t in memoire.get("tickets", []) if t.get("statut") != "resolu"]
    factures = [f for f in memoire.get("factures", {}).values() if f.get("statut") == "en_attente"]

    contexte_agents = "\n".join([
        f"→ {a} [{info['role']}] P{info['priorite']} : {', '.join(info['capacites'][:2])}"
        for a, info in REGISTRE_AGENTS.items()
    ])

    streamer(
        """Tu es le Directeur des Opérations d'un cabinet de conseil top tier (McKinsey niveau).
Tu coordonnes une équipe de 20+ agents IA spécialisés.
Pour chaque situation, tu produis un briefing opérationnel précis :

FORMAT :
🎯 MISSION DU JOUR
━━━━━━━━━━━━━━━━
[Objectif principal avec chiffre clé]

DÉPLOIEMENT DES AGENTS (par ordre de priorité) :
P1 [IMMÉDIAT] → Agent X → Mission précise → Résultat attendu
P2 [AUJOURD'HUI] → Agent Y → Mission précise → Résultat attendu
P3 [CETTE SEMAINE] → Agent Z → Mission précise → Résultat attendu

SYNCHRONISATION :
→ Agent X envoie ses résultats à Agent Y avant 14h
→ Agent Z utilise le rapport de X pour...

KPI DE LA JOURNÉE : [3 métriques concrètes à atteindre]""",
        f"""Situation entreprise :
- Clients : {clients or 'aucun encore'}
- Tickets ouverts : {len(tickets)}
- Factures en attente : {len(factures)}
- Heure : {datetime.now().strftime('%H:%M')}

Agents disponibles :
{contexte_agents}""",
        "COMMANDANT — Briefing Opérationnel"
    )


# ─────────────────────────────────────────────────────────────
# 2. MISSION SPÉCIALE — Déployer des agents sur un objectif précis
# ─────────────────────────────────────────────────────────────

def mission_speciale(objectif):
    contexte_agents = "\n".join([
        f"→ {a} : {info['role']} — {', '.join(info['capacites'])}"
        for a, info in REGISTRE_AGENTS.items()
    ])

    streamer(
        """Tu es un Directeur de Mission d'élite.
Pour atteindre l'objectif donné, tu crées un plan de déploiement multi-agents
avec : qui fait quoi, dans quel ordre, comment les résultats se transmettent.

FORMAT :
OBJECTIF : [reformulation précise et mesurable]
DURÉE ESTIMÉE : [X heures/jours]

PHASE 1 — [Nom de la phase] (J1)
  Agent : [nom_agent.py]
  Mission : [action précise]
  Livrable : [ce qu'il produit]
  → Transmet à : [agent suivant]

PHASE 2 — ...

POINT DE CONTRÔLE : [comment vérifier que ça avance]
PLAN B : [si un agent échoue]
SUCCÈS = [définition concrète du succès]""",
        f"""Objectif : {objectif}
Agents disponibles :
{contexte_agents}""",
        f"MISSION SPÉCIALE — {objectif}"
    )


# ─────────────────────────────────────────────────────────────
# 3. REVUE DE PERFORMANCE — Analyse l'utilisation des agents
# ─────────────────────────────────────────────────────────────

def revue_performance():
    memoire = charger_memoire()
    stats = memoire.get("stats", {}).get("agents_utilises", {})
    interactions = memoire.get("interactions", [])[-20:]

    agents_actifs = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10]
    agents_inactifs = [a for a in REGISTRE_AGENTS if a not in stats]

    streamer(
        """Tu es le Chief Operations Officer. Tu analyses la performance de l'équipe d'agents
et identifies les optimisations à apporter.

FORMAT :
📊 PERFORMANCE ÉQUIPE
━━━━━━━━━━━━━━━━━━━

TOP PERFORMERS : [agents les plus utilisés avec analyse]
AGENTS SOUS-UTILISÉS : [pourquoi et comment les activer]
GAPS IDENTIFIÉS : [besoins non couverts]
RECOMMANDATIONS : [3 actions concrètes pour maximiser l'efficacité]
ROI ESTIMÉ : [impact business des recommandations]""",
        f"""Agents actifs (utilisation) : {agents_actifs}
Agents jamais utilisés : {agents_inactifs[:10]}
Dernières interactions : {json.dumps(interactions, ensure_ascii=False)}
Total agents disponibles : {len(REGISTRE_AGENTS)}""",
        "REVUE DE PERFORMANCE — Équipe Agents"
    )


# ─────────────────────────────────────────────────────────────
# 4. SCRUM BOARD — Tableau de bord des missions en cours
# ─────────────────────────────────────────────────────────────

def scrum_board():
    memoire = charger_memoire()
    projets = memoire.get("projets", {})
    tickets = memoire.get("tickets", [])
    interactions_recentes = memoire.get("interactions", [])[-10:]

    streamer(
        """Tu es le Scrum Master d'une équipe d'agents IA.
Tu produis un SCRUM BOARD en texte :

SPRINT EN COURS : [date]
━━━━━━━━━━━━━━━━━━━━━━━━━

📋 BACKLOG (À faire)
  □ ...

🔄 EN COURS (Agents actifs)
  ⚙ Agent X → Tâche → 60% avancement

✅ TERMINÉ (Complété aujourd'hui)
  ✓ ...

🚧 BLOQUÉ (Nécessite intervention)
  ⚠ ...

VÉLOCITÉ : [tâches/jour]
PROCHAINE ACTION : [1 chose à faire maintenant]""",
        f"""Projets : {json.dumps(projets, ensure_ascii=False)}
Tickets : {json.dumps(tickets[:5], ensure_ascii=False)}
Activité récente : {json.dumps(interactions_recentes, ensure_ascii=False)}""",
        "SCRUM BOARD — Vue temps réel"
    )


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT COMMANDANT — Chef d'orchestre opérationnel")
    print("  Caelum Partners — Niveau cabinet international")
    print("═"*60)

    while True:
        print("\n  1. Briefing opérationnel — Qui fait quoi maintenant")
        print("  2. Mission spéciale — Déployer les agents sur un objectif")
        print("  3. Revue de performance — Analyse de l'équipe")
        print("  4. Scrum Board — Vue temps réel des missions")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            briefing_operationnel()
        elif choix == "2":
            obj = input("  Objectif → ").strip()
            if obj:
                mission_speciale(obj)
        elif choix == "3":
            revue_performance()
        elif choix == "4":
            scrum_board()
        else:
            print("  Choix invalide.")
