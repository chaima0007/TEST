from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AlbinismRightsEntity:
    entity_id: str
    name: str
    country: str
    ritual_killing_body_parts_trade_score: float
    legal_protection_enforcement_gap_score: float
    discrimination_exclusion_severity_score: float
    institutional_abandonment_scale_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_albinism_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.ritual_killing_body_parts_trade_score * 0.30
            + self.legal_protection_enforcement_gap_score * 0.25
            + self.discrimination_exclusion_severity_score * 0.25
            + self.institutional_abandonment_scale_score * 0.20,
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
        self.estimated_albinism_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class AlbinismRightsEngineResult:
    agent: str = "Albinism Rights Engine Agent"
    domain: str = "albinism_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_albinism_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AlbinismRightsEntity] = field(default_factory=list)

def run_albinism_rights_engine() -> AlbinismRightsEngineResult:
    entities = [
        AlbinismRightsEntity(
            entity_id="AL-001",
            name="Tanzanie — 100+ Meurtres Rituels Depuis 2000, Membres Prélevés Vivants & Marché Noir Organes",
            country="Afrique de l'Est",
            ritual_killing_body_parts_trade_score=95.0,
            legal_protection_enforcement_gap_score=92.0,
            discrimination_exclusion_severity_score=92.0,
            institutional_abandonment_scale_score=92.0,
            primary_pattern="ritual_killing_body_parts_trade",
        ),
        AlbinismRightsEntity(
            entity_id="AL-002",
            name="Mozambique — Vague Meurtres 2016-2021, Démembrement Rituels & Réponse Gouvernementale Tardive",
            country="Afrique de l'Est",
            ritual_killing_body_parts_trade_score=90.0,
            legal_protection_enforcement_gap_score=90.0,
            discrimination_exclusion_severity_score=88.0,
            institutional_abandonment_scale_score=88.0,
            primary_pattern="ritual_killing_body_parts_trade",
        ),
        AlbinismRightsEntity(
            entity_id="AL-003",
            name="Malawi — Urgence Présidentielle 2017, 70+ Attaques/Disparitions & Impunité Persistante",
            country="Afrique de l'Est",
            ritual_killing_body_parts_trade_score=88.0,
            legal_protection_enforcement_gap_score=88.0,
            discrimination_exclusion_severity_score=88.0,
            institutional_abandonment_scale_score=88.0,
            primary_pattern="legal_protection_enforcement_gap",
        ),
        AlbinismRightsEntity(
            entity_id="AL-004",
            name="Zimbabwe — Exclusion Emploi/Mariage, Soins Dermatologiques Absents & Préjugé Fantômes",
            country="Afrique Australe",
            ritual_killing_body_parts_trade_score=82.0,
            legal_protection_enforcement_gap_score=85.0,
            discrimination_exclusion_severity_score=88.0,
            institutional_abandonment_scale_score=88.0,
            primary_pattern="discrimination_exclusion_severity",
        ),
        AlbinismRightsEntity(
            entity_id="AL-005",
            name="Nigéria/Afrique Ouest — Exclusion Scolaire, Mariage Refusé, Cancer Peau Non Traité & Stigmate",
            country="Afrique de l'Ouest",
            ritual_killing_body_parts_trade_score=50.0,
            legal_protection_enforcement_gap_score=55.0,
            discrimination_exclusion_severity_score=55.0,
            institutional_abandonment_scale_score=52.0,
            primary_pattern="discrimination_exclusion_severity",
        ),
        AlbinismRightsEntity(
            entity_id="AL-006",
            name="Burundi/Rwanda — Enfants Albinos Cachés par Familles, Abandon Scolaire & Isolement Communautaire",
            country="Afrique Centrale",
            ritual_killing_body_parts_trade_score=48.0,
            legal_protection_enforcement_gap_score=50.0,
            discrimination_exclusion_severity_score=52.0,
            institutional_abandonment_scale_score=52.0,
            primary_pattern="institutional_abandonment_scale",
        ),
        AlbinismRightsEntity(
            entity_id="AL-007",
            name="Under the Same Sun/UTSS — Base Données Meurtres Globale, Advocacy ONU & Kits Protection Solaire",
            country="Global",
            ritual_killing_body_parts_trade_score=22.0,
            legal_protection_enforcement_gap_score=28.0,
            discrimination_exclusion_severity_score=25.0,
            institutional_abandonment_scale_score=30.0,
            primary_pattern="institutional_abandonment_scale",
        ),
        AlbinismRightsEntity(
            entity_id="AL-008",
            name="ONU/OHCHR — Résolution 2015 Albinisme, Rapporteur Indépendant Ikponwosa Ero & CRPD Art.8",
            country="Global",
            ritual_killing_body_parts_trade_score=4.0,
            legal_protection_enforcement_gap_score=5.0,
            discrimination_exclusion_severity_score=3.0,
            institutional_abandonment_scale_score=6.0,
            primary_pattern="legal_protection_enforcement_gap",
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

    return AlbinismRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_albinism_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_ohchr_independent_expert_albinism_ikponwosa_ero_report",
            "under_the_same_sun_albinism_killings_database_africa",
            "amnesty_international_end_attacks_persons_albinism_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_albinism_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_albinism_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
