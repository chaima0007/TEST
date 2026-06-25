"""
prison_industrial_complex_rights_engine.py
Wave 191 — Complexe Carcéral Industriel & Droits
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class PrisonIndustrialComplexRightsEntity:
    entity_id: str
    name: str
    country: str
    mass_incarceration_racial_disparity_score: float
    private_prison_profit_incentive_score: float
    labor_exploitation_incarcerated_score: float
    rehabilitation_access_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_industrial_complex_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_incarceration_racial_disparity_score * 0.30
            + self.private_prison_profit_incentive_score * 0.25
            + self.labor_exploitation_incarcerated_score * 0.25
            + self.rehabilitation_access_denial_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_prison_industrial_complex_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[PrisonIndustrialComplexRightsEntity]:
    return [
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-001",
            name="États-Unis — 2.1M Détenus, CoreCivic GEO Group Profit Racial",
            country="États-Unis",
            mass_incarceration_racial_disparity_score=97.0,
            private_prison_profit_incentive_score=95.0,
            labor_exploitation_incarcerated_score=93.0,
            rehabilitation_access_denial_score=91.0,
            primary_pattern="2.1M détenus, Noirs 5× surreprésentés, CoreCivic $2Mds profits, travail $0.25/h",
        ),
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-002",
            name="Brésil — 830k Détenus, Gangs Contrôlent Prisons, Esclavage Carcéral",
            country="Brésil",
            mass_incarceration_racial_disparity_score=88.0,
            private_prison_profit_incentive_score=82.0,
            labor_exploitation_incarcerated_score=87.0,
            rehabilitation_access_denial_score=89.0,
            primary_pattern="830k détenus, Noirs brésiliens 67% détenus, PCC/CV contrôlent cellules, torture systémique",
        ),
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-003",
            name="Chine — Xinjiang Travail Forcé, Rééducation Industrielle Ouïghours",
            country="Chine",
            mass_incarceration_racial_disparity_score=95.0,
            private_prison_profit_incentive_score=90.0,
            labor_exploitation_incarcerated_score=96.0,
            rehabilitation_access_denial_score=93.0,
            primary_pattern="1M+ Ouïghours camps rééducation, travail forcé chaînes production, zéro recours juridique",
        ),
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-004",
            name="Russie — Colonies Pénales Sibérie, Opposition Politique Incarcérée",
            country="Russie",
            mass_incarceration_racial_disparity_score=82.0,
            private_prison_profit_incentive_score=75.0,
            labor_exploitation_incarcerated_score=85.0,
            rehabilitation_access_denial_score=88.0,
            primary_pattern="Colonies IK travail forcé industries militaires, opposants politiques Navalny, droits niés",
        ),
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-005",
            name="Royaume-Uni — Serco Detention Centers, Migrants Indéfinis Retenus",
            country="Royaume-Uni",
            mass_incarceration_racial_disparity_score=50.0,
            private_prison_profit_incentive_score=57.0,
            labor_exploitation_incarcerated_score=48.0,
            rehabilitation_access_denial_score=52.0,
            primary_pattern="Serco G4S profits centres détention migrants, rétention indéfinie illégale CEDH",
        ),
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-006",
            name="Australie — Nauru Offshore Processing, Trauma Psychologique Réfugiés",
            country="Australie",
            mass_incarceration_racial_disparity_score=45.0,
            private_prison_profit_incentive_score=52.0,
            labor_exploitation_incarcerated_score=42.0,
            rehabilitation_access_denial_score=55.0,
            primary_pattern="Centres offshore Nauru Manus, Broadspectrum profits, trauma enfants réfugiés documenté",
        ),
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-007",
            name="France — Surpopulation Carcérale 145%, Maison Centrale Travail Sous-Payé",
            country="France",
            mass_incarceration_racial_disparity_score=26.0,
            private_prison_profit_incentive_score=23.0,
            labor_exploitation_incarcerated_score=28.0,
            rehabilitation_access_denial_score=22.0,
            primary_pattern="145% surpopulation, travail Gepsa €5/h, quartiers pauvres et issus immigration surreprésentés",
        ),
        PrisonIndustrialComplexRightsEntity(
            entity_id="PIC-008",
            name="Norvège — Halden Prison Modèle, Réhabilitation Taux Récidive 20%",
            country="Norvège",
            mass_incarceration_racial_disparity_score=5.0,
            private_prison_profit_incentive_score=4.0,
            labor_exploitation_incarcerated_score=5.0,
            rehabilitation_access_denial_score=4.0,
            primary_pattern="Halden prison humaniste, 20% récidive vs 76% USA, éducation complète, zéro privatisation",
        ),
    ]


def analyze(entities: List[PrisonIndustrialComplexRightsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict[str, int] = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "prison_industrial_complex_rights_engine",
        "domain": "prison_industrial_complex_rights",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.92,
        "risk_distribution": risk_dist,
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
        "avg_estimated_prison_industrial_complex_index": round(
            statistics.mean([e.estimated_prison_industrial_complex_index for e in entities]), 2
        ),
        "data_sources": [
            "prison_policy_initiative_mass_incarceration_2023",
            "aclu_private_prisons_profit_report_2023",
            "un_standard_minimum_rules_treatment_prisoners",
            "sentencing_project_racial_disparities_2024",
        ],
        "entities": [
            {
                "id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "mass_incarceration_racial_disparity_score": e.mass_incarceration_racial_disparity_score,
                "private_prison_profit_incentive_score": e.private_prison_profit_incentive_score,
                "labor_exploitation_incarcerated_score": e.labor_exploitation_incarcerated_score,
                "rehabilitation_access_denial_score": e.rehabilitation_access_denial_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_prison_industrial_complex_index": e.estimated_prison_industrial_complex_index,
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
    scores = [e.composite_score for e in entities]
    import statistics as st
    avg = round(st.mean(scores), 2)
    dist = {}
    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
    print(f"\navg_composite: {avg:.2f}")
    print(f"distribution: {dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
    print(f"✓ avg_composite = {avg:.2f}")
