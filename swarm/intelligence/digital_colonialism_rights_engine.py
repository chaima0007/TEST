from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

DOMAIN = "digital_colonialism_rights"
PREFIX = "DCR"
ACCENT_COLOR = "#1a0a2e"

@dataclass
class DigitalColonialismRightsEntity:
    entity_id: str
    name: str
    country: str
    data_sovereignty_violation_score: float
    platform_monopoly_score: float
    algorithmic_exploitation_score: float
    digital_divide_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_digital_colonialism_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.data_sovereignty_violation_score * 0.30
            + self.platform_monopoly_score * 0.25
            + self.algorithmic_exploitation_score * 0.25
            + self.digital_divide_score * 0.20,
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
        self.estimated_digital_colonialism_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class DigitalColonialismRightsEngineResult:
    agent: str = "Digital Colonialism Rights Engine Agent"
    domain: str = "digital_colonialism_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_digital_colonialism_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalColonialismRightsEntity] = field(default_factory=list)

def run_digital_colonialism_rights_engine() -> DigitalColonialismRightsEngineResult:
    entities = [
        DigitalColonialismRightsEntity(
            entity_id="DCR-001",
            name="Facebook/Meta — Extraction Données Pays du Sud, Surveillance Comportementale & Désinformation Ciblée",
            country="Global Sud",
            data_sovereignty_violation_score=92.0,
            platform_monopoly_score=88.0,
            algorithmic_exploitation_score=90.0,
            digital_divide_score=78.0,
            primary_pattern="data_sovereignty_violation",
        ),
        DigitalColonialismRightsEntity(
            entity_id="DCR-002",
            name="Google — Monopole IA Global, Aspiration Données Africaines & Indexation Asymétrique Nord-Sud",
            country="Global",
            data_sovereignty_violation_score=88.0,
            platform_monopoly_score=92.0,
            algorithmic_exploitation_score=85.0,
            digital_divide_score=82.0,
            primary_pattern="platform_monopoly",
        ),
        DigitalColonialismRightsEntity(
            entity_id="DCR-003",
            name="Amazon AWS — Infrastructure Coloniale Numérique, Dépendance Cloud États Africains & Lock-in Souveraineté",
            country="Global",
            data_sovereignty_violation_score=85.0,
            platform_monopoly_score=88.0,
            algorithmic_exploitation_score=82.0,
            digital_divide_score=80.0,
            primary_pattern="platform_monopoly",
        ),
        DigitalColonialismRightsEntity(
            entity_id="DCR-004",
            name="Microsoft Azure — Lock-in États Africains, Souveraineté Numérique Compromise & Monopole SaaS Gouvernemental",
            country="Afrique/Global",
            data_sovereignty_violation_score=82.0,
            platform_monopoly_score=85.0,
            algorithmic_exploitation_score=80.0,
            digital_divide_score=78.0,
            primary_pattern="platform_monopoly",
        ),
        DigitalColonialismRightsEntity(
            entity_id="DCR-005",
            name="Alibaba — Expansion Numérique Asie/Afrique, Surveillance Commerce & Dépendance Infrastructure Technologique",
            country="Asie/Afrique",
            data_sovereignty_violation_score=62.0,
            platform_monopoly_score=58.0,
            algorithmic_exploitation_score=55.0,
            digital_divide_score=52.0,
            primary_pattern="algorithmic_exploitation",
        ),
        DigitalColonialismRightsEntity(
            entity_id="DCR-006",
            name="Huawei — Infrastructure 5G Captive, Accès Backdoor Potentiel & Dépendance Technologique Pays en Développement",
            country="Afrique/Asie",
            data_sovereignty_violation_score=58.0,
            platform_monopoly_score=55.0,
            algorithmic_exploitation_score=52.0,
            digital_divide_score=48.0,
            primary_pattern="data_sovereignty_violation",
        ),
        DigitalColonialismRightsEntity(
            entity_id="DCR-007",
            name="EU Digital Markets Act — Régulation Partielle Gatekeepers, DMA 2023 & Limites Protection Pays Tiers",
            country="Europe",
            data_sovereignty_violation_score=32.0,
            platform_monopoly_score=35.0,
            algorithmic_exploitation_score=28.0,
            digital_divide_score=30.0,
            primary_pattern="platform_monopoly",
        ),
        DigitalColonialismRightsEntity(
            entity_id="DCR-008",
            name="Fairdata Initiative — Souveraineté Numérique Communautaire, Open Source & Données Locales Contrôlées",
            country="Global",
            data_sovereignty_violation_score=5.0,
            platform_monopoly_score=7.0,
            algorithmic_exploitation_score=6.0,
            digital_divide_score=8.0,
            primary_pattern="digital_divide",
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

    return DigitalColonialismRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_digital_colonialism_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "algorithmic_colonialism_digital_rights_report_2025",
            "data_sovereignty_global_south_decolonization_study",
            "platform_monopoly_africa_digital_infrastructure_audit",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_digital_colonialism_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_digital_colonialism_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
