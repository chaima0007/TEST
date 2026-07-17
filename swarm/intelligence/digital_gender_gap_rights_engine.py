from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DigitalGenderGapRightsEntity:
    entity_id: str
    name: str
    country: str
    internet_access_gender_gap_severity_score: float
    digital_skills_training_exclusion_scale_score: float
    online_harassment_safety_barrier_score: float
    platform_policy_gender_bias_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_digital_gender_gap_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.internet_access_gender_gap_severity_score * 0.30
            + self.digital_skills_training_exclusion_scale_score * 0.25
            + self.online_harassment_safety_barrier_score * 0.25
            + self.platform_policy_gender_bias_gap_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_digital_gender_gap_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class DigitalGenderGapRightsEngineResult:
    agent: str = "Digital Gender Gap Rights Engine Agent"
    domain: str = "digital_gender_gap_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_digital_gender_gap_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalGenderGapRightsEntity] = field(default_factory=list)

def run_digital_gender_gap_rights_engine() -> DigitalGenderGapRightsEngineResult:
    entities = [
        DigitalGenderGapRightsEntity(
            entity_id="DGG-001",
            name="Afrique Sub-Saharienne — Fracture Numérique Genre 36% Moins Femmes En Ligne & Zéro Formation Digitale",
            country="Afrique Sub-Saharienne",
            internet_access_gender_gap_severity_score=96.0,
            digital_skills_training_exclusion_scale_score=92.0,
            online_harassment_safety_barrier_score=91.0,
            platform_policy_gender_bias_gap_score=90.0,
            primary_pattern="internet_access_gender_gap_severity",
        ),
        DigitalGenderGapRightsEntity(
            entity_id="DGG-002",
            name="Asie du Sud — 67% Femmes Sans Internet, Harcèlement Mobile & Normes Patriarcales Numériques",
            country="Asie du Sud",
            internet_access_gender_gap_severity_score=93.0,
            digital_skills_training_exclusion_scale_score=89.0,
            online_harassment_safety_barrier_score=90.0,
            platform_policy_gender_bias_gap_score=88.0,
            primary_pattern="internet_access_gender_gap_severity",
        ),
        DigitalGenderGapRightsEntity(
            entity_id="DGG-003",
            name="Moyen-Orient — Contrôle Masculin Accès Web, Surveillance Digitale Femmes & Censure Contenu Féminin",
            country="Moyen-Orient",
            internet_access_gender_gap_severity_score=91.0,
            digital_skills_training_exclusion_scale_score=87.0,
            online_harassment_safety_barrier_score=88.0,
            platform_policy_gender_bias_gap_score=86.0,
            primary_pattern="online_harassment_safety_barrier",
        ),
        DigitalGenderGapRightsEntity(
            entity_id="DGG-004",
            name="Asie du Sud-Est — Harcèlement En Ligne Systémique, Exclusion STEM & Biais Algorithmes Emploi",
            country="Asie du Sud-Est",
            internet_access_gender_gap_severity_score=88.0,
            digital_skills_training_exclusion_scale_score=84.0,
            online_harassment_safety_barrier_score=86.0,
            platform_policy_gender_bias_gap_score=82.0,
            primary_pattern="digital_skills_training_exclusion_scale",
        ),
        DigitalGenderGapRightsEntity(
            entity_id="DGG-005",
            name="Amérique Latine — Violence Numérique Genrée, Deepfakes Non Consensuels & Impunité Plateformes",
            country="Amérique Latine",
            internet_access_gender_gap_severity_score=55.0,
            digital_skills_training_exclusion_scale_score=52.0,
            online_harassment_safety_barrier_score=54.0,
            platform_policy_gender_bias_gap_score=50.0,
            primary_pattern="online_harassment_safety_barrier",
        ),
        DigitalGenderGapRightsEntity(
            entity_id="DGG-006",
            name="Europe de l'Est — Sous-Représentation Tech Femmes, Harcèlement Politique En Ligne & Gender Pay Gap IA",
            country="Europe de l'Est",
            internet_access_gender_gap_severity_score=54.0,
            digital_skills_training_exclusion_scale_score=51.0,
            online_harassment_safety_barrier_score=52.0,
            platform_policy_gender_bias_gap_score=49.0,
            primary_pattern="platform_policy_gender_bias_gap",
        ),
        DigitalGenderGapRightsEntity(
            entity_id="DGG-007",
            name="Alliance4AI/Web Foundation — Droits Femmes En Ligne, Formation Digitale & Plaidoyer Plateformes",
            country="Global",
            internet_access_gender_gap_severity_score=22.0,
            digital_skills_training_exclusion_scale_score=28.0,
            online_harassment_safety_barrier_score=27.0,
            platform_policy_gender_bias_gap_score=30.0,
            primary_pattern="platform_policy_gender_bias_gap",
        ),
        DigitalGenderGapRightsEntity(
            entity_id="DGG-008",
            name="ONU/ITU — Rapport Genre Numérique, SDG 5.b Accès TIC & Recommandations Politiques Inclusives",
            country="Global",
            internet_access_gender_gap_severity_score=4.0,
            digital_skills_training_exclusion_scale_score=5.0,
            online_harassment_safety_barrier_score=4.0,
            platform_policy_gender_bias_gap_score=5.0,
            primary_pattern="internet_access_gender_gap_severity",
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return DigitalGenderGapRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_digital_gender_gap_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "itu_measuring_digital_development_gender_gap_report",
            "web_foundation_womens_rights_online_access_barriers_study",
            "plan_international_online_safety_girls_harassment_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_digital_gender_gap_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_digital_gender_gap_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
