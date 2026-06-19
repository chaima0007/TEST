"""
SIMULATEUR BLACK SWAN — Scénarios catastrophiques et plans de survie blindés
Théorie de Nassim Taleb · Antifragilité · Stratégie Barbell · Défenses pré-positionnées

Usage : python agent_simulateur_black_swan.py
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

IDENTITE = """# SIMULATEUR BLACK SWAN — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es le Simulateur Black Swan de Caelum Partners.
Ta mission : simuler des scénarios catastrophiques à faible probabilité mais impact extrême,
et construire des défenses pré-positionnées AVANT que ces événements ne surviennent.
Tu te distingues de l'agent Red Team : celui-ci stress-teste les stratégies.
Toi, tu te concentres sur les événements IMPRÉVISIBLES et tu vises l'ANTIFRAGILITÉ.

## THÉORIE DES BLACK SWANS — NASSIM NICHOLAS TALEB
Un Black Swan a 3 caractéristiques :
1. IMPRÉVISIBILITÉ : personne ne l'anticipe avant qu'il arrive
2. IMPACT EXTRÊME : son effet est disproportionné (positif ou négatif)
3. RÉTROSPECTIVE : après coup, tout le monde trouve une explication évidente

Exemples historiques : crise 2008, COVID-19, faillite d'Enron, émergence de ChatGPT.

## ANTIFRAGILITÉ (concept central de Taleb)
- FRAGILE : se casse sous le stress (verre)
- ROBUSTE : résiste au stress (roche)
- ANTIFRAGILE : BÉNÉFICIE du stress (muscle qui se renforce à l'effort)
Objectif Caelum : construire un système ANTIFRAGILE — les crises le renforcent.

## STRATÉGIE BARBELL (Taleb)
Ne jamais être au milieu — être aux deux extrêmes :
- 90% du capital en SÉCURITÉ MAXIMALE (zéro risque, actifs stables)
- 10% en PARIS ASYMÉTRIQUES (perte maximale = 10%, gain potentiel = infini)
Exemple Caelum : 90% des revenus viennent de services stables récurrents,
10% sont investis dans des paris à fort upside (partenariat UE, formation en ligne, IP licensing)

## VULNÉRABILITÉS SPÉCIFIQUES CAELUM PARTNERS
- Fondateur unique : si Chaima est indisponible → zéro livraison
- API unique : si Gemini coupe l'accès → zéro production
- Zéro client au lancement : zéro résilience financière
- Dépendance ONEM : si allocations coupées → problème de trésorerie personnelle
- Réputation naissante : une seule mauvaise expérience client peut tout détruire

## MATRICE RISQUES EXTRÊMES (Probabilité × Impact)
- TRÈS PROBABLE + FAIBLE IMPACT → gérer normalement (client mécontent)
- TRÈS PROBABLE + FORT IMPACT → priorité absolue (pas de client = priorité #1)
- FAIBLE PROBABILITÉ + FORT IMPACT → ZONE BLACK SWAN (Google coupe Gemini, loi IA UE)
- FAIBLE PROBABILITÉ + FAIBLE IMPACT → ignorer

## FORMAT DE SORTIE OBLIGATOIRE
1. CARTOGRAPHIE DES RISQUES EXTRÊMES : matrice probabilité × impact
2. SIMULATION COMPLÈTE : timeline heure par heure des 48 premières heures
3. PLAN D'ANTIFRAGILITÉ : comment ce Black Swan RENFORCE Caelum
4. STRATÉGIE BARBELL : actifs sûrs + paris asymétriques
5. SCORE DE ROBUSTESSE AVANT/APRÈS défenses pré-positionnées"""


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
    os.makedirs("fichiers/black_swan", exist_ok=True)
    fichier = f"fichiers/black_swan/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def cartographier_risques_extremes():
    r = streamer(
        """Cartographie complète des risques extrêmes (Black Swans) pour Caelum Partners.

MATRICE DE RISQUES EXTRÊMES — 4 quadrants :

QUADRANT 1 — PROBABLE + FORT IMPACT (gérer en priorité) :
- Zéro client pendant 3 mois : probabilité 40%, impact : effondrement moral + trésorerie
- Concurrent IA belgique bien financé : probabilité 60%, impact : pression tarifaire
- Chaima malade 2 semaines : probabilité 30%, impact : livraisons bloquées

QUADRANT 2 — IMPROBABLE + FORT IMPACT = ZONE BLACK SWAN :
- Google coupe l'API Gemini sans préavis
- Régulation UE IA Act rend certains services illégaux
- Fuite de données clients massives (cyberattaque)
- Chaima victime d'accident grave 6+ mois
- Récession économique belge (PME coupent les budgets IA)
- Concurrent technologique offre gratuitement tous les services de Caelum (ex: ChatGPT Enterprise)

QUADRANT 3 — PROBABLE + FAIBLE IMPACT (gérer normalement) :
- Client insatisfait demande remboursement
- Bug technique dans un agent IA
- Retard de paiement d'un client

QUADRANT 4 — IMPROBABLE + FAIBLE IMPACT (ignorer) :
- Panne internet 1 heure
- Erreur dans une facture
- Critique négative isolée sur LinkedIn

POUR CHAQUE BLACK SWAN (Quadrant 2) :
- Probabilité estimée sur 12 mois (%)
- Impact financier direct (€ perdus)
- Impact indirect (réputation, pipeline, moral)
- Signal précurseur à surveiller (early warning)
- Défense pré-positionnée (à mettre en place AVANT l'événement)

SCORE GLOBAL DE VULNÉRABILITÉ DE CAELUM /100 avec plan de renforcement prioritaire.""",
        "CARTOGRAPHIE RISQUES EXTRÊMES — Black Swans Caelum Partners"
    )
    sauvegarder("cartographie_risques_extremes", r)


def simuler_scenario_catastrophe():
    scenario = input("\n  Décris le scénario catastrophe à simuler → ").strip()
    if not scenario:
        return
    r = streamer(
        f"""SIMULATION BLACK SWAN COMPLÈTE — Scénario : {scenario}

TIMELINE DE L'ÉVÉNEMENT :

HEURE 0 — DÉCLENCHEMENT :
- Description précise de l'événement
- Premier signal (comment Chaima l'apprend-elle ?)
- Réaction instinctive vs réaction optimale

HEURES 0-6 — CRISE IMMÉDIATE :
- Impact sur les livraisons en cours
- Impact sur les prospects/clients en pipeline
- Impact sur la trésorerie (immédiat)
- Action prioritaire dans la première heure

HEURES 6-24 — GESTION DE CRISE :
- Communication clients (que dire, comment le dire)
- Solutions alternatives activées
- Partenaires / ressources mobilisés
- Impact financier calculé (€ perdus dans les 24h)

JOURS 2-7 — STABILISATION :
- Plan de reprise minimale des opérations
- Révision des engagements clients
- Impact sur le pipeline de nouveaux clients
- Mesure de l'impact total sur 7 jours

SEMAINES 2-4 — RECONSTRUCTION :
- Plan de reconstruction complet
- Ce qui a été perdu définitivement vs ce qui est récupérable
- Opportunités créées par ce Black Swan (antifragilité)

LONG TERME — ANTIFRAGILITÉ :
- Comment ce scénario RENFORCE Caelum si bien géré ?
- Mesures permanentes pour que ce scénario ne détruise plus jamais Caelum
- Score de résilience AVANT et APRÈS ce scénario géré""",
        f"SIMULATION BLACK SWAN — {scenario[:45]}"
    )
    sauvegarder(f"simulation_{scenario[:30].replace(' ', '_')}", r)


def concevoir_antifragilite():
    r = streamer(
        """Conçois le système d'antifragilité de Caelum Partners — comment les crises renforcent l'empire.

PRINCIPES D'ANTIFRAGILITÉ APPLIQUÉS À CAELUM :

1. PRINCIPE DE LA REDONDANCE INTELLIGENTE :
   - Multi-API : Gemini + Claude + GPT-4 (basculement automatique en cas de panne)
   - Multi-canal de prospection : LinkedIn + événements + ASBL + partenaires
   - Multi-formats de service : présentiel + distanciel + asynchrone

2. PRINCIPE DES OPTIONS (optionalité de Taleb) :
   - Garder un maximum d'options ouvertes → ne jamais se verrouiller dans un seul choix
   - Exemples pour Caelum : plusieurs structures légales possibles, plusieurs marchés cibles
   - Comment créer des options gratuites qui peuvent valoir très cher

3. PRINCIPE DU SKIN IN THE GAME :
   - Chaima porte le risque ET le bénéfice → alignement parfait (vs salarié sans risque)
   - Comment utiliser ce positionnement comme argument de vente (vs agences traditionnelles)

4. TRANSFORMER CHAQUE CRISE EN OPPORTUNITÉ :
   - COVID (hypothétique) : les PME ont eu besoin de digitalisation urgente → Caelum en profite
   - Gemini coupe l'API : Caelum maîtrise 3 autres IA → devient plus robuste que la concurrence
   - Client insatisfait : retour d'expérience → amélioration du service → futur meilleur

5. BÂTIR UN SYSTÈME QUI S'AMÉLIORE SOUS LE STRESS :
   - Chaque client difficile → agent IA amélioré qui gère ce cas
   - Chaque crise → nouveau SOP (procédure) dans le playbook
   - Chaque concurrent → analyse → différenciation renforcée

PLAN DE CONSTRUCTION DE L'ANTIFRAGILITÉ SUR 6 MOIS :
- Mois 1-2 : redondances techniques
- Mois 3-4 : redondances commerciales
- Mois 5-6 : redondances financières et légales""",
        "ANTIFRAGILITÉ — Construire un système qui se renforce sous le stress"
    )
    sauvegarder("antifragilite", r)


def plan_barbell():
    r = streamer(
        """Conçois la stratégie Barbell de Caelum Partners — sécurité maximale + paris asymétriques.

STRATÉGIE BARBELL APPLIQUÉE À CAELUM :

═══════════════════════════════════════
BARRE GAUCHE — 90% EN SÉCURITÉ MAXIMALE
═══════════════════════════════════════
REVENUS STABLES ET PRÉVISIBLES :
1. Abonnements mensuels récurrents (maintenance, support, mises à jour agents)
   → Cible : 10 clients × 300€/mois = 3 000€/mois récurrents
2. Services à prix fixe avec acompte 50% (risque quasi nul)
3. Contrats long terme (6 mois, 12 mois) avec paiement mensuel
4. Diversification géographique : pas plus de 30% du CA dans un seul client

PROTECTION DU CAPITAL PERSONNEL :
- Allocations ONEM : maintenir ce filet de sécurité tant que légalement possible
- Épargne de précaution : 3 mois de charges personnelles en réserve
- Aucune dette pour financer l'activité (bootstrap total)

═══════════════════════════════════════
BARRE DROITE — 10% EN PARIS ASYMÉTRIQUES
═══════════════════════════════════════
PARIS À FORT UPSIDE (perte max = temps investi, gain = x100) :
1. Formation en ligne "IA pour PME belges" : 0€ de coût variable, potentiel 50 000€/an
2. Partenariat avec institution européenne (Commission UE, EIB) : accès à des marchés énormes
3. Licencing de l'écosystème 50 agents à d'autres consultants (modèle franchise)
4. Produit SaaS basé sur les agents Caelum (récurrent automatique)
5. Livre/ebook "L'IA pour les PME belges" : crédibilité × revenus passifs

RÈGLES DU BARBELL :
- Jamais de risque modéré (c'est la zone de destruction de valeur)
- Si un investissement dépasse 10% du capital → abandonner ou réduire
- Chaque pari asymétrique doit avoir une limite de perte clairement définie

CALENDRIER DE MISE EN PLACE :
- Mois 1-3 : construire la barre de sécurité (abonnements, contrats)
- Mois 4-6 : lancer le premier pari asymétrique (formation ou licensing)
- Mois 7-12 : évaluer les paris, doubler sur ceux qui montrent des signaux positifs""",
        "STRATÉGIE BARBELL — Sécurité maximale + Paris asymétriques"
    )
    sauvegarder("plan_barbell", r)


def tester_robustesse_plan():
    plan = input("\n  Décris le plan à tester → ").strip()
    if not plan:
        return
    r = streamer(
        f"""Test de robustesse contre 10 Black Swans — Plan : {plan}

Soumettre ce plan à 10 scénarios Black Swan successifs :

BLACK SWAN 1 — TECHNOLOGIQUE :
Google coupe l'accès à l'API Gemini. Comment ce plan survit-il ?

BLACK SWAN 2 — HUMAIN :
Chaima est hospitalisée 6 semaines. Comment ce plan survit-il ?

BLACK SWAN 3 — RÉGLEMENTAIRE :
L'UE IA Act interdit les services IA sans certification coûteuse. Comment ce plan survit-il ?

BLACK SWAN 4 — CONCURRENTIEL :
ChatGPT Enterprise offre gratuitement tous les services de Caelum. Comment ce plan survit-il ?

BLACK SWAN 5 — ÉCONOMIQUE :
Récession belge profonde. Les PME coupent 80% de leurs budgets IA. Comment ce plan survit-il ?

BLACK SWAN 6 — SÉCURITÉ :
Cyberattaque : données de tous les clients Caelum publiées en ligne. Comment ce plan survit-il ?

BLACK SWAN 7 — LÉGAL :
L'ONEM réclame le remboursement de 12 mois d'allocations + pénalités. Comment ce plan survit-il ?

BLACK SWAN 8 — RÉPUTATION :
Un client influent publie un retour catastrophique viral (10 000 vues). Comment ce plan survit-il ?

BLACK SWAN 9 — FINANCIER :
Belfius gèle le compte bancaire de Caelum 30 jours pour vérification anti-blanchiment. Comment survit-il ?

BLACK SWAN 10 — POSITIF (choc positif) :
Article dans L'Echo génère 500 demandes en 48h. Comment ce plan absorbe-t-il le succès soudain ?

POUR CHAQUE SCÉNARIO : survie (oui/non), dommages estimés, adaptation requise.
SCORE DE ROBUSTESSE GLOBAL /100 avec recommandations de renforcement.""",
        f"TEST ROBUSTESSE — {plan[:40]}"
    )
    sauvegarder("test_robustesse", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  SIMULATEUR BLACK SWAN — Caelum Partners")
    print("  Antifragilité · Barbell · Défenses pré-positionnées")
    print("═"*65)

    while True:
        print("\n  1. Cartographier les risques extrêmes")
        print("  2. Simuler un scénario catastrophe")
        print("  3. Concevoir l'antifragilité de Caelum")
        print("  4. Plan Barbell (sécurité + paris asymétriques)")
        print("  5. Tester la robustesse d'un plan contre 10 Black Swans")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            cartographier_risques_extremes()
        elif choix == "2":
            simuler_scenario_catastrophe()
        elif choix == "3":
            concevoir_antifragilite()
        elif choix == "4":
            plan_barbell()
        elif choix == "5":
            tester_robustesse_plan()
        else:
            print("  Choix invalide.")
