from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class ComplianceLevel(str, Enum):
    FULL          = "full"
    PARTIAL       = "partial"
    MINIMAL       = "minimal"
    NON_COMPLIANT = "non_compliant"


class MethodologyAdherence(str, Enum):
    CHAMPION   = "champion"
    SOLID      = "solid"
    IMPROVABLE = "improvable"
    AT_RISK    = "at_risk"


class ComplianceRisk(str, Enum):
    LOW      = "low"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class ComplianceAction(str, Enum):
    MAINTAIN       = "maintain"
    COACH_GAPS     = "coach_gaps"
    PROCESS_REVIEW = "process_review"
    REMEDIATE      = "remediate"


@dataclass
class ProcessComplianceInput:
    rep_id: str
    rep_name: str
    deal_id: str
    deal_stage: str
    stage_days_elapsed: int
    needs_assessment_completed: int
    pain_points_documented: int
    decision_criteria_captured: int
    decision_process_mapped: int
    budget_confirmed: int
    timeline_confirmed: int
    champion_identified: int
    executive_sponsor_engaged: int
    competition_identified: int
    business_case_built: int
    technical_validation_done: int
    mutual_success_plan_agreed: int
    legal_review_started: int
    crm_last_updated_days_ago: int
    stage_appropriate_activities_completed: int
    coaching_cadence_adherence_pct: float
    manager_reviewed_this_month: int


@dataclass
class ProcessComplianceResult:
    rep_id: str
    deal_id: str
    compliance_level: ComplianceLevel
    methodology_adherence: MethodologyAdherence
    compliance_risk: ComplianceRisk
    compliance_action: ComplianceAction
    discovery_score: float
    qualification_score: float
    progression_score: float
    crm_hygiene_score: float
    compliance_composite: float
    missing_steps_count: int
    is_compliant: bool
    needs_process_coaching: bool
    key_gap: str

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "deal_id": self.deal_id,
            "compliance_level": self.compliance_level.value,
            "methodology_adherence": self.methodology_adherence.value,
            "compliance_risk": self.compliance_risk.value,
            "compliance_action": self.compliance_action.value,
            "discovery_score": self.discovery_score,
            "qualification_score": self.qualification_score,
            "progression_score": self.progression_score,
            "crm_hygiene_score": self.crm_hygiene_score,
            "compliance_composite": self.compliance_composite,
            "missing_steps_count": self.missing_steps_count,
            "is_compliant": self.is_compliant,
            "needs_process_coaching": self.needs_process_coaching,
            "key_gap": self.key_gap,
        }


def _discovery_score(inp: ProcessComplianceInput) -> float:
    score = 0.0
    # Core discovery steps (each worth 20)
    if inp.needs_assessment_completed:
        score += 25.0
    if inp.pain_points_documented:
        score += 25.0
    if inp.decision_criteria_captured:
        score += 25.0
    if inp.competition_identified:
        score += 15.0
    if inp.timeline_confirmed:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _qualification_score(inp: ProcessComplianceInput) -> float:
    score = 0.0
    if inp.decision_process_mapped:
        score += 20.0
    if inp.budget_confirmed:
        score += 25.0
    if inp.champion_identified:
        score += 25.0
    if inp.executive_sponsor_engaged:
        score += 20.0
    if inp.business_case_built:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _progression_score(inp: ProcessComplianceInput) -> float:
    score = 0.0
    if inp.technical_validation_done:
        score += 25.0
    if inp.mutual_success_plan_agreed:
        score += 25.0
    if inp.legal_review_started:
        score += 20.0
    # Stage-appropriate activities
    if inp.stage_appropriate_activities_completed >= 8:
        score += 30.0
    elif inp.stage_appropriate_activities_completed >= 5:
        score += 20.0
    elif inp.stage_appropriate_activities_completed >= 3:
        score += 12.0
    elif inp.stage_appropriate_activities_completed >= 1:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _crm_hygiene_score(inp: ProcessComplianceInput) -> float:
    score = 0.0
    # CRM recency (0-50)
    if inp.crm_last_updated_days_ago <= 1:
        score += 50.0
    elif inp.crm_last_updated_days_ago <= 3:
        score += 38.0
    elif inp.crm_last_updated_days_ago <= 7:
        score += 24.0
    elif inp.crm_last_updated_days_ago <= 14:
        score += 12.0
    # Manager review (0-25)
    if inp.manager_reviewed_this_month:
        score += 25.0
    # Coaching adherence (0-25)
    score += inp.coaching_cadence_adherence_pct * 0.25
    return max(0.0, min(100.0, round(score, 1)))


def _composite(disc: float, qual: float, prog: float, crm: float) -> float:
    raw = disc * 0.30 + qual * 0.25 + prog * 0.25 + crm * 0.20
    return round(raw, 1)


def _missing_steps_count(inp: ProcessComplianceInput) -> int:
    steps = [
        inp.needs_assessment_completed,
        inp.pain_points_documented,
        inp.decision_criteria_captured,
        inp.decision_process_mapped,
        inp.budget_confirmed,
        inp.timeline_confirmed,
        inp.champion_identified,
        inp.executive_sponsor_engaged,
        inp.competition_identified,
        inp.business_case_built,
    ]
    return sum(1 for s in steps if s == 0)


def _compliance_level(composite: float) -> ComplianceLevel:
    if composite >= 80:
        return ComplianceLevel.FULL
    if composite >= 60:
        return ComplianceLevel.PARTIAL
    if composite >= 40:
        return ComplianceLevel.MINIMAL
    return ComplianceLevel.NON_COMPLIANT


def _methodology_adherence(composite: float, missing: int) -> MethodologyAdherence:
    if composite >= 75 and missing <= 1:
        return MethodologyAdherence.CHAMPION
    if composite >= 60 and missing <= 3:
        return MethodologyAdherence.SOLID
    if composite >= 45:
        return MethodologyAdherence.IMPROVABLE
    return MethodologyAdherence.AT_RISK


def _compliance_risk(composite: float, missing: int) -> ComplianceRisk:
    if composite < 30 or missing >= 7:
        return ComplianceRisk.CRITICAL
    if composite < 45 or missing >= 5:
        return ComplianceRisk.HIGH
    if composite < 60 or missing >= 3:
        return ComplianceRisk.MODERATE
    return ComplianceRisk.LOW


def _compliance_action(risk: ComplianceRisk) -> ComplianceAction:
    if risk == ComplianceRisk.CRITICAL:
        return ComplianceAction.REMEDIATE
    if risk == ComplianceRisk.HIGH:
        return ComplianceAction.PROCESS_REVIEW
    if risk == ComplianceRisk.MODERATE:
        return ComplianceAction.COACH_GAPS
    return ComplianceAction.MAINTAIN


def _key_gap(inp: ProcessComplianceInput, disc: float, qual: float, prog: float, crm: float) -> str:
    if not inp.champion_identified:
        return "champion not identified"
    if not inp.budget_confirmed:
        return "budget not confirmed"
    if not inp.decision_process_mapped:
        return "decision process not mapped"
    if not inp.needs_assessment_completed:
        return "needs assessment incomplete"
    if inp.crm_last_updated_days_ago > 14:
        return "CRM out of date"
    scores = {"discovery": disc, "qualification": qual, "progression": prog, "CRM hygiene": crm}
    return f"weakest area: {min(scores, key=lambda k: scores[k])}"


class SalesProcessComplianceMonitor:
    def __init__(self) -> None:
        self._results: dict[str, ProcessComplianceResult] = {}

    def assess(self, inp: ProcessComplianceInput) -> ProcessComplianceResult:
        disc  = _discovery_score(inp)
        qual  = _qualification_score(inp)
        prog  = _progression_score(inp)
        crm   = _crm_hygiene_score(inp)
        comp  = _composite(disc, qual, prog, crm)
        miss  = _missing_steps_count(inp)
        level = _compliance_level(comp)
        adh   = _methodology_adherence(comp, miss)
        risk  = _compliance_risk(comp, miss)
        action = _compliance_action(risk)
        gap   = _key_gap(inp, disc, qual, prog, crm)

        is_compliant        = comp >= 70.0 and miss <= 2
        needs_coaching      = comp < 50.0 or miss >= 4

        result = ProcessComplianceResult(
            rep_id=inp.rep_id,
            deal_id=inp.deal_id,
            compliance_level=level,
            methodology_adherence=adh,
            compliance_risk=risk,
            compliance_action=action,
            discovery_score=disc,
            qualification_score=qual,
            progression_score=prog,
            crm_hygiene_score=crm,
            compliance_composite=comp,
            missing_steps_count=miss,
            is_compliant=is_compliant,
            needs_process_coaching=needs_coaching,
            key_gap=gap,
        )
        self._results[inp.deal_id] = result
        return result

    def assess_batch(self, inputs: List[ProcessComplianceInput]) -> List[ProcessComplianceResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.compliance_composite, reverse=True)
        return results

    def get(self, deal_id: str) -> ProcessComplianceResult | None:
        return self._results.get(deal_id)

    def all_deals(self) -> List[ProcessComplianceResult]:
        return sorted(self._results.values(), key=lambda r: r.compliance_composite, reverse=True)

    def compliant_deals(self) -> List[ProcessComplianceResult]:
        return [r for r in self._results.values() if r.is_compliant]

    def coaching_queue(self) -> List[ProcessComplianceResult]:
        return [r for r in self._results.values() if r.needs_process_coaching]

    def by_level(self, level: ComplianceLevel) -> List[ProcessComplianceResult]:
        return [r for r in self._results.values() if r.compliance_level == level]

    def by_adherence(self, adherence: MethodologyAdherence) -> List[ProcessComplianceResult]:
        return [r for r in self._results.values() if r.methodology_adherence == adherence]

    def avg_compliance_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.compliance_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        level_counts:     dict[str, int] = {}
        adherence_counts: dict[str, int] = {}
        risk_counts:      dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        for r in results:
            level_counts[r.compliance_level.value]          = level_counts.get(r.compliance_level.value, 0) + 1
            adherence_counts[r.methodology_adherence.value] = adherence_counts.get(r.methodology_adherence.value, 0) + 1
            risk_counts[r.compliance_risk.value]             = risk_counts.get(r.compliance_risk.value, 0) + 1
            action_counts[r.compliance_action.value]         = action_counts.get(r.compliance_action.value, 0) + 1
        return {
            "total": n,
            "compliance_level_counts":    level_counts,
            "methodology_adherence_counts": adherence_counts,
            "compliance_risk_counts":     risk_counts,
            "action_counts":              action_counts,
            "avg_compliance_composite":   self.avg_compliance_composite(),
            "fully_compliant_count":      len(self.compliant_deals()),
            "coaching_needed_count":      len(self.coaching_queue()),
            "avg_discovery_score":        round(sum(r.discovery_score for r in results) / n, 1) if n else 0.0,
            "avg_qualification_score":    round(sum(r.qualification_score for r in results) / n, 1) if n else 0.0,
            "avg_progression_score":      round(sum(r.progression_score for r in results) / n, 1) if n else 0.0,
            "avg_crm_hygiene_score":      round(sum(r.crm_hygiene_score for r in results) / n, 1) if n else 0.0,
            "avg_missing_steps":          round(sum(r.missing_steps_count for r in results) / n, 1) if n else 0.0,
        }
