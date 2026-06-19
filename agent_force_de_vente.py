"""
FORCE DE VENTE [56] — Attaque chirurgicale du marché avec les ressources préparées
Usage : python agent_force_de_vente.py
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
Tu es la FORCE DE VENTE d'élite de Caelum Partners, cabinet IA bruxellois fondé par Chaima Mhadbi.
Ta mission : attaquer le marché avec une précision chirurgicale en utilisant les opportunités
validées par le CAPTEUR DE SIGNAUX FAIBLES et les ressources préparées par l'ARCHITECTE DE TALENTS.
Zéro effort de vente gaspillé. Chaque contact est une frappe calculée.

Frameworks maîtrisés :
1. MEDDIC — qualification rigoureuse avant tout investissement temps :
   - Metrics : quels indicateurs le prospect cherche à améliorer ?
   - Economic Buyer : qui signe réellement le chèque ?
   - Decision Criteria : sur quels critères le prospect va décider ?
   - Decision Process : quelles étapes pour aller à la signature ?
   - Identify Pain : quelle douleur est assez forte pour justifier l'achat maintenant ?
   - Champion : qui à l'intérieur pousse pour notre solution ?

2. Value-Based Selling : vendre le ROI et la transformation, jamais les features.
   Formule Caelum : "Votre problème [X] vous coûte [Y€/mois]. Notre solution à [Z€] vous le
   récupère en [N semaines]. ROI = [ratio]."

3. Spécificités B2B belge :
   - Cycles de décision PME : 2-6 semaines (pas 6 mois comme les grandes entreprises)
   - Combo optimal : LinkedIn (chaleur) + email (détail) + téléphone (closing)
   - Marché bilingue : pitch FR pour Bruxelles/Wallonie, NL pour Flandre
   - Bruxellois : pragmatiques, méfiants des discours, veulent voir des cas concrets
   - Culture : construire la confiance avant de vendre, referrals puissants

Métriques de performance suivies :
- Taux de conversion par canal (LinkedIn / email / phone / réseau)
- Taille moyenne des deals (cible : progression vers 3000€)
- Durée du cycle de vente (cible : < 4 semaines)
- Taux de closing sur propositions envoyées (cible : > 30%)

Tu travailles uniquement sur des opportunités validées. Tu ne prospectes jamais au hasard.
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
    os.makedirs("fichiers/force_de_vente", exist_ok=True)
    fichier = f"fichiers/force_de_vente/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def preparer_offensive_marche(segment: str = "") -> str:
    """Concevoir une offensive commerciale complète pour un segment/opportunité validé."""
    if not segment:
        print("\n🎯 Décris le segment ou l'opportunité validée à attaquer :")
        segment = input("  > ").strip()[:2000]
    if not segment:
        segment = "Segment non spécifié"

    prompt = f"""
MISSION : Concevoir une offensive commerciale complète pour attaquer ce segment pour Caelum Partners.

SEGMENT / OPPORTUNITÉ VALIDÉE :
{segment}

PLAN D'OFFENSIVE EN 6 PARTIES :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTIE 1 : INTELLIGENCE DU SEGMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Profil précis de la cible (taille entreprise, secteur, région, rôle du décideur)
- Douleurs principales qualifiées MEDDIC (Identify Pain)
- Arguments ROI chiffrés : "Votre problème vous coûte X€, notre solution Y€ récupère Z en N semaines"
- Offre Caelum recommandée (500€ / 1500€ / 3000€) avec justification
- Objections prévisibles et réponses prêtes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTIE 2 : LISTE DE CIBLES PRIORITAIRES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Critères de qualification ICP (Ideal Customer Profile) pour ce segment
- Requête LinkedIn Sales Navigator recommandée (mots-clés, filtres, géo Belgique)
- Nombre de cibles estimé dans le bassin
- Top 5 entreprises cibles nominatives si identifiables
- Titre exact du décideur à cibler (Economic Buyer MEDDIC)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTIE 3 : MESSAGES PAR CANAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A. Message LinkedIn (invitation + note) — MAX 300 caractères :
   [Texte complet prêt à copier-coller]

B. Email cold outreach — Objet + Corps :
   Objet : [Objet accrocheur < 50 caractères]
   Corps : [Email complet, 150-200 mots, pain → solution → CTA]

C. Message de relance J+3 (si pas de réponse) :
   [Texte court, angle différent]

D. Message de relance J+7 (dernier contact) :
   [Texte court, créer l'urgence sans pression]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTIE 4 : TIMELINE DE L'OFFENSIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Semaine 1 : [actions précises, volume, canaux]
Semaine 2 : [relances, premiers RDV, démos]
Semaine 3 : [propositions commerciales, négociations]
Semaine 4 : [closing, signatures, onboarding]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTIE 5 : KPIs DE L'OFFENSIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Objectif : X contacts → Y réponses → Z RDV → N propositions → M signatures
- Taux de conversion cible par étape
- CA cible de cette offensive (€)
- Délai pour premier deal signé

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTIE 6 : RESSOURCES NÉCESSAIRES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Temps Chaima requis par semaine
- Agents IA à mobiliser pour support
- Outils à activer
- Signal à l'OPTIMISEUR si deal signé : [format du rapport]
"""
    resultat = streamer(prompt, f"OFFENSIVE MARCHÉ — FORCE DE VENTE")
    sauvegarder("offensive_marche", resultat)
    return resultat


def creer_script_closing() -> str:
    """Générer un script de closing pour un type de prospect avec gestionnaires d'objections."""
    print("\n💼 Décris le prospect (secteur, taille, douleur principale, offre visée 500/1500/3000€) :")
    description_prospect = input("  > ").strip()[:2000]
    if not description_prospect:
        description_prospect = "Prospect PME belge non spécifié"

    prompt = f"""
MISSION : Créer un script de closing complet pour Chaima Mhadbi (Caelum Partners)
face à ce profil de prospect PME belge.

PROFIL PROSPECT :
{description_prospect}

SCRIPT DE CLOSING EN 5 ACTES :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTE 1 : OUVERTURE ET ANCRAGE (2-3 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif : créer la confiance et confirmer la douleur.

Script Chaima :
"[Texte exact, naturel, adapté à la culture B2B belge]"

Question d'ancrage de la douleur :
"[Question ouverte qui fait articuler le problème]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTE 2 : QUALIFICATION MEDDIC (5-8 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Questions MEDDIC à poser dans l'ordre naturel :

Metrics : "[Question pour chiffrer la douleur]"
Economic Buyer : "[Question pour identifier le vrai décideur]"
Decision Criteria : "[Question pour connaître les critères de choix]"
Decision Process : "[Question pour cartographier le processus de décision]"
Pain : "[Question pour amplifier la douleur perçue]"
Champion : "[Question pour identifier un allié interne]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTE 3 : PRÉSENTATION DE L'OFFRE (3-5 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Script de présentation ROI :
"Votre problème [X] vous coûte actuellement [Y€/mois]..."
"Notre solution [offre] à [prix€] vous permet de..."
"En [délai], vous récupérez votre investissement car..."
"ROI estimé : [calcul précis avec les chiffres du prospect]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTE 4 : GESTIONNAIRE D'OBJECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top 5 objections + réponses exactes :

Objection 1 : "C'est trop cher."
Réponse : "[Texte exact de la réponse ROI]"

Objection 2 : "On n'a pas le temps de mettre ça en place."
Réponse : "[Texte exact]"

Objection 3 : "On veut d'abord voir si ça marche ailleurs."
Réponse : "[Texte exact avec social proof]"

Objection 4 : "On a déjà une solution interne."
Réponse : "[Texte exact]"

Objection 5 : "Je dois en parler à [quelqu'un d'autre]."
Réponse : "[Texte exact + qualification Champion]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTE 5 : CLOSING (1-2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3 techniques de closing adaptées à la culture belge :

Closing 1 (assumptif) : "[Texte]"
Closing 2 (alternative) : "[Texte]"
Closing 3 (urgence légitime) : "[Texte]"

Phrase finale de confirmation :
"[Texte pour solidifier la décision et préparer onboarding]"

NOTES CULTURELLES BELGIQUE :
- Ce qu'il faut JAMAIS dire face à un Belge francophone
- Ce qui accélère la décision dans ce contexte précis
"""
    resultat = streamer(prompt, "SCRIPT DE CLOSING — FORCE DE VENTE")
    sauvegarder("script_closing", resultat)
    return resultat


def scorer_pipeline_actuel() -> str:
    """Charger les données CRM et scorer le pipeline complet pour prioriser les actions."""
    print("\n📊 Décris ton pipeline actuel (prospects, stade, dernière interaction) :")
    print("   Format : 'Entreprise X — Stade : [RDV/Proposition/Négociation] — Dernière action : [date+action]'")
    print("   (Entrée deux fois pour terminer)\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "" and lignes and lignes[-1] == "":
            break
        lignes.append(ligne)
    pipeline = "\n".join(lignes[:-1]) if lignes else "Pipeline non renseigné."
    pipeline = pipeline[:3000]

    prompt = f"""
MISSION : Scorer et prioriser le pipeline commercial de Caelum Partners pour maximiser
le CA de la semaine et identifier les deals à fermer NOW.

PIPELINE ACTUEL :
{pipeline}

SCORING ET PRIORISATION EN 4 CADRANS :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CADRAN 1 : FERMER MAINTENANT (Priorité absolue)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Critères : deal qualifié MEDDIC + proposition envoyée + Champion identifié
Pour chaque deal :
- Score de closing (0-100) + justification
- Action précise à faire dans les 24h
- Message de closing recommandé (texte exact)
- Probabilité de signature cette semaine (%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CADRAN 2 : ACCÉLÉRER (Potentiel à débloquer)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Critères : deal chaud mais bloqué sur un obstacle identifiable
Pour chaque deal :
- Obstacle précis (technique/décisionnel/budgétaire/timing)
- Action pour débloquer (avec texte exact si message)
- Horizon de closing si débloqué : X semaines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CADRAN 3 : NOURRIR (Long terme ou pas encore qualifié)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Critères : intérêt confirmé mais timing ou qualification insuffisants
Pour chaque deal :
- Fréquence de nurturing recommandée
- Type de contenu/contact à maintenir
- Déclencheur pour passer en Cadran 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CADRAN 4 : ÉLIMINER (Gaspillage de temps commercial)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Critères : pas de douleur qualifiée / pas de budget / pas de décideur / zombie
Pour chaque deal :
- Raison d'élimination (1 ligne)
- Message de clôture élégant (texte exact)

BILAN PIPELINE :
- CA total en jeu (€)
- CA probabilisé cette semaine / ce mois
- Taux de qualification MEDDIC global
- Top 1 action pour maximiser le CA de la semaine
"""
    resultat = streamer(prompt, "SCORING PIPELINE — FORCE DE VENTE")
    sauvegarder("scoring_pipeline", resultat)
    return resultat


def rapport_victoires_semaine() -> str:
    """Rapport hebdomadaire des victoires, avancement pipeline, leçons et plan d'attaque suivant."""
    print("\n🏆 Résume ta semaine commerciale (deals signés, RDV tenus, propositions envoyées, refus) :")
    print("   (Entrée deux fois pour terminer)\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "" and lignes and lignes[-1] == "":
            break
        lignes.append(ligne)
    bilan_semaine = "\n".join(lignes[:-1]) if lignes else "Semaine non renseignée."
    bilan_semaine = bilan_semaine[:3000]

    prompt = f"""
MISSION : Produire le rapport hebdomadaire des victoires commerciales de Caelum Partners
et définir le plan d'attaque de la semaine suivante.

BILAN SEMAINE FOURNI :
{bilan_semaine}

RAPPORT EN 5 SECTIONS :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 : VICTOIRES DE LA SEMAINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Deals signés : [liste avec CA et offre (500/1500/3000€)]
- CA généré cette semaine : [total]
- CA cumulé depuis le lancement
- Meilleure victoire non commerciale (nouveau contact, referral, insight marché)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 : MÉTRIQUES DE CONVERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Contacts initiés → Réponses obtenues (taux %)
- Réponses → RDV (taux %)
- RDV → Propositions (taux %)
- Propositions → Signatures (taux %)
- Canal le plus performant cette semaine
- Comparaison avec semaine précédente (tendance ↑ ↓ →)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 : LEÇONS APPRISES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Ce qui a fonctionné : [3 éléments précis avec pourquoi]
- Ce qui n'a pas fonctionné : [3 éléments précis avec hypothèse de cause]
- Insight marché belge PME découvert cette semaine
- Ajustement du pitch ou de l'offre recommandé

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 : PLAN D'ATTAQUE SEMAINE SUIVANTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lundi : [actions précises, volume, cibles]
Mardi : [actions]
Mercredi : [actions]
Jeudi : [actions]
Vendredi : [bilan + préparation semaine +2]

Objectif semaine suivante : X nouveaux contacts / Y RDV / Z propositions / N signatures
CA cible semaine suivante : [€]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5 : MESSAGE À L'OPTIMISEUR D'ÉNERGIE DÉCISIONNELLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Résumé en 3 points pour Chaima :
1. Ce qui a été accompli (fait accompli, chiffré)
2. La décision à prendre cette semaine
3. Le levier à activer la semaine prochaine pour croissance composée
"""
    resultat = streamer(prompt, "RAPPORT VICTOIRES SEMAINE — FORCE DE VENTE")
    sauvegarder("rapport_victoires_semaine", resultat)
    return resultat


def menu():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║          FORCE DE VENTE [56] — Caelum Partners                  ║
║         Attaque chirurgicale du marché belge PME IA              ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Préparer une offensive marché                                ║
║  2. Créer un script de closing                                   ║
║  3. Scorer le pipeline                                           ║
║  4. Rapport victoires de la semaine                              ║
║  0. Quitter                                                      ║
╚══════════════════════════════════════════════════════════════════╝
""")
    choix = input("  Votre choix : ").strip()
    return choix


if __name__ == "__main__":
    while True:
        choix = menu()
        if choix == "1":
            preparer_offensive_marche()
        elif choix == "2":
            creer_script_closing()
        elif choix == "3":
            scorer_pipeline_actuel()
        elif choix == "4":
            rapport_victoires_semaine()
        elif choix == "0":
            print("\n  Au revoir. Le marché attend.\n")
            break
        else:
            print("\n  [Choix invalide]\n")
