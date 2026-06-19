"""
AGENT GROWTH — Growth hacking autonome pour Caelum Partners
Trouve les leviers de croissance, génère des expériences,
optimise les canaux, double le CA chaque trimestre.

Usage : python agent_growth.py
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

CONTEXTE = {
    "entreprise": "Caelum Partners",
    "fondatrice": "Chaima Mhadbi",
    "localisation": "Bruxelles, Belgique",
    "services": ["Site web 500€", "Automation IA 1500€", "Pack complet 3000€"],
    "cible": "PME 5-50 employés, Bruxelles/Brabant, secteurs: services/conseil/immobilier/juridique",
    "canal_principal": "LinkedIn",
    "site": "caelumpartners.agency",
    "statut": "0 clients — objectif premier client ASAP",
    "budget_marketing": "0€ (bootstrapped)",
    "avantage": "Livraison en 7 jours, prix PME, IA sur mesure",
}

# ─── KNOWLEDGE BASE GROWTH — DONNÉES RÉELLES ──────────────────────────────────

LINKEDIN_ALGO_2024_2025 = """
## ALGORITHME LINKEDIN 2024-2025 — RÈGLES RÉELLES

### Horaires optimaux de publication (heure belge — CET/CEST)
- Mardi : 7h-9h (pic engagement matin) ou 12h-13h (pause déjeuner)
- Mercredi : 7h-9h (meilleur jour global) ou 17h-18h (fin de journée)
- Jeudi : 12h-13h (deuxième meilleur créneau hebdo)
- À ÉVITER : lundi matin (inbox pleine), vendredi après-midi, weekends

### Structure d'un post viral LinkedIn (HOOK + STORY + INSIGHT + CTA)
1. HOOK (ligne 1 — décide si "voir plus" est cliqué) :
   - Question provocatrice : "Pourquoi les PME belges perdent-elles 10h/semaine sur des tâches qu'une IA ferait en 30 secondes ?"
   - Affirmation audacieuse : "J'ai automatisé en 7 jours ce qu'une assistante faisait en 20h/semaine."
   - Stat surprenante : "87% des PME belges n'ont pas encore automatisé leur facturation. Voici pourquoi c'est une erreur."
2. STORY (2-4 lignes) : situation concrète, personnage identifiable, problème réel
3. INSIGHT (2-3 lignes) : la leçon, la solution, le principe actionnable
4. CTA (1 ligne) : "Commentez 'DEMO' pour recevoir..." ou question ouverte qui invite à commenter

### Règles algorithmiques LinkedIn 2024
- Les 60 premières minutes après publication sont décisives (golden hour)
- Répondre à TOUS les commentaires dans les 2 premières heures = signal fort
- Les posts avec 3-5 hashtags pertinents performent mieux
- Les posts avec 1-3 images ou carousels ont 3x plus de portée organique
- Les posts qui genèrent des commentaires longs > des simples likes
- Hashtags recommandés : #PMEBelgique #AutomatisationIA #AgentsIA #Bruxelles #Digitalisation

### Demandes de connexion — règles
- Maximum 300 caractères, personnalisée (mentionner 1 élément spécifique de leur profil)
- JAMAIS pitcher dans la demande de connexion
- Taux d'acceptation moyen d'une demande personnalisée : 35-45%
- Template : "Bonjour [Prénom], j'ai vu votre [post/article] sur [sujet]. Votre point sur [élément précis] m'a interpellé. Je travaille dans le même secteur à Bruxelles. Ravi d'échanger."

### Stats LinkedIn Belgique
- 4,1 millions d'utilisateurs actifs
- 75% des décideurs (C-level) vérifient LinkedIn chaque semaine
- Taux d'engagement moyen B2B : 2-3% (vs 0,5% Facebook)
- Meilleur réseau B2B pour la prospection en Belgique (devant Xing, Twitter)
"""

GROWTH_PLAYBOOK = """
## GROWTH PLAYBOOK CAELUM PARTNERS — 0 À PREMIER CLIENT

### Semaine 1 — Fondations LinkedIn
- Jour 1 : Optimiser profil (photo, bannière Caelum, headline avec bénéfice client)
- Jour 2-7 : Envoyer 20 demandes de connexion/jour aux prospects idéaux (PME Bruxelles)
- Posts : 3 posts cette semaine (lundi, mercredi, vendredi) — thèmes : problème client, solution IA, case study

### Objectif semaine 1 :
- 100+ nouvelles connexions
- 3 réponses à des messages de prospection
- 1 réunion planifiée

### Conversion entonnoir réaliste :
- 100 demandes → 35-45 acceptées → 5-10 réponses aux messages → 1-2 réunions → 0,5 client
- Soit : 200 demandes pour obtenir 1 client (environ 2 semaines intensives)
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


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=3000),
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


def sauvegarder(nom, contenu):
    os.makedirs("fichiers/growth", exist_ok=True)
    fichier = f"fichiers/growth/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


# ─────────────────────────────────────────────────────────────
# 1. MOTEUR DE CROISSANCE — Les 10 leviers à activer maintenant
# ─────────────────────────────────────────────────────────────

def moteur_croissance():
    r = streamer(
        """Tu es le meilleur Growth Hacker au monde, spécialisé en agences IA B2B.
Tu travailles pour Caelum Partners — startup belge d'agents IA.
Tu identifies les 10 leviers de croissance les plus puissants
adaptés au marché belge et européen francophone.

FORMAT :
🚀 LEVIER [N] — [Nom du levier]
   Canal : [LinkedIn/Email/SEO/Partenariats/...]
   Effort : [Faible/Moyen/Élevé]
   Impact : [Faible/Moyen/Élevé]
   Délai résultat : [X jours/semaines]
   Action concrète : [Ce qu'on fait demain matin]
   Métrique de succès : [Comment mesurer]
   Coût : [0€/faible/moyen]""",
        f"""Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}
Objectif : 10 clients dans 90 jours
Budget marketing : 0€ (bootstrapped)
Avantage concurrentiel : IA + rapidité + prix accessible""",
        "MOTEUR DE CROISSANCE — 10 leviers à activer"
    )
    sauvegarder("moteur_croissance", r)


# ─────────────────────────────────────────────────────────────
# 2. EXPÉRIENCES GROWTH — 30 tests A/B à lancer cette semaine
# ─────────────────────────────────────────────────────────────

def experiences_growth():
    r = streamer(
        """Tu es un expert en growth experiments.
Tu génères 30 micro-expériences à tester cette semaine pour accélérer la croissance.
Chaque expérience prend moins de 2 heures à mettre en place.

FORMAT :
EXP[N] — [Nom]
   Hypothèse : Si je [action], alors [résultat attendu]
   Durée test : [X jours]
   Effort : [X heures]
   Mesure : [métrique clé]
   Succès = [seuil chiffré]
   Canal : [LinkedIn/Email/Site/...]""",
        f"Entreprise : {CONTEXTE['entreprise']} | Services : {CONTEXTE['services']} | Cible : {CONTEXTE['cible']}",
        "30 EXPÉRIENCES GROWTH — Cette semaine"
    )
    sauvegarder("experiences_growth", r)


# ─────────────────────────────────────────────────────────────
# 3. MACHINE À LEADS — Système automatique d'acquisition
# ─────────────────────────────────────────────────────────────

def machine_leads():
    r = streamer(
        """Tu es expert en acquisition B2B.
Tu conçois une machine à leads complète et automatisée pour une agence IA.
Le système doit générer des leads qualifiés SANS budget publicitaire.

FORMAT :
## MACHINE À LEADS — Caelum Partners

### CANAL 1 : LinkedIn (principal)
[Routine quotidienne, scripts, outils, KPIs]

### CANAL 2 : SEO / Contenu
[Stratégie, mots-clés, fréquence, types de contenu]

### CANAL 3 : Partenariats
[Types de partenaires, approche, deal structure]

### CANAL 4 : Référencement (bouche à oreille)
[Programme référral, incentives, scripts]

### CANAL 5 : Communautés
[Quelles communautés, comment y apporter de la valeur]

### AUTOMATISATION
[Ce qui peut être automatisé avec les agents IA]

### OBJECTIF : 10 leads qualifiés/semaine""",
        f"Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}",
        "MACHINE À LEADS — Acquisition automatique"
    )
    sauvegarder("machine_leads", r)


# ─────────────────────────────────────────────────────────────
# 4. FUNNEL DE CONVERSION — De inconnu à client payant
# ─────────────────────────────────────────────────────────────

def funnel_conversion():
    r = streamer(
        """Tu es expert en conversion B2B.
Tu conçois le funnel de conversion parfait pour une agence IA.
Chaque étape doit maximiser la conversion à l'étape suivante.

FORMAT :
## FUNNEL CAELUM PARTNERS

ÉTAPE 1 — DÉCOUVERTE
  Déclencheur : [comment ils trouvent Caelum]
  Message : [ce qu'ils voient en premier]
  Conversion → : [action à faire]
  Taux cible : X%

ÉTAPE 2 — INTÉRÊT
...jusqu'à...

ÉTAPE 6 — CLIENT FIDÈLE (upsell/référence)

## SCRIPTS & TEMPLATES
[Messages prêts pour chaque transition]

## AUTOMATISATION PAR AGENT IA
[Quel agent gère chaque étape]""",
        f"Services : {CONTEXTE['services']} | Prix : 500€/1500€/3000€ | Cible : PME Belgique",
        "FUNNEL DE CONVERSION — De prospect à client fidèle"
    )
    sauvegarder("funnel_conversion", r)


# ─────────────────────────────────────────────────────────────
# 5. VIRAL LOOP — Faire grandir l'empire par effet viral
# ─────────────────────────────────────────────────────────────

def viral_loop():
    r = streamer(
        """Tu es expert en growth viral et effets de réseau.
Tu conçois un système de croissance virale pour Caelum Partners.
Chaque client doit amener naturellement d'autres clients.

FORMAT :
## VIRAL LOOP — Caelum Partners

### MÉCANISME VIRAL PRINCIPAL
[Description du loop central]

### INCITATIONS (pourquoi partager ?)
- Client : [bénéfice]
- Référé : [bénéfice]

### PROGRAMME RÉFÉRRAL
[Structure, commission, processus]

### CONTENU VIRAL
[Types de contenu que les clients partagent naturellement]

### SOCIAL PROOF MACHINE
[Avis, témoignages, cas clients — comment les collecter et diffuser]

### PARTENARIATS MULTIPLICATEURS
[Qui peut recommander Caelum à 100 clients d'un coup ?]

### OBJECTIF : coefficient viral k > 0.3""",
        f"Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}",
        "VIRAL LOOP — Croissance exponentielle"
    )
    sauvegarder("viral_loop", r)


# ─────────────────────────────────────────────────────────────
# 6. PLAN CROISSANCE 90 JOURS — De 0 à 10 clients
# ─────────────────────────────────────────────────────────────

def plan_90_jours():
    r = streamer(
        """Tu es le Growth Director d'une startup IA qui scale de 0 à 10 clients en 90 jours.
Tu crées le plan d'exécution jour par jour pour les 30 premiers jours,
puis semaine par semaine pour les 60 jours suivants.

FORMAT :
## OBJECTIF : 10 clients payants en 90 jours (15 000€+ CA)

### MOIS 1 — FONDATIONS & PREMIERS CLIENTS
Semaine 1 (J1-J7) :
  Lundi : ...
  Mardi : ...
  ...
  Objectif : [X leads qualifiés]
  Agent à utiliser : [agent.py]

Semaine 2 ...
Semaine 3 ...
Semaine 4 ...

### MOIS 2 — ACCÉLÉRATION
[Plan hebdomadaire]

### MOIS 3 — SCALE
[Plan hebdomadaire]

### KPIs HEBDOMADAIRES
[Tableau de bord de suivi]

### AGENTS IA À UTILISER
[Quel agent pour quelle tâche]""",
        f"Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}\nBudget : 0€\nÉquipe : 1 personne + agents IA",
        "PLAN 90 JOURS — De 0 à 10 clients"
    )
    sauvegarder("plan_90_jours", r)



# ─────────────────────────────────────────────────────────────
# 7. CAMPAGNE SEMAINE — Plan complet 7 jours LinkedIn
# ─────────────────────────────────────────────────────────────

def generer_campagne_semaine():
    """Génère une campagne LinkedIn complète sur 7 jours : 3 posts + 20 connexions + 5 follow-ups."""
    from datetime import datetime
    semaine_num = datetime.now().strftime("Semaine %W — %B %Y")

    r = streamer(
        f"""Tu es un Growth Expert LinkedIn spécialisé B2B belge.
Tu connais les données réelles du marché :

{LINKEDIN_ALGO_2024_2025}

{GROWTH_PLAYBOOK}

Contexte entreprise : {json.dumps(CONTEXTE, ensure_ascii=False)}

GÉNÈRE UNE CAMPAGNE LINKEDIN COMPLÈTE POUR {semaine_num} :

## 3 POSTS LINKEDIN COMPLETS (rédigés, prêts à publier)

### POST 1 — MARDI 8h (Éducatif / Problème client)
[Rédige le post complet avec hook, story, insight, CTA — 150-250 mots]
Hashtags : [liste exacte]
Image suggérée : [description]

### POST 2 — MERCREDI 12h (Témoignage / Résultat)
[Rédige le post complet]
Hashtags : [liste exacte]

### POST 3 — JEUDI 12h (Offre / CTA direct)
[Rédige le post complet — peut inclure une offre limitée]
Hashtags : [liste exacte]

## 20 MESSAGES DE DEMANDE DE CONNEXION (personnalisés par secteur)

5 messages pour : Consultants/Coachs Bruxelles
5 messages pour : Agences immobilières Brabant
5 messages pour : Cabinets d'avocats/notaires Bruxelles
5 messages pour : PME services RH/recrutement

[Chaque message : max 300 caractères, personnalisé, SANS pitch]

## 5 MESSAGES DE SUIVI (pour connexions acceptées il y a 2-3 jours)

[5 messages de prospection utilisant le template éprouvé Caelum Partners]

## PLANNING JOUR PAR JOUR
Lundi : [actions]
Mardi : [post #1 + X connexions + répondre commentaires]
...
Dimanche : [revue des résultats]

## KPIs À SUIVRE CETTE SEMAINE
- Connexions envoyées : objectif 100
- Connexions acceptées : objectif 35-45
- Réponses aux messages : objectif 3-5
- Réunions planifiées : objectif 1-2
""",
        f"Données : {json.dumps(CONTEXTE, ensure_ascii=False)}",
        f"CAMPAGNE SEMAINE COMPLÈTE — {semaine_num}"
    )
    sauvegarder("campagne_semaine", r)
    return r


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT GROWTH — Growth hacking Caelum Partners")
    print("  Objectif : 10 clients en 90 jours")
    print("═"*65)

    while True:
        print("\n  1. Moteur de croissance — 10 leviers à activer")
        print("  2. 30 expériences growth — tests cette semaine")
        print("  3. Machine à leads — acquisition automatique")
        print("  4. Funnel de conversion — prospect → client fidèle")
        print("  5. Viral loop — croissance exponentielle")
        print("  6. Plan 90 jours — de 0 à 10 clients")
        print("  7. Campagne semaine complète — 3 posts + 20 connexions + 5 follow-ups")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            moteur_croissance()
        elif choix == "2":
            experiences_growth()
        elif choix == "3":
            machine_leads()
        elif choix == "4":
            funnel_conversion()
        elif choix == "5":
            viral_loop()
        elif choix == "6":
            plan_90_jours()
        elif choix == "7":
            generer_campagne_semaine()
        else:
            print("  Choix invalide.")
