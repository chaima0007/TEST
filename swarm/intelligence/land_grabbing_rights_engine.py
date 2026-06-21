from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class LandGrabbingRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_displacement_land_seizure_severity_score: float
    legal_title_recognition_absence_scale_score: float
    corporate_state_complicity_land_grab_score: float
    indigenous_community_consultation_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_land_grabbing_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_displacement_land_seizure_severity_score * 0.30
            + self.legal_title_recognition_absence_scale_score * 0.25
            + self.corporate_state_complicity_land_grab_score * 0.25
            + self.indigenous_community_consultation_gap_score * 0.20,
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
        self.estimated_land_grabbing_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class LandGrabbingRightsEngineResult:
    agent: str = "Land Grabbing Rights Engine Agent"
    domain: str = "land_grabbing_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_land_grabbing_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LandGrabbingRightsEntity] = field(default_factory=list)

def run_land_grabbing_rights_engine() -> LandGrabbingRightsEngineResult:
    entities = [
        LandGrabbingRightsEntity(
            entity_id="LGR-001",
            name="Cambodge — Accaparement Terres 730 000 Ha, Expulsions Forcées Villages & Complicité État-Sociétés Sucrières",
            country="Cambodge",
            forced_displacement_land_seizure_severity_score=96.0,
            legal_title_recognition_absence_scale_score=93.0,
            corporate_state_complicity_land_grab_score=94.0,
            indigenous_community_consultation_gap_score=91.0,
            primary_pattern="forced_displacement_land_seizure_severity",
        ),
        LandGrabbingRightsEntity(
            entity_id="LGR-002",
            name="Éthiopie — Villagisation Forcée 1,5M Personnes, Concessions Agricoles Étrangères & Zéro Consultation",
            country="Éthiopie",
            forced_displacement_land_seizure_severity_score=93.0,
            legal_title_recognition_absence_scale_score=89.0,
            corporate_state_complicity_land_grab_score=90.0,
            indigenous_community_consultation_gap_score=87.0,
            primary_pattern="forced_displacement_land_seizure_severity",
        ),
        LandGrabbingRightsEntity(
            entity_id="LGR-003",
            name="Brésil/Amazonie — Garilampeiros Terres Autochtones, Déforestation Illégale & Agronégocio Impuni",
            country="Brésil",
            forced_displacement_land_seizure_severity_score=91.0,
            legal_title_recognition_absence_scale_score=87.0,
            corporate_state_complicity_land_grab_score=88.0,
            indigenous_community_consultation_gap_score=86.0,
            primary_pattern="corporate_state_complicity_land_grab",
        ),
        LandGrabbingRightsEntity(
            entity_id="LGR-004",
            name="Inde — Loi Acquisition Terres 2013 Contournée, Adivasis Expulsés Mines & Industries Sans Consentement",
            country="Inde",
            forced_displacement_land_seizure_severity_score=88.0,
            legal_title_recognition_absence_scale_score=85.0,
            corporate_state_complicity_land_grab_score=85.0,
            indigenous_community_consultation_gap_score=84.0,
            primary_pattern="legal_title_recognition_absence_scale",
        ),
        LandGrabbingRightsEntity(
            entity_id="LGR-005",
            name="Philippines — CARP Réforme Agraire Non Appliquée, Paysans Expulsés Plantations & Défenseurs Terres Assassinés",
            country="Philippines",
            forced_displacement_land_seizure_severity_score=56.0,
            legal_title_recognition_absence_scale_score=52.0,
            corporate_state_complicity_land_grab_score=53.0,
            indigenous_community_consultation_gap_score=51.0,
            primary_pattern="forced_displacement_land_seizure_severity",
        ),
        LandGrabbingRightsEntity(
            entity_id="LGR-006",
            name="Afrique de l'Est — Acquisitions Foncières Éthiopie/Kenya/Tanzanie, Pastoralistes Expulsés & Titres Coutumiers Ignorés",
            country="Afrique de l'Est",
            forced_displacement_land_seizure_severity_score=54.0,
            legal_title_recognition_absence_scale_score=52.0,
            corporate_state_complicity_land_grab_score=51.0,
            indigenous_community_consultation_gap_score=48.0,
            primary_pattern="legal_title_recognition_absence_scale",
        ),
        LandGrabbingRightsEntity(
            entity_id="LGR-007",
            name="Global Land Alliance/GRAIN — Base Données Accaparements, Plaidoyer Droits Paysans & Standards VGGT FAO",
            country="Global",
            forced_displacement_land_seizure_severity_score=24.0,
            legal_title_recognition_absence_scale_score=28.0,
            corporate_state_complicity_land_grab_score=26.0,
            indigenous_community_consultation_gap_score=26.0,
            primary_pattern="indigenous_community_consultation_gap",
        ),
        LandGrabbingRightsEntity(
            entity_id="LGR-008",
            name="ONU/FAO — Directives Volontaires Gouvernance Foncière (VGGT), UNDRIP Terres & SDG 1.4 Droits Fonciers",
            country="Global",
            forced_displacement_land_seizure_severity_score=4.0,
            legal_title_recognition_absence_scale_score=5.0,
            corporate_state_complicity_land_grab_score=4.0,
            indigenous_community_consultation_gap_score=5.0,
            primary_pattern="forced_displacement_land_seizure_severity",
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

    return LandGrabbingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_land_grabbing_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_land_grabbing_defenders_report",
            "grain_seized_the_2008_landgrab_for_food_and_financial_security",
            "oxfam_land_rights_commercial_agriculture_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_land_grabbing_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_land_grabbing_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
