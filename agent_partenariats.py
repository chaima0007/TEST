"""
AGENT PARTENARIATS & ÉCOSYSTÈME — Niveau VP Partnerships Série B
Expert en développement de partenariats stratégiques pour une entreprise d'agents IA.
Identifie, structure et pilote les alliances qui accélèrent la croissance.

Usage : python agent_partenariats.py
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

DOSSIER_SORTIE = "fichiers/partenariats"
os.makedirs(DOSSIER_SORTIE, exist_ok=True)

PROFIL_ENTREPRISE = """
Entreprise : AgentClaude Solutions
Secteur : Développement et déploiement d'agents IA autonomes
ARR actuel : ~500K€ (estimation Série A)
Stack : Python, LangChain, CrewAI, Claude (Anthropic), Gemini (Google), FastAPI, Cloud Run
Clients : PME et ETI (10-500 salariés), secteurs : RH, Finance, Juridique, Support Client
Taille : ~15 personnes, équipe technique solide
Différenciation : Agents multi-modèles, intégration legacy, conformité RGPD, expertise française
ICP (Ideal Customer Profile) : DSI / DG de PME voulant automatiser sans recruter
"""


def creer_agent(instructions, temperature=0.4):
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


# ─── AGENT 1 : IDENTIFIER PARTENAIRES ────────────────────────────

def agent_identifier_partenaires(type_partenariat):
    """Identifie les partenaires idéaux selon le type de partenariat visé."""
    incrementer_stat("agent_identifier_partenaires")

    agent = creer_agent(f"""Tu es VP Partnerships dans une start-up IA en hypercroissance, ex-Doctolib et Dataiku.
Tu connais parfaitement l'écosystème tech français et européen.
Tu travailles pour :
{PROFIL_ENTREPRISE}

Tu identifies des partenaires avec un raisonnement stratégique, pas une liste générique.
Pour chaque partenaire : tu expliques POURQUOI eux, COMMENT les approcher, et QUELLE valeur on leur apporte.
Tu penses en termes de fit mutuel, pas de wishlist.""", temperature=0.5)

    prompt = f"""Identifie les partenaires idéaux pour un partenariat de type : **{type_partenariat}**

## 1. PARTENAIRES TECHNOLOGIQUES (Cloud & Hyperscalers)
- Programmes partenaires AWS (APN), GCP, Azure : niveaux accessibles, avantages, prérequis
- Programmes Anthropic, Google (Gemini), OpenAI : conditions, co-marketing disponible
- Autres éditeurs tech complémentaires (CRM, ERP, SIRH) : SAP, Salesforce, HubSpot, Sage
Pour chacun :
  → Pourquoi ce partenaire maintenant ?
  → Comment entrer en contact (nom des programmes, contacts type)
  → Notre proposition de valeur pour eux (pas que pour nous)
  → Prérequis à satisfaire avant de postuler

## 2. INTÉGRATEURS & ESN (Revendeurs / Prescripteurs)
- Top ESN françaises susceptibles de revendre : Capgemini, Sopra Steria, Atos, CGI, Devoteam, Onepoint
- Boutiques spécialisées IA (taille 50-500 pers.) plus accessibles et agiles
- Cabinets de conseil digital qui prescrivent nos solutions
Pour chacun :
  → Profil du bon interlocuteur (rôle, département)
  → Modèle commercial adapté (referral / white-label / co-vente)
  → Argument de différenciation vs leurs partenaires actuels

## 3. CONSULTANTS & PRESCRIPTEURS INDÉPENDANTS
- Consultants fractionnels (DAF, DRH, DSI fractionnels) qui conseillent nos ICP
- Cabinets de conseil en transformation digitale
- Experts-comptables et commissaires aux comptes (accès PME)
  → Comment les rémunérer (referral fee structure)
  → Programme d'évangélisation recommandé

## 4. PARTENARIATS ACADÉMIQUES & RECHERCHE
- Laboratoires IA (INRIA, CNRS, laboratoires grandes écoles)
- Chaires IA partenaires (HEC, ESSEC, Polytechnique)
- Dispositifs CIFRE et co-innovation
  → Bénéfices concrets (accès talent, légitimité, subventions)
  → Comment initier le contact

## 5. INVESTISSEURS STRATÉGIQUES
- Fonds spécialisés IA qui investissent dans notre segment
- Corporate VC de grands groupes (Orange Ventures, Airbus Ventures, BPI France)
  → Valeur au-delà du capital (réseau clients, légitimité, distribution)
  → Pitch d'entrée en relation

## 6. TOP 10 PRIORITÉS
Classe les 10 partenaires les plus stratégiques avec un score d'attractivité et le premier pas concret à faire."""

    resultat = executer_stream(agent, prompt, f"Identifier Partenaires — {type_partenariat}")
    sauvegarder(f"partenaires_{type_partenariat.replace(' ', '_')}", resultat, "identification")
    return resultat


# ─── AGENT 2 : PROPOSITION DE PARTENARIAT ────────────────────────

def agent_proposition_partenariat(partenaire, type_partenariat):
    """Génère une proposition de partenariat complète et sur-mesure."""
    incrementer_stat("agent_proposition_partenariat")

    agent = creer_agent(f"""Tu es un expert en deal-making et structuration de partenariats B2B tech.
Tu as structuré des partenariats pour des scale-ups IA valorisées à +100M€.
Tu travailles pour :
{PROFIL_ENTREPRISE}

Tu crées des propositions de partenariat win-win, concrètes et signables.
Tu penses comme un avocat d'affaires et un business developer à la fois.
Tu anticipes les objections et les points de friction légaux et commerciaux.""", temperature=0.4)

    prompt = f"""Génère une proposition de partenariat complète pour :
- **Partenaire cible** : {partenaire}
- **Type de partenariat** : {type_partenariat}

## 1. PROPOSITION DE VALEUR MUTUELLE
- Ce que NOUS apportons à {partenaire} (soyez précis, chiffrez si possible)
- Ce que {partenaire} nous apporte
- Synergies uniques de cette association
- Risque pour chaque partie si on ne fait PAS ce partenariat

## 2. MODÈLE COMMERCIAL
Propose 3 options de structure commerciale :

**Option A — [Nom]** (ex: Referral simple)
- Mécanisme précis
- Taux / montants
- Conditions de déclenchement
- Avantages et inconvénients

**Option B — [Nom]** (ex: Revenue Share)
- Mécanisme précis
- Clé de répartition
- Minimum garanti éventuel

**Option C — [Nom]** (ex: White Label / OEM)
- Mécanisme précis
- Pricing structure
- Gestion de la relation client finale

Recommandation : laquelle proposer en premier et pourquoi.

## 3. CADRE JURIDIQUE NÉCESSAIRE
- Type d'accord à conclure (NDA / LOI / Accord cadre / Contrat de distribution)
- Clauses essentielles à inclure
- Clauses à éviter ou négocier fermement
- Points de vigilance RGPD et propriété intellectuelle
- Durée et conditions de résiliation recommandées

## 4. EXIGENCES TECHNIQUES D'INTÉGRATION
- Intégrations API nécessaires
- Effort de développement estimé (jours/homme)
- Données partagées et protocole de sécurité
- SLA et engagements de disponibilité
- Environnements de test et certification

## 5. PLAN GO-TO-MARKET CONJOINT
Mois 1-3 (Lancement) :
Mois 4-6 (Accélération) :
Mois 7-12 (Scale) :

Actions conjointes : co-webinaires, études de cas, salon professionnel, co-posts LinkedIn, campagne email...

## 6. MÉTRIQUES DE SUCCÈS
- KPIs pour nous (MRR généré, leads apportés, clients communs...)
- KPIs pour {partenaire}
- Revue trimestrielle (QBR) : agenda type et fréquence
- Seuils de déclenchement d'une renégociation

## 7. GOUVERNANCE DU PARTENARIAT
- Interlocuteurs côté nous et côté eux (rôles et responsabilités)
- Comité de pilotage : fréquence et participants
- Process d'escalade en cas de litige
- Conditions de renouvellement et d'évolution"""

    resultat = executer_stream(agent, prompt, f"Proposition Partenariat — {partenaire}")
    sauvegarder(f"proposition_{partenaire.replace(' ', '_')}", resultat, "propositions")
    return resultat


# ─── AGENT 3 : PROGRAMME REVENDEURS ──────────────────────────────

def agent_programme_revendeurs():
    """Conçoit un programme partenaires/revendeurs complet avec tiers et incentives."""
    incrementer_stat("agent_programme_revendeurs")

    agent = creer_agent(f"""Tu es un expert en Channel Sales et Partner Programs, ex-Salesforce et HubSpot.
Tu as conçu des programmes partenaires pour des scale-ups SaaS B2B.
Tu travailles pour :
{PROFIL_ENTREPRISE}

Tu crées des programmes qui motivent réellement les partenaires (pas des programmes paperasse que personne n'utilise).
Tu penses à l'incentive, à la simplicité et à la rentabilité pour le partenaire.""", temperature=0.5)

    prompt = f"""Conçois un programme revendeurs/partenaires complet pour notre société d'agents IA.

## 1. STRUCTURE DES TIERS

### Tier 1 — SILVER (Partenaires entrants)
- Critères d'éligibilité (CA minimum, certifications, secteur...)
- Avantages et bénéfices concrets
- Marge sur revente (%)
- Support inclus
- Outils marketing mis à disposition

### Tier 2 — GOLD (Partenaires actifs)
- Critères pour accéder au Gold (quota, formation...)
- Avantages supplémentaires vs Silver
- Marge améliorée
- Accès prioritaire aux nouvelles fonctionnalités
- Dedicated Partner Success Manager

### Tier 3 — PLATINUM (Partenaires stratégiques)
- Critères d'accès (sélection restreinte, quota élevé)
- Avantages exclusifs (co-développement, early access, co-marketing budget)
- Marge premium
- Siège au Partner Advisory Board
- Accord commercial bilatéral

## 2. STRUCTURE DE RÉMUNÉRATION
- Tableau des marges par tier et par ligne de produit
- SPIFFs (Special Performance Incentive Funds) : quand et comment
- Bonus de performance trimestrielle
- Règles de deal registration (protection des leads apportés)
- Clawback conditions (retour de commissions si churn rapide)

## 3. CERTIFICATIONS REQUISES
- Certification Technique niveau 1 (Installation & configuration)
  → Contenu du cursus, durée, format (e-learning + pratique)
  → Examen et note minimale
- Certification Vente (Solution Selling agents IA)
  → Argumentaires, cas clients, objections
- Certification Avancée (Développement et intégration custom)
  → Prérequis techniques
- Renouvellement annuel des certifications

## 4. CO-MARKETING & MDF (Market Development Funds)
- Budget MDF alloué par tier (% du CA réalisé)
- Activités éligibles (salons, webinaires, contenu, publicité)
- Process de demande et d'approbation
- Reporting d'utilisation requis
- Assets co-brandés mis à disposition

## 5. DEAL REGISTRATION
- Process de soumission (formulaire, délai de réponse)
- Protection offerte (durée, exclusivité géographique ou sectorielle)
- Bonus deal registration (% supplémentaire sur les deals protégés)
- Règles de conflit entre partenaires (arbitrage)

## 6. PORTAIL PARTENAIRE — FONCTIONNALITÉS REQUISES
- Tableau de bord performance (pipeline, commissions, certifications)
- Bibliothèque d'assets (pitchdeck, battlecards, datasheets, vidéos démo)
- Deal registration et tracking
- E-learning et certification
- Ticketing support client
- Co-marketing request

## 7. ONBOARDING PARTENAIRE (90 jours)
- Semaine 1-2 : Kit de démarrage et accès outils
- Mois 1 : Formation et première certification
- Mois 2 : Premier deal conjoint accompagné
- Mois 3 : Autonomie complète, premier QBR

## 8. POLITIQUE DE RÉSILIATION
- Conditions de dégradation de tier (inactivité, non-renouvellement certif)
- Préavis de résiliation partenariat
- Gestion des clients existants en cas de fin de partenariat"""

    resultat = executer_stream(agent, prompt, "Programme Revendeurs — Conception Complète")
    sauvegarder("programme_revendeurs", resultat, "programmes")
    return resultat


# ─── AGENT 4 : NÉGOCIATION PARTENARIAT ───────────────────────────

def agent_negociation_partenariat(partenaire, nos_conditions, leurs_conditions):
    """Stratégie de négociation partenariale avec analyse des leviers et contre-offres."""
    incrementer_stat("agent_negociation_partenariat")

    agent = creer_agent(f"""Tu es un négociateur expert en deals B2B tech, formé à la méthode Harvard (Getting to Yes).
Tu as négocié des partenariats de plusieurs millions d'euros pour des scale-ups.
Tu travailles pour :
{PROFIL_ENTREPRISE}

Tu analyses les rapports de force avec lucidité et proposes des stratégies créatives.
Tu distingues positions (ce qu'ils demandent) des intérêts (pourquoi ils le demandent).
Tu identifies les BATNA (Best Alternative to Negotiated Agreement) des deux parties.""", temperature=0.4)

    prompt = f"""Développe la stratégie de négociation pour le partenariat avec : **{partenaire}**

**Nos conditions initiales :**
{nos_conditions}

**Leurs conditions initiales :**
{leurs_conditions}

## 1. ANALYSE DES RAPPORTS DE FORCE
- Notre BATNA (si on ne signe pas, que se passe-t-il ?)
- Leur BATNA (quelle est leur alternative ?)
- Qui a le plus besoin de ce deal ? Pourquoi ?
- Urgences respectives et contraintes de calendrier
- Asymétries d'information (ce qu'ils savent que nous ignorons et vice versa)

## 2. ANALYSE DES INTÉRÊTS CACHÉS
- Derrière leurs demandes : quels intérêts réels ?
- Ce qui est dit vs ce qui est voulu
- Pressions internes chez {partenaire} (KPIs du contact, politique interne, budget)

## 3. MUST-HAVE vs NICE-TO-HAVE
Notre classification :
| Point | Catégorie | Notre flexibilité | Justification |

Leur classification probable :
| Point | Catégorie probable | Leur flexibilité estimée |

## 4. STRUCTURES CRÉATIVES DE DEAL
Propose 3 structures de deal alternatives qui débloquent les points de friction :
- Option 1 : [Nom] — logique et mécanisme
- Option 2 : [Nom] — logique et mécanisme
- Option 3 : [Nom] — logique et mécanisme (option créative non-conventionnelle)

## 5. CONCESSIONS RECOMMANDÉES
Ce qu'on peut céder (et dans quel ordre, du moins coûteux au plus coûteux) :
Ce qu'on ne cède JAMAIS et comment tenir cette ligne :

## 6. RED FLAGS JURIDIQUES
Clauses dans leurs conditions qui doivent alerter :
- Clause d'exclusivité abusive
- Droits sur notre IP / code source
- Conditions de résiliation unilatérale
- Pénalités disproportionnées
- Clauses de non-concurrence excessives

## 7. SCRIPT DE NÉGOCIATION
Formulations concrètes pour les moments clés :
- Ouverture de la négociation
- Réponse à leur première ancre
- Contre-proposition sur les points critiques
- Gestion d'un blocage (deadlock)
- Conclusion et closing

## 8. SCÉNARIOS DE SORTIE
- Scénario A : On signe dans les 15 jours → que faut-il concéder ?
- Scénario B : Négociation longue (2-3 mois) → comment maintenir le momentum ?
- Scénario C : On rompt les négociations → comment le faire sans brûler le pont ?"""

    resultat = executer_stream(agent, prompt, f"Stratégie Négociation — {partenaire}")
    sauvegarder(f"negociation_{partenaire.replace(' ', '_')}", resultat, "negociations")
    return resultat


# ─── AGENT 5 : GESTION PARTENAIRE ────────────────────────────────

def agent_gestion_partenaire(partenaire, performance):
    """Pilotage de la relation partenaire : QBR, scorecard, co-sell, escalade."""
    incrementer_stat("agent_gestion_partenaire")

    agent = creer_agent(f"""Tu es un Partner Success Manager senior, expert en gestion de partenariats B2B tech.
Tu sais animer des partenariats qui génèrent vraiment du business (pas juste signer des accords qui dorment dans un tiroir).
Tu travailles pour :
{PROFIL_ENTREPRISE}

Tu es proactif, orienté résultat, et tu sais quand un partenariat doit être renouvelé, renforcé ou terminé.""", temperature=0.4)

    prompt = f"""Développe le plan de gestion de la relation avec : **{partenaire}**
Performance actuelle du partenariat : {performance}

## 1. SCORECARD PARTENAIRE
Génère une scorecard complète avec les métriques suivantes (score 1-5 pour chacune) :

**Métriques Business :**
- Leads apportés (volume et qualité)
- Pipeline généré (valeur €)
- Deals closés (CA réalisé vs objectif)
- Taux de conversion des leads partenaire

**Métriques Relationnelles :**
- Niveau d'engagement (réactivité, participation aux formations)
- Certifications obtenues et à jour
- Participation aux actions co-marketing
- NPS du partenaire (satisfaction partenaire)

**Métriques Clients :**
- Satisfaction clients amenés par ce partenaire
- Taux de churn des clients partenaire
- Upsell réalisé sur la base clients partenaire

Score global et classification : PERFORMANT / POTENTIEL / EN RISQUE / À TERMINER

## 2. QBR — QUARTERLY BUSINESS REVIEW
Agenda type d'un QBR avec {partenaire} :

**60 minutes — Structure recommandée :**
- Ouverture et tone-setting (5 min)
- Revue des performances Q passé (15 min)
- Analyse des deals pipeline (10 min)
- Co-sell opportunities identifiées (10 min)
- Plan d'action Q suivant (15 min)
- Sujets divers et closing (5 min)

Template slides (titres et contenu de chaque slide)
Questions clés à poser au partenaire pendant le QBR

## 3. OPPORTUNITÉS DE CO-SELL
Basé sur la performance actuelle ({performance}) :
- Comptes cibles à approcher conjointement ce trimestre
- Division des rôles dans la démarche commerciale (qui fait quoi)
- Ressources à partager pour ces opportunités
- Objectif de pipeline à générer ensemble

## 4. JOINT CASE STUDY
Si le partenariat a des succès à valoriser :
- Template de cas client conjoint (structure recommandée)
- Process de validation et publication
- Canaux de diffusion (site web, LinkedIn, presse pro)
- Droits et approbations nécessaires

## 5. PROCESS D'ESCALADE
Niveaux d'escalade en cas de problème :

Niveau 1 — Opérationnel (Partner Success Manager)
→ Délai de réponse, critères de déclenchement

Niveau 2 — Commercial (Head of Partnerships)
→ Délai de réponse, critères de déclenchement

Niveau 3 — Exécutif (C-Level)
→ Cas extrêmes, menace de rupture

## 6. CRITÈRES DE RENOUVELLEMENT ET RÉSILIATION
**Renouvellement automatique si :**
...

**Renégociation si :**
...

**Suspension du partenariat si :**
...

**Résiliation immédiate si :**
...

## 7. PLAN D'ACTION 90 JOURS
Basé sur la performance actuelle : {performance}
- Actions semaine 1-4
- Actions semaine 5-8
- Actions semaine 9-12
- Checkpoint de décision fin de période"""

    resultat = executer_stream(agent, prompt, f"Gestion Partenaire — {partenaire}")
    sauvegarder(f"gestion_{partenaire.replace(' ', '_')}", resultat, "gestion")
    return resultat


# ─── AGENT 6 : ÉCOSYSTÈME STRATÉGIQUE ────────────────────────────

def agent_ecosysteme_strategique():
    """Cartographie complète de l'écosystème stratégique et positionnement optimal."""
    incrementer_stat("agent_ecosysteme_strategique")

    agent = creer_agent(f"""Tu es un stratège de plateforme et d'écosystème, niveau BCG Platinion ou a16z.
Tu analyses les dynamiques de marché, les effets de réseau et les stratégies de positionnement.
Tu travailles pour :
{PROFIL_ENTREPRISE}

Tu utilises les frameworks : Value Chain (Porter), Platform Strategy, API Economy, Build/Buy/Partner.
Tu penses à 3-5 ans et identifies les mouvements stratégiques qui créent une position défendable.""", temperature=0.5)

    prompt = f"""Réalise une cartographie stratégique complète de l'écosystème des agents IA.

## 1. CARTE DES ACTEURS CLÉS
Identifie et positionne tous les acteurs :

**Fournisseurs (Upstream) :**
- Providers LLM (Anthropic, OpenAI, Google, Meta, Mistral...)
- Cloud providers (AWS, GCP, Azure, Scaleway)
- Fournisseurs de données et outils

**Concurrents directs :**
- Même ICP, même proposition de valeur
- Forces et faiblesses comparatives
- Comment nous différencier de chacun

**Concurrents indirects :**
- Solutions alternatives que les clients pourraient choisir
- Internalisation par les DSI (make vs buy shift)

**Complémenteurs :**
- Acteurs dont le succès renforce le nôtre
- Opportunités de partenariats de complémentarité

**Clients et influenceurs :**
- Segments de clients et leur pouvoir de négociation
- Influenceurs et prescripteurs clés du marché

## 2. DYNAMIQUES DE POUVOIR
- Qui contrôle les goulots d'étranglement (LLM providers, distribution) ?
- Risques de désintermédiation (clients qui by-passent nos services)
- Risques de ré-intermédiation (nouveaux intermédiaires qui s'imposent)
- Effets de réseau présents dans le marché (qui en bénéficie ?)

## 3. POSITIONNEMENT DANS LA CHAÎNE DE VALEUR
Où sommes-nous actuellement dans la chaîne de valeur ?
Où devrions-nous être dans 3 ans ?

Options de positionnement :
- Couche Infrastructure (plomberie) : avantages et inconvénients
- Couche Middleware (orchestration) : notre position actuelle
- Couche Application (solutions verticales) : faut-il monter ?
- Plateforme (marketplace d'agents) : trop ambitieux ? Pas encore ?

Recommandation de mouvement dans la chaîne de valeur + justification

## 4. STRATÉGIE PLATEFORME vs PRODUIT
- Faut-il créer un marketplace / app store d'agents ?
- Opportunités d'API economy : qui voudrait consommer nos agents en API ?
- Modèle de revenus alternatifs (usage-based, API calls, white-label)
- Conditions pour devenir une plateforme (seuil de réseau critique)

## 5. CIBLES D'ACQUISITION POTENTIELLES
Start-ups ou acteurs que nous pourrions acquérir pour accélérer :
| Cible | Taille estimée | Intérêt stratégique | Valorisation approx. |

## 6. ACQUÉREURS POTENTIELS
Qui pourrait nous acquérir et pourquoi :
| Acquéreur | Motivation | Prix probable | Probabilité |

## 7. MOUVEMENTS STRATÉGIQUES PRIORITAIRES
Identifie les 5 mouvements stratégiques les plus importants (ordre de priorité) :
1. [Mouvement] — Pourquoi maintenant — Ressources nécessaires — Délai
2. ...

## 8. SCÉNARIOS À 3 ANS
- Scénario Bull : tout se passe bien, comment maximiser ?
- Scénario Base : croissance régulière, défis attendus
- Scénario Bear : consolidation du marché, comment survivre ?"""

    resultat = executer_stream(agent, prompt, "Écosystème Stratégique — Cartographie Complète")
    sauvegarder("ecosysteme_strategique", resultat, "strategie")
    return resultat


# ─── MENU PRINCIPAL ───────────────────────────────────────────────

def afficher_menu():
    print("\n" + "═" * 65)
    print("   AGENT PARTENARIATS & ÉCOSYSTÈME — Niveau VP Partnerships")
    print("═" * 65)
    print("  1. Identifier les partenaires idéaux (par type)")
    print("  2. Générer une proposition de partenariat complète")
    print("  3. Concevoir le programme revendeurs (Silver/Gold/Platinum)")
    print("  4. Stratégie de négociation partenariale")
    print("  5. Gérer et piloter un partenariat existant (QBR, scorecard)")
    print("  6. Cartographie de l'écosystème stratégique")
    print("  0. Quitter")
    print("═" * 65)


def main():
    print("\n  Initialisation de l'agent partenariats & écosystème...")

    while True:
        afficher_menu()
        choix = input("\n  Votre choix (0-6) : ").strip()

        if choix == "0":
            print("\n  Au revoir. Bons partenariats !\n")
            break

        elif choix == "1":
            type_partenariat = input(
                "  Type de partenariat (ex: technologie, intégrateurs, académique) : "
            ).strip()
            if type_partenariat:
                agent_identifier_partenaires(type_partenariat)
            else:
                print("  [!] Veuillez saisir un type de partenariat.")

        elif choix == "2":
            partenaire = input("  Nom du partenaire cible (ex: Capgemini, AWS) : ").strip()
            type_partenariat = input(
                "  Type de partenariat (ex: referral, white-label, co-vente) : "
            ).strip()
            if partenaire and type_partenariat:
                agent_proposition_partenariat(partenaire, type_partenariat)
            else:
                print("  [!] Veuillez renseigner tous les champs.")

        elif choix == "3":
            agent_programme_revendeurs()

        elif choix == "4":
            partenaire = input("  Partenaire (ex: Devoteam) : ").strip()
            nos_conditions = input(
                "  Nos conditions initiales (ex: 20% referral, durée 2 ans, non-exclusif) : "
            ).strip()
            leurs_conditions = input(
                "  Leurs conditions (ex: 30% referral, exclusivité sectorielle 3 ans) : "
            ).strip()
            if partenaire and nos_conditions and leurs_conditions:
                agent_negociation_partenariat(partenaire, nos_conditions, leurs_conditions)
            else:
                print("  [!] Veuillez renseigner tous les champs.")

        elif choix == "5":
            partenaire = input("  Partenaire à gérer (ex: Sopra Steria) : ").strip()
            performance = input(
                "  Performance actuelle (ex: 3 deals closés, 50K€ CA, peu actif en co-marketing) : "
            ).strip()
            if partenaire and performance:
                agent_gestion_partenaire(partenaire, performance)
            else:
                print("  [!] Veuillez renseigner tous les champs.")

        elif choix == "6":
            agent_ecosysteme_strategique()

        else:
            print("  [!] Option invalide. Choisissez entre 0 et 6.")


if __name__ == "__main__":
    main()
