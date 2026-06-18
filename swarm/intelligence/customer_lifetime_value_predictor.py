"""Module 38 — Customer Lifetime Value Predictor

Predicts the 3-year customer lifetime value (CLV) for each account based on
contract value, renewal history, expansion signals, engagement health, and
competitive risk.  Segments accounts into CLV tiers for prioritised CS,
expansion, and retention resource allocation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class CLVTier(str, Enum):
    PLATINUM = "platinum"    # CLV ≥ 500 k€ over 3 years
    GOLD     = "gold"        # CLV ≥ 200 k€
    SILVER   = "silver"      # CLV ≥ 80 k€
    BRONZE   = "bronze"      # CLV ≥ 20 k€
    MINIMAL  = "minimal"     # CLV < 20 k€


class ExpansionPotential(str, Enum):
    HIGH   = "high"     # strong upsell / cross-sell indicators
    MEDIUM = "medium"
    LOW    = "low"
    NONE   = "none"     # account at risk or churning


class ChurnRisk(str, Enum):
    CRITICAL = "critical"   # likely to churn within 90 days
    HIGH     = "high"       # elevated risk within 6 months
    MEDIUM   = "medium"     # some risk signals
    LOW      = "low"        # healthy account


class CLVAction(str, Enum):
    INVEST    = "invest"      # PLATINUM/GOLD — maximise retention + expansion
    GROW      = "grow"        # SILVER — targeted upsell campaigns
    NURTURE   = "nurture"     # BRONZE — maintain relationship
    MONITOR   = "monitor"     # low CLV + some risk — watch closely
    RESCUE    = "rescue"      # high churn risk — urgent CS intervention


# ─── Input ───────────────────────────────────────────────────────────────────

@dataclass
class CLVInput:
    account_id: str
    account_name: str
    region: str
    segment: str
    # Contract financials
    arr_eur: float                          # annual recurring revenue
    contract_start_months_ago: int         # months since first contract
    contract_length_months: int            # initial contract length
    # Renewal history
    renewals_completed: int                # number of successful renewals
    avg_renewal_growth_pct: float          # average ARR growth at renewal (%)
    last_renewal_months_ago: int           # months since last renewal (0 = active)
    # Expansion signals
    seats_used_pct: float                  # licence utilisation 0–100
    products_adopted: int                  # number of product modules active
    total_products_available: int          # total modules in portfolio
    expansion_conversations_open: bool    # active upsell discussion
    # Engagement / health
    nps_score: float                       # −100 to +100
    support_tickets_90d: int               # support volume in last 90 days
    executive_sponsor_engaged: bool
    last_qbr_months_ago: int               # months since last QBR / EBR
    # Risk signals
    competitor_evaluation_active: bool
    key_champion_left: bool
    payment_delays_12m: int                # number of late payments last 12 months
    # Rep estimates
    rep_churn_risk_score: float            # rep's subjective assessment 0–10 (10=certain churn)


# ─── Output ──────────────────────────────────────────────────────────────────

@dataclass
class CLVResult:
    account_id: str
    account_name: str
    region: str
    segment: str
    arr_eur: float

    # Predicted values
    clv_3yr_eur: float               # 3-year lifetime value projection
    clv_tier: CLVTier
    expansion_potential: ExpansionPotential
    churn_risk: ChurnRisk
    clv_action: CLVAction
    health_score: float              # 0–100 composite
    churn_probability_pct: float     # 0–100 estimated churn probability
    expansion_opportunity_eur: float # potential upsell ARR
    predicted_arr_yr2_eur: float
    predicted_arr_yr3_eur: float

    # Narrative
    value_drivers: list[str]
    risk_signals: list[str]
    recommended_plays: list[str]

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "account_name": self.account_name,
            "region": self.region,
            "segment": self.segment,
            "arr_eur": self.arr_eur,
            "clv_3yr_eur": self.clv_3yr_eur,
            "clv_tier": self.clv_tier.value,
            "expansion_potential": self.expansion_potential.value,
            "churn_risk": self.churn_risk.value,
            "clv_action": self.clv_action.value,
            "health_score": self.health_score,
            "churn_probability_pct": self.churn_probability_pct,
            "expansion_opportunity_eur": self.expansion_opportunity_eur,
            "predicted_arr_yr2_eur": self.predicted_arr_yr2_eur,
            "predicted_arr_yr3_eur": self.predicted_arr_yr3_eur,
            "value_drivers": self.value_drivers,
            "risk_signals": self.risk_signals,
            "recommended_plays": self.recommended_plays,
        }


# ─── Engine ──────────────────────────────────────────────────────────────────

class CustomerLifetimeValuePredictor:

    def __init__(self) -> None:
        self._results: list[CLVResult] = []

    # ── private helpers ────────────────────────────────────────────────────

    def _health_score(self, inp: CLVInput) -> float:
        """
        0–100 composite health score:
          NPS              20 pts  → (nps + 100) / 200 × 20
          utilisation      20 pts  → seats_used_pct / 100 × 20
          adoption         15 pts  → products_adopted / total × 15
          renewals         15 pts  → min(15, renewals_completed × 5)
          support risk     10 pts  → max(0, 10 − tickets × 1.5)
          exec sponsor     10 pts  → 10 if engaged else 0
          QBR recency      10 pts  → max(0, 10 − last_qbr × 2)
        """
        nps_pts   = (inp.nps_score + 100.0) / 200.0 * 20.0
        util_pts  = (inp.seats_used_pct / 100.0) * 20.0
        adop_pts  = (
            (inp.products_adopted / inp.total_products_available) * 15.0
            if inp.total_products_available > 0 else 0.0
        )
        renew_pts   = min(15.0, inp.renewals_completed * 5.0)
        support_pts = max(0.0, 10.0 - inp.support_tickets_90d * 1.5)
        exec_pts    = 10.0 if inp.executive_sponsor_engaged else 0.0
        qbr_pts     = max(0.0, 10.0 - inp.last_qbr_months_ago * 2.0)

        raw = nps_pts + util_pts + adop_pts + renew_pts + support_pts + exec_pts + qbr_pts
        return round(min(100.0, max(0.0, raw)), 1)

    def _churn_probability(self, inp: CLVInput, health: float) -> float:
        """
        Base probability from health score (inverted), then add risk signals.
        Clamped [0, 95].
        """
        base = max(0.0, 100.0 - health) * 0.6   # health 0→100 maps to base 60→0
        extra = 0.0
        if inp.competitor_evaluation_active:
            extra += 20.0
        if inp.key_champion_left:
            extra += 15.0
        if inp.payment_delays_12m >= 2:
            extra += 10.0
        if inp.rep_churn_risk_score >= 7:
            extra += 15.0
        elif inp.rep_churn_risk_score >= 5:
            extra += 8.0
        if inp.last_renewal_months_ago > inp.contract_length_months:
            extra += 10.0  # overdue renewal

        raw = base + extra
        return round(min(95.0, max(0.0, raw)), 1)

    def _churn_risk(self, churn_prob: float) -> ChurnRisk:
        if churn_prob >= 60:
            return ChurnRisk.CRITICAL
        if churn_prob >= 40:
            return ChurnRisk.HIGH
        if churn_prob >= 20:
            return ChurnRisk.MEDIUM
        return ChurnRisk.LOW

    def _expansion_opportunity_eur(self, inp: CLVInput) -> float:
        """Estimate additional ARR available if account expands fully."""
        # Whitespace: unused seats * per-seat revenue approximation
        unused_pct = max(0.0, (100.0 - inp.seats_used_pct) / 100.0)
        seat_whitespace = inp.arr_eur * unused_pct * 0.5  # conservative 50% uptake

        # Product cross-sell
        products_gap = max(0, inp.total_products_available - inp.products_adopted)
        product_whitespace = inp.arr_eur * (products_gap / max(1, inp.total_products_available)) * 0.4

        return round(seat_whitespace + product_whitespace, 0)

    def _expansion_potential(self, inp: CLVInput, churn_risk: ChurnRisk) -> ExpansionPotential:
        if churn_risk == ChurnRisk.CRITICAL:
            return ExpansionPotential.NONE
        score = 0
        if inp.seats_used_pct >= 80:
            score += 2
        elif inp.seats_used_pct >= 60:
            score += 1
        if inp.products_adopted < inp.total_products_available:
            score += 2
        if inp.expansion_conversations_open:
            score += 2
        if inp.executive_sponsor_engaged:
            score += 1
        if inp.nps_score >= 40:
            score += 1
        if score >= 6:
            return ExpansionPotential.HIGH
        if score >= 3:
            return ExpansionPotential.MEDIUM
        if score >= 1:
            return ExpansionPotential.LOW
        return ExpansionPotential.NONE

    def _growth_rate(self, inp: CLVInput, churn_prob: float) -> float:
        """Expected annual growth rate, discounted by churn probability."""
        base_growth = max(0.0, inp.avg_renewal_growth_pct / 100.0)
        churn_discount = churn_prob / 100.0
        # If churning likely, survival-adjust
        survival = 1.0 - churn_discount * 0.8
        return base_growth * survival

    def _predicted_arr(self, inp: CLVInput, churn_prob: float) -> tuple[float, float]:
        """Returns (yr2_arr, yr3_arr)."""
        growth = self._growth_rate(inp, churn_prob)
        yr2 = inp.arr_eur * (1.0 + growth)
        yr3 = yr2 * (1.0 + growth)
        # Apply churn probability to reduce expected revenue
        survival_yr2 = 1.0 - (churn_prob / 100.0) * 0.5
        survival_yr3 = survival_yr2 * (1.0 - (churn_prob / 100.0) * 0.3)
        return (round(yr2 * survival_yr2, 0), round(yr3 * survival_yr3, 0))

    def _clv_3yr(self, inp: CLVInput, yr2: float, yr3: float) -> float:
        return round(inp.arr_eur + yr2 + yr3, 0)

    def _clv_tier(self, clv: float) -> CLVTier:
        if clv >= 500_000:
            return CLVTier.PLATINUM
        if clv >= 200_000:
            return CLVTier.GOLD
        if clv >= 80_000:
            return CLVTier.SILVER
        if clv >= 20_000:
            return CLVTier.BRONZE
        return CLVTier.MINIMAL

    def _clv_action(
        self, tier: CLVTier, churn_risk: ChurnRisk, expansion: ExpansionPotential
    ) -> CLVAction:
        if churn_risk in (ChurnRisk.CRITICAL, ChurnRisk.HIGH):
            return CLVAction.RESCUE
        if tier in (CLVTier.PLATINUM, CLVTier.GOLD):
            return CLVAction.INVEST
        if tier == CLVTier.SILVER and expansion in (ExpansionPotential.HIGH, ExpansionPotential.MEDIUM):
            return CLVAction.GROW
        if tier == CLVTier.BRONZE:
            return CLVAction.NURTURE
        if churn_risk == ChurnRisk.MEDIUM:
            return CLVAction.MONITOR
        return CLVAction.NURTURE

    def _value_drivers(self, inp: CLVInput) -> list[str]:
        drivers: list[str] = []
        if inp.arr_eur >= 100_000:
            drivers.append(f"ARR élevé ({inp.arr_eur:,.0f}€) — compte stratégique")
        if inp.renewals_completed >= 2:
            drivers.append(f"{inp.renewals_completed} renouvellements réussis — fidélité prouvée")
        if inp.avg_renewal_growth_pct > 10:
            drivers.append(f"Croissance ARR moyenne {inp.avg_renewal_growth_pct:.0f}% — expansion historique forte")
        if inp.seats_used_pct >= 80:
            drivers.append(f"Utilisation licences {inp.seats_used_pct:.0f}% — engagement utilisateurs élevé")
        if inp.products_adopted >= 3:
            drivers.append(f"{inp.products_adopted} modules adoptés — stickiness multi-produit")
        if inp.nps_score >= 40:
            drivers.append(f"NPS {inp.nps_score:.0f} — promoteur actif")
        if inp.executive_sponsor_engaged:
            drivers.append("Sponsor exécutif engagé — relation stratégique sécurisée")
        if not drivers:
            drivers.append("Compte à potentiel limité — concentration sur la rétention basique")
        return drivers

    def _risk_signals(self, inp: CLVInput) -> list[str]:
        signals: list[str] = []
        if inp.competitor_evaluation_active:
            signals.append("Évaluation concurrente active — risque de départ imminent")
        if inp.key_champion_left:
            signals.append("Champion clé parti — relation à reconstruire urgemment")
        if inp.payment_delays_12m >= 2:
            signals.append(f"{inp.payment_delays_12m} retards de paiement — tension financière côté client")
        if inp.rep_churn_risk_score >= 7:
            signals.append(f"Score churn rep {inp.rep_churn_risk_score}/10 — signal d'alerte critique")
        if inp.nps_score < 0:
            signals.append(f"NPS négatif ({inp.nps_score:.0f}) — insatisfaction client")
        if inp.support_tickets_90d >= 5:
            signals.append(f"{inp.support_tickets_90d} tickets support en 90j — friction produit")
        if inp.last_qbr_months_ago > 6:
            signals.append(f"Dernier QBR il y a {inp.last_qbr_months_ago} mois — relation négligée")
        return signals

    def _recommended_plays(
        self, tier: CLVTier, churn_risk: ChurnRisk, expansion: ExpansionPotential, inp: CLVInput
    ) -> list[str]:
        plays: list[str] = []
        if churn_risk in (ChurnRisk.CRITICAL, ChurnRisk.HIGH):
            plays += [
                "Appel exécutif dans les 48h — escalade senior",
                "Identifier et neutraliser le concurrent en évaluation",
                "Proposer un plan de valeur personnalisé (ROI review)",
            ]
        elif tier in (CLVTier.PLATINUM, CLVTier.GOLD):
            plays += [
                "QBR stratégique avec le C-level — présentation roadmap",
                "Executive Sponsor Program — renforcer les liens exécutifs",
            ]
        if expansion in (ExpansionPotential.HIGH, ExpansionPotential.MEDIUM):
            plays += [
                f"Session de découverte expansion — présenter les {inp.total_products_available - inp.products_adopted} modules non adoptés",
                "Construire le business case d'expansion basé sur l'utilisation actuelle",
            ]
        if inp.seats_used_pct >= 80:
            plays.append("Proposer une montée en gamme de licences — 80%+ d'utilisation")
        if inp.last_qbr_months_ago > 3:
            plays.append("Planifier un QBR — dernière réunion stratégique trop ancienne")
        if not plays:
            plays.append("Maintenir le contact régulier — newsletter produit + invitations événements")
        return plays

    # ── public API ─────────────────────────────────────────────────────────

    def predict(self, inp: CLVInput) -> CLVResult:
        health     = self._health_score(inp)
        churn_prob = self._churn_probability(inp, health)
        churn_risk = self._churn_risk(churn_prob)
        expansion_opp = self._expansion_opportunity_eur(inp)
        expansion_pot = self._expansion_potential(inp, churn_risk)
        yr2, yr3   = self._predicted_arr(inp, churn_prob)
        clv        = self._clv_3yr(inp, yr2, yr3)
        tier       = self._clv_tier(clv)
        action     = self._clv_action(tier, churn_risk, expansion_pot)

        result = CLVResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            region=inp.region,
            segment=inp.segment,
            arr_eur=inp.arr_eur,
            clv_3yr_eur=clv,
            clv_tier=tier,
            expansion_potential=expansion_pot,
            churn_risk=churn_risk,
            clv_action=action,
            health_score=health,
            churn_probability_pct=churn_prob,
            expansion_opportunity_eur=expansion_opp,
            predicted_arr_yr2_eur=yr2,
            predicted_arr_yr3_eur=yr3,
            value_drivers=self._value_drivers(inp),
            risk_signals=self._risk_signals(inp),
            recommended_plays=self._recommended_plays(tier, churn_risk, expansion_pot, inp),
        )
        self._results.append(result)
        return result

    def predict_batch(self, inputs: list[CLVInput]) -> list[CLVResult]:
        """Predict batch, sorted DESC by clv_3yr_eur (highest value first)."""
        results = [self.predict(inp) for inp in inputs]
        results.sort(key=lambda r: r.clv_3yr_eur, reverse=True)
        return results

    # ── filter helpers ─────────────────────────────────────────────────────

    def all_accounts(self) -> list[CLVResult]:
        return list(self._results)

    def by_tier(self, tier: CLVTier) -> list[CLVResult]:
        return [r for r in self._results if r.clv_tier == tier]

    def by_churn_risk(self, risk: ChurnRisk) -> list[CLVResult]:
        return [r for r in self._results if r.churn_risk == risk]

    def by_expansion(self, potential: ExpansionPotential) -> list[CLVResult]:
        return [r for r in self._results if r.expansion_potential == potential]

    def by_action(self, action: CLVAction) -> list[CLVResult]:
        return [r for r in self._results if r.clv_action == action]

    def platinum_accounts(self) -> list[CLVResult]:
        return self.by_tier(CLVTier.PLATINUM)

    def at_risk_accounts(self) -> list[CLVResult]:
        return [
            r for r in self._results
            if r.churn_risk in (ChurnRisk.CRITICAL, ChurnRisk.HIGH)
        ]

    def high_expansion_accounts(self) -> list[CLVResult]:
        return self.by_expansion(ExpansionPotential.HIGH)

    def needs_rescue(self) -> list[CLVResult]:
        return self.by_action(CLVAction.RESCUE)

    # ── aggregates ─────────────────────────────────────────────────────────

    def total_clv_eur(self) -> float:
        return sum(r.clv_3yr_eur for r in self._results)

    def total_arr_eur(self) -> float:
        return sum(r.arr_eur for r in self._results)

    def total_expansion_opportunity_eur(self) -> float:
        return sum(r.expansion_opportunity_eur for r in self._results)

    def avg_health_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.health_score for r in self._results) / len(self._results), 1)

    def at_risk_arr_eur(self) -> float:
        return sum(r.arr_eur for r in self.at_risk_accounts())

    def summary(self) -> dict:
        n = len(self._results)
        tier_counts: dict[str, int]   = {}
        risk_counts: dict[str, int]   = {}
        action_counts: dict[str, int] = {}
        exp_counts: dict[str, int]    = {}
        for r in self._results:
            tier_counts[r.clv_tier.value]           = tier_counts.get(r.clv_tier.value, 0) + 1
            risk_counts[r.churn_risk.value]         = risk_counts.get(r.churn_risk.value, 0) + 1
            action_counts[r.clv_action.value]       = action_counts.get(r.clv_action.value, 0) + 1
            exp_counts[r.expansion_potential.value] = exp_counts.get(r.expansion_potential.value, 0) + 1
        return {
            "total": n,
            "tier_counts": tier_counts,
            "churn_risk_counts": risk_counts,
            "action_counts": action_counts,
            "expansion_counts": exp_counts,
            "avg_health_score": self.avg_health_score(),
            "total_clv_eur": self.total_clv_eur(),
            "total_arr_eur": self.total_arr_eur(),
            "total_expansion_opportunity_eur": self.total_expansion_opportunity_eur(),
            "at_risk_arr_eur": self.at_risk_arr_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
