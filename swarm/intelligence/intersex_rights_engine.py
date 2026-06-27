from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class IntersexRightsEntity:
    entity_id: str
    name: str
    country: str
    non_consensual_surgery_prevalence_score: float
    legal_protection_absence_score: float
    medical_pathologization_harm_score: float
    identity_documentation_barrier_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_intersex_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.non_consensual_surgery_prevalence_score * 0.30
            + self.legal_protection_absence_score * 0.25
            + self.medical_pathologization_harm_score * 0.25
            + self.identity_documentation_barrier_score * 0.20,
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
        self.estimated_intersex_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class IntersexRightsEngineResult:
    agent: str = "Intersex Rights Engine Agent"
    domain: str = "intersex_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_intersex_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IntersexRightsEntity] = field(default_factory=list)

def run_intersex_rights_engine() -> IntersexRightsEngineResult:
    entities = [
        IntersexRightsEntity(
            entity_id="IX-001",
            name="USA — 2 Chirurgies/Jour Nourrissons Intersexes, Aucune Loi Fédérale & AAP Non Réformée",
            country="Amérique du Nord",
            non_consensual_surgery_prevalence_score=95.0,
            legal_protection_absence_score=95.0,
            medical_pathologization_harm_score=92.0,
            identity_documentation_barrier_score=88.0,
            primary_pattern="non_consensual_surgery_prevalence",
        ),
        IntersexRightsEntity(
            entity_id="IX-002",
            name="Allemagne — Pratiques Chirurgicales Persistent Malgré Loi 2021, Impunité Médicale & Sous-Déclaration",
            country="Europe",
            non_consensual_surgery_prevalence_score=88.0,
            legal_protection_absence_score=85.0,
            medical_pathologization_harm_score=90.0,
            identity_documentation_barrier_score=85.0,
            primary_pattern="medical_pathologization_harm",
        ),
        IntersexRightsEntity(
            entity_id="IX-003",
            name="Chine & Asie Est — Normalisations Génitales Systémiques, Absence Données & Tabou Culturel",
            country="Asie de l'Est",
            non_consensual_surgery_prevalence_score=90.0,
            legal_protection_absence_score=90.0,
            medical_pathologization_harm_score=85.0,
            identity_documentation_barrier_score=88.0,
            primary_pattern="legal_protection_absence",
        ),
        IntersexRightsEntity(
            entity_id="IX-004",
            name="Brésil — 2000 Chirurgies/An DSD Non Éthiques, Protocoles Pathologisants & Plaintes Ignorées",
            country="Amérique Latine",
            non_consensual_surgery_prevalence_score=85.0,
            legal_protection_absence_score=82.0,
            medical_pathologization_harm_score=85.0,
            identity_documentation_barrier_score=82.0,
            primary_pattern="non_consensual_surgery_prevalence",
        ),
        IntersexRightsEntity(
            entity_id="IX-005",
            name="France — Loi 2021 Partielle, Chirurgies Continuent Sur Mineurs & Défenseure Droits Saisie",
            country="Europe",
            non_consensual_surgery_prevalence_score=55.0,
            legal_protection_absence_score=52.0,
            medical_pathologization_harm_score=55.0,
            identity_documentation_barrier_score=50.0,
            primary_pattern="non_consensual_surgery_prevalence",
        ),
        IntersexRightsEntity(
            entity_id="IX-006",
            name="Australie — Rapport Sénat 2013 Partiellement Ignoré, Tutelles Judiciaires & Réforme Lente",
            country="Océanie",
            non_consensual_surgery_prevalence_score=48.0,
            legal_protection_absence_score=50.0,
            medical_pathologization_harm_score=50.0,
            identity_documentation_barrier_score=52.0,
            primary_pattern="identity_documentation_barrier",
        ),
        IntersexRightsEntity(
            entity_id="IX-007",
            name="OII/ILGA World — Campagne EndIntersexSurgeries, Standards Droits Intersexes & Monitoring États",
            country="Global",
            non_consensual_surgery_prevalence_score=22.0,
            legal_protection_absence_score=28.0,
            medical_pathologization_harm_score=25.0,
            identity_documentation_barrier_score=30.0,
            primary_pattern="legal_protection_absence",
        ),
        IntersexRightsEntity(
            entity_id="IX-008",
            name="ONU/CRC & CRPD — Recommandations Chirurgies Intersexes, Art.19 Intégrité Corporelle Enfants",
            country="Global",
            non_consensual_surgery_prevalence_score=4.0,
            legal_protection_absence_score=5.0,
            medical_pathologization_harm_score=3.0,
            identity_documentation_barrier_score=6.0,
            primary_pattern="identity_documentation_barrier",
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

    return IntersexRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_intersex_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "oii_europe_intersex_human_rights_violations_country_report",
            "ilga_world_state_sponsored_homophobia_intersex_report",
            "un_crc_crpd_concluding_observations_intersex_children_surgery",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_intersex_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_intersex_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
