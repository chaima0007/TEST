"""
Sales Stakeholder Mapping Intelligence Engine.

Évalue la cartographie des parties prenantes sur les deals d'un commercial
(couverture/multi-threading, alignement acheteur, développement de champions,
accès exécutif) et produit un score d'efficacité composite avec pattern,
sévérité, action, flags, risque sur deals et un signal lisible.

Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


# ===========================================================================
# Enums
# ===========================================================================

class StakeholderRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class StakeholderPattern(str, Enum):
    none = "none"
    single_threaded = "single_threaded"
    no_economic_buyer = "no_economic_buyer"
    champion_gap = "champion_gap"
    executive_avoidance = "executive_avoidance"
    poor_stakeholder_advancement = "poor_stakeholder_advancement"


class StakeholderSeverity(str, Enum):
    engaged = "engaged"
    developing = "developing"
    fragile = "fragile"
    exposed = "exposed"


class StakeholderAction(str, Enum):
    no_action = "no_action"
    multi_threading_coaching = "multi_threading_coaching"
    economic_buyer_strategy = "economic_buyer_strategy"
    champion_development = "champion_development"
    executive_access_plan = "executive_access_plan"
    stakeholder_mapping_review = "stakeholder_mapping_review"


# ===========================================================================
# Dataclasses
# ===========================================================================

@dataclass
class StakeholderMappingInput:
    rep_id: str = ""
    region: str = ""
    evaluation_period_id: str = ""
    total_active_deals: int = 0
    single_threaded_deals: int = 0
    multi_threaded_deals: int = 0
    avg_contacts_per_deal: float = 0.0
    economic_buyer_identified_count: int = 0
    economic_buyer_engaged_count: int = 0
    champion_identified_count: int = 0
    champion_active_count: int = 0
    executive_sponsor_deals: int = 0
    decision_maker_met_count: int = 0
    avg_stakeholder_influence_score: float = 0.0
    deals_with_legal_involved: int = 0
    deals_with_procurement_involved: int = 0
    committee_buying_deals: int = 0
    multi_department_deals: int = 0
    lost_deals_single_threaded: int = 0
    deals_stalled_no_champion: int = 0
    avg_deal_size_multi_stakeholder_usd: float = 0.0
    avg_deal_size_single_stakeholder_usd: float = 0.0


@dataclass
class StakeholderMappingResult:
    rep_id: str
    region: str
    coverage_breadth_score: float
    buyer_alignment_score: float
    champion_development_score: float
    executive_access_score: float
    stakeholder_effectiveness_composite: float
    stakeholder_risk: StakeholderRisk
    stakeholder_pattern: StakeholderPattern
    stakeholder_severity: StakeholderSeverity
    recommended_action: StakeholderAction
    has_stakeholder_gap: bool
    requires_stakeholder_coaching: bool
    estimated_deal_risk_usd: float
    stakeholder_signal: str
    evaluation_period_id: str = ""

    def to_dict(self) -> Dict:
        return {
            "rep_id": self.rep_id,
            "region": self.region,
            "stakeholder_risk": self.stakeholder_risk.value,
            "stakeholder_pattern": self.stakeholder_pattern.value,
            "stakeholder_severity": self.stakeholder_severity.value,
            "recommended_action": self.recommended_action.value,
            "coverage_breadth_score": self.coverage_breadth_score,
            "buyer_alignment_score": self.buyer_alignment_score,
            "champion_development_score": self.champion_development_score,
            "executive_access_score": self.executive_access_score,
            "stakeholder_effectiveness_composite": self.stakeholder_effectiveness_composite,
            "has_stakeholder_gap": self.has_stakeholder_gap,
            "requires_stakeholder_coaching": self.requires_stakeholder_coaching,
            "estimated_deal_risk_usd": self.estimated_deal_risk_usd,
            "stakeholder_signal": self.stakeholder_signal,
        }


# ===========================================================================
# Engine
# ===========================================================================

class SalesStakeholderMappingIntelligenceEngine:
    def __init__(self) -> None:
        self._results: List[StakeholderMappingResult] = []

    # ---- Sous-scores ------------------------------------------------------

    def _coverage_breadth_score(self, inp: StakeholderMappingInput) -> float:
        denom = max(inp.total_active_deals, 1)
        score = 0.0

        single_rate = inp.single_threaded_deals / denom
        if single_rate >= 0.60:
            score += 45
        elif single_rate >= 0.40:
            score += 25
        elif single_rate >= 0.20:
            score += 10

        if inp.avg_contacts_per_deal < 1.5:
            score += 30
        elif inp.avg_contacts_per_deal < 2.5:
            score += 15

        if inp.multi_threaded_deals == 0:
            score += 20
        elif inp.multi_threaded_deals < 3:
            score += 10

        return float(min(score, 100.0))

    def _buyer_alignment_score(self, inp: StakeholderMappingInput) -> float:
        denom = max(inp.total_active_deals, 1)
        score = 0.0

        eb_rate = inp.economic_buyer_identified_count / denom
        if eb_rate < 0.30:
            score += 40
        elif eb_rate < 0.50:
            score += 20
        elif eb_rate < 0.70:
            score += 8

        if inp.economic_buyer_identified_count > 0:
            engaged_rate = inp.economic_buyer_engaged_count / inp.economic_buyer_identified_count
            if engaged_rate < 0.40:
                score += 30
            elif engaged_rate < 0.60:
                score += 15

        dm_rate = inp.decision_maker_met_count / denom
        if dm_rate < 0.30:
            score += 20
        elif dm_rate < 0.50:
            score += 10

        return float(min(score, 100.0))

    def _champion_development_score(self, inp: StakeholderMappingInput) -> float:
        denom = max(inp.total_active_deals, 1)
        score = 0.0

        champ_rate = inp.champion_identified_count / denom
        if champ_rate < 0.30:
            score += 40
        elif champ_rate < 0.50:
            score += 20
        elif champ_rate < 0.70:
            score += 8

        if inp.champion_identified_count > 0:
            active_rate = inp.champion_active_count / inp.champion_identified_count
            if active_rate < 0.40:
                score += 30
            elif active_rate < 0.60:
                score += 15

        if inp.deals_stalled_no_champion >= 3:
            score += 20
        elif inp.deals_stalled_no_champion >= 1:
            score += 10

        return float(min(score, 100.0))

    def _executive_access_score(self, inp: StakeholderMappingInput) -> float:
        denom = max(inp.total_active_deals, 1)
        score = 0.0

        exec_rate = inp.executive_sponsor_deals / denom
        if exec_rate < 0.10:
            score += 45
        elif exec_rate < 0.20:
            score += 25
        elif exec_rate < 0.35:
            score += 10

        if inp.avg_stakeholder_influence_score < 4.0:
            score += 30
        elif inp.avg_stakeholder_influence_score < 6.0:
            score += 15

        if inp.committee_buying_deals > 0:
            if exec_rate == 0:
                score += 20
            elif exec_rate < 0.20:
                score += 10

        return float(min(score, 100.0))

    # ---- Composite, niveaux, pattern, action ------------------------------

    def _composite(self, coverage: float, buyer: float, champion: float, executive: float) -> float:
        weighted = coverage * 0.30 + buyer * 0.30 + champion * 0.25 + executive * 0.15
        return float(min(round(weighted, 1), 100.0))

    def _risk_level(self, composite: float) -> StakeholderRisk:
        if composite >= 60:
            return StakeholderRisk.critical
        if composite >= 40:
            return StakeholderRisk.high
        if composite >= 20:
            return StakeholderRisk.moderate
        return StakeholderRisk.low

    def _severity(self, composite: float) -> StakeholderSeverity:
        if composite >= 60:
            return StakeholderSeverity.exposed
        if composite >= 40:
            return StakeholderSeverity.fragile
        if composite >= 20:
            return StakeholderSeverity.developing
        return StakeholderSeverity.engaged

    def _detect_pattern(
        self,
        inp: StakeholderMappingInput,
        coverage: float,
        buyer: float,
        champion: float,
        executive: float,
    ) -> StakeholderPattern:
        denom = max(inp.total_active_deals, 1)
        single_rate = inp.single_threaded_deals / denom
        eb_rate = inp.economic_buyer_identified_count / denom
        champ_rate = inp.champion_identified_count / denom
        exec_rate = inp.executive_sponsor_deals / denom

        if coverage >= 35 and single_rate >= 0.50:
            return StakeholderPattern.single_threaded
        if buyer >= 30 and eb_rate < 0.40:
            return StakeholderPattern.no_economic_buyer
        if champion >= 30 and champ_rate < 0.40:
            return StakeholderPattern.champion_gap
        if executive >= 30 and exec_rate < 0.15:
            return StakeholderPattern.executive_avoidance
        if buyer >= 25 and inp.avg_stakeholder_influence_score < 5.0:
            return StakeholderPattern.poor_stakeholder_advancement
        return StakeholderPattern.none

    def _action(self, risk: StakeholderRisk, pattern: StakeholderPattern) -> StakeholderAction:
        if risk == StakeholderRisk.low:
            return StakeholderAction.no_action
        if risk == StakeholderRisk.moderate:
            return StakeholderAction.multi_threading_coaching
        if risk == StakeholderRisk.high:
            if pattern == StakeholderPattern.champion_gap:
                return StakeholderAction.champion_development
            if pattern == StakeholderPattern.executive_avoidance:
                return StakeholderAction.executive_access_plan
            return StakeholderAction.multi_threading_coaching
        # critical
        if pattern == StakeholderPattern.single_threaded:
            return StakeholderAction.multi_threading_coaching
        if pattern == StakeholderPattern.no_economic_buyer:
            return StakeholderAction.economic_buyer_strategy
        return StakeholderAction.stakeholder_mapping_review

    # ---- Flags, risque deals, signal --------------------------------------

    def _has_stakeholder_gap(self, composite: float, inp: StakeholderMappingInput) -> bool:
        if composite >= 40:
            return True
        denom = max(inp.total_active_deals, 1)
        if inp.single_threaded_deals / denom >= 0.50:
            return True
        if inp.champion_identified_count == 0:
            return True
        return False

    def _requires_stakeholder_coaching(self, composite: float, inp: StakeholderMappingInput) -> bool:
        if composite >= 30:
            return True
        denom = max(inp.total_active_deals, 1)
        if inp.economic_buyer_identified_count / denom < 0.40:
            return True
        if inp.avg_contacts_per_deal < 2.0:
            return True
        return False

    def _estimated_deal_risk(self, inp: StakeholderMappingInput, composite: float) -> float:
        return round(
            inp.single_threaded_deals * inp.avg_deal_size_single_stakeholder_usd * (composite / 100.0),
            2,
        )

    def _signal(self, inp: StakeholderMappingInput, pattern: StakeholderPattern, composite: float) -> str:
        if pattern == StakeholderPattern.none and composite < 20:
            return "Stakeholder engagement and multi-threading on track"

        parts: List[str] = []
        if inp.single_threaded_deals > 0:
            parts.append(f"{inp.single_threaded_deals} single-threaded deals")
        if inp.champion_identified_count < inp.total_active_deals:
            parts.append(f"{inp.champion_identified_count} champions identified")
        if inp.executive_sponsor_deals < inp.total_active_deals:
            parts.append(f"{inp.executive_sponsor_deals} exec sponsors engaged")

        if pattern == StakeholderPattern.none:
            prefix = "Stakeholder risk"
        else:
            prefix = pattern.value.replace("_", " ").capitalize()

        if not parts:
            parts.append("stakeholder engagement declining")

        return f"{prefix}: {'; '.join(parts)} (composite {composite:.0f})"

    # ---- Assess / batch / summary -----------------------------------------

    def assess(self, inp: StakeholderMappingInput) -> StakeholderMappingResult:
        coverage = self._coverage_breadth_score(inp)
        buyer = self._buyer_alignment_score(inp)
        champion = self._champion_development_score(inp)
        executive = self._executive_access_score(inp)
        composite = self._composite(coverage, buyer, champion, executive)
        risk = self._risk_level(composite)
        pattern = self._detect_pattern(inp, coverage, buyer, champion, executive)
        severity = self._severity(composite)
        action = self._action(risk, pattern)

        result = StakeholderMappingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            evaluation_period_id=inp.evaluation_period_id,
            coverage_breadth_score=coverage,
            buyer_alignment_score=buyer,
            champion_development_score=champion,
            executive_access_score=executive,
            stakeholder_effectiveness_composite=composite,
            stakeholder_risk=risk,
            stakeholder_pattern=pattern,
            stakeholder_severity=severity,
            recommended_action=action,
            has_stakeholder_gap=self._has_stakeholder_gap(composite, inp),
            requires_stakeholder_coaching=self._requires_stakeholder_coaching(composite, inp),
            estimated_deal_risk_usd=self._estimated_deal_risk(inp, composite),
            stakeholder_signal=self._signal(inp, pattern, composite),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[StakeholderMappingInput]) -> List[StakeholderMappingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_stakeholder_effectiveness_composite": 0.0,
                "stakeholder_gap_count": 0,
                "stakeholder_coaching_count": 0,
                "avg_coverage_breadth_score": 0.0,
                "avg_buyer_alignment_score": 0.0,
                "avg_champion_development_score": 0.0,
                "avg_executive_access_score": 0.0,
                "total_estimated_deal_risk_usd": 0.0,
            }

        def counts(attr: str) -> Dict[str, int]:
            out: Dict[str, int] = {}
            for r in self._results:
                key = getattr(r, attr).value
                out[key] = out.get(key, 0) + 1
            return out

        def avg(attr: str) -> float:
            return round(sum(getattr(r, attr) for r in self._results) / n, 1)

        return {
            "total": n,
            "risk_counts": counts("stakeholder_risk"),
            "pattern_counts": counts("stakeholder_pattern"),
            "severity_counts": counts("stakeholder_severity"),
            "action_counts": counts("recommended_action"),
            "avg_stakeholder_effectiveness_composite": avg("stakeholder_effectiveness_composite"),
            "stakeholder_gap_count": sum(1 for r in self._results if r.has_stakeholder_gap),
            "stakeholder_coaching_count": sum(1 for r in self._results if r.requires_stakeholder_coaching),
            "avg_coverage_breadth_score": avg("coverage_breadth_score"),
            "avg_buyer_alignment_score": avg("buyer_alignment_score"),
            "avg_champion_development_score": avg("champion_development_score"),
            "avg_executive_access_score": avg("executive_access_score"),
            "total_estimated_deal_risk_usd": round(
                sum(r.estimated_deal_risk_usd for r in self._results), 2
            ),
        }


# Alias de compatibilité
SalesStakeholderMappingIntelligenceEngine_v1 = SalesStakeholderMappingIntelligenceEngine
