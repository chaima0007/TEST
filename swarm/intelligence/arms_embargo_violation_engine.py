"""Arms Embargo Violation Engine — Violations d'embargos sur les armes & complicité étatique."""

from dataclasses import dataclass
from typing import List


@dataclass
class ArmsEmbargoViolationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    embargo_breach_frequency_score: float
    state_complicity_level_score: float
    civil_war_fueling_score: float
    accountability_enforcement_failure_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.embargo_breach_frequency_score * 0.30
            + self.state_complicity_level_score * 0.25
            + self.civil_war_fueling_score * 0.25
            + self.accountability_enforcement_failure_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "violation_embargo_systematique": self.embargo_breach_frequency_score,
            "complicite_etatique_armement": self.state_complicity_level_score,
            "alimentation_conflits_armes": self.civil_war_fueling_score,
            "impunite_violations_embargo": self.accountability_enforcement_failure_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Violation d'embargo sur les armes documentée — {self.name} avec score composite {self.composite_score}/100 révélant des transferts d'armes illicites alimentant des conflits et violant les résolutions du Conseil de Sécurité ONU",
            f"Complicité étatique ({self.state_complicity_level_score}/100) — les États fournisseurs violent leurs obligations sous le Traité sur le Commerce des Armes (TCA/ATT 2014) et les résolutions CS-ONU établissant des embargos contraignants",
            f"Activer le Panel d'Experts CS-ONU pour enquête sur les violations d'embargo et engager des poursuites devant la CPI pour complicité dans des crimes de guerre via fourniture d'armes sous embargo",
        ]

    @property
    def estimated_arms_embargo_violation_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.sector,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "embargo_breach_frequency_score": self.embargo_breach_frequency_score,
            "state_complicity_level_score": self.state_complicity_level_score,
            "civil_war_fueling_score": self.civil_war_fueling_score,
            "accountability_enforcement_failure_score": self.accountability_enforcement_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_arms_embargo_violation_index": self.estimated_arms_embargo_violation_index,
            "last_updated": "2026-06-20",
        }


class ArmsEmbargoViolationEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.78
    DATA_SOURCES = [
        "sipri_arms_transfers_database",
        "un_panel_experts_sanctions_monitoring_reports",
        "arms_control_association_embargo_violations_tracker",
    ]

    def __init__(self):
        self.entities: List[ArmsEmbargoViolationEntity] = [
            ArmsEmbargoViolationEntity(
                "AE-001", "Russie/Corée Nord-Iran — Drones Shaheed/Oreshnik, Munitions RPDC & Embargo Violations",
                "Europe de l'Est/MENA/Asie",
                "Russie Reçoit Drones Iran Shaheed Embargo Violé, Munitions Corée Nord 1.5M Obus Documentés ONU, Ukraine Cibles Civiles & CS-ONU Résolutions 1718/2231 Ignorées",
                92, 95, 90, 88,
            ),
            ArmsEmbargoViolationEntity(
                "AE-002", "Émirats/Arabie Saoudite Yémen — Armes Occidentales Embargo ONU Partiel & Civils",
                "MENA",
                "Armes USA/UK/France Yémen Via EAU/KSA Embargo ONU Partiel Résolution 2216, Cluster Bombs Civils, Panel Experts CS-ONU Violations Documentées & Lobby Défense Pressions",
                88, 82, 95, 85,
            ),
            ArmsEmbargoViolationEntity(
                "AE-003", "Chine/Soudan — Darfour Embargo 2005 Violé, Relations Pétrolières & Impunité",
                "Afrique de l'Est/Asie",
                "Chine Fournit Armes Soudan Embargo ONU 2005 Résolution 1591, Relations Pétrolières CNPC, Khartoum/RSF Armés & Panel Experts ONU Violations Documentées 2005-2024",
                85, 82, 88, 85,
            ),
            ArmsEmbargoViolationEntity(
                "AE-004", "Turquie/Libye — Embargo ONU 2011 Violé, Drones Bayraktar & Mercenaires Syriens",
                "MENA/Europe",
                "Turquie Viole Embargo ONU Libye Résolution 1970 2020, Drones TB2 Transferts Sans Notification, Mercenaires Syriens Déployés & Panel Experts ONU Rapport 2020 Violations",
                82, 80, 85, 82,
            ),
            ArmsEmbargoViolationEntity(
                "AE-005", "France/Arabie Saoudite — Contrats 1Md€/An Légaux Yémen & Complicité Civils",
                "MENA/Europe",
                "France Vente Armes Légales Arabie Saoudite 1Md€/An Dont Yémen, KNDS Caesar Howitzers Yémen, Embargo Partiel Non-Respecté & Rapport Parlement Français Complicité",
                55, 52, 58, 50,
            ),
            ArmsEmbargoViolationEntity(
                "AE-006", "USA/Israël — Transferts Armes Gaza, LEAHY Act Contourné & Embargo Débat Congrès",
                "MENA/Amérique du Nord",
                "USA Transferts Armes Israël 14Md$ 2023-24, LEAHY Act Violations Documentées Amnesty, Bombes 2000lb Populations Civiles & Débat Congrès Conditionnalité Armes Non-Appliquée",
                52, 55, 50, 52,
            ),
            ArmsEmbargoViolationEntity(
                "AE-007", "Union Européenne — Régulation Positions Communes, End-User Certificates & Lacunes",
                "Europe",
                "Position Commune UE 2008/944 Critères Export Armes, End-User Certificates Non-Vérifiés Terrain, Divergences États Membres & Rapport PE Manques Application Embargo",
                28, 30, 28, 25,
            ),
            ArmsEmbargoViolationEntity(
                "AE-008", "SIPRI/TCA-ONU — Traité Commerce Armes 2014 & Panel Experts Sanctions Monitoring",
                "Global",
                "TCA Arms Trade Treaty 2014 116 États Parties, SIPRI Base Données Transferts Armes, Panel Experts CS-ONU Monitoring Embargos & Registre ONU Armes Conventionnelles",
                5, 4, 3, 6,
            ),
        ]

    def summary(self) -> dict:
        data = [e.to_dict() for e in self.entities]
        avg = round(sum(e.composite_score for e in self.entities) / len(self.entities), 2)
        risk_dist: dict = {}
        pattern_dist: dict = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        critical = [e for e in self.entities if e.risk_level == "critique"]
        return {
            "total_entities": len(self.entities),
            "avg_composite": avg,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.name for e in sorted(critical, key=lambda x: -x.composite_score)[:3]],
            "critical_alerts": [f"{e.name}: {e.primary_pattern}" for e in critical],
            "last_analysis": "2026-06-20",
            "engine_version": self.ENGINE_VERSION,
            "domain": "arms_embargo_violation",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_arms_embargo_violation_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = ArmsEmbargoViolationEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
