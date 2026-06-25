from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ForcedRecruitmentConscriptionRightsEntity:
    entity_id: str
    name: str
    country: str
    coercive_recruitment_severity_score: float        # ×0.30
    conscientious_objection_denial_score: float       # ×0.25
    punishment_desertion_refusal_score: float         # ×0.25
    minority_disproportionate_conscription_score: float  # ×0.20
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_forced_recruitment_conscription_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.coercive_recruitment_severity_score * 0.30
            + self.conscientious_objection_denial_score * 0.25
            + self.punishment_desertion_refusal_score * 0.25
            + self.minority_disproportionate_conscription_score * 0.20,
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
        self.estimated_forced_recruitment_conscription_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ForcedRecruitmentConscriptionRightsEngineResult:
    agent: str = "Forced Recruitment & Conscription Rights Engine Agent"
    domain: str = "forced_recruitment_conscription_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_forced_recruitment_conscription_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ForcedRecruitmentConscriptionRightsEntity] = field(default_factory=list)


def run_forced_recruitment_conscription_rights_engine() -> ForcedRecruitmentConscriptionRightsEngineResult:
    entities = [
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-001",
            name="Corée du Nord — Service Militaire Obligatoire 10 Ans, Peine de Mort Désertion & Camps Travail Objecteurs",
            country="Corée du Nord",
            coercive_recruitment_severity_score=98.0,
            conscientious_objection_denial_score=99.0,
            punishment_desertion_refusal_score=98.0,
            minority_disproportionate_conscription_score=95.0,
            primary_pattern="conscientious_objection_denial",
        ),
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-002",
            name="Érythrée — Conscription Indéfinie Sawa, Service National Sans Limite Temps & Esclavage d'État",
            country="Érythrée",
            coercive_recruitment_severity_score=96.0,
            conscientious_objection_denial_score=95.0,
            punishment_desertion_refusal_score=97.0,
            minority_disproportionate_conscription_score=93.0,
            primary_pattern="punishment_desertion_refusal",
        ),
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-003",
            name="Myanmar/Birmanie — Junta Tatmadaw Recrutement Forcé Villages, Enfants Soldats & Purge Ethnique Armée",
            country="Myanmar",
            coercive_recruitment_severity_score=93.0,
            conscientious_objection_denial_score=91.0,
            punishment_desertion_refusal_score=92.0,
            minority_disproportionate_conscription_score=95.0,
            primary_pattern="minority_disproportionate_conscription",
        ),
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-004",
            name="Russie — Mobilisation Partielle 2022, Pressions Minorités Ethniques & Refus Droit Conscientieux",
            country="Russie",
            coercive_recruitment_severity_score=88.0,
            conscientious_objection_denial_score=87.0,
            punishment_desertion_refusal_score=89.0,
            minority_disproportionate_conscription_score=91.0,
            primary_pattern="minority_disproportionate_conscription",
        ),
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-005",
            name="Israël/Gaza — Conscription Universelle, Minorités Arabes Discrimination Service & Objecteurs Témoins",
            country="Israël",
            coercive_recruitment_severity_score=58.0,
            conscientious_objection_denial_score=55.0,
            punishment_desertion_refusal_score=57.0,
            minority_disproportionate_conscription_score=62.0,
            primary_pattern="minority_disproportionate_conscription",
        ),
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-006",
            name="Ukraine — Mobilisation 2022-2025, Contrôles Frontières Hommes 18-60 & Pression Démographique Sévère",
            country="Ukraine",
            coercive_recruitment_severity_score=56.0,
            conscientious_objection_denial_score=54.0,
            punishment_desertion_refusal_score=55.0,
            minority_disproportionate_conscription_score=52.0,
            primary_pattern="coercive_recruitment_severity",
        ),
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-007",
            name="War Resisters International — Droit Objection Conscience, Alternatives Service Civil & Campagnes Désertion",
            country="Global",
            coercive_recruitment_severity_score=23.0,
            conscientious_objection_denial_score=25.0,
            punishment_desertion_refusal_score=22.0,
            minority_disproportionate_conscription_score=26.0,
            primary_pattern="conscientious_objection_denial",
        ),
        ForcedRecruitmentConscriptionRightsEntity(
            entity_id="FRC-008",
            name="ONU/HCDH — Résolution Objection Conscience 1998, Art.18 PIDCP & Comité Droits Humains Commentaire 22",
            country="Global",
            coercive_recruitment_severity_score=5.0,
            conscientious_objection_denial_score=4.0,
            punishment_desertion_refusal_score=5.0,
            minority_disproportionate_conscription_score=4.0,
            primary_pattern="conscientious_objection_denial",
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

    return ForcedRecruitmentConscriptionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_forced_recruitment_conscription_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "war_resisters_international_conscientious_objection_country_reports",
            "amnesty_international_forced_recruitment_military_conscription_report",
            "human_rights_watch_eritrea_north_korea_military_slavery_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_forced_recruitment_conscription_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_forced_recruitment_conscription_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
    avg = result.avg_composite
    dist = result.risk_distribution
    print(f"avg_composite : {avg:.2f}")
    ok = (dist.get('critique', 0) == 4 and dist.get('élevé', 0) == 2 and dist.get('modéré', 0) == 1 and dist.get('faible', 0) == 1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")
