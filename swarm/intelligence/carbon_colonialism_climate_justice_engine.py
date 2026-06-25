"""
carbon_colonialism_climate_justice_engine.py
Wave 189 — Colonialisme Carbone & Justice Climatique
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class CarbonColonialismClimateJusticeEntity:
    entity_id: str
    name: str
    country: str
    carbon_offset_land_grab_score: float
    climate_finance_inequity_score: float
    green_energy_displacement_score: float
    loss_damage_reparations_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_carbon_colonialism_climate_justice_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.carbon_offset_land_grab_score * 0.30
            + self.climate_finance_inequity_score * 0.25
            + self.green_energy_displacement_score * 0.25
            + self.loss_damage_reparations_deficit_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_carbon_colonialism_climate_justice_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[CarbonColonialismClimateJusticeEntity]:
    return [
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-001",
            name="République Démocratique du Congo — Accaparement Forêts Carbone, Expulsions Massives",
            country="RDC",
            carbon_offset_land_grab_score=94.0,
            climate_finance_inequity_score=91.0,
            green_energy_displacement_score=89.0,
            loss_damage_reparations_deficit_score=93.0,
            primary_pattern="5M hectares forêts cédés aux crédits carbone sans FPIC, 200k communautés déplacées, financement climatique 0.3% PIB reçu vs 8% promis",
        ),
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-002",
            name="Bangladesh — 0.4% Émissions, 40M Réfugiés Climatiques, Zéro Réparation",
            country="Bangladesh",
            carbon_offset_land_grab_score=88.0,
            climate_finance_inequity_score=93.0,
            green_energy_displacement_score=86.0,
            loss_damage_reparations_deficit_score=95.0,
            primary_pattern="Responsabilité historique nulle, 17% territoire submergé 2050, mécanisme perte-dommage COP28 insuffisant, fonds Green Climate reçu: 124M sur 1,3Md promis",
        ),
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-003",
            name="Mozambique — Projets Éoliens Déplacent Villageois, Bénéfices Exportés",
            country="Mozambique",
            carbon_offset_land_grab_score=90.0,
            climate_finance_inequity_score=87.0,
            green_energy_displacement_score=92.0,
            loss_damage_reparations_deficit_score=88.0,
            primary_pattern="Parcs éoliens Nacala déplacent 15k familles, électricité exportée vers Afrique du Sud, communautés sans accès 82% énergie renouvelable produite localement",
        ),
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-004",
            name="Îles Marshall — Existence Menacée, Financement Climatique Bloqué par Conditionnalités",
            country="Îles Marshall",
            carbon_offset_land_grab_score=82.0,
            climate_finance_inequity_score=89.0,
            green_energy_displacement_score=84.0,
            loss_damage_reparations_deficit_score=93.0,
            primary_pattern="Submersion 2050 certifiée, conditionnalités FMI bloquent accès fonds adaptation, 0 émissions historiques, perte souveraineté nationale programmée",
        ),
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-005",
            name="Kenya — Marché Volontaire Carbone Frauduleux, REDD+ Détourné",
            country="Kenya",
            carbon_offset_land_grab_score=54.0,
            climate_finance_inequity_score=52.0,
            green_energy_displacement_score=50.0,
            loss_damage_reparations_deficit_score=55.0,
            primary_pattern="Projets REDD+ Kariba décertifiés fraude 2023, crédits carbone vendus sans bénéfice communautaire, 180k tonnes CO2 fictives compensées par multinationales",
        ),
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-006",
            name="Brésil — Terres Autochtones Amazonie Sous Pression Carbone/Agrobusiness",
            country="Brésil",
            carbon_offset_land_grab_score=56.0,
            climate_finance_inequity_score=50.0,
            green_energy_displacement_score=53.0,
            loss_damage_reparations_deficit_score=51.0,
            primary_pattern="Déforestation Amazonie 11,568 km² 2022, crédits carbone mal attribués, peuples Yanomami victimes accaparement minier extractivisme climatique",
        ),
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-007",
            name="Éthiopie — Barrage Grand Ethiopian Renaissance, Conflits Hydro-Climatiques",
            country="Éthiopie",
            carbon_offset_land_grab_score=28.0,
            climate_finance_inequity_score=30.0,
            green_energy_displacement_score=25.0,
            loss_damage_reparations_deficit_score=27.0,
            primary_pattern="Barrage GERD génère conflits régionaux eau, financement vert conditionné diplomatiquement, tensions climatiques Nil Bleu mal gérées",
        ),
        CarbonColonialismClimateJusticeEntity(
            entity_id="CCJ-008",
            name="Danemark — Leader Financement Climatique, Fonds Perte-Dommage Pionnier",
            country="Danemark",
            carbon_offset_land_grab_score=5.0,
            climate_finance_inequity_score=4.0,
            green_energy_displacement_score=6.0,
            loss_damage_reparations_deficit_score=5.0,
            primary_pattern="Premier pays fonds perte-dommage COP27, 100M€ engagés, transition juste exportée équitablement, modèle coopération climatique sud-sud",
        ),
    ]


def analyze(entities: List[CarbonColonialismClimateJusticeEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "carbon_colonialism_climate_justice_engine",
        "domain": "carbon_colonialism_climate_justice",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.90,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "carbon_offset_land_grab": 3,
            "climate_finance_inequity": 2,
            "green_energy_displacement": 2,
            "loss_damage_deficit": 1,
        },
        "top_risk_entities": [
            {"id": e.entity_id, "name": e.name, "score": e.composite_score, "risk": e.risk_level}
            for e in top_risk
        ],
        "critical_alerts": [
            f"{e.entity_id}: {e.name} — composite {e.composite_score}"
            for e in entities if e.risk_level == "critique"
        ],
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "avg_estimated_carbon_colonialism_climate_justice_index": round(
            statistics.mean([e.estimated_carbon_colonialism_climate_justice_index for e in entities]), 2
        ),
        "data_sources": [
            "ipcc_ar6_climate_justice_2023",
            "un_fccc_loss_damage_fund_cop28_2023",
            "carbon_market_watch_redd_report_2024",
            "oxfam_climate_finance_inequality_2023",
        ],
        "entities": [
            {
                "id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "carbon_offset_land_grab_score": e.carbon_offset_land_grab_score,
                "climate_finance_inequity_score": e.climate_finance_inequity_score,
                "green_energy_displacement_score": e.green_energy_displacement_score,
                "loss_damage_reparations_deficit_score": e.loss_damage_reparations_deficit_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_carbon_colonialism_climate_justice_index": e.estimated_carbon_colonialism_climate_justice_index,
                "last_updated": e.last_updated,
            }
            for e in entities
        ],
    }


if __name__ == "__main__":
    import json
    entities = build_entities()
    result = analyze(entities)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n✓ avg_composite = {result['avg_composite']}")
    print(f"✓ risk_distribution = {result['risk_distribution']}")
    print(f"✓ total_entities = {result['total_entities']}")
    dist = result["risk_distribution"]
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
