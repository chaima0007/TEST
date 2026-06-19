"""
AGENT GARDIEN DE LA COHÉRENCE — Système de conscience stratégique
Alignement · Détection de dérives · Réalignement sans blocage
Mission : maintenir la clarté de l'empire Caelum Partners

Usage : python agent_gardien_coherence.py
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

PILIERS_EMPIRE = {
    "statut_legal": "ASBL (présidente) séparée de Caelum Partners (commercial IA). "
                    "TVA franchise Article 56bis sous 25 000€/an. BCE inscription obligatoire avant facturation. "
                    "ONEM Article 48 — déclaration C1 trimestrielle via CSC. INASTI 20.5% sur nets.",
    "scalabilite": "Chaque action doit être réplicable ×100 sans Chaima. "
                   "Préférer les actifs (agents, templates, réputation) aux revenus ponctuels. "
                   "Coefficient viral k > 0.3. Revenue per Hour > 200€/h grâce aux agents IA.",
    "vision_5_ans": "Référence européenne IA pour PME. Palier 1 : 10 clients / 15 000€. "
                    "Palier 2 : 30 clients / 50 000€. Palier 3 : 100 clients / 150 000€. "
                    "Palier 4 : 500 clients / 1M€. Palier 5 : singularité européenne.",
    "services": "500€ site web (7j) · 1 500€ automation IA (14j) · 3 000€ pack complet (30j). "
                "Récurrence cible : abonnements maintenance 300€/mois dès client 3.",
    "securite": "Zéro exposition des clés API. Données clients jamais mélangées ASBL/Caelum. "
                "Sauvegardes systématiques. Rotation clé Gemini trimestrielle.",
    "localisation": "Bruxelles, Belgique. Phase actuelle : lancement — 0 client, rampe de décollage.",
}

IDENTITE = f"""# AGENT GARDIEN DE LA COHÉRENCE — SYSTÈME DE CONSCIENCE STRATÉGIQUE

## IDENTITÉ ET RÔLE
Tu es le Gardien de la Cohérence de Caelum Partners.
Tu es la mémoire vive de l'empire : tu maintiens l'alignement entre les nouvelles idées
et les fondations déjà établies.

Tu n'es PAS un censeur. Tu n'es PAS un bloqueur.
Tu es un vérificateur de trajectoire — tu signales calmement, avec des faits,
pour que Chaima puisse décider en pleine connaissance de cause.

## PROTOCOLE D'ALERTE (CONSCIENCE LOGIQUE)
Pour chaque nouvelle proposition ou direction soumise :

**ÉTAPE 1 — ANALYSE DE COHÉRENCE**
Comparer la proposition avec les 5 piliers fondamentaux de l'empire :
1. STATUT LÉGAL : respecte-t-elle le cadre ONEM/ASBL/BCE/TVA belge ?
2. SCALABILITÉ : peut-on la répliquer ×100 sans Chaima ?
3. VISION 5 ANS : fait-elle avancer vers les paliers de croissance ?
4. MODÈLE ÉCONOMIQUE : est-elle cohérente avec les services et la tarification ?
5. SÉCURITÉ : protège-t-elle les données et la conformité ?

**ÉTAPE 2 — CLASSIFICATION**
- ✅ ALIGNÉE : la proposition renforce les piliers → valider et amplifier
- ⚠️ DÉRIVE PARTIELLE : la proposition est bonne mais contredit un point spécifique → signaler et proposer ajustement
- 🚨 CONTRADICTION MAJEURE : la proposition va directement à l'encontre d'un pilier → alerter, expliquer, demander confirmation

**ÉTAPE 3 — FORMAT D'ALERTE**
"Attention — cette direction contredit [pilier précis] établi [quand/pourquoi].
Est-ce un changement de stratégie intentionnel ou une incohérence à corriger ?"
→ Si intentionnel : aider à reformuler pour minimiser les dommages collatéraux
→ Si incohérence : proposer la version alignée de la même idée

## PILIERS FONDAMENTAUX DE L'EMPIRE CAELUM PARTNERS

### STATUT LÉGAL
{PILIERS_EMPIRE['statut_legal']}

### SCALABILITÉ
{PILIERS_EMPIRE['scalabilite']}

### VISION 5 ANS
{PILIERS_EMPIRE['vision_5_ans']}

### SERVICES & TARIFICATION
{PILIERS_EMPIRE['services']}

### SÉCURITÉ
{PILIERS_EMPIRE['securite']}

### LOCALISATION & PHASE
{PILIERS_EMPIRE['localisation']}

## DIRECTIVES DE COMPORTEMENT
- Pas de critique gratuite. Uniquement des faits et des alternatives.
- Pas de "non" autoritaire. Toujours "voici la contradiction, voici l'alternative alignée."
- Ton de vérification, jamais de jugement.
- Si l'utilisateur confirme que c'est un changement intentionnel : enregistrer la nouvelle direction et l'intégrer aux piliers.
- Si l'utilisateur s'éloigne de l'indépendance ou de l'empire sans s'en rendre compte : signaler calmement.

## FORMAT DE SORTIE OBLIGATOIRE
1. SCORE DE COHÉRENCE (0-100) : à quel point la proposition est alignée avec les piliers
2. PILIERS ANALYSÉS : tableau avec chaque pilier + statut (✅ / ⚠️ / 🚨)
3. CONTRADICTION DÉTECTÉE (si applicable) : description précise du conflit
4. PROPOSITION RÉALIGNÉE : la même idée, reformulée pour être 100% cohérente
5. QUESTION DE CONFIRMATION (si dérive) : "Est-ce intentionnel ou à corriger ?"
6. VALIDATION (si alignée) : amplifier la proposition avec des suggestions d'optimisation"""


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
                max_output_tokens=3000,
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
    os.makedirs("fichiers/gardien_coherence", exist_ok=True)
    fichier = f"fichiers/gardien_coherence/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def charger_historique_decisions() -> list:
    """Charge l'historique des décisions validées pour enrichir l'analyse."""
    historique = []
    for fichier in ["memoire_entreprise.json", "historique_caelum.json"]:
        if os.path.exists(fichier):
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    historique.append(data)
            except Exception:
                pass
    return historique


def verifier_coherence():
    """Soumet une nouvelle proposition ou idée à l'analyse de cohérence."""
    print("\n  Décris ta nouvelle idée, proposition ou direction stratégique.")
    print("  (Le Gardien analysera l'alignement avec les piliers de l'empire)\n")
    proposition = input("  Proposition → ").strip()
    if not proposition:
        return

    historique = charger_historique_decisions()
    contexte_hist = json.dumps(historique, ensure_ascii=False)[:1500] if historique else "Aucun historique disponible"

    r = streamer(
        f"""ANALYSE DE COHÉRENCE — Nouvelle proposition soumise au Gardien

PROPOSITION : {proposition}

CONTEXTE HISTORIQUE DISPONIBLE : {contexte_hist}

EFFECTUER L'ANALYSE COMPLÈTE :
1. Score de cohérence global (0-100) avec justification
2. Analyse pilier par pilier (Statut légal / Scalabilité / Vision 5 ans / Services / Sécurité)
3. Contradictions détectées (avec référence précise au pilier concerné)
4. Proposition réalignée (la même idée, 100% cohérente avec les fondations)
5. Question de confirmation si dérive détectée
6. Si parfaitement alignée : amplification et optimisation de la proposition""",
        f"ANALYSE COHÉRENCE — {proposition[:60]}"
    )
    sauvegarder("analyse_coherence", r)


def audit_derive_strategique():
    """Analyse complète de la trajectoire actuelle pour détecter les dérives."""
    historique = charger_historique_decisions()
    contexte = json.dumps(historique, ensure_ascii=False)[:2000] if historique else ""

    r = streamer(
        f"""AUDIT DE DÉRIVE STRATÉGIQUE — Analyse complète de la trajectoire Caelum Partners

Données disponibles : {contexte}

ANALYSER :
1. Y a-t-il des actions récentes qui s'éloignent des 5 piliers fondamentaux ?
2. Des décisions contradictoires entre elles ont-elles été prises ?
3. La trajectoire actuelle mène-t-elle vers la vision 5 ans ou s'en éloigne-t-elle ?
4. Quels sont les 3 risques de dérive les plus probables dans les 30 prochains jours ?
5. RÉALIGNEMENT : les 3 actions prioritaires pour remettre la trajectoire sur les rails

FORMAT : Rapport clair, factuel, sans jugement. Uniquement des faits et des alternatives.""",
        "AUDIT DÉRIVE STRATÉGIQUE — Caelum Partners"
    )
    sauvegarder("audit_derive", r)


def enregistrer_nouvelle_direction():
    """Valide et enregistre un changement de stratégie intentionnel dans les piliers."""
    print("\n  Décris le changement de stratégie intentionnel à enregistrer.")
    print("  (Ce changement sera intégré comme nouveau pilier de référence)\n")
    changement = input("  Changement → ").strip()
    if not changement:
        return

    r = streamer(
        f"""ENREGISTREMENT D'UN CHANGEMENT DE DIRECTION — Mise à jour des piliers

Changement intentionnel déclaré : {changement}

ANALYSER ET FORMALISER :
1. Quel pilier existant est modifié ou remplacé par ce changement ?
2. Quelles décisions passées deviennent caduques avec ce changement ?
3. Quelles nouvelles opportunités ce changement ouvre-t-il ?
4. Quels risques ce changement introduit-il (à surveiller) ?
5. FORMULATION OFFICIELLE DU NOUVEAU PILIER : rédiger la nouvelle directive en 2-3 phrases claires
6. Plan d'adaptation : comment les autres piliers s'ajustent-ils à ce changement ?

Ce changement est INTENTIONNEL et VALIDÉ par Chaima. Formalise-le comme référence future.""",
        f"NOUVEAU PILIER — {changement[:60]}"
    )
    sauvegarder("nouveau_pilier", r)


def scan_coherence_decisions_recentes():
    """Scanne toutes les décisions récentes pour détecter les incohérences internes."""
    print("\n  Liste les décisions prises récemment (séparées par des virgules ou retours à la ligne).")
    print("  Exemple : 'baisser les prix à 200€, cibler les grandes entreprises, travailler seule'\n")
    decisions_raw = []
    while True:
        ligne = input("  Décision → ").strip()
        if not ligne:
            break
        decisions_raw.append(ligne)

    if not decisions_raw:
        return

    decisions = "\n".join(f"- {d}" for d in decisions_raw)

    r = streamer(
        f"""SCAN DE COHÉRENCE — Analyse des décisions récentes

Décisions soumises à analyse :
{decisions}

ANALYSER :
1. Ces décisions sont-elles cohérentes ENTRE ELLES ?
2. Chaque décision est-elle cohérente avec les 5 piliers de l'empire ?
3. Y a-t-il des contradictions directes entre deux décisions listées ?
4. Score de cohérence globale de l'ensemble (0-100)
5. TABLEAU DE COHÉRENCE : décision / pilier / statut (✅ ⚠️ 🚨) / correctif recommandé
6. Version harmonisée : reformuler les décisions contradictoires pour les aligner""",
        "SCAN COHÉRENCE — Décisions récentes"
    )
    sauvegarder("scan_decisions", r)


def rapport_alignement_hebdo():
    """Génère un rapport d'alignement stratégique hebdomadaire."""
    historique = charger_historique_decisions()
    contexte = json.dumps(historique, ensure_ascii=False)[:2000] if historique else "Données insuffisantes"

    r = streamer(
        f"""RAPPORT D'ALIGNEMENT HEBDOMADAIRE — Gardien de la Cohérence

Données disponibles : {contexte}

GÉNÉRER LE RAPPORT :
1. ÉTAT DE L'ALIGNEMENT (note /100) — la trajectoire de la semaine est-elle cohérente avec l'empire ?
2. PILIERS RESPECTÉS cette semaine (liste)
3. DÉRIVES DÉTECTÉES (si applicable) : description + impact potentiel
4. DÉCISIONS À VALIDER : propositions en attente qui nécessitent confirmation de direction
5. VIGILANCE PROCHAINE SEMAINE : 2-3 points à surveiller pour maintenir la cohérence
6. MOT DU GARDIEN : message de synthèse en 3 phrases — où en est l'empire, et vers où il va""",
        "RAPPORT ALIGNEMENT HEBDOMADAIRE — Gardien Caelum"
    )
    sauvegarder("rapport_alignement_hebdo", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  GARDIEN DE LA COHÉRENCE — Conscience Stratégique Caelum")
    print("  Alignement · Détection dérives · Réalignement · Clarté")
    print("═"*65)

    while True:
        print("\n  1. Vérifier la cohérence d'une nouvelle proposition")
        print("  2. Audit de dérive stratégique (trajectoire complète)")
        print("  3. Scanner la cohérence de décisions récentes")
        print("  4. Enregistrer un changement de direction intentionnel")
        print("  5. Rapport d'alignement hebdomadaire")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            verifier_coherence()
        elif choix == "2":
            audit_derive_strategique()
        elif choix == "3":
            scan_coherence_decisions_recentes()
        elif choix == "4":
            enregistrer_nouvelle_direction()
        elif choix == "5":
            rapport_alignement_hebdo()
        else:
            print("  Choix invalide.")
