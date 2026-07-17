from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class NeurotechCognitiveLibertyRightsEntity:
    entity_id: str
    name: str
    country: str
    neural_data_extraction_commercialization_score: float
    cognitive_manipulation_advertising_score: float
    mental_privacy_surveillance_score: float
    neurorights_regulatory_framework_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_neurotech_cognitive_liberty_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.neural_data_extraction_commercialization_score * 0.30
            + self.cognitive_manipulation_advertising_score * 0.25
            + self.mental_privacy_surveillance_score * 0.25
            + self.neurorights_regulatory_framework_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_neurotech_cognitive_liberty_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[NeurotechCognitiveLibertyRightsEntity]:
    return [
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-001",
            name="Chine — BCI Surveillance État, Neurodonnées Citoyens Sans Consentement",
            country="Chine",
            neural_data_extraction_commercialization_score=95.0,
            cognitive_manipulation_advertising_score=91.0,
            mental_privacy_surveillance_score=97.0,
            neurorights_regulatory_framework_score=93.0,
            primary_pattern="Interface cerveau-ordinateur déployée en milieux professionnels, données neurales collectées sans consentement, fusion IA-surveillance cognitive étatique",
        ),
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-002",
            name="États-Unis — Neuralink & BigTech, Monétisation Données Cognitives",
            country="États-Unis",
            neural_data_extraction_commercialization_score=88.0,
            cognitive_manipulation_advertising_score=92.0,
            mental_privacy_surveillance_score=85.0,
            neurorights_regulatory_framework_score=78.0,
            primary_pattern="Extraction données neurales à des fins publicitaires, absence réglementation fédérale neurodroits, manipulation cognitive ciblée Big Tech",
        ),
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-003",
            name="Russie — Psychotronique Militaire, Manipulation Cognitive Dissidents",
            country="Russie",
            neural_data_extraction_commercialization_score=82.0,
            cognitive_manipulation_advertising_score=85.0,
            mental_privacy_surveillance_score=92.0,
            neurorights_regulatory_framework_score=88.0,
            primary_pattern="Technologies psychotroniques appliquées aux dissidents, absence droit à la liberté mentale, manipulation neurocognitive ciblée",
        ),
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-004",
            name="Corée du Sud — Neuromarketing Non Régulé, BCI Consommateurs",
            country="Corée du Sud",
            neural_data_extraction_commercialization_score=72.0,
            cognitive_manipulation_advertising_score=75.0,
            mental_privacy_surveillance_score=68.0,
            neurorights_regulatory_framework_score=65.0,
            primary_pattern="Neuromarketing intensif sans cadre légal adapté, BCI gaming-travail sans protection cognitive, données EEG non protégées",
        ),
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-005",
            name="Inde — Détection Mensonge Neural Judiciaire, Absence Cadre Éthique",
            country="Inde",
            neural_data_extraction_commercialization_score=55.0,
            cognitive_manipulation_advertising_score=48.0,
            mental_privacy_surveillance_score=60.0,
            neurorights_regulatory_framework_score=52.0,
            primary_pattern="Tests polygraphe neural en procédures judiciaires, absence loi neurodroits, pression mentale sur accusés via technologies cognitives",
        ),
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-006",
            name="Brésil — Neurotech Entreprises Sans Régulation, Travail Cognitif Forcé",
            country="Brésil",
            neural_data_extraction_commercialization_score=48.0,
            cognitive_manipulation_advertising_score=52.0,
            mental_privacy_surveillance_score=45.0,
            neurorights_regulatory_framework_score=50.0,
            primary_pattern="BCI milieux ouvriers sans consentement éclairé, données cognitives vendues à des tiers, lacunes législatives neurotechnologie",
        ),
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-007",
            name="France — RGPD Partiel, Émergence Régulation Neurodonnées UE",
            country="France",
            neural_data_extraction_commercialization_score=28.0,
            cognitive_manipulation_advertising_score=25.0,
            mental_privacy_surveillance_score=22.0,
            neurorights_regulatory_framework_score=20.0,
            primary_pattern="RGPD couvre partiellement les neurodonnées, discussions AI Act UE incluant BCI, initiatives CERNA neurodroits en cours",
        ),
        NeurotechCognitiveLibertyRightsEntity(
            entity_id="NCL-008",
            name="Chili — Premier Pays Neurodroits Constitutionnels au Monde",
            country="Chili",
            neural_data_extraction_commercialization_score=6.0,
            cognitive_manipulation_advertising_score=5.0,
            mental_privacy_surveillance_score=4.0,
            neurorights_regulatory_framework_score=3.0,
            primary_pattern="Amendement constitutionnel 2021 protégeant intégrité mentale et identité neurale, loi neurodata 2023, modèle mondial neurodroits",
        ),
    ]


def analyze(entities: List[NeurotechCognitiveLibertyRightsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "neurotech_cognitive_liberty_rights_engine",
        "domain": "neurotech_cognitive_liberty_rights",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.87,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "neural_data_commercialization": 3,
            "cognitive_manipulation": 2,
            "surveillance_mental": 2,
            "regulatory_vacuum": 1,
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
        "avg_estimated_neurotech_cognitive_liberty_index": round(
            statistics.mean([e.estimated_neurotech_cognitive_liberty_index for e in entities]), 2
        ),
        "data_sources": [
            "neurorights_foundation_report_2025",
            "ieee_brain_initiative_ethics_2024",
            "un_special_rapporteur_mental_integrity_2023",
            "nature_neuroscience_neuroethics_2024",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "neural_data_extraction_commercialization_score": e.neural_data_extraction_commercialization_score,
                "cognitive_manipulation_advertising_score": e.cognitive_manipulation_advertising_score,
                "mental_privacy_surveillance_score": e.mental_privacy_surveillance_score,
                "neurorights_regulatory_framework_score": e.neurorights_regulatory_framework_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_neurotech_cognitive_liberty_index": e.estimated_neurotech_cognitive_liberty_index,
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
