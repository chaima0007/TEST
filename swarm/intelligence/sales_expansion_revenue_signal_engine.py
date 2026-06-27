"""
Module 220 — Sales Expansion Revenue Signal Engine
Identifies upsell and cross-sell opportunities within existing accounts
by detecting usage ceiling, product gap, engagement elevation and
executive alignment signals.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ExpansionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ExpansionPattern(str, Enum):
    none                   = "none"
    usage_ceiling_breach   = "usage_ceiling_breach"
    product_gap_signal     = "product_gap_signal"
    engagement_elevation   = "engagement_elevation"
    executive_pull_through = "executive_pull_through"
    contract_white_space   = "contract_white_space"


class ExpansionSeverity(str, Enum):
    dormant    = "dormant"
    emerging   = "emerging"
    active     = "active"
    urgent     = "urgent"


class ExpansionAction(str, Enum):
    no_action                    = "no_action"
    expansion_monitoring         = "expansion_monitoring"
    qbr_expansion_pitch          = "qbr_expansion_pitch"
    product_gap_discovery_call   = "product_gap_discovery_call"
    executive_expansion_briefing = "executive_expansion_briefing"
    usage_ceiling_upsell         = "usage_ceiling_upsell"
    cross_sell_campaign          = "cross_sell_campaign"
    white_space_mapping_session  = "white_space_mapping_session"
    expansion_fast_track         = "expansion_fast_track"


@dataclass
class ExpansionInput:
    account_id: str
    region: str
    evaluation_period_id: str
    # Usage ceiling signals
    license_utilization_pct: float          # % of licensed seats/units actively used
    feature_depth_score_pct: float          # % of available features used deeply
    api_call_growth_rate_pct: float         # % MoM growth in API/integration calls
    storage_utilization_pct: float          # % of contracted storage used
    # Product gap signals
    adjacent_product_fit_score: float       # 0-1 (1 = adjacent products perfectly fit needs)
    competitor_displacement_pct: float      # % of competitive tools that could be replaced
    integration_gap_count: int             # number of integrations customer wants but lacks
    feature_request_frequency: int         # feature requests in last 90 days
    # Engagement elevation signals
    power_user_pct: float                  # % of users qualifying as power users
    nps_score: float                       # current NPS (0-100 scale)
    executive_engagement_score: float      # 0-1 (1 = very engaged executives)
    expansion_conversation_initiated: float # 0-1 (1 = rep has opened expansion convo)
    # Relationship & contract signals
    champion_advocacy_score: float         # 0-1 (1 = champion actively promotes)
    stakeholder_growth_count: int          # net new stakeholders added this period
    contract_renewal_months: int           # months until next renewal
    upsell_budget_confirmed: float         # 0-1 (1 = budget confirmed for expansion)
    # Volume context
    current_arr_usd: float                 # current ARR
    potential_expansion_arr_usd: float     # identified expansion ARR potential
    account_tenure_months: int            # months as customer


@dataclass
class ExpansionResult:
    account_id: str
    region: str
    expansion_risk: str
    expansion_pattern: str
    expansion_severity: str
    recommended_action: str
    usage_ceiling_score: float
    product_gap_score: float
    engagement_score: float
    relationship_score: float
    expansion_composite: float
    has_expansion_signal: bool
    requires_executive_engagement: bool
    estimated_expansion_arr_usd: float
    expansion_signal: str

    def to_dict(self) -> Dict:
        return {
            "account_id":                   self.account_id,
            "region":                       self.region,
            "expansion_risk":               self.expansion_risk,
            "expansion_pattern":            self.expansion_pattern,
            "expansion_severity":           self.expansion_severity,
            "recommended_action":           self.recommended_action,
            "usage_ceiling_score":          self.usage_ceiling_score,
            "product_gap_score":            self.product_gap_score,
            "engagement_score":             self.engagement_score,
            "relationship_score":           self.relationship_score,
            "expansion_composite":          self.expansion_composite,
            "has_expansion_signal":         self.has_expansion_signal,
            "requires_executive_engagement": self.requires_executive_engagement,
            "estimated_expansion_arr_usd":  self.estimated_expansion_arr_usd,
            "expansion_signal":             self.expansion_signal,
        }


class SalesExpansionRevenueSignalEngine:
    def __init__(self) -> None:
        self._results: List[ExpansionResult] = []

    def _usage_ceiling_score(self, i: ExpansionInput) -> float:
        s = 0
        if   i.license_utilization_pct   >= 0.90: s += 40
        elif i.license_utilization_pct   >= 0.75: s += 22
        elif i.license_utilization_pct   >= 0.60: s += 8

        if   i.api_call_growth_rate_pct  >= 0.30: s += 35
        elif i.api_call_growth_rate_pct  >= 0.15: s += 18
        elif i.api_call_growth_rate_pct  >= 0.05: s += 6

        if   i.storage_utilization_pct   >= 0.85: s += 25
        elif i.storage_utilization_pct   >= 0.65: s += 12
        return min(s, 100)

    def _product_gap_score(self, i: ExpansionInput) -> float:
        s = 0
        if   i.adjacent_product_fit_score  >= 0.80: s += 40
        elif i.adjacent_product_fit_score  >= 0.60: s += 22
        elif i.adjacent_product_fit_score  >= 0.40: s += 8

        if   i.integration_gap_count       >= 5:    s += 35
        elif i.integration_gap_count       >= 3:    s += 18
        elif i.integration_gap_count       >= 1:    s += 6

        if   i.competitor_displacement_pct >= 0.50: s += 25
        elif i.competitor_displacement_pct >= 0.30: s += 12
        return min(s, 100)

    def _engagement_score(self, i: ExpansionInput) -> float:
        s = 0
        if   i.power_user_pct              >= 0.40: s += 45
        elif i.power_user_pct              >= 0.25: s += 25
        elif i.power_user_pct              >= 0.12: s += 10

        if   i.nps_score                   >= 70:   s += 30
        elif i.nps_score                   >= 50:   s += 15

        if   i.executive_engagement_score  >= 0.75: s += 25
        elif i.executive_engagement_score  >= 0.50: s += 12
        return min(s, 100)

    def _relationship_score(self, i: ExpansionInput) -> float:
        s = 0
        if   i.champion_advocacy_score     >= 0.80: s += 40
        elif i.champion_advocacy_score     >= 0.60: s += 22
        elif i.champion_advocacy_score     >= 0.40: s += 8

        if   i.stakeholder_growth_count    >= 4:    s += 35
        elif i.stakeholder_growth_count    >= 2:    s += 18
        elif i.stakeholder_growth_count    >= 1:    s += 6

        if   i.upsell_budget_confirmed     >= 0.80: s += 25
        elif i.upsell_budget_confirmed     >= 0.50: s += 12
        return min(s, 100)

    def _composite(self, uc: float, pg: float, en: float, re: float) -> float:
        return min(round(uc * 0.30 + pg * 0.25 + en * 0.25 + re * 0.20, 2), 100.0)

    def _risk(self, c: float) -> ExpansionRisk:
        if c >= 60: return ExpansionRisk.critical
        if c >= 40: return ExpansionRisk.high
        if c >= 20: return ExpansionRisk.moderate
        return ExpansionRisk.low

    def _severity(self, c: float) -> ExpansionSeverity:
        if c >= 60: return ExpansionSeverity.urgent
        if c >= 40: return ExpansionSeverity.active
        if c >= 20: return ExpansionSeverity.emerging
        return ExpansionSeverity.dormant

    def _pattern(self, i: ExpansionInput) -> ExpansionPattern:
        if (i.license_utilization_pct >= 0.88
                and i.api_call_growth_rate_pct >= 0.20):
            return ExpansionPattern.usage_ceiling_breach
        if (i.adjacent_product_fit_score >= 0.75
                and i.integration_gap_count >= 3):
            return ExpansionPattern.product_gap_signal
        if (i.power_user_pct >= 0.35
                and i.nps_score >= 65):
            return ExpansionPattern.engagement_elevation
        if (i.executive_engagement_score >= 0.70
                and i.champion_advocacy_score >= 0.65):
            return ExpansionPattern.executive_pull_through
        if (i.competitor_displacement_pct >= 0.40
                and i.feature_request_frequency >= 4):
            return ExpansionPattern.contract_white_space
        return ExpansionPattern.none

    def _action(self, risk: ExpansionRisk, pat: ExpansionPattern) -> ExpansionAction:
        if risk == ExpansionRisk.critical:
            if pat in (ExpansionPattern.executive_pull_through, ExpansionPattern.usage_ceiling_breach):
                return ExpansionAction.expansion_fast_track
            return ExpansionAction.executive_expansion_briefing
        if risk == ExpansionRisk.high:
            if pat == ExpansionPattern.usage_ceiling_breach:   return ExpansionAction.usage_ceiling_upsell
            if pat == ExpansionPattern.product_gap_signal:     return ExpansionAction.product_gap_discovery_call
            if pat == ExpansionPattern.engagement_elevation:   return ExpansionAction.qbr_expansion_pitch
            if pat == ExpansionPattern.executive_pull_through: return ExpansionAction.executive_expansion_briefing
            if pat == ExpansionPattern.contract_white_space:   return ExpansionAction.white_space_mapping_session
            return ExpansionAction.expansion_monitoring
        if risk == ExpansionRisk.moderate:
            return ExpansionAction.cross_sell_campaign
        return ExpansionAction.no_action

    def _signal(self, i: ExpansionInput, pat: ExpansionPattern, comp: float) -> str:
        if comp < 20:
            return "Expansion signals dormant — account usage, engagement and relationship indicators below expansion threshold"
        labels = {
            ExpansionPattern.usage_ceiling_breach:   "Usage ceiling breach",
            ExpansionPattern.product_gap_signal:     "Product gap signal",
            ExpansionPattern.engagement_elevation:   "Engagement elevation",
            ExpansionPattern.executive_pull_through: "Executive pull-through",
            ExpansionPattern.contract_white_space:   "Contract white space",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.license_utilization_pct*100)}% license utilization — "
            f"{round(i.power_user_pct*100)}% power users — "
            f"NPS {round(i.nps_score)} — "
            f"${round(i.potential_expansion_arr_usd/1000)}k expansion potential — "
            f"composite {round(comp)}"
        )

    def _has_expansion_signal(self, i: ExpansionInput, comp: float) -> bool:
        return (comp >= 40
                or i.license_utilization_pct >= 0.75
                or i.adjacent_product_fit_score >= 0.60)

    def _requires_executive_engagement(self, i: ExpansionInput, comp: float) -> bool:
        return (comp >= 25
                or i.executive_engagement_score >= 0.60
                or i.upsell_budget_confirmed >= 0.50)

    def _expansion_arr(self, i: ExpansionInput, comp: float) -> float:
        return round(i.potential_expansion_arr_usd * (comp / 100), 2)

    def assess(self, i: ExpansionInput) -> ExpansionResult:
        uc   = self._usage_ceiling_score(i)
        pg   = self._product_gap_score(i)
        en   = self._engagement_score(i)
        re   = self._relationship_score(i)
        comp = self._composite(uc, pg, en, re)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = ExpansionResult(
            account_id=i.account_id,
            region=i.region,
            expansion_risk=risk.value,
            expansion_pattern=pat.value,
            expansion_severity=sev.value,
            recommended_action=act.value,
            usage_ceiling_score=uc,
            product_gap_score=pg,
            engagement_score=en,
            relationship_score=re,
            expansion_composite=comp,
            has_expansion_signal=self._has_expansion_signal(i, comp),
            requires_executive_engagement=self._requires_executive_engagement(i, comp),
            estimated_expansion_arr_usd=self._expansion_arr(i, comp),
            expansion_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ExpansionInput]) -> List[ExpansionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_expansion_composite": 0.0,
                "expansion_signal_count": 0,
                "executive_engagement_count": 0,
                "avg_usage_ceiling_score": 0.0,
                "avg_product_gap_score": 0.0,
                "avg_engagement_score": 0.0,
                "avg_relationship_score": 0.0,
                "total_estimated_expansion_arr_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tuc = tpg = ten = tre = tcomp = tarr = 0.0
        gc = ec = 0
        for r in self._results:
            rc[r.expansion_risk]      = rc.get(r.expansion_risk, 0)      + 1
            pc[r.expansion_pattern]   = pc.get(r.expansion_pattern, 0)   + 1
            sc[r.expansion_severity]  = sc.get(r.expansion_severity, 0)  + 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            tuc   += r.usage_ceiling_score
            tpg   += r.product_gap_score
            ten   += r.engagement_score
            tre   += r.relationship_score
            tcomp += r.expansion_composite
            tarr  += r.estimated_expansion_arr_usd
            if r.has_expansion_signal:             gc += 1
            if r.requires_executive_engagement:    ec += 1
        return {
            "total":                               n,
            "risk_counts":                         rc,
            "pattern_counts":                      pc,
            "severity_counts":                     sc,
            "action_counts":                       ac,
            "avg_expansion_composite":             round(tcomp / n, 1),
            "expansion_signal_count":              gc,
            "executive_engagement_count":          ec,
            "avg_usage_ceiling_score":             round(tuc / n, 1),
            "avg_product_gap_score":               round(tpg / n, 1),
            "avg_engagement_score":                round(ten / n, 1),
            "avg_relationship_score":              round(tre / n, 1),
            "total_estimated_expansion_arr_usd":   round(tarr, 2),
        }
