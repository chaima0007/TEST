from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class NeurorightMentalSovereigntyEntity:
    entity_id: str
    name: str
    country: str
    brain_data_collection_consent_absence_score: float
    neurotechnology_regulation_gap_score: float
    mental_state_manipulation_risk_score: float
    cognitive_liberty_violation_scale_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_neuroright_mental_sovereignty_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.brain_data_collection_consent_absence_score * 0.30
            + self.neurotechnology_regulation_gap_score * 0.25
            + self.mental_state_manipulation_risk_score * 0.25
            + self.cognitive_liberty_violation_scale_score * 0.20,
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
        self.estimated_neuroright_mental_sovereignty_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class NeurorightMentalSovereigntyEngineResult:
    agent: str = "Neuroright Mental Sovereignty Engine Agent"
    domain: str = "neuroright_mental_sovereignty"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_neuroright_mental_sovereignty_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[NeurorightMentalSovereigntyEntity] = field(default_factory=list)

def run_neuroright_mental_sovereignty_engine() -> NeurorightMentalSovereigntyEngineResult:
    entities = [
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-001",
            name="Chine — BCI Militaire, Surveillance Émotions Usines & Neuroimagerie Carcérale Ouïghours",
            country="Asie de l'Est",
            brain_data_collection_consent_absence_score=95.0,
            neurotechnology_regulation_gap_score=92.0,
            mental_state_manipulation_risk_score=95.0,
            cognitive_liberty_violation_scale_score=92.0,
            primary_pattern="mental_state_manipulation_risk",
        ),
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-002",
            name="USA/Neuralink — Implants Cérébraux Humains 2024, Données Cerveau Sans Régulation & HIPAA Gap",
            country="Amérique du Nord",
            brain_data_collection_consent_absence_score=88.0,
            neurotechnology_regulation_gap_score=95.0,
            mental_state_manipulation_risk_score=88.0,
            cognitive_liberty_violation_scale_score=85.0,
            primary_pattern="neurotechnology_regulation_gap",
        ),
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-003",
            name="Corée du Sud — Casques EEG Employés, Brain Score Recrutement & Zéro Cadre Légal Neuro-Data",
            country="Asie de l'Est",
            brain_data_collection_consent_absence_score=88.0,
            neurotechnology_regulation_gap_score=88.0,
            mental_state_manipulation_risk_score=88.0,
            cognitive_liberty_violation_scale_score=90.0,
            primary_pattern="cognitive_liberty_violation_scale",
        ),
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-004",
            name="Neuromarketing Global/Amazon-Meta — Scans Cérébraux Consommateurs Sans Consentement Explicite",
            country="Global",
            brain_data_collection_consent_absence_score=85.0,
            neurotechnology_regulation_gap_score=85.0,
            mental_state_manipulation_risk_score=88.0,
            cognitive_liberty_violation_scale_score=85.0,
            primary_pattern="brain_data_collection_consent_absence",
        ),
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-005",
            name="UAE/Russie — Détecteurs Mensonge IA Cerveau Frontières, Interrogatoires & Pas de Recours",
            country="Moyen-Orient/Europe de l'Est",
            brain_data_collection_consent_absence_score=52.0,
            neurotechnology_regulation_gap_score=55.0,
            mental_state_manipulation_risk_score=52.0,
            cognitive_liberty_violation_scale_score=55.0,
            primary_pattern="brain_data_collection_consent_absence",
        ),
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-006",
            name="UE — AI Act Ne Couvre Pas Neuro-Data, RGPD Insuffisant Données Cérébrales & Gap Régulation",
            country="Europe",
            brain_data_collection_consent_absence_score=50.0,
            neurotechnology_regulation_gap_score=55.0,
            mental_state_manipulation_risk_score=48.0,
            cognitive_liberty_violation_scale_score=50.0,
            primary_pattern="neurotechnology_regulation_gap",
        ),
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-007",
            name="Neurorights Foundation/Yuste — 5 Neurodroits, Loi Chili 2021 & 30+ Pays Sensibilisés",
            country="Global",
            brain_data_collection_consent_absence_score=22.0,
            neurotechnology_regulation_gap_score=28.0,
            mental_state_manipulation_risk_score=25.0,
            cognitive_liberty_violation_scale_score=30.0,
            primary_pattern="cognitive_liberty_violation_scale",
        ),
        NeurorightMentalSovereigntyEntity(
            entity_id="NMS-008",
            name="ONU/OHCHR — Neurotechnologie & Droits Humains Rapport 2021, ICCPR Art.17 Vie Privée Mentale",
            country="Global",
            brain_data_collection_consent_absence_score=4.0,
            neurotechnology_regulation_gap_score=5.0,
            mental_state_manipulation_risk_score=3.0,
            cognitive_liberty_violation_scale_score=6.0,
            primary_pattern="mental_state_manipulation_risk",
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

    return NeurorightMentalSovereigntyEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_neuroright_mental_sovereignty_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "neurorights_foundation_yuste_five_neurorights_framework",
            "un_ohchr_neurotechnology_human_rights_report_2021",
            "ieee_neuroethics_brain_computer_interface_rights_standards",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_neuroright_mental_sovereignty_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_neuroright_mental_sovereignty_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
