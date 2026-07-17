"""
Caelum Partners — Child Labor Mining Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Travail des enfants dans les mines (cobalt, or, mica), travail dangereux mineur.

Le travail des enfants dans les mines artisanales et à petite échelle (ASM) représente
l'une des pires formes de travail des enfants selon la Convention ILO C182. Plus de
1 million d'enfants travaillent dans des mines à travers le monde, exposés à des
conditions dangereuses : exposition au mercure, poussière de silice, tunnels instables,
et travail nocturne — dans des mines d'où proviennent les minéraux alimentant
l'économie numérique mondiale (cobalt pour batteries EV, mica pour cosmétiques,
or pour circuits électroniques).

La chaîne d'approvisionnement reliant les enfants mineurs de RDC, du Ghana ou de
l'Inde aux multinationales technologiques et de luxe est documentée mais les
mécanismes de due diligence contraignants restent insuffisants. L'impunité des
entreprises qui bénéficient de ces minéraux sans traçabilité adéquate perpétue
un système d'exploitation générationnelle.

Risk levels (travail dangereux enfants mines et impunité chaînes approvisionnement) :
  critique  -> composite >= 60  (exploitation enfants systémique — mines actives, impunité totale)
  élevé     -> composite >= 40  (travail dangereux actif — pression économique, absence école)
  modéré    -> composite >= 20  (plaidoyer certification — due diligence insuffisante)
  faible    -> composite < 20   (cadre normatif — conventions ILO, SDG 8.7)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class ChildLaborMiningRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    hazardous_child_mining_prevalence_score: float
    supply_chain_corporate_impunity_scale_score: float
    school_access_child_miner_exclusion_score: float
    legal_enforcement_child_labor_mining_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_child_labor_mining_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.hazardous_child_mining_prevalence_score * 0.30
            + self.supply_chain_corporate_impunity_scale_score * 0.25
            + self.school_access_child_miner_exclusion_score * 0.25
            + self.legal_enforcement_child_labor_mining_gap_score * 0.20,
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
        self.estimated_child_labor_mining_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "hazardous_child_mining_prevalence_score": self.hazardous_child_mining_prevalence_score,
            "supply_chain_corporate_impunity_scale_score": self.supply_chain_corporate_impunity_scale_score,
            "school_access_child_miner_exclusion_score": self.school_access_child_miner_exclusion_score,
            "legal_enforcement_child_labor_mining_gap_score": self.legal_enforcement_child_labor_mining_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_child_labor_mining_rights_index": self.estimated_child_labor_mining_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class ChildLaborMiningRightsEngineResult:
    agent: str = "Child Labor Mining Rights Engine Agent"
    domain: str = "child_labor_mining_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_child_labor_mining_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildLaborMiningRightsEntity] = field(default_factory=list)


def run_child_labor_mining_rights_engine() -> ChildLaborMiningRightsEngineResult:
    entities = [
        ChildLaborMiningRightsEntity(
            entity_id="CLM-001",
            name="RDC/Cobalt — 40 000 Enfants Mines Artisanales, Chaîne EV Batteries & Impunité Multinationales",
            country="RDC",
            sector="Mines Cobalt Artisanales",
            hazardous_child_mining_prevalence_score=97.0,
            supply_chain_corporate_impunity_scale_score=95.0,
            school_access_child_miner_exclusion_score=92.0,
            legal_enforcement_child_labor_mining_gap_score=93.0,
            primary_pattern="hazardous_child_mining_prevalence",
        ),
        ChildLaborMiningRightsEntity(
            entity_id="CLM-002",
            name="Ghana/Or Artisanal — Galamsey Enfants 8-14 Ans, Mercure & Zéro Scolarisation",
            country="Ghana",
            sector="Mines Or Galamsey",
            hazardous_child_mining_prevalence_score=94.0,
            supply_chain_corporate_impunity_scale_score=91.0,
            school_access_child_miner_exclusion_score=89.0,
            legal_enforcement_child_labor_mining_gap_score=90.0,
            primary_pattern="hazardous_child_mining_prevalence",
        ),
        ChildLaborMiningRightsEntity(
            entity_id="CLM-003",
            name="Inde/Mica — Mica Cosmétiques & Électronique, Enfants Jharkhand, Mines Clandestines",
            country="Inde",
            sector="Mines Mica Clandestines",
            hazardous_child_mining_prevalence_score=91.0,
            supply_chain_corporate_impunity_scale_score=88.0,
            school_access_child_miner_exclusion_score=86.0,
            legal_enforcement_child_labor_mining_gap_score=87.0,
            primary_pattern="supply_chain_corporate_impunity_scale",
        ),
        ChildLaborMiningRightsEntity(
            entity_id="CLM-004",
            name="Philippines/Or-Charbon — Tunnel Mining Enfants, Accidents Mortels & DENR Inefficace",
            country="Philippines",
            sector="Mines Tunnel Artisanales",
            hazardous_child_mining_prevalence_score=88.0,
            supply_chain_corporate_impunity_scale_score=85.0,
            school_access_child_miner_exclusion_score=83.0,
            legal_enforcement_child_labor_mining_gap_score=84.0,
            primary_pattern="hazardous_child_mining_prevalence",
        ),
        ChildLaborMiningRightsEntity(
            entity_id="CLM-005",
            name="Bolivie/Étain-Argent — Cerro Rico Enfants, Pression Économique Familiale & Syndicats Miniers",
            country="Bolivie",
            sector="Mines Cerro Rico",
            hazardous_child_mining_prevalence_score=57.0,
            supply_chain_corporate_impunity_scale_score=54.0,
            school_access_child_miner_exclusion_score=52.0,
            legal_enforcement_child_labor_mining_gap_score=53.0,
            primary_pattern="legal_enforcement_child_labor_mining_gap",
        ),
        ChildLaborMiningRightsEntity(
            entity_id="CLM-006",
            name="Mali/Or Artisanal — Conflit Armé & Mines, Enfants Recrutés & Zéro Protection",
            country="Mali",
            sector="Mines Or Zones Conflit",
            hazardous_child_mining_prevalence_score=55.0,
            supply_chain_corporate_impunity_scale_score=52.0,
            school_access_child_miner_exclusion_score=50.0,
            legal_enforcement_child_labor_mining_gap_score=51.0,
            primary_pattern="hazardous_child_mining_prevalence",
        ),
        ChildLaborMiningRightsEntity(
            entity_id="CLM-007",
            name="IPEC/Stop Child Labor — Programme ILO, Certification Minière Responsable & Due Diligence",
            country="Global",
            sector="Certification & Plaidoyer",
            hazardous_child_mining_prevalence_score=28.0,
            supply_chain_corporate_impunity_scale_score=25.0,
            school_access_child_miner_exclusion_score=26.0,
            legal_enforcement_child_labor_mining_gap_score=27.0,
            primary_pattern="supply_chain_corporate_impunity_scale",
        ),
        ChildLaborMiningRightsEntity(
            entity_id="CLM-008",
            name="ONU/ILO C182 — Convention Pires Formes Travail Enfants, SDG 8.7 & Accord Volontaire",
            country="Global",
            sector="Cadre Normatif International",
            hazardous_child_mining_prevalence_score=5.0,
            supply_chain_corporate_impunity_scale_score=4.0,
            school_access_child_miner_exclusion_score=4.0,
            legal_enforcement_child_labor_mining_gap_score=3.0,
            primary_pattern="legal_enforcement_child_labor_mining_gap",
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

    return ChildLaborMiningRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_labor_mining_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_cobalt_child_labor_drc_mining_report",
            "ilo_ipec_child_labour_mining_hazardous_work_global_report",
            "somo_centre_research_multinationals_child_labor_minerals_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_child_labor_mining_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_child_labor_mining_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
