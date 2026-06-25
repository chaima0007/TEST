from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RenewalRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RenewalAction(str, Enum):
    CLOSE = "close"            # renewal likely, proceed to close
    NURTURE = "nurture"        # healthy but needs engagement
    INTERVENE = "intervene"    # at-risk, active intervention needed
    ESCALATE = "escalate"      # critical, C-level involvement


class RenewalOutcome(str, Enum):
    RENEW = "renew"
    EXPAND = "expand"          # renew + upsell
    DOWNGRADE = "downgrade"    # renew at lower ARR
    CHURN = "churn"


class EngagementTrend(str, Enum):
    GROWING = "growing"
    STABLE = "stable"
    DECLINING = "declining"
    DORMANT = "dormant"


@dataclass
class RenewalInput:
    customer_id: str
    customer_name: str
    arr_eur: float
    segment: str
    # Timeline
    days_to_renewal: int             # negative = already expired
    contract_years: int              # current contract length
    # Health signals
    health_score: float              # 0-100 (from account health engine)
    nps_score: int                   # -100 to 100
    product_usage_trend: str         # "growing" / "stable" / "declining" / "dormant"
    # Commercial signals
    has_expansion_discussion: bool
    discount_requested: bool
    competitor_mentioned: bool
    price_sensitivity: str           # "low" / "medium" / "high"
    # Relationship
    exec_sponsor_aligned: bool
    champion_strength: int           # 0-10
    open_support_issues: int
    # Historical
    previous_renewal_on_time: bool
    years_as_customer: int


@dataclass
class RenewalResult:
    customer_id: str
    customer_name: str
    arr_eur: float
    segment: str
    days_to_renewal: int
    renewal_risk: RenewalRisk
    renewal_action: RenewalAction
    predicted_outcome: RenewalOutcome
    engagement_trend: EngagementTrend
    renewal_probability_pct: float
    expected_arr_change_pct: float   # positive = expansion, negative = downgrade/churn
    risk_signals: list[str]
    positive_signals: list[str]
    renewal_plays: list[str]
    urgency_score: float             # 0-100, combines risk + time pressure

    def to_dict(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "arr_eur": self.arr_eur,
            "segment": self.segment,
            "days_to_renewal": self.days_to_renewal,
            "renewal_risk": self.renewal_risk.value,
            "renewal_action": self.renewal_action.value,
            "predicted_outcome": self.predicted_outcome.value,
            "engagement_trend": self.engagement_trend.value,
            "renewal_probability_pct": self.renewal_probability_pct,
            "expected_arr_change_pct": self.expected_arr_change_pct,
            "risk_signals": self.risk_signals,
            "positive_signals": self.positive_signals,
            "renewal_plays": self.renewal_plays,
            "urgency_score": self.urgency_score,
        }


def _renewal_risk_score(inp: RenewalInput) -> float:
    score = 0.0
    # Health (max 30): inverted — low health = high risk
    if inp.health_score < 40:
        score += 30.0
    elif inp.health_score < 60:
        score += 18.0
    elif inp.health_score < 75:
        score += 8.0
    # NPS (max 20)
    if inp.nps_score < -20:
        score += 20.0
    elif inp.nps_score < 0:
        score += 12.0
    elif inp.nps_score < 20:
        score += 4.0
    # Usage trend (max 20)
    usage_penalties = {"dormant": 20, "declining": 12, "stable": 3, "growing": 0}
    score += usage_penalties.get(inp.product_usage_trend, 0)
    # Commercial signals (max 15)
    if inp.competitor_mentioned:
        score += 7.0
    if inp.discount_requested:
        score += 5.0
    if inp.price_sensitivity == "high":
        score += 3.0
    elif inp.price_sensitivity == "medium":
        score += 1.0
    # Relationship (max 10)
    if not inp.exec_sponsor_aligned:
        score += 5.0
    if inp.champion_strength <= 3:
        score += 3.0
    if inp.open_support_issues >= 2:
        score += 2.0
    # History (max 5)
    if not inp.previous_renewal_on_time:
        score += 3.0
    if inp.years_as_customer == 0:
        score += 2.0
    return round(min(100.0, max(0.0, score)), 1)


def _renewal_risk(score: float) -> RenewalRisk:
    if score >= 60:
        return RenewalRisk.CRITICAL
    if score >= 40:
        return RenewalRisk.HIGH
    if score >= 20:
        return RenewalRisk.MODERATE
    return RenewalRisk.LOW


def _renewal_action(risk: RenewalRisk, days: int) -> RenewalAction:
    if risk == RenewalRisk.CRITICAL or (risk == RenewalRisk.HIGH and days <= 30):
        return RenewalAction.ESCALATE
    if risk == RenewalRisk.HIGH:
        return RenewalAction.INTERVENE
    if risk == RenewalRisk.MODERATE:
        return RenewalAction.NURTURE
    return RenewalAction.CLOSE


def _engagement_trend(inp: RenewalInput) -> EngagementTrend:
    trend_map = {
        "growing": EngagementTrend.GROWING,
        "stable": EngagementTrend.STABLE,
        "declining": EngagementTrend.DECLINING,
        "dormant": EngagementTrend.DORMANT,
    }
    return trend_map.get(inp.product_usage_trend, EngagementTrend.STABLE)


def _renewal_probability(score: float, inp: RenewalInput) -> float:
    base = max(0.0, 95.0 - score * 0.9)
    # Modifiers
    if inp.has_expansion_discussion:
        base += 5.0
    if inp.exec_sponsor_aligned and inp.champion_strength >= 7:
        base += 4.0
    if inp.years_as_customer >= 3:
        base += 3.0
    if inp.previous_renewal_on_time:
        base += 2.0
    if inp.competitor_mentioned:
        base -= 5.0
    if inp.days_to_renewal <= 0:
        base -= 10.0
    return round(max(0.0, min(100.0, base)), 1)


def _predicted_outcome(
    risk: RenewalRisk, prob: float, inp: RenewalInput
) -> RenewalOutcome:
    if prob < 30 or risk == RenewalRisk.CRITICAL:
        return RenewalOutcome.CHURN
    if inp.discount_requested and not inp.has_expansion_discussion:
        return RenewalOutcome.DOWNGRADE
    if inp.has_expansion_discussion and inp.health_score >= 65:
        return RenewalOutcome.EXPAND
    return RenewalOutcome.RENEW


def _expected_arr_change(outcome: RenewalOutcome, inp: RenewalInput) -> float:
    if outcome == RenewalOutcome.CHURN:
        return -100.0
    if outcome == RenewalOutcome.DOWNGRADE:
        return -20.0 if inp.price_sensitivity == "high" else -10.0
    if outcome == RenewalOutcome.EXPAND:
        return 25.0 if inp.has_expansion_discussion and inp.health_score >= 80 else 15.0
    return 0.0


def _urgency_score(risk_score: float, days: int) -> float:
    time_factor = 0.0
    if days <= 0:
        time_factor = 30.0
    elif days <= 30:
        time_factor = 25.0
    elif days <= 60:
        time_factor = 15.0
    elif days <= 90:
        time_factor = 8.0
    return round(min(100.0, risk_score * 0.7 + time_factor), 1)


def _risk_signals(inp: RenewalInput, score: float) -> list[str]:
    signals: list[str] = []
    if inp.health_score < 40:
        signals.append(f"Score santé critique ({inp.health_score}/100) — risque de non-renouvellement")
    if inp.nps_score < 0:
        signals.append(f"NPS négatif ({inp.nps_score}) — insatisfaction client")
    if inp.product_usage_trend in ("declining", "dormant"):
        signals.append(f"Usage produit {inp.product_usage_trend} — signal de désengagement")
    if inp.competitor_mentioned:
        signals.append("Concurrent mentionné — risque de displacement")
    if inp.discount_requested:
        signals.append("Remise demandée — signal de sensibilité prix")
    if not inp.exec_sponsor_aligned:
        signals.append("Sponsor exécutif non aligné — renouvellement fragile")
    if inp.champion_strength <= 3:
        signals.append(f"Champion faible ({inp.champion_strength}/10) — défenseur interne insuffisant")
    if inp.open_support_issues >= 2:
        signals.append(f"{inp.open_support_issues} tickets support ouverts — satisfaction impactée")
    if inp.days_to_renewal <= 30 and inp.days_to_renewal >= 0:
        signals.append(f"Renouvellement dans {inp.days_to_renewal}j — urgence critique")
    if inp.days_to_renewal < 0:
        signals.append(f"Contrat expiré depuis {abs(inp.days_to_renewal)}j — situation urgente")
    return signals


def _positive_signals(inp: RenewalInput, score: float) -> list[str]:
    signals: list[str] = []
    if inp.health_score >= 75:
        signals.append(f"Score santé élevé ({inp.health_score}/100) — compte en bonne forme")
    if inp.nps_score >= 30:
        signals.append(f"NPS excellent ({inp.nps_score}) — client promoteur actif")
    if inp.product_usage_trend == "growing":
        signals.append("Usage produit en croissance — valeur perçue en hausse")
    if inp.has_expansion_discussion:
        signals.append("Discussion expansion en cours — signal d'upsell positif")
    if inp.exec_sponsor_aligned:
        signals.append("Sponsor exécutif aligné — renouvellement facilité")
    if inp.champion_strength >= 7:
        signals.append(f"Champion fort ({inp.champion_strength}/10) — défenseur interne actif")
    if inp.years_as_customer >= 3:
        signals.append(f"{inp.years_as_customer} ans client — relation établie et fidèle")
    if inp.previous_renewal_on_time:
        signals.append("Renouvellement précédent ponctuel — historique favorable")
    return signals


def _renewal_plays(
    risk: RenewalRisk, action: RenewalAction, inp: RenewalInput, outcome: RenewalOutcome
) -> list[str]:
    plays: list[str] = []
    if action == RenewalAction.ESCALATE:
        plays.append("Escalade C-level — mobiliser direction et executive sponsor d'urgence")
        plays.append("EBR d'urgence — valeur démontrée, roadmap personnalisée, ROI calculé")
        if inp.competitor_mentioned:
            plays.append("Préparer un battlecard concurrentiel — arguments de différenciation")
        plays.append("Proposer une extension contractuelle temporaire — éviter la rupture")
    elif action == RenewalAction.INTERVENE:
        plays.append("Réunion de renouvellement stratégique — CEO/VP Sales + champion client")
        plays.append("Présenter un rapport ROI personnalisé — quantifier la valeur délivrée")
        if inp.discount_requested:
            plays.append("Structurer une offre de renouvellement attractive — valeur vs. remise")
    elif action == RenewalAction.NURTURE:
        plays.append("QBR de renouvellement — aligner sur les objectifs de la prochaine période")
        plays.append("Identifier et activer les cas d'usage non utilisés — maximiser la valeur")
        if inp.has_expansion_discussion:
            plays.append("Formaliser la discussion expansion — proposition commerciale à préparer")
    else:
        plays.append("Engager le processus de renouvellement — dossier commercial à préparer")
        plays.append("Valider les conditions contractuelles — anticiper les demandes")
        if outcome == RenewalOutcome.EXPAND:
            plays.append("Inclure un volet expansion dans la proposition — opportunité upsell")
    return plays


class RenewalIntelligenceEngine:
    def __init__(self) -> None:
        self._results: dict[str, RenewalResult] = {}

    def analyze(self, inp: RenewalInput) -> RenewalResult:
        risk_score = _renewal_risk_score(inp)
        risk = _renewal_risk(risk_score)
        action = _renewal_action(risk, inp.days_to_renewal)
        trend = _engagement_trend(inp)
        prob = _renewal_probability(risk_score, inp)
        outcome = _predicted_outcome(risk, prob, inp)
        arr_change = _expected_arr_change(outcome, inp)
        urgency = _urgency_score(risk_score, inp.days_to_renewal)
        result = RenewalResult(
            customer_id=inp.customer_id,
            customer_name=inp.customer_name,
            arr_eur=inp.arr_eur,
            segment=inp.segment,
            days_to_renewal=inp.days_to_renewal,
            renewal_risk=risk,
            renewal_action=action,
            predicted_outcome=outcome,
            engagement_trend=trend,
            renewal_probability_pct=prob,
            expected_arr_change_pct=arr_change,
            risk_signals=_risk_signals(inp, risk_score),
            positive_signals=_positive_signals(inp, risk_score),
            renewal_plays=_renewal_plays(risk, action, inp, outcome),
            urgency_score=urgency,
        )
        self._results[inp.customer_id] = result
        return result

    def analyze_batch(self, customers: list[RenewalInput]) -> list[RenewalResult]:
        results = [self.analyze(c) for c in customers]
        return sorted(results, key=lambda r: r.urgency_score, reverse=True)

    def all_renewals(self) -> list[RenewalResult]:
        return sorted(self._results.values(), key=lambda r: r.urgency_score, reverse=True)

    def by_risk(self, risk: RenewalRisk) -> list[RenewalResult]:
        return [r for r in self._results.values() if r.renewal_risk == risk]

    def by_action(self, action: RenewalAction) -> list[RenewalResult]:
        return [r for r in self._results.values() if r.renewal_action == action]

    def by_outcome(self, outcome: RenewalOutcome) -> list[RenewalResult]:
        return [r for r in self._results.values() if r.predicted_outcome == outcome]

    def critical_renewals(self) -> list[RenewalResult]:
        return self.by_risk(RenewalRisk.CRITICAL)

    def needs_escalation(self) -> list[RenewalResult]:
        return self.by_action(RenewalAction.ESCALATE)

    def expansion_opportunities(self) -> list[RenewalResult]:
        return self.by_outcome(RenewalOutcome.EXPAND)

    def at_risk_renewals(self) -> list[RenewalResult]:
        return [
            r for r in self._results.values()
            if r.renewal_risk in (RenewalRisk.HIGH, RenewalRisk.CRITICAL)
        ]

    def due_soon(self, within_days: int = 90) -> list[RenewalResult]:
        return [
            r for r in self._results.values()
            if 0 <= r.days_to_renewal <= within_days
        ]

    def avg_renewal_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.renewal_probability_pct for r in self._results.values()) / len(self._results), 1)

    def total_arr_at_risk_eur(self) -> float:
        return sum(
            r.arr_eur for r in self._results.values()
            if r.renewal_risk in (RenewalRisk.HIGH, RenewalRisk.CRITICAL)
        )

    def expected_arr_delta_eur(self) -> float:
        return sum(
            r.arr_eur * r.expected_arr_change_pct / 100.0
            for r in self._results.values()
        )

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "risk_counts": {r.value: sum(1 for x in all_r if x.renewal_risk == r) for r in RenewalRisk},
            "action_counts": {a.value: sum(1 for x in all_r if x.renewal_action == a) for a in RenewalAction},
            "outcome_counts": {o.value: sum(1 for x in all_r if x.predicted_outcome == o) for o in RenewalOutcome},
            "avg_renewal_probability_pct": self.avg_renewal_probability(),
            "critical_count": len(self.critical_renewals()),
            "escalation_count": len(self.needs_escalation()),
            "total_arr_at_risk_eur": self.total_arr_at_risk_eur(),
            "expected_arr_delta_eur": round(self.expected_arr_delta_eur(), 0),
        }

    def reset(self) -> None:
        self._results.clear()
