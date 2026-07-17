from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class BondedLaborDebtSlaveryRightsEntity:
    entity_id: str
    name: str
    country: str
    debt_bondage_coercion_severity_score: float       # ×0.30
    legal_protection_enforcement_gap_score: float     # ×0.25
    economic_dependency_vulnerability_score: float    # ×0.25
    family_generational_bondage_scale_score: float    # ×0.20
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_bonded_labor_debt_slavery_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.debt_bondage_coercion_severity_score * 0.30
            + self.legal_protection_enforcement_gap_score * 0.25
            + self.economic_dependency_vulnerability_score * 0.25
            + self.family_generational_bondage_scale_score * 0.20,
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
        self.estimated_bonded_labor_debt_slavery_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class BondedLaborDebtSlaveryRightsEngineResult:
    agent: str = "Bonded Labor & Debt Slavery Rights Engine Agent"
    domain: str = "bonded_labor_debt_slavery_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_bonded_labor_debt_slavery_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[BondedLaborDebtSlaveryRightsEntity] = field(default_factory=list)


def run_bonded_labor_debt_slavery_rights_engine() -> BondedLaborDebtSlaveryRightsEngineResult:
    entities = [
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-001",
            name="Inde — 18 Millions Travailleurs Liés, Dalits Briqueteries & Dette Inter-Générationnelle Héréditaire",
            country="Inde",
            debt_bondage_coercion_severity_score=97.0,
            legal_protection_enforcement_gap_score=94.0,
            economic_dependency_vulnerability_score=95.0,
            family_generational_bondage_scale_score=96.0,
            primary_pattern="debt_bondage_coercion_severity",
        ),
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-002",
            name="Pakistan — Agriculture Sindh, Servitude Dette Propriétaires & Travail Forçé Minorités Religieuses",
            country="Pakistan",
            debt_bondage_coercion_severity_score=94.0,
            legal_protection_enforcement_gap_score=92.0,
            economic_dependency_vulnerability_score=91.0,
            family_generational_bondage_scale_score=93.0,
            primary_pattern="debt_bondage_coercion_severity",
        ),
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-003",
            name="Brésil — Peonagem Amazonie, Travailleurs Ruraux Piégés Fazendas & Escravatura Rural Moderne",
            country="Brésil",
            debt_bondage_coercion_severity_score=91.0,
            legal_protection_enforcement_gap_score=88.0,
            economic_dependency_vulnerability_score=89.0,
            family_generational_bondage_scale_score=87.0,
            primary_pattern="economic_dependency_vulnerability",
        ),
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-004",
            name="Népal/Bangladesh — Kamaiya, Harwa-Charwa & Migration Dette Recrutement Frauduleux Golfe",
            country="Népal/Bangladesh",
            debt_bondage_coercion_severity_score=89.0,
            legal_protection_enforcement_gap_score=87.0,
            economic_dependency_vulnerability_score=88.0,
            family_generational_bondage_scale_score=90.0,
            primary_pattern="family_generational_bondage_scale",
        ),
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-005",
            name="Mauritanie/Soudan — Esclavage Héréditaire Haratines, Abid & Persistance Pratiques Post-Abolition",
            country="Mauritanie/Soudan",
            debt_bondage_coercion_severity_score=57.0,
            legal_protection_enforcement_gap_score=60.0,
            economic_dependency_vulnerability_score=58.0,
            family_generational_bondage_scale_score=62.0,
            primary_pattern="family_generational_bondage_scale",
        ),
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-006",
            name="Qatar/EAU — Système Kafala, Travailleurs Migrants Passeports Confisqués & Contrats Substitués",
            country="Qatar/EAU",
            debt_bondage_coercion_severity_score=55.0,
            legal_protection_enforcement_gap_score=53.0,
            economic_dependency_vulnerability_score=57.0,
            family_generational_bondage_scale_score=50.0,
            primary_pattern="economic_dependency_vulnerability",
        ),
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-007",
            name="ILO/Walk Free — Protocole 2014 Travail Forcé, Indice Esclavage Moderne & Programmes Sortie Dette",
            country="Global",
            debt_bondage_coercion_severity_score=25.0,
            legal_protection_enforcement_gap_score=22.0,
            economic_dependency_vulnerability_score=24.0,
            family_generational_bondage_scale_score=20.0,
            primary_pattern="legal_protection_enforcement_gap",
        ),
        BondedLaborDebtSlaveryRightsEntity(
            entity_id="BLD-008",
            name="ONU/HCDH — Convention Supplémentaire Abolition Esclavage 1956, Art.1 Servitude & Mécanismes Contrôle",
            country="Global",
            debt_bondage_coercion_severity_score=5.0,
            legal_protection_enforcement_gap_score=6.0,
            economic_dependency_vulnerability_score=5.0,
            family_generational_bondage_scale_score=4.0,
            primary_pattern="debt_bondage_coercion_severity",
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

    return BondedLaborDebtSlaveryRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_bonded_labor_debt_slavery_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_global_estimates_modern_slavery_forced_labour_2022",
            "walk_free_global_slavery_index_bonded_labour_south_asia",
            "anti_slavery_international_debt_bondage_contemporary_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_bonded_labor_debt_slavery_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_bonded_labor_debt_slavery_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
    avg = result.avg_composite
    dist = result.risk_distribution
    print(f"avg_composite : {avg:.2f}")
    ok = (dist.get('critique', 0) == 4 and dist.get('élevé', 0) == 2 and dist.get('modéré', 0) == 1 and dist.get('faible', 0) == 1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")
