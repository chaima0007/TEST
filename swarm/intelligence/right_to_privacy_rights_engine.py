from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#4f46e5"


@dataclass
class RightToPrivacyRightsEntity:
    entity_id: str
    name: str
    country: str
    mass_surveillance_score: float
    data_collection_without_consent_score: float
    communication_interception_score: float
    privacy_law_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_privacy_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_surveillance_score * 0.30
            + self.data_collection_without_consent_score * 0.25
            + self.communication_interception_score * 0.25
            + self.privacy_law_absence_score * 0.20,
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
        self.estimated_right_to_privacy_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToPrivacyRightsEngineResult:
    agent: str = "Right To Privacy Rights Engine Agent"
    domain: str = "right_to_privacy_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_privacy_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToPrivacyRightsEntity] = field(default_factory=list)


def run_right_to_privacy_rights_engine() -> RightToPrivacyRightsEngineResult:
    entities = [
        RightToPrivacyRightsEntity(
            entity_id="RTP-001",
            name="Chine — NSA chinoise, surveillance totale 1.4Md, SCS notation comportementale",
            country="Chine",
            mass_surveillance_score=97.0,
            data_collection_without_consent_score=96.0,
            communication_interception_score=95.0,
            privacy_law_absence_score=94.0,
            primary_pattern="mass_surveillance",
        ),
        RightToPrivacyRightsEntity(
            entity_id="RTP-002",
            name="Russie — SORM-3, Yarovaya retention totale, FSB accès direct serveurs",
            country="Russie",
            mass_surveillance_score=91.0,
            data_collection_without_consent_score=89.0,
            communication_interception_score=93.0,
            privacy_law_absence_score=88.0,
            primary_pattern="communication_interception",
        ),
        RightToPrivacyRightsEntity(
            entity_id="RTP-003",
            name="Iran — Deep packet inspection, Pegasus dissidents, VPN 80% population",
            country="Iran",
            mass_surveillance_score=85.0,
            data_collection_without_consent_score=83.0,
            communication_interception_score=87.0,
            privacy_law_absence_score=82.0,
            primary_pattern="communication_interception",
        ),
        RightToPrivacyRightsEntity(
            entity_id="RTP-004",
            name="USA pré-2024 — NSA PRISM Snowden, FISA 702, bulk metadata collection",
            country="USA",
            mass_surveillance_score=76.0,
            data_collection_without_consent_score=78.0,
            communication_interception_score=74.0,
            privacy_law_absence_score=80.0,
            primary_pattern="privacy_law_absence",
        ),
        RightToPrivacyRightsEntity(
            entity_id="RTP-005",
            name="Israël — NSO Group Pegasus exporté 45 pays, journalistes/activistes ciblés",
            country="Israël",
            mass_surveillance_score=54.0,
            data_collection_without_consent_score=56.0,
            communication_interception_score=58.0,
            privacy_law_absence_score=52.0,
            primary_pattern="communication_interception",
        ),
        RightToPrivacyRightsEntity(
            entity_id="RTP-006",
            name="Inde — UAPA wiretapping sans mandat, Pegasus politiciens/journalistes, PDPB retardé",
            country="Inde",
            mass_surveillance_score=46.0,
            data_collection_without_consent_score=48.0,
            communication_interception_score=50.0,
            privacy_law_absence_score=44.0,
            primary_pattern="data_collection_without_consent",
        ),
        RightToPrivacyRightsEntity(
            entity_id="RTP-007",
            name="UK — GCHQ Tempora, Investigatory Powers Act 2016, bulk surveillance légalisée",
            country="UK",
            mass_surveillance_score=28.0,
            data_collection_without_consent_score=30.0,
            communication_interception_score=32.0,
            privacy_law_absence_score=24.0,
            primary_pattern="mass_surveillance",
        ),
        RightToPrivacyRightsEntity(
            entity_id="RTP-008",
            name="UE/Allemagne — RGPD + Cour Constitutionnelle, Schrems II, BND réformé",
            country="UE/Allemagne",
            mass_surveillance_score=7.0,
            data_collection_without_consent_score=6.0,
            communication_interception_score=8.0,
            privacy_law_absence_score=5.0,
            primary_pattern="privacy_law_absence",
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

    return RightToPrivacyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_privacy_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "privacy_international_global_privacy_index_2024",
            "un_special_rapporteur_privacy_digital_age",
            "eff_surveillance_self_defense_global",
            "access_now_privacy_rights_violations_2024",
            "citizen_lab_targeted_surveillance_report_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_privacy_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
