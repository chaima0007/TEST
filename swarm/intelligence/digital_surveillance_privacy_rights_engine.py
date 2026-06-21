from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DigitalSurveillancePrivacyRightsEntity:
    entity_id: str
    name: str
    country: str
    mass_surveillance_state_infrastructure_score: float
    privacy_legal_protection_enforcement_gap_score: float
    digital_repression_dissidents_score: float
    data_exploitation_corporate_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_digital_surveillance_privacy_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_surveillance_state_infrastructure_score * 0.30
            + self.privacy_legal_protection_enforcement_gap_score * 0.25
            + self.digital_repression_dissidents_score * 0.25
            + self.data_exploitation_corporate_impunity_score * 0.20,
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
        self.estimated_digital_surveillance_privacy_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DigitalSurveillancePrivacyRightsEngineResult:
    agent: str = "Digital Surveillance Privacy Rights Engine Agent"
    domain: str = "digital_surveillance_privacy_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_digital_surveillance_privacy_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalSurveillancePrivacyRightsEntity] = field(default_factory=list)


def run_digital_surveillance_privacy_rights_engine() -> DigitalSurveillancePrivacyRightsEngineResult:
    entities = [
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-001",
            name="Chine/GFW II SCS — Surveillance de Masse IA, Crédit Social, Reconnaissance Faciale Ouïghours & Contrôle Internet Total",
            country="Chine",
            mass_surveillance_state_infrastructure_score=95.0,
            privacy_legal_protection_enforcement_gap_score=92.0,
            digital_repression_dissidents_score=90.0,
            data_exploitation_corporate_impunity_score=85.0,
            primary_pattern="mass_surveillance_state_infrastructure",
        ),
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-002",
            name="Russie/SORM Nagulny — Interception Totale Télécoms, Blogage VPN, Surveillance Opposants & Loi Souveraineté Internet",
            country="Russie",
            mass_surveillance_state_infrastructure_score=88.0,
            privacy_legal_protection_enforcement_gap_score=85.0,
            digital_repression_dissidents_score=90.0,
            data_exploitation_corporate_impunity_score=78.0,
            primary_pattern="digital_repression_dissidents",
        ),
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-003",
            name="Iran/Internet National — Filtrage Contenu Islamique, Coupures Réseau Protestations, Espionnage Activistes & Contrôle Messageries",
            country="Iran",
            mass_surveillance_state_infrastructure_score=85.0,
            privacy_legal_protection_enforcement_gap_score=82.0,
            digital_repression_dissidents_score=88.0,
            data_exploitation_corporate_impunity_score=75.0,
            primary_pattern="digital_repression_dissidents",
        ),
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-004",
            name="Biélorussie/Répression Telegram — Surveillance Manifestants 2020, Interception Messages, Arrestations via Données Numériques & Coupures Internet",
            country="Biélorussie",
            mass_surveillance_state_infrastructure_score=82.0,
            privacy_legal_protection_enforcement_gap_score=80.0,
            digital_repression_dissidents_score=85.0,
            data_exploitation_corporate_impunity_score=72.0,
            primary_pattern="digital_repression_dissidents",
        ),
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-005",
            name="USA/PRISM NSA — Collecte Masse Métadonnées, Section 702 FISA, Surveillance Sans Mandat Étrangers & Absence Recours Citoyens",
            country="USA",
            mass_surveillance_state_infrastructure_score=55.0,
            privacy_legal_protection_enforcement_gap_score=58.0,
            digital_repression_dissidents_score=45.0,
            data_exploitation_corporate_impunity_score=65.0,
            primary_pattern="data_exploitation_corporate_impunity",
        ),
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-006",
            name="Inde/NATGRID Surveillance — Interception Légale Élargie, Absence Loi Protection Données Robuste, Coupures Cachemire & Surveillance Journalistes",
            country="Inde",
            mass_surveillance_state_infrastructure_score=50.0,
            privacy_legal_protection_enforcement_gap_score=52.0,
            digital_repression_dissidents_score=48.0,
            data_exploitation_corporate_impunity_score=55.0,
            primary_pattern="privacy_legal_protection_enforcement_gap",
        ),
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-007",
            name="UE/RGPD Partiel — Protection Données Avancée Mais Lacunes Sécurité Nationale, Surveillance Policière & Adéquation Transferts Données",
            country="Union Européenne",
            mass_surveillance_state_infrastructure_score=25.0,
            privacy_legal_protection_enforcement_gap_score=28.0,
            digital_repression_dissidents_score=20.0,
            data_exploitation_corporate_impunity_score=30.0,
            primary_pattern="privacy_legal_protection_enforcement_gap",
        ),
        DigitalSurveillancePrivacyRightsEntity(
            entity_id="DSPR-008",
            name="Allemagne/BND Réforme — Réforme Service Renseignement 2021, Cour Constitutionnelle Protection Vie Privée & Cadre Légal Surveillance Limité",
            country="Allemagne",
            mass_surveillance_state_infrastructure_score=5.0,
            privacy_legal_protection_enforcement_gap_score=8.0,
            digital_repression_dissidents_score=4.0,
            data_exploitation_corporate_impunity_score=10.0,
            primary_pattern="privacy_legal_protection_enforcement_gap",
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

    return DigitalSurveillancePrivacyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_digital_surveillance_privacy_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freedom_house_freedom_net_2023",
            "privacy_international_surveillance_database",
            "citizen_lab_targeted_threat_lab_2023",
            "electronic_frontier_foundation_global_surveillance_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_digital_surveillance_privacy_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_digital_surveillance_privacy_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
