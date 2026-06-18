"""Module 40 — Competitive Intelligence Engine

Analyses competitive mentions, win/loss patterns and threat levels for each
deal, generates battle-card actions and rep coaching recommendations to defend
against or displace named competitors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class CompetitorThreat(str, Enum):
    CRITICAL  = "critical"   # competitor is actively being evaluated, risk of immediate loss
    HIGH      = "high"       # strong competitive presence, evaluation likely
    MODERATE  = "moderate"   # competitor mentioned but not actively evaluated
    LOW       = "low"        # minor competitive mention, no active evaluation
    NONE      = "none"       # no competitor signals detected


class CompetitivePosition(str, Enum):
    WINNING    = "winning"    # strong indicators we will close
    LEADING    = "leading"    # ahead but not yet locked
    TIED       = "tied"       # neither side has clear advantage
    TRAILING   = "trailing"   # competitor has advantage, recover possible
    LOSING     = "losing"     # high probability of losing to competitor


class CompetitorCategory(str, Enum):
    ENTERPRISE    = "enterprise"     # established enterprise vendor (SAP, Salesforce…)
    MID_MARKET    = "mid_market"     # mid-market specialist
    STARTUP       = "startup"        # emerging challenger
    OPEN_SOURCE   = "open_source"    # free / community product
    IN_HOUSE      = "in_house"       # prospect building internally
    UNKNOWN       = "unknown"        # identity not confirmed


class CompetitiveAction(str, Enum):
    DEFEND_AND_CLOSE  = "defend_and_close"   # neutralise threat and accelerate close
    DIFFERENTIATE     = "differentiate"      # emphasise unique advantages
    ESCALATE          = "escalate"           # involve exec / solution architect
    PRICE_PROTECT     = "price_protect"      # address price-based objection
    MAINTAIN          = "maintain"           # sustain current position
    MONITOR           = "monitor"            # no active threat — keep watch


# ─── Input ────────────────────────────────────────────────────────────────────

@dataclass
class CompetitiveInput:
    deal_id: str
    deal_name: str
    rep_id: str
    rep_name: str
    account_name: str
    deal_size_eur: float
    # Competitor details
    competitor_name: str
    competitor_category: CompetitorCategory
    # Threat signals
    prospect_requested_competitor_demo: bool
    prospect_shared_competitor_pricing: bool
    prospect_mentioned_competitor_features: bool
    champion_supports_competitor: bool
    decision_maker_met_competitor: bool
    rfp_sent_to_competitor: bool
    # Our position
    executive_sponsor_engaged: bool
    decision_maker_relationship_score: int   # 0–10
    product_fit_score: int                   # 0–10
    price_competitive: bool
    unique_features_count: int               # features competitor cannot match
    references_provided: bool
    proof_of_concept_completed: bool
    # History
    previous_losses_to_competitor: int       # count of past losses
    win_rate_vs_competitor_pct: float        # 0–100
    days_since_competitor_first_mentioned: int


# ─── Output ───────────────────────────────────────────────────────────────────

@dataclass
class CompetitiveResult:
    deal_id: str
    deal_name: str
    rep_id: str
    rep_name: str
    account_name: str
    competitor_name: str
    competitor_category: str
    competitor_threat: str
    competitive_position: str
    competitive_action: str
    threat_score: float            # 0–100, higher = more threatened
    position_score: float          # 0–100, higher = stronger position
    win_probability_pct: float     # estimated win probability 0–100
    battle_tactics: list[str]
    differentiators: list[str]
    risk_signals: list[str]
    manager_alerts: list[str]

    def to_dict(self) -> dict:
        return {
            "deal_id":              self.deal_id,
            "deal_name":            self.deal_name,
            "rep_id":               self.rep_id,
            "rep_name":             self.rep_name,
            "account_name":         self.account_name,
            "competitor_name":      self.competitor_name,
            "competitor_category":  self.competitor_category,
            "competitor_threat":    self.competitor_threat,
            "competitive_position": self.competitive_position,
            "competitive_action":   self.competitive_action,
            "threat_score":         self.threat_score,
            "position_score":       self.position_score,
            "win_probability_pct":  self.win_probability_pct,
            "battle_tactics":       self.battle_tactics,
            "differentiators":      self.differentiators,
            "risk_signals":         self.risk_signals,
            "manager_alerts":       self.manager_alerts,
        }


# ─── Engine ───────────────────────────────────────────────────────────────────

class CompetitiveIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[CompetitiveResult] = []

    # ── Threat scoring ─────────────────────────────────────────────────────────

    def _threat_score(self, inp: CompetitiveInput) -> float:
        score = 0.0
        # Active evaluation signals (high weight)
        if inp.rfp_sent_to_competitor:                    score += 30
        if inp.prospect_requested_competitor_demo:        score += 20
        if inp.decision_maker_met_competitor:             score += 20
        if inp.prospect_shared_competitor_pricing:        score += 15
        if inp.champion_supports_competitor:              score += 20
        # Passive signals (medium weight)
        if inp.prospect_mentioned_competitor_features:    score += 10
        # Historical loss pattern
        score += min(20, inp.previous_losses_to_competitor * 5)
        # Low win rate amplifies threat
        if inp.win_rate_vs_competitor_pct < 30:           score += 15
        elif inp.win_rate_vs_competitor_pct < 50:         score += 8
        return min(100.0, score)

    # ── Position scoring ───────────────────────────────────────────────────────

    def _position_score(self, inp: CompetitiveInput) -> float:
        score = 0.0
        # Relationship strength
        score += min(20, inp.decision_maker_relationship_score * 2)
        # Product fit
        score += min(20, inp.product_fit_score * 2)
        # Executive engagement
        if inp.executive_sponsor_engaged:                 score += 15
        # Proof points
        if inp.proof_of_concept_completed:                score += 15
        if inp.references_provided:                       score += 10
        # Competitive advantages
        score += min(15, inp.unique_features_count * 3)
        # Price competitiveness
        if inp.price_competitive:                         score += 10
        # Win-rate boost
        if inp.win_rate_vs_competitor_pct >= 70:          score += 10
        elif inp.win_rate_vs_competitor_pct >= 50:        score += 5
        return min(100.0, score)

    # ── Competitor threat level ────────────────────────────────────────────────

    def _competitor_threat(self, threat_score: float) -> CompetitorThreat:
        if threat_score >= 70:   return CompetitorThreat.CRITICAL
        if threat_score >= 50:   return CompetitorThreat.HIGH
        if threat_score >= 30:   return CompetitorThreat.MODERATE
        if threat_score >= 10:   return CompetitorThreat.LOW
        return CompetitorThreat.NONE

    # ── Competitive position ───────────────────────────────────────────────────

    def _competitive_position(
        self, position_score: float, threat_score: float
    ) -> CompetitivePosition:
        delta = position_score - threat_score
        if delta >= 30:    return CompetitivePosition.WINNING
        if delta >= 10:    return CompetitivePosition.LEADING
        if delta >= -10:   return CompetitivePosition.TIED
        if delta >= -30:   return CompetitivePosition.TRAILING
        return CompetitivePosition.LOSING

    # ── Win probability ────────────────────────────────────────────────────────

    def _win_probability(
        self, position_score: float, threat_score: float, inp: CompetitiveInput
    ) -> float:
        base = 50.0 + (position_score - threat_score) * 0.5
        # Historical win rate anchors the estimate
        base = base * 0.6 + inp.win_rate_vs_competitor_pct * 0.4
        # Penalty for champion supporting competitor
        if inp.champion_supports_competitor:   base -= 15
        # Boost from exec engagement
        if inp.executive_sponsor_engaged:      base += 8
        # Boost from completed PoC
        if inp.proof_of_concept_completed:     base += 7
        return max(5.0, min(95.0, round(base, 1)))

    # ── Recommended action ────────────────────────────────────────────────────

    def _competitive_action(
        self,
        threat: CompetitorThreat,
        position: CompetitivePosition,
        inp: CompetitiveInput,
    ) -> CompetitiveAction:
        if threat in (CompetitorThreat.CRITICAL, CompetitorThreat.HIGH):
            if position in (CompetitivePosition.LOSING, CompetitivePosition.TRAILING):
                return CompetitiveAction.ESCALATE
            if not inp.price_competitive and inp.prospect_shared_competitor_pricing:
                return CompetitiveAction.PRICE_PROTECT
            return CompetitiveAction.DEFEND_AND_CLOSE
        if threat == CompetitorThreat.MODERATE:
            if inp.unique_features_count >= 2:
                return CompetitiveAction.DIFFERENTIATE
            return CompetitiveAction.DEFEND_AND_CLOSE
        if threat == CompetitorThreat.LOW:
            return CompetitiveAction.MAINTAIN
        return CompetitiveAction.MONITOR

    # ── Battle tactics ─────────────────────────────────────────────────────────

    def _battle_tactics(
        self, inp: CompetitiveInput, action: CompetitiveAction
    ) -> list[str]:
        tactics: list[str] = []
        if action == CompetitiveAction.ESCALATE:
            tactics.append(
                f"Escalade exécutive urgente — impliquer le C-level pour contrer {inp.competitor_name}"
            )
            tactics.append("Planifier une session de solution architect pour démonstration technique approfondie")
        if inp.rfp_sent_to_competitor:
            tactics.append(
                f"RFP détecté chez {inp.competitor_name} — activer la battlecard de réponse RFP immédiatement"
            )
        if inp.prospect_requested_competitor_demo:
            tactics.append(
                f"Demo concurrente demandée — organiser une contre-démo centrée sur les cas d'usage critiques du client"
            )
        if inp.prospect_shared_competitor_pricing:
            tactics.append(
                "Grille tarifaire concurrente reçue — construire une analyse TCO sur 3 ans favorable"
            )
        if inp.champion_supports_competitor:
            tactics.append(
                "Champion adverse identifié — identifier et activer un champion alternatif chez le prospect"
            )
        if not inp.references_provided:
            tactics.append(
                "Aucune référence envoyée — sélectionner 2–3 clients comparables et organiser des calls de référence"
            )
        if not inp.proof_of_concept_completed and inp.product_fit_score >= 7:
            tactics.append(
                "Fort fit produit non démontré — proposer un PoC ciblé sur les cas d'usage clés"
            )
        if not tactics:
            tactics.append(
                f"Surveiller l'activité de {inp.competitor_name} — maintenir cadence d'engagement prospect"
            )
        return tactics

    # ── Differentiators ────────────────────────────────────────────────────────

    def _differentiators(self, inp: CompetitiveInput) -> list[str]:
        diff: list[str] = []
        if inp.unique_features_count >= 1:
            diff.append(
                f"{inp.unique_features_count} fonctionnalité(s) exclusive(s) non disponible(s) chez {inp.competitor_name}"
            )
        if inp.proof_of_concept_completed:
            diff.append("PoC complété — valeur prouvée sur l'environnement client réel")
        if inp.executive_sponsor_engaged:
            diff.append("Sponsor exécutif engagé — relation stratégique au niveau C confirmée")
        if inp.decision_maker_relationship_score >= 7:
            diff.append(
                f"Relation décideur forte ({inp.decision_maker_relationship_score}/10) — influence sur la décision finale"
            )
        if inp.win_rate_vs_competitor_pct >= 60:
            diff.append(
                f"Historique favorable vs {inp.competitor_name}: {inp.win_rate_vs_competitor_pct:.0f}% de taux de victoire"
            )
        if inp.price_competitive:
            diff.append("Position tarifaire compétitive — prix aligné ou avantageux vs concurrent")
        if not diff:
            diff.append("Identifier les différenciateurs clés lors de la prochaine réunion — préparer le battlecard")
        return diff

    # ── Risk signals ───────────────────────────────────────────────────────────

    def _risk_signals(self, inp: CompetitiveInput) -> list[str]:
        risks: list[str] = []
        if inp.rfp_sent_to_competitor:
            risks.append(f"RFP envoyé à {inp.competitor_name} — deal en danger immédiat")
        if inp.champion_supports_competitor:
            risks.append("Champion interne soutient le concurrent — influence décisionnelle compromise")
        if inp.decision_maker_met_competitor:
            risks.append(f"Décideur a rencontré {inp.competitor_name} — évaluation active en cours")
        if inp.previous_losses_to_competitor >= 3:
            risks.append(
                f"{inp.previous_losses_to_competitor} pertes historiques vs {inp.competitor_name} — pattern préoccupant"
            )
        if inp.win_rate_vs_competitor_pct < 30:
            risks.append(
                f"Taux de victoire historique de {inp.win_rate_vs_competitor_pct:.0f}% vs {inp.competitor_name} — taux critique"
            )
        if inp.prospect_shared_competitor_pricing and not inp.price_competitive:
            risks.append("Grille tarifaire concurrente partagée + notre prix non compétitif — risque de disqualification prix")
        if inp.days_since_competitor_first_mentioned > 30:
            risks.append(
                f"Concurrent mentionné depuis {inp.days_since_competitor_first_mentioned}j — évaluation longue durée, décision imminente"
            )
        return risks

    # ── Manager alerts ─────────────────────────────────────────────────────────

    def _manager_alerts(
        self,
        inp: CompetitiveInput,
        threat: CompetitorThreat,
        position: CompetitivePosition,
        win_prob: float,
    ) -> list[str]:
        alerts: list[str] = []
        if threat == CompetitorThreat.CRITICAL:
            alerts.append(
                f"⚠ Menace critique ({inp.competitor_name}) sur deal {inp.deal_name} ({inp.deal_size_eur:,.0f}€) — intervention immédiate requise"
            )
        if position in (CompetitivePosition.LOSING,):
            alerts.append(
                f"Position perdante vs {inp.competitor_name} — revue stratégique deal urgente avec le manager"
            )
        if win_prob < 25:
            alerts.append(
                f"Probabilité de victoire critique: {win_prob:.0f}% — évaluer si le deal doit être reclassifié"
            )
        if inp.rfp_sent_to_competitor and inp.deal_size_eur >= 50000:
            alerts.append(
                f"RFP deal stratégique ({inp.deal_size_eur:,.0f}€) — mobiliser l'équipe solution pour réponse complète"
            )
        return alerts

    # ── Main analysis ──────────────────────────────────────────────────────────

    def analyze(self, inp: CompetitiveInput) -> CompetitiveResult:
        threat_score    = self._threat_score(inp)
        position_score  = self._position_score(inp)
        threat          = self._competitor_threat(threat_score)
        position        = self._competitive_position(position_score, threat_score)
        action          = self._competitive_action(threat, position, inp)
        win_prob        = self._win_probability(position_score, threat_score, inp)

        result = CompetitiveResult(
            deal_id             = inp.deal_id,
            deal_name           = inp.deal_name,
            rep_id              = inp.rep_id,
            rep_name            = inp.rep_name,
            account_name        = inp.account_name,
            competitor_name     = inp.competitor_name,
            competitor_category = inp.competitor_category.value,
            competitor_threat   = threat.value,
            competitive_position= position.value,
            competitive_action  = action.value,
            threat_score        = round(threat_score, 1),
            position_score      = round(position_score, 1),
            win_probability_pct = win_prob,
            battle_tactics      = self._battle_tactics(inp, action),
            differentiators     = self._differentiators(inp),
            risk_signals        = self._risk_signals(inp),
            manager_alerts      = self._manager_alerts(inp, threat, position, win_prob),
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[CompetitiveInput]) -> list[CompetitiveResult]:
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.threat_score, reverse=True)
        return results

    # ── Helpers ────────────────────────────────────────────────────────────────

    def critical_threats(self) -> list[CompetitiveResult]:
        return [r for r in self._results if r.competitor_threat == CompetitorThreat.CRITICAL.value]

    def losing_deals(self) -> list[CompetitiveResult]:
        return [r for r in self._results if r.competitive_position == CompetitivePosition.LOSING.value]

    def needs_escalation(self) -> list[CompetitiveResult]:
        return [r for r in self._results if r.competitive_action == CompetitiveAction.ESCALATE.value]

    def high_value_at_risk(self, threshold_eur: float = 50000) -> list[CompetitiveResult]:
        return [
            r for r in self._results
            if r.competitor_threat in (CompetitorThreat.CRITICAL.value, CompetitorThreat.HIGH.value)
        ]

    def strong_positions(self) -> list[CompetitiveResult]:
        return [r for r in self._results if r.competitive_position == CompetitivePosition.WINNING.value]

    def summary(self) -> dict:
        results = self._results
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "threat_counts": {},
                "position_counts": {},
                "action_counts": {},
                "avg_threat_score": 0.0,
                "avg_position_score": 0.0,
                "avg_win_probability": 0.0,
                "critical_count": 0,
                "losing_count": 0,
                "escalation_count": 0,
            }
        threat_counts:   dict[str, int] = {}
        position_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_threat = total_position = total_win = 0.0

        for r in results:
            threat_counts[r.competitor_threat]       = threat_counts.get(r.competitor_threat, 0) + 1
            position_counts[r.competitive_position]  = position_counts.get(r.competitive_position, 0) + 1
            action_counts[r.competitive_action]      = action_counts.get(r.competitive_action, 0) + 1
            total_threat   += r.threat_score
            total_position += r.position_score
            total_win      += r.win_probability_pct

        return {
            "total":               n,
            "threat_counts":       threat_counts,
            "position_counts":     position_counts,
            "action_counts":       action_counts,
            "avg_threat_score":    round(total_threat / n, 1),
            "avg_position_score":  round(total_position / n, 1),
            "avg_win_probability": round(total_win / n, 1),
            "critical_count":      sum(1 for r in results if r.competitor_threat == CompetitorThreat.CRITICAL.value),
            "losing_count":        sum(1 for r in results if r.competitive_position == CompetitivePosition.LOSING.value),
            "escalation_count":    sum(1 for r in results if r.competitive_action == CompetitiveAction.ESCALATE.value),
        }

    def reset(self) -> None:
        self._results = []
