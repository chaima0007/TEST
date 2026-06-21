"""Reproductive Rights Engine — Avortement, mortalité maternelle, contraception & stérilisation forcée."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class ReproductiveRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    abortion_access_criminalization_severity_score: float
    maternal_mortality_healthcare_gap_score: float
    contraception_sex_education_exclusion_score: float
    forced_sterilization_coercion_scale_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_reproductive_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.abortion_access_criminalization_severity_score * 0.30
            + self.maternal_mortality_healthcare_gap_score * 0.25
            + self.contraception_sex_education_exclusion_score * 0.25
            + self.forced_sterilization_coercion_scale_score * 0.20,
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
        self.estimated_reproductive_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ReproductiveRightsEngineResult:
    agent: str = "Reproductive Rights Engine Agent"
    domain: str = "reproductive_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_reproductive_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ReproductiveRightsEntity] = field(default_factory=list)


def run_reproductive_rights_engine() -> ReproductiveRightsEngineResult:
    entities = [
        ReproductiveRightsEntity(
            entity_id="RPR-001",
            name="Afrique Sub-Saharienne — Avortement Illégal 90% Pays, Mortalité 545/100k & Stérilisation Forcée",
            country="Afrique Sub-Saharienne",
            sector="Avortement Illégal ou Très Restreint 90% Pays Afrique Sub-Saharienne WHO, Mortalité Maternelle 545/100 000 Naissances OMS 2023, Stérilisation Forcée Femmes Pauvres & Accès Contraception 25%",
            abortion_access_criminalization_severity_score=96.0,
            maternal_mortality_healthcare_gap_score=92.0,
            contraception_sex_education_exclusion_score=91.0,
            forced_sterilization_coercion_scale_score=91.0,
            primary_pattern="abortion_access_criminalization_severity",
        ),
        ReproductiveRightsEntity(
            entity_id="RPR-002",
            name="Amérique Latine — El Salvador/Nicaragua Avortement Total Ban & Emprisonnement Fausses Couches",
            country="Amérique Latine",
            sector="El Salvador/Nicaragua Avortement Total Interdit Sans Exception, Femmes Emprisonnées Pour Fausses Couches, Violences Obstétriques Systématiques Honduras/Guatemala & Mortalité Maternelle 193/100k",
            abortion_access_criminalization_severity_score=93.0,
            maternal_mortality_healthcare_gap_score=89.0,
            contraception_sex_education_exclusion_score=89.0,
            forced_sterilization_coercion_scale_score=88.0,
            primary_pattern="abortion_access_criminalization_severity",
        ),
        ReproductiveRightsEntity(
            entity_id="RPR-003",
            name="Asie du Sud/Inde — Stérilisation Forcée Femmes Pauvres, Mortalité Rurale & Contraception Inégale",
            country="Asie du Sud",
            sector="Inde Stérilisation Forcée Femmes Pauvres/Dalit Camps NHRC, Mortalité Maternelle Rurale 197/100k, Accès Contraception Inégal Rural/Urbain & Mariage Précoce 23% Filles",
            abortion_access_criminalization_severity_score=88.0,
            maternal_mortality_healthcare_gap_score=88.0,
            contraception_sex_education_exclusion_score=86.0,
            forced_sterilization_coercion_scale_score=87.0,
            primary_pattern="maternal_mortality_healthcare_gap",
        ),
        ReproductiveRightsEntity(
            entity_id="RPR-004",
            name="USA post-Dobbs — 14 États Ban Total Avortement, Criminalisation Médecins & Contraception Menacée",
            country="Amérique du Nord",
            sector="USA 14 États Ban Total Avortement Post-Dobbs 2022, Médecins Poursuivis Pénalement, Pillules Contraceptives Remises en Question & Femmes Forcées Voyager 1 000+ Km Pour Soins",
            abortion_access_criminalization_severity_score=87.0,
            maternal_mortality_healthcare_gap_score=82.0,
            contraception_sex_education_exclusion_score=83.0,
            forced_sterilization_coercion_scale_score=82.0,
            primary_pattern="abortion_access_criminalization_severity",
        ),
        ReproductiveRightsEntity(
            entity_id="RPR-005",
            name="Europe de l'Est/Pologne — Quasi-Ban Avortement, Femmes Décédées & Pression Église",
            country="Europe de l'Est",
            sector="Pologne Quasi-Ban Avortement 2021 Arrêt Tribunal Constitutionnel, 5 Femmes Décédées Faute Soins Documentées, Pression Église Catholique & Femmes Contraintes Avorter Étranger",
            abortion_access_criminalization_severity_score=57.0,
            maternal_mortality_healthcare_gap_score=52.0,
            contraception_sex_education_exclusion_score=53.0,
            forced_sterilization_coercion_scale_score=52.0,
            primary_pattern="abortion_access_criminalization_severity",
        ),
        ReproductiveRightsEntity(
            entity_id="RPR-006",
            name="Moyen-Orient — Avortement Illégal Majorité Pays, Mariage Forcé Précoce & Honour Crimes",
            country="Moyen-Orient",
            sector="Avortement Illégal 90% Pays MENA Sauf Tunisie/Turquie, Mariage Enfants 40% Filles Yemen, Honour Crimes Impunis Jordanie/Irak & Mortalité Maternelle 210/100k",
            abortion_access_criminalization_severity_score=53.0,
            maternal_mortality_healthcare_gap_score=50.0,
            contraception_sex_education_exclusion_score=51.0,
            forced_sterilization_coercion_scale_score=50.0,
            primary_pattern="abortion_access_criminalization_severity",
        ),
        ReproductiveRightsEntity(
            entity_id="RPR-007",
            name="IPPF/UNFPA — Plaidoyer Droits Reproductifs, Accès Planning Familial & ICPD+30",
            country="Global",
            sector="IPPF International Planned Parenthood Federation 120 Pays, UNFPA Fonds Population ONU, Accès Planning Familial Universel SDG 3.7 & ICPD+30 Programme Action 2024",
            abortion_access_criminalization_severity_score=28.0,
            maternal_mortality_healthcare_gap_score=25.0,
            contraception_sex_education_exclusion_score=25.0,
            forced_sterilization_coercion_scale_score=26.0,
            primary_pattern="contraception_sex_education_exclusion",
        ),
        ReproductiveRightsEntity(
            entity_id="RPR-008",
            name="ONU/CEDAW — Convention Discrimination Femmes, Rapporteur Santé & SDG 3.1 Mortalité",
            country="Global",
            sector="CEDAW Convention Élimination Discrimination Femmes 189 États, Rapporteur Spécial ONU Droit Santé, SDG 3.1 Mortalité Maternelle <70/100k 2030 & Comité CEDAW Recommandation Générale 24",
            abortion_access_criminalization_severity_score=5.0,
            maternal_mortality_healthcare_gap_score=3.0,
            contraception_sex_education_exclusion_score=4.0,
            forced_sterilization_coercion_scale_score=4.0,
            primary_pattern="maternal_mortality_healthcare_gap",
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

    return ReproductiveRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_reproductive_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_global_abortion_policies_database_unsafe_abortion_report",
            "guttmacher_institute_abortion_worldwide_report_incidence_safety",
            "amnesty_international_bodily_autonomy_reproductive_rights_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_reproductive_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_reproductive_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
