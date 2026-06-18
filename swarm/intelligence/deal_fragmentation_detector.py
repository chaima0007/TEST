from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FragmentationRisk(str, Enum):
    STABLE        = "stable"
    EARLY_SIGNAL  = "early_signal"
    AT_RISK       = "at_risk"
    FRAGMENTING   = "fragmenting"


class FragmentationPattern(str, Enum):
    HEALTHY       = "healthy"
    CHAMPION_LOSS = "champion_loss"
    ENGAGEMENT_DROP = "engagement_drop"
    SCOPE_SHRINK  = "scope_shrink"
    TIMELINE_SLIP = "timeline_slip"
    MULTI_SIGNAL  = "multi_signal"


class DealPrognosis(str, Enum):
    ON_TRACK    = "on_track"
    NEEDS_ATTENTION = "needs_attention"
    LIKELY_SLIP = "likely_slip"
    AT_RISK_LOST = "at_risk_lost"


class DealAction(str, Enum):
    MAINTAIN  = "maintain"
    RE_ENGAGE = "re_engage"
    RESCUE    = "rescue"
    ESCALATE  = "escalate"


@dataclass
class DealFragmentationInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    stage:                          str
    deal_value:                     float    # current deal value $
    initial_deal_value:             float    # value at deal creation $
    days_in_current_stage:          int      # how long stuck in current stage
    avg_days_per_stage_historical:  float    # historical avg days per stage for similar deals
    champion_last_active_days:      int      # days since champion last responded/engaged
    champion_title_changed:         int      # 1 if champion changed title (left role) recently
    decision_maker_changed:         int      # 1 if economic buyer changed
    stakeholder_count_current:      int      # number of engaged stakeholders now
    stakeholder_count_peak:         int      # maximum stakeholders ever engaged this deal
    meetings_last_30_days:          int      # meetings in last 30 days
    meetings_prev_30_days:          int      # meetings in prior 30-day period
    emails_unanswered:              int      # unanswered emails in thread
    last_meaningful_activity_days:  int      # days since any meaningful customer activity
    price_objection_count_recent:   int      # # price objections raised in last 30 days
    competitor_mentioned_count_recent: int   # times competitor mentioned in last 30 days
    stage_regression_count:         int      # times deal went backward in stage
    close_date_pushed_times:        int      # number of times close date was pushed out
    legal_review_started:           int      # 1 if legal/procurement review has started


@dataclass
class DealFragmentationResult:
    deal_id:                    str
    deal_name:                  str
    fragmentation_risk:         FragmentationRisk
    fragmentation_pattern:      FragmentationPattern
    deal_prognosis:             DealPrognosis
    recommended_action:         DealAction
    champion_risk_score:        float    # 0-100
    engagement_decay_score:     float    # 0-100
    scope_erosion_score:        float    # 0-100
    timeline_drift_score:       float    # 0-100
    fragmentation_composite_score: float # 0-100
    estimated_deal_at_risk:     float    # $ at risk from fragmentation
    recovery_probability:       float    # 0-100 probability of closing successfully
    is_fragmenting:             bool
    needs_immediate_intervention: bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                      self.deal_id,
            "deal_name":                    self.deal_name,
            "fragmentation_risk":           self.fragmentation_risk.value,
            "fragmentation_pattern":        self.fragmentation_pattern.value,
            "deal_prognosis":               self.deal_prognosis.value,
            "recommended_action":           self.recommended_action.value,
            "champion_risk_score":          self.champion_risk_score,
            "engagement_decay_score":       self.engagement_decay_score,
            "scope_erosion_score":          self.scope_erosion_score,
            "timeline_drift_score":         self.timeline_drift_score,
            "fragmentation_composite_score": self.fragmentation_composite_score,
            "estimated_deal_at_risk":       self.estimated_deal_at_risk,
            "recovery_probability":         self.recovery_probability,
            "is_fragmenting":               self.is_fragmenting,
            "needs_immediate_intervention": self.needs_immediate_intervention,
        }


class DealFragmentationDetector:
    def __init__(self) -> None:
        self._results: list[DealFragmentationResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: DealFragmentationInput) -> DealFragmentationResult:
        champ_risk    = self._champion_risk_score(inp)
        engage_decay  = self._engagement_decay_score(inp)
        scope_erosion = self._scope_erosion_score(inp)
        timeline_drift = self._timeline_drift_score(inp)
        composite     = self._fragmentation_composite(champ_risk, engage_decay, scope_erosion, timeline_drift)
        risk          = self._fragmentation_risk(composite)
        pattern       = self._fragmentation_pattern(champ_risk, engage_decay, scope_erosion, timeline_drift)
        prognosis     = self._deal_prognosis(inp, composite)
        recovery_prob = self._recovery_probability(inp, composite)
        at_risk       = inp.deal_value * (composite / 100.0)
        is_frag       = composite >= 55.0 or inp.stage_regression_count >= 2
        needs_interv  = composite >= 65.0 or (inp.champion_title_changed and inp.deal_value >= 100_000)
        action        = self._deal_action(risk, is_frag, needs_interv)

        result = DealFragmentationResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            fragmentation_risk=risk,
            fragmentation_pattern=pattern,
            deal_prognosis=prognosis,
            recommended_action=action,
            champion_risk_score=champ_risk,
            engagement_decay_score=engage_decay,
            scope_erosion_score=scope_erosion,
            timeline_drift_score=timeline_drift,
            fragmentation_composite_score=composite,
            estimated_deal_at_risk=round(at_risk, 2),
            recovery_probability=recovery_prob,
            is_fragmenting=is_frag,
            needs_immediate_intervention=needs_interv,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[DealFragmentationInput]
    ) -> list[DealFragmentationResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def fragmenting_deals(self) -> list[DealFragmentationResult]:
        return [r for r in self._results if r.is_fragmenting]

    @property
    def intervention_needed(self) -> list[DealFragmentationResult]:
        return [r for r in self._results if r.needs_immediate_intervention]

    @property
    def total_deal_at_risk(self) -> float:
        return round(sum(r.estimated_deal_at_risk for r in self._results), 2)

    @property
    def avg_recovery_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.recovery_probability for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _champion_risk_score(self, inp: DealFragmentationInput) -> float:
        score = 0.0
        # Days since champion engaged (up to 40)
        days = inp.champion_last_active_days
        if days >= 30:
            score += min(40.0, days * 0.8)
        elif days >= 14:
            score += days * 0.6
        # Champion title/role change (up to 35)
        if inp.champion_title_changed:
            score += 35.0
        # Decision maker change (up to 25)
        if inp.decision_maker_changed:
            score += 25.0
        return round(max(0.0, min(100.0, score)), 1)

    def _engagement_decay_score(self, inp: DealFragmentationInput) -> float:
        score = 0.0
        # Meeting drop: fewer meetings recently vs before (up to 35)
        if inp.meetings_prev_30_days > 0:
            meeting_drop = (inp.meetings_prev_30_days - inp.meetings_last_30_days) / inp.meetings_prev_30_days
            if meeting_drop > 0:
                score += min(35.0, meeting_drop * 50.0)
        elif inp.meetings_last_30_days == 0:
            score += 25.0  # no meetings at all
        # Unanswered emails (up to 30)
        score += min(30.0, inp.emails_unanswered * 6.0)
        # Last meaningful activity recency (up to 25)
        if inp.last_meaningful_activity_days >= 21:
            score += min(25.0, inp.last_meaningful_activity_days * 0.6)
        # Stakeholder dropout: fewer engaged than peak (up to 10)
        if inp.stakeholder_count_peak > 0:
            dropout_rate = (inp.stakeholder_count_peak - inp.stakeholder_count_current) / inp.stakeholder_count_peak
            score += min(10.0, dropout_rate * 20.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _scope_erosion_score(self, inp: DealFragmentationInput) -> float:
        score = 0.0
        # Deal value shrinkage vs initial (up to 50)
        if inp.initial_deal_value > 0:
            erosion_pct = (inp.initial_deal_value - inp.deal_value) / inp.initial_deal_value
            if erosion_pct > 0:
                score += min(50.0, erosion_pct * 100.0)
        # Recent price objections (up to 30)
        score += min(30.0, inp.price_objection_count_recent * 10.0)
        # Stage regression — went backward (up to 20)
        score += min(20.0, inp.stage_regression_count * 8.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _timeline_drift_score(self, inp: DealFragmentationInput) -> float:
        score = 0.0
        # Days stuck in current stage vs historical avg (up to 45)
        if inp.avg_days_per_stage_historical > 0:
            overage_ratio = inp.days_in_current_stage / inp.avg_days_per_stage_historical
            if overage_ratio > 1.0:
                score += min(45.0, (overage_ratio - 1.0) * 25.0)
        # Close date pushed (up to 35)
        score += min(35.0, inp.close_date_pushed_times * 12.0)
        # Competitor mentions signal stalling (up to 20)
        score += min(20.0, inp.competitor_mentioned_count_recent * 7.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _fragmentation_composite(
        self,
        champ: float,
        engage: float,
        scope: float,
        timeline: float,
    ) -> float:
        composite = champ * 0.30 + engage * 0.30 + scope * 0.20 + timeline * 0.20
        return round(max(0.0, min(100.0, composite)), 1)

    def _fragmentation_risk(self, composite: float) -> FragmentationRisk:
        if composite >= 65:
            return FragmentationRisk.FRAGMENTING
        if composite >= 45:
            return FragmentationRisk.AT_RISK
        if composite >= 25:
            return FragmentationRisk.EARLY_SIGNAL
        return FragmentationRisk.STABLE

    def _fragmentation_pattern(
        self,
        champ: float,
        engage: float,
        scope: float,
        timeline: float,
    ) -> FragmentationPattern:
        signals = sum([champ >= 50, engage >= 50, scope >= 40, timeline >= 50])
        if signals >= 2:
            return FragmentationPattern.MULTI_SIGNAL
        if champ >= 50:
            return FragmentationPattern.CHAMPION_LOSS
        if engage >= 50:
            return FragmentationPattern.ENGAGEMENT_DROP
        if scope >= 40:
            return FragmentationPattern.SCOPE_SHRINK
        if timeline >= 50:
            return FragmentationPattern.TIMELINE_SLIP
        return FragmentationPattern.HEALTHY

    def _deal_prognosis(self, inp: DealFragmentationInput, composite: float) -> DealPrognosis:
        if composite >= 65 or (inp.stage_regression_count >= 2 and composite >= 45):
            return DealPrognosis.AT_RISK_LOST
        if composite >= 45 or inp.close_date_pushed_times >= 3:
            return DealPrognosis.LIKELY_SLIP
        if composite >= 25 or inp.emails_unanswered >= 3:
            return DealPrognosis.NEEDS_ATTENTION
        return DealPrognosis.ON_TRACK

    def _recovery_probability(self, inp: DealFragmentationInput, composite: float) -> float:
        # Base probability from composite (inverse)
        base = max(0.0, 100.0 - composite)
        # Boost if legal/procurement review started (advanced stage signal)
        if inp.legal_review_started:
            base = min(100.0, base + 15.0)
        # Penalty for repeated close date pushes
        base -= inp.close_date_pushed_times * 8.0
        # Penalty for stage regression
        base -= inp.stage_regression_count * 12.0
        return round(max(0.0, min(100.0, base)), 1)

    def _deal_action(
        self,
        risk: FragmentationRisk,
        is_frag: bool,
        needs_interv: bool,
    ) -> DealAction:
        if needs_interv or risk == FragmentationRisk.FRAGMENTING:
            return DealAction.ESCALATE
        if is_frag or risk == FragmentationRisk.AT_RISK:
            return DealAction.RESCUE
        if risk == FragmentationRisk.EARLY_SIGNAL:
            return DealAction.RE_ENGAGE
        return DealAction.MAINTAIN

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                           0,
                "risk_counts":                     {},
                "pattern_counts":                  {},
                "prognosis_counts":                {},
                "action_counts":                   {},
                "avg_fragmentation_composite_score": 0.0,
                "total_estimated_deal_at_risk":    0.0,
                "fragmenting_count":               0,
                "intervention_needed_count":       0,
                "avg_champion_risk_score":         0.0,
                "avg_engagement_decay_score":      0.0,
                "avg_scope_erosion_score":         0.0,
                "avg_recovery_probability":        0.0,
            }

        risk_counts:      dict[str, int] = {}
        pattern_counts:   dict[str, int] = {}
        prognosis_counts: dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_comp  = 0.0
        total_champ = 0.0
        total_eng   = 0.0
        total_scope = 0.0
        total_rec   = 0.0

        for r in self._results:
            risk_counts[r.fragmentation_risk.value]     = risk_counts.get(r.fragmentation_risk.value, 0) + 1
            pattern_counts[r.fragmentation_pattern.value] = pattern_counts.get(r.fragmentation_pattern.value, 0) + 1
            prognosis_counts[r.deal_prognosis.value]    = prognosis_counts.get(r.deal_prognosis.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.fragmentation_composite_score
            total_champ += r.champion_risk_score
            total_eng   += r.engagement_decay_score
            total_scope += r.scope_erosion_score
            total_rec   += r.recovery_probability

        return {
            "total":                             n,
            "risk_counts":                       risk_counts,
            "pattern_counts":                    pattern_counts,
            "prognosis_counts":                  prognosis_counts,
            "action_counts":                     action_counts,
            "avg_fragmentation_composite_score": round(total_comp / n, 1),
            "total_estimated_deal_at_risk":      self.total_deal_at_risk,
            "fragmenting_count":                 len(self.fragmenting_deals),
            "intervention_needed_count":         len(self.intervention_needed),
            "avg_champion_risk_score":           round(total_champ / n, 1),
            "avg_engagement_decay_score":        round(total_eng / n, 1),
            "avg_scope_erosion_score":           round(total_scope / n, 1),
            "avg_recovery_probability":          round(total_rec / n, 1),
        }
