from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SocialMediaCensorshipEntity:
    entity_id: str
    name: str
    country: str
    platform_blocking_scope_score: float
    content_removal_political_score: float
    algorithmic_suppression_score: float
    user_data_state_access_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_social_media_censorship_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.platform_blocking_scope_score * 0.30
            + self.content_removal_political_score * 0.25
            + self.algorithmic_suppression_score * 0.25
            + self.user_data_state_access_score * 0.20,
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
        self.estimated_social_media_censorship_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SocialMediaCensorshipEngineResult:
    agent: str = "Social Media Censorship Engine Agent"
    domain: str = "social_media_censorship"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_social_media_censorship_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SocialMediaCensorshipEntity] = field(default_factory=list)

def run_social_media_censorship_engine() -> SocialMediaCensorshipEngineResult:
    entities = [
        SocialMediaCensorshipEntity(
            entity_id="SMC-001",
            name="Chine — Grand Firewall, WeChat Surveillance & Toutes Plateformes Occidentales Bloquées",
            country="Asie du Nord-Est",
            platform_blocking_scope_score=98.0,
            content_removal_political_score=95.0,
            algorithmic_suppression_score=92.0,
            user_data_state_access_score=95.0,
            primary_pattern="platform_blocking_scope",
        ),
        SocialMediaCensorshipEntity(
            entity_id="SMC-002",
            name="Russie — Blocage Instagram/Facebook post-2022, RuNet & Loi Souveraineté Internet",
            country="Europe de l'Est",
            platform_blocking_scope_score=88.0,
            content_removal_political_score=88.0,
            algorithmic_suppression_score=85.0,
            user_data_state_access_score=85.0,
            primary_pattern="content_removal_political",
        ),
        SocialMediaCensorshipEntity(
            entity_id="SMC-003",
            name="Iran — Blocage WhatsApp/Telegram, Shamr Filtre & Coupures lors Protestations",
            country="Moyen-Orient",
            platform_blocking_scope_score=85.0,
            content_removal_political_score=82.0,
            algorithmic_suppression_score=80.0,
            user_data_state_access_score=88.0,
            primary_pattern="user_data_state_access",
        ),
        SocialMediaCensorshipEntity(
            entity_id="SMC-004",
            name="Myanmar — Blocage Facebook/Twitter Coup 2021, Coupures Internet & Surveillance Militaire",
            country="Asie du Sud-Est",
            platform_blocking_scope_score=82.0,
            content_removal_political_score=80.0,
            algorithmic_suppression_score=78.0,
            user_data_state_access_score=82.0,
            primary_pattern="platform_blocking_scope",
        ),
        SocialMediaCensorshipEntity(
            entity_id="SMC-005",
            name="Meta/TikTok — Modération Opaque Contenu Politique, Biais Algorithmique & Rapports Transparence Lacunaires",
            country="Global/USA",
            platform_blocking_scope_score=52.0,
            content_removal_political_score=55.0,
            algorithmic_suppression_score=58.0,
            user_data_state_access_score=50.0,
            primary_pattern="algorithmic_suppression",
        ),
        SocialMediaCensorshipEntity(
            entity_id="SMC-006",
            name="Inde — Blocages Temporaires Cachemire, Orders IT Rules 2021 & Takedowns Gouvernementaux",
            country="Asie du Sud",
            platform_blocking_scope_score=48.0,
            content_removal_political_score=52.0,
            algorithmic_suppression_score=50.0,
            user_data_state_access_score=55.0,
            primary_pattern="content_removal_political",
        ),
        SocialMediaCensorshipEntity(
            entity_id="SMC-007",
            name="UE/DSA — Digital Services Act, Obligations Transparence & Mécanismes Recours Utilisateurs",
            country="Europe",
            platform_blocking_scope_score=22.0,
            content_removal_political_score=25.0,
            algorithmic_suppression_score=28.0,
            user_data_state_access_score=30.0,
            primary_pattern="algorithmic_suppression",
        ),
        SocialMediaCensorshipEntity(
            entity_id="SMC-008",
            name="ONU/Rapporteur Expression — Lignes Directrices Modération, Standards Droits & Dialogue Plateformes",
            country="Global",
            platform_blocking_scope_score=4.0,
            content_removal_political_score=5.0,
            algorithmic_suppression_score=3.0,
            user_data_state_access_score=6.0,
            primary_pattern="user_data_state_access",
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

    return SocialMediaCensorshipEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_social_media_censorship_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freedom_house_freedom_on_the_net_platform_censorship_report",
            "citizenlab_internet_censorship_global_network_interference_dataset",
            "netblocks_internet_shutdown_observatory_social_media_blocking_monitor",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_social_media_censorship_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_social_media_censorship_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
