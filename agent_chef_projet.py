"""
AGENT CHEF DE PROJET AUTONOME
Gère la planification, le suivi, les risques, les rétrospectives
et les rapports clients pour les projets IA d'AgentClaude Solutions.

Usage : python agent_chef_projet.py
"""

import os
import sys
import json
from datetime import datetime
import google.generativeai as genai
from memoire import (
    charger_memoire, sauvegarder_memoire, incrementer_stat, ajouter_interaction
)

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Variable d'environnement GEMINI_API_KEY manquante.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

ENTREPRISE_PROFIL = """
Nom : AgentClaude Solutions
Spécialité : Automatisation par agents IA (Claude, Gemini)
Services :
  - Agents autonomes sur mesure pour entreprises
  - Migration et modernisation de code legacy
  - Sécurité et audit IA
  - Formation équipes sur agents IA
  - Orchestrateurs autonomes clé en main
Avantage concurrentiel : Agents qui travaillent 24h/24 sans erreur humaine
Méthodologie : Agile / Scrum — sprints de 2 semaines
"""

DOSSIER_PROJETS = "fichiers/projets"


# ─── UTILITAIRES ──────────────────────────────────────────────

def creer_agent(instructions, temperature=0.5):
    """Instancie un modèle Gemini avec les instructions système données."""
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=3000,
        ),
    )


def executer_stream(model, prompt, label):
    """Exécute une requête en streaming et retourne la réponse complète."""
    print(f"\n{'─' * 62}")
    print(f"  ► {label}")
    print(f"{'─' * 62}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder_fichier(nom_projet, type_rapport, contenu):
    """Sauvegarde un rapport dans fichiers/projets/."""
    os.makedirs(DOSSIER_PROJETS, exist_ok=True)
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"{nom_projet.replace(' ', '_')}_{type_rapport}_{horodatage}.txt"
    chemin = os.path.join(DOSSIER_PROJETS, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"Projet : {nom_projet}\n")
        f.write(f"Type : {type_rapport}\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 62 + "\n\n")
        f.write(contenu)
    print(f"\n  ✅ Rapport sauvegardé → {chemin}")
    return chemin


def sauvegarder_projet_memoire(nom, donnees):
    """Enregistre ou met à jour les données d'un projet en mémoire."""
    m = charger_memoire()
    if "projets" not in m:
        m["projets"] = {}
    if nom not in m["projets"]:
        m["projets"][nom] = {
            "date_creation": datetime.now().isoformat(),
            "rapports": [],
        }
    m["projets"][nom].update(donnees)
    m["projets"][nom]["derniere_mise_a_jour"] = datetime.now().isoformat()
    sauvegarder_memoire(m)
    print(f"  ✅ Projet '{nom}' sauvegardé en mémoire.")


def obtenir_contexte_projet(nom):
    """Récupère le contexte d'un projet depuis la mémoire."""
    m = charger_memoire()
    projets = m.get("projets", {})
    if nom in projets:
        p = projets[nom]
        return (
            f"Projet : {nom} | "
            f"Objectif : {p.get('objectif', 'N/A')} | "
            f"Délai : {p.get('delai', 'N/A')} | "
            f"Budget : {p.get('budget', 'N/A')} | "
            f"Rapports générés : {len(p.get('rapports', []))}"
        )
    return "Nouveau projet — aucun historique disponible."


def lister_projets():
    """Affiche la liste des projets en mémoire."""
    m = charger_memoire()
    projets = m.get("projets", {})
    if not projets:
        print("\n  Aucun projet en mémoire.")
        return
    print(f"\n  {'NOM':<25} {'DÉLAI':<15} {'BUDGET':<15} {'MAJ'}")
    print("  " + "─" * 70)
    for nom, data in projets.items():
        maj = data.get("derniere_mise_a_jour", "")[:10]
        print(
            f"  {nom:<25} "
            f"{data.get('delai', 'N/A'):<15} "
            f"{data.get('budget', 'N/A'):<15} "
            f"{maj}"
        )


# ─── AGENTS CHEF DE PROJET ────────────────────────────────────

def agent_planifier_projet(nom, objectif, delai, budget):
    """
    Génère un plan de projet complet :
    WBS, timeline avec jalons, allocation ressources, matrice des risques,
    RACI, ventilation budgétaire, KPIs.
    """
    incrementer_stat("planifier_projet")
    contexte = obtenir_contexte_projet(nom)

    agent = creer_agent(
        f"""Tu es un Chef de Projet Senior certifié PMP, expert en projets IA.
Entreprise : {ENTREPRISE_PROFIL}

Génère un plan de projet exhaustif et professionnel comprenant :

1. **WBS (Work Breakdown Structure)**
   - Décomposition en phases, livrables et tâches
   - Numérotation hiérarchique (1.0, 1.1, 1.1.1...)

2. **Timeline avec jalons**
   - Planning semaine par semaine
   - Jalons clés (Go/No-Go, livrables majeurs, recettes)
   - Chemin critique identifié

3. **Allocation des ressources**
   - Profils nécessaires (Chef de projet, Dev IA, Data Engineer, etc.)
   - Charge en jours/homme par phase
   - Calendrier d'intervention

4. **Matrice des risques (Probabilité × Impact)**
   - Tableau avec colonnes : Risque | Probabilité (1-5) | Impact (1-5) | Score | Réponse
   - Minimum 8 risques identifiés

5. **RACI**
   - Tableau Responsable / Approuve / Consulté / Informé par livrable

6. **Ventilation budgétaire**
   - Répartition par poste (RH, infrastructure, licences, imprévus)
   - Budget consommé / budget restant par phase

7. **KPIs de suivi**
   - Indicateurs de performance (vélocité, taux de bugs, délai, satisfaction)
   - Seuils d'alerte et cibles

Sois précis, structuré, et adapte le plan au contexte IA/agents autonomes.""",
        temperature=0.4,
    )

    prompt = (
        f"Projet : {nom}\n"
        f"Objectif : {objectif}\n"
        f"Délai total : {delai}\n"
        f"Budget : {budget}\n"
        f"Historique : {contexte}"
    )

    resultat = executer_stream(agent, prompt, f"Plan de Projet — {nom}")

    sauvegarder_projet_memoire(nom, {
        "objectif": objectif,
        "delai": delai,
        "budget": budget,
        "plan": resultat[:500],
    })
    chemin = sauvegarder_fichier(nom, "plan_projet", resultat)

    m = charger_memoire()
    if nom in m.get("projets", {}):
        m["projets"][nom].setdefault("rapports", []).append({
            "type": "plan_projet",
            "date": datetime.now().isoformat(),
            "fichier": chemin,
        })
        sauvegarder_memoire(m)

    return resultat


def agent_daily_standup(projet, avancement, blocages):
    """
    Génère un rapport de standup quotidien :
    accompli, planifié, blocages + solutions, alertes équipe, % avancement.
    """
    incrementer_stat("daily_standup")
    contexte = obtenir_contexte_projet(projet)

    agent = creer_agent(
        """Tu es un Scrum Master expérimenté en projets IA.

Génère un rapport de standup quotidien structuré et actionnable :

1. **📋 Ce qui a été accompli hier**
   - Liste des tâches terminées avec responsable
   - Livrables validés ou en attente de validation

2. **🎯 Ce qui est planifié aujourd'hui**
   - Tâches prioritaires du jour
   - Objectif de fin de journée

3. **🚧 Blocages et solutions**
   - Chaque blocage avec : description | impact | solution proposée | responsable
   - Escalades nécessaires si critique

4. **⚠️ Alertes équipe**
   - Risques imminents détectés
   - Dépendances à surveiller
   - Points d'attention pour les prochains jours

5. **📊 Avancement global**
   - Pourcentage d'avancement réel vs plan
   - Tendance (en avance / dans les temps / en retard)
   - Prévision de fin de projet (date recalculée si nécessaire)

Sois concis, factuel et orienté solutions.""",
        temperature=0.3,
    )

    prompt = (
        f"Projet : {projet}\n"
        f"Avancement communiqué : {avancement}\n"
        f"Blocages signalés : {blocages}\n"
        f"Contexte projet : {contexte}\n"
        f"Date du standup : {datetime.now().strftime('%A %d %B %Y')}"
    )

    resultat = executer_stream(agent, prompt, f"Daily Standup — {projet}")

    ajouter_interaction(
        projet, "daily_standup",
        f"Avancement: {avancement[:100]} | Blocages: {blocages[:100]}"
    )
    sauvegarder_fichier(projet, "standup", resultat)

    m = charger_memoire()
    if projet in m.get("projets", {}):
        m["projets"][projet]["dernier_avancement"] = avancement
        m["projets"][projet]["derniers_blocages"] = blocages
        sauvegarder_memoire(m)

    return resultat


def agent_gestion_risques(projet, contexte):
    """
    Identifie les top 10 risques d'un projet IA, les note (probabilité × impact),
    génère plans de mitigation, actions de contingence et propriétaires de risques.
    """
    incrementer_stat("gestion_risques")
    contexte_projet = obtenir_contexte_projet(projet)

    agent = creer_agent(
        f"""Tu es un Risk Manager spécialisé en projets d'Intelligence Artificielle.
Entreprise : {ENTREPRISE_PROFIL}

Produis un registre de risques complet pour un projet IA :

**TOP 10 RISQUES IDENTIFIÉS**

Pour chaque risque, fournis :

| # | Catégorie | Description du risque | Probabilité (1-5) | Impact (1-5) | Score (P×I) | Niveau |
|---|-----------|----------------------|:-----------------:|:------------:|:-----------:|--------|

Catégories à couvrir obligatoirement :
- Risques techniques (IA, données, intégration)
- Risques humains (compétences, dépendances clés)
- Risques organisationnels (périmètre, priorisation)
- Risques externes (réglementation, fournisseurs)
- Risques sécurité/conformité (RGPD, biais IA)

Pour chaque risque, détaille ensuite :

**Plan de mitigation** : Actions préventives à mettre en place dès maintenant
**Actions de contingence** : Que faire si le risque se réalise
**Risk Owner** : Qui est responsable du suivi de ce risque
**Indicateur de déclenchement** : Signal d'alerte à surveiller

Classe les risques par score décroissant. Fournis une heatmap textuelle en conclusion.""",
        temperature=0.4,
    )

    prompt = (
        f"Projet : {projet}\n"
        f"Contexte et description : {contexte}\n"
        f"Historique projet : {contexte_projet}"
    )

    resultat = executer_stream(agent, prompt, f"Gestion des Risques — {projet}")

    sauvegarder_projet_memoire(projet, {"registre_risques": resultat[:500]})
    chemin = sauvegarder_fichier(projet, "registre_risques", resultat)

    m = charger_memoire()
    if projet in m.get("projets", {}):
        m["projets"][projet].setdefault("rapports", []).append({
            "type": "registre_risques",
            "date": datetime.now().isoformat(),
            "fichier": chemin,
        })
        sauvegarder_memoire(m)

    return resultat


def agent_retrospective(projet, resultats, feedback_equipe):
    """
    Génère une rétrospective sprint/projet :
    ce qui a bien marché, à améliorer, actions avec propriétaires et délais,
    leçons apprises, améliorations de processus.
    """
    incrementer_stat("retrospective")
    contexte = obtenir_contexte_projet(projet)

    agent = creer_agent(
        """Tu es un Agile Coach expert en amélioration continue et rétrospectives.

Génère une rétrospective complète et exploitable :

1. **🌟 Ce qui a bien fonctionné (Keep)**
   - Succès techniques, humains et organisationnels
   - Pratiques à pérenniser
   - Reconnaissances individuelles et collectives

2. **🔧 Ce qui doit être amélioré (Improve)**
   - Points de friction identifiés
   - Goulots d'étranglement processus
   - Problèmes de communication ou coordination

3. **🛑 Ce qui doit être arrêté (Stop)**
   - Pratiques contre-productives
   - Réunions ou processus inutiles
   - Sources de dette technique à éliminer

4. **📋 Plan d'action (Actions Items)**
   Format tableau :
   | Action | Responsable | Priorité (H/M/L) | Échéance | Critère de succès |

   Minimum 5 actions concrètes et mesurables.

5. **📚 Leçons apprises**
   - Enseignements transférables à d'autres projets
   - Bonnes pratiques IA spécifiques découvertes
   - Documentation des erreurs à ne pas reproduire

6. **⚙️ Améliorations de processus**
   - Ajustements méthodologiques Agile/Scrum
   - Outils ou automatisations à mettre en place
   - Formation ou montée en compétences identifiées

Sois constructif, factuel et orienté solutions — pas de jugements personnels.""",
        temperature=0.5,
    )

    prompt = (
        f"Projet : {projet}\n"
        f"Résultats obtenus : {resultats}\n"
        f"Feedback équipe : {feedback_equipe}\n"
        f"Contexte projet : {contexte}\n"
        f"Date rétrospective : {datetime.now().strftime('%d/%m/%Y')}"
    )

    resultat = executer_stream(agent, prompt, f"Rétrospective — {projet}")

    sauvegarder_projet_memoire(projet, {"derniere_retro": resultat[:500]})
    chemin = sauvegarder_fichier(projet, "retrospective", resultat)

    m = charger_memoire()
    if projet in m.get("projets", {}):
        m["projets"][projet].setdefault("rapports", []).append({
            "type": "retrospective",
            "date": datetime.now().isoformat(),
            "fichier": chemin,
        })
        sauvegarder_memoire(m)

    ajouter_interaction(projet, "retrospective", resultat[:200])
    return resultat


def agent_rapport_client_projet(projet, periode, livrables):
    """
    Génère un rapport de statut projet professionnel pour le client :
    résumé exécutif, avancement vs plan, statut livrables (RAG),
    suivi budgétaire, prochaines étapes, risques & problèmes.
    """
    incrementer_stat("rapport_client_projet")
    contexte = obtenir_contexte_projet(projet)

    agent = creer_agent(
        f"""Tu es un Chef de Projet Senior qui rédige des rapports clients professionnels.
Entreprise prestataire : {ENTREPRISE_PROFIL}

Génère un rapport de statut projet complet, clair et professionnel :

---
**RAPPORT DE STATUT PROJET**
AgentClaude Solutions — Document Confidentiel
---

1. **RÉSUMÉ EXÉCUTIF** (½ page max)
   - Statut global du projet : 🟢 VERT / 🟡 ORANGE / 🔴 ROUGE
   - Message clé pour le sponsor/client
   - Décisions requises de la part du client

2. **AVANCEMENT VS PLAN**
   - Tableau de bord : Périmètre | Délai | Budget | Qualité — chacun avec RAG
   - % complété prévu vs % réel
   - Courbe d'avancement (description textuelle)
   - Vélocité de l'équipe

3. **STATUT DES LIVRABLES (RAG)**
   Format tableau :
   | Livrable | Échéance | Statut (🟢/🟡/🔴) | % Complété | Commentaire |

4. **SUIVI BUDGÉTAIRE**
   - Budget total / Engagé / Consommé / Reste à dépenser (RAD)
   - Indice de performance coûts (CPI)
   - Alertes budgétaires si applicable

5. **PROCHAINES ÉTAPES**
   - Actions planifiées pour la prochaine période
   - Jalons à venir (3 prochains)
   - Demandes au client (validations, décisions, ressources)

6. **RISQUES ET PROBLÈMES ACTIFS**
   | Type | Description | Niveau | Impact | Action en cours |

7. **INDICATEURS CLÉS (KPIs)**
   - KPIs de qualité, délai, satisfaction — avec tendances

Adopte un ton professionnel, factuel et rassurant pour le client.""",
        temperature=0.4,
    )

    prompt = (
        f"Projet : {projet}\n"
        f"Période couverte : {periode}\n"
        f"Livrables et statuts : {livrables}\n"
        f"Contexte projet en mémoire : {contexte}\n"
        f"Date du rapport : {datetime.now().strftime('%d/%m/%Y')}"
    )

    resultat = executer_stream(agent, prompt, f"Rapport Client — {projet} ({periode})")

    sauvegarder_projet_memoire(projet, {"dernier_rapport_client": resultat[:500]})
    chemin = sauvegarder_fichier(projet, "rapport_client", resultat)

    m = charger_memoire()
    if projet in m.get("projets", {}):
        m["projets"][projet].setdefault("rapports", []).append({
            "type": "rapport_client",
            "date": datetime.now().isoformat(),
            "periode": periode,
            "fichier": chemin,
        })
        sauvegarder_memoire(m)

    ajouter_interaction(projet, "rapport_client", resultat[:200])
    return resultat


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def menu():
    print("\n" + "═" * 62)
    print("  AGENT CHEF DE PROJET — AgentClaude Solutions")
    print("═" * 62)

    while True:
        print("\n  1. Planifier un nouveau projet (WBS, timeline, budget, risques)")
        print("  2. Daily Standup — rapport quotidien")
        print("  3. Gestion des risques — registre complet")
        print("  4. Rétrospective sprint / projet")
        print("  5. Rapport client — statut projet (RAG)")
        print("  6. Lister les projets en mémoire")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  Au revoir !\n")
            break

        elif choix == "1":
            print("\n  ── Nouveau Projet ──")
            nom = input("  Nom du projet → ").strip()
            objectif = input("  Objectif principal → ").strip()
            delai = input("  Délai total (ex: 3 mois, 6 sprints) → ").strip()
            budget = input("  Budget (ex: 50 000 €) → ").strip()
            agent_planifier_projet(nom, objectif, delai, budget)

        elif choix == "2":
            print("\n  ── Daily Standup ──")
            lister_projets()
            projet = input("\n  Nom du projet → ").strip()
            avancement = input("  Avancement hier / aujourd'hui → ").strip()
            blocages = input("  Blocages rencontrés (ou 'aucun') → ").strip()
            agent_daily_standup(projet, avancement, blocages)

        elif choix == "3":
            print("\n  ── Gestion des Risques ──")
            lister_projets()
            projet = input("\n  Nom du projet → ").strip()
            contexte = input("  Contexte / description du projet → ").strip()
            agent_gestion_risques(projet, contexte)

        elif choix == "4":
            print("\n  ── Rétrospective ──")
            lister_projets()
            projet = input("\n  Nom du projet / sprint → ").strip()
            resultats = input("  Résultats obtenus → ").strip()
            feedback_equipe = input("  Feedback de l'équipe → ").strip()
            agent_retrospective(projet, resultats, feedback_equipe)

        elif choix == "5":
            print("\n  ── Rapport Client ──")
            lister_projets()
            projet = input("\n  Nom du projet → ").strip()
            periode = input("  Période couverte (ex: Semaine 12, Sprint 3) → ").strip()
            livrables = input("  Livrables et statuts (ex: Module Auth vert, API orange) → ").strip()
            agent_rapport_client_projet(projet, periode, livrables)

        elif choix == "6":
            lister_projets()

        else:
            print("  ⚠  Choix invalide. Entrez un numéro entre 0 et 6.")


if __name__ == "__main__":
    menu()
