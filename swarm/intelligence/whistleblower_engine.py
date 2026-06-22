#!/usr/bin/env python3
"""CaelumSwarm™ — Whistleblower Protection Risk Engine (EU Directive 2019/1937)"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class WhistleblowerEntity:
    entity_id: str
    name: str
    country: str
    retaliation_exposure_score: float
    legal_protection_gap_score: float
    reporting_channel_obstruction_score: float
    identity_disclosure_risk_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_whistleblower_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.retaliation_exposure_score * 0.30
            + self.legal_protection_gap_score * 0.25
            + self.reporting_channel_obstruction_score * 0.25
            + self.identity_disclosure_risk_score * 0.20,
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
        self.estimated_whistleblower_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class WhistleblowerEngineResult:
    agent: str = "Whistleblower Protection Risk Engine Agent"
    domain: str = "whistleblower"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_whistleblower_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WhistleblowerEntity] = field(default_factory=list)


def run_whistleblower_engine() -> WhistleblowerEngineResult:
    entities = [
        WhistleblowerEntity(
            entity_id="WB-001",
            name="Chine — Lanceurs Alerte COVID Emprisonnés, Censure Signalements & Représailles Fonctionnaires",
            country="Asie",
            retaliation_exposure_score=99.0,
            legal_protection_gap_score=97.0,
            reporting_channel_obstruction_score=95.0,
            identity_disclosure_risk_score=93.0,
            primary_pattern="retaliation_exposure",
        ),
        WhistleblowerEntity(
            entity_id="WB-002",
            name="Arabie Saoudite — Cas Jamal Khashoggi, Poursuites Activistes & Absence Protection Légale",
            country="Moyen-Orient",
            retaliation_exposure_score=93.0,
            legal_protection_gap_score=90.0,
            reporting_channel_obstruction_score=88.0,
            identity_disclosure_risk_score=86.0,
            primary_pattern="identity_disclosure_risk",
        ),
        WhistleblowerEntity(
            entity_id="WB-003",
            name="Russie — Loi Agents Étrangers, Criminalisation Divulgations & Persécution Journalistes-Sources",
            country="Europe de l'Est",
            retaliation_exposure_score=85.0,
            legal_protection_gap_score=82.0,
            reporting_channel_obstruction_score=80.0,
            identity_disclosure_risk_score=78.0,
            primary_pattern="legal_protection_gap",
        ),
        WhistleblowerEntity(
            entity_id="WB-004",
            name="États-Unis — Affaire Snowden, Poursuites Espionage Act & Lacunes Protection Secteur Renseignement",
            country="Amérique du Nord",
            retaliation_exposure_score=80.0,
            legal_protection_gap_score=77.0,
            reporting_channel_obstruction_score=75.0,
            identity_disclosure_risk_score=73.0,
            primary_pattern="legal_protection_gap",
        ),
        WhistleblowerEntity(
            entity_id="WB-005",
            name="Turquie — Représailles Journalistes-Lanceurs Alerte, Loi Antiterrorisme & Pressions Judiciaires",
            country="Europe",
            retaliation_exposure_score=61.0,
            legal_protection_gap_score=58.0,
            reporting_channel_obstruction_score=56.0,
            identity_disclosure_risk_score=54.0,
            primary_pattern="retaliation_exposure",
        ),
        WhistleblowerEntity(
            entity_id="WB-006",
            name="Inde — Cas Satyendra Dubey, Manque Canaux Signalement & Impunité Représailles Secteur Public",
            country="Asie",
            retaliation_exposure_score=51.0,
            legal_protection_gap_score=48.0,
            reporting_channel_obstruction_score=46.0,
            identity_disclosure_risk_score=44.0,
            primary_pattern="reporting_channel_obstruction",
        ),
        WhistleblowerEntity(
            entity_id="WB-007",
            name="Union Européenne — Directive 2019/1937 Transposition, Canaux Internes & Mécanismes Autorités",
            country="Europe",
            retaliation_exposure_score=32.0,
            legal_protection_gap_score=29.0,
            reporting_channel_obstruction_score=27.0,
            identity_disclosure_risk_score=25.0,
            primary_pattern="reporting_channel_obstruction",
        ),
        WhistleblowerEntity(
            entity_id="WB-008",
            name="Transparency International / Whistleblowing International Network — Standards & Advocacy",
            country="Global",
            retaliation_exposure_score=13.0,
            legal_protection_gap_score=11.0,
            reporting_channel_obstruction_score=9.0,
            identity_disclosure_risk_score=7.0,
            primary_pattern="identity_disclosure_risk",
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

    return WhistleblowerEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_whistleblower_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "eu_directive_2019_1937_whistleblower_protection_transposition_tracker",
            "transparency_international_whistleblowing_laws_global_assessment",
            "whistleblowing_international_network_country_profiles_2025",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_whistleblower_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_whistleblower_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
