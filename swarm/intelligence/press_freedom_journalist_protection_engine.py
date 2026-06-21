from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PressFreedomJournalistProtectionEntity:
    entity_id: str
    name: str
    country: str
    journalist_killing_imprisonment_severity_score: float
    media_censorship_state_capture_scale_score: float
    surveillance_source_protection_violation_score: float
    online_journalist_harassment_slapp_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_press_freedom_journalist_protection_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.journalist_killing_imprisonment_severity_score * 0.30
            + self.media_censorship_state_capture_scale_score * 0.25
            + self.surveillance_source_protection_violation_score * 0.25
            + self.online_journalist_harassment_slapp_gap_score * 0.20,
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
        self.estimated_press_freedom_journalist_protection_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class PressFreedomJournalistProtectionEngineResult:
    agent: str = "Press Freedom Journalist Protection Engine Agent"
    domain: str = "press_freedom_journalist_protection"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_press_freedom_journalist_protection_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PressFreedomJournalistProtectionEntity] = field(default_factory=list)


def run_press_freedom_journalist_protection_engine() -> PressFreedomJournalistProtectionEngineResult:
    entities = [
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-001",
            name="Mexique/Honduras — Journalistes Pays Non-Guerre Le Plus Meurtrier, Cartels Tuent Reporters, Impunité 99% & Autodéfense Journalistes",
            country="Mexique/Honduras",
            journalist_killing_imprisonment_severity_score=93.0,
            media_censorship_state_capture_scale_score=91.0,
            surveillance_source_protection_violation_score=90.0,
            online_journalist_harassment_slapp_gap_score=92.0,
            primary_pattern="journalist_killing_imprisonment_severity",
        ),
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-002",
            name="Chine — 100+ Journalistes Emprisonnés, Presse Étrangère Expulsée, Porte-Parole Seul Autorisé & VPN Bloqué Presse",
            country="Chine",
            journalist_killing_imprisonment_severity_score=90.0,
            media_censorship_state_capture_scale_score=88.0,
            surveillance_source_protection_violation_score=89.0,
            online_journalist_harassment_slapp_gap_score=91.0,
            primary_pattern="media_censorship_state_capture_scale",
        ),
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-003",
            name="Russie — Novaya Gazeta Fermée, Loi Agent Étranger, Khashoggi-Style Meurtres Abyan & Ukraine War Coverage Interdit",
            country="Russie",
            journalist_killing_imprisonment_severity_score=87.0,
            media_censorship_state_capture_scale_score=85.0,
            surveillance_source_protection_violation_score=86.0,
            online_journalist_harassment_slapp_gap_score=88.0,
            primary_pattern="journalist_killing_imprisonment_severity",
        ),
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-004",
            name="Arabie Saoudite — Khashoggi Assassinat, Blogueurs Condamnés, Médias Indépendants Inexistants & Critiques Online Emprisonnés",
            country="Arabie Saoudite",
            journalist_killing_imprisonment_severity_score=84.0,
            media_censorship_state_capture_scale_score=82.0,
            surveillance_source_protection_violation_score=83.0,
            online_journalist_harassment_slapp_gap_score=85.0,
            primary_pattern="surveillance_source_protection_violation",
        ),
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-005",
            name="Turquie/Israël — Journalistes Gaza Tués 100+, Turquie 2ème Prison Journalistes, Presse Pro-Gouvernement Monopole & SLAPP",
            country="Turquie/Israël",
            journalist_killing_imprisonment_severity_score=55.0,
            media_censorship_state_capture_scale_score=53.0,
            surveillance_source_protection_violation_score=54.0,
            online_journalist_harassment_slapp_gap_score=56.0,
            primary_pattern="journalist_killing_imprisonment_severity",
        ),
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-006",
            name="USA/Europe — Fox News/MSNBC Polarisation, Reporters Sans Protection Fédérale, SLAPP Suits Croissants & Propriété Oligarques",
            country="USA/Europe",
            journalist_killing_imprisonment_severity_score=52.0,
            media_censorship_state_capture_scale_score=50.0,
            surveillance_source_protection_violation_score=51.0,
            online_journalist_harassment_slapp_gap_score=53.0,
            primary_pattern="online_journalist_harassment_slapp_gap",
        ),
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-007",
            name="RSF/CPJ — Classement Liberté Presse, Committee Protect Journalists, Hotlines Urgence & Rapports Annuels",
            country="Global",
            journalist_killing_imprisonment_severity_score=27.0,
            media_censorship_state_capture_scale_score=25.0,
            surveillance_source_protection_violation_score=26.0,
            online_journalist_harassment_slapp_gap_score=26.0,
            primary_pattern="journalist_killing_imprisonment_severity",
        ),
        PressFreedomJournalistProtectionEntity(
            entity_id="PFJ-008",
            name="ONU/Art.19 PIDCP — Liberté Expression Presse, Rapporteur Spécial & SDG 16.10 Accès Information",
            country="Global",
            journalist_killing_imprisonment_severity_score=5.0,
            media_censorship_state_capture_scale_score=3.0,
            surveillance_source_protection_violation_score=4.0,
            online_journalist_harassment_slapp_gap_score=4.0,
            primary_pattern="media_censorship_state_capture_scale",
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

    return PressFreedomJournalistProtectionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_press_freedom_journalist_protection_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "rsf_press_freedom_index_annual_report",
            "cpj_journalist_imprisonment_global_census",
            "freedom_of_press_foundation_surveillance_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_press_freedom_journalist_protection_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_press_freedom_journalist_protection_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
