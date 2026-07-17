"""
Campaign ROI Calculator — evaluates marketing campaign performance and ROI.

Composite scoring:
  roi_score(35%) + reach_efficiency(25%) + conversion_quality(25%) + cost_efficiency(15%)
  → CampaignStatus: EXCELLENT / GOOD / AVERAGE / POOR / FAILING
  → ChannelType: EMAIL / LINKEDIN / WEBINAR / CONTENT / PAID / OUTBOUND / EVENT
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class CampaignStatus(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    FAILING = "failing"


class ChannelType(str, Enum):
    EMAIL = "email"
    LINKEDIN = "linkedin"
    WEBINAR = "webinar"
    CONTENT = "content"
    PAID = "paid"
    OUTBOUND = "outbound"
    EVENT = "event"


# Industry benchmark ROI by channel (multiplier, e.g., 3.0 = 300% ROI)
_CHANNEL_BENCHMARKS: Dict[ChannelType, float] = {
    ChannelType.EMAIL: 4.2,
    ChannelType.LINKEDIN: 2.8,
    ChannelType.WEBINAR: 3.5,
    ChannelType.CONTENT: 2.0,
    ChannelType.PAID: 2.5,
    ChannelType.OUTBOUND: 3.0,
    ChannelType.EVENT: 1.8,
}

_INSIGHTS: Dict[str, str] = {
    "excellent_roi": "ROI exceptionnel — bien au-dessus du benchmark sectoriel",
    "good_roi": "ROI solide — au-dessus du benchmark sectoriel",
    "below_benchmark": "ROI sous le benchmark — optimisation nécessaire",
    "high_cpl": "Coût par lead élevé — revoir le ciblage ou le message",
    "low_open_rate": "Taux d'ouverture faible — tester de nouveaux objets/senders",
    "low_click_rate": "Taux de clic faible — améliorer le CTA et le contenu",
    "low_conversion": "Taux de conversion lead → opportunité faible — qualifier le ciblage",
    "strong_conversion": "Excellent taux de conversion — ciblage très pertinent",
    "high_unsubscribe": "Taux de désabonnement élevé — revoir la pression et pertinence",
    "wide_reach": "Très bonne portée — campagne scalable",
    "low_reach": "Portée limitée — envisager des canaux complémentaires",
    "strong_engagement": "Engagement très élevé — contenu très pertinent pour la cible",
    "budget_efficient": "Très bonne efficacité budgétaire",
    "budget_inefficient": "Budget mal alloué — redistributer vers les canaux performants",
    "pipeline_generated": "Pipeline significatif généré — bon alignement marketing/ventes",
    "no_pipeline": "Aucun pipeline généré — revoir l'alignement avec les ventes",
}

_RECOMMENDATIONS: Dict[str, str] = {
    "scale_immediately": "Augmenter le budget et la fréquence — fort potentiel ROI",
    "optimize_targeting": "Affiner le ciblage ICP pour améliorer la conversion",
    "ab_test_content": "Lancer des A/B tests sur le contenu et les CTA",
    "reduce_frequency": "Réduire la fréquence d'envoi pour limiter les désabonnements",
    "improve_landing": "Optimiser les landing pages pour améliorer la conversion",
    "add_nurture_sequence": "Ajouter une séquence de nurture pour les leads froids",
    "align_sales": "Renforcer l'alignement marketing-ventes sur le suivi des leads",
    "cut_budget": "Réduire le budget — ROI insuffisant pour justifier l'investissement",
    "pause_campaign": "Mettre la campagne en pause et retravailler la stratégie",
    "repurpose_content": "Réutiliser le contenu performant sur d'autres canaux",
    "increase_personalization": "Augmenter la personnalisation des messages",
    "retarget_engaged": "Lancer une campagne de retargeting sur les contacts engagés",
}


@dataclass
class CampaignMetrics:
    campaign_id: str
    campaign_name: str
    channel: ChannelType
    start_date: str                  # ISO date string
    duration_days: int
    budget_eur: float
    total_spent_eur: float
    # Reach metrics
    total_contacts: int
    emails_sent: int
    opens: int
    clicks: int
    unsubscribes: int
    # Conversion metrics
    leads_generated: int
    mqls: int                        # Marketing Qualified Leads
    sqls: int                        # Sales Qualified Leads
    opportunities_created: int
    deals_won: int
    # Value metrics
    pipeline_value_eur: float
    closed_revenue_eur: float
    avg_deal_size_eur: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CampaignResult:
    campaign: CampaignMetrics
    roi_pct: float                   # (revenue - cost) / cost * 100
    roi_score: float                 # 0-100 normalized
    reach_efficiency: float          # 0-100
    conversion_quality: float        # 0-100
    cost_efficiency: float           # 0-100
    overall_score: float             # composite 0-100
    status: CampaignStatus
    cost_per_lead_eur: float
    cost_per_sql_eur: float
    cost_per_deal_eur: float
    open_rate_pct: float
    click_rate_pct: float
    lead_to_opp_rate_pct: float
    opp_to_won_rate_pct: float
    key_insights: List[str]
    recommendations: List[str]
    benchmark_vs_channel: float      # ratio vs channel benchmark (1.0 = at benchmark)

    def to_dict(self) -> dict:
        return {
            "campaign": self.campaign.to_dict(),
            "roi_pct": self.roi_pct,
            "roi_score": self.roi_score,
            "reach_efficiency": self.reach_efficiency,
            "conversion_quality": self.conversion_quality,
            "cost_efficiency": self.cost_efficiency,
            "overall_score": self.overall_score,
            "status": self.status.value,
            "cost_per_lead_eur": self.cost_per_lead_eur,
            "cost_per_sql_eur": self.cost_per_sql_eur,
            "cost_per_deal_eur": self.cost_per_deal_eur,
            "open_rate_pct": self.open_rate_pct,
            "click_rate_pct": self.click_rate_pct,
            "lead_to_opp_rate_pct": self.lead_to_opp_rate_pct,
            "opp_to_won_rate_pct": self.opp_to_won_rate_pct,
            "key_insights": self.key_insights,
            "recommendations": self.recommendations,
            "benchmark_vs_channel": self.benchmark_vs_channel,
        }


# ─── Dimension scorers ────────────────────────────────────────────────────────

def _roi_score(m: CampaignMetrics) -> Tuple[float, float, float, List[str]]:
    cost = m.total_spent_eur if m.total_spent_eur > 0 else m.budget_eur
    revenue = m.closed_revenue_eur

    if cost <= 0:
        return 0.0, 0.0, 1.0, []

    roi_pct = (revenue - cost) / cost * 100.0
    benchmark_mult = _CHANNEL_BENCHMARKS.get(m.channel, 2.5)
    benchmark_roi_pct = (benchmark_mult - 1.0) * 100.0

    # Normalize: benchmark = 60 pts, 2x benchmark = 100 pts, 0 = 0 pts
    if roi_pct <= 0:
        score = max(0.0, 30.0 + roi_pct * 0.1)  # lose points below 0
    elif roi_pct <= benchmark_roi_pct:
        score = 30.0 + (roi_pct / benchmark_roi_pct) * 30.0
    else:
        ratio = roi_pct / benchmark_roi_pct
        score = min(100.0, 60.0 + (ratio - 1.0) * 40.0)

    insights: List[str] = []
    if roi_pct >= benchmark_roi_pct * 1.5:
        insights.append("excellent_roi")
    elif roi_pct >= benchmark_roi_pct:
        insights.append("good_roi")
    else:
        insights.append("below_benchmark")

    benchmark_vs = roi_pct / benchmark_roi_pct if benchmark_roi_pct > 0 else 0.0
    return round(score, 2), round(roi_pct, 2), round(benchmark_vs, 3), insights


def _reach_efficiency(m: CampaignMetrics) -> Tuple[float, List[str]]:
    insights: List[str] = []

    if m.emails_sent <= 0:
        return 0.0, insights

    open_rate = m.opens / m.emails_sent * 100.0
    click_rate = m.clicks / m.emails_sent * 100.0
    unsub_rate = m.unsubscribes / m.emails_sent * 100.0

    # Industry benchmarks: open 25%, click 3%, unsub <0.5%
    open_score = min(100.0, open_rate / 25.0 * 100.0)
    click_score = min(100.0, click_rate / 3.0 * 100.0)
    unsub_penalty = max(0.0, min(30.0, (unsub_rate - 0.5) * 20.0)) if unsub_rate > 0.5 else 0.0

    if open_rate < 15.0:
        insights.append("low_open_rate")
    if click_rate < 1.5:
        insights.append("low_click_rate")
    if open_rate > 35.0 and click_rate > 5.0:
        insights.append("strong_engagement")
    if unsub_rate > 1.0:
        insights.append("high_unsubscribe")

    contact_reach = min(100.0, m.total_contacts / 500.0 * 100.0)
    if m.total_contacts >= 1000:
        insights.append("wide_reach")
    elif m.total_contacts < 100:
        insights.append("low_reach")

    score = open_score * 0.35 + click_score * 0.35 + contact_reach * 0.30 - unsub_penalty
    return round(max(0.0, score), 2), insights


def _conversion_quality(m: CampaignMetrics) -> Tuple[float, List[str]]:
    insights: List[str] = []

    lead_to_opp_rate = (m.opportunities_created / m.leads_generated * 100.0) if m.leads_generated > 0 else 0.0
    opp_to_won_rate = (m.deals_won / m.opportunities_created * 100.0) if m.opportunities_created > 0 else 0.0

    # Benchmarks: lead→opp 15%, opp→won 25%
    lead_opp_score = min(100.0, lead_to_opp_rate / 15.0 * 100.0)
    opp_won_score = min(100.0, opp_to_won_rate / 25.0 * 100.0)

    # MQL/SQL funnel health
    mql_rate = (m.mqls / m.leads_generated * 100.0) if m.leads_generated > 0 else 0.0
    sql_rate = (m.sqls / m.mqls * 100.0) if m.mqls > 0 else 0.0
    funnel_score = min(100.0, (mql_rate / 40.0 * 50.0) + (sql_rate / 50.0 * 50.0))

    if lead_to_opp_rate < 8.0:
        insights.append("low_conversion")
    elif lead_to_opp_rate >= 20.0:
        insights.append("strong_conversion")

    if m.opportunities_created > 0:
        insights.append("pipeline_generated")
    elif m.leads_generated > 0:
        insights.append("no_pipeline")

    score = lead_opp_score * 0.40 + opp_won_score * 0.35 + funnel_score * 0.25
    return round(score, 2), insights, round(lead_to_opp_rate, 2), round(opp_to_won_rate, 2)


def _cost_efficiency(m: CampaignMetrics) -> Tuple[float, List[str], float, float, float]:
    insights: List[str] = []
    cost = m.total_spent_eur if m.total_spent_eur > 0 else m.budget_eur

    cpl = cost / m.leads_generated if m.leads_generated > 0 else float("inf")
    csql = cost / m.sqls if m.sqls > 0 else float("inf")
    cpd = cost / m.deals_won if m.deals_won > 0 else float("inf")

    # Benchmarks: CPL 150€, CSQL 500€, CPD 5000€
    cpl_score = min(100.0, 150.0 / cpl * 100.0) if cpl > 0 and cpl != float("inf") else 0.0
    csql_score = min(100.0, 500.0 / csql * 100.0) if csql > 0 and csql != float("inf") else 0.0
    cpd_score = min(100.0, 5000.0 / cpd * 100.0) if cpd > 0 and cpd != float("inf") else 0.0

    # Budget utilization: ideally close to 100%
    budget_util = (m.total_spent_eur / m.budget_eur * 100.0) if m.budget_eur > 0 else 100.0
    util_score = 100.0 - abs(100.0 - budget_util) * 0.5

    if cpl != float("inf") and cpl > 300:
        insights.append("high_cpl")

    avg_cost_score = (cpl_score + csql_score + cpd_score) / 3.0
    if avg_cost_score >= 70:
        insights.append("budget_efficient")
    elif avg_cost_score < 30:
        insights.append("budget_inefficient")

    score = cpl_score * 0.35 + csql_score * 0.35 + cpd_score * 0.20 + util_score * 0.10
    cpl_out = round(cpl, 2) if cpl != float("inf") else -1.0
    csql_out = round(csql, 2) if csql != float("inf") else -1.0
    cpd_out = round(cpd, 2) if cpd != float("inf") else -1.0
    return round(max(0.0, score), 2), insights, cpl_out, csql_out, cpd_out


def _campaign_status(score: float) -> CampaignStatus:
    if score >= 80:
        return CampaignStatus.EXCELLENT
    if score >= 60:
        return CampaignStatus.GOOD
    if score >= 40:
        return CampaignStatus.AVERAGE
    if score >= 20:
        return CampaignStatus.POOR
    return CampaignStatus.FAILING


def _build_recommendations(
    status: CampaignStatus,
    roi_pct: float,
    open_rate: float,
    conversion: float,
    unsub_rate: float,
    pipeline: float,
) -> List[str]:
    actions: List[str] = []

    if status == CampaignStatus.EXCELLENT:
        actions.append("scale_immediately")
        actions.append("repurpose_content")
    elif status == CampaignStatus.GOOD:
        actions.append("ab_test_content")
        actions.append("retarget_engaged")
    elif status == CampaignStatus.AVERAGE:
        actions.append("optimize_targeting")
        actions.append("improve_landing")
        actions.append("add_nurture_sequence")
    elif status == CampaignStatus.POOR:
        actions.append("optimize_targeting")
        actions.append("increase_personalization")
        actions.append("cut_budget")
    else:
        actions.append("pause_campaign")

    if open_rate < 15.0:
        actions.append("ab_test_content")
    if conversion < 8.0 and "optimize_targeting" not in actions:
        actions.append("optimize_targeting")
    if unsub_rate > 1.0 and "reduce_frequency" not in actions:
        actions.append("reduce_frequency")
    if pipeline == 0.0 and "align_sales" not in actions:
        actions.append("align_sales")

    seen: set = set()
    return [a for a in actions if not (a in seen or seen.add(a))]  # type: ignore[func-returns-value]


def _calculate_campaign(m: CampaignMetrics) -> CampaignResult:
    roi_s, roi_pct, benchmark_vs, roi_insights = _roi_score(m)
    reach_s, reach_insights = _reach_efficiency(m)
    conv_result = _conversion_quality(m)
    conv_s, conv_insights, l2o_rate, o2w_rate = conv_result
    cost_result = _cost_efficiency(m)
    cost_s, cost_insights, cpl, csql, cpd = cost_result

    overall = round(
        roi_s * 0.35 + reach_s * 0.25 + conv_s * 0.25 + cost_s * 0.15,
        2,
    )
    status = _campaign_status(overall)

    open_rate = (m.opens / m.emails_sent * 100.0) if m.emails_sent > 0 else 0.0
    click_rate = (m.clicks / m.emails_sent * 100.0) if m.emails_sent > 0 else 0.0
    unsub_rate = (m.unsubscribes / m.emails_sent * 100.0) if m.emails_sent > 0 else 0.0

    all_insight_keys = roi_insights + reach_insights + conv_insights + cost_insights
    seen: set = set()
    unique_keys = [k for k in all_insight_keys if not (k in seen or seen.add(k))]  # type: ignore[func-returns-value]
    insights = [_INSIGHTS[k] for k in unique_keys if k in _INSIGHTS]

    rec_keys = _build_recommendations(status, roi_pct, open_rate, l2o_rate, unsub_rate, m.pipeline_value_eur)
    recommendations = [_RECOMMENDATIONS[k] for k in rec_keys if k in _RECOMMENDATIONS]

    return CampaignResult(
        campaign=m,
        roi_pct=roi_pct,
        roi_score=roi_s,
        reach_efficiency=reach_s,
        conversion_quality=conv_s,
        cost_efficiency=cost_s,
        overall_score=overall,
        status=status,
        cost_per_lead_eur=cpl,
        cost_per_sql_eur=csql,
        cost_per_deal_eur=cpd,
        open_rate_pct=round(open_rate, 2),
        click_rate_pct=round(click_rate, 2),
        lead_to_opp_rate_pct=l2o_rate,
        opp_to_won_rate_pct=o2w_rate,
        key_insights=insights,
        recommendations=recommendations,
        benchmark_vs_channel=benchmark_vs,
    )


class CampaignROICalculator:
    def __init__(self) -> None:
        self._store: Dict[str, CampaignResult] = {}

    def calculate(self, campaign: CampaignMetrics) -> CampaignResult:
        result = _calculate_campaign(campaign)
        self._store[campaign.campaign_id] = result
        return result

    def calculate_batch(self, campaigns: List[CampaignMetrics]) -> List[CampaignResult]:
        return [self.calculate(c) for c in campaigns]

    def get(self, campaign_id: str) -> Optional[CampaignResult]:
        return self._store.get(campaign_id)

    def all_results(self) -> List[CampaignResult]:
        return sorted(self._store.values(), key=lambda r: r.overall_score, reverse=True)

    def top_campaigns(self, n: int = 5) -> List[CampaignResult]:
        return self.all_results()[:n]

    def by_status(self, status: CampaignStatus) -> List[CampaignResult]:
        return [r for r in self._store.values() if r.status == status]

    def by_channel(self, channel: ChannelType) -> List[CampaignResult]:
        return [r for r in self._store.values() if r.campaign.channel == channel]

    def failing_campaigns(self) -> List[CampaignResult]:
        return [r for r in self._store.values() if r.status in (CampaignStatus.FAILING, CampaignStatus.POOR)]

    def excellent_campaigns(self) -> List[CampaignResult]:
        return self.by_status(CampaignStatus.EXCELLENT)

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "status_counts": {s.value: 0 for s in CampaignStatus},
                "channel_counts": {c.value: 0 for c in ChannelType},
                "avg_overall_score": 0.0,
                "avg_roi_pct": 0.0,
                "total_pipeline_eur": 0.0,
                "total_closed_revenue_eur": 0.0,
                "total_spent_eur": 0.0,
            }
        status_counts = {s.value: 0 for s in CampaignStatus}
        channel_counts = {c.value: 0 for c in ChannelType}
        for r in items:
            status_counts[r.status.value] += 1
            channel_counts[r.campaign.channel.value] += 1
        avg_score = sum(r.overall_score for r in items) / count
        avg_roi = sum(r.roi_pct for r in items) / count
        total_pipeline = sum(r.campaign.pipeline_value_eur for r in items)
        total_revenue = sum(r.campaign.closed_revenue_eur for r in items)
        total_spent = sum(r.campaign.total_spent_eur for r in items)
        return {
            "total": count,
            "status_counts": status_counts,
            "channel_counts": channel_counts,
            "avg_overall_score": round(avg_score, 2),
            "avg_roi_pct": round(avg_roi, 2),
            "total_pipeline_eur": round(total_pipeline, 2),
            "total_closed_revenue_eur": round(total_revenue, 2),
            "total_spent_eur": round(total_spent, 2),
        }

    def reset(self) -> None:
        self._store.clear()
