"""
Regenerative Finance & Impact Measurement Engine
Caelum Partners Swarm Intelligence Platform — Module 268
Mesure la performance finance régénérative, comptabilité d'impact réelle et alignement aux limites planétaires.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RegenFinanceInput:
    fund_id: str
    fund_type: str  # impact_bond | blended_finance | carbon_market | biodiversity_credit | social_impact_fund | blue_economy | circular_economy_fund | indigenous_land_trust
    region: str
    additionality_score: float
    measurability_of_impact: float
    greenwashing_risk: float          # higher = worse
    stakeholder_inclusion_depth: float
    planetary_boundary_alignment: float
    capital_recycling_efficiency: float
    community_benefit_ratio: float
    reporting_transparency_score: float
    impact_reversibility_risk: float  # higher = worse
    blended_finance_leverage: float
    sdg_alignment_score: float
    indigenous_rights_respect: float
    carbon_integrity_score: float
    biodiversity_net_gain: float
    social_return_on_investment: float
    regenerative_multiplier: float
    impact_verification_rigor: float


class RegenerativeFinanceEngine:
    """Évalue la performance régénérative des fonds d'impact et leur alignement aux limites planétaires."""

    def _integrity_score(self, f: RegenFinanceInput) -> float:
        """0.30 weight — greenwashing_risk (higher=worse), impact_reversibility_risk (higher=worse), additionality_score (inverted: low=risky)."""
        s = 0.0
        # greenwashing_risk: higher value is worse → direct contribution to risk score
        if f.greenwashing_risk >= 0.70:
            s += 40
        elif f.greenwashing_risk >= 0.45:
            s += 22
        elif f.greenwashing_risk >= 0.25:
            s += 8

        # impact_reversibility_risk: higher = worse
        if f.impact_reversibility_risk >= 0.65:
            s += 35
        elif f.impact_reversibility_risk >= 0.40:
            s += 18
        elif f.impact_reversibility_risk >= 0.20:
            s += 6

        # additionality_score: low = risky (inverted)
        if f.additionality_score <= 0.30:
            s += 25
        elif f.additionality_score <= 0.55:
            s += 12

        return min(s, 100.0)

    def _impact_score(self, f: RegenFinanceInput) -> float:
        """0.25 weight — measurability_of_impact (inv), sdg_alignment_score (inv), planetary_boundary_alignment (inv)."""
        s = 0.0
        # measurability_of_impact: low = risky
        if f.measurability_of_impact <= 0.30:
            s += 40
        elif f.measurability_of_impact <= 0.55:
            s += 22
        elif f.measurability_of_impact <= 0.75:
            s += 8

        # sdg_alignment_score: low = risky
        if f.sdg_alignment_score <= 0.30:
            s += 35
        elif f.sdg_alignment_score <= 0.55:
            s += 18
        elif f.sdg_alignment_score <= 0.75:
            s += 6

        # planetary_boundary_alignment: low = risky
        if f.planetary_boundary_alignment <= 0.30:
            s += 25
        elif f.planetary_boundary_alignment <= 0.55:
            s += 12

        return min(s, 100.0)

    def _inclusion_score(self, f: RegenFinanceInput) -> float:
        """0.25 weight — stakeholder_inclusion_depth (inv), indigenous_rights_respect (inv), community_benefit_ratio (inv)."""
        s = 0.0
        # stakeholder_inclusion_depth: low = risky
        if f.stakeholder_inclusion_depth <= 0.30:
            s += 40
        elif f.stakeholder_inclusion_depth <= 0.55:
            s += 22
        elif f.stakeholder_inclusion_depth <= 0.75:
            s += 8

        # indigenous_rights_respect: low = risky
        if f.indigenous_rights_respect <= 0.30:
            s += 35
        elif f.indigenous_rights_respect <= 0.55:
            s += 18
        elif f.indigenous_rights_respect <= 0.75:
            s += 6

        # community_benefit_ratio: low = risky
        if f.community_benefit_ratio <= 0.30:
            s += 25
        elif f.community_benefit_ratio <= 0.55:
            s += 12

        return min(s, 100.0)

    def _verification_score(self, f: RegenFinanceInput) -> float:
        """0.20 weight — reporting_transparency_score (inv), impact_verification_rigor (inv), carbon_integrity_score (inv)."""
        s = 0.0
        # reporting_transparency_score: low = risky
        if f.reporting_transparency_score <= 0.30:
            s += 40
        elif f.reporting_transparency_score <= 0.55:
            s += 22
        elif f.reporting_transparency_score <= 0.75:
            s += 8

        # impact_verification_rigor: low = risky
        if f.impact_verification_rigor <= 0.30:
            s += 35
        elif f.impact_verification_rigor <= 0.55:
            s += 18
        elif f.impact_verification_rigor <= 0.75:
            s += 6

        # carbon_integrity_score: low = risky
        if f.carbon_integrity_score <= 0.30:
            s += 25
        elif f.carbon_integrity_score <= 0.55:
            s += 12

        return min(s, 100.0)

    def _composite(self, integrity: float, impact: float, inclusion: float, verification: float) -> float:
        raw = integrity * 0.30 + impact * 0.25 + inclusion * 0.25 + verification * 0.20
        return min(round(raw * 100) / 100, 100.0)

    def _pattern(self, f: RegenFinanceInput) -> str:
        if f.greenwashing_risk >= 0.65 and f.carbon_integrity_score <= 0.35:
            return "greenwashing_exposure"
        if f.measurability_of_impact <= 0.30 and f.sdg_alignment_score <= 0.35:
            return "impact_dilution"
        if f.indigenous_rights_respect <= 0.30 and f.stakeholder_inclusion_depth <= 0.35:
            return "exclusion_deficit"
        if f.impact_verification_rigor <= 0.30 and f.reporting_transparency_score <= 0.35:
            return "measurement_gap"
        if f.capital_recycling_efficiency <= 0.25 and f.regenerative_multiplier <= 0.30:
            return "capital_misallocation"
        return "none"

    def _risk(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    def _severity(self, composite: float) -> str:
        if composite >= 60:
            return "extractive"
        if composite >= 40:
            return "transitioning"
        if composite >= 20:
            return "regenerating"
        return "thriving"

    def _action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            if pattern == "greenwashing_exposure":
                return "greenwashing_intervention"
            return "impact_audit"
        if risk == "high":
            if pattern in ("exclusion_deficit",):
                return "stakeholder_realignment"
            return "measurement_upgrade"
        if risk == "moderate":
            return "impact_monitoring"
        return "no_action"

    def _signal(self, f: RegenFinanceInput, pattern: str, composite: float) -> str:
        if composite < 20:
            return (
                "Finance régénérative exemplaire — intégrité carbone certifiée, "
                "droits autochtones respectés, impact mesurable et vérifiable, "
                f"multiplicateur régénératif {f.regenerative_multiplier:.2f}"
            )
        labels: Dict[str, str] = {
            "greenwashing_exposure": "Exposition au greenwashing",
            "impact_dilution": "Dilution d'impact",
            "exclusion_deficit": "Déficit d'inclusion",
            "measurement_gap": "Lacune de mesure",
            "capital_misallocation": "Mauvaise allocation du capital",
        }
        label = labels.get(pattern, pattern.replace("_", " "))
        return (
            f"{label} — risque greenwashing {f.greenwashing_risk:.2f} — "
            f"alignement SDG {f.sdg_alignment_score:.2f} — "
            f"droits autochtones {f.indigenous_rights_respect:.2f} — "
            f"composite {round(composite)}"
        )

    def _assess_one(self, f: RegenFinanceInput) -> Dict[str, Any]:
        integrity = self._integrity_score(f)
        impact = self._impact_score(f)
        inclusion = self._inclusion_score(f)
        verification = self._verification_score(f)
        comp = self._composite(integrity, impact, inclusion, verification)
        pat = self._pattern(f)
        risk = self._risk(comp)
        sev = self._severity(comp)
        act = self._action(risk, pat)
        return {
            "fund_id": f.fund_id,
            "fund_type": f.fund_type,
            "region": f.region,
            "regen_finance_risk": risk,
            "impact_pattern": pat,
            "impact_severity": sev,
            "recommended_action": act,
            "integrity_score": integrity,
            "impact_score": impact,
            "inclusion_score": inclusion,
            "verification_score": verification,
            "regen_finance_composite": comp,
            "has_greenwashing_signal": comp >= 40 or f.greenwashing_risk >= 0.55 or f.carbon_integrity_score <= 0.35,
            "requires_impact_audit": comp >= 25 or f.impact_verification_rigor <= 0.35 or f.additionality_score <= 0.30,
            "estimated_impact_deficit_index": min(
                round(comp / 100 * (1 - f.impact_verification_rigor + 0.01) * 10 * 100) / 100,
                10.0,
            ),
            "regen_signal": self._signal(f, pat, comp),
        }

    def assess_batch(self, funds: List[RegenFinanceInput]) -> List[Dict[str, Any]]:
        """Évalue un lot de fonds régénératifs."""
        return [self._assess_one(f) for f in funds]

    def summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Génère un résumé agrégé — exactement 13 clés."""
        n = len(results) or 1
        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        t_integrity = t_impact = t_inclusion = t_verification = t_comp = t_deficit = 0.0
        greenwash_c = audit_c = 0

        for r in results:
            risk_counts[r["regen_finance_risk"]] = risk_counts.get(r["regen_finance_risk"], 0) + 1
            pattern_counts[r["impact_pattern"]] = pattern_counts.get(r["impact_pattern"], 0) + 1
            severity_counts[r["impact_severity"]] = severity_counts.get(r["impact_severity"], 0) + 1
            action_counts[r["recommended_action"]] = action_counts.get(r["recommended_action"], 0) + 1
            t_integrity += r["integrity_score"]
            t_impact += r["impact_score"]
            t_inclusion += r["inclusion_score"]
            t_verification += r["verification_score"]
            t_comp += r["regen_finance_composite"]
            t_deficit += r["estimated_impact_deficit_index"]
            if r["has_greenwashing_signal"]:
                greenwash_c += 1
            if r["requires_impact_audit"]:
                audit_c += 1

        return {
            "total": len(results),
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_regen_finance_composite": round(t_comp / n * 10) / 10,
            "greenwashing_signal_count": greenwash_c,
            "impact_audit_required_count": audit_c,
            "avg_integrity_score": round(t_integrity / n * 10) / 10,
            "avg_impact_score": round(t_impact / n * 10) / 10,
            "avg_inclusion_score": round(t_inclusion / n * 10) / 10,
            "avg_verification_score": round(t_verification / n * 10) / 10,
            "avg_estimated_impact_deficit_index": round(t_deficit / n * 100) / 100,
        }


def to_dict(result: Dict[str, Any]) -> Dict[str, Any]:
    """Retourne exactement 15 clés."""
    return {
        "fund_id": result["fund_id"],
        "fund_type": result["fund_type"],
        "region": result["region"],
        "regen_finance_risk": result["regen_finance_risk"],
        "impact_pattern": result["impact_pattern"],
        "impact_severity": result["impact_severity"],
        "recommended_action": result["recommended_action"],
        "integrity_score": result["integrity_score"],
        "impact_score": result["impact_score"],
        "inclusion_score": result["inclusion_score"],
        "verification_score": result["verification_score"],
        "regen_finance_composite": result["regen_finance_composite"],
        "has_greenwashing_signal": result["has_greenwashing_signal"],
        "requires_impact_audit": result["requires_impact_audit"],
        "estimated_impact_deficit_index": result["estimated_impact_deficit_index"],
    }
