from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EconomicSocialRightsEntity:
    entity_id: str
    name: str
    country: str
    labour_rights_union_freedom_violation_score: float
    social_security_healthcare_collapse_score: float
    economic_inequality_extreme_poverty_score: float
    state_corporate_labour_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_economic_social_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.labour_rights_union_freedom_violation_score * 0.30
            + self.social_security_healthcare_collapse_score * 0.25
            + self.economic_inequality_extreme_poverty_score * 0.25
            + self.state_corporate_labour_impunity_score * 0.20,
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
        self.estimated_economic_social_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class EconomicSocialRightsEngineResult:
    agent: str = "Economic Social Rights Engine Agent"
    domain: str = "economic_social_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_economic_social_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EconomicSocialRightsEntity] = field(default_factory=list)


def run_economic_social_rights_engine() -> EconomicSocialRightsEngineResult:
    entities = [
        EconomicSocialRightsEntity(
            entity_id="ESR-001",
            name="Corée du Nord — Zéro Liberté Syndicale, Travail Forcé d'État Systématique, Pas de Sécurité Sociale & Économie Captive Régime",
            country="Corée du Nord",
            labour_rights_union_freedom_violation_score=99.0,
            social_security_healthcare_collapse_score=96.0,
            economic_inequality_extreme_poverty_score=97.0,
            state_corporate_labour_impunity_score=99.0,
            primary_pattern="labour_rights_union_freedom_violation",
        ),
        EconomicSocialRightsEntity(
            entity_id="ESR-002",
            name="Yémen — Infrastructures Sanitaires Détruites à 70%, 21M Sans Soins Adéquats, Famine & Effondrement Total Sécurité Sociale",
            country="Yémen",
            labour_rights_union_freedom_violation_score=91.0,
            social_security_healthcare_collapse_score=97.0,
            economic_inequality_extreme_poverty_score=95.0,
            state_corporate_labour_impunity_score=90.0,
            primary_pattern="social_security_healthcare_collapse",
        ),
        EconomicSocialRightsEntity(
            entity_id="ESR-003",
            name="Venezuela — Hyperinflation Destruction Sécurité Sociale, 7M Émigrés Fuient Pauvreté & Services Publics Effondrés",
            country="Venezuela",
            labour_rights_union_freedom_violation_score=88.0,
            social_security_healthcare_collapse_score=92.0,
            economic_inequality_extreme_poverty_score=91.0,
            state_corporate_labour_impunity_score=85.0,
            primary_pattern="social_security_healthcare_collapse",
        ),
        EconomicSocialRightsEntity(
            entity_id="ESR-004",
            name="Zimbabwe — Effondrement Services Publics, Droit Santé Violé, Chômage 90% & Travailleurs Sans Filet Social Légal",
            country="Zimbabwe",
            labour_rights_union_freedom_violation_score=85.0,
            social_security_healthcare_collapse_score=89.0,
            economic_inequality_extreme_poverty_score=88.0,
            state_corporate_labour_impunity_score=84.0,
            primary_pattern="economic_inequality_extreme_poverty",
        ),
        EconomicSocialRightsEntity(
            entity_id="ESR-005",
            name="Inde — Codes Labor 2020 Régressifs, 500M Travailleurs Informels Non-Protégés & Syndicats Réprimés Hindutva",
            country="Inde",
            labour_rights_union_freedom_violation_score=59.0,
            social_security_healthcare_collapse_score=52.0,
            economic_inequality_extreme_poverty_score=55.0,
            state_corporate_labour_impunity_score=57.0,
            primary_pattern="labour_rights_union_freedom_violation",
        ),
        EconomicSocialRightsEntity(
            entity_id="ESR-006",
            name="Bangladesh — Grèves Garment Réprimées, 4M Ouvrières Textiles Sans Protection Adéquate & Rana Plaza Impunité Persistante",
            country="Bangladesh",
            labour_rights_union_freedom_violation_score=57.0,
            social_security_healthcare_collapse_score=50.0,
            economic_inequality_extreme_poverty_score=53.0,
            state_corporate_labour_impunity_score=55.0,
            primary_pattern="state_corporate_labour_impunity",
        ),
        EconomicSocialRightsEntity(
            entity_id="ESR-007",
            name="Brésil — Réforme Retraite Lula Partielle, Inégalités Raciales Persistantes & Précarisation Travailleurs Plateforme",
            country="Brésil",
            labour_rights_union_freedom_violation_score=28.0,
            social_security_healthcare_collapse_score=26.0,
            economic_inequality_extreme_poverty_score=30.0,
            state_corporate_labour_impunity_score=27.0,
            primary_pattern="economic_inequality_extreme_poverty",
        ),
        EconomicSocialRightsEntity(
            entity_id="ESR-008",
            name="Norvège — Modèle Nordique, Droits Sociaux Constitutionnels, Syndicats 70% Adhésion & Protection Universelle",
            country="Norvège",
            labour_rights_union_freedom_violation_score=5.0,
            social_security_healthcare_collapse_score=4.0,
            economic_inequality_extreme_poverty_score=5.0,
            state_corporate_labour_impunity_score=4.0,
            primary_pattern="labour_rights_union_freedom_violation",
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

    return EconomicSocialRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_economic_social_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ituc_global_rights_index_2023",
            "ilo_world_employment_social_outlook_2023",
            "un_sr_extreme_poverty_2023",
            "oxfam_inequality_report_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_economic_social_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_economic_social_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
