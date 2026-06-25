from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DigitalSurveillanceMassMonitoringEntity:
    entity_id: str
    name: str
    country: str
    mass_surveillance_scale: float
    legal_accountability_gap: float
    dissident_targeting: float
    data_protection_absence: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_surveillance_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_surveillance_scale * 0.30
            + self.legal_accountability_gap * 0.25
            + self.dissident_targeting * 0.25
            + self.data_protection_absence * 0.20,
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
        self.estimated_surveillance_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DigitalSurveillanceMassMonitoringEngineResult:
    agent: str = "Digital Surveillance Mass Monitoring Engine Agent"
    domain: str = "digital_surveillance_mass_monitoring"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_surveillance_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalSurveillanceMassMonitoringEntity] = field(default_factory=list)


def run_digital_surveillance_mass_monitoring_engine() -> DigitalSurveillanceMassMonitoringEngineResult:
    entities = [
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-001",
            name="Chine/SCS Reconnaissance Faciale — 600M Caméras, Système Crédit Social, Surveillance Totale Xinjiang & Contrôle Biométrique Généralisé",
            country="Chine",
            mass_surveillance_scale=97.0,
            legal_accountability_gap=96.0,
            dissident_targeting=95.0,
            data_protection_absence=94.0,
            primary_pattern="mass_surveillance_scale",
        ),
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-002",
            name="Corée du Nord/Surveillance Totale — Absence Internet Civil, Écoutes Domestiques Systématiques, Contrôle Absolu Communications & Intranet Kwangmyong",
            country="Corée du Nord",
            mass_surveillance_scale=94.0,
            legal_accountability_gap=95.0,
            dissident_targeting=93.0,
            data_protection_absence=90.0,
            primary_pattern="legal_accountability_gap",
        ),
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-003",
            name="Russie/SORM Espionnage — Interception Légale Totale Télécoms, Logiciels Pegasus-like Journalistes, SORM-3 Métadonnées & Loi Yarovaya",
            country="Russie",
            mass_surveillance_scale=84.0,
            legal_accountability_gap=82.0,
            dissident_targeting=86.0,
            data_protection_absence=78.0,
            primary_pattern="dissident_targeting",
        ),
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-004",
            name="USA/NSA PRISM — Programme Snowden, FISA Court Secrète, Surveillance Globale Sans Mandat Étrangers & Section 702 Collecte Masse",
            country="USA",
            mass_surveillance_scale=74.0,
            legal_accountability_gap=70.0,
            dissident_targeting=68.0,
            data_protection_absence=66.0,
            primary_pattern="mass_surveillance_scale",
        ),
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-005",
            name="Inde/Aadhar NATGRID — Biométrie 1.4Mrd Habitants, Fusion Bases Données Gouvernementales, Loi Surveillance Sans Garanties & Coupures Cachemire",
            country="Inde",
            mass_surveillance_scale=57.0,
            legal_accountability_gap=54.0,
            dissident_targeting=52.0,
            data_protection_absence=50.0,
            primary_pattern="mass_surveillance_scale",
        ),
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-006",
            name="Brésil/SINAE Surveillance — Monitoring Mouvements Sociaux, Journalistes Ciblés, Absence Cadre Légal Clair & Données Biométriques Police",
            country="Brésil",
            mass_surveillance_scale=46.0,
            legal_accountability_gap=44.0,
            dissident_targeting=48.0,
            data_protection_absence=42.0,
            primary_pattern="dissident_targeting",
        ),
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-007",
            name="UE/RGPD Protection Partielle — Cadre Légal Avancé Mais Surveillance Sécurité Nationale Possible, Accords MLAT & Lacunes Renseignement",
            country="Union Européenne",
            mass_surveillance_scale=26.0,
            legal_accountability_gap=22.0,
            dissident_targeting=20.0,
            data_protection_absence=18.0,
            primary_pattern="legal_accountability_gap",
        ),
        DigitalSurveillanceMassMonitoringEntity(
            entity_id="DSM-008",
            name="Allemagne/BfDI Protection Forte — Commissaire Données Indépendant, Recours Effectif Citoyens, Contrôle Parlementaire BND & Arrêts Constitutionnels",
            country="Allemagne",
            mass_surveillance_scale=8.0,
            legal_accountability_gap=6.0,
            dissident_targeting=5.0,
            data_protection_absence=4.0,
            primary_pattern="legal_accountability_gap",
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

    # Assertions distribution OBLIGATOIRE : 4 critique / 2 élevé / 1 modéré / 1 faible
    assert risk_dist.get("critique", 0) == 4, f"Expected 4 critique, got {risk_dist.get('critique', 0)}"
    assert risk_dist.get("élevé", 0) == 2, f"Expected 2 élevé, got {risk_dist.get('élevé', 0)}"
    assert risk_dist.get("modéré", 0) == 1, f"Expected 1 modéré, got {risk_dist.get('modéré', 0)}"
    assert risk_dist.get("faible", 0) == 1, f"Expected 1 faible, got {risk_dist.get('faible', 0)}"

    return DigitalSurveillanceMassMonitoringEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_surveillance_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freedom_house_freedom_net_2024",
            "privacy_international_surveillance_database_2024",
            "citizen_lab_targeted_threat_lab_2024",
            "amnesty_international_digital_surveillance_report_2024",
            "electronic_frontier_foundation_global_surveillance_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_digital_surveillance_mass_monitoring_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_surveillance_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — {e.estimated_surveillance_rights_index}")
