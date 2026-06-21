from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class BioethicsGeneticPrivacyRightsEntity:
    entity_id: str
    name: str
    country: str
    genome_editing_embryo_ethics_severity_score: float
    genetic_database_state_surveillance_scale_score: float
    insurance_employment_genetic_discrimination_score: float
    informed_consent_biobank_research_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_bioethics_genetic_privacy_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.genome_editing_embryo_ethics_severity_score * 0.30
            + self.genetic_database_state_surveillance_scale_score * 0.25
            + self.insurance_employment_genetic_discrimination_score * 0.25
            + self.informed_consent_biobank_research_deficit_gap_score * 0.20,
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
        self.estimated_bioethics_genetic_privacy_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class BioethicsGeneticPrivacyRightsEngineResult:
    agent: str
    domain: str
    entities: List[BioethicsGeneticPrivacyRightsEntity]
    total_entities: int = field(init=False)
    avg_composite: float = field(init=False)
    avg_estimated_bioethics_genetic_privacy_rights_index: float = field(init=False)
    risk_distribution: dict = field(init=False)
    pattern_distribution: dict = field(init=False)
    top_risk_entities: List[str] = field(init=False)
    critical_alerts: List[str] = field(init=False)
    confidence_score: float = 0.85
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    data_sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_entities = len(self.entities)
        scores = [e.composite_score for e in self.entities]
        self.avg_composite = round(statistics.mean(scores), 2)
        self.avg_estimated_bioethics_genetic_privacy_rights_index = round(
            self.avg_composite / 100 * 10, 2
        )
        self.risk_distribution = {
            level: sum(1 for e in self.entities if e.risk_level == level)
            for level in ["critique", "élevé", "modéré", "faible"]
        }
        pattern_counts: dict = {}
        for e in self.entities:
            pattern_counts[e.primary_pattern] = pattern_counts.get(e.primary_pattern, 0) + 1
        self.pattern_distribution = pattern_counts
        critique_entities = sorted(
            [e for e in self.entities if e.risk_level == "critique"],
            key=lambda x: x.composite_score,
            reverse=True,
        )
        self.top_risk_entities = [e.entity_id for e in critique_entities[:3]]
        self.critical_alerts = [
            f"{e.entity_id} ({e.name}): composite={e.composite_score} — {e.primary_pattern}"
            for e in critique_entities
        ]


def run_bioethics_genetic_privacy_rights_engine() -> BioethicsGeneticPrivacyRightsEngineResult:
    entities = [
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-001",
            name="Chine/CRISPR — He Jiankui Bébés OGM 2018, ADN Uyghurs Police Collecté, Biobank 10M Génomes État & CRISPR Non-Réglementé",
            country="Chine",
            genome_editing_embryo_ethics_severity_score=95.0,
            genetic_database_state_surveillance_scale_score=93.0,
            insurance_employment_genetic_discrimination_score=92.0,
            informed_consent_biobank_research_deficit_gap_score=94.0,
            primary_pattern="genome_editing_embryo_ethics_severity",
        ),
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-002",
            name="USA/GINA Gaps — GenBank Données Partagées Sans Consentement, Assurances Vie Exemption GINA, Ancestrie ADN Police & DTC Testing Mineurs",
            country="USA",
            genome_editing_embryo_ethics_severity_score=91.0,
            genetic_database_state_surveillance_scale_score=89.0,
            insurance_employment_genetic_discrimination_score=90.0,
            informed_consent_biobank_research_deficit_gap_score=88.0,
            primary_pattern="genetic_database_state_surveillance_scale",
        ),
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-003",
            name="UE/GDPR Tensions — Biobanques UK Reconsent Post-Brexit, 23andMe Faillite Données 14M, GDPR Exemptions Recherche & Profilage Ethnique",
            country="Europe",
            genome_editing_embryo_ethics_severity_score=87.0,
            genetic_database_state_surveillance_scale_score=86.0,
            insurance_employment_genetic_discrimination_score=85.0,
            informed_consent_biobank_research_deficit_gap_score=88.0,
            primary_pattern="informed_consent_biobank_research_deficit_gap",
        ),
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-004",
            name="Inde/Biodata — UIDAI Aadhaar ADN Proposition, Programme Génome Humain National, Absence Loi Génétique & Pharma Tests Essais Pauvres",
            country="Inde",
            genome_editing_embryo_ethics_severity_score=83.0,
            genetic_database_state_surveillance_scale_score=82.0,
            insurance_employment_genetic_discrimination_score=84.0,
            informed_consent_biobank_research_deficit_gap_score=81.0,
            primary_pattern="insurance_employment_genetic_discrimination",
        ),
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-005",
            name="Australie/Police ADN — Base ADN Police 1M, Innocent Inclus, Prédiction Phénotype & Familial Searching Non-Régulé",
            country="Australie",
            genome_editing_embryo_ethics_severity_score=56.0,
            genetic_database_state_surveillance_scale_score=54.0,
            insurance_employment_genetic_discrimination_score=55.0,
            informed_consent_biobank_research_deficit_gap_score=57.0,
            primary_pattern="genetic_database_state_surveillance_scale",
        ),
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-006",
            name="Israël/Génome — État Registre Génétique 2019, Kohanim ADN Discrimination, Comités IVF Non-Indépendants & Surrogacy Exploitation",
            country="Israël",
            genome_editing_embryo_ethics_severity_score=52.0,
            genetic_database_state_surveillance_scale_score=51.0,
            insurance_employment_genetic_discrimination_score=54.0,
            informed_consent_biobank_research_deficit_gap_score=53.0,
            primary_pattern="genome_editing_embryo_ethics_severity",
        ),
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-007",
            name="UNESCO/ISSCR — Déclaration Universelle Génome Humain 1997, ISSCR Guidelines Cellules Souches 2021, Global Observatory & Bioethics Comités",
            country="Global",
            genome_editing_embryo_ethics_severity_score=27.0,
            genetic_database_state_surveillance_scale_score=25.0,
            insurance_employment_genetic_discrimination_score=28.0,
            informed_consent_biobank_research_deficit_gap_score=26.0,
            primary_pattern="informed_consent_biobank_research_deficit_gap",
        ),
        BioethicsGeneticPrivacyRightsEntity(
            entity_id="BGR-008",
            name="ONU/Oviedo — Convention Oviedo Biomédecine 1997, PIDESC Art.15 Science, Déclaration Helsinki & Belmont Report Standards",
            country="Global",
            genome_editing_embryo_ethics_severity_score=4.0,
            genetic_database_state_surveillance_scale_score=4.0,
            insurance_employment_genetic_discrimination_score=4.0,
            informed_consent_biobank_research_deficit_gap_score=4.0,
            primary_pattern="genome_editing_embryo_ethics_severity",
        ),
    ]

    return BioethicsGeneticPrivacyRightsEngineResult(
        agent="Bioethics Genetic Privacy Rights Engine Agent",
        domain="bioethics_genetic_privacy_rights",
        entities=entities,
        data_sources=[
            "un_human_genome_declaration_report",
            "isscr_stem_cell_ethics_guidelines",
            "amnesty_international_genetic_surveillance_report",
        ],
    )


if __name__ == "__main__":
    result = run_bioethics_genetic_privacy_rights_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_bioethics_genetic_privacy_rights_index}")
    print(f"Distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
