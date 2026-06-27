from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DigitalSurveillanceEntity:
    entity_id: str
    name: str
    country: str
    mass_surveillance_scale_score: float
    journalist_activist_targeting_score: float
    legal_safeguard_absence_score: float
    spyware_export_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_digital_surveillance_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_surveillance_scale_score * 0.30
            + self.journalist_activist_targeting_score * 0.25
            + self.legal_safeguard_absence_score * 0.25
            + self.spyware_export_impunity_score * 0.20,
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
        self.estimated_digital_surveillance_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class DigitalSurveillanceEngineResult:
    agent: str = "Digital Surveillance Engine Agent"
    domain: str = "digital_surveillance"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_digital_surveillance_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalSurveillanceEntity] = field(default_factory=list)

def run_digital_surveillance_engine() -> DigitalSurveillanceEngineResult:
    entities = [
        DigitalSurveillanceEntity(
            entity_id="DS-001",
            name="Chine — Système Crédit Social, Reconnaissance Faciale 1,4Mrd & Surveillance Totale Xinjiang",
            country="Asie du Nord-Est",
            mass_surveillance_scale_score=98.0,
            journalist_activist_targeting_score=95.0,
            legal_safeguard_absence_score=92.0,
            spyware_export_impunity_score=90.0,
            primary_pattern="mass_surveillance_scale",
        ),
        DigitalSurveillanceEntity(
            entity_id="DS-002",
            name="NSO Group/Pegasus — Spyware Vendu 45 Pays, Journalistes/Activistes Ciblés & Impunité Israël",
            country="Global/Moyen-Orient",
            mass_surveillance_scale_score=88.0,
            journalist_activist_targeting_score=92.0,
            legal_safeguard_absence_score=85.0,
            spyware_export_impunity_score=92.0,
            primary_pattern="journalist_activist_targeting",
        ),
        DigitalSurveillanceEntity(
            entity_id="DS-003",
            name="Russie — SORM Interception Totale, Loi Yarovaya & Surveillance Opposants Post-2022",
            country="Europe de l'Est",
            mass_surveillance_scale_score=85.0,
            journalist_activist_targeting_score=88.0,
            legal_safeguard_absence_score=85.0,
            spyware_export_impunity_score=80.0,
            primary_pattern="legal_safeguard_absence",
        ),
        DigitalSurveillanceEntity(
            entity_id="DS-004",
            name="Iran — Internet National, VPN Criminalité & Coupures Réseau lors Protestations Mahsa Amini",
            country="Moyen-Orient",
            mass_surveillance_scale_score=80.0,
            journalist_activist_targeting_score=82.0,
            legal_safeguard_absence_score=85.0,
            spyware_export_impunity_score=78.0,
            primary_pattern="legal_safeguard_absence",
        ),
        DigitalSurveillanceEntity(
            entity_id="DS-005",
            name="USA/Five Eyes — PRISM/NSA Métadonnées, Section 702 FISA & Surveillance Internationale Massive",
            country="Amérique du Nord",
            mass_surveillance_scale_score=55.0,
            journalist_activist_targeting_score=50.0,
            legal_safeguard_absence_score=52.0,
            spyware_export_impunity_score=55.0,
            primary_pattern="spyware_export_impunity",
        ),
        DigitalSurveillanceEntity(
            entity_id="DS-006",
            name="UE/Règlement eSurveillance — Débat Chat Control, Chiffrement Menacé & Résistance Société Civile",
            country="Europe",
            mass_surveillance_scale_score=48.0,
            journalist_activist_targeting_score=45.0,
            legal_safeguard_absence_score=52.0,
            spyware_export_impunity_score=50.0,
            primary_pattern="spyware_export_impunity",
        ),
        DigitalSurveillanceEntity(
            entity_id="DS-007",
            name="Access Now/EFF — Défense Chiffrement, Rapports Pegasus & Plaidoyer Régulation Spyware",
            country="Global",
            mass_surveillance_scale_score=22.0,
            journalist_activist_targeting_score=28.0,
            legal_safeguard_absence_score=25.0,
            spyware_export_impunity_score=30.0,
            primary_pattern="mass_surveillance_scale",
        ),
        DigitalSurveillanceEntity(
            entity_id="DS-008",
            name="ONU/Rapporteur Vie Privée — Rapport Surveillance Numerique, Normes & Recommandations États",
            country="Global",
            mass_surveillance_scale_score=4.0,
            journalist_activist_targeting_score=5.0,
            legal_safeguard_absence_score=3.0,
            spyware_export_impunity_score=6.0,
            primary_pattern="journalist_activist_targeting",
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

    return DigitalSurveillanceEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_digital_surveillance_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "citizen_lab_pegasus_spyware_global_targeting_report",
            "access_now_digital_rights_surveillance_annual_report",
            "freedom_house_freedom_on_the_net_global_internet_freedom_index",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_digital_surveillance_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_digital_surveillance_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
