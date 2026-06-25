from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WhistleblowerProtectionEntity:
    entity_id: str
    name: str
    country: str
    legal_framework_absence_score: float
    retaliation_prosecution_score: float
    state_surveillance_chilling_score: float
    media_source_protection_failure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_whistleblower_protection_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.legal_framework_absence_score * 0.30
            + self.retaliation_prosecution_score * 0.25
            + self.state_surveillance_chilling_score * 0.25
            + self.media_source_protection_failure_score * 0.20,
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
        self.estimated_whistleblower_protection_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class WhistleblowerProtectionEngineResult:
    agent: str = "Whistleblower Protection Engine Agent"
    domain: str = "whistleblower_protection"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_whistleblower_protection_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WhistleblowerProtectionEntity] = field(default_factory=list)

def run_whistleblower_protection_engine() -> WhistleblowerProtectionEngineResult:
    entities = [
        WhistleblowerProtectionEntity(
            entity_id="WP-001",
            name="Chine — Aucune Protection, Médecins COVID Arrêtés, Lanceurs Alerte Disparus",
            country="Asie du Nord-Est",
            legal_framework_absence_score=90.0,
            retaliation_prosecution_score=95.0,
            state_surveillance_chilling_score=95.0,
            media_source_protection_failure_score=90.0,
            primary_pattern="state_surveillance_chilling",
        ),
        WhistleblowerProtectionEntity(
            entity_id="WP-002",
            name="Russie — Répression Totale, Journalistes Tués, FSB Surveillance & Navalny Empoisonné",
            country="Europe de l'Est",
            legal_framework_absence_score=88.0,
            retaliation_prosecution_score=92.0,
            state_surveillance_chilling_score=90.0,
            media_source_protection_failure_score=85.0,
            primary_pattern="retaliation_prosecution",
        ),
        WhistleblowerProtectionEntity(
            entity_id="WP-003",
            name="Arabie Saoudite/Golfe — Khashoggi Assassiné, NSO Pegasus & Surveillance Dissidents",
            country="Moyen-Orient",
            legal_framework_absence_score=80.0,
            retaliation_prosecution_score=85.0,
            state_surveillance_chilling_score=88.0,
            media_source_protection_failure_score=82.0,
            primary_pattern="state_surveillance_chilling",
        ),
        WhistleblowerProtectionEntity(
            entity_id="WP-004",
            name="USA — Espionage Act, Snowden/Manning/Assange & Criminalisation Divulgations Intérêt Public",
            country="Amérique du Nord",
            legal_framework_absence_score=85.0,
            retaliation_prosecution_score=90.0,
            state_surveillance_chilling_score=92.0,
            media_source_protection_failure_score=88.0,
            primary_pattern="retaliation_prosecution",
        ),
        WhistleblowerProtectionEntity(
            entity_id="WP-005",
            name="Inde — UAPA Journalistes, Gauri Lankesh Assassinée & Pression Médias Indépendants",
            country="Asie du Sud",
            legal_framework_absence_score=52.0,
            retaliation_prosecution_score=58.0,
            state_surveillance_chilling_score=55.0,
            media_source_protection_failure_score=50.0,
            primary_pattern="media_source_protection_failure",
        ),
        WhistleblowerProtectionEntity(
            entity_id="WP-006",
            name="UE/France/Allemagne — Luxleaks, Directives Partielles & SLAPP Contre Journalistes",
            country="Europe",
            legal_framework_absence_score=48.0,
            retaliation_prosecution_score=52.0,
            state_surveillance_chilling_score=50.0,
            media_source_protection_failure_score=55.0,
            primary_pattern="legal_framework_absence",
        ),
        WhistleblowerProtectionEntity(
            entity_id="WP-007",
            name="UK — Official Secrets Act, Réforme Partielle & Collaboration NSA/GCHQ Surveillance",
            country="Europe de l'Ouest",
            legal_framework_absence_score=25.0,
            retaliation_prosecution_score=30.0,
            state_surveillance_chilling_score=32.0,
            media_source_protection_failure_score=28.0,
            primary_pattern="legal_framework_absence",
        ),
        WhistleblowerProtectionEntity(
            entity_id="WP-008",
            name="ONU/CoE — Résolution 2300, Recommandation CoE & Protection Sources Journalistiques",
            country="Global",
            legal_framework_absence_score=4.0,
            retaliation_prosecution_score=5.0,
            state_surveillance_chilling_score=3.0,
            media_source_protection_failure_score=6.0,
            primary_pattern="media_source_protection_failure",
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

    return WhistleblowerProtectionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_whistleblower_protection_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "government_accountability_project_whistleblower_protection_global_report",
            "rsf_reporters_without_borders_press_freedom_index_annual",
            "council_of_europe_recommendation_protection_whistleblowers_cm_rec_2014_7",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_whistleblower_protection_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_whistleblower_protection_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
