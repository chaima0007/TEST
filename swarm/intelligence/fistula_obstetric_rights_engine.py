from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class FistulaObstetricRightsEntity:
    entity_id: str
    name: str
    country: str
    obstetric_care_access_gap_score: float
    social_rejection_abandonment_score: float
    surgical_repair_access_score: float
    legal_accountability_maternal_rights_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_fistula_obstetric_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.obstetric_care_access_gap_score * 0.30
            + self.social_rejection_abandonment_score * 0.25
            + self.surgical_repair_access_score * 0.25
            + self.legal_accountability_maternal_rights_score * 0.20,
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
        self.estimated_fistula_obstetric_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class FistulaObstetricRightsEngineResult:
    agent: str = "Fistula Obstetric Rights Engine Agent"
    domain: str = "fistula_obstetric_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_fistula_obstetric_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FistulaObstetricRightsEntity] = field(default_factory=list)


def run_fistula_obstetric_rights_engine() -> FistulaObstetricRightsEngineResult:
    entities = [
        FistulaObstetricRightsEntity(
            entity_id="FO-001",
            name="Nigéria/Niger Delta — 40 000 Nouveaux Cas/An, Mortalité Maternelle 600/100K & Zéro Accès Césarienne Zones Rurales",
            country="Afrique de l'Ouest",
            obstetric_care_access_gap_score=95.0,
            social_rejection_abandonment_score=92.0,
            surgical_repair_access_score=95.0,
            legal_accountability_maternal_rights_score=90.0,
            primary_pattern="obstetric_care_access_gap",
        ),
        FistulaObstetricRightsEntity(
            entity_id="FO-002",
            name="Éthiopie/Soudan — 100 000 Cas Non Traités Estimés, Mariage Enfants 40% & Abandon Conjugal Post-Fistule 65%",
            country="Afrique de l'Est",
            obstetric_care_access_gap_score=92.0,
            social_rejection_abandonment_score=95.0,
            surgical_repair_access_score=90.0,
            legal_accountability_maternal_rights_score=88.0,
            primary_pattern="social_rejection_abandonment",
        ),
        FistulaObstetricRightsEntity(
            entity_id="FO-003",
            name="RDC/Congo — Fistule Traumatique Guerre + Obstétricale, Violences Sexuelles Conflit & Soins Réparation Absents",
            country="Afrique Centrale",
            obstetric_care_access_gap_score=90.0,
            social_rejection_abandonment_score=88.0,
            surgical_repair_access_score=92.0,
            legal_accountability_maternal_rights_score=85.0,
            primary_pattern="surgical_repair_access",
        ),
        FistulaObstetricRightsEntity(
            entity_id="FO-004",
            name="Mali/Burkina Faso — Mariage Précoce Massif, Accouchement Sans Assistance 70% Rural & Soins Limités 3 Chirurgiens",
            country="Afrique de l'Ouest",
            obstetric_care_access_gap_score=85.0,
            social_rejection_abandonment_score=88.0,
            surgical_repair_access_score=88.0,
            legal_accountability_maternal_rights_score=82.0,
            primary_pattern="social_rejection_abandonment",
        ),
        FistulaObstetricRightsEntity(
            entity_id="FO-005",
            name="Afghanistan/Yémen — Conflit + Fistule, Accès Soins Obstétricaux Effondré & Femmes Cachées par Honte Familiale",
            country="Moyen-Orient/Asie Centrale",
            obstetric_care_access_gap_score=55.0,
            social_rejection_abandonment_score=58.0,
            surgical_repair_access_score=60.0,
            legal_accountability_maternal_rights_score=55.0,
            primary_pattern="obstetric_care_access_gap",
        ),
        FistulaObstetricRightsEntity(
            entity_id="FO-006",
            name="Bangladesh/Pakistan — Fistule Rurale Persistante, Stigmate Extrême & Programme Réparation Partiel UNFPA",
            country="Asie du Sud",
            obstetric_care_access_gap_score=48.0,
            social_rejection_abandonment_score=52.0,
            surgical_repair_access_score=45.0,
            legal_accountability_maternal_rights_score=48.0,
            primary_pattern="social_rejection_abandonment",
        ),
        FistulaObstetricRightsEntity(
            entity_id="FO-007",
            name="UNFPA Campaign to End Fistula — 100 Pays, 100 000 Réparations & Plaidoyer Accès Soins Maternels",
            country="Global",
            obstetric_care_access_gap_score=25.0,
            social_rejection_abandonment_score=22.0,
            surgical_repair_access_score=18.0,
            legal_accountability_maternal_rights_score=28.0,
            primary_pattern="legal_accountability_maternal_rights",
        ),
        FistulaObstetricRightsEntity(
            entity_id="FO-008",
            name="OMS/ODD3 — Objectif Mortalité Maternelle <70/100K, Couverture Soins Prénataux & Indicateurs Fistule",
            country="Global",
            obstetric_care_access_gap_score=6.0,
            social_rejection_abandonment_score=5.0,
            surgical_repair_access_score=4.0,
            legal_accountability_maternal_rights_score=8.0,
            primary_pattern="legal_accountability_maternal_rights",
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

    return FistulaObstetricRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_fistula_obstetric_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unfpa_campaign_to_end_fistula_global_report_2021",
            "who_obstetric_fistula_prevention_and_treatment_guidelines",
            "lancet_obstetric_fistula_burden_disease_sub_saharan_africa_2022",
            "human_rights_watch_maternal_health_rights_niger_nigeria_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_fistula_obstetric_rights_engine()
    dist = result.risk_distribution
    avg = result.avg_composite
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Risk distribution: {dist}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
    print(f"avg_composite : {avg:.2f}")
    ok = (dist.get('critique', 0) == 4 and dist.get('élevé', 0) == 2 and dist.get('modéré', 0) == 1 and dist.get('faible', 0) == 1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")
