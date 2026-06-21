"""Reproductive Rights Bodily Autonomy Engine — Avortement, stérilisation forcée, mortalité maternelle & autonomie corporelle."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class ReproductiveRightsBodlyAutonomyEntity:
    entity_id: str
    name: str
    country: str
    abortion_criminalization_ban_severity_score: float
    forced_sterilization_contraception_coercion_scale_score: float
    maternal_mortality_healthcare_denial_score: float
    reproductive_autonomy_legal_protection_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_reproductive_rights_bodily_autonomy_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.abortion_criminalization_ban_severity_score * 0.30
            + self.forced_sterilization_contraception_coercion_scale_score * 0.25
            + self.maternal_mortality_healthcare_denial_score * 0.25
            + self.reproductive_autonomy_legal_protection_deficit_gap_score * 0.20,
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
        self.estimated_reproductive_rights_bodily_autonomy_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ReproductiveRightsBodlyAutonomyEngineResult:
    agent: str = "Reproductive Rights Bodily Autonomy Engine Agent"
    domain: str = "reproductive_rights_bodily_autonomy"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_reproductive_rights_bodily_autonomy_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ReproductiveRightsBodlyAutonomyEntity] = field(default_factory=list)


def run_reproductive_rights_bodily_autonomy_engine() -> ReproductiveRightsBodlyAutonomyEngineResult:
    entities = [
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-001",
            name="El Salvador — Avortement Interdit Même Viol/Vie Mère, 30+ Femmes Emprisonnées Fausses Couches, Peines 40 Ans & ONG Criminalisées",
            country="El Salvador",
            abortion_criminalization_ban_severity_score=95.0,
            forced_sterilization_contraception_coercion_scale_score=93.0,
            maternal_mortality_healthcare_denial_score=92.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=94.0,
            primary_pattern="abortion_criminalization_ban_severity",
        ),
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-002",
            name="Nicaragua — Avortement Zéro Exception Post-2006, Femmes Mortes Chimiothérapie Refusée, Médecins Poursuivis & Opposition Étouffée",
            country="Nicaragua",
            abortion_criminalization_ban_severity_score=91.0,
            forced_sterilization_contraception_coercion_scale_score=89.0,
            maternal_mortality_healthcare_denial_score=90.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=88.0,
            primary_pattern="abortion_criminalization_ban_severity",
        ),
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-003",
            name="Pologne/Post-Roe — Quasi-Interdiction Avortement 2021, Izabela Décédée Sepsis, Médecins Refusant Soins & Femmes Voyageant Étranger",
            country="Pologne",
            abortion_criminalization_ban_severity_score=87.0,
            forced_sterilization_contraception_coercion_scale_score=85.0,
            maternal_mortality_healthcare_denial_score=89.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=86.0,
            primary_pattern="maternal_mortality_healthcare_denial",
        ),
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-004",
            name="USA/Dobbs — Roe v. Wade Renversé 2022, 14 États Interdiction Totale, Femmes Traversant Frontières & Médecins Poursuite Criminelle",
            country="USA",
            abortion_criminalization_ban_severity_score=84.0,
            forced_sterilization_contraception_coercion_scale_score=82.0,
            maternal_mortality_healthcare_denial_score=83.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=85.0,
            primary_pattern="reproductive_autonomy_legal_protection_deficit_gap",
        ),
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-005",
            name="Inde/Stérilisation — Camps Stérilisation Forcée Femmes Pauvres, Décès Post-Op 2014 Chhattisgarh, Quotas Gouvernement & Dalits Ciblées",
            country="Inde",
            abortion_criminalization_ban_severity_score=56.0,
            forced_sterilization_contraception_coercion_scale_score=57.0,
            maternal_mortality_healthcare_denial_score=54.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=55.0,
            primary_pattern="forced_sterilization_contraception_coercion_scale",
        ),
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-006",
            name="Chine/Politique — Fin Politique Enfant Unique, Naissances Forcées 3 Enfants, Stérilisation Uyghures 2019-20 & Avortements Tardifs Forcés",
            country="Chine",
            abortion_criminalization_ban_severity_score=52.0,
            forced_sterilization_contraception_coercion_scale_score=54.0,
            maternal_mortality_healthcare_denial_score=51.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=53.0,
            primary_pattern="forced_sterilization_contraception_coercion_scale",
        ),
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-007",
            name="OMS/IPPF — Standards OMS Avortement Sécurisé 2022, IPPF Global, CEDAW Comité & Lignes Directrices Contraception",
            country="Global",
            abortion_criminalization_ban_severity_score=27.0,
            forced_sterilization_contraception_coercion_scale_score=26.0,
            maternal_mortality_healthcare_denial_score=28.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=25.0,
            primary_pattern="reproductive_autonomy_legal_protection_deficit_gap",
        ),
        ReproductiveRightsBodlyAutonomyEntity(
            entity_id="RBA-008",
            name="ONU/PIDESC — PIDESC Art.12 Santé, CEDAW Art.12 Femmes, Comité DESC & SDG 3.1 Mortalité Maternelle",
            country="Global",
            abortion_criminalization_ban_severity_score=4.0,
            forced_sterilization_contraception_coercion_scale_score=4.0,
            maternal_mortality_healthcare_denial_score=4.0,
            reproductive_autonomy_legal_protection_deficit_gap_score=4.0,
            primary_pattern="abortion_criminalization_ban_severity",
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
        for e in sorted_entities if e.risk_level == "critique"
    ]

    return ReproductiveRightsBodlyAutonomyEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_reproductive_rights_bodily_autonomy_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_safe_abortion_guidelines",
            "center_reproductive_rights_global_report",
            "amnesty_international_reproductive_rights_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_reproductive_rights_bodily_autonomy_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_reproductive_rights_bodily_autonomy_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
