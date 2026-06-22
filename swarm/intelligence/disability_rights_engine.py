from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0a1a35"

@dataclass
class DisabilityRightsEntity:
    entity_id: str
    name: str
    country: str
    discrimination_employment_score: float
    accessibility_barrier_score: float
    institutional_exclusion_score: float
    social_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_disability_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.discrimination_employment_score * 0.30
            + self.accessibility_barrier_score * 0.25
            + self.institutional_exclusion_score * 0.25
            + self.social_protection_gap_score * 0.20,
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
        self.estimated_disability_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DisabilityRightsEngineResult:
    agent: str = "Disability Rights Engine Agent"
    domain: str = "disability_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_disability_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DisabilityRightsEntity] = field(default_factory=list)


def run_disability_rights_engine() -> DisabilityRightsEngineResult:
    entities = [
        DisabilityRightsEntity(
            entity_id="DSR-001",
            name="Afghanistan (post-Taliban) — Personnes Handicapées Abandonnées, Aucun Service Réhabilitation, Femmes Handicapées Confinées & Budget Santé Néant",
            country="Afghanistan",
            discrimination_employment_score=97.0,
            accessibility_barrier_score=95.0,
            institutional_exclusion_score=96.0,
            social_protection_gap_score=94.0,
            primary_pattern="institutional_exclusion",
        ),
        DisabilityRightsEntity(
            entity_id="DSR-002",
            name="Yémen — Guerre Créant Handicap Acquis Massif, Zéro Infrastructure Réhabilitation, Mines Antipersonnel & Amputés Sans Prothèses",
            country="Yémen",
            discrimination_employment_score=91.0,
            accessibility_barrier_score=90.0,
            institutional_exclusion_score=89.0,
            social_protection_gap_score=92.0,
            primary_pattern="social_protection_gap",
        ),
        DisabilityRightsEntity(
            entity_id="DSR-003",
            name="Éthiopie — Conflits Tigré Handicapés Déplacés Sans Support, Stigmatisation Culturelle Profonde & Services Sociaux Absents Zones Rurales",
            country="Éthiopie",
            discrimination_employment_score=80.0,
            accessibility_barrier_score=78.0,
            institutional_exclusion_score=82.0,
            social_protection_gap_score=84.0,
            primary_pattern="social_protection_gap",
        ),
        DisabilityRightsEntity(
            entity_id="DSR-004",
            name="Inde — Double Discrimination Caste & Handicap, Ségrégation Éducation Spécialisée, Emploi Informel Précaire & Accès Transports Inexistant",
            country="Inde",
            discrimination_employment_score=75.0,
            accessibility_barrier_score=72.0,
            institutional_exclusion_score=70.0,
            social_protection_gap_score=68.0,
            primary_pattern="discrimination_employment",
        ),
        DisabilityRightsEntity(
            entity_id="DSR-005",
            name="Brésil — Barrières Accessibilité Infrastructures, Écart Emploi 30% Personnes Handicapées, Inégalités Régionales & Violence Institutionnelle",
            country="Brésil",
            discrimination_employment_score=60.0,
            accessibility_barrier_score=62.0,
            institutional_exclusion_score=58.0,
            social_protection_gap_score=56.0,
            primary_pattern="accessibility_barrier",
        ),
        DisabilityRightsEntity(
            entity_id="DSR-006",
            name="USA — ADA Gaps Application, Surreprésentation Handicap en Prison 40%, Assurance Insuffisante & Accès Santé Mentale Défaillant",
            country="USA",
            discrimination_employment_score=50.0,
            accessibility_barrier_score=47.0,
            institutional_exclusion_score=53.0,
            social_protection_gap_score=49.0,
            primary_pattern="institutional_exclusion",
        ),
        DisabilityRightsEntity(
            entity_id="DSR-007",
            name="Allemagne — Inclusion Scolaire Partielle, Ateliers Protégés Controversés, Accessibilité Transport Incomplète & Écart Salaire 15%",
            country="Allemagne",
            discrimination_employment_score=28.0,
            accessibility_barrier_score=30.0,
            institutional_exclusion_score=32.0,
            social_protection_gap_score=26.0,
            primary_pattern="institutional_exclusion",
        ),
        DisabilityRightsEntity(
            entity_id="DSR-008",
            name="Suède — CRPD Meilleure Pratique, Inclusion Universelle Éducation, Emploi Soutenu & Accessibilité Universelle Référence Mondiale",
            country="Suède",
            discrimination_employment_score=10.0,
            accessibility_barrier_score=8.0,
            institutional_exclusion_score=9.0,
            social_protection_gap_score=7.0,
            primary_pattern="discrimination_employment",
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

    return DisabilityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_disability_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "crpd_committee_concluding_observations_states",
            "who_world_report_disability_2023",
            "ilo_disability_employment_gap_global_report",
            "hrw_disability_rights_violations_documentation",
            "un_special_rapporteur_disability_annual_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_disability_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_disability_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
