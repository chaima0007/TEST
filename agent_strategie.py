import os
import json
import datetime
from google import genai
from google.genai import types
from memoire import incrementer_stat

MODEL = "gemini-2.0-flash"

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = _creer_model(MODEL)

ENTREPRISE = "AgentClaude Solutions"
DOMAINE = "solutions d'agents IA autonomes"
SECTEUR = "intelligence artificielle et automatisation"
GEOGRAPHIE = "Europe"


# ─────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────

def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def streamer(prompt: str) -> str:
    """Envoie le prompt au modèle en streaming et retourne le texte complet."""
    response = model.generate_content(prompt, stream=True)
    texte_complet = ""
    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            texte_complet += chunk.text
    print()
    return texte_complet


def sauvegarder(nom_fichier: str, contenu: str) -> str:
    """Sauvegarde le rapport dans fichiers/strategie/ avec horodatage."""
    dossier = "/home/user/TEST/fichiers/strategie"
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = f"{dossier}/{nom_fichier}_{horodatage}.txt"
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


# ─────────────────────────────────────────────
# Agent 1 – Plan Stratégique
# ─────────────────────────────────────────────

def agent_plan_strategique(horizon_ans: int, objectif: str) -> str:
    """Génère un plan stratégique complet sur N ans avec diagnostic, vision, axes et roadmap."""
    incrementer_stat("agent_plan_strategique")

    prompt = f"""Tu es un associé senior de McKinsey & Company, expert en stratégie d'entreprise pour les sociétés technologiques européennes.
Ta mission est de produire un plan stratégique de niveau boardroom pour {ENTREPRISE}, entreprise spécialisée en {DOMAINE}, opérant en {GEOGRAPHIE}.

Horizon de planification : {horizon_ans} ans
Objectif stratégique principal : {objectif}

Produis un plan stratégique exhaustif et opérationnel, structuré comme suit :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. DIAGNOSTIC STRATÉGIQUE (SWOT APPROFONDI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Forces internes (au moins 6 forces différenciantes) :
- Analyse des capacités technologiques distinctives
- Positionnement IP et propriété intellectuelle
- Compétences équipe et culture d'innovation
- Base clients et NPS estimé
- Structure de coûts et efficacité opérationnelle
- Réputation et marque sur le marché IA européen

Faiblesses internes (au moins 5 faiblesses critiques à adresser) :
- Gaps de capacités vs. leaders du marché
- Dépendances technologiques (cloud providers, LLMs tiers)
- Contraintes de financement et runway
- Maturité commerciale et couverture géographique
- Scalabilité des opérations

Opportunités externes (au moins 6 opportunités à saisir) :
- Tendances marché IA en Europe (taille, CAGR, segments)
- Réglementation favorable (AI Act : avantage compétitif pour les acteurs conformes)
- Consolidation sectorielle et cibles M&A potentielles
- Partenariats stratégiques (ESN, éditeurs, systémiers)
- Expansion géographique (DACH, Benelux, Ibérie, CEE)
- Nouveaux cas d'usage émergents (agents verticaux, AI workforce)

Menaces externes (au moins 5 menaces à mitiger) :
- Offensive des hyperscalers (Microsoft Copilot, Google Gemini, AWS Bedrock)
- Consolidation concurrentielle et levées de fonds concurrents
- Risques réglementaires RGPD et AI Act
- Pression tarifaire et commoditisation des LLMs
- Guerre des talents IA en Europe

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. VISION ET AMBITION CHIFFRÉE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Vision à {horizon_ans} ans (une phrase inspirante et mémorable)
- Mission statement opérationnel
- Ambition chiffrée : ARR cible, parts de marché, nombre de clients, effectifs, géographies
- North Star Metric unique
- OKRs stratégiques par année (Year 1 / Year 2 / Year {horizon_ans})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. AXES STRATÉGIQUES (3 à 5 priorités)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour chaque axe stratégique :
- Intitulé de l'axe et rationale stratégique
- Ambition quantifiée à {horizon_ans} ans
- Lien avec l'objectif : {objectif}
- Priorité relative (P1/P2/P3) et séquencement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. INITIATIVES STRATÉGIQUES PAR AXE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour chaque initiative :
- Nom de l'initiative et description (2-3 phrases)
- Owner recommandé (fonction/rôle)
- Budget estimé (CAPEX + OPEX sur la durée)
- KPIs de succès avec cibles chiffrées et fréquence de mesure
- Dépendances inter-initiatives
- Critères de go/no-go

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. ROADMAP TEMPORELLE DÉTAILLÉE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1 – Fondation (Mois 1-6) : Quick wins et mise en place
Phase 2 – Accélération (Mois 7-18) : Scale et expansion
Phase 3 – Leadership (Mois 19-{horizon_ans * 12}) : Domination de marché
Jalons clés et milestones critiques par trimestre
Budget total et allocation par phase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VI. FACTEURS CLÉS DE SUCCÈS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Top 5 FCS non-négociables pour atteindre {objectif}
- Enablers organisationnels (structure, culture, gouvernance)
- Capacités à développer en priorité
- Écosystème partenaires à construire

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VII. RISQUES STRATÉGIQUES ET PLANS DE MITIGATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour chaque risque majeur (au moins 6) :
- Description du risque et scénario déclencheur
- Probabilité (Faible/Moyenne/Élevée) × Impact (Faible/Moyen/Élevé) = Criticité
- Plan de mitigation proactif
- Plan de contingence si le risque se matérialise
- Owner du risque et KRI (Key Risk Indicator)

Présente ce plan avec la rigueur et la densité analytique d'un deliverable McKinsey.
Utilise des données de marché réelles sur l'IA en Europe.
Sois précis, chiffré, actionnable. Tout en français."""

    print(f"\n{'='*60}")
    print(f"PLAN STRATÉGIQUE {horizon_ans} ANS — {ENTREPRISE}")
    print(f"Objectif : {objectif}")
    print(f"{'='*60}\n")

    resultat = streamer(prompt)
    chemin = sauvegarder(f"plan_strategique_{horizon_ans}ans", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")
    return resultat


# ─────────────────────────────────────────────
# Agent 2 – Expansion Marché
# ─────────────────────────────────────────────

def agent_expansion_marche(pays_cible: str) -> str:
    """Stratégie d'entrée sur un nouveau marché géographique ou segment."""
    incrementer_stat("agent_expansion_marche")

    prompt = f"""Tu es un directeur associé BCG spécialisé en stratégie d'expansion internationale pour les scaleups technologiques.
Tu analyses l'entrée de {ENTREPRISE} ({DOMAINE}) sur le marché : {pays_cible}.

Produis une analyse d'entrée de marché exhaustive, digne d'un comité d'investissement stratégique :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. ANALYSE DU MARCHÉ {pays_cible.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Taille et dynamique du marché :
- Taille du marché IA {pays_cible} en valeur (€) avec sources
- CAGR projeté 2024-2028 et facteurs de croissance
- Maturité digitale des entreprises cibles (indice de digitalisation)
- Taux d'adoption des solutions d'agents IA vs. autres marchés européens
- Dépenses IT par secteur prioritaire (Finance, Industrie, Santé, Retail, Services)

Environnement macroéconomique :
- Indicateurs économiques clés (PIB, inflation, emploi tech)
- Politiques gouvernementales favorables à l'IA (subventions, fonds européens)
- Hubs technologiques locaux et écosystème startup
- Infrastructure cloud disponible (datacenter locaux, latence)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. SEGMENTATION CLIENTS CIBLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Segmentation par taille d'entreprise (ETI, grands comptes, PME tech-first)
- Segmentation par secteur vertical (Top 3 secteurs prioritaires avec sizing)
- Profil des acheteurs économiques (CIO, CDO, CHRO, COO) : pain points spécifiques
- Cycle d'achat moyen et processus de décision culturel dans ce marché
- Willingness-to-pay estimée vs. marché français
- Besoins de localisation (langue, conformité locale, intégrations SI locales)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. ANALYSE CONCURRENTIELLE LOCALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Top 5 compétiteurs présents sur ce marché (locaux + internationaux)
- Part de marché estimée par acteur
- Positionnement prix et segments servis
- Forces et faiblesses de chaque concurrent
- Whitespaces identifiés (segments non servis ou mal servis)
- Barrières à l'entrée spécifiques à ce marché

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. MODE D'ENTRÉE RECOMMANDÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Évaluation comparative des options :
Option A – Entrée directe (filiale propre) : avantages / inconvénients / coût / délai
Option B – Partenariat local (revendeur/intégrateur) : avantages / inconvénients / profil partenaire idéal
Option C – Acquisition d'un acteur local : cibles potentielles / valorisation / synergies
Option D – Approche hybride progressive

Recommandation argumentée avec séquencement en 3 phases :
- Phase 1 (Mois 1-6) : test & learn avec ressources limitées
- Phase 2 (Mois 7-18) : scaling si validation des hypothèses
- Phase 3 (Mois 19-36) : leadership local

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. PLAN GO-TO-MARKET DÉTAILLÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Proposition de valeur adaptée au marché {pays_cible} (messaging localisé)
- Canaux de distribution prioritaires (direct, revendeurs, marketplaces cloud)
- Stratégie de pricing local (adaptation au pouvoir d'achat et benchmarks locaux)
- Tactiques d'acquisition clients (Account-Based Marketing, events sectoriels, associations professionnelles)
- Références clients cibles pour crédibilité locale (logos pilotes prioritaires)
- Équipe commerciale requise : profils, coût, délai de recrutement
- Outils et CRM : adaptations nécessaires

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VI. BUDGET ET TIMELINE D'EXPANSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Budget d'entrée sur le marché {pays_cible} :
- CAPEX (structure légale, bureau, équipements) : estimation €
- OPEX annuel (équipe, marketing, partenariats, certifications) : estimation €
- Budget marketing acquisition clients Année 1/2/3 : estimation €
- Revenue projeté Année 1 / 2 / 3 avec hypothèses explicites
- Payback period et break-even point
- ROI attendu à 3 ans vs. alternatives d'allocation du capital

Timeline :
- T0 : décision d'entrée et mobilisation des ressources
- T+3 mois : premiers recrutements et structure juridique
- T+6 mois : premiers clients pilotes signés
- T+12 mois : KPIs de validation (ARR, nombre de clients, NPS)
- T+24 mois : profitabilité opérationnelle locale

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VII. RISQUES RÉGLEMENTAIRES ET CONFORMITÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RGPD et protection des données :
- Obligations spécifiques dans ce pays (DPA locale, transferts de données)
- Localisation des données requise (souveraineté numérique)
- Impact sur l'architecture technique produit

AI Act européen (en vigueur) :
- Classification du risque des agents IA de {ENTREPRISE} (risque limité/élevé/inacceptable)
- Obligations de conformité applicables (transparence, documentation, audit)
- Avantage compétitif de la conformité vs. acteurs non-européens
- Timeline de mise en conformité et coût estimé

Autres risques réglementaires spécifiques à {pays_cible} :
- Réglementation sectorielle (Finance : DORA, Santé : HDS local, etc.)
- Droit du travail pour l'IA (co-détermination, représentation syndicale)
- Certification et homologation requises

Présente cette analyse avec la densité et la précision d'un deliverable BCG.
Données chiffrées, sources citées, recommandations actionnables. Tout en français."""

    print(f"\n{'='*60}")
    print(f"STRATÉGIE D'EXPANSION — {pays_cible.upper()}")
    print(f"Entreprise : {ENTREPRISE}")
    print(f"{'='*60}\n")

    resultat = streamer(prompt)
    chemin = sauvegarder(f"expansion_marche_{pays_cible.lower().replace(' ', '_')}", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")
    return resultat


# ─────────────────────────────────────────────
# Agent 3 – Modèle d'Affaires
# ─────────────────────────────────────────────

def agent_modele_affaires(type_modele: str) -> str:
    """Design et optimisation du modèle d'affaires de l'entreprise."""
    incrementer_stat("agent_modele_affaires")

    prompt = f"""Tu es un partner spécialisé en business model design et stratégie d'entreprise chez Oliver Wyman, expert des modèles économiques des éditeurs de logiciels IA B2B.
Tu analyses et optimises le modèle d'affaires de {ENTREPRISE} ({DOMAINE}).

Type de modèle à analyser : {type_modele}

Produis une analyse business model de niveau conseil senior :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. ANALYSE DES REVENUE STREAMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Revenue streams actuels et potentiels :
1. Licences SaaS récurrentes (ARR) : structure de prix, tiers, limites d'usage
2. Revenus de services (implémentation, formation, CSM) : marges, scalabilité
3. Revenue usage-based (API calls, agents-minutes, tokens consommés) : élasticité
4. Revenue de partenariats (revshare, referral, marketplace) : potentiel
5. Revenus data/analytics (agrégation anonymisée) : légalité RGPD, potentiel
6. Revenue marketplace (agents tiers sur plateforme {ENTREPRISE}) : conditions

Mix optimal des revenue streams pour le contexte {type_modele} :
- Proportion ARR récurrent vs. transactionnel vs. services
- Tendance recommandée sur 3 ans (shift vers quel modèle ?)
- Benchmark éditeurs IA comparables (ARR mix, NRR, GRR)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. MODÈLE DE PRICING EXPERT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyse comparative des modèles de pricing possibles :

Modèle SaaS par siège :
- Avantages / inconvénients pour agents IA
- Grille tarifaire recommandée (Starter / Business / Enterprise)
- Points de prix benchmarkés (Salesforce, HubSpot, Monday.com, Intercom)

Modèle projet (one-time fee) :
- Cas d'usage appropriés
- Pricing par phase (découverte / développement / déploiement / MCO)
- Risques de non-récurrence et comment les mitiger

Modèle retainer (abonnement services) :
- Structure idéale pour {ENTREPRISE}
- Pricing mensuel / annuel avec engagement
- Métriques d'utilisation incluses

Modèle usage-based (consommation) :
- Unités de mesure pertinentes (tâches automatisées, tokens, temps de compute)
- Pricing par unité et seuils volumétriques
- Impact sur prévisibilité du revenu et cash-flow

Recommandation : modèle hybride optimal pour {type_modele} avec grille tarifaire détaillée

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. UNIT ECONOMICS — DEEP DIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAC (Customer Acquisition Cost) :
- CAC par canal (outbound, inbound, partenaires, events)
- CAC blended cible et benchmark éditeurs SaaS IA comparables
- Payback period cible (idéalement < 12 mois)
- LTV/CAC ratio cible (> 3x pour Seed, > 5x pour Série A/B)

LTV (Lifetime Value) :
- Calcul : ARPU × Gross Margin × (1 / Churn Rate)
- ARPU cible par segment (SMB / Mid-market / Enterprise)
- Gross margin cible (80%+ pour SaaS pur, 60-70% avec services)
- Churn acceptable par segment (logo churn vs. revenue churn)
- NRR (Net Revenue Retention) cible : > 120% (expansion > churn)

P&L simplifié à 3 ans :
- Revenus par stream
- COGS (infrastructure cloud, licences LLMs, support)
- Gross Profit et Gross Margin
- R&D, Sales & Marketing, G&A
- EBITDA et chemin vers la profitabilité

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. ANALYSE DE SCALABILITÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scalabilité technique :
- Architecture multi-tenant et économies d'échelle
- Coût marginal d'un client supplémentaire (tendance vers zéro ?)
- Goulots d'étranglement à anticiper (compute, storage, human-in-the-loop)

Scalabilité commerciale :
- Sales capacity planning (ratio AE pour chaque €1M d'ARR)
- Automation du cycle de vente (PLG, self-service, trial)
- Customer Success scalable (ratio CSM : clients, community, in-app)

Scalabilité organisationnelle :
- Structure d'équipe optimale par stade (Seed / Série A / Série B)
- Fonctions à externaliser vs. internaliser
- Rôles clés à recruter en priorité

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. CONSTRUCTION DU MOAT (FOSSÉ CONCURRENTIEL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Avantage data :
- Données propriétaires accumulées (interactions agents, datasets clients)
- Flywheel data : comment plus d'usage → meilleurs modèles → plus de valeur
- Protection des données et obligations RGPD
- Estimation de la valeur du dataset à 3/5 ans

Effets de réseau :
- Réseau de valeur (agents communicants entre clients différents ?)
- Marketplace et écosystème de développeurs
- Intégrations et connecteurs (lock-in par l'écosystème)

Switching costs :
- Coût de migration pour un client (data, formation, intégrations, workflows)
- Stratégie pour augmenter les switching costs légitimement
- Profondeur d'intégration dans les processus métier clients

Avantage marque :
- Positionnement thought leadership IA en Europe
- Certifications et labels (ISO 27001, HDS, AI Act compliance)
- Communauté et réputation développeur

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VI. OPTIONS DE PIVOT ET ADJACENCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Si le modèle {type_modele} ne performe pas selon les KPIs :
- Option A – Pivot vertical (specialisation sectorielle) : Finance / Santé / Industrie
- Option B – Pivot segment (up-market vers Enterprise ou down vers SMB)
- Option C – Pivot produit (platform → point solution ou l'inverse)
- Option D – Pivot géographique (focus sur 1-2 marchés vs. pan-européen)

Pour chaque option : trigger de décision, coût du pivot, probabilité de succès

Conclusion : recommandation du modèle optimal pour {ENTREPRISE} avec plan de transition sur 12 mois.
Tout en français, niveau deliverable conseil senior."""

    print(f"\n{'='*60}")
    print(f"ANALYSE MODÈLE D'AFFAIRES — {type_modele.upper()}")
    print(f"Entreprise : {ENTREPRISE}")
    print(f"{'='*60}\n")

    resultat = streamer(prompt)
    chemin = sauvegarder(f"modele_affaires_{type_modele.lower().replace(' ', '_')}", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")
    return resultat


# ─────────────────────────────────────────────
# Agent 4 – Analyse Concurrentielle Stratégique
# ─────────────────────────────────────────────

def agent_analyse_concurrentielle_strategique(concurrent_principal: str) -> str:
    """Analyse concurrentielle complète : Porter 5 Forces, intelligence compétitive, blue ocean."""
    incrementer_stat("agent_analyse_concurrentielle_strategique")

    prompt = f"""Tu es un expert en stratégie compétitive, ancien partner chez Strategy& (PwC), spécialisé en intelligence concurrentielle pour les éditeurs logiciels IA.
Tu réalises une analyse concurrentielle stratégique complète pour {ENTREPRISE} ({DOMAINE}).

Concurrent principal analysé : {concurrent_principal}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. ANALYSE PORTER 5 FORCES — VERSION AUGMENTÉE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Force 1 — Rivalité entre concurrents existants (Intensité : /10)
- Nombre et taille des acteurs (HHI — Herfindahl-Hirschman Index)
- Différenciation des offres et guerres de prix observées
- Croissance du marché (dilue ou intensifie la rivalité ?)
- Coûts fixes élevés et sur-capacité
- Analyse spécifique de {concurrent_principal} : part de marché, stratégie agressive/défensive, récentes initiatives

Force 2 — Pouvoir de négociation des clients (Pouvoir : /10)
- Concentration clients (top 20% génèrent combien de revenu ?)
- Sensibilité prix par segment (PME vs. ETI vs. Grand Compte)
- Coût de switching (élevé = pouvoir client faible)
- Information asymétrique (le client sait-il comparer les offres ?)
- Tendance : consolidation achats IT, appels d'offres formalisés

Force 3 — Pouvoir de négociation des fournisseurs (Pouvoir : /10)
- Dépendance aux hyperscalers (OpenAI, Anthropic, Google, AWS, Azure)
- Risque de désintermédiation (fournisseur LLM devient concurrent ?)
- Alternatives et stratégie multi-cloud / multi-LLM
- Négociation des tarifs d'infrastructure avec volumes

Force 4 — Menace des nouveaux entrants (Menace : /10)
- Barrières à l'entrée actuelles (capital, talent, données, réglementation)
- Potentiel de disruption par des startups IA générative
- Risque d'entrée des hyperscalers sur les segments de {ENTREPRISE}
- Avantages du first-mover vs. fast-follower dans ce marché

Force 5 — Menace des produits de substitution (Menace : /10)
- Alternatives non-technologiques (externalisation humaine, BPO)
- Solutions RPA/automation alternatives (Automation Anywhere, UiPath)
- No-code / citizen development (Zapier, Make, n8n)
- Build-in-house par les clients (équipes MLOps internes)

Synthèse 5 Forces : score d'attractivité du secteur et position relative de {ENTREPRISE}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. INTELLIGENCE COMPÉTITIVE — {concurrent_principal.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Profil stratégique complet :
- Historique, fondateurs, date de création, siège social
- Stade de financement et investisseurs (VCs, Corporate VCs)
- ARR estimé et croissance (sources publiques, Crunchbase, LinkedIn)
- Effectifs et zones de recrutement actives (signal de stratégie)
- Portefeuille produit : fonctionnalités clés, architecture technique
- Segments clients servis et références (case studies publiés)
- Stratégie de pricing (publique ou estimée)
- Partenariats et intégrations écosystème

Forces et faiblesses de {concurrent_principal} :
Forces (au moins 4) : avantages distinctifs, assets clés, momentum
Faiblesses (au moins 4) : vulnérabilités exploitables, dette technique, lacunes

Mouvements récents et signaux stratégiques :
- Dernières annonces produit et nouvelles fonctionnalités (12 derniers mois)
- Levées de fonds récentes et use of funds probable
- Recrutements stratégiques (signaux de direction)
- Expansion géographique en cours
- Acquisitions ou partenariats

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. CARTOGRAPHIE DES GROUPES STRATÉGIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mapping sur 2 axes clés (ex. : Prix × Sophistication IA, ou Verticalisation × Taille de marché ciblée) :
- Groupe 1 (Hyperscalers / plateformes) : Microsoft, Google, AWS — positionnement
- Groupe 2 (Leaders IA agents européens) : top acteurs du marché
- Groupe 3 (Startups spécialisées verticales) : acteurs niche
- Groupe 4 (Intégrateurs et ESN) : Capgemini, Sopra, Atos + offre IA

Position de {ENTREPRISE} dans cette cartographie :
- Groupe stratégique actuel
- Groupe cible à 3 ans
- Barrières à franchir pour se déplacer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. OPPORTUNITÉS BLUE OCEAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Grille ERRC (Éliminer / Réduire / Renforcer / Créer) :
- Éliminer : quels facteurs concurrentiels coûteux mais sans valeur client supprimer ?
- Réduire : quels facteurs sur-investis par rapport aux standards du secteur ?
- Renforcer : quels facteurs sous-investis vs. attentes clients à amplifier ?
- Créer : quels facteurs jamais offerts dans le secteur à inventer ?

Opportunités de marché non contestées :
- Segments verticaux sous-servis (identification et sizing)
- Géographies délaissées par les concurrents actuels
- Use cases émergents sans solution établie
- Modèles de delivery innovants (agent-as-a-service, outcome-based)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. PLAYBOOK DE RÉPONSE COMPÉTITIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scénario A — {concurrent_principal} coupe ses prix de 20-30% :
- Analyse : est-ce viable pour eux ? Quel impact sur leur marge ?
- Réponse recommandée pour {ENTREPRISE} : ne pas s'aligner / contre-attaquer / se différencier
- Tactiques défensives : value-based pricing, bundling, contrats pluriannuels
- Messaging commercial : comment expliquer la différence de valeur

Scénario B — {concurrent_principal} lance une nouvelle fonctionnalité majeure :
- Analyse : délai de réplication, complexité technique, réaction marché probable
- Réponse recommandée : accélérer roadmap / acquérir / communiquer sur feuille de route
- Gestion des clients inquiets : programme de fidélisation, early access
- Communication externe : positionnement différenciateur

Scénario C — {concurrent_principal} lève 50M€+ ou se fait acquérir :
- Impact sur la dynamique compétitive (accélération commerciale probable)
- Fenêtre d'opportunité avant qu'ils déploient les fonds (6-12 mois)
- Accélération de la levée de fonds de {ENTREPRISE} si nécessaire
- Réponse RP et communication clients/prospects

Scénario D — {concurrent_principal} cible directement vos clients clés (account raiding) :
- Système d'alerte précoce (signaux à surveiller)
- Défenses contractuelles (clauses d'engagement, SLAs renforcés)
- Programme de rétention clients à risque
- Counter-intelligence pour anticiper leurs prochains mouvements

Tout en français, niveau analyse stratégique grand cabinet. Précis, chiffré, actionnable."""

    print(f"\n{'='*60}")
    print(f"ANALYSE CONCURRENTIELLE — {concurrent_principal.upper()}")
    print(f"vs. {ENTREPRISE}")
    print(f"{'='*60}\n")

    resultat = streamer(prompt)
    chemin = sauvegarder(f"analyse_concurrentielle_{concurrent_principal.lower().replace(' ', '_')}", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")
    return resultat


# ─────────────────────────────────────────────
# Agent 5 – Stratégie de Croissance
# ─────────────────────────────────────────────

def agent_croissance(canal: str, budget: str) -> str:
    """Stratégie de croissance par canal avec modélisation CAC/LTV et plan sprint 90 jours."""
    incrementer_stat("agent_croissance")

    prompt = f"""Tu es un Chief Growth Officer (CGO) et ex-VP Growth chez un éditeur SaaS B2B IA ayant scalé de 1M€ à 50M€ ARR.
Tu construis la stratégie de croissance de {ENTREPRISE} ({DOMAINE}).

Canal prioritaire à analyser : {canal}
Budget disponible : {budget}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. ANALYSE DU CANAL : {canal.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Caractéristiques du canal pour un éditeur IA B2B européen :
- Potentiel de volume (audience atteignable en Europe)
- Qualité des leads générés (ICP fit, buyer intent, cycle de vente)
- CAC moyen constaté dans ce canal pour des solutions IA B2B similaires
- Délai avant les premiers résultats tangibles (time-to-revenue)
- Scalabilité : linear scaling ou exponential scaling ?
- Niveau de compétition dans ce canal (saturation ?)
- Dépendances et risques (algorithme, partenaire unique, saisonnalité)

Benchmark secteur — métriques clés pour ce canal :
- CAC médian des 25 éditeurs SaaS IA B2B les plus comparables
- Conversion rate à chaque étape du funnel
- Volume typique atteignable avec {budget} de budget
- ROI attendu (Revenue généré / Investissement canal)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. ANALYSE MULTI-CANAUX — PORTFOLIO COMPLET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour chaque canal majeur, évaluer (score /10) :

SEO / Content Marketing :
- Stratégie de contenu IA thought leadership (mots-clés cibles, volume, difficulté)
- Content clusters recommandés pour {ENTREPRISE}
- Délai avant trafic organique significatif (6-12 mois minimum)
- Ressources requises (content manager, SEO specialist, outils)
- CAC estimé : faible à long terme, investissement initial fort

Paid Acquisition (LinkedIn Ads, Google, Facebook) :
- Ciblage ICP précis pour agents IA B2B (fonction, secteur, taille)
- Budget minimum viable pour ce marché
- Funnel complet : impression → clic → MQL → SQL → client
- A/B tests à prioriser (créatifs, landing pages, CTAs)

Outbound Sales (cold email, LinkedIn SDR) :
- Séquences de prospection recommandées pour acheteurs IA
- Outils (Apollo, Lemlist, Clay, Sales Navigator)
- Ratio SDR : AE optimal pour {ENTREPRISE}
- Scripts et messaging clés (pain-first, ROI-driven)

Partenariats stratégiques :
- Types de partenaires prioritaires (intégrateurs, ESN, éditeurs complémentaires)
- Structure du programme partenaires (niveaux, commissions, enablement)
- Pipeline partenaires : identification et qualification des 10 premiers
- ROI partenariats vs. canaux directs

Events et Conférences :
- Top 10 événements IA / tech B2B en Europe à cibler
- Stratégie speaker / sponsor / sponsor platinum
- Lead collection et nurture post-event
- ROI événement : calcul et seuil de rentabilité

Product-Led Growth (PLG) :
- Freemium vs. free trial vs. reverse trial — quelle option pour {ENTREPRISE} ?
- Activation metric : quel est le moment "aha!" pour un utilisateur d'agents IA ?
- Viral loops intégrés au produit (partage, collaboration, templates)
- Self-serve upgrade : comment convertir freemium → payant sans intervention commerciale ?
- PQLs (Product Qualified Leads) : définition et scoring

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. MODÉLISATION CAC ET LTV PAR CANAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tableau de modélisation pour {ENTREPRISE} :

| Canal | CAC estimé | LTV estimé | LTV/CAC | Payback | Volume/an |
|-------|------------|------------|---------|---------|-----------|
| SEO/Content | X€ | Y€ | ratio | mois | N clients |
| Paid LinkedIn | X€ | Y€ | ratio | mois | N clients |
| Outbound SDR | X€ | Y€ | ratio | mois | N clients |
| Partenariats | X€ | Y€ | ratio | mois | N clients |
| PLG/Freemium | X€ | Y€ | ratio | mois | N clients |
| Events | X€ | Y€ | ratio | mois | N clients |
| {canal} | X€ | Y€ | ratio | mois | N clients |

Hypothèses de calcul explicitées :
- ARPU par segment (SMB / Mid-market / Enterprise)
- Gross Margin utilisée (%)
- Churn annuel utilisé (%)
- Durée de vie client (années)

Recommandation d'allocation du budget {budget} par canal avec justification

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. EXPÉRIENCES DE CROISSANCE À LANCER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Framework ICE (Impact × Confidence × Ease) pour prioriser les experiments :

Top 10 growth experiments recommandés pour {ENTREPRISE} :
Pour chaque experiment :
- Hypothèse testée (si X alors Y car Z)
- Métrique principale et métrique de guardrail
- Segment cible et taille d'échantillon requise
- Durée du test
- Résultat minimum pour valider (what does success look like ?)
- Score ICE
- Owner recommandé

A/B tests prioritaires :
- Landing page headline (messaging pain vs. bénéfice vs. social proof)
- Pricing page (mensuel vs. annuel, ancrage de prix, free trial vs. demo)
- Email nurture (séquence éducative vs. démonstration ROI vs. cas clients)
- Onboarding (time-to-value réduit, activation steps)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. MÉCANIQUE VIRALE ET REFERRAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Viral coefficient K de {ENTREPRISE} :
- K actuel estimé et K cible
- Comment augmenter K : partage produit, agents publics, templates partagés
- Boucle virale B2B : "l'agent de notre client impressionne son client"

Programme de referral B2B :
- Structure : récompenses pour le référent (crédits, cash, reconnaissance)
- Friction minimale : trigger automatique, lien personnalisé, tracking
- Qualification des referred leads : ICP fit minimal requis
- Exemples de succès (Dropbox, Slack, Notion) et adaptation au contexte IA B2B

Community-led growth :
- Création d'une communauté practitioners agents IA (Slack, Discord, Circle)
- Contenu exclusif (benchmarks, templates, playbooks)
- Ambassadeurs et champions clients
- Lien communauté → product feedback → roadmap → rétention

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VI. PLAN SPRINT 90 JOURS — CANAL {canal.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Semaines 1-4 (Foundation) :
- Actions immédiates à lancer dans les 7 premiers jours
- Setup tracking et attribution (Google Analytics 4, CRM, UTMs)
- Recrutement / activation des ressources nécessaires
- Baseline metrics à capturer avant toute action
- Budget alloué : [X€ sur {budget}]

Semaines 5-8 (Expérimentation) :
- Lancement des 3 premiers experiments prioritaires
- Cadence de revue hebdomadaire (kill/scale décisions)
- Premiers insights et ajustements
- KPIs intermédiaires de validation

Semaines 9-12 (Scale) :
- Scaling des experiments validés
- Abandon des experiments non conclusifs
- Projection de résultats à fin de sprint
- Préparation du Sprint 2 (Mois 4-6)

Objectif du sprint 90 jours pour le canal {canal} avec budget {budget} :
- MQLs générés : X
- SQLs générés : X (taux de conversion MQL→SQL : X%)
- Clients signés : X (taux de closing : X%)
- ARR généré : X€
- CAC réalisé : X€ (vs. objectif)

Tout en français, avec la rigueur d'un Growth Director expérimenté. Chiffres précis, métriques SaaS réelles."""

    print(f"\n{'='*60}")
    print(f"STRATÉGIE DE CROISSANCE — {canal.upper()}")
    print(f"Budget : {budget} | Entreprise : {ENTREPRISE}")
    print(f"{'='*60}\n")

    resultat = streamer(prompt)
    chemin = sauvegarder(f"croissance_{canal.lower().replace(' ', '_')}", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")
    return resultat


# ─────────────────────────────────────────────
# Agent 6 – Pitch Investisseur
# ─────────────────────────────────────────────

def agent_pitch_investisseur(stade: str, montant: str) -> str:
    """Construit un pitch deck complet pour les investisseurs avec financials et réponses aux questions dures."""
    incrementer_stat("agent_pitch_investisseur")

    prompt = f"""Tu es un venture partner senior et ex-fondateur ayant levé plus de 150M€ pour des startups deeptech et IA en Europe.
Tu construis le pitch investisseur complet pour {ENTREPRISE} ({DOMAINE}).

Stade de levée : {stade}
Montant cible : {montant}

Produis un pitch deck en format narratif complet, de niveau top-tier VC (Sequoia, Benchmark, Index Ventures, Balderton) :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 1 — OPENING HOOK (PROBLEM/SOLUTION NARRATIVE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

La narration parfaite en 3 actes :

Acte 1 — Le Problème (viscéral, universel, urgent) :
- Scène d'ouverture : cas client concret et immersif (nom fictif, situation réelle)
- Pourquoi ce problème existe maintenant (timing : pourquoi pas il y a 5 ans ?)
- Coût du problème : combien ça coûte aux entreprises en € et en temps ?
- Qui souffre : persona précis du decision-maker qui ressent ce problème
- Preuves que le problème est réel (stats, citations clients, études)

Acte 2 — La Solution (élégante, défendable, au bon moment) :
- Proposition de valeur en une phrase (clarté absolue, zéro jargon)
- Comment ça marche : démo narrative en 3 étapes maximum
- Différence fondamentale avec les alternatives existantes
- Pourquoi maintenant : les 3 conditions technologiques/marché qui rendent cela possible aujourd'hui

Acte 3 — La Vision (ambitieuse, crédible) :
- Où sera {ENTREPRISE} dans 5 ans si tout se passe bien ?
- Impact transformationnel sur les entreprises européennes
- Analogie inspirante (mais précise) avec un succès comparable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 2 — TAILLE DE MARCHÉ (TAM / SAM / SOM)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Méthode Bottom-up (la seule crédible pour les VCs) :

TAM — Total Addressable Market :
- Définition précise : toutes les entreprises européennes qui pourraient bénéficier d'agents IA
- Calcul : N entreprises × ARPU potentiel = €Xmd
- Sources primaires (Gartner, IDC, Forrester, données Eurostat)
- Croissance du TAM : CAGR et facteurs drivers

SAM — Serviceable Addressable Market :
- Segment que {ENTREPRISE} peut réellement servir aujourd'hui (géographie, taille, secteur)
- Calcul bottom-up : N ICP entreprises × ARPU cible = €Xm
- Hypothèses explicites et défendables

SOM — Serviceable Obtainable Market :
- Part réaliste à capturer sur 3-5 ans avec {montant} levés
- Calcul : SOM = Capacité commerciale × Win rate marché
- Comparaison avec des scaleups IA similaires au même stade

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 3 — BUSINESS MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Revenue model en une phrase simple
- Structure de pricing avec tiers et exemples de prix
- Métriques clés : ARPU, Gross Margin, NRR, Churn
- Why now : pourquoi ce modèle est le bon pour ce stade
- Path to monetization optimization (comment le modèle évolue avec la scale)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 4 — TRACTION ET MÉTRIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Traction actuelle (métriques au stade {stade}) :
- ARR actuel et croissance MoM / YoY (courbe de hockey stick si applicable)
- Nombre de clients et logos de référence (catégorisés par segment)
- NRR (Net Revenue Retention) — signal de product-market fit
- CAC réalisé et payback period
- NPS clients et verbatims (2-3 citations impactantes)
- Waterfall de revenus : new logo ARR + expansion ARR - churned ARR

Signaux de product-market fit :
- Rétention M6 et M12 par cohorte
- Temps de mise en valeur (time-to-value)
- Fréquence d'usage et stickiness
- Waiting list ou inbound organique (signal de pull)

Milestones depuis la création :
- Timeline des victoires clés (clients, produit, équipe, financement)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 5 — ÉQUIPE (WHY US)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Les fondateurs (profils types recommandés pour un éditeur IA) :
- CEO : vision business, ventes enterprise, storytelling — background idéal
- CTO : expertise IA/ML, architecture scalable, publications ou brevets — background idéal
- CPO ou COO : product intuition, opérations, go-to-market — background idéal

Unfair advantages de l'équipe :
- Expertise domaine unique (accès à des données propriétaires, réseau industriel)
- Expériences fondatrices : qu'ont-ils vécu qui les rend parfaits pour ce problème ?
- Track record : succès passés actionnables (exits, scale, publications)
- Réseau : accès aux premiers 100 clients, VCs, talents clés

Advisors stratégiques :
- Profils d'advisors recommandés (ex-CDO grands comptes, VC partner, chercheur IA)
- Comment les présenter pour maximiser la crédibilité

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 6 — MATRICE CONCURRENTIELLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Matrice de positionnement (2×2 ou tableau comparatif) :
- Axes de différenciation défendables (PAS les axes génériques)
- Concurrent 1 / 2 / 3 / 4 / 5 vs. {ENTREPRISE}
- Critères : conformité RGPD, spécificité européenne, profondeur IA, intégrations, support

Narration différenciatrice :
- Pourquoi {ENTREPRISE} gagne des deals contre chaque type de concurrent
- Preuve par la traction (win rates par segment, références clients)
- Sustainable differentiation (ce que les concurrents ne peuvent pas copier facilement)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 7 — FINANCIALS (P&L FORECAST 3 ANS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Modèle financier complet (en €, en milliers ou millions selon le stade {stade}) :

                        Année 1    Année 2    Année 3
ARR début de période :    X€         X€         X€
+ New logo ARR :         +X€        +X€        +X€
+ Expansion ARR :        +X€        +X€        +X€
- Churned ARR :          -X€        -X€        -X€
ARR fin de période :      X€         X€         X€
Croissance ARR (%) :      X%         X%         X%

Revenus reconnus :        X€         X€         X€
COGS :                   -X€        -X€        -X€
Gross Profit :            X€         X€         X€
Gross Margin (%) :        X%         X%         X%

R&D :                    -X€        -X€        -X€
Sales & Marketing :      -X€        -X€        -X€
G&A :                    -X€        -X€        -X€
EBITDA :                 -X€        -X€        +X€

Burn mensuel moyen :      X€         X€         X€
Runway avec {montant} :   X mois
Break-even ARR :          X€ (mois X de l'Année X)

Hypothèses clés (défendables et benchmarkées) :
- Nombre de nouveaux clients par an et ARPU moyen
- Churn annuel assumé (logo et revenue)
- % revenus réinvestis en R&D vs. GTM
- Efficacité commerciale (Magic Number, Rule of 40 cible)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 8 — USE OF FUNDS ET MILESTONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Allocation des {montant} levés :
- R&D / Engineering : X% (X€) — développements produit prioritaires
- Sales & Marketing : X% (X€) — canaux et équipes commerciales
- Customer Success : X% (X€) — rétention et expansion
- G&A / Opérations : X% (X€) — structure et conformité
- Working capital / Trésorerie tampon : X% (X€)

Milestones débloqués par cette levée :
- Milestone 1 (Mois 6) : [objectif produit ou commercial précis]
- Milestone 2 (Mois 12) : [ARR cible, nombre de clients, nouvelles géographies]
- Milestone 3 (Mois 18) : [position de marché, signal pour levée suivante]

Story de la prochaine levée :
- Stade suivant (ex. : Série A après ce {stade})
- Montant probable et dilution
- Multiples de valorisation visés (ARR multiple à ce stade)
- Investisseurs cibles pour le tour suivant

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 9 — STRATÉGIE DE SORTIE (EXIT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options de sortie pour les investisseurs :

Option 1 — Acquisition stratégique :
- Acquéreurs naturels : hyperscalers (Microsoft, Google, AWS, Salesforce), ESN européennes, éditeurs RH/ERP/CRM
- Multiple de valorisation attendu (ARR multiple, exemples d'acquisitions comparables)
- Horizon probable : 4-7 ans
- Ce qui rend {ENTREPRISE} attractive pour ces acquéreurs

Option 2 — IPO (Introduction en Bourse) :
- Marchés cibles (Euronext Growth, Nasdaq, NYSE)
- Critères requis (ARR, croissance, profitabilité)
- Horizon probable : 6-10 ans
- Exemples d'IPOs SaaS IA européennes récentes

Option 3 — Secondary / Continuation Fund :
- Liquidité partielle pour fondateurs et early investors
- Horizon et conditions

Retour sur investissement projeté pour le tour {stade} :
- Hypothèse de valorisation à la sortie
- Multiple attendu pour les investisseurs entrant à ce tour
- IRR projeté

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 10 — RÉPONSES AUX 10 QUESTIONS DURES DES VCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour chaque question : réponse honnête, directe, confiante — pas de langue de bois

Q1 : "Pourquoi vous ? Microsoft/Google ne peut pas faire la même chose en 6 mois avec leurs ressources ?"
Réponse : [argumentation différenciation défendable, données, exemples]

Q2 : "Votre NRR est inférieur à 100%, ça veut dire que vos clients ne voient pas assez de valeur. Pourquoi ?"
Réponse : [diagnostic honnête et plan de remédiation]

Q3 : "Avec les LLMs qui s'améliorent exponentiellement, votre produit ne sera-t-il pas obsolète dans 2 ans ?"
Réponse : [argument technologique + argument moat non-technologique]

Q4 : "Votre CAC est trop élevé vs. votre LTV. Comment comptez-vous corriger ça ?"
Réponse : [plan d'amélioration avec horizon et métriques cibles]

Q5 : "L'AI Act va alourdir significativement vos coûts de compliance. Comment vous préparez-vous ?"
Réponse : [stratégie conformité + argument de différenciation par la conformité]

Q6 : "Comment retenez-vous vos ingénieurs IA face aux offres des GAFA à 300K€+ ?"
Réponse : [culture, equity, impact, flexibilité, mission]

Q7 : "Si votre concurrent principal lève 100M€ demain, qu'est-ce qui vous protège ?"
Réponse : [analyse des switchings costs, relations clients, avantage technologique]

Q8 : "Votre pipeline est concentré : vos 3 plus gros clients représentent 60% de l'ARR. C'est un risque majeur."
Réponse : [plan de diversification avec timeline et métriques]

Q9 : "Pourquoi maintenant ? Ce problème existait il y a 3 ans. Qu'est-ce qui a changé ?"
Réponse : [3 changements technologiques/marché/réglementaires précis]

Q10 : "Quel est votre plan B si vous ne trouvez pas de product-market fit dans les 18 prochains mois ?"
Réponse : [scénario pivot, cash management, plan de survie]

Format : narratif dense, chiffré, convaincant. Niveau pitch Series A/B tier-1 VC européen.
Tout en français. Aucun jargon creux, seulement des arguments défendables."""

    print(f"\n{'='*60}")
    print(f"PITCH INVESTISSEUR — {stade.upper()} | {montant}")
    print(f"Entreprise : {ENTREPRISE}")
    print(f"{'='*60}\n")

    resultat = streamer(prompt)
    chemin = sauvegarder(f"pitch_investisseur_{stade.lower().replace(' ', '_')}_{montant.lower().replace(' ', '_')}", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")
    return resultat


# ─────────────────────────────────────────────
# Menu principal
# ─────────────────────────────────────────────

def afficher_menu():
    print("\n" + "=" * 62)
    print("   AGENTCLAUDE SOLUTIONS — STRATEGIC INTELLIGENCE PLATFORM")
    print("=" * 62)
    print("   Agents de Planification Stratégique (Niveau McKinsey/BCG)")
    print("=" * 62)
    print()
    print("  [1]  Plan Stratégique           — Vision, SWOT, Roadmap N ans")
    print("  [2]  Expansion Marché           — Entrée pays / segment")
    print("  [3]  Modèle d'Affaires          — Revenue, Pricing, Unit Economics")
    print("  [4]  Analyse Concurrentielle    — Porter 5 Forces, Blue Ocean")
    print("  [5]  Stratégie de Croissance    — Canal, CAC/LTV, Sprint 90j")
    print("  [6]  Pitch Investisseur         — Deck complet, Financials, Q&A")
    print()
    print("  [0]  Quitter")
    print()
    print("=" * 62)


def main():
    while True:
        afficher_menu()
        choix = input("  Votre choix : ").strip()

        if choix == "0":
            print("\n  Au revoir. Bonne exécution stratégique !")
            break

        elif choix == "1":
            print("\n  ─── PLAN STRATÉGIQUE ───")
            try:
                horizon = int(input("  Horizon (années, ex: 3) : ").strip())
            except ValueError:
                print("  Erreur : entrez un nombre entier.")
                continue
            objectif = input("  Objectif principal (ex: atteindre 10M€ ARR) : ").strip()
            if not objectif:
                print("  Erreur : l'objectif est requis.")
                continue
            agent_plan_strategique(horizon, objectif)

        elif choix == "2":
            print("\n  ─── EXPANSION MARCHÉ ───")
            pays = input("  Pays ou segment cible (ex: Allemagne, Santé UK) : ").strip()
            if not pays:
                print("  Erreur : le pays cible est requis.")
                continue
            agent_expansion_marche(pays)

        elif choix == "3":
            print("\n  ─── MODÈLE D'AFFAIRES ───")
            print("  Types suggérés : SaaS, Usage-based, Freemium, Retainer, Hybride")
            type_m = input("  Type de modèle : ").strip()
            if not type_m:
                print("  Erreur : le type de modèle est requis.")
                continue
            agent_modele_affaires(type_m)

        elif choix == "4":
            print("\n  ─── ANALYSE CONCURRENTIELLE ───")
            concurrent = input("  Concurrent principal (ex: Dust, Relevance AI, Zapier) : ").strip()
            if not concurrent:
                print("  Erreur : le nom du concurrent est requis.")
                continue
            agent_analyse_concurrentielle_strategique(concurrent)

        elif choix == "5":
            print("\n  ─── STRATÉGIE DE CROISSANCE ───")
            print("  Canaux : SEO, LinkedIn Ads, Outbound SDR, Partenariats, Events, PLG, Content")
            canal = input("  Canal prioritaire : ").strip()
            budget = input("  Budget disponible (ex: 50 000€, 200K€) : ").strip()
            if not canal or not budget:
                print("  Erreur : canal et budget sont requis.")
                continue
            agent_croissance(canal, budget)

        elif choix == "6":
            print("\n  ─── PITCH INVESTISSEUR ───")
            print("  Stades : Pré-seed, Seed, Série A, Série B")
            stade = input("  Stade de la levée : ").strip()
            montant = input("  Montant cible (ex: 500K€, 3M€, 10M€) : ").strip()
            if not stade or not montant:
                print("  Erreur : stade et montant sont requis.")
                continue
            agent_pitch_investisseur(stade, montant)

        else:
            print("\n  Choix invalide. Entrez un chiffre entre 0 et 6.")

        input("\n  [Appuyez sur Entrée pour revenir au menu]")


if __name__ == "__main__":
    main()
