from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ProposalRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ProposalPattern(str, Enum):
    none                = "none"
    premature_proposer  = "premature_proposer"
    template_lazy       = "template_lazy"
    ghosted_proposer    = "ghosted_proposer"
    revision_looper     = "revision_looper"
    orphaned_proposal   = "orphaned_proposal"


class ProposalSeverity(str, Enum):
    converting   = "converting"
    softening    = "softening"
    stalling     = "stalling"
    collapsing   = "collapsing"


class ProposalAction(str, Enum):
    no_action                    = "no_action"
    proposal_quality_monitoring  = "proposal_quality_monitoring"
    customization_coaching       = "customization_coaching"
    discovery_gate_enforcement   = "discovery_gate_enforcement"
    engagement_reactivation_coaching = "engagement_reactivation_coaching"
    deal_desk_proposal_support   = "deal_desk_proposal_support"
    champion_alignment_coaching  = "champion_alignment_coaching"
    proposal_quality_coaching    = "proposal_quality_coaching"
    proposal_strategy_intervention = "proposal_strategy_intervention"
    proposal_framework_redesign  = "proposal_framework_redesign"


@dataclass
class ProposalInput:
    rep_id:                                    str
    region:                                    str
    evaluation_period_id:                      str
    proposal_to_close_rate_pct:                float   # 0-1
    proposal_sent_without_discovery_rate_pct:  float   # 0-1 (% sent before full discovery)
    avg_days_to_send_proposal:                 float   # avg days from opp creation to proposal
    proposal_revision_count_avg:               float   # avg number of proposal revisions per deal
    executive_sponsor_present_in_proposal_pct: float   # 0-1 (% with exec sponsor aligned)
    proposal_customization_score:              float   # 0-1 (template vs bespoke)
    value_articulation_score:                  float   # 0-1 (how well value is expressed)
    competitive_differentiation_score:         float   # 0-1
    pricing_structure_complexity_score:        float   # 0-1 (high = overcomplicated)
    proposal_response_time_days:               float   # avg days for prospect to respond
    unanswered_proposal_rate_pct:              float   # 0-1 (% with no response)
    proposal_reused_template_rate_pct:         float   # 0-1 (% using same template)
    mutual_success_plan_inclusion_rate_pct:    float   # 0-1 (% with MAP)
    roi_case_included_rate_pct:                float   # 0-1 (% with ROI/business case)
    legal_redline_rate_pct:                    float   # 0-1 (% requiring legal redlines)
    multi_stakeholder_proposal_rate_pct:       float   # 0-1 (% sent to >1 stakeholder)
    proposal_champion_alignment_score:         float   # 0-1
    total_proposals_sent:                      int
    avg_deal_value_usd:                        float


@dataclass
class ProposalResult:
    rep_id:                      str
    region:                      str
    proposal_risk:               ProposalRisk
    proposal_pattern:            ProposalPattern
    proposal_severity:           ProposalSeverity
    recommended_action:          ProposalAction
    quality_score:               float
    readiness_score:             float
    execution_score:             float
    alignment_score:             float
    proposal_composite:          float
    has_proposal_gap:            bool
    requires_proposal_coaching:  bool
    estimated_deal_loss_usd:     float
    proposal_signal:             str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                     self.rep_id,
            "region":                     self.region,
            "proposal_risk":              self.proposal_risk.value,
            "proposal_pattern":           self.proposal_pattern.value,
            "proposal_severity":          self.proposal_severity.value,
            "recommended_action":         self.recommended_action.value,
            "quality_score":              self.quality_score,
            "readiness_score":            self.readiness_score,
            "execution_score":            self.execution_score,
            "alignment_score":            self.alignment_score,
            "proposal_composite":         self.proposal_composite,
            "has_proposal_gap":           self.has_proposal_gap,
            "requires_proposal_coaching": self.requires_proposal_coaching,
            "estimated_deal_loss_usd":    self.estimated_deal_loss_usd,
            "proposal_signal":            self.proposal_signal,
        }


class SalesProposalQualityWinRateIntelligenceEngine:
    """Detects proposal quality collapse — reps who spray generic proposals before discovery and watch them go unanswered."""

    def __init__(self) -> None:
        self._results: List[ProposalResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _quality_score(self, inp: ProposalInput) -> float:
        s = 0.0
        if   inp.proposal_customization_score <= 0.20: s += 40
        elif inp.proposal_customization_score <= 0.45: s += 22
        elif inp.proposal_customization_score <= 0.65: s += 8
        if   inp.value_articulation_score     <= 0.25: s += 35
        elif inp.value_articulation_score     <= 0.55: s += 18
        if   inp.roi_case_included_rate_pct   <= 0.30: s += 25
        elif inp.roi_case_included_rate_pct   <= 0.55: s += 12
        return min(s, 100.0)

    def _readiness_score(self, inp: ProposalInput) -> float:
        s = 0.0
        if   inp.proposal_sent_without_discovery_rate_pct  >= 0.55: s += 40
        elif inp.proposal_sent_without_discovery_rate_pct  >= 0.30: s += 22
        elif inp.proposal_sent_without_discovery_rate_pct  >= 0.15: s += 8
        if   inp.executive_sponsor_present_in_proposal_pct <= 0.20: s += 35
        elif inp.executive_sponsor_present_in_proposal_pct <= 0.45: s += 18
        if   inp.mutual_success_plan_inclusion_rate_pct    <= 0.20: s += 25
        elif inp.mutual_success_plan_inclusion_rate_pct    <= 0.45: s += 12
        return min(s, 100.0)

    def _execution_score(self, inp: ProposalInput) -> float:
        s = 0.0
        if   inp.unanswered_proposal_rate_pct  >= 0.50: s += 45
        elif inp.unanswered_proposal_rate_pct  >= 0.30: s += 25
        elif inp.unanswered_proposal_rate_pct  >= 0.15: s += 10
        if   inp.proposal_revision_count_avg   >= 5.0:  s += 30
        elif inp.proposal_revision_count_avg   >= 3.0:  s += 15
        if   inp.avg_days_to_send_proposal     >= 21:   s += 25
        elif inp.avg_days_to_send_proposal     >= 10:   s += 12
        return min(s, 100.0)

    def _alignment_score(self, inp: ProposalInput) -> float:
        s = 0.0
        if   inp.proposal_champion_alignment_score     <= 0.20: s += 45
        elif inp.proposal_champion_alignment_score     <= 0.45: s += 25
        elif inp.proposal_champion_alignment_score     <= 0.65: s += 10
        if   inp.multi_stakeholder_proposal_rate_pct   <= 0.20: s += 30
        elif inp.multi_stakeholder_proposal_rate_pct   <= 0.45: s += 15
        if   inp.competitive_differentiation_score     <= 0.20: s += 25
        elif inp.competitive_differentiation_score     <= 0.50: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, qu: float, re: float, ex: float, al: float) -> float:
        return min(round(qu * 0.30 + re * 0.25 + ex * 0.25 + al * 0.20, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: ProposalInput) -> ProposalPattern:
        if inp.proposal_sent_without_discovery_rate_pct >= 0.50 and inp.avg_days_to_send_proposal <= 5:
            return ProposalPattern.premature_proposer
        if inp.proposal_reused_template_rate_pct >= 0.60 and inp.proposal_customization_score <= 0.30:
            return ProposalPattern.template_lazy
        if inp.unanswered_proposal_rate_pct >= 0.45 and inp.proposal_response_time_days >= 14:
            return ProposalPattern.ghosted_proposer
        if inp.proposal_revision_count_avg >= 4.0 and inp.legal_redline_rate_pct >= 0.35:
            return ProposalPattern.revision_looper
        if inp.executive_sponsor_present_in_proposal_pct <= 0.20 and inp.proposal_champion_alignment_score <= 0.30:
            return ProposalPattern.orphaned_proposal
        return ProposalPattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> ProposalRisk:
        if   composite >= 60: return ProposalRisk.critical
        elif composite >= 40: return ProposalRisk.high
        elif composite >= 20: return ProposalRisk.moderate
        return ProposalRisk.low

    def _severity(self, composite: float) -> ProposalSeverity:
        if   composite >= 60: return ProposalSeverity.collapsing
        elif composite >= 40: return ProposalSeverity.stalling
        elif composite >= 20: return ProposalSeverity.softening
        return ProposalSeverity.converting

    def _action(self, risk: ProposalRisk, pattern: ProposalPattern) -> ProposalAction:
        if risk == ProposalRisk.critical:
            if pattern in (ProposalPattern.premature_proposer, ProposalPattern.template_lazy):
                return ProposalAction.proposal_framework_redesign
            return ProposalAction.proposal_strategy_intervention
        if risk == ProposalRisk.high:
            if pattern == ProposalPattern.premature_proposer:
                return ProposalAction.discovery_gate_enforcement
            if pattern == ProposalPattern.template_lazy:
                return ProposalAction.customization_coaching
            if pattern == ProposalPattern.ghosted_proposer:
                return ProposalAction.engagement_reactivation_coaching
            if pattern == ProposalPattern.revision_looper:
                return ProposalAction.deal_desk_proposal_support
            if pattern == ProposalPattern.orphaned_proposal:
                return ProposalAction.champion_alignment_coaching
            return ProposalAction.proposal_quality_coaching
        if risk == ProposalRisk.moderate:
            return ProposalAction.proposal_quality_monitoring
        return ProposalAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: ProposalInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.proposal_to_close_rate_pct <= 0.25
            or inp.unanswered_proposal_rate_pct >= 0.30
        )

    def _requires_coaching(self, inp: ProposalInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.proposal_sent_without_discovery_rate_pct >= 0.30
            or inp.proposal_customization_score <= 0.50
        )

    # ── deal loss estimate ────────────────────────────────────────────────────

    def _deal_loss_estimate(self, inp: ProposalInput, composite: float) -> float:
        return round(
            inp.total_proposals_sent
            * inp.avg_deal_value_usd
            * (1.0 - inp.proposal_to_close_rate_pct)
            * (composite / 100),
            2
        )

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        ProposalPattern.premature_proposer: "Premature proposer",
        ProposalPattern.template_lazy:      "Template lazy",
        ProposalPattern.ghosted_proposer:   "Ghosted proposer",
        ProposalPattern.revision_looper:    "Revision looper",
        ProposalPattern.orphaned_proposal:  "Orphaned proposal",
    }

    def _signal(self, inp: ProposalInput, pattern: ProposalPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Proposal quality and win rate healthy — customization, discovery readiness, "
                "and champion alignment within benchmark targets"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        close_pct = round(inp.proposal_to_close_rate_pct * 100)
        ghost_pct = round(inp.unanswered_proposal_rate_pct * 100)
        custom_pct = round(inp.proposal_customization_score * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {close_pct}% proposals close — {ghost_pct}% unanswered — "
            f"{custom_pct}% customization score — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: ProposalInput) -> ProposalResult:
        qu = self._quality_score(inp)
        re = self._readiness_score(inp)
        ex = self._execution_score(inp)
        al = self._alignment_score(inp)
        comp = self._composite(qu, re, ex, al)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = ProposalResult(
            rep_id                     = inp.rep_id,
            region                     = inp.region,
            proposal_risk              = risk,
            proposal_pattern           = pattern,
            proposal_severity          = severity,
            recommended_action         = action,
            quality_score              = qu,
            readiness_score            = re,
            execution_score            = ex,
            alignment_score            = al,
            proposal_composite         = comp,
            has_proposal_gap           = self._has_gap(inp, comp),
            requires_proposal_coaching = self._requires_coaching(inp, comp),
            estimated_deal_loss_usd    = self._deal_loss_estimate(inp, comp),
            proposal_signal            = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ProposalInput]) -> List[ProposalResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                            0,
                "risk_counts":                      {},
                "pattern_counts":                   {},
                "severity_counts":                  {},
                "action_counts":                    {},
                "avg_proposal_composite":           0.0,
                "proposal_gap_count":               0,
                "coaching_count":                   0,
                "avg_quality_score":                0.0,
                "avg_readiness_score":              0.0,
                "avg_execution_score":              0.0,
                "avg_alignment_score":              0.0,
                "total_estimated_deal_loss_usd":    0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_qu = total_re = total_ex = total_al = total_dl = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.proposal_risk.value]         = risk_counts.get(res.proposal_risk.value, 0) + 1
            pattern_counts[res.proposal_pattern.value]   = pattern_counts.get(res.proposal_pattern.value, 0) + 1
            severity_counts[res.proposal_severity.value] = severity_counts.get(res.proposal_severity.value, 0) + 1
            action_counts[res.recommended_action.value]  = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.proposal_composite
            total_qu   += res.quality_score
            total_re   += res.readiness_score
            total_ex   += res.execution_score
            total_al   += res.alignment_score
            total_dl   += res.estimated_deal_loss_usd
            if res.has_proposal_gap:           gap_count      += 1
            if res.requires_proposal_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                         n,
            "risk_counts":                   risk_counts,
            "pattern_counts":                pattern_counts,
            "severity_counts":               severity_counts,
            "action_counts":                 action_counts,
            "avg_proposal_composite":        round(total_comp / n, 1),
            "proposal_gap_count":            gap_count,
            "coaching_count":                coaching_count,
            "avg_quality_score":             round(total_qu / n, 1),
            "avg_readiness_score":           round(total_re / n, 1),
            "avg_execution_score":           round(total_ex / n, 1),
            "avg_alignment_score":           round(total_al / n, 1),
            "total_estimated_deal_loss_usd": round(total_dl, 2),
        }
