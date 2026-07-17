"""Module 37 — Rep Activity Intelligence Engine

Benchmarks each sales rep's outbound activity against team or industry norms,
detects drop-offs or ramp patterns, assigns an activity health tier, and
surfaces coaching levers for managers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class ActivityTier(str, Enum):
    ELITE   = "elite"     # top-quintile activity volume + quality
    HIGH    = "high"      # above benchmark
    AVERAGE = "average"   # within ±20 % of benchmark
    LOW     = "low"       # below benchmark
    INACTIVE = "inactive" # critically low — requires immediate intervention


class ActivityTrend(str, Enum):
    ACCELERATING = "accelerating"   # week-over-week increasing ≥ 20 %
    STABLE       = "stable"         # within ±20 % WoW change
    DECLINING    = "declining"      # WoW decrease ≥ 20 %
    STALLED      = "stalled"        # < 20 % of benchmark last 7 days


class CoachingFocus(str, Enum):
    CALLS       = "calls"           # phone / video call volume low
    EMAILS      = "emails"          # email outreach volume low
    MEETINGS    = "meetings"        # booked meetings low
    PROSPECTING = "prospecting"     # pipeline gen activities low
    FOLLOW_UP   = "follow_up"       # follow-up cadence weak
    QUALITY     = "quality"         # volume ok but conversion poor
    ON_TRACK    = "on_track"        # no specific coaching needed


class ActivityAction(str, Enum):
    CELEBRATE  = "celebrate"        # ELITE — recognise and replicate
    MAINTAIN   = "maintain"         # HIGH / stable — keep momentum
    NUDGE      = "nudge"            # AVERAGE — minor adjustment needed
    COACH      = "coach"            # LOW — structured coaching plan
    INTERVENE  = "intervene"        # INACTIVE — urgent manager intervention


# ─── Input ───────────────────────────────────────────────────────────────────

@dataclass
class RepActivityInput:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    # Activity last 30 days
    calls_30d: int
    emails_30d: int
    meetings_booked_30d: int
    proposals_30d: int
    linkedin_touches_30d: int
    follow_ups_30d: int
    # Activity last 7 days (for trend)
    calls_7d: int
    emails_7d: int
    meetings_7d: int
    # Team benchmark (30-day per rep)
    benchmark_calls_30d: int
    benchmark_emails_30d: int
    benchmark_meetings_30d: int
    benchmark_proposals_30d: int
    # Conversion signals
    connect_rate_pct: float          # calls answered / calls made
    email_reply_rate_pct: float      # email replies / emails sent
    meeting_show_rate_pct: float     # meetings held / booked
    # Output quality
    deals_created_30d: int
    pipeline_generated_eur: float
    quota_attainment_pct: float


# ─── Output ──────────────────────────────────────────────────────────────────

@dataclass
class RepActivityResult:
    rep_id: str
    rep_name: str
    region: str
    segment: str

    # Computed
    activity_tier: ActivityTier
    activity_trend: ActivityTrend
    coaching_focus: CoachingFocus
    activity_action: ActivityAction
    activity_score: float          # 0–100
    call_index: float              # actual / benchmark
    email_index: float
    meeting_index: float
    proposal_index: float
    connect_rate_pct: float
    email_reply_rate_pct: float
    meeting_show_rate_pct: float
    deals_created_30d: int
    pipeline_generated_eur: float
    coaching_insights: list[str]
    action_items: list[str]

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "region": self.region,
            "segment": self.segment,
            "activity_tier": self.activity_tier.value,
            "activity_trend": self.activity_trend.value,
            "coaching_focus": self.coaching_focus.value,
            "activity_action": self.activity_action.value,
            "activity_score": self.activity_score,
            "call_index": self.call_index,
            "email_index": self.email_index,
            "meeting_index": self.meeting_index,
            "proposal_index": self.proposal_index,
            "connect_rate_pct": self.connect_rate_pct,
            "email_reply_rate_pct": self.email_reply_rate_pct,
            "meeting_show_rate_pct": self.meeting_show_rate_pct,
            "deals_created_30d": self.deals_created_30d,
            "pipeline_generated_eur": self.pipeline_generated_eur,
            "coaching_insights": self.coaching_insights,
            "action_items": self.action_items,
        }


# ─── Engine ──────────────────────────────────────────────────────────────────

class RepActivityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[RepActivityResult] = []

    # ── private helpers ────────────────────────────────────────────────────

    @staticmethod
    def _index(actual: int, benchmark: int) -> float:
        if benchmark <= 0:
            return 1.0
        return round(actual / benchmark, 2)

    def _activity_score(self, inp: RepActivityInput) -> float:
        """
        0–100 composite:
          call volume    25 pts  → min(25, call_index × 25)
          email volume   20 pts  → min(20, email_index × 20)
          meetings       20 pts  → min(20, meeting_index × 20)
          proposals      15 pts  → min(15, proposal_index × 15)
          connect rate   10 pts  → connect_rate / 10 (max 10)
          email reply     5 pts  → reply_rate / 20 (max 5)
          show rate       5 pts  → show_rate / 20 (max 5)
        """
        ci = self._index(inp.calls_30d, inp.benchmark_calls_30d)
        ei = self._index(inp.emails_30d, inp.benchmark_emails_30d)
        mi = self._index(inp.meetings_booked_30d, inp.benchmark_meetings_30d)
        pi = self._index(inp.proposals_30d, inp.benchmark_proposals_30d)

        call_pts     = min(25.0, ci * 25.0)
        email_pts    = min(20.0, ei * 20.0)
        meeting_pts  = min(20.0, mi * 20.0)
        proposal_pts = min(15.0, pi * 15.0)
        connect_pts  = min(10.0, inp.connect_rate_pct / 10.0)
        reply_pts    = min(5.0,  inp.email_reply_rate_pct / 20.0)
        show_pts     = min(5.0,  inp.meeting_show_rate_pct / 20.0)

        raw = (call_pts + email_pts + meeting_pts + proposal_pts
               + connect_pts + reply_pts + show_pts)
        return round(min(100.0, max(0.0, raw)), 1)

    def _activity_tier(self, score: float) -> ActivityTier:
        if score >= 85:
            return ActivityTier.ELITE
        if score >= 65:
            return ActivityTier.HIGH
        if score >= 45:
            return ActivityTier.AVERAGE
        if score >= 20:
            return ActivityTier.LOW
        return ActivityTier.INACTIVE

    def _activity_trend(self, inp: RepActivityInput) -> ActivityTrend:
        # Compare 7-day pace (×4 to annualise to 28 days) vs 30-day total
        total_30 = inp.calls_30d + inp.emails_30d + inp.meetings_booked_30d
        total_7  = inp.calls_7d  + inp.emails_7d  + inp.meetings_7d

        # Expected 7-day share if uniform pace
        expected_7 = total_30 / 4.0 if total_30 > 0 else 0.0

        # STALLED: very low absolute activity in last 7 days
        benchmark_weekly = (
            inp.benchmark_calls_30d
            + inp.benchmark_emails_30d
            + inp.benchmark_meetings_30d
        ) / 4.0
        if benchmark_weekly > 0 and total_7 < benchmark_weekly * 0.2:
            return ActivityTrend.STALLED

        if expected_7 <= 0:
            return ActivityTrend.STABLE

        change_ratio = total_7 / expected_7
        if change_ratio >= 1.2:
            return ActivityTrend.ACCELERATING
        if change_ratio <= 0.8:
            return ActivityTrend.DECLINING
        return ActivityTrend.STABLE

    def _coaching_focus(self, inp: RepActivityInput) -> CoachingFocus:
        ci = self._index(inp.calls_30d, inp.benchmark_calls_30d)
        ei = self._index(inp.emails_30d, inp.benchmark_emails_30d)
        mi = self._index(inp.meetings_booked_30d, inp.benchmark_meetings_30d)
        pi = self._index(inp.proposals_30d, inp.benchmark_proposals_30d)

        indices = {
            CoachingFocus.CALLS:       ci,
            CoachingFocus.EMAILS:      ei,
            CoachingFocus.MEETINGS:    mi,
            CoachingFocus.PROSPECTING: pi,
        }

        # All above threshold — check conversion quality
        if all(v >= 0.8 for v in indices.values()):
            if inp.connect_rate_pct < 15 or inp.email_reply_rate_pct < 10:
                return CoachingFocus.QUALITY
            if inp.follow_ups_30d < 5:
                return CoachingFocus.FOLLOW_UP
            return CoachingFocus.ON_TRACK

        # Worst performing lever
        worst = min(indices, key=lambda k: indices[k])
        return worst

    def _activity_action(self, tier: ActivityTier) -> ActivityAction:
        mapping = {
            ActivityTier.ELITE:    ActivityAction.CELEBRATE,
            ActivityTier.HIGH:     ActivityAction.MAINTAIN,
            ActivityTier.AVERAGE:  ActivityAction.NUDGE,
            ActivityTier.LOW:      ActivityAction.COACH,
            ActivityTier.INACTIVE: ActivityAction.INTERVENE,
        }
        return mapping[tier]

    def _coaching_insights(
        self,
        inp: RepActivityInput,
        tier: ActivityTier,
        trend: ActivityTrend,
        focus: CoachingFocus,
    ) -> list[str]:
        insights: list[str] = []

        ci = self._index(inp.calls_30d, inp.benchmark_calls_30d)
        ei = self._index(inp.emails_30d, inp.benchmark_emails_30d)
        mi = self._index(inp.meetings_booked_30d, inp.benchmark_meetings_30d)

        if ci < 0.7:
            insights.append(
                f"Volume d'appels {inp.calls_30d}/{inp.benchmark_calls_30d} — "
                f"seulement {ci:.0%} du benchmark (déficit {inp.benchmark_calls_30d - inp.calls_30d} appels)"
            )
        if ei < 0.7:
            insights.append(
                f"Volume email {inp.emails_30d}/{inp.benchmark_emails_30d} — "
                f"{ei:.0%} du benchmark"
            )
        if mi < 0.7:
            insights.append(
                f"Réunions bookées {inp.meetings_booked_30d}/{inp.benchmark_meetings_30d} — "
                f"{mi:.0%} du benchmark"
            )
        if inp.connect_rate_pct < 15:
            insights.append(
                f"Taux de connexion faible ({inp.connect_rate_pct:.1f}%) — "
                "améliorer les horaires et scripts d'appel"
            )
        if inp.email_reply_rate_pct < 10:
            insights.append(
                f"Taux de réponse email faible ({inp.email_reply_rate_pct:.1f}%) — "
                "personnaliser l'accroche et l'objet"
            )
        if trend == ActivityTrend.DECLINING:
            insights.append("Tendance activité en baisse — risque de ralentissement pipeline sous 30j")
        if trend == ActivityTrend.STALLED:
            insights.append("Activité quasi nulle sur les 7 derniers jours — signal d'alerte critique")
        if tier == ActivityTier.ELITE:
            insights.append(
                f"Performance exemplaire — score {self._activity_score(inp)} : "
                "idéal pour le peer coaching"
            )
        if inp.pipeline_generated_eur > 0:
            per_meeting = (
                inp.pipeline_generated_eur / inp.meetings_booked_30d
                if inp.meetings_booked_30d > 0 else 0
            )
            if per_meeting > 0:
                insights.append(
                    f"Pipeline/réunion : {per_meeting:,.0f}€ — "
                    f"{'bon ROI réunion' if per_meeting >= 20000 else 'améliorer la qualification avant réunion'}"
                )
        if not insights:
            insights.append("Activité conforme aux benchmarks — maintenir la cadence")
        return insights

    def _action_items(self, tier: ActivityTier, focus: CoachingFocus, inp: RepActivityInput) -> list[str]:
        if tier == ActivityTier.ELITE:
            return [
                "Planifier une session de peer coaching avec les reps moins performants",
                "Documenter les meilleures pratiques pour la playbook équipe",
                "Identifier des opportunités d'expansion territoriale",
            ]
        if tier == ActivityTier.INACTIVE:
            return [
                "Session de revue individuelle avec le manager dans les 24h",
                "Identifier les blocages : motivation, compétences, territoire ?",
                "Plan de remédiation avec jalons hebdomadaires",
                "Réévaluation du quota si territoire ou segment problématique",
            ]
        items: list[str] = []
        if focus == CoachingFocus.CALLS:
            missing = max(0, inp.benchmark_calls_30d - inp.calls_30d)
            items.append(f"Augmenter le volume d'appels de {missing} — viser {inp.benchmark_calls_30d}/mois")
            items.append("Définir des créneaux fixes de cold calling (ex. 8h-10h, 17h-18h)")
        elif focus == CoachingFocus.EMAILS:
            items.append("Activer des séquences email automatisées pour les comptes dormants")
            items.append("Viser +30% de volume email sur les 2 prochaines semaines")
        elif focus == CoachingFocus.MEETINGS:
            items.append("Augmenter les demandes de démo après chaque appel de qualification")
            items.append("Utiliser des outils de planification (Calendly) pour réduire la friction")
        elif focus == CoachingFocus.PROSPECTING:
            items.append("Envoyer au moins 2 propositions supplémentaires cette semaine")
            items.append("Prioriser les comptes avec le plus fort signal d'achat")
        elif focus == CoachingFocus.QUALITY:
            items.append("Coaching sur les scripts d'appel — améliorer le taux de connexion")
            items.append("Retravailler les objets email — A/B test sur 2 variantes cette semaine")
        elif focus == CoachingFocus.FOLLOW_UP:
            items.append("Ajouter des relances systématiques J+3 et J+7 après chaque contact")
            items.append("Mettre en place des tâches de suivi dans le CRM")
        else:
            items.append("Maintenir la cadence actuelle et préparer le pipeline du trimestre prochain")
        return items

    # ── public API ─────────────────────────────────────────────────────────

    def analyze(self, inp: RepActivityInput) -> RepActivityResult:
        score  = self._activity_score(inp)
        tier   = self._activity_tier(score)
        trend  = self._activity_trend(inp)
        focus  = self._coaching_focus(inp)
        action = self._activity_action(tier)

        result = RepActivityResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            region=inp.region,
            segment=inp.segment,
            activity_tier=tier,
            activity_trend=trend,
            coaching_focus=focus,
            activity_action=action,
            activity_score=score,
            call_index=self._index(inp.calls_30d, inp.benchmark_calls_30d),
            email_index=self._index(inp.emails_30d, inp.benchmark_emails_30d),
            meeting_index=self._index(inp.meetings_booked_30d, inp.benchmark_meetings_30d),
            proposal_index=self._index(inp.proposals_30d, inp.benchmark_proposals_30d),
            connect_rate_pct=inp.connect_rate_pct,
            email_reply_rate_pct=inp.email_reply_rate_pct,
            meeting_show_rate_pct=inp.meeting_show_rate_pct,
            deals_created_30d=inp.deals_created_30d,
            pipeline_generated_eur=inp.pipeline_generated_eur,
            coaching_insights=self._coaching_insights(inp, tier, trend, focus),
            action_items=self._action_items(tier, focus, inp),
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[RepActivityInput]) -> list[RepActivityResult]:
        """Analyze batch, sorted DESC by activity_score (best first)."""
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.activity_score, reverse=True)
        return results

    # ── filter helpers ─────────────────────────────────────────────────────

    def all_reps(self) -> list[RepActivityResult]:
        return list(self._results)

    def by_tier(self, tier: ActivityTier) -> list[RepActivityResult]:
        return [r for r in self._results if r.activity_tier == tier]

    def by_trend(self, trend: ActivityTrend) -> list[RepActivityResult]:
        return [r for r in self._results if r.activity_trend == trend]

    def by_action(self, action: ActivityAction) -> list[RepActivityResult]:
        return [r for r in self._results if r.activity_action == action]

    def elite_reps(self) -> list[RepActivityResult]:
        return self.by_tier(ActivityTier.ELITE)

    def inactive_reps(self) -> list[RepActivityResult]:
        return self.by_tier(ActivityTier.INACTIVE)

    def needs_intervention(self) -> list[RepActivityResult]:
        return [
            r for r in self._results
            if r.activity_action in (ActivityAction.INTERVENE, ActivityAction.COACH)
        ]

    def declining_reps(self) -> list[RepActivityResult]:
        return [
            r for r in self._results
            if r.activity_trend in (ActivityTrend.DECLINING, ActivityTrend.STALLED)
        ]

    # ── aggregates ─────────────────────────────────────────────────────────

    def avg_activity_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.activity_score for r in self._results) / len(self._results), 1)

    def total_pipeline_generated_eur(self) -> float:
        return sum(r.pipeline_generated_eur for r in self._results)

    def avg_call_index(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.call_index for r in self._results) / len(self._results), 2)

    def coaching_focus_distribution(self) -> dict[str, int]:
        dist: dict[str, int] = {}
        for r in self._results:
            dist[r.coaching_focus.value] = dist.get(r.coaching_focus.value, 0) + 1
        return dist

    def summary(self) -> dict:
        n = len(self._results)
        tier_counts: dict[str, int]   = {}
        trend_counts: dict[str, int]  = {}
        action_counts: dict[str, int] = {}
        for r in self._results:
            tier_counts[r.activity_tier.value]   = tier_counts.get(r.activity_tier.value, 0) + 1
            trend_counts[r.activity_trend.value] = trend_counts.get(r.activity_trend.value, 0) + 1
            action_counts[r.activity_action.value] = action_counts.get(r.activity_action.value, 0) + 1
        return {
            "total": n,
            "tier_counts": tier_counts,
            "trend_counts": trend_counts,
            "action_counts": action_counts,
            "avg_activity_score": self.avg_activity_score(),
            "total_pipeline_generated_eur": self.total_pipeline_generated_eur(),
            "elite_count": len(self.elite_reps()),
            "inactive_count": len(self.inactive_reps()),
            "intervention_count": len(self.needs_intervention()),
            "declining_count": len(self.declining_reps()),
        }

    def reset(self) -> None:
        self._results.clear()
