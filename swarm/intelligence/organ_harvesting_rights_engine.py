from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#dc2626"


@dataclass
class OrganHarvestingRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_organ_extraction_score: float
    prisoner_organ_trafficking_score: float
    consent_violation_medical_score: float
    accountability_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_organ_harvesting_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_organ_extraction_score * 0.30
            + self.prisoner_organ_trafficking_score * 0.25
            + self.consent_violation_medical_score * 0.25
            + self.accountability_impunity_score * 0.20,
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
        self.estimated_organ_harvesting_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class OrganHarvestingRightsEngineResult:
    agent: str = "Organ Harvesting Rights Engine Agent"
    domain: str = "organ_harvesting_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_organ_harvesting_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[OrganHarvestingRightsEntity] = field(default_factory=list)


def run_organ_harvesting_rights_engine() -> OrganHarvestingRightsEngineResult:
    entities = [
        OrganHarvestingRightsEntity(
            entity_id="OHR-001",
            name="Chine — Prisonniers Conscience Falun Gong, Tribunal Londres 2019 Certitude, 60-100k Transplantations/An Forcées",
            country="Chine",
            forced_organ_extraction_score=98.0,
            prisoner_organ_trafficking_score=97.0,
            consent_violation_medical_score=98.0,
            accountability_impunity_score=96.0,
            primary_pattern="forced_organ_extraction_score",
        ),
        OrganHarvestingRightsEntity(
            entity_id="OHR-002",
            name="Chine — Ouïghours Détenus Xinjiang, Prélèvements Organes Documentés RAND 2022, Banque Organes Ethnique",
            country="Chine",
            forced_organ_extraction_score=93.0,
            prisoner_organ_trafficking_score=91.0,
            consent_violation_medical_score=92.0,
            accountability_impunity_score=94.0,
            primary_pattern="accountability_impunity_score",
        ),
        OrganHarvestingRightsEntity(
            entity_id="OHR-003",
            name="Chine — Prisonniers Politiques, Banque Organes Forcée, Temps Attente 1 Semaine vs 3-5 Ans en Occident",
            country="Chine",
            forced_organ_extraction_score=90.0,
            prisoner_organ_trafficking_score=92.0,
            consent_violation_medical_score=89.0,
            accountability_impunity_score=91.0,
            primary_pattern="prisoner_organ_trafficking_score",
        ),
        OrganHarvestingRightsEntity(
            entity_id="OHR-004",
            name="Inde — Tourisme Organes Illégal Bombay/Chennai, Réseaux Transplantation, Rein Poverty Trap Documenté",
            country="Inde",
            forced_organ_extraction_score=72.0,
            prisoner_organ_trafficking_score=68.0,
            consent_violation_medical_score=74.0,
            accountability_impunity_score=70.0,
            primary_pattern="consent_violation_medical_score",
        ),
        OrganHarvestingRightsEntity(
            entity_id="OHR-005",
            name="Égypte — Organes Réfugiés Sinaï, Trafic Documenté HRW, Migrants Victimes Prélèvements Forcés",
            country="Égypte",
            forced_organ_extraction_score=58.0,
            prisoner_organ_trafficking_score=54.0,
            consent_violation_medical_score=55.0,
            accountability_impunity_score=56.0,
            primary_pattern="forced_organ_extraction_score",
        ),
        OrganHarvestingRightsEntity(
            entity_id="OHR-006",
            name="Pakistan — Trafic Rein, Village Rein Sargodha, Pauvres Vendeurs Contraints, Chirurgiens Complices",
            country="Pakistan",
            forced_organ_extraction_score=46.0,
            prisoner_organ_trafficking_score=50.0,
            consent_violation_medical_score=48.0,
            accountability_impunity_score=44.0,
            primary_pattern="prisoner_organ_trafficking_score",
        ),
        OrganHarvestingRightsEntity(
            entity_id="OHR-007",
            name="Philippines — Tourisme Médical Organes, Régulation Insuffisante, Donneurs Économiquement Vulnérables",
            country="Philippines",
            forced_organ_extraction_score=28.0,
            prisoner_organ_trafficking_score=26.0,
            consent_violation_medical_score=30.0,
            accountability_impunity_score=24.0,
            primary_pattern="consent_violation_medical_score",
        ),
        OrganHarvestingRightsEntity(
            entity_id="OHR-008",
            name="Espagne — Système Opt-Out, Meilleur Taux Don Mondial, Zéro Tourisme Médical, Modèle de Référence",
            country="Espagne",
            forced_organ_extraction_score=5.0,
            prisoner_organ_trafficking_score=4.0,
            consent_violation_medical_score=5.0,
            accountability_impunity_score=6.0,
            primary_pattern="forced_organ_extraction_score",
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

    return OrganHarvestingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_organ_harvesting_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "china_tribunal_forced_organ_harvesting_final_judgement_2019",
            "doctor_against_forced_organ_harvesting_dafor_report",
            "un_special_rapporteur_torture_organ_harvesting",
            "hrw_china_organ_transplant_documentation",
            "ethan_gutmann_slaughter_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_organ_harvesting_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
