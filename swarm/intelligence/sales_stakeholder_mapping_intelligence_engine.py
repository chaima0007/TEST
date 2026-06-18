from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class StakeholderRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class StakeholderPattern(str, Enum):
    none                        = "none"
    single_threaded             = "single_threaded"
    no_economic_buyer           = "no_economic_buyer"
    champion_gap                = "champion_gap"
    executive_avoidance         = "executive_avoidance"
    poor_stakeholder_advancement = "poor_stakeholder_advancement"


class StakeholderSeverity(str, Enum):
    engaged    = "engaged"
    developing = "developing"
    fragile    = "fragile"
    exposed    = "exposed"


class StakeholderAction(str, Enum):
    no_action                = "no_action"
    multi_threading_coaching = "multi_threading_coaching"
    economic_buyer_strategy  = "economic_buyer_strategy"
    champion_development     = "champion_development"
    stakeholder_mapping_review = "stakeholder_mapping_review"
    executive_access_plan    = "executive_access_plan"


@dataclass
class StakeholderMappingInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_active_deals: int
    single_threaded_deals: int
    multi_threaded_deals: int
    avg_contacts_per_deal: float
    economic_buyer_identified_count: int
    economic_buyer_engaged_count: int
    champion_identified_count: int
    champion_active_count: int
    executive_sponsor_deals: int
    decision_maker_met_count: int
    avg_stakeholder_influence_score: float
    deals_with_legal_involved: int
    deals_with_procurement_involved: int
    committee_buying_deals: int
    multi_department_deals: int
    lost_deals_single_threaded: int
    deals_stalled_no_champion: int
    avg_deal_size_multi_stakeholder_usd: float
    avg_deal_size_single_stakeholder_usd: float


@dataclass
class StakeholderMappingResult:
    rep_id: str
    region: str
    stakeholder_risk: StakeholderRisk
    stakeholder_pattern: StakeholderPattern
    stakeholder_severity: StakeholderSeverity
    recommended_action: StakeholderAction
    coverage_breadth_score: float
    buyer_alignment_score: float
    champion_development_score: float
    executive_access_score: float
    stakeholder_effectiveness_composite: float
    has_stakeholder_gap: bool
    requires_stakeholder_coaching: bool
    estimated_deal_risk_usd: float
    stakeholder_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                               self.rep_id,
            "region":                               self.region,
            "stakeholder_risk":                     self.stakeholder_risk.value,
            "stakeholder_pattern":                  self.stakeholder_pattern.value,
            "stakeholder_severity":                 self.stakeholder_severity.value,
            "recommended_action":                   self.recommended_action.value,
            "coverage_breadth_score":               self.coverage_breadth_score,
            "buyer_alignment_score":                self.buyer_alignment_score,
            "champion_development_score":           self.champion_development_score,
            "executive_access_score":               self.executive_access_score,
            "stakeholder_effectiveness_composite":  self.stakeholder_effectiveness_composite,
            "has_stakeholder_gap":                  self.has_stakeholder_gap,
            "requires_stakeholder_coaching":        self.requires_stakeholder_coaching,
            "estimated_deal_risk_usd":              self.estimated_deal_risk_usd,
            "stakeholder_signal":                   self.stakeholder_signal,
        }


class SalesStakeholderMappingIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[StakeholderMappingResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _coverage_breadth_score(self, inp: StakeholderMappingInput) -> float:
        score = 0.0
        total = max(inp.total_active_deals, 1)

        single_rate = inp.single_threaded_deals / total
        if single_rate >= 0.60:
            score += 45.0
        elif single_rate >= 0.40:
            score += 25.0
        elif single_rate >= 0.20:
            score += 10.0

        if inp.avg_contacts_per_deal < 1.5:
            score += 30.0
        elif inp.avg_contacts_per_deal < 2.5:
            score += 15.0

        if inp.multi_threaded_deals == 0:
            score += 20.0
        elif inp.multi_threaded_deals < 3:
            score += 10.0

        return min(score, 100.0)

    def _buyer_alignment_score(self, inp: StakeholderMappingInput) -> float:
        score = 0.0
        total = max(inp.total_active_deals, 1)

        eb_rate = inp.economic_buyer_identified_count / total
        if eb_rate < 0.30:
            score += 40.0
        elif eb_rate < 0.50:
            score += 20.0
        elif eb_rate < 0.70:
            score += 8.0

        eb_identified = max(inp.economic_buyer_identified_count, 1)
        engaged_rate = inp.economic_buyer_engaged_count / eb_identified
        if inp.economic_buyer_identified_count > 0 and engaged_rate < 0.40:
            score += 30.0
        elif inp.economic_buyer_identified_count > 0 and engaged_rate < 0.60:
            score += 15.0

        dm_rate = inp.decision_maker_met_count / total
        if dm_rate < 0.30:
            score += 20.0
        elif dm_rate < 0.50:
            score += 10.0

        return min(score, 100.0)

    def _champion_development_score(self, inp: StakeholderMappingInput) -> float:
        score = 0.0
        total = max(inp.total_active_deals, 1)

        champ_rate = inp.champion_identified_count / total
        if champ_rate < 0.30:
            score += 40.0
        elif champ_rate < 0.50:
            score += 20.0
        elif champ_rate < 0.70:
            score += 8.0

        champ_identified = max(inp.champion_identified_count, 1)
        active_rate = inp.champion_active_count / champ_identified
        if inp.champion_identified_count > 0 and active_rate < 0.40:
            score += 30.0
        elif inp.champion_identified_count > 0 and active_rate < 0.60:
            score += 15.0

        if inp.deals_stalled_no_champion >= 3:
            score += 20.0
        elif inp.deals_stalled_no_champion >= 1:
            score += 10.0

        return min(score, 100.0)

    def _executive_access_score(self, inp: StakeholderMappingInput) -> float:
        score = 0.0
        total = max(inp.total_active_deals, 1)

        exec_rate = inp.executive_sponsor_deals / total
        if exec_rate < 0.10:
            score += 45.0
        elif exec_rate < 0.20:
            score += 25.0
        elif exec_rate < 0.35:
            score += 10.0

        if inp.avg_stakeholder_influence_score < 4.0:
            score += 30.0
        elif inp.avg_stakeholder_influence_score < 6.0:
            score += 15.0

        if inp.committee_buying_deals > 0 and inp.executive_sponsor_deals == 0:
            score += 20.0
        elif inp.committee_buying_deals > 0 and exec_rate < 0.20:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: StakeholderMappingInput,
                         coverage: float, buyer: float,
                         champion: float, executive: float) -> StakeholderPattern:
        total = max(inp.total_active_deals, 1)
        single_rate = inp.single_threaded_deals / total
        if coverage >= 35 and single_rate >= 0.50:
            return StakeholderPattern.single_threaded

        eb_rate = inp.economic_buyer_identified_count / total
        if buyer >= 30 and eb_rate < 0.40:
            return StakeholderPattern.no_economic_buyer

        champ_rate = inp.champion_identified_count / total
        if champion >= 30 and champ_rate < 0.40:
            return StakeholderPattern.champion_gap

        exec_rate = inp.executive_sponsor_deals / total
        if executive >= 30 and exec_rate < 0.15:
            return StakeholderPattern.executive_avoidance

        if buyer >= 25 and inp.avg_stakeholder_influence_score < 5.0:
            return StakeholderPattern.poor_stakeholder_advancement

        return StakeholderPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

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

    def _action(self, risk: StakeholderRisk,
                 pattern: StakeholderPattern) -> StakeholderAction:
        if risk == StakeholderRisk.critical:
            if pattern == StakeholderPattern.single_threaded:
                return StakeholderAction.multi_threading_coaching
            if pattern == StakeholderPattern.no_economic_buyer:
                return StakeholderAction.economic_buyer_strategy
            return StakeholderAction.stakeholder_mapping_review
        if risk == StakeholderRisk.high:
            if pattern == StakeholderPattern.champion_gap:
                return StakeholderAction.champion_development
            if pattern == StakeholderPattern.executive_avoidance:
                return StakeholderAction.executive_access_plan
            return StakeholderAction.multi_threading_coaching
        if risk == StakeholderRisk.moderate:
            return StakeholderAction.multi_threading_coaching
        return StakeholderAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_stakeholder_gap(self, composite: float,
                              inp: StakeholderMappingInput) -> bool:
        total = max(inp.total_active_deals, 1)
        single_rate = inp.single_threaded_deals / total
        return (
            composite >= 40
            or single_rate >= 0.50
            or inp.champion_identified_count == 0
        )

    def _requires_stakeholder_coaching(self, composite: float,
                                        inp: StakeholderMappingInput) -> bool:
        total = max(inp.total_active_deals, 1)
        eb_rate = inp.economic_buyer_identified_count / total
        return (
            composite >= 30
            or eb_rate < 0.40
            or inp.avg_contacts_per_deal < 2.0
        )

    # ------------------------------------------------------------------
    # Deal risk
    # ------------------------------------------------------------------

    def _estimated_deal_risk(self, inp: StakeholderMappingInput,
                              composite: float) -> float:
        return round(
            inp.single_threaded_deals * inp.avg_deal_size_single_stakeholder_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: StakeholderMappingInput,
                 pattern: StakeholderPattern, composite: float) -> str:
        if pattern == StakeholderPattern.none and composite < 20:
            return "Stakeholder engagement and multi-threading on track"
        parts: list[str] = []
        total = max(inp.total_active_deals, 1)
        if inp.single_threaded_deals >= 1:
            parts.append(f"{inp.single_threaded_deals} single-threaded deals")
        if inp.champion_identified_count < total:
            parts.append(f"{inp.champion_identified_count} champions identified")
        if inp.executive_sponsor_deals < total:
            parts.append(f"{inp.executive_sponsor_deals} exec sponsors engaged")
        label = pattern.value.replace("_", " ") if pattern != StakeholderPattern.none else "Stakeholder risk"
        summary = " — ".join(parts) if parts else "stakeholder engagement declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: StakeholderMappingInput) -> StakeholderMappingResult:
        coverage   = round(self._coverage_breadth_score(inp), 1)
        buyer      = round(self._buyer_alignment_score(inp), 1)
        champion   = round(self._champion_development_score(inp), 1)
        executive  = round(self._executive_access_score(inp), 1)

        composite = round(
            coverage * 0.30 + buyer * 0.30 + champion * 0.25 + executive * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, coverage, buyer, champion, executive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_stakeholder_gap(composite, inp)
        coaching = self._requires_stakeholder_coaching(composite, inp)
        deal_risk = self._estimated_deal_risk(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = StakeholderMappingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            stakeholder_risk=risk,
            stakeholder_pattern=pattern,
            stakeholder_severity=severity,
            recommended_action=action,
            coverage_breadth_score=coverage,
            buyer_alignment_score=buyer,
            champion_development_score=champion,
            executive_access_score=executive,
            stakeholder_effectiveness_composite=composite,
            has_stakeholder_gap=gap,
            requires_stakeholder_coaching=coaching,
            estimated_deal_risk_usd=deal_risk,
            stakeholder_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[StakeholderMappingInput]) -> list[StakeholderMappingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
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

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_cov = total_buy = total_champ = total_exec = total_risk = 0.0

        for r in self._results:
            risk_counts[r.stakeholder_risk.value]       = risk_counts.get(r.stakeholder_risk.value, 0) + 1
            pattern_counts[r.stakeholder_pattern.value] = pattern_counts.get(r.stakeholder_pattern.value, 0) + 1
            severity_counts[r.stakeholder_severity.value] = severity_counts.get(r.stakeholder_severity.value, 0) + 1
            action_counts[r.recommended_action.value]     = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.stakeholder_effectiveness_composite
            total_cov   += r.coverage_breadth_score
            total_buy   += r.buyer_alignment_score
            total_champ += r.champion_development_score
            total_exec  += r.executive_access_score
            total_risk  += r.estimated_deal_risk_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_stakeholder_effectiveness_composite":  round(total_comp / n, 1),
            "stakeholder_gap_count":                    sum(1 for r in self._results if r.has_stakeholder_gap),
            "stakeholder_coaching_count":               sum(1 for r in self._results if r.requires_stakeholder_coaching),
            "avg_coverage_breadth_score":               round(total_cov / n, 1),
            "avg_buyer_alignment_score":                round(total_buy / n, 1),
            "avg_champion_development_score":           round(total_champ / n, 1),
            "avg_executive_access_score":               round(total_exec / n, 1),
            "total_estimated_deal_risk_usd":            round(total_risk, 2),
        }
