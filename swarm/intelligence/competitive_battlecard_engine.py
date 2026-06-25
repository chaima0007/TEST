"""Module 24 — Competitive Battlecard Engine."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CompetitorThreat(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class BattlecardAction(str, Enum):
    ESCALATE = "escalate"
    DIFFERENTIATE = "differentiate"
    COUNTER = "counter"
    MONITOR = "monitor"


class WinProbability(str, Enum):
    STRONG = "strong"      # >=70
    MODERATE = "moderate"  # >=45
    WEAK = "weak"          # >=25
    VERY_WEAK = "very_weak"  # <25


class MarketPosition(str, Enum):
    LEADER = "leader"
    CHALLENGER = "challenger"
    NICHE = "niche"
    EMERGING = "emerging"


@dataclass
class CompetitorProfile:
    competitor_id: str
    competitor_name: str
    market_position: MarketPosition
    # Threat signals (each contributes to threat score)
    active_deals_competing: int       # number of active deals they appear in
    win_rate_against_us_pct: float    # their historical win rate vs us (0-100)
    avg_discount_offered_pct: float   # average discount they offer (0-100)
    feature_parity_pct: float         # % of our features they match (0-100)
    price_vs_us_pct: float            # their price relative to ours (e.g. 80 = 20% cheaper)
    # Our strengths vs them
    our_unique_features: list[str]
    our_integration_advantages: list[str]
    our_support_rating: float         # 0-10
    their_support_rating: float       # 0-10
    # Their weaknesses (known)
    known_weaknesses: list[str]
    # Market signal
    recent_price_drop: bool
    new_product_launched: bool
    funding_raised: bool
    customer_churn_signal: bool       # known customer dissatisfaction


@dataclass
class BattlecardResult:
    competitor_id: str
    competitor_name: str
    market_position: str
    threat_score: float              # 0-100
    threat_level: CompetitorThreat
    win_probability: WinProbability
    battlecard_action: BattlecardAction
    executive_summary: str
    our_advantages: list[str]
    their_advantages: list[str]
    counter_tactics: list[str]
    talk_tracks: list[str]
    objection_responses: list[str]
    red_flags: list[str]

    def to_dict(self) -> dict:
        return {
            "competitor_id": self.competitor_id,
            "competitor_name": self.competitor_name,
            "market_position": self.market_position,
            "threat_score": self.threat_score,
            "threat_level": self.threat_level.value,
            "win_probability": self.win_probability.value,
            "battlecard_action": self.battlecard_action.value,
            "executive_summary": self.executive_summary,
            "our_advantages": self.our_advantages,
            "their_advantages": self.their_advantages,
            "counter_tactics": self.counter_tactics,
            "talk_tracks": self.talk_tracks,
            "objection_responses": self.objection_responses,
            "red_flags": self.red_flags,
        }


def _threat_score(comp: CompetitorProfile) -> float:
    """Compute threat score 0-100."""
    pts = 0.0
    # Win rate against us: up to 30 pts
    if comp.win_rate_against_us_pct >= 60:
        pts += 30
    elif comp.win_rate_against_us_pct >= 45:
        pts += 20
    elif comp.win_rate_against_us_pct >= 30:
        pts += 12
    else:
        pts += 4
    # Active deal count: up to 20 pts
    if comp.active_deals_competing >= 10:
        pts += 20
    elif comp.active_deals_competing >= 5:
        pts += 13
    elif comp.active_deals_competing >= 2:
        pts += 7
    else:
        pts += 2
    # Feature parity: up to 20 pts
    if comp.feature_parity_pct >= 80:
        pts += 20
    elif comp.feature_parity_pct >= 60:
        pts += 13
    elif comp.feature_parity_pct >= 40:
        pts += 7
    else:
        pts += 2
    # Price aggression: up to 15 pts (cheaper = more threatening)
    if comp.price_vs_us_pct <= 70:
        pts += 15
    elif comp.price_vs_us_pct <= 85:
        pts += 9
    elif comp.price_vs_us_pct <= 95:
        pts += 4
    # Market signals: up to 15 pts
    if comp.recent_price_drop:
        pts += 5
    if comp.new_product_launched:
        pts += 5
    if comp.funding_raised:
        pts += 5
    return max(0.0, min(100.0, round(pts, 1)))


def _threat_level(score: float) -> CompetitorThreat:
    if score >= 70:
        return CompetitorThreat.CRITICAL
    if score >= 50:
        return CompetitorThreat.HIGH
    if score >= 30:
        return CompetitorThreat.MEDIUM
    return CompetitorThreat.LOW


def _win_probability(comp: CompetitorProfile) -> WinProbability:
    win_pct = 100 - comp.win_rate_against_us_pct
    if win_pct >= 70:
        return WinProbability.STRONG
    if win_pct >= 45:
        return WinProbability.MODERATE
    if win_pct >= 25:
        return WinProbability.WEAK
    return WinProbability.VERY_WEAK


def _battlecard_action(
    threat: CompetitorThreat,
    comp: CompetitorProfile,
) -> BattlecardAction:
    if threat == CompetitorThreat.CRITICAL:
        return BattlecardAction.ESCALATE
    if threat == CompetitorThreat.HIGH:
        return BattlecardAction.DIFFERENTIATE
    if comp.feature_parity_pct >= 50 or comp.avg_discount_offered_pct >= 20:
        return BattlecardAction.COUNTER
    return BattlecardAction.MONITOR


def _our_advantages(comp: CompetitorProfile) -> list[str]:
    adv: list[str] = []
    if comp.our_support_rating - comp.their_support_rating >= 1.5:
        adv.append(
            f"Support & CS supérieur ({comp.our_support_rating}/10 vs {comp.their_support_rating}/10)"
        )
    if comp.price_vs_us_pct > 100:
        adv.append("Pricing plus compétitif — meilleur rapport qualité/prix")
    if len(comp.our_unique_features) >= 3:
        adv.append(f"{len(comp.our_unique_features)} fonctionnalités exclusives non réplicables")
    elif len(comp.our_unique_features) >= 1:
        adv.append(f"{len(comp.our_unique_features)} fonctionnalité(s) exclusive(s)")
    if comp.our_integration_advantages:
        adv.append(f"Écosystème d'intégrations supérieur ({len(comp.our_integration_advantages)} intégrations clés)")
    if comp.customer_churn_signal:
        adv.append("Clients {nom} mécontents — opportunité de déplacement active")
    for feat in comp.our_unique_features[:3]:
        adv.append(feat)
    return adv


def _their_advantages(comp: CompetitorProfile) -> list[str]:
    adv: list[str] = []
    if comp.price_vs_us_pct <= 85:
        adv.append(f"Prix {100 - comp.price_vs_us_pct:.0f}% inférieur — pression tarifaire")
    if comp.feature_parity_pct >= 70:
        adv.append(f"Parité fonctionnelle élevée ({comp.feature_parity_pct:.0f}%)")
    if comp.market_position in (MarketPosition.LEADER, MarketPosition.CHALLENGER):
        adv.append("Notoriété marché et base installée importante")
    if comp.avg_discount_offered_pct >= 25:
        adv.append(f"Remises agressives jusqu'à {comp.avg_discount_offered_pct:.0f}%")
    if comp.new_product_launched:
        adv.append("Nouveau produit récemment lancé — momentum marketing")
    if comp.funding_raised:
        adv.append("Financement récent — guerre des prix possible")
    return adv


def _counter_tactics(comp: CompetitorProfile, threat: CompetitorThreat) -> list[str]:
    tactics: list[str] = []
    if comp.avg_discount_offered_pct >= 20:
        tactics.append("Qualifier le budget avant tout — ne pas s'engager sur le prix sans valeur")
        tactics.append("Présenter le TCO complet — coût de migration + support inclus")
    if comp.feature_parity_pct >= 60:
        tactics.append("Démonstration live des fonctionnalités différenciantes — éviter la comparaison liste")
        tactics.append("Mettre en avant la roadmap — innovation en avance sur la concurrence")
    if threat in (CompetitorThreat.CRITICAL, CompetitorThreat.HIGH):
        tactics.append("Impliquer un exec sponsor — mobiliser C-level si deal à risque")
        tactics.append("Référence client sectorielle — prouver la valeur par les pairs")
    if comp.known_weaknesses:
        tactics.append(f"Exploiter les faiblesses connues : {', '.join(comp.known_weaknesses[:2])}")
    tactics.append("Proposer une période d'essai ou POC — réduire le risque perçu")
    return tactics


def _talk_tracks(comp: CompetitorProfile) -> list[str]:
    tracks: list[str] = []
    tracks.append(
        f"« Nous comprenons que vous évaluez {comp.competitor_name}. Voici pourquoi nos clients choisissent notre solution pour le long terme... »"
    )
    if comp.avg_discount_offered_pct >= 20:
        tracks.append(
            "« Un prix bas aujourd'hui peut coûter cher demain — regardons le TCO sur 3 ans ensemble. »"
        )
    if comp.known_weaknesses:
        tracks.append(
            f"« Nos clients venant de {comp.competitor_name} mentionnent souvent : {comp.known_weaknesses[0]}. Comment gérez-vous ce risque ? »"
        )
    if comp.customer_churn_signal:
        tracks.append(
            f"« Nous aidons actuellement plusieurs clients {comp.competitor_name} en transition — je peux partager leur retour d'expérience. »"
        )
    tracks.append(
        "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. Voici ce que nos clients mesurent... »"
    )
    return tracks


def _objection_responses(comp: CompetitorProfile) -> list[str]:
    responses: list[str] = []
    if comp.price_vs_us_pct <= 90:
        responses.append(
            "Objection prix : « Notre prix reflète un ROI documenté. Sur 3 ans, nos clients économisent en moyenne X% grâce à [valeur]. »"
        )
    responses.append(
        f"Objection fonctionnalités : « {comp.competitor_name} couvre {comp.feature_parity_pct:.0f}% de nos features — mais les 20% restants sont précisément ce qui génère le ROI que vous cherchez. »"
    )
    if comp.new_product_launched:
        responses.append(
            "Objection nouveau produit concurrent : « Un lancement récent = risque de maturité. Nos clients bénéficient de X années de stabilité et de roadmap prouvée. »"
        )
    responses.append(
        "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »"
    )
    return responses


def _red_flags(comp: CompetitorProfile) -> list[str]:
    flags: list[str] = []
    if comp.win_rate_against_us_pct >= 50:
        flags.append(f"Taux de victoire contre nous élevé ({comp.win_rate_against_us_pct:.0f}%) — analyse des deals perdus requise")
    if comp.active_deals_competing >= 8:
        flags.append(f"Présent dans {comp.active_deals_competing} deals actifs — risque pipeline systémique")
    if comp.recent_price_drop:
        flags.append("Baisse de prix récente — guerre des prix en cours")
    if comp.funding_raised:
        flags.append("Nouveau financement — investissements produit/marketing attendus")
    if comp.feature_parity_pct >= 80:
        flags.append("Parité fonctionnelle critique — différenciation urgente requise")
    return flags


def _executive_summary(
    comp: CompetitorProfile,
    threat: CompetitorThreat,
    action: BattlecardAction,
) -> str:
    pos = comp.market_position.value.capitalize()
    return (
        f"{comp.competitor_name} ({pos}) représente une menace {threat.value} "
        f"avec un taux de victoire historique de {comp.win_rate_against_us_pct:.0f}% contre nous. "
        f"Action recommandée : {action.value.replace('_', ' ')}. "
        f"Parité fonctionnelle à {comp.feature_parity_pct:.0f}% — "
        f"différenciation sur {'support, intégrations et roadmap' if comp.our_unique_features else 'ROI et service'}."
    )


class CompetitiveBattlecardEngine:
    """Generates real-time competitive battlecards for sales reps."""

    def __init__(self) -> None:
        self._battlecards: dict[str, BattlecardResult] = {}

    def generate(self, comp: CompetitorProfile) -> BattlecardResult:
        score = _threat_score(comp)
        threat = _threat_level(score)
        win_prob = _win_probability(comp)
        action = _battlecard_action(threat, comp)

        result = BattlecardResult(
            competitor_id=comp.competitor_id,
            competitor_name=comp.competitor_name,
            market_position=comp.market_position.value,
            threat_score=score,
            threat_level=threat,
            win_probability=win_prob,
            battlecard_action=action,
            executive_summary=_executive_summary(comp, threat, action),
            our_advantages=_our_advantages(comp),
            their_advantages=_their_advantages(comp),
            counter_tactics=_counter_tactics(comp, threat),
            talk_tracks=_talk_tracks(comp),
            objection_responses=_objection_responses(comp),
            red_flags=_red_flags(comp),
        )
        self._battlecards[comp.competitor_id] = result
        return result

    def generate_batch(self, competitors: list[CompetitorProfile]) -> list[BattlecardResult]:
        results = [self.generate(c) for c in competitors]
        return sorted(results, key=lambda r: r.threat_score, reverse=True)

    # ── Read helpers ──────────────────────────────────────────────────────────

    def all_battlecards(self) -> list[BattlecardResult]:
        return sorted(self._battlecards.values(), key=lambda r: r.threat_score, reverse=True)

    def by_threat(self, threat: CompetitorThreat) -> list[BattlecardResult]:
        return [r for r in self.all_battlecards() if r.threat_level == threat]

    def by_action(self, action: BattlecardAction) -> list[BattlecardResult]:
        return [r for r in self.all_battlecards() if r.battlecard_action == action]

    def by_win_probability(self, prob: WinProbability) -> list[BattlecardResult]:
        return [r for r in self.all_battlecards() if r.win_probability == prob]

    def critical_threats(self) -> list[BattlecardResult]:
        return self.by_threat(CompetitorThreat.CRITICAL)

    def needs_escalation(self) -> list[BattlecardResult]:
        return self.by_action(BattlecardAction.ESCALATE)

    def avg_threat_score(self) -> float:
        cards = list(self._battlecards.values())
        if not cards:
            return 0.0
        return round(sum(r.threat_score for r in cards) / len(cards), 1)

    def summary(self) -> dict:
        cards = list(self._battlecards.values())
        n = len(cards)
        threat_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        win_counts: dict[str, int] = {}
        for r in cards:
            threat_counts[r.threat_level.value] = threat_counts.get(r.threat_level.value, 0) + 1
            action_counts[r.battlecard_action.value] = action_counts.get(r.battlecard_action.value, 0) + 1
            win_counts[r.win_probability.value] = win_counts.get(r.win_probability.value, 0) + 1
        return {
            "total": n,
            "threat_counts": threat_counts,
            "action_counts": action_counts,
            "win_probability_counts": win_counts,
            "avg_threat_score": self.avg_threat_score(),
            "critical_count": len(self.critical_threats()),
            "escalation_count": len(self.needs_escalation()),
        }

    def reset(self) -> None:
        self._battlecards.clear()
