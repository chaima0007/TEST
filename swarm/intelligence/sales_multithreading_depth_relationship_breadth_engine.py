"""
Module 214 — Sales Multithreading Depth & Relationship Breadth Engine
Tracks how many unique contacts reps engage per account and detects
single-threading risk that leads to hidden deal vulnerability.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class MultithreadRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MultithreadPattern(str, Enum):
    none                     = "none"
    single_thread_dependency = "single_thread_dependency"
    vertical_tunnel          = "vertical_tunnel"
    it_bubble                = "it_bubble"
    executive_bypass         = "executive_bypass"
    breadth_stall            = "breadth_stall"


class MultithreadSeverity(str, Enum):
    networked  = "networked"
    adequate   = "adequate"
    thin       = "thin"
    isolated   = "isolated"


class MultithreadAction(str, Enum):
    no_action                    = "no_action"
    multithreading_monitoring    = "multithreading_monitoring"
    contact_expansion_coaching   = "contact_expansion_coaching"
    stakeholder_mapping_workshop = "stakeholder_mapping_workshop"
    exec_introduction_coaching   = "exec_introduction_coaching"
    it_champion_bridge_coaching  = "it_champion_bridge_coaching"
    relationship_breadth_sprint  = "relationship_breadth_sprint"
    account_rescue_intervention  = "account_rescue_intervention"
    deal_restructure_escalation  = "deal_restructure_escalation"


@dataclass
class MultithreadInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    # Threading depth
    avg_contacts_per_account: float             # average unique contacts engaged
    single_threaded_account_rate_pct: float     # % accounts with only 1 active contact
    avg_new_contacts_added_per_quarter: float   # new contacts added per account per Q
    contact_attrition_rate_pct: float           # % contacts lost per quarter
    # Stakeholder coverage
    economic_buyer_engaged_rate_pct: float      # % deals with EB engaged
    technical_buyer_engaged_rate_pct: float     # % deals with TB engaged
    end_user_engaged_rate_pct: float            # % deals with end user engaged
    champion_to_non_champion_ratio: float       # ratio of champion vs other contacts
    # Engagement quality
    avg_email_threads_per_contact: float        # depth of engagement per contact
    multi_contact_meeting_rate_pct: float       # % meetings with 2+ stakeholders
    cross_functional_reach_score: float         # 0-1 reach across functions
    referral_introduction_rate_pct: float       # % new contacts via internal intro
    # Network health
    dormant_contact_rate_pct: float             # % contacts with no activity >30d
    contact_map_completeness_score: float       # 0-1 org chart coverage
    buying_committee_size_vs_avg: float         # ratio to industry avg (>1 = covered)
    # Executive access
    c_suite_engaged_rate_pct: float             # % deals with C-suite contact
    vp_engaged_rate_pct: float                  # % deals with VP-level contact
    # Volume
    total_active_accounts: int
    avg_deal_value_usd: float


@dataclass
class MultithreadResult:
    rep_id: str
    region: str
    multithread_risk: str
    multithread_pattern: str
    multithread_severity: str
    recommended_action: str
    depth_score: float
    coverage_score: float
    quality_score: float
    network_score: float
    multithread_composite: float
    has_multithread_gap: bool
    requires_expansion_coaching: bool
    estimated_vulnerable_pipeline_usd: float
    multithread_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "multithread_risk":                self.multithread_risk,
            "multithread_pattern":             self.multithread_pattern,
            "multithread_severity":            self.multithread_severity,
            "recommended_action":              self.recommended_action,
            "depth_score":                     self.depth_score,
            "coverage_score":                  self.coverage_score,
            "quality_score":                   self.quality_score,
            "network_score":                   self.network_score,
            "multithread_composite":           self.multithread_composite,
            "has_multithread_gap":             self.has_multithread_gap,
            "requires_expansion_coaching":     self.requires_expansion_coaching,
            "estimated_vulnerable_pipeline_usd": self.estimated_vulnerable_pipeline_usd,
            "multithread_signal":              self.multithread_signal,
        }


class SalesMultithreadingDepthRelationshipBreadthEngine:
    def __init__(self) -> None:
        self._results: List[MultithreadResult] = []

    # ── Sub-scores ────────────────────────────────────────────────────────────

    def _depth_score(self, i: MultithreadInput) -> float:
        s = 0
        if   i.single_threaded_account_rate_pct    >= 0.60: s += 40
        elif i.single_threaded_account_rate_pct    >= 0.40: s += 22
        elif i.single_threaded_account_rate_pct    >= 0.22: s += 8

        if   i.avg_contacts_per_account            <= 1.5:  s += 35
        elif i.avg_contacts_per_account            <= 2.5:  s += 18
        elif i.avg_contacts_per_account            <= 3.5:  s += 6

        if   i.avg_new_contacts_added_per_quarter  <= 0.5:  s += 25
        elif i.avg_new_contacts_added_per_quarter  <= 1.2:  s += 12
        return min(s, 100)

    def _coverage_score(self, i: MultithreadInput) -> float:
        s = 0
        if   i.economic_buyer_engaged_rate_pct     <= 0.25: s += 45
        elif i.economic_buyer_engaged_rate_pct     <= 0.50: s += 25
        elif i.economic_buyer_engaged_rate_pct     <= 0.70: s += 10

        if   i.c_suite_engaged_rate_pct            <= 0.15: s += 30
        elif i.c_suite_engaged_rate_pct            <= 0.35: s += 15

        if   i.contact_map_completeness_score      <= 0.25: s += 25
        elif i.contact_map_completeness_score      <= 0.50: s += 12
        return min(s, 100)

    def _quality_score(self, i: MultithreadInput) -> float:
        s = 0
        if   i.multi_contact_meeting_rate_pct      <= 0.20: s += 40
        elif i.multi_contact_meeting_rate_pct      <= 0.45: s += 22
        elif i.multi_contact_meeting_rate_pct      <= 0.65: s += 8

        if   i.cross_functional_reach_score        <= 0.20: s += 35
        elif i.cross_functional_reach_score        <= 0.45: s += 18

        if   i.referral_introduction_rate_pct      <= 0.15: s += 25
        elif i.referral_introduction_rate_pct      <= 0.35: s += 12
        return min(s, 100)

    def _network_score(self, i: MultithreadInput) -> float:
        s = 0
        if   i.dormant_contact_rate_pct            >= 0.55: s += 45
        elif i.dormant_contact_rate_pct            >= 0.35: s += 25
        elif i.dormant_contact_rate_pct            >= 0.20: s += 10

        if   i.contact_attrition_rate_pct          >= 0.40: s += 30
        elif i.contact_attrition_rate_pct          >= 0.22: s += 15

        if   i.buying_committee_size_vs_avg        <= 0.50: s += 25
        elif i.buying_committee_size_vs_avg        <= 0.75: s += 12
        return min(s, 100)

    # ── Composite ─────────────────────────────────────────────────────────────

    def _composite(self, de: float, co: float, qu: float, ne: float) -> float:
        return min(round(de * 0.30 + co * 0.25 + qu * 0.25 + ne * 0.20, 2), 100.0)

    # ── Risk / Severity ───────────────────────────────────────────────────────

    def _risk(self, c: float) -> MultithreadRisk:
        if c >= 60: return MultithreadRisk.critical
        if c >= 40: return MultithreadRisk.high
        if c >= 20: return MultithreadRisk.moderate
        return MultithreadRisk.low

    def _severity(self, c: float) -> MultithreadSeverity:
        if c >= 60: return MultithreadSeverity.isolated
        if c >= 40: return MultithreadSeverity.thin
        if c >= 20: return MultithreadSeverity.adequate
        return MultithreadSeverity.networked

    # ── Pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, i: MultithreadInput) -> MultithreadPattern:
        if (i.single_threaded_account_rate_pct >= 0.55
                and i.avg_contacts_per_account <= 1.8):
            return MultithreadPattern.single_thread_dependency
        if (i.c_suite_engaged_rate_pct <= 0.15
                and i.vp_engaged_rate_pct <= 0.20
                and i.technical_buyer_engaged_rate_pct >= 0.70):
            return MultithreadPattern.it_bubble
        if (i.c_suite_engaged_rate_pct >= 0.70
                and i.end_user_engaged_rate_pct <= 0.20):
            return MultithreadPattern.executive_bypass
        if (i.vp_engaged_rate_pct >= 0.55
                and i.economic_buyer_engaged_rate_pct <= 0.20):
            return MultithreadPattern.vertical_tunnel
        if (i.dormant_contact_rate_pct >= 0.50
                and i.avg_new_contacts_added_per_quarter <= 0.8):
            return MultithreadPattern.breadth_stall
        return MultithreadPattern.none

    # ── Action ────────────────────────────────────────────────────────────────

    def _action(self, risk: MultithreadRisk, pat: MultithreadPattern) -> MultithreadAction:
        if risk == MultithreadRisk.critical:
            if pat in (MultithreadPattern.single_thread_dependency,
                       MultithreadPattern.breadth_stall):
                return MultithreadAction.deal_restructure_escalation
            return MultithreadAction.account_rescue_intervention
        if risk == MultithreadRisk.high:
            if pat == MultithreadPattern.single_thread_dependency: return MultithreadAction.contact_expansion_coaching
            if pat == MultithreadPattern.it_bubble:                return MultithreadAction.it_champion_bridge_coaching
            if pat == MultithreadPattern.executive_bypass:         return MultithreadAction.exec_introduction_coaching
            if pat == MultithreadPattern.vertical_tunnel:          return MultithreadAction.stakeholder_mapping_workshop
            if pat == MultithreadPattern.breadth_stall:            return MultithreadAction.relationship_breadth_sprint
            return MultithreadAction.multithreading_monitoring
        if risk == MultithreadRisk.moderate:
            return MultithreadAction.multithreading_monitoring
        return MultithreadAction.no_action

    # ── Signal ────────────────────────────────────────────────────────────────

    def _signal(self, i: MultithreadInput, pat: MultithreadPattern, comp: float) -> str:
        if comp < 20:
            return "Relationship breadth strong — multithreading depth, stakeholder coverage, and network health within benchmark targets"
        labels = {
            MultithreadPattern.single_thread_dependency: "Single-thread dependency",
            MultithreadPattern.vertical_tunnel:          "Vertical tunnel",
            MultithreadPattern.it_bubble:                "IT bubble",
            MultithreadPattern.executive_bypass:         "Executive bypass",
            MultithreadPattern.breadth_stall:            "Breadth stall",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.avg_contacts_per_account, 1)} avg contacts/account — "
            f"{round(i.single_threaded_account_rate_pct*100)}% single-threaded — "
            f"{round(i.economic_buyer_engaged_rate_pct*100)}% EB engaged — "
            f"composite {round(comp)}"
        )

    # ── Flags ─────────────────────────────────────────────────────────────────

    def _has_multithread_gap(self, i: MultithreadInput, comp: float) -> bool:
        return (comp >= 40
                or i.single_threaded_account_rate_pct >= 0.40
                or i.economic_buyer_engaged_rate_pct <= 0.40)

    def _requires_expansion_coaching(self, i: MultithreadInput, comp: float) -> bool:
        return (comp >= 25
                or i.avg_contacts_per_account <= 2.5
                or i.multi_contact_meeting_rate_pct <= 0.40)

    # ── Vulnerable pipeline ───────────────────────────────────────────────────

    def _vulnerable_pipeline(self, i: MultithreadInput, comp: float) -> float:
        return round(
            i.total_active_accounts
            * i.avg_deal_value_usd
            * i.single_threaded_account_rate_pct
            * (comp / 100),
            2,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def assess(self, i: MultithreadInput) -> MultithreadResult:
        de  = self._depth_score(i)
        co  = self._coverage_score(i)
        qu  = self._quality_score(i)
        ne  = self._network_score(i)
        comp = self._composite(de, co, qu, ne)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = MultithreadResult(
            rep_id=i.rep_id,
            region=i.region,
            multithread_risk=risk.value,
            multithread_pattern=pat.value,
            multithread_severity=sev.value,
            recommended_action=act.value,
            depth_score=de,
            coverage_score=co,
            quality_score=qu,
            network_score=ne,
            multithread_composite=comp,
            has_multithread_gap=self._has_multithread_gap(i, comp),
            requires_expansion_coaching=self._requires_expansion_coaching(i, comp),
            estimated_vulnerable_pipeline_usd=self._vulnerable_pipeline(i, comp),
            multithread_signal=self._signal(i, pat, comp),
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
                "expansion_coaching_count": 0,
                "avg_depth_score": 0.0,
                "avg_coverage_score": 0.0,
                "avg_quality_score": 0.0,
                "avg_network_score": 0.0,
                "total_estimated_vulnerable_pipeline_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tde = tco = tqu = tne = tcomp = tvp = 0.0
        gc = ecc = 0
        for r in self._results:
            rc[r.multithread_risk]    = rc.get(r.multithread_risk, 0)    + 1
            pc[r.multithread_pattern] = pc.get(r.multithread_pattern, 0) + 1
            sc[r.multithread_severity]= sc.get(r.multithread_severity, 0)+ 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            tde  += r.depth_score
            tco  += r.coverage_score
            tqu  += r.quality_score
            tne  += r.network_score
            tcomp += r.multithread_composite
            tvp  += r.estimated_vulnerable_pipeline_usd
            if r.has_multithread_gap:          gc  += 1
            if r.requires_expansion_coaching:  ecc += 1
        return {
            "total":                                   n,
            "risk_counts":                             rc,
            "pattern_counts":                          pc,
            "severity_counts":                         sc,
            "action_counts":                           ac,
            "avg_multithread_composite":               round(tcomp / n, 1),
            "multithread_gap_count":                   gc,
            "expansion_coaching_count":                ecc,
            "avg_depth_score":                         round(tde / n, 1),
            "avg_coverage_score":                      round(tco / n, 1),
            "avg_quality_score":                       round(tqu / n, 1),
            "avg_network_score":                       round(tne / n, 1),
            "total_estimated_vulnerable_pipeline_usd": round(tvp, 2),
        }
