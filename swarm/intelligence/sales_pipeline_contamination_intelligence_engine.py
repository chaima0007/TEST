from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ContamRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ContamPattern(str, Enum):
    none               = "none"
    zombie_accumulator = "zombie_accumulator"
    stage_freezer      = "stage_freezer"
    unqualified_bloat  = "unqualified_bloat"
    forecast_padder    = "forecast_padder"
    dark_pipeline      = "dark_pipeline"


class ContamSeverity(str, Enum):
    clean       = "clean"
    adequate    = "adequate"
    contaminated = "contaminated"
    toxic       = "toxic"


class ContamAction(str, Enum):
    no_action                  = "no_action"
    pipeline_scrub             = "pipeline_scrub"
    qualification_coaching     = "qualification_coaching"
    deal_inspection            = "deal_inspection"
    pipeline_purge             = "pipeline_purge"
    deal_hygiene_intervention  = "deal_hygiene_intervention"
    executive_pipeline_reset   = "executive_pipeline_reset"


@dataclass
class ContamInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    zombie_deal_pct:                 float  # 0-1 deals with no activity >30d
    repeated_close_date_push_pct:    float  # 0-1 deals pushed 3+ times
    single_stage_stall_pct:          float  # 0-1 deals stalled same stage >21d
    no_next_step_pct:                float  # 0-1 deals with no next step
    unqualified_deal_pct:            float  # 0-1 deals lacking qualification
    avg_days_in_pipeline:            float  # avg deal age in days
    pipeline_inflation_ratio:        float  # pipeline/quota (>3 = inflated)
    lost_deal_recycle_pct:           float  # 0-1 lost re-entered without change
    verbal_commitment_only_pct:      float  # 0-1 verbal-only deals
    single_contact_deal_pct:         float  # 0-1 deals with 1 contact only
    dark_deal_pct:                   float  # 0-1 deals no log >14d
    forecast_category_mismatch_pct:  float  # 0-1 deals in wrong forecast cat
    avg_deal_size_variance:          float  # 0-1 normalized size variance
    competitor_not_identified_pct:   float  # 0-1 deals missing competitor
    budget_not_confirmed_pct:        float  # 0-1 deals no budget confirmed
    decision_maker_not_id_pct:       float  # 0-1 deals missing decision maker
    deal_age_vs_cycle_ratio:         float  # actual_age/typical_cycle
    total_active_deals:              int
    avg_deal_value_usd:              float


@dataclass
class ContamResult:
    rep_id:                       str
    region:                       str
    contam_risk:                  ContamRisk
    contam_pattern:               ContamPattern
    contam_severity:              ContamSeverity
    recommended_action:           ContamAction
    zombie_score:                 float
    qualification_score:          float
    accuracy_score:               float
    hygiene_score:                float
    contam_composite:             float
    has_contam_gap:               bool
    requires_contam_intervention: bool
    estimated_phantom_pipeline_usd: float
    contam_signal:                str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "contam_risk":                      self.contam_risk.value,
            "contam_pattern":                   self.contam_pattern.value,
            "contam_severity":                  self.contam_severity.value,
            "recommended_action":               self.recommended_action.value,
            "zombie_score":                     self.zombie_score,
            "qualification_score":              self.qualification_score,
            "accuracy_score":                   self.accuracy_score,
            "hygiene_score":                    self.hygiene_score,
            "contam_composite":                 self.contam_composite,
            "has_contam_gap":                   self.has_contam_gap,
            "requires_contam_intervention":     self.requires_contam_intervention,
            "estimated_phantom_pipeline_usd":   self.estimated_phantom_pipeline_usd,
            "contam_signal":                    self.contam_signal,
        }


class SalesPipelineContaminationIntelligenceEngine:
    """Detects per-rep pipeline contamination — zombie accumulation, unqualified bloat, forecast padding."""

    def __init__(self) -> None:
        self._results: List[ContamResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _zombie_score(self, inp: ContamInput) -> float:
        s = 0.0
        if   inp.zombie_deal_pct  >= 0.40: s += 40
        elif inp.zombie_deal_pct  >= 0.25: s += 22
        elif inp.zombie_deal_pct  >= 0.10: s += 8
        if   inp.dark_deal_pct    >= 0.45: s += 35
        elif inp.dark_deal_pct    >= 0.25: s += 18
        if   inp.deal_age_vs_cycle_ratio >= 2.0: s += 25
        elif inp.deal_age_vs_cycle_ratio >= 1.50: s += 12
        return min(s, 100.0)

    def _qualification_score(self, inp: ContamInput) -> float:
        s = 0.0
        if   inp.unqualified_deal_pct          >= 0.50: s += 40
        elif inp.unqualified_deal_pct          >= 0.30: s += 22
        elif inp.unqualified_deal_pct          >= 0.15: s += 8
        if   inp.decision_maker_not_id_pct     >= 0.55: s += 35
        elif inp.decision_maker_not_id_pct     >= 0.35: s += 18
        if   inp.single_contact_deal_pct       >= 0.60: s += 25
        elif inp.single_contact_deal_pct       >= 0.40: s += 12
        return min(s, 100.0)

    def _accuracy_score(self, inp: ContamInput) -> float:
        s = 0.0
        if   inp.repeated_close_date_push_pct  >= 0.50: s += 40
        elif inp.repeated_close_date_push_pct  >= 0.30: s += 22
        elif inp.repeated_close_date_push_pct  >= 0.15: s += 8
        if   inp.forecast_category_mismatch_pct >= 0.40: s += 35
        elif inp.forecast_category_mismatch_pct >= 0.20: s += 18
        if   inp.pipeline_inflation_ratio       >= 4.0: s += 25
        elif inp.pipeline_inflation_ratio       >= 3.0: s += 12
        return min(s, 100.0)

    def _hygiene_score(self, inp: ContamInput) -> float:
        s = 0.0
        if   inp.no_next_step_pct              >= 0.55: s += 45
        elif inp.no_next_step_pct              >= 0.35: s += 25
        elif inp.no_next_step_pct              >= 0.20: s += 10
        if   inp.budget_not_confirmed_pct      >= 0.60: s += 30
        elif inp.budget_not_confirmed_pct      >= 0.40: s += 15
        if   inp.verbal_commitment_only_pct    >= 0.35: s += 25
        elif inp.verbal_commitment_only_pct    >= 0.20: s += 10
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, z: float, q: float, a: float, h: float) -> float:
        return min(round(z * 0.35 + q * 0.25 + a * 0.25 + h * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: ContamInput) -> ContamPattern:
        if inp.zombie_deal_pct >= 0.30 and inp.deal_age_vs_cycle_ratio >= 1.50:
            return ContamPattern.zombie_accumulator
        if inp.single_stage_stall_pct >= 0.40 and inp.repeated_close_date_push_pct >= 0.35:
            return ContamPattern.stage_freezer
        if inp.unqualified_deal_pct >= 0.35 and inp.decision_maker_not_id_pct >= 0.40:
            return ContamPattern.unqualified_bloat
        if inp.pipeline_inflation_ratio >= 3.5 and inp.forecast_category_mismatch_pct >= 0.30:
            return ContamPattern.forecast_padder
        if inp.dark_deal_pct >= 0.35 and inp.no_next_step_pct >= 0.40:
            return ContamPattern.dark_pipeline
        return ContamPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> ContamRisk:
        if   composite >= 60: return ContamRisk.critical
        elif composite >= 40: return ContamRisk.high
        elif composite >= 20: return ContamRisk.moderate
        return ContamRisk.low

    def _severity(self, composite: float) -> ContamSeverity:
        if   composite >= 60: return ContamSeverity.toxic
        elif composite >= 40: return ContamSeverity.contaminated
        elif composite >= 20: return ContamSeverity.adequate
        return ContamSeverity.clean

    def _action(self, risk: ContamRisk, pattern: ContamPattern) -> ContamAction:
        if risk == ContamRisk.critical:
            if pattern in (ContamPattern.zombie_accumulator, ContamPattern.forecast_padder):
                return ContamAction.executive_pipeline_reset
            return ContamAction.pipeline_purge
        if risk == ContamRisk.high:
            if pattern == ContamPattern.zombie_accumulator:
                return ContamAction.pipeline_purge
            if pattern == ContamPattern.unqualified_bloat:
                return ContamAction.qualification_coaching
            if pattern == ContamPattern.stage_freezer:
                return ContamAction.deal_inspection
            if pattern == ContamPattern.dark_pipeline:
                return ContamAction.deal_hygiene_intervention
            if pattern == ContamPattern.forecast_padder:
                return ContamAction.deal_inspection
            return ContamAction.deal_hygiene_intervention
        if risk == ContamRisk.moderate:
            return ContamAction.pipeline_scrub
        return ContamAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: ContamInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.zombie_deal_pct                >= 0.20
            or inp.repeated_close_date_push_pct   >= 0.25
        )

    def _requires_intervention(self, inp: ContamInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.unqualified_deal_pct           >= 0.25
            or inp.no_next_step_pct               >= 0.30
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _phantom_pipeline(self, inp: ContamInput, composite: float) -> float:
        phantom_pct = min(1.0, inp.zombie_deal_pct + inp.unqualified_deal_pct * 0.5)
        return round(inp.total_active_deals * inp.avg_deal_value_usd * phantom_pct * (composite / 100), 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        ContamPattern.zombie_accumulator: "Zombie accumulator",
        ContamPattern.stage_freezer:      "Stage freezer",
        ContamPattern.unqualified_bloat:  "Unqualified bloat",
        ContamPattern.forecast_padder:    "Forecast padder",
        ContamPattern.dark_pipeline:      "Dark pipeline",
    }

    def _signal(self, inp: ContamInput, pattern: ContamPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Pipeline contamination low — deal quality, qualification, "
                "forecast accuracy, and hygiene within benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        zomb_pct = round(inp.zombie_deal_pct * 100)
        push_pct = round(inp.repeated_close_date_push_pct * 100)
        unq_pct  = round(inp.unqualified_deal_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {zomb_pct}% zombie deals — "
            f"{push_pct}% close date pushed 3+ times — "
            f"{unq_pct}% unqualified — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: ContamInput) -> ContamResult:
        z  = self._zombie_score(inp)
        q  = self._qualification_score(inp)
        a  = self._accuracy_score(inp)
        h  = self._hygiene_score(inp)
        comp = self._composite(z, q, a, h)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = ContamResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            contam_risk                 = risk,
            contam_pattern              = pattern,
            contam_severity             = severity,
            recommended_action          = action,
            zombie_score                = z,
            qualification_score         = q,
            accuracy_score              = a,
            hygiene_score               = h,
            contam_composite            = comp,
            has_contam_gap              = self._has_gap(inp, comp),
            requires_contam_intervention= self._requires_intervention(inp, comp),
            estimated_phantom_pipeline_usd = self._phantom_pipeline(inp, comp),
            contam_signal               = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ContamInput]) -> List[ContamResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_contam_composite": 0.0,
                "contam_gap_count": 0,
                "intervention_count": 0,
                "avg_zombie_score": 0.0,
                "avg_qualification_score": 0.0,
                "avg_accuracy_score": 0.0,
                "avg_hygiene_score": 0.0,
                "total_estimated_phantom_pipeline_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_z = total_q = total_a = total_h = total_pp = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.contam_risk.value]       = risk_counts.get(res.contam_risk.value, 0) + 1
            pattern_counts[res.contam_pattern.value] = pattern_counts.get(res.contam_pattern.value, 0) + 1
            severity_counts[res.contam_severity.value] = severity_counts.get(res.contam_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.contam_composite
            total_z    += res.zombie_score
            total_q    += res.qualification_score
            total_a    += res.accuracy_score
            total_h    += res.hygiene_score
            total_pp   += res.estimated_phantom_pipeline_usd
            if res.has_contam_gap:              gap_count          += 1
            if res.requires_contam_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_contam_composite":                     round(total_comp / n, 1),
            "contam_gap_count":                         gap_count,
            "intervention_count":                       intervention_count,
            "avg_zombie_score":                         round(total_z / n, 1),
            "avg_qualification_score":                  round(total_q / n, 1),
            "avg_accuracy_score":                       round(total_a / n, 1),
            "avg_hygiene_score":                        round(total_h / n, 1),
            "total_estimated_phantom_pipeline_usd":     round(total_pp, 2),
        }
