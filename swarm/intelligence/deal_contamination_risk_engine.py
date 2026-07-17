from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class ContaminationLevel(str, Enum):
    CLEAN = "clean"
    ADVISORY = "advisory"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"


class ContaminationRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ContaminationType(str, Enum):
    NONE = "none"
    CONFLICT_OF_INTEREST = "conflict_of_interest"
    COMPLIANCE_GAP = "compliance_gap"
    CHANNEL_CONFLICT = "channel_conflict"
    FINANCIAL_IRREGULARITY = "financial_irregularity"


class ContaminationAction(str, Enum):
    PROCEED = "proceed"
    ESCALATE_TO_MANAGER = "escalate_to_manager"
    LEGAL_REVIEW = "legal_review"
    HALT_DEAL = "halt_deal"


@dataclass
class DealContaminationInput:
    deal_id: str
    rep_id: str
    deal_name: str
    deal_value_usd: float
    customer_id: str
    conflict_of_interest_flag: int
    related_party_involvement: int
    former_employer_customer: int
    rep_personal_relationship_score: float
    approval_bypass_count: int
    unusual_discount_pct: float
    non_standard_terms_count: int
    compliance_review_completed: int
    legal_review_completed: int
    multiple_bid_waivers: int
    commission_split_disputes: int
    channel_conflict_flag: int
    competitive_employment_conflict: int
    gift_policy_violations_count: int
    data_handling_compliance_score: float
    revenue_recognition_risk_score: float
    audit_trail_completeness_score: float


@dataclass
class DealContaminationResult:
    deal_id: str
    deal_name: str
    contamination_level: ContaminationLevel
    contamination_risk: ContaminationRisk
    primary_contamination_type: ContaminationType
    contamination_action: ContaminationAction
    ethics_score: float
    compliance_score: float
    financial_integrity_score: float
    audit_quality_score: float
    contamination_composite: float
    requires_legal_review: bool
    requires_escalation: bool
    estimated_compliance_exposure_usd: float
    contamination_signal: str

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "deal_name": self.deal_name,
            "contamination_level": self.contamination_level.value,
            "contamination_risk": self.contamination_risk.value,
            "primary_contamination_type": self.primary_contamination_type.value,
            "contamination_action": self.contamination_action.value,
            "ethics_score": self.ethics_score,
            "compliance_score": self.compliance_score,
            "financial_integrity_score": self.financial_integrity_score,
            "audit_quality_score": self.audit_quality_score,
            "contamination_composite": self.contamination_composite,
            "requires_legal_review": self.requires_legal_review,
            "requires_escalation": self.requires_escalation,
            "estimated_compliance_exposure_usd": self.estimated_compliance_exposure_usd,
            "contamination_signal": self.contamination_signal,
        }


def _ethics_score(inp: DealContaminationInput) -> float:
    # Higher = more contaminated/risky
    score = 0.0
    if inp.conflict_of_interest_flag:
        score += 35.0
    if inp.related_party_involvement:
        score += 25.0
    if inp.former_employer_customer:
        score += 10.0
    # Personal relationship adds risk above threshold
    if inp.rep_personal_relationship_score >= 80:
        score += 20.0
    elif inp.rep_personal_relationship_score >= 60:
        score += 12.0
    elif inp.rep_personal_relationship_score >= 40:
        score += 5.0
    if inp.competitive_employment_conflict:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _compliance_score(inp: DealContaminationInput) -> float:
    # Higher = more contaminated
    score = 0.0
    if not inp.compliance_review_completed:
        score += 30.0
    if not inp.legal_review_completed and inp.deal_value_usd >= 100000:
        score += 25.0
    if inp.multiple_bid_waivers:
        score += 20.0
    # Data handling compliance (0-25): low compliance = high risk
    score += (100.0 - inp.data_handling_compliance_score) * 0.25
    return max(0.0, min(100.0, round(score, 1)))


def _financial_integrity_score(inp: DealContaminationInput) -> float:
    # Higher = more contaminated
    score = 0.0
    # Approval bypass
    if inp.approval_bypass_count >= 3:
        score += 30.0
    elif inp.approval_bypass_count >= 2:
        score += 20.0
    elif inp.approval_bypass_count >= 1:
        score += 10.0
    # Unusual discount
    if inp.unusual_discount_pct >= 30:
        score += 25.0
    elif inp.unusual_discount_pct >= 20:
        score += 15.0
    elif inp.unusual_discount_pct >= 10:
        score += 8.0
    # Non-standard terms
    if inp.non_standard_terms_count >= 5:
        score += 20.0
    elif inp.non_standard_terms_count >= 3:
        score += 12.0
    elif inp.non_standard_terms_count >= 1:
        score += 5.0
    # Revenue recognition risk
    score += inp.revenue_recognition_risk_score * 0.25
    # Commission disputes
    if inp.commission_split_disputes:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _audit_quality_score(inp: DealContaminationInput) -> float:
    # Higher = MORE contamination risk from poor audit trail
    base = (100.0 - inp.audit_trail_completeness_score)
    # Gift policy violations increase audit risk
    gift_penalty = min(25.0, inp.gift_policy_violations_count * 10.0)
    # Channel conflict also affects audit
    channel_penalty = 15.0 if inp.channel_conflict_flag else 0.0
    return max(0.0, min(100.0, round(base * 0.60 + gift_penalty + channel_penalty, 1)))


def _composite(ethics: float, compliance: float, financial: float, audit: float) -> float:
    # HIGHER composite = MORE contaminated
    raw = ethics * 0.30 + compliance * 0.30 + financial * 0.25 + audit * 0.15
    return round(raw, 1)


def _contamination_level(composite: float) -> ContaminationLevel:
    if composite < 15:
        return ContaminationLevel.CLEAN
    if composite < 35:
        return ContaminationLevel.ADVISORY
    if composite < 60:
        return ContaminationLevel.REVIEW_REQUIRED
    return ContaminationLevel.BLOCKED


def _contamination_risk(composite: float) -> ContaminationRisk:
    if composite >= 60:
        return ContaminationRisk.CRITICAL
    if composite >= 40:
        return ContaminationRisk.HIGH
    if composite >= 20:
        return ContaminationRisk.MODERATE
    return ContaminationRisk.LOW


def _primary_type(inp: DealContaminationInput, ethics: float, compliance: float,
                  financial: float) -> ContaminationType:
    if inp.conflict_of_interest_flag or inp.related_party_involvement:
        return ContaminationType.CONFLICT_OF_INTEREST
    if inp.channel_conflict_flag:
        return ContaminationType.CHANNEL_CONFLICT
    scores = {
        ContaminationType.CONFLICT_OF_INTEREST: ethics,
        ContaminationType.COMPLIANCE_GAP: compliance,
        ContaminationType.FINANCIAL_IRREGULARITY: financial,
    }
    best = max(scores, key=lambda k: scores[k])
    if scores[best] < 10:
        return ContaminationType.NONE
    return best


def _action(level: ContaminationLevel, requires_legal: bool) -> ContaminationAction:
    if level == ContaminationLevel.BLOCKED:
        return ContaminationAction.HALT_DEAL
    if level == ContaminationLevel.REVIEW_REQUIRED:
        if requires_legal:
            return ContaminationAction.LEGAL_REVIEW
        return ContaminationAction.ESCALATE_TO_MANAGER
    if level == ContaminationLevel.ADVISORY:
        return ContaminationAction.ESCALATE_TO_MANAGER
    return ContaminationAction.PROCEED


def _compliance_exposure_usd(inp: DealContaminationInput, composite: float) -> float:
    if composite < 15:
        return 0.0
    # Exposure scales with deal value and contamination level
    exposure_rate = composite / 100.0
    base = inp.deal_value_usd * exposure_rate * 0.5
    # Regulatory multiplier for data / privacy issues
    if inp.data_handling_compliance_score < 50:
        base *= 1.5
    return round(base, 2)


def _signal(inp: DealContaminationInput, c_type: ContaminationType, composite: float) -> str:
    if inp.conflict_of_interest_flag:
        return f"conflict of interest flag raised — deal requires ethics board review"
    if inp.related_party_involvement:
        return f"related party involvement detected — independent review mandatory"
    if inp.approval_bypass_count >= 2:
        return f"{inp.approval_bypass_count} approval steps bypassed — financial controls violated"
    if inp.unusual_discount_pct >= 25:
        return f"{inp.unusual_discount_pct:.0f}% discount above policy — revenue recognition risk"
    if not inp.compliance_review_completed:
        return f"compliance review not completed — deal cannot progress without it"
    if inp.channel_conflict_flag:
        return f"channel conflict detected — partner agreement may be violated"
    if inp.gift_policy_violations_count >= 2:
        return f"{inp.gift_policy_violations_count} gift policy violations — anti-bribery risk"
    if composite < 15:
        return f"deal clean — no contamination signals detected"
    return f"primary contamination type: {c_type.value.replace('_', ' ')}"


class DealContaminationRiskEngine:
    def __init__(self) -> None:
        self._results: dict[str, DealContaminationResult] = {}
        self._deal_values: dict[str, float] = {}

    def assess(self, inp: DealContaminationInput) -> DealContaminationResult:
        ethics = _ethics_score(inp)
        compliance = _compliance_score(inp)
        financial = _financial_integrity_score(inp)
        audit = _audit_quality_score(inp)
        composite = _composite(ethics, compliance, financial, audit)

        level = _contamination_level(composite)
        risk = _contamination_risk(composite)
        c_type = _primary_type(inp, ethics, compliance, financial)
        requires_legal = (
            inp.conflict_of_interest_flag == 1
            or inp.related_party_involvement == 1
            or (inp.deal_value_usd >= 250000 and composite >= 40)
        )
        requires_escalation = composite >= 20 or inp.approval_bypass_count >= 1
        action = _action(level, requires_legal)
        exposure = _compliance_exposure_usd(inp, composite)
        signal = _signal(inp, c_type, composite)

        result = DealContaminationResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            contamination_level=level,
            contamination_risk=risk,
            primary_contamination_type=c_type,
            contamination_action=action,
            ethics_score=ethics,
            compliance_score=compliance,
            financial_integrity_score=financial,
            audit_quality_score=audit,
            contamination_composite=composite,
            requires_legal_review=requires_legal,
            requires_escalation=requires_escalation,
            estimated_compliance_exposure_usd=exposure,
            contamination_signal=signal,
        )
        self._results[inp.deal_id] = result
        self._deal_values[inp.deal_id] = inp.deal_value_usd
        return result

    def assess_batch(self, inputs: List[DealContaminationInput]) -> List[DealContaminationResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.contamination_composite, reverse=True)
        return results

    def get(self, deal_id: str) -> DealContaminationResult | None:
        return self._results.get(deal_id)

    def all_deals(self) -> List[DealContaminationResult]:
        return sorted(self._results.values(), key=lambda r: r.contamination_composite, reverse=True)

    def flagged_deals(self) -> List[DealContaminationResult]:
        return [r for r in self._results.values() if r.contamination_level != ContaminationLevel.CLEAN]

    def by_level(self, level: ContaminationLevel) -> List[DealContaminationResult]:
        return [r for r in self._results.values() if r.contamination_level == level]

    def by_risk(self, risk: ContaminationRisk) -> List[DealContaminationResult]:
        return [r for r in self._results.values() if r.contamination_risk == risk]

    def total_compliance_exposure_usd(self) -> float:
        return round(sum(r.estimated_compliance_exposure_usd for r in self._results.values()), 2)

    def avg_contamination_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.contamination_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()
        self._deal_values.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        level_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        type_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            level_counts[r.contamination_level.value] = level_counts.get(r.contamination_level.value, 0) + 1
            risk_counts[r.contamination_risk.value] = risk_counts.get(r.contamination_risk.value, 0) + 1
            type_counts[r.primary_contamination_type.value] = type_counts.get(r.primary_contamination_type.value, 0) + 1
            action_counts[r.contamination_action.value] = action_counts.get(r.contamination_action.value, 0) + 1
        return {
            "total": n,
            "level_counts": level_counts,
            "risk_counts": risk_counts,
            "type_counts": type_counts,
            "action_counts": action_counts,
            "avg_contamination_composite": self.avg_contamination_composite(),
            "legal_review_required_count": sum(1 for r in results if r.requires_legal_review),
            "escalation_required_count": sum(1 for r in results if r.requires_escalation),
            "avg_ethics_score": round(sum(r.ethics_score for r in results) / n, 1) if n else 0.0,
            "avg_compliance_score": round(sum(r.compliance_score for r in results) / n, 1) if n else 0.0,
            "avg_financial_integrity_score": round(sum(r.financial_integrity_score for r in results) / n, 1) if n else 0.0,
            "avg_audit_quality_score": round(sum(r.audit_quality_score for r in results) / n, 1) if n else 0.0,
            "total_compliance_exposure_usd": self.total_compliance_exposure_usd(),
        }
