"""
MAÎTRE VÉLOCITÉ CAPITAL — Atteindre une vélocité du capital ≥ 10x en 90 jours
Chaque euro investi doit en générer 10 en 90 jours · Multiplication · Levier maximum

Usage : python agent_maitre_velocite.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """# MAÎTRE VÉLOCITÉ CAPITAL — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es le Maître Vélocité Capital de Caelum Partners.
Ta mission : atteindre une vélocité du capital ≥ 10x en 90 jours.
Chaque euro investi doit générer 10 euros dans les 90 jours suivants.
C'est plus agressif que l'optimisation — c'est de la MULTIPLICATION.

## FORMULE DE VÉLOCITÉ DU CAPITAL
Vélocité = Chiffre d'Affaires / Capital Investi × (365 / Période en jours)
Objectif Caelum : Vélocité ≥ 10 en 90 jours
Exemple : investir 300€ (temps + outils) → générer 3 000€ en 90 jours = vélocité 10x

## STRUCTURE DE COÛT DE CAELUM (avantage structurel exceptionnel)
- Coût variable des services : ~5-15% (uniquement temps de Chaima)
- Marge brute : 85-95% (l'IA remplace les coûts humains classiques)
- Capital initial requis : quasi zéro (pas de stock, pas de locaux, pas d'équipe)
- Coût d'acquisition client : potentiellement 0€ (réseau, LinkedIn, ASBL)
- Délai de production : 7-30 jours selon service

## TECHNIQUES DE LEVIER À VÉLOCITÉ MAXIMALE

### LEVIER 1 — ACQUISITION ZÉRO COÛT
- LinkedIn organique : 0€ d'investissement, potentiellement 1 client en 7 jours
- ASBL réseau : contacts existants → prospects chauds gratuits
- Bouche-à-oreille : ROI infini (0€ coût, chaque référence = revenu pur)

### LEVIER 2 — STRUCTURES DE PRÉPAIEMENT
- Acompte 50% à la signature : capital disponible avant de commencer → vélocité infinie
- Paiement 100% à la signature (offre de lancement avec remise) : cash day 0
- Abonnement annuel prépayé avec remise 20% : 12 mois de CA en 1 transaction

### LEVIER 3 — MODÈLE AGENCE (REVENTE)
- Former d'autres consultants à utiliser l'écosystème Caelum
- Prendre une commission de 20-30% sur leurs revenus générés via Caelum
- Chaque partenaire = nouveau centre de profit sans coût additionnel

### LEVIER 4 — REVENUS RÉCURRENTS COMPOSÉS
- Client unique × revenus récurrents = compound effect
- 10 clients à 300€/mois = 3 000€/mois récurrents → vélocité s'améliore chaque mois

## SCÉNARIOS DE VÉLOCITÉ 10X EN 90 JOURS
- Scénario A (conservateur) : 1 client 3 000€ + 2 clients 1 500€ = 6 000€ sur 300€ investis = 20x
- Scénario B (réaliste) : 3 clients pack + 2 clients automation = 12 000€ sur 500€ = 24x
- Scénario C (agressif) : 5 clients pack + 5 abonnements = 21 000€ sur 700€ = 30x

## FORMAT DE SORTIE OBLIGATOIRE
1. CALCUL DE VÉLOCITÉ ACTUELLE : ratio précis avec diagnostic
2. PLAN 10X EN 90 JOURS : actions semaine par semaine
3. LEVIERS IDENTIFIÉS : les 3 leviers avec le meilleur ROI immédiat
4. SIMULATION : 3 scénarios chiffrés (conservateur / réaliste / agressif)
5. STRUCTURE DE COÛT OPTIMALE : pour maximiser la vélocité à long terme"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.2, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/velocite_capital", exist_ok=True)
    fichier = f"fichiers/velocite_capital/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def calculer_velocite_actuelle():
    r = streamer(
        """Calcule la vélocité actuelle du capital de Caelum Partners avec diagnostic complet.

SITUATION ACTUELLE :
- Capital investi à ce jour : ~0€ (bootstrapped total, utilisation quota gratuit Gemini)
- Revenus générés à ce jour : 0€ (phase pré-lancement)
- Temps investi par Chaima : X heures de développement des 50 agents

CALCUL DE VÉLOCITÉ ACTUELLE :
1. Capital financier investi (€) : estimer le coût réel si externalisé
2. Capital temps investi (heures × valeur horaire) : Chaima × taux horaire marché
3. Capital total investi (financier + temps)
4. Revenus actuels : 0€
5. Vélocité actuelle : 0x (pas encore de clients)

DIAGNOSTIC :
- Pourquoi la vélocité est-elle à 0 ? (normal phase lancement — mais à corriger)
- Qu'est-ce qui empêche la vélocité de démarrer ?
- Quel est le premier levier à actionner pour atteindre vélocité 1x cette semaine ?

BENCHMARK :
- Vélocité standard d'une PME : 1-2x par an
- Vélocité d'une agence web : 3-5x par an
- Vélocité cible Caelum : 10x en 90 jours (4x l'objectif d'une bonne agence)
- Pourquoi 10x est RÉALISTE pour Caelum (marges 85-95%, coût quasi nul)

PREMIÈRE ACTION pour démarrer la vélocité dès cette semaine.""",
        "VÉLOCITÉ ACTUELLE — Diagnostic et calcul Caelum Partners"
    )
    sauvegarder("velocite_actuelle", r)


def concevoir_strategie_10x():
    r = streamer(
        """Conçois le plan précis pour atteindre une vélocité 10x du capital en 90 jours.

HYPOTHÈSE DE BASE :
- Capital investi total (temps + outils) : 500€ équivalent
- Objectif : générer 5 000€ en 90 jours = vélocité 10x minimum

PLAN SEMAINE PAR SEMAINE (13 semaines) :

SEMAINES 1-2 (J1-J14) — AMORÇAGE :
- Objectif : 1 premier client payant (n'importe quel montant)
- Actions quotidiennes (liste numérotée)
- Revenue cible : 500€ minimum

SEMAINES 3-4 (J15-J28) — MOMENTUM :
- Objectif : 2ème et 3ème client
- Systématisation du processus de vente
- Revenue cible : 3 000€ cumulés

SEMAINES 5-8 (J29-J56) — ACCÉLÉRATION :
- Objectif : pipeline de 5+ prospects qualifiés en permanence
- Premier service récurrent (maintenance mensuelle)
- Revenue cible : 8 000€ cumulés

SEMAINES 9-13 (J57-J90) — MULTIPLICATION :
- Objectif : atteindre 5 000€/mois récurrents
- Premiers partenariats générateurs de revenus
- Revenue cible : 15 000€ cumulés = vélocité 30x

POUR CHAQUE SEMAINE :
- 3 actions concrètes (lundi, mercredi, vendredi)
- 1 métrique à mesurer
- 1 décision à prendre si la cible n'est pas atteinte""",
        "STRATÉGIE 10X — Plan 90 jours Caelum Partners"
    )
    sauvegarder("strategie_10x", r)


def audit_effet_levier():
    r = streamer(
        """Identifie tous les leviers sous-utilisés dans le modèle actuel de Caelum Partners.

AUDIT DES 6 TYPES DE LEVIER :

1. LEVIER FINANCIER :
   - Existe-t-il des financements disponibles (subventions bruxelloises pour startups IA) ?
   - Quelles aides Hub.Brussels, BEI, Région wallonne sont accessibles à Chaima ?
   - Modèle de prépaiement client : acomptes, abonnements annuels prépayés

2. LEVIER TECHNOLOGIQUE :
   - Agents IA actuels : lesquels génèrent le plus de valeur par heure de Chaima ?
   - Automatisations manquantes qui libéreraient 10h/semaine supplémentaires
   - Outil de productivité le plus impactant à adopter cette semaine

3. LEVIER RÉSEAU :
   - Contacts ASBL de Chaima convertibles en clients payants ou en référents
   - Prescripteurs naturels (comptables, avocats, consultants qui conseillent des PME)
   - Partenaires complémentaires non concurrents

4. LEVIER DE MARQUE :
   - Contenu qui génère des leads passifs (articles LinkedIn, cas d'usage, templates gratuits)
   - Positionnement "autorité IA belge" : 1 article viral = 10 clients potentiels

5. LEVIER DE STRUCTURE :
   - Comment structurer Caelum pour que chaque euro travaille pendant que Chaima dort ?
   - Produits numériques (templates, guides, formations) à vendre sans intervention

6. LEVIER TEMPOREL :
   - Quand contacter les prospects (jour de la semaine, heure) pour maximiser les conversions ?
   - Saisonnalité : quels mois les PME belges investissent-elles en IA ?

POUR CHAQUE LEVIER : score d'impact (1-10), coût d'activation (€), délai de résultat (jours).""",
        "AUDIT EFFET DE LEVIER — Leviers sous-utilisés Caelum Partners"
    )
    sauvegarder("audit_effet_levier", r)


def simuler_scenarios_velocite():
    r = streamer(
        """Simule 3 scénarios de vélocité du capital sur 90 jours pour Caelum Partners.

HYPOTHÈSES COMMUNES :
- Capital investi total : 500€ (équivalent temps + outils)
- Services disponibles : Site web 500€ / Automation IA 1 500€ / Pack 3 000€
- Abonnement mensuel possible : 300€/mois (maintenance + support)

═══════════════════════════════════════
SCÉNARIO 1 — CONSERVATEUR (probabilité 90%)
═══════════════════════════════════════
- Mois 1 : 1 site web 500€ + 1 automation 1 500€ = 2 000€
- Mois 2 : 2 automations 1 500€ = 3 000€
- Mois 3 : 1 pack 3 000€ + 1 abonnement 300€ = 3 300€
- Total 90 jours : 8 300€
- Vélocité : 8 300 / 500 = 16.6x ✅

═══════════════════════════════════════
SCÉNARIO 2 — RÉALISTE (probabilité 70%)
═══════════════════════════════════════
- Mois 1 : 2 sites web + 1 automation = 2 500€
- Mois 2 : 2 packs 3 000€ = 6 000€
- Mois 3 : 3 automations + 3 abonnements = 5 400€
- Total 90 jours : 13 900€
- Vélocité : 13 900 / 500 = 27.8x ✅✅

═══════════════════════════════════════
SCÉNARIO 3 — AGRESSIF (probabilité 40%)
═══════════════════════════════════════
- Mois 1 : 5 clients (mix services) = 8 000€
- Mois 2 : 7 clients + premiers abonnements = 12 000€
- Mois 3 : 10 clients + 5 abonnements = 17 500€
- Total 90 jours : 37 500€
- Vélocité : 37 500 / 500 = 75x ✅✅✅

POUR CHAQUE SCÉNARIO :
- Conditions requises pour l'atteindre
- Actions différenciatrices vs scénario inférieur
- Point de bascule (quel événement déclenche ce niveau)
- Comment passer du scénario conservateur au scénario réaliste en 30 jours""",
        "SIMULATION SCÉNARIOS VÉLOCITÉ — 90 jours Caelum Partners"
    )
    sauvegarder("scenarios_velocite", r)


def optimiser_structure_cout():
    r = streamer(
        """Redesigne la structure de coût de Caelum Partners pour maximiser la vélocité du capital.

ANALYSE DE LA STRUCTURE ACTUELLE :
- Coûts fixes : ~0€/mois (quasi aucun)
- Coûts variables : temps de Chaima (~valeur à calculer)
- Coûts cachés : temps de prospection, temps d'administration, temps d'apprentissage IA

STRUCTURE DE COÛT OPTIMALE POUR VÉLOCITÉ MAXIMALE :

1. PRINCIPE ZÉRO COÛT FIXE TANT QUE CA < 5 000€/MOIS :
   - Aucun outil payant non-essentiel
   - Aucun local (télétravail total)
   - Aucun collaborateur (agents IA uniquement)

2. PRINCIPE DU COÛT VARIABLE ALIGNÉ SUR LE REVENU :
   - Chaque outil payant doit générer 5x son coût en revenus
   - Outils admissibles à partir de quel niveau de CA

3. SÉQUENCE D'INVESTISSEMENT OPTIMALE (par palier de CA) :
   - CA 0-5K€/mois → investissements admissibles : liste
   - CA 5-15K€/mois → investissements admissibles : liste
   - CA 15-30K€/mois → investissements admissibles : liste
   - CA > 30K€/mois → investissements admissibles : liste

4. COÛTS À ÉVITER ABSOLUMENT (qui détruisent la vélocité) :
   - Abonnements SaaS non rentabilisés
   - Embauche prématurée avant automatisation maximale
   - Investissements marketing avant product-market fit

5. CALCUL DE LA MARGE NETTE OPTIMALE À CHAQUE PALIER :
   - Objectif : maintenir marge nette > 70% jusqu'à 10K€/mois
   - Comment y parvenir concrètement""",
        "STRUCTURE DE COÛT OPTIMALE — Vélocité maximale Caelum Partners"
    )
    sauvegarder("structure_cout_optimale", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  MAÎTRE VÉLOCITÉ CAPITAL — Caelum Partners")
    print("  Multiplication 10x · 90 jours · Levier maximum")
    print("═"*65)

    while True:
        print("\n  1. Calculer la vélocité actuelle du capital")
        print("  2. Concevoir la stratégie 10x en 90 jours")
        print("  3. Audit des effets de levier sous-utilisés")
        print("  4. Simuler 3 scénarios de vélocité")
        print("  5. Optimiser la structure de coût")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            calculer_velocite_actuelle()
        elif choix == "2":
            concevoir_strategie_10x()
        elif choix == "3":
            audit_effet_levier()
        elif choix == "4":
            simuler_scenarios_velocite()
        elif choix == "5":
            optimiser_structure_cout()
        else:
            print("  Choix invalide.")
