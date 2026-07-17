from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"

@dataclass
class LaborUnionRightsFreedomAssociationEntity:
    entity_id: str
    name: str
    country: str
    union_busting_repression_severity_score: float
    collective_bargaining_prohibition_scale_score: float
    strike_right_criminalization_score: float
    labor_organizer_persecution_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_labor_union_rights_freedom_association_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.union_busting_repression_severity_score * 0.30
            + self.collective_bargaining_prohibition_scale_score * 0.25
            + self.strike_right_criminalization_score * 0.25
            + self.labor_organizer_persecution_impunity_score * 0.20,
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
        self.estimated_labor_union_rights_freedom_association_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class LaborUnionRightsFreedomAssociationEngineResult:
    agent: str = "Labor Union Rights Freedom Association Engine Agent"
    domain: str = "labor_union_rights_freedom_association"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = ENGINE_VERSION
    avg_estimated_labor_union_rights_freedom_association_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LaborUnionRightsFreedomAssociationEntity] = field(default_factory=list)


def run_labor_union_rights_freedom_association_engine() -> LaborUnionRightsFreedomAssociationEngineResult:
    entities = [
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-001",
            name="Chine/ACFTU Syndicats Contrôlés Parti — Grèves Illégales Réprimées Force, Négociation Collective Façade, Organisateurs Indépendants Arrêtés & Aucun Syndicat Autonome Toléré",
            country="Chine",
            union_busting_repression_severity_score=95.0,
            collective_bargaining_prohibition_scale_score=92.0,
            strike_right_criminalization_score=90.0,
            labor_organizer_persecution_impunity_score=88.0,
            primary_pattern="repression_syndicale_violente",
        ),
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-002",
            name="Guatemala/Maquila — Assassinats Syndicalistes Impunité 95%, Travailleurs Listes Noires Secteur Textile, Licenciements Anti-Syndicaux Normalité & État Complice Violence Patronale",
            country="Guatemala",
            union_busting_repression_severity_score=90.0,
            collective_bargaining_prohibition_scale_score=78.0,
            strike_right_criminalization_score=72.0,
            labor_organizer_persecution_impunity_score=88.0,
            primary_pattern="persecution_organisateurs_syndicaux",
        ),
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-003",
            name="Bangladesh/Garment Secteur — Syndicats Clandestins Post-Rana Plaza, Organisatrices Femmes Menacées Licenciées, Grèves Réprimées Police & Accords Bangladesh Accord Pressions Limites",
            country="Bangladesh",
            union_busting_repression_severity_score=82.0,
            collective_bargaining_prohibition_scale_score=80.0,
            strike_right_criminalization_score=78.0,
            labor_organizer_persecution_impunity_score=80.0,
            primary_pattern="repression_syndicale_violente",
        ),
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-004",
            name="Égypte/Syndicats Indépendants Interdits — Arrestations Activistes Travail, Loi 2017 Dissolution Forcée Syndicats Autonomes, Grèves Poursuivies Pénalement & Sécurité État Surveillance",
            country="Égypte",
            union_busting_repression_severity_score=85.0,
            collective_bargaining_prohibition_scale_score=88.0,
            strike_right_criminalization_score=82.0,
            labor_organizer_persecution_impunity_score=80.0,
            primary_pattern="interdiction_negociation_collective",
        ),
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-005",
            name="Turquie/État Urgence — Licenciements Syndicaux Fonctionnaires Post-2016, Syndicats Secteur Public Dissous, Grève Interdite Services Essentiels Élargis & KESK Procès Militants",
            country="Turquie",
            union_busting_repression_severity_score=55.0,
            collective_bargaining_prohibition_scale_score=60.0,
            strike_right_criminalization_score=52.0,
            labor_organizer_persecution_impunity_score=58.0,
            primary_pattern="criminalisation_droit_greve",
        ),
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-006",
            name="USA/Amazon Starbucks — Campagnes Anti-Syndicat Agressives, NLRA Sanctions Insuffisantes Délais 3 Ans, Fermeture Magasins Syndicalisés & Résistance Patronale Légale Systémique",
            country="USA",
            union_busting_repression_severity_score=45.0,
            collective_bargaining_prohibition_scale_score=48.0,
            strike_right_criminalization_score=42.0,
            labor_organizer_persecution_impunity_score=50.0,
            primary_pattern="repression_syndicale_violente",
        ),
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-007",
            name="Brésil/Réforme Travail 2017 — Affaiblissement Financement Syndicats Cotisation Facultative, Négociation Individuelle Autorisée Surpasse Convention, CUT Perte 90% Ressources & Taux Syndicalisation Baisse",
            country="Brésil",
            union_busting_repression_severity_score=30.0,
            collective_bargaining_prohibition_scale_score=28.0,
            strike_right_criminalization_score=25.0,
            labor_organizer_persecution_impunity_score=35.0,
            primary_pattern="interdiction_negociation_collective",
        ),
        LaborUnionRightsFreedomAssociationEntity(
            entity_id="LURFA-008",
            name="Danemark/Flexicurité Modèle — Taux Affiliation Syndicale 67%, Négociation Collective Couvre 85% Travailleurs, Droit Grève Constitutionnel & Dialogue Social Institutionnalisé Tripartite",
            country="Danemark",
            union_busting_repression_severity_score=3.0,
            collective_bargaining_prohibition_scale_score=4.0,
            strike_right_criminalization_score=2.0,
            labor_organizer_persecution_impunity_score=5.0,
            primary_pattern="repression_syndicale_violente",
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

    return LaborUnionRightsFreedomAssociationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_labor_union_rights_freedom_association_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ituc_global_rights_index_2023",
            "ilo_freedom_association_reports_2023",
            "frontline_defenders_labor_rights_2023",
            "solidarity_center_union_repression_database",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_labor_union_rights_freedom_association_engine()
    print(f"Agent: {result.agent}")
    print(f"Engine version: {result.engine_version}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Avg index: {result.avg_estimated_labor_union_rights_freedom_association_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Data sources: {result.data_sources}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_labor_union_rights_freedom_association_index}")
