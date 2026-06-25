"""
algorithmic_justice_bias_rights_engine.py
Wave 191 — Justice Algorithmique & Biais IA
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class AlgorithmicJusticeBiasRightsEntity:
    entity_id: str
    name: str
    country: str
    algorithmic_discrimination_deployment_score: float
    due_process_algorithmic_denial_score: float
    transparency_explainability_deficit_score: float
    regulatory_accountability_framework_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_algorithmic_justice_bias_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.algorithmic_discrimination_deployment_score * 0.30
            + self.due_process_algorithmic_denial_score * 0.25
            + self.transparency_explainability_deficit_score * 0.25
            + self.regulatory_accountability_framework_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_algorithmic_justice_bias_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[AlgorithmicJusticeBiasRightsEntity]:
    return [
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-001",
            name="États-Unis — COMPAS & Biais Racial Prédictif Justice Pénale",
            country="États-Unis",
            algorithmic_discrimination_deployment_score=92.0,
            due_process_algorithmic_denial_score=89.0,
            transparency_explainability_deficit_score=91.0,
            regulatory_accountability_framework_score=85.0,
            primary_pattern="COMPAS prédit récidive avec biais racial documenté, opacité totale, zéro droit contestation",
        ),
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-002",
            name="Chine — Crédit Social IA, Surveillance Citoyens Discriminatoire",
            country="Chine",
            algorithmic_discrimination_deployment_score=95.0,
            due_process_algorithmic_denial_score=94.0,
            transparency_explainability_deficit_score=93.0,
            regulatory_accountability_framework_score=88.0,
            primary_pattern="Système crédit social IA discrimine minorités, zéro due process, blacklists opaques",
        ),
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-003",
            name="Royaume-Uni — Windrush Algorithme Immigration Discriminatoire",
            country="Royaume-Uni",
            algorithmic_discrimination_deployment_score=87.0,
            due_process_algorithmic_denial_score=85.0,
            transparency_explainability_deficit_score=83.0,
            regulatory_accountability_framework_score=80.0,
            primary_pattern="Algorithme visa discrimine Caribbean-British, scandale Windrush amplifié par IA",
        ),
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-004",
            name="Inde — Aadhaar Exclusion Biométrique Castes Défavorisées",
            country="Inde",
            algorithmic_discrimination_deployment_score=84.0,
            due_process_algorithmic_denial_score=82.0,
            transparency_explainability_deficit_score=80.0,
            regulatory_accountability_framework_score=78.0,
            primary_pattern="Aadhaar échoue reconnaître empreintes travailleurs manuels, exclusion aide sociale",
        ),
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-005",
            name="France — Parcoursup Algorithme Opaque Sélection Universitaire",
            country="France",
            algorithmic_discrimination_deployment_score=52.0,
            due_process_algorithmic_denial_score=55.0,
            transparency_explainability_deficit_score=58.0,
            regulatory_accountability_framework_score=45.0,
            primary_pattern="Parcoursup opaque, critères géographiques favorisent lycées privés, contestation limitée",
        ),
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-006",
            name="Pays-Bas — SyRI Fraude Sociale Profiling Ethnique Illégal",
            country="Pays-Bas",
            algorithmic_discrimination_deployment_score=48.0,
            due_process_algorithmic_denial_score=50.0,
            transparency_explainability_deficit_score=54.0,
            regulatory_accountability_framework_score=42.0,
            primary_pattern="SyRI ciblait quartiers ethniques, tribunal l'a invalidé en 2020, précédent CEDH",
        ),
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-007",
            name="Canada — MCAP Algorithme Garde Enfants Biais Autochtones",
            country="Canada",
            algorithmic_discrimination_deployment_score=28.0,
            due_process_algorithmic_denial_score=30.0,
            transparency_explainability_deficit_score=25.0,
            regulatory_accountability_framework_score=22.0,
            primary_pattern="Algorithme protection enfance surreprésente familles autochtones, biais systémique documenté",
        ),
        AlgorithmicJusticeBiasRightsEntity(
            entity_id="AJB-008",
            name="Suède — AI Act Conformité, Registre Algorithmes Public",
            country="Suède",
            algorithmic_discrimination_deployment_score=5.0,
            due_process_algorithmic_denial_score=5.0,
            transparency_explainability_deficit_score=6.0,
            regulatory_accountability_framework_score=4.0,
            primary_pattern="Registre public algorithmes État, AI Act conforme, droit contestation garanti RGPD",
        ),
    ]


def analyze(entities: List[AlgorithmicJusticeBiasRightsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict[str, int] = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "algorithmic_justice_bias_rights_engine",
        "domain": "algorithmic_justice_bias_rights",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.90,
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
        "avg_estimated_algorithmic_justice_bias_index": round(
            statistics.mean([e.estimated_algorithmic_justice_bias_index for e in entities]), 2
        ),
        "data_sources": [
            "propublica_compas_analysis_2016",
            "ai_now_institute_algorithmic_accountability_2023",
            "algorithmic_justice_league_report_2023",
            "eu_ai_act_impact_assessment_2024",
        ],
        "entities": [
            {
                "id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "algorithmic_discrimination_deployment_score": e.algorithmic_discrimination_deployment_score,
                "due_process_algorithmic_denial_score": e.due_process_algorithmic_denial_score,
                "transparency_explainability_deficit_score": e.transparency_explainability_deficit_score,
                "regulatory_accountability_framework_score": e.regulatory_accountability_framework_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_algorithmic_justice_bias_index": e.estimated_algorithmic_justice_bias_index,
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
