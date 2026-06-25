from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#7c3aed"


@dataclass
class InternetCensorshipRightsEntity:
    entity_id: str
    name: str
    country: str
    content_blocking_score: float
    surveillance_censorship_score: float
    platform_coercion_score: float
    journalist_blogger_persecution_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_internet_censorship_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.content_blocking_score * 0.30
            + self.surveillance_censorship_score * 0.25
            + self.platform_coercion_score * 0.25
            + self.journalist_blogger_persecution_score * 0.20,
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
        self.estimated_internet_censorship_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class InternetCensorshipRightsEngineResult:
    agent: str = "Internet Censorship Rights Engine Agent"
    domain: str = "internet_censorship_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_internet_censorship_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[InternetCensorshipRightsEntity] = field(default_factory=list)


def run_internet_censorship_rights_engine() -> InternetCensorshipRightsEngineResult:
    entities = [
        InternetCensorshipRightsEntity(
            entity_id="ICR-001",
            name="Chine — Grand Firewall, 10k Domaines Bloqués, 99% Filtrage, 2 Millions Censeurs, Surveillance Totale",
            country="Chine",
            content_blocking_score=99.0,
            surveillance_censorship_score=98.0,
            platform_coercion_score=97.0,
            journalist_blogger_persecution_score=96.0,
            primary_pattern="content_blocking_score",
        ),
        InternetCensorshipRightsEntity(
            entity_id="ICR-002",
            name="Corée du Nord — Intranet Kwangmyong Isolé, Peine de Mort Accès Internet Étranger, Isolation Totale",
            country="Corée du Nord",
            content_blocking_score=100.0,
            surveillance_censorship_score=99.0,
            platform_coercion_score=99.0,
            journalist_blogger_persecution_score=98.0,
            primary_pattern="content_blocking_score",
        ),
        InternetCensorshipRightsEntity(
            entity_id="ICR-003",
            name="Iran — Internet National Halal, 80% Coupures, Telegram Interdit, VPN Criminalisé, Répression Sévère",
            country="Iran",
            content_blocking_score=92.0,
            surveillance_censorship_score=90.0,
            platform_coercion_score=88.0,
            journalist_blogger_persecution_score=91.0,
            primary_pattern="content_blocking_score",
        ),
        InternetCensorshipRightsEntity(
            entity_id="ICR-004",
            name="Russie — RuNet Post-2022, Twitter/Instagram Bannis, 300k Sites Bloqués, Loi VPN Restriction Totale",
            country="Russie",
            content_blocking_score=80.0,
            surveillance_censorship_score=78.0,
            platform_coercion_score=82.0,
            journalist_blogger_persecution_score=80.0,
            primary_pattern="platform_coercion_score",
        ),
        InternetCensorshipRightsEntity(
            entity_id="ICR-005",
            name="Turquie — Wikipedia Bannie 3 Ans, Twitter/YouTube Coupures Répétées, 400k Sites Bloqués Cumulés",
            country="Turquie",
            content_blocking_score=58.0,
            surveillance_censorship_score=55.0,
            platform_coercion_score=56.0,
            journalist_blogger_persecution_score=54.0,
            primary_pattern="content_blocking_score",
        ),
        InternetCensorshipRightsEntity(
            entity_id="ICR-006",
            name="Inde — #1 Coupures Internet Monde, 84 Shutdowns 2023, Cachemire 552 Jours Record Mondial",
            country="Inde",
            content_blocking_score=52.0,
            surveillance_censorship_score=48.0,
            platform_coercion_score=50.0,
            journalist_blogger_persecution_score=46.0,
            primary_pattern="content_blocking_score",
        ),
        InternetCensorshipRightsEntity(
            entity_id="ICR-007",
            name="Brésil — Suspension X/Twitter 2024, Décisions Judiciaires Ciblées, Régulation Plateformes Controversée",
            country="Brésil",
            content_blocking_score=28.0,
            surveillance_censorship_score=24.0,
            platform_coercion_score=30.0,
            journalist_blogger_persecution_score=22.0,
            primary_pattern="platform_coercion_score",
        ),
        InternetCensorshipRightsEntity(
            entity_id="ICR-008",
            name="Islande — Zéro Blocage, Liberté Presse Digitale Maximale, Meilleure Pratique Mondiale Référence",
            country="Islande",
            content_blocking_score=4.0,
            surveillance_censorship_score=5.0,
            platform_coercion_score=4.0,
            journalist_blogger_persecution_score=3.0,
            primary_pattern="content_blocking_score",
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

    return InternetCensorshipRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_internet_censorship_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freedom_house_freedom_net_2024",
            "rsf_press_freedom_index_digital_2024",
            "citizen_lab_censorship_report_2024",
            "article19_internet_shutdown_tracker",
            "cpj_online_journalist_imprisonment_census_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_internet_censorship_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
