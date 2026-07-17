from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AccountTier(str, Enum):
    STRATEGIC  = "strategic"
    ENTERPRISE = "enterprise"
    GROWTH     = "growth"
    SMB        = "smb"
    STARTER    = "starter"


class AccountHealth(str, Enum):
    EXCELLENT = "excellent"
    GOOD      = "good"
    FAIR      = "fair"
    AT_RISK   = "at_risk"
    CHURNING  = "churning"


class EngagementLevel(str, Enum):
    HIGH    = "high"
    MEDIUM  = "medium"
    LOW     = "low"
    DORMANT = "dormant"


class AccountAction(str, Enum):
    EXPAND   = "expand"
    RETAIN   = "retain"
    NURTURE  = "nurture"
    RESCUE   = "rescue"
    MONITOR  = "monitor"


@dataclass
class AccountScoringInput:
    account_id:                str
    account_name:              str
    industry:                  str
    region:                    str
    account_age_days:          int      # days since account created
    total_mrr:                 float    # current monthly recurring revenue
    expansion_mrr:             float    # MRR added via upsell/cross-sell this period
    churned_mrr:               float    # MRR lost this period
    nps_score:                 float    # Net Promoter Score (-100 to 100)
    support_tickets_open:      int      # currently open support tickets
    support_tickets_resolved:  int      # resolved tickets this period
    login_frequency_per_week:  float    # avg logins per week
    feature_adoption_pct:      float    # % of features actively used (0–100)
    seats_used:                int      # seats actively used
    seats_total:               int      # total seats purchased
    renewal_date_days:         int      # days until renewal (negative = overdue)
    last_contact_days:         int      # days since last CSM contact
    executive_contacts:        int      # number of executive-level contacts
    total_contacts:            int      # total contacts in account
    deals_won:                 int      # historical deals won with this account
    deals_lost:                int      # historical deals lost
    upsell_opportunities:      int      # open upsell opportunities


@dataclass
class AccountScoringResult:
    account_id:            str
    account_name:          str
    account_tier:          AccountTier
    account_health:        AccountHealth
    engagement_level:      EngagementLevel
    account_action:        AccountAction
    health_score:          float    # 0–100
    engagement_score:      float    # 0–100
    growth_score:          float    # 0–100
    fit_score:             float    # 0–100
    churn_risk:            float    # 0–100 (higher = more risk)
    expansion_probability: float    # 0–100
    composite_score:       float    # 0–100 weighted composite
    is_at_risk:            bool
    needs_attention:       bool

    def to_dict(self) -> dict:
        return {
            "account_id":            self.account_id,
            "account_name":          self.account_name,
            "account_tier":          self.account_tier.value,
            "account_health":        self.account_health.value,
            "engagement_level":      self.engagement_level.value,
            "account_action":        self.account_action.value,
            "health_score":          self.health_score,
            "engagement_score":      self.engagement_score,
            "growth_score":          self.growth_score,
            "fit_score":             self.fit_score,
            "churn_risk":            self.churn_risk,
            "expansion_probability": self.expansion_probability,
            "composite_score":       self.composite_score,
            "is_at_risk":            self.is_at_risk,
            "needs_attention":       self.needs_attention,
        }


class AccountScoringEngine:
    def __init__(self) -> None:
        self._results: list[AccountScoringResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: AccountScoringInput) -> AccountScoringResult:
        health_score   = self._health_score(inp)
        engagement_sc  = self._engagement_score(inp)
        growth_sc      = self._growth_score(inp)
        fit_sc         = self._fit_score(inp)
        churn_risk     = self._churn_risk(inp, health_score, engagement_sc)
        expansion_prob = self._expansion_probability(inp, growth_sc, engagement_sc)
        composite      = self._composite_score(health_score, engagement_sc, growth_sc, fit_sc)
        tier           = self._account_tier(inp)
        health         = self._account_health(health_score, churn_risk)
        engagement     = self._engagement_level(engagement_sc, inp)
        is_at_risk     = churn_risk >= 60.0 or health in (AccountHealth.AT_RISK, AccountHealth.CHURNING)
        needs_attention = (
            inp.last_contact_days > 30 or
            inp.support_tickets_open > 5 or
            inp.renewal_date_days < 30
        )
        action = self._account_action(inp, health, engagement, churn_risk, expansion_prob)

        result = AccountScoringResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            account_tier=tier,
            account_health=health,
            engagement_level=engagement,
            account_action=action,
            health_score=health_score,
            engagement_score=engagement_sc,
            growth_score=growth_sc,
            fit_score=fit_sc,
            churn_risk=churn_risk,
            expansion_probability=expansion_prob,
            composite_score=composite,
            is_at_risk=is_at_risk,
            needs_attention=needs_attention,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[AccountScoringInput]
    ) -> list[AccountScoringResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_accounts(self) -> list[AccountScoringResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def attention_needed(self) -> list[AccountScoringResult]:
        return [r for r in self._results if r.needs_attention]

    @property
    def high_value_accounts(self) -> list[AccountScoringResult]:
        return [r for r in self._results if r.account_tier in (AccountTier.STRATEGIC, AccountTier.ENTERPRISE)]

    @property
    def avg_composite_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.composite_score for r in self._results) / len(self._results), 1)

    @property
    def avg_churn_risk(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.churn_risk for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _health_score(self, inp: AccountScoringInput) -> float:
        score = 0.0
        # NPS contribution (up to 30)
        nps_norm = (inp.nps_score + 100) / 200  # -100..100 → 0..1
        score += nps_norm * 30.0
        # Feature adoption (up to 25)
        score += min(25.0, inp.feature_adoption_pct * 0.25)
        # Support health: fewer open tickets relative to resolved (up to 20)
        total_tix = inp.support_tickets_open + max(1, inp.support_tickets_resolved)
        resolution_rate = inp.support_tickets_resolved / total_tix
        score += resolution_rate * 20.0
        # Seat utilisation (up to 15)
        if inp.seats_total > 0:
            util = inp.seats_used / inp.seats_total
            score += min(15.0, util * 15.0)
        # MRR growth (up to 10) — net of churn
        net_mrr_delta = inp.expansion_mrr - inp.churned_mrr
        if inp.total_mrr > 0:
            net_growth_pct = net_mrr_delta / inp.total_mrr * 100
            score += max(0.0, min(10.0, net_growth_pct * 0.5 + 5.0))
        return round(max(0.0, min(100.0, score)), 1)

    def _engagement_score(self, inp: AccountScoringInput) -> float:
        score = 0.0
        # Login frequency (up to 35) — 5+ logins/week is max
        score += min(35.0, inp.login_frequency_per_week / 5.0 * 35.0)
        # Last contact recency (up to 25)
        if inp.last_contact_days <= 7:
            score += 25.0
        elif inp.last_contact_days <= 14:
            score += 18.0
        elif inp.last_contact_days <= 30:
            score += 10.0
        elif inp.last_contact_days <= 60:
            score += 4.0
        # Executive contact coverage (up to 20)
        if inp.total_contacts > 0:
            exec_coverage = inp.executive_contacts / inp.total_contacts
            score += min(20.0, exec_coverage * 40.0)
        # Feature adoption (up to 20)
        score += min(20.0, inp.feature_adoption_pct * 0.2)
        return round(max(0.0, min(100.0, score)), 1)

    def _growth_score(self, inp: AccountScoringInput) -> float:
        score = 0.0
        # Upsell pipeline (up to 30)
        score += min(30.0, inp.upsell_opportunities * 6.0)
        # Expansion MRR momentum (up to 25)
        if inp.total_mrr > 0:
            expansion_pct = inp.expansion_mrr / inp.total_mrr * 100
            score += min(25.0, expansion_pct * 2.5)
        # Seat headroom (up to 25)
        if inp.seats_total > 0:
            headroom = 1.0 - (inp.seats_used / inp.seats_total)
            score += min(25.0, headroom * 25.0)
        # Historical win rate as proxy for upsell readiness (up to 20)
        total_deals = inp.deals_won + inp.deals_lost
        if total_deals > 0:
            win_rate = inp.deals_won / total_deals
            score += min(20.0, win_rate * 20.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _fit_score(self, inp: AccountScoringInput) -> float:
        score = 0.0
        # Account tenure (up to 30) — older accounts have better fit signal
        tenure_years = inp.account_age_days / 365.0
        score += min(30.0, tenure_years * 10.0)
        # MRR size (up to 30) — proxy for product–market fit
        if inp.total_mrr >= 50_000:
            score += 30.0
        elif inp.total_mrr >= 20_000:
            score += 20.0
        elif inp.total_mrr >= 5_000:
            score += 12.0
        elif inp.total_mrr >= 1_000:
            score += 6.0
        # Seat count as complexity indicator (up to 20)
        score += min(20.0, inp.seats_total * 0.4)
        # NPS contribution (up to 20)
        nps_norm = (inp.nps_score + 100) / 200
        score += nps_norm * 20.0
        return round(max(0.0, min(100.0, score)), 1)

    def _churn_risk(
        self,
        inp: AccountScoringInput,
        health_score: float,
        engagement_score: float,
    ) -> float:
        risk = 0.0
        # Low health → higher risk
        risk += max(0.0, (100.0 - health_score) * 0.35)
        # Low engagement → higher risk
        risk += max(0.0, (100.0 - engagement_score) * 0.25)
        # Renewal proximity (days < 30 or overdue)
        if inp.renewal_date_days < 0:
            risk += 20.0
        elif inp.renewal_date_days < 30:
            risk += 12.0
        elif inp.renewal_date_days < 60:
            risk += 5.0
        # High open tickets
        risk += min(10.0, inp.support_tickets_open * 1.0)
        # MRR churn signal
        if inp.total_mrr > 0:
            churn_pct = inp.churned_mrr / inp.total_mrr * 100
            risk += min(10.0, churn_pct * 0.5)
        return round(max(0.0, min(100.0, risk)), 1)

    def _expansion_probability(
        self,
        inp: AccountScoringInput,
        growth_score: float,
        engagement_score: float,
    ) -> float:
        base = (growth_score * 0.6 + engagement_score * 0.4)
        # Boost if upsell opps exist
        if inp.upsell_opportunities > 0:
            base = min(100.0, base + 10.0)
        # Discount if renewal is overdue
        if inp.renewal_date_days < 0:
            base = max(0.0, base - 20.0)
        return round(max(0.0, min(100.0, base)), 1)

    def _composite_score(
        self,
        health: float,
        engagement: float,
        growth: float,
        fit: float,
    ) -> float:
        score = health * 0.35 + engagement * 0.25 + growth * 0.20 + fit * 0.20
        return round(max(0.0, min(100.0, score)), 1)

    def _account_tier(self, inp: AccountScoringInput) -> AccountTier:
        if inp.total_mrr >= 50_000:
            return AccountTier.STRATEGIC
        if inp.total_mrr >= 20_000:
            return AccountTier.ENTERPRISE
        if inp.total_mrr >= 5_000:
            return AccountTier.GROWTH
        if inp.total_mrr >= 1_000:
            return AccountTier.SMB
        return AccountTier.STARTER

    def _account_health(
        self, health_score: float, churn_risk: float
    ) -> AccountHealth:
        if churn_risk >= 70:
            return AccountHealth.CHURNING
        if churn_risk >= 50 or health_score < 35:
            return AccountHealth.AT_RISK
        if health_score >= 75:
            return AccountHealth.EXCELLENT
        if health_score >= 55:
            return AccountHealth.GOOD
        return AccountHealth.FAIR

    def _engagement_level(
        self, engagement_score: float, inp: AccountScoringInput
    ) -> EngagementLevel:
        if engagement_score >= 70:
            return EngagementLevel.HIGH
        if engagement_score >= 45:
            return EngagementLevel.MEDIUM
        if engagement_score >= 20:
            return EngagementLevel.LOW
        return EngagementLevel.DORMANT

    def _account_action(
        self,
        inp: AccountScoringInput,
        health: AccountHealth,
        engagement: EngagementLevel,
        churn_risk: float,
        expansion_prob: float,
    ) -> AccountAction:
        if health == AccountHealth.CHURNING or churn_risk >= 70:
            return AccountAction.RESCUE
        if health == AccountHealth.AT_RISK:
            return AccountAction.RESCUE
        if expansion_prob >= 65 and health in (AccountHealth.EXCELLENT, AccountHealth.GOOD):
            return AccountAction.EXPAND
        if engagement == EngagementLevel.DORMANT:
            return AccountAction.NURTURE
        if health in (AccountHealth.EXCELLENT, AccountHealth.GOOD):
            return AccountAction.RETAIN
        return AccountAction.MONITOR

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                 0,
                "tier_counts":           {},
                "health_counts":         {},
                "engagement_counts":     {},
                "action_counts":         {},
                "avg_health_score":      0.0,
                "avg_composite_score":   0.0,
                "at_risk_count":         0,
                "needs_attention_count": 0,
                "avg_churn_risk":        0.0,
                "avg_expansion_probability": 0.0,
                "high_value_count":      0,
                "avg_growth_score":      0.0,
            }

        tier_counts:       dict[str, int] = {}
        health_counts:     dict[str, int] = {}
        engagement_counts: dict[str, int] = {}
        action_counts:     dict[str, int] = {}
        total_health  = 0.0
        total_comp    = 0.0
        total_churn   = 0.0
        total_expand  = 0.0
        total_growth  = 0.0

        for r in self._results:
            tier_counts[r.account_tier.value]        = tier_counts.get(r.account_tier.value, 0) + 1
            health_counts[r.account_health.value]    = health_counts.get(r.account_health.value, 0) + 1
            engagement_counts[r.engagement_level.value] = engagement_counts.get(r.engagement_level.value, 0) + 1
            action_counts[r.account_action.value]    = action_counts.get(r.account_action.value, 0) + 1
            total_health += r.health_score
            total_comp   += r.composite_score
            total_churn  += r.churn_risk
            total_expand += r.expansion_probability
            total_growth += r.growth_score

        return {
            "total":                     n,
            "tier_counts":               tier_counts,
            "health_counts":             health_counts,
            "engagement_counts":         engagement_counts,
            "action_counts":             action_counts,
            "avg_health_score":          round(total_health / n, 1),
            "avg_composite_score":       round(total_comp / n, 1),
            "at_risk_count":             len(self.at_risk_accounts),
            "needs_attention_count":     len(self.attention_needed),
            "avg_churn_risk":            round(total_churn / n, 1),
            "avg_expansion_probability": round(total_expand / n, 1),
            "high_value_count":          len(self.high_value_accounts),
            "avg_growth_score":          round(total_growth / n, 1),
        }
