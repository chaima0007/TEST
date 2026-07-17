from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DealOutcome(str, Enum):
    WON = "won"
    LOST = "lost"
    NO_DECISION = "no_decision"
    CHURNED = "churned"


class LossReason(str, Enum):
    PRICE = "price"
    PRODUCT = "product"
    COMPETITOR = "competitor"
    TIMING = "timing"
    CHAMPION_LEFT = "champion_left"
    INTERNAL_PRIORITY = "internal_priority"
    RELATIONSHIP = "relationship"
    UNKNOWN = "unknown"


class CompetitivePosition(str, Enum):
    DOMINANT = "dominant"      # win rate ≥70%
    STRONG = "strong"          # win rate 50-69%
    COMPETITIVE = "competitive" # win rate 30-49%
    WEAK = "weak"              # win rate <30%
    UNKNOWN = "unknown"        # insufficient data


class CompetitiveAction(str, Enum):
    REPLICATE = "replicate"    # winning patterns to scale
    DEFEND = "defend"          # protect position
    DIFFERENTIATE = "differentiate"  # strengthen differentiators
    BATTLECARD = "battlecard"  # urgent competitive enablement needed


@dataclass
class DealRecord:
    deal_id: str
    competitor: str
    outcome: DealOutcome
    loss_reason: LossReason | None
    deal_size_eur: float
    segment: str
    region: str
    sales_cycle_days: int
    rep_id: str
    # Signals
    price_objection: bool
    product_gap_mentioned: bool
    exec_sponsor_engaged: bool
    proof_of_concept_done: bool
    references_provided: bool


@dataclass
class CompetitorAnalysis:
    competitor: str
    total_deals: int
    wins: int
    losses: int
    no_decisions: int
    win_rate_pct: float
    avg_deal_size_eur: float
    avg_cycle_days: float
    position: CompetitivePosition
    action: CompetitiveAction
    top_loss_reasons: list[str]
    win_patterns: list[str]
    loss_patterns: list[str]
    battlecard_priorities: list[str]
    arr_won_eur: float
    arr_lost_eur: float
    net_arr_eur: float              # won - lost

    def to_dict(self) -> dict:
        return {
            "competitor": self.competitor,
            "total_deals": self.total_deals,
            "wins": self.wins,
            "losses": self.losses,
            "no_decisions": self.no_decisions,
            "win_rate_pct": self.win_rate_pct,
            "avg_deal_size_eur": self.avg_deal_size_eur,
            "avg_cycle_days": self.avg_cycle_days,
            "position": self.position.value,
            "action": self.action.value,
            "top_loss_reasons": self.top_loss_reasons,
            "win_patterns": self.win_patterns,
            "loss_patterns": self.loss_patterns,
            "battlecard_priorities": self.battlecard_priorities,
            "arr_won_eur": self.arr_won_eur,
            "arr_lost_eur": self.arr_lost_eur,
            "net_arr_eur": self.net_arr_eur,
        }


def _win_rate_pct(wins: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((wins / total) * 100.0, 1)


def _competitive_position(win_rate: float, total: int) -> CompetitivePosition:
    if total < 3:
        return CompetitivePosition.UNKNOWN
    if win_rate >= 70:
        return CompetitivePosition.DOMINANT
    if win_rate >= 50:
        return CompetitivePosition.STRONG
    if win_rate >= 30:
        return CompetitivePosition.COMPETITIVE
    return CompetitivePosition.WEAK


def _competitive_action(position: CompetitivePosition, win_rate: float) -> CompetitiveAction:
    if position == CompetitivePosition.DOMINANT:
        return CompetitiveAction.REPLICATE
    if position == CompetitivePosition.STRONG:
        return CompetitiveAction.DEFEND
    if position in (CompetitivePosition.COMPETITIVE, CompetitivePosition.UNKNOWN):
        return CompetitiveAction.DIFFERENTIATE
    return CompetitiveAction.BATTLECARD


def _top_loss_reasons(losses: list[DealRecord]) -> list[str]:
    if not losses:
        return []
    counts: dict[str, int] = {}
    for d in losses:
        reason = d.loss_reason.value if d.loss_reason else LossReason.UNKNOWN.value
        counts[reason] = counts.get(reason, 0) + 1
    sorted_reasons = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    labels = {
        "price": "Pricing trop élevé vs. concurrent",
        "product": "Gap fonctionnel identifié par le prospect",
        "competitor": "Relation établie avec le concurrent",
        "timing": "Décision reportée — mauvais timing",
        "champion_left": "Champion interne a quitté l'entreprise",
        "internal_priority": "Projet déprioritisé en interne",
        "relationship": "Relation insuffisante avec le décideur",
        "unknown": "Raison non identifiée — debriefing manquant",
    }
    return [f"{labels.get(r, r)} ({c} deals)" for r, c in sorted_reasons[:3]]


def _win_patterns(wins: list[DealRecord]) -> list[str]:
    if not wins:
        return []
    patterns: list[str] = []
    total = len(wins)
    poc_rate = sum(1 for d in wins if d.proof_of_concept_done) / total
    ref_rate = sum(1 for d in wins if d.references_provided) / total
    exec_rate = sum(1 for d in wins if d.exec_sponsor_engaged) / total
    if poc_rate >= 0.6:
        patterns.append(f"POC systématique — {poc_rate:.0%} des deals gagnés incluaient un POC")
    if ref_rate >= 0.5:
        patterns.append(f"Références clients clés — {ref_rate:.0%} avec références fournies")
    if exec_rate >= 0.7:
        patterns.append(f"Engagement C-level — {exec_rate:.0%} avec sponsor exécutif engagé")
    avg_size = sum(d.deal_size_eur for d in wins) / total
    if avg_size > 0:
        patterns.append(f"Taille moyenne des deals gagnés: {avg_size:,.0f}€")
    return patterns


def _loss_patterns(losses: list[DealRecord]) -> list[str]:
    if not losses:
        return []
    patterns: list[str] = []
    total = len(losses)
    price_rate = sum(1 for d in losses if d.price_objection) / total
    product_rate = sum(1 for d in losses if d.product_gap_mentioned) / total
    exec_rate = sum(1 for d in losses if not d.exec_sponsor_engaged) / total
    if price_rate >= 0.5:
        patterns.append(f"Objection prix fréquente — {price_rate:.0%} des défaites liées au prix")
    if product_rate >= 0.4:
        patterns.append(f"Gap produit mentionné — {product_rate:.0%} des défaites avec gap fonctionnel")
    if exec_rate >= 0.6:
        patterns.append(f"Sponsor exécutif absent — {exec_rate:.0%} des défaites sans C-level engagé")
    avg_cycle = sum(d.sales_cycle_days for d in losses) / total
    patterns.append(f"Cycle de vente moyen des défaites: {avg_cycle:.0f}j")
    return patterns


def _battlecard_priorities(
    losses: list[DealRecord], position: CompetitivePosition, competitor: str
) -> list[str]:
    priorities: list[str] = []
    price_losses = sum(1 for d in losses if d.price_objection)
    product_losses = sum(1 for d in losses if d.product_gap_mentioned)
    if price_losses > 0:
        priorities.append(f"Préparer la justification ROI vs. {competitor} — contrer l'argument prix")
    if product_losses > 0:
        priorities.append(f"Documenter les fonctionnalités différenciantes vs. {competitor}")
    if position == CompetitivePosition.WEAK:
        priorities.append(f"Win story urgente — 3 cas clients gagnés vs. {competitor} à documenter")
        priorities.append("Définir le terrain de jeu idéal — éviter les deals où le concurrent est fort")
    elif position == CompetitivePosition.COMPETITIVE:
        priorities.append(f"Renforcer la discovery pour détecter {competitor} tôt")
        priorities.append("Préparer des références clients dans le même secteur")
    elif position == CompetitivePosition.STRONG:
        priorities.append("Maintenir l'avantage — surveiller les évolutions produit du concurrent")
    else:
        priorities.append(f"Documenter le playbook gagnant vs. {competitor} pour l'équipe")
    return priorities


class CompetitiveWinLossAnalyzer:
    def __init__(self) -> None:
        self._deals: list[DealRecord] = []
        self._analyses: dict[str, CompetitorAnalysis] = {}

    def add_deal(self, deal: DealRecord) -> None:
        self._deals.append(deal)
        self._analyses.pop(deal.competitor, None)

    def add_deals(self, deals: list[DealRecord]) -> None:
        for d in deals:
            self._deals.append(d)
        self._analyses.clear()

    def _analyze_competitor(self, competitor: str) -> CompetitorAnalysis:
        deals = [d for d in self._deals if d.competitor == competitor]
        wins = [d for d in deals if d.outcome == DealOutcome.WON]
        losses = [d for d in deals if d.outcome == DealOutcome.LOST]
        no_dec = [d for d in deals if d.outcome == DealOutcome.NO_DECISION]
        total = len(deals)
        wr = _win_rate_pct(len(wins), total)
        avg_size = sum(d.deal_size_eur for d in deals) / total if total else 0.0
        avg_cycle = sum(d.sales_cycle_days for d in deals) / total if total else 0.0
        arr_won = sum(d.deal_size_eur for d in wins)
        arr_lost = sum(d.deal_size_eur for d in losses)
        position = _competitive_position(wr, total)
        action = _competitive_action(position, wr)
        analysis = CompetitorAnalysis(
            competitor=competitor,
            total_deals=total,
            wins=len(wins),
            losses=len(losses),
            no_decisions=len(no_dec),
            win_rate_pct=wr,
            avg_deal_size_eur=round(avg_size, 0),
            avg_cycle_days=round(avg_cycle, 1),
            position=position,
            action=action,
            top_loss_reasons=_top_loss_reasons(losses),
            win_patterns=_win_patterns(wins),
            loss_patterns=_loss_patterns(losses),
            battlecard_priorities=_battlecard_priorities(losses, position, competitor),
            arr_won_eur=arr_won,
            arr_lost_eur=arr_lost,
            net_arr_eur=arr_won - arr_lost,
        )
        self._analyses[competitor] = analysis
        return analysis

    def analyze(self, competitor: str) -> CompetitorAnalysis:
        return self._analyze_competitor(competitor)

    def analyze_all(self) -> list[CompetitorAnalysis]:
        competitors = list({d.competitor for d in self._deals})
        return sorted(
            [self._analyze_competitor(c) for c in competitors],
            key=lambda a: a.win_rate_pct,
            reverse=True,
        )

    def by_position(self, position: CompetitivePosition) -> list[CompetitorAnalysis]:
        return [a for a in self.analyze_all() if a.position == position]

    def weakest_competitors(self) -> list[CompetitorAnalysis]:
        return self.by_position(CompetitivePosition.WEAK)

    def dominant_over(self) -> list[CompetitorAnalysis]:
        return self.by_position(CompetitivePosition.DOMINANT)

    def needs_battlecard(self) -> list[CompetitorAnalysis]:
        return [a for a in self.analyze_all() if a.action == CompetitiveAction.BATTLECARD]

    def overall_win_rate(self) -> float:
        total = len(self._deals)
        if not total:
            return 0.0
        wins = sum(1 for d in self._deals if d.outcome == DealOutcome.WON)
        return round((wins / total) * 100.0, 1)

    def total_arr_won_eur(self) -> float:
        return sum(d.deal_size_eur for d in self._deals if d.outcome == DealOutcome.WON)

    def total_arr_lost_eur(self) -> float:
        return sum(d.deal_size_eur for d in self._deals if d.outcome == DealOutcome.LOST)

    def most_common_loss_reason(self) -> str:
        losses = [d for d in self._deals if d.outcome == DealOutcome.LOST]
        if not losses:
            return LossReason.UNKNOWN.value
        counts: dict[str, int] = {}
        for d in losses:
            r = d.loss_reason.value if d.loss_reason else LossReason.UNKNOWN.value
            counts[r] = counts.get(r, 0) + 1
        return max(counts, key=counts.get)  # type: ignore[arg-type]

    def summary(self) -> dict:
        analyses = self.analyze_all()
        total_d = len(self._deals)
        return {
            "total_deals": total_d,
            "total_competitors": len(analyses),
            "overall_win_rate_pct": self.overall_win_rate(),
            "total_arr_won_eur": self.total_arr_won_eur(),
            "total_arr_lost_eur": self.total_arr_lost_eur(),
            "net_arr_eur": self.total_arr_won_eur() - self.total_arr_lost_eur(),
            "position_counts": {
                p.value: sum(1 for a in analyses if a.position == p) for p in CompetitivePosition
            },
            "action_counts": {
                a.value: sum(1 for an in analyses if an.action == a) for a in CompetitiveAction
            },
            "most_common_loss_reason": self.most_common_loss_reason(),
            "needs_battlecard_count": len(self.needs_battlecard()),
        }

    def reset(self) -> None:
        self._deals.clear()
        self._analyses.clear()
