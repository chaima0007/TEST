"""Racial Discrimination Minority Rights Engine — CERD, Minority Rights Group & HRW."""

from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class RacialDiscriminationMinorityRightsEntity:
    entity_id: str
    name: str
    country: str
    systemic_racial_discrimination_score: float
    minority_legal_protection_gap_score: float
    racial_violence_impunity_score: float
    institutional_exclusion_score: float
    primary_pattern: str = ""
    last_updated: str = "2026-06-21"

    @property
    def composite_score(self) -> float:
        return round(
            self.systemic_racial_discrimination_score * 0.30
            + self.minority_legal_protection_gap_score * 0.25
            + self.racial_violence_impunity_score * 0.25
            + self.institutional_exclusion_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    @property
    def estimated_racial_discrimination_minority_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "composite_score": self.composite_score,
            "systemic_racial_discrimination_score": self.systemic_racial_discrimination_score,
            "minority_legal_protection_gap_score": self.minority_legal_protection_gap_score,
            "racial_violence_impunity_score": self.racial_violence_impunity_score,
            "institutional_exclusion_score": self.institutional_exclusion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "estimated_racial_discrimination_minority_rights_index": self.estimated_racial_discrimination_minority_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class RacialDiscriminationMinorityRightsEngineResult:
    agent: str = "Racial Discrimination Minority Rights Engine Agent"
    domain: str = "racial_discrimination_minority_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_racial_discrimination_minority_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RacialDiscriminationMinorityRightsEntity] = field(default_factory=list)


def run_racial_discrimination_minority_rights_engine() -> RacialDiscriminationMinorityRightsEngineResult:
    entities = [
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-001",
            name="USA/Violence Policière Raciale — Killings BLM Persistance, 1 000+ Morts/An, Disparités Raciales Justice Pénale & Sur-Incarcération Noirs 5×",
            country="USA",
            systemic_racial_discrimination_score=85.0,
            minority_legal_protection_gap_score=80.0,
            racial_violence_impunity_score=82.0,
            institutional_exclusion_score=78.0,
            primary_pattern="racial_violence_impunity",
        ),
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-002",
            name="Chine/Tibet & Xinjiang — Discrimination Ethnique Systémique, Suppression Culture Tibétaine, Assimilation Forcée Ouïghours & Persécution Religieuse",
            country="Chine",
            systemic_racial_discrimination_score=92.0,
            minority_legal_protection_gap_score=90.0,
            racial_violence_impunity_score=88.0,
            institutional_exclusion_score=85.0,
            primary_pattern="systemic_racial_discrimination",
        ),
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-003",
            name="Inde/Discrimination Castes Dalits — 200M Dalits Intouchabilité Persistante, Violences Sexuelles Dalites, Exclusion Économique & Impunité Auteurs",
            country="Inde",
            systemic_racial_discrimination_score=82.0,
            minority_legal_protection_gap_score=78.0,
            racial_violence_impunity_score=80.0,
            institutional_exclusion_score=75.0,
            primary_pattern="systemic_racial_discrimination",
        ),
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-004",
            name="Brésil/Racisme Structurel & Féminicide Noir — Noirs 75% Victimes Homicides, Féminicide Noir 2× Plus Élevé, Exclusion Socio-Économique & Impunité Persistante",
            country="Brésil",
            systemic_racial_discrimination_score=80.0,
            minority_legal_protection_gap_score=75.0,
            racial_violence_impunity_score=82.0,
            institutional_exclusion_score=72.0,
            primary_pattern="racial_violence_impunity",
        ),
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-005",
            name="Hongrie/Discrimination Roms UE — 700K Roms Ségrégation Scolaire, Exclusion Emploi, Expulsions Forcées & Discours Haineux Gouvernemental Légitimé",
            country="Hongrie",
            systemic_racial_discrimination_score=62.0,
            minority_legal_protection_gap_score=58.0,
            racial_violence_impunity_score=55.0,
            institutional_exclusion_score=65.0,
            primary_pattern="institutional_exclusion",
        ),
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-006",
            name="Israël/Palestine — Apartheid Selon HRW & Amnesty, Discrimination Systémique Arabes Israéliens, Déni Droits Palestiniens & Ségrégation Territoriale",
            country="Israël/Palestine",
            systemic_racial_discrimination_score=58.0,
            minority_legal_protection_gap_score=62.0,
            racial_violence_impunity_score=55.0,
            institutional_exclusion_score=60.0,
            primary_pattern="minority_legal_protection_gap",
        ),
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-007",
            name="France/Discrimination Institutionnelle Voilée — Rapport Défenseur des Droits: Discrimination 20% Minorités Emploi, Contrôles Faciaux, Islamophobie & Inégalités Logement",
            country="France",
            systemic_racial_discrimination_score=35.0,
            minority_legal_protection_gap_score=38.0,
            racial_violence_impunity_score=30.0,
            institutional_exclusion_score=42.0,
            primary_pattern="institutional_exclusion",
        ),
        RacialDiscriminationMinorityRightsEntity(
            entity_id="RDMR-008",
            name="Canada/TRC & Multiculturalisme — Politique Multiculturalisme Avancée, TRC 94 Appels à l'Action, Réconciliation Peuples Autochtones & Cadre Anti-Discrimination Robuste",
            country="Canada",
            systemic_racial_discrimination_score=12.0,
            minority_legal_protection_gap_score=15.0,
            racial_violence_impunity_score=10.0,
            institutional_exclusion_score=18.0,
            primary_pattern="minority_legal_protection_gap",
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

    return RacialDiscriminationMinorityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_racial_discrimination_minority_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "cerd_committee_reports_2023",
            "minority_rights_group_international_2023",
            "human_rights_watch_racial_discrimination_2022",
            "amnesty_international_systemic_racism_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_racial_discrimination_minority_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_racial_discrimination_minority_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
