"""
AGENT JURIDIQUE AUTONOME
Génère des documents juridiques professionnels pour AgentClaude Solutions.
Contrats clients, NDA, CGV, audits RGPD, mentions légales.

Usage : python agent_juridique.py
"""

import os
import sys
import google.generativeai as genai
from datetime import datetime
from memoire import incrementer_stat

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Variable d'environnement GEMINI_API_KEY non définie.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

DOSSIER_SORTIE = "fichiers/juridique"
os.makedirs(DOSSIER_SORTIE, exist_ok=True)

ENTREPRISE = """
Raison sociale  : AgentClaude Solutions SAS
Activité        : Développement et déploiement d'agents IA autonomes pour entreprises
SIREN           : [À compléter]
Siège social    : [Adresse à compléter], France
Représentant    : [Dirigeant à compléter]
Email contact   : contact@agentclaude.fr
"""


# ─── UTILITAIRES ──────────────────────────────────────────────

def creer_agent(instructions, temperature=0.2):
    """Crée un modèle Gemini avec les instructions système données."""
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=4096,
        ),
    )


def executer_stream(model, prompt, label):
    """Exécute une requête en streaming et affiche le résultat."""
    print(f"\n{'─' * 64}")
    print(f"  ► {label}")
    print(f"{'─' * 64}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur de génération : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder_document(contenu, nom_fichier):
    """Sauvegarde le document dans fichiers/juridique/ et retourne le chemin."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_propre = nom_fichier.replace(" ", "_").replace("/", "-")
    chemin = os.path.join(DOSSIER_SORTIE, f"{horodatage}_{nom_propre}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"\n  Document sauvegardé → {chemin}")
    return chemin


# ─── AGENT 1 : CONTRAT DE PRESTATION DE SERVICES ─────────────

def agent_contrat_client(client, services, montant):
    """
    Génère un contrat de prestation de services complet.

    Args:
        client  : Nom complet ou raison sociale du client
        services: Description des services fournis
        montant : Montant total de la prestation (ex: "12 000 € HT")
    """
    incrementer_stat("agent_contrat_client")

    agent = creer_agent(
        f"""Tu es un juriste spécialisé en droit des nouvelles technologies et des contrats B2B.
Tu rédiges des contrats de prestation de services pour une société française spécialisée en agents IA.

Informations sur le prestataire :
{ENTREPRISE}

Tu dois produire un contrat de prestation complet, rigoureux et conforme au droit français.
Le document doit être directement utilisable, avec toutes les clauses rédigées intégralement.
Utilise un style juridique professionnel, précis, et sans ambiguïté.
"""
    )

    prompt = f"""Rédige un contrat de prestation de services complet entre AgentClaude Solutions (prestataire)
et le client indiqué ci-dessous.

CLIENT : {client}
SERVICES : {services}
MONTANT : {montant}
DATE : {datetime.now().strftime("%d/%m/%Y")}

Le contrat doit contenir obligatoirement les sections suivantes, toutes rédigées intégralement :

1. PARTIES — identification complète du prestataire et du client
2. OBJET DU CONTRAT — description précise de la mission
3. PRESTATIONS DÉTAILLÉES — liste des livrables, délais, modalités d'exécution
4. PRIX ET MODALITÉS DE PAIEMENT — montant HT/TTC, échéancier, conditions de règlement, pénalités de retard
5. DURÉE DU CONTRAT — date de début, durée, renouvellement
6. PROPRIÉTÉ INTELLECTUELLE — le code source, les agents IA et tous les livrables développés
   spécifiquement pour le client lui appartiennent intégralement après paiement complet ;
   AgentClaude Solutions conserve ses outils et méthodes génériques préexistants
7. CONFIDENTIALITÉ — obligations réciproques de confidentialité pendant et après le contrat
8. PROTECTION DES DONNÉES PERSONNELLES (RGPD) — rôles respectifs (responsable de traitement /
   sous-traitant), obligations du sous-traitant, registre des traitements, mesures de sécurité,
   durée de conservation, droit de résiliation en cas de manquement
9. RÉSILIATION — conditions de résiliation anticipée, préavis, conséquences financières
10. LIMITATION DE RESPONSABILITÉ — plafond de responsabilité, exclusions, force majeure
11. DROIT APPLICABLE ET JURIDICTION COMPÉTENTE — droit français, tribunal compétent

Terminer par les blocs de signature avec date, nom, qualité et emplacement de signature pour chacune des parties.
"""

    contenu = executer_stream(agent, prompt, f"Contrat Client — {client}")
    sauvegarder_document(contenu, f"contrat_{client}")
    return contenu


# ─── AGENT 2 : ACCORD DE CONFIDENTIALITÉ (NDA) ───────────────

def agent_nda(partie_a, partie_b, duree):
    """
    Génère un accord de confidentialité bilatéral.

    Args:
        partie_a : Première partie (ex: "AgentClaude Solutions")
        partie_b : Deuxième partie (ex: "Société XYZ")
        duree    : Durée de l'obligation (ex: "3 ans", "5 ans")
    """
    incrementer_stat("agent_nda")

    agent = creer_agent(
        """Tu es un juriste expert en propriété intellectuelle et en droit des contrats.
Tu rédiges des accords de confidentialité (NDA) bilatéraux pour des sociétés travaillant dans le domaine
de l'intelligence artificielle, des agents IA et des logiciels.
Ton style est juridique, précis, exhaustif et conforme au droit français et européen.
"""
    )

    prompt = f"""Rédige un accord de confidentialité (NDA) BILATÉRAL complet entre les deux parties suivantes :

PARTIE A : {partie_a}
PARTIE B : {partie_b}
DURÉE DE L'OBLIGATION DE CONFIDENTIALITÉ : {duree}
DATE : {datetime.now().strftime("%d/%m/%Y")}

L'accord doit impérativement couvrir les points suivants, intégralement rédigés :

1. PRÉAMBULE — contexte des échanges, raison d'être de l'accord
2. DÉFINITIONS — "Informations Confidentielles", "Partie Divulgatrice", "Partie Réceptrice",
   définitions élargies pour couvrir : algorithmes IA, données d'entraînement, architectures d'agents,
   prompts propriétaires, données clients, stratégie commerciale, code source, API keys, modèles IA
3. OBLIGATIONS DE CONFIDENTIALITÉ — portée bilatérale et symétrique, standard de protection
   (au moins égal à la protection de ses propres informations confidentielles, jamais inférieur
   à un standard de diligence raisonnable)
4. EXCLUSIONS — informations tombées dans le domaine public, informations connues avant divulgation,
   obtenues légalement de tiers, développées indépendamment
5. SECRETS DE COMMERCE EN IA — clause spécifique protégeant :
   les architectures d'agents, les chaînes de prompts, les workflows d'automatisation,
   les bases de données vectorielles, les modèles fine-tunés, les données d'évaluation propriétaires
6. RESTRICTIONS D'USAGE — usage limité aux seules fins de la collaboration envisagée,
   interdiction de reverse engineering, d'extraction, de copie partielle
7. RESTITUTION / DESTRUCTION — délais et modalités à la fin de la relation
8. DURÉE — entrée en vigueur, durée de l'accord, survie des obligations post-expiration ({duree})
9. SANCTIONS — réparation du préjudice, astreinte, mesures d'urgence (référé), dommages-intérêts
10. DISPOSITIONS GÉNÉRALES — droit applicable (droit français), juridiction compétente (Tribunal de Commerce de Paris),
    intégralité de l'accord, nullité partielle, modifications

Blocs de signature complets pour les deux parties.
"""

    contenu = executer_stream(agent, prompt, f"NDA — {partie_a} / {partie_b}")
    sauvegarder_document(contenu, f"NDA_{partie_a}_{partie_b}".replace(" ", "_"))
    return contenu


# ─── AGENT 3 : CONDITIONS GÉNÉRALES DE VENTE ─────────────────

def agent_cgv():
    """
    Génère des CGV complètes pour une société de services en agents IA.
    """
    incrementer_stat("agent_cgv")

    agent = creer_agent(
        f"""Tu es un juriste spécialisé en droit de la consommation, droit du numérique et droit des contrats B2B.
Tu rédiges des Conditions Générales de Vente (CGV) pour une société française proposant
des services d'intelligence artificielle et d'agents autonomes.

Société : AgentClaude Solutions SAS
{ENTREPRISE}

Les CGV doivent être conformes au Code civil, au Code de la consommation, à la loi pour
la Confiance dans l'Économie Numérique (LCEN), au RGPD et aux directives européennes applicables.
"""
    )

    prompt = f"""Rédige des Conditions Générales de Vente (CGV) complètes pour AgentClaude Solutions,
société proposant des services d'agents IA autonomes à des clients professionnels (B2B) et particuliers.

Date de mise à jour : {datetime.now().strftime("%d/%m/%Y")}

Les CGV doivent contenir les articles suivants, intégralement rédigés :

ARTICLE 1 — DÉFINITIONS
Définir : "Société", "Client", "Utilisateur", "Services", "Agent IA", "Livrable",
"Commande", "Devis", "Abonnement", "Contenu Généré par IA"

ARTICLE 2 — CHAMP D'APPLICATION ET ACCEPTATION
Applicabilité, primauté des CGV, acceptation électronique, mise à jour

ARTICLE 3 — DESCRIPTION DES SERVICES
Développement d'agents IA sur mesure, abonnements SaaS, formation, audit,
maintenance et support ; préciser les limites de chaque offre

ARTICLE 4 — COMMANDES ET DEVIS
Processus de commande, valeur du devis, bon de commande, confirmation,
droit de refus de commande

ARTICLE 5 — PRIX ET MODALITÉS DE PAIEMENT
Prix HT/TTC, TVA applicable, facturation, délais de paiement (30 jours nets),
pénalités de retard (taux légal + 10 points), indemnité forfaitaire de 40 €,
suspension de service en cas d'impayé

ARTICLE 6 — LIVRAISON ET EXÉCUTION DES SERVICES
Délais indicatifs, obligations du client (accès, données, retours),
réception des livrables, validation, recette

ARTICLE 7 — PROPRIÉTÉ INTELLECTUELLE
Droits sur les livrables développés sur mesure (cession au client après paiement intégral),
conservation des droits sur les outils et méthodes génériques du prestataire,
licence d'utilisation sur les composants tiers (open-source, API)

ARTICLE 8 — GARANTIES ET NIVEAUX DE SERVICE
Garantie de conformité, corrections de bugs (90 jours post-livraison),
exclusions (mauvaise utilisation, modifications non autorisées),
absence de garantie de résultats pour les sorties générées par IA

ARTICLE 9 — RESPONSABILITÉ
Plafond de responsabilité (montant des sommes versées sur les 12 derniers mois),
exclusion des dommages indirects, immatériels, pertes d'exploitation,
responsabilité spécifique liée aux sorties d'agents IA (hallucinations, biais)

ARTICLE 10 — DONNÉES PERSONNELLES ET RGPD
Qualité des parties (responsable / sous-traitant selon le cas),
données collectées, finalités, durée de conservation,
droits des personnes (accès, rectification, effacement, portabilité, opposition),
coordonnées du délégué à la protection des données ou du responsable RGPD,
transferts hors UE

ARTICLE 11 — DROIT DE RÉTRACTATION
Rappel du droit de rétractation de 14 jours pour les particuliers,
exclusions applicables aux services commencés avec accord préalable,
procédure et formulaire type

ARTICLE 12 — FORCE MAJEURE
Définition, notification, suspension, résiliation si > 30 jours

ARTICLE 13 — RÉSILIATION
Résiliation pour manquement (mise en demeure 15 jours), résiliation anticipée,
effets, restitution des données

ARTICLE 14 — LITIGES ET DROIT APPLICABLE
Droit français applicable, médiation de la consommation (pour les particuliers),
tentative de règlement amiable, juridiction compétente

ARTICLE 15 — DISPOSITIONS DIVERSES
Nullité partielle, non-renonciation, intégralité de l'accord, langue française
"""

    contenu = executer_stream(agent, prompt, "CGV — AgentClaude Solutions")
    sauvegarder_document(contenu, "CGV_AgentClaude_Solutions")
    return contenu


# ─── AGENT 4 : AUDIT DE CONFORMITÉ RGPD ──────────────────────

def agent_rgpd_audit(description_traitement):
    """
    Réalise un audit RGPD d'un traitement de données personnelles.

    Args:
        description_traitement : Description du traitement à auditer
    """
    incrementer_stat("agent_rgpd_audit")

    agent = creer_agent(
        """Tu es un Délégué à la Protection des Données (DPO) certifié CIPP/E,
expert en conformité RGPD et en droit du numérique européen.
Tu réalises des audits de conformité RGPD exhaustifs, structurés et directement actionnables.
Tu identifies les risques juridiques, les manquements et tu proposes un plan d'action priorisé.
Tu maîtrises le RGPD (Règlement UE 2016/679), les lignes directrices du CEPD,
les délibérations de la CNIL, et les sanctions en vigueur.
"""
    )

    prompt = f"""Réalise un audit de conformité RGPD complet du traitement de données décrit ci-dessous.

DESCRIPTION DU TRAITEMENT :
{description_traitement}

DATE D'AUDIT : {datetime.now().strftime("%d/%m/%Y")}
ORGANISATION : AgentClaude Solutions SAS

Produis un rapport d'audit structuré en plusieurs parties :

PARTIE 1 — CARTOGRAPHIE DU TRAITEMENT
- Identification de toutes les catégories de données personnelles traitées
  (données directement identifiantes, indirectement identifiantes, sensibles art. 9)
- Personnes concernées (employés, clients, prospects, utilisateurs finaux, tiers)
- Finalités explicites et finalités dérivées possibles
- Responsable(s) de traitement et sous-traitants impliqués
- Flux de données (collecte, stockage, transfert, suppression)

PARTIE 2 — BASES LÉGALES
- Base légale applicable pour chaque finalité (consentement, exécution contrat,
  obligation légale, intérêt vital, mission d'intérêt public, intérêt légitime)
- Évaluation de la validité et de la solidité de chaque base légale
- Risques identifiés si la base légale est insuffisante

PARTIE 3 — DURÉES DE CONSERVATION
- Durées recommandées par finalité et par type de données
- Référentiel CNIL et secteur applicable
- Procédures de purge et d'archivage recommandées
- Risques en cas de conservation excessive

PARTIE 4 — DROITS DES PERSONNES CONCERNÉES
- Droit d'information : mentions légales et politique de confidentialité (conformité)
- Droits exercés : accès, rectification, effacement ("droit à l'oubli"),
  limitation, portabilité, opposition, décision automatisée
- Processus de gestion des demandes (délais légaux : 1 mois, prorogeable 2 mois)
- Identification des lacunes dans les processus actuels

PARTIE 5 — OBLIGATION DE DÉSIGNATION D'UN DPO
- Évaluation du critère de désignation obligatoire (art. 37 RGPD) :
  organisme public / activité principale de surveillance à grande échelle /
  traitement à grande échelle de données sensibles art. 9-10
- Recommandation : DPO obligatoire / DPO recommandé / DPO non obligatoire
- Profil et missions du DPO si applicable

PARTIE 6 — ANALYSE D'IMPACT (DPIA/PIA)
- Critères de nécessité d'une DPIA (art. 35 RGPD + liste CNIL)
- Conclusion : DPIA obligatoire / recommandée / non requise avec justification
- Structure de la DPIA si requise

PARTIE 7 — MESURES DE SÉCURITÉ TECHNIQUES ET ORGANISATIONNELLES
- Mesures existantes identifiées dans la description
- Mesures manquantes et fortement recommandées :
  * Chiffrement (données en transit, données au repos)
  * Contrôle d'accès et authentification forte (MFA)
  * Journalisation et traçabilité
  * Pseudonymisation / anonymisation
  * Politique de sauvegarde et PRA
  * Formation et sensibilisation des équipes
  * Procédure de notification de violation (72h CNIL, communication aux personnes)

PARTIE 8 — CHECKLIST DE CONFORMITÉ RGPD
Tableau récapitulatif avec pour chaque point :
  - CONFORME / NON CONFORME / À VÉRIFIER
  - Risque associé (FAIBLE / MOYEN / ÉLEVÉ / CRITIQUE)

PARTIE 9 — PLAN D'ACTION PRIORISÉ
Liste numérotée des actions à mener, chacune avec :
  - Description de l'action
  - Priorité (P1 urgent < 1 mois / P2 important < 3 mois / P3 souhaitable < 6 mois)
  - Ressources nécessaires (juridique, technique, organisationnel)
  - Indicateur de succès

PARTIE 10 — RISQUES RÉSIDUELS ET SANCTIONS POTENTIELLES
- Principaux risques résiduels si aucune action n'est entreprise
- Sanctions CNIL encourues (avertissement, mise en demeure, amende jusqu'à 20 M€ ou 4% CA mondial)
- Exemples de sanctions CNIL comparables dans le secteur numérique
"""

    contenu = executer_stream(agent, prompt, f"Audit RGPD — {description_traitement[:60]}...")
    sauvegarder_document(contenu, "audit_RGPD")
    return contenu


# ─── AGENT 5 : MENTIONS LÉGALES SITE WEB ─────────────────────

def agent_mentions_legales(url):
    """
    Génère les mentions légales complètes pour un site web.

    Args:
        url : URL du site web (ex: "https://www.agentclaude.fr")
    """
    incrementer_stat("agent_mentions_legales")

    agent = creer_agent(
        f"""Tu es un juriste expert en droit du numérique, droit de la consommation
et protection des données personnelles.
Tu rédiges des mentions légales complètes, conformes à la LCEN (Loi pour la Confiance
dans l'Économie Numérique), au RGPD, à la directive ePrivacy et aux recommandations CNIL.

Société éditrice : AgentClaude Solutions SAS
{ENTREPRISE}
"""
    )

    prompt = f"""Rédige les mentions légales complètes pour le site web suivant :

URL DU SITE : {url}
DATE : {datetime.now().strftime("%d/%m/%Y")}
ÉDITEUR : AgentClaude Solutions SAS — société spécialisée en agents IA

Le document doit contenir les sections suivantes, intégralement rédigées :

1. ÉDITEUR DU SITE
   - Raison sociale, forme juridique, capital social
   - Adresse du siège social
   - SIREN / SIRET / RCS
   - Numéro de TVA intracommunautaire
   - Directeur de la publication
   - Email et téléphone de contact

2. HÉBERGEUR
   - Nom, raison sociale, adresse de l'hébergeur
   - Indiquer un hébergeur cloud réaliste (ex: OVHcloud, Scaleway, AWS Paris)
   - Contact de l'hébergeur

3. PROPRIÉTÉ INTELLECTUELLE
   - Droits sur le contenu du site (textes, images, logos, code, agents IA démontrés)
   - Interdiction de reproduction sans autorisation écrite
   - Marques déposées
   - Liens hypertextes : conditions d'autorisation et de refus
   - Contenu généré par IA : précisions sur la nature des démos

4. RESPONSABILITÉ ET LIMITATION
   - Exactitude et mise à jour des informations
   - Disponibilité du site (pas de garantie de continuité)
   - Liens vers des sites tiers (pas de responsabilité sur le contenu externe)
   - Virus et sécurité (responsabilité de l'utilisateur pour son système)

5. DONNÉES PERSONNELLES ET POLITIQUE DE CONFIDENTIALITÉ
   - Identité du responsable de traitement
   - Données collectées (formulaires, analytics, cookies, logs serveur)
   - Finalités du traitement
   - Base légale pour chaque finalité
   - Durées de conservation
   - Destinataires des données (prestataires, sous-traitants, pays tiers)
   - Droits des personnes (accès, rectification, effacement, portabilité,
     opposition, limitation, décision automatisée) avec procédure d'exercice
   - Droit de réclamation auprès de la CNIL (www.cnil.fr)
   - Coordonnées du responsable ou DPO

6. POLITIQUE DE COOKIES
   - Définition des cookies et traceurs
   - Cookies strictement nécessaires (liste)
   - Cookies analytiques / de mesure d'audience (Google Analytics, Matomo…)
   - Cookies de personnalisation et marketing (si applicable)
   - Durée de vie de chaque catégorie
   - Modalités de consentement et de retrait du consentement
   - Instructions pour paramétrer les navigateurs (Chrome, Firefox, Safari, Edge)
   - Opt-out des principaux outils d'analyse

7. DROIT APPLICABLE ET LITIGES
   - Droit français applicable
   - Médiation de la consommation (pour les particuliers) avec coordonnées d'un médiateur
   - Juridiction compétente pour les litiges B2B

8. MISE À JOUR DES MENTIONS LÉGALES
   - Date de dernière mise à jour
   - Clause de modification unilatérale avec notification
"""

    contenu = executer_stream(agent, prompt, f"Mentions Légales — {url}")
    sauvegarder_document(contenu, f"mentions_legales_{url.replace('https://', '').replace('/', '_')}")
    return contenu


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def menu():
    print("\n" + "═" * 64)
    print("  AGENT JURIDIQUE — AgentClaude Solutions")
    print("  Documents juridiques professionnels générés par IA")
    print("═" * 64)

    while True:
        print("\n  1. Contrat de prestation de services client")
        print("  2. Accord de confidentialité — NDA bilatéral")
        print("  3. Conditions Générales de Vente (CGV)")
        print("  4. Audit de conformité RGPD")
        print("  5. Mentions légales site web")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  Au revoir.\n")
            break

        elif choix == "1":
            print("\n  ─── Contrat de prestation de services ───")
            client = input("  Nom / Raison sociale du client → ").strip()
            services = input("  Description des services (ex: développement agent IA facturation) → ").strip()
            montant = input("  Montant de la prestation (ex: 15 000 € HT) → ").strip()
            if client and services and montant:
                agent_contrat_client(client, services, montant)
            else:
                print("  Tous les champs sont obligatoires.")

        elif choix == "2":
            print("\n  ─── Accord de confidentialité (NDA) ───")
            partie_a = input("  Partie A (ex: AgentClaude Solutions) → ").strip() or "AgentClaude Solutions"
            partie_b = input("  Partie B (nom de l'autre société) → ").strip()
            duree = input("  Durée de l'obligation (ex: 3 ans) → ").strip() or "3 ans"
            if partie_b:
                agent_nda(partie_a, partie_b, duree)
            else:
                print("  Le nom de la Partie B est obligatoire.")

        elif choix == "3":
            print("\n  ─── Génération des CGV AgentClaude Solutions ───")
            confirmation = input("  Générer les CGV complètes ? (o/n) → ").strip().lower()
            if confirmation == "o":
                agent_cgv()

        elif choix == "4":
            print("\n  ─── Audit RGPD ───")
            print("  Décrivez le traitement à auditer (collecte, stockage, usage des données) :")
            description = input("  → ").strip()
            if description:
                agent_rgpd_audit(description)
            else:
                print("  La description du traitement est obligatoire.")

        elif choix == "5":
            print("\n  ─── Mentions légales site web ───")
            url = input("  URL du site (ex: https://www.agentclaude.fr) → ").strip()
            if not url:
                url = "https://www.agentclaude.fr"
            agent_mentions_legales(url)

        else:
            print("  Choix invalide. Entrez un chiffre entre 0 et 5.")


if __name__ == "__main__":
    menu()
