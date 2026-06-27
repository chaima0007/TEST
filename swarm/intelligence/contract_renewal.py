"""Contract Renewal Intelligence — scores and prioritizes renewal opportunities with churn risk and expansion potential."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class RenewalRisk(str, Enum):
    GREEN = "green"         # renewal_score >= 75 — high confidence renewal
    YELLOW = "yellow"       # renewal_score >= 50 — likely but watch signals
    ORANGE = "orange"       # renewal_score >= 25 — significant risk
    RED = "red"             # renewal_score < 25  — churn likely


class RenewalAction(str, Enum):
    CLOSE_RENEWAL = "close_renewal"       # high score, renewal ready to sign
    ACCELERATE = "accelerate"             # good health, push to close
    INTERVENE = "intervene"               # risk signals, escalate intervention
    SAVE = "save"                         # churn risk, last-resort save motion
    EARLY_RENEW = "early_renew"           # healthy account, lock in early


class UpliftPotential(str, Enum):
    HIGH = "high"       # uplift_score >= 70
    MEDIUM = "medium"   # uplift_score >= 40
    LOW = "low"         # uplift_score < 40


@dataclass
class RenewalInput:
    contract_id: str
    account_name: str
    segment: str                    # enterprise / mid_market / smb
    arr_eur: float
    days_to_renewal: int            # days until contract expiry

    # Health signals
    health_score: float             # 0-100 overall account health
    nps_score: float                # -100 to +100
    product_adoption_score: float   # 0-100
    support_escalations: int        # open escalations at renewal time

    # Relationship signals
    executive_engaged: bool
    champion_strength: float        # 0-100
    qbr_completed_last_90d: bool
    stakeholder_count: int          # distinct stakeholders engaged

    # Commercial signals
    current_discount_pct: float     # 0-100, current contract discount
    price_increase_proposed: float  # 0-100, proposed price increase %
    competitive_bids_received: int  # number of competitive proposals received
    budget_confirmed: bool
    multi_year_interest: bool       # customer has expressed interest in multi-year

    # Expansion signals
    seat_utilization_pct: float     # 0-100
    feature_adoption_pct: float     # 0-100
    expansion_history: bool         # has expanded in the past
    new_use_cases: int              # new use cases discovered since last renewal


@dataclass
class RenewalResult:
    contract_id: str
    account_name: str
    segment: str
    arr_eur: float
    days_to_renewal: int

    renewal_risk: RenewalRisk
    renewal_action: RenewalAction
    uplift_potential: UpliftPotential
    renewal_score: float            # 0-100
    uplift_score: float             # 0-100
    recommended_uplift_pct: float   # recommended price increase %

    churn_signals: list[str]
    retention_levers: list[str]
    negotiation_tactics: list[str]
    timeline_steps: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["renewal_risk"] = self.renewal_risk.value
        d["renewal_action"] = self.renewal_action.value
        d["uplift_potential"] = self.uplift_potential.value
        return d


# ─── Scoring helpers ──────────────────────────────────────────────────────────

def _renewal_score(inp: RenewalInput) -> float:
    score = 0.0

    # Health (0-30)
    score += inp.health_score * 0.30

    # NPS (0-20): normalised -100..+100 → 0..20
    nps_norm = (inp.nps_score + 100) / 200.0 * 20.0
    score += max(0.0, min(20.0, nps_norm))

    # Relationship (0-25)
    if inp.executive_engaged:
        score += 10.0
    if inp.champion_strength >= 70:
        score += 10.0
    elif inp.champion_strength >= 40:
        score += 5.0
    if inp.qbr_completed_last_90d:
        score += 5.0

    # Risk deductions
    if inp.support_escalations >= 3:
        score -= 15.0
    elif inp.support_escalations >= 1:
        score -= 7.0
    if inp.competitive_bids_received >= 2:
        score -= 10.0
    elif inp.competitive_bids_received >= 1:
        score -= 5.0
    if inp.price_increase_proposed > 15:
        score -= 8.0
    elif inp.price_increase_proposed > 5:
        score -= 3.0

    # Positive signals
    if inp.budget_confirmed:
        score += 8.0
    if inp.multi_year_interest:
        score += 7.0
    if inp.stakeholder_count >= 3:
        score += 5.0

    return round(max(0.0, min(100.0, score)), 1)


def _uplift_score(inp: RenewalInput) -> float:
    score = 0.0

    if inp.seat_utilization_pct >= 90:
        score += 30.0
    elif inp.seat_utilization_pct >= 75:
        score += 20.0
    elif inp.seat_utilization_pct >= 60:
        score += 10.0

    if inp.feature_adoption_pct >= 80:
        score += 25.0
    elif inp.feature_adoption_pct >= 60:
        score += 15.0
    elif inp.feature_adoption_pct >= 40:
        score += 5.0

    if inp.expansion_history:
        score += 20.0

    score += min(25.0, inp.new_use_cases * 8.0)

    if inp.health_score >= 70:
        score += 10.0

    return round(max(0.0, min(100.0, score)), 1)


def _uplift_potential(up_score: float) -> UpliftPotential:
    if up_score >= 70:
        return UpliftPotential.HIGH
    if up_score >= 40:
        return UpliftPotential.MEDIUM
    return UpliftPotential.LOW


def _renewal_risk(score: float) -> RenewalRisk:
    if score >= 75:
        return RenewalRisk.GREEN
    if score >= 50:
        return RenewalRisk.YELLOW
    if score >= 25:
        return RenewalRisk.ORANGE
    return RenewalRisk.RED


def _recommended_uplift(inp: RenewalInput, up_score: float) -> float:
    if up_score >= 70 and inp.health_score >= 70:
        base = min(inp.price_increase_proposed, 15.0)
        return round(max(8.0, base), 1)
    if up_score >= 40:
        return round(min(inp.price_increase_proposed, 8.0), 1)
    return round(min(inp.price_increase_proposed, 3.0), 1)


def _renewal_action(
    inp: RenewalInput,
    risk: RenewalRisk,
    up_potential: UpliftPotential,
    days: int,
) -> RenewalAction:
    if risk == RenewalRisk.RED:
        return RenewalAction.SAVE
    if risk == RenewalRisk.ORANGE:
        return RenewalAction.INTERVENE
    if risk == RenewalRisk.GREEN and days > 90 and inp.health_score >= 80:
        return RenewalAction.EARLY_RENEW
    if risk == RenewalRisk.GREEN and days <= 90:
        return RenewalAction.CLOSE_RENEWAL
    return RenewalAction.ACCELERATE


def _build_churn_signals(inp: RenewalInput, score: float) -> list[str]:
    signals: list[str] = []
    if inp.support_escalations >= 3:
        signals.append(f"{inp.support_escalations} escalades support actives — insatisfaction critique")
    elif inp.support_escalations >= 1:
        signals.append(f"{inp.support_escalations} escalade(s) support — à résoudre avant renouvellement")
    if inp.competitive_bids_received >= 2:
        signals.append(f"{inp.competitive_bids_received} offres concurrentes reçues — risque de départ élevé")
    elif inp.competitive_bids_received >= 1:
        signals.append("1 offre concurrente reçue — surveiller le processus de décision")
    if inp.nps_score < 0:
        signals.append(f"NPS négatif ({inp.nps_score:.0f}) — client détracteur, churn imminent")
    elif inp.nps_score < 20:
        signals.append(f"NPS faible ({inp.nps_score:.0f}) — satisfaction fragile")
    if inp.champion_strength < 30:
        signals.append("Champion faible ou absent — pas de défenseur interne")
    if not inp.executive_engaged:
        signals.append("Sponsor exécutif non engagé — décision de renouvellement incertaine")
    if inp.product_adoption_score < 40:
        signals.append(f"Adoption produit faible ({inp.product_adoption_score:.0f}/100) — valeur non perçue")
    if inp.price_increase_proposed > 15:
        signals.append(f"Hausse de prix proposée ({inp.price_increase_proposed:.0f}%) — résistance budget attendue")
    if not inp.budget_confirmed and inp.days_to_renewal <= 60:
        signals.append("Budget non confirmé à moins de 60j du renouvellement — risque de glissement")
    return signals


def _build_retention_levers(inp: RenewalInput, risk: RenewalRisk) -> list[str]:
    levers: list[str] = []
    if inp.health_score >= 70:
        levers.append("Capitaliser sur la bonne santé compte — présenter les ROI atteints")
    if inp.expansion_history:
        levers.append("Référencer l'historique d'expansion — client qui croit avec nous")
    if inp.multi_year_interest:
        levers.append("Négocier un engagement pluriannuel — sécuriser et offrir visibilité tarifaire")
    if inp.seat_utilization_pct >= 80:
        levers.append(f"Utilisation sièges à {inp.seat_utilization_pct:.0f}% — démontrer la valeur business générée")
    if inp.qbr_completed_last_90d:
        levers.append("QBR récent — continuer sur la dynamique établie")
    if inp.stakeholder_count >= 3:
        levers.append(f"{inp.stakeholder_count} parties prenantes engagées — base de support étendue")
    if inp.new_use_cases > 0:
        levers.append(f"{inp.new_use_cases} nouveau(x) cas d'usage identifié(s) — expansion naturelle du ROI")
    if inp.executive_engaged:
        levers.append("Alignement exécutif actif — mobiliser pour signature")
    if risk in (RenewalRisk.RED, RenewalRisk.ORANGE) and inp.champion_strength >= 50:
        levers.append("Champion encore engagé — activer pour contre-attaque interne")
    return levers


def _build_negotiation_tactics(inp: RenewalInput, risk: RenewalRisk, up_potential: UpliftPotential) -> list[str]:
    tactics: list[str] = []
    if risk in (RenewalRisk.RED, RenewalRisk.ORANGE):
        tactics.append("Présenter un plan de remédiation formel — montrer l'engagement et la roadmap")
        if inp.competitive_bids_received >= 1:
            tactics.append("Préparer un briefing concurrentiel — argumentaire ROI vs alternatives")
        if inp.support_escalations >= 1:
            tactics.append("Résoudre les escalades avant toute discussion commerciale")
    if up_potential == UpliftPotential.HIGH:
        tactics.append("Défendre la hausse tarifaire avec des données ROI quantifiées")
        tactics.append("Proposer un palier tarifaire pluriannuel — protection prix contre engagement long terme")
    elif up_potential == UpliftPotential.MEDIUM:
        tactics.append("Limiter la hausse à 5-8% — priorité renouvellement sur marge")
    else:
        tactics.append("Reconduire au prix actuel — concentrer sur le renouvellement ferme")
    if inp.multi_year_interest:
        tactics.append("Structurer un deal 2 ou 3 ans avec visibilité tarifaire pour le client")
    if inp.competitive_bids_received >= 1:
        tactics.append("Quantifier le coût de migration — switching cost à présenter en réunion")
    if inp.budget_confirmed:
        tactics.append("Budget confirmé — accélérer vers la signature sans délai")
    else:
        tactics.append("Qualifier et confirmer le budget avant d'envoyer la proposition")
    return tactics


def _build_timeline_steps(inp: RenewalInput, action: RenewalAction, days: int) -> list[str]:
    steps: list[str] = []

    if action == RenewalAction.SAVE:
        steps.append("J-0 : Appel de sauvegarde immédiat — senior leadership impliqué")
        steps.append("J+2 : Plan de remédiation formalisé — résoudre les blocages identifiés")
        steps.append("J+7 : QBR de récupération — ROI, roadmap, valeur démontrée")
        steps.append("J+14 : Proposition de renouvellement avec concessions si nécessaire")
        steps.append("J+21 : Signature ou escalade finale C-level vs C-level")
    elif action == RenewalAction.INTERVENE:
        steps.append(f"J-{days} : Analyse des risques — plan d'intervention priorisé")
        steps.append("J+7 : Résolution des escalades techniques et relationnelles")
        steps.append("J+14 : QBR de santé — remettre la relation sur les rails")
        steps.append("J+21 : Envoi de la proposition de renouvellement")
        steps.append("J+30 : Closing et signature")
    elif action == RenewalAction.EARLY_RENEW:
        steps.append("Initier la conversation de renouvellement anticipé maintenant")
        steps.append("QBR de valeur — présenter les ROI et les gains futurs")
        steps.append("Proposer une offre pluriannuelle avec avantage tarifaire")
        steps.append("Signature avant la fenêtre de renouvellement officielle")
    elif action == RenewalAction.CLOSE_RENEWAL:
        steps.append("Préparer et envoyer la proposition de renouvellement sous 5 jours")
        steps.append("Réunion de closing — aligner budget, termes et signataires")
        steps.append("Signature dans les 30 jours")
    else:
        steps.append("Qualifier le renouvellement — budget et décideur confirmés")
        steps.append("Préparer la proposition de renouvellement avec uplift justifié")
        steps.append("Réunion de présentation — sponsor exécutif impliqué")
        steps.append("Closing et signature avant J-30")

    return steps


class ContractRenewalEngine:
    """Scores and prioritizes contract renewals, surfaces churn risk and uplift opportunities."""

    def __init__(self) -> None:
        self._results: dict[str, RenewalResult] = {}

    def score(self, inp: RenewalInput) -> RenewalResult:
        r_score = _renewal_score(inp)
        u_score = _uplift_score(inp)
        risk = _renewal_risk(r_score)
        u_potential = _uplift_potential(u_score)
        action = _renewal_action(inp, risk, u_potential, inp.days_to_renewal)
        uplift_pct = _recommended_uplift(inp, u_score)
        churn = _build_churn_signals(inp, r_score)
        levers = _build_retention_levers(inp, risk)
        tactics = _build_negotiation_tactics(inp, risk, u_potential)
        timeline = _build_timeline_steps(inp, action, inp.days_to_renewal)

        result = RenewalResult(
            contract_id=inp.contract_id,
            account_name=inp.account_name,
            segment=inp.segment,
            arr_eur=inp.arr_eur,
            days_to_renewal=inp.days_to_renewal,
            renewal_risk=risk,
            renewal_action=action,
            uplift_potential=u_potential,
            renewal_score=r_score,
            uplift_score=u_score,
            recommended_uplift_pct=uplift_pct,
            churn_signals=churn,
            retention_levers=levers,
            negotiation_tactics=tactics,
            timeline_steps=timeline,
        )
        self._results[inp.contract_id] = result
        return result

    def score_batch(self, inputs: list[RenewalInput]) -> list[RenewalResult]:
        return sorted(
            [self.score(inp) for inp in inputs],
            key=lambda r: r.renewal_score,
            reverse=True,
        )

    def get(self, contract_id: str) -> Optional[RenewalResult]:
        return self._results.get(contract_id)

    def all_contracts(self) -> list[RenewalResult]:
        return sorted(self._results.values(), key=lambda r: r.renewal_score, reverse=True)

    def by_risk(self, risk: RenewalRisk) -> list[RenewalResult]:
        return [r for r in self.all_contracts() if r.renewal_risk == risk]

    def by_action(self, action: RenewalAction) -> list[RenewalResult]:
        return [r for r in self.all_contracts() if r.renewal_action == action]

    def at_risk(self) -> list[RenewalResult]:
        return [r for r in self.all_contracts() if r.renewal_risk in (RenewalRisk.RED, RenewalRisk.ORANGE)]

    def green(self) -> list[RenewalResult]:
        return self.by_risk(RenewalRisk.GREEN)

    def needs_save(self) -> list[RenewalResult]:
        return self.by_action(RenewalAction.SAVE)

    def high_uplift(self) -> list[RenewalResult]:
        return [r for r in self.all_contracts() if r.uplift_potential == UpliftPotential.HIGH]

    def total_arr_at_risk(self) -> float:
        return round(sum(r.arr_eur for r in self.at_risk()), 2)

    def total_arr_renewing(self) -> float:
        return round(sum(r.arr_eur for r in self._results.values()), 2)

    def avg_renewal_score(self) -> float:
        vals = list(self._results.values())
        if not vals:
            return 0.0
        return round(sum(r.renewal_score for r in vals) / len(vals), 1)

    def total_potential_uplift_eur(self) -> float:
        return round(sum(
            r.arr_eur * r.recommended_uplift_pct / 100.0
            for r in self._results.values()
        ), 2)

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "risk_counts": {},
                "action_counts": {},
                "uplift_counts": {},
                "avg_renewal_score": 0.0,
                "total_arr_at_risk_eur": 0.0,
                "total_arr_renewing_eur": 0.0,
                "total_potential_uplift_eur": 0.0,
                "needs_save_count": 0,
                "high_uplift_count": 0,
            }
        risk_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        uplift_counts: dict[str, int] = {}
        for r in all_r:
            risk_counts[r.renewal_risk.value] = risk_counts.get(r.renewal_risk.value, 0) + 1
            action_counts[r.renewal_action.value] = action_counts.get(r.renewal_action.value, 0) + 1
            uplift_counts[r.uplift_potential.value] = uplift_counts.get(r.uplift_potential.value, 0) + 1
        return {
            "total": len(all_r),
            "risk_counts": risk_counts,
            "action_counts": action_counts,
            "uplift_counts": uplift_counts,
            "avg_renewal_score": self.avg_renewal_score(),
            "total_arr_at_risk_eur": self.total_arr_at_risk(),
            "total_arr_renewing_eur": self.total_arr_renewing(),
            "total_potential_uplift_eur": self.total_potential_uplift_eur(),
            "needs_save_count": len(self.needs_save()),
            "high_uplift_count": len(self.high_uplift()),
        }

    def reset(self) -> None:
        self._results.clear()
