from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class LgbtqRightsCriminalizationEntity:
    entity_id: str
    name: str
    country: str
    state_criminalization_imprisonment_severity_score: float
    violence_persecution_impunity_scale_score: float
    legal_identity_recognition_denial_score: float
    anti_lgbtq_legislation_rollback_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_lgbtq_rights_criminalization_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.state_criminalization_imprisonment_severity_score * 0.30
            + self.violence_persecution_impunity_scale_score * 0.25
            + self.legal_identity_recognition_denial_score * 0.25
            + self.anti_lgbtq_legislation_rollback_deficit_gap_score * 0.20,
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
        self.estimated_lgbtq_rights_criminalization_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class LgbtqRightsCriminalizationEngineResult:
    agent: str = "LGBTQ+ Rights Criminalization Engine Agent"
    domain: str = "lgbtq_rights_criminalization"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_lgbtq_rights_criminalization_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LgbtqRightsCriminalizationEntity] = field(default_factory=list)


def run_lgbtq_rights_criminalization_engine() -> LgbtqRightsCriminalizationEngineResult:
    entities = [
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-001",
            name="Ouganda/Anti-Homosexuality Act 2023 — Peine Mort Homosexualité Aggravée, Perpétuité Simple, Dénonciation Obligatoire & 1 000+ Arrestations",
            country="Ouganda",
            state_criminalization_imprisonment_severity_score=97.0,
            violence_persecution_impunity_scale_score=95.0,
            legal_identity_recognition_denial_score=96.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=94.0,
            primary_pattern="state_criminalization_imprisonment_severity",
        ),
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-002",
            name="Iran/République Islamique — Peine Mort Sodomie Codifiée Penal, 4 000+ Exécutions LGBTQ+ depuis 1979, Conversion Forcée & Chirurgie Trans Coercitive",
            country="Iran",
            state_criminalization_imprisonment_severity_score=94.0,
            violence_persecution_impunity_scale_score=93.0,
            legal_identity_recognition_denial_score=92.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=91.0,
            primary_pattern="state_criminalization_imprisonment_severity",
        ),
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-003",
            name="Arabie Saoudite/Châtiments Corporels — Flagellation & Décapitation Charia, Aucun Statut Légal, Police Morale & Expatriés LGBTQ+ Expulsés",
            country="Arabie Saoudite",
            state_criminalization_imprisonment_severity_score=91.0,
            violence_persecution_impunity_scale_score=90.0,
            legal_identity_recognition_denial_score=93.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=89.0,
            primary_pattern="legal_identity_recognition_denial",
        ),
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-004",
            name="Tchétchénie/Camps Purge — Opération Nettoyage 2017-2019, 150+ Hommes Détenus Camps Secrets, Tortures & Familles Invitées Tuer Membres LGBTQ+",
            country="Russie/Tchétchénie",
            state_criminalization_imprisonment_severity_score=88.0,
            violence_persecution_impunity_scale_score=92.0,
            legal_identity_recognition_denial_score=87.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=90.0,
            primary_pattern="violence_persecution_impunity_scale",
        ),
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-005",
            name="Russie/Loi Propagande — Propagande LGBTQ+ Interdite Tous Âges 2023, Organisations Liquidées, Médias Censurés & Amendes Massives",
            country="Russie",
            state_criminalization_imprisonment_severity_score=57.0,
            violence_persecution_impunity_scale_score=55.0,
            legal_identity_recognition_denial_score=58.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=56.0,
            primary_pattern="anti_lgbtq_legislation_rollback_deficit_gap",
        ),
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-006",
            name="Nigeria/Sharia Peine Mort — 12 États Sharia Peine Mort Homosexualité, Loi Same-Sex Prohibition 14 Ans Prison & Lynchages Communautaires",
            country="Nigeria",
            state_criminalization_imprisonment_severity_score=54.0,
            violence_persecution_impunity_scale_score=52.0,
            legal_identity_recognition_denial_score=55.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=53.0,
            primary_pattern="state_criminalization_imprisonment_severity",
        ),
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-007",
            name="ILGA/Rainbow Europe — Cartographie 64 Pays Criminalisation, Baromètre Droits LGBTQ+, Score Moyen Europe 49% & Rapport Annuel Violations",
            country="Global",
            state_criminalization_imprisonment_severity_score=27.0,
            violence_persecution_impunity_scale_score=25.0,
            legal_identity_recognition_denial_score=26.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=28.0,
            primary_pattern="anti_lgbtq_legislation_rollback_deficit_gap",
        ),
        LgbtqRightsCriminalizationEntity(
            entity_id="LRC-008",
            name="ONU/Principes Yogyakarta — 29 Principes Application Droit International Orientation Sexuelle 2006, Résolution UNHRC & Expert Indépendant SOGI",
            country="Global",
            state_criminalization_imprisonment_severity_score=5.0,
            violence_persecution_impunity_scale_score=4.0,
            legal_identity_recognition_denial_score=4.0,
            anti_lgbtq_legislation_rollback_deficit_gap_score=5.0,
            primary_pattern="legal_identity_recognition_denial",
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

    return LgbtqRightsCriminalizationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_lgbtq_rights_criminalization_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilga_world_state_sponsored_homophobia_report",
            "hrw_lgbtq_rights_violations_global_documentation",
            "amnesty_international_lgbtq_persecution_annual_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_lgbtq_rights_criminalization_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_lgbtq_rights_criminalization_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
