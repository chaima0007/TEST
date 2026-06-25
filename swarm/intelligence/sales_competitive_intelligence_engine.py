from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class CompRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompPattern(str, Enum):
    none                    = "none"
    price_surrender         = "price_surrender"
    feature_gap_concession  = "feature_gap_concession"
    late_entry_loss         = "late_entry_loss"
    relationship_deficit    = "relationship_deficit"
    multi_vendor_spread     = "multi_vendor_spread"


class CompSeverity(str, Enum):
    dominant    = "dominant"
    competitive = "competitive"
    challenged  = "challenged"
    losing      = "losing"


class CompAction(str, Enum):
    no_action                   = "no_action"
    competitive_monitoring      = "competitive_monitoring"
    battle_card_coaching        = "battle_card_coaching"
    value_differentiation_coaching = "value_differentiation_coaching"
    competitive_escalation      = "competitive_escalation"
    win_loss_review             = "win_loss_review"
    competitive_strategy_reset  = "competitive_strategy_reset"


@dataclass
class CompInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    win_rate_vs_competitor_pct:     float   # 0-1
    competitive_deal_pct:           float   # 0-1 (deals with named competitor)
    avg_discount_in_comp_deals_pct: float   # 0-1
    price_objection_rate_pct:       float   # 0-1
    feature_gap_mention_rate_pct:   float   # 0-1
    battle_card_usage_rate_pct:     float   # 0-1
    late_stage_competitive_loss_pct: float  # 0-1
    displacement_win_rate_pct:      float   # 0-1
    proof_of_concept_win_rate_pct:  float   # 0-1
    avg_cycle_len_comp_deals_days:  float   # days
    multi_vendor_eval_pct:          float   # 0-1
    executive_alignment_pct:        float   # 0-1
    competitor_mention_per_call:    float   # count
    differentiation_score:          float   # 0-1 (rep self/mgr rated)
    reference_customer_usage_rate:  float   # 0-1
    total_competitive_deals:        int
    avg_deal_value_usd:             float
    total_pipeline_at_risk_usd:     float


@dataclass
class CompResult:
    rep_id:                         str
    region:                         str
    comp_risk:                      CompRisk
    comp_pattern:                   CompPattern
    comp_severity:                  CompSeverity
    recommended_action:             CompAction
    win_rate_score:                 float
    positioning_score:              float
    battle_readiness_score:         float
    relationship_advantage_score:   float
    comp_composite:                 float
    has_comp_gap:                   bool
    requires_comp_coaching:         bool
    estimated_pipeline_at_risk_usd: float
    comp_signal:                    str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "comp_risk":                        self.comp_risk.value,
            "comp_pattern":                     self.comp_pattern.value,
            "comp_severity":                    self.comp_severity.value,
            "recommended_action":               self.recommended_action.value,
            "win_rate_score":                   self.win_rate_score,
            "positioning_score":                self.positioning_score,
            "battle_readiness_score":           self.battle_readiness_score,
            "relationship_advantage_score":     self.relationship_advantage_score,
            "comp_composite":                   self.comp_composite,
            "has_comp_gap":                     self.has_comp_gap,
            "requires_comp_coaching":           self.requires_comp_coaching,
            "estimated_pipeline_at_risk_usd":   self.estimated_pipeline_at_risk_usd,
            "comp_signal":                      self.comp_signal,
        }


class SalesCompetitiveIntelligenceEngine:
    """Detects per-rep competitive blind spots — price surrender, feature-gap concession, late-entry losses."""

    def __init__(self) -> None:
        self._results: List[CompResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _win_rate_score(self, inp: CompInput) -> float:
        s = 0.0
        if   inp.win_rate_vs_competitor_pct  <= 0.30: s += 45
        elif inp.win_rate_vs_competitor_pct  <= 0.50: s += 25
        elif inp.win_rate_vs_competitor_pct  <= 0.65: s += 10
        if   inp.displacement_win_rate_pct   <= 0.20: s += 30
        elif inp.displacement_win_rate_pct   <= 0.40: s += 15
        if   inp.late_stage_competitive_loss_pct >= 0.40: s += 25
        elif inp.late_stage_competitive_loss_pct >= 0.25: s += 12
        return min(s, 100.0)

    def _positioning_score(self, inp: CompInput) -> float:
        s = 0.0
        if   inp.avg_discount_in_comp_deals_pct >= 0.30: s += 40
        elif inp.avg_discount_in_comp_deals_pct >= 0.20: s += 22
        elif inp.avg_discount_in_comp_deals_pct >= 0.12: s += 8
        if   inp.feature_gap_mention_rate_pct   >= 0.50: s += 35
        elif inp.feature_gap_mention_rate_pct   >= 0.30: s += 18
        if   inp.differentiation_score           <= 0.35: s += 25
        elif inp.differentiation_score           <= 0.60: s += 12
        return min(s, 100.0)

    def _battle_readiness_score(self, inp: CompInput) -> float:
        s = 0.0
        if   inp.battle_card_usage_rate_pct     <= 0.25: s += 40
        elif inp.battle_card_usage_rate_pct     <= 0.55: s += 22
        elif inp.battle_card_usage_rate_pct     <= 0.75: s += 8
        if   inp.proof_of_concept_win_rate_pct  <= 0.35: s += 35
        elif inp.proof_of_concept_win_rate_pct  <= 0.55: s += 18
        if   inp.reference_customer_usage_rate  <= 0.20: s += 25
        elif inp.reference_customer_usage_rate  <= 0.45: s += 12
        return min(s, 100.0)

    def _relationship_advantage_score(self, inp: CompInput) -> float:
        s = 0.0
        if   inp.executive_alignment_pct    <= 0.25: s += 45
        elif inp.executive_alignment_pct    <= 0.50: s += 25
        elif inp.executive_alignment_pct    <= 0.70: s += 10
        if   inp.multi_vendor_eval_pct      >= 0.60: s += 30
        elif inp.multi_vendor_eval_pct      >= 0.40: s += 15
        if   inp.competitor_mention_per_call >= 3.0: s += 25
        elif inp.competitor_mention_per_call >= 1.5: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, wr: float, po: float, br: float, ra: float) -> float:
        return min(round(wr * 0.35 + po * 0.25 + br * 0.25 + ra * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: CompInput) -> CompPattern:
        if inp.avg_discount_in_comp_deals_pct >= 0.25 and inp.win_rate_vs_competitor_pct <= 0.40:
            return CompPattern.price_surrender
        if inp.feature_gap_mention_rate_pct >= 0.45 and inp.differentiation_score <= 0.40:
            return CompPattern.feature_gap_concession
        if inp.late_stage_competitive_loss_pct >= 0.35 and inp.competitive_deal_pct >= 0.50:
            return CompPattern.late_entry_loss
        if inp.executive_alignment_pct <= 0.25 and inp.multi_vendor_eval_pct >= 0.50:
            return CompPattern.relationship_deficit
        if inp.multi_vendor_eval_pct >= 0.65 and inp.displacement_win_rate_pct <= 0.25:
            return CompPattern.multi_vendor_spread
        return CompPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> CompRisk:
        if   composite >= 60: return CompRisk.critical
        elif composite >= 40: return CompRisk.high
        elif composite >= 20: return CompRisk.moderate
        return CompRisk.low

    def _severity(self, composite: float) -> CompSeverity:
        if   composite >= 60: return CompSeverity.losing
        elif composite >= 40: return CompSeverity.challenged
        elif composite >= 20: return CompSeverity.competitive
        return CompSeverity.dominant

    def _action(self, risk: CompRisk, pattern: CompPattern) -> CompAction:
        if risk == CompRisk.critical:
            if pattern in (CompPattern.price_surrender, CompPattern.feature_gap_concession):
                return CompAction.competitive_strategy_reset
            return CompAction.win_loss_review
        if risk == CompRisk.high:
            if pattern == CompPattern.price_surrender:
                return CompAction.value_differentiation_coaching
            if pattern == CompPattern.feature_gap_concession:
                return CompAction.battle_card_coaching
            if pattern == CompPattern.late_entry_loss:
                return CompAction.competitive_escalation
            if pattern == CompPattern.relationship_deficit:
                return CompAction.competitive_escalation
            if pattern == CompPattern.multi_vendor_spread:
                return CompAction.battle_card_coaching
            return CompAction.battle_card_coaching
        if risk == CompRisk.moderate:
            return CompAction.competitive_monitoring
        return CompAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: CompInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.win_rate_vs_competitor_pct    <= 0.45
            or inp.late_stage_competitive_loss_pct >= 0.30
        )

    def _requires_coaching(self, inp: CompInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.battle_card_usage_rate_pct    <= 0.45
            or inp.differentiation_score         <= 0.50
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _pipeline_at_risk(self, inp: CompInput, composite: float) -> float:
        loss_prob = min(1.0, (1 - inp.win_rate_vs_competitor_pct) * (composite / 100))
        return round(inp.total_pipeline_at_risk_usd * loss_prob, 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        CompPattern.price_surrender:        "Price surrender",
        CompPattern.feature_gap_concession: "Feature-gap concession",
        CompPattern.late_entry_loss:        "Late-entry loss",
        CompPattern.relationship_deficit:   "Relationship deficit",
        CompPattern.multi_vendor_spread:    "Multi-vendor spread",
    }

    def _signal(self, inp: CompInput, pattern: CompPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Competitive position strong — win rate, positioning, "
                "battle readiness, and executive alignment within benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        wr_pct   = round(inp.win_rate_vs_competitor_pct * 100)
        disc_pct = round(inp.avg_discount_in_comp_deals_pct * 100)
        late_pct = round(inp.late_stage_competitive_loss_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {wr_pct}% competitive win rate — "
            f"{disc_pct}% avg discount in comp deals — "
            f"{late_pct}% late-stage losses — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: CompInput) -> CompResult:
        wr  = self._win_rate_score(inp)
        po  = self._positioning_score(inp)
        br  = self._battle_readiness_score(inp)
        ra  = self._relationship_advantage_score(inp)
        comp = self._composite(wr, po, br, ra)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = CompResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            comp_risk                       = risk,
            comp_pattern                    = pattern,
            comp_severity                   = severity,
            recommended_action              = action,
            win_rate_score                  = wr,
            positioning_score               = po,
            battle_readiness_score          = br,
            relationship_advantage_score    = ra,
            comp_composite                  = comp,
            has_comp_gap                    = self._has_gap(inp, comp),
            requires_comp_coaching          = self._requires_coaching(inp, comp),
            estimated_pipeline_at_risk_usd  = self._pipeline_at_risk(inp, comp),
            comp_signal                     = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[CompInput]) -> List[CompResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_comp_composite": 0.0,
                "comp_gap_count": 0,
                "coaching_count": 0,
                "avg_win_rate_score": 0.0,
                "avg_positioning_score": 0.0,
                "avg_battle_readiness_score": 0.0,
                "avg_relationship_advantage_score": 0.0,
                "total_estimated_pipeline_at_risk_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_wr = total_po = total_br = total_ra = total_pr = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.comp_risk.value]       = risk_counts.get(res.comp_risk.value, 0) + 1
            pattern_counts[res.comp_pattern.value] = pattern_counts.get(res.comp_pattern.value, 0) + 1
            severity_counts[res.comp_severity.value] = severity_counts.get(res.comp_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.comp_composite
            total_wr   += res.win_rate_score
            total_po   += res.positioning_score
            total_br   += res.battle_readiness_score
            total_ra   += res.relationship_advantage_score
            total_pr   += res.estimated_pipeline_at_risk_usd
            if res.has_comp_gap:          gap_count      += 1
            if res.requires_comp_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_comp_composite":                       round(total_comp / n, 1),
            "comp_gap_count":                           gap_count,
            "coaching_count":                           coaching_count,
            "avg_win_rate_score":                       round(total_wr / n, 1),
            "avg_positioning_score":                    round(total_po / n, 1),
            "avg_battle_readiness_score":               round(total_br / n, 1),
            "avg_relationship_advantage_score":         round(total_ra / n, 1),
            "total_estimated_pipeline_at_risk_usd":     round(total_pr, 2),
        }
