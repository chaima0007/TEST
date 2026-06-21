from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class InternetFreedomCensorshipEntity:
    entity_id: str
    name: str
    country: str
    internet_shutdown_frequency_duration_score: float
    social_media_platform_blocking_score: float
    online_activist_prosecution_score: float
    vpn_circumvention_tools_restriction_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_internet_freedom_censorship_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.internet_shutdown_frequency_duration_score * 0.30
            + self.social_media_platform_blocking_score * 0.25
            + self.online_activist_prosecution_score * 0.25
            + self.vpn_circumvention_tools_restriction_score * 0.20,
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
        self.estimated_internet_freedom_censorship_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class InternetFreedomCensorshipEngineResult:
    agent: str = "Internet Freedom Censorship Engine Agent"
    domain: str = "internet_freedom_censorship"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_internet_freedom_censorship_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[InternetFreedomCensorshipEntity] = field(default_factory=list)


def run_internet_freedom_censorship_engine() -> InternetFreedomCensorshipEngineResult:
    entities = [
        InternetFreedomCensorshipEntity(
            entity_id="IFC-001",
            name="Corée du Nord — Internet Totalement Absent Population, Intranet Kwangmyong Uniquement & Accès Peine de Mort",
            country="Corée du Nord",
            internet_shutdown_frequency_duration_score=99.0,
            social_media_platform_blocking_score=99.0,
            online_activist_prosecution_score=98.0,
            vpn_circumvention_tools_restriction_score=99.0,
            primary_pattern="internet_shutdown_frequency_duration",
        ),
        InternetFreedomCensorshipEntity(
            entity_id="IFC-002",
            name="Iran — Internet Coupé 5 Jours Manifestations 2019, Instagram/WhatsApp Bloqués, VPN Illégaux & 50+ Militants Condamnés Tweets",
            country="Iran",
            internet_shutdown_frequency_duration_score=91.0,
            social_media_platform_blocking_score=90.0,
            online_activist_prosecution_score=88.0,
            vpn_circumvention_tools_restriction_score=89.0,
            primary_pattern="online_activist_prosecution",
        ),
        InternetFreedomCensorshipEntity(
            entity_id="IFC-003",
            name="Myanmar — Internet Coupé 500+ Jours Post-Coup 2021, Journalistes Citoyens Arrêtés Posts Facebook & Telenor Données Policiers",
            country="Myanmar",
            internet_shutdown_frequency_duration_score=93.0,
            social_media_platform_blocking_score=85.0,
            online_activist_prosecution_score=90.0,
            vpn_circumvention_tools_restriction_score=86.0,
            primary_pattern="internet_shutdown_frequency_duration",
        ),
        InternetFreedomCensorshipEntity(
            entity_id="IFC-004",
            name="Russie — Twitter/Instagram/Facebook Bloqués 2022, VPN Légaux Supprimés, Roskomnadzor 350K URL Bloquées & Blogueurs Emprisonnés",
            country="Russie",
            internet_shutdown_frequency_duration_score=82.0,
            social_media_platform_blocking_score=88.0,
            online_activist_prosecution_score=86.0,
            vpn_circumvention_tools_restriction_score=87.0,
            primary_pattern="social_media_platform_blocking",
        ),
        InternetFreedomCensorshipEntity(
            entity_id="IFC-005",
            name="Chine — Grand Firewall 10K+ Sites Bloqués, VPN Illégaux, WeChat Surveillance Contenu & Weibo Censure Automatique IA",
            country="Chine",
            internet_shutdown_frequency_duration_score=50.0,
            social_media_platform_blocking_score=55.0,
            online_activist_prosecution_score=52.0,
            vpn_circumvention_tools_restriction_score=58.0,
            primary_pattern="vpn_circumvention_tools_restriction",
        ),
        InternetFreedomCensorshipEntity(
            entity_id="IFC-006",
            name="Turquie — Twitter Bloqué 2022/2023, Wikipedia Bannie 3 Ans, 3000+ Sites Bloqués & 400+ Poursuites Tweets",
            country="Turquie",
            internet_shutdown_frequency_duration_score=52.0,
            social_media_platform_blocking_score=58.0,
            online_activist_prosecution_score=55.0,
            vpn_circumvention_tools_restriction_score=50.0,
            primary_pattern="social_media_platform_blocking",
        ),
        InternetFreedomCensorshipEntity(
            entity_id="IFC-007",
            name="Inde — Plus Grand Pays Coupures Internet 500+ en 2023, Cachemire 600 Jours & IT Rules Controversées",
            country="Inde",
            internet_shutdown_frequency_duration_score=30.0,
            social_media_platform_blocking_score=28.0,
            online_activist_prosecution_score=25.0,
            vpn_circumvention_tools_restriction_score=22.0,
            primary_pattern="internet_shutdown_frequency_duration",
        ),
        InternetFreedomCensorshipEntity(
            entity_id="IFC-008",
            name="Estonie — Liberté Internet Index Top 5, Aucun Blocage, Cybersécurité Modèle & Protection Données RGPD Robuste",
            country="Estonie",
            internet_shutdown_frequency_duration_score=5.0,
            social_media_platform_blocking_score=4.0,
            online_activist_prosecution_score=4.0,
            vpn_circumvention_tools_restriction_score=3.0,
            primary_pattern="internet_shutdown_frequency_duration",
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

    return InternetFreedomCensorshipEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_internet_freedom_censorship_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freedom_house_freedom_net_internet_2023",
            "netblocks_internet_shutdown_tracker_2023",
            "article_19_internet_freedom_report_2023",
            "access_now_keepiton_report_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_internet_freedom_censorship_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_internet_freedom_censorship_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
