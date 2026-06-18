"""
Sales Coach Agent — generates personalized coaching recommendations for sales reps.

Scoring dimensions:
  pipeline_health(30%) + activity_score(25%) + skill_gaps(25%) + win_rate_trend(20%)
  → coaching_priority: URGENT / HIGH / MEDIUM / LOW
  → CoachingFocus: PROSPECTING / QUALIFICATION / PRESENTATION / NEGOTIATION / CLOSING / RETENTION
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class CoachingPriority(str, Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CoachingFocus(str, Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PRESENTATION = "presentation"
    NEGOTIATION = "negotiation"
    CLOSING = "closing"
    RETENTION = "retention"


class SkillArea(str, Enum):
    DISCOVERY = "discovery"
    OBJECTION_HANDLING = "objection_handling"
    DEMO = "demo"
    PRICING = "pricing"
    FOLLOW_UP = "follow_up"
    RELATIONSHIP = "relationship"
    TIME_MANAGEMENT = "time_management"


_COACHING_TIPS: Dict[str, str] = {
    "increase_prospecting": "Augmenter le volume de prospection — pipeline insuffisant pour atteindre les objectifs",
    "qualify_harder": "Renforcer la qualification BANT avant d'investir du temps sur un deal",
    "follow_up_faster": "Réduire le délai de relance — les deals stagnent trop longtemps sans activité",
    "improve_demo": "Personnaliser davantage les démonstrations aux cas d'usage client",
    "handle_objections": "Préparer des réponses structurées aux objections récurrentes (prix, timing, concurrent)",
    "close_earlier": "Tester des techniques de closing plus tôt dans le cycle de vente",
    "protect_margin": "Résister aux demandes de remise — pratiquer la vente par la valeur",
    "multi_thread": "Multiplier les contacts dans le compte — éviter le single-threaded selling",
    "shorten_cycle": "Identifier les blocages qui allongent le cycle et y adresser un plan d'action",
    "upsell_existing": "Activer les opportunités d'upsell sur la base installée existante",
    "weekly_review": "Effectuer une revue hebdomadaire du pipeline avec le manager pour débloquer les deals",
    "use_crm": "Améliorer la discipline de mise à jour CRM pour une meilleure visibilité pipeline",
}

_SKILL_TIPS: Dict[SkillArea, str] = {
    SkillArea.DISCOVERY: "Approfondir la phase de découverte — poser plus de questions ouvertes sur les enjeux business",
    SkillArea.OBJECTION_HANDLING: "Travailler les réponses aux objections prix et concurrentielles avec des role-plays",
    SkillArea.DEMO: "Structurer les démonstrations autour des pain points identifiés, pas des fonctionnalités",
    SkillArea.PRICING: "Maîtriser la justification de valeur avant de présenter le prix",
    SkillArea.FOLLOW_UP: "Mettre en place des séquences de relance multicanal (email + LinkedIn + téléphone)",
    SkillArea.RELATIONSHIP: "Investir dans la relation au-delà du deal — déjeuners, événements, contenus utiles",
    SkillArea.TIME_MANAGEMENT: "Prioriser les deals à fort potentiel et déléguer ou abandonner les deals froids",
}


@dataclass
class RepPerformance:
    rep_id: str
    rep_name: str
    manager_id: str
    territory: str
    # Pipeline metrics
    open_deals: int
    pipeline_value_eur: float
    quota_eur: float
    pipeline_coverage_ratio: float   # pipeline / quota (e.g., 3.0 = 3x coverage)
    # Activity metrics
    calls_last_30d: int
    emails_last_30d: int
    meetings_last_30d: int
    demos_last_30d: int
    # Outcome metrics
    win_rate_last_90d: float          # 0-100
    win_rate_prev_90d: float          # 0-100 (previous period)
    avg_deal_size_eur: float
    avg_sales_cycle_days: int
    # Skill self-assessment / manager scores (0-100)
    discovery_score: float
    objection_score: float
    demo_score: float
    pricing_score: float
    follow_up_score: float
    relationship_score: float
    time_mgmt_score: float
    # Recent outcomes
    deals_won_last_90d: int
    deals_lost_last_90d: int
    deals_stalled_last_30d: int       # deals with no activity >14 days

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CoachingPlan:
    rep: RepPerformance
    coaching_priority: CoachingPriority
    primary_focus: CoachingFocus
    coaching_score: float              # 0-100 (higher = needs more coaching)
    pipeline_health_score: float
    activity_score: float
    skill_gap_score: float             # lower = more gaps
    win_rate_trend_score: float
    top_recommendations: List[str]
    skill_development: List[str]
    kpis_to_watch: List[str]
    estimated_quota_attainment_pct: float

    def to_dict(self) -> dict:
        return {
            "rep": self.rep.to_dict(),
            "coaching_priority": self.coaching_priority.value,
            "primary_focus": self.primary_focus.value,
            "coaching_score": self.coaching_score,
            "pipeline_health_score": self.pipeline_health_score,
            "activity_score": self.activity_score,
            "skill_gap_score": self.skill_gap_score,
            "win_rate_trend_score": self.win_rate_trend_score,
            "top_recommendations": self.top_recommendations,
            "skill_development": self.skill_development,
            "kpis_to_watch": self.kpis_to_watch,
            "estimated_quota_attainment_pct": self.estimated_quota_attainment_pct,
        }


# ─── Dimension scorers ────────────────────────────────────────────────────────

def _pipeline_health(r: RepPerformance) -> Tuple[float, List[str]]:
    tips: List[str] = []

    coverage = r.pipeline_coverage_ratio
    if coverage >= 4.0:
        cov_score = 100.0
    elif coverage >= 3.0:
        cov_score = 85.0
    elif coverage >= 2.0:
        cov_score = 65.0
    elif coverage >= 1.0:
        cov_score = 40.0
    else:
        cov_score = max(0.0, coverage * 40.0)

    if coverage < 2.0:
        tips.append("increase_prospecting")

    stall_pct = (r.deals_stalled_last_30d / r.open_deals * 100.0) if r.open_deals > 0 else 0.0
    stall_score = max(0.0, 100.0 - stall_pct * 2.0)
    if stall_pct > 30.0:
        tips.append("follow_up_faster")
        tips.append("weekly_review")

    quota_attain = (r.pipeline_value_eur / r.quota_eur * 100.0) if r.quota_eur > 0 else 0.0
    quota_score = min(100.0, quota_attain / 3.0)   # 300% coverage = 100 pts

    score = cov_score * 0.40 + stall_score * 0.35 + quota_score * 0.25
    return round(score, 2), tips


def _activity_score(r: RepPerformance) -> Tuple[float, List[str]]:
    tips: List[str] = []

    # Benchmark: 60 calls, 120 emails, 15 meetings, 8 demos per 30 days
    call_score = min(100.0, r.calls_last_30d / 60.0 * 100.0)
    email_score = min(100.0, r.emails_last_30d / 120.0 * 100.0)
    meeting_score = min(100.0, r.meetings_last_30d / 15.0 * 100.0)
    demo_score = min(100.0, r.demos_last_30d / 8.0 * 100.0)

    if r.demos_last_30d < 3:
        tips.append("improve_demo")
    if r.calls_last_30d + r.emails_last_30d < 50:
        tips.append("use_crm")

    score = call_score * 0.25 + email_score * 0.25 + meeting_score * 0.25 + demo_score * 0.25
    return round(score, 2), tips


def _skill_gaps(r: RepPerformance) -> Tuple[float, List[str]]:
    skill_map = {
        SkillArea.DISCOVERY: r.discovery_score,
        SkillArea.OBJECTION_HANDLING: r.objection_score,
        SkillArea.DEMO: r.demo_score,
        SkillArea.PRICING: r.pricing_score,
        SkillArea.FOLLOW_UP: r.follow_up_score,
        SkillArea.RELATIONSHIP: r.relationship_score,
        SkillArea.TIME_MANAGEMENT: r.time_mgmt_score,
    }

    skill_scores = list(skill_map.values())
    avg_skill = sum(skill_scores) / len(skill_scores)

    # Identify weak skills (below 60)
    weak_skills = [area for area, score in skill_map.items() if score < 60.0]
    skill_tips = [_SKILL_TIPS[area] for area in weak_skills]

    return round(avg_skill, 2), skill_tips


def _win_rate_trend(r: RepPerformance) -> Tuple[float, List[str]]:
    tips: List[str] = []

    current = r.win_rate_last_90d
    previous = r.win_rate_prev_90d

    rate_score = min(100.0, current * 1.5)  # 66% win rate = 100 pts

    trend = current - previous
    if trend >= 5.0:
        trend_bonus = 15.0
    elif trend >= 0.0:
        trend_bonus = 5.0
    elif trend >= -5.0:
        trend_bonus = -5.0
    else:
        trend_bonus = -15.0
        tips.append("qualify_harder")
        tips.append("handle_objections")

    if current < 20.0:
        tips.append("close_earlier")

    score = min(100.0, max(0.0, rate_score + trend_bonus))
    return round(score, 2), tips


def _determine_focus(r: RepPerformance, pipeline_health: float, win_rate: float) -> CoachingFocus:
    if r.pipeline_coverage_ratio < 1.5:
        return CoachingFocus.PROSPECTING
    if r.win_rate_last_90d < 15.0:
        return CoachingFocus.QUALIFICATION
    if r.demos_last_30d < 2:
        return CoachingFocus.PRESENTATION
    if r.avg_sales_cycle_days > 120:
        return CoachingFocus.NEGOTIATION
    if r.deals_stalled_last_30d > r.open_deals * 0.40:
        return CoachingFocus.CLOSING
    if r.deals_lost_last_90d > r.deals_won_last_90d * 2:
        return CoachingFocus.QUALIFICATION
    return CoachingFocus.RETENTION


def _coaching_priority(coaching_score: float) -> CoachingPriority:
    if coaching_score >= 75:
        return CoachingPriority.URGENT
    if coaching_score >= 55:
        return CoachingPriority.HIGH
    if coaching_score >= 35:
        return CoachingPriority.MEDIUM
    return CoachingPriority.LOW


def _estimated_quota_attainment(r: RepPerformance, win_rate: float, pipeline_health: float) -> float:
    if r.quota_eur <= 0:
        return 0.0
    effective_pipeline = r.pipeline_value_eur * (win_rate / 100.0)
    attainment = (effective_pipeline / r.quota_eur) * 100.0
    # Adjust by pipeline health signal
    health_factor = 0.80 + (pipeline_health / 100.0) * 0.40  # 0.80-1.20
    return round(min(200.0, attainment * health_factor), 2)


def _kpis_to_watch(r: RepPerformance, focus: CoachingFocus) -> List[str]:
    base = ["Taux de conversion pipeline → deal gagné", "Durée moyenne du cycle de vente"]
    focus_kpis = {
        CoachingFocus.PROSPECTING: ["Nombre de nouveaux prospects contactés/semaine", "Taux de réponse cold outreach"],
        CoachingFocus.QUALIFICATION: ["Score BANT moyen des deals qualifiés", "Taux de deals disqualifiés en early stage"],
        CoachingFocus.PRESENTATION: ["Taux de conversion demo → proposition", "Score de satisfaction demo (feedback client)"],
        CoachingFocus.NEGOTIATION: ["Taux de remise moyen accordé", "Nombre de cycles de négociation par deal"],
        CoachingFocus.CLOSING: ["Taux de closing en fin de trimestre", "Délai entre proposition et signature"],
        CoachingFocus.RETENTION: ["Taux de renouvellement contrats", "Net Revenue Retention (NRR) du portefeuille"],
    }
    return base + focus_kpis.get(focus, [])


def _coach_rep(r: RepPerformance) -> CoachingPlan:
    pipeline_score, pipeline_tips = _pipeline_health(r)
    activity, activity_tips = _activity_score(r)
    skill_avg, skill_development = _skill_gaps(r)
    win_trend, win_tips = _win_rate_trend(r)

    # Invert skill avg to get gap score (lower skill = higher gap = more coaching needed)
    skill_gap_score = 100.0 - skill_avg

    # Composite: higher = needs more coaching
    coaching_score = round(
        (100.0 - pipeline_score) * 0.30
        + (100.0 - activity) * 0.25
        + skill_gap_score * 0.25
        + (100.0 - win_trend) * 0.20,
        2,
    )

    focus = _determine_focus(r, pipeline_score, r.win_rate_last_90d)
    priority = _coaching_priority(coaching_score)

    # Collect all coaching tips (deduped)
    all_tip_keys = pipeline_tips + activity_tips + win_tips
    seen: set = set()
    unique_tips = [t for t in all_tip_keys if not (t in seen or seen.add(t))]  # type: ignore[func-returns-value]
    recommendations = [_COACHING_TIPS[k] for k in unique_tips if k in _COACHING_TIPS]

    attainment = _estimated_quota_attainment(r, r.win_rate_last_90d, pipeline_score)
    kpis = _kpis_to_watch(r, focus)

    return CoachingPlan(
        rep=r,
        coaching_priority=priority,
        primary_focus=focus,
        coaching_score=coaching_score,
        pipeline_health_score=pipeline_score,
        activity_score=activity,
        skill_gap_score=skill_gap_score,
        win_rate_trend_score=win_trend,
        top_recommendations=recommendations,
        skill_development=skill_development,
        kpis_to_watch=kpis,
        estimated_quota_attainment_pct=attainment,
    )


class SalesCoachAgent:
    def __init__(self) -> None:
        self._store: Dict[str, CoachingPlan] = {}

    def coach(self, rep: RepPerformance) -> CoachingPlan:
        plan = _coach_rep(rep)
        self._store[rep.rep_id] = plan
        return plan

    def coach_batch(self, reps: List[RepPerformance]) -> List[CoachingPlan]:
        return [self.coach(r) for r in reps]

    def get(self, rep_id: str) -> Optional[CoachingPlan]:
        return self._store.get(rep_id)

    def all_plans(self) -> List[CoachingPlan]:
        return sorted(self._store.values(), key=lambda p: p.coaching_score, reverse=True)

    def urgent_reps(self) -> List[CoachingPlan]:
        return [p for p in self._store.values() if p.coaching_priority == CoachingPriority.URGENT]

    def by_priority(self, priority: CoachingPriority) -> List[CoachingPlan]:
        return [p for p in self._store.values() if p.coaching_priority == priority]

    def by_focus(self, focus: CoachingFocus) -> List[CoachingPlan]:
        return [p for p in self._store.values() if p.primary_focus == focus]

    def by_manager(self, manager_id: str) -> List[CoachingPlan]:
        return [p for p in self._store.values() if p.rep.manager_id == manager_id]

    def top_coaching_needs(self, n: int = 5) -> List[CoachingPlan]:
        return self.all_plans()[:n]

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total_reps": 0,
                "priority_counts": {p.value: 0 for p in CoachingPriority},
                "focus_counts": {f.value: 0 for f in CoachingFocus},
                "avg_coaching_score": 0.0,
                "avg_quota_attainment_pct": 0.0,
                "urgent_count": 0,
            }
        priority_counts = {p.value: 0 for p in CoachingPriority}
        focus_counts = {f.value: 0 for f in CoachingFocus}
        for p in items:
            priority_counts[p.coaching_priority.value] += 1
            focus_counts[p.primary_focus.value] += 1
        avg_score = sum(p.coaching_score for p in items) / count
        avg_attain = sum(p.estimated_quota_attainment_pct for p in items) / count
        return {
            "total_reps": count,
            "priority_counts": priority_counts,
            "focus_counts": focus_counts,
            "avg_coaching_score": round(avg_score, 2),
            "avg_quota_attainment_pct": round(avg_attain, 2),
            "urgent_count": priority_counts[CoachingPriority.URGENT.value],
        }

    def reset(self) -> None:
        self._store.clear()
