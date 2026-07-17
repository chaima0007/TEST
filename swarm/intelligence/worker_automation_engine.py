from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WorkerAutomationInput:
    entity_id: str
    sector_type: str
    region: str
    # 17 float fields (0-1)
    displacement_rate: float
    automation_penetration: float
    skill_adaptability: float
    reskilling_investment: float
    social_safety_coverage: float
    policy_effectiveness: float
    job_creation_rate: float
    union_strength: float
    education_quality: float
    wage_inequality: float
    geographic_mobility: float
    age_vulnerability: float
    gender_impact: float
    manufacturing_exposure: float
    service_sector_risk: float
    platform_economy_growth: float
    retraining_success_rate: float


@dataclass
class WorkerAutomationResult:
    entity_id: str
    sector_type: str
    region: str
    displacement_score: float
    skill_gap_score: float
    social_safety_score: float
    policy_response_score: float
    composite_score: float
    risk_level: str
    automation_pattern: str
    severity: str
    recommended_action: str
    signal: str
    displacement_rate: float
    automation_penetration: float

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "sector_type": self.sector_type,
            "region": self.region,
            "displacement_score": self.displacement_score,
            "skill_gap_score": self.skill_gap_score,
            "social_safety_score": self.social_safety_score,
            "policy_response_score": self.policy_response_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "automation_pattern": self.automation_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "displacement_rate": self.displacement_rate,
            "automation_penetration": self.automation_penetration,
        }


class WorkerAutomationEngine:
    def __init__(self) -> None:
        self._results: list[WorkerAutomationResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: WorkerAutomationInput) -> WorkerAutomationResult:
        displacement  = self._displacement_score(inp)
        skill_gap     = self._skill_gap_score(inp)
        social_safety = self._social_safety_score(inp)
        policy_resp   = self._policy_response_score(inp)
        composite     = self._composite(displacement, skill_gap, social_safety, policy_resp)
        risk_level    = self._risk_level(composite)
        pattern       = self._automation_pattern(inp)
        severity      = self._severity(risk_level)
        action        = self._recommended_action(risk_level)
        signal        = self._signal(risk_level)

        result = WorkerAutomationResult(
            entity_id=inp.entity_id,
            sector_type=inp.sector_type,
            region=inp.region,
            displacement_score=displacement,
            skill_gap_score=skill_gap,
            social_safety_score=social_safety,
            policy_response_score=policy_resp,
            composite_score=composite,
            risk_level=risk_level,
            automation_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            displacement_rate=inp.displacement_rate,
            automation_penetration=inp.automation_penetration,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[WorkerAutomationInput]) -> list[WorkerAutomationResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _displacement_score(self, inp: WorkerAutomationInput) -> float:
        score = (
            inp.displacement_rate * 0.40
            + inp.automation_penetration * 0.35
            + inp.manufacturing_exposure * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _skill_gap_score(self, inp: WorkerAutomationInput) -> float:
        score = (
            (1 - inp.skill_adaptability) * 0.40
            + (1 - inp.reskilling_investment) * 0.35
            + (1 - inp.retraining_success_rate) * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _social_safety_score(self, inp: WorkerAutomationInput) -> float:
        score = (
            (1 - inp.social_safety_coverage) * 0.40
            + (1 - inp.union_strength) * 0.35
            + inp.wage_inequality * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _policy_response_score(self, inp: WorkerAutomationInput) -> float:
        score = (
            (1 - inp.policy_effectiveness) * 0.40
            + (1 - inp.education_quality) * 0.35
            + (1 - inp.job_creation_rate) * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _composite(
        self,
        displacement: float,
        skill_gap: float,
        social_safety: float,
        policy_resp: float,
    ) -> float:
        composite = (
            displacement * 0.30
            + skill_gap * 0.25
            + social_safety * 0.25
            + policy_resp * 0.20
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

    def _automation_pattern(self, inp: WorkerAutomationInput) -> str:
        if inp.displacement_rate > 0.85 and inp.automation_penetration > 0.80:
            return "mass_workforce_obsolescence"
        if inp.skill_adaptability < 0.15 and inp.reskilling_investment < 0.20:
            return "skill_mismatch_crisis"
        if inp.social_safety_coverage < 0.15 and inp.union_strength < 0.20:
            return "social_safety_net_collapse"
        if inp.wage_inequality > 0.80 and inp.platform_economy_growth > 0.75:
            return "automation_inequality_trap"
        if inp.policy_effectiveness < 0.20 and inp.job_creation_rate < 0.20:
            return "policy_vacuum_crisis"
        return "none"

    def _severity(self, risk_level: str) -> str:
        return {
            "critical": "crise_obsolescence_massive_travailleurs",
            "high":     "déplacement_automatisation_majeur",
            "moderate": "vulnérabilité_transformation_emploi",
            "low":      "transition_emploi_sous_surveillance",
        }[risk_level]

    def _recommended_action(self, risk_level: str) -> str:
        return {
            "critical": "intervention_urgente_reconversion_massive",
            "high":     "programme_requalification_accéléré",
            "moderate": "renforcement_filets_protection_sociale",
            "low":      "veille_transformation_emploi_continue",
        }[risk_level]

    def _signal(self, risk_level: str) -> str:
        return {
            "critical": "🔴 Crise d'obsolescence massive des travailleurs — intervention d'urgence requise",
            "high":     "🟠 Déplacement par automatisation majeur détecté — requalification accélérée nécessaire",
            "moderate": "🟡 Vulnérabilité à la transformation de l'emploi — renforcement des protections sociales",
            "low":      "🟢 Transition emploi sous surveillance — veille préventive maintenue",
        }[risk_level]

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "module_id": 393,
                "module_name": "Automatisation & Déplacement des Travailleurs Intelligence Engine",
                "total": 0,
                "critical": 0,
                "high": 0,
                "moderate": 0,
                "low": 0,
                "avg_composite": 0.0,
                "pattern_distribution": {},
                "risk_distribution": {},
                "severity_distribution": {},
                "action_distribution": {},
                "avg_estimated_automation_displacement_index": 0.0,
            }

        pattern_distribution: dict[str, int] = {}
        risk_distribution: dict[str, int] = {}
        severity_distribution: dict[str, int] = {}
        action_distribution: dict[str, int] = {}
        total_composite = 0.0
        critical = 0
        high = 0
        moderate = 0
        low = 0

        for r in self._results:
            pattern_distribution[r.automation_pattern] = pattern_distribution.get(r.automation_pattern, 0) + 1
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity] = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical += 1
            elif r.risk_level == "high":
                high += 1
            elif r.risk_level == "moderate":
                moderate += 1
            else:
                low += 1

        avg_composite = round(total_composite / n, 2)

        return {
            "module_id": 393,
            "module_name": "Automatisation & Déplacement des Travailleurs Intelligence Engine",
            "total": n,
            "critical": critical,
            "high": high,
            "moderate": moderate,
            "low": low,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_automation_displacement_index": round(avg_composite / 100 * 10, 2),
        }
