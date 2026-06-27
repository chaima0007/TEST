from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class ComplexityTier(str, Enum):
    SIMPLE = "simple"
    STANDARD = "standard"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"


class ComplexityRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ComplexityDimension(str, Enum):
    PEOPLE = "people"
    PROCESS = "process"
    TECHNOLOGY = "technology"
    LEGAL = "legal"


class ComplexityAction(str, Enum):
    STANDARD_PROCESS = "standard_process"
    ASSIGN_SOLUTION_ENGINEER = "assign_solution_engineer"
    EXECUTIVE_SPONSOR_REQUIRED = "executive_sponsor_required"
    DEDICATED_DEAL_TEAM = "dedicated_deal_team"


@dataclass
class DealComplexityInput:
    deal_id: str
    rep_id: str
    deal_name: str
    deal_value_usd: float
    stakeholder_count: int
    department_count: int
    legal_review_required: int
    security_review_required: int
    procurement_involvement: int
    custom_contract_required: int
    integration_complexity_score: float
    multi_year_deal: int
    competitive_deal: int
    proof_of_concept_required: int
    deal_stage: int
    industry_regulatory_complexity: float
    geographic_complexity: int
    pricing_complexity_score: float
    existing_tech_debt_score: float
    executive_alignment_required: int
    partner_involvement_required: int
    estimated_implementation_months: int


@dataclass
class DealComplexityResult:
    deal_id: str
    rep_id: str
    complexity_tier: ComplexityTier
    complexity_risk: ComplexityRisk
    primary_complexity_dimension: ComplexityDimension
    complexity_action: ComplexityAction
    people_complexity_score: float
    process_complexity_score: float
    technology_complexity_score: float
    legal_complexity_score: float
    complexity_composite: float
    requires_deal_desk: bool
    needs_executive_sponsor: bool
    estimated_win_probability_impact_pct: float
    complexity_summary: str

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "rep_id": self.rep_id,
            "complexity_tier": self.complexity_tier.value,
            "complexity_risk": self.complexity_risk.value,
            "primary_complexity_dimension": self.primary_complexity_dimension.value,
            "complexity_action": self.complexity_action.value,
            "people_complexity_score": self.people_complexity_score,
            "process_complexity_score": self.process_complexity_score,
            "technology_complexity_score": self.technology_complexity_score,
            "legal_complexity_score": self.legal_complexity_score,
            "complexity_composite": self.complexity_composite,
            "requires_deal_desk": self.requires_deal_desk,
            "needs_executive_sponsor": self.needs_executive_sponsor,
            "estimated_win_probability_impact_pct": self.estimated_win_probability_impact_pct,
            "complexity_summary": self.complexity_summary,
        }


def _people_complexity_score(inp: DealComplexityInput) -> float:
    score = 0.0
    # Stakeholder count (0-30)
    if inp.stakeholder_count >= 10:
        score += 30.0
    elif inp.stakeholder_count >= 6:
        score += 22.0
    elif inp.stakeholder_count >= 3:
        score += 12.0
    elif inp.stakeholder_count >= 2:
        score += 5.0
    # Department count (0-25)
    if inp.department_count >= 5:
        score += 25.0
    elif inp.department_count >= 3:
        score += 17.0
    elif inp.department_count >= 2:
        score += 8.0
    # Executive alignment (0-20)
    if inp.executive_alignment_required:
        score += 20.0
    # Geographic complexity (0-15)
    if inp.geographic_complexity >= 3:
        score += 15.0
    elif inp.geographic_complexity >= 2:
        score += 8.0
    # Competitive environment (0-10)
    if inp.competitive_deal:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _process_complexity_score(inp: DealComplexityInput) -> float:
    score = 0.0
    # Procurement involvement (0-25)
    if inp.procurement_involvement:
        score += 25.0
    # Multi-year deal (0-20)
    if inp.multi_year_deal:
        score += 20.0
    # POC required (0-20)
    if inp.proof_of_concept_required:
        score += 20.0
    # Implementation duration (0-20)
    if inp.estimated_implementation_months >= 12:
        score += 20.0
    elif inp.estimated_implementation_months >= 6:
        score += 13.0
    elif inp.estimated_implementation_months >= 3:
        score += 6.0
    # Partner involvement (0-15)
    if inp.partner_involvement_required:
        score += 15.0
    return max(0.0, min(100.0, round(score, 1)))


def _technology_complexity_score(inp: DealComplexityInput) -> float:
    score = 0.0
    # Integration complexity (0-40)
    score += inp.integration_complexity_score * 0.40
    # Existing tech debt (0-30)
    score += inp.existing_tech_debt_score * 0.30
    # Security review (0-20)
    if inp.security_review_required:
        score += 20.0
    # Pricing complexity (0-10)
    score += inp.pricing_complexity_score * 0.10
    return max(0.0, min(100.0, round(score, 1)))


def _legal_complexity_score(inp: DealComplexityInput) -> float:
    score = 0.0
    # Legal review (0-30)
    if inp.legal_review_required:
        score += 30.0
    # Custom contract (0-25)
    if inp.custom_contract_required:
        score += 25.0
    # Industry regulatory complexity (0-25)
    score += inp.industry_regulatory_complexity * 0.25
    # Security + legal combined (0-10 bonus)
    if inp.security_review_required and inp.legal_review_required:
        score += 10.0
    # Geographic complexity adds legal (0-10)
    if inp.geographic_complexity >= 3:
        score += 10.0
    elif inp.geographic_complexity >= 2:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(people: float, process: float, technology: float, legal: float) -> float:
    raw = people * 0.25 + process * 0.25 + technology * 0.25 + legal * 0.25
    return round(raw, 1)


def _complexity_tier(composite: float) -> ComplexityTier:
    if composite >= 70:
        return ComplexityTier.ENTERPRISE
    if composite >= 50:
        return ComplexityTier.COMPLEX
    if composite >= 25:
        return ComplexityTier.STANDARD
    return ComplexityTier.SIMPLE


def _complexity_risk(composite: float, inp: DealComplexityInput) -> ComplexityRisk:
    if composite >= 70 or (inp.legal_review_required and inp.security_review_required and inp.custom_contract_required):
        return ComplexityRisk.CRITICAL
    if composite >= 50:
        return ComplexityRisk.HIGH
    if composite >= 25:
        return ComplexityRisk.MODERATE
    return ComplexityRisk.LOW


def _primary_dimension(people: float, process: float, technology: float, legal: float) -> ComplexityDimension:
    scores = {
        ComplexityDimension.PEOPLE: people,
        ComplexityDimension.PROCESS: process,
        ComplexityDimension.TECHNOLOGY: technology,
        ComplexityDimension.LEGAL: legal,
    }
    return max(scores, key=lambda k: scores[k])


def _complexity_action(risk: ComplexityRisk, inp: DealComplexityInput) -> ComplexityAction:
    if risk == ComplexityRisk.CRITICAL:
        return ComplexityAction.DEDICATED_DEAL_TEAM
    if risk == ComplexityRisk.HIGH:
        return ComplexityAction.EXECUTIVE_SPONSOR_REQUIRED
    if risk == ComplexityRisk.MODERATE:
        return ComplexityAction.ASSIGN_SOLUTION_ENGINEER
    return ComplexityAction.STANDARD_PROCESS


def _win_probability_impact(composite: float) -> float:
    if composite >= 70:
        return -30.0
    if composite >= 50:
        return -20.0
    if composite >= 25:
        return -12.0
    return -5.0


def _complexity_summary(inp: DealComplexityInput, people: float, process: float,
                         technology: float, legal: float) -> str:
    dimension = _primary_dimension(people, process, technology, legal)
    factors = []
    if inp.legal_review_required and inp.custom_contract_required:
        factors.append("custom legal")
    if inp.security_review_required:
        factors.append("security review")
    if inp.proof_of_concept_required:
        factors.append("POC required")
    if inp.estimated_implementation_months >= 9:
        factors.append(f"{inp.estimated_implementation_months}-month implementation")
    if inp.geographic_complexity >= 2:
        factors.append("multi-region")
    if factors:
        return f"primary: {dimension.value} — {', '.join(factors[:3])}"
    return f"primary complexity driver: {dimension.value} ({max(people, process, technology, legal):.0f}/100)"


class DealComplexityIntelligence:
    def __init__(self) -> None:
        self._results: dict[str, DealComplexityResult] = {}
        self._deal_values: dict[str, float] = {}

    def assess(self, inp: DealComplexityInput) -> DealComplexityResult:
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        composite = _composite(people, process, technology, legal)

        tier = _complexity_tier(composite)
        risk = _complexity_risk(composite, inp)
        dimension = _primary_dimension(people, process, technology, legal)
        action = _complexity_action(risk, inp)
        requires_desk = composite >= 60 or (inp.legal_review_required and inp.custom_contract_required)
        needs_exec = composite >= 75 or inp.deal_value_usd >= 500000.0
        win_impact = _win_probability_impact(composite)
        summary = _complexity_summary(inp, people, process, technology, legal)

        result = DealComplexityResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            complexity_tier=tier,
            complexity_risk=risk,
            primary_complexity_dimension=dimension,
            complexity_action=action,
            people_complexity_score=people,
            process_complexity_score=process,
            technology_complexity_score=technology,
            legal_complexity_score=legal,
            complexity_composite=composite,
            requires_deal_desk=requires_desk,
            needs_executive_sponsor=needs_exec,
            estimated_win_probability_impact_pct=win_impact,
            complexity_summary=summary,
        )
        self._results[inp.deal_id] = result
        self._deal_values[inp.deal_id] = inp.deal_value_usd
        return result

    def assess_batch(self, inputs: List[DealComplexityInput]) -> List[DealComplexityResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.complexity_composite, reverse=True)
        return results

    def get(self, deal_id: str) -> DealComplexityResult | None:
        return self._results.get(deal_id)

    def all_deals(self) -> List[DealComplexityResult]:
        return sorted(self._results.values(), key=lambda r: r.complexity_composite, reverse=True)

    def deal_desk_queue(self) -> List[DealComplexityResult]:
        return [r for r in self._results.values() if r.requires_deal_desk]

    def executive_sponsor_queue(self) -> List[DealComplexityResult]:
        return [r for r in self._results.values() if r.needs_executive_sponsor]

    def by_tier(self, tier: ComplexityTier) -> List[DealComplexityResult]:
        return [r for r in self._results.values() if r.complexity_tier == tier]

    def by_risk(self, risk: ComplexityRisk) -> List[DealComplexityResult]:
        return [r for r in self._results.values() if r.complexity_risk == risk]

    def avg_complexity_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.complexity_composite for r in self._results.values()) / len(self._results), 1)

    def high_complexity_pipeline_usd(self) -> float:
        return round(sum(
            self._deal_values.get(r.deal_id, 0.0)
            for r in self._results.values() if r.complexity_composite >= 50
        ), 2)

    def reset(self) -> None:
        self._results.clear()
        self._deal_values.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        tier_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        dim_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            tier_counts[r.complexity_tier.value] = tier_counts.get(r.complexity_tier.value, 0) + 1
            risk_counts[r.complexity_risk.value] = risk_counts.get(r.complexity_risk.value, 0) + 1
            dim_counts[r.primary_complexity_dimension.value] = dim_counts.get(r.primary_complexity_dimension.value, 0) + 1
            action_counts[r.complexity_action.value] = action_counts.get(r.complexity_action.value, 0) + 1
        return {
            "total": n,
            "tier_counts": tier_counts,
            "risk_counts": risk_counts,
            "dimension_counts": dim_counts,
            "action_counts": action_counts,
            "avg_complexity_composite": self.avg_complexity_composite(),
            "deal_desk_required_count": len(self.deal_desk_queue()),
            "executive_sponsor_needed_count": len(self.executive_sponsor_queue()),
            "avg_people_score": round(sum(r.people_complexity_score for r in results) / n, 1) if n else 0.0,
            "avg_process_score": round(sum(r.process_complexity_score for r in results) / n, 1) if n else 0.0,
            "avg_technology_score": round(sum(r.technology_complexity_score for r in results) / n, 1) if n else 0.0,
            "avg_legal_score": round(sum(r.legal_complexity_score for r in results) / n, 1) if n else 0.0,
            "high_complexity_pipeline_usd": self.high_complexity_pipeline_usd(),
        }
