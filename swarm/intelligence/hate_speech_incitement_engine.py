from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HateSpeechIncitementEntity:
    entity_id: str
    name: str
    country: str
    incitement_violence_scale_score: float
    platform_amplification_failure_score: float
    legal_accountability_gap_score: float
    minority_targeting_pattern_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_hate_speech_incitement_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.incitement_violence_scale_score * 0.30
            + self.platform_amplification_failure_score * 0.25
            + self.legal_accountability_gap_score * 0.25
            + self.minority_targeting_pattern_score * 0.20,
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
        self.estimated_hate_speech_incitement_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class HateSpeechIncitementEngineResult:
    agent: str = "Hate Speech Incitement Engine Agent"
    domain: str = "hate_speech_incitement"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_hate_speech_incitement_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HateSpeechIncitementEntity] = field(default_factory=list)

def run_hate_speech_incitement_engine() -> HateSpeechIncitementEngineResult:
    entities = [
        HateSpeechIncitementEntity(
            entity_id="HS-001",
            name="Myanmar/Facebook — Rohingya Génocide 2017, Aveu Zuckerberg Échec Modération & 700K Déplacés",
            country="Asie du Sud-Est",
            incitement_violence_scale_score=95.0,
            platform_amplification_failure_score=95.0,
            legal_accountability_gap_score=92.0,
            minority_targeting_pattern_score=90.0,
            primary_pattern="incitement_violence_scale",
        ),
        HateSpeechIncitementEntity(
            entity_id="HS-002",
            name="Éthiopie/Tigray — Facebook Discours Ethnique Meurtriers, 500K Morts & Appels Génocide Tigréens",
            country="Afrique de l'Est",
            incitement_violence_scale_score=92.0,
            platform_amplification_failure_score=90.0,
            legal_accountability_gap_score=88.0,
            minority_targeting_pattern_score=92.0,
            primary_pattern="minority_targeting_pattern",
        ),
        HateSpeechIncitementEntity(
            entity_id="HS-003",
            name="Inde/BJP — Comptes Vérifiés Twitter Discours Anti-Musulmans, Incitation Pogroms & Silence X",
            country="Asie du Sud",
            incitement_violence_scale_score=88.0,
            platform_amplification_failure_score=90.0,
            legal_accountability_gap_score=88.0,
            minority_targeting_pattern_score=88.0,
            primary_pattern="platform_amplification_failure",
        ),
        HateSpeechIncitementEntity(
            entity_id="HS-004",
            name="USA/Jan.6 — Incitation Trump Capitol, Plateformes Tardives & Musk Réintègre Comptes Haineux",
            country="Amérique du Nord",
            incitement_violence_scale_score=85.0,
            platform_amplification_failure_score=88.0,
            legal_accountability_gap_score=85.0,
            minority_targeting_pattern_score=88.0,
            primary_pattern="platform_amplification_failure",
        ),
        HateSpeechIncitementEntity(
            entity_id="HS-005",
            name="UE/DSA — Règlement Services Numériques 2024, Sanctions Meta & Enforcement Lacunaire",
            country="Europe",
            incitement_violence_scale_score=52.0,
            platform_amplification_failure_score=58.0,
            legal_accountability_gap_score=55.0,
            minority_targeting_pattern_score=50.0,
            primary_pattern="legal_accountability_gap",
        ),
        HateSpeechIncitementEntity(
            entity_id="HS-006",
            name="Russie/RT — Propagande État Déshumanisation Ukraine, Discours Guerre Génocidaire & Bans Tardifs",
            country="Europe de l'Est",
            incitement_violence_scale_score=48.0,
            platform_amplification_failure_score=55.0,
            legal_accountability_gap_score=50.0,
            minority_targeting_pattern_score=50.0,
            primary_pattern="platform_amplification_failure",
        ),
        HateSpeechIncitementEntity(
            entity_id="HS-007",
            name="Global Network Initiative/Access Now — Standards Modération & Droits Humains Ligne",
            country="Global",
            incitement_violence_scale_score=22.0,
            platform_amplification_failure_score=25.0,
            legal_accountability_gap_score=28.0,
            minority_targeting_pattern_score=30.0,
            primary_pattern="legal_accountability_gap",
        ),
        HateSpeechIncitementEntity(
            entity_id="HS-008",
            name="ONU/Plan Action Rabat & Stratégie Discours Haine — Seuils Incitation & Liberté Expression",
            country="Global",
            incitement_violence_scale_score=4.0,
            platform_amplification_failure_score=5.0,
            legal_accountability_gap_score=3.0,
            minority_targeting_pattern_score=6.0,
            primary_pattern="legal_accountability_gap",
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

    return HateSpeechIncitementEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_hate_speech_incitement_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_adviser_prevention_genocide_hate_speech_report",
            "global_network_initiative_content_moderation_human_rights_assessment",
            "ims_media_monitoring_hate_speech_conflict_zones_database",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_hate_speech_incitement_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_hate_speech_incitement_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
