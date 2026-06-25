from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict


class MultithreadRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MultithreadPattern(str, Enum):
    none                    = "none"
    single_contact_dependency = "single_contact_dependency"
    champion_only_reliance  = "champion_only_reliance"
    executive_bypass        = "executive_bypass"
    org_chart_blind         = "org_chart_blind"
    breadth_shallow         = "breadth_shallow"


class MultithreadSeverity(str, Enum):
    networked  = "networked"
    adequate   = "adequate"
    shallow    = "shallow"
    isolated   = "isolated"


class MultithreadAction(str, Enum):
    no_action                          = "no_action"
    stakeholder_mapping_coaching       = "stakeholder_mapping_coaching"
    champion_diversification_coaching  = "champion_diversification_coaching"
    executive_access_coaching          = "executive_access_coaching"
    organization_navigation_coaching   = "organization_navigation_coaching"
    multithread_intervention           = "multithread_intervention"
    deal_at_risk_intervention          = "deal_at_risk_intervention"


@dataclass
class MultithreadInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    avg_contacts_per_active_deal:        float   # e.g. 2.5
    single_contact_deal_rate_pct:        float   # 0-1
    champion_only_reliance_pct:          float   # 0-1
    executive_engaged_rate_pct:          float   # 0-1
    economic_buyer_direct_contact_pct:   float   # 0-1
    referral_from_champion_to_exec_pct:  float   # 0-1
    multi_dept_engaged_rate_pct:         float   # 0-1
    org_chart_mapped_pct:                float   # 0-1
    technical_buyer_engaged_pct:         float   # 0-1
    user_buyer_engaged_pct:              float   # 0-1
    legal_procurement_early_engaged_pct: float   # 0-1
    new_stakeholder_added_per_deal_avg:  float   # count
    deal_sponsor_count_avg:              float   # count
    champion_churn_impacted_deals_pct:   float   # 0-1
    lost_due_single_thread_pct:          float   # 0-1
    multi_sponsor_deals_win_rate_pct:    float   # 0-1
    org_breadth_score_avg:               float   # 0-1
    total_active_deals:                  int
    avg_opportunity_value_usd:           float


@dataclass
class MultithreadResult:
    rep_id:                             str
    region:                             str
    multithread_risk:                   MultithreadRisk
    multithread_pattern:                MultithreadPattern
    multithread_severity:               MultithreadSeverity
    recommended_action:                 MultithreadAction
    depth_score:                        float
    breadth_score:                      float
    executive_access_score:             float
    risk_exposure_score:                float
    multithread_composite:              float
    has_multithread_gap:                bool
    requires_multithread_coaching:      bool
    estimated_deal_risk_usd:            float
    multithread_signal:                 str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "multithread_risk":             self.multithread_risk.value,
            "multithread_pattern":          self.multithread_pattern.value,
            "multithread_severity":         self.multithread_severity.value,
            "recommended_action":           self.recommended_action.value,
            "depth_score":                  self.depth_score,
            "breadth_score":                self.breadth_score,
            "executive_access_score":       self.executive_access_score,
            "risk_exposure_score":          self.risk_exposure_score,
            "multithread_composite":        self.multithread_composite,
            "has_multithread_gap":          self.has_multithread_gap,
            "requires_multithread_coaching": self.requires_multithread_coaching,
            "estimated_deal_risk_usd":      self.estimated_deal_risk_usd,
            "multithread_signal":           self.multithread_signal,
        }


class SalesMultiThreadingIntelligenceEngine:
    """Detects per-rep stakeholder coverage gaps — single-thread dependency, executive bypass, and org blindness."""

    def __init__(self) -> None:
        self._results: List[MultithreadResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _depth_score(self, inp: MultithreadInput) -> float:
        s = 0.0
        if   inp.avg_contacts_per_active_deal <= 1.5: s += 40
        elif inp.avg_contacts_per_active_deal <= 2.0: s += 22
        elif inp.avg_contacts_per_active_deal <= 2.5: s += 8
        if   inp.single_contact_deal_rate_pct >= 0.60: s += 35
        elif inp.single_contact_deal_rate_pct >= 0.40: s += 18
        if   inp.champion_only_reliance_pct   >= 0.70: s += 25
        elif inp.champion_only_reliance_pct   >= 0.50: s += 12
        return min(s, 100.0)

    def _breadth_score(self, inp: MultithreadInput) -> float:
        s = 0.0
        if   inp.multi_dept_engaged_rate_pct <= 0.25: s += 40
        elif inp.multi_dept_engaged_rate_pct <= 0.45: s += 22
        elif inp.multi_dept_engaged_rate_pct <= 0.65: s += 8
        if   inp.org_chart_mapped_pct        <= 0.20: s += 35
        elif inp.org_chart_mapped_pct        <= 0.40: s += 18
        if   inp.technical_buyer_engaged_pct <= 0.30: s += 25
        elif inp.technical_buyer_engaged_pct <= 0.50: s += 12
        return min(s, 100.0)

    def _executive_access_score(self, inp: MultithreadInput) -> float:
        s = 0.0
        if   inp.executive_engaged_rate_pct           <= 0.20: s += 45
        elif inp.executive_engaged_rate_pct           <= 0.40: s += 25
        elif inp.executive_engaged_rate_pct           <= 0.60: s += 10
        if   inp.economic_buyer_direct_contact_pct    <= 0.25: s += 30
        elif inp.economic_buyer_direct_contact_pct    <= 0.50: s += 15
        if   inp.referral_from_champion_to_exec_pct   <= 0.15: s += 25
        elif inp.referral_from_champion_to_exec_pct   <= 0.30: s += 12
        return min(s, 100.0)

    def _risk_exposure_score(self, inp: MultithreadInput) -> float:
        s = 0.0
        if   inp.champion_churn_impacted_deals_pct >= 0.30: s += 40
        elif inp.champion_churn_impacted_deals_pct >= 0.15: s += 22
        elif inp.champion_churn_impacted_deals_pct >= 0.05: s += 8
        if   inp.lost_due_single_thread_pct        >= 0.30: s += 35
        elif inp.lost_due_single_thread_pct        >= 0.15: s += 18
        if   inp.deal_sponsor_count_avg            <= 1.0:  s += 25
        elif inp.deal_sponsor_count_avg            <= 1.5:  s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, d: float, b: float, e: float, r: float) -> float:
        return min(round(d * 0.35 + b * 0.30 + e * 0.20 + r * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: MultithreadInput) -> MultithreadPattern:
        if inp.single_contact_deal_rate_pct >= 0.55 and inp.avg_contacts_per_active_deal <= 1.5:
            return MultithreadPattern.single_contact_dependency
        if inp.champion_only_reliance_pct >= 0.65 and inp.executive_engaged_rate_pct <= 0.25:
            return MultithreadPattern.champion_only_reliance
        if inp.executive_engaged_rate_pct <= 0.20 and inp.economic_buyer_direct_contact_pct <= 0.20:
            return MultithreadPattern.executive_bypass
        if inp.org_chart_mapped_pct <= 0.15 and inp.multi_dept_engaged_rate_pct <= 0.25:
            return MultithreadPattern.org_chart_blind
        if inp.new_stakeholder_added_per_deal_avg <= 0.5 and inp.org_breadth_score_avg <= 0.30:
            return MultithreadPattern.breadth_shallow
        return MultithreadPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> MultithreadRisk:
        if   composite >= 60: return MultithreadRisk.critical
        elif composite >= 40: return MultithreadRisk.high
        elif composite >= 20: return MultithreadRisk.moderate
        return MultithreadRisk.low

    def _severity(self, composite: float) -> MultithreadSeverity:
        if   composite >= 60: return MultithreadSeverity.isolated
        elif composite >= 40: return MultithreadSeverity.shallow
        elif composite >= 20: return MultithreadSeverity.adequate
        return MultithreadSeverity.networked

    def _action(self, risk: MultithreadRisk, pattern: MultithreadPattern) -> MultithreadAction:
        if risk == MultithreadRisk.critical:
            if pattern == MultithreadPattern.single_contact_dependency:
                return MultithreadAction.deal_at_risk_intervention
            if pattern == MultithreadPattern.champion_only_reliance:
                return MultithreadAction.deal_at_risk_intervention
            return MultithreadAction.multithread_intervention
        if risk == MultithreadRisk.high:
            if pattern == MultithreadPattern.executive_bypass:
                return MultithreadAction.executive_access_coaching
            if pattern == MultithreadPattern.org_chart_blind:
                return MultithreadAction.organization_navigation_coaching
            if pattern == MultithreadPattern.breadth_shallow:
                return MultithreadAction.stakeholder_mapping_coaching
            return MultithreadAction.champion_diversification_coaching
        if risk == MultithreadRisk.moderate:
            return MultithreadAction.stakeholder_mapping_coaching
        return MultithreadAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: MultithreadInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.single_contact_deal_rate_pct >= 0.45
            or inp.champion_only_reliance_pct   >= 0.55
        )

    def _requires_coaching(self, inp: MultithreadInput, composite: float) -> bool:
        return (
            composite >= 30
            or inp.avg_contacts_per_active_deal <= 2.0
            or inp.executive_engaged_rate_pct   <= 0.35
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _deal_risk(self, inp: MultithreadInput, composite: float) -> float:
        return round(
            inp.total_active_deals
            * inp.avg_opportunity_value_usd
            * inp.single_contact_deal_rate_pct
            * (composite / 100),
            2,
        )

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        MultithreadPattern.single_contact_dependency: "Single contact dependency",
        MultithreadPattern.champion_only_reliance:    "Champion-only reliance",
        MultithreadPattern.executive_bypass:          "Executive bypass",
        MultithreadPattern.org_chart_blind:           "Org chart blind",
        MultithreadPattern.breadth_shallow:           "Breadth shallow",
    }

    def _signal(self, inp: MultithreadInput, pattern: MultithreadPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Multi-threading strong — stakeholder depth, org breadth, "
                "and executive access within benchmarks"
            )
        label = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        contacts   = f"{inp.avg_contacts_per_active_deal:.1f}"
        single_pct = round(inp.single_contact_deal_rate_pct * 100)
        exec_pct   = round(inp.executive_engaged_rate_pct * 100)
        comp_int   = round(composite)
        return (
            f"{label} — {contacts} avg contacts/deal — "
            f"{single_pct}% single-contact deals — "
            f"{exec_pct}% exec engaged — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: MultithreadInput) -> MultithreadResult:
        d  = self._depth_score(inp)
        b  = self._breadth_score(inp)
        e  = self._executive_access_score(inp)
        r  = self._risk_exposure_score(inp)
        comp = self._composite(d, b, e, r)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = MultithreadResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            multithread_risk            = risk,
            multithread_pattern         = pattern,
            multithread_severity        = severity,
            recommended_action          = action,
            depth_score                 = d,
            breadth_score               = b,
            executive_access_score      = e,
            risk_exposure_score         = r,
            multithread_composite       = comp,
            has_multithread_gap         = self._has_gap(inp, comp),
            requires_multithread_coaching = self._requires_coaching(inp, comp),
            estimated_deal_risk_usd     = self._deal_risk(inp, comp),
            multithread_signal          = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[MultithreadInput]) -> List[MultithreadResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_multithread_composite": 0.0,
                "multithread_gap_count": 0,
                "coaching_count": 0,
                "avg_depth_score": 0.0,
                "avg_breadth_score": 0.0,
                "avg_executive_access_score": 0.0,
                "avg_risk_exposure_score": 0.0,
                "total_estimated_deal_risk_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_d = total_b = total_e = total_r = total_risk = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.multithread_risk.value]     = risk_counts.get(res.multithread_risk.value, 0) + 1
            pattern_counts[res.multithread_pattern.value] = pattern_counts.get(res.multithread_pattern.value, 0) + 1
            severity_counts[res.multithread_severity.value] = severity_counts.get(res.multithread_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.multithread_composite
            total_d    += res.depth_score
            total_b    += res.breadth_score
            total_e    += res.executive_access_score
            total_r    += res.risk_exposure_score
            total_risk += res.estimated_deal_risk_usd
            if res.has_multithread_gap:        gap_count      += 1
            if res.requires_multithread_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                          n,
            "risk_counts":                    risk_counts,
            "pattern_counts":                 pattern_counts,
            "severity_counts":                severity_counts,
            "action_counts":                  action_counts,
            "avg_multithread_composite":      round(total_comp / n, 1),
            "multithread_gap_count":          gap_count,
            "coaching_count":                 coaching_count,
            "avg_depth_score":                round(total_d / n, 1),
            "avg_breadth_score":              round(total_b / n, 1),
            "avg_executive_access_score":     round(total_e / n, 1),
            "avg_risk_exposure_score":        round(total_r / n, 1),
            "total_estimated_deal_risk_usd":  round(total_risk, 2),
        }
