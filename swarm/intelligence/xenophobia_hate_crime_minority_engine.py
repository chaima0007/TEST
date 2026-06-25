from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class XenophobiaHateCrimeMinorityEntity:
    entity_id: str
    name: str
    country: str
    state_sponsored_xenophobia_policy_score: float
    hate_crime_violence_impunity_score: float
    legal_discrimination_minority_rights_score: float
    media_political_hate_speech_normalization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_xenophobia_hate_crime_minority_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.state_sponsored_xenophobia_policy_score * 0.30
            + self.hate_crime_violence_impunity_score * 0.25
            + self.legal_discrimination_minority_rights_score * 0.25
            + self.media_political_hate_speech_normalization_score * 0.20,
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
        self.estimated_xenophobia_hate_crime_minority_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class XenophobiaHateCrimeMinorityEngineResult:
    agent: str = "Xenophobia Hate Crime Minority Engine Agent"
    domain: str = "xenophobia_hate_crime_minority"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_xenophobia_hate_crime_minority_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[XenophobiaHateCrimeMinorityEntity] = field(default_factory=list)

def run_xenophobia_hate_crime_minority_engine() -> XenophobiaHateCrimeMinorityEngineResult:
    entities = [
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-001",
            name="Myanmar — Rohingya Génocide 2017, 1M Exilés, Épithète Officielle Kalars, Armée Brûle Villages & Facebook Vecteur Haine",
            country="Asie du Sud-Est",
            state_sponsored_xenophobia_policy_score=97.0,
            hate_crime_violence_impunity_score=96.0,
            legal_discrimination_minority_rights_score=95.0,
            media_political_hate_speech_normalization_score=94.0,
            primary_pattern="state_sponsored_xenophobia_policy",
        ),
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-002",
            name="Inde/Hindutva — Vache Vigilantes Lynchages, Lois Anti-Conversion Ciblant Musulmans, Assam NRC Apatridie & BJP Rhétorique",
            country="Asie du Sud",
            state_sponsored_xenophobia_policy_score=82.0,
            hate_crime_violence_impunity_score=85.0,
            legal_discrimination_minority_rights_score=80.0,
            media_political_hate_speech_normalization_score=88.0,
            primary_pattern="hate_crime_violence_impunity",
        ),
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-003",
            name="Éthiopie/Tigray — Tigréens Ciblés Ethniquement 2020-2022, Déplacements Forcés & Discours Déshumanisant Officiels Addis Abeba",
            country="Afrique de l'Est",
            state_sponsored_xenophobia_policy_score=88.0,
            hate_crime_violence_impunity_score=90.0,
            legal_discrimination_minority_rights_score=85.0,
            media_political_hate_speech_normalization_score=88.0,
            primary_pattern="hate_crime_violence_impunity",
        ),
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-004",
            name="Hongrie/Orbán — Migrants Envahisseurs, Loi Stop Soros, Campagnes Anti-Migrants & LGBTQ Diabolisation Officielle",
            country="Europe Centrale",
            state_sponsored_xenophobia_policy_score=85.0,
            hate_crime_violence_impunity_score=62.0,
            legal_discrimination_minority_rights_score=78.0,
            media_political_hate_speech_normalization_score=92.0,
            primary_pattern="media_political_hate_speech_normalization",
        ),
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-005",
            name="USA/Far-Right 2017-2024 — Charlottesville, Pittsburgh Synagogue, Asian Hate Crimes COVID +177% & Gab/4chan Radicalisation",
            country="Amérique du Nord",
            state_sponsored_xenophobia_policy_score=48.0,
            hate_crime_violence_impunity_score=62.0,
            legal_discrimination_minority_rights_score=45.0,
            media_political_hate_speech_normalization_score=68.0,
            primary_pattern="media_political_hate_speech_normalization",
        ),
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-006",
            name="Afrique du Sud — Xénophobie Violences Récurrentes Africains Étrangers, Pogroms 2008+2019 & 12 Tués 2019",
            country="Afrique Australe",
            state_sponsored_xenophobia_policy_score=38.0,
            hate_crime_violence_impunity_score=55.0,
            legal_discrimination_minority_rights_score=42.0,
            media_political_hate_speech_normalization_score=48.0,
            primary_pattern="hate_crime_violence_impunity",
        ),
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-007",
            name="France — Gilets Jaunes Antisémitisme, Discours RN Normalisé, Crimes Islamophobes +53% 2023 & CNCDH Rapport",
            country="Europe de l'Ouest",
            state_sponsored_xenophobia_policy_score=22.0,
            hate_crime_violence_impunity_score=30.0,
            legal_discrimination_minority_rights_score=25.0,
            media_political_hate_speech_normalization_score=38.0,
            primary_pattern="media_political_hate_speech_normalization",
        ),
        XenophobiaHateCrimeMinorityEntity(
            entity_id="XHC-008",
            name="Canada/Cadre Légal — Lois Anti-Discrimination C-36, Charter Protections, BCHRT Actif & Lacunes Autochtones Persistantes",
            country="Amérique du Nord",
            state_sponsored_xenophobia_policy_score=5.0,
            hate_crime_violence_impunity_score=8.0,
            legal_discrimination_minority_rights_score=6.0,
            media_political_hate_speech_normalization_score=10.0,
            primary_pattern="legal_discrimination_minority_rights",
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

    return XenophobiaHateCrimeMinorityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_xenophobia_hate_crime_minority_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "osce_odihr_hate_crime_data_2023",
            "human_rights_watch_xenophobia_discrimination_2023",
            "amnesty_international_hate_crimes_minorities_2023",
            "un_committee_elimination_racial_discrimination_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_xenophobia_hate_crime_minority_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_xenophobia_hate_crime_minority_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
