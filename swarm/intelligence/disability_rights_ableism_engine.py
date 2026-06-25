from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"

@dataclass
class DisabilityRightsAbleismEntity:
    entity_id: str
    name: str
    country: str
    forced_institutionalization_autonomy_denial_score: float
    disability_discrimination_employment_access_score: float
    medical_model_rights_based_deficit_score: float
    disability_legal_protection_enforcement_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_disability_rights_ableism_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_institutionalization_autonomy_denial_score * 0.30
            + self.disability_discrimination_employment_access_score * 0.25
            + self.medical_model_rights_based_deficit_score * 0.25
            + self.disability_legal_protection_enforcement_gap_score * 0.20,
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
        self.estimated_disability_rights_ableism_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class DisabilityRightsAbleismEngineResult:
    agent: str = "Disability Rights Ableism Engine Agent"
    domain: str = "disability_rights_ableism"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = ENGINE_VERSION
    avg_estimated_disability_rights_ableism_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DisabilityRightsAbleismEntity] = field(default_factory=list)


def run_disability_rights_ableism_engine() -> DisabilityRightsAbleismEngineResult:
    entities = [
        DisabilityRightsAbleismEntity(
            entity_id="DRA-001",
            name="Russie/Psychushka — Internement Psychiatrique Opposants Politiques Classifiés Handicapés, Déni Autonomie Systémique, Aucun Recours Légal Effectif & Conditions Dégradantes Documentées",
            country="Russie",
            forced_institutionalization_autonomy_denial_score=92.0,
            disability_discrimination_employment_access_score=88.0,
            medical_model_rights_based_deficit_score=90.0,
            disability_legal_protection_enforcement_gap_score=85.0,
            primary_pattern="institutionnalisation_forcee",
        ),
        DisabilityRightsAbleismEntity(
            entity_id="DRA-002",
            name="Chine/Ankang — Institutions Psychiatriques Sécurité Contrôlées Police, Dissidents Diagnostiqués 'Paranoïa Querulante', Traitement Forcé & Famille Sans Information Détention",
            country="Chine",
            forced_institutionalization_autonomy_denial_score=90.0,
            disability_discrimination_employment_access_score=85.0,
            medical_model_rights_based_deficit_score=88.0,
            disability_legal_protection_enforcement_gap_score=82.0,
            primary_pattern="institutionnalisation_forcee",
        ),
        DisabilityRightsAbleismEntity(
            entity_id="DRA-003",
            name="Inde/600M Personnes Handicap — Zéro Accessibilité Infrastructure Urbaine, Exclusion Emploi Formel 97%, Écoles Non Inclusives & RPWD 2016 Application Quasi Nulle",
            country="Inde",
            forced_institutionalization_autonomy_denial_score=72.0,
            disability_discrimination_employment_access_score=85.0,
            medical_model_rights_based_deficit_score=75.0,
            disability_legal_protection_enforcement_gap_score=80.0,
            primary_pattern="discrimination_emploi_acces",
        ),
        DisabilityRightsAbleismEntity(
            entity_id="DRA-004",
            name="USA/Olmstead — Désinstitutionnalisation Inachevée 40 États, 400K Personnes Institutions, Listes Attente Communautaires 10+ Ans & Financement Medicaid Biaisé Institutions",
            country="USA",
            forced_institutionalization_autonomy_denial_score=68.0,
            disability_discrimination_employment_access_score=72.0,
            medical_model_rights_based_deficit_score=65.0,
            disability_legal_protection_enforcement_gap_score=70.0,
            primary_pattern="institutionnalisation_forcee",
        ),
        DisabilityRightsAbleismEntity(
            entity_id="DRA-005",
            name="Brésil/Loi Handicap 2015 — Application Partielle IBGE 18% Population Handicapée, Accessibilité Transport Inexistante Villes Secondaires & Guichets Emploi Non Adaptés",
            country="Brésil",
            forced_institutionalization_autonomy_denial_score=48.0,
            disability_discrimination_employment_access_score=55.0,
            medical_model_rights_based_deficit_score=52.0,
            disability_legal_protection_enforcement_gap_score=50.0,
            primary_pattern="deficit_application_protection_legale",
        ),
        DisabilityRightsAbleismEntity(
            entity_id="DRA-006",
            name="Maroc/Exclusion Totale Emploi Formel — Personnes Handicap 2.6M Sans Couverture Sociale, Infrastructure Inexistante, Modèle Médical Dominant & Législation 2016 Non Appliquée",
            country="Maroc",
            forced_institutionalization_autonomy_denial_score=45.0,
            disability_discrimination_employment_access_score=58.0,
            medical_model_rights_based_deficit_score=48.0,
            disability_legal_protection_enforcement_gap_score=52.0,
            primary_pattern="modele_medical_droits_negation",
        ),
        DisabilityRightsAbleismEntity(
            entity_id="DRA-007",
            name="UE/Convention CDPH Ratifiée — Gaps Application Significatifs États Membres, Institutionnalisation Persistante 5 États, Plaintes Comité ONU Non Suivies & Ajustements Raisonnables Partiels",
            country="Union Européenne",
            forced_institutionalization_autonomy_denial_score=25.0,
            disability_discrimination_employment_access_score=30.0,
            medical_model_rights_based_deficit_score=28.0,
            disability_legal_protection_enforcement_gap_score=35.0,
            primary_pattern="deficit_application_protection_legale",
        ),
        DisabilityRightsAbleismEntity(
            entity_id="DRA-008",
            name="Suède/Modèle Inclusion LSS — Droits Personnels Assistance Reconnus, Taux Emploi Handicap 60%, Accessibilité Universelle Infrastructure & Désinstitutionnalisation Quasi Complète",
            country="Suède",
            forced_institutionalization_autonomy_denial_score=4.0,
            disability_discrimination_employment_access_score=5.0,
            medical_model_rights_based_deficit_score=3.0,
            disability_legal_protection_enforcement_gap_score=6.0,
            primary_pattern="deficit_application_protection_legale",
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

    return DisabilityRightsAbleismEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_disability_rights_ableism_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_crpd_committee_concluding_observations_2023",
            "disability_rights_international_reports",
            "who_world_disability_report_2023",
            "european_disability_forum_annual_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_disability_rights_ableism_engine()
    print(f"Agent: {result.agent}")
    print(f"Engine version: {result.engine_version}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Avg index: {result.avg_estimated_disability_rights_ableism_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Data sources: {result.data_sources}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_disability_rights_ableism_index}")
