from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CommitCategory(str, Enum):
    COMMIT   = "commit"
    UPSIDE   = "upside"
    PIPELINE = "pipeline"
    AT_RISK  = "at_risk"
    OMITTED  = "omitted"


class ForecastConfidence(str, Enum):
    HIGH     = "high"
    MEDIUM   = "medium"
    LOW      = "low"
    VERY_LOW = "very_low"


class BiasType(str, Enum):
    ACCURATE            = "accurate"
    SANDBAGGER          = "sandbagger"
    OPTIMISTIC          = "optimistic"
    SANDBAGGING_RISK    = "sandbagging_risk"
    OVERFORECASTING_RISK = "overforecasting_risk"


class CommitAction(str, Enum):
    CONFIRM    = "confirm"
    CHALLENGE  = "challenge"
    PULL_IN    = "pull_in"
    PUSH_OUT   = "push_out"
    ESCALATE   = "escalate"
    MONITOR    = "monitor"


@dataclass
class ForecastCommitInput:
    deal_id: str
    rep_id: str
    rep_name: str
    account_name: str
    rep_commit_amount: float
    pipeline_value: float
    close_date_days_out: int
    stage_probability: float
    ai_win_probability: float
    rep_win_probability: float
    days_in_current_stage: int
    expected_days_in_stage: int
    decision_maker_confirmed: bool
    verbal_commit_received: bool
    legal_reviewing: bool
    contract_sent: bool
    po_received: bool
    budget_confirmed: bool
    champion_strong: bool
    exec_aligned: bool
    competitor_eliminated: bool
    objections_resolved: bool
    last_activity_days_ago: int
    rep_historical_accuracy: float
    prior_quarter_sandbagging: float = 0.0


@dataclass
class ForecastCommitResult:
    deal_id: str
    rep_id: str
    rep_name: str
    account_name: str
    commit_score: float
    sandbag_score: float
    risk_score: float
    calibrated_probability: float
    commit_category: CommitCategory
    forecast_confidence: ForecastConfidence
    bias_type: BiasType
    commit_action: CommitAction
    confidence_factors: list[str]
    risk_factors: list[str]
    recommended_actions: list[str]

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "account_name": self.account_name,
            "commit_score": self.commit_score,
            "sandbag_score": self.sandbag_score,
            "risk_score": self.risk_score,
            "calibrated_probability": self.calibrated_probability,
            "commit_category": self.commit_category.value,
            "forecast_confidence": self.forecast_confidence.value,
            "bias_type": self.bias_type.value,
            "commit_action": self.commit_action.value,
            "confidence_factors": self.confidence_factors,
            "risk_factors": self.risk_factors,
            "recommended_actions": self.recommended_actions,
        }


class ForecastCommitEngine:
    def __init__(self) -> None:
        self.results: list[ForecastCommitResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _commit_score(self, inp: ForecastCommitInput) -> float:
        """Measures how solid the rep's commit is based on signals."""
        score = 0.0
        # Hard closing signals (strongest)
        if inp.po_received:
            score += 35.0
        elif inp.contract_sent:
            score += 25.0
        elif inp.legal_reviewing:
            score += 18.0
        elif inp.verbal_commit_received:
            score += 12.0
        # Budget & decision alignment
        if inp.budget_confirmed:
            score += 15.0
        if inp.decision_maker_confirmed:
            score += 12.0
        # Relationship & champion
        if inp.champion_strong:
            score += 8.0
        if inp.exec_aligned:
            score += 7.0
        # Competitive & objections
        if inp.competitor_eliminated:
            score += 8.0
        if inp.objections_resolved:
            score += 7.0
        # Timeline health
        if inp.close_date_days_out > 0:
            if inp.close_date_days_out <= 14:
                score += 5.0
        # Recent activity
        if inp.last_activity_days_ago <= 3:
            score += 3.0
        elif inp.last_activity_days_ago > 14:
            score -= 10.0
        # Rep AI probability alignment
        if inp.rep_win_probability > 0:
            prob_delta = abs(inp.rep_win_probability - inp.ai_win_probability)
            if prob_delta <= 0.10:
                score += 5.0
            elif prob_delta >= 0.30:
                score -= 5.0
        return max(0.0, min(100.0, score))

    def _sandbag_score(self, inp: ForecastCommitInput) -> float:
        """Measures likelihood the rep is sandbagging (underreporting)."""
        score = 0.0
        # Rep commits less than expected value
        if inp.pipeline_value > 0 and inp.rep_commit_amount > 0:
            commit_ratio = inp.rep_commit_amount / inp.pipeline_value
            if commit_ratio < 0.70:
                score += min(25.0, (1.0 - commit_ratio) * 30.0)
        # Rep probability lower than AI probability
        if inp.rep_win_probability > 0:
            delta = inp.ai_win_probability - inp.rep_win_probability
            if delta > 0.20:
                score += min(30.0, delta * 60.0)
        # Strong closing signals but uncommitted
        closing_signals = sum([
            inp.po_received, inp.contract_sent, inp.verbal_commit_received,
            inp.legal_reviewing, inp.budget_confirmed, inp.decision_maker_confirmed,
        ])
        if closing_signals >= 3 and inp.rep_commit_amount < inp.pipeline_value * 0.80:
            score += 15.0
        # Historical sandbagging pattern
        if inp.prior_quarter_sandbagging > 0.15:
            score += min(20.0, inp.prior_quarter_sandbagging * 50.0)
        return max(0.0, min(100.0, score))

    def _risk_score(self, inp: ForecastCommitInput) -> float:
        """Measures risk that this deal will not close as forecast."""
        score = 0.0
        # Stage over-age
        if inp.expected_days_in_stage > 0:
            overrun = inp.days_in_current_stage - inp.expected_days_in_stage
            if overrun > 0:
                score += min(20.0, overrun / inp.expected_days_in_stage * 20.0)
        # Missing critical signals for the close date
        if inp.close_date_days_out <= 30:
            if not inp.decision_maker_confirmed:
                score += 12.0
            if not inp.budget_confirmed:
                score += 12.0
            if not inp.champion_strong:
                score += 8.0
        if inp.close_date_days_out <= 14:
            if not inp.contract_sent and not inp.po_received:
                score += 15.0
        # AI probability substantially lower than rep
        if inp.rep_win_probability > 0:
            delta = inp.rep_win_probability - inp.ai_win_probability
            if delta > 0.20:
                score += min(20.0, delta * 40.0)
        # Inactivity
        if inp.last_activity_days_ago > 14:
            score += 15.0
        elif inp.last_activity_days_ago > 7:
            score += 8.0
        # No objection resolution yet
        if not inp.objections_resolved:
            score += 5.0
        # Competitor still present
        if not inp.competitor_eliminated:
            score += 5.0
        return max(0.0, min(100.0, score))

    def _calibrated_probability(
        self, inp: ForecastCommitInput, commit: float, risk: float
    ) -> float:
        """Blends AI, stage, and rep probabilities weighted by commit quality."""
        # Weight AI higher when rep has historical inaccuracy
        rep_weight = max(0.20, min(0.40, inp.rep_historical_accuracy * 0.50))
        ai_weight  = 1.0 - rep_weight - 0.20
        stage_weight = 0.20
        raw = (
            inp.ai_win_probability   * ai_weight +
            inp.rep_win_probability  * rep_weight +
            inp.stage_probability    * stage_weight
        )
        # Adjust for risk
        risk_adj = 1.0 - (risk / 100.0) * 0.30
        calibrated = raw * risk_adj
        return round(max(0.0, min(1.0, calibrated)), 3)

    def _commit_category(
        self, inp: ForecastCommitInput, commit: float, sandbag: float
    ) -> CommitCategory:
        # PO or contract sent and close within 30 days → solid commit
        if (inp.po_received or (inp.contract_sent and inp.close_date_days_out <= 14)):
            return CommitCategory.COMMIT
        if commit >= 65 and inp.rep_win_probability >= 0.75:
            return CommitCategory.COMMIT
        # Sandbag detected → might actually close sooner
        if sandbag >= 50:
            return CommitCategory.UPSIDE
        if commit >= 40 and inp.rep_win_probability >= 0.50:
            return CommitCategory.UPSIDE
        if commit >= 20 and inp.ai_win_probability >= 0.35:
            return CommitCategory.PIPELINE
        if commit < 20 and inp.last_activity_days_ago > 14:
            return CommitCategory.OMITTED
        return CommitCategory.AT_RISK

    def _forecast_confidence(
        self, commit: float, risk: float, cat: CommitCategory
    ) -> ForecastConfidence:
        if cat == CommitCategory.COMMIT and commit >= 70 and risk <= 25:
            return ForecastConfidence.HIGH
        if cat in (CommitCategory.COMMIT, CommitCategory.UPSIDE) and risk <= 40:
            return ForecastConfidence.MEDIUM
        if cat == CommitCategory.PIPELINE and risk <= 50:
            return ForecastConfidence.LOW
        return ForecastConfidence.VERY_LOW

    def _bias_type(self, inp: ForecastCommitInput, sandbag: float) -> BiasType:
        delta = inp.rep_win_probability - inp.ai_win_probability
        accuracy = inp.rep_historical_accuracy
        # Clear sandbagger: AI much higher, prior history of it
        if sandbag >= 60 or (sandbag >= 40 and inp.prior_quarter_sandbagging > 0.20):
            return BiasType.SANDBAGGER
        # Sandbagging risk without confirmed history
        if sandbag >= 25:
            return BiasType.SANDBAGGING_RISK
        # Rep is over-optimistic
        if delta > 0.25 or (delta > 0.15 and accuracy < 0.60):
            return BiasType.OVERFORECASTING_RISK
        if delta > 0.15:
            return BiasType.OPTIMISTIC
        return BiasType.ACCURATE

    def _commit_action(
        self,
        inp: ForecastCommitInput,
        cat: CommitCategory,
        bias: BiasType,
        risk: float,
    ) -> CommitAction:
        if cat == CommitCategory.COMMIT and bias == BiasType.ACCURATE and risk <= 25:
            return CommitAction.CONFIRM
        if cat == CommitCategory.COMMIT and bias in (BiasType.SANDBAGGER, BiasType.SANDBAGGING_RISK):
            return CommitAction.PULL_IN
        if bias in (BiasType.OVERFORECASTING_RISK, BiasType.OPTIMISTIC):
            return CommitAction.PUSH_OUT
        if cat == CommitCategory.AT_RISK:
            return CommitAction.ESCALATE
        if cat == CommitCategory.OMITTED:
            return CommitAction.PUSH_OUT
        if risk >= 60:
            return CommitAction.ESCALATE
        if cat == CommitCategory.COMMIT and risk > 35:
            return CommitAction.CHALLENGE
        if cat in (CommitCategory.UPSIDE, CommitCategory.PIPELINE):
            return CommitAction.MONITOR
        return CommitAction.CONFIRM

    def _build_confidence_factors(self, inp: ForecastCommitInput) -> list[str]:
        factors: list[str] = []
        if inp.po_received:
            factors.append("Bon de commande reçu — engagement financier formel")
        if inp.contract_sent:
            factors.append("Contrat envoyé — phase contractuelle engagée")
        if inp.legal_reviewing:
            factors.append("Équipe légale en review — validation finale en cours")
        if inp.verbal_commit_received:
            factors.append("Accord verbal obtenu — intention d'achat confirmée")
        if inp.budget_confirmed:
            factors.append("Budget confirmé — financement sécurisé")
        if inp.decision_maker_confirmed:
            factors.append("Décideur identifié et engagé — alignement décisionnel")
        if inp.champion_strong:
            factors.append("Champion fort — support interne solide")
        if inp.exec_aligned:
            factors.append("Alignement C-level — soutien stratégique acquis")
        if inp.competitor_eliminated:
            factors.append("Concurrents éliminés — position de leader confirmée")
        if inp.objections_resolved:
            factors.append("Toutes les objections résolues — voie libre pour la signature")
        return factors

    def _build_risk_factors(self, inp: ForecastCommitInput, risk: float) -> list[str]:
        factors: list[str] = []
        if not inp.decision_maker_confirmed and inp.close_date_days_out <= 30:
            factors.append("Décideur non confirmé à J-30 — risque de décision sans validation")
        if not inp.budget_confirmed and inp.close_date_days_out <= 30:
            factors.append("Budget non confirmé à J-30 — risque de blocage financier")
        if not inp.contract_sent and inp.close_date_days_out <= 14:
            factors.append("Pas de contrat envoyé à J-14 — risque de glissement de closing")
        if inp.last_activity_days_ago > 14:
            factors.append(f"Pas d'activité depuis {inp.last_activity_days_ago}j — deal en dérive")
        if inp.rep_win_probability - inp.ai_win_probability > 0.20:
            factors.append("Probabilité rep supérieure à l'IA — risque de surconfiance commerciale")
        if inp.days_in_current_stage > inp.expected_days_in_stage * 1.5 and inp.expected_days_in_stage > 0:
            factors.append("Deal en retard dans le stade actuel — progression bloquée")
        if not inp.objections_resolved:
            factors.append("Objections non résolues — résistance acheteur persistante")
        if not inp.competitor_eliminated:
            factors.append("Concurrents toujours actifs — deal non sécurisé")
        return factors

    def _build_actions(
        self, inp: ForecastCommitInput, action: CommitAction, bias: BiasType
    ) -> list[str]:
        actions: list[str] = []
        if action == CommitAction.CONFIRM:
            actions.append("Valider le commit — deal solide, maintenir le rythme de clôture")
            actions.append("Planifier la revue contractuelle finale avec les parties")
        elif action == CommitAction.PULL_IN:
            actions.append("Challenger le rep — les signaux suggèrent une clôture plus rapide")
            actions.append("Proposer une incitation de fin de mois pour accélérer la signature")
        elif action == CommitAction.PUSH_OUT:
            actions.append("Réaligner la date de clôture sur les signaux réels du deal")
            actions.append("Identifier les blocages spécifiques empêchant la signature")
        elif action == CommitAction.CHALLENGE:
            actions.append("Valider les hypothèses du rep avec des preuves concrètes")
            actions.append("Demander un plan de clôture détaillé avec jalons et responsables")
        elif action == CommitAction.ESCALATE:
            actions.append("Escalader au manager — deal à risque nécessitant une intervention")
            actions.append("Réunion d'urgence avec le rep pour plan de récupération")
        else:  # MONITOR
            actions.append("Surveiller l'évolution des signaux — deal en phase de maturation")
            actions.append("Fixer un point de revue dans 7 jours pour évaluer la progression")
        return actions

    # ── public API ────────────────────────────────────────────────────────────

    def analyze(self, inp: ForecastCommitInput) -> ForecastCommitResult:
        commit  = round(self._commit_score(inp), 1)
        sandbag = round(self._sandbag_score(inp), 1)
        risk    = round(self._risk_score(inp), 1)
        calib   = self._calibrated_probability(inp, commit, risk)
        cat     = self._commit_category(inp, commit, sandbag)
        conf    = self._forecast_confidence(commit, risk, cat)
        bias    = self._bias_type(inp, sandbag)
        action  = self._commit_action(inp, cat, bias, risk)
        result = ForecastCommitResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            account_name=inp.account_name,
            commit_score=commit,
            sandbag_score=sandbag,
            risk_score=risk,
            calibrated_probability=calib,
            commit_category=cat,
            forecast_confidence=conf,
            bias_type=bias,
            commit_action=action,
            confidence_factors=self._build_confidence_factors(inp),
            risk_factors=self._build_risk_factors(inp, risk),
            recommended_actions=self._build_actions(inp, action, bias),
        )
        self.results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[ForecastCommitInput]
    ) -> list[ForecastCommitResult]:
        for inp in inputs:
            self.analyze(inp)
        self.results.sort(key=lambda r: r.commit_score, reverse=True)
        return self.results

    def reset(self) -> None:
        self.results = []

    # ── helpers ───────────────────────────────────────────────────────────────

    @property
    def solid_commits(self) -> list[ForecastCommitResult]:
        return [r for r in self.results if r.commit_category == CommitCategory.COMMIT]

    @property
    def at_risk_commits(self) -> list[ForecastCommitResult]:
        return [r for r in self.results if r.commit_category == CommitCategory.AT_RISK]

    @property
    def sandbagged_deals(self) -> list[ForecastCommitResult]:
        return [
            r for r in self.results
            if r.bias_type in (BiasType.SANDBAGGER, BiasType.SANDBAGGING_RISK)
        ]

    @property
    def overforecasted_deals(self) -> list[ForecastCommitResult]:
        return [
            r for r in self.results
            if r.bias_type in (BiasType.OPTIMISTIC, BiasType.OVERFORECASTING_RISK)
        ]

    @property
    def needs_escalation(self) -> list[ForecastCommitResult]:
        return [r for r in self.results if r.commit_action == CommitAction.ESCALATE]

    def summary(self) -> dict:
        n = len(self.results)
        if n == 0:
            return {
                "total": 0,
                "category_counts": {},
                "confidence_counts": {},
                "bias_counts": {},
                "action_counts": {},
                "avg_commit_score": 0.0,
                "avg_sandbag_score": 0.0,
                "avg_risk_score": 0.0,
                "avg_calibrated_probability": 0.0,
                "solid_commit_count": 0,
                "at_risk_count": 0,
                "escalation_count": 0,
            }
        cat_counts:  dict[str, int] = {}
        conf_counts: dict[str, int] = {}
        bias_counts: dict[str, int] = {}
        act_counts:  dict[str, int] = {}
        total_commit = total_sandbag = total_risk = total_prob = 0.0
        for r in self.results:
            cat_counts[r.commit_category.value]   = cat_counts.get(r.commit_category.value, 0) + 1
            conf_counts[r.forecast_confidence.value] = conf_counts.get(r.forecast_confidence.value, 0) + 1
            bias_counts[r.bias_type.value]        = bias_counts.get(r.bias_type.value, 0) + 1
            act_counts[r.commit_action.value]     = act_counts.get(r.commit_action.value, 0) + 1
            total_commit  += r.commit_score
            total_sandbag += r.sandbag_score
            total_risk    += r.risk_score
            total_prob    += r.calibrated_probability
        return {
            "total": n,
            "category_counts": cat_counts,
            "confidence_counts": conf_counts,
            "bias_counts": bias_counts,
            "action_counts": act_counts,
            "avg_commit_score": round(total_commit / n, 1),
            "avg_sandbag_score": round(total_sandbag / n, 1),
            "avg_risk_score": round(total_risk / n, 1),
            "avg_calibrated_probability": round(total_prob / n, 3),
            "solid_commit_count": len(self.solid_commits),
            "at_risk_count": len(self.at_risk_commits),
            "escalation_count": len(self.needs_escalation),
        }
