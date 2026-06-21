from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ElderAbuseRightsEntity:
    entity_id: str
    name: str
    country: str
    institutional_abuse_prevalence_score: float
    financial_exploitation_scale_score: float
    legal_protection_framework_gap_score: float
    autonomy_dignity_violation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_elder_abuse_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.institutional_abuse_prevalence_score * 0.30
            + self.financial_exploitation_scale_score * 0.25
            + self.legal_protection_framework_gap_score * 0.25
            + self.autonomy_dignity_violation_score * 0.20,
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
        self.estimated_elder_abuse_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ElderAbuseRightsEngineResult:
    agent: str = "Elder Abuse Rights Engine Agent"
    domain: str = "elder_abuse_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_elder_abuse_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ElderAbuseRightsEntity] = field(default_factory=list)

def run_elder_abuse_rights_engine() -> ElderAbuseRightsEngineResult:
    entities = [
        ElderAbuseRightsEntity(
            entity_id="EA-001",
            name="Inde — Maltraitance 32% Personnes Âgées, Abandon Familial Systémique & Loi 2007 Non Appliquée",
            country="Asie du Sud",
            institutional_abuse_prevalence_score=95.0,
            financial_exploitation_scale_score=92.0,
            legal_protection_framework_gap_score=95.0,
            autonomy_dignity_violation_score=90.0,
            primary_pattern="legal_protection_framework_gap",
        ),
        ElderAbuseRightsEntity(
            entity_id="EA-002",
            name="Chine — Abandon Parents Âgés, Abus Financiers Répandus & Loi Filiale Controversée 2013",
            country="Asie de l'Est",
            institutional_abuse_prevalence_score=90.0,
            financial_exploitation_scale_score=92.0,
            legal_protection_framework_gap_score=88.0,
            autonomy_dignity_violation_score=90.0,
            primary_pattern="financial_exploitation_scale",
        ),
        ElderAbuseRightsEntity(
            entity_id="EA-003",
            name="USA — 5M Seniors Maltraités/An, COVID Maisons Retraite 40% Décès & FFAM Défaillance",
            country="Amérique du Nord",
            institutional_abuse_prevalence_score=88.0,
            financial_exploitation_scale_score=90.0,
            legal_protection_framework_gap_score=85.0,
            autonomy_dignity_violation_score=88.0,
            primary_pattern="institutional_abuse_prevalence",
        ),
        ElderAbuseRightsEntity(
            entity_id="EA-004",
            name="Mexique/LATAM — Isolation Institutionnelle, Droits Confisqués & Protection Sociale Absente",
            country="Amérique Latine",
            institutional_abuse_prevalence_score=85.0,
            financial_exploitation_scale_score=82.0,
            legal_protection_framework_gap_score=88.0,
            autonomy_dignity_violation_score=85.0,
            primary_pattern="legal_protection_framework_gap",
        ),
        ElderAbuseRightsEntity(
            entity_id="EA-005",
            name="France — Scandale EHPAD Orpea 2022, Maltraitance Systémique & Contrôles ARS Insuffisants",
            country="Europe",
            institutional_abuse_prevalence_score=55.0,
            financial_exploitation_scale_score=52.0,
            legal_protection_framework_gap_score=55.0,
            autonomy_dignity_violation_score=52.0,
            primary_pattern="institutional_abuse_prevalence",
        ),
        ElderAbuseRightsEntity(
            entity_id="EA-006",
            name="Australie — Royal Commission 2021, 14 800 Incidents Signalés, Staffing Crisis & Réforme Partielle",
            country="Océanie",
            institutional_abuse_prevalence_score=50.0,
            financial_exploitation_scale_score=48.0,
            legal_protection_framework_gap_score=50.0,
            autonomy_dignity_violation_score=50.0,
            primary_pattern="autonomy_dignity_violation",
        ),
        ElderAbuseRightsEntity(
            entity_id="EA-007",
            name="HelpAge International/OMS — MIPAA Madrid 2002, Rapport Global Âgisme & Standards Protection",
            country="Global",
            institutional_abuse_prevalence_score=22.0,
            financial_exploitation_scale_score=28.0,
            legal_protection_framework_gap_score=25.0,
            autonomy_dignity_violation_score=30.0,
            primary_pattern="autonomy_dignity_violation",
        ),
        ElderAbuseRightsEntity(
            entity_id="EA-008",
            name="ONU/Madrid & CDPH — Convention Droits Personnes Âgées Proposée, Art.12 Capacité Autonomie",
            country="Global",
            institutional_abuse_prevalence_score=4.0,
            financial_exploitation_scale_score=5.0,
            legal_protection_framework_gap_score=3.0,
            autonomy_dignity_violation_score=6.0,
            primary_pattern="legal_protection_framework_gap",
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

    return ElderAbuseRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_elder_abuse_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_global_report_ageism_elder_abuse_prevalence",
            "helpage_international_mipaa_review_elder_rights_monitoring",
            "un_open_ended_working_group_ageing_convention_proposal",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_elder_abuse_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_elder_abuse_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
