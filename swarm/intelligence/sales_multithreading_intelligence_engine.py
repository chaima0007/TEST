from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class MultithreadRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MultithreadPattern(str, Enum):
    none                    = "none"
    single_threading        = "single_threading"
    champion_dependency     = "champion_dependency"
    executive_blind_spot    = "executive_blind_spot"
    stakeholder_map_gap     = "stakeholder_map_gap"
    relationship_stagnation = "relationship_stagnation"


class MultithreadSeverity(str, Enum):
    networked   = "networked"
    developing  = "developing"
    exposed     = "exposed"
    fragile     = "fragile"


class MultithreadAction(str, Enum):
    no_action                       = "no_action"
    multithread_coaching            = "multithread_coaching"
    champion_backup_strategy        = "champion_backup_strategy"
    executive_outreach_plan         = "executive_outreach_plan"
    stakeholder_mapping_session     = "stakeholder_mapping_session"
    relationship_expansion_sprint   = "relationship_expansion_sprint"


@dataclass
class MultithreadInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_active_deals: int
    avg_stakeholders_per_deal: float
    single_threaded_deals_pct: float
    executive_sponsor_engaged_pct: float
    champion_identified_pct: float
    economic_buyer_engaged_pct: float
    user_buyer_engaged_pct: float
    technical_buyer_engaged_pct: float
    avg_days_since_secondary_contact: float
    deals_with_decision_maker_pct: float
    deal_reviews_with_multi_contacts_pct: float
    avg_contacts_added_per_month: float
    internal_champion_strength_score: float
    champion_last_active_days_avg: float
    deals_at_risk_from_champion_loss_pct: float
    multi_site_deals_pct: float
    stakeholder_map_completion_pct: float
    referrals_from_existing_contacts_count: int
    avg_opportunity_value_usd: float


@dataclass
class MultithreadResult:
    rep_id: str
    region: str
    multithread_risk: MultithreadRisk
    multithread_pattern: MultithreadPattern
    multithread_severity: MultithreadSeverity
    recommended_action: MultithreadAction
    threading_breadth_score: float
    champion_dependency_score: float
    decision_maker_coverage_score: float
    relationship_map_score: float
    multithread_composite: float
    has_threading_gap: bool
    requires_multithread_coaching: bool
    estimated_at_risk_usd: float
    multithread_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "multithread_risk":                 self.multithread_risk.value,
            "multithread_pattern":              self.multithread_pattern.value,
            "multithread_severity":             self.multithread_severity.value,
            "recommended_action":               self.recommended_action.value,
            "threading_breadth_score":          self.threading_breadth_score,
            "champion_dependency_score":        self.champion_dependency_score,
            "decision_maker_coverage_score":    self.decision_maker_coverage_score,
            "relationship_map_score":           self.relationship_map_score,
            "multithread_composite":            self.multithread_composite,
            "has_threading_gap":                self.has_threading_gap,
            "requires_multithread_coaching":    self.requires_multithread_coaching,
            "estimated_at_risk_usd":            self.estimated_at_risk_usd,
            "multithread_signal":               self.multithread_signal,
        }


class SalesMultithreadingIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[MultithreadResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _threading_breadth_score(self, inp: MultithreadInput) -> float:
        score = 0.0

        if inp.single_threaded_deals_pct >= 0.70:
            score += 45.0
        elif inp.single_threaded_deals_pct >= 0.50:
            score += 25.0
        elif inp.single_threaded_deals_pct >= 0.30:
            score += 10.0

        if inp.avg_stakeholders_per_deal < 2.0:
            score += 30.0
        elif inp.avg_stakeholders_per_deal < 3.0:
            score += 15.0
        elif inp.avg_stakeholders_per_deal < 4.0:
            score += 5.0

        if inp.executive_sponsor_engaged_pct < 0.20:
            score += 25.0
        elif inp.executive_sponsor_engaged_pct < 0.40:
            score += 12.0

        return min(score, 100.0)

    def _champion_dependency_score(self, inp: MultithreadInput) -> float:
        score = 0.0

        if inp.champion_last_active_days_avg >= 21.0:
            score += 40.0
        elif inp.champion_last_active_days_avg >= 14.0:
            score += 22.0
        elif inp.champion_last_active_days_avg >= 7.0:
            score += 8.0

        if inp.deals_at_risk_from_champion_loss_pct >= 0.50:
            score += 35.0
        elif inp.deals_at_risk_from_champion_loss_pct >= 0.30:
            score += 18.0

        if inp.internal_champion_strength_score < 0.40:
            score += 25.0
        elif inp.internal_champion_strength_score < 0.60:
            score += 12.0

        return min(score, 100.0)

    def _decision_maker_coverage_score(self, inp: MultithreadInput) -> float:
        score = 0.0

        if inp.economic_buyer_engaged_pct < 0.30:
            score += 40.0
        elif inp.economic_buyer_engaged_pct < 0.50:
            score += 20.0
        elif inp.economic_buyer_engaged_pct < 0.70:
            score += 8.0

        if inp.deals_with_decision_maker_pct < 0.30:
            score += 35.0
        elif inp.deals_with_decision_maker_pct < 0.50:
            score += 18.0

        if inp.technical_buyer_engaged_pct < 0.20:
            score += 25.0
        elif inp.technical_buyer_engaged_pct < 0.40:
            score += 12.0

        return min(score, 100.0)

    def _relationship_map_score(self, inp: MultithreadInput) -> float:
        score = 0.0

        if inp.stakeholder_map_completion_pct < 0.25:
            score += 40.0
        elif inp.stakeholder_map_completion_pct < 0.50:
            score += 20.0
        elif inp.stakeholder_map_completion_pct < 0.75:
            score += 8.0

        if inp.avg_contacts_added_per_month < 1.0:
            score += 35.0
        elif inp.avg_contacts_added_per_month < 3.0:
            score += 18.0

        if inp.avg_days_since_secondary_contact >= 30.0:
            score += 25.0
        elif inp.avg_days_since_secondary_contact >= 14.0:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: MultithreadInput,
                          breadth: float, champion: float,
                          decision: float, relationship: float) -> MultithreadPattern:
        if breadth >= 35 and inp.single_threaded_deals_pct >= 0.50:
            return MultithreadPattern.single_threading

        if champion >= 35 and inp.deals_at_risk_from_champion_loss_pct >= 0.40:
            return MultithreadPattern.champion_dependency

        if decision >= 30 and inp.executive_sponsor_engaged_pct < 0.25:
            return MultithreadPattern.executive_blind_spot

        if relationship >= 30 and inp.stakeholder_map_completion_pct < 0.40:
            return MultithreadPattern.stakeholder_map_gap

        if relationship >= 20 and inp.avg_contacts_added_per_month < 1.5:
            return MultithreadPattern.relationship_stagnation

        return MultithreadPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> MultithreadRisk:
        if composite >= 60:
            return MultithreadRisk.critical
        if composite >= 40:
            return MultithreadRisk.high
        if composite >= 20:
            return MultithreadRisk.moderate
        return MultithreadRisk.low

    def _severity(self, composite: float) -> MultithreadSeverity:
        if composite >= 60:
            return MultithreadSeverity.fragile
        if composite >= 40:
            return MultithreadSeverity.exposed
        if composite >= 20:
            return MultithreadSeverity.developing
        return MultithreadSeverity.networked

    def _action(self, risk: MultithreadRisk,
                 pattern: MultithreadPattern) -> MultithreadAction:
        if risk == MultithreadRisk.critical:
            if pattern == MultithreadPattern.champion_dependency:
                return MultithreadAction.champion_backup_strategy
            if pattern == MultithreadPattern.executive_blind_spot:
                return MultithreadAction.executive_outreach_plan
            return MultithreadAction.multithread_coaching
        if risk == MultithreadRisk.high:
            if pattern == MultithreadPattern.stakeholder_map_gap:
                return MultithreadAction.stakeholder_mapping_session
            if pattern == MultithreadPattern.relationship_stagnation:
                return MultithreadAction.relationship_expansion_sprint
            return MultithreadAction.multithread_coaching
        if risk == MultithreadRisk.moderate:
            return MultithreadAction.multithread_coaching
        return MultithreadAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_threading_gap(self, composite: float,
                            inp: MultithreadInput) -> bool:
        return (
            composite >= 40
            or inp.single_threaded_deals_pct >= 0.60
            or inp.deals_at_risk_from_champion_loss_pct >= 0.50
        )

    def _requires_multithread_coaching(self, composite: float,
                                        inp: MultithreadInput) -> bool:
        return (
            composite >= 30
            or inp.avg_stakeholders_per_deal < 2.0
            or inp.economic_buyer_engaged_pct < 0.30
        )

    # ------------------------------------------------------------------
    # Revenue at risk
    # ------------------------------------------------------------------

    def _estimated_at_risk(self, inp: MultithreadInput,
                             composite: float) -> float:
        single_threaded = round(inp.total_active_deals * inp.single_threaded_deals_pct)
        return round(single_threaded * inp.avg_opportunity_value_usd * (composite / 100.0) * 0.20, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: MultithreadInput,
                 pattern: MultithreadPattern, composite: float) -> str:
        if pattern == MultithreadPattern.none and composite < 20:
            return "Stakeholder coverage healthy — multi-threading, champion strength, and executive access within benchmarks"
        parts: list[str] = []
        if inp.single_threaded_deals_pct < 1.0:
            parts.append(f"{inp.single_threaded_deals_pct*100:.0f}% single-threaded deals")
        if inp.executive_sponsor_engaged_pct < 1.0:
            parts.append(f"{inp.executive_sponsor_engaged_pct*100:.0f}% executive access")
        if inp.deals_at_risk_from_champion_loss_pct < 1.0:
            parts.append(f"{inp.deals_at_risk_from_champion_loss_pct*100:.0f}% at-risk from champion loss")
        label = pattern.value.replace("_", " ") if pattern != MultithreadPattern.none else "Threading risk"
        summary = " — ".join(parts) if parts else "stakeholder coverage declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: MultithreadInput) -> MultithreadResult:
        breadth      = round(self._threading_breadth_score(inp), 1)
        champion     = round(self._champion_dependency_score(inp), 1)
        decision     = round(self._decision_maker_coverage_score(inp), 1)
        relationship = round(self._relationship_map_score(inp), 1)

        composite = round(
            breadth * 0.30 + champion * 0.30 + decision * 0.25 + relationship * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, breadth, champion, decision, relationship)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_threading_gap(composite, inp)
        coach  = self._requires_multithread_coaching(composite, inp)
        impact = self._estimated_at_risk(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = MultithreadResult(
            rep_id=inp.rep_id,
            region=inp.region,
            multithread_risk=risk,
            multithread_pattern=pattern,
            multithread_severity=severity,
            recommended_action=action,
            threading_breadth_score=breadth,
            champion_dependency_score=champion,
            decision_maker_coverage_score=decision,
            relationship_map_score=relationship,
            multithread_composite=composite,
            has_threading_gap=gap,
            requires_multithread_coaching=coach,
            estimated_at_risk_usd=impact,
            multithread_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[MultithreadInput]) -> list[MultithreadResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_multithread_composite": 0.0,
                "threading_gap_count": 0,
                "coaching_count": 0,
                "avg_threading_breadth_score": 0.0,
                "avg_champion_dependency_score": 0.0,
                "avg_decision_maker_coverage_score": 0.0,
                "avg_relationship_map_score": 0.0,
                "total_estimated_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_br = total_ch = total_dec = total_rel = total_impact = 0.0

        for r in self._results:
            risk_counts[r.multithread_risk.value]       = risk_counts.get(r.multithread_risk.value, 0) + 1
            pattern_counts[r.multithread_pattern.value] = pattern_counts.get(r.multithread_pattern.value, 0) + 1
            severity_counts[r.multithread_severity.value] = severity_counts.get(r.multithread_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.multithread_composite
            total_br     += r.threading_breadth_score
            total_ch     += r.champion_dependency_score
            total_dec    += r.decision_maker_coverage_score
            total_rel    += r.relationship_map_score
            total_impact += r.estimated_at_risk_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_multithread_composite":                round(total_comp / n, 1),
            "threading_gap_count":                      sum(1 for r in self._results if r.has_threading_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_multithread_coaching),
            "avg_threading_breadth_score":              round(total_br / n, 1),
            "avg_champion_dependency_score":            round(total_ch / n, 1),
            "avg_decision_maker_coverage_score":        round(total_dec / n, 1),
            "avg_relationship_map_score":               round(total_rel / n, 1),
            "total_estimated_at_risk_usd":              round(total_impact, 2),
        }
