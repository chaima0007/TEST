"""Expansion Revenue Detector — identifies and scores upsell/cross-sell opportunities in existing accounts."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class ExpansionTier(str, Enum):
    HOT = "hot"     # score >= 70 — strong expansion signal, act now
    WARM = "warm"   # score >= 45 — good opportunity, nurture actively
    COOL = "cool"   # score >= 25 — potential, but timing or signals weak
    COLD = "cold"   # score < 25  — not the right moment


class ExpansionAction(str, Enum):
    CLOSE = "close"      # hot opportunity ready to convert
    NURTURE = "nurture"  # warm lead, build value and engagement
    QUALIFY = "qualify"  # cool signal, validate before investing effort
    WATCH = "watch"      # cold, monitor passively


@dataclass
class ExpansionInput:
    account_id: str
    account_name: str

    current_arr_eur: float
    product_tier: str              # starter / professional / enterprise
    contract_months_remaining: int # months until next renewal (0 = expired/m2m)

    # Usage signals
    seats_licensed: int
    seats_used: int
    feature_adoption_pct: float    # 0-100, active use of licensed features
    modules_purchased: int
    modules_available: int         # total modules in the product catalogue

    # Relationship signals
    nps_score: int                 # -100 to 100 (-999 if not recorded)
    executive_engagement: bool
    champion_strength: int         # 0-100
    days_since_last_qbr: int

    # Growth signals
    expansion_signals: int         # explicit signals: headcount growth, new use cases, budget signals
    competitive_pressure: bool     # competitor actively pursuing the account
    previous_expansion_done: bool  # account has expanded before
    health_score: float            # 0-100, current account health score


@dataclass
class ExpansionResult:
    account_id: str
    account_name: str
    current_arr_eur: float
    product_tier: str

    expansion_tier: ExpansionTier
    expansion_action: ExpansionAction
    expansion_score: float          # 0-100

    utilization_score: float        # 0-100
    relationship_score: float       # 0-100
    growth_score: float             # 0-100
    timing_score: float             # 0-100

    opportunity_types: list[str]    # SEAT_EXPANSION / UPSELL / CROSS_SELL / RENEWAL_UPLIFT / NEW_MODULE
    estimated_expansion_eur: float  # estimated additional ARR if closed
    seat_utilization_pct: float     # computed: seats_used / seats_licensed * 100
    modules_utilization_pct: float  # computed: modules_purchased / modules_available * 100

    positive_signals: list[str]
    risk_factors: list[str]
    recommended_actions: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["expansion_tier"] = self.expansion_tier.value
        d["expansion_action"] = self.expansion_action.value
        return d


def _seat_utilization(inp: ExpansionInput) -> float:
    return round(inp.seats_used / max(1, inp.seats_licensed) * 100.0, 1)


def _modules_utilization(inp: ExpansionInput) -> float:
    return round(inp.modules_purchased / max(1, inp.modules_available) * 100.0, 1)


def _utilization_score(inp: ExpansionInput, seat_util: float) -> float:
    if seat_util > 90:
        score = 100.0
    elif seat_util > 80:
        score = 80.0
    elif seat_util > 70:
        score = 60.0
    elif seat_util > 50:
        score = 40.0
    else:
        score = 20.0
    if inp.feature_adoption_pct > 80:
        score += 15.0
    elif inp.feature_adoption_pct > 60:
        score += 8.0
    return round(max(0.0, min(100.0, score)), 2)


def _relationship_score(inp: ExpansionInput) -> float:
    score = 0.0
    if inp.executive_engagement:
        score += 30.0
    if inp.champion_strength > 80:
        score += 25.0
    elif inp.champion_strength > 60:
        score += 15.0
    elif inp.champion_strength > 40:
        score += 8.0
    if inp.nps_score != -999:
        if inp.nps_score > 50:
            score += 20.0
        elif inp.nps_score > 20:
            score += 10.0
        elif inp.nps_score < -20:
            score -= 30.0
        elif inp.nps_score < 0:
            score -= 15.0
    if inp.days_since_last_qbr <= 30:
        score += 15.0
    elif inp.days_since_last_qbr <= 90:
        score += 5.0
    elif inp.days_since_last_qbr > 180:
        score -= 10.0
    return round(max(0.0, min(100.0, score)), 2)


def _growth_score(inp: ExpansionInput) -> float:
    score = min(75.0, inp.expansion_signals * 25.0)
    if not inp.competitive_pressure:
        score += 15.0
    if inp.previous_expansion_done:
        score += 10.0
    return round(max(0.0, min(100.0, score)), 2)


def _timing_score(inp: ExpansionInput) -> float:
    m = inp.contract_months_remaining
    if m == 0:
        return 40.0     # expired / month-to-month — tricky
    if 3 <= m <= 9:
        return 100.0    # sweet spot for renewal conversations
    if 1 <= m < 3:
        return 70.0     # urgent
    if 9 < m <= 18:
        return 60.0     # good early engagement window
    return 30.0         # > 18 months — too early


def _expansion_score(util: float, rel: float, growth: float, timing: float) -> float:
    return round(util * 0.30 + rel * 0.25 + growth * 0.25 + timing * 0.20, 2)


def _expansion_tier(score: float) -> ExpansionTier:
    if score >= 70:
        return ExpansionTier.HOT
    if score >= 45:
        return ExpansionTier.WARM
    if score >= 25:
        return ExpansionTier.COOL
    return ExpansionTier.COLD


def _expansion_action(tier: ExpansionTier, inp: ExpansionInput) -> ExpansionAction:
    if tier == ExpansionTier.HOT:
        return ExpansionAction.CLOSE
    if tier == ExpansionTier.WARM:
        return ExpansionAction.NURTURE
    if tier == ExpansionTier.COOL:
        return ExpansionAction.QUALIFY
    return ExpansionAction.WATCH


def _opportunity_types(inp: ExpansionInput, seat_util: float, modules_util: float) -> list[str]:
    types: list[str] = []
    if seat_util > 80:
        types.append("SEAT_EXPANSION")
    if inp.product_tier != "enterprise" and inp.health_score >= 65:
        types.append("UPSELL")
    if modules_util < 60 and inp.modules_available > inp.modules_purchased:
        types.append("CROSS_SELL")
    if 0 < inp.contract_months_remaining <= 9 and inp.health_score >= 65:
        types.append("RENEWAL_UPLIFT")
    if inp.feature_adoption_pct < 50:
        types.append("NEW_MODULE")
    return types


def _estimated_expansion_eur(inp: ExpansionInput, score: float, opportunity_types: list[str]) -> float:
    est = 0.0
    if "SEAT_EXPANSION" in opportunity_types:
        seat_util = inp.seats_used / max(1, inp.seats_licensed) * 100
        additional_pct = min(0.40, (seat_util - 80) / 100)
        est += inp.current_arr_eur * additional_pct
    if "UPSELL" in opportunity_types:
        uplift = 0.50 if inp.product_tier == "starter" else 0.30
        est += inp.current_arr_eur * uplift
    if "CROSS_SELL" in opportunity_types:
        modules_util = inp.modules_purchased / max(1, inp.modules_available)
        est += inp.current_arr_eur * (1 - modules_util) * 0.25
    if "RENEWAL_UPLIFT" in opportunity_types:
        est += inp.current_arr_eur * 0.10
    if "NEW_MODULE" in opportunity_types and "CROSS_SELL" not in opportunity_types:
        est += inp.current_arr_eur * 0.12
    return round(max(0.0, est), 2)


def _build_signals(
    inp: ExpansionInput,
    tier: ExpansionTier,
    opportunity_types: list[str],
    seat_util: float,
    modules_util: float,
) -> tuple[list[str], list[str], list[str]]:
    positives: list[str] = []
    risks: list[str] = []
    actions: list[str] = []

    # Positive signals
    if seat_util > 90:
        positives.append(f"Capacité quasi-atteinte — {seat_util:.0f}% des licences utilisées")
    elif seat_util > 80:
        positives.append(f"Forte utilisation — {seat_util:.0f}% des licences actives")
    if inp.feature_adoption_pct > 80:
        positives.append(f"Adoption fonctionnelle excellente ({inp.feature_adoption_pct:.0f}%)")
    elif inp.feature_adoption_pct > 60:
        positives.append(f"Bonne adoption des fonctionnalités ({inp.feature_adoption_pct:.0f}%)")
    if inp.executive_engagement:
        positives.append("Engagement exécutif confirmé — deal décisionnel facilité")
    if inp.champion_strength > 80:
        positives.append("Champion très actif — défense interne forte")
    elif inp.champion_strength > 60:
        positives.append("Champion engagé — bonne adhésion interne")
    if inp.nps_score != -999 and inp.nps_score > 50:
        positives.append(f"NPS excellent ({inp.nps_score}) — client promoteur")
    elif inp.nps_score != -999 and inp.nps_score > 20:
        positives.append(f"NPS positif ({inp.nps_score}) — satisfaction bonne")
    if inp.expansion_signals > 0:
        positives.append(f"{inp.expansion_signals} signal(s) de croissance détecté(s) — intent expansion confirmé")
    if inp.previous_expansion_done:
        positives.append("Historique d'expansion — client récurrent dans les achats")
    if inp.days_since_last_qbr <= 30:
        positives.append("QBR récent — relation maintenue et opportunités discutées")
    if 3 <= inp.contract_months_remaining <= 9:
        positives.append(f"Renouvellement dans {inp.contract_months_remaining} mois — fenêtre d'expansion idéale")

    # Risk factors
    if inp.competitive_pressure:
        risks.append("Pression concurrentielle active — rétention prioritaire avant expansion")
    if inp.health_score < 50:
        risks.append(f"Santé compte faible ({inp.health_score:.0f}) — résoudre les problèmes avant d'upseller")
    if inp.nps_score != -999 and inp.nps_score < 0:
        risks.append(f"NPS négatif ({inp.nps_score}) — insatisfaction à résoudre en priorité")
    if inp.champion_strength < 30:
        risks.append("Champion faible ou absent — support interne insuffisant")
    if not inp.executive_engagement and tier == ExpansionTier.HOT:
        risks.append("Pas d'engagement exécutif — impacte la rapidité de décision")
    if inp.days_since_last_qbr > 180:
        risks.append(f"Dernier QBR il y a {inp.days_since_last_qbr}j — relation à ré-activer")
    if inp.contract_months_remaining == 0:
        risks.append("Contrat expiré ou mois-à-mois — priorité renouvellement avant expansion")
    if inp.feature_adoption_pct < 30:
        risks.append(f"Adoption faible ({inp.feature_adoption_pct:.0f}%) — risque de churn avant expansion")
    if modules_util > 90:
        risks.append("Déjà en possession de la plupart des modules — espace d'expansion limité")

    # Recommended actions
    if "SEAT_EXPANSION" in opportunity_types:
        actions.append(f"Proposer une extension de licences — utilisation actuelle à {seat_util:.0f}%")
    if "UPSELL" in opportunity_types:
        actions.append(f"Préparer une démonstration du tier supérieur (passage de {inp.product_tier})")
    if "CROSS_SELL" in opportunity_types:
        mods_missing = inp.modules_available - inp.modules_purchased
        actions.append(f"Présenter les {mods_missing} module(s) non adoptés lors du prochain QBR")
    if "RENEWAL_UPLIFT" in opportunity_types:
        actions.append(f"Négocier une revalorisation tarifaire à la prochaine fenêtre de renouvellement ({inp.contract_months_remaining}m)")
    if "NEW_MODULE" in opportunity_types:
        actions.append(f"Améliorer l'adoption ({inp.feature_adoption_pct:.0f}%) via une session d'activation fonctionnelle")
    if inp.competitive_pressure:
        actions.append("Renforcer la valeur perçue avant toute conversation d'expansion")
    if inp.health_score < 60:
        actions.append("Priorité : résoudre les problèmes de santé compte avant expansion")
    if not inp.executive_engagement and tier in (ExpansionTier.HOT, ExpansionTier.WARM):
        actions.append("Planifier un executive briefing pour accélérer la décision d'expansion")
    if inp.days_since_last_qbr > 90:
        actions.append("Planifier un QBR — dernière revue > 90j")

    return positives, risks, actions


class ExpansionRevenueDetector:
    """Identifies and scores upsell/cross-sell opportunities in existing customer accounts."""

    def __init__(self) -> None:
        self._results: dict[str, ExpansionResult] = {}

    def detect(self, inp: ExpansionInput) -> ExpansionResult:
        seat_util = _seat_utilization(inp)
        modules_util = _modules_utilization(inp)

        util = _utilization_score(inp, seat_util)
        rel = _relationship_score(inp)
        growth = _growth_score(inp)
        timing = _timing_score(inp)
        score = _expansion_score(util, rel, growth, timing)

        tier = _expansion_tier(score)
        action = _expansion_action(tier, inp)
        opp_types = _opportunity_types(inp, seat_util, modules_util)
        est_eur = _estimated_expansion_eur(inp, score, opp_types)

        positives, risks, actions = _build_signals(inp, tier, opp_types, seat_util, modules_util)

        result = ExpansionResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            current_arr_eur=inp.current_arr_eur,
            product_tier=inp.product_tier,
            expansion_tier=tier,
            expansion_action=action,
            expansion_score=score,
            utilization_score=util,
            relationship_score=rel,
            growth_score=growth,
            timing_score=timing,
            opportunity_types=opp_types,
            estimated_expansion_eur=est_eur,
            seat_utilization_pct=seat_util,
            modules_utilization_pct=modules_util,
            positive_signals=positives,
            risk_factors=risks,
            recommended_actions=actions,
        )
        self._results[inp.account_id] = result
        return result

    def detect_batch(self, inputs: list[ExpansionInput]) -> list[ExpansionResult]:
        return sorted(
            [self.detect(inp) for inp in inputs],
            key=lambda r: r.expansion_score,
            reverse=True,
        )

    def get(self, account_id: str) -> Optional[ExpansionResult]:
        return self._results.get(account_id)

    def all_accounts(self) -> list[ExpansionResult]:
        return sorted(self._results.values(), key=lambda r: r.expansion_score, reverse=True)

    def by_tier(self, tier: ExpansionTier) -> list[ExpansionResult]:
        return [r for r in self.all_accounts() if r.expansion_tier == tier]

    def hot(self) -> list[ExpansionResult]:
        return self.by_tier(ExpansionTier.HOT)

    def warm(self) -> list[ExpansionResult]:
        return self.by_tier(ExpansionTier.WARM)

    def ready_to_close(self) -> list[ExpansionResult]:
        return [r for r in self.all_accounts() if r.expansion_action == ExpansionAction.CLOSE]

    def with_opportunity_type(self, opp_type: str) -> list[ExpansionResult]:
        return [r for r in self.all_accounts() if opp_type in r.opportunity_types]

    def total_estimated_expansion_eur(self) -> float:
        return round(sum(r.estimated_expansion_eur for r in self._results.values()), 2)

    def total_current_arr_eur(self) -> float:
        return round(sum(r.current_arr_eur for r in self._results.values()), 2)

    def avg_expansion_score(self) -> float:
        accounts = list(self._results.values())
        if not accounts:
            return 0.0
        return round(sum(r.expansion_score for r in accounts) / len(accounts), 1)

    def top_n(self, n: int) -> list[ExpansionResult]:
        return sorted(self._results.values(), key=lambda r: r.estimated_expansion_eur, reverse=True)[:n]

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "tier_counts": {},
                "action_counts": {},
                "avg_expansion_score": 0.0,
                "total_estimated_expansion_eur": 0.0,
                "total_current_arr_eur": 0.0,
                "hot_count": 0,
                "close_ready_count": 0,
            }
        tier_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in all_r:
            tier_counts[r.expansion_tier.value] = tier_counts.get(r.expansion_tier.value, 0) + 1
            action_counts[r.expansion_action.value] = action_counts.get(r.expansion_action.value, 0) + 1
        return {
            "total": len(all_r),
            "tier_counts": tier_counts,
            "action_counts": action_counts,
            "avg_expansion_score": self.avg_expansion_score(),
            "total_estimated_expansion_eur": self.total_estimated_expansion_eur(),
            "total_current_arr_eur": self.total_current_arr_eur(),
            "hot_count": len(self.hot()),
            "close_ready_count": len(self.ready_to_close()),
        }

    def reset(self) -> None:
        self._results.clear()
