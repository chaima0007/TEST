"""Online Censorship Platform Governance Engine — Censure internet, plateformes, liberté expression numérique."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class OnlineCensorshipPlatformGovernanceEntity:
    entity_id: str
    name: str
    country: str
    internet_shutdown_content_blocking_severity_score: float
    social_media_political_censorship_scale_score: float
    algorithmic_manipulation_disinformation_state_score: float
    platform_transparency_accountability_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_online_censorship_platform_governance_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.internet_shutdown_content_blocking_severity_score * 0.30
            + self.social_media_political_censorship_scale_score * 0.25
            + self.algorithmic_manipulation_disinformation_state_score * 0.25
            + self.platform_transparency_accountability_deficit_gap_score * 0.20,
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
        self.estimated_online_censorship_platform_governance_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class OnlineCensorshipPlatformGovernanceEngineResult:
    agent: str = "Online Censorship Platform Governance Engine Agent"
    domain: str = "online_censorship_platform_governance"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_online_censorship_platform_governance_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[OnlineCensorshipPlatformGovernanceEntity] = field(default_factory=list)


def run_online_censorship_platform_governance_engine() -> OnlineCensorshipPlatformGovernanceEngineResult:
    entities = [
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-001",
            name="Chine/GFW — Grand Firewall Chine, 10 000 Sites Bloqués, WeChat Surveillance & Contenu Politique Filtré IA",
            country="Chine",
            internet_shutdown_content_blocking_severity_score=96.0,
            social_media_political_censorship_scale_score=94.0,
            algorithmic_manipulation_disinformation_state_score=95.0,
            platform_transparency_accountability_deficit_gap_score=93.0,
            primary_pattern="internet_shutdown_content_blocking_severity",
        ),
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-002",
            name="Iran — Internet Coupé Manifestations 2019/2022, Telegram Bloqué, Système Intranet National & Dissidents Arrêtés Posts",
            country="Iran",
            internet_shutdown_content_blocking_severity_score=91.0,
            social_media_political_censorship_scale_score=92.0,
            algorithmic_manipulation_disinformation_state_score=88.0,
            platform_transparency_accountability_deficit_gap_score=90.0,
            primary_pattern="internet_shutdown_content_blocking_severity",
        ),
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-003",
            name="Russie/RuNet — Loi Souveraineté Internet 2019, Twitter Ralenti, Meta Interdit & Blogueurs 15 Ans Prison Critique Guerre",
            country="Russie",
            internet_shutdown_content_blocking_severity_score=87.0,
            social_media_political_censorship_scale_score=89.0,
            algorithmic_manipulation_disinformation_state_score=86.0,
            platform_transparency_accountability_deficit_gap_score=88.0,
            primary_pattern="social_media_political_censorship_scale",
        ),
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-004",
            name="Inde/Shutdowns — 84 Coupures Internet 2022 Monde Leader, J&K 18 Mois Coupure, Farmers Protest Bloqué & Twitter Ordres Retrait",
            country="Inde",
            internet_shutdown_content_blocking_severity_score=84.0,
            social_media_political_censorship_scale_score=82.0,
            algorithmic_manipulation_disinformation_state_score=83.0,
            platform_transparency_accountability_deficit_gap_score=81.0,
            primary_pattern="internet_shutdown_content_blocking_severity",
        ),
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-005",
            name="Turquie — Twitter Bloqué 2022 Tremblement Terre, Wikipedia 3 Ans Bloqué, Journalistes Arrêtés Tweets & 400k Sites Filtrés",
            country="Turquie",
            internet_shutdown_content_blocking_severity_score=56.0,
            social_media_political_censorship_scale_score=54.0,
            algorithmic_manipulation_disinformation_state_score=57.0,
            platform_transparency_accountability_deficit_gap_score=55.0,
            primary_pattern="social_media_political_censorship_scale",
        ),
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-006",
            name="Nigeria/Twitter — Twitter Suspendu 7 Mois 2021, SARS Hashtag Censuré, NCC Ordres Retrait & VPN Criminalisé Envisagé",
            country="Nigeria",
            internet_shutdown_content_blocking_severity_score=52.0,
            social_media_political_censorship_scale_score=51.0,
            algorithmic_manipulation_disinformation_state_score=54.0,
            platform_transparency_accountability_deficit_gap_score=53.0,
            primary_pattern="platform_transparency_accountability_deficit_gap",
        ),
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-007",
            name="EFF/Article 19 — Electronic Frontier Foundation, Article 19 Expression Numérique, Access Now Shutdowns & Rapporteur Spécial Expression",
            country="Global",
            internet_shutdown_content_blocking_severity_score=27.0,
            social_media_political_censorship_scale_score=25.0,
            algorithmic_manipulation_disinformation_state_score=28.0,
            platform_transparency_accountability_deficit_gap_score=26.0,
            primary_pattern="platform_transparency_accountability_deficit_gap",
        ),
        OnlineCensorshipPlatformGovernanceEntity(
            entity_id="OCP-008",
            name="ONU/A-HRC — Résolution Droits En Ligne = Hors Ligne, Rapporteur Spécial Liberté Expression, IGF & Standards Plateformes",
            country="Global",
            internet_shutdown_content_blocking_severity_score=4.0,
            social_media_political_censorship_scale_score=4.0,
            algorithmic_manipulation_disinformation_state_score=4.0,
            platform_transparency_accountability_deficit_gap_score=4.0,
            primary_pattern="internet_shutdown_content_blocking_severity",
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
        for e in sorted_entities if e.risk_level == "critique"
    ]

    return OnlineCensorshipPlatformGovernanceEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_online_censorship_platform_governance_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freedom_house_freedom_on_net_report",
            "access_now_shutdown_tracker",
            "article19_digital_expression_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_online_censorship_platform_governance_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_online_censorship_platform_governance_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
