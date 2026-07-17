from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class FreedomExpressionArtisticCensorshipEntity:
    entity_id: str
    name: str
    country: str
    artist_imprisonment_persecution_score: float
    state_cultural_censorship_banned_works_score: float
    online_content_creative_suppression_score: float
    self_censorship_chilling_artistic_effect_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_freedom_expression_artistic_censorship_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.artist_imprisonment_persecution_score * 0.30
            + self.state_cultural_censorship_banned_works_score * 0.25
            + self.online_content_creative_suppression_score * 0.25
            + self.self_censorship_chilling_artistic_effect_score * 0.20,
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
        self.estimated_freedom_expression_artistic_censorship_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class FreedomExpressionArtisticCensorshipEngineResult:
    agent: str = "Freedom Expression Artistic Censorship Engine Agent"
    domain: str = "freedom_expression_artistic_censorship"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_freedom_expression_artistic_censorship_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FreedomExpressionArtisticCensorshipEntity] = field(default_factory=list)


def run_freedom_expression_artistic_censorship_engine() -> FreedomExpressionArtisticCensorshipEngineResult:
    entities = [
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-001",
            name="Chine — Ai Weiwei Exil, Zhang Yimou Censuré, Artistes Uyghurs Disparus & Plateforme TikTok/Weibo Censure Algorithmes",
            country="Chine",
            artist_imprisonment_persecution_score=94.0,
            state_cultural_censorship_banned_works_score=93.0,
            online_content_creative_suppression_score=95.0,
            self_censorship_chilling_artistic_effect_score=92.0,
            primary_pattern="online_content_creative_suppression",
        ),
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-002",
            name="Iran — Jafar Panahi Emprisonné Multiple, Mohammad Rasoulof Exil Cannes, Chanteuses Interdites Scène & Rokhayl Cinéma",
            country="Iran",
            artist_imprisonment_persecution_score=91.0,
            state_cultural_censorship_banned_works_score=90.0,
            online_content_creative_suppression_score=88.0,
            self_censorship_chilling_artistic_effect_score=89.0,
            primary_pattern="artist_imprisonment_persecution",
        ),
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-003",
            name="Russie/2022 — Pugacheva Exil, Théâtres Auto-Censure Guerre, Kirill Serebrennikov Jugé 2017 & VKontakte Modération",
            country="Russie",
            artist_imprisonment_persecution_score=87.0,
            state_cultural_censorship_banned_works_score=85.0,
            online_content_creative_suppression_score=83.0,
            self_censorship_chilling_artistic_effect_score=88.0,
            primary_pattern="self_censorship_chilling_artistic_effect",
        ),
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-004",
            name="Arabie Saoudite — Netflix Contenu Retiré Pressions, Rappeurs Emprisonnés, Cinéma Ouvert 2018 Mais Contenus Filtrés",
            country="Arabie Saoudite",
            artist_imprisonment_persecution_score=84.0,
            state_cultural_censorship_banned_works_score=86.0,
            online_content_creative_suppression_score=82.0,
            self_censorship_chilling_artistic_effect_score=85.0,
            primary_pattern="state_cultural_censorship_banned_works",
        ),
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-005",
            name="Turquie — Elif Safak Procès Multiple, Cumhuriyet Artistes, Instagram Bloqué Périodique & Ahmet Altan Emprisonné",
            country="Turquie",
            artist_imprisonment_persecution_score=56.0,
            state_cultural_censorship_banned_works_score=54.0,
            online_content_creative_suppression_score=58.0,
            self_censorship_chilling_artistic_effect_score=57.0,
            primary_pattern="artist_imprisonment_persecution",
        ),
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-006",
            name="Inde — CBFC Coupes Films, OTT Règlementation 2021, Vivek Agnihotri Controverse & Art Contemporain Kashi Pression",
            country="Inde",
            artist_imprisonment_persecution_score=52.0,
            state_cultural_censorship_banned_works_score=55.0,
            online_content_creative_suppression_score=53.0,
            self_censorship_chilling_artistic_effect_score=54.0,
            primary_pattern="state_cultural_censorship_banned_works",
        ),
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-007",
            name="Hongrie — Cinéma Budget État Conditionnel Loyauté Politique, Müpa Budgets Coupés Opposition & LGBTQ Art Interdit",
            country="Hongrie",
            artist_imprisonment_persecution_score=30.0,
            state_cultural_censorship_banned_works_score=35.0,
            online_content_creative_suppression_score=28.0,
            self_censorship_chilling_artistic_effect_score=32.0,
            primary_pattern="state_cultural_censorship_banned_works",
        ),
        FreedomExpressionArtisticCensorshipEntity(
            entity_id="FEAC-008",
            name="France — CNC Financement Art Sans Censure, Loi Presse 1881, SACD Protection & Quelques Controverses Autodiscipline",
            country="France",
            artist_imprisonment_persecution_score=7.0,
            state_cultural_censorship_banned_works_score=6.0,
            online_content_creative_suppression_score=8.0,
            self_censorship_chilling_artistic_effect_score=9.0,
            primary_pattern="self_censorship_chilling_artistic_effect",
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

    return FreedomExpressionArtisticCensorshipEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_freedom_expression_artistic_censorship_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freemuse_state_of_artistic_freedom_2023",
            "pen_international_artistic_freedom_violations_2023",
            "human_rights_watch_cultural_rights_2023",
            "ipi_artistic_expression_press_freedom_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_freedom_expression_artistic_censorship_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_freedom_expression_artistic_censorship_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
