"""
FinOps Cloud Optimizer Agent — CaelumSwarm™
Framework: FinOps Foundation (FOCUS 1.0)
Role: Optimisation coûts AWS, rightsizing, reserved capacity, spot instances
Target: Réduire 30%+ les coûts tout en maintenant SLO Elite
"""

import json
from datetime import datetime, date

FINOPS_VERSION = "FOCUS 1.0"

CURRENT_CLOUD_COSTS = {
    "monthly_total_eur": 4200,
    "breakdown": {
        "eks_nodes": {"cost": 1800, "pct": 42.9, "instances": "12x m6i.xlarge On-Demand"},
        "rds_aurora": {"cost": 680, "pct": 16.2, "type": "r6g.xlarge Multi-AZ On-Demand"},
        "elasticache_redis": {"cost": 420, "pct": 10.0, "type": "6x cache.r6g.large On-Demand"},
        "data_transfer": {"cost": 380, "pct": 9.0, "gb_month": 5000},
        "s3_storage": {"cost": 220, "pct": 5.2, "tb": 44},
        "nat_gateway": {"cost": 180, "pct": 4.3, "gb_processed": 3000},
        "secrets_manager": {"cost": 120, "pct": 2.9},
        "cloudwatch_logs": {"cost": 150, "pct": 3.6, "gb_ingested": 500},
        "other": {"cost": 250, "pct": 5.9},
    },
    "largest_opportunities": ["eks_nodes", "rds_aurora", "elasticache_redis"],
}

OPTIMIZATION_STRATEGIES = {
    "reserved_instances": {
        "description": "Compute Savings Plans 3 ans, paiement partiel anticipé",
        "applies_to": ["eks_nodes", "rds_aurora"],
        "discount_percent": 42,
        "commitment_years": 3,
        "estimated_savings_eur_month": 1050,
        "break_even_months": 8,
    },
    "spot_instances": {
        "description": "Spot Instances pour workloads non-critiques (batch, tests)",
        "applies_to": ["eks_batch_nodes", "nightly_jobs"],
        "discount_percent": 75,
        "interruption_rate": 0.05,
        "estimated_savings_eur_month": 320,
        "mitigation": "Karpenter + Spot interruption handlers",
    },
    "rightsizing": {
        "description": "Réduire instances surdimensionnées après analyse CPU/RAM P95",
        "findings": [
            {
                "resource": "rds_aurora",
                "current": "r6g.xlarge",
                "recommended": "r6g.large",
                "reason": "CPU P95 = 28%, RAM P95 = 45%",
                "savings_eur_month": 180,
            },
            {
                "resource": "elasticache_redis",
                "current": "cache.r6g.large×6",
                "recommended": "cache.r6g.medium×6",
                "reason": "Memory used P95 = 52%",
                "savings_eur_month": 140,
            },
        ],
        "total_savings_eur_month": 320,
    },
    "intelligent_tiering_s3": {
        "description": "S3 Intelligent-Tiering pour données >30j non-accédées",
        "estimated_savings_eur_month": 66,
        "implementation": "S3 lifecycle policy → Intelligent-Tiering",
    },
    "nat_gateway_optimization": {
        "description": "VPC Endpoints pour S3/ECR/SecretsManager → éliminer trafic NAT",
        "current_cost": 180,
        "vpc_endpoints_cost": 45,
        "estimated_savings_eur_month": 135,
    },
    "cloudwatch_log_retention": {
        "description": "Réduire rétention CloudWatch → Loki (S3 long-term)",
        "current_retention_days": 90,
        "recommended_cloudwatch": 7,
        "export_to": "S3 → Glacier",
        "estimated_savings_eur_month": 105,
    },
    "karpenter_autoscaling": {
        "description": "Karpenter au lieu de Cluster Autoscaler — bin-packing optimal",
        "estimated_savings_eur_month": 180,
        "features": ["bin-packing", "mixed instance families", "spot+on-demand mix"],
    },
    "graviton_migration": {
        "description": "Migrer vers instances ARM Graviton3 (jusqu'à 40% moins cher)",
        "instances_to_migrate": ["m6i.xlarge → m7g.xlarge", "r6i.large → r7g.large"],
        "discount_percent": 38,
        "estimated_savings_eur_month": 290,
    },
}

FINOPS_GOVERNANCE = {
    "tagging_policy": {
        "required_tags": ["Project", "Environment", "Owner", "CostCenter", "Wave", "Domain"],
        "enforcement": "AWS Config Rule + OPA Gatekeeper",
        "untagged_resource_action": "Alert + auto-tag with 'unknown'",
    },
    "budget_alerts": [
        {"name": "Monthly 80% threshold", "amount_eur": 3360, "action": "Email + Slack alert"},
        {"name": "Monthly 100% threshold", "amount_eur": 4200, "action": "Email + PagerDuty"},
        {"name": "Spike detection +20%", "type": "anomaly", "action": "Immediate alert"},
    ],
    "cost_allocation": {
        "by_wave": True,
        "by_domain": True,
        "by_environment": True,
        "showback_reports": "Monthly pour chaque Wave engine",
    },
    "waste_detection": {
        "idle_instances": "CPU < 5% pendant 7 jours → rightsizing alert",
        "unused_volumes": "EBS non-attachés → delete après 30j",
        "orphaned_snapshots": "Snapshots >90j → review + delete",
        "unused_elastic_ips": "EIP non-attachées → release",
    },
}

COST_FORECAST = {
    "current_monthly": 4200,
    "after_reserved_instances": 3150,
    "after_spot_migration": 2830,
    "after_rightsizing": 2510,
    "after_nat_optimization": 2375,
    "after_graviton": 2085,
    "after_all_optimizations": 1996,
    "total_savings_pct": 52.5,
    "payback_months": 8,
    "annual_savings_eur": 26448,
}


# ---------------------------------------------------------------------------
# FONCTIONS
# ---------------------------------------------------------------------------

def analyze_cost_breakdown(environment: str) -> dict:
    """Analyse la répartition des coûts et identifie les top opportunités."""
    total = CURRENT_CLOUD_COSTS["monthly_total_eur"]
    breakdown = CURRENT_CLOUD_COSTS["breakdown"]

    sorted_items = sorted(
        [(k, v) for k, v in breakdown.items()],
        key=lambda x: x[1]["cost"],
        reverse=True,
    )

    top3 = [{"resource": k, "cost_eur": v["cost"], "pct": v["pct"]} for k, v in sorted_items[:3]]
    top3_cost = sum(item["cost_eur"] for item in top3)

    total_optimizable = sum(
        s.get("estimated_savings_eur_month", s.get("total_savings_eur_month", 0))
        for s in OPTIMIZATION_STRATEGIES.values()
    )

    return {
        "environment": environment,
        "analysis_date": date.today().isoformat(),
        "total_monthly_eur": total,
        "top_opportunities": top3,
        "top3_concentration_pct": round(top3_cost / total * 100, 1),
        "total_optimizable_eur_month": total_optimizable,
        "potential_savings_pct": round(total_optimizable / total * 100, 1),
        "largest_single_opportunity": {
            "name": "reserved_instances",
            "savings_eur_month": OPTIMIZATION_STRATEGIES["reserved_instances"]["estimated_savings_eur_month"],
        },
        "recommendation": (
            "Prioriser Reserved Instances (Savings Plans 3 ans) — ROI le plus rapide. "
            "Compléter avec Graviton3 migration et rightsizing RDS/ElastiCache."
        ),
    }


def calculate_savings_plan_roi(commitment_years: int, upfront_payment: str) -> dict:
    """Calcule le ROI des Savings Plans AWS selon le niveau d'engagement."""
    discount_map = {
        (1, "none"):    0.27,
        (1, "partial"): 0.31,
        (1, "full"):    0.34,
        (3, "none"):    0.35,
        (3, "partial"): 0.42,
        (3, "full"):    0.46,
    }

    upfront_cost_map = {
        "none":    0.00,
        "partial": 0.45,
        "full":    1.00,
    }

    key = (commitment_years, upfront_payment.lower())
    discount = discount_map.get(key, 0.35)

    eks_cost = CURRENT_CLOUD_COSTS["breakdown"]["eks_nodes"]["cost"]
    rds_cost = CURRENT_CLOUD_COSTS["breakdown"]["rds_aurora"]["cost"]
    eligible_monthly = eks_cost + rds_cost

    monthly_savings = round(eligible_monthly * discount, 2)
    annual_savings = round(monthly_savings * 12, 2)
    total_savings_period = round(monthly_savings * 12 * commitment_years, 2)

    upfront_fraction = upfront_cost_map.get(upfront_payment.lower(), 0.45)
    upfront_cost = round(eligible_monthly * (1 - discount) * 12 * upfront_fraction, 2)
    break_even_months = round(upfront_cost / monthly_savings, 1) if monthly_savings > 0 else 0

    return {
        "commitment_years": commitment_years,
        "upfront_payment": upfront_payment,
        "discount_percent": round(discount * 100, 1),
        "eligible_monthly_cost_eur": eligible_monthly,
        "monthly_savings_eur": monthly_savings,
        "annual_savings_eur": annual_savings,
        "total_savings_over_period_eur": total_savings_period,
        "estimated_upfront_cost_eur": upfront_cost,
        "break_even_months": break_even_months,
        "recommendation": (
            f"Savings Plan {commitment_years}an(s) paiement {upfront_payment} → "
            f"{round(discount * 100, 1)}% de réduction. "
            f"ROI atteint en {break_even_months} mois."
        ),
    }


def simulate_karpenter_optimization(current_nodes: int, workload_profile: str) -> dict:
    """Simule l'optimisation Karpenter (bin-packing + spot)."""
    profiles = {
        "mixed":      {"bin_packing_gain": 0.25, "spot_ratio": 0.40, "spot_discount": 0.75},
        "batch":      {"bin_packing_gain": 0.20, "spot_ratio": 0.70, "spot_discount": 0.75},
        "web":        {"bin_packing_gain": 0.30, "spot_ratio": 0.25, "spot_discount": 0.72},
        "stateful":   {"bin_packing_gain": 0.15, "spot_ratio": 0.10, "spot_discount": 0.70},
    }

    profile = profiles.get(workload_profile.lower(), profiles["mixed"])
    cost_per_node_month = CURRENT_CLOUD_COSTS["breakdown"]["eks_nodes"]["cost"] / current_nodes

    # Bin-packing: réduction du nombre de nœuds
    nodes_after_binpacking = round(current_nodes * (1 - profile["bin_packing_gain"]))
    cost_after_binpacking = nodes_after_binpacking * cost_per_node_month

    # Mix spot/on-demand
    spot_nodes = round(nodes_after_binpacking * profile["spot_ratio"])
    od_nodes = nodes_after_binpacking - spot_nodes
    spot_node_cost = cost_per_node_month * (1 - profile["spot_discount"])
    final_cost = round(od_nodes * cost_per_node_month + spot_nodes * spot_node_cost, 2)

    initial_cost = CURRENT_CLOUD_COSTS["breakdown"]["eks_nodes"]["cost"]
    savings = round(initial_cost - final_cost, 2)
    savings_pct = round(savings / initial_cost * 100, 1)

    return {
        "workload_profile": workload_profile,
        "initial_nodes": current_nodes,
        "initial_monthly_cost_eur": initial_cost,
        "after_bin_packing": {
            "nodes": nodes_after_binpacking,
            "cost_eur": round(cost_after_binpacking, 2),
        },
        "after_spot_mix": {
            "on_demand_nodes": od_nodes,
            "spot_nodes": spot_nodes,
            "spot_ratio_pct": round(profile["spot_ratio"] * 100, 1),
            "final_monthly_cost_eur": final_cost,
        },
        "monthly_savings_eur": savings,
        "savings_pct": savings_pct,
        "interruption_risk": "Faible — Karpenter gère la réallocation automatique",
        "recommendation": (
            f"Karpenter sur profil '{workload_profile}' → {nodes_after_binpacking} nœuds "
            f"({spot_nodes} Spot + {od_nodes} On-Demand). "
            f"Économie : {savings}€/mois ({savings_pct}%)."
        ),
    }


def generate_cost_report(period: str) -> dict:
    """Génère un rapport FinOps mensuel pour CaelumSwarm™."""
    total = CURRENT_CLOUD_COSTS["monthly_total_eur"]
    breakdown = CURRENT_CLOUD_COSTS["breakdown"]

    total_strategy_savings = sum(
        s.get("estimated_savings_eur_month", s.get("total_savings_eur_month", 0))
        for s in OPTIMIZATION_STRATEGIES.values()
    )

    top_waste = []
    for rule_name, rule_desc in FINOPS_GOVERNANCE["waste_detection"].items():
        top_waste.append({"rule": rule_name, "action": rule_desc})

    return {
        "report_title": f"FinOps Report CaelumSwarm™ — {period}",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "framework": FINOPS_VERSION,
        "period": period,
        "summary": {
            "total_cost_eur": total,
            "budget_utilization_pct": round(total / 4200 * 100, 1),
            "cost_vs_prev_month_pct": 0.0,
            "projected_annual_eur": total * 12,
        },
        "cost_by_service": {
            svc: {"cost_eur": data["cost"], "pct": data["pct"]}
            for svc, data in breakdown.items()
        },
        "optimization_pipeline": {
            "strategies_identified": len(OPTIMIZATION_STRATEGIES),
            "total_potential_savings_eur_month": total_strategy_savings,
            "savings_pct_potential": round(total_strategy_savings / total * 100, 1),
        },
        "governance_status": {
            "tagging_compliance": "En cours — AWS Config Rule actif",
            "budget_alerts_configured": len(FINOPS_GOVERNANCE["budget_alerts"]),
            "waste_rules_active": len(FINOPS_GOVERNANCE["waste_detection"]),
        },
        "top_waste_rules": top_waste,
        "next_actions": [
            "Activer Compute Savings Plans 3 ans (économie immédiate 1 050€/mois)",
            "Déployer Karpenter + Spot NodePool pour workloads batch",
            "Rightsizing RDS Aurora r6g.xlarge → r6g.large",
            "Configurer VPC Endpoints S3/ECR/SecretsManager",
            "Migrer vers Graviton3 (m7g, r7g)",
        ],
    }


def prioritize_optimizations() -> list:
    """Priorise les optimisations par ROI décroissant."""
    items = []

    for name, strategy in OPTIMIZATION_STRATEGIES.items():
        savings = strategy.get(
            "estimated_savings_eur_month",
            strategy.get("total_savings_eur_month", 0),
        )
        effort_map = {
            "reserved_instances":       ("Faible", 1),
            "spot_instances":           ("Moyen",  2),
            "rightsizing":              ("Moyen",  3),
            "graviton_migration":       ("Élevé",  4),
            "karpenter_autoscaling":    ("Élevé",  5),
            "nat_gateway_optimization": ("Faible", 6),
            "cloudwatch_log_retention": ("Faible", 7),
            "intelligent_tiering_s3":   ("Faible", 8),
        }
        effort_label, order = effort_map.get(name, ("Moyen", 99))

        roi_score = savings / max(order, 1) * 10

        items.append({
            "rank": 0,
            "name": name,
            "description": strategy["description"],
            "savings_eur_month": savings,
            "savings_eur_year": savings * 12,
            "effort": effort_label,
            "roi_score": round(roi_score, 1),
            "_sort_key": -savings,
        })

    items.sort(key=lambda x: x["_sort_key"])
    for i, item in enumerate(items, start=1):
        item["rank"] = i
        del item["_sort_key"]

    return items


# ---------------------------------------------------------------------------
# BLOC PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    sep = "=" * 70

    # 1. En-tête
    print(sep)
    print("  FINOPS CLOUD OPTIMIZER — CaelumSwarm™")
    print(f"  Framework : {FINOPS_VERSION}  |  Date : {date.today().isoformat()}")
    print(sep)

    # 2. Coûts actuels (4 200 €/mois breakdown)
    print("\n[1] COÛTS ACTUELS — 4 200 €/MOIS\n")
    total = CURRENT_CLOUD_COSTS["monthly_total_eur"]
    print(f"  {'Service':<30} {'Coût (€)':>10}  {'%':>6}")
    print(f"  {'-'*30}  {'-'*10}  {'-'*6}")
    for svc, data in CURRENT_CLOUD_COSTS["breakdown"].items():
        bar = "#" * int(data["pct"] / 2.5)
        print(f"  {svc:<30} {data['cost']:>10}€  {data['pct']:>5.1f}%  {bar}")
    print(f"\n  {'TOTAL':<30} {total:>10}€  100.0%")

    # 3. 8 stratégies d'optimisation
    print("\n" + sep)
    print("[2] STRATÉGIES D'OPTIMISATION (8 leviers)\n")
    for name, strategy in OPTIMIZATION_STRATEGIES.items():
        savings = strategy.get(
            "estimated_savings_eur_month",
            strategy.get("total_savings_eur_month", 0),
        )
        print(f"  • {name}")
        print(f"    {strategy['description']}")
        print(f"    Économie estimée : {savings}€/mois ({savings * 12}€/an)")
        if "discount_percent" in strategy:
            print(f"    Réduction : {strategy['discount_percent']}%")
        print()

    # 4. Roadmap priorisée par ROI décroissant
    print(sep)
    print("[3] ROADMAP PRIORISÉE — ROI DÉCROISSANT\n")
    priorities = prioritize_optimizations()
    print(f"  {'#':<3}  {'Stratégie':<30}  {'€/mois':>8}  {'€/an':>9}  {'Effort':<8}  {'Score ROI':>9}")
    print(f"  {'-'*3}  {'-'*30}  {'-'*8}  {'-'*9}  {'-'*8}  {'-'*9}")
    for item in priorities:
        print(
            f"  {item['rank']:<3}  {item['name']:<30}  {item['savings_eur_month']:>7}€"
            f"  {item['savings_eur_year']:>8}€  {item['effort']:<8}  {item['roi_score']:>9}"
        )

    # 5. Reserved Instances ROI (3 ans)
    print("\n" + sep)
    print("[4] RESERVED INSTANCES — ROI CALCULATION (3 ANS)\n")
    for upfront in ("none", "partial", "full"):
        roi = calculate_savings_plan_roi(3, upfront)
        print(f"  Paiement anticipé : {upfront.upper():<8}  "
              f"Réduction : {roi['discount_percent']}%  "
              f"Économie mensuelle : {roi['monthly_savings_eur']}€  "
              f"Break-even : {roi['break_even_months']} mois")
    best_roi = calculate_savings_plan_roi(3, "partial")
    print(f"\n  => Recommandation : 3 ans / Partial — {best_roi['monthly_savings_eur']}€/mois économisés")
    print(f"     Économie sur 3 ans : {best_roi['total_savings_over_period_eur']}€")

    # 6. Karpenter simulation
    print("\n" + sep)
    print("[5] KARPENTER SIMULATION\n")
    for profile in ("mixed", "batch", "web"):
        sim = simulate_karpenter_optimization(12, profile)
        print(f"  Profil '{profile}':")
        print(f"    Nœuds : {sim['initial_nodes']} → {sim['after_spot_mix']['on_demand_nodes']} OD "
              f"+ {sim['after_spot_mix']['spot_nodes']} Spot")
        print(f"    Coût  : {sim['initial_monthly_cost_eur']}€ → {sim['after_spot_mix']['final_monthly_cost_eur']}€  "
              f"(-{sim['savings_pct']}%, -{sim['monthly_savings_eur']}€/mois)")
        print()

    # 7. Forecast : 4 200 € → 1 996 € (-52.5%)
    print(sep)
    print("[6] FORECAST D'OPTIMISATION\n")
    steps = [
        ("Coût actuel (baseline)",       COST_FORECAST["current_monthly"],           0),
        ("Après Reserved Instances",     COST_FORECAST["after_reserved_instances"],  None),
        ("Après Spot Instances",         COST_FORECAST["after_spot_migration"],       None),
        ("Après Rightsizing",            COST_FORECAST["after_rightsizing"],          None),
        ("Après NAT optimization",       COST_FORECAST["after_nat_optimization"],     None),
        ("Après Graviton migration",     COST_FORECAST["after_graviton"],             None),
        ("Après TOUTES optimisations",   COST_FORECAST["after_all_optimizations"],    None),
    ]
    baseline = steps[0][1]
    for label, cost, _ in steps:
        delta = cost - baseline
        bar_len = int(cost / baseline * 40)
        bar = "#" * bar_len
        sign = f"  ({delta:+.0f}€)" if delta != 0 else ""
        print(f"  {label:<35} {cost:>5}€/mois  [{bar:<40}]{sign}")

    savings_total = baseline - COST_FORECAST["after_all_optimizations"]
    print(f"\n  Économie totale   : {savings_total}€/mois  (-{COST_FORECAST['total_savings_pct']}%)")
    print(f"  Économie annuelle : {COST_FORECAST['annual_savings_eur']:,}€/an")
    print(f"  Payback période   : {COST_FORECAST['payback_months']} mois")

    # 8. Gouvernance FinOps
    print("\n" + sep)
    print("[7] GOUVERNANCE FINOPS\n")

    print("  Tags obligatoires :")
    for tag in FINOPS_GOVERNANCE["tagging_policy"]["required_tags"]:
        print(f"    • {tag}")

    print("\n  Alertes budgétaires :")
    for alert in FINOPS_GOVERNANCE["budget_alerts"]:
        amount = alert.get("amount_eur", "anomalie")
        print(f"    • {alert['name']:<35}  Seuil : {amount}€  →  {alert['action']}")

    print("\n  Waste detection :")
    for rule, desc in FINOPS_GOVERNANCE["waste_detection"].items():
        print(f"    • {rule:<25} : {desc}")

    print("\n  Allocation des coûts :")
    ca = FINOPS_GOVERNANCE["cost_allocation"]
    print(f"    Par Wave     : {'Oui' if ca['by_wave'] else 'Non'}")
    print(f"    Par Domain   : {'Oui' if ca['by_domain'] else 'Non'}")
    print(f"    Par Env      : {'Oui' if ca['by_environment'] else 'Non'}")
    print(f"    Showback     : {ca['showback_reports']}")

    # 9. Rapport mensuel synthèse
    print("\n" + sep)
    print("[8] RAPPORT FINOPS MENSUEL — SYNTHÈSE\n")
    report = generate_cost_report(date.today().strftime("%B %Y"))
    print(f"  Période          : {report['period']}")
    print(f"  Coût total       : {report['summary']['total_cost_eur']}€")
    print(f"  Projection annuelle : {report['summary']['projected_annual_eur']}€")
    print(f"  Stratégies identifiées : {report['optimization_pipeline']['strategies_identified']}")
    print(f"  Potentiel économies    : {report['optimization_pipeline']['total_potential_savings_eur_month']}€/mois")
    print(f"  Alertes budget actives : {report['governance_status']['budget_alerts_configured']}")
    print("\n  Prochaines actions prioritaires :")
    for action in report["next_actions"]:
        print(f"    => {action}")

    # 10. Analyse breakdown (environnement production)
    print("\n" + sep)
    print("[9] ANALYSE ENVIRONNEMENT — PRODUCTION\n")
    analysis = analyze_cost_breakdown("production")
    print(f"  Top 3 services les plus coûteux :")
    for opp in analysis["top_opportunities"]:
        print(f"    • {opp['resource']:<25} {opp['cost_eur']}€/mois  ({opp['pct']}%)")
    print(f"  Concentration top-3 : {analysis['top3_concentration_pct']}% du budget total")
    print(f"  Total optimisable   : {analysis['total_optimizable_eur_month']}€/mois")
    print(f"  Potentiel réduction : {analysis['potential_savings_pct']}%")
    print(f"\n  => {analysis['recommendation']}")

    # Footer
    print("\n" + sep)
    print("  FinOps Cloud Optimizer Agent — PRET")
    print("  AWS / Savings Plans / Karpenter / Graviton")
    print(sep + "\n")


if __name__ == "__main__":
    main()
