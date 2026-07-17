from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class PensionCollapseInput:
    entity_id: str
    pension_system_type: str
    region: str
    demographic_dependency_ratio: float = 0.0
    funding_gap_index: float = 0.0
    investment_return_shortfall: float = 0.0
    longevity_risk_exposure: float = 0.0
    automation_contribution_erosion: float = 0.0
    political_reform_paralysis: float = 0.0
    intergenerational_fairness_gap: float = 0.0
    pension_debt_to_gdp: float = 0.0
    benefit_adequacy_erosion: float = 0.0
    public_pension_trust_deficit: float = 0.0
    private_pension_volatility: float = 0.0
    informal_economy_coverage_gap: float = 0.0
    migration_contribution_dependency: float = 0.0
    early_retirement_pressure: float = 0.0
    disability_benefit_strain: float = 0.0
    pension_system_complexity_risk: float = 0.0
    climate_transition_stranded_assets: float = 0.0


def _compute_pension_scores(inp: PensionCollapseInput) -> Dict[str, float]:
    demographic_score = (
        inp.demographic_dependency_ratio * 0.4
        + inp.longevity_risk_exposure * 0.35
        + inp.automation_contribution_erosion * 0.25
    ) * 100

    funding_score = (
        inp.funding_gap_index * 0.4
        + inp.pension_debt_to_gdp * 0.35
        + inp.investment_return_shortfall * 0.25
    ) * 100

    social_score = (
        inp.intergenerational_fairness_gap * 0.4
        + inp.benefit_adequacy_erosion * 0.35
        + inp.public_pension_trust_deficit * 0.25
    ) * 100

    structural_score = (
        inp.political_reform_paralysis * 0.4
        + inp.informal_economy_coverage_gap * 0.35
        + inp.climate_transition_stranded_assets * 0.25
    ) * 100

    composite = (
        demographic_score * 0.30
        + funding_score * 0.25
        + social_score * 0.25
        + structural_score * 0.20
    )

    return {
        "demographic_score": round(demographic_score, 2),
        "funding_score": round(funding_score, 2),
        "social_score": round(social_score, 2),
        "structural_score": round(structural_score, 2),
        "pension_composite": round(composite, 2),
    }


def _compute_pension_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    elif composite >= 40:
        return "high"
    elif composite >= 20:
        return "moderate"
    else:
        return "low"


def _compute_pension_pattern(inp: PensionCollapseInput) -> str:
    if inp.demographic_dependency_ratio >= 0.70 and inp.automation_contribution_erosion >= 0.65:
        return "demographic_collapse"
    if inp.funding_gap_index >= 0.70 and inp.pension_debt_to_gdp >= 0.65:
        return "pension_insolvency"
    if inp.intergenerational_fairness_gap >= 0.70 and inp.benefit_adequacy_erosion >= 0.65:
        return "generational_war"
    if inp.political_reform_paralysis >= 0.70 and inp.public_pension_trust_deficit >= 0.65:
        return "reform_paralysis"
    if inp.automation_contribution_erosion >= 0.70 and inp.informal_economy_coverage_gap >= 0.65:
        return "automation_displacement"
    return "none"


def _compute_pension_severity(composite: float) -> str:
    if composite >= 75:
        return "pension_emergency"
    elif composite >= 50:
        return "pension_crisis"
    elif composite >= 25:
        return "pension_stress"
    else:
        return "pension_sustainable"


def _compute_recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "pension_emergency_restructuring"
    if risk == "high" and pattern == "pension_insolvency":
        return "sovereign_pension_bailout"
    if risk == "high":
        return "pension_reform_program"
    if risk == "moderate":
        return "pension_monitoring"
    return "no_action"


def _compute_pension_signal(risk: str, pattern: str, region: str) -> str:
    signals = {
        "critical": f"⚠️ ALERTE CRITIQUE — Risque d'effondrement du système de retraite détecté ({region})",
        "high": f"🔴 RISQUE ÉLEVÉ — Intervention urgente requise pour stabiliser le système de retraite ({region})",
        "moderate": f"🟡 RISQUE MODÉRÉ — Surveillance renforcée du système de retraite recommandée ({region})",
        "low": f"🟢 RISQUE FAIBLE — Système de retraite stable ({region})",
    }
    pattern_notes = {
        "demographic_collapse": " | Motif: Effondrement démographique imminent",
        "pension_insolvency": " | Motif: Insolvabilité du fonds de retraite",
        "generational_war": " | Motif: Conflit intergénérationnel critique",
        "reform_paralysis": " | Motif: Paralysie des réformes structurelles",
        "automation_displacement": " | Motif: Érosion des cotisations par l'automatisation",
        "none": "",
    }
    return signals.get(risk, "") + pattern_notes.get(pattern, "")


def analyze_pension_entity(inp: PensionCollapseInput) -> Dict[str, Any]:
    scores = _compute_pension_scores(inp)
    composite = scores["pension_composite"]
    risk = _compute_pension_risk(composite)
    pattern = _compute_pension_pattern(inp)
    severity = _compute_pension_severity(composite)
    action = _compute_recommended_action(risk, pattern)
    signal = _compute_pension_signal(risk, pattern, inp.region)

    return {
        "entity_id": inp.entity_id,
        "region": inp.region,
        "pension_system_type": inp.pension_system_type,
        "pension_risk": risk,
        "pension_pattern": pattern,
        "pension_severity": severity,
        "recommended_action": action,
        "demographic_score": scores["demographic_score"],
        "funding_score": scores["funding_score"],
        "social_score": scores["social_score"],
        "structural_score": scores["structural_score"],
        "pension_composite": composite,
        "is_pension_crisis": composite >= 60,
        "requires_pension_intervention": composite >= 40,
        "pension_signal": signal,
    }


class PensionCollapseEngine:
    def analyze(self, entities: List[PensionCollapseInput]) -> Dict[str, Any]:
        results = [analyze_pension_entity(e) for e in entities]

        total = len(results)
        critical_count = sum(1 for r in results if r["pension_risk"] == "critical")
        high_count = sum(1 for r in results if r["pension_risk"] == "high")
        moderate_count = sum(1 for r in results if r["pension_risk"] == "moderate")
        low_count = sum(1 for r in results if r["pension_risk"] == "low")
        crisis_count = sum(1 for r in results if r["is_pension_crisis"])
        intervention_count = sum(1 for r in results if r["requires_pension_intervention"])

        avg_composite = sum(r["pension_composite"] for r in results) / total if total > 0 else 0.0
        avg_demographic = sum(r["demographic_score"] for r in results) / total if total > 0 else 0.0
        avg_funding = sum(r["funding_score"] for r in results) / total if total > 0 else 0.0
        avg_social = sum(r["social_score"] for r in results) / total if total > 0 else 0.0
        avg_structural = sum(r["structural_score"] for r in results) / total if total > 0 else 0.0

        patterns = [r["pension_pattern"] for r in results if r["pension_pattern"] != "none"]
        dominant_pattern = max(set(patterns), key=patterns.count) if patterns else "none"

        return {
            "module": "Module 320 — Pension & Social Security System Collapse Intelligence Engine",
            "total_entities": total,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "crisis_count": crisis_count,
            "intervention_count": intervention_count,
            "avg_composite": round(avg_composite, 2),
            "avg_demographic_score": round(avg_demographic, 2),
            "avg_funding_score": round(avg_funding, 2),
            "avg_social_score": round(avg_social, 2),
            "avg_structural_score": round(avg_structural, 2),
            "dominant_pattern": dominant_pattern,
            "avg_estimated_pension_crisis_index": round(avg_composite / 100 * 10, 2),
            "results": results,
        }
