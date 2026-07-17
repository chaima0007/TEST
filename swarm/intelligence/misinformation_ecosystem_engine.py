"""
Module 355 — Misinformation Ecosystem & Truth Collapse Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MisinformationEcosystemInput:
    entity_id: str
    info_domain: str
    region: str
    viral_misinformation_velocity: float
    fact_checking_infrastructure_gap: float
    platform_amplification_bias: float
    coordinated_inauthentic_behavior_level: float
    epistemic_bubble_density: float
    source_trust_collapse_index: float
    AI_generated_misinformation_volume: float
    bot_network_coordination_intensity: float
    media_literacy_deficit: float
    state_sponsored_disinformation_scale: float
    scientific_consensus_attack_rate: float
    health_misinformation_mortality: float
    financial_misinformation_market_impact: float
    algorithmic_rabbit_hole_depth: float
    truth_fatigue_index: float
    influencer_misinformation_amplification: float
    counter_narrative_suppression: float


@dataclass
class MisinformationEcosystemResult:
    entity_id: str
    info_domain: str
    region: str
    velocity_score: float
    coordination_score: float
    erosion_score: float
    defense_score: float
    composite_score: float
    risk_level: str
    misinfo_pattern: str
    severity: str
    recommended_action: str
    signal: str
    viral_misinformation_velocity: float
    source_trust_collapse_index: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "info_domain": self.info_domain,
            "region": self.region,
            "velocity_score": self.velocity_score,
            "coordination_score": self.coordination_score,
            "erosion_score": self.erosion_score,
            "defense_score": self.defense_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "misinfo_pattern": self.misinfo_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "viral_misinformation_velocity": self.viral_misinformation_velocity,
            "source_trust_collapse_index": self.source_trust_collapse_index,
        }


def _velocity_score(e: MisinformationEcosystemInput) -> float:
    raw = (
        e.viral_misinformation_velocity * 0.4
        + e.platform_amplification_bias * 0.35
        + e.AI_generated_misinformation_volume * 0.25
    ) * 100
    return round(raw * 100) / 100


def _coordination_score(e: MisinformationEcosystemInput) -> float:
    raw = (
        e.coordinated_inauthentic_behavior_level * 0.4
        + e.bot_network_coordination_intensity * 0.35
        + e.state_sponsored_disinformation_scale * 0.25
    ) * 100
    return round(raw * 100) / 100


def _erosion_score(e: MisinformationEcosystemInput) -> float:
    raw = (
        e.source_trust_collapse_index * 0.4
        + e.truth_fatigue_index * 0.35
        + e.epistemic_bubble_density * 0.25
    ) * 100
    return round(raw * 100) / 100


def _defense_score(e: MisinformationEcosystemInput) -> float:
    raw = (
        e.fact_checking_infrastructure_gap * 0.4
        + e.media_literacy_deficit * 0.35
        + e.counter_narrative_suppression * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(velocity: float, coordination: float, erosion: float, defense: float) -> float:
    return round((velocity * 0.30 + coordination * 0.25 + erosion * 0.25 + defense * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _misinfo_pattern(e: MisinformationEcosystemInput) -> str:
    if e.source_trust_collapse_index >= 0.70 and e.truth_fatigue_index >= 0.65:
        return "epistemic_collapse"
    if e.AI_generated_misinformation_volume >= 0.70 and e.platform_amplification_bias >= 0.65:
        return "AI_disinfo_saturation"
    if e.state_sponsored_disinformation_scale >= 0.70 and e.coordinated_inauthentic_behavior_level >= 0.65:
        return "state_info_warfare"
    if e.health_misinformation_mortality >= 0.70 and e.scientific_consensus_attack_rate >= 0.65:
        return "health_disinfo_crisis"
    if e.algorithmic_rabbit_hole_depth >= 0.70 and e.influencer_misinformation_amplification >= 0.65:
        return "algorithmic_radicalization"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_vérité_systémique"
    if composite >= 40:
        return "crise_désinformation_majeure"
    if composite >= 20:
        return "écosystème_désinformation_actif"
    return "désinformation_contenue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_médias_urgente"
    if risk == "high":
        return "contre-mesures_désinformation_activées"
    if risk == "moderate":
        return "renforcement_littératie_médiatique"
    return "veille_désinformation_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Effondrement vérité systémique — désinformation critique"
    if risk == "high":
        return "🟠 Crise désinformation majeure détectée"
    if risk == "moderate":
        return "🟡 Écosystème désinformation actif"
    return "🟢 Désinformation relativement contenue"


def analyze_entity(e: MisinformationEcosystemInput) -> MisinformationEcosystemResult:
    velocity = _velocity_score(e)
    coordination = _coordination_score(e)
    erosion = _erosion_score(e)
    defense = _defense_score(e)
    comp = _composite(velocity, coordination, erosion, defense)
    risk = _risk_level(comp)
    pattern = _misinfo_pattern(e)
    sev = _severity(comp)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return MisinformationEcosystemResult(
        entity_id=e.entity_id,
        info_domain=e.info_domain,
        region=e.region,
        velocity_score=velocity,
        coordination_score=coordination,
        erosion_score=erosion,
        defense_score=defense,
        composite_score=comp,
        risk_level=risk,
        misinfo_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        viral_misinformation_velocity=e.viral_misinformation_velocity,
        source_trust_collapse_index=e.source_trust_collapse_index,
    )


class MisinformationEcosystemEngine:
    def analyze(self, entities: List[MisinformationEcosystemInput]) -> Dict[str, Any]:
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
            pattern_distribution[r.misinfo_pattern] = pattern_distribution.get(r.misinfo_pattern, 0) + 1
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
        results: List[MisinformationEcosystemResult],
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
            "module_id": 355,
            "module_name": "Misinformation Ecosystem & Truth Collapse Intelligence Engine",
            "total_entities": len(results),
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_misinfo_index": round(avg_composite / 100 * 10, 2),
        }
