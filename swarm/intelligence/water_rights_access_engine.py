"""
Caelum Partners — Water Rights Access Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droit à l'eau potable, privatisation eau, exclusion hydrique populations vulnérables.

En 2010, l'Assemblée générale des Nations Unies a reconnu le droit à l'eau potable
et à l'assainissement comme un droit humain fondamental (Résolution 64/292). Pourtant,
en 2026, plus de 2 milliards de personnes manquent d'accès à une eau potable sûre,
et 3,6 milliards sont privées de services d'assainissement adéquats selon l'OMS/UNICEF.

La privatisation de l'eau sous pression des institutions financières internationales
(FMI, Banque mondiale) a exacerbé l'exclusion hydrique dans les pays à faible revenu.
Les communautés autochtones, les femmes rurales et les populations racialisées sont
les plus touchées par cette exclusion systémique. La contamination des réseaux d'eau
par le plomb (Flint, USA), l'arsenic (Bangladesh, Inde) ou les PFAS (communautés
frontières USA) révèle une discrimination environnementale structurelle.

Risk levels (privation droit eau et exclusion hydrique systémique) :
  critique  -> composite >= 60  (privation massive — millions sans eau sûre, aucune alternative)
  élevé     -> composite >= 40  (exclusion active — contamination, déconnexions, discrimination)
  modéré    -> composite >= 20  (plaidoyer droit eau — cadre ONU insuffisamment appliqué)
  faible    -> composite < 20   (protection normative — SDG 6, cadre rapporteur spécial)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class WaterRightsAccessEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    safe_water_access_deprivation_severity_score: float
    water_privatisation_corporate_capture_scale_score: float
    indigenous_water_rights_violation_score: float
    sanitation_hygiene_exclusion_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_water_rights_access_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.safe_water_access_deprivation_severity_score * 0.30
            + self.water_privatisation_corporate_capture_scale_score * 0.25
            + self.indigenous_water_rights_violation_score * 0.25
            + self.sanitation_hygiene_exclusion_gap_score * 0.20,
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
        self.estimated_water_rights_access_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "safe_water_access_deprivation_severity_score": self.safe_water_access_deprivation_severity_score,
            "water_privatisation_corporate_capture_scale_score": self.water_privatisation_corporate_capture_scale_score,
            "indigenous_water_rights_violation_score": self.indigenous_water_rights_violation_score,
            "sanitation_hygiene_exclusion_gap_score": self.sanitation_hygiene_exclusion_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_water_rights_access_index": self.estimated_water_rights_access_index,
            "last_updated": self.last_updated,
        }


@dataclass
class WaterRightsAccessEngineResult:
    agent: str = "Water Rights Access Engine Agent"
    domain: str = "water_rights_access"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_water_rights_access_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WaterRightsAccessEntity] = field(default_factory=list)


def run_water_rights_access_engine() -> WaterRightsAccessEngineResult:
    entities = [
        WaterRightsAccessEntity(
            entity_id="WAR-001",
            name="Afrique Sub-Saharienne — 400M Sans Eau Potable, Privatisation FMI & Femmes 6h/Jour Collecte",
            country="Afrique Sub-Saharienne",
            sector="Accès Eau Rurale",
            safe_water_access_deprivation_severity_score=96.0,
            water_privatisation_corporate_capture_scale_score=93.0,
            indigenous_water_rights_violation_score=91.0,
            sanitation_hygiene_exclusion_gap_score=92.0,
            primary_pattern="safe_water_access_deprivation_severity",
        ),
        WaterRightsAccessEntity(
            entity_id="WAR-002",
            name="Asie du Sud — Inde/Bangladesh Pollution Arsenic, 200M Privés Eau Sûre & Industries Sans Traitement",
            country="Asie du Sud",
            sector="Contamination Eau Industrielle",
            safe_water_access_deprivation_severity_score=93.0,
            water_privatisation_corporate_capture_scale_score=90.0,
            indigenous_water_rights_violation_score=88.0,
            sanitation_hygiene_exclusion_gap_score=89.0,
            primary_pattern="safe_water_access_deprivation_severity",
        ),
        WaterRightsAccessEntity(
            entity_id="WAR-003",
            name="MENA/Yemen — Guerre Eau, 18M Sans Accès Sûr, Puits Bombardés & Choléra",
            country="Yemen/MENA",
            sector="Eau en Zones de Conflit",
            safe_water_access_deprivation_severity_score=90.0,
            water_privatisation_corporate_capture_scale_score=87.0,
            indigenous_water_rights_violation_score=85.0,
            sanitation_hygiene_exclusion_gap_score=86.0,
            primary_pattern="safe_water_access_deprivation_severity",
        ),
        WaterRightsAccessEntity(
            entity_id="WAR-004",
            name="Amérique Latine/Communautés Autochtones — Barrages Hydro, Droits Autochtones Eau & Agro-Industrie",
            country="Amérique Latine",
            sector="Droits Eau Autochtones",
            safe_water_access_deprivation_severity_score=87.0,
            water_privatisation_corporate_capture_scale_score=84.0,
            indigenous_water_rights_violation_score=90.0,
            sanitation_hygiene_exclusion_gap_score=83.0,
            primary_pattern="indigenous_water_rights_violation",
        ),
        WaterRightsAccessEntity(
            entity_id="WAR-005",
            name="USA/Flint/Frontline Communities — Contamination Plomb, Pollution PFAS Communautés Noires & Inaction État",
            country="USA",
            sector="Justice Eau Environnementale",
            safe_water_access_deprivation_severity_score=57.0,
            water_privatisation_corporate_capture_scale_score=54.0,
            indigenous_water_rights_violation_score=52.0,
            sanitation_hygiene_exclusion_gap_score=53.0,
            primary_pattern="water_privatisation_corporate_capture_scale",
        ),
        WaterRightsAccessEntity(
            entity_id="WAR-006",
            name="Europe de l'Est/Roms — Accès Eau Non Raccordés, Déconnexions Arbitraires & Discrimination",
            country="Europe de l'Est",
            sector="Exclusion Hydrique Roms",
            safe_water_access_deprivation_severity_score=54.0,
            water_privatisation_corporate_capture_scale_score=51.0,
            indigenous_water_rights_violation_score=49.0,
            sanitation_hygiene_exclusion_gap_score=50.0,
            primary_pattern="sanitation_hygiene_exclusion_gap",
        ),
        WaterRightsAccessEntity(
            entity_id="WAR-007",
            name="Coalition Eau Bien Commun/Oxfam — Plaidoyer Droit Eau ONU Rés 64/292 & Antiprivatisation",
            country="Global",
            sector="Plaidoyer Droit à l'Eau",
            safe_water_access_deprivation_severity_score=28.0,
            water_privatisation_corporate_capture_scale_score=25.0,
            indigenous_water_rights_violation_score=26.0,
            sanitation_hygiene_exclusion_gap_score=27.0,
            primary_pattern="water_privatisation_corporate_capture_scale",
        ),
        WaterRightsAccessEntity(
            entity_id="WAR-008",
            name="ONU/SDG 6 — Objectif Eau & Assainissement 2030, Rapporteur Spécial Eau & Cadre Normatif",
            country="Global",
            sector="Cadre Normatif International",
            safe_water_access_deprivation_severity_score=5.0,
            water_privatisation_corporate_capture_scale_score=4.0,
            indigenous_water_rights_violation_score=4.0,
            sanitation_hygiene_exclusion_gap_score=3.0,
            primary_pattern="safe_water_access_deprivation_severity",
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

    return WaterRightsAccessEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_water_rights_access_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_unicef_jmp_progress_drinking_water_sanitation_hygiene_report",
            "un_special_rapporteur_human_right_safe_drinking_water_sanitation_report",
            "foodandwaterwatch_water_privatisation_global_crisis_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_water_rights_access_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_water_rights_access_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
