from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class MinorityLanguageCulturalRightsEntity:
    entity_id: str
    name: str
    country: str
    language_prohibition_forced_assimilation_severity_score: float
    minority_language_education_media_suppression_scale_score: float
    cultural_heritage_destruction_appropriation_score: float
    language_revitalization_legal_recognition_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_minority_language_cultural_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.language_prohibition_forced_assimilation_severity_score * 0.30
            + self.minority_language_education_media_suppression_scale_score * 0.25
            + self.cultural_heritage_destruction_appropriation_score * 0.25
            + self.language_revitalization_legal_recognition_deficit_gap_score * 0.20,
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
        self.estimated_minority_language_cultural_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class MinorityLanguageCulturalRightsEngineResult:
    agent: str
    domain: str
    entities: List[MinorityLanguageCulturalRightsEntity]
    total_entities: int = field(init=False)
    avg_composite: float = field(init=False)
    avg_estimated_minority_language_cultural_rights_index: float = field(init=False)
    risk_distribution: dict = field(init=False)
    pattern_distribution: dict = field(init=False)
    top_risk_entities: List[str] = field(init=False)
    critical_alerts: List[str] = field(init=False)
    confidence_score: float = 0.85
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    data_sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_entities = len(self.entities)
        scores = [e.composite_score for e in self.entities]
        self.avg_composite = round(statistics.mean(scores), 2)
        self.avg_estimated_minority_language_cultural_rights_index = round(
            self.avg_composite / 100 * 10, 2
        )
        self.risk_distribution = {
            level: sum(1 for e in self.entities if e.risk_level == level)
            for level in ["critique", "élevé", "modéré", "faible"]
        }
        pattern_counts: dict = {}
        for e in self.entities:
            pattern_counts[e.primary_pattern] = pattern_counts.get(e.primary_pattern, 0) + 1
        self.pattern_distribution = pattern_counts
        critique_entities = sorted(
            [e for e in self.entities if e.risk_level == "critique"],
            key=lambda x: x.composite_score,
            reverse=True,
        )
        self.top_risk_entities = [e.entity_id for e in critique_entities[:3]]
        self.critical_alerts = [
            f"{e.entity_id} ({e.name}): composite={e.composite_score} — {e.primary_pattern}"
            for e in critique_entities
        ]


def run_minority_language_cultural_rights_engine() -> MinorityLanguageCulturalRightsEngineResult:
    entities = [
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-001",
            name="Chine/Tibétain-Ouïghour — Langues Tibétaines Interdites Écoles 2020, Ouïghour Alphabet Latin Supprimé, Monastères Fermés & Enseignement Mandarin Forcé",
            country="Chine",
            language_prohibition_forced_assimilation_severity_score=95.0,
            minority_language_education_media_suppression_scale_score=93.0,
            cultural_heritage_destruction_appropriation_score=92.0,
            language_revitalization_legal_recognition_deficit_gap_score=94.0,
            primary_pattern="language_prohibition_forced_assimilation_severity",
        ),
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-002",
            name="Turquie/Kurde — Kurde Interdit 1924-1991, PKK Excuse Censure Médias, Fonctionnaires Kurdes Destitués & Enseignement Limité Privé",
            country="Turquie",
            language_prohibition_forced_assimilation_severity_score=91.0,
            minority_language_education_media_suppression_scale_score=89.0,
            cultural_heritage_destruction_appropriation_score=90.0,
            language_revitalization_legal_recognition_deficit_gap_score=88.0,
            primary_pattern="minority_language_education_media_suppression_scale",
        ),
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-003",
            name="France/Langues Régionales — Loi 2021 Invalidée Occitan/Breton, Alsacien Déclin 50% Locuteurs, Éducation Bilingue Bloquée & République Une Et Indivisible",
            country="France",
            language_prohibition_forced_assimilation_severity_score=87.0,
            minority_language_education_media_suppression_scale_score=85.0,
            cultural_heritage_destruction_appropriation_score=88.0,
            language_revitalization_legal_recognition_deficit_gap_score=86.0,
            primary_pattern="language_revitalization_legal_recognition_deficit_gap",
        ),
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-004",
            name="USA/Hawaiian-Navajo — Hawaiian Quasi-Éteint 1970s, Navajo Code Talkers Honte Post-Guerre, English-Only Lois 31 États & Boarding Schools Héritage",
            country="USA",
            language_prohibition_forced_assimilation_severity_score=83.0,
            minority_language_education_media_suppression_scale_score=82.0,
            cultural_heritage_destruction_appropriation_score=84.0,
            language_revitalization_legal_recognition_deficit_gap_score=81.0,
            primary_pattern="language_prohibition_forced_assimilation_severity",
        ),
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-005",
            name="Russie/Langues — 17 Langues Minorités Non-Enseignées Post-2018 Loi, Tatare Kirillisé Forcé, Médias Locaux Fermés & Pression Identité Russe",
            country="Russie",
            language_prohibition_forced_assimilation_severity_score=56.0,
            minority_language_education_media_suppression_scale_score=54.0,
            cultural_heritage_destruction_appropriation_score=55.0,
            language_revitalization_legal_recognition_deficit_gap_score=57.0,
            primary_pattern="minority_language_education_media_suppression_scale",
        ),
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-006",
            name="Australie/Langues Autochtones — 250 Langues 1788 → 120 Survivantes, 20 Menacées Extinction, AIATSIS Budget & Accord Walmajarri Documentation",
            country="Australie",
            language_prohibition_forced_assimilation_severity_score=52.0,
            minority_language_education_media_suppression_scale_score=51.0,
            cultural_heritage_destruction_appropriation_score=54.0,
            language_revitalization_legal_recognition_deficit_gap_score=53.0,
            primary_pattern="language_revitalization_legal_recognition_deficit_gap",
        ),
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-007",
            name="UNESCO/FEL — Atlas Langues Menacées, Foundation Endangered Languages, Enduring Voices & Réseau Vitalité Linguistique",
            country="Global",
            language_prohibition_forced_assimilation_severity_score=27.0,
            minority_language_education_media_suppression_scale_score=25.0,
            cultural_heritage_destruction_appropriation_score=28.0,
            language_revitalization_legal_recognition_deficit_gap_score=26.0,
            primary_pattern="language_revitalization_legal_recognition_deficit_gap",
        ),
        MinorityLanguageCulturalRightsEntity(
            entity_id="MLC-008",
            name="ONU/DDPA Langues — Déclaration Droits Peuples Autochtones Art.13-16 Langues, PIDESC Art.27 Minorités & UNESCO Conv. Diversité 2005",
            country="Global",
            language_prohibition_forced_assimilation_severity_score=4.0,
            minority_language_education_media_suppression_scale_score=4.0,
            cultural_heritage_destruction_appropriation_score=4.0,
            language_revitalization_legal_recognition_deficit_gap_score=4.0,
            primary_pattern="language_prohibition_forced_assimilation_severity",
        ),
    ]

    return MinorityLanguageCulturalRightsEngineResult(
        agent="Minority Language Cultural Rights Engine Agent",
        domain="minority_language_cultural_rights",
        entities=entities,
        data_sources=[
            "unesco_endangered_languages_atlas",
            "minority_rights_group_language_report",
            "un_special_rapporteur_minority_rights_language",
        ],
    )


if __name__ == "__main__":
    result = run_minority_language_cultural_rights_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_minority_language_cultural_rights_index}")
    print(f"Distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
