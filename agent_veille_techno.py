"""
AGENT VEILLE TECHNOLOGIQUE — Niveau Analyste Gartner
Expert en intelligence technologique pour une entreprise d'agents IA.
Surveille, évalue et anticipe les évolutions du marché.

Usage : python agent_veille_techno.py
"""

import os
import sys
import json
from datetime import datetime
import google.generativeai as genai
from memoire import incrementer_stat

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécutez : export GEMINI_API_KEY=votre_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

DOSSIER_SORTIE = "fichiers/veille_techno"
os.makedirs(DOSSIER_SORTIE, exist_ok=True)

PROFIL_ENTREPRISE = """
Entreprise : AgentClaude Solutions
Secteur : Développement et déploiement d'agents IA autonomes
Stack actuelle : Python, LangChain, CrewAI, Claude (Anthropic), Gemini (Google), FastAPI, Cloud Run
Clients : PME et ETI cherchant à automatiser leurs processus métier
Taille : Start-up Série A, ~15 personnes
Points forts : Agents multi-modèles, intégration legacy, sécurité IA
"""


def creer_agent(instructions, temperature=0.3):
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(
            temperature=temperature, max_output_tokens=4096
        ),
    )


def executer_stream(model, prompt, label):
    print(f"\n{'═'*65}")
    print(f"  ▶  {label}")
    print(f"{'═'*65}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur lors de la génération : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder(nom_fichier, contenu, sous_dossier=""):
    dossier = os.path.join(DOSSIER_SORTIE, sous_dossier) if sous_dossier else DOSSIER_SORTIE
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(dossier, f"{horodatage}_{nom_fichier}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write("=" * 65 + "\n\n")
        f.write(contenu)
    print(f"\n[✓] Sauvegardé : {chemin}")
    return chemin


# ─── AGENT 1 : SCANNER NOUVEAUTÉS ────────────────────────────────

def agent_scanner_nouveautes(domaine):
    """Scanne les dernières évolutions IA : modèles, frameworks, API, prix."""
    incrementer_stat("agent_scanner_nouveautes")

    agent = creer_agent(f"""Tu es un analyste technologique senior niveau Gartner, spécialisé dans l'IA et les agents autonomes.
Tu travailles pour une entreprise dont voici le profil :
{PROFIL_ENTREPRISE}

Ta mission est de produire un briefing de veille structuré et actionnable.
Pour chaque nouveauté identifiée, tu dois évaluer :
- L'impact concret sur notre entreprise (chiffré si possible)
- Le niveau d'urgence : URGENT / À SURVEILLER / IGNORER
- Si c'est une OPPORTUNITÉ ou une MENACE
- L'action concrète recommandée

Sois factuel, précis, sans superflu. Pense comme un stratège, pas comme un journaliste tech.""", temperature=0.4)

    prompt = f"""Effectue un scan complet des dernières évolutions dans le domaine : **{domaine}**

Couvre les axes suivants :

## 1. NOUVEAUX MODÈLES & MISES À JOUR
- Nouveaux modèles LLM/multimodaux sortis récemment
- Mises à jour majeures de modèles existants (GPT, Claude, Gemini, Llama, Mistral...)
- Changements de capacités (contexte, vitesse, prix, multimodalité)

## 2. NOUVEAUX FRAMEWORKS & OUTILS
- Nouveaux frameworks d'agents (LangGraph, AutoGen, CrewAI updates, etc.)
- Outils d'observabilité et monitoring IA
- Nouvelles librairies ou SDK pertinents

## 3. CHANGEMENTS API & PRIX
- Modifications tarifaires chez les providers
- Nouvelles API ou deprecations
- Changements dans les rate limits ou conditions d'utilisation

## 4. BRIEFING STRUCTURÉ PAR ITEM
Pour chaque élément identifié, fournis :
- Nom & description courte
- Ce qui a changé
- Impact sur notre business (1-5 étoiles)
- Niveau d'action : 🔴 URGENT | 🟡 À SURVEILLER | 🟢 IGNORER
- Nature : 🚀 OPPORTUNITÉ | ⚠️ MENACE | ↔️ NEUTRE
- Action recommandée concrète

## 5. SYNTHÈSE EXÉCUTIVE
Top 3 des actions prioritaires cette semaine."""

    resultat = executer_stream(agent, prompt, f"Scanner Nouveautés — {domaine}")
    sauvegarder(f"scanner_{domaine.replace(' ', '_')}", resultat, "scans")
    return resultat


# ─── AGENT 2 : ÉVALUATION TECHNOLOGIE ────────────────────────────

def agent_evaluer_technologie(technologie, cas_usage):
    """Évaluation technique approfondie d'une technologie avec recommandation Thoughtworks."""
    incrementer_stat("agent_evaluer_technologie")

    agent = creer_agent(f"""Tu es un architecte solutions et évaluateur technologique niveau Gartner / Thoughtworks.
Tu évalues les technologies pour une entreprise d'agents IA :
{PROFIL_ENTREPRISE}

Tu utilises le framework d'évaluation Thoughtworks Technology Radar :
- ADOPT : Utiliser maintenant en production
- TRIAL : Explorer sur un projet pilote
- ASSESS : Investiguer, pas encore prêt
- HOLD : Éviter pour l'instant

Tu évalues aussi le TRL (Technology Readiness Level, 1-9) selon la définition NASA/ESA.
Tu es rigoureux, objectif, et tu bases tes évaluations sur des données concrètes.""", temperature=0.2)

    prompt = f"""Réalise une évaluation technique approfondie de : **{technologie}**
Cas d'usage cible : **{cas_usage}**

## 1. PRÉSENTATION TECHNIQUE
- Description précise et architecture
- Fonctionnement interne (sans jargon inutile)
- Écosystème et communauté (taille, activité GitHub, support commercial)

## 2. CAPACITÉS ET LIMITATIONS
- Ce que la technologie fait exceptionnellement bien
- Limitations documentées et cas d'échec connus
- Performances réelles vs marketing
- Scalabilité et robustesse en production

## 3. NIVEAU DE MATURITÉ
- TRL (1-9) avec justification détaillée
- Niveau de maturité selon Gartner Hype Cycle (position actuelle)
- Production-readiness : PoC / Pilote / Production / Enterprise-grade

## 4. COMPLEXITÉ D'INTÉGRATION
- Effort d'intégration estimé (jours/homme)
- Dépendances et prérequis
- Courbe d'apprentissage pour notre équipe
- Risques d'intégration identifiés

## 5. ANALYSE DES COÛTS
- Coût de licence/API (si applicable)
- Coût d'infrastructure
- Coût humain (formation, maintenance)
- TCO sur 3 ans estimé pour notre contexte

## 6. IMPLICATIONS SÉCURITÉ
- Vecteurs d'attaque et vulnérabilités connues
- Conformité RGPD / EU AI Act
- Gestion des données sensibles
- Audit et traçabilité

## 7. STABILITÉ ÉDITEUR/VENDOR
- Solidité financière de l'éditeur
- Risque d'abandon ou pivot
- Alternative open-source si besoin
- Clauses contractuelles à surveiller

## 8. COMPARAISON AVEC NOTRE STACK
- Overlap avec ce que nous utilisons déjà
- Avantages vs notre solution actuelle
- Coût de migration si on adopte

## 9. RECOMMANDATION FINALE
**Verdict Thoughtworks : [ADOPT / TRIAL / ASSESS / HOLD]**
Justification en 3 points clés.
Conditions de révision de cette évaluation (triggers)."""

    resultat = executer_stream(agent, prompt, f"Évaluation Technologie — {technologie}")
    sauvegarder(f"evaluation_{technologie.replace(' ', '_')}", resultat, "evaluations")
    return resultat


# ─── AGENT 3 : RADAR TECHNOLOGIQUE ───────────────────────────────

def agent_radar_technologique():
    """Génère un radar technologique complet style Thoughtworks pour l'entreprise."""
    incrementer_stat("agent_radar_technologique")

    agent = creer_agent(f"""Tu es le CTO et Chief Architect d'une entreprise d'agents IA, avec une expertise niveau Thoughtworks.
Profil de l'entreprise :
{PROFIL_ENTREPRISE}

Tu crées le Technology Radar annuel de l'entreprise.
Chaque entrée du radar est classée dans un quadrant et un anneau :

Quadrants :
- LLM & MODÈLES IA
- FRAMEWORKS & LIBRAIRIES
- INFRASTRUCTURE & DÉPLOIEMENT
- OUTILS (Monitoring, Sécurité, DevOps)

Anneaux :
- ADOPT : Utiliser en production maintenant (fiable, recommandé)
- TRIAL : Expérimenter sur projet pilote (prometteur)
- ASSESS : Explorer et évaluer (intéressant mais incertain)
- HOLD : Éviter ou ne pas investir davantage

Chaque entrée doit avoir : justification courte, mouvement depuis dernier radar (NEW/↑/↓/stable).""", temperature=0.3)

    prompt = f"""Génère le Technology Radar Q{datetime.now().month//3 + 1} {datetime.now().year} pour notre entreprise d'agents IA.

## QUADRANT 1 : LLM & MODÈLES IA
Classe et commente les modèles clés :
Claude (3.5/3.7 Sonnet, Haiku, Opus), GPT-4o / o1 / o3, Gemini (Flash/Pro/Ultra), Llama 3.x, Mistral Large, DeepSeek, Qwen, Command R+, models open-weights spécialisés...

## QUADRANT 2 : FRAMEWORKS & LIBRAIRIES AGENTS
LangChain / LangGraph, CrewAI, AutoGen / AG2, Pydantic AI, Agno, Haystack, LlamaIndex, Instructor, DSPy, Semantic Kernel, Smolagents, LMNT...

## QUADRANT 3 : INFRASTRUCTURE & DÉPLOIEMENT
Cloud Run, Lambda (AWS), Azure Container Apps, Modal, Fly.io, Railway, Supabase, Neon DB, Qdrant, Weaviate, Pinecone, Chroma, pgvector...

## QUADRANT 4 : OUTILS (Monitoring / Sécurité / DevOps)
LangSmith, LangFuse, Arize Phoenix, Weights & Biases, Helicone, Guardrails AI, LlamaGuard, Rebuff, Promptfoo, MLflow...

## FORMAT DE SORTIE
Pour chaque technologie :
| Technologie | Anneau | Mouvement | Justification (1 ligne) |

Puis une SYNTHÈSE NARRATIVE avec :
- Les 5 paris technologiques à faire maintenant
- Les 3 technologies à abandonner ou éviter
- Les signaux faibles à surveiller (technologies émergentes sous-radar)"""

    resultat = executer_stream(agent, prompt, "Radar Technologique — Vue Complète")
    sauvegarder("radar_technologique", resultat, "radars")
    return resultat


# ─── AGENT 4 : ALERTE DISRUPTION ─────────────────────────────────

def agent_alerte_disruption(secteur):
    """Identifie les disruptions potentielles et recommande des réponses stratégiques."""
    incrementer_stat("agent_alerte_disruption")

    agent = creer_agent(f"""Tu es un stratège en disruption technologique et innovation, niveau McKinsey Digital.
Tu analyses les menaces existentielles et opportunités de disruption pour :
{PROFIL_ENTREPRISE}

Tu utilises les frameworks : Clayton Christensen (disruption par le bas), Jobs-to-be-Done, Five Forces de Porter.
Tu es direct, tu n'édulcores pas les menaces. Ton rôle est de sonner l'alarme quand c'est nécessaire.""", temperature=0.4)

    prompt = f"""Analyse les risques de disruption dans le secteur : **{secteur}**
Pour une entreprise d'agents IA comme la nôtre.

## 1. NOUVEAUX ENTRANTS & COMMODITISATION
- Qui entre sur notre marché ? (Big Tech, startups financées, open-source)
- Risque de commoditisation de nos services (dans 6 mois ? 2 ans ?)
- Modèles gratuits ou quasi-gratuits qui menacent notre pricing

## 2. ÉVOLUTIONS TECHNOLOGIQUES DISRUPTIVES
- Technologies qui pourraient rendre nos agents obsolètes
- GPT-5 / Claude 4 / Gemini Ultra : capacités émergentes qui cannibalisent nos services ?
- Agents autonomes natifs qui n'ont plus besoin d'intégration custom
- Computer-use, browser automation : impact sur notre proposition de valeur

## 3. RISQUES RÉGLEMENTAIRES
- EU AI Act : dates clés et obligations pour nous
- Obligations de conformité qui augmentent nos coûts
- Régulations qui pourraient bloquer certains use cases clients
- Litiges et jurisprudence IA à surveiller

## 4. RISQUES STRATÉGIQUES
- Clients qui internalisent nos capacités (build vs buy shift)
- Partenaires qui deviennent concurrents
- Dépendances critiques (si Anthropic/Google change ses CGU...)
- Concentration du marché qui nous exclut

## 5. MATRICE DE PROBABILITÉ / IMPACT
Pour chaque risque identifié :
| Risque | Probabilité (1-5) | Impact (1-5) | Délai | Score Priorité |

## 6. RÉPONSES STRATÉGIQUES RECOMMANDÉES
Pour les 3 risques prioritaires :
- Stratégie de défense
- Stratégie d'adaptation
- Stratégie d'anticipation (être soi-même le disrupteur)
- Ressources nécessaires et délai d'action"""

    resultat = executer_stream(agent, prompt, f"Alerte Disruption — {secteur}")
    sauvegarder(f"disruption_{secteur.replace(' ', '_')}", resultat, "alertes")
    return resultat


# ─── AGENT 5 : VEILLE BREVETS ─────────────────────────────────────

def agent_veille_brevets(domaine):
    """Analyse du paysage brevets IA : risques FTO et opportunités de protection."""
    incrementer_stat("agent_veille_brevets")

    agent = creer_agent(f"""Tu es un expert en propriété intellectuelle et brevets technologiques, spécialisé dans l'IA.
Tu combines expertise juridique et technique pour conseiller :
{PROFIL_ENTREPRISE}

Tu analyses le paysage des brevets pour identifier :
1. Les techniques protégées à éviter (freedom-to-operate)
2. Les opportunités de protection de nos propres innovations
3. Les risques de litiges et comment les anticiper

Tu es concret et pratique, pas théorique.""", temperature=0.2)

    prompt = f"""Analyse le paysage des brevets dans le domaine : **{domaine}**

## 1. CARTOGRAPHIE DES DÉPOSANTS CLÉS
- Principaux détenteurs de brevets dans ce domaine
- Portfolios brevets des acteurs majeurs (Google/DeepMind, OpenAI/Microsoft, Meta, IBM, Amazon)
- Patent trolls actifs dans ce secteur
- Brevets fondamentaux vs. brevets périphériques

## 2. TECHNIQUES PROTÉGÉES (ZONES À RISQUE)
- Techniques d'entraînement protégées à éviter
- Architectures brevetées (attention mechanisms, RLHF, RAG variations...)
- Méthodes d'orchestration d'agents potentiellement protégées
- Interfaces et UX brevetées

## 3. ANALYSE FREEDOM-TO-OPERATE (FTO)
- Évaluation du risque pour notre stack actuelle
- Zones de liberté opérationnelle confirmées
- Zones grises nécessitant analyse juridique approfondie
- Risque de poursuite : FAIBLE / MODÉRÉ / ÉLEVÉ

## 4. OPPORTUNITÉS DE PROTECTION POUR NOUS
- Nos innovations potentiellement brevetables
- Méthodes d'orchestration multi-agents originales
- Pipelines propriétaires qui méritent protection
- Stratégie : brevet / secret commercial / publication défensive

## 5. RECOMMANDATIONS PRATIQUES
- Actions immédiates pour réduire l'exposition
- Budget estimé pour une stratégie IP minimale
- Partenaires juridiques spécialisés recommandés
- Processus interne à mettre en place pour capturer l'innovation"""

    resultat = executer_stream(agent, prompt, f"Veille Brevets — {domaine}")
    sauvegarder(f"brevets_{domaine.replace(' ', '_')}", resultat, "brevets")
    return resultat


# ─── AGENT 6 : BENCHMARK TECHNIQUE ───────────────────────────────

def agent_benchmark_technique(notre_stack, concurrent_stack):
    """Benchmarking technique entre notre stack et celle d'un concurrent."""
    incrementer_stat("agent_benchmark_technique")

    agent = creer_agent(f"""Tu es un architecte technique senior spécialisé dans l'évaluation comparative de stacks IA.
Tu travailles pour :
{PROFIL_ENTREPRISE}

Tu réalises des benchmarks rigoureux, factuels et actionnables.
Tu utilises le framework Build vs Buy vs Partner pour les décisions.
Tu es objectif : si la stack concurrente est meilleure sur un point, tu le dis clairement.""", temperature=0.2)

    prompt = f"""Réalise un benchmark technique complet entre :
- **Notre stack** : {notre_stack}
- **Stack concurrente** : {concurrent_stack}

## 1. COMPARAISON FONCTIONNELLE
Tableau comparatif feature par feature :
| Fonctionnalité | Notre Stack | Stack Concurrente | Gagnant | Écart |

Couvre : performance, latence, scalabilité, fiabilité, observabilité, sécurité, coût, DX (Developer Experience), documentation, support communauté.

## 2. PERFORMANCE & BENCHMARKS QUANTITATIFS
- Latence moyenne / P99 (estimations ou données publiques)
- Throughput (requêtes/seconde)
- Coût par 1000 appels
- Temps de mise en production d'un nouvel agent
- Taux d'erreur et résilience

## 3. DETTE TECHNIQUE
- Points de fragilité dans notre stack actuelle
- Couplages forts problématiques
- Risques de scalabilité à 10x notre taille actuelle
- Dépendances outdatées ou fin de vie

## 4. GAPS À COMBLER
- Fonctionnalités manquantes critiques (business impact)
- Fonctionnalités manquantes importantes (developer experience)
- Fonctionnalités manquantes mineures (nice-to-have)

## 5. ANALYSE BUILD vs BUY vs PARTNER
Pour chaque gap identifié :
| Gap | Build | Buy | Partner | Recommandation | Effort | Délai |

## 6. PLAN DE MIGRATION (si applicable)
Si la stack concurrente est significativement meilleure :
- Stratégie de migration progressive (strangler fig pattern)
- Milestones et jalons
- Risques de migration et mitigations
- Go/No-go criteria

## 7. VERDICT FINAL
Score global Notre Stack vs Concurrent (sur 100).
Recommandation : Maintenir / Améliorer / Migrer partiellement / Migrer totalement."""

    resultat = executer_stream(agent, prompt, f"Benchmark — Notre Stack vs {concurrent_stack[:40]}")
    label = f"{notre_stack[:20]}_vs_{concurrent_stack[:20]}".replace(' ', '_')
    sauvegarder(f"benchmark_{label}", resultat, "benchmarks")
    return resultat


# ─── MENU PRINCIPAL ───────────────────────────────────────────────

def afficher_menu():
    print("\n" + "═" * 65)
    print("   AGENT VEILLE TECHNOLOGIQUE — Niveau Analyste Gartner")
    print("═" * 65)
    print("  1. Scanner les nouveautés IA (modèles, frameworks, API, prix)")
    print("  2. Évaluer une technologie (TRL + radar Thoughtworks)")
    print("  3. Générer le Radar Technologique complet")
    print("  4. Alerte disruption (menaces et réponses stratégiques)")
    print("  5. Veille brevets (FTO + opportunités IP)")
    print("  6. Benchmark technique (notre stack vs concurrent)")
    print("  0. Quitter")
    print("═" * 65)


def main():
    print("\n  Initialisation de l'agent de veille technologique...")

    while True:
        afficher_menu()
        choix = input("\n  Votre choix (0-6) : ").strip()

        if choix == "0":
            print("\n  Au revoir. Restez à la pointe de la tech !\n")
            break

        elif choix == "1":
            domaine = input("  Domaine à scanner (ex: LLM, agents autonomes, RAG) : ").strip()
            if domaine:
                agent_scanner_nouveautes(domaine)
            else:
                print("  [!] Veuillez saisir un domaine.")

        elif choix == "2":
            technologie = input("  Technologie à évaluer (ex: LangGraph, Qdrant) : ").strip()
            cas_usage = input("  Cas d'usage cible (ex: orchestration multi-agents) : ").strip()
            if technologie and cas_usage:
                agent_evaluer_technologie(technologie, cas_usage)
            else:
                print("  [!] Veuillez renseigner tous les champs.")

        elif choix == "3":
            agent_radar_technologique()

        elif choix == "4":
            secteur = input("  Secteur à analyser (ex: automatisation RH, service client IA) : ").strip()
            if secteur:
                agent_alerte_disruption(secteur)
            else:
                print("  [!] Veuillez saisir un secteur.")

        elif choix == "5":
            domaine = input("  Domaine brevets (ex: orchestration d'agents, RAG, fine-tuning) : ").strip()
            if domaine:
                agent_veille_brevets(domaine)
            else:
                print("  [!] Veuillez saisir un domaine.")

        elif choix == "6":
            notre_stack = input("  Notre stack actuelle (ex: LangChain + CrewAI + Claude) : ").strip()
            concurrent = input("  Stack concurrente (ex: AutoGen + GPT-4o + Azure) : ").strip()
            if notre_stack and concurrent:
                agent_benchmark_technique(notre_stack, concurrent)
            else:
                print("  [!] Veuillez renseigner les deux stacks.")

        else:
            print("  [!] Option invalide. Choisissez entre 0 et 6.")


if __name__ == "__main__":
    main()
