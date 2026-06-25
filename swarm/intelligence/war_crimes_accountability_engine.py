from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WarCrimesAccountabilityEntity:
    entity_id: str
    name: str
    country: str
    war_crimes_scale_civilian_harm_score: float
    chemical_biological_weapons_use_score: float
    accountability_icc_prosecution_gap_score: float
    humanitarian_law_violations_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_war_crimes_accountability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.war_crimes_scale_civilian_harm_score * 0.30
            + self.chemical_biological_weapons_use_score * 0.25
            + self.accountability_icc_prosecution_gap_score * 0.25
            + self.humanitarian_law_violations_impunity_score * 0.20,
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
        self.estimated_war_crimes_accountability_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class WarCrimesAccountabilityEngineResult:
    agent: str = "War Crimes Accountability Engine Agent"
    domain: str = "war_crimes_accountability"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.89
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_war_crimes_accountability_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WarCrimesAccountabilityEntity] = field(default_factory=list)


def run_war_crimes_accountability_engine() -> WarCrimesAccountabilityEngineResult:
    entities = [
        WarCrimesAccountabilityEntity(
            entity_id="WCA-001",
            name="Syrie — 500K+ Morts, Armes Chimiques Impunies, 600+ Hôpitaux Bombardés, Veto Russie/Chine CPI & Aucun Jugement",
            country="Syrie",
            war_crimes_scale_civilian_harm_score=97.0,
            chemical_biological_weapons_use_score=96.0,
            accountability_icc_prosecution_gap_score=95.0,
            humanitarian_law_violations_impunity_score=96.0,
            primary_pattern="chemical_biological_weapons_use",
        ),
        WarCrimesAccountabilityEntity(
            entity_id="WCA-002",
            name="Russie/Ukraine — Bucha Massacres Documentés, Bombes Sous-Munitions Civils, Centrales Nucléaires Ciblées & CPI Mandat Poutine Non-Exécuté",
            country="Russie/Ukraine",
            war_crimes_scale_civilian_harm_score=93.0,
            chemical_biological_weapons_use_score=82.0,
            accountability_icc_prosecution_gap_score=90.0,
            humanitarian_law_violations_impunity_score=91.0,
            primary_pattern="accountability_icc_prosecution_gap",
        ),
        WarCrimesAccountabilityEntity(
            entity_id="WCA-003",
            name="Yémen/Coalition — Frappes Marchés/Hôpitaux/Mariages ONU Documentées, Armes US/UK Utilisées & Panel ONU Bloqué 2023",
            country="Yémen",
            war_crimes_scale_civilian_harm_score=90.0,
            chemical_biological_weapons_use_score=72.0,
            accountability_icc_prosecution_gap_score=89.0,
            humanitarian_law_violations_impunity_score=92.0,
            primary_pattern="humanitarian_law_violations_impunity",
        ),
        WarCrimesAccountabilityEntity(
            entity_id="WCA-004",
            name="Israël/Gaza — 35K+ Morts Civils 2023-2024, CIJ Génocide Plausible, Blocus Humanitaire & 100+ Journalistes Tués",
            country="Israël/Gaza",
            war_crimes_scale_civilian_harm_score=91.0,
            chemical_biological_weapons_use_score=75.0,
            accountability_icc_prosecution_gap_score=88.0,
            humanitarian_law_violations_impunity_score=90.0,
            primary_pattern="war_crimes_scale_civilian_harm",
        ),
        WarCrimesAccountabilityEntity(
            entity_id="WCA-005",
            name="Myanmar — Crimes Contre Rohingya Génocide CIJ, Junta Bombes Villages Karen/Chin & Armes Importées Malgré Embargo",
            country="Myanmar",
            war_crimes_scale_civilian_harm_score=58.0,
            chemical_biological_weapons_use_score=50.0,
            accountability_icc_prosecution_gap_score=62.0,
            humanitarian_law_violations_impunity_score=60.0,
            primary_pattern="accountability_icc_prosecution_gap",
        ),
        WarCrimesAccountabilityEntity(
            entity_id="WCA-006",
            name="Éthiopie — Tigré Blocus Alimentaire Crime de Guerre, Viols Systématiques Arme Guerre & Impunité Totale Commandants",
            country="Éthiopie",
            war_crimes_scale_civilian_harm_score=55.0,
            chemical_biological_weapons_use_score=40.0,
            accountability_icc_prosecution_gap_score=58.0,
            humanitarian_law_violations_impunity_score=62.0,
            primary_pattern="humanitarian_law_violations_impunity",
        ),
        WarCrimesAccountabilityEntity(
            entity_id="WCA-007",
            name="Colombie — FARC/Para Crimes Passés, JEP Réconciliation en Progrès & 30 Ans Conflit Quelques Jugements",
            country="Colombie",
            war_crimes_scale_civilian_harm_score=30.0,
            chemical_biological_weapons_use_score=22.0,
            accountability_icc_prosecution_gap_score=28.0,
            humanitarian_law_violations_impunity_score=25.0,
            primary_pattern="war_crimes_scale_civilian_harm",
        ),
        WarCrimesAccountabilityEntity(
            entity_id="WCA-008",
            name="Pays-Bas/CPI — Siège CPI La Haye, Jurisprudence Crimes Guerre, Contribution Financière Majeure & Pas en Conflit",
            country="Pays-Bas",
            war_crimes_scale_civilian_harm_score=5.0,
            chemical_biological_weapons_use_score=3.0,
            accountability_icc_prosecution_gap_score=8.0,
            humanitarian_law_violations_impunity_score=4.0,
            primary_pattern="accountability_icc_prosecution_gap",
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

    return WarCrimesAccountabilityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_war_crimes_accountability_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "icc_annual_report_situations_2023",
            "un_commission_inquiry_war_crimes_2023",
            "human_rights_watch_ihl_violations_2023",
            "icrc_international_humanitarian_law_report_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_war_crimes_accountability_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_war_crimes_accountability_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
