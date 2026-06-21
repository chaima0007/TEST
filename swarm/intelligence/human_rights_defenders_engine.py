"""Human Rights Defenders Engine — Meurtres défenseurs, criminalisation, surveillance & espace civique."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class HumanRightsDefendersEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    defender_killing_criminalization_severity_score: float
    surveillance_harassment_intimidation_scale_score: float
    legal_framework_protection_absence_score: float
    civic_space_shrinking_repression_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_human_rights_defenders_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.defender_killing_criminalization_severity_score * 0.30
            + self.surveillance_harassment_intimidation_scale_score * 0.25
            + self.legal_framework_protection_absence_score * 0.25
            + self.civic_space_shrinking_repression_score * 0.20,
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
        self.estimated_human_rights_defenders_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class HumanRightsDefendersEngineResult:
    agent: str = "Human Rights Defenders Engine Agent"
    domain: str = "human_rights_defenders"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_human_rights_defenders_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HumanRightsDefendersEntity] = field(default_factory=list)


def run_human_rights_defenders_engine() -> HumanRightsDefendersEngineResult:
    entities = [
        HumanRightsDefendersEntity(
            entity_id="HRD-001",
            name="Colombie — 180+ Défenseurs Tués/An, Syndicats/Environnementalistes & Impunité 95%",
            country="Amérique Latine",
            sector="Colombie 187 Défenseurs Tués 2023 Global Witness Record LATAM, Syndicats/Défenseurs Terres Autochtones Ciblés, Groupes Armés Post-FARC Paramilitaires & Impunité 95% Meurtres Défenseurs",
            defender_killing_criminalization_severity_score=97.0,
            surveillance_harassment_intimidation_scale_score=93.0,
            legal_framework_protection_absence_score=92.0,
            civic_space_shrinking_repression_score=94.0,
            primary_pattern="defender_killing_criminalization_severity",
        ),
        HumanRightsDefendersEntity(
            entity_id="HRD-002",
            name="Philippines — Red-Tagging, Duterte Legacy, Journalistes/Avocats Assassinés",
            country="Asie du Sud-Est",
            sector="Philippines Red-Tagging Défenseurs Qualifiés Terroristes NTF-ELCAC, 900+ Activistes Tués Depuis 2016, Avocats/Journalistes/Prêtres Assassinés Karapatan & Impunité Forces Sécurité",
            defender_killing_criminalization_severity_score=93.0,
            surveillance_harassment_intimidation_scale_score=91.0,
            legal_framework_protection_absence_score=90.0,
            civic_space_shrinking_repression_score=90.0,
            primary_pattern="defender_killing_criminalization_severity",
        ),
        HumanRightsDefendersEntity(
            entity_id="HRD-003",
            name="Mexique — Cartels vs Journalistes, 15 Journalistes Tués 2023 & Sans Protection État",
            country="Amérique Latine",
            sector="Mexique 15 Journalistes Tués 2023 RSF, Cartels Tuent Défenseurs Sans Réaction État, Mécanisme Protection Sous-Financé 2012 & Veracruz/Guerrero Zones Mort Défenseurs",
            defender_killing_criminalization_severity_score=90.0,
            surveillance_harassment_intimidation_scale_score=87.0,
            legal_framework_protection_absence_score=87.0,
            civic_space_shrinking_repression_score=87.0,
            primary_pattern="defender_killing_criminalization_severity",
        ),
        HumanRightsDefendersEntity(
            entity_id="HRD-004",
            name="Russie/Biélorussie — Memorial Liquidé, Navalny, Journalistes Emprisonnés & Exil Forcé",
            country="Europe de l'Est",
            sector="Russie Memorial International Liquidé 2021, Alexeï Navalny Tué Détention 2024, Biélorussie 300+ Journalistes Emprisonnés Post-2020, Loi Agents Étrangers & Exil Forcé Défenseurs",
            defender_killing_criminalization_severity_score=87.0,
            surveillance_harassment_intimidation_scale_score=85.0,
            legal_framework_protection_absence_score=84.0,
            civic_space_shrinking_repression_score=84.0,
            primary_pattern="defender_killing_criminalization_severity",
        ),
        HumanRightsDefendersEntity(
            entity_id="HRD-005",
            name="Chine/Hong Kong — NSL HK, Avocats 709 & Surveillance AI Défenseurs",
            country="Asie du Nord-Est",
            sector="Hong Kong National Security Law 2020 Fermeture Médias/ONG, Chine Rafle 709 Avocats 300+, Surveillance AI Reconnaissance Faciale Défenseurs Ouïghours & Interdiction Sortie Territoire",
            defender_killing_criminalization_severity_score=58.0,
            surveillance_harassment_intimidation_scale_score=55.0,
            legal_framework_protection_absence_score=52.0,
            civic_space_shrinking_repression_score=52.0,
            primary_pattern="surveillance_harassment_intimidation",
        ),
        HumanRightsDefendersEntity(
            entity_id="HRD-006",
            name="Turquie/Azerbaïdjan — Procès Journalistes, Lois ONG Restrictives & Harcèlement Judiciaire",
            country="Europe du Sud-Est",
            sector="Turquie 1 500 Avocats Poursuivis 2016-2024, Taner Kılıç Amnesty 6 Ans Procès, Azerbaïdjan Journalistes Emprisonnés COP29 & Lois ONG Restrictives Agents Étrangers 2022",
            defender_killing_criminalization_severity_score=55.0,
            surveillance_harassment_intimidation_scale_score=51.0,
            legal_framework_protection_absence_score=50.0,
            civic_space_shrinking_repression_score=49.0,
            primary_pattern="defender_killing_criminalization_severity",
        ),
        HumanRightsDefendersEntity(
            entity_id="HRD-007",
            name="Front Line Defenders/RSF/CPJ — Protection Urgente, Alerte Précoce & Relocalisation",
            country="Global",
            sector="Front Line Defenders Protection Urgente Défenseurs Danger, RSF Reporters Sans Frontières Index Liberté Presse, CPJ Committee Protect Journalists Relocalisation & Alerte Précoce Mécanismes",
            defender_killing_criminalization_severity_score=28.0,
            surveillance_harassment_intimidation_scale_score=25.0,
            legal_framework_protection_absence_score=25.0,
            civic_space_shrinking_repression_score=26.0,
            primary_pattern="legal_framework_protection_absence",
        ),
        HumanRightsDefendersEntity(
            entity_id="HRD-008",
            name="ONU/Déclaration Défenseurs 1998 — Rapporteur Spécial, Mécanismes HRC & SDG 16",
            country="Global",
            sector="Déclaration ONU Défenseurs Droits Homme 1998 Résolution A/RES/53/144, Rapporteur Spécial ONU HRD Mary Lawlor Depuis 2020, Mécanismes HRC CIDH/UA & SDG 16 Paix Justice",
            defender_killing_criminalization_severity_score=5.0,
            surveillance_harassment_intimidation_scale_score=3.0,
            legal_framework_protection_absence_score=4.0,
            civic_space_shrinking_repression_score=4.0,
            primary_pattern="legal_framework_protection_absence",
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
        for e in sorted_entities if e.risk_level == "critique"
    ]

    return HumanRightsDefendersEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_human_rights_defenders_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "front_line_defenders_annual_report_human_rights_defenders_killed",
            "reporters_sans_frontieres_world_press_freedom_index_report",
            "civicus_monitor_civic_space_closing_global_tracker_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_human_rights_defenders_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_human_rights_defenders_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
