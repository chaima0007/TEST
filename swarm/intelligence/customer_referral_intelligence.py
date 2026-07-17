from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class ReferralVelocity(str, Enum):
    ACCELERATING = "accelerating"
    STEADY = "steady"
    DECLINING = "declining"
    INACTIVE = "inactive"


class AdvocacyLevel(str, Enum):
    CHAMPION = "champion"
    PROMOTER = "promoter"
    PASSIVE = "passive"
    DETRACTOR = "detractor"


class ReferralRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ReferralAction(str, Enum):
    ACTIVATE_REFERRAL = "activate_referral"
    NURTURE_ADVOCATE = "nurture_advocate"
    RE_ENGAGE = "re_engage"
    CONVERT_DETRACTOR = "convert_detractor"


@dataclass
class CustomerReferralInput:
    customer_id: str
    customer_name: str
    rep_id: str
    contract_value_usd: float
    nps_score: float
    referrals_given_lifetime: int
    referrals_converted_to_deals: int
    referral_pipeline_value_usd: float
    case_study_agreed: int
    review_submitted: int
    speaking_event_participated: int
    product_feedback_sessions_completed: int
    community_posts_count: int
    champion_identified: int
    exec_relationship_strength: float
    account_tenure_days: int
    last_referral_days_ago: int
    referral_ask_count: int
    competitive_references_blocked: int
    customer_success_score: float
    renewal_probability_pct: float
    expansion_completed: int


@dataclass
class CustomerReferralResult:
    customer_id: str
    customer_name: str
    referral_velocity: ReferralVelocity
    advocacy_level: AdvocacyLevel
    referral_risk: ReferralRisk
    referral_action: ReferralAction
    advocacy_score: float
    relationship_depth_score: float
    referral_propensity_score: float
    advocacy_impact_score: float
    referral_composite: float
    estimated_referral_pipeline_usd: float
    is_active_referrer: bool
    needs_advocacy_activation: bool
    primary_advocacy_signal: str

    def to_dict(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "referral_velocity": self.referral_velocity.value,
            "advocacy_level": self.advocacy_level.value,
            "referral_risk": self.referral_risk.value,
            "referral_action": self.referral_action.value,
            "advocacy_score": self.advocacy_score,
            "relationship_depth_score": self.relationship_depth_score,
            "referral_propensity_score": self.referral_propensity_score,
            "advocacy_impact_score": self.advocacy_impact_score,
            "referral_composite": self.referral_composite,
            "estimated_referral_pipeline_usd": self.estimated_referral_pipeline_usd,
            "is_active_referrer": self.is_active_referrer,
            "needs_advocacy_activation": self.needs_advocacy_activation,
            "primary_advocacy_signal": self.primary_advocacy_signal,
        }


def _advocacy_score(inp: CustomerReferralInput) -> float:
    score = 0.0
    # NPS contribution (0-35)
    if inp.nps_score >= 70:
        score += 35.0
    elif inp.nps_score >= 50:
        score += 25.0
    elif inp.nps_score >= 20:
        score += 15.0
    elif inp.nps_score >= 0:
        score += 8.0
    elif inp.nps_score < -20:
        score -= 10.0
    # Case study (0-20)
    if inp.case_study_agreed:
        score += 20.0
    # Review submitted (0-15)
    if inp.review_submitted:
        score += 15.0
    # Speaking event (0-15)
    if inp.speaking_event_participated:
        score += 15.0
    # Product feedback (0-10)
    if inp.product_feedback_sessions_completed >= 3:
        score += 10.0
    elif inp.product_feedback_sessions_completed >= 1:
        score += 5.0
    # Community posts (0-5)
    if inp.community_posts_count >= 5:
        score += 5.0
    elif inp.community_posts_count >= 2:
        score += 3.0
    return max(0.0, min(100.0, round(score, 1)))


def _relationship_depth_score(inp: CustomerReferralInput) -> float:
    score = 0.0
    # Champion identified (0-30)
    if inp.champion_identified:
        score += 30.0
    # Exec relationship (0-30)
    score += inp.exec_relationship_strength * 0.30
    # Account tenure (0-20)
    if inp.account_tenure_days >= 730:
        score += 20.0
    elif inp.account_tenure_days >= 365:
        score += 14.0
    elif inp.account_tenure_days >= 180:
        score += 8.0
    elif inp.account_tenure_days >= 90:
        score += 4.0
    # Customer success score contribution (0-20)
    score += inp.customer_success_score * 0.20
    return max(0.0, min(100.0, round(score, 1)))


def _referral_propensity_score(inp: CustomerReferralInput) -> float:
    score = 0.0
    # Lifetime referrals given (0-30)
    if inp.referrals_given_lifetime >= 5:
        score += 30.0
    elif inp.referrals_given_lifetime >= 3:
        score += 22.0
    elif inp.referrals_given_lifetime >= 1:
        score += 12.0
    # Conversion rate (0-25)
    if inp.referrals_given_lifetime > 0:
        conv_rate = inp.referrals_converted_to_deals / inp.referrals_given_lifetime
    else:
        conv_rate = 0.0
    if conv_rate >= 0.5:
        score += 25.0
    elif conv_rate >= 0.3:
        score += 18.0
    elif conv_rate >= 0.1:
        score += 10.0
    # Renewal probability (0-20)
    if inp.renewal_probability_pct >= 90:
        score += 20.0
    elif inp.renewal_probability_pct >= 70:
        score += 14.0
    elif inp.renewal_probability_pct >= 50:
        score += 8.0
    # Expansion completed (0-15)
    if inp.expansion_completed:
        score += 15.0
    # Blocking competitors (0-10)
    if inp.competitive_references_blocked:
        score += 10.0
    # Recent ask without referral (penalty)
    if inp.referral_ask_count >= 3 and inp.referrals_given_lifetime == 0:
        score -= 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _advocacy_impact_score(inp: CustomerReferralInput) -> float:
    score = 0.0
    # Pipeline value from referrals (0-40)
    if inp.referral_pipeline_value_usd >= 500000:
        score += 40.0
    elif inp.referral_pipeline_value_usd >= 200000:
        score += 30.0
    elif inp.referral_pipeline_value_usd >= 100000:
        score += 22.0
    elif inp.referral_pipeline_value_usd >= 50000:
        score += 14.0
    elif inp.referral_pipeline_value_usd >= 10000:
        score += 7.0
    # Deal conversion value multiplier (0-30)
    if inp.referrals_converted_to_deals >= 3:
        score += 30.0
    elif inp.referrals_converted_to_deals >= 2:
        score += 20.0
    elif inp.referrals_converted_to_deals >= 1:
        score += 10.0
    # Contract value (large accounts have more influence) (0-15)
    if inp.contract_value_usd >= 500000:
        score += 15.0
    elif inp.contract_value_usd >= 200000:
        score += 10.0
    elif inp.contract_value_usd >= 100000:
        score += 6.0
    elif inp.contract_value_usd >= 50000:
        score += 3.0
    # Speaking event impact (0-15)
    if inp.speaking_event_participated:
        score += 15.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(advocacy: float, relationship: float, propensity: float, impact: float) -> float:
    raw = advocacy * 0.30 + relationship * 0.25 + propensity * 0.25 + impact * 0.20
    return round(raw, 1)


def _referral_velocity(inp: CustomerReferralInput) -> ReferralVelocity:
    if inp.referrals_given_lifetime == 0 or inp.last_referral_days_ago > 365:
        return ReferralVelocity.INACTIVE
    if inp.last_referral_days_ago > 180:
        return ReferralVelocity.DECLINING
    if inp.last_referral_days_ago <= 30 and inp.referrals_given_lifetime >= 2:
        return ReferralVelocity.ACCELERATING
    return ReferralVelocity.STEADY


def _advocacy_level(composite: float, inp: CustomerReferralInput) -> AdvocacyLevel:
    if inp.nps_score < 0 and composite < 30:
        return AdvocacyLevel.DETRACTOR
    if composite >= 75 and inp.nps_score >= 50:
        return AdvocacyLevel.CHAMPION
    if composite >= 55:
        return AdvocacyLevel.PROMOTER
    return AdvocacyLevel.PASSIVE


def _referral_risk(composite: float, inp: CustomerReferralInput) -> ReferralRisk:
    if inp.nps_score < -30 or composite < 25:
        return ReferralRisk.CRITICAL
    if inp.nps_score < 0 or composite < 40:
        return ReferralRisk.HIGH
    if composite < 60:
        return ReferralRisk.MODERATE
    return ReferralRisk.LOW


def _referral_action(level: AdvocacyLevel, composite: float, inp: CustomerReferralInput) -> ReferralAction:
    if level == AdvocacyLevel.DETRACTOR:
        return ReferralAction.CONVERT_DETRACTOR
    if level == AdvocacyLevel.PASSIVE or inp.last_referral_days_ago > 180:
        return ReferralAction.RE_ENGAGE
    if composite >= 70 and inp.referrals_given_lifetime >= 1:
        return ReferralAction.ACTIVATE_REFERRAL
    return ReferralAction.NURTURE_ADVOCATE


def _estimated_referral_pipeline(inp: CustomerReferralInput, composite: float) -> float:
    base = inp.contract_value_usd * 2.5
    if composite >= 75:
        return round(base * 0.60, 0)
    elif composite >= 55:
        return round(base * 0.35, 0)
    elif composite >= 40:
        return round(base * 0.15, 0)
    else:
        return round(base * 0.05, 0)


def _primary_advocacy_signal(inp: CustomerReferralInput, composite: float) -> str:
    if inp.nps_score < -20:
        return f"NPS {inp.nps_score} — detractor risk, prioritize recovery"
    if inp.speaking_event_participated and inp.case_study_agreed:
        return "speaker + case study — elite advocate, maximize referral program"
    if inp.referrals_given_lifetime >= 3:
        return f"{inp.referrals_given_lifetime} referrals given — {inp.referrals_converted_to_deals} converted to deals"
    if inp.case_study_agreed:
        return "case study agreed — activate for peer referrals"
    if inp.nps_score >= 70 and inp.referrals_given_lifetime == 0:
        return "NPS promoter never asked for referral — activate now"
    if inp.last_referral_days_ago > 180:
        return f"last referral {inp.last_referral_days_ago} days ago — re-engagement needed"
    if inp.renewal_probability_pct >= 90:
        return "high renewal confidence — strong referral candidate"
    return "standard advocacy nurture track"


class CustomerReferralIntelligence:
    def __init__(self) -> None:
        self._results: dict[str, CustomerReferralResult] = {}

    def analyze(self, inp: CustomerReferralInput) -> CustomerReferralResult:
        advocacy = _advocacy_score(inp)
        relationship = _relationship_depth_score(inp)
        propensity = _referral_propensity_score(inp)
        impact = _advocacy_impact_score(inp)
        composite = _composite(advocacy, relationship, propensity, impact)

        velocity = _referral_velocity(inp)
        level = _advocacy_level(composite, inp)
        risk = _referral_risk(composite, inp)
        action = _referral_action(level, composite, inp)
        est_pipeline = _estimated_referral_pipeline(inp, composite)
        signal = _primary_advocacy_signal(inp, composite)

        is_active_referrer = inp.referrals_given_lifetime >= 1 and inp.last_referral_days_ago <= 180
        needs_advocacy_activation = (
            composite >= 60 and inp.referrals_given_lifetime == 0 and inp.nps_score >= 30
        )

        result = CustomerReferralResult(
            customer_id=inp.customer_id,
            customer_name=inp.customer_name,
            referral_velocity=velocity,
            advocacy_level=level,
            referral_risk=risk,
            referral_action=action,
            advocacy_score=advocacy,
            relationship_depth_score=relationship,
            referral_propensity_score=propensity,
            advocacy_impact_score=impact,
            referral_composite=composite,
            estimated_referral_pipeline_usd=est_pipeline,
            is_active_referrer=is_active_referrer,
            needs_advocacy_activation=needs_advocacy_activation,
            primary_advocacy_signal=signal,
        )
        self._results[inp.customer_id] = result
        return result

    def analyze_batch(self, inputs: List[CustomerReferralInput]) -> List[CustomerReferralResult]:
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.referral_composite, reverse=True)
        return results

    def get(self, customer_id: str) -> CustomerReferralResult | None:
        return self._results.get(customer_id)

    def all_customers(self) -> List[CustomerReferralResult]:
        return sorted(self._results.values(), key=lambda r: r.referral_composite, reverse=True)

    def active_referrers(self) -> List[CustomerReferralResult]:
        return [r for r in self._results.values() if r.is_active_referrer]

    def activation_queue(self) -> List[CustomerReferralResult]:
        return [r for r in self._results.values() if r.needs_advocacy_activation]

    def by_velocity(self, velocity: ReferralVelocity) -> List[CustomerReferralResult]:
        return [r for r in self._results.values() if r.referral_velocity == velocity]

    def by_advocacy_level(self, level: AdvocacyLevel) -> List[CustomerReferralResult]:
        return [r for r in self._results.values() if r.advocacy_level == level]

    def avg_referral_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.referral_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        velocity_counts: dict[str, int] = {}
        advocacy_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            velocity_counts[r.referral_velocity.value] = velocity_counts.get(r.referral_velocity.value, 0) + 1
            advocacy_counts[r.advocacy_level.value] = advocacy_counts.get(r.advocacy_level.value, 0) + 1
            risk_counts[r.referral_risk.value] = risk_counts.get(r.referral_risk.value, 0) + 1
            action_counts[r.referral_action.value] = action_counts.get(r.referral_action.value, 0) + 1
        return {
            "total": n,
            "velocity_counts": velocity_counts,
            "advocacy_counts": advocacy_counts,
            "risk_counts": risk_counts,
            "action_counts": action_counts,
            "avg_referral_composite": self.avg_referral_composite(),
            "active_referrer_count": len(self.active_referrers()),
            "activation_needed_count": len(self.activation_queue()),
            "avg_advocacy_score": round(sum(r.advocacy_score for r in results) / n, 1) if n else 0.0,
            "avg_relationship_depth_score": round(sum(r.relationship_depth_score for r in results) / n, 1) if n else 0.0,
            "avg_referral_propensity_score": round(sum(r.referral_propensity_score for r in results) / n, 1) if n else 0.0,
            "avg_advocacy_impact_score": round(sum(r.advocacy_impact_score for r in results) / n, 1) if n else 0.0,
            "total_estimated_referral_pipeline_usd": round(sum(r.estimated_referral_pipeline_usd for r in results), 0) if n else 0.0,
        }
