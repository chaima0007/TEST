"""
CAPTEUR DE SIGNAUX FAIBLES [54] — Détecteur d'opportunités avant qu'elles deviennent évidentes
Usage : python agent_capteur_signaux.py
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
Tu es le CAPTEUR DE SIGNAUX FAIBLES de Caelum Partners, cabinet IA bruxellois fondé par Chaima Mhadbi.
Ta mission : détecter les opportunités AVANT qu'elles deviennent évidentes pour la concurrence.
Tu reçois les inputs du CHASSEUR D'INEFFICACITÉ et valides lesquels sont de vraies opportunités.

Méthodologies maîtrisées :
1. Matrice d'Ansoff : marché existant/nouveau × produit existant/nouveau → 4 stratégies de croissance
2. Analyse STEEP : Social, Technologique, Économique, Environnemental, Politique — filtres macro
3. Courbe en S d'adoption : Early adopters → Early majority → Late majority → Laggards
4. Théorie du signal faible (Ansoff, 1975) : le bruit d'aujourd'hui est le signal de demain

Contexte marché belge IA :
- 4,1 millions d'utilisateurs LinkedIn en Belgique (cible privilégiée B2B)
- 99% des entreprises belges sont des PME (moins de 250 employés)
- Adoption IA dans les PME belges < 15% → marché vierge massif
- Double marché : francophone (Bruxelles, Wallonie) + néerlandophone (Flandre)
- Réglementations EU AI Act en cours → fenêtre d'opportunité pre-compliance

Caelum Partners : ASBL sociale + entité commerciale IA, Brussels.
Services : 500€ (audit) / 1500€ (implémentation) / 3000€ (accompagnement complet).
Phase lancement, 0 clients. Chaima seule + 50 agents IA.

Tu scores chaque signal de 0 à 100 avec une justification rigoureuse.
Un signal validé passe immédiatement à l'ARCHITECTE DE TALENTS pour préparation des ressources.
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
    os.makedirs("fichiers/signaux_faibles", exist_ok=True)
    fichier = f"fichiers/signaux_faibles/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def valider_opportunite(signal: str = "") -> str:
    """Valider si un signal est une vraie opportunité ou du bruit."""
    if not signal:
        print("\n🔍 Décris le signal à valider (opportunité, observation, tendance détectée) :")
        signal = input("  > ").strip()[:2000]

    if not signal:
        signal = "Signal non spécifié"

    prompt = f"""
MISSION : Valider si ce signal est une opportunité réelle pour Caelum Partners ou du bruit à ignorer.

SIGNAL À ANALYSER :
{signal}

PROCESSUS DE VALIDATION EN 5 ÉTAPES :

1. ANALYSE STEEP DU SIGNAL :
   - Social : quelle dynamique sociale sous-tend ce signal ?
   - Technologique : quelle maturité technologique est requise ?
   - Économique : quel est le potentiel de CA pour Caelum ?
   - Environnemental : contraintes réglementaires ou sectorielles ?
   - Politique : impact de l'EU AI Act ou politiques belges/UE ?

2. POSITIONNEMENT SUR LA COURBE EN S :
   - Où est ce signal dans le cycle d'adoption ? (Innovation → Early adopters → Majorité → Retardataires)
   - Fenêtre d'opportunité : combien de temps avant que ce soit mainstream ?
   - Avantage premier entrant pour Caelum si on agit maintenant ?

3. MATRICE D'ANSOFF — QUELLE STRATÉGIE ?
   - Pénétration marché (offre existante, marché existant) ?
   - Développement marché (offre existante, nouveau marché) ?
   - Développement produit (nouvelle offre, marché existant) ?
   - Diversification (nouvelle offre, nouveau marché) ?

4. SCORE OPPORTUNITÉ (0-100) :
   Critères pondérés :
   - Taille du marché adressable (20 pts)
   - Timing par rapport à la courbe S (20 pts)
   - Fit avec l'offre Caelum 500€/1500€/3000€ (20 pts)
   - Fenêtre concurrentielle (temps avant que ce soit saturé) (20 pts)
   - Facilité d'accès pour Chaima seule + 50 agents (20 pts)

5. VERDICT FINAL :
   ✅ OPPORTUNITÉ VALIDÉE / ⚠️ SIGNAL À SURVEILLER / ❌ BRUIT À IGNORER
   + Recommandation : transmettre à l'ARCHITECTE DE TALENTS ? Oui/Non + justification

Sois analytique, rigoureux et sans complaisance. Le score doit refléter la réalité du marché.
"""
    resultat = streamer(prompt, f"VALIDATION DE SIGNAL — CAPTEUR DE SIGNAUX FAIBLES")
    sauvegarder("validation_signal", resultat)
    return resultat


def scanner_signaux_marche_belge() -> str:
    """Scanner le marché belge des PME IA pour identifier les signaux faibles actuels."""
    prompt = """
MISSION : Scanner le marché belge des PME pour les signaux faibles IA en ce moment.

CONTEXTE DE SCAN :
- Marché cible : PME belges (< 250 employés), toutes régions (Bruxelles, Wallonie, Flandre)
- 4,1M utilisateurs LinkedIn Belgique, adoption IA PME < 15%
- Phase EU AI Act implémentation progressive
- Caelum Partners en phase lancement, cherche les 3 premiers clients

SCAN EN 6 DIMENSIONS :

1. SIGNAUX SECTORIELS (quels secteurs PME montrent des signes précurseurs d'adoption IA ?) :
   - Secteurs en mouvement observé
   - Signaux détectés (articles, LinkedIn, tendances)
   - Score d'urgence par secteur (1-10)

2. SIGNAUX DE DOULEUR (quelles douleurs PME belges sont non résolues et adressables par IA ?) :
   - Top 5 douleurs identifiées
   - Quelle offre Caelum les adresse (500€/1500€/3000€) ?
   - Intensité de la douleur (1-10)

3. SIGNAUX CONCURRENTIELS (qui entre sur ce marché ?) :
   - Acteurs entrants détectés
   - Zones encore non couvertes = fenêtres pour Caelum
   - Délai estimé avant saturation de chaque zone

4. SIGNAUX RÉGLEMENTAIRES (EU AI Act, RGPD, aides publiques belges à l'IA ?) :
   - Nouvelles obligations créant un besoin d'accompagnement
   - Aides/subventions disponibles → argument commercial pour les PME

5. SIGNAUX TECHNOLOGIQUES (quelles nouveautés IA créent des opportunités d'implémentation PME ?) :
   - Technologies accessibles aux PME en 2024-2025
   - Cas d'usage ROI rapide (< 3 mois) pour PME belges

6. TOP 5 SIGNAUX FAIBLES PRIORITAIRES POUR CAELUM :
   Classés par : Score global / Urgence / Fit Caelum / Action recommandée

TRANSMISSION : Quels signaux valident une opportunité immédiate à passer à l'ARCHITECTE DE TALENTS ?
"""
    resultat = streamer(prompt, "SCAN MARCHÉ BELGE IA — CAPTEUR DE SIGNAUX FAIBLES")
    sauvegarder("scan_marche_belge", resultat)
    return resultat


def prioriser_opportunites(liste_opportunites: str = "") -> str:
    """Prioriser une liste d'opportunités par timing, taille de marché, fit Caelum et fenêtre concurrentielle."""
    if not liste_opportunites:
        print("\n📋 Colle ta liste d'opportunités (une par ligne, Entrée deux fois pour terminer) :")
        lignes = []
        while True:
            ligne = input()
            if ligne == "" and lignes and lignes[-1] == "":
                break
            lignes.append(ligne)
        liste_opportunites = "\n".join(lignes[:-1]) if lignes else "Aucune opportunité fournie."
    liste_opportunites = liste_opportunites[:3000]

    prompt = f"""
MISSION : Prioriser cette liste d'opportunités pour Caelum Partners selon une grille multi-critères rigoureuse.

OPPORTUNITÉS À PRIORISER :
{liste_opportunites}

GRILLE DE PRIORISATION — 4 CRITÈRES PONDÉRÉS :

Pour chaque opportunité, score sur 100 :

1. TIMING (25 pts) :
   - Où est-on sur la courbe S ? (Early = 25pts, Growing = 15pts, Mature = 5pts)
   - Fenêtre avant que ce soit mainstream ?

2. TAILLE DU MARCHÉ ADRESSABLE (25 pts) :
   - Nombre de PME belges concernées
   - CA potentiel annuel pour Caelum (missions 500€/1500€/3000€)

3. FIT CAELUM (25 pts) :
   - Alignement avec les services actuels ?
   - Chaima peut-elle attaquer seule + 50 agents ?
   - Délai pour première livraison ?

4. FENÊTRE CONCURRENTIELLE (25 pts) :
   - Combien de concurrents déjà positionnés ?
   - Différenciation Caelum possible ?
   - Durée estimée de l'avantage premier entrant ?

SORTIE :

1. TABLEAU DE PRIORISATION :
   | Opportunité | Timing | Marché | Fit | Concurrence | TOTAL | Rang |

2. TOP 3 OPPORTUNITÉS À ATTAQUER MAINTENANT :
   Pour chacune : pourquoi maintenant, comment, par qui (quel agent IA Caelum ?)

3. OPPORTUNITÉS À SURVEILLER (dans 3-6 mois) :
   Signal à remonter : déclencheur à observer pour attaquer

4. OPPORTUNITÉS À ABANDONNER :
   Justification rigoureuse

5. TRANSMISSION À L'ARCHITECTE DE TALENTS :
   Liste des opportunités validées avec brief de préparation des ressources

Classe avec précision. La mauvaise priorisation est la forme la plus coûteuse de gaspillage.
"""
    resultat = streamer(prompt, "PRIORISATION DES OPPORTUNITÉS — CAPTEUR DE SIGNAUX FAIBLES")
    sauvegarder("priorisation_opportunites", resultat)
    return resultat


def rapport_opportunites_validees() -> str:
    """Rapport hebdomadaire des opportunités validées, prêt pour l'ARCHITECTE DE TALENTS."""
    prompt = """
MISSION : Produire le rapport hebdomadaire des opportunités validées pour Caelum Partners.
Ce rapport est transmis directement à l'ARCHITECTE DE TALENTS pour préparation des ressources.

FORMAT DU RAPPORT HEBDOMADAIRE :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAPPORT SIGNAUX FAIBLES — SEMAINE [N]
Caelum Partners | Chaima Mhadbi | Brussels
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. RÉSUMÉ EXÉCUTIF (3 lignes max) :
   - Nombre de signaux analysés cette semaine
   - Nombre d'opportunités validées
   - Opportunité #1 à attaquer immédiatement

2. OPPORTUNITÉS VALIDÉES (Score ≥ 70/100) :
   Pour chaque opportunité validée :
   - Description de l'opportunité
   - Score final et détail par critère
   - Segment cible de PME belges
   - Offre Caelum recommandée (500€/1500€/3000€)
   - Fenêtre d'action : combien de jours avant expiration ?
   - Brief pour l'ARCHITECTE DE TALENTS : ressources nécessaires

3. SIGNAUX EN OBSERVATION (Score 40-69/100) :
   - Signal + déclencheur à observer pour validation
   - Horizon de réévaluation

4. SIGNAUX ÉCARTÉS (Score < 40/100) :
   - Signal + raison d'élimination (1 ligne chacun)

5. MÉTRIQUES HEBDOMADAIRES :
   - Ratio signal/opportunité validée
   - Valeur CA potentielle des opportunités validées (€)
   - Top secteur PME belge identifié cette semaine

6. INSTRUCTIONS POUR L'ARCHITECTE DE TALENTS :
   Brief précis : quelles ressources préparer pour attaquer les opportunités validées ?

Ce rapport est la boussole stratégique hebdomadaire de Caelum Partners.
"""
    resultat = streamer(prompt, "RAPPORT HEBDO OPPORTUNITÉS VALIDÉES — CAPTEUR DE SIGNAUX FAIBLES")
    sauvegarder("rapport_opportunites_validees", resultat)
    return resultat


def menu():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║       CAPTEUR DE SIGNAUX FAIBLES [54] — Caelum Partners         ║
║         Détecteur d'opportunités avant qu'elles soient évidentes ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Valider un signal                                            ║
║  2. Scanner le marché belge                                      ║
║  3. Prioriser des opportunités                                   ║
║  4. Rapport opportunités validées                                ║
║  0. Quitter                                                      ║
╚══════════════════════════════════════════════════════════════════╝
""")
    choix = input("  Votre choix : ").strip()
    return choix


if __name__ == "__main__":
    while True:
        choix = menu()
        if choix == "1":
            valider_opportunite()
        elif choix == "2":
            scanner_signaux_marche_belge()
        elif choix == "3":
            prioriser_opportunites()
        elif choix == "4":
            rapport_opportunites_validees()
        elif choix == "0":
            print("\n  Au revoir. Les signaux n'attendent pas.\n")
            break
        else:
            print("\n  [Choix invalide]\n")
