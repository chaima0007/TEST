from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class BioethicsRightsEntity:
    entity_id: str
    name: str
    country: str
    non_consensual_experimentation_severity_score: float
    organ_harvesting_trafficking_scale_score: float
    genetic_data_surveillance_coercion_score: float
    medical_ai_algorithmic_discrimination_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_bioethics_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.non_consensual_experimentation_severity_score * 0.30
            + self.organ_harvesting_trafficking_scale_score * 0.25
            + self.genetic_data_surveillance_coercion_score * 0.25
            + self.medical_ai_algorithmic_discrimination_gap_score * 0.20,
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
        self.estimated_bioethics_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class BioethicsRightsEngineResult:
    agent: str = "Bioethics Rights Engine Agent"
    domain: str = "bioethics_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_bioethics_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[BioethicsRightsEntity] = field(default_factory=list)

def run_bioethics_rights_engine() -> BioethicsRightsEngineResult:
    entities = [
        BioethicsRightsEntity(
            entity_id="BER-001",
            name="Chine — Prélèvement Organes Prisonniers Consciencieux Documenté Tribunal 2019, Falun Gong/Ouïghours & Marché Transplantations Forcées",
            country="Chine",
            non_consensual_experimentation_severity_score=95.0,
            organ_harvesting_trafficking_scale_score=97.0,
            genetic_data_surveillance_coercion_score=93.0,
            medical_ai_algorithmic_discrimination_gap_score=90.0,
            primary_pattern="organ_harvesting_trafficking_scale",
        ),
        BioethicsRightsEntity(
            entity_id="BER-002",
            name="Pays en Développement — Essais Cliniques Multinationales Sans Consentement Éclairé, Standards Réduits & Exploitation Vulnérabilité",
            country="Global Sud",
            non_consensual_experimentation_severity_score=93.0,
            organ_harvesting_trafficking_scale_score=87.0,
            genetic_data_surveillance_coercion_score=89.0,
            medical_ai_algorithmic_discrimination_gap_score=92.0,
            primary_pattern="non_consensual_experimentation_severity",
        ),
        BioethicsRightsEntity(
            entity_id="BER-003",
            name="Inde — Stérilisations Forcées Camps, Essais Médicaux Tribus, Brevets Ogm Biopiraterie & Données Aadhaar Vendues",
            country="Inde",
            non_consensual_experimentation_severity_score=90.0,
            organ_harvesting_trafficking_scale_score=84.0,
            genetic_data_surveillance_coercion_score=88.0,
            medical_ai_algorithmic_discrimination_gap_score=86.0,
            primary_pattern="non_consensual_experimentation_severity",
        ),
        BioethicsRightsEntity(
            entity_id="BER-004",
            name="USA Legacy/Tuskegee — Expérimentations Prisonniers Guatemala 1945-56, Tests Armes Chimiques Soldats & Héritage Eugenics",
            country="USA",
            non_consensual_experimentation_severity_score=87.0,
            organ_harvesting_trafficking_scale_score=81.0,
            genetic_data_surveillance_coercion_score=83.0,
            medical_ai_algorithmic_discrimination_gap_score=88.0,
            primary_pattern="non_consensual_experimentation_severity",
        ),
        BioethicsRightsEntity(
            entity_id="BER-005",
            name="Europe — Biais Algorithmes Diagnostic IA Peau Sombre, RGPD Gaps Données Médicales & Essais Pédiatriques Consentement",
            country="Europe",
            non_consensual_experimentation_severity_score=52.0,
            organ_harvesting_trafficking_scale_score=48.0,
            genetic_data_surveillance_coercion_score=56.0,
            medical_ai_algorithmic_discrimination_gap_score=62.0,
            primary_pattern="medical_ai_algorithmic_discrimination_gap",
        ),
        BioethicsRightsEntity(
            entity_id="BER-006",
            name="Moyen-Orient — Tourisme Transplantation Reins, Donneurs Pauvres Pakistan/Égypte & Absence Régulation",
            country="Moyen-Orient",
            non_consensual_experimentation_severity_score=50.0,
            organ_harvesting_trafficking_scale_score=57.0,
            genetic_data_surveillance_coercion_score=47.0,
            medical_ai_algorithmic_discrimination_gap_score=50.0,
            primary_pattern="organ_harvesting_trafficking_scale",
        ),
        BioethicsRightsEntity(
            entity_id="BER-007",
            name="Comité International Bioéthique/Nuffield — Standards Consentement, Déclaration Helsinki & IA Médicale Éthique",
            country="Global",
            non_consensual_experimentation_severity_score=26.0,
            organ_harvesting_trafficking_scale_score=24.0,
            genetic_data_surveillance_coercion_score=27.0,
            medical_ai_algorithmic_discrimination_gap_score=28.0,
            primary_pattern="medical_ai_algorithmic_discrimination_gap",
        ),
        BioethicsRightsEntity(
            entity_id="BER-008",
            name="ONU/UNESCO — Déclaration Universelle Bioéthique 2005, Comité Bioéthique & SDG 3 Santé Bien-Être",
            country="Global",
            non_consensual_experimentation_severity_score=4.0,
            organ_harvesting_trafficking_scale_score=4.0,
            genetic_data_surveillance_coercion_score=5.0,
            medical_ai_algorithmic_discrimination_gap_score=4.0,
            primary_pattern="genetic_data_surveillance_coercion",
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

    return BioethicsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_bioethics_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "china_tribunal_organ_harvesting_final_judgment_2019",
            "declaration_of_helsinki_world_medical_association",
            "nuffield_council_bioethics_reports",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_bioethics_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_bioethics_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
