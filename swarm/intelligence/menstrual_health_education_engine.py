from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MenstrualHealthEducationEntity:
    entity_id: str
    name: str
    country: str
    menstrual_taboo_exclusion_severity_score: float
    education_dropout_period_poverty_score: float
    hygiene_infrastructure_denial_score: float
    healthcare_menstrual_disorder_neglect_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_menstrual_health_education_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.menstrual_taboo_exclusion_severity_score * 0.30
            + self.education_dropout_period_poverty_score * 0.25
            + self.hygiene_infrastructure_denial_score * 0.25
            + self.healthcare_menstrual_disorder_neglect_score * 0.20,
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
        self.estimated_menstrual_health_education_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class MenstrualHealthEducationEngineResult:
    agent: str = "Menstrual Health Education Engine Agent"
    domain: str = "menstrual_health_education"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_menstrual_health_education_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MenstrualHealthEducationEntity] = field(default_factory=list)

def run_menstrual_health_education_engine() -> MenstrualHealthEducationEngineResult:
    entities = [
        MenstrualHealthEducationEntity(
            entity_id="MHE-001",
            name="Népal — Chhaupadi: Exil Menstruation Cabanes, Femmes Mortes Froid/Serpents & Illégal Non Appliqué",
            country="Asie du Sud",
            menstrual_taboo_exclusion_severity_score=95.0,
            education_dropout_period_poverty_score=90.0,
            hygiene_infrastructure_denial_score=90.0,
            healthcare_menstrual_disorder_neglect_score=88.0,
            primary_pattern="menstrual_taboo_exclusion_severity",
        ),
        MenstrualHealthEducationEntity(
            entity_id="MHE-002",
            name="Inde/Bangladesh — 88% Filles Sans Serviettes Hygiéniques, 50% Écoles Sans Toilettes & Décrochage",
            country="Asie du Sud",
            menstrual_taboo_exclusion_severity_score=88.0,
            education_dropout_period_poverty_score=95.0,
            hygiene_infrastructure_denial_score=92.0,
            healthcare_menstrual_disorder_neglect_score=88.0,
            primary_pattern="education_dropout_period_poverty",
        ),
        MenstrualHealthEducationEntity(
            entity_id="MHE-003",
            name="Kenya/Afrique Sub-Saharienne — 1/10 Filles Absente École/Règles, Échange Sexe Contre Serviettes",
            country="Afrique de l'Est",
            menstrual_taboo_exclusion_severity_score=88.0,
            education_dropout_period_poverty_score=90.0,
            hygiene_infrastructure_denial_score=88.0,
            healthcare_menstrual_disorder_neglect_score=88.0,
            primary_pattern="education_dropout_period_poverty",
        ),
        MenstrualHealthEducationEntity(
            entity_id="MHE-004",
            name="Soudan/Yémen — Conflits Interrompent MHM, Camps Réfugiées Sans Sanitaires & Dignité Absente",
            country="Moyen-Orient/Afrique",
            menstrual_taboo_exclusion_severity_score=82.0,
            education_dropout_period_poverty_score=85.0,
            hygiene_infrastructure_denial_score=92.0,
            healthcare_menstrual_disorder_neglect_score=88.0,
            primary_pattern="hygiene_infrastructure_denial",
        ),
        MenstrualHealthEducationEntity(
            entity_id="MHE-005",
            name="Guatemala/Mexique Indigène — Tabous Culturels Menstruation, Exclusion Rituelle & Honte Institutionnelle",
            country="Amérique Latine",
            menstrual_taboo_exclusion_severity_score=55.0,
            education_dropout_period_poverty_score=52.0,
            hygiene_infrastructure_denial_score=52.0,
            healthcare_menstrual_disorder_neglect_score=50.0,
            primary_pattern="menstrual_taboo_exclusion_severity",
        ),
        MenstrualHealthEducationEntity(
            entity_id="MHE-006",
            name="Pakistan — Filles Abandonnent École Dès 1ères Règles, 50% Femmes Croient Menstruation Impure",
            country="Asie du Sud",
            menstrual_taboo_exclusion_severity_score=55.0,
            education_dropout_period_poverty_score=50.0,
            hygiene_infrastructure_denial_score=48.0,
            healthcare_menstrual_disorder_neglect_score=50.0,
            primary_pattern="healthcare_menstrual_disorder_neglect",
        ),
        MenstrualHealthEducationEntity(
            entity_id="MHE-007",
            name="Days for Girls/WASH NGO — Kits MHM, Éducation Menstruelle, Plaidoyer ODD 6.2 & Genre",
            country="Global",
            menstrual_taboo_exclusion_severity_score=22.0,
            education_dropout_period_poverty_score=28.0,
            hygiene_infrastructure_denial_score=25.0,
            healthcare_menstrual_disorder_neglect_score=30.0,
            primary_pattern="hygiene_infrastructure_denial",
        ),
        MenstrualHealthEducationEntity(
            entity_id="MHE-008",
            name="ONU Femmes/UNICEF — Politique MHM Globale, SDG 6.2 Genre-Sensitive WASH & Rapport 2023",
            country="Global",
            menstrual_taboo_exclusion_severity_score=4.0,
            education_dropout_period_poverty_score=5.0,
            hygiene_infrastructure_denial_score=3.0,
            healthcare_menstrual_disorder_neglect_score=6.0,
            primary_pattern="menstrual_taboo_exclusion_severity",
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

    return MenstrualHealthEducationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_menstrual_health_education_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_wash_menstrual_health_management_schools_global_report",
            "days_for_girls_period_poverty_mhm_global_monitoring",
            "un_women_menstrual_health_human_rights_framework_sdg6",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_menstrual_health_education_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_menstrual_health_education_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
