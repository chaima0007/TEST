from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RefugeeDetentionEntity:
    entity_id: str
    name: str
    country: str
    arbitrary_detention_scale_score: float
    inhumane_conditions_score: float
    legal_access_denial_score: float
    pushback_refoulement_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_refugee_detention_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.arbitrary_detention_scale_score * 0.30
            + self.inhumane_conditions_score * 0.25
            + self.legal_access_denial_score * 0.25
            + self.pushback_refoulement_score * 0.20,
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
        self.estimated_refugee_detention_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RefugeeDetentionEngineResult:
    agent: str = "Refugee Detention Engine Agent"
    domain: str = "refugee_detention"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_refugee_detention_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RefugeeDetentionEntity] = field(default_factory=list)

def run_refugee_detention_engine() -> RefugeeDetentionEngineResult:
    entities = [
        RefugeeDetentionEntity(
            entity_id="RD-001",
            name="Libye — Centres Détention Milices, Tortures/Viols Documentés & Financement UE Complicité",
            country="Afrique du Nord",
            arbitrary_detention_scale_score=95.0,
            inhumane_conditions_score=95.0,
            legal_access_denial_score=92.0,
            pushback_refoulement_score=90.0,
            primary_pattern="inhumane_conditions",
        ),
        RefugeeDetentionEntity(
            entity_id="RD-002",
            name="Australie/Nauru — Offshore Detention, Manus Island Fermé/Remplacé & Limbes Juridiques",
            country="Océanie",
            arbitrary_detention_scale_score=88.0,
            inhumane_conditions_score=85.0,
            legal_access_denial_score=90.0,
            pushback_refoulement_score=88.0,
            primary_pattern="legal_access_denial",
        ),
        RefugeeDetentionEntity(
            entity_id="RD-003",
            name="USA/Immigration — Centres ICE Privés, Décès en Détention & Séparation Familles Frontière",
            country="Amérique du Nord",
            arbitrary_detention_scale_score=85.0,
            inhumane_conditions_score=82.0,
            legal_access_denial_score=80.0,
            pushback_refoulement_score=85.0,
            primary_pattern="arbitrary_detention_scale",
        ),
        RefugeeDetentionEntity(
            entity_id="RD-004",
            name="Grèce/Turquie — Pushbacks Illégaux Égée, Camps Surpeuplés & Violations Art.33 Convention",
            country="Europe",
            arbitrary_detention_scale_score=80.0,
            inhumane_conditions_score=82.0,
            legal_access_denial_score=78.0,
            pushback_refoulement_score=85.0,
            primary_pattern="pushback_refoulement",
        ),
        RefugeeDetentionEntity(
            entity_id="RD-005",
            name="Bangladesh/Rohingyas — Cox's Bazar 1M Réfugiés, Restriction Liberté & Retour Forcé Myanmar",
            country="Asie du Sud",
            arbitrary_detention_scale_score=52.0,
            inhumane_conditions_score=55.0,
            legal_access_denial_score=58.0,
            pushback_refoulement_score=52.0,
            primary_pattern="pushback_refoulement",
        ),
        RefugeeDetentionEntity(
            entity_id="RD-006",
            name="UE/Rwanda Plan — Externalisation Asile, Accord UK-Rwanda & Détention Expéditive",
            country="Europe",
            arbitrary_detention_scale_score=48.0,
            inhumane_conditions_score=45.0,
            legal_access_denial_score=55.0,
            pushback_refoulement_score=52.0,
            primary_pattern="legal_access_denial",
        ),
        RefugeeDetentionEntity(
            entity_id="RD-007",
            name="UNHCR/ECRE — Plaidoyer Anti-Détention, Alternatives & Standards Minima Protection",
            country="Global",
            arbitrary_detention_scale_score=22.0,
            inhumane_conditions_score=25.0,
            legal_access_denial_score=28.0,
            pushback_refoulement_score=30.0,
            primary_pattern="arbitrary_detention_scale",
        ),
        RefugeeDetentionEntity(
            entity_id="RD-008",
            name="ONU/Convention 1951 — Statut Réfugiés, Protocole 1967 & Principe Non-Refoulement",
            country="Global",
            arbitrary_detention_scale_score=4.0,
            inhumane_conditions_score=5.0,
            legal_access_denial_score=3.0,
            pushback_refoulement_score=6.0,
            primary_pattern="pushback_refoulement",
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

    return RefugeeDetentionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_refugee_detention_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_detention_project_immigration_detention_global_report",
            "unhcr_global_trends_forced_displacement_annual_report",
            "human_rights_watch_refugee_detention_conditions_global_audit",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_refugee_detention_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_refugee_detention_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
