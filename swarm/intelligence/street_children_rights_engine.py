from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class StreetChildrenRightsEntity:
    entity_id: str
    name: str
    country: str
    street_exposure_protection_absence_score: float   # ×0.30
    violence_exploitation_vulnerability_score: float  # ×0.25
    access_education_services_gap_score: float        # ×0.25
    criminalization_detention_children_score: float   # ×0.20
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_street_children_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.street_exposure_protection_absence_score * 0.30
            + self.violence_exploitation_vulnerability_score * 0.25
            + self.access_education_services_gap_score * 0.25
            + self.criminalization_detention_children_score * 0.20,
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
        self.estimated_street_children_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class StreetChildrenRightsEngineResult:
    agent: str = "Street Children Rights Engine Agent"
    domain: str = "street_children_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_street_children_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[StreetChildrenRightsEntity] = field(default_factory=list)


def run_street_children_rights_engine() -> StreetChildrenRightsEngineResult:
    entities = [
        StreetChildrenRightsEntity(
            entity_id="SCR-001",
            name="Inde — 11 Millions Enfants des Rues, Travail Forcé Rag-Picking & Zéro Protection Institutionnelle",
            country="Inde",
            street_exposure_protection_absence_score=95.0,
            violence_exploitation_vulnerability_score=93.0,
            access_education_services_gap_score=91.0,
            criminalization_detention_children_score=90.0,
            primary_pattern="street_exposure_protection_absence",
        ),
        StreetChildrenRightsEntity(
            entity_id="SCR-002",
            name="Brésil — Favelas, Violence Policière Extrajudiciaire Enfants Rue & Escadrons Nettoyage Social",
            country="Brésil",
            street_exposure_protection_absence_score=92.0,
            violence_exploitation_vulnerability_score=94.0,
            access_education_services_gap_score=88.0,
            criminalization_detention_children_score=91.0,
            primary_pattern="violence_exploitation_vulnerability",
        ),
        StreetChildrenRightsEntity(
            entity_id="SCR-003",
            name="RDC/Afrique Centrale — Enfants Sorciers Rejetés, Orphelins Conflit & Exploitation Minières Artisanales",
            country="RDC",
            street_exposure_protection_absence_score=91.0,
            violence_exploitation_vulnerability_score=90.0,
            access_education_services_gap_score=92.0,
            criminalization_detention_children_score=87.0,
            primary_pattern="access_education_services_gap",
        ),
        StreetChildrenRightsEntity(
            entity_id="SCR-004",
            name="Bangladesh — Dhaka Enfants Rue 700 000, Trafic Mendicité Forcée & Zéro Accès Santé Mentale",
            country="Bangladesh",
            street_exposure_protection_absence_score=89.0,
            violence_exploitation_vulnerability_score=87.0,
            access_education_services_gap_score=88.0,
            criminalization_detention_children_score=85.0,
            primary_pattern="street_exposure_protection_absence",
        ),
        StreetChildrenRightsEntity(
            entity_id="SCR-005",
            name="Honduras/Guatemala — Triangle Nord, Migration Forcée Mineurs & Gangs MS-13 Recrutement Rue",
            country="Amérique Centrale",
            street_exposure_protection_absence_score=58.0,
            violence_exploitation_vulnerability_score=60.0,
            access_education_services_gap_score=55.0,
            criminalization_detention_children_score=57.0,
            primary_pattern="violence_exploitation_vulnerability",
        ),
        StreetChildrenRightsEntity(
            entity_id="SCR-006",
            name="Ukraine/Europe Est — Enfants Déplacés Guerre, SDF Mineurs & Réseau Trafic Post-Conflit",
            country="Ukraine/Europe Est",
            street_exposure_protection_absence_score=55.0,
            violence_exploitation_vulnerability_score=52.0,
            access_education_services_gap_score=54.0,
            criminalization_detention_children_score=50.0,
            primary_pattern="street_exposure_protection_absence",
        ),
        StreetChildrenRightsEntity(
            entity_id="SCR-007",
            name="UNICEF/Consortium — Programmes Réinsertion, Centres Accueil & Éducation Non-Formelle Enfants Rue",
            country="Global",
            street_exposure_protection_absence_score=24.0,
            violence_exploitation_vulnerability_score=26.0,
            access_education_services_gap_score=22.0,
            criminalization_detention_children_score=28.0,
            primary_pattern="access_education_services_gap",
        ),
        StreetChildrenRightsEntity(
            entity_id="SCR-008",
            name="ONU/CRC — Convention Droits Enfant Art.27, Protocoles Protection Enfants Sans Abri & Standards Minima",
            country="Global",
            street_exposure_protection_absence_score=5.0,
            violence_exploitation_vulnerability_score=4.0,
            access_education_services_gap_score=5.0,
            criminalization_detention_children_score=4.0,
            primary_pattern="street_exposure_protection_absence",
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

    return StreetChildrenRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_street_children_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_street_children_global_situation_analysis",
            "consortium_street_children_global_street_child_report",
            "human_rights_watch_street_children_violence_police_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_street_children_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_street_children_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
    avg = result.avg_composite
    dist = result.risk_distribution
    print(f"avg_composite : {avg:.2f}")
    ok = (dist.get('critique', 0) == 4 and dist.get('élevé', 0) == 2 and dist.get('modéré', 0) == 1 and dist.get('faible', 0) == 1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")
