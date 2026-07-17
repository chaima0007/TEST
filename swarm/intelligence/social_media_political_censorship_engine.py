from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SocialMediaPoliticalCensorshipEntity:
    entity_id: str
    name: str
    country: str
    platform_content_removal_political_severity_score: float
    internet_shutdown_election_suppression_scale_score: float
    state_disinformation_manipulation_score: float
    journalist_blogger_platform_ban_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_social_media_political_censorship_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.platform_content_removal_political_severity_score * 0.30
            + self.internet_shutdown_election_suppression_scale_score * 0.25
            + self.state_disinformation_manipulation_score * 0.25
            + self.journalist_blogger_platform_ban_deficit_gap_score * 0.20,
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
        self.estimated_social_media_political_censorship_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class SocialMediaPoliticalCensorshipEngineResult:
    agent: str = "Social Media Political Censorship Engine Agent"
    domain: str = "social_media_political_censorship"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_social_media_political_censorship_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SocialMediaPoliticalCensorshipEntity] = field(default_factory=list)


def run_social_media_political_censorship_engine() -> SocialMediaPoliticalCensorshipEngineResult:
    entities = [
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-001",
            name="Chine/Grande Muraille Feu — WeChat Weibo Contrôle Total, Algorithmes Surveillance & Mots-Clés Censurés Millions",
            country="Chine",
            platform_content_removal_political_severity_score=97.0,
            internet_shutdown_election_suppression_scale_score=95.0,
            state_disinformation_manipulation_score=96.0,
            journalist_blogger_platform_ban_deficit_gap_score=94.0,
            primary_pattern="platform_content_removal_political_severity",
        ),
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-002",
            name="Russie/Blocages Twitter Meta — Loi Souveraineté Numérique RuNet, VPN Criminalisés & Blogueurs Emprisonnés Guerre",
            country="Russie",
            platform_content_removal_political_severity_score=93.0,
            internet_shutdown_election_suppression_scale_score=91.0,
            state_disinformation_manipulation_score=94.0,
            journalist_blogger_platform_ban_deficit_gap_score=92.0,
            primary_pattern="state_disinformation_manipulation",
        ),
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-003",
            name="Iran/VPN Généralisés — Coupures Élection Mahsa Amini, Instagram TikTok Bloqués & Cyber Police Arrestations",
            country="Iran",
            platform_content_removal_political_severity_score=90.0,
            internet_shutdown_election_suppression_scale_score=92.0,
            state_disinformation_manipulation_score=89.0,
            journalist_blogger_platform_ban_deficit_gap_score=91.0,
            primary_pattern="internet_shutdown_election_suppression_scale",
        ),
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-004",
            name="Inde/Shutdowns 2022 — 584 Internet Coupures Record Mondial, Twitter Ordres Retrait & Farmer Protests Blocages",
            country="Inde",
            platform_content_removal_political_severity_score=87.0,
            internet_shutdown_election_suppression_scale_score=89.0,
            state_disinformation_manipulation_score=85.0,
            journalist_blogger_platform_ban_deficit_gap_score=86.0,
            primary_pattern="internet_shutdown_election_suppression_scale",
        ),
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-005",
            name="Éthiopie/Tigré — Coupures Internet 1 An Conflit, Journalistes Bloqués & Propagande État Réseaux Sociaux",
            country="Éthiopie",
            platform_content_removal_political_severity_score=57.0,
            internet_shutdown_election_suppression_scale_score=60.0,
            state_disinformation_manipulation_score=58.0,
            journalist_blogger_platform_ban_deficit_gap_score=55.0,
            primary_pattern="internet_shutdown_election_suppression_scale",
        ),
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-006",
            name="Pakistan/Blocages PTI — Imran Khan Arrestations Twitter X Suspendu, TikTok Banni & Journalistes Disparus",
            country="Pakistan",
            platform_content_removal_political_severity_score=54.0,
            internet_shutdown_election_suppression_scale_score=56.0,
            state_disinformation_manipulation_score=55.0,
            journalist_blogger_platform_ban_deficit_gap_score=57.0,
            primary_pattern="journalist_blogger_platform_ban_deficit_gap",
        ),
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-007",
            name="EFF/Access Now KeepItOn — Coalition Anti-Shutdown, Digital Rights Atlas & Rapport Annuel Coupures Internet",
            country="Global",
            platform_content_removal_political_severity_score=27.0,
            internet_shutdown_election_suppression_scale_score=26.0,
            state_disinformation_manipulation_score=25.0,
            journalist_blogger_platform_ban_deficit_gap_score=28.0,
            primary_pattern="journalist_blogger_platform_ban_deficit_gap",
        ),
        SocialMediaPoliticalCensorshipEntity(
            entity_id="SMC-008",
            name="ONU/RES 32/13 — Internet Droit Fondamental, Rapporteur Spécial Expression En Ligne & GNI Principes",
            country="Global",
            platform_content_removal_political_severity_score=5.0,
            internet_shutdown_election_suppression_scale_score=5.0,
            state_disinformation_manipulation_score=4.0,
            journalist_blogger_platform_ban_deficit_gap_score=5.0,
            primary_pattern="platform_content_removal_political_severity",
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

    return SocialMediaPoliticalCensorshipEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_social_media_political_censorship_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "access_now_keepiton_internet_shutdown_tracker",
            "freedom_house_freedom_on_the_net_report",
            "eff_coercive_content_moderation_analysis",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_social_media_political_censorship_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_social_media_political_censorship_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
