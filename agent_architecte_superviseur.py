"""
AGENT ARCHITECTE & SUPERVISEUR CAELUM PARTNERS V2 [82]
Orchestrateur méta — cartographie la flotte, détecte les défaillances, garantit la résilience.
Mission : Zéro interruption · Autonomie totale · Scalabilité internationale

Usage : python agent_architecte_superviseur.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

FLOTTE_DOMAINES = {
    "EXPANSION": [
        "agent_stratege_croissance.py", "agent_empire.py", "agent_chasseur_marches.py",
        "agent_architecte_diversification.py", "agent_asset_builder.py"
    ],
    "CONFORMITÉ": [
        "agent_convergence.py", "agent_juridique.py", "agent_conformite_offensive.py",
        "agent_rgpd_ops.py", "agent_comptable_belge.py", "agent_auditeur_financier.py"
    ],
    "MARKETING": [
        "agent_preuve_travail.py", "agent_marque.py", "agent_linkedin_content.py",
        "agent_blog_seo.py", "agent_newsletter.py", "agent_pitch_deck.py"
    ],
    "OPÉRATIONS": [
        "agent_facturation.py", "agent_support_client.py", "agent_onboarding_client.py",
        "agent_crm.py", "agent_generateur_devis.py", "agent_satisfaction_upsell.py"
    ],
    "INTELLIGENCE": [
        "agent_gardien_coherence.py", "agent_synthetiseur_realite.py",
        "agent_red_team.py", "agent_watchdog.py", "agent_auditeur_flotte.py"
    ],
    "COMMERCIAL": [
        "agent_commercial.py", "agent_email.py", "agent_negociateur.py",
        "agent_force_de_vente.py", "agent_calendrier_prospection.py"
    ]
}

IDENTITE = f"""# AGENT ARCHITECTE & SUPERVISEUR CAELUM PARTNERS V2

## MISSION D'OVERSIGHT
Tu es l'Architecte en chef et garant de la continuité opérationnelle de Caelum Partners.
Responsabilité : Gérer l'intégralité de la flotte d'agents, détecter les points de défaillance, automatiser la résilience.
Objectif : Autonomie totale de l'infrastructure, zéro interruption, scalabilité internationale.

## STRUCTURE OPÉRATIONNELLE
{json.dumps(FLOTTE_DOMAINES, ensure_ascii=False, indent=2)}

## PROTOCOLE DE RÉSILIENCE "ZÉRO DÉFAILLANCE"
1. LOGGING : Toute tâche est tracée avec timestamp, agent utilisé, résultat.
2. SATURATION API :
   a) Mettre en pause tâches à faible priorité (veille, reporting)
   b) Basculer vers modèle de secours si nécessaire
   c) Notifier Chaima avec estimation de reprise
3. INTÉGRITÉ : Avant toute nouvelle mission, vérifier si un agent existant peut l'exécuter.
4. ANTI-DOUBLON : Jamais créer deux agents avec la même mission.

## EXPANSION INTERNATIONALE
- Chaque nouvelle branche : sous-dossier conformité locale (Avocat, TVA, RGPD)
- Passage d'un pays à l'autre = simple changement de "module légal"
- Modules disponibles : Belgique (INASTI, BCE, CSC), France (URSSAF, SIRET), Luxembourg (TVA 17%)

## DIRECTIVE MAÎTRE
Analyser l'état de la flotte, identifier les goulots d'étranglement, proposer le protocole de basculement automatique."""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE,
                temperature=0.15,
                max_output_tokens=4000,
            ),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/superviseur", exist_ok=True)
    fichier = f"fichiers/superviseur/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def cartographie_flotte():
    """Cartographie complète de tous les agents par domaine."""
    agents_presents = [f for f in os.listdir(".") if f.startswith("agent_") and f.endswith(".py")]
    r = streamer(
        f"""COMMANDE MAÎTRE — CARTOGRAPHIE DE LA FLOTTE

Agents présents sur le système ({len(agents_presents)}) :
{chr(10).join(sorted(agents_presents))}

Structure par domaine cible :
{json.dumps(FLOTTE_DOMAINES, ensure_ascii=False, indent=2)}

Effectue :
1. CARTOGRAPHIE : classe chaque agent présent dans son domaine
2. COUVERTURE : identifie les domaines sous-couverts (< 3 agents)
3. GOULOTS : identifie les dépendances critiques (agent A bloque agent B)
4. MANQUANTS : liste les agents nécessaires pour 100% du cycle de vie
5. PRIORITÉ : classe les manquants par impact business (urgent/important/futur)""",
        "CARTOGRAPHIE COMPLÈTE DE LA FLOTTE"
    )
    sauvegarder("cartographie_flotte", r)


def analyse_couverture():
    """Analyse des gaps dans la couverture du cycle de vie client."""
    r = streamer(
        """ANALYSE DE COUVERTURE — 100% CYCLE DE VIE CAELUM PARTNERS

Le cycle de vie complet d'un client Caelum Partners :
PHASE 1 — ACQUISITION : prospection → contact → démo → proposition → signature
PHASE 2 — LIVRAISON : onboarding → développement → livraison → formation
PHASE 3 — FIDÉLISATION : suivi → satisfaction → upsell → référence
PHASE 4 — OPÉRATIONS : facturation → comptabilité → conformité → reporting
PHASE 5 — CROISSANCE : nouveaux marchés → partenariats → recrutement → scale

Pour chaque phase :
1. Quels agents couvrent cette phase ?
2. Quels gaps existent ?
3. Quel est le risque si ce gap n'est pas comblé ?
4. Recommandation prioritaire

Conclusion : score de couverture global /100""",
        "ANALYSE COUVERTURE CYCLE DE VIE"
    )
    sauvegarder("analyse_couverture", r)


def protocole_basculement():
    """Génère le protocole de basculement en cas de défaillance."""
    r = streamer(
        """PROTOCOLE DE BASCULEMENT AUTOMATIQUE — ZÉRO DÉFAILLANCE

Génère le protocole complet pour garantir que Caelum Partners continue de fonctionner même si :
- L'accès à Gemini API est temporairement coupé (quota, panne)
- Chaima est indisponible plusieurs jours
- Un agent retourne une erreur critique

FORMAT :

SCÉNARIO 1 — Panne API Gemini
→ Détection, actions immédiates, agent de secours, délai estimé

SCÉNARIO 2 — Chaima indisponible (maladie, voyage)
→ Tâches qui peuvent attendre, tâches critiques (facturation, réponse client), workflow de délégation

SCÉNARIO 3 — Erreur agent critique (commercial, facturation)
→ Diagnostic, isolation, plan B manuel, notification

SCÉNARIO 4 — Saturation (trop de missions simultanées)
→ Priorisation, file d'attente, délai par criticité

Pour chaque scénario : déclencheur → diagnostic → action → reprise.""",
        "PROTOCOLE BASCULEMENT AUTOMATIQUE"
    )
    sauvegarder("protocole_basculement", r)


def rapport_etat():
    """Rapport d'état complet de l'infrastructure."""
    agents_presents = [f for f in os.listdir(".") if f.startswith("agent_") and f.endswith(".py")]
    fichiers_data = [f for f in os.listdir(".") if f.endswith(".json")]
    r = streamer(
        f"""RAPPORT D'ÉTAT — INFRASTRUCTURE CAELUM PARTNERS
Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}

INVENTAIRE :
- Agents Python : {len(agents_presents)}
- Fichiers de données : {len(fichiers_data)}
- Domaines couverts : {len(FLOTTE_DOMAINES)}

Génère un RAPPORT EXÉCUTIF incluant :
1. ÉTAT DE SANTÉ GLOBAL (score /10)
2. AGENTS CRITIQUES (sans lesquels rien ne fonctionne)
3. AGENTS REDONDANTS (mission dupliquée, peut être fusionné)
4. PROCHAINE ACTION PRIORITAIRE (ce qui débloquera le plus de valeur)
5. ALERTE (si quelque chose nécessite attention immédiate)

Format : rapport dense, bullet points, pas de blabla.""",
        "RAPPORT D'ÉTAT INFRASTRUCTURE"
    )
    sauvegarder("rapport_etat", r)


def expansion_internationale():
    print("\n  Quel pays cibles-tu ? (ex: France, Luxembourg, Suisse, Pays-Bas) :")
    pays = input("  Pays → ").strip() or "France"
    r = streamer(
        f"""PLAN D'EXPANSION INTERNATIONALE — {pays.upper()}

Caelum Partners veut s'étendre en {pays}.
Génère le PLAN DE MODULE LÉGAL pour ce pays :

1. STRUCTURE JURIDIQUE RECOMMANDÉE (équivalent ASBL/SRL belge)
2. FISCALITÉ (TVA, seuils, obligations déclaratives)
3. CONTRATS À ADAPTER (CGV, mentions légales obligatoires)
4. RGPD/Protection données (spécificités locales)
5. DIFFÉRENCES CULTURELLES BUSINESS (comment prospecter différemment)
6. PARTENAIRES LOCAUX À TROUVER EN PRIORITÉ
7. TIMELINE D'ENTRÉE (6 mois réaliste)

Format : plan actionnable, pas théorique.""",
        f"EXPANSION — {pays.upper()}"
    )
    sauvegarder(f"expansion_{pays.lower()}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ARCHITECTE & SUPERVISEUR V2 — Caelum Partners")
    print("  Cartographie · Résilience · Expansion internationale")
    print("═"*65)

    while True:
        print("\n  1. Cartographie complète de la flotte")
        print("  2. Analyse de couverture (gaps cycle de vie)")
        print("  3. Protocole de basculement (zéro défaillance)")
        print("  4. Rapport d'état infrastructure")
        print("  5. Plan d'expansion internationale")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            cartographie_flotte()
        elif choix == "2":
            analyse_couverture()
        elif choix == "3":
            protocole_basculement()
        elif choix == "4":
            rapport_etat()
        elif choix == "5":
            expansion_internationale()
        else:
            print("  Choix invalide.")
