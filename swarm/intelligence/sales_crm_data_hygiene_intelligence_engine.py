from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class HygRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class HygPattern(str, Enum):
    none               = "none"
    ghost_pipeline     = "ghost_pipeline"      # deals stuck with no updates
    field_skipper      = "field_skipper"        # consistently leaves required fields blank
    stage_freezer      = "stage_freezer"        # deals never advance stages
    contact_orphaner   = "contact_orphaner"     # deals with no contacts linked
    activity_shadow    = "activity_shadow"      # calls/emails not logged


class HygSeverity(str, Enum):
    clean       = "clean"
    adequate    = "adequate"
    degraded    = "degraded"
    corrupted   = "corrupted"


class HygAction(str, Enum):
    no_action                   = "no_action"
    data_entry_coaching         = "data_entry_coaching"
    stage_hygiene_coaching      = "stage_hygiene_coaching"
    contact_linking_coaching    = "contact_linking_coaching"
    activity_logging_coaching   = "activity_logging_coaching"
    crm_audit_required          = "crm_audit_required"
    crm_data_reset              = "crm_data_reset"


@dataclass
class HygInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    required_field_completion_pct:       float   # % of required CRM fields filled (0–1)
    avg_days_since_last_update:          float   # avg days since last activity logged
    stage_advancement_rate_pct:          float   # % of deals that advanced stage in 30d (0–1)
    deal_without_contact_pct:            float   # % of deals with no contact linked (0–1)
    activity_log_rate_pct:               float   # % of calls/emails actually logged (0–1)
    close_date_accuracy_pct:             float   # % of close dates within 14d of actual (0–1)
    forecast_category_accuracy_pct:      float   # % of deals in correct forecast bucket (0–1)
    duplicate_deal_rate_pct:             float   # % of deals that are duplicates (0–1)
    stale_deal_rate_pct:                 float   # % of deals with >30d no update (0–1)
    next_step_field_fill_rate_pct:       float   # % of deals with next step populated (0–1)
    deal_amount_accuracy_pct:            float   # % of deals with correct amount (0–1)
    email_linked_rate_pct:               float   # % of emails linked to CRM records (0–1)
    opportunity_age_vs_sales_cycle_pct:  float   # avg opp age / target sales cycle (0–1+)
    manual_update_compliance_pct:        float   # % of manual update requirements met (0–1)
    total_active_deals:                  int
    avg_opportunity_value_usd:           float
    total_pipeline_usd:                  float
    forecasted_revenue_usd:              float
    quota_usd:                           float


@dataclass
class HygResult:
    rep_id:                       str
    region:                       str
    hyg_risk:                     HygRisk
    hyg_pattern:                  HygPattern
    hyg_severity:                 HygSeverity
    recommended_action:           HygAction
    completeness_score:           float
    currency_score:               float
    accuracy_score:               float
    activity_capture_score:       float
    hyg_composite:                float
    has_hyg_gap:                  bool
    requires_hyg_coaching:        bool
    estimated_forecast_error_usd: float
    hyg_signal:                   str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "hyg_risk":                       self.hyg_risk.value,
            "hyg_pattern":                    self.hyg_pattern.value,
            "hyg_severity":                   self.hyg_severity.value,
            "recommended_action":             self.recommended_action.value,
            "completeness_score":             self.completeness_score,
            "currency_score":                 self.currency_score,
            "accuracy_score":                 self.accuracy_score,
            "activity_capture_score":         self.activity_capture_score,
            "hyg_composite":                  self.hyg_composite,
            "has_hyg_gap":                    self.has_hyg_gap,
            "requires_hyg_coaching":          self.requires_hyg_coaching,
            "estimated_forecast_error_usd":   self.estimated_forecast_error_usd,
            "hyg_signal":                     self.hyg_signal,
        }


class SalesCRMDataHygieneIntelligenceEngine:

    def __init__(self) -> None:
        self._results: List[HygResult] = []

    def _completeness_score(self, inp: HygInput) -> float:
        s = 0.0
        if inp.required_field_completion_pct <= 0.60:
            s += 45
        elif inp.required_field_completion_pct <= 0.75:
            s += 28
        elif inp.required_field_completion_pct <= 0.88:
            s += 12
        if inp.next_step_field_fill_rate_pct <= 0.40:
            s += 35
        elif inp.next_step_field_fill_rate_pct <= 0.60:
            s += 18
        elif inp.next_step_field_fill_rate_pct <= 0.75:
            s += 6
        if inp.deal_without_contact_pct >= 0.35:
            s += 20
        elif inp.deal_without_contact_pct >= 0.20:
            s += 10
        return min(s, 100.0)

    def _currency_score(self, inp: HygInput) -> float:
        s = 0.0
        if inp.avg_days_since_last_update >= 21:
            s += 45
        elif inp.avg_days_since_last_update >= 14:
            s += 28
        elif inp.avg_days_since_last_update >= 7:
            s += 12
        if inp.stale_deal_rate_pct >= 0.40:
            s += 35
        elif inp.stale_deal_rate_pct >= 0.25:
            s += 18
        elif inp.stale_deal_rate_pct >= 0.12:
            s += 6
        if inp.stage_advancement_rate_pct <= 0.25:
            s += 20
        elif inp.stage_advancement_rate_pct <= 0.45:
            s += 10
        return min(s, 100.0)

    def _accuracy_score(self, inp: HygInput) -> float:
        s = 0.0
        if inp.close_date_accuracy_pct <= 0.40:
            s += 40
        elif inp.close_date_accuracy_pct <= 0.60:
            s += 22
        elif inp.close_date_accuracy_pct <= 0.78:
            s += 8
        if inp.forecast_category_accuracy_pct <= 0.50:
            s += 35
        elif inp.forecast_category_accuracy_pct <= 0.70:
            s += 18
        elif inp.forecast_category_accuracy_pct <= 0.82:
            s += 6
        if inp.duplicate_deal_rate_pct >= 0.15:
            s += 25
        elif inp.duplicate_deal_rate_pct >= 0.08:
            s += 12
        return min(s, 100.0)

    def _activity_capture_score(self, inp: HygInput) -> float:
        s = 0.0
        if inp.activity_log_rate_pct <= 0.40:
            s += 45
        elif inp.activity_log_rate_pct <= 0.60:
            s += 28
        elif inp.activity_log_rate_pct <= 0.75:
            s += 12
        if inp.email_linked_rate_pct <= 0.40:
            s += 35
        elif inp.email_linked_rate_pct <= 0.60:
            s += 18
        elif inp.email_linked_rate_pct <= 0.75:
            s += 6
        if inp.manual_update_compliance_pct <= 0.50:
            s += 20
        elif inp.manual_update_compliance_pct <= 0.70:
            s += 10
        return min(s, 100.0)

    def _composite(self, cs: float, cu: float, ac: float, ap: float) -> float:
        return round(cs * 0.30 + cu * 0.25 + ac * 0.25 + ap * 0.20, 2)

    def _pattern(self, inp: HygInput) -> HygPattern:
        if inp.stale_deal_rate_pct >= 0.35 and inp.avg_days_since_last_update >= 18:
            return HygPattern.ghost_pipeline
        if inp.required_field_completion_pct <= 0.65 and inp.next_step_field_fill_rate_pct <= 0.45:
            return HygPattern.field_skipper
        if inp.stage_advancement_rate_pct <= 0.20 and inp.stale_deal_rate_pct >= 0.30:
            return HygPattern.stage_freezer
        if inp.deal_without_contact_pct >= 0.30 and inp.email_linked_rate_pct <= 0.50:
            return HygPattern.contact_orphaner
        if inp.activity_log_rate_pct <= 0.45 and inp.email_linked_rate_pct <= 0.50:
            return HygPattern.activity_shadow
        return HygPattern.none

    def _risk(self, composite: float) -> HygRisk:
        if composite >= 60: return HygRisk.critical
        if composite >= 40: return HygRisk.high
        if composite >= 20: return HygRisk.moderate
        return HygRisk.low

    def _severity(self, composite: float) -> HygSeverity:
        if composite >= 60: return HygSeverity.corrupted
        if composite >= 40: return HygSeverity.degraded
        if composite >= 20: return HygSeverity.adequate
        return HygSeverity.clean

    def _action(self, risk: HygRisk, pattern: HygPattern) -> HygAction:
        if risk == HygRisk.critical:
            if pattern in (HygPattern.ghost_pipeline, HygPattern.stage_freezer):
                return HygAction.crm_data_reset
            return HygAction.crm_audit_required
        if risk == HygRisk.high:
            if pattern == HygPattern.field_skipper:
                return HygAction.data_entry_coaching
            if pattern == HygPattern.stage_freezer:
                return HygAction.stage_hygiene_coaching
            if pattern == HygPattern.contact_orphaner:
                return HygAction.contact_linking_coaching
            if pattern == HygPattern.activity_shadow:
                return HygAction.activity_logging_coaching
            return HygAction.data_entry_coaching
        if risk == HygRisk.moderate:
            return HygAction.data_entry_coaching
        return HygAction.no_action

    def _has_gap(self, inp: HygInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.required_field_completion_pct <= 0.80
            or inp.stale_deal_rate_pct >= 0.20
        )

    def _requires_coaching(self, inp: HygInput, composite: float) -> bool:
        return (
            composite >= 20
            or inp.activity_log_rate_pct <= 0.70
            or inp.close_date_accuracy_pct <= 0.70
        )

    def _forecast_error(self, inp: HygInput, composite: float) -> float:
        accuracy_gap = max(0.0, 0.90 - inp.forecast_category_accuracy_pct)
        return round(inp.forecasted_revenue_usd * accuracy_gap * (composite / 100.0), 2)

    def _signal(self, inp: HygInput, pattern: HygPattern, composite: float) -> str:
        if composite < 20:
            return (
                "CRM data hygiene strong — completeness, currency, "
                "accuracy, and activity capture within benchmarks"
            )
        labels = {
            HygPattern.ghost_pipeline:   "Ghost pipeline",
            HygPattern.field_skipper:    "Field skipper",
            HygPattern.stage_freezer:    "Stage freezer",
            HygPattern.contact_orphaner: "Contact orphaner",
            HygPattern.activity_shadow:  "Activity shadow",
        }
        label     = labels.get(pattern, "CRM hygiene gap")
        fill_pct  = round(inp.required_field_completion_pct * 100)
        stale_pct = round(inp.stale_deal_rate_pct * 100)
        log_pct   = round(inp.activity_log_rate_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {fill_pct}% fields complete — "
            f"{stale_pct}% deals stale — "
            f"{log_pct}% activities logged — composite {comp_int}"
        )

    def assess(self, inp: HygInput) -> HygResult:
        cs = self._completeness_score(inp)
        cu = self._currency_score(inp)
        ac = self._accuracy_score(inp)
        ap = self._activity_capture_score(inp)
        comp    = self._composite(cs, cu, ac, ap)
        pattern = self._pattern(inp)
        risk    = self._risk(comp)
        sev     = self._severity(comp)
        action  = self._action(risk, pattern)
        result  = HygResult(
            rep_id                       = inp.rep_id,
            region                       = inp.region,
            hyg_risk                     = risk,
            hyg_pattern                  = pattern,
            hyg_severity                 = sev,
            recommended_action           = action,
            completeness_score           = round(cs, 2),
            currency_score               = round(cu, 2),
            accuracy_score               = round(ac, 2),
            activity_capture_score       = round(ap, 2),
            hyg_composite                = comp,
            has_hyg_gap                  = self._has_gap(inp, comp),
            requires_hyg_coaching        = self._requires_coaching(inp, comp),
            estimated_forecast_error_usd = self._forecast_error(inp, comp),
            hyg_signal                   = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[HygInput]) -> List[HygResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        rr = self._results
        if not rr:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_hyg_composite": 0.0, "hyg_gap_count": 0,
                "coaching_count": 0, "avg_completeness_score": 0.0,
                "avg_currency_score": 0.0, "avg_accuracy_score": 0.0,
                "avg_activity_capture_score": 0.0,
                "total_estimated_forecast_error_usd": 0.0,
            }
        n = len(rr)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tcs = tcu = tac = tap = trev = 0.0
        gc = cc = 0
        for r in rr:
            rc[r.hyg_risk.value]           = rc.get(r.hyg_risk.value, 0) + 1
            pc[r.hyg_pattern.value]        = pc.get(r.hyg_pattern.value, 0) + 1
            sc[r.hyg_severity.value]       = sc.get(r.hyg_severity.value, 0) + 1
            ac[r.recommended_action.value] = ac.get(r.recommended_action.value, 0) + 1
            tcs  += r.completeness_score
            tcu  += r.currency_score
            tac  += r.accuracy_score
            tap  += r.activity_capture_score
            trev += r.estimated_forecast_error_usd
            gc   += r.has_hyg_gap
            cc   += r.requires_hyg_coaching
        return {
            "total":                               n,
            "risk_counts":                         rc,
            "pattern_counts":                      pc,
            "severity_counts":                     sc,
            "action_counts":                       ac,
            "avg_hyg_composite":                   round(sum(r.hyg_composite for r in rr) / n, 1),
            "hyg_gap_count":                       gc,
            "coaching_count":                      cc,
            "avg_completeness_score":              round(tcs / n, 1),
            "avg_currency_score":                  round(tcu / n, 1),
            "avg_accuracy_score":                  round(tac / n, 1),
            "avg_activity_capture_score":          round(tap / n, 1),
            "total_estimated_forecast_error_usd":  round(trev, 2),
        }
