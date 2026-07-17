"""
Agent Auto-Optimiseur de Ressources & Coûts — analyse automatiquement les dépenses
opérationnelles de CaelumSwarm™ et génère des optimisations IA pour réduire les coûts
sans dégrader la qualité d'analyse droits humains.

CaelumSwarm™ FinOps Intelligence Layer — Caelum Partners
"""

from __future__ import annotations

import math
from datetime import date
from typing import Any

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

COST_CATEGORIES: dict[str, dict[str, Any]] = {
    "CLOUD_COMPUTE": {
        "label": "Calcul Cloud (VM / conteneurs / GPU)",
        "monthly_EUR": 14_200,
        "variable_or_fixed": "HYBRID",
        "optimization_potential_pct": 35,
        "risk_if_reduced": "MEDIUM",
        "optimization_levers": [
            "Migration instances Spot/Preemptible pour workloads batch",
            "Auto-scaling horizontal basé sur la charge swarm",
            "Right-sizing des instances via métriques CPU/RAM réelles",
            "Arrêt automatique des environnements de dev hors heures ouvrées",
        ],
    },
    "AI_API_CALLS": {
        "label": "Appels API IA (LLM / embeddings / classification)",
        "monthly_EUR": 11_800,
        "variable_or_fixed": "VARIABLE",
        "optimization_potential_pct": 42,
        "risk_if_reduced": "MEDIUM",
        "optimization_levers": [
            "Couche de cache sémantique pour requêtes similaires",
            "Routage dynamique vers modèles moins coûteux pour tâches simples",
            "Traitement en batch des requêtes non-urgentes",
            "Compression des prompts et réduction des tokens superflus",
        ],
    },
    "DATA_STORAGE": {
        "label": "Stockage de données (S3 / bases de données / archives)",
        "monthly_EUR": 5_400,
        "variable_or_fixed": "HYBRID",
        "optimization_potential_pct": 28,
        "risk_if_reduced": "LOW",
        "optimization_levers": [
            "Tiering automatique cold/warm/hot selon l'âge des données",
            "Compression des données structurées (Parquet / Zstandard)",
            "Suppression des snapshots redondants et logs expirés",
            "Déduplication des datasets sources avant ingestion",
        ],
    },
    "BANDWIDTH": {
        "label": "Bande passante & transferts de données",
        "monthly_EUR": 3_100,
        "variable_or_fixed": "VARIABLE",
        "optimization_potential_pct": 30,
        "risk_if_reduced": "LOW",
        "optimization_levers": [
            "CDN pour les assets statiques et rapports exportés",
            "Compression gzip/brotli sur toutes les réponses API",
            "Colocalisation compute / stockage pour réduire les egress fees",
            "Agrégation des webhooks sortants vers les clients",
        ],
    },
    "MONITORING_TOOLS": {
        "label": "Outils de monitoring & observabilité",
        "monthly_EUR": 2_800,
        "variable_or_fixed": "FIXED",
        "optimization_potential_pct": 20,
        "risk_if_reduced": "HIGH",
        "optimization_levers": [
            "Consolidation des outils APM (réduire de 4 à 2 solutions)",
            "Réduction de la granularité des métriques non-critiques",
            "Auto-archivage des logs après 30 jours vers stockage froid",
        ],
    },
    "EXTERNAL_DATA_SOURCES": {
        "label": "Sources de données externes (API tiers / flux ONG / data brokers)",
        "monthly_EUR": 6_900,
        "variable_or_fixed": "FIXED",
        "optimization_potential_pct": 18,
        "risk_if_reduced": "HIGH",
        "optimization_levers": [
            "Renégociation des contrats annuels avec volume garanti",
            "Mutualisation des abonnements inter-waves via cache partagé",
            "Remplacement de sources commerciales par des flux ouverts validés",
        ],
    },
    "HUMAN_REVIEW": {
        "label": "Révision humaine & validation qualité droits humains",
        "monthly_EUR": 4_200,
        "variable_or_fixed": "HYBRID",
        "optimization_potential_pct": 15,
        "risk_if_reduced": "HIGH",
        "optimization_levers": [
            "Priorisation IA des cas à risque élevé pour review humaine",
            "Templates de validation structurés pour réduire le temps par cas",
            "Formation des reviewers aux outils d'assistance IA intégrés",
        ],
    },
    "COMPLIANCE_TOOLS": {
        "label": "Outils de conformité & sécurité (RGPD / audit / chiffrement)",
        "monthly_EUR": 1_600,
        "variable_or_fixed": "FIXED",
        "optimization_potential_pct": 10,
        "risk_if_reduced": "HIGH",
        "optimization_levers": [
            "Consolidation des licences audit dans un seul provider",
            "Automatisation des rapports de conformité périodiques",
        ],
    },
}

OPTIMIZATION_STRATEGIES: dict[str, dict[str, Any]] = {
    "CACHING_LAYER": {
        "label": "Couche de cache sémantique multi-niveaux",
        "implementation_effort_days": 8,
        "expected_savings_pct": 22,
        "quality_impact": "NONE",
        "payback_period_months": 1,
    },
    "BATCH_PROCESSING": {
        "label": "Traitement batch des analyses non-temps-réel",
        "implementation_effort_days": 5,
        "expected_savings_pct": 18,
        "quality_impact": "MINIMAL",
        "payback_period_months": 1,
    },
    "MODEL_DOWNGRADE_ROUTING": {
        "label": "Routage intelligent vers modèles IA moins coûteux",
        "implementation_effort_days": 12,
        "expected_savings_pct": 30,
        "quality_impact": "MINIMAL",
        "payback_period_months": 2,
    },
    "SPOT_INSTANCE_MIGRATION": {
        "label": "Migration workloads batch vers instances Spot",
        "implementation_effort_days": 10,
        "expected_savings_pct": 65,
        "quality_impact": "NONE",
        "payback_period_months": 1,
    },
    "DATA_COMPRESSION": {
        "label": "Compression & déduplication des données stockées",
        "implementation_effort_days": 4,
        "expected_savings_pct": 40,
        "quality_impact": "NONE",
        "payback_period_months": 1,
    },
    "LAZY_EVALUATION": {
        "label": "Évaluation paresseuse des entités à faible risque",
        "implementation_effort_days": 15,
        "expected_savings_pct": 25,
        "quality_impact": "MODERATE",
        "payback_period_months": 3,
    },
}

RESOURCE_METRICS: dict[str, dict[str, Any]] = {
    "cpu_utilization_pct": {
        "current": 34.2,
        "optimal": 65.0,
        "measurement_unit": "%",
    },
    "memory_utilization_pct": {
        "current": 51.8,
        "optimal": 72.0,
        "measurement_unit": "%",
    },
    "api_cache_hit_rate": {
        "current": 12.5,
        "optimal": 55.0,
        "measurement_unit": "%",
    },
    "storage_efficiency_pct": {
        "current": 58.0,
        "optimal": 85.0,
        "measurement_unit": "%",
    },
    "compute_waste_pct": {
        "current": 41.3,
        "optimal": 10.0,
        "measurement_unit": "%",
    },
}

COST_BENCHMARKS: dict[str, dict[str, Any]] = {
    "SEED": {
        "gross_margin_target_pct": 55,
        "cogs_as_pct_arr": 45,
        "infra_as_pct_arr": 25,
        "ai_costs_as_pct_revenue": 18,
        "benchmark_source": "SaaStr EU 2024 — AI-native SaaS Seed",
    },
    "SERIES_A": {
        "gross_margin_target_pct": 68,
        "cogs_as_pct_arr": 32,
        "infra_as_pct_arr": 15,
        "ai_costs_as_pct_revenue": 12,
        "benchmark_source": "Bessemer Venture Partners Cloud Index 2024",
    },
    "GROWTH": {
        "gross_margin_target_pct": 78,
        "cogs_as_pct_arr": 22,
        "infra_as_pct_arr": 8,
        "ai_costs_as_pct_revenue": 7,
        "benchmark_source": "OpenView SaaS Benchmarks 2024 — Growth Stage",
    },
}

# ---------------------------------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------------------------------


def analyze_cost_structure(
    monthly_costs: dict[str, float],
    monthly_revenue_EUR: float,
) -> dict[str, Any]:
    """
    Full cost structure analysis for CaelumSwarm™.

    Parameters
    ----------
    monthly_costs : dict mapping cost-category keys to EUR monthly spend
    monthly_revenue_EUR : current monthly revenue in EUR

    Returns
    -------
    dict with gross_margin, cogs_breakdown, unit_economics,
    vs_benchmark comparison, and red_flags list
    """
    if monthly_revenue_EUR <= 0:
        raise ValueError("monthly_revenue_EUR must be strictly positive")

    # --- Totals ---
    total_monthly_cost = sum(monthly_costs.values())
    arr = monthly_revenue_EUR * 12

    # --- Gross margin ---
    gross_profit = monthly_revenue_EUR - total_monthly_cost
    gross_margin_pct = (gross_profit / monthly_revenue_EUR) * 100

    # --- COGS breakdown ---
    cogs_breakdown: dict[str, dict[str, Any]] = {}
    for key, amount in monthly_costs.items():
        meta = COST_CATEGORIES.get(key, {})
        share_pct = (amount / total_monthly_cost * 100) if total_monthly_cost else 0
        pct_of_revenue = (amount / monthly_revenue_EUR) * 100
        cogs_breakdown[key] = {
            "label": meta.get("label", key),
            "monthly_EUR": amount,
            "share_of_total_costs_pct": round(share_pct, 2),
            "pct_of_revenue": round(pct_of_revenue, 2),
            "variable_or_fixed": meta.get("variable_or_fixed", "UNKNOWN"),
            "optimization_potential_EUR": round(
                amount * meta.get("optimization_potential_pct", 0) / 100, 0
            ),
        }

    # --- Unit economics (assumptions: 8 waves/month, 8 entities/wave, 1 report/wave) ---
    waves_per_month = 8
    entities_per_wave = 8
    cost_per_wave = total_monthly_cost / waves_per_month
    cost_per_entity = total_monthly_cost / (waves_per_month * entities_per_wave)
    cost_per_report = cost_per_wave  # 1 report per wave

    unit_economics = {
        "waves_per_month": waves_per_month,
        "entities_analyzed_per_month": waves_per_month * entities_per_wave,
        "cost_per_wave_EUR": round(cost_per_wave, 2),
        "cost_per_entity_analyzed_EUR": round(cost_per_entity, 2),
        "cost_per_report_EUR": round(cost_per_report, 2),
        "revenue_per_wave_EUR": round(monthly_revenue_EUR / waves_per_month, 2),
        "contribution_margin_per_wave_EUR": round(
            (monthly_revenue_EUR - total_monthly_cost) / waves_per_month, 2
        ),
    }

    # --- Benchmark comparison (detect stage) ---
    if arr < 200_000:
        stage = "SEED"
    elif arr < 2_000_000:
        stage = "SERIES_A"
    else:
        stage = "GROWTH"

    bmark = COST_BENCHMARKS[stage]
    infra_ai_monthly = monthly_costs.get("CLOUD_COMPUTE", 0) + monthly_costs.get(
        "AI_API_CALLS", 0
    )
    vs_benchmark = {
        "detected_stage": stage,
        "benchmark_source": bmark["benchmark_source"],
        "gross_margin": {
            "actual_pct": round(gross_margin_pct, 1),
            "target_pct": bmark["gross_margin_target_pct"],
            "delta_pts": round(gross_margin_pct - bmark["gross_margin_target_pct"], 1),
            "status": "OK" if gross_margin_pct >= bmark["gross_margin_target_pct"] else "BELOW_TARGET",
        },
        "cogs_as_pct_arr": {
            "actual_pct": round((total_monthly_cost * 12 / arr) * 100, 1),
            "target_pct": bmark["cogs_as_pct_arr"],
            "status": (
                "OK"
                if (total_monthly_cost * 12 / arr) * 100 <= bmark["cogs_as_pct_arr"]
                else "ABOVE_TARGET"
            ),
        },
        "ai_costs_as_pct_revenue": {
            "actual_pct": round(
                (monthly_costs.get("AI_API_CALLS", 0) / monthly_revenue_EUR) * 100, 1
            ),
            "target_pct": bmark["ai_costs_as_pct_revenue"],
            "status": (
                "OK"
                if (monthly_costs.get("AI_API_CALLS", 0) / monthly_revenue_EUR) * 100
                <= bmark["ai_costs_as_pct_revenue"]
                else "ABOVE_TARGET"
            ),
        },
        "infra_as_pct_arr": {
            "actual_pct": round((infra_ai_monthly * 12 / arr) * 100, 1),
            "target_pct": bmark["infra_as_pct_arr"],
        },
    }

    # --- Red flags ---
    red_flags: list[str] = []
    if gross_margin_pct < bmark["gross_margin_target_pct"]:
        red_flags.append(
            f"Marge brute {gross_margin_pct:.1f}% en-dessous de la cible benchmark "
            f"{bmark['gross_margin_target_pct']}% pour le stade {stage}"
        )
    if (monthly_costs.get("AI_API_CALLS", 0) / monthly_revenue_EUR) * 100 > bmark[
        "ai_costs_as_pct_revenue"
    ] * 1.5:
        red_flags.append(
            "Coûts API IA supérieurs de +50% au benchmark — cache sémantique urgent"
        )
    if RESOURCE_METRICS["compute_waste_pct"]["current"] > 35:
        red_flags.append(
            f"Gaspillage compute à {RESOURCE_METRICS['compute_waste_pct']['current']}% "
            f"(cible ≤ {RESOURCE_METRICS['compute_waste_pct']['optimal']}%) — "
            "right-sizing immédiat recommandé"
        )
    if RESOURCE_METRICS["api_cache_hit_rate"]["current"] < 20:
        red_flags.append(
            f"Taux de cache API à {RESOURCE_METRICS['api_cache_hit_rate']['current']}% "
            f"(cible ≥ {RESOURCE_METRICS['api_cache_hit_rate']['optimal']}%) — "
            "opportunité d'économies majeure non exploitée"
        )
    if total_monthly_cost > monthly_revenue_EUR:
        red_flags.append(
            "CRITIQUE : coûts opérationnels supérieurs au chiffre d'affaires mensuel — "
            "burn rate non viable"
        )

    return {
        "analysis_date": str(date.today()),
        "monthly_revenue_EUR": monthly_revenue_EUR,
        "arr_EUR": arr,
        "total_monthly_cost_EUR": total_monthly_cost,
        "gross_profit_monthly_EUR": round(gross_profit, 2),
        "gross_margin_pct": round(gross_margin_pct, 2),
        "cogs_breakdown": cogs_breakdown,
        "unit_economics": unit_economics,
        "vs_benchmark": vs_benchmark,
        "red_flags": red_flags,
        "total_optimization_potential_EUR": sum(
            v["optimization_potential_EUR"] for v in cogs_breakdown.values()
        ),
    }


def generate_optimization_plan(
    costs: dict[str, float],
    target_reduction_pct: float,
) -> dict[str, Any]:
    """
    Creates a prioritized optimization plan to achieve target cost reduction.

    Parameters
    ----------
    costs : dict mapping cost-category keys to EUR monthly spend
    target_reduction_pct : desired percentage reduction (0–100)

    Returns
    -------
    dict with quick_wins, medium_term, strategic lists and summary
    """
    if not (0 < target_reduction_pct <= 100):
        raise ValueError("target_reduction_pct must be between 0 and 100")

    total_cost = sum(costs.values())
    target_savings_EUR = total_cost * (target_reduction_pct / 100)

    quick_wins: list[dict[str, Any]] = []
    medium_term: list[dict[str, Any]] = []
    strategic: list[dict[str, Any]] = []

    # --- Quick wins: effort < 7 days, impact NONE or MINIMAL ---
    # 1. Spot instance migration for batch compute
    cloud_saving = costs.get("CLOUD_COMPUTE", 0) * 0.40  # 40% of batch workloads
    quick_wins.append({
        "action": "Migrer les workloads batch swarm vers instances Spot/Preemptible",
        "category": "CLOUD_COMPUTE",
        "strategy": "SPOT_INSTANCE_MIGRATION",
        "expected_savings_EUR": round(cloud_saving * 0.65, 0),
        "effort_days": 5,
        "risk": "LOW",
        "owner_role": "DevOps / SRE",
        "implementation_note": "Spot avec fallback on-demand via interruption handler",
    })

    # 2. Cache layer for AI API calls
    ai_saving = costs.get("AI_API_CALLS", 0) * OPTIMIZATION_STRATEGIES["CACHING_LAYER"]["expected_savings_pct"] / 100
    quick_wins.append({
        "action": "Déployer un cache sémantique Redis pour les appels LLM répétitifs",
        "category": "AI_API_CALLS",
        "strategy": "CACHING_LAYER",
        "expected_savings_EUR": round(ai_saving, 0),
        "effort_days": 8,
        "risk": "LOW",
        "owner_role": "Ingénieur IA / Backend",
        "implementation_note": "Embeddings similarity threshold ≥ 0.92 avant cache hit",
    })

    # 3. Data compression
    storage_saving = costs.get("DATA_STORAGE", 0) * OPTIMIZATION_STRATEGIES["DATA_COMPRESSION"]["expected_savings_pct"] / 100
    quick_wins.append({
        "action": "Activer la compression Zstandard sur les datasets swarm stockés",
        "category": "DATA_STORAGE",
        "strategy": "DATA_COMPRESSION",
        "expected_savings_EUR": round(storage_saving, 0),
        "effort_days": 4,
        "risk": "LOW",
        "owner_role": "Data Engineer",
        "implementation_note": "Ratio de compression attendu 3:1 sur données structurées",
    })

    # 4. Bandwidth CDN
    bw_saving = costs.get("BANDWIDTH", 0) * 0.35
    quick_wins.append({
        "action": "Activer CDN CloudFront/Cloudflare pour les exports PDF/JSON rapports",
        "category": "BANDWIDTH",
        "strategy": "DATA_COMPRESSION",
        "expected_savings_EUR": round(bw_saving, 0),
        "effort_days": 2,
        "risk": "LOW",
        "owner_role": "DevOps",
        "implementation_note": "Invalidation cache sur chaque nouvelle publication wave",
    })

    # --- Medium term: 1-3 months ---
    # 1. Model downgrade routing
    ai_routing_saving = costs.get("AI_API_CALLS", 0) * 0.20
    medium_term.append({
        "action": "Implémenter le routage dynamique : tâches simples → modèles légers",
        "category": "AI_API_CALLS",
        "strategy": "MODEL_DOWNGRADE_ROUTING",
        "expected_savings_EUR": round(ai_routing_saving, 0),
        "effort_days": 12,
        "risk": "MEDIUM",
        "owner_role": "Ingénieur IA / Architecte",
        "implementation_note": (
            "Classifier la complexité de la requête (score 0-1) avant dispatch ; "
            "conserver modèle premium pour entités critique ≥60"
        ),
    })

    # 2. Batch processing for non-urgent waves
    batch_saving = costs.get("CLOUD_COMPUTE", 0) * 0.18
    medium_term.append({
        "action": "Basculer 30% des waves planifiées en mode batch nocturne",
        "category": "CLOUD_COMPUTE",
        "strategy": "BATCH_PROCESSING",
        "expected_savings_EUR": round(batch_saving, 0),
        "effort_days": 5,
        "risk": "LOW",
        "owner_role": "Backend / Product",
        "implementation_note": "SLA batch : résultat disponible sous 8h vs 15min temps réel",
    })

    # 3. Monitoring consolidation
    monitoring_saving = costs.get("MONITORING_TOOLS", 0) * 0.25
    medium_term.append({
        "action": "Consolider APM : migrer de 4 outils vers Grafana Cloud unified",
        "category": "MONITORING_TOOLS",
        "strategy": "CACHING_LAYER",
        "expected_savings_EUR": round(monitoring_saving, 0),
        "effort_days": 10,
        "risk": "MEDIUM",
        "owner_role": "SRE / Infra",
        "implementation_note": "Maintenir alertes critique droits humains inchangées",
    })

    # 4. External data renegotiation
    ext_saving = costs.get("EXTERNAL_DATA_SOURCES", 0) * 0.15
    medium_term.append({
        "action": "Renégocier contrats data tiers avec engagement volume annuel",
        "category": "EXTERNAL_DATA_SOURCES",
        "strategy": "BATCH_PROCESSING",
        "expected_savings_EUR": round(ext_saving, 0),
        "effort_days": 20,
        "risk": "LOW",
        "owner_role": "Legal / Procurement",
        "implementation_note": "Cibler -15% via engagement 12 mois + SLA qualité données",
    })

    # --- Strategic: 3-12 months ---
    # 1. Lazy evaluation
    lazy_saving = costs.get("AI_API_CALLS", 0) * OPTIMIZATION_STRATEGIES["LAZY_EVALUATION"]["expected_savings_pct"] / 100
    strategic.append({
        "action": "Architecture lazy evaluation : n'analyser que les entités à delta significatif",
        "category": "AI_API_CALLS",
        "strategy": "LAZY_EVALUATION",
        "expected_savings_EUR": round(lazy_saving, 0),
        "effort_days": 15,
        "risk": "MEDIUM",
        "owner_role": "Architecte / Ingénieur IA",
        "implementation_note": (
            "Comparer hash contextuel avant re-scoring ; ne re-scorer que si delta > seuil"
        ),
    })

    # 2. Multi-cloud / tiered storage
    storage_strategic_saving = costs.get("DATA_STORAGE", 0) * 0.30
    strategic.append({
        "action": "Migration vers stockage hiérarchisé multi-cloud (hot/warm/cold/glacier)",
        "category": "DATA_STORAGE",
        "strategy": "DATA_COMPRESSION",
        "expected_savings_EUR": round(storage_strategic_saving, 0),
        "effort_days": 30,
        "risk": "MEDIUM",
        "owner_role": "Data Engineer / Architecte",
        "implementation_note": "Données >90 jours → Glacier ; query via Athena sans transfert",
    })

    # 3. Human review AI assist
    human_saving = costs.get("HUMAN_REVIEW", 0) * 0.20
    strategic.append({
        "action": "Intégrer assistant IA dans workflow review humaine (pré-remplissage)",
        "category": "HUMAN_REVIEW",
        "strategy": "MODEL_DOWNGRADE_ROUTING",
        "expected_savings_EUR": round(human_saving, 0),
        "effort_days": 25,
        "risk": "LOW",
        "owner_role": "Product / Ingénieur IA",
        "implementation_note": "Réduction temps review estimée à -20% ; qualité maintenue",
    })

    # --- Summary ---
    quick_wins_total = sum(i["expected_savings_EUR"] for i in quick_wins)
    medium_term_total = sum(i["expected_savings_EUR"] for i in medium_term)
    strategic_total = sum(i["expected_savings_EUR"] for i in strategic)
    total_achievable = quick_wins_total + medium_term_total + strategic_total
    achievable_pct = (total_achievable / total_cost) * 100 if total_cost else 0

    summary = {
        "total_monthly_cost_EUR": total_cost,
        "target_reduction_pct": target_reduction_pct,
        "target_savings_EUR": round(target_savings_EUR, 0),
        "quick_wins_savings_EUR": round(quick_wins_total, 0),
        "medium_term_savings_EUR": round(medium_term_total, 0),
        "strategic_savings_EUR": round(strategic_total, 0),
        "total_achievable_savings_EUR": round(total_achievable, 0),
        "achievable_reduction_pct": round(achievable_pct, 1),
        "target_reachable": achievable_pct >= target_reduction_pct,
        "recommended_first_action": quick_wins[0]["action"] if quick_wins else "N/A",
    }

    return {
        "quick_wins": quick_wins,
        "medium_term": medium_term,
        "strategic": strategic,
        "summary": summary,
    }


def simulate_cost_scenarios(
    base_costs: dict[str, float],
    growth_scenarios: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Simulates CaelumSwarm™ cost evolution at different ARR levels.

    Parameters
    ----------
    base_costs : dict mapping cost-category keys to current monthly EUR spend
    growth_scenarios : list of dicts with keys 'name', 'arr_EUR', 'growth_type'
                       (growth_type: 'conservative'|'realistic'|'aggressive')

    Returns
    -------
    dict with projections per scenario, gross_margin_evolution, break_even_analysis
    """
    base_total = sum(base_costs.values())

    # Scaling factors relative to ARR growth
    # Infrastructure and AI costs scale sub-linearly due to economies of scale
    SCALE_FACTORS = {
        "conservative": {
            "infra_elasticity": 0.75,   # costs grow at 75% of revenue growth
            "ai_api_elasticity": 0.60,  # AI benefits most from caching at scale
            "storage_elasticity": 0.80,
            "fixed_growth_rate": 0.05,  # fixed costs grow 5% per doubling
        },
        "realistic": {
            "infra_elasticity": 0.65,
            "ai_api_elasticity": 0.50,
            "storage_elasticity": 0.70,
            "fixed_growth_rate": 0.03,
        },
        "aggressive": {
            "infra_elasticity": 0.55,
            "ai_api_elasticity": 0.40,
            "storage_elasticity": 0.60,
            "fixed_growth_rate": 0.02,
        },
    }

    # Current ARR baseline
    # Assume base monthly revenue such that current stage makes sense
    base_arr = 720_000  # 60K€/month revenue (base assumption for demo)
    base_monthly_revenue = base_arr / 12

    ARR_CHECKPOINTS = [100_000, 500_000, 1_000_000, 5_000_000]

    results: dict[str, Any] = {}

    for scenario in growth_scenarios:
        name = scenario.get("name", "unnamed")
        growth_type = scenario.get("growth_type", "realistic")
        factors = SCALE_FACTORS.get(growth_type, SCALE_FACTORS["realistic"])

        checkpoint_projections = []

        for arr_target in ARR_CHECKPOINTS:
            revenue_ratio = arr_target / base_arr
            monthly_revenue = arr_target / 12

            # Project each cost category
            projected_costs: dict[str, float] = {}
            for key, base_amount in base_costs.items():
                meta = COST_CATEGORIES.get(key, {})
                vf = meta.get("variable_or_fixed", "HYBRID")

                if vf == "VARIABLE":
                    if key == "AI_API_CALLS":
                        elasticity = factors["ai_api_elasticity"]
                    elif key == "BANDWIDTH":
                        elasticity = factors["infra_elasticity"]
                    else:
                        elasticity = 0.70
                    projected = base_amount * (revenue_ratio ** elasticity)

                elif vf == "FIXED":
                    # Fixed costs grow slowly
                    doublings = math.log2(revenue_ratio) if revenue_ratio > 0 else 0
                    growth = (1 + factors["fixed_growth_rate"]) ** doublings
                    projected = base_amount * growth

                else:  # HYBRID
                    if key == "CLOUD_COMPUTE":
                        elasticity = factors["infra_elasticity"]
                    elif key == "DATA_STORAGE":
                        elasticity = factors["storage_elasticity"]
                    else:
                        elasticity = 0.65
                    # 60% variable, 40% fixed behavior
                    var_part = base_amount * 0.60 * (revenue_ratio ** elasticity)
                    doublings = math.log2(revenue_ratio) if revenue_ratio > 0 else 0
                    fix_part = base_amount * 0.40 * (1 + factors["fixed_growth_rate"]) ** doublings
                    projected = var_part + fix_part

                projected_costs[key] = round(projected, 0)

            total_projected = sum(projected_costs.values())
            gross_margin = ((monthly_revenue - total_projected) / monthly_revenue) * 100 if monthly_revenue else 0

            # Detect benchmark stage for this ARR
            if arr_target < 200_000:
                stage = "SEED"
            elif arr_target < 2_000_000:
                stage = "SERIES_A"
            else:
                stage = "GROWTH"
            target_margin = COST_BENCHMARKS[stage]["gross_margin_target_pct"]

            checkpoint_projections.append({
                "arr_EUR": arr_target,
                "monthly_revenue_EUR": round(monthly_revenue, 0),
                "total_monthly_cost_EUR": round(total_projected, 0),
                "gross_margin_pct": round(gross_margin, 1),
                "benchmark_target_margin_pct": target_margin,
                "margin_vs_benchmark_pts": round(gross_margin - target_margin, 1),
                "cost_breakdown": {
                    k: round(v, 0) for k, v in projected_costs.items()
                },
                "infra_as_pct_arr": round(
                    (projected_costs.get("CLOUD_COMPUTE", 0) * 12 / arr_target) * 100, 1
                ),
                "ai_as_pct_revenue": round(
                    (projected_costs.get("AI_API_CALLS", 0) / monthly_revenue) * 100, 1
                    if monthly_revenue else 0
                ),
            })

        results[name] = {
            "growth_type": growth_type,
            "arr_checkpoints_EUR": ARR_CHECKPOINTS,
            "projections": checkpoint_projections,
            "key_insight": _derive_scenario_insight(checkpoint_projections, growth_type),
        }

    # --- Break-even analysis ---
    # Find ARR at which gross margin reaches target for each stage
    break_even = {}
    for stage, bmark in COST_BENCHMARKS.items():
        target = bmark["gross_margin_target_pct"]
        # Use realistic scenario projections
        realistic_key = next(
            (s["name"] for s in growth_scenarios if s.get("growth_type") == "realistic"),
            None,
        )
        if realistic_key and realistic_key in results:
            projections = results[realistic_key]["projections"]
            hit = next(
                (p for p in projections if p["gross_margin_pct"] >= target), None
            )
            break_even[stage] = {
                "target_margin_pct": target,
                "achieved_at_arr_EUR": hit["arr_EUR"] if hit else ">5M",
                "note": f"Marge {target}% atteinte à {hit['arr_EUR']:,}€ ARR" if hit
                        else f"Marge {target}% non atteinte dans les projections",
            }

    return {
        "base_monthly_costs_EUR": base_total,
        "base_arr_assumption_EUR": base_arr,
        "scenarios": results,
        "break_even_analysis": break_even,
        "summary": _summarize_simulations(results),
    }


def _derive_scenario_insight(projections: list[dict], growth_type: str) -> str:
    """Internal helper: derive a qualitative insight from a scenario."""
    if not projections:
        return "Données insuffisantes"
    last = projections[-1]
    first = projections[0]
    margin_gain = last["gross_margin_pct"] - first["gross_margin_pct"]
    if margin_gain > 20:
        return (
            f"Scénario {growth_type} : fort effet d'échelle — marge progresse de "
            f"+{margin_gain:.1f} pts entre {first['arr_EUR']:,}€ et {last['arr_EUR']:,}€ ARR"
        )
    elif margin_gain > 8:
        return (
            f"Scénario {growth_type} : amélioration modérée de la marge (+{margin_gain:.1f} pts) "
            "— optimisations proactives recommandées"
        )
    else:
        return (
            f"Scénario {growth_type} : compression marginale faible (+{margin_gain:.1f} pts) "
            "— investissement FinOps critique pour atteindre les benchmarks"
        )


def _summarize_simulations(results: dict[str, Any]) -> dict[str, Any]:
    """Internal helper: cross-scenario summary."""
    margin_at_1m: dict[str, float] = {}
    for name, scenario in results.items():
        for p in scenario["projections"]:
            if p["arr_EUR"] == 1_000_000:
                margin_at_1m[name] = p["gross_margin_pct"]
    best = max(margin_at_1m, key=lambda k: margin_at_1m[k]) if margin_at_1m else None
    return {
        "gross_margin_at_1M_ARR_by_scenario": margin_at_1m,
        "best_scenario_at_1M_ARR": best,
        "recommendation": (
            f"Le scénario '{best}' offre la meilleure marge brute à 1M€ ARR "
            f"({margin_at_1m.get(best, 0):.1f}%) — "
            "prioriser les optimisations IA et compute dès maintenant pour y parvenir."
        )
        if best else "Insuffisamment de données pour recommander un scénario",
    }


def auto_recommend_resource_scaling(
    current_load: dict[str, Any],
    forecast_load: dict[str, Any],
) -> dict[str, Any]:
    """
    Recommends scaling decisions for each resource type.

    Parameters
    ----------
    current_load : dict of resource_name -> current_value metrics
    forecast_load : dict of resource_name -> forecast_value (next 30 days)

    Returns
    -------
    dict with recommendations per resource, cost_delta_EUR, automation_possible
    """
    recommendations: dict[str, dict[str, Any]] = {}

    for resource, current_val in current_load.items():
        meta = RESOURCE_METRICS.get(resource, {})
        optimal = meta.get("optimal", 70.0)
        forecast_val = forecast_load.get(resource, current_val)
        unit = meta.get("measurement_unit", "%")

        # Determine scaling direction
        if resource == "compute_waste_pct":
            # High waste = over-provisioned = scale DOWN
            if current_val > optimal * 1.5:
                direction = "SCALE_DOWN"
                urgency = "HIGH"
                cost_impact = "SAVING"
                cost_delta_pct = -((current_val - optimal) / 100) * 0.4
            elif current_val > optimal * 1.1:
                direction = "SCALE_IN"
                urgency = "MEDIUM"
                cost_impact = "SAVING"
                cost_delta_pct = -((current_val - optimal) / 100) * 0.2
            else:
                direction = "MAINTAIN"
                urgency = "LOW"
                cost_impact = "NEUTRAL"
                cost_delta_pct = 0.0

        elif resource == "api_cache_hit_rate":
            # Low cache = overpaying API — invest to increase cache
            if current_val < optimal * 0.4:
                direction = "SCALE_UP"
                urgency = "HIGH"
                cost_impact = "INVESTMENT_FOR_SAVING"
                cost_delta_pct = 0.03  # small upfront cost, then big savings
            elif current_val < optimal * 0.7:
                direction = "SCALE_OUT"
                urgency = "MEDIUM"
                cost_impact = "INVESTMENT_FOR_SAVING"
                cost_delta_pct = 0.01
            else:
                direction = "MAINTAIN"
                urgency = "LOW"
                cost_impact = "NEUTRAL"
                cost_delta_pct = 0.0

        elif resource in ("cpu_utilization_pct", "memory_utilization_pct"):
            # Under-utilized = wasteful; over-utilized = risky
            if current_val < optimal * 0.5:
                direction = "SCALE_DOWN"
                urgency = "MEDIUM"
                cost_impact = "SAVING"
                cost_delta_pct = -(optimal - current_val) / optimal * 0.30
            elif current_val < optimal * 0.85:
                direction = "MAINTAIN"
                urgency = "LOW"
                cost_impact = "NEUTRAL"
                cost_delta_pct = 0.0
            elif current_val < optimal * 1.15:
                direction = "SCALE_UP"
                urgency = "MEDIUM"
                cost_impact = "COST_INCREASE"
                cost_delta_pct = 0.15
            else:
                direction = "SCALE_OUT"
                urgency = "HIGH"
                cost_impact = "COST_INCREASE"
                cost_delta_pct = 0.30

        elif resource == "storage_efficiency_pct":
            # Low efficiency = compressed storage opportunity
            if current_val < optimal * 0.7:
                direction = "SCALE_IN"  # consolidate / compress
                urgency = "MEDIUM"
                cost_impact = "SAVING"
                cost_delta_pct = -(optimal - current_val) / 100 * 0.35
            else:
                direction = "MAINTAIN"
                urgency = "LOW"
                cost_impact = "NEUTRAL"
                cost_delta_pct = 0.0

        else:
            direction = "MAINTAIN"
            urgency = "LOW"
            cost_impact = "NEUTRAL"
            cost_delta_pct = 0.0

        # Forecast adjustment
        forecast_delta = forecast_val - current_val
        if abs(forecast_delta) > 15 and direction == "MAINTAIN":
            direction = "SCALE_UP" if forecast_delta > 0 else "SCALE_DOWN"
            urgency = "MEDIUM"
            cost_impact = "PROACTIVE"

        # Automation possibility
        automation_possible = direction in ("SCALE_DOWN", "SCALE_IN", "MAINTAIN") or (
            resource == "api_cache_hit_rate" and direction in ("SCALE_UP", "SCALE_OUT")
        )

        # Monthly cost delta estimate (based on rough infra fraction)
        base_infra_monthly = 14_200  # CLOUD_COMPUTE baseline
        cost_delta_EUR = round(base_infra_monthly * cost_delta_pct, 0)

        # Risk assessment
        if urgency == "HIGH" and direction in ("SCALE_DOWN", "SCALE_IN"):
            risk = "LOW"  # saving money aggressively is low risk operationally
        elif direction in ("SCALE_UP", "SCALE_OUT") and urgency == "HIGH":
            risk = "MEDIUM"
        elif direction == "MAINTAIN":
            risk = "NONE"
        else:
            risk = "LOW"

        recommendations[resource] = {
            "label": meta.get("label", resource) if "label" in meta else resource.replace("_", " ").title(),
            "current_value": current_val,
            "forecast_value_30d": forecast_val,
            "optimal_value": optimal,
            "measurement_unit": unit,
            "scaling_direction": direction,
            "urgency": urgency,
            "cost_impact_type": cost_impact,
            "cost_delta_monthly_EUR": cost_delta_EUR,
            "risk": risk,
            "automation_possible": automation_possible,
            "recommended_action": _scaling_action_text(resource, direction, current_val, optimal, unit),
            "timing": "Immédiat (< 48h)" if urgency == "HIGH" else
                      "Court terme (< 2 semaines)" if urgency == "MEDIUM" else
                      "Planifié (< 3 mois)",
        }

    total_cost_delta = sum(
        r["cost_delta_monthly_EUR"] for r in recommendations.values()
    )
    automatable_count = sum(
        1 for r in recommendations.values() if r["automation_possible"]
    )

    return {
        "recommendations": recommendations,
        "total_cost_delta_monthly_EUR": round(total_cost_delta, 0),
        "automatable_recommendations": automatable_count,
        "total_recommendations": len(recommendations),
        "automation_coverage_pct": round(automatable_count / len(recommendations) * 100, 1)
        if recommendations else 0,
        "executive_summary": (
            f"{automatable_count}/{len(recommendations)} recommandations automatisables. "
            f"Delta coût mensuel estimé : {total_cost_delta:+,.0f}€. "
            "Prioriser : compute waste reduction + cache API."
        ),
    }


def _scaling_action_text(resource: str, direction: str, current: float, optimal: float, unit: str) -> str:
    """Internal helper: human-readable action text."""
    actions = {
        "SCALE_UP": f"Augmenter la capacité — {resource} à {current}{unit}, cible {optimal}{unit}",
        "SCALE_DOWN": f"Réduire la capacité — {resource} à {current}{unit}, surévalué vs cible {optimal}{unit}",
        "SCALE_OUT": f"Distribuer horizontalement — charge {current}{unit} approche seuil {optimal}{unit}",
        "SCALE_IN": f"Consolider les ressources — {resource} à {current}{unit} peut être optimisé",
        "MAINTAIN": f"Maintenir — {resource} à {current}{unit} dans la plage acceptable",
    }
    return actions.get(direction, "Évaluer manuellement")


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Demonstration of the CaelumSwarm™ Resource & Cost Auto-Optimizer Agent.

    Covers:
    1. Cost structure analysis — 50K€/month operational costs
    2. Optimization plan targeting 25% reduction
    3. Three-scenario simulation (conservative / realistic / aggressive)
    4. Scaling recommendations
    """
    SEP = "=" * 72
    sep = "-" * 72

    print(SEP)
    print("  CaelumSwarm™ — Agent Auto-Optimiseur de Ressources & Coûts")
    print(f"  Date d'analyse : {date.today()}")
    print(SEP)

    # -----------------------------------------------------------------------
    # 1. COST STRUCTURE ANALYSIS
    # -----------------------------------------------------------------------
    print("\n[1/4] ANALYSE DE LA STRUCTURE DE COÛTS")
    print(sep)

    mock_costs = {
        "CLOUD_COMPUTE": 14_200,
        "AI_API_CALLS": 11_800,
        "DATA_STORAGE": 5_400,
        "BANDWIDTH": 3_100,
        "MONITORING_TOOLS": 2_800,
        "EXTERNAL_DATA_SOURCES": 6_900,
        "HUMAN_REVIEW": 4_200,
        "COMPLIANCE_TOOLS": 1_600,
    }
    monthly_revenue = 60_000  # 720K€ ARR

    analysis = analyze_cost_structure(mock_costs, monthly_revenue)

    print(f"  Chiffre d'affaires mensuel   : {analysis['monthly_revenue_EUR']:>10,.0f} €")
    print(f"  ARR                          : {analysis['arr_EUR']:>10,.0f} €")
    print(f"  Coûts opérationnels totaux   : {analysis['total_monthly_cost_EUR']:>10,.0f} €")
    print(f"  Bénéfice brut mensuel        : {analysis['gross_profit_monthly_EUR']:>10,.0f} €")
    print(f"  Marge brute                  : {analysis['gross_margin_pct']:>10.1f} %")
    print(f"  Stade benchmark détecté      : {analysis['vs_benchmark']['detected_stage']}")
    print(f"  Marge cible benchmark        : {analysis['vs_benchmark']['gross_margin']['target_pct']:>10.0f} %")
    print(f"  Écart vs benchmark           : {analysis['vs_benchmark']['gross_margin']['delta_pts']:>+10.1f} pts")

    print(f"\n  Répartition des coûts :")
    for key, data in analysis["cogs_breakdown"].items():
        bar = "█" * int(data["share_of_total_costs_pct"] / 3)
        print(
            f"    {data['label'][:42]:<42} {data['monthly_EUR']:>7,.0f}€"
            f"  ({data['share_of_total_costs_pct']:>5.1f}%)  {bar}"
        )

    print(f"\n  Économies potentielles totales : {analysis['total_optimization_potential_EUR']:,.0f}€/mois")

    print(f"\n  Économie unitaire :")
    ue = analysis["unit_economics"]
    print(f"    Coût par wave analysée       : {ue['cost_per_wave_EUR']:,.2f}€")
    print(f"    Coût par entité analysée     : {ue['cost_per_entity_analyzed_EUR']:,.2f}€")
    print(f"    Coût par rapport produit     : {ue['cost_per_report_EUR']:,.2f}€")
    print(f"    Marge de contribution/wave   : {ue['contribution_margin_per_wave_EUR']:,.2f}€")

    if analysis["red_flags"]:
        print(f"\n  Alertes détectées ({len(analysis['red_flags'])}) :")
        for flag in analysis["red_flags"]:
            print(f"    ⚠  {flag}")
    else:
        print("\n  Aucune alerte critique détectée.")

    # -----------------------------------------------------------------------
    # 2. OPTIMIZATION PLAN — TARGET -25%
    # -----------------------------------------------------------------------
    print(f"\n\n[2/4] PLAN D'OPTIMISATION — CIBLE -25%")
    print(sep)

    plan = generate_optimization_plan(mock_costs, target_reduction_pct=25.0)
    summary = plan["summary"]

    print(f"  Coûts actuels                : {summary['total_monthly_cost_EUR']:>10,.0f}€/mois")
    print(f"  Économies cibles (-25%)      : {summary['target_savings_EUR']:>10,.0f}€/mois")
    print(f"  Économies réalisables        : {summary['total_achievable_savings_EUR']:>10,.0f}€/mois")
    print(f"  Réduction réalisable         : {summary['achievable_reduction_pct']:>10.1f}%")
    print(f"  Objectif atteignable         : {'OUI ✓' if summary['target_reachable'] else 'NON — renforcer les actions'}")

    print(f"\n  --- Gains rapides (< 1 semaine) : {summary['quick_wins_savings_EUR']:,.0f}€/mois ---")
    for i, item in enumerate(plan["quick_wins"], 1):
        print(f"    {i}. {item['action']}")
        print(f"       Économie : {item['expected_savings_EUR']:,.0f}€/mois | Effort : {item['effort_days']}j | Risque : {item['risk']} | Responsable : {item['owner_role']}")

    print(f"\n  --- Moyen terme (1-3 mois) : {summary['medium_term_savings_EUR']:,.0f}€/mois ---")
    for i, item in enumerate(plan["medium_term"], 1):
        print(f"    {i}. {item['action']}")
        print(f"       Économie : {item['expected_savings_EUR']:,.0f}€/mois | Effort : {item['effort_days']}j | Risque : {item['risk']} | Responsable : {item['owner_role']}")

    print(f"\n  --- Stratégique (3-12 mois) : {summary['strategic_savings_EUR']:,.0f}€/mois ---")
    for i, item in enumerate(plan["strategic"], 1):
        print(f"    {i}. {item['action']}")
        print(f"       Économie : {item['expected_savings_EUR']:,.0f}€/mois | Effort : {item['effort_days']}j | Risque : {item['risk']} | Responsable : {item['owner_role']}")

    # -----------------------------------------------------------------------
    # 3. COST SIMULATION — 3 SCENARIOS
    # -----------------------------------------------------------------------
    print(f"\n\n[3/4] SIMULATION DE COÛTS — 3 SCÉNARIOS DE CROISSANCE")
    print(sep)

    scenarios = [
        {"name": "Conservateur", "arr_EUR": 720_000, "growth_type": "conservative"},
        {"name": "Réaliste", "arr_EUR": 720_000, "growth_type": "realistic"},
        {"name": "Agressif", "arr_EUR": 720_000, "growth_type": "aggressive"},
    ]

    simulation = simulate_cost_scenarios(mock_costs, scenarios)

    arr_labels = ["100K€", "500K€", "1M€", "5M€"]
    print(f"\n  {'ARR':<10} {'Scénario':<16} {'Coûts/mois':<15} {'Marge brute':<14} {'vs Benchmark'}")
    print(f"  {'-'*9} {'-'*15} {'-'*14} {'-'*13} {'-'*15}")

    for s_name, s_data in simulation["scenarios"].items():
        for arr_label, proj in zip(arr_labels, s_data["projections"]):
            delta = proj["margin_vs_benchmark_pts"]
            status = "✓" if delta >= 0 else "✗"
            print(
                f"  {arr_label:<10} {s_name:<16} {proj['total_monthly_cost_EUR']:>10,.0f}€  "
                f"{proj['gross_margin_pct']:>8.1f}%   {status} {delta:>+.1f} pts"
            )
        print()

    print(f"  Insights par scénario :")
    for s_name, s_data in simulation["scenarios"].items():
        print(f"    • {s_name} : {s_data['key_insight']}")

    print(f"\n  Point mort marge benchmark :")
    for stage, be in simulation["break_even_analysis"].items():
        print(f"    • {stage:10} ({be['target_margin_pct']}% cible) : {be['note']}")

    print(f"\n  Recommandation simulation :")
    print(f"    {simulation['summary']['recommendation']}")

    # -----------------------------------------------------------------------
    # 4. RESOURCE SCALING RECOMMENDATIONS
    # -----------------------------------------------------------------------
    print(f"\n\n[4/4] RECOMMANDATIONS DE SCALING DES RESSOURCES")
    print(sep)

    current_load = {
        "cpu_utilization_pct": 34.2,
        "memory_utilization_pct": 51.8,
        "api_cache_hit_rate": 12.5,
        "storage_efficiency_pct": 58.0,
        "compute_waste_pct": 41.3,
    }

    forecast_load = {
        "cpu_utilization_pct": 42.0,
        "memory_utilization_pct": 58.5,
        "api_cache_hit_rate": 18.0,
        "storage_efficiency_pct": 60.0,
        "compute_waste_pct": 38.0,
    }

    scaling = auto_recommend_resource_scaling(current_load, forecast_load)

    print(f"\n  {'Ressource':<32} {'Actuel':>8} {'Optimal':>8} {'Action':>12} {'Urgence':>8} {'Delta €/mois':>13} {'Auto?':>6}")
    print(f"  {'-'*31} {'-'*7} {'-'*7} {'-'*11} {'-'*7} {'-'*12} {'-'*5}")

    for res_key, rec in scaling["recommendations"].items():
        auto_str = "Oui" if rec["automation_possible"] else "Non"
        delta = rec["cost_delta_monthly_EUR"]
        delta_str = f"{delta:>+,.0f}€" if delta != 0 else "  —"
        print(
            f"  {res_key:<32} {rec['current_value']:>7.1f}{rec['measurement_unit']}"
            f" {rec['optimal_value']:>7.1f}{rec['measurement_unit']}"
            f" {rec['scaling_direction']:>12} {rec['urgency']:>8} {delta_str:>13} {auto_str:>6}"
        )

    print(f"\n  Résumé :")
    print(f"    {scaling['executive_summary']}")
    print(f"    Delta coût mensuel total : {scaling['total_cost_delta_monthly_EUR']:+,.0f}€")
    print(f"    Couverture automation    : {scaling['automation_coverage_pct']:.1f}%")

    for res_key, rec in scaling["recommendations"].items():
        if rec["urgency"] == "HIGH":
            print(f"\n    [PRIORITÉ HAUTE] {rec['recommended_action']}")
            print(f"    Timing : {rec['timing']} | Risque : {rec['risk']}")

    print(f"\n{SEP}")
    print("  Analyse terminée — CaelumSwarm™ FinOps Intelligence Layer")
    print(SEP)

    return True


# ---------------------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_demo()
