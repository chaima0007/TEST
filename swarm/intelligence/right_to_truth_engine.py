from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RightToTruthEntity:
    entity_id: str
    name: str
    country: str
    truth_commission_absence_score: float
    official_denial_obstruction_score: float
    victim_silencing_score: float
    archive_destruction_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_truth_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.truth_commission_absence_score * 0.30
            + self.official_denial_obstruction_score * 0.25
            + self.victim_silencing_score * 0.25
            + self.archive_destruction_score * 0.20,
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
        self.estimated_right_to_truth_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RightToTruthEngineResult:
    agent: str = "Right to Truth Engine Agent"
    domain: str = "right_to_truth"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_truth_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToTruthEntity] = field(default_factory=list)

def run_right_to_truth_engine() -> RightToTruthEngineResult:
    entities = [
        RightToTruthEntity(
            entity_id="RT-001",
            name="Syrie — 100 000 Disparus, Déni Officiel Assad & Destruction Preuves Chimiques",
            country="Moyen-Orient",
            truth_commission_absence_score=88.0,
            official_denial_obstruction_score=95.0,
            victim_silencing_score=90.0,
            archive_destruction_score=88.0,
            primary_pattern="official_denial_obstruction",
        ),
        RightToTruthEntity(
            entity_id="RT-002",
            name="Amérique Latine/Cône Sud — Juntes, 30 000 Disparus & Vérité Post-Dictature Incomplète",
            country="Amérique Latine",
            truth_commission_absence_score=90.0,
            official_denial_obstruction_score=88.0,
            victim_silencing_score=85.0,
            archive_destruction_score=88.0,
            primary_pattern="truth_commission_absence",
        ),
        RightToTruthEntity(
            entity_id="RT-003",
            name="Sri Lanka — 40 000 Civils Tamouls Tués, Vérité Sabotée & Commissions Paralysées",
            country="Asie du Sud",
            truth_commission_absence_score=82.0,
            official_denial_obstruction_score=85.0,
            victim_silencing_score=80.0,
            archive_destruction_score=78.0,
            primary_pattern="victim_silencing",
        ),
        RightToTruthEntity(
            entity_id="RT-004",
            name="Rwanda/Post-Génocide — Gacaca, TPIR & Révisionnisme Négationniste Persistant",
            country="Afrique Sub-Saharienne",
            truth_commission_absence_score=70.0,
            official_denial_obstruction_score=75.0,
            victim_silencing_score=78.0,
            archive_destruction_score=80.0,
            primary_pattern="archive_destruction",
        ),
        RightToTruthEntity(
            entity_id="RT-005",
            name="Algérie/Maroc — Années de Plomb, Disparus & Commission Vérité Partielle Sans Réparation",
            country="Afrique du Nord",
            truth_commission_absence_score=52.0,
            official_denial_obstruction_score=58.0,
            victim_silencing_score=55.0,
            archive_destruction_score=50.0,
            primary_pattern="official_denial_obstruction",
        ),
        RightToTruthEntity(
            entity_id="RT-006",
            name="Russie/Tchétchénie — Disparus Deux Guerres, FSB Bloque Enquêtes & Archives Classifiées",
            country="Europe de l'Est",
            truth_commission_absence_score=48.0,
            official_denial_obstruction_score=55.0,
            victim_silencing_score=52.0,
            archive_destruction_score=58.0,
            primary_pattern="victim_silencing",
        ),
        RightToTruthEntity(
            entity_id="RT-007",
            name="Espagne — Loi Mémoire Historique, Fosses Communes Franco & Résistance Partis Droite",
            country="Europe",
            truth_commission_absence_score=25.0,
            official_denial_obstruction_score=30.0,
            victim_silencing_score=28.0,
            archive_destruction_score=32.0,
            primary_pattern="truth_commission_absence",
        ),
        RightToTruthEntity(
            entity_id="RT-008",
            name="ONU/HCDH — Rapporteur Vérité, Principes Joinet-Orentlicher & Base de Données",
            country="Global",
            truth_commission_absence_score=4.0,
            official_denial_obstruction_score=5.0,
            victim_silencing_score=3.0,
            archive_destruction_score=6.0,
            primary_pattern="archive_destruction",
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

    return RightToTruthEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_truth_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ictj_international_center_transitional_justice_truth_commissions_database",
            "un_special_rapporteur_truth_reparation_guarantees_non_recurrence_annual_report",
            "amnesty_international_truth_justice_reparation_annual_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_right_to_truth_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_right_to_truth_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
