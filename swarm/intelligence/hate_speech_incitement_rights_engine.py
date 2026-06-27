from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#ef4444"


@dataclass
class HateSpeechIncitementRightsEntity:
    entity_id: str
    name: str
    country: str
    state_sponsored_hate_score: float
    online_incitement_impunity_score: float
    minority_targeting_score: float
    legal_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_hate_speech_incitement_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.state_sponsored_hate_score * 0.30
            + self.online_incitement_impunity_score * 0.25
            + self.minority_targeting_score * 0.25
            + self.legal_protection_gap_score * 0.20,
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
        self.estimated_hate_speech_incitement_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class HateSpeechIncitementRightsEngineResult:
    agent: str = "Hate Speech Incitement Rights Engine Agent"
    domain: str = "hate_speech_incitement_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_hate_speech_incitement_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HateSpeechIncitementRightsEntity] = field(default_factory=list)


def run_hate_speech_incitement_rights_engine() -> HateSpeechIncitementRightsEngineResult:
    entities = [
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-001",
            name="Myanmar — Discours Haine Anti-Rohingya, ONU Génocide Intentionnel Documenté, Facebook Vecteur Principal",
            country="Myanmar",
            state_sponsored_hate_score=93.0,
            online_incitement_impunity_score=91.0,
            minority_targeting_score=95.0,
            legal_protection_gap_score=92.0,
            primary_pattern="minority_targeting_score",
        ),
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-002",
            name="Inde — Discours Haine Anti-Musulman Organisé BJP/RSS, Lynchages Mob Documentés, Impunité Institutionnelle",
            country="Inde",
            state_sponsored_hate_score=86.0,
            online_incitement_impunity_score=84.0,
            minority_targeting_score=88.0,
            legal_protection_gap_score=83.0,
            primary_pattern="minority_targeting_score",
        ),
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-003",
            name="Russie — Propagande Haineuse LGBT, Agents Étrangers, Incitation Documentée, Cadre Légal Anti-Minorités",
            country="Russie",
            state_sponsored_hate_score=89.0,
            online_incitement_impunity_score=82.0,
            minority_targeting_score=84.0,
            legal_protection_gap_score=87.0,
            primary_pattern="state_sponsored_hate_score",
        ),
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-004",
            name="Éthiopie — Médias Ethniques Incitation Génocide Tigré/Amhara, Modèle Radio Rwanda 2.0, Impunité Totale",
            country="Éthiopie",
            state_sponsored_hate_score=82.0,
            online_incitement_impunity_score=80.0,
            minority_targeting_score=85.0,
            legal_protection_gap_score=80.0,
            primary_pattern="minority_targeting_score",
        ),
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-005",
            name="Brésil — Bolsonarisme, Discours Haine LGBTQ et Autochtones, Impunité Digitale Documentée",
            country="Brésil",
            state_sponsored_hate_score=52.0,
            online_incitement_impunity_score=55.0,
            minority_targeting_score=53.0,
            legal_protection_gap_score=50.0,
            primary_pattern="online_incitement_impunity_score",
        ),
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-006",
            name="Pakistan — Blasphème Instrumentalisé, Minorités Chrétiennes et Hindoues Ciblées, Incitation Religieuse Systémique",
            country="Pakistan",
            state_sponsored_hate_score=48.0,
            online_incitement_impunity_score=50.0,
            minority_targeting_score=55.0,
            legal_protection_gap_score=52.0,
            primary_pattern="minority_targeting_score",
        ),
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-007",
            name="France — Montée Extrême Droite, Discours Haine Anti-Immigration, Lacunes Réglementation Plateformes",
            country="France",
            state_sponsored_hate_score=28.0,
            online_incitement_impunity_score=32.0,
            minority_targeting_score=30.0,
            legal_protection_gap_score=27.0,
            primary_pattern="online_incitement_impunity_score",
        ),
        HateSpeechIncitementRightsEntity(
            entity_id="HSR-008",
            name="Allemagne — NetzDG Loi Contre Discours Haine en Ligne, Meilleure Pratique UE, Sanctions Plateformes Effectives",
            country="Allemagne",
            state_sponsored_hate_score=9.0,
            online_incitement_impunity_score=10.0,
            minority_targeting_score=8.0,
            legal_protection_gap_score=9.0,
            primary_pattern="online_incitement_impunity_score",
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

    return HateSpeechIncitementRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_hate_speech_incitement_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_rabat_plan_action_hate_speech_2012",
            "article19_hate_speech_global_monitor",
            "hrw_online_hate_speech_minority_targeting",
            "ohchr_minority_rights_hate_speech_report",
            "eu_code_conduct_countering_hate_speech_evaluation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_hate_speech_incitement_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
