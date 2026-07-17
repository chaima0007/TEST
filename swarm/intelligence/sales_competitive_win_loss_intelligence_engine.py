from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CompetitiveRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompetitivePattern(str, Enum):
    none                = "none"
    high_loss_rate      = "high_loss_rate"
    no_competitive_intel = "no_competitive_intel"
    price_driven_loss   = "price_driven_loss"
    feature_gap_loss    = "feature_gap_loss"
    icp_mismatch        = "icp_mismatch"


class CompetitiveSeverity(str, Enum):
    dominant    = "dominant"
    competitive = "competitive"
    challenged  = "challenged"
    losing      = "losing"


class CompetitiveAction(str, Enum):
    no_action                   = "no_action"
    competitive_training        = "competitive_training"
    deal_coaching               = "deal_coaching"
    value_positioning           = "value_positioning"
    product_feedback_escalation = "product_feedback_escalation"
    competitive_win_back        = "competitive_win_back"


@dataclass
class CompetitiveWinLossInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_competitive_deals: int
    competitive_wins: int
    competitive_losses: int
    competitive_ties: int
    deals_lost_on_price_competitive: int
    deals_lost_on_features_competitive: int
    deals_lost_on_relationship_competitive: int
    win_rate_vs_top_competitor_pct: float
    avg_deal_size_won_usd: float
    avg_deal_size_lost_usd: float
    competitive_intel_documented_count: int
    battle_card_used_count: int
    proof_of_concept_win_rate_pct: float
    multi_stakeholder_competitive_wins: int
    single_stakeholder_competitive_losses: int
    competitive_displacement_wins: int
    deals_displaced_by_competitor: int
    avg_competitive_cycle_days: float
    executive_involved_competitive_wins: int


@dataclass
class CompetitiveWinLossResult:
    rep_id: str
    region: str
    competitive_risk: CompetitiveRisk
    competitive_pattern: CompetitivePattern
    competitive_severity: CompetitiveSeverity
    recommended_action: CompetitiveAction
    win_rate_score: float
    competitive_intel_score: float
    deal_quality_score: float
    competitive_resilience_score: float
    competitive_effectiveness_composite: float
    is_competitive_threat: bool
    requires_competitive_coaching: bool
    estimated_revenue_at_risk_usd: float
    competitive_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                               self.rep_id,
            "region":                               self.region,
            "competitive_risk":                     self.competitive_risk.value,
            "competitive_pattern":                  self.competitive_pattern.value,
            "competitive_severity":                 self.competitive_severity.value,
            "recommended_action":                   self.recommended_action.value,
            "win_rate_score":                       self.win_rate_score,
            "competitive_intel_score":              self.competitive_intel_score,
            "deal_quality_score":                   self.deal_quality_score,
            "competitive_resilience_score":         self.competitive_resilience_score,
            "competitive_effectiveness_composite":  self.competitive_effectiveness_composite,
            "is_competitive_threat":                self.is_competitive_threat,
            "requires_competitive_coaching":        self.requires_competitive_coaching,
            "estimated_revenue_at_risk_usd":        self.estimated_revenue_at_risk_usd,
            "competitive_signal":                   self.competitive_signal,
        }


class SalesCompetitiveWinLossIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[CompetitiveWinLossResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _win_rate_score(self, inp: CompetitiveWinLossInput) -> float:
        score = 0.0
        total = max(inp.total_competitive_deals, 1)

        win_rate = inp.competitive_wins / total
        if win_rate < 0.25:
            score += 45.0
        elif win_rate < 0.40:
            score += 25.0
        elif win_rate < 0.55:
            score += 10.0

        loss_rate = inp.competitive_losses / total
        if loss_rate >= 0.60:
            score += 30.0
        elif loss_rate >= 0.45:
            score += 15.0
        elif loss_rate >= 0.30:
            score += 5.0

        if inp.win_rate_vs_top_competitor_pct < 0.20:
            score += 15.0
        elif inp.win_rate_vs_top_competitor_pct < 0.35:
            score += 7.0

        return min(score, 100.0)

    def _competitive_intel_score(self, inp: CompetitiveWinLossInput) -> float:
        score = 0.0
        total = max(inp.total_competitive_deals, 1)

        intel_rate = inp.competitive_intel_documented_count / total
        if intel_rate < 0.30:
            score += 40.0
        elif intel_rate < 0.50:
            score += 20.0
        elif intel_rate < 0.70:
            score += 8.0

        battle_rate = inp.battle_card_used_count / total
        if battle_rate < 0.20:
            score += 30.0
        elif battle_rate < 0.40:
            score += 15.0

        if inp.proof_of_concept_win_rate_pct < 0.30:
            score += 20.0
        elif inp.proof_of_concept_win_rate_pct < 0.50:
            score += 10.0

        return min(score, 100.0)

    def _deal_quality_score(self, inp: CompetitiveWinLossInput) -> float:
        score = 0.0
        total = max(inp.total_competitive_deals, 1)

        price_loss_rate = inp.deals_lost_on_price_competitive / total
        if price_loss_rate >= 0.40:
            score += 40.0
        elif price_loss_rate >= 0.25:
            score += 20.0
        elif price_loss_rate >= 0.10:
            score += 8.0

        feature_loss_rate = inp.deals_lost_on_features_competitive / total
        if feature_loss_rate >= 0.30:
            score += 30.0
        elif feature_loss_rate >= 0.15:
            score += 15.0

        losses = max(inp.competitive_losses, 1)
        single_loss_rate = inp.single_stakeholder_competitive_losses / losses
        if inp.competitive_losses > 0 and single_loss_rate >= 0.60:
            score += 20.0
        elif inp.competitive_losses > 0 and single_loss_rate >= 0.40:
            score += 10.0

        return min(score, 100.0)

    def _competitive_resilience_score(self, inp: CompetitiveWinLossInput) -> float:
        score = 0.0
        total = max(inp.total_competitive_deals, 1)

        displacement_net = inp.deals_displaced_by_competitor - inp.competitive_displacement_wins
        if displacement_net >= 3:
            score += 40.0
        elif displacement_net >= 1:
            score += 20.0

        displacement_rate = inp.deals_displaced_by_competitor / total
        if displacement_rate >= 0.20:
            score += 30.0
        elif displacement_rate >= 0.10:
            score += 15.0

        wins = max(inp.competitive_wins, 1)
        multi_win_rate = inp.multi_stakeholder_competitive_wins / wins
        if inp.competitive_wins > 0 and multi_win_rate < 0.30:
            score += 20.0
        elif inp.competitive_wins > 0 and multi_win_rate < 0.50:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: CompetitiveWinLossInput,
                         win_rate: float, intel: float,
                         deal_quality: float, resilience: float) -> CompetitivePattern:
        total = max(inp.total_competitive_deals, 1)
        loss_rate = inp.competitive_losses / total
        if win_rate >= 35 and loss_rate >= 0.50:
            return CompetitivePattern.high_loss_rate

        intel_rate = inp.competitive_intel_documented_count / total
        if intel >= 30 and intel_rate < 0.40:
            return CompetitivePattern.no_competitive_intel

        price_loss_rate = inp.deals_lost_on_price_competitive / total
        if deal_quality >= 30 and price_loss_rate >= 0.30:
            return CompetitivePattern.price_driven_loss

        feature_loss_rate = inp.deals_lost_on_features_competitive / total
        if deal_quality >= 25 and feature_loss_rate >= 0.20:
            return CompetitivePattern.feature_gap_loss

        displacement_net = inp.deals_displaced_by_competitor - inp.competitive_displacement_wins
        if resilience >= 25 and displacement_net >= 2:
            return CompetitivePattern.icp_mismatch

        return CompetitivePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> CompetitiveRisk:
        if composite >= 60:
            return CompetitiveRisk.critical
        if composite >= 40:
            return CompetitiveRisk.high
        if composite >= 20:
            return CompetitiveRisk.moderate
        return CompetitiveRisk.low

    def _severity(self, composite: float) -> CompetitiveSeverity:
        if composite >= 60:
            return CompetitiveSeverity.losing
        if composite >= 40:
            return CompetitiveSeverity.challenged
        if composite >= 20:
            return CompetitiveSeverity.competitive
        return CompetitiveSeverity.dominant

    def _action(self, risk: CompetitiveRisk,
                 pattern: CompetitivePattern) -> CompetitiveAction:
        if risk == CompetitiveRisk.critical:
            if pattern == CompetitivePattern.high_loss_rate:
                return CompetitiveAction.competitive_win_back
            if pattern == CompetitivePattern.no_competitive_intel:
                return CompetitiveAction.competitive_training
            return CompetitiveAction.deal_coaching
        if risk == CompetitiveRisk.high:
            if pattern == CompetitivePattern.price_driven_loss:
                return CompetitiveAction.value_positioning
            if pattern == CompetitivePattern.feature_gap_loss:
                return CompetitiveAction.product_feedback_escalation
            return CompetitiveAction.deal_coaching
        if risk == CompetitiveRisk.moderate:
            return CompetitiveAction.competitive_training
        return CompetitiveAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_competitive_threat(self, composite: float,
                                inp: CompetitiveWinLossInput) -> bool:
        total = max(inp.total_competitive_deals, 1)
        win_rate = inp.competitive_wins / total
        displacement_net = inp.deals_displaced_by_competitor - inp.competitive_displacement_wins
        return (
            composite >= 40
            or win_rate < 0.25
            or displacement_net >= 2
        )

    def _requires_competitive_coaching(self, composite: float,
                                        inp: CompetitiveWinLossInput) -> bool:
        total = max(inp.total_competitive_deals, 1)
        intel_rate = inp.competitive_intel_documented_count / total
        return (
            composite >= 30
            or intel_rate < 0.40
            or inp.proof_of_concept_win_rate_pct < 0.30
        )

    # ------------------------------------------------------------------
    # Revenue at risk
    # ------------------------------------------------------------------

    def _estimated_revenue_at_risk(self, inp: CompetitiveWinLossInput,
                                    composite: float) -> float:
        return round(
            inp.competitive_losses * inp.avg_deal_size_lost_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: CompetitiveWinLossInput,
                 pattern: CompetitivePattern, composite: float) -> str:
        if pattern == CompetitivePattern.none and composite < 20:
            return "Competitive win rates strong across all deal segments"
        parts: list[str] = []
        total = max(inp.total_competitive_deals, 1)
        win_rate = inp.competitive_wins / total
        if win_rate < 0.50:
            parts.append(f"{win_rate*100:.0f}% win rate")
        if inp.competitive_losses >= 1:
            parts.append(f"{inp.competitive_losses} competitive losses")
        if inp.deals_displaced_by_competitor >= 1:
            parts.append(f"{inp.deals_displaced_by_competitor} displaced by competitor")
        label = pattern.value.replace("_", " ") if pattern != CompetitivePattern.none else "Competitive risk"
        summary = " — ".join(parts) if parts else "competitive performance degrading"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: CompetitiveWinLossInput) -> CompetitiveWinLossResult:
        win_rate   = round(self._win_rate_score(inp), 1)
        intel      = round(self._competitive_intel_score(inp), 1)
        deal_qual  = round(self._deal_quality_score(inp), 1)
        resilience = round(self._competitive_resilience_score(inp), 1)

        composite = round(
            win_rate * 0.35 + intel * 0.25 + deal_qual * 0.20 + resilience * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, win_rate, intel, deal_qual, resilience)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        threat   = self._is_competitive_threat(composite, inp)
        coaching = self._requires_competitive_coaching(composite, inp)
        revenue  = self._estimated_revenue_at_risk(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = CompetitiveWinLossResult(
            rep_id=inp.rep_id,
            region=inp.region,
            competitive_risk=risk,
            competitive_pattern=pattern,
            competitive_severity=severity,
            recommended_action=action,
            win_rate_score=win_rate,
            competitive_intel_score=intel,
            deal_quality_score=deal_qual,
            competitive_resilience_score=resilience,
            competitive_effectiveness_composite=composite,
            is_competitive_threat=threat,
            requires_competitive_coaching=coaching,
            estimated_revenue_at_risk_usd=revenue,
            competitive_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[CompetitiveWinLossInput]) -> list[CompetitiveWinLossResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_competitive_effectiveness_composite": 0.0,
                "competitive_threat_count": 0,
                "competitive_coaching_count": 0,
                "avg_win_rate_score": 0.0,
                "avg_competitive_intel_score": 0.0,
                "avg_deal_quality_score": 0.0,
                "avg_competitive_resilience_score": 0.0,
                "total_estimated_revenue_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_wr = total_intel = total_dq = total_res = total_rev = 0.0

        for r in self._results:
            risk_counts[r.competitive_risk.value]       = risk_counts.get(r.competitive_risk.value, 0) + 1
            pattern_counts[r.competitive_pattern.value] = pattern_counts.get(r.competitive_pattern.value, 0) + 1
            severity_counts[r.competitive_severity.value] = severity_counts.get(r.competitive_severity.value, 0) + 1
            action_counts[r.recommended_action.value]     = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.competitive_effectiveness_composite
            total_wr    += r.win_rate_score
            total_intel += r.competitive_intel_score
            total_dq    += r.deal_quality_score
            total_res   += r.competitive_resilience_score
            total_rev   += r.estimated_revenue_at_risk_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_competitive_effectiveness_composite":  round(total_comp / n, 1),
            "competitive_threat_count":                 sum(1 for r in self._results if r.is_competitive_threat),
            "competitive_coaching_count":               sum(1 for r in self._results if r.requires_competitive_coaching),
            "avg_win_rate_score":                       round(total_wr / n, 1),
            "avg_competitive_intel_score":              round(total_intel / n, 1),
            "avg_deal_quality_score":                   round(total_dq / n, 1),
            "avg_competitive_resilience_score":         round(total_res / n, 1),
            "total_estimated_revenue_at_risk_usd":      round(total_rev, 2),
        }
