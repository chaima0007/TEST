from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BiometricSurveillanceInput:
    entity_id: str
    surveillance_domain: str
    region: str
    facial_recognition_deployment_density: float
    behavioral_biometric_collection_rate: float
    DNA_database_expansion_rate: float
    biometric_data_commercialization_risk: float
    cross_border_biometric_sharing_level: float
    biometric_error_rate_impact: float
    surveillance_infrastructure_concentration: float
    biometric_consent_violation_index: float
    predictive_policing_bias: float
    emotion_recognition_deployment: float
    voice_print_mass_collection: float
    gait_analysis_deployment: float
    biometric_resistance_suppression: float
    identity_theft_systemic_risk: float
    biometric_political_persecution_risk: float
    permanent_record_creation_rate: float
    biometric_apartheid_risk: float


@dataclass
class BiometricSurveillanceResult:
    entity_id: str
    surveillance_domain: str
    region: str
    deployment_score: float
    violation_score: float
    control_score: float
    persecution_score: float
    composite_score: float
    risk_level: str
    surveillance_pattern: str
    severity: str
    recommended_action: str
    signal: str
    facial_recognition_deployment_density: float
    biometric_political_persecution_risk: float

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "surveillance_domain": self.surveillance_domain,
            "region": self.region,
            "deployment_score": self.deployment_score,
            "violation_score": self.violation_score,
            "control_score": self.control_score,
            "persecution_score": self.persecution_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "surveillance_pattern": self.surveillance_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "facial_recognition_deployment_density": self.facial_recognition_deployment_density,
            "biometric_political_persecution_risk": self.biometric_political_persecution_risk,
        }


class BiometricSurveillanceEngine:
    def __init__(self) -> None:
        self._results: list[BiometricSurveillanceResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: BiometricSurveillanceInput) -> BiometricSurveillanceResult:
        deployment = self._deployment_score(inp)
        violation  = self._violation_score(inp)
        control    = self._control_score(inp)
        persecution = self._persecution_score(inp)
        composite  = self._composite(deployment, violation, control, persecution)
        risk_level = self._risk_level(composite)
        pattern    = self._surveillance_pattern(inp)
        severity   = self._severity(risk_level)
        action     = self._recommended_action(risk_level)
        signal     = self._signal(risk_level, composite)

        result = BiometricSurveillanceResult(
            entity_id=inp.entity_id,
            surveillance_domain=inp.surveillance_domain,
            region=inp.region,
            deployment_score=deployment,
            violation_score=violation,
            control_score=control,
            persecution_score=persecution,
            composite_score=composite,
            risk_level=risk_level,
            surveillance_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            facial_recognition_deployment_density=inp.facial_recognition_deployment_density,
            biometric_political_persecution_risk=inp.biometric_political_persecution_risk,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[BiometricSurveillanceInput]) -> list[BiometricSurveillanceResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _deployment_score(self, inp: BiometricSurveillanceInput) -> float:
        score = (
            inp.facial_recognition_deployment_density * 0.4
            + inp.behavioral_biometric_collection_rate * 0.35
            + inp.gait_analysis_deployment * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _violation_score(self, inp: BiometricSurveillanceInput) -> float:
        score = (
            inp.biometric_consent_violation_index * 0.4
            + inp.biometric_data_commercialization_risk * 0.35
            + inp.DNA_database_expansion_rate * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _control_score(self, inp: BiometricSurveillanceInput) -> float:
        score = (
            inp.surveillance_infrastructure_concentration * 0.4
            + inp.biometric_resistance_suppression * 0.35
            + inp.predictive_policing_bias * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _persecution_score(self, inp: BiometricSurveillanceInput) -> float:
        score = (
            inp.biometric_political_persecution_risk * 0.4
            + inp.biometric_apartheid_risk * 0.35
            + inp.permanent_record_creation_rate * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _composite(
        self,
        deployment: float,
        violation: float,
        control: float,
        persecution: float,
    ) -> float:
        composite = (
            deployment * 0.30
            + violation * 0.25
            + control * 0.25
            + persecution * 0.20
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

    def _surveillance_pattern(self, inp: BiometricSurveillanceInput) -> str:
        if inp.facial_recognition_deployment_density >= 0.70 and inp.surveillance_infrastructure_concentration >= 0.65:
            return "total_biometric_state"
        if inp.DNA_database_expansion_rate >= 0.70 and inp.biometric_consent_violation_index >= 0.65:
            return "genetic_panopticon"
        if inp.predictive_policing_bias >= 0.70 and inp.biometric_political_persecution_risk >= 0.65:
            return "predictive_persecution"
        if inp.biometric_data_commercialization_risk >= 0.70 and inp.cross_border_biometric_sharing_level >= 0.65:
            return "identity_monopoly"
        if inp.biometric_apartheid_risk >= 0.70 and inp.biometric_resistance_suppression >= 0.65:
            return "biometric_apartheid"
        return "none"

    def _severity(self, risk_level: str) -> str:
        return {
            "critical": "état_surveillance_total",
            "high":     "contrôle_biométrique_avancé",
            "moderate": "dérive_biométrique_active",
            "low":      "surveillance_contenue",
        }[risk_level]

    def _recommended_action(self, risk_level: str) -> str:
        return {
            "critical": "résistance_biométrique_urgente",
            "high":     "régulation_biométrique_stricte",
            "moderate": "renforcement_droits_biométriques",
            "low":      "veille_biométrique_continue",
        }[risk_level]

    def _signal(self, risk_level: str, composite: float) -> str:
        signals = {
            "critical": "🔴 État de surveillance totale — contrôle biométrique systémique",
            "high":     "🟠 Contrôle biométrique avancé détecté",
            "moderate": "🟡 Dérive biométrique — vigilance requise",
            "low":      "🟢 Surveillance biométrique contenue",
        }
        return signals[risk_level]

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "module_id": 333,
                "module_name": "Biometric Surveillance & Identity Control Intelligence Engine",
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
                "avg_estimated_surveillance_index": 0.0,
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
            pattern_distribution[r.surveillance_pattern] = pattern_distribution.get(r.surveillance_pattern, 0) + 1
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
            "module_id": 333,
            "module_name": "Biometric Surveillance & Identity Control Intelligence Engine",
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
            "avg_estimated_surveillance_index": round(avg_composite / 100 * 10, 2),
        }
