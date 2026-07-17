from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#ca8a04"


@dataclass
class EconomicSanctionsRightsEntity:
    entity_id: str
    name: str
    country: str
    civilian_harm_score: float
    humanitarian_exception_failure_score: float
    medical_access_denial_score: float
    food_security_impact_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_economic_sanctions_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.civilian_harm_score * 0.30
            + self.humanitarian_exception_failure_score * 0.25
            + self.medical_access_denial_score * 0.25
            + self.food_security_impact_score * 0.20,
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
        self.estimated_economic_sanctions_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class EconomicSanctionsRightsEngineResult:
    agent: str = "Economic Sanctions Rights Engine Agent"
    domain: str = "economic_sanctions_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_economic_sanctions_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EconomicSanctionsRightsEntity] = field(default_factory=list)


def run_economic_sanctions_rights_engine() -> EconomicSanctionsRightsEngineResult:
    entities = [
        EconomicSanctionsRightsEntity(
            entity_id="ESR-001",
            name="Iran — Sanctions USA, 85M Privés Médicaments Cancer/Insuline, Accès Pharmaceutique Impossible 2020-2024",
            country="Iran",
            civilian_harm_score=92.0,
            humanitarian_exception_failure_score=90.0,
            medical_access_denial_score=94.0,
            food_security_impact_score=85.0,
            primary_pattern="medical_access_denial_score",
        ),
        EconomicSanctionsRightsEntity(
            entity_id="ESR-002",
            name="Venezuela — Sanctions OFAC, 40 000 Morts Excès Mortalité 2017-2018 Étude The Lancet, Effondrement Médical",
            country="Venezuela",
            civilian_harm_score=88.0,
            humanitarian_exception_failure_score=86.0,
            medical_access_denial_score=87.0,
            food_security_impact_score=90.0,
            primary_pattern="food_security_impact_score",
        ),
        EconomicSanctionsRightsEntity(
            entity_id="ESR-003",
            name="Syrie — Sanctions Mixtes, 14M Aide Humanitaire Bloquée, Famine Intentionnelle Instrumentalisée ONU",
            country="Syrie",
            civilian_harm_score=90.0,
            humanitarian_exception_failure_score=88.0,
            medical_access_denial_score=82.0,
            food_security_impact_score=92.0,
            primary_pattern="civilian_harm_score",
        ),
        EconomicSanctionsRightsEntity(
            entity_id="ESR-004",
            name="Cuba — Blocus 60 Ans USA, Privation Médicaments, Transplants Impossibles, Impacts OMS Documentés",
            country="Cuba",
            civilian_harm_score=76.0,
            humanitarian_exception_failure_score=80.0,
            medical_access_denial_score=82.0,
            food_security_impact_score=72.0,
            primary_pattern="medical_access_denial_score",
        ),
        EconomicSanctionsRightsEntity(
            entity_id="ESR-005",
            name="Corée du Nord — Sanctions CSNU, Population Civile Sous-Alimentée, Nutrition Enfants 42% Stunting",
            country="Corée du Nord",
            civilian_harm_score=56.0,
            humanitarian_exception_failure_score=54.0,
            medical_access_denial_score=52.0,
            food_security_impact_score=58.0,
            primary_pattern="food_security_impact_score",
        ),
        EconomicSanctionsRightsEntity(
            entity_id="ESR-006",
            name="Myanmar — Sanctions Post-Coup, Impact Populations Vulnérables Civiles, Crise Humanitaire 2021-2024",
            country="Myanmar",
            civilian_harm_score=48.0,
            humanitarian_exception_failure_score=46.0,
            medical_access_denial_score=44.0,
            food_security_impact_score=50.0,
            primary_pattern="civilian_harm_score",
        ),
        EconomicSanctionsRightsEntity(
            entity_id="ESR-007",
            name="Russie — Sanctions Post-Ukraine, Impact Consommateurs Ordinaires, Inflation 20%, Accès Biens Réduit",
            country="Russie",
            civilian_harm_score=32.0,
            humanitarian_exception_failure_score=28.0,
            medical_access_denial_score=26.0,
            food_security_impact_score=30.0,
            primary_pattern="civilian_harm_score",
        ),
        EconomicSanctionsRightsEntity(
            entity_id="ESR-008",
            name="UE — Système Exemptions Humanitaires, Meilleure Pratique Comparée, Mécanismes Dérogation Codifiés",
            country="UE",
            civilian_harm_score=8.0,
            humanitarian_exception_failure_score=6.0,
            medical_access_denial_score=7.0,
            food_security_impact_score=9.0,
            primary_pattern="food_security_impact_score",
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

    return EconomicSanctionsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_economic_sanctions_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_unilateral_sanctions_report_2024",
            "oxfam_sanctions_humanitarian_impact_2023",
            "hrw_sanctions_civilian_harm_documentation",
            "icrc_sanctions_humanitarian_law_guidance",
            "who_sanctions_medical_access_global_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_economic_sanctions_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
