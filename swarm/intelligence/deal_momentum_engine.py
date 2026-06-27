from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MomentumLevel(str, Enum):
    ACCELERATING = "accelerating"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    STALLING = "stalling"
    DECLINING = "declining"
    STALLED = "stalled"


class StallReason(str, Enum):
    NO_STALL = "no_stall"
    DECISION_DELAYED = "decision_delayed"
    BUDGET_FROZEN = "budget_frozen"
    STAKEHOLDER_CHANGE = "stakeholder_change"
    COMPETITIVE_THREAT = "competitive_threat"
    CHAMPION_LEFT = "champion_left"
    TECHNICAL_BLOCKER = "technical_blocker"
    INTERNAL_MISALIGNMENT = "internal_misalignment"


class MomentumTrend(str, Enum):
    IMPROVING = "improving"
    STABLE = "stable"
    DETERIORATING = "deteriorating"
    CRITICAL = "critical"


class MomentumAction(str, Enum):
    MAINTAIN = "maintain"
    ACCELERATE = "accelerate"
    RE_ENGAGE = "re_engage"
    EXECUTIVE_ESCALATION = "executive_escalation"
    COMPETITIVE_DEFENSE = "competitive_defense"
    CHAMPION_RECOVERY = "champion_recovery"
    TECHNICAL_RESOLUTION = "technical_resolution"
    CLOSE_OR_ABANDON = "close_or_abandon"


@dataclass
class DealMomentumInput:
    deal_id: str
    rep_id: str
    rep_name: str
    account_name: str
    days_in_stage: int
    expected_days_in_stage: int
    days_to_close: int
    days_overdue: int
    activities_last_14d: int
    activities_last_30d: int
    last_activity_days_ago: int
    meetings_last_30d: int
    next_step_defined: bool
    next_step_days_out: Optional[int]
    decision_maker_engaged_14d: bool
    champion_active: bool
    exec_sponsor_engaged: bool
    champion_left: bool
    stage_advances_90d: int
    stage_regressions_90d: int
    proposal_sent: bool
    pricing_discussed: bool
    poc_started: bool
    competitor_mentioned: bool
    competitor_demo_requested: bool
    objections_unresolved: int
    technical_blockers: int
    budget_confirmed: bool
    legal_engaged: bool
    prior_momentum_score: float = 50.0


@dataclass
class DealMomentumResult:
    deal_id: str
    rep_id: str
    rep_name: str
    account_name: str
    momentum_score: float
    velocity_score: float
    engagement_score: float
    risk_score: float
    momentum_level: MomentumLevel
    stall_reason: StallReason
    momentum_trend: MomentumTrend
    momentum_action: MomentumAction
    momentum_indicators: list[str]
    risk_signals: list[str]
    recommended_actions: list[str]

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "account_name": self.account_name,
            "momentum_score": self.momentum_score,
            "velocity_score": self.velocity_score,
            "engagement_score": self.engagement_score,
            "risk_score": self.risk_score,
            "momentum_level": self.momentum_level.value,
            "stall_reason": self.stall_reason.value,
            "momentum_trend": self.momentum_trend.value,
            "momentum_action": self.momentum_action.value,
            "momentum_indicators": self.momentum_indicators,
            "risk_signals": self.risk_signals,
            "recommended_actions": self.recommended_actions,
        }


class DealMomentumEngine:
    def __init__(self) -> None:
        self.results: list[DealMomentumResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _velocity_score(self, inp: DealMomentumInput) -> float:
        score = 50.0
        # Stage over-age penalty
        if inp.expected_days_in_stage > 0:
            overrun = inp.days_in_stage - inp.expected_days_in_stage
            if overrun > 0:
                score -= min(35.0, overrun / inp.expected_days_in_stage * 35.0)
        # Overdue penalty
        if inp.days_overdue > 0:
            score -= min(25.0, float(inp.days_overdue) * 2.0)
        # Stage progression rewards/penalties
        score += min(20.0, float(inp.stage_advances_90d) * 8.0)
        score -= min(20.0, float(inp.stage_regressions_90d) * 10.0)
        # Deal progression rewards
        if inp.proposal_sent:
            score += 10.0
        if inp.pricing_discussed:
            score += 8.0
        if inp.poc_started:
            score += 7.0
        return max(0.0, min(100.0, score))

    def _engagement_score(self, inp: DealMomentumInput) -> float:
        score = 0.0
        # Activity volume
        score += min(30.0, float(inp.activities_last_14d) * 6.0)
        # Activity trend (last 14d vs expected half of 30d)
        half_30d = inp.activities_last_30d / 2.0 if inp.activities_last_30d > 0 else 0.0
        if inp.activities_last_14d >= half_30d and inp.activities_last_30d > 0:
            score += 15.0
        elif inp.activities_last_14d < half_30d:
            score -= 10.0
        # Stakeholder engagement
        if inp.decision_maker_engaged_14d:
            score += 20.0
        if inp.champion_active:
            score += 15.0
        if inp.exec_sponsor_engaged:
            score += 10.0
        # Recency bonus/penalty
        if inp.last_activity_days_ago <= 3:
            score += 10.0
        elif inp.last_activity_days_ago > 14:
            score -= 20.0
        elif inp.last_activity_days_ago > 7:
            score -= 10.0
        # Next step
        if inp.next_step_defined:
            score += 10.0
            if inp.next_step_days_out is not None and inp.next_step_days_out > 14:
                score -= 5.0
        # Champion left — critical penalty
        if inp.champion_left:
            score -= 30.0
        return max(0.0, min(100.0, score))

    def _risk_score(self, inp: DealMomentumInput) -> float:
        score = 0.0
        if inp.champion_left:
            score += 30.0
        if inp.competitor_demo_requested:
            score += 25.0
        elif inp.competitor_mentioned:
            score += 15.0
        score += min(20.0, float(inp.objections_unresolved) * 8.0)
        score += min(20.0, float(inp.technical_blockers) * 10.0)
        if not inp.budget_confirmed and inp.days_to_close <= 30:
            score += 15.0
        score += min(10.0, float(inp.stage_regressions_90d) * 5.0)
        return max(0.0, min(100.0, score))

    def _momentum_score(
        self,
        velocity: float,
        engagement: float,
        risk: float,
        prior: float,
    ) -> float:
        raw = velocity * 0.35 + engagement * 0.40 + (100.0 - risk) * 0.25
        blended = raw * 0.70 + prior * 0.30
        return round(max(0.0, min(100.0, blended)), 1)

    def _momentum_level(self, score: float) -> MomentumLevel:
        if score >= 75:
            return MomentumLevel.ACCELERATING
        if score >= 60:
            return MomentumLevel.POSITIVE
        if score >= 45:
            return MomentumLevel.NEUTRAL
        if score >= 30:
            return MomentumLevel.STALLING
        if score >= 15:
            return MomentumLevel.DECLINING
        return MomentumLevel.STALLED

    def _stall_reason(
        self, inp: DealMomentumInput, level: MomentumLevel
    ) -> StallReason:
        if inp.champion_left:
            return StallReason.CHAMPION_LEFT
        if inp.technical_blockers >= 2:
            return StallReason.TECHNICAL_BLOCKER
        if inp.competitor_demo_requested:
            return StallReason.COMPETITIVE_THREAT
        if inp.stage_regressions_90d >= 2:
            return StallReason.INTERNAL_MISALIGNMENT
        if not inp.budget_confirmed and inp.days_to_close <= 14:
            return StallReason.BUDGET_FROZEN
        if inp.days_overdue > 30:
            return StallReason.DECISION_DELAYED
        if level in (MomentumLevel.STALLING, MomentumLevel.DECLINING, MomentumLevel.STALLED):
            if not inp.decision_maker_engaged_14d and not inp.champion_active:
                return StallReason.STAKEHOLDER_CHANGE
            return StallReason.DECISION_DELAYED
        return StallReason.NO_STALL

    def _momentum_trend(
        self, score: float, prior: float, level: MomentumLevel
    ) -> MomentumTrend:
        delta = score - prior
        if delta >= 10.0:
            return MomentumTrend.IMPROVING
        if delta <= -15.0 and level in (
            MomentumLevel.DECLINING,
            MomentumLevel.STALLED,
        ):
            return MomentumTrend.CRITICAL
        if delta <= -5.0:
            return MomentumTrend.DETERIORATING
        return MomentumTrend.STABLE

    def _momentum_action(
        self,
        inp: DealMomentumInput,
        level: MomentumLevel,
        stall: StallReason,
        trend: MomentumTrend,
    ) -> MomentumAction:
        if stall == StallReason.CHAMPION_LEFT:
            return MomentumAction.CHAMPION_RECOVERY
        if level == MomentumLevel.STALLED and inp.last_activity_days_ago > 14:
            return MomentumAction.CLOSE_OR_ABANDON
        if stall == StallReason.COMPETITIVE_THREAT:
            return MomentumAction.COMPETITIVE_DEFENSE
        if stall == StallReason.TECHNICAL_BLOCKER:
            return MomentumAction.TECHNICAL_RESOLUTION
        if level in (MomentumLevel.DECLINING, MomentumLevel.STALLED) and (
            inp.exec_sponsor_engaged or inp.decision_maker_engaged_14d
        ):
            return MomentumAction.EXECUTIVE_ESCALATION
        if level in (MomentumLevel.STALLING, MomentumLevel.DECLINING):
            return MomentumAction.RE_ENGAGE
        if level in (MomentumLevel.POSITIVE, MomentumLevel.ACCELERATING):
            if inp.days_to_close <= 30:
                return MomentumAction.ACCELERATE
            return MomentumAction.MAINTAIN
        if level == MomentumLevel.NEUTRAL and inp.next_step_defined:
            return MomentumAction.MAINTAIN
        return MomentumAction.ACCELERATE

    def _build_indicators(self, inp: DealMomentumInput) -> list[str]:
        indicators: list[str] = []
        if inp.stage_advances_90d >= 2:
            indicators.append(f"{inp.stage_advances_90d} avancement(s) de stade — progression active")
        if inp.meetings_last_30d >= 2:
            indicators.append(f"{inp.meetings_last_30d} réunion(s) ce mois — engagement élevé")
        if inp.decision_maker_engaged_14d:
            indicators.append("Décideur engagé récemment — alignement validé")
        if inp.champion_active:
            indicators.append("Champion actif — support interne confirmé")
        if inp.exec_sponsor_engaged:
            indicators.append("Sponsor exec impliqué — engagement stratégique")
        if inp.proposal_sent:
            indicators.append("Proposition envoyée — étape commerciale franchie")
        if inp.pricing_discussed:
            indicators.append("Tarification discutée — évaluation budgétaire active")
        if inp.poc_started:
            indicators.append("POC démarré — validation technique en cours")
        if inp.legal_engaged:
            indicators.append("Équipe légale impliquée — phase finale de négociation")
        if inp.budget_confirmed:
            indicators.append("Budget confirmé — engagement financier sécurisé")
        if inp.next_step_defined:
            days = f" dans {inp.next_step_days_out}j" if inp.next_step_days_out is not None else ""
            indicators.append(f"Prochaine étape définie{days} — plan d'action en place")
        return indicators

    def _build_risk_signals(self, inp: DealMomentumInput) -> list[str]:
        signals: list[str] = []
        if inp.champion_left:
            signals.append("Champion quitté l'entreprise — risque critique sur le deal")
        if inp.competitor_demo_requested:
            signals.append("Démo concurrent demandée — évaluation comparative active")
        elif inp.competitor_mentioned:
            signals.append("Concurrent mentionné — risque concurrentiel identifié")
        if inp.objections_unresolved > 0:
            signals.append(f"{inp.objections_unresolved} objection(s) non résolue(s) — blocage potentiel")
        if inp.technical_blockers > 0:
            signals.append(f"{inp.technical_blockers} blocage(s) technique(s) — frein à la progression")
        if inp.days_overdue > 0:
            signals.append(f"Deal en retard de {inp.days_overdue}j sur le plan prévu")
        if inp.stage_regressions_90d >= 1:
            signals.append(f"{inp.stage_regressions_90d} régression(s) de stade — dynamique négative")
        if not inp.budget_confirmed and inp.days_to_close <= 30:
            signals.append("Budget non confirmé à J-30 — risque de fermeture sans décision")
        if inp.last_activity_days_ago > 14:
            signals.append(f"Pas d'activité depuis {inp.last_activity_days_ago}j — deal en dérive")
        return signals

    def _build_actions(
        self,
        inp: DealMomentumInput,
        action: MomentumAction,
        level: MomentumLevel,
    ) -> list[str]:
        actions: list[str] = []
        if action == MomentumAction.CHAMPION_RECOVERY:
            actions.append("Identifier et qualifier un nouveau champion interne en urgence")
            actions.append("Solliciter une introduction via le sponsor exec ou réseau")
        elif action == MomentumAction.CLOSE_OR_ABANDON:
            actions.append("Évaluer le potentiel résiduel — décision close/abandon requise")
            actions.append("Dernière tentative de contact multi-canal avant archivage")
        elif action == MomentumAction.COMPETITIVE_DEFENSE:
            actions.append("Déployer la battlecard concurrente — différenciation ciblée")
            actions.append("Accélérer la démonstration de valeur unique avant décision")
        elif action == MomentumAction.TECHNICAL_RESOLUTION:
            actions.append("Mobiliser l'équipe technique pour résoudre les blocages identifiés")
            actions.append("Planifier un appel technique avec les parties prenantes concernées")
        elif action == MomentumAction.EXECUTIVE_ESCALATION:
            actions.append("Escalader au niveau C-suite — réunion exécutive à planifier")
            actions.append("Préparer un executive brief avec ROI et impact business")
        elif action == MomentumAction.RE_ENGAGE:
            actions.append("Relancer avec un contenu à haute valeur ajoutée personnalisé")
            actions.append("Proposer une nouvelle date de réunion dans les 5 jours")
        elif action == MomentumAction.ACCELERATE:
            actions.append("Accélérer vers la prochaine étape — créer un sentiment d'urgence")
            actions.append("Présenter une offre à durée limitée ou incentive de signature")
        else:  # MAINTAIN
            actions.append("Maintenir le rythme d'engagement — ne pas perdre la dynamique")
            actions.append("Confirmer les prochaines étapes avec un calendrier précis")
        return actions

    # ── public API ────────────────────────────────────────────────────────────

    def analyze(self, inp: DealMomentumInput) -> DealMomentumResult:
        vel = round(self._velocity_score(inp), 1)
        eng = round(self._engagement_score(inp), 1)
        risk = round(self._risk_score(inp), 1)
        score = self._momentum_score(vel, eng, risk, inp.prior_momentum_score)
        level = self._momentum_level(score)
        stall = self._stall_reason(inp, level)
        trend = self._momentum_trend(score, inp.prior_momentum_score, level)
        action = self._momentum_action(inp, level, stall, trend)
        result = DealMomentumResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            account_name=inp.account_name,
            momentum_score=score,
            velocity_score=vel,
            engagement_score=eng,
            risk_score=risk,
            momentum_level=level,
            stall_reason=stall,
            momentum_trend=trend,
            momentum_action=action,
            momentum_indicators=self._build_indicators(inp),
            risk_signals=self._build_risk_signals(inp),
            recommended_actions=self._build_actions(inp, action, level),
        )
        self.results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[DealMomentumInput]
    ) -> list[DealMomentumResult]:
        for inp in inputs:
            self.analyze(inp)
        self.results.sort(key=lambda r: r.momentum_score, reverse=True)
        return self.results

    def reset(self) -> None:
        self.results = []

    # ── helpers ───────────────────────────────────────────────────────────────

    @property
    def stalled_deals(self) -> list[DealMomentumResult]:
        return [r for r in self.results if r.momentum_level == MomentumLevel.STALLED]

    @property
    def at_risk_deals(self) -> list[DealMomentumResult]:
        return [
            r for r in self.results
            if r.momentum_level in (MomentumLevel.DECLINING, MomentumLevel.STALLED)
        ]

    @property
    def accelerating_deals(self) -> list[DealMomentumResult]:
        return [r for r in self.results if r.momentum_level == MomentumLevel.ACCELERATING]

    @property
    def requires_escalation(self) -> list[DealMomentumResult]:
        return [
            r for r in self.results
            if r.momentum_action == MomentumAction.EXECUTIVE_ESCALATION
        ]

    @property
    def competitive_threats(self) -> list[DealMomentumResult]:
        return [
            r for r in self.results
            if r.stall_reason == StallReason.COMPETITIVE_THREAT
        ]

    def summary(self) -> dict:
        n = len(self.results)
        if n == 0:
            return {
                "total": 0,
                "level_counts": {},
                "stall_counts": {},
                "trend_counts": {},
                "action_counts": {},
                "avg_momentum_score": 0.0,
                "avg_velocity_score": 0.0,
                "avg_engagement_score": 0.0,
                "avg_risk_score": 0.0,
                "at_risk_count": 0,
                "escalation_count": 0,
            }
        level_counts: dict[str, int] = {}
        stall_counts: dict[str, int] = {}
        trend_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_m = total_v = total_e = total_r = 0.0
        for res in self.results:
            level_counts[res.momentum_level.value] = level_counts.get(res.momentum_level.value, 0) + 1
            stall_counts[res.stall_reason.value] = stall_counts.get(res.stall_reason.value, 0) + 1
            trend_counts[res.momentum_trend.value] = trend_counts.get(res.momentum_trend.value, 0) + 1
            action_counts[res.momentum_action.value] = action_counts.get(res.momentum_action.value, 0) + 1
            total_m += res.momentum_score
            total_v += res.velocity_score
            total_e += res.engagement_score
            total_r += res.risk_score
        return {
            "total": n,
            "level_counts": level_counts,
            "stall_counts": stall_counts,
            "trend_counts": trend_counts,
            "action_counts": action_counts,
            "avg_momentum_score": round(total_m / n, 1),
            "avg_velocity_score": round(total_v / n, 1),
            "avg_engagement_score": round(total_e / n, 1),
            "avg_risk_score": round(total_r / n, 1),
            "at_risk_count": len(self.at_risk_deals),
            "escalation_count": len(self.requires_escalation),
        }
