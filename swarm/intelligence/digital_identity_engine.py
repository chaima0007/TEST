from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DigitalIdentityInput:
    entity_id: str
    identity_system: str
    region: str
    # 17 float fields 0-1
    biometric_surveillance_integration: float
    identity_monopoly_capture: float
    exclusion_risk: float
    data_breach_vulnerability: float
    government_identity_coercion: float
    private_identity_capture: float
    interoperability_failure: float
    self_sovereign_suppression: float
    digital_twin_identity_risk: float
    demographic_targeting_capacity: float
    identity_weaponization_risk: float
    stateless_person_exclusion: float
    cross_border_identity_friction: float
    consent_identity_erosion: float
    algorithmic_identity_discrimination: float
    identity_theft_amplification: float
    democratic_identity_manipulation: float


@dataclass
class DigitalIdentityResult:
    entity_id: str
    identity_system: str
    region: str
    surveillance_score: float
    exclusion_score: float
    sovereignty_score: float
    weaponization_score: float
    composite_score: float
    risk_level: str
    identity_pattern: str
    severity: str
    recommended_action: str
    signal: str
    biometric_surveillance_integration: float
    identity_weaponization_risk: float

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "identity_system": self.identity_system,
            "region": self.region,
            "surveillance_score": self.surveillance_score,
            "exclusion_score": self.exclusion_score,
            "sovereignty_score": self.sovereignty_score,
            "weaponization_score": self.weaponization_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "identity_pattern": self.identity_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "biometric_surveillance_integration": self.biometric_surveillance_integration,
            "identity_weaponization_risk": self.identity_weaponization_risk,
        }


class DigitalIdentityEngine:
    def __init__(self) -> None:
        self._results: list[DigitalIdentityResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: DigitalIdentityInput) -> DigitalIdentityResult:
        surveillance  = self._surveillance_score(inp)
        exclusion     = self._exclusion_score(inp)
        sovereignty   = self._sovereignty_score(inp)
        weaponization = self._weaponization_score(inp)
        composite     = self._composite(surveillance, exclusion, sovereignty, weaponization)
        risk_level    = self._risk_level(composite)
        pattern       = self._identity_pattern(inp)
        severity      = self._severity(risk_level)
        action        = self._recommended_action(risk_level)
        signal        = self._signal(risk_level)

        result = DigitalIdentityResult(
            entity_id=inp.entity_id,
            identity_system=inp.identity_system,
            region=inp.region,
            surveillance_score=surveillance,
            exclusion_score=exclusion,
            sovereignty_score=sovereignty,
            weaponization_score=weaponization,
            composite_score=composite,
            risk_level=risk_level,
            identity_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            biometric_surveillance_integration=inp.biometric_surveillance_integration,
            identity_weaponization_risk=inp.identity_weaponization_risk,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[DigitalIdentityInput]) -> list[DigitalIdentityResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _surveillance_score(self, inp: DigitalIdentityInput) -> float:
        score = (
            inp.biometric_surveillance_integration * 0.40
            + inp.government_identity_coercion * 0.35
            + inp.digital_twin_identity_risk * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _exclusion_score(self, inp: DigitalIdentityInput) -> float:
        score = (
            inp.exclusion_risk * 0.40
            + inp.stateless_person_exclusion * 0.35
            + inp.interoperability_failure * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _sovereignty_score(self, inp: DigitalIdentityInput) -> float:
        score = (
            inp.self_sovereign_suppression * 0.40
            + inp.consent_identity_erosion * 0.35
            + inp.private_identity_capture * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _weaponization_score(self, inp: DigitalIdentityInput) -> float:
        score = (
            inp.identity_weaponization_risk * 0.40
            + inp.democratic_identity_manipulation * 0.35
            + inp.demographic_targeting_capacity * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _composite(
        self,
        surveillance: float,
        exclusion: float,
        sovereignty: float,
        weaponization: float,
    ) -> float:
        composite = (
            surveillance  * 0.30
            + exclusion   * 0.25
            + sovereignty * 0.25
            + weaponization * 0.20
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

    def _identity_pattern(self, inp: DigitalIdentityInput) -> str:
        if inp.biometric_surveillance_integration > 0.85 and inp.government_identity_coercion > 0.80:
            return "biometric_surveillance_state"
        if inp.identity_monopoly_capture > 0.85 and inp.private_identity_capture > 0.80:
            return "identity_monopoly_empire"
        if inp.exclusion_risk > 0.85 and inp.stateless_person_exclusion > 0.80:
            return "identity_exclusion_crisis"
        if inp.identity_weaponization_risk > 0.80 and inp.democratic_identity_manipulation > 0.75:
            return "identity_weaponization"
        if inp.self_sovereign_suppression > 0.80 and inp.consent_identity_erosion > 0.75:
            return "sovereign_identity_collapse"
        return "none"

    def _severity(self, risk_level: str) -> str:
        return {
            "critical": "souveraineté_identitaire_effondrée",
            "high":     "identité_numérique_sous_contrôle",
            "moderate": "vulnérabilité_identitaire_structurelle",
            "low":      "risque_identitaire_contenu",
        }[risk_level]

    def _recommended_action(self, risk_level: str) -> str:
        return {
            "critical": "restauration_souveraineté_identitaire_urgente",
            "high":     "protection_identité_décentralisée",
            "moderate": "renforcement_droits_identitaires",
            "low":      "veille_identité_numérique",
        }[risk_level]

    def _signal(self, risk_level: str) -> str:
        return {
            "critical": "🔴 Souveraineté identitaire effondrée — contrôle systémique de l'identité",
            "high":     "🟠 Identité numérique sous contrôle avancé détecté",
            "moderate": "🟡 Vulnérabilité identitaire structurelle active",
            "low":      "🟢 Risque identitaire limité et contenu",
        }[risk_level]

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "module_id": 376,
                "module_name": "Digital Identity & Decentralized Sovereignty Intelligence Engine",
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
                "avg_estimated_identity_sovereignty_index": 0.0,
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
            pattern_distribution[r.identity_pattern] = pattern_distribution.get(r.identity_pattern, 0) + 1
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
            "module_id": 376,
            "module_name": "Digital Identity & Decentralized Sovereignty Intelligence Engine",
            "total": n,
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_identity_sovereignty_index": round(avg_composite / 100 * 10, 2),
        }
