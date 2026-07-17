from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class ThreadingStatus(str, Enum):
    SINGLE_THREADED = "single_threaded"
    AT_RISK = "at_risk"
    ADEQUATELY_THREADED = "adequately_threaded"
    WELL_THREADED = "well_threaded"


class ThreadingRisk(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


class StakeholderCoverage(str, Enum):
    POOR = "poor"
    PARTIAL = "partial"
    ADEQUATE = "adequate"
    COMPREHENSIVE = "comprehensive"


class ThreadingAction(str, Enum):
    EMERGENCY_EXECUTIVE_OUTREACH = "emergency_executive_outreach"
    EXPAND_STAKEHOLDER_MAP = "expand_stakeholder_map"
    STRENGTHEN_EXISTING = "strengthen_existing"
    MAINTAIN = "maintain"


@dataclass
class DealMultithreadingInput:
    deal_id: str
    rep_id: str
    deal_name: str
    stakeholder_count: int
    executive_contacts_count: int
    champion_confirmed: int
    economic_buyer_identified: int
    decision_maker_engaged: int
    technical_evaluator_engaged: int
    user_buyer_engaged: int
    last_exec_contact_days_ago: int
    contact_engagement_rate: float
    contacts_with_recent_activity: int
    deal_stage: int
    deal_value_usd: float
    days_in_current_stage: int
    stakeholder_sentiment_avg: float
    champion_risk_score: float
    org_change_signals: int
    single_threaded_days: int
    previous_multithreaded: int
    rep_multithreading_score: float


@dataclass
class DealMultithreadingResult:
    deal_id: str
    rep_id: str
    threading_status: ThreadingStatus
    threading_risk: ThreadingRisk
    stakeholder_coverage: StakeholderCoverage
    threading_action: ThreadingAction
    coverage_score: float
    engagement_score: float
    executive_access_score: float
    resilience_score: float
    threading_composite: float
    is_single_threaded: bool
    needs_executive_access: bool
    estimated_risk_exposure_usd: float
    primary_threading_gap: str

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "rep_id": self.rep_id,
            "threading_status": self.threading_status.value,
            "threading_risk": self.threading_risk.value,
            "stakeholder_coverage": self.stakeholder_coverage.value,
            "threading_action": self.threading_action.value,
            "coverage_score": self.coverage_score,
            "engagement_score": self.engagement_score,
            "executive_access_score": self.executive_access_score,
            "resilience_score": self.resilience_score,
            "threading_composite": self.threading_composite,
            "is_single_threaded": self.is_single_threaded,
            "needs_executive_access": self.needs_executive_access,
            "estimated_risk_exposure_usd": self.estimated_risk_exposure_usd,
            "primary_threading_gap": self.primary_threading_gap,
        }


def _coverage_score(inp: DealMultithreadingInput) -> float:
    score = 0.0
    # Stakeholder breadth (0-30)
    if inp.stakeholder_count >= 6:
        score += 30.0
    elif inp.stakeholder_count >= 4:
        score += 22.0
    elif inp.stakeholder_count >= 2:
        score += 12.0
    elif inp.stakeholder_count == 1:
        score += 3.0
    # Role coverage (0-40): champion, economic buyer, decision maker, technical, user
    if inp.champion_confirmed:
        score += 8.0
    if inp.economic_buyer_identified:
        score += 10.0
    if inp.decision_maker_engaged:
        score += 10.0
    if inp.technical_evaluator_engaged:
        score += 6.0
    if inp.user_buyer_engaged:
        score += 6.0
    # Executive presence (0-20)
    if inp.executive_contacts_count >= 3:
        score += 20.0
    elif inp.executive_contacts_count >= 2:
        score += 14.0
    elif inp.executive_contacts_count >= 1:
        score += 7.0
    # Rep multithreading skill bonus (0-10)
    score += inp.rep_multithreading_score * 0.10
    return max(0.0, min(100.0, round(score, 1)))


def _engagement_score(inp: DealMultithreadingInput) -> float:
    score = 0.0
    # Contact engagement rate (0-40)
    score += inp.contact_engagement_rate * 0.40
    # Recent activity contacts (0-30)
    if inp.contacts_with_recent_activity >= 4:
        score += 30.0
    elif inp.contacts_with_recent_activity >= 3:
        score += 22.0
    elif inp.contacts_with_recent_activity >= 2:
        score += 14.0
    elif inp.contacts_with_recent_activity == 1:
        score += 6.0
    # Stakeholder sentiment (0-20)
    score += inp.stakeholder_sentiment_avg * 0.20
    # Org change penalty
    if inp.org_change_signals:
        score -= 15.0
    # Long time in stage penalty
    if inp.days_in_current_stage >= 60:
        score -= 10.0
    elif inp.days_in_current_stage >= 30:
        score -= 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _executive_access_score(inp: DealMultithreadingInput) -> float:
    score = 0.0
    # Executive contacts (0-40)
    if inp.executive_contacts_count >= 3:
        score += 40.0
    elif inp.executive_contacts_count >= 2:
        score += 28.0
    elif inp.executive_contacts_count >= 1:
        score += 15.0
    # Recency of exec contact (0-30)
    if inp.last_exec_contact_days_ago <= 7:
        score += 30.0
    elif inp.last_exec_contact_days_ago <= 14:
        score += 22.0
    elif inp.last_exec_contact_days_ago <= 30:
        score += 14.0
    elif inp.last_exec_contact_days_ago <= 60:
        score += 6.0
    # Economic buyer and decision maker identified (0-30)
    if inp.economic_buyer_identified:
        score += 15.0
    if inp.decision_maker_engaged:
        score += 15.0
    return max(0.0, min(100.0, round(score, 1)))


def _resilience_score(inp: DealMultithreadingInput) -> float:
    score = 0.0
    # Champion strength (0-30)
    if inp.champion_confirmed:
        champion_health = max(0.0, 100.0 - inp.champion_risk_score)
        score += champion_health * 0.30
    # Previously multithreaded recovery (0-10)
    if inp.previous_multithreaded:
        score += 10.0
    # Single-threaded duration penalty (0-30 deducted)
    if inp.single_threaded_days >= 60:
        score -= 30.0
    elif inp.single_threaded_days >= 30:
        score -= 18.0
    elif inp.single_threaded_days >= 14:
        score -= 8.0
    # Stakeholder count base resilience (0-30)
    if inp.stakeholder_count >= 5:
        score += 30.0
    elif inp.stakeholder_count >= 3:
        score += 20.0
    elif inp.stakeholder_count >= 2:
        score += 10.0
    # Org change risk
    if inp.org_change_signals:
        score -= 20.0
    # Champion risk penalty
    if inp.champion_risk_score >= 70:
        score -= 15.0
    elif inp.champion_risk_score >= 50:
        score -= 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(coverage: float, engagement: float, exec_access: float, resilience: float) -> float:
    raw = coverage * 0.30 + engagement * 0.25 + exec_access * 0.25 + resilience * 0.20
    return round(raw, 1)


def _is_single_threaded(inp: DealMultithreadingInput) -> bool:
    return inp.stakeholder_count == 1 or (inp.contacts_with_recent_activity <= 1 and inp.deal_stage >= 1)


def _needs_executive_access(inp: DealMultithreadingInput) -> bool:
    return inp.executive_contacts_count == 0 and inp.deal_stage >= 1


def _threading_status(composite: float, inp: DealMultithreadingInput) -> ThreadingStatus:
    if _is_single_threaded(inp):
        return ThreadingStatus.SINGLE_THREADED
    if composite >= 70:
        return ThreadingStatus.WELL_THREADED
    if composite >= 50:
        return ThreadingStatus.ADEQUATELY_THREADED
    return ThreadingStatus.AT_RISK


def _threading_risk(composite: float, inp: DealMultithreadingInput) -> ThreadingRisk:
    if composite < 25 or (inp.deal_stage >= 2 and _is_single_threaded(inp)):
        return ThreadingRisk.CRITICAL
    if composite < 45:
        return ThreadingRisk.HIGH
    if composite < 65:
        return ThreadingRisk.MODERATE
    return ThreadingRisk.LOW


def _stakeholder_coverage(inp: DealMultithreadingInput) -> StakeholderCoverage:
    roles_covered = sum([
        inp.champion_confirmed, inp.economic_buyer_identified,
        inp.decision_maker_engaged, inp.technical_evaluator_engaged, inp.user_buyer_engaged,
    ])
    if roles_covered >= 4 and inp.stakeholder_count >= 4:
        return StakeholderCoverage.COMPREHENSIVE
    if roles_covered >= 3 and inp.stakeholder_count >= 3:
        return StakeholderCoverage.ADEQUATE
    if roles_covered >= 2 or inp.stakeholder_count >= 2:
        return StakeholderCoverage.PARTIAL
    return StakeholderCoverage.POOR


def _threading_action(risk: ThreadingRisk, inp: DealMultithreadingInput) -> ThreadingAction:
    if risk == ThreadingRisk.CRITICAL:
        return ThreadingAction.EMERGENCY_EXECUTIVE_OUTREACH
    if risk == ThreadingRisk.HIGH:
        return ThreadingAction.EXPAND_STAKEHOLDER_MAP
    if risk == ThreadingRisk.MODERATE:
        return ThreadingAction.STRENGTHEN_EXISTING
    return ThreadingAction.MAINTAIN


def _estimated_risk_exposure_usd(inp: DealMultithreadingInput, composite: float) -> float:
    risk_factor = max(0.0, (100.0 - composite) / 100.0)
    return round(inp.deal_value_usd * risk_factor, 2)


def _primary_threading_gap(inp: DealMultithreadingInput, coverage: float,
                            engagement: float, exec_access: float, resilience: float) -> str:
    if inp.executive_contacts_count == 0 and inp.deal_stage >= 1:
        return "no executive sponsor — critical blind spot at current stage"
    if inp.economic_buyer_identified == 0:
        return "economic buyer not identified — procurement decision at risk"
    if inp.champion_confirmed == 0:
        return "no confirmed champion — deal lacks internal advocate"
    if inp.org_change_signals:
        return "org restructuring signals detected — key contact stability at risk"
    if inp.contacts_with_recent_activity <= 1 and inp.stakeholder_count >= 3:
        return "stakeholder engagement collapsed — re-activate dormant contacts"
    scores = {
        "stakeholder coverage": coverage,
        "contact engagement": engagement,
        "executive access": exec_access,
        "deal resilience": resilience,
    }
    weakest = min(scores, key=lambda k: scores[k])
    return f"weakest dimension: {weakest}"


class DealMultithreadingIntelligence:
    def __init__(self) -> None:
        self._results: dict[str, DealMultithreadingResult] = {}

    def assess(self, inp: DealMultithreadingInput) -> DealMultithreadingResult:
        coverage = _coverage_score(inp)
        engagement = _engagement_score(inp)
        exec_access = _executive_access_score(inp)
        resilience = _resilience_score(inp)
        composite = _composite(coverage, engagement, exec_access, resilience)

        is_single = _is_single_threaded(inp)
        needs_exec = _needs_executive_access(inp)
        risk = _threading_risk(composite, inp)
        status = _threading_status(composite, inp)
        coverage_level = _stakeholder_coverage(inp)
        action = _threading_action(risk, inp)
        exposure = _estimated_risk_exposure_usd(inp, composite)
        gap = _primary_threading_gap(inp, coverage, engagement, exec_access, resilience)

        result = DealMultithreadingResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            threading_status=status,
            threading_risk=risk,
            stakeholder_coverage=coverage_level,
            threading_action=action,
            coverage_score=coverage,
            engagement_score=engagement,
            executive_access_score=exec_access,
            resilience_score=resilience,
            threading_composite=composite,
            is_single_threaded=is_single,
            needs_executive_access=needs_exec,
            estimated_risk_exposure_usd=exposure,
            primary_threading_gap=gap,
        )
        self._results[inp.deal_id] = result
        return result

    def assess_batch(self, inputs: List[DealMultithreadingInput]) -> List[DealMultithreadingResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.threading_composite, reverse=True)
        return results

    def get(self, deal_id: str) -> DealMultithreadingResult | None:
        return self._results.get(deal_id)

    def all_deals(self) -> List[DealMultithreadingResult]:
        return sorted(self._results.values(), key=lambda r: r.threading_composite, reverse=True)

    def single_threaded_deals(self) -> List[DealMultithreadingResult]:
        return [r for r in self._results.values() if r.is_single_threaded]

    def executive_access_needed(self) -> List[DealMultithreadingResult]:
        return [r for r in self._results.values() if r.needs_executive_access]

    def by_status(self, status: ThreadingStatus) -> List[DealMultithreadingResult]:
        return [r for r in self._results.values() if r.threading_status == status]

    def by_risk(self, risk: ThreadingRisk) -> List[DealMultithreadingResult]:
        return [r for r in self._results.values() if r.threading_risk == risk]

    def avg_threading_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.threading_composite for r in self._results.values()) / len(self._results), 1)

    def total_at_risk_pipeline(self) -> float:
        return round(sum(r.estimated_risk_exposure_usd for r in self._results.values()), 2)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        status_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        coverage_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            status_counts[r.threading_status.value] = status_counts.get(r.threading_status.value, 0) + 1
            risk_counts[r.threading_risk.value] = risk_counts.get(r.threading_risk.value, 0) + 1
            coverage_counts[r.stakeholder_coverage.value] = coverage_counts.get(r.stakeholder_coverage.value, 0) + 1
            action_counts[r.threading_action.value] = action_counts.get(r.threading_action.value, 0) + 1
        return {
            "total": n,
            "threading_status_counts": status_counts,
            "risk_counts": risk_counts,
            "coverage_counts": coverage_counts,
            "action_counts": action_counts,
            "avg_threading_composite": self.avg_threading_composite(),
            "single_threaded_count": len(self.single_threaded_deals()),
            "executive_access_needed_count": len(self.executive_access_needed()),
            "avg_coverage_score": round(sum(r.coverage_score for r in results) / n, 1) if n else 0.0,
            "avg_engagement_score": round(sum(r.engagement_score for r in results) / n, 1) if n else 0.0,
            "avg_executive_access_score": round(sum(r.executive_access_score for r in results) / n, 1) if n else 0.0,
            "avg_resilience_score": round(sum(r.resilience_score for r in results) / n, 1) if n else 0.0,
            "total_at_risk_pipeline_usd": self.total_at_risk_pipeline(),
        }
