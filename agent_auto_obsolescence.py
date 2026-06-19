"""
STRATÈGE DE L'AUTO-OBSOLESCENCE — Destruction créatrice de Caelum Partners
Usage : python agent_auto_obsolescence.py
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
IDENTITE = """Tu es le Stratège de l'Auto-Obsolescence de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles.
Ta conviction absolue : "Il vaut mieux être celui qui remplace ses propres services que d'être remplacé par un concurrent."
Tu t'inspires de trois théories fondatrices : la destruction créatrice de Schumpeter, la théorie de la disruption de Clayton Christensen, et "Only the paranoid survive" d'Andy Grove (Intel).
Ta mission : imaginer activement comment les services actuels de Caelum deviennent obsolètes, puis concevoir les remplaçants AVANT que les concurrents ne le fassent.
Services actuels à perturber : site web 500€ en 7 jours (que se passe-t-il si l'IA génère des sites en 5 minutes pour 50€ ?), automation IA 1500€ en 14 jours (que se passe-t-il si les plateformes s'automatisent elles-mêmes ?), pack complet 3000€ en 30 jours (que se passe-t-il si les clients apprennent eux-mêmes à prompter l'IA ?).
Signaux d'auto-obsolescence à surveiller : commoditisation (guerre des prix), rupture technologique (nouvelle capacité IA), changement de comportement client (outils DIY), changement réglementaire (IA Act européen).
La commoditisation est le premier signe de la mort : quand n'importe qui peut faire ce que Caelum fait, le prix s'effondre.
La disruption vient souvent par le bas : des solutions moins chères, moins bonnes, mais "assez bonnes" pour les clients les moins exigeants.
Le paradoxe du succès : plus Caelum réussit avec ses services actuels, plus il est difficile de les cannibiliser soi-même.
L'EU AI Act (en vigueur 2024-2026) peut créer des obligations de conformité qui deviennent des barrières à l'entrée — ou des obstacles pour Caelum.
Ta méthode : scénarios de disruption avec probabilités et délais, roadmaps de pivot avec jalons déclencheurs, stress tests du modèle économique.
Tu es impitoyable dans l'analyse : tu ne ménages pas les services actuels, tu les condamnes si les données le justifient.
Tu identifies les signaux faibles actuels (outils IA émergents, mouvements concurrentiels, décisions des grandes plateformes) qui préfigurent l'obsolescence.
Tu conçois le "service suivant" — celui qui rend les offres actuelles inutiles — comme si Caelum était son propre concurrent le plus dangereux.
Tu calibres le timing du pivot : trop tôt = on abandonne un marché rentable, trop tard = on se fait disrupter.
Tu parles en français, tu es stratégique, provocateur dans l'analyse, et tu forces Chaima à regarder en face ce qui pourrait tuer son business."""

def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.25, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/auto_obsolescence", exist_ok=True)
    fichier = f"fichiers/auto_obsolescence/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def simuler_obsolescence_services():
    prompt = """Simule l'obsolescence de chaque service actuel de Caelum Partners. Sois impitoyable : si un service va mourir, dis-le clairement avec les données à l'appui.

SERVICES ACTUELS DE CAELUM :
- Service A : Site web 500€, livré en 7 jours, pour PME belges
- Service B : Automation IA 1500€, livrée en 14 jours, pour PME belges
- Service C : Pack complet 3000€, livré en 30 jours, pour PME belges

Pour chaque service, produis une fiche d'obsolescence complète :

SERVICE A — SITE WEB 500€
1. TECHNOLOGIES DISRUPTIVES ACTUELLES
   - Outils existants aujourd'hui (Wix ADI, Squarespace AI, Framer AI, Durable.co, etc.) : que font-ils, à quel prix ?
   - Dans combien de temps ces outils seront-ils "assez bons" pour 80% des besoins des PME belges ?
   - Prix de rupture : à partir de quel prix un outil DIY rend-il l'offre 500€ de Caelum injustifiable ?

2. SCÉNARIO D'OBSOLESCENCE
   - Délai estimé avant que ce service soit commoditisé : [6 mois / 1 an / 2 ans / 5 ans+]
   - Probabilité d'obsolescence dans ce délai : [%]
   - Quel type de client abandonne Caelum en premier pour aller vers le DIY ?
   - Quel type de client reste avec Caelum même quand l'alternative DIY existe ?

3. SIGNAL D'ALARME À SURVEILLER
   - Indicateur précis qui signale que l'obsolescence est imminente
   - Seuil déclencheur : ex. "quand 3 outils DIY offrent des sites en moins de 10 minutes pour moins de 100€"

SERVICE B — AUTOMATION IA 1500€
[même structure]

SERVICE C — PACK COMPLET 3000€
[même structure]

SYNTHÈSE : TABLEAU D'OBSOLESCENCE
- Classement des 3 services par urgence de remplacement
- Fenêtre d'opportunité restante pour chaque service : combien de temps Caelum peut encore vendre ces offres ?
- Revenu cumulé potentiel pendant la fenêtre d'opportunité (hypothèse 2-5 clients/mois)
- Recommandation : commencer à développer le remplacement maintenant ou dans combien de mois ?

Format : analytique, chiffré, avec probabilités. Langue : français."""

    resultat = streamer(prompt, "SIMULATION — Obsolescence des services Caelum")
    sauvegarder("simulation_obsolescence", resultat)

def concevoir_service_suivant():
    prompt = """Conçois le service de nouvelle génération qui rend les offres actuelles de Caelum Partners obsolètes — comme si Caelum était son propre concurrent le plus redoutable.

Contexte : Caelum Partners, agence IA bruxelloise, services actuels 500€/1500€/3000€ approchant de la commoditisation progressive.
Capacités existantes : 50+ agents IA Gemini, expertise RGPD belge, bilinguisme FR/NL, automatisation de processus.

Conçois le "Service Suivant" en 5 composantes :

1. VISION DU SERVICE DE NOUVELLE GÉNÉRATION
   - Nom de code interne
   - Ce que ce service fait que les services actuels ne peuvent pas faire
   - Pourquoi ce service rend les offres 500€/1500€/3000€ comparativement obsolètes
   - La technologie clé qui le rend possible (agents autonomes, LLM multimodaux, orchestration complexe, etc.)

2. ARCHITECTURE DU SERVICE
   - Que reçoit le client ? (livrables concrets)
   - Comment est-il produit ? (processus interne, rôle de l'IA vs rôle de Chaima)
   - Délai de livraison vs services actuels
   - Niveau d'autonomie du service : est-il 80%+ automatisé ?

3. MODÈLE ÉCONOMIQUE DU SERVICE SUIVANT
   - Tarification : est-ce une offre plus chère (montée en gamme) ou moins chère mais scalable ?
   - Modèle de revenus : projet unique / abonnement / revenu variable / licence ?
   - Potentiel de scale : combien de clients simultanés Caelum peut-elle servir sans recruter ?
   - Marge estimée vs services actuels

4. TRANSITION DU MARCHÉ ACTUEL VERS LE SERVICE SUIVANT
   - Comment proposer le service suivant aux clients actuels des offres 500€/1500€/3000€ ?
   - Script de transition : comment présenter la nouvelle offre sans invalider l'ancienne (pour les clients en cours)
   - Plan de migration : clients actuels → nouveau service en combien de temps

5. ROADMAP DE DÉVELOPPEMENT DU SERVICE SUIVANT
   - 15 étapes numérotées pour passer de l'idée au premier client du nouveau service
   - Délai total réaliste depuis aujourd'hui
   - Ce que Chaima doit apprendre ou développer en priorité
   - Jalons intermédiaires : MVP en 30 jours, première version en 90 jours, version complète en 180 jours

Format : plan de développement concret, visionnaire mais faisable. Langue : français."""

    resultat = streamer(prompt, "INNOVATION — Conception du service de nouvelle génération")
    sauvegarder("service_nouvelle_generation", resultat)

def analyser_signaux_disruption():
    prompt = """Scanne l'environnement technologique et réglementaire actuel pour identifier tous les signaux de disruption qui menacent ou transforment les services de Caelum Partners.

Services à risque : site web 500€, automation IA 1500€, pack complet 3000€ pour PME belges.

Analyse en 5 catégories de signaux :

1. NOUVEAUX OUTILS IA QUI COMMODITISENT LES SERVICES ACTUELS
   - Outils de création de sites web par IA : liste des 5 plus avancés en 2024-2025, leurs capacités, leurs prix
   - Outils d'automatisation no-code/low-code : Make, Zapier, n8n + nouvelles solutions IA — que permettent-ils sans expert ?
   - Agents IA autonomes : AutoGPT, AgentGPT, Devin, Cursor — impactent-ils l'offre "développement sur mesure" ?
   - Délai estimé avant que ces outils atteignent un niveau "assez bon" pour les PME belges sans accompagnement

2. MOUVEMENTS DES CONCURRENTS ÉTABLIS
   - Les grandes agences web belges (Dotcom, Starring Jane, etc.) : ont-elles commencé à intégrer l'IA dans leurs offres ?
   - Les freelances IA belges : y en a-t-il davantage, à quels prix, avec quelles offres ?
   - Les plateformes globales (Fiverr, Malt, Upwork) : comment la concurrence internationale presse-t-elle les prix belges ?

3. EU AI ACT — IMPLICATIONS POUR CAELUM
   - Quelles obligations de l'EU AI Act s'appliquent aux services de Caelum Partners ?
   - Systèmes à haut risque : les agents IA de Caelum tombent-ils dans cette catégorie ?
   - Obligations de transparence : que doit Caelum déclarer à ses clients sur l'utilisation de l'IA ?
   - Délai de mise en conformité et coût estimé pour une agence de la taille de Caelum
   - L'EU AI Act comme barrière à l'entrée pour les concurrents moins conformes : opportunité ou contrainte ?

4. CHANGEMENTS DE COMPORTEMENT DES CLIENTS PME BELGES
   - Les PME belges apprennent-elles à utiliser l'IA elles-mêmes (ChatGPT, Copilot, Gemini) ?
   - Quelles tâches que Caelum réalise actuellement les PME commencent-elles à faire en interne ?
   - Effet sur la demande : le marché des agences IA va-t-il croître ou se contracter à 2-3 ans ?

5. SIGNAUX FAIBLES À SURVEILLER — SYSTÈME D'ALERTE PRÉCOCE
   - 10 indicateurs précis à surveiller chaque mois (sources spécifiques, métriques, seuils d'alerte)
   - Comment organiser une veille de 30 minutes par semaine sur ces signaux
   - Tableau de bord de disruption : format simple pour tracker les signaux dans le temps

Format : factuel, chiffré, sources citées quand possible, orienté décision. Langue : français."""

    resultat = streamer(prompt, "SIGNAUX — Détection des vecteurs de disruption")
    sauvegarder("signaux_disruption", resultat)

def roadmap_pivot_proactif():
    prompt = """Conçois la roadmap de pivot proactif pour Caelum Partners : quand et comment basculer vers les services de nouvelle génération AVANT d'être forcé de le faire par le marché.

Contexte : Caelum Partners en phase de lancement (0 clients), services 500€/1500€/3000€, fondatrice Chaima seule, bootstrappée à Bruxelles.

Produis une roadmap de pivot en 5 sections :

1. MATRICE DES DÉCLENCHEURS DE PIVOT
   Pour chaque service actuel, définir 3 types de déclencheurs :

   SERVICE SITE WEB 500€ :
   - Déclencheur technologique : quel outil IA doit atteindre quelle capacité pour que ce service soit menacé ?
   - Déclencheur marché : quel signal de prix ou de volume indique une commoditisation ?
   - Déclencheur interne : quel niveau de revenus ou nombre de clients avant de pouvoir pivoter sereinement ?

   SERVICE AUTOMATION 1500€ :
   [même structure]

   SERVICE PACK COMPLET 3000€ :
   [même structure]

2. FENÊTRES DE PIVOT OPTIMALES
   - Trop tôt : pourquoi pivoter trop tôt est dangereux (abandon d'un marché encore rentable)
   - Trop tard : pourquoi attendre trop longtemps est fatal (perte de marché avant d'avoir le remplaçant)
   - La zone optimale : quand les revenus du service actuel couvrent encore les coûts de développement du suivant
   - Indicateur de la zone optimale pour Caelum (chiffre concret)

3. PLAN DE PIVOT EN 3 PHASES
   PHASE 1 — PRÉPARATION (sans rien changer au marché) :
   - Développer le service suivant en parallèle des services actuels
   - Budget temps : X heures/semaine sur le développement du nouveau service
   - Financement du développement : les revenus actuels financent l'innovation suivante

   PHASE 2 — TRANSITION (double offre) :
   - Proposer l'ancienne ET la nouvelle offre simultanément
   - Segmentation : ancienne offre pour qui ? Nouvelle offre pour qui ?
   - Durée de la transition : combien de mois maintenir les deux en parallèle ?

   PHASE 3 — BASCULE COMPLÈTE :
   - Arrêt progressif de l'ancienne offre : comment annoncer aux clients existants ?
   - Focus total sur le nouveau service
   - Reconfiguration du site web, des propositions commerciales, du discours commercial

4. GESTION DU RISQUE PENDANT LE PIVOT
   - Risque financier : comment maintenir les revenus pendant la transition ?
   - Risque de réputation : comment pivoter sans paraître instable aux yeux des clients ?
   - Risque opérationnel : comment gérer deux services simultanément en solo ?
   - Plan B : si le nouveau service ne décolle pas, peut-on revenir à l'ancien ?

5. CALENDRIER DE DÉCISION — 24 MOIS
   - Mois 1-6 : consolider le marché actuel ET surveiller les signaux
   - Mois 7-12 : lancer le développement du service suivant si les déclencheurs sont atteints
   - Mois 13-18 : phase de transition double offre
   - Mois 19-24 : bascule complète vers le service de nouvelle génération
   - Points de décision GO/NO-GO explicites à chaque jalon

Format : roadmap décisionnelle avec jalons quantifiés. Langue : français."""

    resultat = streamer(prompt, "PIVOT — Roadmap proactive de transformation")
    sauvegarder("roadmap_pivot", resultat)

def tester_resilience_modele():
    prompt = """Soumets le modèle économique de Caelum Partners à un stress test complet contre 5 scénarios de disruption sur 5 ans.

Modèle actuel : agence IA bruxelloise, services 500€/1500€/3000€, solo-fondatrice Chaima Mhadbi, bootstrappée, 0 clients au démarrage.

Pour chaque scénario, évalue : probabilité, impact sur les revenus, délai de survenue, capacité de survie de Caelum, stratégie de réponse.

SCÉNARIO 1 — "LE TSUNAMI IA DIY" (Probabilité : 70%)
Hypothèse : D'ici 18 mois, des plateformes comme Wix, Shopify et Make proposent des offres IA complètes (site + automation + agents) pour 99€/mois. 80% des PME belges migrent vers ces solutions.
- Impact sur les revenus de Caelum : réduction estimée de [X]% du marché adressable
- Quels clients restent avec Caelum ? Pourquoi ?
- Comment Caelum survit-elle ? Quelle repositionnement dans les 6 mois ?
- Revenu de survie minimal : à combien de clients par mois Caelum doit-elle descendre pour rester viable ?

SCÉNARIO 2 — "L'EU AI ACT PARALYSE" (Probabilité : 40%)
Hypothèse : L'EU AI Act impose des obligations de conformité coûteuses (audit, certification, documentation) que Caelum ne peut pas absorber en solo. Les clients craignent les risques légaux des agents IA.
- Quelles obligations concrètes s'appliquent aux agents IA de Caelum ?
- Coût de mise en conformité estimé (temps + argent)
- Impact sur le délai de livraison et le prix des services
- Comment transformer la conformité en avantage concurrentiel face aux agences non conformes ?

SCÉNARIO 3 — "UN GRAND CABINET DE CONSEIL ENTRE SUR LE MARCHÉ PME" (Probabilité : 30%)
Hypothèse : Accenture, Deloitte ou une SSII belge lance une offre IA "PME accessible" à 800€/mois, avec la crédibilité d'une grande marque. Effet de marque écrasant sur Caelum.
- Pourquoi les grands cabinets sont structurellement désavantagés face aux PME (coûts fixes, processus lourds)
- Segment de clients que les grands ne peuvent pas servir et que Caelum peut garder
- Différenciation de survie : qu'est-ce que Caelum fait que les grands ne peuvent pas répliquer ?

SCÉNARIO 4 — "L'HYPERINFLATION IA — LE COÛT DES API EXPLOSE" (Probabilité : 25%)
Hypothèse : Google/OpenAI triplent leurs prix d'API en 2026. Le coût de production des agents Caelum explose, détruisant les marges.
- Impact sur la marge par service (500€/1500€/3000€) si le coût API triple
- Seuil de rentabilité : à partir de quand les services deviennent-ils déficitaires ?
- Options de réponse : hausser les prix, optimiser les prompts, changer de modèle IA, licences alternatives

SCÉNARIO 5 — "LE CLIENT CAELUM DEVIENT CONCURRENT" (Probabilité : 50%)
Hypothèse : Après un projet Caelum, un client PME embauche un profil IA interne et commence à offrir les mêmes services à ses propres clients. Caelum a formé son propre concurrent.
- Comment protéger la propriété intellectuelle des agents développés pour les clients ?
- Clauses contractuelles à inclure (non-concurrence, propriété des agents, conditions d'utilisation)
- Ce scénario peut-il être transformé en opportunité (programme partenaires, licences) ?

VERDICT FINAL — SCORE DE RÉSILIENCE DU MODÈLE /100
- Synthèse des 5 scénarios : le modèle actuel est-il structurellement résilient ?
- Les 3 changements structurels prioritaires pour rendre le modèle plus robuste
- Le modèle économique recommandé pour 2026 : en quoi diffère-t-il du modèle actuel ?

Format : stress test rigoureux, probabilités et impacts chiffrés. Langue : français."""

    resultat = streamer(prompt, "STRESS TEST — Résilience du modèle Caelum Partners")
    sauvegarder("stress_test_resilience", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  STRATÈGE DE L'AUTO-OBSOLESCENCE — Destruction créatrice")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Simuler l'obsolescence des services actuels")
        print("  2. Concevoir le service de nouvelle génération")
        print("  3. Analyser les signaux de disruption")
        print("  4. Roadmap de pivot proactif")
        print("  5. Tester la résilience du modèle")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            simuler_obsolescence_services()
        elif choix == "2":
            concevoir_service_suivant()
        elif choix == "3":
            analyser_signaux_disruption()
        elif choix == "4":
            roadmap_pivot_proactif()
        elif choix == "5":
            tester_resilience_modele()
        else:
            print("  Choix invalide.")
