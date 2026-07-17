from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class TransitionalJusticeEntity:
    entity_id: str
    name: str
    country: str
    truth_commission_absence_score: float
    reparations_implementation_gap_score: float
    amnesty_impunity_bloc_score: float
    institutional_reform_failure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_transitional_justice_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.truth_commission_absence_score * 0.30
            + self.reparations_implementation_gap_score * 0.25
            + self.amnesty_impunity_bloc_score * 0.25
            + self.institutional_reform_failure_score * 0.20,
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
        self.estimated_transitional_justice_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class TransitionalJusticeEngineResult:
    agent: str = "Transitional Justice Engine Agent"
    domain: str = "transitional_justice"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_transitional_justice_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[TransitionalJusticeEntity] = field(default_factory=list)

def run_transitional_justice_engine() -> TransitionalJusticeEngineResult:
    entities = [
        TransitionalJusticeEntity(
            entity_id="TJ-001",
            name="Syrie — Aucune CVR, Assad Impuni, 100K+ Disparus & Justice Internationale Bloquée Veto",
            country="Moyen-Orient",
            truth_commission_absence_score=95.0,
            reparations_implementation_gap_score=92.0,
            amnesty_impunity_bloc_score=95.0,
            institutional_reform_failure_score=92.0,
            primary_pattern="amnesty_impunity_bloc",
        ),
        TransitionalJusticeEntity(
            entity_id="TJ-002",
            name="Myanmar — Junta Post-Coup, Génocide Rohingya Non Jugé & CIJ Procédure Sans Exécution",
            country="Asie du Sud-Est",
            truth_commission_absence_score=90.0,
            reparations_implementation_gap_score=88.0,
            amnesty_impunity_bloc_score=92.0,
            institutional_reform_failure_score=88.0,
            primary_pattern="amnesty_impunity_bloc",
        ),
        TransitionalJusticeEntity(
            entity_id="TJ-003",
            name="Cambodge/Khmers Rouges — CETC Trop Tardif, Rares Condamnations & Génération Victime Vieillie",
            country="Asie du Sud-Est",
            truth_commission_absence_score=85.0,
            reparations_implementation_gap_score=88.0,
            amnesty_impunity_bloc_score=82.0,
            institutional_reform_failure_score=88.0,
            primary_pattern="reparations_implementation_gap",
        ),
        TransitionalJusticeEntity(
            entity_id="TJ-004",
            name="Sri Lanka — CVR Promises Non Tenues, Crimes Guerre Tamouls Impunis & Résistance Militaire",
            country="Asie du Sud",
            truth_commission_absence_score=82.0,
            reparations_implementation_gap_score=85.0,
            amnesty_impunity_bloc_score=80.0,
            institutional_reform_failure_score=82.0,
            primary_pattern="truth_commission_absence",
        ),
        TransitionalJusticeEntity(
            entity_id="TJ-005",
            name="Colombie — JEP Fonctionnelle Mais Lente, FARC Réintégration Partielle & Dissidences Actives",
            country="Amérique Latine",
            truth_commission_absence_score=52.0,
            reparations_implementation_gap_score=55.0,
            amnesty_impunity_bloc_score=50.0,
            institutional_reform_failure_score=55.0,
            primary_pattern="reparations_implementation_gap",
        ),
        TransitionalJusticeEntity(
            entity_id="TJ-006",
            name="Tunisie — IVD Sabotée, Reparations Non Versées & Contre-Réforme Autoritaire Saïed",
            country="Afrique du Nord",
            truth_commission_absence_score=50.0,
            reparations_implementation_gap_score=55.0,
            amnesty_impunity_bloc_score=52.0,
            institutional_reform_failure_score=48.0,
            primary_pattern="reparations_implementation_gap",
        ),
        TransitionalJusticeEntity(
            entity_id="TJ-007",
            name="ICTJ/No Peace Without Justice — Expertise Mondiale CVR, Réparations & Réforme Institutionnelle",
            country="Global",
            truth_commission_absence_score=22.0,
            reparations_implementation_gap_score=25.0,
            amnesty_impunity_bloc_score=28.0,
            institutional_reform_failure_score=30.0,
            primary_pattern="truth_commission_absence",
        ),
        TransitionalJusticeEntity(
            entity_id="TJ-008",
            name="ONU/HCDH — Principes de Base Réparations, Rapporteur Justice Transitionnelle & Résolutions",
            country="Global",
            truth_commission_absence_score=4.0,
            reparations_implementation_gap_score=5.0,
            amnesty_impunity_bloc_score=3.0,
            institutional_reform_failure_score=6.0,
            primary_pattern="institutional_reform_failure",
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

    return TransitionalJusticeEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_transitional_justice_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ictj_transitional_justice_global_survey_annual_report",
            "un_special_rapporteur_truth_justice_reparations_guarantees_non_recurrence",
            "icc_rome_statute_state_parties_compliance_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_transitional_justice_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_transitional_justice_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
