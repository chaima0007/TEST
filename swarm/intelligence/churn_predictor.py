"""Churn Predictor — predicts customer churn probability and recommends retention actions."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class ChurnRisk(str, Enum):
    CRITICAL = "critical"   # >=80% churn probability
    HIGH = "high"           # >=60%
    MEDIUM = "medium"       # >=40%
    LOW = "low"             # >=20%
    SAFE = "safe"           # <20%


class RetentionAction(str, Enum):
    EMERGENCY = "emergency"     # immediate executive intervention
    RESCUE = "rescue"           # dedicated rescue plan
    PROACTIVE = "proactive"     # proactive outreach required
    NURTURE = "nurture"         # regular nurture cadence
    EXPAND = "expand"           # safe to expand/upsell


@dataclass
class ChurnInput:
    account_id: str
    account_name: str
    arr_eur: float
    contract_end_days: int          # days until contract renewal

    # Usage signals
    monthly_active_users: int
    mau_trend_pct: float            # -100 to +100 (negative = decline)
    feature_adoption_pct: float     # 0-100
    login_frequency_days: float     # avg days between logins (lower = better)

    # Support signals
    open_tickets: int
    overdue_tickets: int
    critical_bugs_open: int
    avg_ticket_resolution_days: float

    # Financial signals
    payment_delays: int             # number of late payments
    invoice_disputes: int

    # Relationship signals
    champion_lost: bool
    executive_sponsor_engaged: bool
    nps_score: int                  # -100 to 100
    nps_trend: str                  # "improving" / "stable" / "declining"
    last_qbr_days: int              # days since last Quarterly Business Review

    # Competitive signals
    competitor_mentioned: bool
    rfp_received: bool


@dataclass
class ChurnResult:
    account_id: str
    account_name: str
    arr_eur: float
    churn_probability_pct: float
    churn_risk: ChurnRisk
    retention_action: RetentionAction
    churn_drivers: list[str]
    retention_signals: list[str]
    risk_flags: list[str]
    recommended_actions: list[str]
    arr_at_risk_eur: float
    days_to_act: int

    # Component scores (0-100 each)
    usage_risk_score: float
    support_risk_score: float
    financial_risk_score: float
    relationship_risk_score: float
    competitive_risk_score: float

    def to_dict(self) -> dict:
        d = asdict(self)
        d["churn_risk"] = self.churn_risk.value
        d["retention_action"] = self.retention_action.value
        return d


# ─── Risk component calculators ──────────────────────────────────────────────

def _usage_risk(inp: ChurnInput) -> float:
    # MAU trend: most impactful signal
    if inp.mau_trend_pct < 0:
        mau_score = min(80, -inp.mau_trend_pct * 1.2)
    else:
        mau_score = 0.0

    # Feature adoption: low adoption = high risk
    if inp.feature_adoption_pct < 50:
        adoption_risk = min(40, (50 - inp.feature_adoption_pct) * 0.8)
    else:
        adoption_risk = 0.0

    # Login frequency: infrequent logins signal disengagement
    if inp.login_frequency_days > 3:
        login_risk = min(40, (inp.login_frequency_days - 3) * 5)
    else:
        login_risk = 0.0

    return round(min(100, mau_score * 0.50 + adoption_risk * 0.30 + login_risk * 0.20), 2)


def _support_risk(inp: ChurnInput) -> float:
    ticket_score = min(25, inp.open_tickets * 5)
    overdue_score = min(30, inp.overdue_tickets * 10)
    bug_score = min(40, inp.critical_bugs_open * 15)
    resolution_penalty = (
        min(20, (inp.avg_ticket_resolution_days - 5) * 3)
        if inp.avg_ticket_resolution_days > 5
        else 0
    )
    return round(min(100, ticket_score + overdue_score + bug_score + resolution_penalty), 2)


def _financial_risk(inp: ChurnInput) -> float:
    delay_score = min(60, inp.payment_delays * 15)
    dispute_score = min(40, inp.invoice_disputes * 20)
    return round(min(100, delay_score + dispute_score), 2)


def _relationship_risk(inp: ChurnInput) -> float:
    score = 0.0

    if inp.champion_lost:
        score += 40

    if inp.executive_sponsor_engaged:
        score -= 15

    # NPS score
    if inp.nps_score < -30:
        score += 30
    elif inp.nps_score < 0:
        score += 15
    elif inp.nps_score > 50:
        score -= 10

    # NPS trend
    if inp.nps_trend.lower() == "declining":
        score += 15
    elif inp.nps_trend.lower() == "improving":
        score -= 10

    # QBR recency
    if inp.last_qbr_days > 90:
        score += 20
    elif inp.last_qbr_days > 60:
        score += 10

    return round(max(0, min(100, score)), 2)


def _competitive_risk(inp: ChurnInput) -> float:
    score = 0.0
    if inp.competitor_mentioned:
        score += 35
    if inp.rfp_received:
        score += 50
    return round(min(100, score), 2)


def _churn_probability(
    usage: float,
    support: float,
    financial: float,
    relationship: float,
    competitive: float,
    inp: ChurnInput,
) -> float:
    base = (
        usage * 0.25
        + support * 0.15
        + financial * 0.15
        + relationship * 0.30
        + competitive * 0.15
    )

    # Contract urgency modifier
    bonus = 0.0
    if inp.contract_end_days <= 60 and base >= 35:
        bonus += 8
    if inp.contract_end_days <= 30:
        bonus += 5

    return round(min(95, max(0, base + bonus)), 2)


def _churn_risk(prob: float) -> ChurnRisk:
    if prob >= 80:
        return ChurnRisk.CRITICAL
    if prob >= 60:
        return ChurnRisk.HIGH
    if prob >= 40:
        return ChurnRisk.MEDIUM
    if prob >= 20:
        return ChurnRisk.LOW
    return ChurnRisk.SAFE


_DAYS_TO_ACT = {
    ChurnRisk.CRITICAL: 3,
    ChurnRisk.HIGH: 7,
    ChurnRisk.MEDIUM: 14,
    ChurnRisk.LOW: 30,
    ChurnRisk.SAFE: 90,
}


def _retention_action(inp: ChurnInput, risk: ChurnRisk) -> RetentionAction:
    if risk == ChurnRisk.CRITICAL:
        return RetentionAction.EMERGENCY
    if risk == ChurnRisk.HIGH:
        if inp.champion_lost or inp.rfp_received:
            return RetentionAction.EMERGENCY
        return RetentionAction.RESCUE
    if risk == ChurnRisk.MEDIUM:
        return RetentionAction.PROACTIVE
    if risk == ChurnRisk.LOW:
        return RetentionAction.NURTURE
    # SAFE — expand only if usage and sentiment positive
    if inp.mau_trend_pct >= 0 and inp.nps_score > 30:
        return RetentionAction.EXPAND
    return RetentionAction.NURTURE


def _build_signals(
    inp: ChurnInput,
    prob: float,
    risk: ChurnRisk,
    arr_at_risk: float,
) -> tuple[list[str], list[str], list[str], list[str]]:
    drivers: list[str] = []
    signals: list[str] = []
    flags: list[str] = []
    actions: list[str] = []

    # Drivers
    if inp.mau_trend_pct <= -20:
        drivers.append(f"Usage en déclin (MAU {inp.mau_trend_pct:+.0f}%)")
    elif inp.mau_trend_pct < 0:
        drivers.append(f"Légère baisse d'usage (MAU {inp.mau_trend_pct:+.0f}%)")
    if inp.login_frequency_days > 7:
        drivers.append(f"Connexions rares (tous les {inp.login_frequency_days:.0f} jours)")
    if inp.feature_adoption_pct < 30:
        drivers.append(f"Adoption très faible ({inp.feature_adoption_pct:.0f}%)")
    if inp.overdue_tickets > 0:
        drivers.append(f"{inp.overdue_tickets} ticket(s) en retard — insatisfaction support")
    if inp.critical_bugs_open > 0:
        drivers.append(f"{inp.critical_bugs_open} bug(s) critique(s) ouvert(s) — impact business")
    if inp.payment_delays > 0:
        drivers.append(f"{inp.payment_delays} retard(s) de paiement")
    if inp.champion_lost:
        drivers.append("Champion perdu — relation à reconstruire")
    if inp.nps_score < -30:
        drivers.append(f"NPS très négatif ({inp.nps_score})")
    elif inp.nps_score < 0:
        drivers.append(f"NPS négatif ({inp.nps_score})")
    if inp.nps_trend.lower() == "declining":
        drivers.append("NPS en déclin")
    if inp.competitor_mentioned:
        drivers.append("Concurrent mentionné — évaluation en cours")
    if inp.rfp_received:
        drivers.append("RFP reçu — évaluation formelle ouverte")
    if inp.contract_end_days <= 60:
        drivers.append(f"Renouvellement dans {inp.contract_end_days} jours")

    # Retention signals
    if inp.mau_trend_pct >= 10:
        signals.append(f"Usage en hausse (+{inp.mau_trend_pct:.0f}% MAU)")
    if inp.feature_adoption_pct >= 70:
        signals.append(f"Forte adoption fonctionnelle ({inp.feature_adoption_pct:.0f}%)")
    if inp.executive_sponsor_engaged:
        signals.append("Sponsor exécutif impliqué — relation stratégique solide")
    if inp.nps_score > 30:
        signals.append(f"NPS positif ({inp.nps_score}) — client satisfait")
    if inp.nps_trend.lower() == "improving":
        signals.append("NPS en amélioration")
    if inp.open_tickets == 0:
        signals.append("Aucun ticket ouvert — client satisfait")
    if inp.payment_delays == 0 and inp.invoice_disputes == 0:
        signals.append("Historique de paiement parfait")

    # Risk flags
    if prob >= 80:
        flags.append(f"CRITIQUE — perte imminente (ARR {arr_at_risk:,.0f}€ à risque)")
    if inp.champion_lost and inp.rfp_received:
        flags.append("Double menace — champion perdu ET RFP ouvert simultanément")
    if inp.payment_delays >= 3:
        flags.append("Retards de paiement répétés — risque contentieux")
    if inp.contract_end_days <= 30:
        flags.append(f"Renouvellement CRITIQUE dans {inp.contract_end_days} jours")
    if inp.critical_bugs_open >= 2:
        flags.append(f"{inp.critical_bugs_open} bugs critiques bloquants — escalade requise")

    # Recommended actions
    if inp.champion_lost:
        actions.append("Identifier et activer un nouveau champion interne en urgence")
    if inp.rfp_received:
        actions.append("Déclencher un call exécutif d'urgence et préparer une contre-proposition")
    if inp.critical_bugs_open > 0:
        actions.append(f"Escalader les {inp.critical_bugs_open} bug(s) critique(s) à l'équipe engineering")
    if inp.mau_trend_pct <= -20:
        actions.append("Planifier un Success Call pour comprendre le déclin d'usage")
    if inp.feature_adoption_pct < 30:
        actions.append("Proposer une session de formation sur les fonctionnalités clés")
    if inp.contract_end_days <= 90:
        actions.append("Déclencher le processus de renouvellement anticipé")
    if inp.nps_score < 0:
        actions.append("Conduire une interview NPS Detractor pour identifier les irritants")
    if inp.payment_delays > 0:
        actions.append("Aligner Finance et Account Manager sur la situation de paiement")
    if inp.last_qbr_days > 90:
        actions.append("Planifier un QBR immédiatement — dernier QBR trop ancien")
    if not inp.executive_sponsor_engaged:
        actions.append("Demander une introduction au sponsor exécutif côté client")

    return drivers, signals, flags, actions


class ChurnPredictor:
    """Predicts customer churn probability and recommends targeted retention actions."""

    def __init__(self) -> None:
        self._results: dict[str, ChurnResult] = {}

    def predict(self, inp: ChurnInput) -> ChurnResult:
        usage = _usage_risk(inp)
        support = _support_risk(inp)
        financial = _financial_risk(inp)
        relationship = _relationship_risk(inp)
        competitive = _competitive_risk(inp)

        prob = _churn_probability(usage, support, financial, relationship, competitive, inp)
        risk = _churn_risk(prob)
        action = _retention_action(inp, risk)
        arr_at_risk = round(inp.arr_eur * prob / 100, 2)

        base_days = _DAYS_TO_ACT[risk]
        days_to_act = min(base_days, inp.contract_end_days) if inp.contract_end_days > 0 else base_days

        drivers, signals, flags, actions = _build_signals(inp, prob, risk, arr_at_risk)

        result = ChurnResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            arr_eur=inp.arr_eur,
            churn_probability_pct=prob,
            churn_risk=risk,
            retention_action=action,
            churn_drivers=drivers,
            retention_signals=signals,
            risk_flags=flags,
            recommended_actions=actions,
            arr_at_risk_eur=arr_at_risk,
            days_to_act=days_to_act,
            usage_risk_score=usage,
            support_risk_score=support,
            financial_risk_score=financial,
            relationship_risk_score=relationship,
            competitive_risk_score=competitive,
        )
        self._results[inp.account_id] = result
        return result

    def predict_batch(self, inputs: list[ChurnInput]) -> list[ChurnResult]:
        return sorted(
            [self.predict(inp) for inp in inputs],
            key=lambda r: r.churn_probability_pct,
            reverse=True,
        )

    def get(self, account_id: str) -> Optional[ChurnResult]:
        return self._results.get(account_id)

    def all_accounts(self) -> list[ChurnResult]:
        return sorted(self._results.values(), key=lambda r: r.churn_probability_pct, reverse=True)

    def by_risk(self, risk: ChurnRisk) -> list[ChurnResult]:
        return [r for r in self.all_accounts() if r.churn_risk == risk]

    def critical(self) -> list[ChurnResult]:
        return self.by_risk(ChurnRisk.CRITICAL)

    def high_risk(self) -> list[ChurnResult]:
        return self.by_risk(ChurnRisk.HIGH)

    def at_risk(self) -> list[ChurnResult]:
        return [r for r in self.all_accounts() if r.churn_risk in (ChurnRisk.CRITICAL, ChurnRisk.HIGH)]

    def safe_accounts(self) -> list[ChurnResult]:
        return self.by_risk(ChurnRisk.SAFE)

    def needs_emergency(self) -> list[ChurnResult]:
        return [r for r in self.all_accounts() if r.retention_action == RetentionAction.EMERGENCY]

    def expansion_candidates(self) -> list[ChurnResult]:
        return [r for r in self.all_accounts() if r.retention_action == RetentionAction.EXPAND]

    def total_arr_at_risk_eur(self) -> float:
        return round(sum(r.arr_at_risk_eur for r in self.all_accounts()), 2)

    def avg_churn_probability(self) -> float:
        accounts = self.all_accounts()
        if not accounts:
            return 0.0
        return round(sum(r.churn_probability_pct for r in accounts) / len(accounts), 1)

    def top_n(self, n: int = 10) -> list[ChurnResult]:
        return self.all_accounts()[:n]

    def summary(self) -> dict:
        all_r = self.all_accounts()
        if not all_r:
            return {
                "total": 0,
                "risk_counts": {},
                "action_counts": {},
                "avg_churn_probability": 0.0,
                "total_arr_at_risk_eur": 0.0,
                "critical_count": 0,
                "emergency_count": 0,
            }
        risk_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in all_r:
            risk_counts[r.churn_risk.value] = risk_counts.get(r.churn_risk.value, 0) + 1
            action_counts[r.retention_action.value] = action_counts.get(r.retention_action.value, 0) + 1
        return {
            "total": len(all_r),
            "risk_counts": risk_counts,
            "action_counts": action_counts,
            "avg_churn_probability": self.avg_churn_probability(),
            "total_arr_at_risk_eur": self.total_arr_at_risk_eur(),
            "critical_count": len(self.critical()),
            "emergency_count": len(self.needs_emergency()),
        }

    def reset(self) -> None:
        self._results.clear()
