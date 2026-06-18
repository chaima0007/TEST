"""
AGENT EMAIL — Séquences cold outreach + nurturing automatisées
Génère les emails parfaits pour chaque situation commerciale.
Niveau copywriter à 500€/heure.

Usage : python agent_email.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

ENTREPRISE = {
    "nom": "Caelum Partners",
    "fondatrice": "Chaima Mhadbi",
    "email": "contact@caelumpartners.agency",
    "site": "caelumpartners.agency",
    "services": {
        "site_web": "Site web premium à 500€ livré en 7 jours",
        "automation": "Automatisation IA simple à 1500€",
        "pack": "Pack complet IA + Web + Marketing à 3000€",
    },
    "proposition": "Votre entreprise automatisée avec l'IA, en moins de 30 jours."
}

SYSTEM_EMAIL = f"""Tu es le meilleur copywriter email B2B au monde.
Tu écris pour {ENTREPRISE['nom']} — {ENTREPRISE['proposition']}
Fondatrice : {ENTREPRISE['fondatrice']} | {ENTREPRISE['email']}

Tes emails sont :
- Courts : maximum 150 mots (les décideurs lisent en 15 secondes)
- Personnalisés : une référence spécifique au prospect
- Value-first : valeur avant de demander quelque chose
- Un seul CTA : une seule action demandée
- Signature : {ENTREPRISE['fondatrice']} — {ENTREPRISE['nom']} | {ENTREPRISE['site']}

Tu n'utilises JAMAIS : "J'espère que", "Je me permets", "N'hésitez pas"
Tu utilises : des faits, des chiffres, des résultats concrets."""


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


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*60}\n  {label}\n{'═'*60}\n")
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=1500),
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
# 1. COLD EMAIL — Premier contact à froid
# ─────────────────────────────────────────────────────────────

def cold_email():
    print("\n  ── COLD EMAIL ──")
    nom = input("  Nom du prospect → ").strip()
    entreprise = input("  Entreprise → ").strip()
    secteur = input("  Secteur → ").strip()
    probleme = input("  Problème probable qu'il a → ").strip()
    service = input("  Service à proposer (site_web/automation/pack) → ").strip() or "site_web"

    streamer(
        SYSTEM_EMAIL + "\n\nGénère 3 versions du cold email (A/B/C test) :\nVersion A : approche problème\nVersion B : approche résultat chiffré\nVersion C : approche curiosité/question",
        f"""Prospect : {nom} | Entreprise : {entreprise} | Secteur : {secteur}
Problème identifié : {probleme}
Service à proposer : {ENTREPRISE['services'].get(service, service)}
Objectif : obtenir une réponse ou un rendez-vous""",
        f"COLD EMAIL — {nom} / {entreprise}"
    )


# ─────────────────────────────────────────────────────────────
# 2. SÉQUENCE DE RELANCE — 5 emails sur 14 jours
# ─────────────────────────────────────────────────────────────

def sequence_relance():
    print("\n  ── SÉQUENCE RELANCE 5 EMAILS ──")
    nom = input("  Nom du prospect → ").strip()
    entreprise = input("  Entreprise → ").strip()
    contexte = input("  Contexte (pas de réponse depuis, avancement...) → ").strip()

    streamer(
        SYSTEM_EMAIL + """

Génère une séquence de 5 emails de relance sur 14 jours.
Pour chaque email :
📅 J+X — OBJET : [...]
---
[Corps de l'email]
---
Stratégie : chaque email apporte quelque chose de nouveau (article, insight, offre limitée...)
Ne jamais répéter la même approche.""",
        f"""Prospect : {nom} | Entreprise : {entreprise}
Contexte : {contexte}
Service : {ENTREPRISE['services']['site_web']}""",
        f"SÉQUENCE RELANCE — {nom}"
    )


# ─────────────────────────────────────────────────────────────
# 3. EMAIL DE PROPOSITION — Envoyer un devis
# ─────────────────────────────────────────────────────────────

def email_proposition():
    print("\n  ── EMAIL DE PROPOSITION ──")
    nom = input("  Nom du client → ").strip()
    service = input("  Service (site_web/automation/pack) → ").strip() or "site_web"
    besoins = input("  Besoins spécifiques discutés → ").strip()
    budget = input("  Budget évoqué (optionnel) → ").strip()

    service_info = ENTREPRISE["services"].get(service, "")

    streamer(
        SYSTEM_EMAIL + """

Génère l'email de proposition parfait qui :
1. Récapitule les besoins en montrant que tu as bien compris
2. Présente la solution sur mesure
3. Donne le prix clairement (pas de flou)
4. Montre le ROI / valeur perçue
5. Crée l'urgence (délai, disponibilité)
6. CTA unique : "Pouvez-vous confirmer d'ici vendredi ?"

Attache mentalement une proposition PDF (à générer séparément).""",
        f"""Client : {nom} | Service : {service_info}
Besoins : {besoins} | Budget évoqué : {budget or 'non précisé'}""",
        f"EMAIL PROPOSITION — {nom}"
    )


# ─────────────────────────────────────────────────────────────
# 4. EMAIL DE NURTURING — Entretenir la relation (newsletter)
# ─────────────────name───────────────────────────────────────

def email_nurturing():
    print("\n  ── EMAIL NURTURING / NEWSLETTER ──")
    sujet = input("  Sujet de valeur à partager → ").strip()
    cible = input("  Cible (PME/startup/DSI/tous) → ").strip() or "PME"

    streamer(
        SYSTEM_EMAIL + """

Génère un email de nurturing qui apporte de la valeur sans vendre.
Structure :
- Sujet accrocheur (35 chars max)
- Preview text (80 chars)
- Corps : 1 insight actionnable, 1 exemple concret, 1 mini-tips
- CTA soft : lire un article, répondre à une question
- Ton : expert qui partage, pas vendeur

Objectif : que le prospect pense "cette personne est vraiment utile".""",
        f"Sujet : {sujet}\nCible : {cible}\nEntreprise : {ENTREPRISE['nom']}",
        f"EMAIL NURTURING — {sujet}"
    )


# ─────────────────────────────────────────────────────────────
# 5. EMAIL DE BIENVENUE — Onboarding nouveau client
# ─────────────────────────────────────────────────────────────

def email_bienvenue():
    print("\n  ── EMAIL DE BIENVENUE CLIENT ──")
    nom = input("  Nom du nouveau client → ").strip()
    service = input("  Service acheté → ").strip()
    prochaine_etape = input("  Prochaine étape concrète → ").strip()

    streamer(
        SYSTEM_EMAIL + """

Génère l'email de bienvenue parfait pour un nouveau client.
Il doit :
1. Confirmer la décision (validation émotionnelle)
2. Présenter les prochaines étapes clairement (J+1, J+3, J+7)
3. Donner un accès rapide à ce dont ils ont besoin
4. Présenter le point de contact dédié
5. Créer l'enthousiasme pour ce qui arrive

Ton : chaleureux mais professionnel. Pas de sur-promesse.""",
        f"Client : {nom} | Service : {service} | Prochaine étape : {prochaine_etape}",
        f"EMAIL BIENVENUE — {nom}"
    )


# ─────────────────────────────────────────────────────────────
# 6. OBJET D'EMAIL — A/B test de lignes d'objet
# ─────────────────────────────────────────────────────────────

def generer_objets():
    print("\n  ── GÉNÉRATEUR D'OBJETS EMAIL ──")
    contexte = input("  Contexte de l'email → ").strip()
    nb = input("  Combien d'objets ? (défaut: 10) → ").strip()

    streamer(
        """Tu es un expert en email marketing avec 10+ ans d'expérience.
Tu génères des lignes d'objet qui maximisent le taux d'ouverture.
Techniques : curiosité, chiffre, personnalisation [Prénom], urgence, bénéfice direct.
Classe par type : Curiosité / Chiffre / Bénéfice / Urgence / Question""",
        f"Contexte : {contexte}\nNombre : {nb or 10}\nEntreprise : {ENTREPRISE['nom']}",
        "OBJETS EMAIL — A/B Testing"
    )


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT EMAIL — Copywriting niveau 500€/heure")
    print("  Caelum Partners")
    print("═"*60)

    while True:
        print("\n  1. Cold email — Premier contact")
        print("  2. Séquence relance — 5 emails sur 14 jours")
        print("  3. Email de proposition — Envoyer un devis")
        print("  4. Email nurturing — Apporter de la valeur")
        print("  5. Email bienvenue — Onboarding nouveau client")
        print("  6. Générateur d'objets — A/B test")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            cold_email()
        elif choix == "2":
            sequence_relance()
        elif choix == "3":
            email_proposition()
        elif choix == "4":
            email_nurturing()
        elif choix == "5":
            email_bienvenue()
        elif choix == "6":
            generer_objets()
        else:
            print("  Choix invalide.")
