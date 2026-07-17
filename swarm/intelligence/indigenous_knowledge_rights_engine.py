from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#d97706"


@dataclass
class IndigenousKnowledgeRightsEntity:
    entity_id: str
    name: str
    country: str
    biopiracy_score: float
    cultural_appropriation_score: float
    language_extinction_score: float
    sacred_site_protection_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_indigenous_knowledge_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.biopiracy_score * 0.30
            + self.cultural_appropriation_score * 0.25
            + self.language_extinction_score * 0.25
            + self.sacred_site_protection_score * 0.20,
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
        self.estimated_indigenous_knowledge_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class IndigenousKnowledgeRightsEngineResult:
    agent: str = "Indigenous Knowledge Rights Engine Agent"
    domain: str = "indigenous_knowledge_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_indigenous_knowledge_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IndigenousKnowledgeRightsEntity] = field(default_factory=list)


def run_indigenous_knowledge_rights_engine() -> IndigenousKnowledgeRightsEngineResult:
    entities = [
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-001",
            name="Inde (Ayurveda/Yoga) — Brevets Basmati/Neem/Turmeric & TKDL Base Données Réponse",
            country="Inde",
            biopiracy_score=97.0,
            cultural_appropriation_score=95.0,
            language_extinction_score=91.0,
            sacred_site_protection_score=93.0,
            primary_pattern="biopiracy",
        ),
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-002",
            name="Amazonie (Ayahuasca) — Brevets USA Plantes Sacrées & Big Pharma Exploitant Chamanes",
            country="Brésil/Pérou",
            biopiracy_score=91.0,
            cultural_appropriation_score=89.0,
            language_extinction_score=85.0,
            sacred_site_protection_score=87.0,
            primary_pattern="biopiracy",
        ),
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-003",
            name="Afrique du Sud (Rooibos/Hoodia) — San Peuple Sans Compensation Multinationales & ABS Fragile",
            country="Afrique du Sud",
            biopiracy_score=85.0,
            cultural_appropriation_score=82.0,
            language_extinction_score=79.0,
            sacred_site_protection_score=80.0,
            primary_pattern="biopiracy",
        ),
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-004",
            name="Papouasie (PNG) — 800 Langues en Danger, Multinationales Minières & Sites Sacrés Détruits",
            country="Papouasie-Nouvelle-Guinée",
            biopiracy_score=77.0,
            cultural_appropriation_score=76.0,
            language_extinction_score=78.0,
            sacred_site_protection_score=74.0,
            primary_pattern="language_extinction",
        ),
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-005",
            name="Mexique — Maïs Transgénique Menaçant Variétés Indigènes & Masques Zapotèques Appropriés",
            country="Mexique",
            biopiracy_score=56.0,
            cultural_appropriation_score=54.0,
            language_extinction_score=53.0,
            sacred_site_protection_score=51.0,
            primary_pattern="cultural_appropriation",
        ),
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-006",
            name="Canada/First Nations — Ressources Génétiques Sans FPIC & UNDRIP Ratifié Mais Incomplet",
            country="Canada",
            biopiracy_score=48.0,
            cultural_appropriation_score=46.0,
            language_extinction_score=45.0,
            sacred_site_protection_score=43.0,
            primary_pattern="biopiracy",
        ),
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-007",
            name="Australie — Native Title + ATSI Heritage Act 2021 & Sites Sacrés Mieux Protégés",
            country="Australie",
            biopiracy_score=32.0,
            cultural_appropriation_score=30.0,
            language_extinction_score=29.0,
            sacred_site_protection_score=28.0,
            primary_pattern="sacred_site_protection",
        ),
        IndigenousKnowledgeRightsEntity(
            entity_id="IKR-008",
            name="Nagoya Protocol/WIPO IGC — Accord ABS, Négociations Instrument International & Cadre Émergent",
            country="Global",
            biopiracy_score=11.0,
            cultural_appropriation_score=10.0,
            language_extinction_score=9.0,
            sacred_site_protection_score=10.0,
            primary_pattern="biopiracy",
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

    return IndigenousKnowledgeRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_indigenous_knowledge_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "wipo_intergovernmental_committee_traditional_knowledge",
            "un_declaration_rights_indigenous_peoples_implementation",
            "cbd_nagoya_protocol_access_benefit_sharing_reports",
            "cultural_survival_indigenous_rights_violations_2024",
            "grain_biopiracy_cases_database",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_indigenous_knowledge_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
