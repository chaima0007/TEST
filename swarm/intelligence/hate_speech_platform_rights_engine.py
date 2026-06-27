from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HateSpeechPlatformRightsEntity:
    entity_id: str
    name: str
    country: str
    online_hate_escalation_violence_severity_score: float
    content_moderation_bias_minority_targeting_score: float
    platform_impunity_accountability_gap_score: float
    victim_legal_redress_absence_scale_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_hate_speech_platform_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.online_hate_escalation_violence_severity_score * 0.30
            + self.content_moderation_bias_minority_targeting_score * 0.25
            + self.platform_impunity_accountability_gap_score * 0.25
            + self.victim_legal_redress_absence_scale_score * 0.20,
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
        self.estimated_hate_speech_platform_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class HateSpeechPlatformRightsEngineResult:
    agent: str = "Hate Speech Platform Rights Engine Agent"
    domain: str = "hate_speech_platform_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_hate_speech_platform_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HateSpeechPlatformRightsEntity] = field(default_factory=list)

def run_hate_speech_platform_rights_engine() -> HateSpeechPlatformRightsEngineResult:
    entities = [
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-001",
            name="Myanmar/Facebook — Discours Haine Rohingyas, Génocide Algorithmique & Zéro Modération Birmane",
            country="Asie du Sud-Est",
            online_hate_escalation_violence_severity_score=95.0,
            content_moderation_bias_minority_targeting_score=92.0,
            platform_impunity_accountability_gap_score=92.0,
            victim_legal_redress_absence_scale_score=90.0,
            primary_pattern="online_hate_escalation_violence_severity",
        ),
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-002",
            name="Inde/WhatsApp — Lynchages Viraux, Fake News Musulmans & 200M Users Sans Vérification",
            country="Asie du Sud",
            online_hate_escalation_violence_severity_score=90.0,
            content_moderation_bias_minority_targeting_score=92.0,
            platform_impunity_accountability_gap_score=88.0,
            victim_legal_redress_absence_scale_score=88.0,
            primary_pattern="content_moderation_bias_minority_targeting",
        ),
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-003",
            name="Éthiopie/Tigré — Facebook Haine Ethnique Tigréens, Massacres & Algorithme Amplification",
            country="Afrique de l'Est",
            online_hate_escalation_violence_severity_score=88.0,
            content_moderation_bias_minority_targeting_score=88.0,
            platform_impunity_accountability_gap_score=90.0,
            victim_legal_redress_absence_scale_score=86.0,
            primary_pattern="platform_impunity_accountability_gap",
        ),
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-004",
            name="USA/Twitter-X — Suppression Modération, Haine Raciale & Islamophobie Sans Restriction",
            country="Amérique du Nord",
            online_hate_escalation_violence_severity_score=85.0,
            content_moderation_bias_minority_targeting_score=86.0,
            platform_impunity_accountability_gap_score=88.0,
            victim_legal_redress_absence_scale_score=84.0,
            primary_pattern="platform_impunity_accountability_gap",
        ),
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-005",
            name="UE — DSA Insuffisant, Haine En Ligne +40% & Délais Retrait 24h Non Respectés",
            country="Europe",
            online_hate_escalation_violence_severity_score=55.0,
            content_moderation_bias_minority_targeting_score=52.0,
            platform_impunity_accountability_gap_score=52.0,
            victim_legal_redress_absence_scale_score=55.0,
            primary_pattern="victim_legal_redress_absence_scale",
        ),
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-006",
            name="Afrique/Asie Francophone — Haine Ethnique Sans Modération Locale & Zéro Langue Minoritaire",
            country="Afrique/Asie",
            online_hate_escalation_violence_severity_score=50.0,
            content_moderation_bias_minority_targeting_score=52.0,
            platform_impunity_accountability_gap_score=52.0,
            victim_legal_redress_absence_scale_score=48.0,
            primary_pattern="content_moderation_bias_minority_targeting",
        ),
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-007",
            name="Global Voices/ADL — Monitoring Discours Haine, Contre-Narration & Plaidoyer DSA/Section 230",
            country="Global",
            online_hate_escalation_violence_severity_score=22.0,
            content_moderation_bias_minority_targeting_score=28.0,
            platform_impunity_accountability_gap_score=25.0,
            victim_legal_redress_absence_scale_score=30.0,
            primary_pattern="victim_legal_redress_absence_scale",
        ),
        HateSpeechPlatformRightsEntity(
            entity_id="HSP-008",
            name="ONU/HRC — Plan Rabat Discours Haine, Rapporteur Spécial Liberté Expression & SDG 16",
            country="Global",
            online_hate_escalation_violence_severity_score=4.0,
            content_moderation_bias_minority_targeting_score=5.0,
            platform_impunity_accountability_gap_score=3.0,
            victim_legal_redress_absence_scale_score=6.0,
            primary_pattern="online_hate_escalation_violence_severity",
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

    return HateSpeechPlatformRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_hate_speech_platform_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_adviser_genocide_prevention_myanmar_facebook_hate_speech_report",
            "global_witnesses_facebook_hate_speech_ethiopia_tigray_investigation",
            "adl_online_hate_index_platform_accountability_annual_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_hate_speech_platform_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_hate_speech_platform_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
