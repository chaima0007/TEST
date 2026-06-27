from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class NomadicPeoplesRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_sedentarization_displacement_scale_score: float
    legal_recognition_land_rights_gap_score: float
    discrimination_service_access_denial_score: float
    cultural_identity_assimilation_pressure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_nomadic_peoples_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_sedentarization_displacement_scale_score * 0.30
            + self.legal_recognition_land_rights_gap_score * 0.25
            + self.discrimination_service_access_denial_score * 0.25
            + self.cultural_identity_assimilation_pressure_score * 0.20,
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
        self.estimated_nomadic_peoples_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class NomadicPeoplesRightsEngineResult:
    agent: str = "Nomadic Peoples Rights Engine Agent"
    domain: str = "nomadic_peoples_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_nomadic_peoples_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[NomadicPeoplesRightsEntity] = field(default_factory=list)

def run_nomadic_peoples_rights_engine() -> NomadicPeoplesRightsEngineResult:
    entities = [
        NomadicPeoplesRightsEntity(
            entity_id="NP-001",
            name="Roms Europe — 10-12M Personnes, 80% Pauvreté, Expulsions Forcées & Discrimination Institutionnelle",
            country="Europe",
            forced_sedentarization_displacement_scale_score=92.0,
            legal_recognition_land_rights_gap_score=90.0,
            discrimination_service_access_denial_score=95.0,
            cultural_identity_assimilation_pressure_score=90.0,
            primary_pattern="discrimination_service_access_denial",
        ),
        NomadicPeoplesRightsEntity(
            entity_id="NP-002",
            name="Touaregs Sahel — Mali/Niger/Burkina, Rébellions Réprimées, Pastoralisme Menacé & Déplacements",
            country="Afrique de l'Ouest",
            forced_sedentarization_displacement_scale_score=90.0,
            legal_recognition_land_rights_gap_score=92.0,
            discrimination_service_access_denial_score=88.0,
            cultural_identity_assimilation_pressure_score=88.0,
            primary_pattern="legal_recognition_land_rights_gap",
        ),
        NomadicPeoplesRightsEntity(
            entity_id="NP-003",
            name="Bédouins Israël/Neguev — 90K Maisons Illégales, Démolitions Rahat & Plan Begin Non Reconnu",
            country="Moyen-Orient",
            forced_sedentarization_displacement_scale_score=88.0,
            legal_recognition_land_rights_gap_score=90.0,
            discrimination_service_access_denial_score=88.0,
            cultural_identity_assimilation_pressure_score=82.0,
            primary_pattern="forced_sedentarization_displacement_scale",
        ),
        NomadicPeoplesRightsEntity(
            entity_id="NP-004",
            name="Penan Bornéo/Malaisie — Forêt Déforestée, Chasseurs-Cueilleurs Expulsés & Mines Illégales",
            country="Asie du Sud-Est",
            forced_sedentarization_displacement_scale_score=85.0,
            legal_recognition_land_rights_gap_score=85.0,
            discrimination_service_access_denial_score=85.0,
            cultural_identity_assimilation_pressure_score=85.0,
            primary_pattern="cultural_identity_assimilation_pressure",
        ),
        NomadicPeoplesRightsEntity(
            entity_id="NP-005",
            name="Maasai Kenya/Tanzanie — Déplacements Parcs Touristiques, Perte Pâturages & Discrimination",
            country="Afrique de l'Est",
            forced_sedentarization_displacement_scale_score=52.0,
            legal_recognition_land_rights_gap_score=55.0,
            discrimination_service_access_denial_score=55.0,
            cultural_identity_assimilation_pressure_score=52.0,
            primary_pattern="forced_sedentarization_displacement_scale",
        ),
        NomadicPeoplesRightsEntity(
            entity_id="NP-006",
            name="Roms/Gens du Voyage France — 600+ Évacuations/An, Scolarité Difficile & Loi Besson Stigma",
            country="Europe",
            forced_sedentarization_displacement_scale_score=48.0,
            legal_recognition_land_rights_gap_score=52.0,
            discrimination_service_access_denial_score=55.0,
            cultural_identity_assimilation_pressure_score=48.0,
            primary_pattern="discrimination_service_access_denial",
        ),
        NomadicPeoplesRightsEntity(
            entity_id="NP-007",
            name="ERRC/OSCE — European Roma Rights Centre, Monitoring Expulsions & Advocacy Conseil Europe",
            country="Global",
            forced_sedentarization_displacement_scale_score=22.0,
            legal_recognition_land_rights_gap_score=28.0,
            discrimination_service_access_denial_score=25.0,
            cultural_identity_assimilation_pressure_score=30.0,
            primary_pattern="legal_recognition_land_rights_gap",
        ),
        NomadicPeoplesRightsEntity(
            entity_id="NP-008",
            name="ONU/DNUDPA — Déclaration Droits Peuples Autochtones Nomades, CERD Roms & ICCPR Art.27",
            country="Global",
            forced_sedentarization_displacement_scale_score=4.0,
            legal_recognition_land_rights_gap_score=5.0,
            discrimination_service_access_denial_score=3.0,
            cultural_identity_assimilation_pressure_score=6.0,
            primary_pattern="cultural_identity_assimilation_pressure",
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

    return NomadicPeoplesRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_nomadic_peoples_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "european_roma_rights_centre_annual_report_forced_evictions",
            "minority_rights_group_nomadic_peoples_under_threat_report",
            "un_dnudpa_nomadic_indigenous_peoples_rights_implementation",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_nomadic_peoples_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_nomadic_peoples_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
