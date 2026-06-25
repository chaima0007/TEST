from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SportsAthleteRightsEntity:
    entity_id: str
    name: str
    country: str
    athlete_exploitation_unpaid_labor_severity_score: float
    doping_corruption_cover_up_scale_score: float
    sports_sexual_abuse_coach_impunity_score: float
    athlete_free_speech_political_expression_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_sports_athlete_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.athlete_exploitation_unpaid_labor_severity_score * 0.30
            + self.doping_corruption_cover_up_scale_score * 0.25
            + self.sports_sexual_abuse_coach_impunity_score * 0.25
            + self.athlete_free_speech_political_expression_deficit_gap_score * 0.20,
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
        self.estimated_sports_athlete_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class SportsAthleteRightsEngineResult:
    agent: str = "Sports Athlete Rights Engine Agent"
    domain: str = "sports_athlete_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sports_athlete_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SportsAthleteRightsEntity] = field(default_factory=list)


def run_sports_athlete_rights_engine() -> SportsAthleteRightsEngineResult:
    entities = [
        SportsAthleteRightsEntity(
            entity_id="SAR-001",
            name="Russie/Chine — Dopage Systématique État, RUSADA Scandale, McLaren Report, Athlètes Femmes Gymnastes Abus & Boycotts Silenciés",
            country="Russie/Chine",
            athlete_exploitation_unpaid_labor_severity_score=95.0,
            doping_corruption_cover_up_scale_score=93.0,
            sports_sexual_abuse_coach_impunity_score=92.0,
            athlete_free_speech_political_expression_deficit_gap_score=91.0,
            primary_pattern="doping_corruption_cover_up_scale",
        ),
        SportsAthleteRightsEntity(
            entity_id="SAR-002",
            name="Qatar/FIFA — Travailleurs Stades Morts 6 500, Corruption FIFA Sepp Blatter, Athlètes Droits Bafoués & Chaleur Mortelle",
            country="Qatar",
            athlete_exploitation_unpaid_labor_severity_score=92.0,
            doping_corruption_cover_up_scale_score=90.0,
            sports_sexual_abuse_coach_impunity_score=89.0,
            athlete_free_speech_political_expression_deficit_gap_score=88.0,
            primary_pattern="athlete_exploitation_unpaid_labor_severity",
        ),
        SportsAthleteRightsEntity(
            entity_id="SAR-003",
            name="USA/NCAA — Athlètes Universitaires Non Payés 5B$/An Revenus, Abus Sexuels Larry Nassar 300 Victimes & NFL CTE Dissimulé",
            country="USA",
            athlete_exploitation_unpaid_labor_severity_score=89.0,
            doping_corruption_cover_up_scale_score=87.0,
            sports_sexual_abuse_coach_impunity_score=86.0,
            athlete_free_speech_political_expression_deficit_gap_score=85.0,
            primary_pattern="sports_sexual_abuse_coach_impunity",
        ),
        SportsAthleteRightsEntity(
            entity_id="SAR-004",
            name="Arabie Saoudite — Sports Washing Golfs/Boxe, LIV Golf Critiques Tues, Activistes Sportifs Emprisonnés & Femmes Sport Tardif",
            country="Arabie Saoudite",
            athlete_exploitation_unpaid_labor_severity_score=86.0,
            doping_corruption_cover_up_scale_score=84.0,
            sports_sexual_abuse_coach_impunity_score=83.0,
            athlete_free_speech_political_expression_deficit_gap_score=82.0,
            primary_pattern="athlete_free_speech_political_expression_deficit_gap",
        ),
        SportsAthleteRightsEntity(
            entity_id="SAR-005",
            name="Chine/IOC — Hong Kong Athlètes Pression, IOC Silence Droits Humains, Nathan Law Exilé & Peng Shuai Disparition",
            country="Chine",
            athlete_exploitation_unpaid_labor_severity_score=57.0,
            doping_corruption_cover_up_scale_score=55.0,
            sports_sexual_abuse_coach_impunity_score=54.0,
            athlete_free_speech_political_expression_deficit_gap_score=53.0,
            primary_pattern="athlete_free_speech_political_expression_deficit_gap",
        ),
        SportsAthleteRightsEntity(
            entity_id="SAR-006",
            name="USA/Europe — NIL Student Athletes Inégaux, Contrats Exploiteurs, Black Athletes Protest NFL & Transfer Portal Abus",
            country="USA/Europe",
            athlete_exploitation_unpaid_labor_severity_score=54.0,
            doping_corruption_cover_up_scale_score=52.0,
            sports_sexual_abuse_coach_impunity_score=51.0,
            athlete_free_speech_political_expression_deficit_gap_score=50.0,
            primary_pattern="athlete_exploitation_unpaid_labor_severity",
        ),
        SportsAthleteRightsEntity(
            entity_id="SAR-007",
            name="Global Athletes/WADA — Association Athlètes Internationaux, Anti-Dopage Réforme, Droits Représentation & Plateforme Signalement",
            country="Global",
            athlete_exploitation_unpaid_labor_severity_score=27.0,
            doping_corruption_cover_up_scale_score=26.0,
            sports_sexual_abuse_coach_impunity_score=25.0,
            athlete_free_speech_political_expression_deficit_gap_score=25.0,
            primary_pattern="doping_corruption_cover_up_scale",
        ),
        SportsAthleteRightsEntity(
            entity_id="SAR-008",
            name="ONU/CDES — Droit Sport Charte Internationale, Olympisme Droits Humains & SDG 3 Santé Bien-Être",
            country="Global",
            athlete_exploitation_unpaid_labor_severity_score=5.0,
            doping_corruption_cover_up_scale_score=4.0,
            sports_sexual_abuse_coach_impunity_score=4.0,
            athlete_free_speech_political_expression_deficit_gap_score=4.0,
            primary_pattern="athlete_free_speech_political_expression_deficit_gap",
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

    return SportsAthleteRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sports_athlete_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_athletes_athlete_rights_violations_report",
            "wada_doping_violations_annual_statistics",
            "human_rights_watch_sports_abuse_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_sports_athlete_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sports_athlete_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
