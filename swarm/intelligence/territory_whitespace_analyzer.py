from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WhitespacePriority(str, Enum):
    LOW         = "low"
    MEDIUM      = "medium"
    HIGH        = "high"
    URGENT      = "urgent"


class WhitespaceType(str, Enum):
    NEW_LOGO         = "new_logo"
    PRODUCT_EXPAND   = "product_expand"
    GEO_EXPAND       = "geo_expand"
    SEGMENT_EXPAND   = "segment_expand"
    DORMANT_REACTIVATE = "dormant_reactivate"


class TerritoryHealth(str, Enum):
    UNDERPENETRATED  = "underpenetrated"
    DEVELOPING       = "developing"
    OPTIMIZED        = "optimized"
    SATURATED        = "saturated"


class WhitespaceAction(str, Enum):
    NURTURE         = "nurture"
    PROSPECT        = "prospect"
    PRIORITIZE      = "prioritize"
    IMMEDIATE_FOCUS = "immediate_focus"


@dataclass
class TerritoryWhitespaceInput:
    territory_id:                   str
    territory_name:                 str
    rep_id:                         str
    total_accounts_in_territory:    int     # total addressable accounts in territory
    accounts_with_active_deals:     int     # accounts with open opportunities
    accounts_with_customers:        int     # accounts already customers
    accounts_never_contacted:       int     # accounts with zero outreach ever
    icp_match_score_avg:            float   # 0-100, avg ICP match score for never-contacted accounts
    avg_company_size_employees:     int     # avg size of untouched accounts
    industry_growth_rate_pct:       float   # industry YoY growth rate (%)
    competitor_present_pct:         float   # % of whitespace accounts where competitor is present
    buying_trigger_signal_count:    int     # # of accounts showing buying trigger signals (funding, hiring, etc.)
    lookalike_customer_match_count: int     # # of accounts that match existing customer profiles
    avg_deal_size_similar_accounts: float   # avg deal size from similar accounts ($)
    territory_quota_attainment_pct: float   # rep's current quota attainment % in territory
    months_rep_in_territory:        int     # months rep has worked this territory
    outreach_coverage_pct:          float   # % of territory accounts ever reached out to
    territory_revenue_potential:    float   # estimated total revenue potential ($)
    current_territory_revenue:      float   # current ARR from territory ($)
    conference_event_signal:        int     # 1 if major industry conference coming (outreach opportunity)
    seasonal_buying_signal:         int     # 1 if accounts in seasonal peak buying window
    executive_referral_count:       int     # # of exec referrals available for whitespace accounts


@dataclass
class TerritoryWhitespaceResult:
    territory_id:                   str
    territory_name:                 str
    whitespace_priority:            WhitespacePriority
    whitespace_type:                WhitespaceType
    territory_health:               TerritoryHealth
    whitespace_action:              WhitespaceAction
    opportunity_density_score:      float   # 0-100
    market_timing_score:            float   # 0-100
    territory_coverage_score:       float   # 0-100
    icp_alignment_score:            float   # 0-100
    whitespace_composite:           float   # 0-100
    estimated_whitespace_arr:       float   # $ potential ARR in whitespace
    territory_penetration_pct:      float   # % of territory already captured
    is_high_potential_territory:    bool
    needs_immediate_prospecting:    bool

    def to_dict(self) -> dict:
        return {
            "territory_id":                 self.territory_id,
            "territory_name":               self.territory_name,
            "whitespace_priority":          self.whitespace_priority.value,
            "whitespace_type":              self.whitespace_type.value,
            "territory_health":             self.territory_health.value,
            "whitespace_action":            self.whitespace_action.value,
            "opportunity_density_score":    self.opportunity_density_score,
            "market_timing_score":          self.market_timing_score,
            "territory_coverage_score":     self.territory_coverage_score,
            "icp_alignment_score":          self.icp_alignment_score,
            "whitespace_composite":         self.whitespace_composite,
            "estimated_whitespace_arr":     self.estimated_whitespace_arr,
            "territory_penetration_pct":    self.territory_penetration_pct,
            "is_high_potential_territory":  self.is_high_potential_territory,
            "needs_immediate_prospecting":  self.needs_immediate_prospecting,
        }


class TerritoryWhitespaceAnalyzer:
    def __init__(self) -> None:
        self._results: list[TerritoryWhitespaceResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: TerritoryWhitespaceInput) -> TerritoryWhitespaceResult:
        opp_density  = self._opportunity_density_score(inp)
        mkt_timing   = self._market_timing_score(inp)
        coverage     = self._territory_coverage_score(inp)
        icp_align    = self._icp_alignment_score(inp)
        composite    = self._composite(opp_density, mkt_timing, coverage, icp_align)
        priority     = self._whitespace_priority(composite, inp)
        ws_type      = self._whitespace_type(inp)
        health       = self._territory_health(inp)
        penetration  = self._territory_penetration_pct(inp)
        ws_arr       = self._estimated_whitespace_arr(inp)
        is_high      = composite >= 60.0 or inp.buying_trigger_signal_count >= 5
        needs_now    = (composite >= 75.0 or
                        (inp.seasonal_buying_signal and composite >= 55.0) or
                        inp.buying_trigger_signal_count >= 8)
        action       = self._whitespace_action(priority, needs_now)

        result = TerritoryWhitespaceResult(
            territory_id=inp.territory_id,
            territory_name=inp.territory_name,
            whitespace_priority=priority,
            whitespace_type=ws_type,
            territory_health=health,
            whitespace_action=action,
            opportunity_density_score=opp_density,
            market_timing_score=mkt_timing,
            territory_coverage_score=coverage,
            icp_alignment_score=icp_align,
            whitespace_composite=composite,
            estimated_whitespace_arr=ws_arr,
            territory_penetration_pct=penetration,
            is_high_potential_territory=is_high,
            needs_immediate_prospecting=needs_now,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[TerritoryWhitespaceInput]) -> list[TerritoryWhitespaceResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def high_potential_territories(self) -> list[TerritoryWhitespaceResult]:
        return [r for r in self._results if r.is_high_potential_territory]

    @property
    def immediate_prospecting_queue(self) -> list[TerritoryWhitespaceResult]:
        return [r for r in self._results if r.needs_immediate_prospecting]

    @property
    def total_estimated_whitespace_arr(self) -> float:
        return round(sum(r.estimated_whitespace_arr for r in self._results), 2)

    @property
    def avg_whitespace_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.whitespace_composite for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _opportunity_density_score(self, inp: TerritoryWhitespaceInput) -> float:
        score = 0.0
        if inp.total_accounts_in_territory > 0:
            untouched_pct = inp.accounts_never_contacted / inp.total_accounts_in_territory
            score += min(35.0, untouched_pct * 50.0)
        # Lookalike customer matches (up to 30)
        score += min(30.0, inp.lookalike_customer_match_count * 5.0)
        # Buying trigger signals (up to 25)
        score += min(25.0, inp.buying_trigger_signal_count * 3.0)
        # Exec referrals available (up to 10)
        score += min(10.0, inp.executive_referral_count * 2.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _market_timing_score(self, inp: TerritoryWhitespaceInput) -> float:
        score = 30.0
        # Industry growth rate
        growth = inp.industry_growth_rate_pct
        if growth >= 20:
            score += 30.0
        elif growth >= 10:
            score += 20.0
        elif growth >= 5:
            score += 10.0
        # Seasonal buying window
        if inp.seasonal_buying_signal:
            score += 20.0
        # Conference/event signal
        if inp.conference_event_signal:
            score += 15.0
        # Competitor penetration (less competition = better timing)
        comp_pct = inp.competitor_present_pct
        if comp_pct <= 20:
            score += 5.0
        elif comp_pct >= 60:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _territory_coverage_score(self, inp: TerritoryWhitespaceInput) -> float:
        # Higher uncovered territory = more whitespace opportunity
        covered = inp.outreach_coverage_pct
        whitespace_score = max(0.0, 100.0 - covered)
        # Tenure in territory (less experienced reps have more whitespace blindspots)
        tenure = inp.months_rep_in_territory
        if tenure <= 3:
            whitespace_score = min(100.0, whitespace_score + 10.0)
        elif tenure <= 12:
            pass  # neutral
        else:
            # Experienced rep with low coverage = they know what they're doing
            whitespace_score = min(100.0, whitespace_score + 5.0)
        # Quota attainment proxy (higher attainment in territory = better coverage signals)
        attain = inp.territory_quota_attainment_pct
        if attain < 50:
            whitespace_score = min(100.0, whitespace_score + 10.0)
        return round(max(0.0, min(100.0, whitespace_score)), 1)

    def _icp_alignment_score(self, inp: TerritoryWhitespaceInput) -> float:
        score = inp.icp_match_score_avg * 0.60
        # Company size fit (mid-market is ideal: 100-2000 employees)
        size = inp.avg_company_size_employees
        if 100 <= size <= 2000:
            score += 25.0
        elif 50 <= size < 100 or 2000 < size <= 5000:
            score += 15.0
        elif size > 5000:
            score += 8.0
        # Deal size signal from similar accounts
        if inp.avg_deal_size_similar_accounts >= 100_000:
            score += 15.0
        elif inp.avg_deal_size_similar_accounts >= 50_000:
            score += 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        opp: float,
        timing: float,
        coverage: float,
        icp: float,
    ) -> float:
        composite = opp * 0.30 + timing * 0.25 + coverage * 0.25 + icp * 0.20
        return round(max(0.0, min(100.0, composite)), 1)

    def _whitespace_priority(self, composite: float, inp: TerritoryWhitespaceInput) -> WhitespacePriority:
        if composite >= 75 or inp.buying_trigger_signal_count >= 8:
            return WhitespacePriority.URGENT
        if composite >= 55:
            return WhitespacePriority.HIGH
        if composite >= 35:
            return WhitespacePriority.MEDIUM
        return WhitespacePriority.LOW

    def _whitespace_type(self, inp: TerritoryWhitespaceInput) -> WhitespaceType:
        # Dormant reactivate if low coverage but old territory
        if inp.accounts_never_contacted < inp.total_accounts_in_territory * 0.3 and inp.months_rep_in_territory >= 12:
            return WhitespaceType.DORMANT_REACTIVATE
        # GEO expand if many accounts with high ICP match but in new segment
        if inp.icp_match_score_avg >= 70 and inp.accounts_never_contacted >= 20:
            return WhitespaceType.GEO_EXPAND
        # Product expand if lots of customers but few active deals
        if inp.accounts_with_customers >= 5 and inp.accounts_with_active_deals < inp.accounts_with_customers:
            return WhitespaceType.PRODUCT_EXPAND
        # Segment expand if lookalike matches but haven't touched
        if inp.lookalike_customer_match_count >= 5:
            return WhitespaceType.SEGMENT_EXPAND
        return WhitespaceType.NEW_LOGO

    def _territory_health(self, inp: TerritoryWhitespaceInput) -> TerritoryHealth:
        if inp.total_accounts_in_territory == 0:
            return TerritoryHealth.UNDERPENETRATED
        penetration = (inp.accounts_with_customers + inp.accounts_with_active_deals) / inp.total_accounts_in_territory
        if penetration >= 0.7:
            return TerritoryHealth.SATURATED
        if penetration >= 0.4:
            return TerritoryHealth.OPTIMIZED
        if penetration >= 0.2:
            return TerritoryHealth.DEVELOPING
        return TerritoryHealth.UNDERPENETRATED

    def _territory_penetration_pct(self, inp: TerritoryWhitespaceInput) -> float:
        if inp.total_accounts_in_territory == 0:
            return 0.0
        penetration = (inp.accounts_with_customers + inp.accounts_with_active_deals) / inp.total_accounts_in_territory
        return round(min(100.0, penetration * 100.0), 1)

    def _estimated_whitespace_arr(self, inp: TerritoryWhitespaceInput) -> float:
        # Uncaptured revenue potential
        if inp.territory_revenue_potential > 0 and inp.current_territory_revenue >= 0:
            whitespace = max(0.0, inp.territory_revenue_potential - inp.current_territory_revenue)
        else:
            whitespace = 0.0
        # Also estimate from lookalike + trigger signals
        signal_arr = (inp.lookalike_customer_match_count + inp.buying_trigger_signal_count) * inp.avg_deal_size_similar_accounts * 0.15
        return round(max(whitespace, signal_arr), 2)

    def _whitespace_action(self, priority: WhitespacePriority, needs_now: bool) -> WhitespaceAction:
        if needs_now or priority == WhitespacePriority.URGENT:
            return WhitespaceAction.IMMEDIATE_FOCUS
        if priority == WhitespacePriority.HIGH:
            return WhitespaceAction.PRIORITIZE
        if priority == WhitespacePriority.MEDIUM:
            return WhitespaceAction.PROSPECT
        return WhitespaceAction.NURTURE

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                            0,
                "priority_counts":                  {},
                "type_counts":                      {},
                "health_counts":                    {},
                "action_counts":                    {},
                "avg_whitespace_composite":         0.0,
                "total_estimated_whitespace_arr":   0.0,
                "high_potential_count":             0,
                "immediate_prospecting_count":      0,
                "avg_opportunity_density_score":    0.0,
                "avg_market_timing_score":          0.0,
                "avg_territory_coverage_score":     0.0,
                "avg_icp_alignment_score":          0.0,
            }

        priority_counts: dict[str, int] = {}
        type_counts:     dict[str, int] = {}
        health_counts:   dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp  = 0.0
        total_opp   = 0.0
        total_timing = 0.0
        total_cov   = 0.0
        total_icp   = 0.0

        for r in self._results:
            priority_counts[r.whitespace_priority.value] = priority_counts.get(r.whitespace_priority.value, 0) + 1
            type_counts[r.whitespace_type.value]         = type_counts.get(r.whitespace_type.value, 0) + 1
            health_counts[r.territory_health.value]      = health_counts.get(r.territory_health.value, 0) + 1
            action_counts[r.whitespace_action.value]     = action_counts.get(r.whitespace_action.value, 0) + 1
            total_comp   += r.whitespace_composite
            total_opp    += r.opportunity_density_score
            total_timing += r.market_timing_score
            total_cov    += r.territory_coverage_score
            total_icp    += r.icp_alignment_score

        return {
            "total":                            n,
            "priority_counts":                  priority_counts,
            "type_counts":                      type_counts,
            "health_counts":                    health_counts,
            "action_counts":                    action_counts,
            "avg_whitespace_composite":         round(total_comp / n, 1),
            "total_estimated_whitespace_arr":   self.total_estimated_whitespace_arr,
            "high_potential_count":             len(self.high_potential_territories),
            "immediate_prospecting_count":      len(self.immediate_prospecting_queue),
            "avg_opportunity_density_score":    round(total_opp / n, 1),
            "avg_market_timing_score":          round(total_timing / n, 1),
            "avg_territory_coverage_score":     round(total_cov / n, 1),
            "avg_icp_alignment_score":          round(total_icp / n, 1),
        }
