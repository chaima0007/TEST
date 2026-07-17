"""
Agent Détecteur d'Opportunités Éclair — identifie et capture en temps réel les opportunités
commerciales, réglementaires et partenariales à fort potentiel et fenêtre courte pour CaelumSwarm™.

Contexte : Juin 2026, à 13 mois de la deadline CSDDD (juillet 2027). La fenêtre de décision
des grandes entreprises est en train de se refermer — celles qui n'ont pas encore de solution
de conformité sont en état d'alerte maximale. CaelumSwarm™ est positionné pour capturer
cette vague si et seulement si les opportunités éclair sont saisies dans les 24-72h.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from typing import Any

# ---------------------------------------------------------------------------
# 1. CONSTANTS
# ---------------------------------------------------------------------------

OPPORTUNITY_TYPES: dict[str, dict] = {
    "REGULATORY_DEADLINE_WINDOW": {
        "label": "Fenêtre de Délai Réglementaire",
        "avg_window_days": 45,
        "value_multiplier": 3.2,
        "detection_method": "Veille réglementaire automatisée + alertes Journal Officiel EU",
        "response_time_target_hours": 6,
        "caelum_relevance": "HIGH",
    },
    "COMPETITOR_FAILURE": {
        "label": "Défaillance Concurrentielle",
        "avg_window_days": 14,
        "value_multiplier": 2.8,
        "detection_method": "Monitoring uptime concurrents + écoute réseaux sociaux professionnels",
        "response_time_target_hours": 2,
        "caelum_relevance": "HIGH",
    },
    "MARKET_FUNDING_EVENT": {
        "label": "Événement de Financement Marché",
        "avg_window_days": 90,
        "value_multiplier": 2.1,
        "detection_method": "Crunchbase / Dealroom alerts + LinkedIn capital-raise announcements",
        "response_time_target_hours": 24,
        "caelum_relevance": "MEDIUM",
    },
    "MEDIA_MOMENT": {
        "label": "Moment Médiatique",
        "avg_window_days": 7,
        "value_multiplier": 1.6,
        "detection_method": "Google Alerts CSDDD/ESG + veille presse B2B + Twitter/X trending",
        "response_time_target_hours": 4,
        "caelum_relevance": "MEDIUM",
    },
    "CONFERENCE_TIMING": {
        "label": "Timing Conférence Sectorielle",
        "avg_window_days": 21,
        "value_multiplier": 1.9,
        "detection_method": "Calendrier événementiel ESG/LegalTech + liste exposants publics",
        "response_time_target_hours": 48,
        "caelum_relevance": "MEDIUM",
    },
    "TALENT_AVAILABILITY": {
        "label": "Disponibilité Talent Stratégique",
        "avg_window_days": 30,
        "value_multiplier": 1.4,
        "detection_method": "LinkedIn talent signals + annonces de licenciements sectoriels",
        "response_time_target_hours": 72,
        "caelum_relevance": "MEDIUM",
    },
    "PARTNERSHIP_WINDOW": {
        "label": "Fenêtre Partenariale",
        "avg_window_days": 60,
        "value_multiplier": 2.5,
        "detection_method": "Suivi appels à partenaires institutionnels + réseau GSI/Big4",
        "response_time_target_hours": 12,
        "caelum_relevance": "HIGH",
    },
    "GRANT_OR_SUBSIDY": {
        "label": "Subvention ou Aide Publique",
        "avg_window_days": 30,
        "value_multiplier": 1.8,
        "detection_method": "Portails Bpifrance / EU Horizon / France 2030 + alertes AMI",
        "response_time_target_hours": 36,
        "caelum_relevance": "HIGH",
    },
}

# Simulated live signals as of June 21, 2026 — T-13 months before CSDDD July 2027 deadline
MARKET_SIGNALS_LIVE: list[dict] = [
    {
        "signal_id": "SIG-2026-001",
        "type": "REGULATORY_DEADLINE_WINDOW",
        "description": (
            "La France, l'Allemagne et les Pays-Bas viennent de publier leurs projets de"
            " transposition CSDDD simultanément. Fenêtre de 6 semaines pour positionner"
            " CaelumSwarm™ avant que les cabinets de conseil occupent le terrain."
        ),
        "detected_at": "2026-06-18T09:00:00Z",
        "expires_at": "2026-07-30T23:59:00Z",
        "urgency": "CRITICAL",
        "estimated_revenue_EUR": 480000,
        "action_required": (
            "Contacter immédiatement les DAF et DRSEs des 200 entreprises cibles dans ces 3 pays"
            " avec un brief comparatif des exigences de transposition nationales."
        ),
        "probability_success_pct": 72,
    },
    {
        "signal_id": "SIG-2026-002",
        "type": "COMPETITOR_FAILURE",
        "description": (
            "Outage majeur de 18h chez EcoVadis (plateforme rating RSE) le 19 juin 2026."
            " Multiples clients enterprise ont exprimé leur frustration sur LinkedIn et"
            " demandent des alternatives pour leurs bilans T2."
        ),
        "detected_at": "2026-06-19T14:30:00Z",
        "expires_at": "2026-06-26T23:59:00Z",
        "urgency": "CRITICAL",
        "estimated_revenue_EUR": 320000,
        "action_required": (
            "Déployer campagne d'outreach ciblée sur les clients EcoVadis mécontents."
            " Offrir migration express + 3 mois gratuits. Fenêtre : 72h max."
        ),
        "probability_success_pct": 58,
    },
    {
        "signal_id": "SIG-2026-003",
        "type": "MARKET_FUNDING_EVENT",
        "description": (
            "Tikehau Capital et Meridiam viennent de clôturer deux fonds d'infrastructure"
            " durable à 2,4 Md€ combinés. Les sociétés en portefeuille devront démontrer"
            " leur conformité CSDDD dès la prochaine revue LPs (septembre 2026)."
        ),
        "detected_at": "2026-06-15T11:00:00Z",
        "expires_at": "2026-08-31T23:59:00Z",
        "urgency": "HIGH",
        "estimated_revenue_EUR": 650000,
        "action_required": (
            "Pitcher CaelumSwarm™ aux IR teams des deux fonds comme solution recommandée"
            " à leurs portcos. Cibler 35 sociétés en portefeuille qualifiées."
        ),
        "probability_success_pct": 41,
    },
    {
        "signal_id": "SIG-2026-004",
        "type": "MEDIA_MOMENT",
        "description": (
            "Le Parlement Européen publie un rapport d'avancement CSDDD très médiatisé"
            " qui identifie un 'retard alarmant' dans la préparation des entreprises."
            " AFP, Les Échos et Le Monde couvrent. Pic de recherche Google +340%."
        ),
        "detected_at": "2026-06-20T07:00:00Z",
        "expires_at": "2026-06-27T23:59:00Z",
        "urgency": "HIGH",
        "estimated_revenue_EUR": 95000,
        "action_required": (
            "Publier dans les 4h un article d'opinion signé CEO sur LinkedIn + blog."
            " Pitcher les journalistes avec données exclusives CaelumSwarm™ sur le retard"
            " de conformité. Objectif : 3 citations presse dans les 48h."
        ),
        "probability_success_pct": 67,
    },
    {
        "signal_id": "SIG-2026-005",
        "type": "CONFERENCE_TIMING",
        "description": (
            "Sommet Sustainability Leaders Paris (7-8 juillet 2026) — 1 200 DRSE attendus."
            " La liste des exposants confirme l'absence de solution CSDDD pure-player."
            " Possibilité de table ronde sponsorisée encore disponible."
        ),
        "detected_at": "2026-06-16T10:00:00Z",
        "expires_at": "2026-06-28T23:59:00Z",
        "urgency": "HIGH",
        "estimated_revenue_EUR": 280000,
        "action_required": (
            "Réserver le créneau table ronde sous 48h (deadline organisateur)."
            " Préparer démo live CaelumSwarm™ + 200 kits prospectus personnalisés par secteur."
        ),
        "probability_success_pct": 54,
    },
    {
        "signal_id": "SIG-2026-006",
        "type": "REGULATORY_DEADLINE_WINDOW",
        "description": (
            "L'ESMA vient de préciser que les rapports CSRD (scope 3 supply chain)"
            " devront être alignés CSDDD dès l'exercice 2026. Environ 2 400 entreprises"
            " françaises découvrent qu'elles ont un gap critique dans leur stack actuel."
        ),
        "detected_at": "2026-06-17T15:00:00Z",
        "expires_at": "2026-09-30T23:59:00Z",
        "urgency": "HIGH",
        "estimated_revenue_EUR": 920000,
        "action_required": (
            "Lancer une campagne 'Gap CSRD-CSDDD' ciblant les 2 400 entreprises via"
            " LinkedIn Ads + emailing partenaires. Proposer un diagnostic gratuit 30 min."
        ),
        "probability_success_pct": 38,
    },
    {
        "signal_id": "SIG-2026-007",
        "type": "PARTNERSHIP_WINDOW",
        "description": (
            "PwC Legal France cherche un partenaire technologique CSDDD pour répondre"
            " à 3 appels d'offres groupés (Total, Vinci, Engie) d'ici le 15 juillet."
            " Leur solution actuelle ne couvre pas le module chaîne d'approvisionnement."
        ),
        "detected_at": "2026-06-20T16:00:00Z",
        "expires_at": "2026-07-15T17:00:00Z",
        "urgency": "CRITICAL",
        "estimated_revenue_EUR": 1200000,
        "action_required": (
            "Appeler le Managing Partner PwC Legal sous 6h. Préparer term sheet partenariat"
            " avec revenue-share 30/70. Ces 3 comptes représentent 1,2 M€ de TCV potentiel."
        ),
        "probability_success_pct": 63,
    },
    {
        "signal_id": "SIG-2026-008",
        "type": "GRANT_OR_SUBSIDY",
        "description": (
            "Bpifrance ouvre un AMI 'Transition Numérique Responsable' doté de 45 M€."
            " Les solutions d'IA pour la conformité ESG sont explicitement éligibles."
            " Date limite de dépôt : 31 juillet 2026."
        ),
        "detected_at": "2026-06-14T09:00:00Z",
        "expires_at": "2026-07-31T17:00:00Z",
        "urgency": "HIGH",
        "estimated_revenue_EUR": 400000,
        "action_required": (
            "Mandater un consultant Bpifrance et soumettre le dossier d'ici le 25 juillet."
            " Budget demandé : 800 K€ (50% subventionné = 400 K€ net)."
        ),
        "probability_success_pct": 55,
    },
    {
        "signal_id": "SIG-2026-009",
        "type": "TALENT_AVAILABILITY",
        "description": (
            "L'ex-Head of ESG Tech de Schneider Electric (15 ans d'expérience, réseau"
            " CAC40 solide) est en recherche active depuis la restructuration du 10 juin."
            " Son profil LinkedIn indique 'open to opportunities'."
        ),
        "detected_at": "2026-06-21T08:00:00Z",
        "expires_at": "2026-07-21T23:59:00Z",
        "urgency": "MEDIUM",
        "estimated_revenue_EUR": 180000,
        "action_required": (
            "Contacter sous 48h pour un call exploratoire. Poste envisagé : VP Partnerships"
            " DACH/Benelux. Son réseau seul justifie le recrutement (pipeline estimé 1,5 M€)."
        ),
        "probability_success_pct": 45,
    },
    {
        "signal_id": "SIG-2026-010",
        "type": "MARKET_FUNDING_EVENT",
        "description": (
            "Raise Series B de 40 M€ annoncée par Nexio (concurrent indirect, supply chain"
            " visibility). Leurs investisseurs incluent 3 fonds que nous ciblons. Leurs"
            " clients CAC40 cherchent maintenant à consolider leur stack ESG/compliance."
        ),
        "detected_at": "2026-06-19T10:00:00Z",
        "expires_at": "2026-09-19T23:59:00Z",
        "urgency": "MEDIUM",
        "estimated_revenue_EUR": 340000,
        "action_required": (
            "Contacter les clients CAC40 communs pour positionner CaelumSwarm™ en"
            " complément (pas concurrent) de Nexio. Préparer matrice de complémentarité."
        ),
        "probability_success_pct": 35,
    },
    {
        "signal_id": "SIG-2026-011",
        "type": "COMPETITOR_FAILURE",
        "description": (
            "Enablon (Wolters Kluwer) annonce l'arrêt de sa module CSDDD 'legacy' au"
            " 31 décembre 2026 sans alternative native. 180+ clients européens en migration"
            " forcée. Lettre officielle envoyée le 18 juin 2026."
        ),
        "detected_at": "2026-06-18T18:00:00Z",
        "expires_at": "2026-08-18T23:59:00Z",
        "urgency": "CRITICAL",
        "estimated_revenue_EUR": 780000,
        "action_required": (
            "Obtenir la liste des clients Enablon via partenaires. Campagne de migration"
            " 'Switch in 30 days' avec garantie de reprise de données. Deadline naturelle"
            " du client : fin septembre pour sécuriser Q4."
        ),
        "probability_success_pct": 61,
    },
    {
        "signal_id": "SIG-2026-012",
        "type": "REGULATORY_DEADLINE_WINDOW",
        "description": (
            "Le gouvernement belge accélère sa transposition CSDDD et impose aux entreprises"
            " de plus de 250 salariés un audit de conformité avant le 1er octobre 2026."
            " Marché belge sous-adressé, quasi aucun concurrent local actif."
        ),
        "detected_at": "2026-06-20T12:00:00Z",
        "expires_at": "2026-08-01T23:59:00Z",
        "urgency": "HIGH",
        "estimated_revenue_EUR": 290000,
        "action_required": (
            "Activer le réseau partenaire Benelux. Adapter le site en néerlandais/flamand."
            " Cibler les fédérations patronales (FEB/VBO) pour co-webinaire juillet."
        ),
        "probability_success_pct": 49,
    },
]

CAPTURE_STRATEGIES: dict[str, dict] = {
    "RAPID_OUTREACH": {
        "label": "Outreach Éclair",
        "execution_time_hours": 4,
        "required_resources": [
            "Commercial senior × 1",
            "Liste contacts qualifiés",
            "Template email personnalisé",
            "Séquence LinkedIn Sales Navigator",
        ],
        "expected_conversion_rate_pct": 12,
        "risk_level": "LOW",
    },
    "CONTENT_HIJACKING": {
        "label": "Détournement de Contenu",
        "execution_time_hours": 6,
        "required_resources": [
            "Content marketer × 1",
            "Designer × 0.5",
            "Approbation CEO pour prise de parole",
            "Compte LinkedIn + blog actif",
        ],
        "expected_conversion_rate_pct": 8,
        "risk_level": "LOW",
    },
    "EVENT_AMBUSH": {
        "label": "Embuscade Événementielle",
        "execution_time_hours": 48,
        "required_resources": [
            "Commercial senior × 2",
            "Budget stand/sponsoring 15-30K€",
            "Démo live CaelumSwarm™ prête",
            "Kits prospectus sectoriels × 200",
        ],
        "expected_conversion_rate_pct": 18,
        "risk_level": "MEDIUM",
    },
    "PARTNER_ACTIVATION": {
        "label": "Activation Partenaire",
        "execution_time_hours": 12,
        "required_resources": [
            "Directeur Partenariats × 1",
            "Term sheet template",
            "Démo technique API/intégration",
            "NDA + accord cadre standard",
        ],
        "expected_conversion_rate_pct": 28,
        "risk_level": "MEDIUM",
    },
    "REGULATORY_ARBITRAGE": {
        "label": "Arbitrage Réglementaire",
        "execution_time_hours": 24,
        "required_resources": [
            "Expert juridique CSDDD × 1",
            "Content marketer × 1",
            "Base de données prospects filtrée par pays/seuil réglementaire",
            "Webinaire ou guide PDF exclusif",
        ],
        "expected_conversion_rate_pct": 22,
        "risk_level": "LOW",
    },
}

OPPORTUNITY_SCORING_MATRIX: dict[str, dict] = {
    "strategic_fit": {
        "weight": 0.25,
        "scoring_guide": {
            "LOW": 20,
            "MEDIUM": 50,
            "HIGH": 80,
            "CRITICAL": 100,
        },
    },
    "revenue_potential": {
        "weight": 0.25,
        "scoring_guide": {
            "LOW": 20,       # < 100K€
            "MEDIUM": 50,    # 100K–400K€
            "HIGH": 80,      # 400K–800K€
            "CRITICAL": 100, # > 800K€
        },
    },
    "win_probability": {
        "weight": 0.20,
        "scoring_guide": {
            "LOW": 20,       # < 30%
            "MEDIUM": 50,    # 30–50%
            "HIGH": 80,      # 50–70%
            "CRITICAL": 100, # > 70%
        },
    },
    "time_sensitivity": {
        "weight": 0.15,
        "scoring_guide": {
            "LOW": 20,       # > 60 jours
            "MEDIUM": 50,    # 30–60 jours
            "HIGH": 80,      # 7–30 jours
            "CRITICAL": 100, # < 7 jours
        },
    },
    "resource_requirement": {
        "weight": 0.15,
        "scoring_guide": {
            "LOW": 100,      # minimal — 1 personne, < 4h
            "MEDIUM": 70,    # modéré — équipe restreinte, < 48h
            "HIGH": 40,      # important — plusieurs équipes, > 48h
            "CRITICAL": 10,  # très lourd — budget > 50K€ ou mobilisation totale
        },
    },
}

# ---------------------------------------------------------------------------
# 2. HELPER UTILITIES
# ---------------------------------------------------------------------------

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(iso_str: str) -> datetime:
    """Parse ISO-8601 string to aware datetime (UTC)."""
    # Replace trailing Z with +00:00 for fromisoformat compatibility
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


def _days_until(iso_str: str) -> float:
    delta = _parse_iso(iso_str) - _now_utc()
    return delta.total_seconds() / 86400


def _revenue_band(eur: int) -> str:
    if eur > 800_000:
        return "CRITICAL"
    if eur > 400_000:
        return "HIGH"
    if eur > 100_000:
        return "MEDIUM"
    return "LOW"


def _probability_band(pct: int) -> str:
    if pct > 70:
        return "CRITICAL"
    if pct > 50:
        return "HIGH"
    if pct >= 30:
        return "MEDIUM"
    return "LOW"


def _time_sensitivity_band(days: float) -> str:
    if days < 7:
        return "CRITICAL"
    if days < 30:
        return "HIGH"
    if days < 60:
        return "MEDIUM"
    return "LOW"


def _urgency_to_strategic_fit(urgency: str, opp_type: str) -> str:
    """Map signal urgency + type to strategic fit score band."""
    high_relevance_types = {
        k for k, v in OPPORTUNITY_TYPES.items() if v["caelum_relevance"] == "HIGH"
    }
    if urgency == "CRITICAL" and opp_type in high_relevance_types:
        return "CRITICAL"
    if urgency == "CRITICAL" or (urgency == "HIGH" and opp_type in high_relevance_types):
        return "HIGH"
    if urgency == "HIGH":
        return "MEDIUM"
    return "LOW"


def _resource_band(opp_type: str, urgency: str) -> str:
    """Estimate resource requirement band from opportunity type and urgency."""
    fast_types = {"COMPETITOR_FAILURE", "MEDIA_MOMENT"}
    heavy_types = {"CONFERENCE_TIMING", "PARTNERSHIP_WINDOW"}
    if opp_type in fast_types:
        return "LOW"
    if urgency == "CRITICAL" and opp_type in heavy_types:
        return "HIGH"
    if opp_type in heavy_types:
        return "MEDIUM"
    return "MEDIUM"


def _best_strategy(signal: dict) -> str:
    """Return the most appropriate CAPTURE_STRATEGIES key for a signal."""
    opp_type = signal["type"]
    urgency = signal["urgency"]

    mapping: dict[str, str] = {
        "REGULATORY_DEADLINE_WINDOW": "REGULATORY_ARBITRAGE",
        "COMPETITOR_FAILURE": "RAPID_OUTREACH",
        "MARKET_FUNDING_EVENT": "PARTNER_ACTIVATION",
        "MEDIA_MOMENT": "CONTENT_HIJACKING",
        "CONFERENCE_TIMING": "EVENT_AMBUSH",
        "TALENT_AVAILABILITY": "RAPID_OUTREACH",
        "PARTNERSHIP_WINDOW": "PARTNER_ACTIVATION",
        "GRANT_OR_SUBSIDY": "REGULATORY_ARBITRAGE",
    }
    strategy = mapping.get(opp_type, "RAPID_OUTREACH")
    # Override: CRITICAL urgency competitor or partner → RAPID_OUTREACH beats slower strategies
    if urgency == "CRITICAL" and opp_type == "COMPETITOR_FAILURE":
        strategy = "RAPID_OUTREACH"
    return strategy


# ---------------------------------------------------------------------------
# 3. CORE FUNCTIONS
# ---------------------------------------------------------------------------

def score_opportunity(signal: dict) -> dict:
    """
    Score a single opportunity across all OPPORTUNITY_SCORING_MATRIX dimensions.

    Returns:
        dimension_scores   : per-dimension raw score (0-100) and band
        composite_score    : weighted aggregate (0-100)
        tier               : ÉCLAIR / HAUTE / MOYENNE / FAIBLE
        recommended_strategy: key into CAPTURE_STRATEGIES
        capture_plan_outline: brief 5-step action sequence
    """
    matrix = OPPORTUNITY_SCORING_MATRIX
    days_left = _days_until(signal["expires_at"])

    # Derive bands
    bands: dict[str, str] = {
        "strategic_fit": _urgency_to_strategic_fit(signal["urgency"], signal["type"]),
        "revenue_potential": _revenue_band(signal["estimated_revenue_EUR"]),
        "win_probability": _probability_band(signal["probability_success_pct"]),
        "time_sensitivity": _time_sensitivity_band(days_left),
        "resource_requirement": _resource_band(signal["type"], signal["urgency"]),
    }

    # Compute raw scores
    dimension_scores: dict[str, dict] = {}
    composite = 0.0
    for dim, cfg in matrix.items():
        band = bands[dim]
        raw = cfg["scoring_guide"][band]
        weighted = raw * cfg["weight"]
        composite += weighted
        dimension_scores[dim] = {
            "band": band,
            "raw_score": raw,
            "weight": cfg["weight"],
            "weighted_contribution": round(weighted, 2),
        }

    composite_score = round(composite, 1)

    # Tier classification
    if composite_score >= 85:
        tier = "ÉCLAIR"
    elif composite_score >= 65:
        tier = "HAUTE"
    elif composite_score >= 40:
        tier = "MOYENNE"
    else:
        tier = "FAIBLE"

    strategy_key = _best_strategy(signal)
    strategy = CAPTURE_STRATEGIES[strategy_key]
    opp_type_info = OPPORTUNITY_TYPES[signal["type"]]

    capture_plan_outline = [
        f"[H+0] Valider le signal en interne et désigner un 'owner' dédié.",
        f"[H+{strategy['execution_time_hours']//4}] Préparer les ressources : {', '.join(strategy['required_resources'][:2])}.",
        f"[H+{strategy['execution_time_hours']//2}] Exécuter l'action principale — {strategy['label']}.",
        f"[H+{strategy['execution_time_hours']}] Premier point de contact / publication / dépôt effectué.",
        f"[H+{min(strategy['execution_time_hours'] * 2, int(opp_type_info['response_time_target_hours']) + strategy['execution_time_hours'])}] "
        f"Suivi relance et qualification pipeline dans CRM.",
    ]

    return {
        "signal_id": signal["signal_id"],
        "description_short": signal["description"][:120] + "...",
        "dimension_scores": dimension_scores,
        "composite_score": composite_score,
        "tier": tier,
        "days_remaining": round(days_left, 1),
        "recommended_strategy": strategy_key,
        "strategy_label": strategy["label"],
        "capture_plan_outline": capture_plan_outline,
    }


def detect_opportunities(signals: list[dict], filters: dict | None = None) -> dict:
    """
    Scans all live signals and returns a prioritized opportunity landscape.

    Args:
        signals : list of signal dicts (from MARKET_SIGNALS_LIVE)
        filters : optional dict with keys: min_score (int), urgency (list[str]),
                  type (list[str]), min_revenue_EUR (int)

    Returns:
        opportunities            : full list sorted by composite_score DESC
        total_pipeline_EUR       : sum of estimated_revenue_EUR × probability
        expiring_soon            : signals expiring in < 48h
        recommended_immediate_actions : top 3 actions to take today
    """
    filters = filters or {}
    min_score = filters.get("min_score", 0)
    urgency_filter = filters.get("urgency", [])
    type_filter = filters.get("type", [])
    min_revenue = filters.get("min_revenue_EUR", 0)

    scored: list[dict] = []
    for signal in signals:
        # Apply filters
        if urgency_filter and signal["urgency"] not in urgency_filter:
            continue
        if type_filter and signal["type"] not in type_filter:
            continue
        if signal["estimated_revenue_EUR"] < min_revenue:
            continue

        result = score_opportunity(signal)
        if result["composite_score"] >= min_score:
            # Merge signal metadata into scored result
            result["signal"] = signal
            scored.append(result)

    # Sort by composite score DESC, then by revenue DESC
    scored.sort(
        key=lambda x: (x["composite_score"], x["signal"]["estimated_revenue_EUR"]),
        reverse=True,
    )

    # Total pipeline (probability-weighted)
    total_pipeline = sum(
        s["signal"]["estimated_revenue_EUR"] * s["signal"]["probability_success_pct"] / 100
        for s in scored
    )

    # Expiring soon: < 48h
    expiring_soon = [
        {
            "signal_id": s["signal_id"],
            "description": s["signal"]["description"][:100] + "...",
            "expires_at": s["signal"]["expires_at"],
            "days_remaining": s["days_remaining"],
            "tier": s["tier"],
        }
        for s in scored
        if s["days_remaining"] < 2
    ]

    # Recommended immediate actions: top 3 CRITICAL or ÉCLAIR/HAUTE tier
    top_actions = [s for s in scored if s["tier"] in ("ÉCLAIR", "HAUTE")][:3]
    recommended_immediate_actions = [
        {
            "rank": i + 1,
            "signal_id": s["signal_id"],
            "tier": s["tier"],
            "score": s["composite_score"],
            "action": s["signal"]["action_required"][:200],
            "strategy": s["strategy_label"],
            "deadline": s["signal"]["expires_at"],
        }
        for i, s in enumerate(top_actions)
    ]

    return {
        "scan_timestamp": _now_utc().isoformat(),
        "signals_scanned": len(signals),
        "signals_qualified": len(scored),
        "opportunities": scored,
        "total_pipeline_EUR": round(total_pipeline, 0),
        "expiring_soon": expiring_soon,
        "recommended_immediate_actions": recommended_immediate_actions,
    }


def generate_capture_brief(opportunity: dict, strategy: str) -> dict:
    """
    Creates a rapid execution brief (under 2 pages) for seizing an opportunity.

    Args:
        opportunity : scored opportunity dict (output from score_opportunity merged with signal)
        strategy    : key from CAPTURE_STRATEGIES

    Returns:
        situation, opportunity_window, our_advantage, action_plan (5 steps),
        resources_needed, success_metrics, risk_if_we_miss
    """
    signal = opportunity.get("signal", opportunity)  # handle both merged and raw signal
    strat = CAPTURE_STRATEGIES.get(strategy, CAPTURE_STRATEGIES["RAPID_OUTREACH"])
    opp_type = OPPORTUNITY_TYPES.get(signal["type"], {})
    days_left = _days_until(signal["expires_at"])
    hours_left = days_left * 24

    # Revenue projections
    expected_value = round(
        signal["estimated_revenue_EUR"]
        * signal["probability_success_pct"] / 100
        * strat["expected_conversion_rate_pct"] / 100,
        0,
    )

    situation = (
        f"Signal détecté le {signal['detected_at'][:10]} — Type : {opp_type.get('label', signal['type'])}. "
        f"{signal['description']} "
        f"Ce signal est classifié {signal['urgency']} avec une fenêtre de {round(days_left, 0):.0f} jours "
        f"(expiration : {signal['expires_at'][:10]}). Le potentiel brut est estimé à "
        f"{signal['estimated_revenue_EUR']:,}€ avec une probabilité de succès de {signal['probability_success_pct']}%."
    )

    opportunity_window = {
        "opens": signal["detected_at"][:10],
        "closes": signal["expires_at"][:10],
        "days_remaining": round(days_left, 1),
        "hours_remaining": round(hours_left, 0),
        "urgency_level": signal["urgency"],
        "market_window_benchmark": f"{opp_type.get('avg_window_days', 'N/A')} jours (moyenne type {signal['type']})",
        "response_target": f"Action initiale sous {opp_type.get('response_time_target_hours', 24)}h",
    }

    our_advantage = (
        f"CaelumSwarm™ est la seule solution d'intelligence réglementaire CSDDD avec "
        f"couverture multi-juridictionnelle (FR/DE/NL/BE/ES) et analyse automatisée "
        f"de la chaîne d'approvisionnement. Pour ce signal de type '{signal['type']}', "
        f"notre avantage décisif est : (1) rapidité de déploiement — go-live en 30 jours, "
        f"(2) données propriétaires sur {len(MARKET_SIGNALS_LIVE)}+ signaux de marché actifs, "
        f"(3) expertise CSDDD depth-first vs. les concurrents généralistes ESG. "
        f"La stratégie '{strat['label']}' exploite exactement ce différentiel avec un taux "
        f"de conversion attendu de {strat['expected_conversion_rate_pct']}%."
    )

    exec_hours = strat["execution_time_hours"]
    action_plan = [
        {
            "step": 1,
            "timing": "H+0 (maintenant)",
            "duration_hours": 1,
            "action": f"Valider le brief en équipe restreinte (CEO/Commercial/Expert CSDDD). Désigner le lead owner. Confirmer disponibilité des ressources : {', '.join(strat['required_resources'])}.",
            "owner": "CEO + Directeur Commercial",
        },
        {
            "step": 2,
            "timing": f"H+1 à H+{exec_hours // 4}",
            "duration_hours": exec_hours // 4,
            "action": f"Préparer les assets de capture : personnaliser le pitch deck pour ce signal, briefer {strat['required_resources'][0]} sur le contexte spécifique, configurer le tracking CRM.",
            "owner": "Commercial Senior + Marketing",
        },
        {
            "step": 3,
            "timing": f"H+{exec_hours // 4} à H+{exec_hours // 2}",
            "duration_hours": exec_hours // 4,
            "action": f"Exécution principale — {strat['label']} : {signal['action_required'][:300]}",
            "owner": "Commercial Senior",
        },
        {
            "step": 4,
            "timing": f"H+{exec_hours // 2} à H+{exec_hours}",
            "duration_hours": exec_hours // 2,
            "action": "Premier contact établi. Qualifier les réponses reçues (Très Intéressé / Intéressé / Pas maintenant). Logger dans CRM. Programmer les relances automatiques J+2, J+5.",
            "owner": "Commercial Senior + CRM",
        },
        {
            "step": 5,
            "timing": f"H+{exec_hours} à H+{exec_hours * 2}",
            "duration_hours": exec_hours,
            "action": "Bilan intermédiaire : nombre de contacts établis, taux de réponse, deals ouverts. Décision Go/No-Go pour escalade ou changement de stratégie. Rapport au CODIR.",
            "owner": "Directeur Commercial + CEO",
        },
    ]

    resources_needed = {
        "human": strat["required_resources"],
        "time_hours_total": exec_hours * 2,
        "budget_estimate_EUR": round(exec_hours * 2 * 250, 0),  # ~250€/h fully-loaded
        "risk_level": strat["risk_level"],
        "go_live_readiness": "Immédiate — assets CaelumSwarm™ disponibles",
    }

    success_metrics = {
        "primary_kpi": f"{strat['expected_conversion_rate_pct']}% taux de conversion → "
                       f"{round(signal['estimated_revenue_EUR'] * strat['expected_conversion_rate_pct'] / 100):,}€ TCV",
        "expected_value_EUR": int(expected_value),
        "secondary_kpis": [
            f"Nombre de contacts initiaux sous H+{exec_hours} : ≥ 10",
            "Nombre de démos qualifiées sous J+7 : ≥ 3",
            "Pipeline CRM ouvert sous J+14 : ≥ 2 deals",
        ],
        "timeline_to_first_revenue": "30-60 jours si deal signé cette semaine",
    }

    missed_value = round(
        signal["estimated_revenue_EUR"] * signal["probability_success_pct"] / 100
    )
    risk_if_we_miss = (
        f"Ne pas agir dans les {opp_type.get('response_time_target_hours', 24)}h suivant la détection "
        f"signifie : (1) perte de {missed_value:,}€ de pipeline qualifié, "
        f"(2) la fenêtre '{signal['type']}' se referme en {round(days_left, 0):.0f} jours — "
        f"la prochaine occurrence similaire n'est pas garantie avant 12-18 mois, "
        f"(3) un concurrent (EY, Deloitte, ou un pur-player SaaS) capturera ce momentum, "
        f"renforçant sa position au moment précis où la pression CSDDD juillet 2027 atteint son pic."
    )

    return {
        "brief_id": f"BRIEF-{signal['signal_id']}-{strategy[:4]}",
        "generated_at": _now_utc().isoformat(),
        "signal_id": signal["signal_id"],
        "strategy": strategy,
        "tier": opportunity.get("tier", "N/A"),
        "composite_score": opportunity.get("composite_score", "N/A"),
        "situation": situation,
        "opportunity_window": opportunity_window,
        "our_advantage": our_advantage,
        "action_plan": action_plan,
        "resources_needed": resources_needed,
        "success_metrics": success_metrics,
        "risk_if_we_miss": risk_if_we_miss,
    }


def prioritize_weekly_opportunities(all_opportunities: list[dict]) -> dict:
    """
    Builds a prioritized weekly action plan from a list of scored opportunities.

    Args:
        all_opportunities : list of scored opportunity dicts (from detect_opportunities)

    Returns:
        monday_priority, top_3_this_week with full briefs,
        resource_allocation_hours, expected_weekly_revenue_EUR, go_no_go_decisions
    """
    # Separate by tier
    eclair = [o for o in all_opportunities if o["tier"] == "ÉCLAIR"]
    haute = [o for o in all_opportunities if o["tier"] == "HAUTE"]
    moyenne = [o for o in all_opportunities if o["tier"] == "MOYENNE"]
    faible = [o for o in all_opportunities if o["tier"] == "FAIBLE"]

    top_3 = (eclair + haute)[:3]

    # Monday priority: actions that must start day 1
    monday_priority = []
    for i, opp in enumerate(top_3):
        signal = opp["signal"]
        days_left = _days_until(signal["expires_at"])
        monday_priority.append({
            "rank": i + 1,
            "signal_id": opp["signal_id"],
            "tier": opp["tier"],
            "score": opp["composite_score"],
            "description": signal["description"][:120] + "...",
            "urgency": signal["urgency"],
            "days_remaining": round(days_left, 1),
            "revenue_potential_EUR": signal["estimated_revenue_EUR"],
            "first_action": signal["action_required"][:180],
            "strategy": opp["strategy_label"],
        })

    # Generate full briefs for top 3
    top_3_briefs = []
    for opp in top_3:
        brief = generate_capture_brief(opp, opp["recommended_strategy"])
        top_3_briefs.append(brief)

    # Resource allocation (hours per strategy)
    total_hours = 0
    allocation: dict[str, int] = {}
    for opp in top_3:
        strat_key = opp["recommended_strategy"]
        strat = CAPTURE_STRATEGIES[strat_key]
        h = strat["execution_time_hours"] * 2  # include follow-up
        allocation[strat_key] = allocation.get(strat_key, 0) + h
        total_hours += h

    resource_allocation = {
        "total_team_hours_this_week": total_hours,
        "breakdown_by_strategy": allocation,
        "recommended_headcount": max(2, len(top_3)),
        "budget_estimate_EUR": round(total_hours * 250, 0),
        "note": "Allocation basée sur top 3 opportunités. Les tiers MOYENNE/FAIBLE en file d'attente.",
    }

    # Expected revenue (probability × conversion)
    expected_weekly_revenue = 0.0
    for opp in top_3:
        signal = opp["signal"]
        strat = CAPTURE_STRATEGIES[opp["recommended_strategy"]]
        expected_weekly_revenue += (
            signal["estimated_revenue_EUR"]
            * signal["probability_success_pct"] / 100
            * strat["expected_conversion_rate_pct"] / 100
        )

    # Go/No-Go for lower tiers
    go_no_go_decisions = []
    for opp in (moyenne + faible):
        signal = opp["signal"]
        days_left = _days_until(signal["expires_at"])
        decision = "GO" if opp["tier"] == "MOYENNE" and days_left < 14 else "NO-GO cette semaine"
        go_no_go_decisions.append({
            "signal_id": opp["signal_id"],
            "tier": opp["tier"],
            "score": opp["composite_score"],
            "decision": decision,
            "rationale": (
                f"Score {opp['composite_score']}/100 — "
                f"{round(days_left, 0):.0f}j restants — "
                f"Capacité équipe réservée pour top 3 cette semaine."
                if decision == "NO-GO cette semaine"
                else f"Score {opp['composite_score']}/100 — fenêtre courte ({round(days_left, 0):.0f}j) — activer si top 3 libèrent de la bande passante."
            ),
            "revisit_date": (
                (_now_utc() + timedelta(days=7)).strftime("%Y-%m-%d")
                if "NO-GO" in decision else "Cette semaine (J+3)"
            ),
        })

    return {
        "week_of": _now_utc().strftime("%Y-W%W"),
        "generated_at": _now_utc().isoformat(),
        "summary": {
            "eclair_count": len(eclair),
            "haute_count": len(haute),
            "moyenne_count": len(moyenne),
            "faible_count": len(faible),
            "total_qualified": len(all_opportunities),
        },
        "monday_priority": monday_priority,
        "top_3_this_week": top_3_briefs,
        "resource_allocation_hours": resource_allocation,
        "expected_weekly_revenue_EUR": round(expected_weekly_revenue, 0),
        "go_no_go_decisions": go_no_go_decisions,
    }


# ---------------------------------------------------------------------------
# 4. DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Full demonstration of the Flash Opportunity Detector Agent for CaelumSwarm™.
    Scans all 12 live signals, scores top 3 in detail, generates capture brief
    for the highest-scoring (ÉCLAIR) opportunity, and builds the weekly priority plan.
    """
    SEP = "=" * 72
    sep = "-" * 72

    print(SEP)
    print("  CAELUMSWARM™ — AGENT DÉTECTEUR D'OPPORTUNITÉS ÉCLAIR")
    print(f"  Scan du {_now_utc().strftime('%d/%m/%Y %H:%M UTC')}  |  T-13 mois CSDDD deadline")
    print(SEP)

    # ── ÉTAPE 1 : Détection complète ─────────────────────────────────────────
    print("\n[ÉTAPE 1/4] DÉTECTION — Scan de tous les signaux actifs\n")
    detection = detect_opportunities(MARKET_SIGNALS_LIVE)

    print(f"  Signaux scannés    : {detection['signals_scanned']}")
    print(f"  Signaux qualifiés  : {detection['signals_qualified']}")
    print(f"  Pipeline total     : {detection['total_pipeline_EUR']:,.0f} € (pondéré probabilité)")
    print(f"  Signaux exp. <48h  : {len(detection['expiring_soon'])}")

    print(f"\n  Classement des opportunités :")
    print(f"  {'#':<3} {'ID':<15} {'Score':<8} {'Tier':<10} {'Rev.€':<12} {'Urgence':<10} {'Expire'}")
    print(f"  {sep}")
    for i, opp in enumerate(detection["opportunities"]):
        sig = opp["signal"]
        print(
            f"  {i+1:<3} {opp['signal_id']:<15} {opp['composite_score']:<8} "
            f"{opp['tier']:<10} {sig['estimated_revenue_EUR']:>10,}€  "
            f"{sig['urgency']:<10} {sig['expires_at'][:10]}"
        )

    if detection["expiring_soon"]:
        print(f"\n  ⚡ ALERTE — Signaux expirant sous 48h :")
        for s in detection["expiring_soon"]:
            print(f"    • {s['signal_id']} — {s['days_remaining']:.1f}j — {s['description'][:80]}...")

    print(f"\n  Actions immédiates recommandées :")
    for action in detection["recommended_immediate_actions"]:
        print(f"  [{action['rank']}] {action['signal_id']} ({action['tier']} | score {action['score']})")
        print(f"      Stratégie : {action['strategy']}")
        print(f"      Action    : {action['action'][:160]}...")
        print()

    # ── ÉTAPE 2 : Score détaillé top 3 ───────────────────────────────────────
    print(sep)
    print("\n[ÉTAPE 2/4] SCORING DÉTAILLÉ — Top 3 opportunités\n")

    top_3 = detection["opportunities"][:3]
    for rank, opp in enumerate(top_3, 1):
        sig = opp["signal"]
        print(f"  #{rank} — {opp['signal_id']} | Tier : {opp['tier']} | Score : {opp['composite_score']}/100")
        print(f"  Type : {OPPORTUNITY_TYPES[sig['type']]['label']}")
        print(f"  Revenu estimé : {sig['estimated_revenue_EUR']:,}€  |  Probabilité : {sig['probability_success_pct']}%")
        print(f"  Expiration : {sig['expires_at'][:10]}  |  Jours restants : {opp['days_remaining']:.1f}")
        print(f"  Stratégie recommandée : {opp['strategy_label']}")
        print(f"\n  Détail des dimensions :")
        for dim, scores in opp["dimension_scores"].items():
            bar = "█" * (scores["raw_score"] // 10) + "░" * (10 - scores["raw_score"] // 10)
            print(
                f"    {dim:<22} [{bar}] {scores['raw_score']:>3}/100  "
                f"(band: {scores['band']:<8} → contrib: {scores['weighted_contribution']:.1f})"
            )
        print(f"\n  Plan de capture :")
        for step in opp["capture_plan_outline"]:
            print(f"    {step}")
        print()

    # ── ÉTAPE 3 : Brief de capture pour le #1 ÉCLAIR ─────────────────────────
    print(sep)
    print("\n[ÉTAPE 3/4] BRIEF DE CAPTURE — Opportunité #1 (tier ÉCLAIR)\n")

    top_opp = detection["opportunities"][0]
    brief = generate_capture_brief(top_opp, top_opp["recommended_strategy"])

    print(f"  Brief ID    : {brief['brief_id']}")
    print(f"  Généré le   : {brief['generated_at'][:19]}")
    print(f"  Score       : {brief['composite_score']}/100 — Tier {brief['tier']}")
    print(f"\n  SITUATION")
    print(f"  {brief['situation']}")

    ow = brief["opportunity_window"]
    print(f"\n  FENÊTRE D'OPPORTUNITÉ")
    print(f"  Ouverture   : {ow['opens']}  |  Fermeture : {ow['closes']}")
    print(f"  Temps restant : {ow['days_remaining']} jours / {ow['hours_remaining']:.0f}h")
    print(f"  Urgence : {ow['urgency_level']}  |  Cible réponse : {ow['response_target']}")

    print(f"\n  NOTRE AVANTAGE")
    print(f"  {brief['our_advantage']}")

    print(f"\n  PLAN D'ACTION (5 étapes)")
    for step in brief["action_plan"]:
        print(f"  Étape {step['step']} | {step['timing']} | Durée : {step['duration_hours']}h | Owner : {step['owner']}")
        print(f"    {step['action'][:200]}")

    res = brief["resources_needed"]
    print(f"\n  RESSOURCES NÉCESSAIRES")
    print(f"  Humain     : {', '.join(res['human'])}")
    print(f"  Temps total : {res['time_hours_total']}h  |  Coût estimé : {res['budget_estimate_EUR']:,}€")
    print(f"  Niveau risque : {res['risk_level']}  |  Disponibilité : {res['go_live_readiness']}")

    sm = brief["success_metrics"]
    print(f"\n  MÉTRIQUES DE SUCCÈS")
    print(f"  KPI principal    : {sm['primary_kpi']}")
    print(f"  Valeur attendue  : {sm['expected_value_EUR']:,}€")
    for kpi in sm["secondary_kpis"]:
        print(f"    • {kpi}")
    print(f"  Premier revenu   : {sm['timeline_to_first_revenue']}")

    print(f"\n  RISQUE SI ON NE BOUGE PAS")
    print(f"  {brief['risk_if_we_miss']}")

    # ── ÉTAPE 4 : Plan hebdomadaire ───────────────────────────────────────────
    print(f"\n{sep}")
    print("\n[ÉTAPE 4/4] PLAN HEBDOMADAIRE PRIORITAIRE\n")

    weekly = prioritize_weekly_opportunities(detection["opportunities"])

    summ = weekly["summary"]
    print(f"  Semaine : {weekly['week_of']}  |  Généré : {weekly['generated_at'][:19]}")
    print(
        f"  Répartition : {summ['eclair_count']} ÉCLAIR · "
        f"{summ['haute_count']} HAUTE · "
        f"{summ['moyenne_count']} MOYENNE · "
        f"{summ['faible_count']} FAIBLE"
    )
    print(f"  Revenu hebdomadaire attendu : {weekly['expected_weekly_revenue_EUR']:,.0f} €")

    alloc = weekly["resource_allocation_hours"]
    print(f"\n  ALLOCATION RESSOURCES")
    print(f"  Heures totales     : {alloc['total_team_hours_this_week']}h")
    print(f"  Effectif recommandé : {alloc['recommended_headcount']} personnes")
    print(f"  Budget estimé      : {alloc['budget_estimate_EUR']:,}€")
    for strat_key, hours in alloc["breakdown_by_strategy"].items():
        label = CAPTURE_STRATEGIES[strat_key]["label"]
        print(f"    • {label:<30} {hours}h")

    print(f"\n  PRIORITÉS DU LUNDI")
    for p in weekly["monday_priority"]:
        print(
            f"  [{p['rank']}] {p['signal_id']} | {p['tier']} | Score {p['score']} | "
            f"{p['days_remaining']}j restants | Rev. {p['revenue_potential_EUR']:,}€"
        )
        print(f"      {p['first_action'][:160]}...")

    if weekly["go_no_go_decisions"]:
        print(f"\n  DÉCISIONS GO / NO-GO (tiers inférieurs)")
        for dec in weekly["go_no_go_decisions"]:
            status = "GO  " if dec["decision"] == "GO" else "WAIT"
            print(f"  [{status}] {dec['signal_id']} ({dec['tier']} | {dec['score']}) — {dec['decision']}")
            print(f"         Rationale : {dec['rationale'][:140]}")
            print(f"         Revisit   : {dec['revisit_date']}")

    print(f"\n{SEP}")
    print("  SCAN TERMINÉ — Toutes les opportunités ont été analysées et priorisées.")
    print(f"  Pipeline total CaelumSwarm™ cette semaine : {detection['total_pipeline_EUR']:,.0f} €")
    print(SEP)

    return True


# ---------------------------------------------------------------------------
# 5. ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if not success:
        raise SystemExit(1)
