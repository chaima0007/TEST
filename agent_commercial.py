"""
AGENT COMMERCIAL AUTONOME
Gère prospects, génère des propositions, rédige emails, suit les clients.
Tout seul. Zéro intervention humaine.

Usage : python agent_commercial.py
"""

import os
import sys
import json
from google import genai
from google.genai import types
from memoire import (
    ajouter_client, ajouter_interaction, obtenir_contexte_client,
    lister_clients, charger_memoire, incrementer_stat
)

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

ENTREPRISE_PROFIL = """
Nom : AgentClaude Solutions
Spécialité : Automatisation par agents IA (Claude, Gemini)
Services :
  - Agents autonomes sur mesure pour entreprises
  - Migration et modernisation de code legacy
  - Sécurité et audit IA
  - Formation équipes sur agents IA
  - Orchestrateurs autonomes clé en main
Avantage concurrentiel : Agents qui travaillent 24h/24 sans erreur humaine
"""


def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def creer_agent(instructions, temperature=0.6):
    return _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(
            temperature=temperature, max_output_tokens=2048
        ),
    )


def executer_stream(model, prompt, label):
    print(f"\n{'─'*60}")
    print(f"  ► {label}")
    print(f"{'─'*60}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur : {e}]"
        print(reponse)
    print()
    return reponse


# ─── AGENTS COMMERCIAUX ───────────────────────────────────────

def analyser_prospect(nom, secteur, besoin):
    """Analyse un prospect et évalue son potentiel."""
    incrementer_stat("analyser_prospect")
    contexte = obtenir_contexte_client(nom)

    agent = creer_agent(f"""Tu es un Directeur Commercial expert en vente de solutions IA.
Profil entreprise vendeuse :
{ENTREPRISE_PROFIL}

Analyse un prospect et détermine :
1. Score d'opportunité (0-100)
2. Besoins réels cachés derrière la demande
3. Objections probables et comment les contrer
4. Approche de vente recommandée
5. Prix indicatif de la solution""", temperature=0.3)

    return executer_stream(agent,
        f"Prospect : {nom}\nSecteur : {secteur}\nBesoin exprimé : {besoin}\nHistorique : {contexte}",
        f"Analyse Prospect — {nom}"
    )


def generer_proposition(nom, secteur, besoin, analyse):
    """Génère une proposition commerciale professionnelle."""
    incrementer_stat("generer_proposition")

    agent = creer_agent(f"""Tu es un expert en rédaction de propositions commerciales IA.
Profil entreprise :
{ENTREPRISE_PROFIL}

Génère une proposition commerciale complète et professionnelle :
- Page de couverture avec accroche percutante
- Compréhension du besoin client
- Solution proposée avec agents IA détaillés
- Bénéfices mesurables (ROI, gain de temps, réduction erreurs)
- Planning de mise en œuvre
- Tarification (3 niveaux : Starter/Pro/Enterprise)
- Témoignages fictifs réalistes
- Appel à l'action clair""", temperature=0.5)

    return executer_stream(agent,
        f"Client : {nom} ({secteur})\nBesoin : {besoin}\nAnalyse : {analyse[:500]}",
        f"Proposition Commerciale — {nom}"
    )


def rediger_email_prospection(nom, secteur, besoin):
    """Rédige un email de prospection personnalisé."""
    incrementer_stat("rediger_email")

    agent = creer_agent(f"""Tu es un expert en cold emailing B2B pour solutions IA.
Profil entreprise :
{ENTREPRISE_PROFIL}

Rédige un email de prospection qui :
- Accroche dès la première ligne (pas "Je me permets de...")
- Montre qu'on comprend leur problème spécifique
- Présente 1 bénéfice concret chiffré
- Inclut une preuve sociale (cas client fictif réaliste)
- Termine par un CTA simple (pas "réservez une démo" générique)
- Fait maximum 150 mots
- Objet : percutant, personnel, pas spammy""", temperature=0.7)

    return executer_stream(agent,
        f"Destinataire : {nom}\nSecteur : {secteur}\nProblème détecté : {besoin}",
        f"Email Prospection — {nom}"
    )


def suivi_relance(nom):
    """Génère un email de relance intelligent basé sur l'historique."""
    incrementer_stat("suivi_relance")
    contexte = obtenir_contexte_client(nom)

    agent = creer_agent("""Tu es un expert en suivi commercial.
Génère un email de relance qui :
- Fait référence à l'échange précédent naturellement
- Apporte une nouvelle valeur (insight, stats récentes IA)
- N'est pas insistant ou désespéré
- Propose une alternative plus simple si pas de réponse
- Maximum 100 mots""", temperature=0.6)

    return executer_stream(agent,
        f"Client : {nom}\nHistorique : {contexte}",
        f"Email Relance — {nom}"
    )


def rapport_pipeline_commercial():
    """Génère un rapport sur le pipeline commercial."""
    m = charger_memoire()
    clients = m["clients"]

    prospects = [n for n, d in clients.items() if d["statut"] == "prospect"]
    actifs = [n for n, d in clients.items() if d["statut"] == "actif"]
    total_interactions = len(m["interactions"])

    agent = creer_agent("""Tu es un Directeur Commercial.
Génère un rapport de pipeline commercial synthétique avec :
- Vue d'ensemble des opportunités
- Recommandations d'actions prioritaires
- Prévisions de conversion
- Alertes sur clients inactifs""", temperature=0.3)

    return executer_stream(agent,
        f"""Pipeline actuel :
- Prospects : {len(prospects)} ({', '.join(prospects[:5])})
- Clients actifs : {len(actifs)} ({', '.join(actifs[:5])})
- Total interactions : {total_interactions}
- Stats agents : {json.dumps(m['stats']['agents_utilises'], ensure_ascii=False)}""",
        "Rapport Pipeline Commercial"
    )


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def menu():
    print("\n" + "═" * 60)
    print("  AGENT COMMERCIAL AUTONOME — AgentClaude Solutions")
    print("═" * 60)

    while True:
        print("\n  1. Analyser un nouveau prospect")
        print("  2. Générer une proposition commerciale")
        print("  3. Rédiger un email de prospection")
        print("  4. Générer un email de relance")
        print("  5. Voir tous les clients")
        print("  6. Rapport pipeline commercial")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break

        elif choix == "1":
            nom = input("  Nom du prospect → ").strip()
            secteur = input("  Secteur (ex: banque, retail, santé) → ").strip()
            besoin = input("  Besoin exprimé → ").strip()
            ajouter_client(nom, secteur, besoin)
            analyse = analyser_prospect(nom, secteur, besoin)
            ajouter_interaction(nom, "analyse_prospect", analyse)

        elif choix == "2":
            nom = input("  Nom du client → ").strip()
            secteur = input("  Secteur → ").strip()
            besoin = input("  Besoin → ").strip()
            analyse = analyser_prospect(nom, secteur, besoin)
            proposition = generer_proposition(nom, secteur, besoin, analyse)
            ajouter_interaction(nom, "proposition_commerciale", proposition)
            with open(f"proposition_{nom.replace(' ', '_')}.txt", "w", encoding="utf-8") as f:
                f.write(proposition)
            print(f"\n  ✅ Proposition sauvegardée → proposition_{nom.replace(' ', '_')}.txt")

        elif choix == "3":
            nom = input("  Nom → ").strip()
            secteur = input("  Secteur → ").strip()
            besoin = input("  Problème détecté → ").strip()
            ajouter_client(nom, secteur, besoin)
            email = rediger_email_prospection(nom, secteur, besoin)
            ajouter_interaction(nom, "email_prospection", email)

        elif choix == "4":
            lister_clients()
            nom = input("\n  Nom du client à relancer → ").strip()
            relance = suivi_relance(nom)
            ajouter_interaction(nom, "email_relance", relance)

        elif choix == "5":
            lister_clients()

        elif choix == "6":
            rapport_pipeline_commercial()


if __name__ == "__main__":
    menu()
