from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FoodWasteEconomyInput:
    entity_id: str
    food_sector: str
    region: str
    retail_waste_rate: float
    production_surplus: float
    cold_chain_failure: float
    date_labeling_confusion: float
    consumer_waste_behavior: float
    redistribution_gap: float
    composting_infrastructure: float
    regulatory_compliance_gap: float
    supply_chain_inefficiency: float
    packaging_waste_impact: float
    food_bank_capacity: float
    corporate_responsibility_gap: float
    circular_economy_adoption: float
    economic_loss_per_capita: float
    biodiversity_impact: float
    water_waste_embedded: float
    carbon_footprint_waste: float


@dataclass
class FoodWasteEconomyResult:
    entity_id: str
    food_sector: str
    region: str
    waste_score: float
    supply_chain_score: float
    policy_score: float
    circular_score: float
    composite_score: float
    risk_level: str
    patterns: List[str]
    economic_loss_per_capita: float
    water_waste_embedded: float
    carbon_footprint_waste: float
    biodiversity_impact: float
    estimated_food_waste_index: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "food_sector": self.food_sector,
            "region": self.region,
            "waste_score": self.waste_score,
            "supply_chain_score": self.supply_chain_score,
            "policy_score": self.policy_score,
            "circular_score": self.circular_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "patterns": self.patterns,
            "economic_loss_per_capita": self.economic_loss_per_capita,
            "water_waste_embedded": self.water_waste_embedded,
            "carbon_footprint_waste": self.carbon_footprint_waste,
            "biodiversity_impact": self.biodiversity_impact,
            "estimated_food_waste_index": self.estimated_food_waste_index,
        }


def _waste_score(e: FoodWasteEconomyInput) -> float:
    raw = (
        e.retail_waste_rate
        + e.production_surplus
        + e.redistribution_gap
        + e.consumer_waste_behavior
    ) / 4
    return round(raw * 100) / 100


def _supply_chain_score(e: FoodWasteEconomyInput) -> float:
    raw = (
        e.cold_chain_failure
        + e.supply_chain_inefficiency
        + e.packaging_waste_impact
        + e.water_waste_embedded
    ) / 4
    return round(raw * 100) / 100


def _policy_score(e: FoodWasteEconomyInput) -> float:
    raw = (
        e.date_labeling_confusion
        + e.regulatory_compliance_gap
        + e.corporate_responsibility_gap
        + (100 - e.food_bank_capacity)
    ) / 4
    return round(raw * 100) / 100


def _circular_score(e: FoodWasteEconomyInput) -> float:
    raw = (
        (100 - e.composting_infrastructure)
        + (100 - e.circular_economy_adoption)
        + e.biodiversity_impact
        + e.carbon_footprint_waste
    ) / 4
    return round(raw * 100) / 100


def _composite_score(
    waste: float,
    supply_chain: float,
    policy: float,
    circular: float,
) -> float:
    return round(
        (waste * 0.30 + supply_chain * 0.25 + policy * 0.25 + circular * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _patterns(e: FoodWasteEconomyInput) -> List[str]:
    result = []
    if e.retail_waste_rate > 60 or e.production_surplus > 60:
        result.append("retail_overproduction_dump")
    if e.cold_chain_failure > 55:
        result.append("cold_chain_collapse")
    if e.date_labeling_confusion > 50:
        result.append("date_label_confusion")
    if e.consumer_waste_behavior > 55:
        result.append("consumer_behavioral_waste")
    if e.regulatory_compliance_gap > 55 or e.corporate_responsibility_gap > 55:
        result.append("policy_incentive_failure")
    return result


def analyze_food_waste_economy(e: FoodWasteEconomyInput) -> FoodWasteEconomyResult:
    waste = _waste_score(e)
    supply_chain = _supply_chain_score(e)
    policy = _policy_score(e)
    circular = _circular_score(e)
    composite = _composite_score(waste, supply_chain, policy, circular)
    risk = _risk_level(composite)
    pats = _patterns(e)
    estimated_index = round(composite / 100 * 10, 2)

    return FoodWasteEconomyResult(
        entity_id=e.entity_id,
        food_sector=e.food_sector,
        region=e.region,
        waste_score=waste,
        supply_chain_score=supply_chain,
        policy_score=policy,
        circular_score=circular,
        composite_score=composite,
        risk_level=risk,
        patterns=pats,
        economic_loss_per_capita=e.economic_loss_per_capita,
        water_waste_embedded=e.water_waste_embedded,
        carbon_footprint_waste=e.carbon_footprint_waste,
        biodiversity_impact=e.biodiversity_impact,
        estimated_food_waste_index=estimated_index,
    )


class FoodWasteEconomyEngine:
    def analyze(self, entities: List[FoodWasteEconomyInput]) -> Dict[str, Any]:
        results = [analyze_food_waste_economy(e) for e in entities]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}

        total_waste = 0.0
        total_supply_chain = 0.0
        total_policy = 0.0
        total_circular = 0.0
        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            for pat in r.patterns:
                pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1
            total_waste += r.waste_score
            total_supply_chain += r.supply_chain_score
            total_policy += r.policy_score
            total_circular += r.circular_score
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical_count += 1
            elif r.risk_level == "high":
                high_count += 1
            elif r.risk_level == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(results) or 1
        avg_waste = round(total_waste / n * 10) / 10
        avg_supply_chain = round(total_supply_chain / n * 10) / 10
        avg_policy = round(total_policy / n * 10) / 10
        avg_circular = round(total_circular / n * 10) / 10
        avg_composite = round(total_composite / n * 10) / 10

        return self.summary(
            results=results,
            risk_distribution=risk_distribution,
            pattern_distribution=pattern_distribution,
            avg_waste=avg_waste,
            avg_supply_chain=avg_supply_chain,
            avg_policy=avg_policy,
            avg_circular=avg_circular,
            avg_composite=avg_composite,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
        )

    def summary(
        self,
        results: List[FoodWasteEconomyResult] = None,
        risk_distribution: Dict[str, int] = None,
        pattern_distribution: Dict[str, int] = None,
        avg_waste: float = 0.0,
        avg_supply_chain: float = 0.0,
        avg_policy: float = 0.0,
        avg_circular: float = 0.0,
        avg_composite: float = 0.0,
        critical_count: int = 0,
        high_count: int = 0,
        moderate_count: int = 0,
        low_count: int = 0,
    ) -> Dict[str, Any]:
        results = results or []
        return {
            "total_entities": len(results),
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_waste_score": avg_waste,
            "avg_supply_chain_score": avg_supply_chain,
            "avg_policy_score": avg_policy,
            "avg_circular_score": avg_circular,
            "avg_composite_score": avg_composite,
            "top_patterns": pattern_distribution or {},
            "risk_distribution": risk_distribution or {},
            "avg_estimated_food_waste_index": round(avg_composite / 100 * 10, 2),
        }


MOCK_ENTITIES: List[FoodWasteEconomyInput] = [
    # FWE-001 — critique — grande distribution, Île-de-France
    # patterns: retail_overproduction_dump, cold_chain_collapse, date_label_confusion, consumer_behavioral_waste, policy_incentive_failure
    FoodWasteEconomyInput(
        entity_id="FWE-001",
        food_sector="grande_distribution",
        region="Île-de-France",
        retail_waste_rate=80.0,
        production_surplus=75.0,
        cold_chain_failure=60.0,
        date_labeling_confusion=70.0,
        consumer_waste_behavior=65.0,
        redistribution_gap=70.0,
        composting_infrastructure=80.0,
        regulatory_compliance_gap=70.0,
        supply_chain_inefficiency=65.0,
        packaging_waste_impact=70.0,
        food_bank_capacity=20.0,
        corporate_responsibility_gap=65.0,
        circular_economy_adoption=75.0,
        economic_loss_per_capita=1200.0,
        biodiversity_impact=70.0,
        water_waste_embedded=65.0,
        carbon_footprint_waste=75.0,
    ),
    # FWE-002 — critique — logistique alimentaire, Auvergne-Rhône-Alpes
    # patterns: retail_overproduction_dump, cold_chain_collapse, date_label_confusion, consumer_behavioral_waste, policy_incentive_failure
    FoodWasteEconomyInput(
        entity_id="FWE-002",
        food_sector="logistique_alimentaire",
        region="Auvergne-Rhône-Alpes",
        retail_waste_rate=65.0,
        production_surplus=65.0,
        cold_chain_failure=80.0,
        date_labeling_confusion=55.0,
        consumer_waste_behavior=60.0,
        redistribution_gap=72.0,
        composting_infrastructure=75.0,
        regulatory_compliance_gap=60.0,
        supply_chain_inefficiency=75.0,
        packaging_waste_impact=70.0,
        food_bank_capacity=25.0,
        corporate_responsibility_gap=60.0,
        circular_economy_adoption=80.0,
        economic_loss_per_capita=1100.0,
        biodiversity_impact=65.0,
        water_waste_embedded=68.0,
        carbon_footprint_waste=70.0,
    ),
    # FWE-003 — critique — restauration collective, Hauts-de-France
    # patterns: retail_overproduction_dump, date_label_confusion, consumer_behavioral_waste, policy_incentive_failure
    FoodWasteEconomyInput(
        entity_id="FWE-003",
        food_sector="restauration_collective",
        region="Hauts-de-France",
        retail_waste_rate=70.0,
        production_surplus=68.0,
        cold_chain_failure=50.0,
        date_labeling_confusion=55.0,
        consumer_waste_behavior=80.0,
        redistribution_gap=65.0,
        composting_infrastructure=80.0,
        regulatory_compliance_gap=65.0,
        supply_chain_inefficiency=60.0,
        packaging_waste_impact=62.0,
        food_bank_capacity=30.0,
        corporate_responsibility_gap=70.0,
        circular_economy_adoption=78.0,
        economic_loss_per_capita=950.0,
        biodiversity_impact=68.0,
        water_waste_embedded=58.0,
        carbon_footprint_waste=72.0,
    ),
    # FWE-004 — élevé — industrie agroalimentaire, Bretagne
    # pattern: date_label_confusion
    FoodWasteEconomyInput(
        entity_id="FWE-004",
        food_sector="industrie_agroalimentaire",
        region="Bretagne",
        retail_waste_rate=50.0,
        production_surplus=48.0,
        cold_chain_failure=45.0,
        date_labeling_confusion=70.0,
        consumer_waste_behavior=48.0,
        redistribution_gap=52.0,
        composting_infrastructure=60.0,
        regulatory_compliance_gap=50.0,
        supply_chain_inefficiency=50.0,
        packaging_waste_impact=48.0,
        food_bank_capacity=40.0,
        corporate_responsibility_gap=48.0,
        circular_economy_adoption=55.0,
        economic_loss_per_capita=650.0,
        biodiversity_impact=50.0,
        water_waste_embedded=45.0,
        carbon_footprint_waste=48.0,
    ),
    # FWE-005 — élevé — coopérative agricole, Nouvelle-Aquitaine
    # pattern: policy_incentive_failure
    FoodWasteEconomyInput(
        entity_id="FWE-005",
        food_sector="coopérative_agricole",
        region="Nouvelle-Aquitaine",
        retail_waste_rate=52.0,
        production_surplus=50.0,
        cold_chain_failure=48.0,
        date_labeling_confusion=50.0,
        consumer_waste_behavior=50.0,
        redistribution_gap=55.0,
        composting_infrastructure=62.0,
        regulatory_compliance_gap=70.0,
        supply_chain_inefficiency=52.0,
        packaging_waste_impact=50.0,
        food_bank_capacity=35.0,
        corporate_responsibility_gap=65.0,
        circular_economy_adoption=58.0,
        economic_loss_per_capita=700.0,
        biodiversity_impact=52.0,
        water_waste_embedded=48.0,
        carbon_footprint_waste=50.0,
    ),
    # FWE-006 — modéré — marché de proximité, Occitanie
    FoodWasteEconomyInput(
        entity_id="FWE-006",
        food_sector="marché_de_proximité",
        region="Occitanie",
        retail_waste_rate=30.0,
        production_surplus=28.0,
        cold_chain_failure=25.0,
        date_labeling_confusion=30.0,
        consumer_waste_behavior=28.0,
        redistribution_gap=32.0,
        composting_infrastructure=55.0,
        regulatory_compliance_gap=28.0,
        supply_chain_inefficiency=30.0,
        packaging_waste_impact=28.0,
        food_bank_capacity=60.0,
        corporate_responsibility_gap=30.0,
        circular_economy_adoption=50.0,
        economic_loss_per_capita=350.0,
        biodiversity_impact=30.0,
        water_waste_embedded=25.0,
        carbon_footprint_waste=28.0,
    ),
    # FWE-007 — faible — filière biologique, Pays de la Loire
    FoodWasteEconomyInput(
        entity_id="FWE-007",
        food_sector="filière_biologique",
        region="Pays de la Loire",
        retail_waste_rate=10.0,
        production_surplus=12.0,
        cold_chain_failure=10.0,
        date_labeling_confusion=12.0,
        consumer_waste_behavior=8.0,
        redistribution_gap=10.0,
        composting_infrastructure=20.0,
        regulatory_compliance_gap=10.0,
        supply_chain_inefficiency=12.0,
        packaging_waste_impact=10.0,
        food_bank_capacity=80.0,
        corporate_responsibility_gap=12.0,
        circular_economy_adoption=25.0,
        economic_loss_per_capita=80.0,
        biodiversity_impact=10.0,
        water_waste_embedded=8.0,
        carbon_footprint_waste=8.0,
    ),
    # FWE-008 — faible — agriculture raisonnée, Grand Est
    FoodWasteEconomyInput(
        entity_id="FWE-008",
        food_sector="agriculture_raisonnée",
        region="Grand Est",
        retail_waste_rate=8.0,
        production_surplus=10.0,
        cold_chain_failure=8.0,
        date_labeling_confusion=10.0,
        consumer_waste_behavior=10.0,
        redistribution_gap=8.0,
        composting_infrastructure=15.0,
        regulatory_compliance_gap=8.0,
        supply_chain_inefficiency=10.0,
        packaging_waste_impact=8.0,
        food_bank_capacity=85.0,
        corporate_responsibility_gap=10.0,
        circular_economy_adoption=20.0,
        economic_loss_per_capita=60.0,
        biodiversity_impact=8.0,
        water_waste_embedded=10.0,
        carbon_footprint_waste=10.0,
    ),
]
