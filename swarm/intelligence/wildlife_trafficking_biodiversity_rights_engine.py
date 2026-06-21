from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WildlifeTraffickingBiodiversityRightsEntity:
    entity_id: str
    name: str
    country: str
    trafficking_volume_species_extinction_risk_score: float
    enforcement_anti_poaching_failure_score: float
    corruption_criminal_network_penetration_score: float
    legal_framework_cites_compliance_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_wildlife_trafficking_biodiversity_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.trafficking_volume_species_extinction_risk_score * 0.30
            + self.enforcement_anti_poaching_failure_score * 0.25
            + self.corruption_criminal_network_penetration_score * 0.25
            + self.legal_framework_cites_compliance_deficit_score * 0.20,
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
        self.estimated_wildlife_trafficking_biodiversity_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class WildlifeTraffickingBiodiversityRightsEngineResult:
    agent: str = "Wildlife Trafficking Biodiversity Rights Engine Agent"
    domain: str = "wildlife_trafficking_biodiversity_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_wildlife_trafficking_biodiversity_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WildlifeTraffickingBiodiversityRightsEntity] = field(default_factory=list)


def run_wildlife_trafficking_biodiversity_rights_engine() -> WildlifeTraffickingBiodiversityRightsEngineResult:
    entities = [
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-001",
            name="Chine/Marché Traditionnel — 3ème Marché Mondial Espèces Illicites, 73% Pangolins Mondiaux Consommés, Médecine Traditionnelle 1 400 Espèces & Fermes Élevage Légalisées",
            country="Chine",
            trafficking_volume_species_extinction_risk_score=92.0,
            enforcement_anti_poaching_failure_score=78.0,
            corruption_criminal_network_penetration_score=80.0,
            legal_framework_cites_compliance_deficit_score=75.0,
            primary_pattern="trafficking_volume_species_extinction_risk",
        ),
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-002",
            name="Afrique du Sud/Rhinocéros — 499 Rhinos Braconnés 2023, Mafias Vietnamiennes Réseaux Kruger, Gardes Corrompus & Corne Marché Noir 60 000$/kg",
            country="Afrique du Sud",
            trafficking_volume_species_extinction_risk_score=88.0,
            enforcement_anti_poaching_failure_score=85.0,
            corruption_criminal_network_penetration_score=87.0,
            legal_framework_cites_compliance_deficit_score=83.0,
            primary_pattern="corruption_criminal_network_penetration",
        ),
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-003",
            name="Vietnam/Hub Transit Asie — Principal Hub Transit Asie du SE, Ours Bile Farmed 1 200 Ursidés, Ailerons Requin & Réseaux Cybercrime Espèces Annexe I",
            country="Vietnam",
            trafficking_volume_species_extinction_risk_score=84.0,
            enforcement_anti_poaching_failure_score=82.0,
            corruption_criminal_network_penetration_score=89.0,
            legal_framework_cites_compliance_deficit_score=80.0,
            primary_pattern="corruption_criminal_network_penetration",
        ),
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-004",
            name="RDC/Gorilles Ivoire — Gorilles de Montagne 1 063 Individus Survivants, Braconnage Défenses Éléphants Financement Groupes Armés, Forêts Conflits & Gardes Assassinés",
            country="RDC",
            trafficking_volume_species_extinction_risk_score=80.0,
            enforcement_anti_poaching_failure_score=83.0,
            corruption_criminal_network_penetration_score=82.0,
            legal_framework_cites_compliance_deficit_score=85.0,
            primary_pattern="legal_framework_cites_compliance_deficit",
        ),
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-005",
            name="Mexique/Totoaba Cartel — Totoaba Mariscos Valeur 8 500$/kg Buche, Extinction Vaquita Marina 10 Individus, Cartels Sinaloa & Circuits Douaniers Corruptibles",
            country="Mexique",
            trafficking_volume_species_extinction_risk_score=58.0,
            enforcement_anti_poaching_failure_score=62.0,
            corruption_criminal_network_penetration_score=65.0,
            legal_framework_cites_compliance_deficit_score=60.0,
            primary_pattern="corruption_criminal_network_penetration",
        ),
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-006",
            name="Thaïlande/Zoo Tigres — Temple Bouddha Tigres 147 Confisqués 2016, Élevage Illégal Tigres Blancs, Bois de Rose Kanchanaburi & Cybercrime Facebook Espèces",
            country="Thaïlande",
            trafficking_volume_species_extinction_risk_score=54.0,
            enforcement_anti_poaching_failure_score=52.0,
            corruption_criminal_network_penetration_score=58.0,
            legal_framework_cites_compliance_deficit_score=55.0,
            primary_pattern="corruption_criminal_network_penetration",
        ),
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-007",
            name="Brésil/Amazonie Psittacidés — 400 000 Perroquets/an Trafiqués Intérieur, Ara Spix 250 Captivité, Police Environnementale Réduite & IBAMA Sous-Financement",
            country="Brésil",
            trafficking_volume_species_extinction_risk_score=28.0,
            enforcement_anti_poaching_failure_score=35.0,
            corruption_criminal_network_penetration_score=32.0,
            legal_framework_cites_compliance_deficit_score=38.0,
            primary_pattern="legal_framework_cites_compliance_deficit",
        ),
        WildlifeTraffickingBiodiversityRightsEntity(
            entity_id="WTB-008",
            name="UE/CITES AppVet — Base CITES AppVet Saisies, Règlement EU 338/97 Espèces Protégées, Douanes Europol Opérations Thunderball & Score Conformité 89%",
            country="Union Européenne",
            trafficking_volume_species_extinction_risk_score=8.0,
            enforcement_anti_poaching_failure_score=9.0,
            corruption_criminal_network_penetration_score=7.0,
            legal_framework_cites_compliance_deficit_score=8.0,
            primary_pattern="trafficking_volume_species_extinction_risk",
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

    return WildlifeTraffickingBiodiversityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_wildlife_trafficking_biodiversity_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unodc_wildlife_crime_world_report_2024",
            "traffic_wildlife_trade_monitoring_network",
            "iucn_red_list_species_status_2024",
            "cites_trade_database_annual_saisies",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_wildlife_trafficking_biodiversity_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_wildlife_trafficking_biodiversity_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
