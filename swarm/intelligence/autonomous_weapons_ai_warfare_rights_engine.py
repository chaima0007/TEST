"""
Caelum Partners — Autonomous Weapons AI Warfare Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Armes autonomes létales, IA militaire, responsabilité humaine, droit international humanitaire.

Les systèmes d'armes létales autonomes (LAWS) représentent l'une des menaces les plus graves
aux fondements du droit international humanitaire. Contrairement aux combattants humains,
les systèmes IA ne peuvent pas exercer le jugement éthique requis pour distinguer combattants
et civils, évaluer la proportionnalité ou respecter le principe de précaution. La Campagne
Stop Killer Robots et le CICR appellent à une réglementation internationale contraignante,
mais aucun traité n'a encore été adopté malgré des années de négociations au CCW à Genève.

Risk levels (armes autonomes létales et vide juridique IA militaire) :
  critique  -> composite >= 60  (LAWS déployés — zéro contrôle humain — victimes civiles)
  élevé     -> composite >= 40  (systèmes semi-autonomes — réglementation insuffisante)
  modéré    -> composite >= 20  (plaidoyer actif — négociations sans accord contraignant)
  faible    -> composite < 20   (cadre normatif — rapports et recommandations ONU)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class AutonomousWeaponsAIWarfareRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    lethal_autonomous_weapon_civilian_harm_severity_score: float
    human_control_accountability_removal_scale_score: float
    ai_bias_targeting_discrimination_score: float
    autonomous_weapon_ban_treaty_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_autonomous_weapons_ai_warfare_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.lethal_autonomous_weapon_civilian_harm_severity_score * 0.30
            + self.human_control_accountability_removal_scale_score * 0.25
            + self.ai_bias_targeting_discrimination_score * 0.25
            + self.autonomous_weapon_ban_treaty_deficit_gap_score * 0.20,
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
        self.estimated_autonomous_weapons_ai_warfare_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "lethal_autonomous_weapon_civilian_harm_severity_score": self.lethal_autonomous_weapon_civilian_harm_severity_score,
            "human_control_accountability_removal_scale_score": self.human_control_accountability_removal_scale_score,
            "ai_bias_targeting_discrimination_score": self.ai_bias_targeting_discrimination_score,
            "autonomous_weapon_ban_treaty_deficit_gap_score": self.autonomous_weapon_ban_treaty_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_autonomous_weapons_ai_warfare_rights_index": self.estimated_autonomous_weapons_ai_warfare_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class AutonomousWeaponsAIWarfareRightsEngineResult:
    agent: str = "Autonomous Weapons AI Warfare Rights Engine Agent"
    domain: str = "autonomous_weapons_ai_warfare_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_autonomous_weapons_ai_warfare_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AutonomousWeaponsAIWarfareRightsEntity] = field(default_factory=list)


def run_autonomous_weapons_ai_warfare_rights_engine() -> AutonomousWeaponsAIWarfareRightsEngineResult:
    entities = [
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-001",
            name="USA/DARPA — Autonomous F-16 Dogfight, Drone Swarms, Loitering Munitions Kargu & LAWS Aucun Veto Humain Cible",
            country="USA",
            sector="Systèmes Armes Autonomes Létales",
            lethal_autonomous_weapon_civilian_harm_severity_score=94.0,
            human_control_accountability_removal_scale_score=92.0,
            ai_bias_targeting_discrimination_score=93.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=91.0,
            primary_pattern="lethal_autonomous_weapon_civilian_harm_severity",
        ),
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-002",
            name="Russie/Uran-9 — Robots Combat Syrie, S-70 Okhotnik Drone, IA Cibles Non-Supervisée & KUB-BLA Kamikaze",
            country="Russie",
            sector="Robots Combat IA Non-Supervisée",
            lethal_autonomous_weapon_civilian_harm_severity_score=90.0,
            human_control_accountability_removal_scale_score=92.0,
            ai_bias_targeting_discrimination_score=88.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=90.0,
            primary_pattern="human_control_accountability_removal_scale",
        ),
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-003",
            name="Chine/PLA — IA Militaire Plan 2030, Drone CH-5 Ventes Export, Systèmes Anti-Drones IA & Sharp Sword UCAV",
            country="Chine",
            sector="IA Militaire Exportation",
            lethal_autonomous_weapon_civilian_harm_severity_score=87.0,
            human_control_accountability_removal_scale_score=85.0,
            ai_bias_targeting_discrimination_score=88.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=86.0,
            primary_pattern="lethal_autonomous_weapon_civilian_harm_severity",
        ),
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-004",
            name="Israël/Elbit — Système Harpy LAWS, Hermes Ciblage Automatique, Iron Dome IA & Export Sans Contrôle Humain",
            country="Israël",
            sector="Export LAWS Ciblage Automatique",
            lethal_autonomous_weapon_civilian_harm_severity_score=83.0,
            human_control_accountability_removal_scale_score=82.0,
            ai_bias_targeting_discrimination_score=84.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=81.0,
            primary_pattern="ai_bias_targeting_discrimination",
        ),
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-005",
            name="UE/Défense — Eurodrone Autonomie Partielle, FCAS Humain Supervisé, Politique IA Éthique Défense & Règlement IA Exemption Militaire",
            country="Europe",
            sector="Défense Européenne IA Éthique",
            lethal_autonomous_weapon_civilian_harm_severity_score=56.0,
            human_control_accountability_removal_scale_score=54.0,
            ai_bias_targeting_discrimination_score=55.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=57.0,
            primary_pattern="autonomous_weapon_ban_treaty_deficit_gap",
        ),
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-006",
            name="Turquie/Bayraktar — TB2 Usage Libyen/Azerbaïdjan, Kargu-2 LAWS Exporté, Pas Veto Humain Obligatoire & Réglementations Absentes",
            country="Turquie",
            sector="Export Drones LAWS Réglementation Absente",
            lethal_autonomous_weapon_civilian_harm_severity_score=52.0,
            human_control_accountability_removal_scale_score=51.0,
            ai_bias_targeting_discrimination_score=54.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=53.0,
            primary_pattern="human_control_accountability_removal_scale",
        ),
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-007",
            name="ICRC/PAX — Campagne Stop Killer Robots, CICR Appel Réglementation, CCW GGE LAWS Genève & Principes Martens Application",
            country="Global",
            sector="Plaidoyer International LAWS",
            lethal_autonomous_weapon_civilian_harm_severity_score=27.0,
            human_control_accountability_removal_scale_score=25.0,
            ai_bias_targeting_discrimination_score=28.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=26.0,
            primary_pattern="autonomous_weapon_ban_treaty_deficit_gap",
        ),
        AutonomousWeaponsAIWarfareRightsEntity(
            entity_id="AWR-008",
            name="ONU/CCW — Convention Certaines Armes Classiques GGE LAWS, Résolution ONU IA Militaire 2023 & Dix Principes Guterres",
            country="Global",
            sector="Cadre Normatif International LAWS",
            lethal_autonomous_weapon_civilian_harm_severity_score=4.0,
            human_control_accountability_removal_scale_score=4.0,
            ai_bias_targeting_discrimination_score=4.0,
            autonomous_weapon_ban_treaty_deficit_gap_score=4.0,
            primary_pattern="lethal_autonomous_weapon_civilian_harm_severity",
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

    return AutonomousWeaponsAIWarfareRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_autonomous_weapons_ai_warfare_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "icrc_autonomous_weapons_report",
            "stop_killer_robots_campaign_report",
            "un_secretary_general_new_agenda_peace",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_autonomous_weapons_ai_warfare_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_autonomous_weapons_ai_warfare_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
