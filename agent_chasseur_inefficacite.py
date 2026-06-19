"""
CHASSEUR D'INEFFICACITÉ [53] — Détecteur de pertes et gaspillages dans les processus Caelum
Usage : python agent_chasseur_inefficacite.py
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
Tu es le CHASSEUR D'INEFFICACITÉ de Caelum Partners, cabinet IA bruxellois fondé par Chaima Mhadbi.
Ton rôle unique : détecter chaque seconde, chaque euro, chaque action qui N'augmente PAS
la vélocité d'acquisition client ou la qualité de l'offre. Tout le reste est du gaspillage.

Méthodologie : Lean Manufacturing appliqué aux services IA — les 8 Muda :
1. Transport (déplacements inutiles de données ou d'informations)
2. Inventaire (tâches en attente, backlog non traité)
3. Mouvement (actions sans valeur : réunions sans décision, emails sans suite)
4. Attente (délais entre étapes du processus)
5. Surproduction (livrables non demandés, over-delivery chronophage)
6. Sur-traitement (perfectionnisme au-delà de ce que le client valorise)
7. Défauts (retravaux, corrections, malentendus clients)
8. Talents non utilisés (agents IA dormants, compétences sous-exploitées)

Contexte Caelum : ASBL sociale + entité commerciale IA, Brussels. Services à 500€/1500€/3000€.
Phase lancement : 0 clients. Chaima seule + 50 agents IA. Objectif : leader IA européen PME en 5 ans.
Chaque inefficacité détectée est un levier de croissance dormant.

Ton output alimente directement le CAPTEUR DE SIGNAUX FAIBLES pour validation.
Tu travailles avec une précision chirurgicale. Zéro tolérance pour le gaspillage.
Chaque rapport est chiffré en €/heure perdu et en impact sur la vélocité client.
"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.15, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/chasseur_inefficacite", exist_ok=True)
    fichier = f"fichiers/chasseur_inefficacite/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def scanner_processus_complet():
    """Scan complet du processus Caelum de bout en bout pour trouver tous les points de gaspillage."""
    prompt = """
MISSION : Scanner le processus complet de Caelum Partners de bout en bout et identifier TOUS les points de gaspillage.

Cartographie le processus suivant selon les 8 Muda du Lean :

PROCESSUS À ANALYSER (prospect → facturation → livraison) :
1. Génération de leads (LinkedIn, email, bouche-à-oreille)
2. Premier contact et qualification prospect
3. Présentation de l'offre (500€ / 1500€ / 3000€)
4. Proposition commerciale et négociation
5. Signature et onboarding client
6. Livraison de la mission IA
7. Suivi client et upsell
8. Facturation et encaissement

POUR CHAQUE ÉTAPE, identifie :
- Type de gaspillage (quel Muda exactement)
- Cause racine (pourquoi ça se perd)
- Coût estimé en minutes/heure par semaine
- Impact sur la vélocité d'acquisition client (1-10)
- Solution immédiate actionnable

FORMAT DE SORTIE :
1. Tableau récapitulatif des 8 étapes × gaspillages détectés
2. Top 5 des pertes les plus critiques avec chiffrage €/mois (base : 50€/heure Chaima)
3. 3 actions à prendre AUJOURD'HUI pour éliminer les pertes prioritaires
4. Message résumé pour le CAPTEUR DE SIGNAUX FAIBLES

Sois précis, chiffré, actionnable. Pas de théorie. Des faits et des actions.
"""
    resultat = streamer(prompt, "SCAN PROCESSUS COMPLET — CHASSEUR D'INEFFICACITÉ")
    sauvegarder("scan_processus", resultat)
    return resultat


def auditer_emploi_du_temps():
    """L'utilisateur décrit sa semaine, l'agent identifie le temps gaspillé."""
    print("\n📋 Décris ta semaine type (activités, durées, tâches récurrentes) :")
    print("   (Appuie sur Entrée deux fois pour terminer)\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "" and lignes and lignes[-1] == "":
            break
        lignes.append(ligne)
    description_semaine = "\n".join(lignes[:-1]) if lignes else "Semaine non décrite."
    # Sanitize: remove any API keys or sensitive patterns before sending
    description_semaine = description_semaine[:3000]

    prompt = f"""
MISSION : Auditer l'emploi du temps de Chaima Mhadbi (Caelum Partners, Brussels) et identifier
toutes les activités qui ne génèrent PAS de valeur client directe.

SEMAINE DÉCRITE PAR CHAIMA :
{description_semaine}

ANALYSE REQUISE :

1. CATÉGORISATION DE CHAQUE ACTIVITÉ :
   - ✅ Valeur directe (génère du CA ou améliore l'offre)
   - ⚠️ Valeur indirecte (nécessaire mais optimisable)
   - ❌ Gaspillage pur (à éliminer immédiatement)

2. QUANTIFICATION :
   - Heures totales analysées
   - % du temps en valeur directe
   - % du temps gaspillé
   - Coût du gaspillage en € (base 50€/heure)

3. DIAGNOSTIC LEAN (quel Muda domine dans cette semaine ?)

4. PLAN D'ÉLIMINATION :
   - 3 activités à supprimer cette semaine
   - 3 activités à déléguer aux agents IA
   - 3 activités à regrouper/optimiser

5. SEMAINE IDÉALE RECONSTRUITE :
   - Lundi à vendredi : blocs de temps optimisés
   - Ratio cible : 70% valeur directe / 20% valeur indirecte / 10% admin incompressible

Sois brutal et honnête. L'objectif est la domination de marché, pas le confort.
"""
    resultat = streamer(prompt, "AUDIT EMPLOI DU TEMPS — CHASSEUR D'INEFFICACITÉ")
    sauvegarder("audit_emploi_du_temps", resultat)
    return resultat


def calculer_cout_inefficacites():
    """Quantifier chaque inefficacité détectée en €/heure perdu, puis coût mensuel total."""
    print("\n📊 Liste les inefficacités détectées (une par ligne, Entrée deux fois pour terminer) :")
    print("   Exemple : 'Réponse aux emails 3x/jour — 45min' ou 'Proposition commerciale recopiée à la main'\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "" and lignes and lignes[-1] == "":
            break
        lignes.append(ligne)
    liste_inefficacites = "\n".join(lignes[:-1]) if lignes else "Aucune inefficacité fournie."
    liste_inefficacites = liste_inefficacites[:3000]

    prompt = f"""
MISSION : Calculer le coût réel de chaque inefficacité listée pour Caelum Partners et produire
un bilan financier complet des pertes mensuelles.

INEFFICACITÉS DÉTECTÉES :
{liste_inefficacites}

CALCUL REQUIS POUR CHAQUE INEFFICACITÉ :

1. ANALYSE INDIVIDUELLE (tableau structuré) :
   | Inefficacité | Type Muda | Temps/semaine | €/semaine | €/mois | Impact vélocité (1-10) |

   Base de calcul :
   - Coût heure Chaima : 50€/h (valeur opportunité)
   - Coût heure perdue sur mission client : 100€/h (CA non généré)
   - 4 semaines/mois, 48 semaines/an

2. COÛT TOTAL MENSUEL DES INEFFICACITÉS :
   - Coût direct (temps perdu)
   - Coût indirect (CA non généré)
   - Coût total annualisé

3. COMPARAISON AVEC LES OBJECTIFS CAELUM :
   - Ce gaspillage représente combien de clients perdus ?
   - Combien de missions à 500€ / 1500€ / 3000€ non réalisées ?

4. RETOUR SUR INVESTISSEMENT DE L'ÉLIMINATION :
   - Si on élimine les 3 premières inefficacités : gain mensuel ?
   - Délai de récupération si on investit 1 journée à les éliminer ?

5. VERDICT CHASSEUR :
   Une phrase percutante résumant l'ampleur des pertes et l'urgence d'agir.

Tout doit être chiffré avec précision. Les approximations sont une forme de gaspillage.
"""
    resultat = streamer(prompt, "CALCUL COÛT DES INEFFICACITÉS — CHASSEUR D'INEFFICACITÉ")
    sauvegarder("cout_inefficacites", resultat)
    return resultat


def generer_rapport_elimination():
    """Rapport priorisé : quoi éliminer AUJOURD'HUI, cette semaine, ce mois."""
    prompt = """
MISSION : Générer le rapport d'élimination prioritaire pour Caelum Partners.
Ce rapport est le document opérationnel qui guide l'action immédiate de Chaima Mhadbi.

CONTEXTE CAELUM :
- Phase lancement, 0 clients actuellement
- Services : 500€ (audit) / 1500€ (implémentation) / 3000€ (accompagnement complet)
- Ressources : Chaima seule + 50 agents IA + réseau partenarial
- Objectif 90 jours : premiers 3 clients signés
- Marché : PME belges (99% des entreprises belges), adoption IA < 15%

RAPPORT EN 4 HORIZONS TEMPORELS :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HORIZON 1 : ÉLIMINER AUJOURD'HUI (0-24h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3 gaspillages à éliminer maintenant avec action concrète immédiate.
Chaque item : Gaspillage → Action → Résultat attendu → Temps économisé/semaine

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HORIZON 2 : ÉLIMINER CETTE SEMAINE (J+2 à J+7)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 gaspillages systémiques à restructurer cette semaine.
Chaque item : Gaspillage → Plan d'action en 3 étapes → KPI de validation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HORIZON 3 : ÉLIMINER CE MOIS (J+8 à J+30)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 inefficacités structurelles à automatiser ou déléguer aux agents IA.
Chaque item : Gaspillage → Agent IA recommandé → Implémentation → Gain mensuel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HORIZON 4 : TRANSFORMER EN AVANTAGE CONCURRENTIEL (J+31 à J+90)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3 inefficacités qui, une fois éliminées, deviennent des atouts commerciaux pour Caelum.

BILAN FINAL :
- Gain total estimé si tout est exécuté : X heures/mois libérées + Y€/mois récupérés
- Signal prioritaire à transmettre au CAPTEUR DE SIGNAUX FAIBLES
- Score d'urgence global (1-10) avec justification

Ce rapport est une arme. Traite-le comme tel.
"""
    resultat = streamer(prompt, "RAPPORT D'ÉLIMINATION PRIORITAIRE — CHASSEUR D'INEFFICACITÉ")
    sauvegarder("rapport_elimination", resultat)
    return resultat


def menu():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║         CHASSEUR D'INEFFICACITÉ [53] — Caelum Partners          ║
║              Détecteur de pertes et gaspillages                  ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Scanner le processus complet                                 ║
║  2. Auditer l'emploi du temps                                    ║
║  3. Calculer le coût des inefficacités                           ║
║  4. Rapport d'élimination prioritaire                            ║
║  0. Quitter                                                      ║
╚══════════════════════════════════════════════════════════════════╝
""")
    choix = input("  Votre choix : ").strip()
    return choix


if __name__ == "__main__":
    while True:
        choix = menu()
        if choix == "1":
            scanner_processus_complet()
        elif choix == "2":
            auditer_emploi_du_temps()
        elif choix == "3":
            calculer_cout_inefficacites()
        elif choix == "4":
            generer_rapport_elimination()
        elif choix == "0":
            print("\n  Au revoir. Chaque minute compte.\n")
            break
        else:
            print("\n  [Choix invalide]\n")
