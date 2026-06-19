"""
ARCHITECTE DE TALENTS [55] — Préparateur de ressources pour saisir les opportunités validées
Usage : python agent_architecte_talents.py
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

IDENTITE = """
Tu es l'ARCHITECTE DE TALENTS de Caelum Partners, cabinet IA bruxellois fondé par Chaima Mhadbi.
Ta mission : préparer les bonnes ressources (agents IA, processus, compétences, partenariats)
pour attaquer les opportunités validées par le CAPTEUR DE SIGNAUX FAIBLES.

À la phase actuelle de Caelum, "talents" = combinaison de :
- Compétences de Chaima Mhadbi (expertise IA, vente, conseil, gestion de projet)
- 50 agents IA spécialisés (automatisation, analyse, génération de contenu, etc.)
- Réseau de partenaires/sous-traitants potentiels (développeurs, consultants sectoriels)
- Outils et plateformes (Google Cloud, APIs, outils no-code/low-code)

Frameworks maîtrisés :
1. Inventaire de compétences (Skills Matrix) : cartographie précise du capital disponible
2. Gap Analysis : identifier l'écart entre capacités actuelles et capacités requises
3. Décision Build-Buy-Partner :
   - Build : développer en interne (nouvel agent IA, nouvelle compétence Chaima)
   - Buy : acheter ou abonner (outil SaaS, formation courte)
   - Partner : sous-traiter ou s'allier (expert sectoriel, développeur spécialisé)
4. Matrice RACI pour missions multi-parties (Responsible, Accountable, Consulted, Informed)

Contraintes critiques :
- RGPD obligatoire : les données partagées avec sous-traitants doivent être minimisées
- Conformité EU AI Act pour les systèmes IA déployés chez les clients
- Budget limité en phase lancement : privilégier Build (agents) et Partner (expertise)
- Chaima est la ressource scarcest : ses heures ne doivent toucher que la haute valeur

Tu prépares les ressources AVANT que la FORCE DE VENTE attaque le marché.
Chaque plan de ressources est conçu pour maximiser la vélocité d'acquisition client.
"""


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
    os.makedirs("fichiers/architecte_talents", exist_ok=True)
    fichier = f"fichiers/architecte_talents/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def inventaire_competences_actuelles() -> str:
    """Cartographier toutes les capacités actuelles de Caelum : Chaima + 50 agents + outils."""
    prompt = """
MISSION : Dresser l'inventaire complet des compétences et ressources actuelles de Caelum Partners.
Cet inventaire est le point de départ de toute décision Build-Buy-Partner.

CARTOGRAPHIE EN 4 COUCHES :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COUCHE 1 : CHAIMA MHADBI — COMPÉTENCES HUMAINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cartographie par domaine :
A. Compétences IA & Tech
   - Maîtrise des LLMs et APIs IA (Google Gemini, OpenAI, etc.)
   - Prompt engineering et orchestration d'agents
   - Automatisation no-code/low-code
   - Niveau estimé : Expert / Intermédiaire / Débutant

B. Compétences Business
   - Stratégie commerciale et vente B2B
   - Gestion de projet et livraison client
   - Communication et présentation
   - Gestion financière et comptabilité

C. Compétences Sectorielles
   - Secteurs PME belges connus en profondeur
   - Réseaux professionnels activables immédiatement
   - Langues : français, néerlandais, anglais, arabe ?

D. Compétences à Haute Valeur vs Tâches Déléguables :
   | Compétence | Niveau | Déléguable aux agents ? | Valeur marché (€/h) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COUCHE 2 : LES 50 AGENTS IA — CAPACITÉS DÉPLOYÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Inventaire par catégorie fonctionnelle :
1. Agents de prospection et vente (combien ? capacités ?)
2. Agents de production de contenu (rédaction, présentation, rapports)
3. Agents d'analyse et recherche (marché, concurrents, données)
4. Agents de livraison client (automatisation processus, formation IA)
5. Agents de gestion interne (admin, finance, suivi)
6. Agents spécialisés sectoriels (si existants)

Pour chaque catégorie : nombre d'agents + capacités clés + limites actuelles

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COUCHE 3 : OUTILS ET PLATEFORMES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- APIs IA disponibles et coût mensuel estimé
- Outils CRM, projet, communication
- Infrastructure technique (cloud, hébergement)
- Outils de livraison client

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COUCHE 4 : RÉSEAU ET PARTENARIATS POTENTIELS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Partenaires potentiels identifiés (type, valeur ajoutée)
- Sous-traitants qualifiables rapidement
- Réseau Caelum ASBL activable

BILAN STRATÉGIQUE :
1. Top 5 forces actuelles de Caelum (avantages concurrentiels réels)
2. Top 5 gaps critiques (ce qui manque pour attaquer les premières opportunités)
3. Capacité de livraison actuelle : combien de missions simultanées maximum ?
4. Recommandation : quoi développer en priorité (Build) vs acheter (Buy) vs sous-traiter (Partner) ?
"""
    resultat = streamer(prompt, "INVENTAIRE COMPÉTENCES ACTUELLES — ARCHITECTE DE TALENTS")
    sauvegarder("inventaire_competences", resultat)
    return resultat


def analyse_gap_opportunite(opportunite: str = "") -> str:
    """Pour une opportunité validée, identifier les gaps de compétences et comment les combler."""
    if not opportunite:
        print("\n🎯 Décris l'opportunité validée à analyser :")
        opportunite = input("  > ").strip()[:2000]
    if not opportunite:
        opportunite = "Opportunité non spécifiée"

    prompt = f"""
MISSION : Analyser le gap de ressources pour saisir cette opportunité validée pour Caelum Partners.

OPPORTUNITÉ À ANALYSER :
{opportunite}

ANALYSE DE GAP EN 5 ÉTAPES :

1. DÉCOMPOSITION DE L'OPPORTUNITÉ :
   - Segment PME cible précis
   - Problème client résolu
   - Offre Caelum appropriée (500€ / 1500€ / 3000€) et justification
   - Délai de livraison attendu par le client
   - Livrables concrets attendus

2. RESSOURCES REQUISES POUR SAISIR L'OPPORTUNITÉ :
   a) Compétences humaines nécessaires (côté Chaima)
   b) Types d'agents IA nécessaires
   c) Outils spécifiques requis
   d) Expertise sectorielle nécessaire
   e) Temps total de livraison estimé

3. ANALYSE DES GAPS (Requis vs Disponible) :
   | Ressource requise | Disponible chez Caelum ? | Gap | Criticité (1-5) |

4. PLAN DE COMBLEMENT DES GAPS — DÉCISION BUILD-BUY-PARTNER :

   Pour chaque gap critique :

   🔨 BUILD (développer en interne) :
   - Quel agent IA créer ou adapter ?
   - Quelle compétence Chaima développer ?
   - Délai de mise en place : X jours
   - Coût : X heures Chaima

   💳 BUY (acheter ou s'abonner) :
   - Quel outil ou service acheter ?
   - Coût mensuel / ponctuel
   - Délai d'opérationnalité

   🤝 PARTNER (sous-traiter ou s'allier) :
   - Quel profil de partenaire/sous-traitant ?
   - Données à partager (minimisation RGPD)
   - Contrat type recommandé
   - Coût et marge Caelum

5. PLAN D'ACTION POUR ÊTRE PRÊT EN X JOURS :
   - J+0 à J+7 : actions immédiates
   - J+8 à J+14 : mise en place ressources
   - J+15 : capacité de livraison confirmée → signal à la FORCE DE VENTE

   Feu vert pour la FORCE DE VENTE : OUI à partir du [date] / NON car [blocage]
"""
    resultat = streamer(prompt, f"ANALYSE GAP OPPORTUNITÉ — ARCHITECTE DE TALENTS")
    sauvegarder("analyse_gap", resultat)
    return resultat


def recommander_sous_traitants() -> str:
    """Identifier quelles capacités construire, acheter ou sous-traiter pour le marché belge."""
    prompt = """
MISSION : Recommander la stratégie Build-Buy-Partner optimale pour Caelum Partners
sur le marché belge des PME IA, en phase de lancement.

CONTEXTE : Caelum Partners, 0 clients, phase lancement. Chaima seule + 50 agents IA.
Services 500€/1500€/3000€. Marché : PME belges, adoption IA < 15%.

ANALYSE BUILD-BUY-PARTNER PAR DOMAINE :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAINE 1 : EXPERTISE SECTORIELLE PME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Top 5 secteurs PME belges à fort potentiel IA
- Pour chaque secteur : Build / Buy / Partner ? Pourquoi ?
- Profil de sous-traitant idéal par secteur (si Partner)
- Conditions RGPD à respecter pour partage données clients

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAINE 2 : CAPACITÉS TECHNIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Développement d'agents IA customisés → Build ou Partner ?
- Intégrations systèmes client (ERP, CRM) → Build ou Buy ?
- Infrastructure cloud et sécurité → Buy ou Partner ?
- Recommandation par cas d'usage avec budget estimé

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAINE 3 : SUPPORT COMMERCIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Prospection et qualification → agents IA (Build) ?
- Présentation et closing → Chaima seule ou Partner ?
- Support après-vente → agents IA ou sous-traitant ?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAINE 4 : ADMINISTRATION ET LÉGAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Comptabilité, juridique, RGPD → Partner impératif
- Profils recommandés à Bruxelles (type, tarif estimé)
- Clauses contractuelles clés pour protéger Caelum

TABLEAU DE DÉCISION GLOBAL :
| Domaine | Capacité | Build/Buy/Partner | Coût estimé | Délai | Priorité |

TOP 5 PARTENARIATS À INITIER EN PRIORITÉ :
Pour chaque partenariat : profil exact, comment les trouver à Bruxelles, pitch d'approche

RÈGLES RGPD POUR LES PARTENARIATS :
- Données minimales à partager
- Clauses DPA (Data Processing Agreement) essentielles
- Check-list de conformité avant de partager des données client
"""
    resultat = streamer(prompt, "RECOMMANDATIONS SOUS-TRAITANTS — ARCHITECTE DE TALENTS")
    sauvegarder("recommandations_sous_traitants", resultat)
    return resultat


def plan_montee_en_competence() -> str:
    """Plan de développement des compétences de Chaima sur 90 jours basé sur les opportunités validées."""
    prompt = """
MISSION : Concevoir le plan de montée en compétence 90 jours pour Chaima Mhadbi,
fondé sur les opportunités validées pour Caelum Partners.

PROFIL APPRENANTE :
- Chaima Mhadbi, fondatrice Caelum Partners, Brussels
- Experte IA et automatisation, en phase de développement business
- Contrainte : temps limité (entreprise à lancer, missions à livrer)
- Objectif : first 3 clients signés dans les 90 jours

PLAN 90 JOURS EN 3 SPRINTS :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPRINT 1 (J+1 à J+30) : FONDATIONS COMMERCIALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif sprint : signer le premier client

Compétences prioritaires à développer :
1. Compétence : [Nom] | Pourquoi maintenant | Format d'apprentissage | Durée | Ressource recommandée
2. (répéter pour 3-4 compétences max)

Indicateur de réussite du sprint : [KPI précis]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPRINT 2 (J+31 à J+60) : EXCELLENCE DE LIVRAISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif sprint : livrer le premier client avec excellence + signer le 2ème

Compétences prioritaires :
(3-4 compétences, même format)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPRINT 3 (J+61 à J+90) : SCALABILITÉ ET LEADERSHIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif sprint : 3 clients actifs, machine commerciale autonome

Compétences prioritaires :
(3-4 compétences, même format)

RÈGLES DU PLAN :
1. Maximum 5h/semaine d'apprentissage formel (le reste = apprentissage par l'action)
2. Chaque compétence apprise doit être appliquée dans les 48h (learning by doing)
3. Priorité aux compétences qui génèrent du CA dans les 30 prochains jours
4. Jamais apprendre ce qu'un agent IA peut faire à la place

MÉTRIQUES DE SUCCÈS :
- J+30 : [KPI spécifique]
- J+60 : [KPI spécifique]
- J+90 : [KPI spécifique]

SIGNAL À LA FORCE DE VENTE :
À partir de quel jour Chaima est-elle prête à attaquer chaque segment d'opportunité ?
"""
    resultat = streamer(prompt, "PLAN MONTÉE EN COMPÉTENCE 90 JOURS — ARCHITECTE DE TALENTS")
    sauvegarder("plan_montee_competence_90j", resultat)
    return resultat


def menu():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║        ARCHITECTE DE TALENTS [55] — Caelum Partners             ║
║         Préparateur de ressources pour les opportunités          ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Inventaire compétences actuelles                             ║
║  2. Analyse gap pour une opportunité                             ║
║  3. Recommander sous-traitants                                   ║
║  4. Plan montée en compétence 90 jours                          ║
║  0. Quitter                                                      ║
╚══════════════════════════════════════════════════════════════════╝
""")
    choix = input("  Votre choix : ").strip()
    return choix


if __name__ == "__main__":
    while True:
        choix = menu()
        if choix == "1":
            inventaire_competences_actuelles()
        elif choix == "2":
            analyse_gap_opportunite()
        elif choix == "3":
            recommander_sous_traitants()
        elif choix == "4":
            plan_montee_en_competence()
        elif choix == "0":
            print("\n  Au revoir. Les ressources sont prêtes quand vous l'êtes.\n")
            break
        else:
            print("\n  [Choix invalide]\n")
