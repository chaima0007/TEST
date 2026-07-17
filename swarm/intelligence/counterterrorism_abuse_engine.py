from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CounterterrorismAbuseEntity:
    entity_id: str
    name: str
    country: str
    arbitrary_detention_torture_score: float
    civil_rights_dismantlement_score: float
    minorities_targeting_score: float
    judicial_oversight_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_counterterrorism_abuse_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.arbitrary_detention_torture_score * 0.30
            + self.civil_rights_dismantlement_score * 0.25
            + self.minorities_targeting_score * 0.25
            + self.judicial_oversight_absence_score * 0.20,
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
        self.estimated_counterterrorism_abuse_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class CounterterrorismAbuseEngineResult:
    agent: str = "Counterterrorism Abuse Engine Agent"
    domain: str = "counterterrorism_abuse"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_counterterrorism_abuse_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CounterterrorismAbuseEntity] = field(default_factory=list)

def run_counterterrorism_abuse_engine() -> CounterterrorismAbuseEngineResult:
    entities = [
        CounterterrorismAbuseEntity(
            entity_id="CA-001",
            name="Chine/Xinjiang — Camps Rééducation Ouïghours, XUAR & Antiterrorisme Prétexte État",
            country="Asie du Nord-Est",
            arbitrary_detention_torture_score=95.0,
            civil_rights_dismantlement_score=92.0,
            minorities_targeting_score=98.0,
            judicial_oversight_absence_score=90.0,
            primary_pattern="minorities_targeting",
        ),
        CounterterrorismAbuseEntity(
            entity_id="CA-002",
            name="USA/Post-9/11 — Patriot Act, NDAA, Guantánamo & Surveillance Masse NSA",
            country="Amérique du Nord",
            arbitrary_detention_torture_score=80.0,
            civil_rights_dismantlement_score=88.0,
            minorities_targeting_score=85.0,
            judicial_oversight_absence_score=78.0,
            primary_pattern="civil_rights_dismantlement",
        ),
        CounterterrorismAbuseEntity(
            entity_id="CA-003",
            name="Égypte/Al-Sissi — 60 000 Détenus Politiques, Loi Antiterror & Journalistes Emprisonnés",
            country="Afrique du Nord",
            arbitrary_detention_torture_score=85.0,
            civil_rights_dismantlement_score=80.0,
            minorities_targeting_score=78.0,
            judicial_oversight_absence_score=82.0,
            primary_pattern="arbitrary_detention_torture",
        ),
        CounterterrorismAbuseEntity(
            entity_id="CA-004",
            name="Inde — UAPA, Loi Sédition Coloniale, Accusés Kashmir & Militants Droits Humains",
            country="Asie du Sud",
            arbitrary_detention_torture_score=72.0,
            civil_rights_dismantlement_score=78.0,
            minorities_targeting_score=82.0,
            judicial_oversight_absence_score=75.0,
            primary_pattern="minorities_targeting",
        ),
        CounterterrorismAbuseEntity(
            entity_id="CA-005",
            name="France/Europe — Loi Renseignement, État Urgence Permanent & Surveillance Communautés",
            country="Europe",
            arbitrary_detention_torture_score=52.0,
            civil_rights_dismantlement_score=58.0,
            minorities_targeting_score=60.0,
            judicial_oversight_absence_score=55.0,
            primary_pattern="judicial_oversight_absence",
        ),
        CounterterrorismAbuseEntity(
            entity_id="CA-006",
            name="Turquie — Coup 2016, 150 000 Arrêtés, HDP Kurdes Emprisonnés & Professeurs Épurés",
            country="Europe de l'Est",
            arbitrary_detention_torture_score=55.0,
            civil_rights_dismantlement_score=52.0,
            minorities_targeting_score=58.0,
            judicial_oversight_absence_score=50.0,
            primary_pattern="arbitrary_detention_torture",
        ),
        CounterterrorismAbuseEntity(
            entity_id="CA-007",
            name="ONU/CDH — Résolutions Antiterrorisme & Droits, Procédures Spéciales & HCDH Monitoring",
            country="Global",
            arbitrary_detention_torture_score=22.0,
            civil_rights_dismantlement_score=28.0,
            minorities_targeting_score=30.0,
            judicial_oversight_absence_score=32.0,
            primary_pattern="civil_rights_dismantlement",
        ),
        CounterterrorismAbuseEntity(
            entity_id="CA-008",
            name="ONU/ONUDC/CTITF — Task Force Contre-Terrorisme, Droits Fondamentaux & Garanties",
            country="Global",
            arbitrary_detention_torture_score=4.0,
            civil_rights_dismantlement_score=5.0,
            minorities_targeting_score=3.0,
            judicial_oversight_absence_score=6.0,
            primary_pattern="judicial_oversight_absence",
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

    return CounterterrorismAbuseEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_counterterrorism_abuse_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_antiterrorism_double_standards_report",
            "un_special_rapporteur_promotion_protection_human_rights_counter_terrorism_annual",
            "icj_assessing_damage_urging_action_eminent_jurists_panel_terrorism_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_counterterrorism_abuse_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_counterterrorism_abuse_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
