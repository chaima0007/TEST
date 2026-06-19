"""
AGENT ARCHITECTE DE DIVERSIFICATION — Micro-branches autonomes & omnipresence marché
Analyse de porosité · MVP lean · Automatisation par la flotte existante
Mission : rendre Caelum Partners omniprésent sur son segment

Usage : python agent_architecte_diversification.py
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

IDENTITE = """# AGENT ARCHITECTE DE DIVERSIFICATION

## IDENTITÉ
Tu es l'Architecte de Diversification de Caelum Partners.
Tu analyses le cœur de métier existant et tu conçois des micro-branches autonomes
qui étendent la présence de Caelum sur de nouveaux segments sans ressources supplémentaires.
Tu ne proposes que des diversifications actionnables avec l'infrastructure actuelle.

## MISSION
Identifier où les compétences actuelles de Caelum Partners peuvent résoudre
un nouveau problème client — et concevoir la structure minimale viable (MVP)
pour que cette branche tourne seule grâce à la flotte d'agents existante.

Objectif final : Caelum Partners omniprésent sur son segment.
Chaque euro de revenu génère une nouvelle branche autonome.

## MÉTHODOLOGIE DE TRAVAIL

### ANALYSE DE POROSITÉ
Les compétences actuelles de Caelum (à réutiliser) :
- Orchestration d'agents IA Gemini (72+ agents actifs)
- Rédaction professionnelle FR/NL/EN bilingue
- Conformité légale belge intégrée
- Automatisation de processus répétitifs
- Connaissance secteurs : immo, juridique, médical, RH, construction, HORECA
- Templates et playbooks réutilisables
- Prospection et closing B2B belge

Pour chaque nouvelle opportunité : quel % de ces compétences est directement transférable ?
Si > 70% → branche viable sans investissement majeur.

### MODÈLE LEAN MVP
Chaque micro-branche suit ce modèle :
1. PROBLÈME : quel problème précis résout-on ?
2. SOLUTION MINIMALE : le service le plus simple qui résout ce problème
3. PRIX MVP : quel tarif pour tester la demande ?
4. PREMIER CLIENT : qui contacter en premier pour valider ?
5. AUTOMATISATION : quels agents de la flotte gèrent cette branche ?

### CRITÈRES DE SÉLECTION D'UNE BRANCHE
Score sur 4 dimensions (chacune /10) :
- POROSITÉ (compétences transférables) : > 7/10 requis
- MARCHÉ (taille et accessibilité en Belgique) : > 6/10 requis
- AUTOMATISABILITÉ (peut tourner sans Chaima) : > 7/10 requis
- REVENU POTENTIEL (€ générable en 90 jours) : > 6/10 requis
Score total > 28/40 = branche à lancer

## STRUCTURE DE SORTIE — RAPPORT D'OPPORTUNITÉ
Pour chaque nouvelle branche proposée :
1. CONCEPT : description du service/produit en 3 phrases
2. CIBLE : clientèle visée (différente du cœur de métier)
3. SYNERGIE : pourquoi c'est facile à lancer avec les outils existants
4. PLAN D'AUTOMATISATION : quels agents de la flotte prennent en charge cette branche
5. MVP : comment tester cette branche cette semaine avec zéro investissement
6. PROJECTION 90 JOURS : revenus potentiels si 3 clients signent

## DIRECTIVE DE COMPORTEMENT
- Ne proposer que des branches actionnables avec l'infrastructure actuelle
- Chaque branche doit avoir un MVP testable en < 7 jours
- Chaque branche doit être automatisable par les agents existants (pas de nouveaux outils)
- Ne jamais proposer une branche qui viole la conformité ONEM de Chaima
- Prioriser les branches à haute marge (>80%) et faible temps de livraison (<14 jours)"""


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
                temperature=0.3,
                max_output_tokens=3500,
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
    os.makedirs("fichiers/diversification", exist_ok=True)
    fichier = f"fichiers/diversification/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def generer_3_branches():
    """Génère 3 nouvelles micro-branches de diversification actionnables."""
    r = streamer(
        """DIRECTIVE : Agis en tant qu'Architecte de Diversification.

Analyse le cœur de métier de Caelum Partners (agents IA, automatisation, rédaction pro,
conformité belge, services 500€/1500€/3000€ pour PME belges) et propose 3 nouvelles
branches de développement qui permettraient d'étendre notre présence tout en utilisant
l'infrastructure existante (72+ agents IA).

POUR CHAQUE BRANCHE — FORMAT RAPPORT D'OPPORTUNITÉ COMPLET :

━━━ BRANCHE [N] ━━━
1. CONCEPT : description du service en 3 phrases maximum
2. CIBLE : clientèle différente du cœur de métier (secteur + taille + profil décideur)
3. SYNERGIE : pourquoi nos compétences actuelles nous rendent imbattables sur ce segment
4. PLAN D'AUTOMATISATION : quels agents existants (nommer précisément) gèrent cette branche
5. MVP : comment tester cette semaine (action précise + premier prospect à contacter)
6. PROJECTION 90 JOURS : CA estimé si 3 clients à ce tarif
7. SCORE D'OPPORTUNITÉ /40 (Porosité + Marché + Automatisabilité + Revenu)

Priorité aux branches : haute marge (>80%), délai livraison <14 jours,
automatisables à >80% par les agents existants.""",
        "3 MICRO-BRANCHES DE DIVERSIFICATION — Caelum Partners"
    )
    sauvegarder("3_branches_diversification", r)


def analyser_opportunite_specifique():
    """Analyse une idée de diversification soumise par l'utilisateur."""
    print("\n  Décris l'opportunité ou l'idée de diversification à analyser.\n")
    idee = input("  Idée → ").strip()[:2000]
    if not idee:
        return
    r = streamer(
        f"""ANALYSE D'OPPORTUNITÉ DE DIVERSIFICATION

Idée soumise : {idee}

RAPPORT D'OPPORTUNITÉ COMPLET :
1. CONCEPT : reformulation précise du service proposé
2. CIBLE : qui exactement achèterait ce service ? (secteur, taille, rôle décideur)
3. ANALYSE DE POROSITÉ : % des compétences Caelum directement transférables
   → Liste précise des compétences utilisées
   → Ce qui manque et comment le combler
4. SYNERGIE AVEC LA FLOTTE : quels agents existants automatisent cette branche ?
5. SCORE D'OPPORTUNITÉ /40 :
   - Porosité /10
   - Marché belge /10
   - Automatisabilité /10
   - Revenu potentiel 90j /10
6. MVP CETTE SEMAINE : action concrète pour tester la demande en 7 jours
7. VERDICT : lancer / pivoter / abandonner — avec justification""",
        f"ANALYSE OPPORTUNITÉ — {idee[:50]}"
    )
    sauvegarder("analyse_opportunite", r)


def cartographier_branches_actives():
    """Cartographie toutes les branches potentielles selon le portefeuille de compétences."""
    r = streamer(
        """CARTOGRAPHIE COMPLÈTE — Branches de Diversification Caelum Partners

Cartographie systématique de toutes les micro-branches possibles
à partir des compétences et outils actuels de Caelum Partners.

MÉTHODE : Matrice Compétences × Segments

SEGMENTS BELGES À ANALYSER :
- Professions libérales (médecins, avocats, notaires, comptables, architectes)
- PME secteur tertiaire (consulting, formation, communication)
- Commerce de détail belge
- Secteur associatif / ASBL (connaissances internes)
- Startups et scale-ups belges
- Secteur public et communes belges
- E-commerce belge
- Artisans et indépendants

POUR CHAQUE SEGMENT :
- Score d'opportunité /40
- Branche recommandée (service spécifique)
- Prix MVP
- Premier agent de la flotte à mobiliser

CLASSEMENT FINAL : top 5 branches par score décroissant + plan de déploiement""",
        "CARTOGRAPHIE BRANCHES — Caelum Partners"
    )
    sauvegarder("cartographie_branches", r)


def plan_deploiement_branche():
    """Génère le plan de déploiement complet pour une branche validée."""
    print("\n  Quelle branche veux-tu déployer ?")
    branche = input("  Branche → ").strip()[:200]
    if not branche:
        return
    r = streamer(
        f"""PLAN DE DÉPLOIEMENT — Branche : {branche}

Générer le plan de déploiement COMPLET et OPÉRATIONNEL pour cette branche.

PLAN EN 4 PHASES :

PHASE 0 — VALIDATION (J1-J7, zéro investissement)
- Action de validation de la demande (qui contacter, quoi dire, quel résultat attendu)
- Signal "oui, on déploie" : si X prospects montrent de l'intérêt

PHASE 1 — MVP (J8-J30, premier client)
- Offre MVP : service minimum à livrer pour le premier client
- Prix MVP et justification
- Agents de la flotte mobilisés + leurs fonctions dans cette branche
- Processus de livraison complet (de la signature à la facturation)

PHASE 2 — OPTIMISATION (M2-M3, 3 clients)
- Automatisation progressive : quelles tâches encore manuelles passer en automatique ?
- Nouveaux agents à créer si nécessaire
- Ajustement du pricing selon les retours clients

PHASE 3 — SCALE (M4+, branche autonome)
- La branche tourne sans intervention de Chaima pour les tâches répétitives
- Métriques de succès (CA mensuel, nb clients, temps Chaima/client)
- Critère pour recruter ou sous-traiter""",
        f"PLAN DÉPLOIEMENT — {branche[:50]}"
    )
    sauvegarder(f"plan_deploiement_{branche.replace(' ', '_')[:30]}", r)


def bilan_portefeuille_branches():
    """Bilan de toutes les branches actives et leur contribution à l'empire."""
    r = streamer(
        """BILAN PORTEFEUILLE DE BRANCHES — Caelum Partners

Générer le tableau de bord de diversification de Caelum Partners.

ANALYSER :
1. CŒUR DE MÉTIER (services 500€/1500€/3000€) :
   - Stabilité, marges, risque de commoditisation
   - Quelle durée de vie estimée avant disruption ?

2. BRANCHES ADJACENTES ACTIVES (si données disponibles) :
   - Contribution au CA total
   - Niveau d'automatisation atteint
   - Satisfaction client

3. BRANCHES EN DÉVELOPPEMENT :
   - Avancement du MVP
   - Premiers signaux de demande

4. OPPORTUNITÉS IDENTIFIÉES NON ENCORE LANCÉES :
   - Classées par score d'opportunité

5. RECOMMANDATION PORTEFEUILLE :
   - Distribution idéale du CA dans 12 mois (% par branche)
   - Prochaine branche à lancer (basée sur le score)
   - Branche à arrêter si applicable""",
        "BILAN PORTEFEUILLE BRANCHES — Caelum Partners"
    )
    sauvegarder("bilan_portefeuille", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ARCHITECTE DE DIVERSIFICATION — Micro-branches Autonomes")
    print("  Porosité · MVP Lean · Automatisation · Omniprésence")
    print("═"*65)

    while True:
        print("\n  1. Générer 3 nouvelles micro-branches de diversification")
        print("  2. Analyser une opportunité de diversification spécifique")
        print("  3. Cartographier toutes les branches potentielles")
        print("  4. Plan de déploiement pour une branche validée")
        print("  5. Bilan du portefeuille de branches actif")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            generer_3_branches()
        elif choix == "2":
            analyser_opportunite_specifique()
        elif choix == "3":
            cartographier_branches_actives()
        elif choix == "4":
            plan_deploiement_branche()
        elif choix == "5":
            bilan_portefeuille_branches()
        else:
            print("  Choix invalide.")
