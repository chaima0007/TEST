from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HumanRightsDefendersProtectionEntity:
    entity_id: str
    name: str
    country: str
    hrd_killing_disappearance_severity_score: float
    criminalization_legal_harassment_scale_score: float
    digital_surveillance_doxxing_hrd_score: float
    ngo_restriction_foreign_agent_law_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_human_rights_defenders_protection_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.hrd_killing_disappearance_severity_score * 0.30
            + self.criminalization_legal_harassment_scale_score * 0.25
            + self.digital_surveillance_doxxing_hrd_score * 0.25
            + self.ngo_restriction_foreign_agent_law_deficit_gap_score * 0.20,
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
        self.estimated_human_rights_defenders_protection_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class HumanRightsDefendersProtectionEngineResult:
    agent: str = "Human Rights Defenders Protection Engine Agent"
    domain: str = "human_rights_defenders_protection"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_human_rights_defenders_protection_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HumanRightsDefendersProtectionEntity] = field(default_factory=list)


def run_human_rights_defenders_protection_engine() -> HumanRightsDefendersProtectionEngineResult:
    entities = [
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-001",
            name="Colombie — Premier Pays Monde Meurtres Défenseurs, Leaders Sociaux Assassinés, Communautés Autochtones Ciblées & Impunité 95%",
            country="Colombie",
            hrd_killing_disappearance_severity_score=96.0,
            criminalization_legal_harassment_scale_score=92.0,
            digital_surveillance_doxxing_hrd_score=90.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=94.0,
            primary_pattern="hrd_killing_disappearance_severity",
        ),
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-002",
            name="Mexique — Journalistes Défenseurs Environnement Assassinés, Cartels Ciblant Activistes, Disparitions Forcées & Protection Insuffisante",
            country="Mexique",
            hrd_killing_disappearance_severity_score=93.0,
            criminalization_legal_harassment_scale_score=89.0,
            digital_surveillance_doxxing_hrd_score=90.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=88.0,
            primary_pattern="hrd_killing_disappearance_severity",
        ),
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-003",
            name="Russie — Lois Agents Étrangers Museler ONG, Alexei Navalny Assassiné Prison, Memorial Liquidé & Défenseurs Exilés Persécutés",
            country="Russie",
            hrd_killing_disappearance_severity_score=90.0,
            criminalization_legal_harassment_scale_score=87.0,
            digital_surveillance_doxxing_hrd_score=86.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=85.0,
            primary_pattern="ngo_restriction_foreign_agent_law_deficit_gap",
        ),
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-004",
            name="Éthiopie/Soudan — Défenseurs Tigré Arrêtés, Journalistes Emprisonnés Conflit, Activistes Disparus & Accès Humanitaire Bloqué",
            country="Éthiopie/Soudan",
            hrd_killing_disappearance_severity_score=87.0,
            criminalization_legal_harassment_scale_score=83.0,
            digital_surveillance_doxxing_hrd_score=82.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=84.0,
            primary_pattern="criminalization_legal_harassment_scale",
        ),
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-005",
            name="Chine/Vietnam — Avocats Droits Homme Détenus Arbitrairement, Loi Cybersécurité Surveillance Massive & ONG Sous Contrôle Parti",
            country="Chine/Vietnam",
            hrd_killing_disappearance_severity_score=57.0,
            criminalization_legal_harassment_scale_score=54.0,
            digital_surveillance_doxxing_hrd_score=55.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=53.0,
            primary_pattern="digital_surveillance_doxxing_hrd",
        ),
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-006",
            name="Égypte/Bangladesh — Défenseurs Emprisonnés Lois Antiterrorisme, ONG Loi 70/2017 Restrictive & Doxxing Militantes Femmes",
            country="Égypte/Bangladesh",
            hrd_killing_disappearance_severity_score=54.0,
            criminalization_legal_harassment_scale_score=51.0,
            digital_surveillance_doxxing_hrd_score=52.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=50.0,
            primary_pattern="ngo_restriction_foreign_agent_law_deficit_gap",
        ),
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-007",
            name="Front Line Defenders — Système Alerte Urgence Défenseurs Risque, Documentation Meurtres Annuels & Bourses Protection Numérique",
            country="Global",
            hrd_killing_disappearance_severity_score=28.0,
            criminalization_legal_harassment_scale_score=25.0,
            digital_surveillance_doxxing_hrd_score=26.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=24.0,
            primary_pattern="hrd_killing_disappearance_severity",
        ),
        HumanRightsDefendersProtectionEntity(
            entity_id="HRD-008",
            name="ONU Déclaration 1998 — Déclaration Défenseurs Droits Homme, Rapporteur Spécial HRD & Résolutions Conseil Droits Homme",
            country="Global",
            hrd_killing_disappearance_severity_score=5.0,
            criminalization_legal_harassment_scale_score=4.0,
            digital_surveillance_doxxing_hrd_score=4.0,
            ngo_restriction_foreign_agent_law_deficit_gap_score=3.0,
            primary_pattern="criminalization_legal_harassment_scale",
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

    return HumanRightsDefendersProtectionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_human_rights_defenders_protection_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "front_line_defenders_annual_report_hrd_killings",
            "global_witness_hrd_murders_tracking_database",
            "civicus_ngo_restriction_closing_space_monitor",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_human_rights_defenders_protection_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_human_rights_defenders_protection_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
