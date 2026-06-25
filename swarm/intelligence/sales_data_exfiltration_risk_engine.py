"""Sales Data Exfiltration Risk Engine — detects behavioral patterns suggesting
a sales rep may be exfiltrating customer data: bulk CRM exports, territory
boundary breaches, after-hours bulk actions, and pre-departure download surges
that expose the company to data theft, compliance violations, and competitor
intelligence transfer."""

from __future__ import annotations

import dataclasses
from enum import Enum


class ExfiltrationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ExfiltrationPattern(str, Enum):
    none                    = "none"
    bulk_export             = "bulk_export"
    territory_boundary_breach = "territory_boundary_breach"
    unusual_access_hours    = "unusual_access_hours"
    account_scraping        = "account_scraping"
    pre_departure_download  = "pre_departure_download"


class ExfiltrationSeverity(str, Enum):
    normal     = "normal"
    suspicious = "suspicious"
    concerning = "concerning"
    threat     = "threat"


class ExfiltrationAction(str, Enum):
    no_action              = "no_action"
    audit_trail_review     = "audit_trail_review"
    access_restriction     = "access_restriction"
    security_investigation = "security_investigation"
    immediate_lockdown     = "immediate_lockdown"


@dataclasses.dataclass
class SalesDataExfiltrationInput:
    rep_id:                             str
    region:                             str
    evaluation_period_id:               str
    crm_export_count_last_30d:          int
    crm_export_count_prior_30d:         int
    records_exported_last_30d:          int
    records_exported_prior_30d:         int
    off_hours_access_count:             int
    accounts_accessed_outside_territory: int
    new_account_views_not_in_pipeline:  int
    bulk_contact_download_count:        int
    failed_access_attempts:             int
    admin_impersonation_attempts:       int
    data_copy_to_personal_storage_alerts: int
    crm_api_calls_last_30d:             int
    crm_api_calls_prior_30d:            int
    resignation_signal_days_ago:        int
    competitor_domain_email_access:     int
    avg_session_duration_minutes:       float
    unusual_report_run_count:           int
    territory_violation_count:          int
    after_hours_bulk_action_count:      int


@dataclasses.dataclass
class SalesDataExfiltrationResult:
    rep_id:                        str
    region:                        str
    exfiltration_risk:             ExfiltrationRisk
    exfiltration_pattern:          ExfiltrationPattern
    exfiltration_severity:         ExfiltrationSeverity
    recommended_action:            ExfiltrationAction
    export_anomaly_score:          float
    access_pattern_score:          float
    boundary_violation_score:      float
    behavioral_risk_score:         float
    exfiltration_composite:        float
    is_exfiltration_risk:          bool
    requires_immediate_review:     bool
    estimated_records_at_risk:     int
    exfiltration_signal:           str

    def to_dict(self) -> dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "exfiltration_risk":             self.exfiltration_risk.value,
            "exfiltration_pattern":          self.exfiltration_pattern.value,
            "exfiltration_severity":         self.exfiltration_severity.value,
            "recommended_action":            self.recommended_action.value,
            "export_anomaly_score":          round(self.export_anomaly_score, 1),
            "access_pattern_score":          round(self.access_pattern_score, 1),
            "boundary_violation_score":      round(self.boundary_violation_score, 1),
            "behavioral_risk_score":         round(self.behavioral_risk_score, 1),
            "exfiltration_composite":        round(self.exfiltration_composite, 1),
            "is_exfiltration_risk":          self.is_exfiltration_risk,
            "requires_immediate_review":     self.requires_immediate_review,
            "estimated_records_at_risk":     self.estimated_records_at_risk,
            "exfiltration_signal":           self.exfiltration_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesDataExfiltrationRiskEngine:
    """Detects data exfiltration patterns in sales rep CRM behavior to protect
    customer data and prevent competitive intelligence transfer."""

    def __init__(self) -> None:
        self._results: list[SalesDataExfiltrationResult] = []

    # ── sub-scores (HIGHER = more exfiltration risk) ─────────────────────────

    def _export_anomaly_score(self, inp: SalesDataExfiltrationInput) -> float:
        score = 0.0
        # CRM export surge vs baseline
        if inp.crm_export_count_prior_30d > 0:
            export_ratio = inp.crm_export_count_last_30d / inp.crm_export_count_prior_30d
            if export_ratio >= 5.0:
                score += 45.0
            elif export_ratio >= 3.0:
                score += 30.0
            elif export_ratio >= 2.0:
                score += 15.0
        elif inp.crm_export_count_last_30d >= 5:
            score += 25.0
        # Records exported surge
        if inp.records_exported_prior_30d > 0:
            rec_ratio = inp.records_exported_last_30d / inp.records_exported_prior_30d
            if rec_ratio >= 5.0:
                score += 30.0
            elif rec_ratio >= 3.0:
                score += 18.0
            elif rec_ratio >= 2.0:
                score += 8.0
        elif inp.records_exported_last_30d >= 500:
            score += 20.0
        # Bulk contact downloads
        if inp.bulk_contact_download_count >= 5:
            score += 25.0
        elif inp.bulk_contact_download_count >= 2:
            score += 15.0
        elif inp.bulk_contact_download_count >= 1:
            score += 8.0
        return _clamp(score)

    def _access_pattern_score(self, inp: SalesDataExfiltrationInput) -> float:
        score = 0.0
        # Off-hours access (evenings/weekends in bulk)
        if inp.off_hours_access_count >= 15:
            score += 35.0
        elif inp.off_hours_access_count >= 8:
            score += 20.0
        elif inp.off_hours_access_count >= 4:
            score += 10.0
        # After-hours bulk actions (most dangerous)
        if inp.after_hours_bulk_action_count >= 5:
            score += 40.0
        elif inp.after_hours_bulk_action_count >= 2:
            score += 25.0
        elif inp.after_hours_bulk_action_count >= 1:
            score += 12.0
        # Unusual report runs (exploratory data gathering)
        if inp.unusual_report_run_count >= 8:
            score += 20.0
        elif inp.unusual_report_run_count >= 4:
            score += 10.0
        elif inp.unusual_report_run_count >= 2:
            score += 5.0
        # Long sessions (bulk scraping)
        if inp.avg_session_duration_minutes >= 240:
            score += 15.0
        elif inp.avg_session_duration_minutes >= 120:
            score += 7.0
        return _clamp(score)

    def _boundary_violation_score(self, inp: SalesDataExfiltrationInput) -> float:
        score = 0.0
        # Accounts outside territory (unauthorized access)
        if inp.accounts_accessed_outside_territory >= 20:
            score += 40.0
        elif inp.accounts_accessed_outside_territory >= 10:
            score += 25.0
        elif inp.accounts_accessed_outside_territory >= 5:
            score += 12.0
        elif inp.accounts_accessed_outside_territory >= 2:
            score += 6.0
        # Territory violation events (policy breaches)
        if inp.territory_violation_count >= 10:
            score += 30.0
        elif inp.territory_violation_count >= 5:
            score += 18.0
        elif inp.territory_violation_count >= 2:
            score += 8.0
        # New account views not in pipeline (fishing)
        if inp.new_account_views_not_in_pipeline >= 30:
            score += 25.0
        elif inp.new_account_views_not_in_pipeline >= 15:
            score += 14.0
        elif inp.new_account_views_not_in_pipeline >= 5:
            score += 6.0
        # Failed access attempts (probing security boundaries)
        if inp.failed_access_attempts >= 10:
            score += 15.0
        elif inp.failed_access_attempts >= 5:
            score += 8.0
        return _clamp(score)

    def _behavioral_risk_score(self, inp: SalesDataExfiltrationInput) -> float:
        score = 0.0
        # Admin impersonation (critical security event)
        if inp.admin_impersonation_attempts >= 2:
            score += 50.0
        elif inp.admin_impersonation_attempts >= 1:
            score += 30.0
        # Personal storage alerts
        if inp.data_copy_to_personal_storage_alerts >= 3:
            score += 40.0
        elif inp.data_copy_to_personal_storage_alerts >= 1:
            score += 25.0
        # Competitor domain email access (intel sharing signal)
        if inp.competitor_domain_email_access >= 3:
            score += 30.0
        elif inp.competitor_domain_email_access >= 1:
            score += 18.0
        # Resignation signal with elevated activity (pre-departure)
        if 0 < inp.resignation_signal_days_ago <= 30:
            score += 20.0
        elif 0 < inp.resignation_signal_days_ago <= 60:
            score += 10.0
        # API call surge (automated scraping)
        if inp.crm_api_calls_prior_30d > 0:
            api_ratio = inp.crm_api_calls_last_30d / inp.crm_api_calls_prior_30d
            if api_ratio >= 5.0:
                score += 15.0
            elif api_ratio >= 3.0:
                score += 8.0
        elif inp.crm_api_calls_last_30d >= 100:
            score += 10.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> ExfiltrationRisk:
        if composite < 20:
            return ExfiltrationRisk.low
        if composite < 40:
            return ExfiltrationRisk.moderate
        if composite < 60:
            return ExfiltrationRisk.high
        return ExfiltrationRisk.critical

    def _classify_severity(self, composite: float) -> ExfiltrationSeverity:
        if composite < 20:
            return ExfiltrationSeverity.normal
        if composite < 40:
            return ExfiltrationSeverity.suspicious
        if composite < 60:
            return ExfiltrationSeverity.concerning
        return ExfiltrationSeverity.threat

    def _classify_pattern(
        self,
        inp: SalesDataExfiltrationInput,
        export: float,
        access: float,
        boundary: float,
        behavioral: float,
    ) -> ExfiltrationPattern:
        # Pre-departure download: resignation signal + high export
        if inp.resignation_signal_days_ago > 0 and (export >= 20 or inp.bulk_contact_download_count >= 2):
            return ExfiltrationPattern.pre_departure_download
        # Admin impersonation or personal storage = critical behavioral
        if inp.admin_impersonation_attempts >= 1 or inp.data_copy_to_personal_storage_alerts >= 1:
            return ExfiltrationPattern.account_scraping
        # Bulk export pattern
        if export >= 30:
            return ExfiltrationPattern.bulk_export
        # Unusual hours bulk actions
        if access >= 30 and inp.after_hours_bulk_action_count >= 2:
            return ExfiltrationPattern.unusual_access_hours
        # Territory boundary violations
        if boundary >= 25:
            return ExfiltrationPattern.territory_boundary_breach
        return ExfiltrationPattern.none

    def _recommended_action(
        self, risk: ExfiltrationRisk, composite: float, behavioral: float
    ) -> ExfiltrationAction:
        if composite >= 60 or behavioral >= 50:
            return ExfiltrationAction.immediate_lockdown
        if composite >= 50 or behavioral >= 30:
            return ExfiltrationAction.security_investigation
        if risk == ExfiltrationRisk.high:
            return ExfiltrationAction.access_restriction
        if risk == ExfiltrationRisk.moderate:
            return ExfiltrationAction.audit_trail_review
        return ExfiltrationAction.no_action

    def _signal(
        self,
        pattern: ExfiltrationPattern,
        composite: float,
        inp: SalesDataExfiltrationInput,
    ) -> str:
        if pattern == ExfiltrationPattern.none:
            return "CRM access behavior within normal parameters"
        msgs = {
            ExfiltrationPattern.pre_departure_download: (
                f"Resignation signal {inp.resignation_signal_days_ago}d ago — "
                f"{inp.records_exported_last_30d} records exported — "
                f"{inp.bulk_contact_download_count} bulk downloads"
            ),
            ExfiltrationPattern.account_scraping: (
                f"{inp.admin_impersonation_attempts} admin impersonation attempt(s) — "
                f"{inp.data_copy_to_personal_storage_alerts} personal storage alert(s)"
            ),
            ExfiltrationPattern.bulk_export: (
                f"{inp.crm_export_count_last_30d} CRM exports — "
                f"{inp.records_exported_last_30d} records — "
                f"{inp.bulk_contact_download_count} bulk downloads"
            ),
            ExfiltrationPattern.unusual_access_hours: (
                f"{inp.after_hours_bulk_action_count} after-hours bulk action(s) — "
                f"{inp.off_hours_access_count} off-hours sessions"
            ),
            ExfiltrationPattern.territory_boundary_breach: (
                f"{inp.accounts_accessed_outside_territory} accounts outside territory — "
                f"{inp.territory_violation_count} violation(s)"
            ),
        }
        base = msgs.get(pattern, f"exfiltration composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SalesDataExfiltrationInput) -> SalesDataExfiltrationResult:
        export    = self._export_anomaly_score(inp)
        access    = self._access_pattern_score(inp)
        boundary  = self._boundary_violation_score(inp)
        behavioral = self._behavioral_risk_score(inp)

        composite = _clamp(
            export     * 0.30
            + access   * 0.25
            + boundary * 0.25
            + behavioral * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, export, access, boundary, behavioral)
        action   = self._recommended_action(risk, composite, behavioral)

        is_exfiltration_risk = (
            composite >= 40
            or inp.admin_impersonation_attempts >= 1
            or inp.data_copy_to_personal_storage_alerts >= 2
        )
        requires_immediate_review = (
            composite >= 30
            or inp.admin_impersonation_attempts >= 1
            or inp.competitor_domain_email_access >= 2
            or (inp.resignation_signal_days_ago > 0 and inp.bulk_contact_download_count >= 1)
        )

        estimated_records_at_risk = int(
            inp.records_exported_last_30d
            + inp.new_account_views_not_in_pipeline * 10
            + inp.accounts_accessed_outside_territory * 5
        )

        result = SalesDataExfiltrationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            exfiltration_risk=risk,
            exfiltration_pattern=pattern,
            exfiltration_severity=severity,
            recommended_action=action,
            export_anomaly_score=export,
            access_pattern_score=access,
            boundary_violation_score=boundary,
            behavioral_risk_score=behavioral,
            exfiltration_composite=composite,
            is_exfiltration_risk=is_exfiltration_risk,
            requires_immediate_review=requires_immediate_review,
            estimated_records_at_risk=estimated_records_at_risk,
            exfiltration_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SalesDataExfiltrationInput]
    ) -> list[SalesDataExfiltrationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                          0,
                "risk_counts":                    {},
                "pattern_counts":                 {},
                "severity_counts":                {},
                "action_counts":                  {},
                "avg_exfiltration_composite":     0.0,
                "exfiltration_risk_count":        0,
                "immediate_review_count":         0,
                "avg_export_anomaly_score":       0.0,
                "avg_access_pattern_score":       0.0,
                "avg_boundary_violation_score":   0.0,
                "avg_behavioral_risk_score":      0.0,
                "total_estimated_records_at_risk": 0,
            }

        risk_counts:    dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_comp = total_exp = total_acc = total_bnd = total_beh = 0.0
        total_rec = 0
        exfil = review = 0

        for r in self._results:
            risk_counts[r.exfiltration_risk.value]       = risk_counts.get(r.exfiltration_risk.value, 0) + 1
            pattern_counts[r.exfiltration_pattern.value] = pattern_counts.get(r.exfiltration_pattern.value, 0) + 1
            severity_counts[r.exfiltration_severity.value] = severity_counts.get(r.exfiltration_severity.value, 0) + 1
            action_counts[r.recommended_action.value]    = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.exfiltration_composite
            total_exp  += r.export_anomaly_score
            total_acc  += r.access_pattern_score
            total_bnd  += r.boundary_violation_score
            total_beh  += r.behavioral_risk_score
            total_rec  += r.estimated_records_at_risk
            if r.is_exfiltration_risk:
                exfil += 1
            if r.requires_immediate_review:
                review += 1

        n = len(self._results)
        return {
            "total":                           n,
            "risk_counts":                     risk_counts,
            "pattern_counts":                  pattern_counts,
            "severity_counts":                 severity_counts,
            "action_counts":                   action_counts,
            "avg_exfiltration_composite":      round(total_comp / n, 1),
            "exfiltration_risk_count":         exfil,
            "immediate_review_count":          review,
            "avg_export_anomaly_score":        round(total_exp  / n, 1),
            "avg_access_pattern_score":        round(total_acc  / n, 1),
            "avg_boundary_violation_score":    round(total_bnd  / n, 1),
            "avg_behavioral_risk_score":       round(total_beh  / n, 1),
            "total_estimated_records_at_risk": total_rec,
        }
