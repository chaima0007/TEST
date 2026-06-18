"""
ORCHESTRATEUR AUTONOME D'ENTREPRISE
Agent central qui analyse une demande client et délègue automatiquement
aux bons agents spécialisés — zéro intervention humaine.

Usage : python orchestrateur.py
"""

import os
import sys
import json
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Clé API manquante. Tape : set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"


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


def agent(nom, instructions, prompt, effort="normal"):
    """Lance un agent et retourne sa réponse en streaming."""
    print(f"\n{'─'*60}")
    print(f"  ► {nom}")
    print(f"{'─'*60}")

    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(
            temperature=0.2 if effort == "precis" else 0.6,
            max_output_tokens=2048,
        ),
    )
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


# ─────────────────────────────────────────────────────────────
# AGENT 0 : CERVEAU CENTRAL — Analyse et délègue
# ─────────────────────────────────────────────────────────────

def cerveau_central(demande_client):
    """Analyse la demande et décide quels agents activer."""

    reponse = agent(
        "Cerveau Central — Analyse & Planification",
        """Tu es le cerveau d'une entreprise d'automatisation IA.
Ton rôle : analyser toute demande client et produire un plan d'action JSON.
Réponds UNIQUEMENT avec ce JSON :
{
  "type": "code|rapport|securite|email|analyse|formation",
  "priorite": "haute|moyenne|faible",
  "agents_necessaires": ["liste des agents à activer"],
  "resume": "résumé de la demande en 1 phrase",
  "actions": ["action 1", "action 2", "action 3"]
}""",
        f"Demande client : {demande_client}",
        effort="precis"
    )

    try:
        debut = reponse.find("{")
        fin = reponse.rfind("}") + 1
        return json.loads(reponse[debut:fin])
    except Exception:
        return {
            "type": "general",
            "priorite": "moyenne",
            "agents_necessaires": ["Agent Généraliste"],
            "resume": demande_client,
            "actions": ["Traiter la demande"],
        }


# ─────────────────────────────────────────────────────────────
# AGENTS SPÉCIALISÉS
# ─────────────────────────────────────────────────────────────

def agent_code(demande, contexte):
    return agent(
        "Agent Code — Développeur Senior",
        """Tu es un développeur senior full-stack expert en Python, JavaScript, et IA.
Tu génères du code propre, sécurisé, bien structuré.
Tu expliques chaque décision technique importante.""",
        f"Demande : {demande}\nContexte : {contexte}",
    )


def agent_analyse(demande, contexte):
    return agent(
        "Agent Analyse — Consultant Business",
        """Tu es un consultant business expert en analyse de marché et stratégie.
Tu produis des analyses claires avec données chiffrées, avantages/risques et recommandations concrètes.""",
        f"Demande : {demande}\nContexte : {contexte}",
    )


def agent_rapport(demande, resultats_precedents):
    return agent(
        "Agent Rapport — Rédacteur Exécutif",
        """Tu es un rédacteur exécutif. Tu transformes des analyses techniques en rapports
professionnels clairs, structurés, prêts à envoyer à un client ou directeur.
Format : titre, résumé, points clés, recommandations, conclusion.""",
        f"Demande : {demande}\n\nDonnées à synthétiser :\n{resultats_precedents}",
    )


def agent_email(destinataire, sujet, contenu_technique):
    return agent(
        "Agent Email — Communication Professionnelle",
        """Tu es un expert en communication d'entreprise.
Tu rédiges des emails professionnels, clairs, convaincants et personnalisés.
Tu adaptes le ton selon le destinataire (client, partenaire, équipe).""",
        f"Destinataire : {destinataire}\nSujet : {sujet}\nContenu à communiquer : {contenu_technique}",
    )


def agent_formation(sujet, niveau):
    return agent(
        "Agent Formation — Professeur Expert",
        """Tu es un formateur expert. Tu crées des modules de formation structurés :
objectifs pédagogiques, contenu progressif, exercices pratiques, évaluation.
Tu adaptes le niveau (débutant/intermédiaire/avancé).""",
        f"Sujet : {sujet}\nNiveau : {niveau}",
    )


def agent_securite_rapide(contenu):
    return agent(
        "Agent Sécurité — Vérification Rapide",
        """Tu es un expert cybersécurité. Vérifie rapidement si le contenu fourni
contient des risques : données sensibles exposées, failles, mauvaises pratiques.
Réponds : RISQUE DÉTECTÉ ou SÉCURISÉ + explication courte.""",
        f"Contenu à vérifier : {contenu[:1000]}",
        effort="precis"
    )


# ─────────────────────────────────────────────────────────────
# ORCHESTRATEUR PRINCIPAL
# ─────────────────────────────────────────────────────────────

def orchestrateur(demande_client):
    print(f"\n{'═'*60}")
    print("  ORCHESTRATEUR AUTONOME — Traitement en cours")
    print(f"{'═'*60}")
    print(f"\n  Demande : {demande_client}\n")

    # Étape 1 : Analyse centrale
    plan = cerveau_central(demande_client)

    print(f"\n  Type       : {plan.get('type', '?').upper()}")
    print(f"  Priorité   : {plan.get('priorite', '?').upper()}")
    print(f"  Résumé     : {plan.get('resume', '?')}")
    print(f"  Agents     : {', '.join(plan.get('agents_necessaires', []))}")

    resultats = {}
    type_demande = plan.get("type", "general")

    # Étape 2 : Vérification sécurité automatique sur toute demande
    verif = agent_securite_rapide(demande_client)
    resultats["securite"] = verif

    # Étape 3 : Activation des agents selon le type
    if type_demande == "code":
        resultats["code"] = agent_code(demande_client, plan.get("resume", ""))

    elif type_demande == "analyse":
        resultats["analyse"] = agent_analyse(demande_client, plan.get("resume", ""))

    elif type_demande == "email":
        resultats["email"] = agent_email("Client", demande_client, plan.get("resume", ""))

    elif type_demande == "formation":
        resultats["formation"] = agent_formation(demande_client, "adapté")

    else:
        # Demande générale → analyse + rapport
        resultats["analyse"] = agent_analyse(demande_client, plan.get("resume", ""))
        resultats["rapport"] = agent_rapport(
            demande_client,
            resultats.get("analyse", "")
        )

    # Étape 4 : Rapport final automatique
    synthese_finale = agent_rapport(
        demande_client,
        "\n\n".join([f"{k.upper()} :\n{v}" for k, v in resultats.items()])
    )

    # Sauvegarde
    nom_fichier = "rapport_" + demande_client[:30].replace(" ", "_").replace("/", "-") + ".txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"DEMANDE : {demande_client}\n\n")
        f.write(f"PLAN :\n{json.dumps(plan, ensure_ascii=False, indent=2)}\n\n")
        for k, v in resultats.items():
            f.write(f"\n{'='*40}\n{k.upper()}\n{'='*40}\n{v}\n")
        f.write(f"\n{'='*40}\nSYNTHÈSE FINALE\n{'='*40}\n{synthese_finale}\n")

    print(f"\n{'═'*60}")
    print(f"  ✅ Traitement terminé")
    print(f"  📄 Rapport sauvegardé → {nom_fichier}")
    print(f"{'═'*60}\n")

    return synthese_finale


# ─────────────────────────────────────────────────────────────
# INTERFACE
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  BRAS DROIT IA — Orchestrateur Autonome d'Entreprise")
    print("  Spécialisé en solutions Claude & Agents IA")
    print("═" * 60)

    if len(sys.argv) > 1:
        demande = " ".join(sys.argv[1:])
    else:
        print("\nQue dois-je faire pour ton entreprise ?")
        print("Exemples :")
        print("  - Analyse le marché des agents IA en Europe")
        print("  - Crée un email de présentation pour un client banque")
        print("  - Génère un code de chatbot pour site web")
        print("  - Forme mon équipe sur les agents Claude\n")
        demande = input("Ta demande → ").strip()

    if demande:
        orchestrateur(demande)
    else:
        print("Aucune demande saisie.")
