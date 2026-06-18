from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExpansionType(str, Enum):
    UPSELL       = "upsell"
    CROSS_SELL   = "cross_sell"
    RENEWAL_PLUS = "renewal_plus"   # renewal with uplift
    PLATFORM_ADD = "platform_add"
    NEW_DIVISION = "new_division"


class ExpansionReadiness(str, Enum):
    READY_NOW       = "ready_now"
    UPCOMING        = "upcoming"      # 60–90 days
    NEEDS_NURTURING = "needs_nurturing"
    NOT_READY       = "not_ready"


class ChurnSignal(str, Enum):
    NONE     = "none"
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class ExpansionAction(str, Enum):
    PITCH_NOW          = "pitch_now"
    SCHEDULE_QBR       = "schedule_qbr"
    NURTURE_ADOPTION   = "nurture_adoption"
    RISK_INTERVENTION  = "risk_intervention"
    REACTIVATE         = "reactivate"
    MAINTAIN_HEALTH    = "maintain_health"


@dataclass
class AccountExpansionInput:
    account_id:               str
    account_name:             str
    csm_id:                   str
    segment:                  str              # smb / mid_market / enterprise
    current_arr:              float
    contract_end_days:        int             # days until contract renewal
    # Product adoption
    product_adoption_pct:     float           # 0–100
    features_used:            int
    total_features_available: int
    active_users:             int
    licensed_users:           int
    # Health signals
    nps_score:                float           # -100 to 100
    support_tickets_open:     int
    support_tickets_resolved: int
    last_qbr_days:            int             # days since last QBR
    executive_engagement:     bool
    # Expansion signals
    expansion_type:           ExpansionType
    expansion_budget_confirmed: bool
    whitespace_products:      int             # products not yet adopted
    internal_champion:        bool
    competitor_conversation:  bool            # are they talking to competitors?
    # Performance
    time_to_value_days:       int             # days to first value realization
    benchmark_ttv_days:       int            # benchmark for segment
    roi_demonstrated:         bool
    growth_since_start_pct:   float          # account revenue growth %
    upsell_attempts:          int


@dataclass
class AccountExpansionResult:
    account_id:               str
    account_name:             str
    csm_id:                   str
    expansion_readiness:      ExpansionReadiness
    churn_signal:             ChurnSignal
    expansion_action:         ExpansionAction
    expansion_score:          float       # 0–100
    health_score:             float       # 0–100
    churn_risk_score:         float       # 0–100
    adoption_rate:            float       # active/licensed users × 100
    feature_utilization:      float       # features_used/total × 100
    expansion_potential:      float       # estimated expansion ARR
    nrr_forecast:             float       # net revenue retention forecast %
    is_at_risk:               bool
    is_ready_to_expand:       bool

    def to_dict(self) -> dict:
        return {
            "account_id":           self.account_id,
            "account_name":         self.account_name,
            "csm_id":               self.csm_id,
            "expansion_readiness":  self.expansion_readiness.value,
            "churn_signal":         self.churn_signal.value,
            "expansion_action":     self.expansion_action.value,
            "expansion_score":      self.expansion_score,
            "health_score":         self.health_score,
            "churn_risk_score":     self.churn_risk_score,
            "adoption_rate":        self.adoption_rate,
            "feature_utilization":  self.feature_utilization,
            "expansion_potential":  self.expansion_potential,
            "nrr_forecast":         self.nrr_forecast,
            "is_at_risk":           self.is_at_risk,
            "is_ready_to_expand":   self.is_ready_to_expand,
        }


class AccountExpansionEngine:
    def __init__(self) -> None:
        self._results: list[AccountExpansionResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: AccountExpansionInput) -> AccountExpansionResult:
        adoption      = self._adoption_rate(inp)
        feat_util     = self._feature_utilization(inp)
        health        = self._health_score(inp, adoption, feat_util)
        churn_risk    = self._churn_risk_score(inp, health, adoption)
        churn_sig     = self._churn_signal(churn_risk)
        exp_score     = self._expansion_score(inp, health, adoption, feat_util)
        readiness     = self._expansion_readiness(inp, exp_score, churn_sig)
        exp_potential = self._expansion_potential(inp, exp_score)
        nrr           = self._nrr_forecast(inp, health, churn_risk, exp_score)
        action        = self._expansion_action(inp, readiness, churn_sig, exp_score)
        at_risk       = churn_sig in (ChurnSignal.HIGH, ChurnSignal.CRITICAL)
        ready         = readiness == ExpansionReadiness.READY_NOW

        result = AccountExpansionResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            csm_id=inp.csm_id,
            expansion_readiness=readiness,
            churn_signal=churn_sig,
            expansion_action=action,
            expansion_score=exp_score,
            health_score=health,
            churn_risk_score=churn_risk,
            adoption_rate=adoption,
            feature_utilization=feat_util,
            expansion_potential=exp_potential,
            nrr_forecast=nrr,
            is_at_risk=at_risk,
            is_ready_to_expand=ready,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[AccountExpansionInput]
    ) -> list[AccountExpansionResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_accounts(self) -> list[AccountExpansionResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def ready_to_expand(self) -> list[AccountExpansionResult]:
        return [r for r in self._results if r.is_ready_to_expand]

    @property
    def high_value_opportunities(self) -> list[AccountExpansionResult]:
        return [r for r in self._results if r.expansion_potential >= 50_000]

    @property
    def total_expansion_potential(self) -> float:
        return round(sum(r.expansion_potential for r in self._results), 2)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _adoption_rate(self, inp: AccountExpansionInput) -> float:
        if inp.licensed_users <= 0:
            return 0.0
        return round(min(100.0, (inp.active_users / inp.licensed_users) * 100), 1)

    def _feature_utilization(self, inp: AccountExpansionInput) -> float:
        if inp.total_features_available <= 0:
            return 0.0
        return round(min(100.0, (inp.features_used / inp.total_features_available) * 100), 1)

    def _health_score(
        self, inp: AccountExpansionInput, adoption: float, feat_util: float
    ) -> float:
        score = 0.0
        # Adoption
        score += adoption * 0.30
        # Feature utilization
        score += feat_util * 0.20
        # NPS
        nps_norm = (inp.nps_score + 100) / 200  # 0–1
        score += nps_norm * 25.0
        # Support health
        if inp.support_tickets_open == 0:       score += 10
        elif inp.support_tickets_open <= 2:     score += 5
        else:                                   score -= 10
        # Executive engagement
        if inp.executive_engagement:            score += 8
        # QBR recency
        if inp.last_qbr_days <= 30:             score += 7
        elif inp.last_qbr_days <= 90:           score += 3
        elif inp.last_qbr_days > 180:           score -= 10
        return round(max(0.0, min(100.0, score)), 1)

    def _churn_risk_score(
        self, inp: AccountExpansionInput, health: float, adoption: float
    ) -> float:
        score = 0.0
        # Low health = churn risk
        if health < 40:      score += 30
        elif health < 60:    score += 15
        # Low adoption
        if adoption < 30:    score += 20
        elif adoption < 60:  score += 10
        # Contract approaching
        if inp.contract_end_days <= 30:   score += 25
        elif inp.contract_end_days <= 60: score += 10
        # Competitor signal
        if inp.competitor_conversation:   score += 20
        # Open support tickets
        if inp.support_tickets_open >= 5: score += 10
        elif inp.support_tickets_open >= 3: score += 5
        return round(max(0.0, min(100.0, score)), 1)

    def _churn_signal(self, churn_risk: float) -> ChurnSignal:
        if churn_risk >= 70: return ChurnSignal.CRITICAL
        if churn_risk >= 50: return ChurnSignal.HIGH
        if churn_risk >= 30: return ChurnSignal.MEDIUM
        if churn_risk >= 10: return ChurnSignal.LOW
        return ChurnSignal.NONE

    def _expansion_score(
        self,
        inp: AccountExpansionInput,
        health: float,
        adoption: float,
        feat_util: float,
    ) -> float:
        score = 0.0
        # Health prerequisite
        score += health * 0.30
        # Adoption indicates engagement
        score += adoption * 0.20
        # Whitespace opportunity
        score += min(20.0, inp.whitespace_products * 4.0)
        # Budget confirmed
        if inp.expansion_budget_confirmed: score += 15
        # Internal champion
        if inp.internal_champion:          score += 10
        # ROI demonstrated
        if inp.roi_demonstrated:           score += 8
        # Competitor risk reduces expansion readiness
        if inp.competitor_conversation:    score -= 15
        # Growth signals expansion willingness
        if inp.growth_since_start_pct >= 20: score += 10
        elif inp.growth_since_start_pct >= 10: score += 5
        return round(max(0.0, min(100.0, score)), 1)

    def _expansion_readiness(
        self,
        inp: AccountExpansionInput,
        exp_score: float,
        churn_sig: ChurnSignal,
    ) -> ExpansionReadiness:
        if churn_sig in (ChurnSignal.HIGH, ChurnSignal.CRITICAL):
            return ExpansionReadiness.NOT_READY
        if exp_score >= 70 and inp.expansion_budget_confirmed:
            return ExpansionReadiness.READY_NOW
        if exp_score >= 55 and inp.contract_end_days <= 90:
            return ExpansionReadiness.UPCOMING
        if exp_score >= 35:
            return ExpansionReadiness.NEEDS_NURTURING
        return ExpansionReadiness.NOT_READY

    def _expansion_potential(self, inp: AccountExpansionInput, exp_score: float) -> float:
        # Base: 20% of current ARR × expansion score factor
        base = inp.current_arr * 0.20 * (exp_score / 100)
        # Whitespace multiplier
        whitespace_mult = 1.0 + (inp.whitespace_products * 0.10)
        return round(base * whitespace_mult, 2)

    def _nrr_forecast(
        self,
        inp: AccountExpansionInput,
        health: float,
        churn_risk: float,
        exp_score: float,
    ) -> float:
        # Base NRR starts at 100 (renewal)
        nrr = 100.0
        # Expansion potential adds to NRR
        nrr += (exp_score / 100) * 30  # up to +30% from expansion
        # Churn risk reduces NRR
        nrr -= (churn_risk / 100) * 40  # up to -40% from churn
        # Health signal
        if health >= 70:  nrr += 5
        elif health < 40: nrr -= 10
        return round(max(0.0, min(200.0, nrr)), 1)

    def _expansion_action(
        self,
        inp: AccountExpansionInput,
        readiness: ExpansionReadiness,
        churn_sig: ChurnSignal,
        exp_score: float,
    ) -> ExpansionAction:
        if churn_sig == ChurnSignal.CRITICAL:
            return ExpansionAction.RISK_INTERVENTION
        if churn_sig == ChurnSignal.HIGH:
            return ExpansionAction.RISK_INTERVENTION
        if readiness == ExpansionReadiness.READY_NOW:
            return ExpansionAction.PITCH_NOW
        if readiness == ExpansionReadiness.UPCOMING:
            return ExpansionAction.SCHEDULE_QBR
        if exp_score < 20 and inp.last_qbr_days > 180:
            return ExpansionAction.REACTIVATE
        if readiness == ExpansionReadiness.NEEDS_NURTURING:
            return ExpansionAction.NURTURE_ADOPTION
        return ExpansionAction.MAINTAIN_HEALTH

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                       0,
                "readiness_counts":            {},
                "churn_signal_counts":         {},
                "action_counts":               {},
                "expansion_type_counts":       {},
                "avg_health_score":            0.0,
                "avg_expansion_score":         0.0,
                "avg_churn_risk_score":        0.0,
                "avg_nrr_forecast":            0.0,
                "total_expansion_potential":   0.0,
                "at_risk_count":               0,
                "ready_to_expand_count":       0,
                "high_value_count":            0,
            }

        readiness_counts: dict[str, int] = {}
        churn_counts:     dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        type_counts:      dict[str, int] = {}
        total_health  = 0.0
        total_exp     = 0.0
        total_churn   = 0.0
        total_nrr     = 0.0

        for r in self._results:
            readiness_counts[r.expansion_readiness.value] = readiness_counts.get(r.expansion_readiness.value, 0) + 1
            churn_counts[r.churn_signal.value]            = churn_counts.get(r.churn_signal.value, 0) + 1
            action_counts[r.expansion_action.value]       = action_counts.get(r.expansion_action.value, 0) + 1
            total_health += r.health_score
            total_exp    += r.expansion_score
            total_churn  += r.churn_risk_score
            total_nrr    += r.nrr_forecast

        return {
            "total":                       n,
            "readiness_counts":            readiness_counts,
            "churn_signal_counts":         churn_counts,
            "action_counts":               action_counts,
            "expansion_type_counts":       type_counts,
            "avg_health_score":            round(total_health / n, 1),
            "avg_expansion_score":         round(total_exp / n, 1),
            "avg_churn_risk_score":        round(total_churn / n, 1),
            "avg_nrr_forecast":            round(total_nrr / n, 1),
            "total_expansion_potential":   self.total_expansion_potential,
            "at_risk_count":               len(self.at_risk_accounts),
            "ready_to_expand_count":       len(self.ready_to_expand),
            "high_value_count":            len(self.high_value_opportunities),
        }
