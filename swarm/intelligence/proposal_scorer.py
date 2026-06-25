"""
Proposal Scorer — estimates win probability for B2B sales proposals.

Evaluates five dimensions:
  value_alignment(20%) + competitive_position(25%) + relationship_strength(20%)
  + timing_fit(15%) + proposal_quality(20%)
  → win_probability 0.0-1.0, ProposalTier: WEAK/FAIR/GOOD/STRONG
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ProposalTier(str, Enum):
    WEAK = "weak"
    FAIR = "fair"
    GOOD = "good"
    STRONG = "strong"


_TIER_THRESHOLDS = {
    ProposalTier.STRONG: 0.65,
    ProposalTier.GOOD: 0.50,
    ProposalTier.FAIR: 0.35,
}

_BASELINE_WIN_RATE = 0.20

_WEIGHTS = {
    "value_alignment": 0.20,
    "competitive_position": 0.25,
    "relationship_strength": 0.20,
    "timing_fit": 0.15,
    "proposal_quality": 0.20,
}

_RECOMMENDATIONS: Dict[str, str] = {
    "budget_mismatch": "Revoir le prix — écart important avec le budget déclaré du client",
    "no_roi_quantified": "Quantifier le ROI attendu avec des chiffres concrets",
    "weak_competitive": "Renforcer la différenciation face aux concurrents identifiés",
    "no_references": "Ajouter des références sectorielles pertinentes",
    "low_relationship": "Intensifier le contact avec les décideurs avant soumission",
    "poor_timing": "Reconsidérer le calendrier — période défavorable détectée",
    "no_personalization": "Personnaliser davantage la proposition (nom, enjeux spécifiques)",
    "missing_case_study": "Inclure une étude de cas similaire au secteur client",
    "deadline_pressure": "Clarifier les délais — pression temporelle risque de dévaloriser l'offre",
    "single_contact": "Élargir à plusieurs interlocuteurs (comité d'achat probable)",
}


@dataclass
class ProposalSignals:
    proposal_id: str
    client_name: str
    sector: str
    deal_value_eur: float
    client_budget_eur: float          # 0 if unknown
    competitor_count: int             # number of known competitors
    has_incumbent: bool               # client already has a vendor
    meetings_held: int                # meetings with client before proposal
    decision_maker_reached: bool
    days_to_deadline: int
    has_roi_model: bool               # proposal includes quantified ROI
    has_case_study: bool
    has_personalization: bool         # proposal references client-specific context
    relationship_score: float         # 0-100 (CRM relationship health)
    previous_deals_won: int           # number of previous won deals with this client
    proposal_page_count: int          # proxy for proposal completeness (optimal: 10-20)
    our_price_vs_market: float        # ratio: 1.0=at market, <1.0=cheaper, >1.0=premium

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScoredProposal:
    proposal: ProposalSignals
    win_probability: float
    proposal_tier: ProposalTier
    dimension_scores: Dict[str, float]
    recommendations: List[str]
    strengths: List[str]

    def to_dict(self) -> dict:
        return {
            "proposal": self.proposal.to_dict(),
            "win_probability": self.win_probability,
            "proposal_tier": self.proposal_tier.value,
            "dimension_scores": self.dimension_scores,
            "recommendations": self.recommendations,
            "strengths": self.strengths,
        }


# ─── Dimension scorers ────────────────────────────────────────────────────────

def _value_alignment(p: ProposalSignals) -> Tuple[float, List[str], List[str]]:
    tips: List[str] = []
    strengths: List[str] = []

    if p.client_budget_eur <= 0:
        score = 60.0
    else:
        ratio = p.deal_value_eur / p.client_budget_eur
        if ratio <= 0.80:
            score = 100.0
            strengths.append("Proposition sous le budget client")
        elif ratio <= 1.10:
            score = 85.0
        elif ratio <= 1.30:
            score = 60.0
            tips.append("budget_mismatch")
        else:
            score = max(0.0, 100.0 - (ratio - 1.0) * 80.0)
            tips.append("budget_mismatch")

    if not p.has_roi_model:
        score = max(0.0, score - 15.0)
        tips.append("no_roi_quantified")
    else:
        strengths.append("ROI quantifié inclus")

    return score, tips, strengths


def _competitive_position(p: ProposalSignals) -> Tuple[float, List[str], List[str]]:
    tips: List[str] = []
    strengths: List[str] = []

    base = 100.0 - p.competitor_count * 15.0
    if p.has_incumbent:
        base -= 20.0
    base = max(0.0, base)

    price_ratio = p.our_price_vs_market
    if price_ratio <= 0.90:
        base = min(100.0, base + 15.0)
        strengths.append("Prix compétitif vs marché")
    elif price_ratio >= 1.30:
        base = max(0.0, base - 20.0)
        tips.append("weak_competitive")

    if not p.has_case_study:
        tips.append("no_references")
        base = max(0.0, base - 10.0)
    else:
        strengths.append("Étude de cas incluse")

    if p.previous_deals_won > 0:
        base = min(100.0, base + p.previous_deals_won * 10.0)
        strengths.append(f"{p.previous_deals_won} deal(s) précédent(s) remporté(s)")

    return max(0.0, base), tips, strengths


def _relationship_strength(p: ProposalSignals) -> Tuple[float, List[str], List[str]]:
    tips: List[str] = []
    strengths: List[str] = []

    score = p.relationship_score
    if not p.decision_maker_reached:
        score = max(0.0, score - 25.0)
        tips.append("low_relationship")
    else:
        strengths.append("Décideur contacté")

    meetings_bonus = min(30.0, p.meetings_held * 7.5)
    score = min(100.0, score + meetings_bonus)

    if p.meetings_held >= 3:
        strengths.append(f"{p.meetings_held} réunions tenues")
    elif p.meetings_held == 0:
        tips.append("single_contact")

    return score, tips, strengths


def _timing_fit(p: ProposalSignals) -> Tuple[float, List[str], List[str]]:
    tips: List[str] = []
    strengths: List[str] = []

    days = p.days_to_deadline
    if days <= 0:
        return 0.0, ["deadline_pressure"], []
    if days <= 7:
        score = 30.0
        tips.append("deadline_pressure")
    elif days <= 14:
        score = 60.0
    elif days <= 30:
        score = 90.0
        strengths.append("Délai favorable pour préparer la réponse")
    elif days <= 60:
        score = 100.0
        strengths.append("Timing excellent")
    else:
        score = max(60.0, 100.0 - (days - 60) * 0.5)

    if p.has_incumbent and days <= 14:
        score = max(0.0, score - 15.0)
        tips.append("poor_timing")

    return score, tips, strengths


def _proposal_quality(p: ProposalSignals) -> Tuple[float, List[str], List[str]]:
    tips: List[str] = []
    strengths: List[str] = []

    pages = p.proposal_page_count
    if pages < 5:
        page_score = 40.0
    elif pages <= 20:
        page_score = 100.0
        strengths.append("Longueur de proposition optimale")
    elif pages <= 40:
        page_score = 75.0
    else:
        page_score = max(40.0, 75.0 - (pages - 40) * 1.5)

    pers_score = 100.0 if p.has_personalization else 50.0
    if not p.has_personalization:
        tips.append("no_personalization")
    else:
        strengths.append("Proposition personnalisée")

    cs_score = 100.0 if p.has_case_study else 60.0
    if not p.has_case_study:
        tips.append("missing_case_study")

    score = (page_score * 0.3 + pers_score * 0.4 + cs_score * 0.3)
    return score, tips, strengths


def _compute_win_probability(dimension_scores: Dict[str, float]) -> float:
    composite = sum(dimension_scores[k] * w for k, w in _WEIGHTS.items())
    prob = _BASELINE_WIN_RATE + (composite / 100.0) * 0.60
    return round(max(0.0, min(1.0, prob)), 4)


def _classify_tier(prob: float) -> ProposalTier:
    if prob >= _TIER_THRESHOLDS[ProposalTier.STRONG]:
        return ProposalTier.STRONG
    if prob >= _TIER_THRESHOLDS[ProposalTier.GOOD]:
        return ProposalTier.GOOD
    if prob >= _TIER_THRESHOLDS[ProposalTier.FAIR]:
        return ProposalTier.FAIR
    return ProposalTier.WEAK


def _score_proposal(p: ProposalSignals) -> ScoredProposal:
    va_score, va_tips, va_str = _value_alignment(p)
    cp_score, cp_tips, cp_str = _competitive_position(p)
    rs_score, rs_tips, rs_str = _relationship_strength(p)
    tf_score, tf_tips, tf_str = _timing_fit(p)
    pq_score, pq_tips, pq_str = _proposal_quality(p)

    dimension_scores = {
        "value_alignment": round(va_score, 2),
        "competitive_position": round(cp_score, 2),
        "relationship_strength": round(rs_score, 2),
        "timing_fit": round(tf_score, 2),
        "proposal_quality": round(pq_score, 2),
    }

    all_tip_keys: List[str] = va_tips + cp_tips + rs_tips + tf_tips + pq_tips
    seen: set = set()
    deduped_tips = [k for k in all_tip_keys if not (k in seen or seen.add(k))]  # type: ignore[func-returns-value]
    recommendations = [_RECOMMENDATIONS[k] for k in deduped_tips if k in _RECOMMENDATIONS]

    all_strengths = va_str + cp_str + rs_str + tf_str + pq_str

    prob = _compute_win_probability(dimension_scores)
    tier = _classify_tier(prob)

    return ScoredProposal(
        proposal=p,
        win_probability=prob,
        proposal_tier=tier,
        dimension_scores=dimension_scores,
        recommendations=recommendations,
        strengths=all_strengths,
    )


class ProposalScorer:
    def __init__(self) -> None:
        self._store: Dict[str, ScoredProposal] = {}

    def score(self, proposal: ProposalSignals) -> ScoredProposal:
        result = _score_proposal(proposal)
        self._store[proposal.proposal_id] = result
        return result

    def score_batch(self, proposals: List[ProposalSignals]) -> List[ScoredProposal]:
        return [self.score(p) for p in proposals]

    def get(self, proposal_id: str) -> Optional[ScoredProposal]:
        return self._store.get(proposal_id)

    def all_scored(self) -> List[ScoredProposal]:
        return sorted(self._store.values(), key=lambda s: s.win_probability, reverse=True)

    def top_prospects(self, n: int = 5) -> List[ScoredProposal]:
        return self.all_scored()[:n]

    def by_tier(self, tier: ProposalTier) -> List[ScoredProposal]:
        return [s for s in self._store.values() if s.proposal_tier == tier]

    def at_risk(self) -> List[ScoredProposal]:
        return [s for s in self._store.values() if s.proposal_tier == ProposalTier.WEAK]

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "tier_counts": {t.value: 0 for t in ProposalTier},
                "avg_win_probability": 0.0,
                "best_win_probability": 0.0,
                "total_pipeline_eur": 0.0,
                "expected_won_eur": 0.0,
            }
        tier_counts = {t.value: 0 for t in ProposalTier}
        for s in items:
            tier_counts[s.proposal_tier.value] += 1
        avg_prob = sum(s.win_probability for s in items) / count
        best_prob = max(s.win_probability for s in items)
        total_pipeline = sum(s.proposal.deal_value_eur for s in items)
        expected_won = sum(s.proposal.deal_value_eur * s.win_probability for s in items)
        return {
            "total": count,
            "tier_counts": tier_counts,
            "avg_win_probability": round(avg_prob, 4),
            "best_win_probability": round(best_prob, 4),
            "total_pipeline_eur": round(total_pipeline, 2),
            "expected_won_eur": round(expected_won, 2),
        }

    def reset(self) -> None:
        self._store.clear()
