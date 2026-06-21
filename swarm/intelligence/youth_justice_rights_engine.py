from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class YouthJusticeRightsEntity:
    entity_id: str
    name: str
    country: str
    juvenile_detention_incarceration_severity_score: float
    fair_trial_youth_procedural_gap_score: float
    rehabilitation_reintegration_absence_score: float
    racial_class_bias_youth_justice_scale_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_youth_justice_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.juvenile_detention_incarceration_severity_score * 0.30
            + self.fair_trial_youth_procedural_gap_score * 0.25
            + self.rehabilitation_reintegration_absence_score * 0.25
            + self.racial_class_bias_youth_justice_scale_score * 0.20,
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
        self.estimated_youth_justice_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class YouthJusticeRightsEngineResult:
    agent: str = "Youth Justice Rights Engine Agent"
    domain: str = "youth_justice_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_youth_justice_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[YouthJusticeRightsEntity] = field(default_factory=list)

def run_youth_justice_rights_engine() -> YouthJusticeRightsEngineResult:
    entities = [
        YouthJusticeRightsEntity(
            entity_id="YJR-001",
            name="USA — 48 000 Mineurs Détenus, Biais Racial 5x Noir/Blanc & Essai Adulte Mineurs 13 Ans",
            country="États-Unis",
            juvenile_detention_incarceration_severity_score=96.0,
            fair_trial_youth_procedural_gap_score=92.0,
            rehabilitation_reintegration_absence_score=91.0,
            racial_class_bias_youth_justice_scale_score=95.0,
            primary_pattern="juvenile_detention_incarceration_severity",
        ),
        YouthJusticeRightsEntity(
            entity_id="YJR-002",
            name="Brésil — FEBEM Surpopulation 300%, Torture Systémique Mineurs & Gangs Recrutement Post-Détention",
            country="Brésil",
            juvenile_detention_incarceration_severity_score=93.0,
            fair_trial_youth_procedural_gap_score=89.0,
            rehabilitation_reintegration_absence_score=90.0,
            racial_class_bias_youth_justice_scale_score=88.0,
            primary_pattern="juvenile_detention_incarceration_severity",
        ),
        YouthJusticeRightsEntity(
            entity_id="YJR-003",
            name="Afrique Sub-Saharienne — Détention Préventive Mineurs 18 Mois, Zéro Avocat & Centres Rehab Inexistants",
            country="Afrique Sub-Saharienne",
            juvenile_detention_incarceration_severity_score=91.0,
            fair_trial_youth_procedural_gap_score=87.0,
            rehabilitation_reintegration_absence_score=88.0,
            racial_class_bias_youth_justice_scale_score=85.0,
            primary_pattern="fair_trial_youth_procedural_gap",
        ),
        YouthJusticeRightsEntity(
            entity_id="YJR-004",
            name="Inde — 33 000 Mineurs Détenus, Discrimination Caste dans Justice Juvénile & Réhabilitation Absente",
            country="Inde",
            juvenile_detention_incarceration_severity_score=88.0,
            fair_trial_youth_procedural_gap_score=85.0,
            rehabilitation_reintegration_absence_score=86.0,
            racial_class_bias_youth_justice_scale_score=82.0,
            primary_pattern="rehabilitation_reintegration_absence",
        ),
        YouthJusticeRightsEntity(
            entity_id="YJR-005",
            name="Australie — Sur-Représentation Autochtones 26x, Détention 10 Ans & Banning Ordonnances Jeunes",
            country="Australie",
            juvenile_detention_incarceration_severity_score=56.0,
            fair_trial_youth_procedural_gap_score=52.0,
            rehabilitation_reintegration_absence_score=52.0,
            racial_class_bias_youth_justice_scale_score=55.0,
            primary_pattern="racial_class_bias_youth_justice_scale",
        ),
        YouthJusticeRightsEntity(
            entity_id="YJR-006",
            name="France/UE — CEF Surpopulation, Mineurs Non Accompagnés Sans Protection & CJPM Insuffisamment Appliqué",
            country="France/UE",
            juvenile_detention_incarceration_severity_score=54.0,
            fair_trial_youth_procedural_gap_score=51.0,
            rehabilitation_reintegration_absence_score=52.0,
            racial_class_bias_youth_justice_scale_score=50.0,
            primary_pattern="fair_trial_youth_procedural_gap",
        ),
        YouthJusticeRightsEntity(
            entity_id="YJR-007",
            name="IAYFJM/PRI — Standards Minima Pékin, Justice Restaurative Jeunes & Alternatives Détention Plaidoyer",
            country="Global",
            juvenile_detention_incarceration_severity_score=22.0,
            fair_trial_youth_procedural_gap_score=28.0,
            rehabilitation_reintegration_absence_score=27.0,
            racial_class_bias_youth_justice_scale_score=30.0,
            primary_pattern="rehabilitation_reintegration_absence",
        ),
        YouthJusticeRightsEntity(
            entity_id="YJR-008",
            name="ONU/UNICEF — Convention Droits Enfant Art.37-40, Règles Beijing & Lignes Directrices Riyad",
            country="Global",
            juvenile_detention_incarceration_severity_score=4.0,
            fair_trial_youth_procedural_gap_score=5.0,
            rehabilitation_reintegration_absence_score=4.0,
            racial_class_bias_youth_justice_scale_score=5.0,
            primary_pattern="juvenile_detention_incarceration_severity",
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

    return YouthJusticeRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_youth_justice_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_justice_children_juvenile_justice_global_assessment",
            "human_rights_watch_youth_justice_incarceration_racial_bias_report",
            "penal_reform_international_global_prison_trends_youth_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_youth_justice_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_youth_justice_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
