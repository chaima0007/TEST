from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ChampionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ChampionPattern(str, Enum):
    none                  = "none"
    single_thread_exposed = "single_thread_exposed"
    ghost_risk_zone       = "ghost_risk_zone"
    org_change_vulnerable = "org_change_vulnerable"
    advocacy_collapse     = "advocacy_collapse"
    blind_spot_account    = "blind_spot_account"


class ChampionSeverity(str, Enum):
    stable      = "stable"
    drifting    = "drifting"
    vulnerable  = "vulnerable"
    critical    = "critical"


class ChampionAction(str, Enum):
    no_action                        = "no_action"
    champion_health_monitoring       = "champion_health_monitoring"
    multithreading_urgency_coaching  = "multithreading_urgency_coaching"
    org_change_alert_protocol        = "org_change_alert_protocol"
    executive_engagement_activation  = "executive_engagement_activation"
    stakeholder_mapping_sprint       = "stakeholder_mapping_sprint"
    relationship_rescue_intervention = "relationship_rescue_intervention"
    deal_continuity_escalation       = "deal_continuity_escalation"


@dataclass
class ChampionInput:
    rep_id:                                   str
    region:                                   str
    evaluation_period_id:                     str
    champion_engagement_drop_rate_pct:        float   # 0-1 (% accounts where champion engagement dropped >30%)
    champion_response_latency_trend:          float   # 0-1 (normalized trend, 1=severely worsening)
    org_change_detected_rate_pct:             float   # 0-1 (% accounts with detected org changes)
    champion_linkedin_activity_drop_pct:      float   # 0-1 (% accounts where champion LinkedIn activity dropped)
    single_threaded_deal_rate_pct:            float   # 0-1 (% deals with only 1 contact)
    backup_contact_coverage_rate_pct:         float   # 0-1 (% accounts with ≥2 contacts)
    executive_sponsor_coverage_rate_pct:      float   # 0-1 (% deals with exec sponsor)
    champion_internal_advocacy_score:         float   # 0-1 (how actively champion promotes internally)
    champion_tenure_avg_months:               float   # avg tenure of champions in role
    stakeholder_mapping_completeness_score:   float   # 0-1
    champion_deal_influence_score:            float   # 0-1 (how much champion drives deal outcome)
    internal_coach_coverage_rate_pct:         float   # 0-1 (% deals with internal coach identified)
    economic_buyer_direct_access_rate_pct:    float   # 0-1 (% deals with EB direct access)
    champion_replacement_recovery_rate_pct:   float   # 0-1 (% of lost champion deals recovered)
    deal_ghosting_after_champion_loss_rate_pct: float # 0-1 (% deals that go dark after champion change)
    relationship_breadth_score:               float   # 0-1 (avg unique contacts per account)
    champion_departure_detected_deals:        int     # deals affected this period
    total_active_deals:                       int
    avg_deal_value_usd:                       float


@dataclass
class ChampionResult:
    rep_id:                         str
    region:                         str
    champion_risk:                  ChampionRisk
    champion_pattern:               ChampionPattern
    champion_severity:              ChampionSeverity
    recommended_action:             ChampionAction
    stability_score:                float
    coverage_score:                 float
    resilience_score:               float
    intelligence_score:             float
    champion_composite:             float
    has_champion_gap:               bool
    requires_champion_intervention: bool
    estimated_at_risk_pipeline_usd: float
    champion_signal:                str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "champion_risk":                   self.champion_risk.value,
            "champion_pattern":                self.champion_pattern.value,
            "champion_severity":               self.champion_severity.value,
            "recommended_action":              self.recommended_action.value,
            "stability_score":                 self.stability_score,
            "coverage_score":                  self.coverage_score,
            "resilience_score":                self.resilience_score,
            "intelligence_score":              self.intelligence_score,
            "champion_composite":              self.champion_composite,
            "has_champion_gap":                self.has_champion_gap,
            "requires_champion_intervention":  self.requires_champion_intervention,
            "estimated_at_risk_pipeline_usd":  self.estimated_at_risk_pipeline_usd,
            "champion_signal":                 self.champion_signal,
        }


class SalesChampionDepartureRelationshipContinuityEngine:
    """Detects champion departure risk — reps with single-threaded deals, declining engagement, and no backup contacts."""

    def __init__(self) -> None:
        self._results: List[ChampionResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _stability_score(self, inp: ChampionInput) -> float:
        s = 0.0
        if   inp.champion_engagement_drop_rate_pct >= 0.55: s += 40
        elif inp.champion_engagement_drop_rate_pct >= 0.30: s += 22
        elif inp.champion_engagement_drop_rate_pct >= 0.15: s += 8
        if   inp.org_change_detected_rate_pct      >= 0.40: s += 35
        elif inp.org_change_detected_rate_pct      >= 0.20: s += 18
        if   inp.champion_tenure_avg_months        <= 6:    s += 25
        elif inp.champion_tenure_avg_months        <= 12:   s += 12
        return min(s, 100.0)

    def _coverage_score(self, inp: ChampionInput) -> float:
        s = 0.0
        if   inp.single_threaded_deal_rate_pct          >= 0.65: s += 45
        elif inp.single_threaded_deal_rate_pct          >= 0.40: s += 25
        elif inp.single_threaded_deal_rate_pct          >= 0.20: s += 10
        if   inp.backup_contact_coverage_rate_pct       <= 0.25: s += 30
        elif inp.backup_contact_coverage_rate_pct       <= 0.50: s += 15
        if   inp.executive_sponsor_coverage_rate_pct    <= 0.20: s += 25
        elif inp.executive_sponsor_coverage_rate_pct    <= 0.45: s += 12
        return min(s, 100.0)

    def _resilience_score(self, inp: ChampionInput) -> float:
        s = 0.0
        if   inp.champion_replacement_recovery_rate_pct <= 0.15: s += 40
        elif inp.champion_replacement_recovery_rate_pct <= 0.35: s += 22
        elif inp.champion_replacement_recovery_rate_pct <= 0.55: s += 8
        if   inp.deal_ghosting_after_champion_loss_rate_pct >= 0.55: s += 35
        elif inp.deal_ghosting_after_champion_loss_rate_pct >= 0.30: s += 18
        if   inp.internal_coach_coverage_rate_pct          <= 0.20: s += 25
        elif inp.internal_coach_coverage_rate_pct          <= 0.45: s += 12
        return min(s, 100.0)

    def _intelligence_score(self, inp: ChampionInput) -> float:
        s = 0.0
        if   inp.stakeholder_mapping_completeness_score <= 0.20: s += 45
        elif inp.stakeholder_mapping_completeness_score <= 0.45: s += 25
        elif inp.stakeholder_mapping_completeness_score <= 0.65: s += 10
        if   inp.relationship_breadth_score             <= 0.20: s += 30
        elif inp.relationship_breadth_score             <= 0.45: s += 15
        if   inp.economic_buyer_direct_access_rate_pct  <= 0.20: s += 25
        elif inp.economic_buyer_direct_access_rate_pct  <= 0.45: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, st: float, co: float, re: float, in_: float) -> float:
        return min(round(st * 0.30 + co * 0.25 + re * 0.25 + in_ * 0.20, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: ChampionInput) -> ChampionPattern:
        if inp.single_threaded_deal_rate_pct >= 0.60 and inp.backup_contact_coverage_rate_pct <= 0.25:
            return ChampionPattern.single_thread_exposed
        if inp.deal_ghosting_after_champion_loss_rate_pct >= 0.55 and inp.champion_replacement_recovery_rate_pct <= 0.20:
            return ChampionPattern.ghost_risk_zone
        if inp.org_change_detected_rate_pct >= 0.35 and inp.champion_tenure_avg_months <= 12:
            return ChampionPattern.org_change_vulnerable
        if inp.champion_internal_advocacy_score <= 0.25 and inp.champion_deal_influence_score >= 0.70:
            return ChampionPattern.advocacy_collapse
        if inp.stakeholder_mapping_completeness_score <= 0.25 and inp.relationship_breadth_score <= 0.30:
            return ChampionPattern.blind_spot_account
        return ChampionPattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> ChampionRisk:
        if   composite >= 60: return ChampionRisk.critical
        elif composite >= 40: return ChampionRisk.high
        elif composite >= 20: return ChampionRisk.moderate
        return ChampionRisk.low

    def _severity(self, composite: float) -> ChampionSeverity:
        if   composite >= 60: return ChampionSeverity.critical
        elif composite >= 40: return ChampionSeverity.vulnerable
        elif composite >= 20: return ChampionSeverity.drifting
        return ChampionSeverity.stable

    def _action(self, risk: ChampionRisk, pattern: ChampionPattern) -> ChampionAction:
        if risk == ChampionRisk.critical:
            if pattern in (ChampionPattern.single_thread_exposed, ChampionPattern.ghost_risk_zone):
                return ChampionAction.deal_continuity_escalation
            return ChampionAction.relationship_rescue_intervention
        if risk == ChampionRisk.high:
            if pattern == ChampionPattern.single_thread_exposed:
                return ChampionAction.multithreading_urgency_coaching
            if pattern == ChampionPattern.ghost_risk_zone:
                return ChampionAction.relationship_rescue_intervention
            if pattern == ChampionPattern.org_change_vulnerable:
                return ChampionAction.org_change_alert_protocol
            if pattern == ChampionPattern.advocacy_collapse:
                return ChampionAction.executive_engagement_activation
            if pattern == ChampionPattern.blind_spot_account:
                return ChampionAction.stakeholder_mapping_sprint
            return ChampionAction.multithreading_urgency_coaching
        if risk == ChampionRisk.moderate:
            return ChampionAction.champion_health_monitoring
        return ChampionAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: ChampionInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.single_threaded_deal_rate_pct >= 0.40
            or inp.champion_engagement_drop_rate_pct >= 0.30
        )

    def _requires_intervention(self, inp: ChampionInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.backup_contact_coverage_rate_pct <= 0.50
            or inp.deal_ghosting_after_champion_loss_rate_pct >= 0.25
        )

    # ── pipeline at risk ──────────────────────────────────────────────────────

    def _pipeline_at_risk(self, inp: ChampionInput, composite: float) -> float:
        return round(
            inp.champion_departure_detected_deals
            * inp.avg_deal_value_usd
            * inp.deal_ghosting_after_champion_loss_rate_pct
            * (composite / 100),
            2
        )

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        ChampionPattern.single_thread_exposed: "Single-thread exposed",
        ChampionPattern.ghost_risk_zone:       "Ghost risk zone",
        ChampionPattern.org_change_vulnerable: "Org change vulnerable",
        ChampionPattern.advocacy_collapse:     "Advocacy collapse",
        ChampionPattern.blind_spot_account:    "Blind spot account",
    }

    def _signal(self, inp: ChampionInput, pattern: ChampionPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Champion relationships stable — multithreading, engagement, and "
                "stakeholder coverage within benchmark targets"
            )
        label      = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        single_pct = round(inp.single_threaded_deal_rate_pct * 100)
        drop_pct   = round(inp.champion_engagement_drop_rate_pct * 100)
        ghost_pct  = round(inp.deal_ghosting_after_champion_loss_rate_pct * 100)
        comp_int   = round(composite)
        return (
            f"{label} — {single_pct}% single-threaded — {drop_pct}% engagement drop — "
            f"{ghost_pct}% ghosted after champion loss — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: ChampionInput) -> ChampionResult:
        st  = self._stability_score(inp)
        co  = self._coverage_score(inp)
        re  = self._resilience_score(inp)
        in_ = self._intelligence_score(inp)
        comp = self._composite(st, co, re, in_)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = ChampionResult(
            rep_id                         = inp.rep_id,
            region                         = inp.region,
            champion_risk                  = risk,
            champion_pattern               = pattern,
            champion_severity              = severity,
            recommended_action             = action,
            stability_score                = st,
            coverage_score                 = co,
            resilience_score               = re,
            intelligence_score             = in_,
            champion_composite             = comp,
            has_champion_gap               = self._has_gap(inp, comp),
            requires_champion_intervention = self._requires_intervention(inp, comp),
            estimated_at_risk_pipeline_usd = self._pipeline_at_risk(inp, comp),
            champion_signal                = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ChampionInput]) -> List[ChampionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                                0,
                "risk_counts":                          {},
                "pattern_counts":                       {},
                "severity_counts":                      {},
                "action_counts":                        {},
                "avg_champion_composite":               0.0,
                "champion_gap_count":                   0,
                "intervention_count":                   0,
                "avg_stability_score":                  0.0,
                "avg_coverage_score":                   0.0,
                "avg_resilience_score":                 0.0,
                "avg_intelligence_score":               0.0,
                "total_estimated_at_risk_pipeline_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_st = total_co = total_re = total_in = total_ar = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.champion_risk.value]        = risk_counts.get(res.champion_risk.value, 0) + 1
            pattern_counts[res.champion_pattern.value]  = pattern_counts.get(res.champion_pattern.value, 0) + 1
            severity_counts[res.champion_severity.value]= severity_counts.get(res.champion_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.champion_composite
            total_st   += res.stability_score
            total_co   += res.coverage_score
            total_re   += res.resilience_score
            total_in   += res.intelligence_score
            total_ar   += res.estimated_at_risk_pipeline_usd
            if res.has_champion_gap:               gap_count          += 1
            if res.requires_champion_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_champion_composite":               round(total_comp / n, 1),
            "champion_gap_count":                   gap_count,
            "intervention_count":                   intervention_count,
            "avg_stability_score":                  round(total_st / n, 1),
            "avg_coverage_score":                   round(total_co / n, 1),
            "avg_resilience_score":                 round(total_re / n, 1),
            "avg_intelligence_score":               round(total_in / n, 1),
            "total_estimated_at_risk_pipeline_usd": round(total_ar, 2),
        }
