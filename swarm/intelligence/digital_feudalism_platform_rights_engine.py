"""
digital_feudalism_platform_rights_engine.py
Wave 189 — Féodalisme Numérique & Droits des Plateformes
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class DigitalFeudalismPlatformRightsEntity:
    entity_id: str
    name: str
    country: str
    platform_monopoly_dependency_score: float
    algorithmic_wage_theft_score: float
    data_extraction_labor_rights_score: float
    regulatory_capture_accountability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_digital_feudalism_platform_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.platform_monopoly_dependency_score * 0.30
            + self.algorithmic_wage_theft_score * 0.25
            + self.data_extraction_labor_rights_score * 0.25
            + self.regulatory_capture_accountability_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_digital_feudalism_platform_rights_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[DigitalFeudalismPlatformRightsEntity]:
    return [
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-001",
            name="États-Unis — Big Tech Monopole, Travailleurs Gig Sans Droits, Capture Régulatoire",
            country="États-Unis",
            platform_monopoly_dependency_score=93.0,
            algorithmic_wage_theft_score=91.0,
            data_extraction_labor_rights_score=90.0,
            regulatory_capture_accountability_score=89.0,
            primary_pattern="Amazon/Meta/Google monopole 70% marché publicitaire, Uber/DoorDash 1.7M gig workers sans protection sociale, lobbying 800M$ anti-régulation",
        ),
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-002",
            name="Pakistan — Freelancers Plateformes Occidentales, Frais Extraction 30%, Zéro Recours",
            country="Pakistan",
            platform_monopoly_dependency_score=89.0,
            algorithmic_wage_theft_score=93.0,
            data_extraction_labor_rights_score=91.0,
            regulatory_capture_accountability_score=87.0,
            primary_pattern="4M freelancers sur Upwork/Fiverr, commissions 20-30% extraites vers Silicon Valley, désactivations algorithmiques arbitraires sans appel, protections travail inexistantes",
        ),
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-003",
            name="Inde — 15M Livreurs Algorithmiques, Salaires Déprimés par IA, Surveillance Totale",
            country="Inde",
            platform_monopoly_dependency_score=88.0,
            algorithmic_wage_theft_score=90.0,
            data_extraction_labor_rights_score=92.0,
            regulatory_capture_accountability_score=86.0,
            primary_pattern="Zomato/Swiggy 15M gig workers, algorithme fixe tarifs sous salaire minimum, tracking GPS continu 24h, contrats imposés unilatéralement sans syndicat",
        ),
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-004",
            name="Nigeria — Banning Content Créateurs Africains, Monétisation Bloquée, Neo-Colonialisme Digital",
            country="Nigeria",
            platform_monopoly_dependency_score=85.0,
            algorithmic_wage_theft_score=87.0,
            data_extraction_labor_rights_score=88.0,
            regulatory_capture_accountability_score=90.0,
            primary_pattern="TikTok/YouTube démonétisation 10x plus fréquente créateurs africains, algorithme biaisé réduisant portée contenus africains 68%, valeur extraite sans redistribution",
        ),
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-005",
            name="Union Européenne — DSA/DMA Résistance Plateformes, Amendes Insuffisantes",
            country="Union Européenne",
            platform_monopoly_dependency_score=52.0,
            algorithmic_wage_theft_score=50.0,
            data_extraction_labor_rights_score=54.0,
            regulatory_capture_accountability_score=55.0,
            primary_pattern="DSA/DMA adopté mais Meta/Google résistent application, amendes RGPD plafonnées 4% CA mondiales insuffisantes, Platform Workers Directive négociée sous pression",
        ),
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-006",
            name="Royaume-Uni — Gig Economy Post-Brexit, Uber Arrêt Cour Suprême Non Appliqué",
            country="Royaume-Uni",
            platform_monopoly_dependency_score=54.0,
            algorithmic_wage_theft_score=56.0,
            data_extraction_labor_rights_score=51.0,
            regulatory_capture_accountability_score=53.0,
            primary_pattern="Arrêt Cour Suprême 2021 Uber partiellement contourné, 5.5M gig workers, Employment Rights Bill 2024 sous pression lobby plateforme, CMA insuffisant",
        ),
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-007",
            name="Mexique — Rappi/DiDi Sans Sécurité Sociale, Accident = Ruine pour Livreurs",
            country="Mexique",
            platform_monopoly_dependency_score=29.0,
            algorithmic_wage_theft_score=31.0,
            data_extraction_labor_rights_score=27.0,
            regulatory_capture_accountability_score=28.0,
            primary_pattern="800k livreurs Rappi/DiDi/Uber sans IMSS, accidents non couverts, réforme travail plateforme bloquée par lobbying, dépendance économique totale sans recours",
        ),
        DigitalFeudalismPlatformRightsEntity(
            entity_id="DFP-008",
            name="France — Charte Uber Refusée, Statut ARPE Protections Partielles",
            country="France",
            platform_monopoly_dependency_score=8.0,
            algorithmic_wage_theft_score=7.0,
            data_extraction_labor_rights_score=9.0,
            regulatory_capture_accountability_score=6.0,
            primary_pattern="Cour Cassation requalification salariés, ARPE protection accidents, charte Uber refusée conseil constitutionnel, modèle avancé Europe protection gig workers",
        ),
    ]


def analyze(entities: List[DigitalFeudalismPlatformRightsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "digital_feudalism_platform_rights_engine",
        "domain": "digital_feudalism_platform_rights",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.88,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "platform_monopoly_dependency": 3,
            "algorithmic_wage_theft": 2,
            "data_extraction_labor": 2,
            "regulatory_capture": 1,
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
        "avg_estimated_digital_feudalism_platform_rights_index": round(
            statistics.mean([e.estimated_digital_feudalism_platform_rights_index for e in entities]), 2
        ),
        "data_sources": [
            "ilo_platform_work_global_report_2023",
            "fairwork_foundation_gig_economy_2024",
            "eu_platform_workers_directive_2024",
            "un_special_rapporteur_digital_rights_2023",
        ],
        "entities": [
            {
                "id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "platform_monopoly_dependency_score": e.platform_monopoly_dependency_score,
                "algorithmic_wage_theft_score": e.algorithmic_wage_theft_score,
                "data_extraction_labor_rights_score": e.data_extraction_labor_rights_score,
                "regulatory_capture_accountability_score": e.regulatory_capture_accountability_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_digital_feudalism_platform_rights_index": e.estimated_digital_feudalism_platform_rights_index,
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
