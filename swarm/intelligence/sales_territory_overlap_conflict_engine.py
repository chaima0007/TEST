"""Sales Territory Overlap Conflict Engine — detects when multiple reps compete for
the same accounts causing channel conflict, double-commission risk, and pipeline
duplication that inflates forecasts and damages customer experience."""

from __future__ import annotations

import dataclasses
from enum import Enum


class OverlapRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class OverlapPattern(str, Enum):
    none                    = "none"
    dual_rep_same_account   = "dual_rep_same_account"
    territory_boundary_blur = "territory_boundary_blur"
    channel_partner_conflict = "channel_partner_conflict"
    segment_spillover       = "segment_spillover"
    acquisition_overlap     = "acquisition_overlap"


class OverlapSeverity(str, Enum):
    clean     = "clean"
    watch     = "watch"
    contested = "contested"
    conflict  = "conflict"


class OverlapAction(str, Enum):
    no_action              = "no_action"
    account_reassignment   = "account_reassignment"
    territory_review       = "territory_review"
    manager_mediation      = "manager_mediation"
    executive_arbitration  = "executive_arbitration"


@dataclasses.dataclass
class TerritoryOverlapInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    accounts_shared_with_other_reps:     int
    total_accounts_owned:                int
    pipeline_overlap_usd:                float
    total_pipeline_usd:                  float
    dual_rep_deals_count:                int
    channel_partner_overlap_count:       int
    cross_segment_activity_count:        int
    territory_violation_flags:           int
    disputed_account_count:              int
    commission_dispute_count:            int
    overlap_escalations_last_90d:        int
    accounts_outside_primary_segment:    int
    total_segment_accounts:              int
    boundary_crossing_score:             float
    partner_conflict_score:              float
    avg_deal_value_overlapped_usd:       float
    avg_deal_value_clean_usd:            float
    repeat_overlap_accounts:             int
    manager_override_needed_count:       int


@dataclasses.dataclass
class TerritoryOverlapResult:
    rep_id:                          str
    region:                          str
    overlap_risk:                    OverlapRisk
    overlap_pattern:                 OverlapPattern
    overlap_severity:                OverlapSeverity
    recommended_action:              OverlapAction
    account_collision_score:         float
    pipeline_duplication_score:      float
    channel_conflict_score:          float
    boundary_integrity_score:        float
    overlap_composite:               float
    is_territory_conflict:           bool
    requires_arbitration:            bool
    estimated_at_risk_pipeline_usd:  float
    overlap_signal:                  str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "overlap_risk":                   self.overlap_risk.value,
            "overlap_pattern":                self.overlap_pattern.value,
            "overlap_severity":               self.overlap_severity.value,
            "recommended_action":             self.recommended_action.value,
            "account_collision_score":        round(self.account_collision_score, 1),
            "pipeline_duplication_score":     round(self.pipeline_duplication_score, 1),
            "channel_conflict_score":         round(self.channel_conflict_score, 1),
            "boundary_integrity_score":       round(self.boundary_integrity_score, 1),
            "overlap_composite":              round(self.overlap_composite, 1),
            "is_territory_conflict":          self.is_territory_conflict,
            "requires_arbitration":           self.requires_arbitration,
            "estimated_at_risk_pipeline_usd": round(self.estimated_at_risk_pipeline_usd, 2),
            "overlap_signal":                 self.overlap_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesTerritoryOverlapConflictEngine:
    """Detects territory overlap conflicts to protect pipeline integrity and customer experience."""

    def __init__(self) -> None:
        self._results: list[TerritoryOverlapResult] = []

    # ── sub-scores (HIGHER = more conflict risk) ─────────────────────────────

    def _account_collision_score(self, inp: TerritoryOverlapInput) -> float:
        score = 0.0
        # Shared account ratio
        if inp.total_accounts_owned > 0:
            shared_ratio = inp.accounts_shared_with_other_reps / inp.total_accounts_owned
            if shared_ratio >= 0.5:
                score += 45.0
            elif shared_ratio >= 0.3:
                score += 28.0
            elif shared_ratio >= 0.15:
                score += 15.0
            elif shared_ratio >= 0.05:
                score += 6.0
        # Disputed accounts
        if inp.disputed_account_count >= 5:
            score += 30.0
        elif inp.disputed_account_count >= 3:
            score += 18.0
        elif inp.disputed_account_count >= 1:
            score += 8.0
        # Repeat overlap accounts (systemic problem)
        if inp.repeat_overlap_accounts >= 3:
            score += 25.0
        elif inp.repeat_overlap_accounts >= 1:
            score += 12.0
        return _clamp(score)

    def _pipeline_duplication_score(self, inp: TerritoryOverlapInput) -> float:
        score = 0.0
        # Pipeline overlap ratio
        if inp.total_pipeline_usd > 0:
            overlap_ratio = inp.pipeline_overlap_usd / inp.total_pipeline_usd
            if overlap_ratio >= 0.5:
                score += 50.0
            elif overlap_ratio >= 0.3:
                score += 32.0
            elif overlap_ratio >= 0.15:
                score += 18.0
            elif overlap_ratio >= 0.05:
                score += 8.0
        # Dual-rep deals (two reps actively working same deal)
        if inp.dual_rep_deals_count >= 4:
            score += 30.0
        elif inp.dual_rep_deals_count >= 2:
            score += 18.0
        elif inp.dual_rep_deals_count >= 1:
            score += 8.0
        # Commission disputes (direct financial impact)
        if inp.commission_dispute_count >= 3:
            score += 20.0
        elif inp.commission_dispute_count >= 1:
            score += 10.0
        return _clamp(score)

    def _channel_conflict_score(self, inp: TerritoryOverlapInput) -> float:
        score = 0.0
        # Channel partner overlap
        if inp.channel_partner_overlap_count >= 5:
            score += 40.0
        elif inp.channel_partner_overlap_count >= 3:
            score += 25.0
        elif inp.channel_partner_overlap_count >= 1:
            score += 12.0
        # Partner conflict score from external signals
        if inp.partner_conflict_score >= 70:
            score += 35.0
        elif inp.partner_conflict_score >= 40:
            score += 20.0
        elif inp.partner_conflict_score >= 20:
            score += 10.0
        # Segment spillover
        if inp.total_segment_accounts > 0:
            spill_ratio = inp.accounts_outside_primary_segment / inp.total_segment_accounts
            if spill_ratio >= 0.3:
                score += 25.0
            elif spill_ratio >= 0.15:
                score += 14.0
            elif spill_ratio >= 0.05:
                score += 6.0
        return _clamp(score)

    def _boundary_integrity_score(self, inp: TerritoryOverlapInput) -> float:
        score = 0.0
        # Territory violation flags
        if inp.territory_violation_flags >= 5:
            score += 45.0
        elif inp.territory_violation_flags >= 3:
            score += 28.0
        elif inp.territory_violation_flags >= 1:
            score += 12.0
        # Boundary crossing raw score
        if inp.boundary_crossing_score >= 70:
            score += 30.0
        elif inp.boundary_crossing_score >= 40:
            score += 18.0
        elif inp.boundary_crossing_score >= 20:
            score += 8.0
        # Manager overrides needed (management overhead)
        if inp.manager_override_needed_count >= 4:
            score += 25.0
        elif inp.manager_override_needed_count >= 2:
            score += 14.0
        elif inp.manager_override_needed_count >= 1:
            score += 6.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> OverlapRisk:
        if composite < 20:
            return OverlapRisk.low
        if composite < 40:
            return OverlapRisk.moderate
        if composite < 60:
            return OverlapRisk.high
        return OverlapRisk.critical

    def _classify_severity(self, composite: float) -> OverlapSeverity:
        if composite < 20:
            return OverlapSeverity.clean
        if composite < 40:
            return OverlapSeverity.watch
        if composite < 60:
            return OverlapSeverity.contested
        return OverlapSeverity.conflict

    def _classify_pattern(
        self,
        inp: TerritoryOverlapInput,
        account: float,
        pipeline: float,
        channel: float,
        boundary: float,
    ) -> OverlapPattern:
        # Acquisition overlap: two reps both claiming same recently acquired account
        if inp.repeat_overlap_accounts >= 3 and pipeline >= 30:
            return OverlapPattern.acquisition_overlap
        # Dual-rep on same account: active two-rep competition
        if inp.dual_rep_deals_count >= 2 and inp.commission_dispute_count >= 1:
            return OverlapPattern.dual_rep_same_account
        # Channel partner conflict: partner vs direct conflict
        if inp.channel_partner_overlap_count >= 3 and channel >= 25:
            return OverlapPattern.channel_partner_conflict
        # Territory boundary blur: rep repeatedly crossing territory lines
        if inp.territory_violation_flags >= 3 and boundary >= 20:
            return OverlapPattern.territory_boundary_blur
        # Segment spillover: rep drifting into wrong customer segment
        if inp.total_segment_accounts > 0:
            if inp.accounts_outside_primary_segment / inp.total_segment_accounts >= 0.15:
                return OverlapPattern.segment_spillover
        return OverlapPattern.none

    def _recommended_action(
        self, risk: OverlapRisk, composite: float
    ) -> OverlapAction:
        if composite >= 60:
            return OverlapAction.executive_arbitration
        if composite >= 50:
            return OverlapAction.manager_mediation
        if risk == OverlapRisk.high:
            return OverlapAction.territory_review
        if risk == OverlapRisk.moderate:
            return OverlapAction.account_reassignment
        return OverlapAction.no_action

    def _signal(
        self,
        pattern: OverlapPattern,
        composite: float,
        inp: TerritoryOverlapInput,
    ) -> str:
        if pattern == OverlapPattern.none:
            return "Territory boundaries respected — no conflict detected"
        msgs = {
            OverlapPattern.acquisition_overlap: (
                f"{inp.repeat_overlap_accounts} repeat overlap accounts — "
                f"${inp.pipeline_overlap_usd:,.0f} pipeline at risk"
            ),
            OverlapPattern.dual_rep_same_account: (
                f"{inp.dual_rep_deals_count} dual-rep deals — "
                f"{inp.commission_dispute_count} commission disputes"
            ),
            OverlapPattern.channel_partner_conflict: (
                f"{inp.channel_partner_overlap_count} partner conflicts — "
                f"partner score {inp.partner_conflict_score:.0f}"
            ),
            OverlapPattern.territory_boundary_blur: (
                f"{inp.territory_violation_flags} violation flags — "
                f"{inp.disputed_account_count} disputed accounts"
            ),
            OverlapPattern.segment_spillover: (
                f"{inp.accounts_outside_primary_segment} accounts outside segment — "
                f"{inp.cross_segment_activity_count} cross-segment activities"
            ),
        }
        base = msgs.get(pattern, f"overlap composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: TerritoryOverlapInput) -> TerritoryOverlapResult:
        account  = self._account_collision_score(inp)
        pipeline = self._pipeline_duplication_score(inp)
        channel  = self._channel_conflict_score(inp)
        boundary = self._boundary_integrity_score(inp)

        composite = _clamp(
            account  * 0.30
            + pipeline * 0.30
            + channel  * 0.25
            + boundary * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, account, pipeline, channel, boundary)
        action   = self._recommended_action(risk, composite)

        is_territory_conflict = (
            composite >= 40
            or inp.commission_dispute_count >= 2
            or inp.disputed_account_count >= 3
        )
        requires_arbitration = (
            composite >= 30
            or inp.overlap_escalations_last_90d >= 2
            or inp.manager_override_needed_count >= 3
        )

        if inp.total_pipeline_usd > 0:
            overlap_ratio = inp.pipeline_overlap_usd / inp.total_pipeline_usd
        else:
            overlap_ratio = 0.0
        estimated_at_risk_pipeline_usd = inp.pipeline_overlap_usd * (composite / 100.0)

        result = TerritoryOverlapResult(
            rep_id=inp.rep_id,
            region=inp.region,
            overlap_risk=risk,
            overlap_pattern=pattern,
            overlap_severity=severity,
            recommended_action=action,
            account_collision_score=account,
            pipeline_duplication_score=pipeline,
            channel_conflict_score=channel,
            boundary_integrity_score=boundary,
            overlap_composite=composite,
            is_territory_conflict=is_territory_conflict,
            requires_arbitration=requires_arbitration,
            estimated_at_risk_pipeline_usd=estimated_at_risk_pipeline_usd,
            overlap_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[TerritoryOverlapInput]
    ) -> list[TerritoryOverlapResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                               0,
                "risk_counts":                         {},
                "pattern_counts":                      {},
                "severity_counts":                     {},
                "action_counts":                       {},
                "avg_overlap_composite":               0.0,
                "territory_conflict_count":            0,
                "arbitration_count":                   0,
                "avg_account_collision_score":         0.0,
                "avg_pipeline_duplication_score":      0.0,
                "avg_channel_conflict_score":          0.0,
                "avg_boundary_integrity_score":        0.0,
                "total_estimated_at_risk_pipeline_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_acc = total_pip = total_ch = total_bnd = 0.0
        conflict = arb = 0
        total_at_risk = 0.0

        for r in self._results:
            risk_counts[r.overlap_risk.value]       = risk_counts.get(r.overlap_risk.value, 0) + 1
            pattern_counts[r.overlap_pattern.value] = pattern_counts.get(r.overlap_pattern.value, 0) + 1
            severity_counts[r.overlap_severity.value] = severity_counts.get(r.overlap_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.overlap_composite
            total_acc   += r.account_collision_score
            total_pip   += r.pipeline_duplication_score
            total_ch    += r.channel_conflict_score
            total_bnd   += r.boundary_integrity_score
            total_at_risk += r.estimated_at_risk_pipeline_usd
            if r.is_territory_conflict:
                conflict += 1
            if r.requires_arbitration:
                arb += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_overlap_composite":                round(total_comp / n, 1),
            "territory_conflict_count":             conflict,
            "arbitration_count":                    arb,
            "avg_account_collision_score":          round(total_acc  / n, 1),
            "avg_pipeline_duplication_score":       round(total_pip  / n, 1),
            "avg_channel_conflict_score":           round(total_ch   / n, 1),
            "avg_boundary_integrity_score":         round(total_bnd  / n, 1),
            "total_estimated_at_risk_pipeline_usd": round(total_at_risk, 2),
        }
