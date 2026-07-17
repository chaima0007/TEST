from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RefugeeCrisisInput:
    entity_id: str
    displacement_type: str
    region: str
    # 17 float fields
    displacement_volume: float
    climate_displacement_acceleration: float
    conflict_displacement_intensity: float
    asylum_system_collapse: float
    statelessness_risk: float
    host_country_capacity_overflow: float
    refugee_integration_failure: float
    trafficking_vulnerability: float
    return_impossibility: float
    UNHCR_funding_gap: float
    border_militarization_harm: float
    xenophobia_political_backlash: float
    protracted_displacement_duration: float
    education_access_gap: float
    healthcare_refugee_gap: float
    economic_exclusion_refugees: float
    secondary_displacement_risk: float


@dataclass
class RefugeeCrisisResult:
    entity_id: str
    displacement_type: str
    region: str
    displacement_score: float
    protection_score: float
    integration_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    displacement_pattern: str
    severity: str
    recommended_action: str
    signal: str
    displacement_volume: float
    secondary_displacement_risk: float

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "displacement_type": self.displacement_type,
            "region": self.region,
            "displacement_score": self.displacement_score,
            "protection_score": self.protection_score,
            "integration_score": self.integration_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "displacement_pattern": self.displacement_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "displacement_volume": self.displacement_volume,
            "secondary_displacement_risk": self.secondary_displacement_risk,
        }


class RefugeeCrisisEngine:
    def __init__(self) -> None:
        self._results: list[RefugeeCrisisResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: RefugeeCrisisInput) -> RefugeeCrisisResult:
        displacement = self._displacement_score(inp)
        protection   = self._protection_score(inp)
        integration  = self._integration_score(inp)
        systemic     = self._systemic_score(inp)
        composite    = self._composite(displacement, protection, integration, systemic)
        risk_level   = self._risk_level(composite)
        pattern      = self._displacement_pattern(inp)
        severity     = self._severity(risk_level)
        action       = self._recommended_action(risk_level)
        signal       = self._signal(risk_level)

        result = RefugeeCrisisResult(
            entity_id=inp.entity_id,
            displacement_type=inp.displacement_type,
            region=inp.region,
            displacement_score=displacement,
            protection_score=protection,
            integration_score=integration,
            systemic_score=systemic,
            composite_score=composite,
            risk_level=risk_level,
            displacement_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            displacement_volume=inp.displacement_volume,
            secondary_displacement_risk=inp.secondary_displacement_risk,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[RefugeeCrisisInput]) -> list[RefugeeCrisisResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _displacement_score(self, inp: RefugeeCrisisInput) -> float:
        score = (
            inp.displacement_volume * 0.4
            + inp.climate_displacement_acceleration * 0.35
            + inp.conflict_displacement_intensity * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _protection_score(self, inp: RefugeeCrisisInput) -> float:
        score = (
            inp.trafficking_vulnerability * 0.4
            + inp.border_militarization_harm * 0.35
            + inp.statelessness_risk * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _integration_score(self, inp: RefugeeCrisisInput) -> float:
        score = (
            inp.refugee_integration_failure * 0.4
            + inp.economic_exclusion_refugees * 0.35
            + inp.education_access_gap * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _systemic_score(self, inp: RefugeeCrisisInput) -> float:
        score = (
            inp.asylum_system_collapse * 0.4
            + inp.UNHCR_funding_gap * 0.35
            + inp.xenophobia_political_backlash * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _composite(
        self,
        displacement: float,
        protection: float,
        integration: float,
        systemic: float,
    ) -> float:
        composite = (
            displacement * 0.30
            + protection * 0.25
            + integration * 0.25
            + systemic * 0.20
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

    def _displacement_pattern(self, inp: RefugeeCrisisInput) -> str:
        if inp.climate_displacement_acceleration > 0.85 and inp.displacement_volume > 0.80:
            return "climate_mass_displacement"
        if inp.asylum_system_collapse > 0.85 and inp.host_country_capacity_overflow > 0.80:
            return "asylum_system_implosion"
        if inp.statelessness_risk > 0.85 and inp.return_impossibility > 0.80:
            return "statelessness_crisis"
        if inp.trafficking_vulnerability > 0.80 and inp.border_militarization_harm > 0.75:
            return "refugee_trafficking_epidemic"
        if inp.protracted_displacement_duration > 0.80 and inp.economic_exclusion_refugees > 0.75:
            return "protracted_displacement_trap"
        return "none"

    def _severity(self, risk_level: str) -> str:
        return {
            "critical": "crise_déplacement_catastrophique",
            "high":     "déplacement_forcé_majeur",
            "moderate": "vulnérabilité_réfugiés_active",
            "low":      "déplacement_contenu",
        }[risk_level]

    def _recommended_action(self, risk_level: str) -> str:
        return {
            "critical": "intervention_humanitaire_urgente",
            "high":     "mobilisation_protection_internationale",
            "moderate": "renforcement_dispositif_accueil",
            "low":      "veille_déplacement_préventive",
        }[risk_level]

    def _signal(self, risk_level: str) -> str:
        return {
            "critical": "🔴 Crise déplacement catastrophique — intervention humanitaire d'urgence requise",
            "high":     "🟠 Déplacement forcé majeur détecté — mobilisation internationale nécessaire",
            "moderate": "🟡 Vulnérabilité réfugiés active — renforcement du dispositif d'accueil",
            "low":      "🟢 Déplacement contenu — veille préventive maintenue",
        }[risk_level]

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "module_id": 385,
                "module_name": "Global Refugee Crisis & Forced Displacement Intelligence Engine",
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
                "avg_estimated_displacement_index": 0.0,
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
            pattern_distribution[r.displacement_pattern] = pattern_distribution.get(r.displacement_pattern, 0) + 1
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
            "module_id": 385,
            "module_name": "Global Refugee Crisis & Forced Displacement Intelligence Engine",
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
            "avg_estimated_displacement_index": round(avg_composite / 100 * 10, 2),
        }
