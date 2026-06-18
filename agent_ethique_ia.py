"""
AGENT ÉTHIQUE IA — Boussole Morale de l'Entreprise
Évaluation éthique, détection de biais, conformité AI Act, impact sociétal.
La conscience artificielle au service d'une IA responsable.

Usage : python agent_ethique_ia.py
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

DOSSIER_SORTIE = "fichiers/ethique"
os.makedirs(DOSSIER_SORTIE, exist_ok=True)

ENTREPRISE = """
Raison sociale  : AgentClaude Solutions SAS
Activité        : Développement et déploiement d'agents IA autonomes pour entreprises
Engagement      : IA responsable, transparente et au service du bien commun
"""


# ─── UTILITAIRES ──────────────────────────────────────────────

def creer_agent(instructions, temperature=0.3):
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
    """Sauvegarde le document dans fichiers/ethique/ et retourne le chemin."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_propre = nom_fichier.replace(" ", "_").replace("/", "-")
    chemin = os.path.join(DOSSIER_SORTIE, f"{horodatage}_{nom_propre}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"\n  Document sauvegardé → {chemin}")
    return chemin


# ─── AGENT 1 : AUDIT ÉTHIQUE ──────────────────────────────────

def agent_audit_ethique(decision_ou_produit):
    """
    Évaluation d'impact éthique avant toute décision majeure.
    Analyse 8 dimensions éthiques avec scores, signaux d'alerte et mitigations.

    Args:
        decision_ou_produit : Description de la décision ou du produit à évaluer
    """
    incrementer_stat("agent_audit_ethique")

    agent = creer_agent(
        """Tu es un expert en éthique de l'intelligence artificielle, philosophe des technologies
et conseiller en responsabilité numérique. Tu combines la rigueur analytique de la philosophie
morale avec une connaissance approfondie des enjeux techniques de l'IA.

Tu évalues les décisions et produits liés à l'IA selon 8 dimensions éthiques fondamentales :
équité, transparence, vie privée, autonomie, bienfaisance, non-malfaisance, justice et responsabilité.

Ton analyse est lucide, impartiale et courageuse. Tu identifies les risques que d'autres préfèrent ignorer.
Tu proposes des mitigations concrètes et réalisables. Ton travail protège l'entreprise, les utilisateurs
et la société.
"""
    )

    prompt = f"""Conduis un audit éthique complet de la décision ou du produit suivant :

OBJET DE L'AUDIT : {decision_ou_produit}
DATE : {datetime.now().strftime("%d/%m/%Y")}
ORGANISATION : AgentClaude Solutions SAS

Produis un rapport d'audit éthique structuré selon les 8 dimensions ci-dessous.
Pour chaque dimension, attribue un score de 0 (critique) à 10 (exemplaire) avec justification.

══════════════════════════════════════════════════════════════
DIMENSION 1 — ÉQUITÉ (Score /10)
══════════════════════════════════════════════════════════════
- Quels biais potentiels ce système ou cette décision introduit-il ?
- Quels groupes pourraient être désavantagés (genre, âge, origine, revenu, culture, langue) ?
- Les données d'entraînement ou les critères de décision sont-ils représentatifs ?
- Des mécanismes de correction des biais sont-ils prévus ?

══════════════════════════════════════════════════════════════
DIMENSION 2 — TRANSPARENCE (Score /10)
══════════════════════════════════════════════════════════════
- Le système est-il explicable à un utilisateur non technique ?
- Les décisions automatisées peuvent-elles être auditées et contestées ?
- Le niveau de confiance et les limites du système sont-ils communiqués clairement ?
- Existe-t-il une documentation technique accessible ?

══════════════════════════════════════════════════════════════
DIMENSION 3 — VIE PRIVÉE (Score /10)
══════════════════════════════════════════════════════════════
- Le principe de minimisation des données est-il respecté ?
- Quelles données personnelles sont collectées, pour quelle durée, avec quelle justification ?
- Des données peuvent-elles être utilisées à des fins non consenties (re-identification, profilage) ?
- Les mesures de protection (chiffrement, pseudonymisation, accès restreint) sont-elles suffisantes ?

══════════════════════════════════════════════════════════════
DIMENSION 4 — AUTONOMIE (Score /10)
══════════════════════════════════════════════════════════════
- L'utilisateur conserve-t-il un réel contrôle sur ses décisions et ses données ?
- Le système crée-t-il une dépendance ou une perte d'autonomie cognitive ?
- Existe-t-il un moyen clair de refuser, de corriger ou de se désengager ?
- Le design évite-t-il les dark patterns manipulateurs ?

══════════════════════════════════════════════════════════════
DIMENSION 5 — BIENFAISANCE (Score /10)
══════════════════════════════════════════════════════════════
- L'impact net sur les utilisateurs et la société est-il positif ?
- Quels bénéfices concrets ce système apporte-t-il ? Pour qui ?
- Le ratio bénéfices/coûts (financiers, sociaux, environnementaux) est-il favorable ?
- Le système contribue-t-il au progrès humain ou simplement au profit de l'entreprise ?

══════════════════════════════════════════════════════════════
DIMENSION 6 — NON-MALFAISANCE (Score /10)
══════════════════════════════════════════════════════════════
- Quels dommages potentiels ce système peut-il causer ?
- Scénarios de mésusage identifiés : qui pourrait abuser de ce système et comment ?
- Risques d'erreurs critiques (faux positifs/négatifs, hallucinations, défaillances) ?
- Des mécanismes de surveillance et de correction d'urgence sont-ils en place ?

══════════════════════════════════════════════════════════════
DIMENSION 7 — JUSTICE (Score /10)
══════════════════════════════════════════════════════════════
- Qui bénéficie de ce système ? Qui en supporte les coûts ou les risques ?
- Le système creuse-t-il ou réduit-il les inégalités existantes ?
- Les populations vulnérables (seniors, personnes en situation de précarité, non-technophiles) sont-elles protégées ?
- La valeur générée est-elle distribuée équitablement dans la chaîne (utilisateurs, travailleurs, société) ?

══════════════════════════════════════════════════════════════
DIMENSION 8 — RESPONSABILITÉ (Score /10)
══════════════════════════════════════════════════════════════
- Qui est responsable en cas de décision erronée ou de dommage causé par le système ?
- Existe-t-il une traçabilité des décisions prises par ou avec l'IA ?
- Des processus de recours et d'indemnisation sont-ils prévus pour les personnes lésées ?
- La gouvernance interne garantit-elle un contrôle humain effectif ?

══════════════════════════════════════════════════════════════
SYNTHÈSE ÉTHIQUE GLOBALE
══════════════════════════════════════════════════════════════

TABLEAU DE BORD DES SCORES :
| Dimension        | Score /10 | Niveau |
|------------------|-----------|--------|
(remplis ce tableau pour les 8 dimensions)

SCORE ÉTHIQUE GLOBAL : (moyenne pondérée sur 10)

SIGNAUX D'ALERTE CRITIQUES :
(liste les 3 à 5 risques les plus graves à adresser immédiatement)

MITIGATIONS OBLIGATOIRES AVANT DÉPLOIEMENT :
(mesures concrètes, responsable désigné, délai)

VERDICT ÉTHIQUE :
- FEU VERT : déploiement autorisé sans condition
- FEU ORANGE : déploiement conditionné aux mitigations listées
- FEU ROUGE : déploiement suspendu jusqu'à refonte substantielle

SIGNATURE DE L'AUDITEUR :
Date : {datetime.now().strftime("%d/%m/%Y")}
Auditeur : Agent Éthique IA — AgentClaude Solutions
"""

    contenu = executer_stream(agent, prompt, f"Audit Éthique — {decision_ou_produit[:60]}")
    sauvegarder_document(contenu, f"audit_ethique_{decision_ou_produit[:40].replace(' ', '_')}")
    return contenu


# ─── AGENT 2 : DÉTECTION DE BIAIS ─────────────────────────────

def agent_biais_detection(systeme_ia, donnees_description):
    """
    Détection et mitigation des biais dans un système IA.
    Analyse les biais potentiels, l'impact sur les groupes d'utilisateurs,
    propose des techniques de débiaisage et un rapport de transparence.

    Args:
        systeme_ia          : Description du système IA (fonctionnement, usage, données)
        donnees_description : Description des données utilisées (source, taille, représentativité)
    """
    incrementer_stat("agent_biais_detection")

    agent = creer_agent(
        """Tu es un chercheur spécialisé en équité algorithmique (algorithmic fairness) et en
détection de biais dans les systèmes d'intelligence artificielle.

Tu maîtrises les différents types de biais : biais de sélection, de confirmation, d'automation,
d'ancrage, de représentation, de mesure, d'historique et de déploiement.

Tu analyses les systèmes IA avec rigueur scientifique, identifies les groupes impactés,
proposes des métriques de fairness mesurables et des techniques de débiaisage éprouvées.
Tu génères des rapports de transparence que les clients peuvent lire et comprendre.
"""
    )

    prompt = f"""Conduis une analyse complète de détection et de mitigation des biais pour le système IA décrit.

SYSTÈME IA : {systeme_ia}
DONNÉES UTILISÉES : {donnees_description}
DATE : {datetime.now().strftime("%d/%m/%Y")}

══════════════════════════════════════════════════════════════
PARTIE 1 — INVENTAIRE DES BIAIS POTENTIELS
══════════════════════════════════════════════════════════════

Pour chaque type de biais, évalue sa probabilité (Faible/Moyenne/Élevée) et son impact potentiel :

BIAIS DE SÉLECTION
- Les données d'entraînement sur-représentent-elles certains groupes ?
- Des populations sont-elles absentes ou sous-représentées ?
- Comment ce biais se manifeste-t-il dans les prédictions ou décisions ?

BIAIS DE CONFIRMATION
- Le système est-il conçu ou entraîné à confirmer des hypothèses préexistantes ?
- Les critères d'évaluation favorisent-ils le statu quo au détriment de la diversité ?

BIAIS D'AUTOMATION
- Les utilisateurs font-ils trop confiance aux sorties du système sans vérification humaine ?
- Le système est-il présenté comme plus fiable qu'il ne l'est réellement ?

BIAIS D'ANCRAGE
- Les premières données ou décisions du système influencent-elles indûment les suivantes ?
- Y a-t-il un effet de boucle de rétroaction qui amplifie les biais initiaux ?

BIAIS SUPPLÉMENTAIRES IDENTIFIÉS
(biais d'historique, de mesure, de représentation, de déploiement contextuel)

══════════════════════════════════════════════════════════════
PARTIE 2 — IMPACT SUR LES GROUPES D'UTILISATEURS
══════════════════════════════════════════════════════════════

Analyse l'impact différentiel sur les groupes suivants :
- Genre et identité de genre
- Origine ethnique et culturelle
- Âge (seniors, jeunes adultes, mineurs)
- Niveau socio-économique et accès technologique
- Langue et culture (non-francophones, non-occidentaux)
- Personnes en situation de handicap
- Géographie (urbain/rural, pays développés/émergents)

Pour chaque groupe potentiellement impacté :
- Nature du désavantage observé ou prévisible
- Mécanisme par lequel le biais produit cet effet
- Gravité de l'impact (mineur / significatif / grave)

══════════════════════════════════════════════════════════════
PARTIE 3 — TECHNIQUES DE DÉBIAISAGE RECOMMANDÉES
══════════════════════════════════════════════════════════════

PRÉ-TRAITEMENT (avant entraînement)
- Techniques de rééchantillonnage des données
- Augmentation synthétique des données sous-représentées
- Révision des critères de labellisation

DANS LE MODÈLE (pendant l'entraînement)
- Contraintes d'équité intégrées dans la fonction de perte
- Régularisation pour réduire la sensibilité aux attributs protégés
- Architectures favorisant l'équité

POST-TRAITEMENT (après prédiction)
- Calibration des seuils de décision par groupe
- Égalisation des taux d'erreur (égalité des chances, parité démographique)
- Mécanismes de recours humain pour les cas limites

══════════════════════════════════════════════════════════════
PARTIE 4 — MÉTRIQUES DE FAIRNESS À SURVEILLER EN PRODUCTION
══════════════════════════════════════════════════════════════

Génère un tableau de bord de métriques :
| Métrique | Définition | Valeur cible | Fréquence de mesure |
(liste 8 à 10 métriques pertinentes pour ce système spécifique)

Explique comment interpréter chaque métrique et à partir de quel seuil déclencher une alerte.

══════════════════════════════════════════════════════════════
PARTIE 5 — RAPPORT DE TRANSPARENCE CLIENT
══════════════════════════════════════════════════════════════

Rédige un résumé de transparence en langage accessible (non technique) destiné aux clients
et utilisateurs finaux du système. Ce document doit :
- Expliquer ce que fait le système et comment
- Reconnaître honnêtement les limites et biais résiduels connus
- Décrire les mesures prises pour les minimiser
- Indiquer comment signaler un problème ou contester une décision
- Être signé et daté par l'équipe éthique

Ton : honnête, accessible, rassurant sans être complaisant.
"""

    contenu = executer_stream(agent, prompt, f"Analyse Biais — {systeme_ia[:50]}")
    sauvegarder_document(contenu, f"biais_{systeme_ia[:40].replace(' ', '_')}")
    return contenu


# ─── AGENT 3 : CONFORMITÉ AI ACT EU ───────────────────────────

def agent_conformite_ai_act():
    """
    Vérificateur de conformité au Règlement IA européen (AI Act).
    Classifie les systèmes IA par niveau de risque, génère la documentation
    requise, suit les échéances et produit une feuille de route de conformité.
    """
    incrementer_stat("agent_conformite_ai_act")

    agent = creer_agent(
        """Tu es un expert juridique spécialisé dans le Règlement européen sur l'intelligence artificielle
(AI Act — Règlement (UE) 2024/1689), entré en vigueur le 1er août 2024.

Tu maîtrises parfaitement :
- La classification des systèmes IA par niveau de risque (inacceptable, élevé, limité, minimal)
- Les obligations documentaires pour chaque catégorie
- Les calendriers d'application progressifs (2024-2027)
- Les sanctions encourues (jusqu'à 35 millions € ou 7% du CA mondial)
- Les liens avec le RGPD, la directive sur la responsabilité en matière d'IA, et les normes CEN/ISO

Tu génères des analyses de conformité précises, pragmatiques et directement actionnables
pour des PME françaises développant des agents IA.
"""
    )

    prompt = f"""Génère un audit de conformité complet au Règlement IA européen (AI Act) pour AgentClaude Solutions.

ORGANISATION : AgentClaude Solutions SAS
ACTIVITÉ : Développement d'agents IA autonomes pour entreprises (facturation, juridique, RH, commercial, etc.)
DATE : {datetime.now().strftime("%d/%m/%Y")}

══════════════════════════════════════════════════════════════
PARTIE 1 — CLASSIFICATION DES SYSTÈMES IA PAR NIVEAU DE RISQUE
══════════════════════════════════════════════════════════════

Pour chaque catégorie de risque, liste les systèmes d'AgentClaude Solutions concernés :

RISQUE INACCEPTABLE (art. 5) — INTERDITS
Vérifie si certains usages pourraient tomber dans cette catégorie :
- Notation sociale par les pouvoirs publics
- Manipulation subliminale
- Exploitation des vulnérabilités de groupes spécifiques
- Surveillance biométrique de masse en temps réel
- Inférence d'émotions sur le lieu de travail ou dans l'éducation (sauf exceptions)
→ Verdict pour AgentClaude Solutions : quels usages à proscrire absolument ?

RISQUE ÉLEVÉ (Annexe III) — OBLIGATIONS STRICTES
Analyse si les agents IA d'AgentClaude entrent dans ces domaines :
- Emploi et gestion des travailleurs (recrutement, évaluation, licenciement)
- Services essentiels (crédit, assurance, éducation, soins de santé)
- Justice et processus démocratiques
- Services répressifs et contrôle migratoire
→ Liste des agents potentiellement à risque élevé et obligations applicables

RISQUE LIMITÉ — OBLIGATIONS DE TRANSPARENCE
- Chatbots et agents interactifs : obligation d'informer l'utilisateur qu'il interagit avec une IA
- Génération de deepfakes : obligation de marquage
- Systèmes de recommandation : information sur la logique utilisée
→ Actions requises pour les agents d'AgentClaude Solutions

RISQUE MINIMAL — AUCUNE OBLIGATION SPÉCIFIQUE
- Filtres anti-spam, jeux vidéo IA, etc.
→ Confirme les systèmes qui n'engendrent pas d'obligations particulières

══════════════════════════════════════════════════════════════
PARTIE 2 — DOCUMENTATION REQUISE PAR CATÉGORIE
══════════════════════════════════════════════════════════════

Pour les systèmes à RISQUE ÉLEVÉ, génère la liste des documents obligatoires :

DOCUMENTATION TECHNIQUE (art. 11)
- Description du système et de ses composants
- Architecture et processus de développement
- Données d'entraînement, de validation et de test
- Performance attendue et métriques de précision
- Robustesse, sécurité et cybersécurité

ÉVALUATION DE CONFORMITÉ (art. 43)
- Processus interne vs organisme notifié
- Registre UE des systèmes IA à risque élevé (art. 51)
- Déclaration de conformité UE

PROCÉDURES DE SURVEILLANCE HUMAINE (art. 14)
- Identification des points de contrôle humain obligatoires
- Formation et compétences requises des opérateurs
- Procédures d'intervention et de désengagement d'urgence
- Traçabilité des décisions (logs automatiques)

══════════════════════════════════════════════════════════════
PARTIE 3 — CALENDRIER DES ÉCHÉANCES CLÉS (2024-2027)
══════════════════════════════════════════════════════════════

Génère un tableau de bord chronologique :

| Date | Échéance | Obligation | Applicable à AgentClaude ? |
|------|----------|------------|----------------------------|
(remplis ce tableau avec toutes les dates critiques de l'AI Act)

Notamment :
- Février 2025 : interdictions systèmes à risque inacceptable
- Août 2025 : codes de pratique modèles IA à usage général (GPAI)
- Août 2026 : obligations systèmes à risque élevé (Annexe III)
- Août 2027 : extension aux systèmes IA intégrés dans produits existants

══════════════════════════════════════════════════════════════
PARTIE 4 — FEUILLE DE ROUTE DE CONFORMITÉ PRIORISÉE
══════════════════════════════════════════════════════════════

Génère un plan d'action structuré :

ACTIONS IMMÉDIATES (maintenant — 3 mois)
- Mesures critiques à prendre sans délai

ACTIONS À MOYEN TERME (3 — 12 mois)
- Mise en conformité des systèmes à risque élevé

ACTIONS À LONG TERME (12 — 36 mois)
- Gouvernance IA mature, certifications, audits externes

Pour chaque action :
- Description précise de l'action
- Responsable interne suggéré (direction technique, juridique, DPO...)
- Ressources nécessaires (estimation en jours/homme)
- Indicateur de succès mesurable

══════════════════════════════════════════════════════════════
PARTIE 5 — RISQUES JURIDIQUES ET SANCTIONS ENCOURUES
══════════════════════════════════════════════════════════════

- Infraction à l'interdiction de systèmes risque inacceptable : jusqu'à 35 M€ ou 7% CA mondial
- Non-conformité système à risque élevé : jusqu'à 15 M€ ou 3% CA mondial
- Fourniture d'informations inexactes aux autorités : jusqu'à 7,5 M€ ou 1% CA mondial

Évalue l'exposition au risque actuelle d'AgentClaude Solutions et les priorités de mise en conformité.
"""

    contenu = executer_stream(agent, prompt, "Conformité AI Act Européen — AgentClaude Solutions")
    sauvegarder_document(contenu, "conformite_AI_Act_EU")
    return contenu


# ─── AGENT 4 : IMPACT SOCIÉTAL ────────────────────────────────

def agent_impact_societale(projet_ia):
    """
    Évaluation d'impact sociétal d'un projet IA.
    Analyse emploi, environnement, inclusion économique, impact culturel
    et implications sociétales à long terme.

    Args:
        projet_ia : Description du projet IA à évaluer
    """
    incrementer_stat("agent_impact_societale")

    agent = creer_agent(
        """Tu es un économiste spécialisé dans l'impact des technologies sur la société,
l'emploi et l'environnement. Tu combines rigueur académique et sens des responsabilités.

Tu analyses les projets d'intelligence artificielle sous l'angle de leur impact sociétal global :
effets sur l'emploi, coût environnemental, inclusion numérique, diversité culturelle
et implications pour les générations futures.

Tu refuses l'angélisme technologique comme le catastrophisme stérile. Tu évalues les faits,
tu identifies les compromis réels, et tu proposes des engagements concrets pour maximiser
l'impact positif et minimiser les dommages.
"""
    )

    prompt = f"""Réalise une évaluation d'impact sociétal complète et honnête du projet IA décrit.

PROJET : {projet_ia}
DATE : {datetime.now().strftime("%d/%m/%Y")}
PORTEUR : AgentClaude Solutions SAS

══════════════════════════════════════════════════════════════
DIMENSION 1 — IMPACT SUR L'EMPLOI
══════════════════════════════════════════════════════════════

EMPLOIS CRÉÉS
- Nouveaux métiers générés directement par ce projet
- Emplois induits (maintenance, formation, audit, supervision)
- Compétences émergentes valorisées sur le marché du travail

EMPLOIS DÉPLACÉS OU TRANSFORMÉS
- Tâches automatisées : quels postes sont directement impactés ?
- Estimation quantitative : combien d'ETP (équivalents temps plein) concernés ?
- Profils les plus vulnérables à l'automatisation dans ce contexte
- Délai de transition estimé

ANALYSE NETTE
- Bilan emplois créés vs emplois déplacés
- Qualité des emplois créés vs déplacés (rémunération, conditions, sens)
- Recommandations pour accompagner la transition (formation, reclassement)

══════════════════════════════════════════════════════════════
DIMENSION 2 — IMPACT ENVIRONNEMENTAL
══════════════════════════════════════════════════════════════

COÛT CARBONE DES APPELS API
- Estimation de la consommation énergétique par requête (ordre de grandeur)
- Projection annuelle selon le volume d'usage estimé
- Comparaison avec l'équivalent humain de la même tâche
- Stratégies d'optimisation : batching, caching, modèles plus légers, green hosting

EMPREINTE NUMÉRIQUE GLOBALE
- Données stockées : coût énergétique du stockage
- Infrastructure cloud : régions utilisées, mix énergétique des data centers
- Durée de vie des équipements (obsolescence programmée des terminaux)

ENGAGEMENTS ENVIRONNEMENTAUX POSSIBLES
- Compensation carbone des appels API
- Choix de fournisseurs cloud à énergie renouvelable
- Objectifs de réduction de l'empreinte année par année

══════════════════════════════════════════════════════════════
DIMENSION 3 — INCLUSION ÉCONOMIQUE
══════════════════════════════════════════════════════════════

QUI A ACCÈS À CE SYSTÈME ?
- Modèle économique : le prix exclut-il des populations ou des entreprises ?
- Barrières techniques à l'accès (équipement, connexion, compétences numériques)
- Langues supportées : l'outil est-il accessible aux non-francophones / non-anglophones ?
- PME vs grandes entreprises : qui bénéficie le plus ?

FRACTURE NUMÉRIQUE
- Impact sur les entreprises qui ne peuvent pas se permettre ce type d'outil
- Risque de creusement des inégalités entre entreprises technophiles et autres
- Propositions pour démocratiser l'accès (offres freemium, partenariats publics, etc.)

══════════════════════════════════════════════════════════════
DIMENSION 4 — IMPACT CULTUREL
══════════════════════════════════════════════════════════════

BIAIS LINGUISTIQUES ET CULTURELS
- Les modèles IA utilisés sont-ils entraînés principalement sur des données anglophones/occidentales ?
- Quelles cultures, valeurs ou perspectives sont sur-représentées dans les sorties ?
- Impact sur la diversité des approches, pratiques professionnelles et modèles de pensée

HOMOGÉNÉISATION DES PRATIQUES
- Ce système peut-il contribuer à l'uniformisation des façons de travailler ?
- Perte potentielle de savoir-faire locaux, artisanaux ou contextuels
- Comment préserver la diversité des approches tout en bénéficiant de l'IA ?

══════════════════════════════════════════════════════════════
DIMENSION 5 — IMPLICATIONS SOCIÉTALES À LONG TERME
══════════════════════════════════════════════════════════════

SCÉNARIOS 2030-2040
- Scénario optimiste : comment ce projet contribue-t-il à une société meilleure ?
- Scénario pessimiste : quels risques systémiques si ce type d'outil se généralise ?
- Scénario probable : réalité nuancée entre les deux

EFFETS DE SECOND ORDRE
- Conséquences imprévues possibles de la généralisation de cet outil
- Effets de réseau et risques de dépendance systémique
- Concentration du pouvoir économique : qui contrôle ces technologies ?

══════════════════════════════════════════════════════════════
SYNTHÈSE — RAPPORT D'IMPACT ÉQUILIBRÉ
══════════════════════════════════════════════════════════════

BILAN SOCIÉTAL GLOBAL (sur 10) : ___/10

ENGAGEMENTS DE MITIGATION D'AgentClaude Solutions :
(liste 5 à 8 engagements concrets, mesurables et vérifiables)

INDICATEURS DE SUIVI SOCIÉTAL :
(métriques à mesurer annuellement pour évaluer l'impact réel)

Date d'évaluation : {datetime.now().strftime("%d/%m/%Y")}
"""

    contenu = executer_stream(agent, prompt, f"Impact Sociétal — {projet_ia[:50]}")
    sauvegarder_document(contenu, f"impact_societale_{projet_ia[:40].replace(' ', '_')}")
    return contenu


# ─── AGENT 5 : CHARTE ÉTHIQUE ─────────────────────────────────

def agent_charte_ethique():
    """
    Génère une Charte Éthique IA complète pour l'entreprise.
    Définit les principes, les lignes rouges, les droits des clients,
    les politiques de transparence et les processus de gouvernance éthique.
    """
    incrementer_stat("agent_charte_ethique")

    agent = creer_agent(
        f"""Tu es un expert en gouvernance d'entreprise, éthique des affaires et responsabilité
numérique. Tu as rédigé des chartes éthiques pour des entreprises tech de premier plan.

Tu crois profondément que l'éthique n'est pas un frein à l'innovation mais son meilleur
accélérateur : les clients enterprise font confiance aux entreprises dont les valeurs sont
claires, publiques et respectées. Une charte éthique bien rédigée est un avantage concurrentiel.

Tu rédiges pour AgentClaude Solutions une charte qui soit à la fois aspirationnelle et concrète :
des engagements que l'entreprise peut réellement tenir, pas de la communication creuse.

Entreprise : AgentClaude Solutions SAS
{ENTREPRISE}
"""
    )

    prompt = f"""Rédige la Charte Éthique IA complète d'AgentClaude Solutions.

DATE D'ADOPTION : {datetime.now().strftime("%d/%m/%Y")}

Ce document doit être un texte fondateur, écrit à la première personne du pluriel ("Nous"),
qui engage l'entreprise durablement. Il sera publié sur le site web, partagé avec les clients
enterprise et intégré dans tous les contrats commerciaux.

══════════════════════════════════════════════════════════════
PRÉAMBULE — NOTRE VISION DE L'IA RESPONSABLE
══════════════════════════════════════════════════════════════
(3 paragraphes : pourquoi cette charte, ce en quoi nous croyons, notre engagement de long terme)

══════════════════════════════════════════════════════════════
CHAPITRE 1 — NOS 10 PRINCIPES FONDATEURS
══════════════════════════════════════════════════════════════
Rédige 10 principes, chacun avec :
- Un titre court et mémorable
- Une déclaration d'engagement (2-3 phrases)
- Une illustration concrète dans notre activité quotidienne

Les principes doivent couvrir : transparence, équité, vie privée, autonomie utilisateur,
supervision humaine, bénéfice sociétal, responsabilité, durabilité environnementale,
inclusion et amélioration continue.

══════════════════════════════════════════════════════════════
CHAPITRE 2 — NOS LIGNES ROUGES ABSOLUES
══════════════════════════════════════════════════════════════
Ce que nous ne construirons JAMAIS, quels que soient le client, le prix ou la pression commerciale.

Liste 8 à 10 lignes rouges absolues, rédigées fermement :
(exemples : systèmes de surveillance de masse, outils de manipulation psychologique,
armes autonomes, discrimination algorithmique délibérée, etc.)

Pour chaque ligne rouge :
- La description précise de ce qui est interdit
- La raison éthique fondamentale
- Ce que nous ferons si un client le demande (procédure de refus)

══════════════════════════════════════════════════════════════
CHAPITRE 3 — DÉCLARATION DES DROITS DES DONNÉES CLIENTS
══════════════════════════════════════════════════════════════
Un texte clair et accessible listant les droits garantis à tous nos clients :
- Droit à la transparence algorithmique
- Droit à l'explication de toute décision automatisée
- Droit à la portabilité et à la suppression de leurs données
- Droit à un interlocuteur humain
- Droit de contester et faire corriger les résultats
- Droit à l'audit de leurs systèmes déployés
- Droit à une IA qui ne ment pas sur sa nature

══════════════════════════════════════════════════════════════
CHAPITRE 4 — POLITIQUE DE TRANSPARENCE ALGORITHMIQUE
══════════════════════════════════════════════════════════════
- Ce que nous documentons et publions sur nos systèmes IA
- Quelles informations sont accessibles aux clients vs. confidentielles
- Notre politique vis-à-vis des modèles tiers utilisés (OpenAI, Google, Anthropic, etc.)
- Comment nous communiquons les mises à jour, les limitations et les incidents
- Notre approche des "model cards" et fiches système

══════════════════════════════════════════════════════════════
CHAPITRE 5 — EXIGENCES DE SUPERVISION HUMAINE
══════════════════════════════════════════════════════════════
- Dans quels cas un humain doit obligatoirement valider avant action
- Formation minimale requise pour opérer nos agents IA
- Procédures d'escalade et de désengagement d'urgence
- Comment nous aidons nos clients à maintenir le contrôle

══════════════════════════════════════════════════════════════
CHAPITRE 6 — PROCESSUS DE RÉVISION ÉTHIQUE INTERNE
══════════════════════════════════════════════════════════════
- Qui siège au Comité d'Éthique IA (profils requis : technique, juridique, société civile...)
- Quand un audit éthique est-il déclenché ? (nouveaux produits, nouvelles données, partenariats...)
- Fréquence des révisions de la charte (annuelle minimum)
- Comment les employés peuvent-ils soulever des préoccupations éthiques ?

══════════════════════════════════════════════════════════════
CHAPITRE 7 — PROTECTION DES LANCEURS D'ALERTE
══════════════════════════════════════════════════════════════
- Garanties offertes aux employés et partenaires qui signalent des violations éthiques
- Canal de signalement anonyme
- Protection contre les représailles
- Délai d'instruction des signalements

══════════════════════════════════════════════════════════════
CHAPITRE 8 — ENGAGEMENT D'AUDIT ÉTHIQUE ANNUEL
══════════════════════════════════════════════════════════════
- Engagement de publier un rapport éthique annuel
- Ce que ce rapport contiendra (incidents, progrès, manquements reconnus, objectifs)
- Processus de vérification externe (auditeur indépendant ou organisme tiers)
- Comment les clients peuvent accéder à ce rapport

══════════════════════════════════════════════════════════════
SIGNATURES ET ENTRÉE EN VIGUEUR
══════════════════════════════════════════════════════════════

Clôture solennelle avec :
- Date d'adoption
- Engagement de révision annuelle
- Invitation aux parties prenantes à nous tenir responsables de ces engagements

Ton : grave, sincère, courageux. Pas de langue de bois. Ces engagements doivent faire peur
à un concurrent sans scrupule et rassurer un client enterprise exigeant.
"""

    contenu = executer_stream(agent, prompt, "Charte Éthique IA — AgentClaude Solutions")
    sauvegarder_document(contenu, "charte_ethique_ia_agentclaude")
    return contenu


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def menu():
    print("\n" + "═" * 64)
    print("  AGENT ÉTHIQUE IA — AgentClaude Solutions")
    print("  La conscience morale de l'intelligence artificielle")
    print("═" * 64)

    while True:
        print("\n  1. Audit éthique d'une décision ou d'un produit (8 dimensions)")
        print("  2. Détection et mitigation des biais dans un système IA")
        print("  3. Conformité AI Act européen — analyse et feuille de route")
        print("  4. Évaluation d'impact sociétal d'un projet IA")
        print("  5. Générer la Charte Éthique IA de l'entreprise")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  L'éthique est une pratique quotidienne, pas un document.\n")
            break

        elif choix == "1":
            print("\n  ─── Audit Éthique — 8 Dimensions ───")
            print("  Décrivez la décision, le produit ou le système à évaluer :")
            decision = input("  → ").strip()
            if decision:
                agent_audit_ethique(decision)
            else:
                print("  La description est obligatoire.")

        elif choix == "2":
            print("\n  ─── Détection de Biais ───")
            systeme = input("  Description du système IA → ").strip()
            donnees = input("  Description des données utilisées → ").strip()
            if systeme and donnees:
                agent_biais_detection(systeme, donnees)
            else:
                print("  Tous les champs sont obligatoires.")

        elif choix == "3":
            print("\n  ─── Conformité AI Act Européen ───")
            confirmation = input("  Lancer l'analyse de conformité AI Act ? (o/n) → ").strip().lower()
            if confirmation == "o":
                agent_conformite_ai_act()

        elif choix == "4":
            print("\n  ─── Impact Sociétal ───")
            print("  Décrivez le projet IA à évaluer :")
            projet = input("  → ").strip()
            if projet:
                agent_impact_societale(projet)
            else:
                print("  La description du projet est obligatoire.")

        elif choix == "5":
            print("\n  ─── Génération de la Charte Éthique IA ───")
            confirmation = input("  Générer la Charte Éthique complète ? (o/n) → ").strip().lower()
            if confirmation == "o":
                agent_charte_ethique()

        else:
            print("  Choix invalide. Entrez un chiffre entre 0 et 5.")


if __name__ == "__main__":
    menu()
