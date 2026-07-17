from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

DOMAIN = "housing_eviction_rights"
PREFIX = "HER"
ACCENT_COLOR = "#1a1206"


@dataclass
class HousingEvictionRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_eviction_scale_score: float
    affordable_housing_deficit_score: float
    homelessness_criminalization_score: float
    security_tenure_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_housing_eviction_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_eviction_scale_score * 0.30
            + self.affordable_housing_deficit_score * 0.25
            + self.homelessness_criminalization_score * 0.25
            + self.security_tenure_absence_score * 0.20,
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
        self.estimated_housing_eviction_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class HousingEvictionRightsEngineResult:
    agent: str = "Housing Eviction Rights Engine Agent"
    domain: str = DOMAIN
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_housing_eviction_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HousingEvictionRightsEntity] = field(default_factory=list)


def run_housing_eviction_rights_engine() -> HousingEvictionRightsEngineResult:
    entities = [
        HousingEvictionRightsEntity(
            entity_id="HER-001",
            name="Kenya/Mathare — 500 000 Résidents Bidonvilles Évictions Massives Sans Préavis, Démolitions Nocturnes, Zéro Relogement & Tenure Légale Inexistante",
            country="Kenya",
            forced_eviction_scale_score=92.0,
            affordable_housing_deficit_score=90.0,
            homelessness_criminalization_score=88.0,
            security_tenure_absence_score=91.0,
            primary_pattern="forced_eviction_scale",
        ),
        HousingEvictionRightsEntity(
            entity_id="HER-002",
            name="Philippines/Manila — Smoky Mountain & Tondo Démolitions, 3M Résidents Bidonvilles Menacés, Relocalisation Périphérie Éloignée & Expulsions Liées Développement",
            country="Philippines",
            forced_eviction_scale_score=88.0,
            affordable_housing_deficit_score=86.0,
            homelessness_criminalization_score=85.0,
            security_tenure_absence_score=88.0,
            primary_pattern="security_tenure_absence",
        ),
        HousingEvictionRightsEntity(
            entity_id="HER-003",
            name="Brésil/Favelas — 11M Habitants Favelas, Opérations Policières+Démolitions, Vila Autódromo Rio Modèle Résistance & Pacification Précède Éviction",
            country="Brésil",
            forced_eviction_scale_score=85.0,
            affordable_housing_deficit_score=83.0,
            homelessness_criminalization_score=82.0,
            security_tenure_absence_score=84.0,
            primary_pattern="affordable_housing_deficit",
        ),
        HousingEvictionRightsEntity(
            entity_id="HER-004",
            name="Inde/Mumbai — Dharavi 1M Résidents Menacés Redéveloppement, Démolitions Slums 100 000+/An, Procédures Expulsion Accélérées & Adivasi Terres Spoliées",
            country="Inde",
            forced_eviction_scale_score=82.0,
            affordable_housing_deficit_score=80.0,
            homelessness_criminalization_score=79.0,
            security_tenure_absence_score=80.0,
            primary_pattern="forced_eviction_scale",
        ),
        HousingEvictionRightsEntity(
            entity_id="HER-005",
            name="USA — 650 000 Sans-Abri Criminalisés par Anti-Camping Lois, Crise Logement Abordable 7M Unités Manquantes, Expulsions Masse Post-COVID & Sweep Encampments",
            country="USA",
            forced_eviction_scale_score=58.0,
            affordable_housing_deficit_score=56.0,
            homelessness_criminalization_score=61.0,
            security_tenure_absence_score=52.0,
            primary_pattern="homelessness_criminalization",
        ),
        HousingEvictionRightsEntity(
            entity_id="HER-006",
            name="France — 200 000 Expulsions Locatives/An, Trêve Hivernale Insuffisante, 4M Personnes Mal-Logées SDF+Bidonvilles & Migrants Campements Systématiquement Démantelés",
            country="France",
            forced_eviction_scale_score=58.0,
            affordable_housing_deficit_score=57.0,
            homelessness_criminalization_score=56.0,
            security_tenure_absence_score=52.0,
            primary_pattern="affordable_housing_deficit",
        ),
        HousingEvictionRightsEntity(
            entity_id="HER-007",
            name="Allemagne — Protections Locataires Kündigung 3 Mois Préavis, Mietpreisbremse mais Gentrification Berlin Contourne Protections & Lacunes Logement Social",
            country="Allemagne",
            forced_eviction_scale_score=35.0,
            affordable_housing_deficit_score=38.0,
            homelessness_criminalization_score=32.0,
            security_tenure_absence_score=30.0,
            primary_pattern="affordable_housing_deficit",
        ),
        HousingEvictionRightsEntity(
            entity_id="HER-008",
            name="Autriche — Droit au Logement Constitutionnel Inscrit 2012, Wiener Wohnen 220 000 Logements Sociaux Vienne, Modèle Européen Bail Long Terme & Expulsions Encadrées",
            country="Autriche",
            forced_eviction_scale_score=11.0,
            affordable_housing_deficit_score=10.0,
            homelessness_criminalization_score=9.0,
            security_tenure_absence_score=10.0,
            primary_pattern="forced_eviction_scale",
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

    return HousingEvictionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_housing_eviction_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_habitat_forced_evictions_global_report",
            "cohre_housing_rights_violations_database",
            "feantsa_homelessness_europe_annual_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_housing_eviction_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_housing_eviction_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
