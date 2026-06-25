from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PositioningStrength(str, Enum):
    DOMINANT = "dominant"
    STRONG = "strong"
    COMPETITIVE = "competitive"
    WEAK = "weak"
    CRITICAL = "critical"


class CompetitorThreat(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ELIMINATED = "eliminated"
    UNKNOWN = "unknown"


class WinProbability(str, Enum):
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"


class PositioningAction(str, Enum):
    ACCELERATE = "accelerate"
    DIFFERENTIATE = "differentiate"
    DEFEND = "defend"
    EXECUTIVE_ESCALATION = "executive_escalation"
    COMPETITIVE_RESPONSE = "competitive_response"
    ABANDON = "abandon"


@dataclass
class CompetitivePositioningInput:
    deal_id: str
    account_id: str
    competitor_name: str
    deal_stage: str               # discovery/demo/proposal/negotiation/closing
    deal_value: float
    our_product_fit: float        # 0–100 fit score for prospect's needs
    competitor_product_fit: float # 0–100 competitor's fit score
    our_price_competitiveness: float  # 0–100 (100 = most competitive price)
    competitor_price_delta: float     # positive = we're more expensive (%)
    our_relationship_strength: float  # 0–100
    competitor_relationship_strength: float
    our_features_advantage: int   # -5 to +5 (positive = we have more features)
    champion_supports_us: bool
    economic_buyer_engaged: bool
    competitor_in_poc: bool       # competitor running a POC
    we_ran_poc: bool
    competitor_reference_count: int  # references they've provided
    our_reference_count: int
    days_in_stage: int
    expected_close_days: int
    prior_wins_vs_competitor: int
    prior_losses_vs_competitor: int
    competitor_incumbent: bool    # competitor is current vendor
    unique_differentiators: int   # count of unique differentiators we've demonstrated


@dataclass
class CompetitivePositioningResult:
    deal_id: str
    account_id: str
    competitor_name: str
    positioning_score: float
    positioning_strength: PositioningStrength
    competitor_threat: CompetitorThreat
    win_probability: WinProbability
    recommended_action: PositioningAction
    battlecard_points: list[str]
    risk_factors: list[str]
    win_rate_vs_competitor: float
    competitive_gap: float
    is_winnable: bool
    urgency_score: float
    key_differentiators: list[str]

    def to_dict(self) -> dict:
        return {
            "deal_id":                self.deal_id,
            "account_id":             self.account_id,
            "competitor_name":        self.competitor_name,
            "positioning_score":      self.positioning_score,
            "positioning_strength":   self.positioning_strength.value,
            "competitor_threat":      self.competitor_threat.value,
            "win_probability":        self.win_probability.value,
            "recommended_action":     self.recommended_action.value,
            "battlecard_points":      self.battlecard_points,
            "risk_factors":           self.risk_factors,
            "win_rate_vs_competitor": self.win_rate_vs_competitor,
            "competitive_gap":        self.competitive_gap,
            "is_winnable":            self.is_winnable,
            "urgency_score":          self.urgency_score,
            "key_differentiators":    self.key_differentiators,
        }


class CompetitivePositioningEngine:
    def __init__(self) -> None:
        self._results: list[CompetitivePositioningResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: CompetitivePositioningInput) -> CompetitivePositioningResult:
        pos_score  = self._positioning_score(inp)
        threat     = self._competitor_threat(inp)
        strength   = self._positioning_strength(pos_score, inp)
        win_rate   = self._win_rate(inp)
        win_prob   = self._win_probability(pos_score, win_rate, inp)
        gap        = self._competitive_gap(inp)
        urgency    = self._urgency_score(inp)
        action     = self._recommended_action(inp, pos_score, threat, win_prob)
        winnable   = win_prob not in (WinProbability.VERY_LOW,)
        battlecard = self._battlecard_points(inp, strength)
        risks      = self._risk_factors(inp, threat, pos_score)
        diffs      = self._key_differentiators(inp)

        result = CompetitivePositioningResult(
            deal_id=inp.deal_id,
            account_id=inp.account_id,
            competitor_name=inp.competitor_name,
            positioning_score=pos_score,
            positioning_strength=strength,
            competitor_threat=threat,
            win_probability=win_prob,
            recommended_action=action,
            battlecard_points=battlecard,
            risk_factors=risks,
            win_rate_vs_competitor=win_rate,
            competitive_gap=gap,
            is_winnable=winnable,
            urgency_score=urgency,
            key_differentiators=diffs,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[CompetitivePositioningInput]
    ) -> list[CompetitivePositioningResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def high_threat_deals(self) -> list[CompetitivePositioningResult]:
        return [r for r in self._results if r.competitor_threat == CompetitorThreat.HIGH]

    @property
    def winnable_deals(self) -> list[CompetitivePositioningResult]:
        return [r for r in self._results if r.is_winnable]

    @property
    def dominant_positions(self) -> list[CompetitivePositioningResult]:
        return [r for r in self._results if r.positioning_strength == PositioningStrength.DOMINANT]

    @property
    def needs_escalation(self) -> list[CompetitivePositioningResult]:
        return [r for r in self._results
                if r.recommended_action == PositioningAction.EXECUTIVE_ESCALATION]

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _positioning_score(self, inp: CompetitivePositioningInput) -> float:
        score = 0.0
        # Product fit advantage
        fit_delta = inp.our_product_fit - inp.competitor_product_fit
        score += fit_delta * 0.30 + 50 * 0.10  # center at 50

        # Relationship advantage
        rel_delta = inp.our_relationship_strength - inp.competitor_relationship_strength
        score += rel_delta * 0.20

        # Price competitiveness
        score += inp.our_price_competitiveness * 0.15

        # POC advantage
        if inp.we_ran_poc and not inp.competitor_in_poc:
            score += 10
        elif not inp.we_ran_poc and inp.competitor_in_poc:
            score -= 10

        # Champion support
        if inp.champion_supports_us:
            score += 8
        if inp.economic_buyer_engaged:
            score += 7

        # Features advantage
        score += inp.our_features_advantage * 2.0  # ±10 max

        # Reference advantage
        ref_delta = inp.our_reference_count - inp.competitor_reference_count
        score += min(5.0, max(-5.0, ref_delta * 1.0))

        # Differentiators
        score += min(10.0, inp.unique_differentiators * 2.0)

        # Incumbent penalty
        if inp.competitor_incumbent:
            score -= 15

        return round(max(0.0, min(100.0, score)), 1)

    def _competitor_threat(self, inp: CompetitivePositioningInput) -> CompetitorThreat:
        threat_score = 0
        if inp.competitor_incumbent:          threat_score += 3
        if inp.competitor_in_poc:             threat_score += 2
        if inp.competitor_product_fit > 80:   threat_score += 2
        if inp.competitor_relationship_strength > 70: threat_score += 2
        if inp.competitor_reference_count > 3: threat_score += 1
        if inp.competitor_price_delta < -15:  threat_score += 1  # they're >15% cheaper

        if threat_score >= 7:   return CompetitorThreat.HIGH
        if threat_score >= 4:   return CompetitorThreat.MEDIUM
        if threat_score >= 1:   return CompetitorThreat.LOW
        return CompetitorThreat.UNKNOWN

    def _positioning_strength(
        self, score: float, inp: CompetitivePositioningInput
    ) -> PositioningStrength:
        if score >= 78: return PositioningStrength.DOMINANT
        if score >= 62: return PositioningStrength.STRONG
        if score >= 46: return PositioningStrength.COMPETITIVE
        if score >= 30: return PositioningStrength.WEAK
        return PositioningStrength.CRITICAL

    def _win_rate(self, inp: CompetitivePositioningInput) -> float:
        total = inp.prior_wins_vs_competitor + inp.prior_losses_vs_competitor
        if total == 0:
            return 0.50
        return round(inp.prior_wins_vs_competitor / total, 3)

    def _win_probability(
        self,
        pos_score: float,
        win_rate: float,
        inp: CompetitivePositioningInput,
    ) -> WinProbability:
        blended = pos_score * 0.70 + win_rate * 100 * 0.30
        if blended >= 75: return WinProbability.VERY_HIGH
        if blended >= 60: return WinProbability.HIGH
        if blended >= 45: return WinProbability.MEDIUM
        if blended >= 30: return WinProbability.LOW
        return WinProbability.VERY_LOW

    def _competitive_gap(self, inp: CompetitivePositioningInput) -> float:
        fit_gap = inp.our_product_fit - inp.competitor_product_fit
        rel_gap = inp.our_relationship_strength - inp.competitor_relationship_strength
        gap = (fit_gap * 0.60 + rel_gap * 0.40)
        return round(gap, 1)

    def _urgency_score(self, inp: CompetitivePositioningInput) -> float:
        score = 0.0
        if inp.expected_close_days <= 14:  score += 40
        elif inp.expected_close_days <= 30: score += 25
        elif inp.expected_close_days <= 60: score += 10
        if inp.competitor_in_poc:          score += 20
        if inp.competitor_incumbent:       score += 15
        if inp.deal_stage in ("negotiation", "closing"): score += 15
        elif inp.deal_stage == "proposal": score += 8
        return round(min(100.0, score), 1)

    def _recommended_action(
        self,
        inp: CompetitivePositioningInput,
        pos_score: float,
        threat: CompetitorThreat,
        win_prob: WinProbability,
    ) -> PositioningAction:
        if win_prob == WinProbability.VERY_LOW and pos_score < 30:
            return PositioningAction.ABANDON
        if threat == CompetitorThreat.HIGH and pos_score < 50:
            return PositioningAction.EXECUTIVE_ESCALATION
        if inp.competitor_in_poc and not inp.we_ran_poc:
            return PositioningAction.COMPETITIVE_RESPONSE
        if pos_score < 46:
            return PositioningAction.DEFEND
        if threat == CompetitorThreat.HIGH:
            return PositioningAction.DIFFERENTIATE
        if pos_score >= 75:
            return PositioningAction.ACCELERATE
        return PositioningAction.DIFFERENTIATE

    def _battlecard_points(
        self, inp: CompetitivePositioningInput, strength: PositioningStrength
    ) -> list[str]:
        points: list[str] = []
        fit_delta = inp.our_product_fit - inp.competitor_product_fit
        if fit_delta > 10:
            points.append(
                f"Supériorité produit claire (+{fit_delta:.0f}pts) — démontrer les cas d'usage clés"
            )
        if inp.our_price_competitiveness >= 70:
            points.append("Positionnement prix compétitif — mettre en avant le ROI total (TCO)")
        if inp.we_ran_poc and not inp.competitor_in_poc:
            points.append("Avantage POC — résultats concrets à présenter au comité")
        if inp.champion_supports_us:
            points.append("Champion interne actif — le mobiliser pour défendre la décision")
        if inp.our_reference_count > inp.competitor_reference_count:
            delta = inp.our_reference_count - inp.competitor_reference_count
            points.append(
                f"Plus de références clients ({delta} de plus) — organiser des appels de référence"
            )
        if inp.unique_differentiators >= 3:
            points.append(
                f"{inp.unique_differentiators} différenciateurs uniques démontrés — les ancrer dans la proposition de valeur"
            )
        if inp.our_relationship_strength > inp.competitor_relationship_strength + 20:
            points.append("Relation commerciale supérieure — capitaliser sur la confiance établie")
        if inp.prior_wins_vs_competitor > 2:
            points.append(
                f"Bilan favorable face à {inp.competitor_name} ({inp.prior_wins_vs_competitor}V/{inp.prior_losses_vs_competitor}D) — utiliser comme preuve sociale"
            )
        return points

    def _risk_factors(
        self,
        inp: CompetitivePositioningInput,
        threat: CompetitorThreat,
        pos_score: float,
    ) -> list[str]:
        risks: list[str] = []
        if inp.competitor_incumbent:
            risks.append(f"{inp.competitor_name} est le fournisseur actuel — coûts de migration importants")
        if inp.competitor_in_poc and not inp.we_ran_poc:
            risks.append(f"{inp.competitor_name} a une preuve de concept — risque de verrouillage technique")
        if inp.competitor_price_delta < -15:
            risks.append(
                f"Écart de prix défavorable ({abs(inp.competitor_price_delta):.0f}% moins cher) — préparer la justification du ROI"
            )
        if inp.competitor_relationship_strength > inp.our_relationship_strength + 20:
            risks.append(
                f"Relation concurrente plus forte — risque de décision basée sur la relation"
            )
        if not inp.champion_supports_us:
            risks.append("Absence de champion interne — décision moins prévisible")
        if not inp.economic_buyer_engaged:
            risks.append("Décideur budget non engagé — deal en risque de stagnation")
        if inp.prior_losses_vs_competitor > inp.prior_wins_vs_competitor:
            risks.append(
                f"Bilan négatif face à {inp.competitor_name} ({inp.prior_wins_vs_competitor}V/{inp.prior_losses_vs_competitor}D) — analyser les pertes passées"
            )
        return risks

    def _key_differentiators(self, inp: CompetitivePositioningInput) -> list[str]:
        diffs: list[str] = []
        fit_delta = inp.our_product_fit - inp.competitor_product_fit
        if fit_delta > 5:
            diffs.append(f"Adéquation produit supérieure ({inp.our_product_fit:.0f}/100 vs {inp.competitor_product_fit:.0f}/100)")
        if inp.our_price_competitiveness >= 60 and inp.competitor_price_delta > 0:
            diffs.append(f"Prix compétitif — {inp.competitor_price_delta:.0f}% plus économique sur le TCO")
        if inp.we_ran_poc:
            diffs.append("Preuve de concept réalisée avec succès")
        if inp.unique_differentiators > 0:
            diffs.append(f"{inp.unique_differentiators} fonctionnalité(s) unique(s) non disponibles chez {inp.competitor_name}")
        if inp.our_reference_count >= 3:
            diffs.append(f"{inp.our_reference_count} références clients vérifiables dans le secteur")
        return diffs

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "strength_counts": {},
                "threat_counts": {},
                "probability_counts": {},
                "action_counts": {},
                "avg_positioning_score": 0.0,
                "avg_win_rate": 0.0,
                "avg_urgency_score": 0.0,
                "high_threat_count": 0,
                "winnable_count": 0,
                "dominant_count": 0,
                "escalation_count": 0,
                "avg_competitive_gap": 0.0,
            }

        strength_counts:     dict[str, int] = {}
        threat_counts:       dict[str, int] = {}
        probability_counts:  dict[str, int] = {}
        action_counts:       dict[str, int] = {}
        total_pos = 0.0
        total_wr  = 0.0
        total_urg = 0.0
        total_gap = 0.0

        for r in self._results:
            strength_counts[r.positioning_strength.value]  = strength_counts.get(r.positioning_strength.value, 0) + 1
            threat_counts[r.competitor_threat.value]       = threat_counts.get(r.competitor_threat.value, 0) + 1
            probability_counts[r.win_probability.value]    = probability_counts.get(r.win_probability.value, 0) + 1
            action_counts[r.recommended_action.value]      = action_counts.get(r.recommended_action.value, 0) + 1
            total_pos += r.positioning_score
            total_wr  += r.win_rate_vs_competitor
            total_urg += r.urgency_score
            total_gap += r.competitive_gap

        return {
            "total":                n,
            "strength_counts":      strength_counts,
            "threat_counts":        threat_counts,
            "probability_counts":   probability_counts,
            "action_counts":        action_counts,
            "avg_positioning_score": round(total_pos / n, 1),
            "avg_win_rate":         round(total_wr / n, 3),
            "avg_urgency_score":    round(total_urg / n, 1),
            "high_threat_count":    len(self.high_threat_deals),
            "winnable_count":       len(self.winnable_deals),
            "dominant_count":       len(self.dominant_positions),
            "escalation_count":     len(self.needs_escalation),
            "avg_competitive_gap":  round(total_gap / n, 1),
        }
