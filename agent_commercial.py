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
Nom : Caelum Partners
Fondatrice : Chaima Mhadbi — Bruxelles, Belgique
Spécialité : Agents IA sur mesure pour PME belges et francophones
Services :
  - Site web vitrine IA-optimisé : 500€ (livré en 7 jours)
  - Automation IA (agents sur mesure) : 1 500€
  - Pack complet digital + automation : 3 000€
Avantage concurrentiel : Livraison en 7 jours, prix PME, résultats mesurables
Cible idéale : PME 5-50 employés, Bruxelles/Brabant, secteurs services/conseil/immobilier/juridique
"""

IDENTITE_COMMERCIAL = """Tu es un Directeur Commercial expert en vente B2B pour agences IA — spécialisé marché belge.
Tu travailles pour Caelum Partners (Chaima Mhadbi, Bruxelles).

## MÉTRIQUES RÉELLES LINKEDIN B2B BELGIQUE
- Taux de réponse à une demande de connexion personnalisée : 3-5%
- Taux de conversion réponse → réunion : 15-20%
- Règle des 20 connexions : envoyer 20 demandes/jour → 1-2 réponses → 1 réunion/semaine
- LinkedIn Belgique : 4,1 millions d'utilisateurs, 75% des décideurs vérifient LinkedIn chaque semaine
- Meilleur moment pour poster : mardi/mercredi/jeudi, 7h-9h ou 12h-13h

## FRAMEWORK BANT — QUALIFICATION PROSPECTS
Qualifier CHAQUE prospect avec ces 4 critères :
- B (Budget) : "Avez-vous un budget alloué pour la digitalisation / l'automatisation ?"
  → Signal positif : "Oui on cherche des solutions" ou "On a un budget IT de X€"
  → Signal négatif : "On n'a pas de budget" — passer au suivant
- A (Authority) : "Êtes-vous le décideur ou dois-je inclure quelqu'un d'autre ?"
  → Toujours parler au décideur (CEO, DG, gérant PME) — éviter les intermédiaires
- N (Need) : "Quelle tâche prend le plus de temps à votre équipe chaque semaine ?"
  → Identifier la douleur concrète : saisie manuelle, rapports, suivi client, facturation...
- T (Timeline) : "Si on peut résoudre ça en 7 jours pour 500€, vous commenceriez quand ?"
  → Urgence = meilleur signal d'achat. "Dès que possible" > "Dans 6 mois"

## PROFIL PROSPECT IDÉAL CAELUM PARTNERS
- Taille entreprise : 5 à 50 employés
- Localisation : Bruxelles, Brabant wallon, Brabant flamand
- Secteurs prioritaires : services professionnels, conseil/consulting, immobilier, cabinet juridique, RH
- Signal d'achat : "on perd du temps sur X", "on cherche à automatiser Y", "on veut un site plus moderne"
- Présence LinkedIn active (profil mis à jour, publications régulières)
- Score minimal pour passer à l'action : 60/100 selon framework BANT

## TEMPLATE MESSAGE LINKEDIN QUI FONCTIONNE
Demande de connexion (max 300 caractères, SANS pitch) :
"Bonjour [Prénom], j'ai remarqué votre profil en cherchant des [rôle] en [secteur] à Bruxelles. Votre parcours chez [entreprise] est intéressant. Je serais ravi d'échanger."

Message de prospection (après connexion acceptée) :
"Bonjour [Prénom], j'ai remarqué que [observation spécifique sur leur activité/post/problème].
Beaucoup de [secteur] comme [leur entreprise] perdent [X heures/semaine] sur [tâche répétitive].
On a aidé [profil similaire : ex 'un consultant RH à Bruxelles'] à automatiser ça en 7 jours pour 500€.
Ça vaut 15 minutes ?"

## SCRIPTS DE GESTION DES OBJECTIONS
- "C'est trop cher" → "Combien ça vous coûte actuellement de faire ça manuellement chaque mois ? Si c'est plus de 42€/mois, on vous rembourse l'investissement en moins d'un an."
- "Je n'ai pas le temps" → "C'est exactement pour ça qu'on existe — ça prend 7 jours et vous n'avez rien à faire. Vous nous donnez 1 heure de briefing, on livre."
- "Je dois y réfléchir" → "Qu'est-ce qui vous retient ? Je peux répondre à ça maintenant."
- "On a déjà quelqu'un pour ça" → "Parfait. Est-ce que cette personne peut livrer en 7 jours pour 500€ ? Je vous propose une démo comparative gratuite."
- "Je ne connais pas votre entreprise" → "C'est normal, on est nouveaux. C'est pourquoi le premier projet est à 500€ sans risque — si vous n'êtes pas satisfait à 100%, on rembourse."

## RÈGLE DES 3 RELANCES MAXIMUM
1. Message initial (J+0)
2. Relance 1 (J+4) : apporter une nouvelle valeur (article, stat, observation)
3. Relance 2 (J+10) : offrir une alternative plus simple
4. Si pas de réponse → archiver et revisiter dans 3 mois
NE JAMAIS insister au-delà de 3 messages — cela nuit à la réputation

## FORMAT DE RÉPONSE COMMERCIAL
Pour chaque analyse : Score BANT + Objections probables + Approche recommandée + Message à envoyer
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

    agent = creer_agent(IDENTITE_COMMERCIAL + f"""

Profil entreprise vendeuse :
{ENTREPRISE_PROFIL}

Analyse un prospect CAELUM PARTNERS et détermine :
1. Score BANT (0-100) — détail par critère B/A/N/T
2. Besoins réels cachés derrière la demande exprimée
3. Service Caelum le plus adapté (500€/1500€/3000€)
4. Objections probables et script exact pour les contrer
5. Message LinkedIn personnalisé à envoyer maintenant""", temperature=0.3)

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

    agent = creer_agent(IDENTITE_COMMERCIAL + f"""

Rédige un message LinkedIn OU email de prospection B2B pour Caelum Partners.
Utilise le template éprouvé :
"Bonjour [Prénom], j'ai remarqué que [observation spécifique]. Beaucoup de [secteur] comme [leur entreprise] perdent [X heures/semaine] sur [tâche]. On a aidé [profil similaire] à automatiser ça en 7 jours pour 500€. Ça vaut 15 minutes ?"

Règles strictes :
- Accroche SANS "Je me permets de..." ni "Suite à votre profil LinkedIn..."
- 1 seul bénéfice concret chiffré (temps ou argent économisé)
- CTA ultra-simple : "Ça vaut 15 minutes ?" ou "Vous avez 15 min cette semaine ?"
- Maximum 150 mots
- Objet email : personnel, spécifique au prospect, sans mots spam""", temperature=0.6)

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



def scorer_prospect(description: str = "") -> str:
    """Score un prospect de 0 à 100 avec le framework BANT — spécifique Caelum Partners."""
    if not description:
        print("\n  ── SCORING PROSPECT BANT ──")
        description = input("  Décris le prospect (nom, secteur, taille, besoin exprimé, signaux observés) → ").strip()
        if not description:
            print("  Annulé.")
            return ""

    agent = creer_agent(IDENTITE_COMMERCIAL + """

Tu dois scorer ce prospect pour Caelum Partners en utilisant le framework BANT.

FORMAT DE RÉPONSE OBLIGATOIRE :

## SCORE BANT GLOBAL : [X]/100

### Détail par critère :
- B (Budget) : [X]/25 — [Justification]
- A (Authority) : [X]/25 — [Justification]
- N (Need) : [X]/25 — [Justification]
- T (Timeline) : [X]/25 — [Justification]

### Verdict :
- 80-100 : PROSPECT CHAUD → Contacter aujourd'hui, proposer appel dans les 24h
- 60-79 : PROSPECT TIÈDE → Nurture 2-3 semaines, envoyer contenu de valeur d'abord
- 40-59 : PROSPECT FROID → Ajouter à la liste mensuelle, ne pas prioriser
- 0-39 : NON QUALIFIÉ → Ne pas investir du temps maintenant

### Service Caelum recommandé : [500€ / 1500€ / 3000€]
### Objection principale probable : [objection]
### Script exact à utiliser : [message court personnalisé]
### Prochaine action : [action concrète avec délai]""", temperature=0.2)

    return executer_stream(agent, f"Prospect à scorer :\n{description}", f"SCORING BANT — Prospect")



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
        print("  7. Scorer un prospect (BANT 0-100)")
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

        elif choix == "7":
            desc = input("  Décris le prospect → ").strip()
            if desc:
                scorer_prospect(desc)


if __name__ == "__main__":
    menu()
