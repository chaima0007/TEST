from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0ea5e9"


@dataclass
class AsylumRightsEntity:
    entity_id: str
    name: str
    country: str
    refoulement_score: float
    asylum_procedure_score: float
    detention_asylum_seekers_score: float
    legal_aid_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_asylum_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.refoulement_score * 0.30
            + self.asylum_procedure_score * 0.25
            + self.detention_asylum_seekers_score * 0.25
            + self.legal_aid_gap_score * 0.20,
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
        self.estimated_asylum_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class AsylumRightsEngineResult:
    agent: str = "Asylum Rights Engine Agent"
    domain: str = "asylum_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_asylum_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AsylumRightsEntity] = field(default_factory=list)


def run_asylum_rights_engine() -> AsylumRightsEngineResult:
    entities = [
        AsylumRightsEntity(
            entity_id="ASR-001",
            name="Libye — Centre Détention Tariq al-Sikka, Torture Migrants & Refoulement vers Mer",
            country="Libye",
            refoulement_score=97.0,
            asylum_procedure_score=95.0,
            detention_asylum_seekers_score=96.0,
            legal_aid_gap_score=93.0,
            primary_pattern="refoulement",
        ),
        AsylumRightsEntity(
            entity_id="ASR-002",
            name="Grèce — Pushbacks Documentés CEDH, Refoulements Mer Égée & Conditions Moria",
            country="Grèce",
            refoulement_score=92.0,
            asylum_procedure_score=90.0,
            detention_asylum_seekers_score=89.0,
            legal_aid_gap_score=88.0,
            primary_pattern="refoulement",
        ),
        AsylumRightsEntity(
            entity_id="ASR-003",
            name="Mexique/USA Frontière — MPP Remain in Mexico, Titre 42 & Violence Cartels",
            country="Mexique/USA",
            refoulement_score=86.0,
            asylum_procedure_score=84.0,
            detention_asylum_seekers_score=83.0,
            legal_aid_gap_score=82.0,
            primary_pattern="detention_asylum_seekers",
        ),
        AsylumRightsEntity(
            entity_id="ASR-004",
            name="Australie — Offshore Processing Manus/Nauru, Détention 10 Ans & Condamnations CEDH",
            country="Australie",
            refoulement_score=80.0,
            asylum_procedure_score=78.0,
            detention_asylum_seekers_score=77.0,
            legal_aid_gap_score=76.0,
            primary_pattern="detention_asylum_seekers",
        ),
        AsylumRightsEntity(
            entity_id="ASR-005",
            name="UE Hongrie/Pologne — Clôtures Frontières, Pushbacks Documentés & Discours Criminalisation",
            country="UE (Hongrie/Pologne)",
            refoulement_score=57.0,
            asylum_procedure_score=55.0,
            detention_asylum_seekers_score=54.0,
            legal_aid_gap_score=53.0,
            primary_pattern="refoulement",
        ),
        AsylumRightsEntity(
            entity_id="ASR-006",
            name="UK — Rwanda Plan, Illegal Migration Act 2023 & Backlog 160k Demandes",
            country="UK",
            refoulement_score=49.0,
            asylum_procedure_score=47.0,
            detention_asylum_seekers_score=46.0,
            legal_aid_gap_score=45.0,
            primary_pattern="asylum_procedure",
        ),
        AsylumRightsEntity(
            entity_id="ASR-007",
            name="Canada — IRCC Backlogs, Safe Third Country Agreement Élargi & Protections Partielles",
            country="Canada",
            refoulement_score=32.0,
            asylum_procedure_score=30.0,
            detention_asylum_seekers_score=29.0,
            legal_aid_gap_score=28.0,
            primary_pattern="legal_aid_gap",
        ),
        AsylumRightsEntity(
            entity_id="ASR-008",
            name="UNHCR — Convention 1951, Global Compact Refugees & Standard Protection Internationale",
            country="Global",
            refoulement_score=13.0,
            asylum_procedure_score=12.0,
            detention_asylum_seekers_score=11.0,
            legal_aid_gap_score=12.0,
            primary_pattern="asylum_procedure",
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

    return AsylumRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_asylum_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_global_trends_forced_displacement_2024",
            "hrw_refugee_asylum_pushbacks_documentation",
            "amnesty_international_asylum_seekers_detention_2024",
            "echr_cases_non_refoulement_violations_2024",
            "borderline_europe_pushbacks_observatory",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_asylum_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
