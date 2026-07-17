"""LGBTQ+ Rights Engine — Criminalisation LGBT+, violence étatique, protections juridiques & réfugiés."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class LGBTQRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    criminalization_violence_severity_score: float
    legal_protection_recognition_absence_score: float
    healthcare_access_discrimination_scale_score: float
    asylum_refugee_lgbtq_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_lgbtq_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.criminalization_violence_severity_score * 0.30
            + self.legal_protection_recognition_absence_score * 0.25
            + self.healthcare_access_discrimination_scale_score * 0.25
            + self.asylum_refugee_lgbtq_protection_gap_score * 0.20,
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
        self.estimated_lgbtq_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class LGBTQRightsEngineResult:
    agent: str = "LGBTQ+ Rights Engine Agent"
    domain: str = "lgbtq_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_lgbtq_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LGBTQRightsEntity] = field(default_factory=list)


def run_lgbtq_rights_engine() -> LGBTQRightsEngineResult:
    entities = [
        LGBTQRightsEntity(
            entity_id="LGR-001",
            name="Afrique Sub-Saharienne — 32 Pays Criminalisation, Peine Mort Uganda/Mauritanie & Violence Police",
            country="Afrique Sub-Saharienne",
            sector="32 Pays Criminalisation Homosexualité Afrique Sub-Saharienne ILGA 2024, Ouganda Anti-Homosexuality Act 2023 Peine Mort, Mauritanie Lapidation, Violence Police Impunie & ONG LGBT Fermées",
            criminalization_violence_severity_score=95.0,
            legal_protection_recognition_absence_score=93.0,
            healthcare_access_discrimination_scale_score=91.0,
            asylum_refugee_lgbtq_protection_gap_score=92.0,
            primary_pattern="criminalization_violence_severity",
        ),
        LGBTQRightsEntity(
            entity_id="LGR-002",
            name="Moyen-Orient/Iran-Arabie Saoudite — Exécutions Légales, Torture & Zéro Protection Réfugiés",
            country="Moyen-Orient",
            sector="Iran 75+ Exécutions LGBT 1979-2024 Pendaison, Arabie Saoudite Flagellation/Prison Charia, Torture Systématique, Zéro Protection Réfugiés LGBTQ+ & Surveillance Digitale Applications",
            criminalization_violence_severity_score=93.0,
            legal_protection_recognition_absence_score=91.0,
            healthcare_access_discrimination_scale_score=88.0,
            asylum_refugee_lgbtq_protection_gap_score=92.0,
            primary_pattern="criminalization_violence_severity",
        ),
        LGBTQRightsEntity(
            entity_id="LGR-003",
            name="Russie/Europe de l'Est — Loi Propagande, Chasse aux Gays Tchétchénie & Discrimination",
            country="Europe de l'Est",
            sector="Russie Loi Propagande Homosexuelle 2013/2023 Élargie, Chasse aux Gays Tchétchénie 2017-19 Camps Clandestins HRW, Kadyrov Déni Total, Criminalisation Trans Proposée & 700+ ONG Restreintes",
            criminalization_violence_severity_score=90.0,
            legal_protection_recognition_absence_score=88.0,
            healthcare_access_discrimination_scale_score=84.0,
            asylum_refugee_lgbtq_protection_gap_score=85.0,
            primary_pattern="legal_protection_recognition_absence",
        ),
        LGBTQRightsEntity(
            entity_id="LGR-004",
            name="Asie du Sud-Est/Malaisie-Brunei — Flagellation Sharia, Arrestations LGBT & Pression Sociale",
            country="Asie du Sud-Est",
            sector="Brunei Code Pénal Charia 2019 Lapidation Homosexualité, Malaisie Flagellation/Prison LGBT, Arrestations Régulières Actes Sexuels Consentis & Pression Sociale/Religieuse Extrême",
            criminalization_violence_severity_score=87.0,
            legal_protection_recognition_absence_score=85.0,
            healthcare_access_discrimination_scale_score=82.0,
            asylum_refugee_lgbtq_protection_gap_score=81.0,
            primary_pattern="criminalization_violence_severity",
        ),
        LGBTQRightsEntity(
            entity_id="LGR-005",
            name="Amérique Latine/Brésil — Assassinats Trans Record, Violence Malgré Légalisation & Impunité",
            country="Amérique Latine",
            sector="Brésil 1er Mondial Meurtres Trans 2023 TGEU, Violence LGBT Despite Mariage Légal 2013, Impunité Quasi-Totale Auteurs & Rhétorique Anti-LGBT Bolsonaro Legacy",
            criminalization_violence_severity_score=58.0,
            legal_protection_recognition_absence_score=52.0,
            healthcare_access_discrimination_scale_score=53.0,
            asylum_refugee_lgbtq_protection_gap_score=51.0,
            primary_pattern="criminalization_violence_severity",
        ),
        LGBTQRightsEntity(
            entity_id="LGR-006",
            name="USA/Régression — Lois Anti-Trans Mineurs, Books Bans & Recul Droits Post-2022",
            country="Amérique du Nord",
            sector="USA 20+ États Lois Anti-Trans Mineurs Soins Médicaux 2023, Interdictions Livres LGBT Bibliothèques, Recul Droits Post-Dobbs & Harcèlement Communauté LGBTQ+",
            criminalization_violence_severity_score=52.0,
            legal_protection_recognition_absence_score=52.0,
            healthcare_access_discrimination_scale_score=52.0,
            asylum_refugee_lgbtq_protection_gap_score=47.0,
            primary_pattern="legal_protection_recognition_absence",
        ),
        LGBTQRightsEntity(
            entity_id="LGR-007",
            name="ILGA World/Rainbow Europe — Cartographie Droits, Plaidoyer ONU & Standards Protection",
            country="Global",
            sector="ILGA World State Sponsored Homophobia Report Annuel 2024, Rainbow Europe Map Index Droits LGBTQ+, Plaidoyer CDH-ONU Résolutions & Standards Protection Internationaux",
            criminalization_violence_severity_score=28.0,
            legal_protection_recognition_absence_score=25.0,
            healthcare_access_discrimination_scale_score=24.0,
            asylum_refugee_lgbtq_protection_gap_score=26.0,
            primary_pattern="legal_protection_recognition_absence",
        ),
        LGBTQRightsEntity(
            entity_id="LGR-008",
            name="ONU/Principes Jogjakarta — Résolution HRC, Experts Indépendants & SDG Inclusion",
            country="Global",
            sector="Principes Jogjakarta 2006/2017 Cadre Normatif International, Résolution CDH-ONU SOGI, Expert Indépendant IE SOGI Mandate & SDG Inclusion Orientation Sexuelle Identité Genre",
            criminalization_violence_severity_score=5.0,
            legal_protection_recognition_absence_score=4.0,
            healthcare_access_discrimination_scale_score=3.0,
            asylum_refugee_lgbtq_protection_gap_score=4.0,
            primary_pattern="asylum_refugee_lgbtq_protection_gap",
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

    return LGBTQRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_lgbtq_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilga_world_state_sponsored_homophobia_global_legislation_report",
            "human_rights_watch_lgbtq_rights_criminalization_violence_report",
            "rainbow_europe_map_index_lgbtq_rights_comparative_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_lgbtq_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_lgbtq_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
