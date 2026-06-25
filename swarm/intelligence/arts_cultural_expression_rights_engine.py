from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ArtsCulturalExpressionRightsEntity:
    entity_id: str
    name: str
    country: str
    artist_censorship_imprisonment_severity_score: float
    cultural_institution_state_capture_scale_score: float
    online_creative_content_suppression_score: float
    artistic_minority_voice_exclusion_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_arts_cultural_expression_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.artist_censorship_imprisonment_severity_score * 0.30
            + self.cultural_institution_state_capture_scale_score * 0.25
            + self.online_creative_content_suppression_score * 0.25
            + self.artistic_minority_voice_exclusion_deficit_gap_score * 0.20,
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
        self.estimated_arts_cultural_expression_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ArtsCulturalExpressionRightsEngineResult:
    agent: str = "Arts Cultural Expression Rights Engine Agent"
    domain: str = "arts_cultural_expression_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_arts_cultural_expression_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ArtsCulturalExpressionRightsEntity] = field(default_factory=list)


def run_arts_cultural_expression_rights_engine() -> ArtsCulturalExpressionRightsEngineResult:
    entities = [
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-001",
            name="Chine — Ai Weiwei Exilé, Artistes Xinjiang Emprisonnés, Films Censurés 2000+/An & Internet Culturel Filtré",
            country="Chine",
            artist_censorship_imprisonment_severity_score=95.0,
            cultural_institution_state_capture_scale_score=93.0,
            online_creative_content_suppression_score=92.0,
            artistic_minority_voice_exclusion_deficit_gap_score=91.0,
            primary_pattern="online_creative_content_suppression",
        ),
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-002",
            name="Iran — Rappeurs Exécutés Toomaj Salehi, Cinéastes Jafar Panahi Prison, Femmes Artistes Voile & Concerts Interdits",
            country="Iran",
            artist_censorship_imprisonment_severity_score=92.0,
            cultural_institution_state_capture_scale_score=90.0,
            online_creative_content_suppression_score=89.0,
            artistic_minority_voice_exclusion_deficit_gap_score=88.0,
            primary_pattern="artist_censorship_imprisonment_severity",
        ),
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-003",
            name="Russie — Pussy Riot Emprisonnées, Théâtres Fermés Guerre Ukraine, Artistes Exilés 5 000+ & Livres Retirés",
            country="Russie",
            artist_censorship_imprisonment_severity_score=89.0,
            cultural_institution_state_capture_scale_score=87.0,
            online_creative_content_suppression_score=86.0,
            artistic_minority_voice_exclusion_deficit_gap_score=85.0,
            primary_pattern="cultural_institution_state_capture_scale",
        ),
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-004",
            name="Arabie Saoudite — Vision 2030 Contrôlée, Artistes Critiques Traqués, Cinéma 35 Ans Interdit & Social Media Stars Arrêtés",
            country="Arabie Saoudite",
            artist_censorship_imprisonment_severity_score=86.0,
            cultural_institution_state_capture_scale_score=84.0,
            online_creative_content_suppression_score=83.0,
            artistic_minority_voice_exclusion_deficit_gap_score=82.0,
            primary_pattern="artist_censorship_imprisonment_severity",
        ),
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-005",
            name="Turquie/Hongrie — Écrivains Procès 301 Code Pénal Insulte Turcité, Théâtres Hongrois Étatisés & Subventions Politisées",
            country="Turquie/Hongrie",
            artist_censorship_imprisonment_severity_score=57.0,
            cultural_institution_state_capture_scale_score=55.0,
            online_creative_content_suppression_score=54.0,
            artistic_minority_voice_exclusion_deficit_gap_score=53.0,
            primary_pattern="cultural_institution_state_capture_scale",
        ),
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-006",
            name="USA/UK — TikTok Menace Interdiction, DMCA Surcensure, Artistes Noirs Historiquement Effacés & NFT Droits Ambigus",
            country="USA/UK",
            artist_censorship_imprisonment_severity_score=54.0,
            cultural_institution_state_capture_scale_score=52.0,
            online_creative_content_suppression_score=51.0,
            artistic_minority_voice_exclusion_deficit_gap_score=50.0,
            primary_pattern="artistic_minority_voice_exclusion_deficit_gap",
        ),
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-007",
            name="PEN International/Freemuse — Défense Artistes Emprisonnés, Alertes Violations, Advocacy ONU & Réseau Mondial",
            country="Global",
            artist_censorship_imprisonment_severity_score=27.0,
            cultural_institution_state_capture_scale_score=26.0,
            online_creative_content_suppression_score=25.0,
            artistic_minority_voice_exclusion_deficit_gap_score=25.0,
            primary_pattern="artist_censorship_imprisonment_severity",
        ),
        ArtsCulturalExpressionRightsEntity(
            entity_id="ACE-008",
            name="ONU/Art.27 DUDH — Droit Vie Culturelle, Art.15 DESC Vie Culturelle & UNESCO Convention 2005 Diversité",
            country="Global",
            artist_censorship_imprisonment_severity_score=5.0,
            cultural_institution_state_capture_scale_score=4.0,
            online_creative_content_suppression_score=4.0,
            artistic_minority_voice_exclusion_deficit_gap_score=4.0,
            primary_pattern="artistic_minority_voice_exclusion_deficit_gap",
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

    return ArtsCulturalExpressionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_arts_cultural_expression_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freemuse_state_of_artistic_freedom_annual_report",
            "pen_international_writer_persecution_database",
            "article19_online_expression_censorship_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_arts_cultural_expression_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_arts_cultural_expression_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
