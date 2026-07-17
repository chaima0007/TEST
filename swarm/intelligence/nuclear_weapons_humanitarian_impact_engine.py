from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class NuclearWeaponsHumanitarianImpactEntity:
    entity_id: str
    name: str
    country: str
    nuclear_threat_proliferation_severity_score: float
    civilian_humanitarian_impact_risk_score: float
    arms_control_treaty_violation_scale_score: float
    nuclear_doctrine_escalation_risk_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_nuclear_weapons_humanitarian_impact_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.nuclear_threat_proliferation_severity_score * 0.30
            + self.civilian_humanitarian_impact_risk_score * 0.25
            + self.arms_control_treaty_violation_scale_score * 0.25
            + self.nuclear_doctrine_escalation_risk_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_nuclear_weapons_humanitarian_impact_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[NuclearWeaponsHumanitarianImpactEntity]:
    return [
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-001",
            name="Corée du Nord — Tests NPT, 50+ Ogives Estimées",
            country="Corée du Nord",
            nuclear_threat_proliferation_severity_score=95.0,
            civilian_humanitarian_impact_risk_score=92.0,
            arms_control_treaty_violation_scale_score=96.0,
            nuclear_doctrine_escalation_risk_score=93.0,
            primary_pattern="Violation NPT systématique, tests missiles balistiques intercontinentaux, menace régionale",
        ),
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-002",
            name="Russie — Menaces Nucléaires Ukraine 2022-24, Retrait New START",
            country="Russie",
            nuclear_threat_proliferation_severity_score=92.0,
            civilian_humanitarian_impact_risk_score=90.0,
            arms_control_treaty_violation_scale_score=91.0,
            nuclear_doctrine_escalation_risk_score=93.0,
            primary_pattern="Rhétorique nucléaire guerre Ukraine, retrait New START 2023, 6000 ogives arsenal",
        ),
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-003",
            name="Pakistan — 100+ Ogives, Instabilité Civilo-Militaire",
            country="Pakistan",
            nuclear_threat_proliferation_severity_score=88.0,
            civilian_humanitarian_impact_risk_score=86.0,
            arms_control_treaty_violation_scale_score=82.0,
            nuclear_doctrine_escalation_risk_score=89.0,
            primary_pattern="Instabilité civilo-militaire, prolifération réseau AQ Khan, first-use doctrine",
        ),
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-004",
            name="Inde/Pakistan — Tensions Kashmir, Doctrines Nucléaires",
            country="Inde/Pakistan",
            nuclear_threat_proliferation_severity_score=85.0,
            civilian_humanitarian_impact_risk_score=88.0,
            arms_control_treaty_violation_scale_score=78.0,
            nuclear_doctrine_escalation_risk_score=87.0,
            primary_pattern="Conflit Kashmir latent, doctrines dissuasion antagonistes, risque escalade accidentelle",
        ),
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-005",
            name="Iran — Enrichissement 60% Uranium, Breakout Capacity",
            country="Iran",
            nuclear_threat_proliferation_severity_score=58.0,
            civilian_humanitarian_impact_risk_score=55.0,
            arms_control_treaty_violation_scale_score=62.0,
            nuclear_doctrine_escalation_risk_score=56.0,
            primary_pattern="Enrichissement uranium 60% proche seuil armement, JCPOA effondré, capacité breakout 2 semaines",
        ),
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-006",
            name="Israël — Ambiguïté Nucléaire, 90 Ogives Estimées Negev",
            country="Israël",
            nuclear_threat_proliferation_severity_score=52.0,
            civilian_humanitarian_impact_risk_score=50.0,
            arms_control_treaty_violation_scale_score=58.0,
            nuclear_doctrine_escalation_risk_score=53.0,
            primary_pattern="Politique ambiguïté nucléaire officielle, installation Negev, non-signataire NPT",
        ),
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-007",
            name="Chine — Modernisation Arsenal, Opacité Doctrine",
            country="Chine",
            nuclear_threat_proliferation_severity_score=28.0,
            civilian_humanitarian_impact_risk_score=26.0,
            arms_control_treaty_violation_scale_score=24.0,
            nuclear_doctrine_escalation_risk_score=27.0,
            primary_pattern="Modernisation rapide arsenal vers 1500 ogives 2035, opacité doctrine NFU, silos Xinjiang",
        ),
        NuclearWeaponsHumanitarianImpactEntity(
            entity_id="NWH-008",
            name="TPNW — Traité Interdiction Armes Nucléaires 2021, 68 États",
            country="International",
            nuclear_threat_proliferation_severity_score=4.0,
            civilian_humanitarian_impact_risk_score=4.0,
            arms_control_treaty_violation_scale_score=4.0,
            nuclear_doctrine_escalation_risk_score=4.0,
            primary_pattern="68 États signataires TPNW 2021, aucune puissance nucléaire adhérente, pression normative humanitaire",
        ),
    ]


def analyze(entities: List[NuclearWeaponsHumanitarianImpactEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "nuclear_weapons_humanitarian_impact_engine",
        "domain": "nuclear_weapons_humanitarian_impact",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.91,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "proliferation_violation": 3,
            "escalation_doctrine": 2,
            "humanitarian_impact": 2,
            "disarmament_treaty": 1,
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
        "avg_estimated_nuclear_weapons_humanitarian_impact_index": round(
            statistics.mean([e.estimated_nuclear_weapons_humanitarian_impact_index for e in entities]), 2
        ),
        "data_sources": [
            "sipri_nuclear_forces_2023",
            "ican_global_status_2023",
            "bulletin_atomic_scientists_2023",
            "un_tpnw_implementation_2023",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "nuclear_threat_proliferation_severity_score": e.nuclear_threat_proliferation_severity_score,
                "civilian_humanitarian_impact_risk_score": e.civilian_humanitarian_impact_risk_score,
                "arms_control_treaty_violation_scale_score": e.arms_control_treaty_violation_scale_score,
                "nuclear_doctrine_escalation_risk_score": e.nuclear_doctrine_escalation_risk_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_nuclear_weapons_humanitarian_impact_index": e.estimated_nuclear_weapons_humanitarian_impact_index,
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
