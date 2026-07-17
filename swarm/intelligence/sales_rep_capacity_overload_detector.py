"""Sales Rep Capacity Overload Detector — identifies when reps are assigned more
accounts, deals, and activities than they can handle, causing quality degradation,
deal neglect, CRM decay, and ultimately pipeline leakage."""

from __future__ import annotations

import dataclasses
from enum import Enum


class CapacityRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CapacityStressor(str, Enum):
    none               = "none"
    account_overload   = "account_overload"
    deal_volume_excess = "deal_volume_excess"
    activity_overburn  = "activity_overburn"
    admin_burden       = "admin_burden"
    multi_role_strain  = "multi_role_strain"


class CapacitySeverity(str, Enum):
    optimal    = "optimal"
    stretched  = "stretched"
    overloaded = "overloaded"
    critical   = "critical"


class CapacityAction(str, Enum):
    no_action              = "no_action"
    workload_review        = "workload_review"
    account_redistribution = "account_redistribution"
    hire_support           = "hire_support"
    immediate_relief       = "immediate_relief"


@dataclasses.dataclass
class RepCapacityInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    total_accounts_owned:           int
    benchmark_accounts_per_rep:     int
    active_deals_in_pipeline:       int
    benchmark_deals_per_rep:        int
    outbound_activities_last_30d:   int
    benchmark_activities_per_month: int
    meetings_held_last_30d:         int
    benchmark_meetings_per_month:   int
    crm_tasks_overdue_count:        int
    emails_responded_pct:           float
    avg_response_time_hours:        float
    deals_not_touched_last_14d:     int
    accounts_not_contacted_last_30d: int
    admin_hours_per_week:           float
    selling_hours_per_week:         float
    concurrent_pocs_count:          int
    deal_quality_score:             float
    peer_avg_deal_quality_score:    float
    pto_days_missed_last_90d:       int


@dataclasses.dataclass
class RepCapacityResult:
    rep_id:                     str
    region:                     str
    capacity_risk:              CapacityRisk
    capacity_stressor:          CapacityStressor
    capacity_severity:          CapacitySeverity
    recommended_action:         CapacityAction
    account_load_score:         float
    deal_volume_score:          float
    activity_strain_score:      float
    quality_degradation_score:  float
    capacity_composite:         float
    is_overloaded:              bool
    requires_immediate_relief:  bool
    estimated_neglected_pipeline_pct: float
    capacity_signal:            str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "capacity_risk":                    self.capacity_risk.value,
            "capacity_stressor":                self.capacity_stressor.value,
            "capacity_severity":                self.capacity_severity.value,
            "recommended_action":               self.recommended_action.value,
            "account_load_score":               round(self.account_load_score, 1),
            "deal_volume_score":                round(self.deal_volume_score, 1),
            "activity_strain_score":            round(self.activity_strain_score, 1),
            "quality_degradation_score":        round(self.quality_degradation_score, 1),
            "capacity_composite":               round(self.capacity_composite, 1),
            "is_overloaded":                    self.is_overloaded,
            "requires_immediate_relief":        self.requires_immediate_relief,
            "estimated_neglected_pipeline_pct": round(self.estimated_neglected_pipeline_pct, 1),
            "capacity_signal":                  self.capacity_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesRepCapacityOverloadDetector:
    """Detects rep capacity overload to prevent pipeline quality degradation."""

    def __init__(self) -> None:
        self._results: list[RepCapacityResult] = []

    # ── sub-scores (HIGHER = more overload) ─────────────────────────────────

    def _account_load_score(self, inp: RepCapacityInput) -> float:
        score = 0.0
        if inp.benchmark_accounts_per_rep > 0:
            acct_ratio = inp.total_accounts_owned / inp.benchmark_accounts_per_rep
            if acct_ratio >= 2.0:
                score += 50.0
            elif acct_ratio >= 1.5:
                score += 32.0
            elif acct_ratio >= 1.25:
                score += 18.0
            elif acct_ratio >= 1.10:
                score += 8.0
        # Accounts not recently contacted
        if inp.total_accounts_owned > 0:
            neglect_ratio = inp.accounts_not_contacted_last_30d / inp.total_accounts_owned
            if neglect_ratio >= 0.50:
                score += 30.0
            elif neglect_ratio >= 0.30:
                score += 18.0
            elif neglect_ratio >= 0.15:
                score += 8.0
        # Concurrent POC/eval overload
        if inp.concurrent_pocs_count >= 5:
            score += 20.0
        elif inp.concurrent_pocs_count >= 3:
            score += 10.0
        return _clamp(score)

    def _deal_volume_score(self, inp: RepCapacityInput) -> float:
        score = 0.0
        if inp.benchmark_deals_per_rep > 0:
            deal_ratio = inp.active_deals_in_pipeline / inp.benchmark_deals_per_rep
            if deal_ratio >= 2.5:
                score += 50.0
            elif deal_ratio >= 2.0:
                score += 32.0
            elif deal_ratio >= 1.5:
                score += 18.0
            elif deal_ratio >= 1.25:
                score += 8.0
        # Deals not touched recently
        if inp.active_deals_in_pipeline > 0:
            untouched_ratio = inp.deals_not_touched_last_14d / inp.active_deals_in_pipeline
            if untouched_ratio >= 0.5:
                score += 30.0
            elif untouched_ratio >= 0.3:
                score += 18.0
            elif untouched_ratio >= 0.15:
                score += 8.0
        # Overdue CRM tasks
        if inp.crm_tasks_overdue_count >= 10:
            score += 20.0
        elif inp.crm_tasks_overdue_count >= 5:
            score += 12.0
        elif inp.crm_tasks_overdue_count >= 2:
            score += 5.0
        return _clamp(score)

    def _activity_strain_score(self, inp: RepCapacityInput) -> float:
        score = 0.0
        if inp.benchmark_activities_per_month > 0:
            activity_ratio = inp.outbound_activities_last_30d / inp.benchmark_activities_per_month
            # Both over-activity (burnout) and under-activity (neglect) are bad
            if activity_ratio >= 2.0:
                score += 35.0
            elif activity_ratio >= 1.5:
                score += 20.0
            elif activity_ratio <= 0.5:
                score += 30.0
            elif activity_ratio <= 0.7:
                score += 15.0
        # Admin burden eating selling time
        total_hours = inp.admin_hours_per_week + inp.selling_hours_per_week
        if total_hours > 0:
            admin_ratio = inp.admin_hours_per_week / total_hours
            if admin_ratio >= 0.50:
                score += 35.0
            elif admin_ratio >= 0.35:
                score += 20.0
            elif admin_ratio >= 0.25:
                score += 10.0
        # Missed PTO (overwork signal)
        if inp.pto_days_missed_last_90d >= 5:
            score += 30.0
        elif inp.pto_days_missed_last_90d >= 2:
            score += 15.0
        return _clamp(score)

    def _quality_degradation_score(self, inp: RepCapacityInput) -> float:
        score = 0.0
        # Email response rate declining
        if inp.emails_responded_pct < 0.50:
            score += 35.0
        elif inp.emails_responded_pct < 0.70:
            score += 20.0
        elif inp.emails_responded_pct < 0.85:
            score += 8.0
        # Response time too slow
        if inp.avg_response_time_hours >= 48:
            score += 30.0
        elif inp.avg_response_time_hours >= 24:
            score += 18.0
        elif inp.avg_response_time_hours >= 12:
            score += 8.0
        # Deal quality below peers
        if inp.peer_avg_deal_quality_score > 0:
            quality_gap = inp.peer_avg_deal_quality_score - inp.deal_quality_score
            if quality_gap >= 20:
                score += 35.0
            elif quality_gap >= 10:
                score += 20.0
            elif quality_gap >= 5:
                score += 8.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> CapacityRisk:
        if composite < 20:
            return CapacityRisk.low
        if composite < 40:
            return CapacityRisk.moderate
        if composite < 60:
            return CapacityRisk.high
        return CapacityRisk.critical

    def _classify_severity(self, composite: float) -> CapacitySeverity:
        if composite < 20:
            return CapacitySeverity.optimal
        if composite < 40:
            return CapacitySeverity.stretched
        if composite < 60:
            return CapacitySeverity.overloaded
        return CapacitySeverity.critical

    def _classify_stressor(
        self,
        inp: RepCapacityInput,
        account: float,
        deal: float,
        activity: float,
        quality: float,
    ) -> CapacityStressor:
        # Multi-role strain: excessive admin stealing selling time
        if inp.admin_hours_per_week + inp.selling_hours_per_week > 0:
            admin_ratio = inp.admin_hours_per_week / (inp.admin_hours_per_week + inp.selling_hours_per_week)
            if admin_ratio >= 0.45:
                return CapacityStressor.admin_burden
        # Activity overburn: unsustainable outbound pace
        if inp.benchmark_activities_per_month > 0:
            if inp.outbound_activities_last_30d / inp.benchmark_activities_per_month >= 1.8:
                return CapacityStressor.activity_overburn
        # Account overload: too many accounts
        if inp.benchmark_accounts_per_rep > 0:
            if inp.total_accounts_owned / inp.benchmark_accounts_per_rep >= 1.5 and account >= 25:
                return CapacityStressor.account_overload
        # Deal volume excess: too many active deals
        if inp.benchmark_deals_per_rep > 0:
            if inp.active_deals_in_pipeline / inp.benchmark_deals_per_rep >= 1.5 and deal >= 25:
                return CapacityStressor.deal_volume_excess
        # Multi-role: concurrent POCs
        if inp.concurrent_pocs_count >= 4:
            return CapacityStressor.multi_role_strain
        return CapacityStressor.none

    def _recommended_action(
        self, risk: CapacityRisk, composite: float
    ) -> CapacityAction:
        if composite >= 60:
            return CapacityAction.immediate_relief
        if composite >= 50:
            return CapacityAction.hire_support
        if risk == CapacityRisk.high:
            return CapacityAction.account_redistribution
        if risk == CapacityRisk.moderate:
            return CapacityAction.workload_review
        return CapacityAction.no_action

    def _signal(
        self,
        stressor: CapacityStressor,
        composite: float,
        inp: RepCapacityInput,
    ) -> str:
        if stressor == CapacityStressor.none:
            return "Rep workload within healthy capacity parameters"
        msgs = {
            CapacityStressor.admin_burden: (
                f"Admin {inp.admin_hours_per_week:.0f}h/wk — "
                f"selling {inp.selling_hours_per_week:.0f}h/wk — "
                f"{inp.crm_tasks_overdue_count} overdue tasks"
            ),
            CapacityStressor.activity_overburn: (
                f"{inp.outbound_activities_last_30d} activities vs "
                f"{inp.benchmark_activities_per_month} benchmark — "
                f"{inp.pto_days_missed_last_90d}d PTO missed"
            ),
            CapacityStressor.account_overload: (
                f"{inp.total_accounts_owned} accounts vs "
                f"{inp.benchmark_accounts_per_rep} benchmark — "
                f"{inp.accounts_not_contacted_last_30d} not contacted"
            ),
            CapacityStressor.deal_volume_excess: (
                f"{inp.active_deals_in_pipeline} deals vs "
                f"{inp.benchmark_deals_per_rep} benchmark — "
                f"{inp.deals_not_touched_last_14d} untouched 14d+"
            ),
            CapacityStressor.multi_role_strain: (
                f"{inp.concurrent_pocs_count} concurrent POCs — "
                f"deal quality {inp.deal_quality_score:.0f} vs peer avg {inp.peer_avg_deal_quality_score:.0f}"
            ),
        }
        base = msgs.get(stressor, f"capacity composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: RepCapacityInput) -> RepCapacityResult:
        account  = self._account_load_score(inp)
        deal     = self._deal_volume_score(inp)
        activity = self._activity_strain_score(inp)
        quality  = self._quality_degradation_score(inp)

        composite = _clamp(
            account  * 0.30
            + deal    * 0.30
            + activity * 0.25
            + quality  * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        stressor = self._classify_stressor(inp, account, deal, activity, quality)
        action   = self._recommended_action(risk, composite)

        is_overloaded = (
            composite >= 40
            or inp.crm_tasks_overdue_count >= 8
            or (inp.active_deals_in_pipeline > 0 and inp.deals_not_touched_last_14d / inp.active_deals_in_pipeline >= 0.4)
        )
        requires_immediate_relief = (
            composite >= 30
            or inp.emails_responded_pct < 0.5
            or inp.pto_days_missed_last_90d >= 3
        )

        estimated_neglected_pipeline_pct = _clamp(
            (inp.deals_not_touched_last_14d / inp.active_deals_in_pipeline * 100.0)
            if inp.active_deals_in_pipeline > 0 else 0.0
        )

        result = RepCapacityResult(
            rep_id=inp.rep_id,
            region=inp.region,
            capacity_risk=risk,
            capacity_stressor=stressor,
            capacity_severity=severity,
            recommended_action=action,
            account_load_score=account,
            deal_volume_score=deal,
            activity_strain_score=activity,
            quality_degradation_score=quality,
            capacity_composite=composite,
            is_overloaded=is_overloaded,
            requires_immediate_relief=requires_immediate_relief,
            estimated_neglected_pipeline_pct=estimated_neglected_pipeline_pct,
            capacity_signal=self._signal(stressor, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[RepCapacityInput]
    ) -> list[RepCapacityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                               0,
                "risk_counts":                         {},
                "stressor_counts":                     {},
                "severity_counts":                     {},
                "action_counts":                       {},
                "avg_capacity_composite":              0.0,
                "overloaded_count":                    0,
                "immediate_relief_count":              0,
                "avg_account_load_score":              0.0,
                "avg_deal_volume_score":               0.0,
                "avg_activity_strain_score":           0.0,
                "avg_quality_degradation_score":       0.0,
                "avg_estimated_neglected_pipeline_pct": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        stressor_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_acc = total_deal = total_act = total_qual = total_neg = 0.0
        overloaded = relief = 0

        for r in self._results:
            risk_counts[r.capacity_risk.value]       = risk_counts.get(r.capacity_risk.value, 0) + 1
            stressor_counts[r.capacity_stressor.value] = stressor_counts.get(r.capacity_stressor.value, 0) + 1
            severity_counts[r.capacity_severity.value] = severity_counts.get(r.capacity_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.capacity_composite
            total_acc  += r.account_load_score
            total_deal += r.deal_volume_score
            total_act  += r.activity_strain_score
            total_qual += r.quality_degradation_score
            total_neg  += r.estimated_neglected_pipeline_pct
            if r.is_overloaded:
                overloaded += 1
            if r.requires_immediate_relief:
                relief += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "stressor_counts":                      stressor_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_capacity_composite":               round(total_comp / n, 1),
            "overloaded_count":                     overloaded,
            "immediate_relief_count":               relief,
            "avg_account_load_score":               round(total_acc  / n, 1),
            "avg_deal_volume_score":                round(total_deal / n, 1),
            "avg_activity_strain_score":            round(total_act  / n, 1),
            "avg_quality_degradation_score":        round(total_qual / n, 1),
            "avg_estimated_neglected_pipeline_pct": round(total_neg  / n, 1),
        }
