from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class MomentumRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MomentumPattern(str, Enum):
    none               = "none"
    stall_accumulator  = "stall_accumulator"
    slow_burn          = "slow_burn"
    late_stage_freeze  = "late_stage_freeze"
    contact_desert     = "contact_desert"
    forecast_drift     = "forecast_drift"


class MomentumSeverity(str, Enum):
    accelerating = "accelerating"
    steady       = "steady"
    decelerating = "decelerating"
    stalled      = "stalled"


class MomentumAction(str, Enum):
    no_action                  = "no_action"
    pipeline_review            = "pipeline_review"
    deal_acceleration_coaching = "deal_acceleration_coaching"
    stall_intervention         = "stall_intervention"
    contact_cadence_coaching   = "contact_cadence_coaching"
    pipeline_purge             = "pipeline_purge"
    executive_deal_rescue      = "executive_deal_rescue"


@dataclass
class MomentumInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    avg_days_in_stage:               float   # avg days per deal stage
    stage_progression_rate_pct:      float   # 0-1 deals progressing per week
    deal_velocity_score:             float   # 0-1 normalized pipeline velocity
    stalled_deal_pct:                float   # 0-1 deals not moved in 14+ days
    avg_time_to_close_days:          float   # days from create to close
    time_to_close_ratio:             float   # actual/benchmark (>1 = slower)
    engagement_recency_score:        float   # 0-1 recency of last contact
    next_step_completion_rate_pct:   float   # 0-1
    multi_touch_frequency:           float   # avg touches per deal per week
    deal_age_skew:                   float   # 0-1 proportion of old deals
    reopen_rate_pct:                 float   # 0-1 lost/stalled deals reopened
    forecast_category_movement_pct:  float   # 0-1 deals moving forecast fwd
    competitive_displacement_rate_pct: float # 0-1 wins from displacement
    decision_date_slip_rate_pct:     float   # 0-1 close dates that slipped
    avg_days_since_last_contact:     float   # avg days since last rep contact
    deal_expansion_rate_pct:         float   # 0-1 deals that grew in value
    lost_deal_recapture_pct:         float   # 0-1
    total_active_deals:              int
    avg_deal_value_usd:              float


@dataclass
class MomentumResult:
    rep_id:                       str
    region:                       str
    momentum_risk:                MomentumRisk
    momentum_pattern:             MomentumPattern
    momentum_severity:            MomentumSeverity
    recommended_action:           MomentumAction
    velocity_score:               float
    engagement_score:             float
    momentum_score:               float
    discipline_score:             float
    momentum_composite:           float
    has_momentum_gap:             bool
    requires_momentum_coaching:   bool
    estimated_stalled_pipeline_usd: float
    momentum_signal:              str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "momentum_risk":                    self.momentum_risk.value,
            "momentum_pattern":                 self.momentum_pattern.value,
            "momentum_severity":                self.momentum_severity.value,
            "recommended_action":               self.recommended_action.value,
            "velocity_score":                   self.velocity_score,
            "engagement_score":                 self.engagement_score,
            "momentum_score":                   self.momentum_score,
            "discipline_score":                 self.discipline_score,
            "momentum_composite":               self.momentum_composite,
            "has_momentum_gap":                 self.has_momentum_gap,
            "requires_momentum_coaching":       self.requires_momentum_coaching,
            "estimated_stalled_pipeline_usd":   self.estimated_stalled_pipeline_usd,
            "momentum_signal":                  self.momentum_signal,
        }


class SalesDealMomentumIntelligenceEngine:
    """Detects per-rep deal momentum decay — stall accumulators, slow burns, late-stage freezes."""

    def __init__(self) -> None:
        self._results: List[MomentumResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _velocity_score(self, inp: MomentumInput) -> float:
        s = 0.0
        if   inp.stalled_deal_pct          >= 0.50: s += 40
        elif inp.stalled_deal_pct          >= 0.30: s += 22
        elif inp.stalled_deal_pct          >= 0.15: s += 8
        if   inp.time_to_close_ratio       >= 1.60: s += 35
        elif inp.time_to_close_ratio       >= 1.30: s += 18
        elif inp.time_to_close_ratio       >= 1.10: s += 6
        if   inp.deal_velocity_score       <= 0.20: s += 25
        elif inp.deal_velocity_score       <= 0.40: s += 12
        return min(s, 100.0)

    def _engagement_score(self, inp: MomentumInput) -> float:
        s = 0.0
        if   inp.avg_days_since_last_contact >= 21: s += 40
        elif inp.avg_days_since_last_contact >= 14: s += 22
        elif inp.avg_days_since_last_contact >= 7:  s += 8
        if   inp.engagement_recency_score    <= 0.20: s += 35
        elif inp.engagement_recency_score    <= 0.40: s += 18
        if   inp.multi_touch_frequency       <= 0.50: s += 25
        elif inp.multi_touch_frequency       <= 1.00: s += 12
        return min(s, 100.0)

    def _momentum_score(self, inp: MomentumInput) -> float:
        s = 0.0
        if   inp.forecast_category_movement_pct <= 0.15: s += 40
        elif inp.forecast_category_movement_pct <= 0.30: s += 22
        elif inp.forecast_category_movement_pct <= 0.50: s += 8
        if   inp.decision_date_slip_rate_pct    >= 0.55: s += 35
        elif inp.decision_date_slip_rate_pct    >= 0.35: s += 18
        if   inp.deal_age_skew                  >= 0.60: s += 25
        elif inp.deal_age_skew                  >= 0.40: s += 12
        return min(s, 100.0)

    def _discipline_score(self, inp: MomentumInput) -> float:
        s = 0.0
        if   inp.next_step_completion_rate_pct  <= 0.30: s += 45
        elif inp.next_step_completion_rate_pct  <= 0.55: s += 25
        elif inp.next_step_completion_rate_pct  <= 0.75: s += 10
        if   inp.stage_progression_rate_pct     <= 0.10: s += 30
        elif inp.stage_progression_rate_pct     <= 0.20: s += 15
        if   inp.reopen_rate_pct                >= 0.30: s += 25
        elif inp.reopen_rate_pct                >= 0.15: s += 10
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, v: float, e: float, m: float, d: float) -> float:
        return min(round(v * 0.35 + e * 0.25 + m * 0.25 + d * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: MomentumInput) -> MomentumPattern:
        if inp.stalled_deal_pct >= 0.40 and inp.deal_age_skew >= 0.40:
            return MomentumPattern.stall_accumulator
        if inp.time_to_close_ratio >= 1.40 and inp.forecast_category_movement_pct <= 0.25:
            return MomentumPattern.slow_burn
        if inp.decision_date_slip_rate_pct >= 0.50 and inp.stage_progression_rate_pct <= 0.15:
            return MomentumPattern.late_stage_freeze
        if inp.avg_days_since_last_contact >= 14 and inp.engagement_recency_score <= 0.30:
            return MomentumPattern.contact_desert
        if inp.forecast_category_movement_pct <= 0.20 and inp.deal_velocity_score <= 0.30:
            return MomentumPattern.forecast_drift
        return MomentumPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> MomentumRisk:
        if   composite >= 60: return MomentumRisk.critical
        elif composite >= 40: return MomentumRisk.high
        elif composite >= 20: return MomentumRisk.moderate
        return MomentumRisk.low

    def _severity(self, composite: float) -> MomentumSeverity:
        if   composite >= 60: return MomentumSeverity.stalled
        elif composite >= 40: return MomentumSeverity.decelerating
        elif composite >= 20: return MomentumSeverity.steady
        return MomentumSeverity.accelerating

    def _action(self, risk: MomentumRisk, pattern: MomentumPattern) -> MomentumAction:
        if risk == MomentumRisk.critical:
            if pattern in (MomentumPattern.stall_accumulator, MomentumPattern.late_stage_freeze):
                return MomentumAction.executive_deal_rescue
            return MomentumAction.pipeline_purge
        if risk == MomentumRisk.high:
            if pattern == MomentumPattern.stall_accumulator:
                return MomentumAction.stall_intervention
            if pattern == MomentumPattern.contact_desert:
                return MomentumAction.contact_cadence_coaching
            if pattern == MomentumPattern.slow_burn:
                return MomentumAction.deal_acceleration_coaching
            if pattern == MomentumPattern.late_stage_freeze:
                return MomentumAction.stall_intervention
            if pattern == MomentumPattern.forecast_drift:
                return MomentumAction.deal_acceleration_coaching
            return MomentumAction.deal_acceleration_coaching
        if risk == MomentumRisk.moderate:
            return MomentumAction.pipeline_review
        return MomentumAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: MomentumInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.stalled_deal_pct             >= 0.25
            or inp.decision_date_slip_rate_pct  >= 0.40
        )

    def _requires_coaching(self, inp: MomentumInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.next_step_completion_rate_pct <= 0.55
            or inp.avg_days_since_last_contact   >= 10
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _stalled_pipeline(self, inp: MomentumInput, composite: float) -> float:
        stalled_deals = inp.total_active_deals * inp.stalled_deal_pct
        risk_mult = min(1.0, (composite / 100) * (1 + inp.deal_age_skew))
        return round(stalled_deals * inp.avg_deal_value_usd * risk_mult, 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        MomentumPattern.stall_accumulator:  "Stall accumulator",
        MomentumPattern.slow_burn:          "Slow burn",
        MomentumPattern.late_stage_freeze:  "Late-stage freeze",
        MomentumPattern.contact_desert:     "Contact desert",
        MomentumPattern.forecast_drift:     "Forecast drift",
    }

    def _signal(self, inp: MomentumInput, pattern: MomentumPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Deal momentum strong — velocity, engagement, forecast movement, "
                "and next-step discipline within benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        stall_pct = round(inp.stalled_deal_pct * 100)
        slip_pct  = round(inp.decision_date_slip_rate_pct * 100)
        contact_d = round(inp.avg_days_since_last_contact)
        comp_int  = round(composite)
        return (
            f"{label} — {stall_pct}% deals stalled — "
            f"{slip_pct}% close dates slipped — "
            f"{contact_d}d avg last contact — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: MomentumInput) -> MomentumResult:
        v  = self._velocity_score(inp)
        e  = self._engagement_score(inp)
        m  = self._momentum_score(inp)
        d  = self._discipline_score(inp)
        comp = self._composite(v, e, m, d)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = MomentumResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            momentum_risk               = risk,
            momentum_pattern            = pattern,
            momentum_severity           = severity,
            recommended_action          = action,
            velocity_score              = v,
            engagement_score            = e,
            momentum_score              = m,
            discipline_score            = d,
            momentum_composite          = comp,
            has_momentum_gap            = self._has_gap(inp, comp),
            requires_momentum_coaching  = self._requires_coaching(inp, comp),
            estimated_stalled_pipeline_usd = self._stalled_pipeline(inp, comp),
            momentum_signal             = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[MomentumInput]) -> List[MomentumResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_momentum_composite": 0.0,
                "momentum_gap_count": 0,
                "coaching_count": 0,
                "avg_velocity_score": 0.0,
                "avg_engagement_score": 0.0,
                "avg_momentum_score": 0.0,
                "avg_discipline_score": 0.0,
                "total_estimated_stalled_pipeline_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_v = total_e = total_m = total_d = total_sp = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.momentum_risk.value]       = risk_counts.get(res.momentum_risk.value, 0) + 1
            pattern_counts[res.momentum_pattern.value] = pattern_counts.get(res.momentum_pattern.value, 0) + 1
            severity_counts[res.momentum_severity.value] = severity_counts.get(res.momentum_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.momentum_composite
            total_v    += res.velocity_score
            total_e    += res.engagement_score
            total_m    += res.momentum_score
            total_d    += res.discipline_score
            total_sp   += res.estimated_stalled_pipeline_usd
            if res.has_momentum_gap:           gap_count      += 1
            if res.requires_momentum_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_momentum_composite":                   round(total_comp / n, 1),
            "momentum_gap_count":                       gap_count,
            "coaching_count":                           coaching_count,
            "avg_velocity_score":                       round(total_v / n, 1),
            "avg_engagement_score":                     round(total_e / n, 1),
            "avg_momentum_score":                       round(total_m / n, 1),
            "avg_discipline_score":                     round(total_d / n, 1),
            "total_estimated_stalled_pipeline_usd":     round(total_sp, 2),
        }
