from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MigrantDetentionEntity:
    entity_id: str
    name: str
    country: str
    detention_conditions_score: float
    indefinite_detention_scale_score: float
    deportation_refoulement_risk_score: float
    legal_aid_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_migrant_detention_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.detention_conditions_score * 0.30
            + self.indefinite_detention_scale_score * 0.25
            + self.deportation_refoulement_risk_score * 0.25
            + self.legal_aid_denial_score * 0.20,
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
        self.estimated_migrant_detention_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class MigrantDetentionEngineResult:
    agent: str = "Migrant Detention Engine Agent"
    domain: str = "migrant_detention"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_migrant_detention_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MigrantDetentionEntity] = field(default_factory=list)

def run_migrant_detention_engine() -> MigrantDetentionEngineResult:
    entities = [
        MigrantDetentionEntity(
            entity_id="MD-001",
            name="Australie — Offshore Detention Manus/Nauru, Détention Indéfinie & Refoulement Systématique",
            country="Océanie",
            detention_conditions_score=88.0,
            indefinite_detention_scale_score=92.0,
            deportation_refoulement_risk_score=90.0,
            legal_aid_denial_score=85.0,
            primary_pattern="indefinite_detention_scale",
        ),
        MigrantDetentionEntity(
            entity_id="MD-002",
            name="USA/ICE — Centres Détention Privés, Séparation Familles & Conditions Inhumaines Frontière",
            country="Amérique du Nord",
            detention_conditions_score=85.0,
            indefinite_detention_scale_score=88.0,
            deportation_refoulement_risk_score=85.0,
            legal_aid_denial_score=82.0,
            primary_pattern="detention_conditions",
        ),
        MigrantDetentionEntity(
            entity_id="MD-003",
            name="UE/Libye — Externalisation Migration, Garde-Côtes Libyens & Centres Détention Tortures",
            country="Afrique du Nord/Europe",
            detention_conditions_score=82.0,
            indefinite_detention_scale_score=85.0,
            deportation_refoulement_risk_score=88.0,
            legal_aid_denial_score=80.0,
            primary_pattern="deportation_refoulement_risk",
        ),
        MigrantDetentionEntity(
            entity_id="MD-004",
            name="Mexique — INM Centres Détention, Violence Gardes & Complicité Trafiquants",
            country="Amérique Centrale",
            detention_conditions_score=78.0,
            indefinite_detention_scale_score=80.0,
            deportation_refoulement_risk_score=82.0,
            legal_aid_denial_score=75.0,
            primary_pattern="deportation_refoulement_risk",
        ),
        MigrantDetentionEntity(
            entity_id="MD-005",
            name="Turquie — 3,5M Réfugiés Syriens, Refoulements Frontière & Centres Surpeuplés",
            country="Europe de l'Est",
            detention_conditions_score=52.0,
            indefinite_detention_scale_score=55.0,
            deportation_refoulement_risk_score=58.0,
            legal_aid_denial_score=50.0,
            primary_pattern="deportation_refoulement_risk",
        ),
        MigrantDetentionEntity(
            entity_id="MD-006",
            name="Maroc/Algérie — Expulsions Massives Subsahariens, Violence & Absence Recours Légaux",
            country="Afrique du Nord",
            detention_conditions_score=48.0,
            indefinite_detention_scale_score=52.0,
            deportation_refoulement_risk_score=55.0,
            legal_aid_denial_score=50.0,
            primary_pattern="legal_aid_denial",
        ),
        MigrantDetentionEntity(
            entity_id="MD-007",
            name="Canada — Détention Arbitraire Limitée, Alternatives Détention & Réforme Partielle",
            country="Amérique du Nord",
            detention_conditions_score=22.0,
            indefinite_detention_scale_score=28.0,
            deportation_refoulement_risk_score=30.0,
            legal_aid_denial_score=25.0,
            primary_pattern="detention_conditions",
        ),
        MigrantDetentionEntity(
            entity_id="MD-008",
            name="HCR/ONU — Principes Directeurs Détention, Règles Mandela & Alternatives à la Détention",
            country="Global",
            detention_conditions_score=4.0,
            indefinite_detention_scale_score=5.0,
            deportation_refoulement_risk_score=3.0,
            legal_aid_denial_score=6.0,
            primary_pattern="legal_aid_denial",
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

    return MigrantDetentionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_migrant_detention_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_detention_project_immigration_detention_global_report",
            "human_rights_watch_immigration_enforcement_detention_report_annual",
            "unhcr_detention_guidelines_asylum_seekers_stateless_persons",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_migrant_detention_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_migrant_detention_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
