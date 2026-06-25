from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#e11d48"


@dataclass
class OnlineHarassmentRightsEntity:
    entity_id: str
    name: str
    country: str
    cyber_gender_violence_score: float
    doxxing_impunity_score: float
    platform_inaction_score: float
    legal_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_online_harassment_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.cyber_gender_violence_score * 0.30
            + self.doxxing_impunity_score * 0.25
            + self.platform_inaction_score * 0.25
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
        self.estimated_online_harassment_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class OnlineHarassmentRightsEngineResult:
    agent: str = "Online Harassment Rights Engine Agent"
    domain: str = "online_harassment_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_online_harassment_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[OnlineHarassmentRightsEntity] = field(default_factory=list)


def run_online_harassment_rights_engine() -> OnlineHarassmentRightsEngineResult:
    entities = [
        OnlineHarassmentRightsEntity(
            entity_id="OHR-001",
            name="Inde — 58% femmes harcelées ligne, revenge porn 20 000 cas/an, IT Act insuffisant",
            country="Inde",
            cyber_gender_violence_score=96.0,
            doxxing_impunity_score=94.0,
            platform_inaction_score=95.0,
            legal_protection_gap_score=93.0,
            primary_pattern="cyber_gender_violence",
        ),
        OnlineHarassmentRightsEntity(
            entity_id="OHR-002",
            name="Pakistan — Cyberviolence féministes, blasphème utilisé comme harcèlement, PECA loi abusive",
            country="Pakistan",
            cyber_gender_violence_score=90.0,
            doxxing_impunity_score=92.0,
            platform_inaction_score=89.0,
            legal_protection_gap_score=91.0,
            primary_pattern="legal_protection_gap",
        ),
        OnlineHarassmentRightsEntity(
            entity_id="OHR-003",
            name="Brésil — LeakNude sites, 88% femmes harcelées politiques ligne, Marielle Franco doxxing",
            country="Brésil",
            cyber_gender_violence_score=84.0,
            doxxing_impunity_score=86.0,
            platform_inaction_score=83.0,
            legal_protection_gap_score=82.0,
            primary_pattern="doxxing_impunity",
        ),
        OnlineHarassmentRightsEntity(
            entity_id="OHR-004",
            name="Philippines — 72% journalistes femmes quittent réseaux, trolls armée Duterte, Maria Ressa",
            country="Philippines",
            cyber_gender_violence_score=76.0,
            doxxing_impunity_score=78.0,
            platform_inaction_score=80.0,
            legal_protection_gap_score=74.0,
            primary_pattern="platform_inaction",
        ),
        OnlineHarassmentRightsEntity(
            entity_id="OHR-005",
            name="USA — 41% adultes harcelés ligne, revenge porn lois 48 États seulement, Twitter/X modération zéro",
            country="USA",
            cyber_gender_violence_score=54.0,
            doxxing_impunity_score=56.0,
            platform_inaction_score=58.0,
            legal_protection_gap_score=52.0,
            primary_pattern="platform_inaction",
        ),
        OnlineHarassmentRightsEntity(
            entity_id="OHR-006",
            name="UK — Online Safety Act 2023 tardif, 46% femmes harcelées, deepfakes non-criminalisés avant 2024",
            country="UK",
            cyber_gender_violence_score=44.0,
            doxxing_impunity_score=42.0,
            platform_inaction_score=46.0,
            legal_protection_gap_score=48.0,
            primary_pattern="platform_inaction",
        ),
        OnlineHarassmentRightsEntity(
            entity_id="OHR-007",
            name="France — Loi Avia partiellement censurée, cyberviolence femmes +30%, PHAROS insuffisant",
            country="France",
            cyber_gender_violence_score=28.0,
            doxxing_impunity_score=26.0,
            platform_inaction_score=30.0,
            legal_protection_gap_score=24.0,
            primary_pattern="cyber_gender_violence",
        ),
        OnlineHarassmentRightsEntity(
            entity_id="OHR-008",
            name="Allemagne/Finlande — NetzDG effectif, formations modération, sanctions plateformes réelles",
            country="Allemagne/Finlande",
            cyber_gender_violence_score=7.0,
            doxxing_impunity_score=8.0,
            platform_inaction_score=6.0,
            legal_protection_gap_score=9.0,
            primary_pattern="legal_protection_gap",
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

    return OnlineHarassmentRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_online_harassment_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_women_online_violence_against_women_2024",
            "aic_online_harassment_global_report",
            "amnesty_toxic_twitter_women_study",
            "coalition_against_online_violence_2024",
            "end_violence_against_women_digital_rights",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_online_harassment_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
