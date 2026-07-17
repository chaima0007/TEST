from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#a855f7"


@dataclass
class ForcedSterilizationRightsEntity:
    entity_id: str
    name: str
    country: str
    coercive_sterilization_score: float
    consent_violation_score: float
    ethnic_targeting_score: float
    legal_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_forced_sterilization_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.coercive_sterilization_score * 0.30
            + self.consent_violation_score * 0.25
            + self.ethnic_targeting_score * 0.25
            + self.legal_accountability_gap_score * 0.20,
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
        self.estimated_forced_sterilization_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ForcedSterilizationRightsEngineResult:
    agent: str = "Forced Sterilization Rights Engine Agent"
    domain: str = "forced_sterilization_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_forced_sterilization_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ForcedSterilizationRightsEntity] = field(default_factory=list)


def run_forced_sterilization_rights_engine() -> ForcedSterilizationRightsEngineResult:
    entities = [
        ForcedSterilizationRightsEntity(
            entity_id="FSR-001",
            name="Chine — Stérilisations Forcées Ouïghours au Xinjiang & Politique Enfant Unique Historique 1980-2015",
            country="Chine",
            coercive_sterilization_score=92.0,
            consent_violation_score=90.0,
            ethnic_targeting_score=93.0,
            legal_accountability_gap_score=89.0,
            primary_pattern="ethnic_targeting_score",
        ),
        ForcedSterilizationRightsEntity(
            entity_id="FSR-002",
            name="Ouzbékistan — Programme de Stérilisation des Femmes Rurales avec Quotas Imposés aux Médecins Documentés",
            country="Ouzbékistan",
            coercive_sterilization_score=88.0,
            consent_violation_score=87.0,
            ethnic_targeting_score=82.0,
            legal_accountability_gap_score=90.0,
            primary_pattern="legal_accountability_gap_score",
        ),
        ForcedSterilizationRightsEntity(
            entity_id="FSR-003",
            name="Inde — Camps de Stérilisation Forcée des Femmes Pauvres au Chhattisgarh, 13 Décès Documentés en 2014",
            country="Inde",
            coercive_sterilization_score=85.0,
            consent_violation_score=84.0,
            ethnic_targeting_score=80.0,
            legal_accountability_gap_score=86.0,
            primary_pattern="legal_accountability_gap_score",
        ),
        ForcedSterilizationRightsEntity(
            entity_id="FSR-004",
            name="Pérou — Programme Fujimori, 300 000 Stérilisations Forcées de Femmes Autochtones entre 1996 et 2000",
            country="Pérou",
            coercive_sterilization_score=87.0,
            consent_violation_score=86.0,
            ethnic_targeting_score=88.0,
            legal_accountability_gap_score=84.0,
            primary_pattern="ethnic_targeting_score",
        ),
        ForcedSterilizationRightsEntity(
            entity_id="FSR-005",
            name="USA Historique — Eugénisme Native American dans les années 1970 & Stérilisations Documentées Détenues ICE 2020",
            country="USA",
            coercive_sterilization_score=52.0,
            consent_violation_score=50.0,
            ethnic_targeting_score=55.0,
            legal_accountability_gap_score=48.0,
            primary_pattern="ethnic_targeting_score",
        ),
        ForcedSterilizationRightsEntity(
            entity_id="FSR-006",
            name="Kenya — Femmes Séropositives Stérilisées Sans Consentement, Violations Documentées par Human Rights Watch",
            country="Kenya",
            coercive_sterilization_score=48.0,
            consent_violation_score=52.0,
            ethnic_targeting_score=44.0,
            legal_accountability_gap_score=50.0,
            primary_pattern="consent_violation_score",
        ),
        ForcedSterilizationRightsEntity(
            entity_id="FSR-007",
            name="République Tchèque — Stérilisations de Femmes Roms Sans Consentement, Reconnaissances Judiciaires Récentes",
            country="République Tchèque",
            coercive_sterilization_score=30.0,
            consent_violation_score=32.0,
            ethnic_targeting_score=28.0,
            legal_accountability_gap_score=29.0,
            primary_pattern="consent_violation_score",
        ),
        ForcedSterilizationRightsEntity(
            entity_id="FSR-008",
            name="Canada — Premières Compensations aux Femmes Autochtones Stérilisées & Loi C-66 Excuses Officielles",
            country="Canada",
            coercive_sterilization_score=11.0,
            consent_violation_score=10.0,
            ethnic_targeting_score=12.0,
            legal_accountability_gap_score=9.0,
            primary_pattern="ethnic_targeting_score",
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

    return ForcedSterilizationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_forced_sterilization_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_health_forced_sterilization_2011",
            "hrw_forced_sterilization_documentation_global",
            "amnesty_reproductive_rights_violations_report",
            "who_eliminating_forced_coercive_sterilization_2014",
            "ohchr_forced_sterilization_intersex_persons_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_forced_sterilization_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
