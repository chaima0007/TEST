from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SocialCreditInput:
    entity_id: str
    control_domain: str
    region: str
    # 17 float fields 0-1
    behavioral_score_deployment_density: float
    access_restriction_based_on_score: float
    corporate_social_scoring_integration: float
    gamification_compliance_mechanism: float
    score_opacity_and_unappealability: float
    AI_behavioral_prediction_scoring: float
    cross_sector_score_aggregation: float
    dissent_behavioral_penalization: float
    score_based_opportunity_denial: float
    social_ostracism_enforcement: float
    private_public_score_fusion: float
    automated_punishment_system: float
    behavioral_norm_homogenization: float
    opposition_score_targeting: float
    family_collective_score_punishment: float
    score_export_to_allied_systems: float
    resistance_detection_scoring: float


@dataclass
class SocialCreditResult:
    entity_id: str
    control_domain: str
    region: str
    control_score: float
    opacity_score: float
    punishment_score: float
    homogenization_score: float
    composite_score: float
    risk_level: str
    social_credit_pattern: str
    severity: str
    recommended_action: str
    signal: str
    behavioral_score_deployment_density: float
    dissent_behavioral_penalization: float

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "control_domain": self.control_domain,
            "region": self.region,
            "control_score": self.control_score,
            "opacity_score": self.opacity_score,
            "punishment_score": self.punishment_score,
            "homogenization_score": self.homogenization_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "social_credit_pattern": self.social_credit_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "behavioral_score_deployment_density": self.behavioral_score_deployment_density,
            "dissent_behavioral_penalization": self.dissent_behavioral_penalization,
        }


class SocialCreditEngine:
    def __init__(self) -> None:
        self._results: list[SocialCreditResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: SocialCreditInput) -> SocialCreditResult:
        control        = self._control_score(inp)
        opacity        = self._opacity_score(inp)
        punishment     = self._punishment_score(inp)
        homogenization = self._homogenization_score(inp)
        composite      = self._composite(control, opacity, punishment, homogenization)
        risk_level     = self._risk_level(composite)
        pattern        = self._social_credit_pattern(inp)
        severity       = self._severity(risk_level)
        action         = self._recommended_action(risk_level)
        signal         = self._signal(risk_level)

        result = SocialCreditResult(
            entity_id=inp.entity_id,
            control_domain=inp.control_domain,
            region=inp.region,
            control_score=control,
            opacity_score=opacity,
            punishment_score=punishment,
            homogenization_score=homogenization,
            composite_score=composite,
            risk_level=risk_level,
            social_credit_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            behavioral_score_deployment_density=inp.behavioral_score_deployment_density,
            dissent_behavioral_penalization=inp.dissent_behavioral_penalization,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[SocialCreditInput]) -> list[SocialCreditResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _control_score(self, inp: SocialCreditInput) -> float:
        score = (
            inp.behavioral_score_deployment_density * 0.4
            + inp.access_restriction_based_on_score * 0.35
            + inp.automated_punishment_system * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _opacity_score(self, inp: SocialCreditInput) -> float:
        score = (
            inp.score_opacity_and_unappealability * 0.4
            + inp.AI_behavioral_prediction_scoring * 0.35
            + inp.cross_sector_score_aggregation * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _punishment_score(self, inp: SocialCreditInput) -> float:
        score = (
            inp.dissent_behavioral_penalization * 0.4
            + inp.opposition_score_targeting * 0.35
            + inp.family_collective_score_punishment * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _homogenization_score(self, inp: SocialCreditInput) -> float:
        score = (
            inp.behavioral_norm_homogenization * 0.4
            + inp.social_ostracism_enforcement * 0.35
            + inp.gamification_compliance_mechanism * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _composite(
        self,
        control: float,
        opacity: float,
        punishment: float,
        homogenization: float,
    ) -> float:
        composite = (
            control * 0.30
            + opacity * 0.25
            + punishment * 0.25
            + homogenization * 0.20
        )
        return round(max(0.0, min(100.0, composite)), 2)

    def _risk_level(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    def _social_credit_pattern(self, inp: SocialCreditInput) -> str:
        if inp.behavioral_score_deployment_density >= 0.70 and inp.automated_punishment_system >= 0.65:
            return "total_behavioral_control"
        if inp.dissent_behavioral_penalization >= 0.70 and inp.opposition_score_targeting >= 0.65:
            return "dissent_elimination"
        if inp.family_collective_score_punishment >= 0.70 and inp.social_ostracism_enforcement >= 0.65:
            return "collective_punishment_system"
        if inp.behavioral_norm_homogenization >= 0.70 and inp.score_opacity_and_unappealability >= 0.65:
            return "behavioral_homogenization_lock"
        if inp.corporate_social_scoring_integration >= 0.70 and inp.private_public_score_fusion >= 0.65:
            return "corporate_state_score_fusion"
        return "none"

    def _severity(self, risk_level: str) -> str:
        return {
            "critical": "contrôle_comportemental_total",
            "high":     "système_crédit_social_avancé",
            "moderate": "notation_comportementale_structurelle",
            "low":      "scoring_comportemental_limité",
        }[risk_level]

    def _recommended_action(self, risk_level: str) -> str:
        return {
            "critical": "résistance_crédit_social_urgente",
            "high":     "interdiction_système_crédit_social",
            "moderate": "protection_droits_comportementaux",
            "low":      "veille_scoring_comportemental",
        }[risk_level]

    def _signal(self, risk_level: str) -> str:
        return {
            "critical": "🔴 Contrôle comportemental total — crédit social systémique",
            "high":     "🟠 Système crédit social avancé détecté",
            "moderate": "🟡 Notation comportementale structurelle active",
            "low":      "🟢 Scoring comportemental limité et contenu",
        }[risk_level]

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "module_id": 348,
                "module_name": "Social Credit & Behavioral Score Intelligence Engine",
                "total_entities": 0,
                "critical_count": 0,
                "high_count": 0,
                "moderate_count": 0,
                "low_count": 0,
                "avg_composite": 0.0,
                "pattern_distribution": {},
                "risk_distribution": {},
                "severity_distribution": {},
                "action_distribution": {},
                "avg_estimated_social_credit_index": 0.0,
            }

        pattern_distribution: dict[str, int] = {}
        risk_distribution: dict[str, int] = {}
        severity_distribution: dict[str, int] = {}
        action_distribution: dict[str, int] = {}
        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in self._results:
            pattern_distribution[r.social_credit_pattern] = pattern_distribution.get(r.social_credit_pattern, 0) + 1
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity] = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical_count += 1
            elif r.risk_level == "high":
                high_count += 1
            elif r.risk_level == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        avg_composite = round(total_composite / n, 2)

        return {
            "module_id": 348,
            "module_name": "Social Credit & Behavioral Score Intelligence Engine",
            "total_entities": n,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_social_credit_index": round(avg_composite / 100 * 10, 2),
        }
