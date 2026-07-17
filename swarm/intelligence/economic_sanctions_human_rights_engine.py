from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EconomicSanctionsHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    civilian_suffering_scale_score: float
    medicine_food_access_denial_score: float
    democratic_governance_erosion_score: float
    sanctions_impunity_perpetrators_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_economic_sanctions_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.civilian_suffering_scale_score * 0.30
            + self.medicine_food_access_denial_score * 0.25
            + self.democratic_governance_erosion_score * 0.25
            + self.sanctions_impunity_perpetrators_score * 0.20,
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
        self.estimated_economic_sanctions_human_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EconomicSanctionsHumanRightsEngineResult:
    agent: str = "Economic Sanctions Human Rights Engine Agent"
    domain: str = "economic_sanctions_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_economic_sanctions_human_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EconomicSanctionsHumanRightsEntity] = field(default_factory=list)

def run_economic_sanctions_human_rights_engine() -> EconomicSanctionsHumanRightsEngineResult:
    entities = [
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-001",
            name="Iran — Sanctions OFAC, Pénurie Médicaments Oncologie & Effondrement Rial Populations",
            country="Moyen-Orient",
            civilian_suffering_scale_score=92.0,
            medicine_food_access_denial_score=95.0,
            democratic_governance_erosion_score=80.0,
            sanctions_impunity_perpetrators_score=85.0,
            primary_pattern="medicine_food_access_denial",
        ),
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-002",
            name="Venezuela — Sanctions USA/UE, Hyperinflation, Fuite 7M Réfugiés & Crise Humanitaire",
            country="Amérique Latine",
            civilian_suffering_scale_score=88.0,
            medicine_food_access_denial_score=90.0,
            democratic_governance_erosion_score=85.0,
            sanctions_impunity_perpetrators_score=82.0,
            primary_pattern="civilian_suffering_scale",
        ),
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-003",
            name="Cuba — Blocus 60 Ans, Pénuries Chroniques & Embargo Unilatéral Condamné ONU",
            country="Caraïbes",
            civilian_suffering_scale_score=80.0,
            medicine_food_access_denial_score=85.0,
            democratic_governance_erosion_score=78.0,
            sanctions_impunity_perpetrators_score=82.0,
            primary_pattern="medicine_food_access_denial",
        ),
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-004",
            name="Corée du Nord — Sanctions CSNU, Famines Endémiques & Régime Enrichi sous Blocus",
            country="Asie du Nord-Est",
            civilian_suffering_scale_score=82.0,
            medicine_food_access_denial_score=80.0,
            democratic_governance_erosion_score=72.0,
            sanctions_impunity_perpetrators_score=90.0,
            primary_pattern="sanctions_impunity_perpetrators",
        ),
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-005",
            name="Russie/Ukraine — Sanctions G7, Réponse Agression & Double Standard vs Alliés Autoritaires",
            country="Europe de l'Est",
            civilian_suffering_scale_score=52.0,
            medicine_food_access_denial_score=48.0,
            democratic_governance_erosion_score=55.0,
            sanctions_impunity_perpetrators_score=58.0,
            primary_pattern="democratic_governance_erosion",
        ),
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-006",
            name="Syrie/Yémen — Sanctions & Guerre, Caesar Act, Blocus Houthis & Aide Humanitaire Bloquée",
            country="Moyen-Orient",
            civilian_suffering_scale_score=55.0,
            medicine_food_access_denial_score=52.0,
            democratic_governance_erosion_score=50.0,
            sanctions_impunity_perpetrators_score=48.0,
            primary_pattern="civilian_suffering_scale",
        ),
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-007",
            name="UE/USA — Sanctions Ciblées GAFI, Gel Avoirs & Exemptions Humanitaires Insuffisantes",
            country="Global",
            civilian_suffering_scale_score=22.0,
            medicine_food_access_denial_score=28.0,
            democratic_governance_erosion_score=30.0,
            sanctions_impunity_perpetrators_score=32.0,
            primary_pattern="democratic_governance_erosion",
        ),
        EconomicSanctionsHumanRightsEntity(
            entity_id="ES-008",
            name="ONU/CSNU — Régime Sanctions Multilatérales, Comités & Mécanisme Suivi Humanitaire",
            country="Global",
            civilian_suffering_scale_score=4.0,
            medicine_food_access_denial_score=5.0,
            democratic_governance_erosion_score=3.0,
            sanctions_impunity_perpetrators_score=6.0,
            primary_pattern="sanctions_impunity_perpetrators",
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

    return EconomicSanctionsHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_economic_sanctions_human_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "human_rights_watch_sanctions_civilian_impact_annual_report",
            "oxfam_unintended_consequences_sanctions_humanitarian_crisis_report",
            "un_special_rapporteur_unilateral_coercive_measures_human_rights_annual",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_economic_sanctions_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_economic_sanctions_human_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
