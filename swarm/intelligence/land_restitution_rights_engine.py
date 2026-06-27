from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#854d0e"


@dataclass
class LandRestitutionRightsEntity:
    entity_id: str
    name: str
    country: str
    dispossession_without_remedy_score: float
    restitution_process_denial_score: float
    displacement_without_return_score: float
    reparations_justice_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_land_restitution_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.dispossession_without_remedy_score * 0.30
            + self.restitution_process_denial_score * 0.25
            + self.displacement_without_return_score * 0.25
            + self.reparations_justice_gap_score * 0.20,
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
        self.estimated_land_restitution_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class LandRestitutionRightsEngineResult:
    agent: str = "Land Restitution Rights Engine Agent"
    domain: str = "land_restitution_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_land_restitution_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LandRestitutionRightsEntity] = field(default_factory=list)


def run_land_restitution_rights_engine() -> LandRestitutionRightsEngineResult:
    entities = [
        LandRestitutionRightsEntity(
            entity_id="LRR-001",
            name="Palestine/Territoires Occupés — 150 000 Propriétés Confisquées Depuis 1948, Aucune Restitution, Dépossession Continue",
            country="Palestine/Territoires Occupés",
            dispossession_without_remedy_score=95.0,
            restitution_process_denial_score=94.0,
            displacement_without_return_score=93.0,
            reparations_justice_gap_score=95.0,
            primary_pattern="dispossession_without_remedy_score",
        ),
        LandRestitutionRightsEntity(
            entity_id="LRR-002",
            name="Zimbabwe — Réforme Agraire Violente Mugabe, 4 000 Fermiers Expropriés Sans Compensation, Aucun Mécanisme Réparation",
            country="Zimbabwe",
            dispossession_without_remedy_score=87.0,
            restitution_process_denial_score=85.0,
            displacement_without_return_score=82.0,
            reparations_justice_gap_score=88.0,
            primary_pattern="reparations_justice_gap_score",
        ),
        LandRestitutionRightsEntity(
            entity_id="LRR-003",
            name="Syrie — 1,5M Déplacés Internes, Propriétés Saisies Loi 10/2018, Retour Impossible Sans Abandon Droits",
            country="Syrie",
            dispossession_without_remedy_score=88.0,
            restitution_process_denial_score=86.0,
            displacement_without_return_score=90.0,
            reparations_justice_gap_score=85.0,
            primary_pattern="displacement_without_return_score",
        ),
        LandRestitutionRightsEntity(
            entity_id="LRR-004",
            name="Colombie — 8M Déplacés, Restitution Terres Victimes FARC Bloquée par Élites, Assassinats Défenseurs Terres",
            country="Colombie",
            dispossession_without_remedy_score=80.0,
            restitution_process_denial_score=78.0,
            displacement_without_return_score=82.0,
            reparations_justice_gap_score=76.0,
            primary_pattern="displacement_without_return_score",
        ),
        LandRestitutionRightsEntity(
            entity_id="LRR-005",
            name="Kenya — Terres Mau-Mau, Restitution Coloniale Partielle, Rift Valley Non Résolue, Tensions Interethniques Persistantes",
            country="Kenya",
            dispossession_without_remedy_score=52.0,
            restitution_process_denial_score=50.0,
            displacement_without_return_score=48.0,
            reparations_justice_gap_score=53.0,
            primary_pattern="reparations_justice_gap_score",
        ),
        LandRestitutionRightsEntity(
            entity_id="LRR-006",
            name="Afrique du Sud — Restitution Post-Apartheid Lente, 30 Ans 80% Terres Toujours Propriété Blanche, Process Engorgé",
            country="Afrique du Sud",
            dispossession_without_remedy_score=48.0,
            restitution_process_denial_score=50.0,
            displacement_without_return_score=44.0,
            reparations_justice_gap_score=47.0,
            primary_pattern="restitution_process_denial_score",
        ),
        LandRestitutionRightsEntity(
            entity_id="LRR-007",
            name="Allemagne — Restitution Propriétés Juives, Process Active Mais Lente, Héritiers Diaspora Difficultés Administratives",
            country="Allemagne",
            dispossession_without_remedy_score=28.0,
            restitution_process_denial_score=30.0,
            displacement_without_return_score=24.0,
            reparations_justice_gap_score=26.0,
            primary_pattern="restitution_process_denial_score",
        ),
        LandRestitutionRightsEntity(
            entity_id="LRR-008",
            name="Canada — Traités Modernes Autochtones, Tribunal Revendications Particulières, Meilleure Pratique Restitution Négociée",
            country="Canada",
            dispossession_without_remedy_score=10.0,
            restitution_process_denial_score=9.0,
            displacement_without_return_score=8.0,
            reparations_justice_gap_score=11.0,
            primary_pattern="dispossession_without_remedy_score",
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

    return LandRestitutionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_land_restitution_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_basic_principles_reparations_2005",
            "unhcr_pinheiro_principles_housing_property_restitution",
            "hrw_land_rights_displacement_documentation",
            "amnesty_land_restitution_indigenous_report",
            "un_special_rapporteur_adequate_housing_restitution",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_land_restitution_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
