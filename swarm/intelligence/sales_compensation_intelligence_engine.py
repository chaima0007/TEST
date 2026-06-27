from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CompRiskLevel(str, Enum):
    LOW      = "low"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class GamingPattern(str, Enum):
    CLEAN          = "clean"
    SANDBAGGING    = "sandbagging"
    SPIFF_CHASING  = "spiff_chasing"
    DISCOUNT_HEAVY = "discount_heavy"
    MIXED          = "mixed"


class IncentiveAlignment(str, Enum):
    WELL_ALIGNED      = "well_aligned"
    PARTIALLY_ALIGNED = "partially_aligned"
    MISALIGNED        = "misaligned"
    PERVERSE          = "perverse"


class CompAction(str, Enum):
    MAINTAIN         = "maintain"
    MONITOR          = "monitor"
    RESTRUCTURE      = "restructure"
    IMMEDIATE_REVIEW = "immediate_review"


@dataclass
class SalesCompIntelInput:
    rep_id:                    str
    rep_name:                  str
    manager_id:                str
    region:                    str
    base_salary:               float    # annual base salary
    ote_salary:                float    # on-target earnings
    quota:                     float    # annual quota
    deals_closed_qtd:          int      # deals closed this quarter
    revenue_closed_qtd:        float    # revenue closed this quarter
    avg_deal_size:             float    # average deal size this quarter
    deals_in_pipeline:         int      # open pipeline deals
    pipeline_value:            float    # total pipeline value
    large_deal_pct:            float    # % of revenue from deals >3x avg (0-100)
    spiff_driven_pct:          float    # % of deals closed during active spiff (0-100)
    quarter_end_close_pct:     float    # % of deals closed in last 2 weeks of quarter (0-100)
    multiyear_deal_pct:        float    # % revenue from multiyear deals (0-100)
    avg_discount_pct:          float    # average discount given (0-100)
    quota_attainment_q1:       float    # last 3Q attainment %, 0-200+
    quota_attainment_q2:       float
    quota_attainment_q3:       float
    comp_complaints:           int      # HR comp-related complaints filed YTD
    activity_score_qtd:        float    # CRM activity score 0-100


@dataclass
class SalesCompIntelResult:
    rep_id:                       str
    rep_name:                     str
    comp_risk_level:              CompRiskLevel
    gaming_pattern:               GamingPattern
    incentive_alignment:          IncentiveAlignment
    comp_action:                  CompAction
    sandbagging_score:            float    # 0-100
    spiff_dependency_score:       float    # 0-100
    discount_behavior_score:      float    # 0-100 (higher = more problematic)
    attainment_consistency_score: float    # 0-100 (higher = more consistent)
    compensation_efficiency_score: float   # 0-100 (revenue / comp cost)
    estimated_overcompensation:   float    # estimated $ overpaid vs value delivered
    quota_accuracy_score:         float    # 0-100 (how accurate quota was set)
    is_gaming_comp:               bool
    needs_comp_review:            bool

    def to_dict(self) -> dict:
        return {
            "rep_id":                        self.rep_id,
            "rep_name":                      self.rep_name,
            "comp_risk_level":               self.comp_risk_level.value,
            "gaming_pattern":                self.gaming_pattern.value,
            "incentive_alignment":           self.incentive_alignment.value,
            "comp_action":                   self.comp_action.value,
            "sandbagging_score":             self.sandbagging_score,
            "spiff_dependency_score":        self.spiff_dependency_score,
            "discount_behavior_score":       self.discount_behavior_score,
            "attainment_consistency_score":  self.attainment_consistency_score,
            "compensation_efficiency_score": self.compensation_efficiency_score,
            "estimated_overcompensation":    self.estimated_overcompensation,
            "quota_accuracy_score":          self.quota_accuracy_score,
            "is_gaming_comp":                self.is_gaming_comp,
            "needs_comp_review":             self.needs_comp_review,
        }


class SalesCompIntelligenceEngine:
    def __init__(self) -> None:
        self._results: list[SalesCompIntelResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: SalesCompIntelInput) -> SalesCompIntelResult:
        sandbagging     = self._sandbagging_score(inp)
        spiff_dep       = self._spiff_dependency_score(inp)
        discount_beh    = self._discount_behavior_score(inp)
        attain_consist  = self._attainment_consistency_score(inp)
        comp_efficiency = self._compensation_efficiency_score(inp)
        overcomp        = self._estimated_overcompensation(inp, comp_efficiency)
        quota_acc       = self._quota_accuracy_score(inp)
        risk            = self._comp_risk_level(inp, sandbagging, spiff_dep, discount_beh)
        pattern         = self._gaming_pattern(sandbagging, spiff_dep, discount_beh)
        alignment       = self._incentive_alignment(inp, sandbagging, spiff_dep, discount_beh)
        is_gaming       = sandbagging >= 55.0 or spiff_dep >= 65.0 or discount_beh >= 60.0
        needs_review    = (
            risk in (CompRiskLevel.HIGH, CompRiskLevel.CRITICAL) or
            inp.comp_complaints >= 2 or
            comp_efficiency < 30.0
        )
        action = self._comp_action(risk, alignment, is_gaming, needs_review)

        result = SalesCompIntelResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            comp_risk_level=risk,
            gaming_pattern=pattern,
            incentive_alignment=alignment,
            comp_action=action,
            sandbagging_score=sandbagging,
            spiff_dependency_score=spiff_dep,
            discount_behavior_score=discount_beh,
            attainment_consistency_score=attain_consist,
            compensation_efficiency_score=comp_efficiency,
            estimated_overcompensation=overcomp,
            quota_accuracy_score=quota_acc,
            is_gaming_comp=is_gaming,
            needs_comp_review=needs_review,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[SalesCompIntelInput]
    ) -> list[SalesCompIntelResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def gaming_reps(self) -> list[SalesCompIntelResult]:
        return [r for r in self._results if r.is_gaming_comp]

    @property
    def review_needed(self) -> list[SalesCompIntelResult]:
        return [r for r in self._results if r.needs_comp_review]

    @property
    def total_overcompensation(self) -> float:
        return round(sum(r.estimated_overcompensation for r in self._results), 2)

    @property
    def avg_compensation_efficiency(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.compensation_efficiency_score for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _sandbagging_score(self, inp: SalesCompIntelInput) -> float:
        score = 0.0
        # Quarter-end close concentration (up to 40)
        score += min(40.0, inp.quarter_end_close_pct * 0.7)
        # Attainment pattern: suspiciously stable near 100% (sand-baggers hit ~105-115%)
        attainments = [inp.quota_attainment_q1, inp.quota_attainment_q2, inp.quota_attainment_q3]
        avg_att = sum(attainments) / 3
        if 95.0 <= avg_att <= 120.0:
            # Very tight range around just above quota → sandbagging signal
            variance = max(attainments) - min(attainments)
            if variance < 15.0:
                score += min(35.0, (15.0 - variance) * 2.5)
        # Low activity score despite decent revenue → holding deals back
        if inp.activity_score_qtd < 40.0 and inp.revenue_closed_qtd > 0:
            score += min(25.0, (40.0 - inp.activity_score_qtd) * 0.6)
        return round(max(0.0, min(100.0, score)), 1)

    def _spiff_dependency_score(self, inp: SalesCompIntelInput) -> float:
        score = 0.0
        # Spiff-driven deal concentration (up to 50)
        score += min(50.0, inp.spiff_driven_pct * 0.9)
        # Large deal skew — chasing accelerators (up to 30)
        score += min(30.0, inp.large_deal_pct * 0.6)
        # Multiyear deal push (up to 20) — often spiff-motivated
        score += min(20.0, inp.multiyear_deal_pct * 0.4)
        return round(max(0.0, min(100.0, score)), 1)

    def _discount_behavior_score(self, inp: SalesCompIntelInput) -> float:
        score = 0.0
        # Discount depth (up to 50)
        score += min(50.0, inp.avg_discount_pct * 1.2)
        # High discount + high close rate → buying revenue, not winning it (up to 30)
        if inp.avg_discount_pct >= 20.0 and inp.deals_closed_qtd > 0:
            close_rate_proxy = inp.revenue_closed_qtd / max(1.0, inp.pipeline_value) * 100
            if close_rate_proxy > 50.0:
                score += min(30.0, (close_rate_proxy - 50.0) * 0.8)
        # Complaints signal discount abuse complaints from peers/customers (up to 20)
        score += min(20.0, inp.comp_complaints * 7.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _attainment_consistency_score(self, inp: SalesCompIntelInput) -> float:
        attainments = [inp.quota_attainment_q1, inp.quota_attainment_q2, inp.quota_attainment_q3]
        avg_att = sum(attainments) / 3
        variance = max(attainments) - min(attainments)
        # High average + low variance = most consistent (score 100)
        consistency = max(0.0, 100.0 - variance * 2.0)
        # Adjust for overall achievement level
        achievement_bonus = min(20.0, max(0.0, (avg_att - 80.0) * 0.4))
        return round(max(0.0, min(100.0, consistency * 0.8 + achievement_bonus)), 1)

    def _compensation_efficiency_score(self, inp: SalesCompIntelInput) -> float:
        if inp.ote_salary <= 0:
            return 0.0
        # Revenue multiple: how many X OTE does the rep generate?
        revenue_multiple = inp.revenue_closed_qtd * 4 / inp.ote_salary  # annualized
        # Target is 5x OTE = score 100; below 2x = very poor
        if revenue_multiple >= 5.0:
            return 100.0
        if revenue_multiple <= 1.0:
            return 0.0
        return round(min(100.0, (revenue_multiple - 1.0) / 4.0 * 100.0), 1)

    def _estimated_overcompensation(
        self, inp: SalesCompIntelInput, efficiency_score: float
    ) -> float:
        if efficiency_score >= 60.0:
            return 0.0
        # Rep is underperforming relative to comp
        annualized_revenue = inp.revenue_closed_qtd * 4
        target_revenue = inp.ote_salary * 3.0  # 3x OTE is minimum acceptable
        if annualized_revenue >= target_revenue:
            return 0.0
        shortfall_pct = (target_revenue - annualized_revenue) / target_revenue
        overpay_estimate = inp.ote_salary * shortfall_pct * 0.4
        return round(max(0.0, overpay_estimate), 2)

    def _quota_accuracy_score(self, inp: SalesCompIntelInput) -> float:
        attainments = [inp.quota_attainment_q1, inp.quota_attainment_q2, inp.quota_attainment_q3]
        avg_att = sum(attainments) / 3
        # Perfect quota accuracy = rep hits 95-105% consistently
        # Too easy (>130% avg) → quota set too low → score penalized
        # Too hard (<60% avg) → quota set too high → score penalized
        if 90.0 <= avg_att <= 110.0:
            return round(min(100.0, 100.0 - abs(avg_att - 100.0) * 2.0), 1)
        if avg_att > 110.0:
            excess = avg_att - 110.0
            return round(max(0.0, 100.0 - excess * 1.5), 1)
        shortfall = 90.0 - avg_att
        return round(max(0.0, 100.0 - shortfall * 2.0), 1)

    def _comp_risk_level(
        self,
        inp: SalesCompIntelInput,
        sandbagging: float,
        spiff_dep: float,
        discount_beh: float,
    ) -> CompRiskLevel:
        combined = sandbagging * 0.4 + spiff_dep * 0.3 + discount_beh * 0.3
        if combined >= 60 or inp.comp_complaints >= 3:
            return CompRiskLevel.CRITICAL
        if combined >= 40 or inp.comp_complaints >= 2:
            return CompRiskLevel.HIGH
        if combined >= 20:
            return CompRiskLevel.MODERATE
        return CompRiskLevel.LOW

    def _gaming_pattern(
        self, sandbagging: float, spiff_dep: float, discount_beh: float
    ) -> GamingPattern:
        signals = sum([sandbagging >= 50, spiff_dep >= 55, discount_beh >= 50])
        if signals >= 2:
            return GamingPattern.MIXED
        if sandbagging >= 50:
            return GamingPattern.SANDBAGGING
        if spiff_dep >= 55:
            return GamingPattern.SPIFF_CHASING
        if discount_beh >= 50:
            return GamingPattern.DISCOUNT_HEAVY
        return GamingPattern.CLEAN

    def _incentive_alignment(
        self,
        inp: SalesCompIntelInput,
        sandbagging: float,
        spiff_dep: float,
        discount_beh: float,
    ) -> IncentiveAlignment:
        gaming_signal = sandbagging * 0.35 + spiff_dep * 0.35 + discount_beh * 0.30
        if gaming_signal >= 55 or inp.comp_complaints >= 3:
            return IncentiveAlignment.PERVERSE
        if gaming_signal >= 35:
            return IncentiveAlignment.MISALIGNED
        if gaming_signal >= 18:
            return IncentiveAlignment.PARTIALLY_ALIGNED
        return IncentiveAlignment.WELL_ALIGNED

    def _comp_action(
        self,
        risk: CompRiskLevel,
        alignment: IncentiveAlignment,
        is_gaming: bool,
        needs_review: bool,
    ) -> CompAction:
        if risk == CompRiskLevel.CRITICAL or alignment == IncentiveAlignment.PERVERSE:
            return CompAction.IMMEDIATE_REVIEW
        if is_gaming or alignment == IncentiveAlignment.MISALIGNED:
            return CompAction.RESTRUCTURE
        if needs_review or alignment == IncentiveAlignment.PARTIALLY_ALIGNED:
            return CompAction.MONITOR
        return CompAction.MAINTAIN

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                            0,
                "risk_counts":                      {},
                "pattern_counts":                   {},
                "alignment_counts":                 {},
                "action_counts":                    {},
                "avg_compensation_efficiency_score": 0.0,
                "avg_sandbagging_score":            0.0,
                "total_estimated_overcompensation": 0.0,
                "gaming_count":                     0,
                "review_needed_count":              0,
                "avg_spiff_dependency_score":       0.0,
                "avg_discount_behavior_score":      0.0,
                "avg_quota_accuracy_score":         0.0,
            }

        risk_counts:      dict[str, int] = {}
        pattern_counts:   dict[str, int] = {}
        alignment_counts: dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_eff   = 0.0
        total_sand  = 0.0
        total_spiff = 0.0
        total_disc  = 0.0
        total_quot  = 0.0

        for r in self._results:
            risk_counts[r.comp_risk_level.value]    = risk_counts.get(r.comp_risk_level.value, 0) + 1
            pattern_counts[r.gaming_pattern.value]  = pattern_counts.get(r.gaming_pattern.value, 0) + 1
            alignment_counts[r.incentive_alignment.value] = alignment_counts.get(r.incentive_alignment.value, 0) + 1
            action_counts[r.comp_action.value]      = action_counts.get(r.comp_action.value, 0) + 1
            total_eff   += r.compensation_efficiency_score
            total_sand  += r.sandbagging_score
            total_spiff += r.spiff_dependency_score
            total_disc  += r.discount_behavior_score
            total_quot  += r.quota_accuracy_score

        return {
            "total":                            n,
            "risk_counts":                      risk_counts,
            "pattern_counts":                   pattern_counts,
            "alignment_counts":                 alignment_counts,
            "action_counts":                    action_counts,
            "avg_compensation_efficiency_score": round(total_eff / n, 1),
            "avg_sandbagging_score":            round(total_sand / n, 1),
            "total_estimated_overcompensation": self.total_overcompensation,
            "gaming_count":                     len(self.gaming_reps),
            "review_needed_count":              len(self.review_needed),
            "avg_spiff_dependency_score":       round(total_spiff / n, 1),
            "avg_discount_behavior_score":      round(total_disc / n, 1),
            "avg_quota_accuracy_score":         round(total_quot / n, 1),
        }
