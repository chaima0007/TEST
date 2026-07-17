from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

DOMAIN = "transgender_rights"
PREFIX = "TGR"
ACCENT_COLOR = "#1a0d26"


@dataclass
class TransgenderRightsEntity:
    entity_id: str
    name: str
    country: str
    legal_recognition_denial_score: float
    healthcare_access_barrier_score: float
    violence_discrimination_score: float
    criminalization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_transgender_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.legal_recognition_denial_score * 0.30
            + self.healthcare_access_barrier_score * 0.25
            + self.violence_discrimination_score * 0.25
            + self.criminalization_score * 0.20,
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
        self.estimated_transgender_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class TransgenderRightsEngineResult:
    agent: str = "Transgender Rights Engine Agent"
    domain: str = DOMAIN
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_transgender_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[TransgenderRightsEntity] = field(default_factory=list)


def run_transgender_rights_engine() -> TransgenderRightsEngineResult:
    entities = [
        TransgenderRightsEntity(
            entity_id="TGR-001",
            name="Iran — Chirurgie de Réassignation Forcée ou Prison, État Contrôle Corps Trans, Persécution LGBTQ+ Systémique & Peine de Mort Homosexualité",
            country="Iran",
            legal_recognition_denial_score=90.0,
            healthcare_access_barrier_score=88.0,
            violence_discrimination_score=87.0,
            criminalization_score=92.0,
            primary_pattern="criminalization",
        ),
        TransgenderRightsEntity(
            entity_id="TGR-002",
            name="Nigeria — Same-Sex Marriage Prohibition Act 14 Ans Prison, Sharia Nord Peine Mort, Arrestations Masse Personnes Trans & Violence Policière Impunie",
            country="Nigeria",
            legal_recognition_denial_score=86.0,
            healthcare_access_barrier_score=84.0,
            violence_discrimination_score=85.0,
            criminalization_score=89.0,
            primary_pattern="criminalization",
        ),
        TransgenderRightsEntity(
            entity_id="TGR-003",
            name="Arabie Saoudite — Peine de Mort Homosexualité, Fouet & Emprisonnement Identités Trans, Aucune Reconnaissance Légale & Médecins Refusant Soins LGBTQ+",
            country="Arabie Saoudite",
            legal_recognition_denial_score=83.0,
            healthcare_access_barrier_score=82.0,
            violence_discrimination_score=84.0,
            criminalization_score=87.0,
            primary_pattern="violence_discrimination",
        ),
        TransgenderRightsEntity(
            entity_id="TGR-004",
            name="Ouganda — Anti-Homosexuality Act 2023 Peine de Mort, Arrestations Défenseurs LGBTQ+, Fermeture ONG & Chasse Personnes Trans par Voisinage",
            country="Ouganda",
            legal_recognition_denial_score=80.0,
            healthcare_access_barrier_score=79.0,
            violence_discrimination_score=83.0,
            criminalization_score=85.0,
            primary_pattern="criminalization",
        ),
        TransgenderRightsEntity(
            entity_id="TGR-005",
            name="Turquie — Interdiction Pride Istanbul depuis 2015, Régression Lois Anti-Trans, Expulsions Militantes & Discours Haineux Gouvernemental Institutionnalisé",
            country="Turquie",
            legal_recognition_denial_score=60.0,
            healthcare_access_barrier_score=58.0,
            violence_discrimination_score=62.0,
            criminalization_score=55.0,
            primary_pattern="violence_discrimination",
        ),
        TransgenderRightsEntity(
            entity_id="TGR-006",
            name="Brésil — 140+ Féminicides Trans/Année, Premier Pays Meurtres Trans Monde, Progrès Légaux Contredits par Violence Quotidienne & Impunité Judicaire",
            country="Brésil",
            legal_recognition_denial_score=57.0,
            healthcare_access_barrier_score=55.0,
            violence_discrimination_score=65.0,
            criminalization_score=48.0,
            primary_pattern="violence_discrimination",
        ),
        TransgenderRightsEntity(
            entity_id="TGR-007",
            name="USA — Progress Mariage Égal mais Recul Certains États, Lois Anti-Trans Mineurs 20+ États, Accès Soins Bloqué & Discrimination Militaire Réintroduite",
            country="USA",
            legal_recognition_denial_score=38.0,
            healthcare_access_barrier_score=40.0,
            violence_discrimination_score=35.0,
            criminalization_score=30.0,
            primary_pattern="healthcare_access_barrier",
        ),
        TransgenderRightsEntity(
            entity_id="TGR-008",
            name="Islande — Reconnaissance Légale Genre par Auto-Détermination depuis 2019, Soins Trans Gratuits Système Public, Modèle Nordique Droits Trans & Zéro Criminalisation",
            country="Islande",
            legal_recognition_denial_score=8.0,
            healthcare_access_barrier_score=7.0,
            violence_discrimination_score=6.0,
            criminalization_score=5.0,
            primary_pattern="legal_recognition_denial",
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

    return TransgenderRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_transgender_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "trans_murder_monitoring_tmm_annual_report",
            "ilga_world_state_sponsored_homophobia_report",
            "hrw_transgender_rights_violations_global",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_transgender_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_transgender_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
