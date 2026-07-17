from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#38bdf8"


@dataclass
class StatelessChildrenRightsEntity:
    entity_id: str
    name: str
    country: str
    birth_registration_denial_score: float
    childhood_statelessness_score: float
    education_denial_score: float
    healthcare_exclusion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_stateless_children_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.birth_registration_denial_score * 0.30
            + self.childhood_statelessness_score * 0.25
            + self.education_denial_score * 0.25
            + self.healthcare_exclusion_score * 0.20,
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
        self.estimated_stateless_children_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class StatelessChildrenRightsEngineResult:
    agent: str = "Stateless Children Rights Engine Agent"
    domain: str = "stateless_children_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_stateless_children_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[StatelessChildrenRightsEntity] = field(default_factory=list)


def run_stateless_children_rights_engine() -> StatelessChildrenRightsEngineResult:
    entities = [
        StatelessChildrenRightsEntity(
            entity_id="SCR-001",
            name="Bangladesh — Rohingyas Apatrides, 700 000 Enfants Sans Nationalité Myanmar, Enregistrements Naissance Refusés",
            country="Bangladesh",
            birth_registration_denial_score=95.0,
            childhood_statelessness_score=94.0,
            education_denial_score=92.0,
            healthcare_exclusion_score=91.0,
            primary_pattern="birth_registration_denial_score",
        ),
        StatelessChildrenRightsEntity(
            entity_id="SCR-002",
            name="Émirats Arabes Unis — Bidun, Enfants Apatrides 2e Génération 100 000+, Certificats Naissance Systématiquement Refusés",
            country="Émirats Arabes Unis",
            birth_registration_denial_score=92.0,
            childhood_statelessness_score=90.0,
            education_denial_score=86.0,
            healthcare_exclusion_score=88.0,
            primary_pattern="birth_registration_denial_score",
        ),
        StatelessChildrenRightsEntity(
            entity_id="SCR-003",
            name="Kuwait — Bidun, 88 000 Enfants Apatrides Sans Certificats Naissance, Exclusion Totale Droits Civils",
            country="Kuwait",
            birth_registration_denial_score=90.0,
            childhood_statelessness_score=88.0,
            education_denial_score=84.0,
            healthcare_exclusion_score=86.0,
            primary_pattern="childhood_statelessness_score",
        ),
        StatelessChildrenRightsEntity(
            entity_id="SCR-004",
            name="Thaïlande — Enfants Tribaux des Montagnes, 200 000 Sans Papiers Apatrides, Accès Éducation et Santé Bloqué",
            country="Thaïlande",
            birth_registration_denial_score=84.0,
            childhood_statelessness_score=82.0,
            education_denial_score=80.0,
            healthcare_exclusion_score=78.0,
            primary_pattern="birth_registration_denial_score",
        ),
        StatelessChildrenRightsEntity(
            entity_id="SCR-005",
            name="République Dominicaine — Enfants Haïtiens Déchus Nationalité Rétroactivement, 200 000 Rendus Apatrides",
            country="République Dominicaine",
            birth_registration_denial_score=55.0,
            childhood_statelessness_score=52.0,
            education_denial_score=48.0,
            healthcare_exclusion_score=50.0,
            primary_pattern="birth_registration_denial_score",
        ),
        StatelessChildrenRightsEntity(
            entity_id="SCR-006",
            name="Côte d'Ivoire — Apatrides Droits de Filiation, Dioula et Autres Communautés, Enregistrement Naissance Discriminatoire",
            country="Côte d'Ivoire",
            birth_registration_denial_score=48.0,
            childhood_statelessness_score=45.0,
            education_denial_score=43.0,
            healthcare_exclusion_score=42.0,
            primary_pattern="childhood_statelessness_score",
        ),
        StatelessChildrenRightsEntity(
            entity_id="SCR-007",
            name="USA — Enfants Sans Papiers de Parents Sans Statut, Limbes Légaux, Risque Apatridie de Facto Documenté",
            country="USA",
            birth_registration_denial_score=32.0,
            childhood_statelessness_score=29.0,
            education_denial_score=26.0,
            healthcare_exclusion_score=28.0,
            primary_pattern="birth_registration_denial_score",
        ),
        StatelessChildrenRightsEntity(
            entity_id="SCR-008",
            name="Finlande — Procédure Accélérée Apatridie, Meilleure Pratique UNHCR, Enregistrement Naissance Universel Garanti",
            country="Finlande",
            birth_registration_denial_score=8.0,
            childhood_statelessness_score=7.0,
            education_denial_score=6.0,
            healthcare_exclusion_score=7.0,
            primary_pattern="birth_registration_denial_score",
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

    return StatelessChildrenRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_stateless_children_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_statelessness_global_action_plan_2024",
            "unicef_birth_registration_global_report",
            "global_campaign_equal_nationality_rights",
            "un_crc_general_comment_statelessness_children",
            "institute_statelessness_inclusion_global_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_stateless_children_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
