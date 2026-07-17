from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EconomicAusteritySocialRightsEntity:
    entity_id: str
    name: str
    country: str
    healthcare_education_cuts_severity_score: float
    pension_social_security_dismantlement_scale_score: float
    imf_structural_adjustment_conditionality_score: float
    progressive_taxation_wealth_redistribution_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_economic_austerity_social_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.healthcare_education_cuts_severity_score * 0.30
            + self.pension_social_security_dismantlement_scale_score * 0.25
            + self.imf_structural_adjustment_conditionality_score * 0.25
            + self.progressive_taxation_wealth_redistribution_deficit_gap_score * 0.20,
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
        self.estimated_economic_austerity_social_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EconomicAusteritySocialRightsEngineResult:
    agent: str = "Economic Austerity Social Rights Engine Agent"
    domain: str = "economic_austerity_social_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_economic_austerity_social_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EconomicAusteritySocialRightsEntity] = field(default_factory=list)

def run_economic_austerity_social_rights_engine() -> EconomicAusteritySocialRightsEngineResult:
    entities = [
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-001",
            name="Grèce 2010-18 — Troïka Mémorandums, Salaires -40%, Hôpitaux Fermés 30%, Suicides +35% & Enfants Malnutrition Retour",
            country="Grèce",
            healthcare_education_cuts_severity_score=95.0,
            pension_social_security_dismantlement_scale_score=93.0,
            imf_structural_adjustment_conditionality_score=92.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=94.0,
            primary_pattern="healthcare_education_cuts_severity",
        ),
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-002",
            name="Argentine/FMI — Prêt 57Mds 2018, Coupes Sociales Macri, Pauvreté 40% & Milei Chainsaw 30% Budget État",
            country="Argentine",
            healthcare_education_cuts_severity_score=91.0,
            pension_social_security_dismantlement_scale_score=89.0,
            imf_structural_adjustment_conditionality_score=90.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=88.0,
            primary_pattern="imf_structural_adjustment_conditionality",
        ),
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-003",
            name="Zimbabwe/SAP — ESAP 1990s FMI Désastre, Santé Effondrée, Inflation 500% & Pauvreté 80% Post-Ajustement",
            country="Zimbabwe",
            healthcare_education_cuts_severity_score=87.0,
            pension_social_security_dismantlement_scale_score=86.0,
            imf_structural_adjustment_conditionality_score=85.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=88.0,
            primary_pattern="imf_structural_adjustment_conditionality",
        ),
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-004",
            name="UK/Austerité Cameron — NHS Coupes 2010-19, Universal Credit Pauvreté, Banques Alimentaires +400% & Espérance Vie Stagnée Pauvres",
            country="UK",
            healthcare_education_cuts_severity_score=83.0,
            pension_social_security_dismantlement_scale_score=82.0,
            imf_structural_adjustment_conditionality_score=84.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=81.0,
            primary_pattern="pension_social_security_dismantlement_scale",
        ),
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-005",
            name="Brésil/EC 95 — Amendement Constitutionnel Plafond Dépenses 20 Ans, SUS Santé Sous-Financé, Bolsonaro Privatisations & Familles Faim Retour",
            country="Brésil",
            healthcare_education_cuts_severity_score=56.0,
            pension_social_security_dismantlement_scale_score=54.0,
            imf_structural_adjustment_conditionality_score=55.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=57.0,
            primary_pattern="healthcare_education_cuts_severity",
        ),
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-006",
            name="France/Retraites — Réforme 64 Ans Contestée, CFDT/CGT Résistance, Décret Article 49.3 & Droits Sociaux Érodés",
            country="France",
            healthcare_education_cuts_severity_score=52.0,
            pension_social_security_dismantlement_scale_score=51.0,
            imf_structural_adjustment_conditionality_score=54.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=53.0,
            primary_pattern="pension_social_security_dismantlement_scale",
        ),
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-007",
            name="CESR/Oxfam — Center Economic Social Rights, Oxfam Inégalités Rapport, Alternative Budget & Mécanismes DESC",
            country="Global",
            healthcare_education_cuts_severity_score=27.0,
            pension_social_security_dismantlement_scale_score=25.0,
            imf_structural_adjustment_conditionality_score=28.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=26.0,
            primary_pattern="progressive_taxation_wealth_redistribution_deficit_gap",
        ),
        EconomicAusteritySocialRightsEntity(
            entity_id="EAS-008",
            name="ONU/PIDESC Art.2 — Réalisation Progressive DESC, Comité DESC Observation 2 Ressources Max, SDG 1 Pauvreté & Standards Minimum Core",
            country="Global",
            healthcare_education_cuts_severity_score=4.0,
            pension_social_security_dismantlement_scale_score=4.0,
            imf_structural_adjustment_conditionality_score=4.0,
            progressive_taxation_wealth_redistribution_deficit_gap_score=4.0,
            primary_pattern="imf_structural_adjustment_conditionality",
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

    return EconomicAusteritySocialRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_economic_austerity_social_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "cesr_economic_social_rights_austerity_report",
            "oxfam_inequality_austerity_report",
            "un_desc_structural_adjustment_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_economic_austerity_social_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_economic_austerity_social_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
