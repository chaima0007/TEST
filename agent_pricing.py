"""
AGENT PRICING — AgentClaude Solutions
Optimisation intelligente des prix pour ne plus perdre de deals.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

import google.generativeai as genai

from memoire import (
    charger_memoire,
    ajouter_interaction,
    incrementer_stat,
    obtenir_contexte_client,
)

# ── Configuration ────────────────────────────────────────────────────────────
MODEL = "gemini-2.0-flash"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

DOSSIER_SORTIE = Path("fichiers/pricing")
DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)


# ── Utilitaires ──────────────────────────────────────────────────────────────

def sauvegarder_fichier(nom_fichier: str, contenu: str) -> Path:
    chemin = DOSSIER_SORTIE / nom_fichier
    chemin.write_text(contenu, encoding="utf-8")
    print(f"\n  Fichier sauvegardé : {chemin}")
    return chemin


def streamer(prompt: str, system_prompt: str = "") -> str:
    """Appel Gemini avec streaming, retourne le texte complet."""
    messages = []
    if system_prompt:
        messages.append({"role": "user", "parts": [system_prompt]})
        messages.append({"role": "model", "parts": ["Compris. Je suis prêt."]})
    messages.append({"role": "user", "parts": [prompt]})

    model = genai.GenerativeModel(MODEL)
    print()
    texte_complet = ""
    try:
        reponse = model.generate_content(
            messages,
            stream=True,
            generation_config=genai.GenerationConfig(temperature=0.7),
        )
        for chunk in reponse:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                texte_complet += chunk.text
    except Exception as e:
        print(f"\n  Erreur API : {e}")
    print()
    return texte_complet


# ── Agent 1 : Calculer le prix optimal ───────────────────────────────────────

def agent_calculer_prix(
    type_projet: str,
    complexite: str,
    delai: str,
    client_secteur: str,
) -> str:
    """
    Calcule un prix optimal pour un projet.

    type_projet  : agent sur mesure | migration | audit | formation | orchestrateur
    complexite   : simple | moyen | complexe | enterprise
    delai        : normal | urgent | très urgent
    client_secteur: startup | PME | ETI | grand compte
    """
    incrementer_stat("agent_calculer_prix")

    system_prompt = """Tu es l'expert pricing d'AgentClaude Solutions, une société spécialisée
en déploiement d'agents IA sur mesure (LLM, automation, orchestration multi-agents).
Tu connais parfaitement les tarifs du marché français et européen pour ce type de prestations.
Tu raisonnes en euros HT. Tu es direct, précis et justifies chaque recommandation."""

    prompt = f"""Calcule le prix optimal pour ce projet IA :

TYPE DE PROJET  : {type_projet}
COMPLEXITÉ      : {complexite}
DÉLAI           : {delai}
SECTEUR CLIENT  : {client_secteur}

Fournis une analyse structurée avec EXACTEMENT ces sections :

## 1. PRIX RECOMMANDÉ
Un chiffre précis en € HT.

## 2. FOURCHETTE (min / max)
Prix minimum acceptable et prix maximum justifiable.

## 3. JUSTIFICATION
Pourquoi ce prix est juste : charge estimée (jours/homme), expertise requise, valeur délivrée.

## 4. COMPARAISON MARCHÉ
Où se situent les concurrents (freelances, ESN, pure players IA) sur ce type de projet.

## 5. STRUCTURE DE PAIEMENT RECOMMANDÉE
Détailler : acompte 30 % + jalons (avec montants et conditions de déclenchement).

## 6. RISQUES PRICING
Ce qui pourrait justifier de monter ou descendre le prix."""

    print(f"\n{'='*60}")
    print(f"  CALCUL PRIX — {type_projet.upper()} | {complexite} | {delai}")
    print(f"{'='*60}")

    resultat = streamer(prompt, system_prompt)

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"prix_{type_projet.replace(' ', '_')}_{complexite}_{horodatage}.txt"
    contenu = f"""RAPPORT PRICING — AgentClaude Solutions
Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}

Type de projet : {type_projet}
Complexité     : {complexite}
Délai          : {delai}
Secteur client : {client_secteur}

{'='*60}

{resultat}
"""
    sauvegarder_fichier(nom_fichier, contenu)
    return resultat


# ── Agent 2 : Préparer la négociation ────────────────────────────────────────

def agent_negociation(
    prix_propose: str,
    objection_client: str,
    contexte: str,
) -> str:
    """
    Prépare une stratégie de négociation face aux objections client.

    prix_propose    : prix initial proposé (ex: "8 500 €")
    objection_client: l'objection exacte du client
    contexte        : contexte du deal (secteur, taille client, enjeux)
    """
    incrementer_stat("agent_negociation")

    system_prompt = """Tu es un consultant senior en vente de services IA pour AgentClaude Solutions.
Tu maîtrises les techniques de négociation B2B, notamment pour les services technologiques premium.
Tu aides à défendre les prix tout en préservant la relation client.
Tu raisonnes en euros HT. Ton ton est professionnel et stratégique."""

    prompt = f"""Notre client a répondu à notre proposition commerciale. Aide-moi à préparer la négociation.

PRIX PROPOSÉ    : {prix_propose}
OBJECTION CLIENT: "{objection_client}"
CONTEXTE        : {contexte}

Prépare une stratégie complète avec EXACTEMENT ces sections :

## 1. ANALYSE DE L'OBJECTION
Quelle est la vraie nature de cette objection (budget réel, comparaison, tactique de négociation) ?
Quelle est la probabilité que ce soit un vrai blocage vs une tactique ?

## 2. CONTRE-ARGUMENTS CLÉS
3 à 5 arguments béton pour défendre notre prix, avec des formulations précises à utiliser.

## 3. STRATÉGIE DE CONCESSION
Ce qu'on peut céder (et dans quel ordre) vs ce qu'on ne cède PAS.
Pour chaque concession possible : ce qu'on demande en échange.

## 4. PROPOSITIONS ALTERNATIVES
Minimum 3 alternatives créatives (réduction périmètre, paiement échelonné, valeur ajoutée...).

## 5. POINT DE RUPTURE (WALK-AWAY)
En dessous de quel prix on refuse le deal, et pourquoi.
Comment annoncer un refus avec élégance sans brûler la relation.

## 6. SCRIPT DE RÉPONSE
Un email ou une ouverture de réunion mot à mot pour répondre à cette objection."""

    print(f"\n{'='*60}")
    print(f"  STRATÉGIE NÉGOCIATION — Objection : \"{objection_client[:40]}...\"")
    print(f"{'='*60}")

    resultat = streamer(prompt, system_prompt)

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"negociation_{horodatage}.txt"
    contenu = f"""STRATÉGIE DE NÉGOCIATION — AgentClaude Solutions
Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}

Prix proposé    : {prix_propose}
Objection client: {objection_client}
Contexte        : {contexte}

{'='*60}

{resultat}
"""
    sauvegarder_fichier(nom_fichier, contenu)
    return resultat


# ── Agent 3 : Grille tarifaire complète ──────────────────────────────────────

def agent_grille_tarifaire() -> str:
    """
    Génère une grille tarifaire complète pour tous les services d'AgentClaude Solutions.
    """
    incrementer_stat("agent_grille_tarifaire")

    system_prompt = """Tu es le directeur commercial d'AgentClaude Solutions, expert en structuration
tarifaire pour des services IA B2B en France.
Tu crées des grilles tarifaires professionnelles, claires et compétitives.
Tu penses en termes de valeur perçue, de segmentation client et de récurrence.
Toutes les grilles sont en euros HT."""

    prompt = """Génère la grille tarifaire complète d'AgentClaude Solutions pour 2025.

Nos lignes de services :
- Agents IA sur mesure (développement)
- Migration systèmes vers IA
- Audit & conseil IA
- Formations IA
- Orchestrateurs multi-agents

Pour chaque ligne de service, crée :

## SERVICE : [Nom du service]

### Tiers Starter / Pro / Enterprise
Pour chaque tier : description, ce qui est inclus, prix (one-shot ET récurrent si applicable).

### Tarification One-Shot vs Récurrent
Avantages de chaque modèle, quand proposer lequel.

### Remises Volume
Grille de remises selon le volume ou la durée d'engagement.

### Tarifs Partenaires / Revendeurs
Commission ou remise pour les apporteurs d'affaires et revendeurs.

---

Ensuite fournis :

## CALCULATEUR ROI CLIENT (Template)
Un template simple que le commercial peut remplir avec le client pour démontrer le ROI.

## RÈGLES DE REMISE
Ce qui autorise une remise et jusqu'à quel niveau (sans validation direction vs avec)."""

    print(f"\n{'='*60}")
    print(f"  GÉNÉRATION GRILLE TARIFAIRE COMPLÈTE")
    print(f"{'='*60}")

    resultat = streamer(prompt, system_prompt)

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"grille_tarifaire_{horodatage}.txt"
    contenu = f"""GRILLE TARIFAIRE OFFICIELLE — AgentClaude Solutions
Générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
Version : {horodatage}

USAGE INTERNE — NE PAS DIFFUSER SANS VALIDATION DIRECTION

{'='*60}

{resultat}
"""
    sauvegarder_fichier(nom_fichier, contenu)
    return resultat


# ── Agent 4 : Benchmark concurrents ──────────────────────────────────────────

def agent_benchmark_prix(concurrent: str, service: str) -> str:
    """
    Analyse concurrentielle des prix du marché IA.

    concurrent : nom du concurrent (ou "marché" pour une vision globale)
    service    : le service à analyser
    """
    incrementer_stat("agent_benchmark_prix")

    system_prompt = """Tu es un analyste marché spécialisé dans les services IA en France et Europe.
Tu as une connaissance approfondie des acteurs du marché : freelances IA, ESN (Capgemini, Sopra, Accenture...),
pure players IA (Arago, Ingedata, Iguane Solutions...) et plateformes SaaS IA.
Tu aides AgentClaude Solutions à se positionner stratégiquement.
Toutes les estimations sont en euros HT. Tu précises toujours l'incertitude de tes estimations."""

    prompt = f"""Analyse concurrentielle des prix pour : {service}
Concurrent analysé : {concurrent}

Fournis une analyse complète avec EXACTEMENT ces sections :

## 1. ESTIMATION TARIFAIRE DU CONCURRENT
Fourchette de prix probable pour ce service chez {concurrent}.
Méthodologie de calcul / sources d'information.

## 2. MODÈLE COMMERCIAL
Comment ce concurrent structure ses offres (one-shot, abonnement, success fees...).
Ce qui est inclus / exclu dans leur prix affiché.

## 3. CARTOGRAPHIE DU MARCHÉ
Positionnement des principaux acteurs sur une matrice Prix / Valeur :
- Les low-cost (< X €)
- Le milieu de gamme (X à Y €)
- Le premium (> Y €)

## 4. GAPS ET OPPORTUNITÉS
Où est le marché sous-servi ?
Quels segments sont sur-tarifés par les concurrents ?
Quels segments sont sous-exploités ?

## 5. RECOMMANDATION POSITIONNEMENT
Pour AgentClaude Solutions sur ce service :
- Où se positionner par rapport à {concurrent} (premium, parité, challenger) ?
- Arguments de différenciation à mettre en avant
- Zones où être moins cher et pourquoi
- Zones où être plus cher et pourquoi

## 6. VEILLE CONCURRENTIELLE
Signaux à surveiller pour détecter un changement de stratégie prix du marché."""

    print(f"\n{'='*60}")
    print(f"  BENCHMARK PRIX — {concurrent} | {service}")
    print(f"{'='*60}")

    resultat = streamer(prompt, system_prompt)

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"benchmark_{concurrent.replace(' ', '_')}_{horodatage}.txt"
    contenu = f"""BENCHMARK CONCURRENTIEL — AgentClaude Solutions
Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}

Concurrent analysé : {concurrent}
Service            : {service}

{'='*60}

{resultat}
"""
    sauvegarder_fichier(nom_fichier, contenu)
    return resultat


# ── Agent 5 : Proposition de valeur ROI ──────────────────────────────────────

def agent_proposition_valeur(
    client: str,
    probleme: str,
    solution_proposee: str,
) -> str:
    """
    Construit un business case ROI pour convaincre la direction client.

    client            : nom/description du client
    probleme          : problème métier actuel du client
    solution_proposee : ce qu'AgentClaude Solutions propose de faire
    """
    incrementer_stat("agent_proposition_valeur")

    # Récupère contexte mémoire si client connu
    contexte_client = obtenir_contexte_client(client)

    system_prompt = """Tu es un consultant business value d'AgentClaude Solutions.
Tu excelles à quantifier la valeur des solutions IA et à construire des business cases
que les DSI, DAF et dirigeants peuvent défendre en CODIR.
Tu penses en €, en temps gagné, en risques évités et en avantages compétitifs.
Tu es pragmatique et utilises des hypothèses conservatrices et défendables."""

    prompt = f"""Construis un business case ROI complet pour convaincre la direction de ce client.

CLIENT           : {client}
CONTEXTE CONNU   : {contexte_client}
PROBLÈME ACTUEL  : {probleme}
SOLUTION PROPOSÉE: {solution_proposee}

Crée un document de business case avec EXACTEMENT ces sections :

## RÉSUMÉ EXÉCUTIF (1 page)
Synthèse pour le CODIR : problème, solution, ROI attendu, recommandation.

## 1. QUANTIFICATION DU PROBLÈME ACTUEL
Évalue le coût actuel du problème :
- Temps perdu (heures × coût horaire moyen)
- Erreurs et reprises (coût estimé)
- Opportunités manquées
- Risques non couverts
TOTAL : coût annuel estimé du problème (avec hypothèses explicites)

## 2. CALCUL DU ROI DE LA SOLUTION
Pour notre investissement de [X €] :
- Gains directs (temps récupéré, erreurs évitées)
- Gains indirects (satisfaction client, scalabilité, avantage compétitif)
- Tableau ROI sur 1 an / 2 ans / 3 ans
- Délai de retour sur investissement (payback period)

## 3. SCÉNARIOS
Scénario pessimiste / réaliste / optimiste avec probabilités.

## 4. RISQUES DE NE PAS AGIR
Ce qui se passe si le client ne fait rien dans 6 mois, 1 an, 2 ans.
Concurrents qui adoptent déjà ce type de solution.

## 5. PLAN DE MISE EN ŒUVRE
Timeline réaliste avec jalons et livrables mesurables.
Métriques de succès proposées (KPIs).

## 6. PROCHAINES ÉTAPES
Actions concrètes à valider lors de la prochaine réunion.
Ce que le client doit nous fournir pour démarrer."""

    print(f"\n{'='*60}")
    print(f"  BUSINESS CASE ROI — {client}")
    print(f"{'='*60}")

    resultat = streamer(prompt, system_prompt)

    # Mémoriser l'interaction
    ajouter_interaction(
        client,
        "business_case_roi",
        f"Business case généré pour : {solution_proposee[:100]}",
    )

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_client = client.replace(" ", "_").replace("/", "-")
    nom_fichier = f"business_case_{nom_client}_{horodatage}.txt"
    contenu = f"""BUSINESS CASE ROI — AgentClaude Solutions
Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}

Client            : {client}
Problème          : {probleme}
Solution proposée : {solution_proposee}

{'='*60}

{resultat}
"""
    sauvegarder_fichier(nom_fichier, contenu)
    return resultat


# ── Menu principal ────────────────────────────────────────────────────────────

def afficher_menu():
    print(f"""
{'═'*60}
  AGENT PRICING — AgentClaude Solutions
  Optimisez vos prix, gagnez plus de deals
{'═'*60}

  1. Calculer le prix optimal d'un projet
  2. Préparer une négociation (répondre aux objections)
  3. Générer la grille tarifaire complète
  4. Benchmark concurrentiel des prix
  5. Construire un business case ROI client

  0. Quitter
{'═'*60}""")


def saisir_choix(prompt: str, options: list[str]) -> str:
    """Affiche les options et retourne le choix de l'utilisateur."""
    print(f"\n  {prompt}")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    while True:
        try:
            val = int(input("  Votre choix (numéro) : ").strip())
            if 1 <= val <= len(options):
                return options[val - 1]
        except (ValueError, KeyboardInterrupt):
            pass
        print("  Choix invalide, recommencez.")


def run_agent_1():
    print("\n  — CALCULER LE PRIX OPTIMAL D'UN PROJET —\n")
    type_projet = saisir_choix(
        "Type de projet :",
        ["agent sur mesure", "migration", "audit", "formation", "orchestrateur"],
    )
    complexite = saisir_choix(
        "Complexité :",
        ["simple", "moyen", "complexe", "enterprise"],
    )
    delai = saisir_choix(
        "Délai :",
        ["normal", "urgent", "très urgent"],
    )
    secteur = saisir_choix(
        "Secteur client :",
        ["startup", "PME", "ETI", "grand compte"],
    )
    agent_calculer_prix(type_projet, complexite, delai, secteur)


def run_agent_2():
    print("\n  — PRÉPARER UNE NÉGOCIATION —\n")
    prix = input("  Prix proposé au client (ex: 12 000 €) : ").strip()
    print("\n  Objections courantes :")
    print("    1. C'est trop cher")
    print("    2. J'ai une meilleure offre d'un concurrent")
    print("    3. On n'a pas le budget cette année")
    print("    4. Saisir une objection personnalisée")
    choix_obj = input("  Votre choix (1-4) : ").strip()

    objections_type = {
        "1": "C'est trop cher, vous êtes au-dessus de notre budget",
        "2": "J'ai une meilleure offre d'un concurrent à un prix inférieur",
        "3": "On n'a pas le budget cette année, peut-être l'année prochaine",
    }
    if choix_obj in objections_type:
        objection = objections_type[choix_obj]
    else:
        objection = input("  Objection du client (verbatim) : ").strip()

    contexte = input("  Contexte du deal (secteur, taille client, enjeux) : ").strip()
    if not contexte:
        contexte = "PME française, premier contact avec les solutions IA"
    agent_negociation(prix, objection, contexte)


def run_agent_3():
    print("\n  — GÉNÉRER LA GRILLE TARIFAIRE COMPLÈTE —\n")
    print("  Génération en cours... Cela peut prendre quelques instants.")
    agent_grille_tarifaire()


def run_agent_4():
    print("\n  — BENCHMARK CONCURRENTIEL —\n")
    concurrent = input("  Nom du concurrent (ou 'marché' pour vue globale) : ").strip()
    if not concurrent:
        concurrent = "marché"
    service = saisir_choix(
        "Service à analyser :",
        [
            "agent IA sur mesure",
            "migration legacy vers IA",
            "audit IA",
            "formation IA",
            "orchestrateur multi-agents",
        ],
    )
    agent_benchmark_prix(concurrent, service)


def run_agent_5():
    print("\n  — BUSINESS CASE ROI CLIENT —\n")
    client = input("  Nom du client : ").strip()
    if not client:
        client = "Client prospect"
    probleme = input("  Problème métier actuel (décrivez la situation) : ").strip()
    if not probleme:
        probleme = "Processus manuels chronophages et sources d'erreurs"
    solution = input("  Solution proposée par AgentClaude Solutions : ").strip()
    if not solution:
        solution = "Agent IA pour automatiser et optimiser les processus métier"
    agent_proposition_valeur(client, probleme, solution)


def main():
    if "GEMINI_API_KEY" not in os.environ:
        print("  ERREUR : La variable d'environnement GEMINI_API_KEY n'est pas définie.")
        sys.exit(1)

    print(f"\n  Modèle : {MODEL}")
    print(f"  Dossier de sortie : {DOSSIER_SORTIE.resolve()}")

    while True:
        afficher_menu()
        try:
            choix = input("  Votre choix : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Au revoir !")
            break

        if choix == "0":
            print("\n  Au revoir !")
            break
        elif choix == "1":
            run_agent_1()
        elif choix == "2":
            run_agent_2()
        elif choix == "3":
            run_agent_3()
        elif choix == "4":
            run_agent_4()
        elif choix == "5":
            run_agent_5()
        else:
            print("\n  Choix invalide. Entrez un chiffre entre 0 et 5.")

        input("\n  Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
