from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#8b5cf6"


@dataclass
class RightToBeForgottenRightsEntity:
    entity_id: str
    name: str
    country: str
    data_erasure_denial_score: float
    surveillance_data_retention_score: float
    digital_reputation_harm_score: float
    platform_compliance_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_be_forgotten_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.data_erasure_denial_score * 0.30
            + self.surveillance_data_retention_score * 0.25
            + self.digital_reputation_harm_score * 0.25
            + self.platform_compliance_gap_score * 0.20,
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
        self.estimated_right_to_be_forgotten_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToBeForgottenRightsEngineResult:
    agent: str = "Right To Be Forgotten Rights Engine Agent"
    domain: str = "right_to_be_forgotten_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_be_forgotten_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToBeForgottenRightsEntity] = field(default_factory=list)


def run_right_to_be_forgotten_rights_engine() -> RightToBeForgottenRightsEngineResult:
    entities = [
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-001",
            name="Chine — Surveillance Permanente, Aucun Droit Effacement, PIPL Non-Effectif",
            country="Chine",
            data_erasure_denial_score=97.0,
            surveillance_data_retention_score=96.0,
            digital_reputation_harm_score=94.0,
            platform_compliance_gap_score=95.0,
            primary_pattern="total_erasure_denial",
        ),
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-002",
            name="Russie — Yarovaya Act Rétention 6 Mois, Dissidents Profils Non-Effaçables",
            country="Russie",
            data_erasure_denial_score=90.0,
            surveillance_data_retention_score=92.0,
            digital_reputation_harm_score=88.0,
            platform_compliance_gap_score=89.0,
            primary_pattern="state_data_retention",
        ),
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-003",
            name="Iran — Données Activistes Exportées, FATA Cyberpolice Persécution Digitale",
            country="Iran",
            data_erasure_denial_score=85.0,
            surveillance_data_retention_score=87.0,
            digital_reputation_harm_score=83.0,
            platform_compliance_gap_score=84.0,
            primary_pattern="state_data_retention",
        ),
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-004",
            name="Inde — Aadhaar Biométrique 1.4Md Sans Droit Suppression, DPDPA Lacunes",
            country="Inde",
            data_erasure_denial_score=76.0,
            surveillance_data_retention_score=74.0,
            digital_reputation_harm_score=72.0,
            platform_compliance_gap_score=77.0,
            primary_pattern="biometric_retention",
        ),
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-005",
            name="USA — CCPA Partiel, Pas RTBF Fédéral, Google Search Refus 97% Demandes Hors UE",
            country="USA",
            data_erasure_denial_score=54.0,
            surveillance_data_retention_score=56.0,
            digital_reputation_harm_score=52.0,
            platform_compliance_gap_score=55.0,
            primary_pattern="platform_compliance_gap",
        ),
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-006",
            name="Brésil — LGPD 2020 Appliqué Partiellement, ANPD Sanctions Insuffisantes",
            country="Brésil",
            data_erasure_denial_score=44.0,
            surveillance_data_retention_score=46.0,
            digital_reputation_harm_score=43.0,
            platform_compliance_gap_score=45.0,
            primary_pattern="platform_compliance_gap",
        ),
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-007",
            name="UK — GDPR Équivalence Post-Brexit Partielle, ICO Sanctions Limitées",
            country="UK",
            data_erasure_denial_score=28.0,
            surveillance_data_retention_score=30.0,
            digital_reputation_harm_score=27.0,
            platform_compliance_gap_score=29.0,
            primary_pattern="digital_reputation_harm",
        ),
        RightToBeForgottenRightsEntity(
            entity_id="RTBF-008",
            name="UE — RGPD Art.17 Complet, Amendes Google/Meta Effectives, CNIL Modèle",
            country="UE",
            data_erasure_denial_score=7.0,
            surveillance_data_retention_score=8.0,
            digital_reputation_harm_score=6.0,
            platform_compliance_gap_score=9.0,
            primary_pattern="surveillance_data_retention",
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

    return RightToBeForgottenRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_be_forgotten_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "gdpr_article_17_erasure_implementation_reports_2024",
            "eu_cjeu_google_spain_ruling_follow_up",
            "hrw_digital_surveillance_data_retention_2024",
            "un_privacy_special_rapporteur_digital_age_report",
            "article_19_digital_rights_global_report_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_be_forgotten_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
