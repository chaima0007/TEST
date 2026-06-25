"""
Sales Stakeholder Mapping Intelligence Engine

Évalue la qualité du mapping des parties prenantes dans un deal B2B :
couverture des acheteurs, développement des champions, accès executive.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields
from enum import Enum
from typing import Optional


class StakeholderRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class StakeholderPattern(str, Enum):
    none = "none"
    single_threaded = "single_threaded"
    champion_missing = "champion_missing"
    executive_blind_spot = "executive_blind_spot"
    blocker_unmapped = "blocker_unmapped"
    buyer_committee_gap = "buyer_committee_gap"
    relationship_decay = "relationship_decay"


class StakeholderSeverity(str, Enum):
    engaged = "engaged"
    developing = "developing"
    fragile = "fragile"
    exposed = "exposed"


class StakeholderAction(str, Enum):
    maintain = "maintain"
    build_champion = "build_champion"
    executive_alignment = "executive_alignment"
    map_blockers = "map_blockers"
    expand_contacts = "expand_contacts"
    reactivate_relationships = "reactivate_relationships"


@dataclass
class StakeholderMappingInput:
    total_stakeholders_identified: int = 5
    stakeholders_actively_engaged: int = 3
    economic_buyers_identified: int = 1
    economic_buyers_engaged: int = 1
    champions_identified: int = 1
    champion_strength_score: float = 65.0
    blockers_identified: int = 1
    blockers_mapped: int = 0
    executive_contacts: int = 2
    executive_meetings_last_30d: int = 1
    technical_contacts: int = 2
    end_user_contacts: int = 1
    days_since_last_contact_avg: float = 12.0
    deal_value: float = 50000.0
    deal_stage: int = 3
    multi_threaded: bool = True
    buying_committee_size_estimate: int = 6
    stakeholder_sentiment_avg: float = 70.0
    internal_sponsor: bool = True
    procurement_contact: bool = False
    legal_contact: bool = False
    finance_contact: bool = False


@dataclass
class StakeholderMappingResult:
    composite_score: float
    risk: StakeholderRisk
    pattern: StakeholderPattern
    severity: StakeholderSeverity
    action: StakeholderAction
    coverage_breadth_score: float
    buyer_alignment_score: float
    champion_development_score: float
    executive_access_score: float
    has_stakeholder_gap: bool
    requires_stakeholder_coaching: bool
    estimated_deal_risk: float
    signal: str
    coverage_ratio: float
    champion_score: float

    def to_dict(self) -> dict:
        return {
            "composite_score": self.composite_score,
            "risk": self.risk.value,
            "pattern": self.pattern.value,
            "severity": self.severity.value,
            "action": self.action.value,
            "coverage_breadth_score": self.coverage_breadth_score,
            "buyer_alignment_score": self.buyer_alignment_score,
            "champion_development_score": self.champion_development_score,
            "executive_access_score": self.executive_access_score,
            "has_stakeholder_gap": self.has_stakeholder_gap,
            "requires_stakeholder_coaching": self.requires_stakeholder_coaching,
            "estimated_deal_risk": self.estimated_deal_risk,
            "signal": self.signal,
            "coverage_ratio": self.coverage_ratio,
            "champion_score": self.champion_score,
        }


class SalesStakeholderMappingIntelligenceEngine:

    def _coverage_breadth_score(self, inp: StakeholderMappingInput) -> float:
        if inp.buying_committee_size_estimate == 0:
            return 0.0
        coverage_ratio = inp.total_stakeholders_identified / inp.buying_committee_size_estimate
        engagement_ratio = inp.stakeholders_actively_engaged / max(inp.total_stakeholders_identified, 1)
        functional_coverage = sum([
            inp.technical_contacts > 0,
            inp.end_user_contacts > 0,
            inp.economic_buyers_identified > 0,
            inp.internal_sponsor,
        ]) / 4.0
        raw = (min(coverage_ratio, 1.0) * 40) + (engagement_ratio * 35) + (functional_coverage * 25)
        return min(max(round(raw, 1), 0.0), 100.0)

    def _buyer_alignment_score(self, inp: StakeholderMappingInput) -> float:
        buyer_coverage = inp.economic_buyers_engaged / max(inp.economic_buyers_identified, 1)
        blockers_ratio = inp.blockers_mapped / max(inp.blockers_identified, 1) if inp.blockers_identified > 0 else 1.0
        sentiment_score = inp.stakeholder_sentiment_avg
        raw = (buyer_coverage * 40) + (blockers_ratio * 30) + (sentiment_score * 0.30)
        return min(max(round(raw, 1), 0.0), 100.0)

    def _champion_development_score(self, inp: StakeholderMappingInput) -> float:
        champion_presence = min(inp.champions_identified, 1) * 40
        champion_strength = inp.champion_strength_score * 0.50
        multi_thread_bonus = 10 if inp.multi_threaded else 0
        raw = champion_presence + champion_strength + multi_thread_bonus
        return min(max(round(raw, 1), 0.0), 100.0)

    def _executive_access_score(self, inp: StakeholderMappingInput) -> float:
        exec_meetings = min(inp.executive_meetings_last_30d / max(inp.executive_contacts, 1), 1.0) * 50
        exec_contacts_score = min(inp.executive_contacts / 2.0, 1.0) * 30
        contact_freshness = max(0, 1 - inp.days_since_last_contact_avg / 30) * 20
        raw = exec_meetings + exec_contacts_score + contact_freshness
        return min(max(round(raw, 1), 0.0), 100.0)

    def _composite(self, c: float, b: float, ch: float, e: float) -> float:
        return min(round(c * 0.30 + b * 0.30 + ch * 0.25 + e * 0.15, 1), 100.0)

    def _risk_level(self, score: float) -> StakeholderRisk:
        if score >= 75:
            return StakeholderRisk.low
        if score >= 55:
            return StakeholderRisk.moderate
        if score >= 35:
            return StakeholderRisk.high
        return StakeholderRisk.critical

    def _severity(self, risk: StakeholderRisk) -> StakeholderSeverity:
        return {
            StakeholderRisk.low: StakeholderSeverity.engaged,
            StakeholderRisk.moderate: StakeholderSeverity.developing,
            StakeholderRisk.high: StakeholderSeverity.fragile,
            StakeholderRisk.critical: StakeholderSeverity.exposed,
        }[risk]

    def _detect_pattern(self, inp: StakeholderMappingInput, c: float, b: float, ch: float, e: float) -> StakeholderPattern:
        if not inp.multi_threaded and inp.total_stakeholders_identified <= 2:
            return StakeholderPattern.single_threaded
        if inp.champions_identified == 0 or inp.champion_strength_score < 40:
            return StakeholderPattern.champion_missing
        if inp.executive_contacts == 0 or inp.executive_meetings_last_30d == 0:
            return StakeholderPattern.executive_blind_spot
        if inp.blockers_identified > 0 and inp.blockers_mapped == 0:
            return StakeholderPattern.blocker_unmapped
        coverage = inp.total_stakeholders_identified / max(inp.buying_committee_size_estimate, 1)
        if coverage < 0.5:
            return StakeholderPattern.buyer_committee_gap
        if inp.days_since_last_contact_avg > 21:
            return StakeholderPattern.relationship_decay
        return StakeholderPattern.none

    def _action(self, pattern: StakeholderPattern) -> StakeholderAction:
        mapping = {
            StakeholderPattern.single_threaded: StakeholderAction.expand_contacts,
            StakeholderPattern.champion_missing: StakeholderAction.build_champion,
            StakeholderPattern.executive_blind_spot: StakeholderAction.executive_alignment,
            StakeholderPattern.blocker_unmapped: StakeholderAction.map_blockers,
            StakeholderPattern.buyer_committee_gap: StakeholderAction.expand_contacts,
            StakeholderPattern.relationship_decay: StakeholderAction.reactivate_relationships,
            StakeholderPattern.none: StakeholderAction.maintain,
        }
        return mapping[pattern]

    def _has_stakeholder_gap(self, inp: StakeholderMappingInput) -> bool:
        coverage = inp.total_stakeholders_identified / max(inp.buying_committee_size_estimate, 1)
        return coverage < 0.6 or not inp.multi_threaded or inp.champions_identified == 0

    def _requires_stakeholder_coaching(self, inp: StakeholderMappingInput) -> bool:
        return (inp.champion_strength_score < 50
                or inp.blockers_mapped < inp.blockers_identified
                or inp.days_since_last_contact_avg > 21)

    def _estimated_deal_risk(self, inp: StakeholderMappingInput, score: float) -> float:
        risk_factor = (100 - score) / 100
        stage_multiplier = 1.0 + (inp.deal_stage / 10)
        return round(inp.deal_value * risk_factor * stage_multiplier, 2)

    def _signal(self, risk: StakeholderRisk, pattern: StakeholderPattern) -> str:
        if risk == StakeholderRisk.low and pattern == StakeholderPattern.none:
            return "Stakeholder mapping healthy — coverage, buyer alignment, champion and executive access within benchmarks"
        signals = {
            StakeholderPattern.single_threaded: "Deal single-threaded — critical risk if primary contact leaves or disengages",
            StakeholderPattern.champion_missing: "No strong champion identified — deal lacks internal advocacy",
            StakeholderPattern.executive_blind_spot: "No executive access — deal may stall at approval stage",
            StakeholderPattern.blocker_unmapped: "Known blockers not yet mapped — unknown risk in buying committee",
            StakeholderPattern.buyer_committee_gap: "Buying committee coverage below 50% — key influencers unknown",
            StakeholderPattern.relationship_decay: "Average contact gap >21 days — relationship cooling detected",
            StakeholderPattern.none: f"Stakeholder mapping {risk.value} — expand coverage proactively",
        }
        return signals.get(pattern, "Stakeholder mapping requires attention")

    def assess(self, inp: StakeholderMappingInput) -> StakeholderMappingResult:
        c = self._coverage_breadth_score(inp)
        b = self._buyer_alignment_score(inp)
        ch = self._champion_development_score(inp)
        e = self._executive_access_score(inp)
        composite = self._composite(c, b, ch, e)
        risk = self._risk_level(composite)
        severity = self._severity(risk)
        pattern = self._detect_pattern(inp, c, b, ch, e)
        action = self._action(pattern)

        coverage_ratio = round(
            inp.total_stakeholders_identified / max(inp.buying_committee_size_estimate, 1), 2
        )

        return StakeholderMappingResult(
            composite_score=composite,
            risk=risk,
            pattern=pattern,
            severity=severity,
            action=action,
            coverage_breadth_score=c,
            buyer_alignment_score=b,
            champion_development_score=ch,
            executive_access_score=e,
            has_stakeholder_gap=self._has_stakeholder_gap(inp),
            requires_stakeholder_coaching=self._requires_stakeholder_coaching(inp),
            estimated_deal_risk=self._estimated_deal_risk(inp, composite),
            signal=self._signal(risk, pattern),
            coverage_ratio=coverage_ratio,
            champion_score=inp.champion_strength_score,
        )

    def batch(self, inputs: list[StakeholderMappingInput]) -> list[StakeholderMappingResult]:
        return [self.assess(inp) for inp in inputs]

    def summary(self, results: list[StakeholderMappingResult]) -> dict:
        if not results:
            return {}
        scores = [r.composite_score for r in results]
        return {
            "total_deals": len(results),
            "avg_composite_score": round(sum(scores) / len(scores), 1),
            "critical_count": sum(1 for r in results if r.risk == StakeholderRisk.critical),
            "high_risk_count": sum(1 for r in results if r.risk == StakeholderRisk.high),
            "coaching_required_count": sum(1 for r in results if r.requires_stakeholder_coaching),
            "stakeholder_gap_count": sum(1 for r in results if r.has_stakeholder_gap),
            "top_pattern": max(set(r.pattern.value for r in results), key=lambda p: sum(1 for r in results if r.pattern.value == p)),
            "total_deal_risk": round(sum(r.estimated_deal_risk for r in results), 2),
            "avg_champion_score": round(sum(r.champion_score for r in results) / len(results), 1),
            "min_score": min(scores),
            "max_score": max(scores),
            "low_risk_pct": round(sum(1 for r in results if r.risk == StakeholderRisk.low) / len(results) * 100, 1),
            "expand_contacts_count": sum(1 for r in results if r.action == StakeholderAction.expand_contacts),
        }
