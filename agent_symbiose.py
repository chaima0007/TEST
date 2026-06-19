"""
ORCHESTRATEUR DE SYMBIOSE — Maximiser les synergies entre tous les agents de la flotte Caelum
Systèmes · Émergence · Feedback loops · La somme dépasse les parties

Usage : python agent_symbiose.py
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

IDENTITE = """# ORCHESTRATEUR DE SYMBIOSE — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es l'Orchestrateur de Symbiose de Caelum Partners.
Ta mission : maximiser les synergies entre tous les agents de la flotte Caelum,
faire en sorte qu'ils se renforcent mutuellement, partagent les données,
évitent les redondances et créent des capacités émergentes.
La somme du système doit être SUPÉRIEURE à la somme de ses parties.

## PENSÉE SYSTÉMIQUE — FONDEMENTS THÉORIQUES

### BOUCLES DE RÉTROACTION (Peter Senge, "La Cinquième Discipline")
- BOUCLE RENFORÇANTE (R) : amplifie le changement (croissance ou effondrement)
  Exemple Caelum : plus de clients → plus de données → meilleurs agents → plus de clients
- BOUCLE D'ÉQUILIBRAGE (E) : maintient la stabilité (résistance au changement)
  Exemple : plus de projets → plus de charge Chaima → moins de qualité → moins de clients

### THÉORIE DE L'ÉMERGENCE
Des propriétés émergent d'un système complexe qui n'existent dans aucun composant seul.
Exemple : aucune molécule d'eau n'est "liquide" — la liquidité émerge de leur interaction.
Chez Caelum : aucun agent seul ne peut faire le travail d'un cabinet de conseil,
mais l'écosystème des 50 agents ensemble crée cette capacité émergente.

## ARCHITECTURE DE LA FLOTTE CAELUM (50+ agents)
Groupes d'agents par fonction :

GROUPE COMMERCIAL :
- agent_commercial.py → agent_email.py → agent_crm.py → agent_facturation.py
- Flux : prospect → email → CRM → contrat → facture

GROUPE STRATÉGIQUE :
- agent_strategie.py → agent_oracle.py → agent_empire.py → agent_titan.py
- Flux : analyse → prévision → stratégie → exécution

GROUPE FINANCIER :
- agent_flux_economique.py → agent_maitre_velocite.py → agent_comptable_belge.py → agent_kpi.py
- Flux : vélocité → optimisation → conformité → mesure

GROUPE RÉSILIENCE :
- agent_red_team.py → agent_simulateur_black_swan.py → agent_watchdog.py
- Flux : stress test → simulation → monitoring continu

GROUPE CONNAISSANCE :
- agent_memoire_session.py → agent_memoire_collective.py → agent_gardien_playbook.py
- Flux : session → mémoire long terme → playbook institutionnel

## PATTERNS D'ORCHESTRATION ENTRE AGENTS
1. SÉQUENTIEL : A → B → C (output de A = input de B)
2. PARALLÈLE : A + B + C simultanément → agrégation des résultats
3. CONDITIONNEL : si résultat A = X alors → B, sinon → C
4. FEEDBACK : résultat de C améliore les inputs de A

## FORMAT DE SORTIE OBLIGATOIRE
1. CARTE DE SYNERGIES : toutes les connexions agent-agent avec type et valeur
2. WORKFLOWS CHAÎNÉS : séquences optimales pour chaque objectif business
3. REDONDANCES IDENTIFIÉES : agents en doublon ou en conflit
4. FLUX DE DONNÉES OPTIMAL : format JSON partagé entre agents
5. CAPACITÉS ÉMERGENTES : ce que le système entier peut faire qu'aucun agent solo ne peut"""


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
    os.makedirs("fichiers/symbiose", exist_ok=True)
    fichier = f"fichiers/symbiose/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def cartographier_synergies():
    r = streamer(
        """Cartographie toutes les synergies possibles entre les agents de la flotte Caelum Partners.

AGENTS CONNUS DE LA FLOTTE CAELUM :
agent_commercial, agent_email, agent_crm, agent_facturation, agent_strategie,
agent_oracle, agent_empire, agent_titan, agent_flux_economique, agent_maitre_velocite,
agent_comptable_belge, agent_kpi, agent_red_team, agent_simulateur_black_swan,
agent_watchdog, agent_memoire_session, agent_memoire_collective, agent_gardien_playbook,
agent_juridique, agent_seo, agent_veille, agent_innovation, agent_data, agent_dashboard_ceo,
agent_pricing, agent_marque, agent_reputation, agent_partenariats, agent_growth

POUR CHAQUE PAIRE D'AGENTS À FORT POTENTIEL DE SYNERGIE :
1. CONNEXION : agent A → agent B
   - Donnée partagée : (quoi ?)
   - Format recommandé : (JSON, texte, fichier)
   - Valeur créée par la connexion : (quoi que ni A ni B ne peuvent faire seuls ?)

IDENTIFIER LES BOUCLES DE RÉTROACTION RENFORÇANTES :
- Boucle 1 : [agent X] → [agent Y] → [agent Z] → améliore [agent X]
- Boucle 2 : ...
- Boucle 3 : ...

IDENTIFIER LES CAPACITÉS ÉMERGENTES :
Quand 3+ agents travaillent ensemble, quelles nouvelles capacités apparaissent ?
Exemple : commercial + email + crm + facturation = pipeline de vente automatique complet

RECOMMANDATIONS DE CONNEXION PRIORITAIRES :
Les 5 connexions à implémenter cette semaine pour un impact maximum.""",
        "CARTOGRAPHIE SYNERGIES — Flotte complète Caelum Partners"
    )
    sauvegarder("cartographie_synergies", r)


def concevoir_workflow_chaine():
    objectif = input("\n  Quel est l'objectif business à atteindre ? → ").strip()
    if not objectif:
        return
    r = streamer(
        f"""Conçois le workflow optimal d'agents chaînés pour atteindre cet objectif.
Objectif : {objectif}

ANALYSE DE L'OBJECTIF :
1. Quelles informations sont nécessaires pour atteindre cet objectif ?
2. Quels agents de la flotte Caelum possèdent ces informations ou capacités ?
3. Dans quel ordre les chaîner pour un résultat optimal ?

WORKFLOW CHAÎNÉ RECOMMANDÉ :

ÉTAPE 1 — [Nom de l'agent] :
- Input requis : (données d'entrée)
- Traitement : (que fait cet agent ?)
- Output produit : (format et contenu de sa sortie)
- Durée estimée : X minutes

ÉTAPE 2 — [Nom de l'agent] :
- Input : (output de l'étape 1 + données supplémentaires)
- Traitement : ...
- Output : ...

[Continuer jusqu'à l'objectif atteint]

ÉTAPE FINALE — SYNTHÈSE :
- Comment combiner tous les outputs pour atteindre l'objectif ?
- Format du livrable final
- Qui reçoit le livrable (Chaima / client / partenaire)

ALTERNATIVES :
- Workflow alternatif si un agent est indisponible
- Workflow accéléré (si besoin urgent, quelle étape peut être sautée ?)

COMMANDES BASH pour exécuter ce workflow séquentiellement.""",
        f"WORKFLOW CHAÎNÉ — Objectif : {objectif[:40]}"
    )
    sauvegarder(f"workflow_{objectif[:25].replace(' ', '_')}", r)


def identifier_redondances():
    r = streamer(
        """Identifie toutes les redondances et conflits dans la flotte d'agents Caelum Partners.

ANALYSE DES CHEVAUCHEMENTS FONCTIONNELS :

REDONDANCES IDENTIFIÉES (agents qui font la même chose) :
1. agent_memoire_session.py vs agent_memoire_collective.py
   - Chevauchement : tous deux gèrent la mémoire → risque de données dupliquées
   - Solution : définir la responsabilité exclusive de chacun

2. agent_strategie.py vs agent_empire.py vs agent_titan.py vs agent_oracle.py
   - Chevauchement : tous font de la stratégie globale → confusion possible
   - Solution : différenciation claire des niveaux de décision

3. agent_comptable_belge.py vs agent_flux_economique.py vs agent_maitre_velocite.py
   - Chevauchement : tous s'occupent de l'argent → recommandations contradictoires ?
   - Solution : périmètre exclusif pour chacun

4. agent_red_team.py vs agent_simulateur_black_swan.py vs agent_watchdog.py
   - Chevauchement : tous font de la gestion des risques → redondance possible
   - Solution : spécialisation claire (stress-test vs simulation extrême vs monitoring)

CONFLITS POTENTIELS (agents qui donnent des recommandations contradictoires) :
- agent_croissance (croissance rapide) vs agent_red_team (prudence maximale)
- agent_pricing (prix premium) vs agent_commercial (fermer les deals)
- agent_innovation (tester de nouvelles choses) vs agent_gardien_playbook (respecter les templates)

PLAN DE RÉSOLUTION :
Pour chaque redondance : définition précise du périmètre exclusif de chaque agent
Pour chaque conflit : protocole d'arbitrage (quel agent prime dans quel contexte ?)

ARCHITECTURE CIBLE (agents sans redondance) :
Représentation en couches : données → analyse → stratégie → exécution → monitoring""",
        "IDENTIFICATION REDONDANCES — Flotte agents Caelum Partners"
    )
    sauvegarder("identification_redondances", r)


def optimiser_flux_donnees():
    r = streamer(
        """Conçois le système optimal de partage de données entre tous les agents Caelum Partners.

PROBLÈME ACTUEL :
Chaque agent travaille de façon isolée → perte d'informations entre sessions.
Objectif : créer une mémoire partagée que tous les agents peuvent lire et écrire.

ARCHITECTURE DE DONNÉES PARTAGÉES RECOMMANDÉE :

FICHIER CENTRAL : caelum_state.json
Structure recommandée :
{
  "entreprise": {
    "nom": "Caelum Partners",
    "fondatrice": "Chaima Mhadbi",
    "ca_mensuel_actuel": 0,
    "nb_clients_actifs": 0,
    "nb_prospects_pipeline": 0,
    "phase": "lancement"
  },
  "clients": [
    {"id": "C001", "nom": "...", "statut": "...", "valeur": 0, "date_debut": "..."}
  ],
  "pipeline": [
    {"id": "P001", "nom": "...", "score": 0, "etape": "...", "valeur_estimee": 0}
  ],
  "decisions": [
    {"date": "...", "decision": "...", "agent": "...", "resultat": "..."}
  ],
  "metriques": {
    "dso": 0,
    "mrr": 0,
    "churn_rate": 0,
    "nps": 0
  }
}

PROTOCOLES DE LECTURE/ÉCRITURE :
- Chaque agent LIT l'état actuel avant de répondre
- Chaque agent ÉCRIT les nouvelles informations après interaction
- Format de la mise à jour : delta JSON (pas réécriture complète)

LISTE DES FICHIERS PARTAGÉS PAR TYPE :
1. fichiers/etat_global/caelum_state.json → état temps réel
2. fichiers/clients/*.json → un fichier par client
3. fichiers/decisions/log.json → toutes les décisions loggées
4. fichiers/metriques/kpis.json → KPIs mis à jour en temps réel

PROTOCOLE D'ÉCRITURE SÉCURISÉ :
- Comment éviter les conflits d'écriture simultanée
- Comment versionner les données (pas d'écrasement sans backup)""",
        "FLUX DE DONNÉES OPTIMAL — Architecture partagée Caelum Partners"
    )
    sauvegarder("flux_donnees_optimal", r)


def audit_emergence():
    r = streamer(
        """Identifie les capacités émergentes de la flotte d'agents Caelum Partners — ce qu'aucun agent seul ne peut faire.

THÉORIE DE L'ÉMERGENCE APPLIQUÉE AUX AGENTS IA :
Une capacité émergente apparaît quand la combinaison de plusieurs agents produit
un résultat impossible pour un agent seul.

CAPACITÉS ÉMERGENTES IDENTIFIÉES :

ÉMERGENCE 1 — CABINET DE CONSEIL COMPLET :
Agents combinés : strategie + oracle + empire + titan + red_team
Capacité émergente : analyse stratégique de niveau McKinsey, impossible pour un seul agent
Comment l'activer : workflow de consultation de 2h → livrable de 50 pages

ÉMERGENCE 2 — MACHINE DE CROISSANCE AUTONOME :
Agents combinés : commercial + email + crm + growth + seo
Capacité émergente : pipeline de vente qui génère des clients sans intervention de Chaima
Comment l'activer : configuration des triggers automatiques entre agents

ÉMERGENCE 3 — INTELLIGENCE PRÉDICTIVE :
Agents combinés : data + kpi + oracle + veille + memoire_collective
Capacité émergente : prédiction des tendances marché avec 80% de précision à 3 mois
Comment l'activer : flux de données hebdomadaire entre ces 5 agents

ÉMERGENCE 4 — SYSTÈME IMMUNITAIRE LÉGAL :
Agents combinés : juridique + conformite_offensive + red_team + watchdog
Capacité émergente : détection et neutralisation automatique de tout risque légal
Comment l'activer : audit mensuel en cascade

ÉMERGENCE 5 — CAPITAL INTELLIGENCE :
Agents combinés : flux_economique + maitre_velocite + comptable_belge + kpi + dashboard_ceo
Capacité émergente : optimisation automatique de toutes les décisions financières
Comment l'activer : mise à jour quotidienne des métriques partagées

PLAN D'ACTIVATION DES ÉMERGENCES :
- Émergence prioritaire à activer cette semaine : ...
- Ressources nécessaires (temps, fichiers, configuration)
- Métriques pour mesurer que l'émergence est active et fonctionnelle""",
        "AUDIT ÉMERGENCE — Capacités systémiques de la flotte Caelum"
    )
    sauvegarder("audit_emergence", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ORCHESTRATEUR DE SYMBIOSE — Caelum Partners")
    print("  Synergies · Émergence · Flux de données · Systèmes")
    print("═"*65)

    while True:
        print("\n  1. Cartographier toutes les synergies entre agents")
        print("  2. Concevoir un workflow chaîné pour un objectif")
        print("  3. Identifier les redondances dans la flotte")
        print("  4. Optimiser le flux de données partagé")
        print("  5. Audit des capacités émergentes du système")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            cartographier_synergies()
        elif choix == "2":
            concevoir_workflow_chaine()
        elif choix == "3":
            identifier_redondances()
        elif choix == "4":
            optimiser_flux_donnees()
        elif choix == "5":
            audit_emergence()
        else:
            print("  Choix invalide.")
