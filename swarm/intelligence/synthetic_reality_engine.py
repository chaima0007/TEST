"""
Module 378 — Synthetic Reality & Deepfake Economy Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SyntheticRealityInput:
    entity_id: str
    media_domain: str
    region: str
    deepfake_saturation_level: float
    reality_consensus_erosion: float
    political_deepfake_weaponization: float
    financial_fraud_deepfake: float
    identity_theft_synthetic: float
    consent_violation_synthetic_media: float
    detection_technology_gap: float
    celebrity_non_consent: float
    synthetic_evidence_falsification: float
    emotional_manipulation_capacity: float
    reality_verification_collapse: float
    AI_media_monopoly: float
    deepfake_criminalization_failure: float
    synthetic_pornography_harm: float
    geopolitical_deepfake_incidents: float
    economic_deepfake_fraud_scale: float
    social_trust_erosion: float


@dataclass
class SyntheticRealityResult:
    entity_id: str
    media_domain: str
    region: str
    saturation_score: float
    trust_score: float
    fraud_score: float
    weaponization_score: float
    composite_score: float
    risk_level: str
    synthetic_pattern: str
    severity: str
    recommended_action: str
    signal: str
    deepfake_saturation_level: float
    social_trust_erosion: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "media_domain": self.media_domain,
            "region": self.region,
            "saturation_score": self.saturation_score,
            "trust_score": self.trust_score,
            "fraud_score": self.fraud_score,
            "weaponization_score": self.weaponization_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "synthetic_pattern": self.synthetic_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "deepfake_saturation_level": self.deepfake_saturation_level,
            "social_trust_erosion": self.social_trust_erosion,
        }


def _saturation_score(e: SyntheticRealityInput) -> float:
    raw = (
        e.deepfake_saturation_level * 0.40
        + e.consent_violation_synthetic_media * 0.35
        + e.celebrity_non_consent * 0.25
    ) * 100
    return round(raw * 100) / 100


def _trust_score(e: SyntheticRealityInput) -> float:
    raw = (
        e.social_trust_erosion * 0.40
        + e.reality_consensus_erosion * 0.35
        + e.reality_verification_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _fraud_score(e: SyntheticRealityInput) -> float:
    raw = (
        e.financial_fraud_deepfake * 0.40
        + e.identity_theft_synthetic * 0.35
        + e.economic_deepfake_fraud_scale * 0.25
    ) * 100
    return round(raw * 100) / 100


def _weaponization_score(e: SyntheticRealityInput) -> float:
    raw = (
        e.political_deepfake_weaponization * 0.40
        + e.geopolitical_deepfake_incidents * 0.35
        + e.synthetic_evidence_falsification * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(saturation: float, trust: float, fraud: float, weaponization: float) -> float:
    return round((saturation * 0.30 + trust * 0.25 + fraud * 0.25 + weaponization * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _synthetic_pattern(e: SyntheticRealityInput) -> str:
    if e.reality_consensus_erosion > 0.85 and e.reality_verification_collapse > 0.80:
        return "reality_consensus_collapse"
    if e.political_deepfake_weaponization > 0.85 and e.geopolitical_deepfake_incidents > 0.80:
        return "political_deepfake_crisis"
    if e.financial_fraud_deepfake > 0.85 and e.economic_deepfake_fraud_scale > 0.80:
        return "synthetic_fraud_epidemic"
    if e.synthetic_evidence_falsification > 0.80 and e.deepfake_criminalization_failure > 0.75:
        return "synthetic_evidence_crisis"
    if e.AI_media_monopoly > 0.80 and e.detection_technology_gap > 0.75:
        return "AI_media_monopoly_capture"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_réalité_systémique"
    if composite >= 40:
        return "crise_deepfake_majeure"
    if composite >= 20:
        return "économie_synthétique_active"
    return "réalité_synthétique_contenue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_réalité_urgente"
    if risk == "high":
        return "contre-mesures_deepfake_activées"
    if risk == "moderate":
        return "renforcement_détection_synthétique"
    return "veille_réalité_synthétique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Effondrement réalité systémique — deepfake critique"
    if risk == "high":
        return "🟠 Crise deepfake majeure détectée"
    if risk == "moderate":
        return "🟡 Économie synthétique active"
    return "🟢 Réalité synthétique relativement contenue"


def analyze_entity(e: SyntheticRealityInput) -> SyntheticRealityResult:
    saturation = _saturation_score(e)
    trust = _trust_score(e)
    fraud = _fraud_score(e)
    weaponization = _weaponization_score(e)
    comp = _composite(saturation, trust, fraud, weaponization)
    risk = _risk_level(comp)
    pattern = _synthetic_pattern(e)
    sev = _severity(comp)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SyntheticRealityResult(
        entity_id=e.entity_id,
        media_domain=e.media_domain,
        region=e.region,
        saturation_score=saturation,
        trust_score=trust,
        fraud_score=fraud,
        weaponization_score=weaponization,
        composite_score=comp,
        risk_level=risk,
        synthetic_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        deepfake_saturation_level=e.deepfake_saturation_level,
        social_trust_erosion=e.social_trust_erosion,
    )


class SyntheticRealityEngine:
    def analyze(self, entities: List[SyntheticRealityInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in entities]
        entity_dicts = [r.to_dict() for r in results]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.synthetic_pattern] = pattern_distribution.get(r.synthetic_pattern, 0) + 1
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

        n = len(results)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        smry = self.summary(
            results=results,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
            avg_composite=avg_composite,
            pattern_distribution=pattern_distribution,
            risk_distribution=risk_distribution,
            severity_distribution=severity_distribution,
            action_distribution=action_distribution,
        )

        return {"entities": entity_dicts, "summary": smry}

    def summary(
        self,
        results: List[SyntheticRealityResult],
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
        avg_composite: float,
        pattern_distribution: Dict[str, int],
        risk_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
    ) -> Dict[str, Any]:
        return {
            "module_id": 378,
            "module_name": "Synthetic Reality & Deepfake Economy Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_synthetic_reality_index": round(avg_composite / 100 * 10, 2),
        }
