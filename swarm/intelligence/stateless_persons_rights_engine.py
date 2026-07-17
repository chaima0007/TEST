from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class StatelessPersonsRightsEntity:
    entity_id: str
    name: str
    country: str
    statelessness_documentation_denial_severity_score: float
    arbitrary_detention_deportation_stateless_scale_score: float
    birth_registration_nationality_access_gap_score: float
    stateless_children_education_rights_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_stateless_persons_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.statelessness_documentation_denial_severity_score * 0.30
            + self.arbitrary_detention_deportation_stateless_scale_score * 0.25
            + self.birth_registration_nationality_access_gap_score * 0.25
            + self.stateless_children_education_rights_deficit_gap_score * 0.20,
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
        self.estimated_stateless_persons_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class StatelessPersonsRightsEngineResult:
    agent: str = "Stateless Persons Rights Engine Agent"
    domain: str = "stateless_persons_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_stateless_persons_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[StatelessPersonsRightsEntity] = field(default_factory=list)


def run_stateless_persons_rights_engine() -> StatelessPersonsRightsEngineResult:
    entities = [
        StatelessPersonsRightsEntity(
            entity_id="SPR-001",
            name="Myanmar/Rohingya — Apatridie Légale 1982, Carte Identité NV Refusée, Camps Concentration & Génocide Documentation",
            country="Myanmar",
            statelessness_documentation_denial_severity_score=95.0,
            arbitrary_detention_deportation_stateless_scale_score=93.0,
            birth_registration_nationality_access_gap_score=92.0,
            stateless_children_education_rights_deficit_gap_score=91.0,
            primary_pattern="statelessness_documentation_denial_severity",
        ),
        StatelessPersonsRightsEntity(
            entity_id="SPR-002",
            name="Koweït/Bidoun — 100 000 Apatrides Bidoun Légaux, Pas Passeports, Enfants Non Enregistrés & Discrimination Systémique",
            country="Koweït",
            statelessness_documentation_denial_severity_score=91.0,
            arbitrary_detention_deportation_stateless_scale_score=89.0,
            birth_registration_nationality_access_gap_score=90.0,
            stateless_children_education_rights_deficit_gap_score=88.0,
            primary_pattern="birth_registration_nationality_access_gap",
        ),
        StatelessPersonsRightsEntity(
            entity_id="SPR-003",
            name="Éthiopie/Érythrée — Rapatriés Déchus Citoyenneté 1998, Binationaux Expulsés & Générations Apatrides Conflits",
            country="Éthiopie",
            statelessness_documentation_denial_severity_score=87.0,
            arbitrary_detention_deportation_stateless_scale_score=86.0,
            birth_registration_nationality_access_gap_score=85.0,
            stateless_children_education_rights_deficit_gap_score=84.0,
            primary_pattern="arbitrary_detention_deportation_stateless_scale",
        ),
        StatelessPersonsRightsEntity(
            entity_id="SPR-004",
            name="Dom. Rep./Haïtiens — Arrêt 168-13 Rétroactif 1929, 200k Stateless Haïtiano-Dominicains & Registres Refus",
            country="Rép. Dominicaine",
            statelessness_documentation_denial_severity_score=84.0,
            arbitrary_detention_deportation_stateless_scale_score=82.0,
            birth_registration_nationality_access_gap_score=83.0,
            stateless_children_education_rights_deficit_gap_score=81.0,
            primary_pattern="statelessness_documentation_denial_severity",
        ),
        StatelessPersonsRightsEntity(
            entity_id="SPR-005",
            name="Thaïlande/Minorités — Tribus Montagnardes Apatrides, 480 000 Sans Nationalité, Travail Enfant & Accès Éducation Refusé",
            country="Thaïlande",
            statelessness_documentation_denial_severity_score=56.0,
            arbitrary_detention_deportation_stateless_scale_score=54.0,
            birth_registration_nationality_access_gap_score=53.0,
            stateless_children_education_rights_deficit_gap_score=55.0,
            primary_pattern="stateless_children_education_rights_deficit_gap",
        ),
        StatelessPersonsRightsEntity(
            entity_id="SPR-006",
            name="Europe/Roms — Roms Apatrides Est-Europe, Enregistrement Naissance Refus, Discrimination Institutionnelle & Expulsions Massives",
            country="Europe",
            statelessness_documentation_denial_severity_score=52.0,
            arbitrary_detention_deportation_stateless_scale_score=51.0,
            birth_registration_nationality_access_gap_score=53.0,
            stateless_children_education_rights_deficit_gap_score=50.0,
            primary_pattern="birth_registration_nationality_access_gap",
        ),
        StatelessPersonsRightsEntity(
            entity_id="SPR-007",
            name="UNHCR/ENS — #IBelong 2024-2024, European Network on Statelessness, Mesures Réduction & Procédures Détermination Apatridie",
            country="Global",
            statelessness_documentation_denial_severity_score=27.0,
            arbitrary_detention_deportation_stateless_scale_score=26.0,
            birth_registration_nationality_access_gap_score=25.0,
            stateless_children_education_rights_deficit_gap_score=28.0,
            primary_pattern="statelessness_documentation_denial_severity",
        ),
        StatelessPersonsRightsEntity(
            entity_id="SPR-008",
            name="ONU/Conv 1954 — Convention Apatridie 1954 & 1961, UNHCR Mandat, Art.1 Définition & Protocole Réduction Apatridie",
            country="Global",
            statelessness_documentation_denial_severity_score=4.0,
            arbitrary_detention_deportation_stateless_scale_score=4.0,
            birth_registration_nationality_access_gap_score=4.0,
            stateless_children_education_rights_deficit_gap_score=4.0,
            primary_pattern="arbitrary_detention_deportation_stateless_scale",
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

    return StatelessPersonsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_stateless_persons_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_statelessness_global_report",
            "european_network_on_statelessness_report",
            "human_rights_watch_rohingya_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_stateless_persons_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_stateless_persons_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
