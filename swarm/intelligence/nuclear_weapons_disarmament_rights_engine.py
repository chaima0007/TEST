"""
Caelum Partners — Nuclear Weapons Disarmament Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droits humains face aux armes nucléaires : désarmement, populations irradiées
et menaces existentielles à la survie de l'humanité.

Les armes nucléaires constituent l'unique catégorie d'armes de destruction massive
n'ayant pas encore fait l'objet d'une interdiction totale effective. Le Traité sur
la Prohibition des Armes Nucléaires (TPNW, 2017) représente une avancée historique
du droit humanitaire international, mais aucune des 9 puissances nucléaires ne l'a
ratifié. La Russie a suspendu sa participation au traité New START en 2023 et intégré
des menaces nucléaires explicites dans sa doctrine de guerre en Ukraine.

Les tests nucléaires français en Polynésie (1966-1996) et américains aux îles Marshall
(1946-1958) ont exposé des populations civiles à des radiations massives sans
consentement ni indemnisation adéquate pendant des décennies — des violations graves
du droit à la santé et de l'intégrité physique des peuples autochtones du Pacifique.

Risk levels (droits humains et armes nucléaires) :
  critique  -> composite >= 60  (danger existentiel — doctrines nucléaires actives avec cibles civiles)
  élevé     -> composite >= 40  (prolifération active — développement ou modernisation accélérée)
  modéré    -> composite >= 20  (risque résiduel — non-conformité aux traités de désarmement)
  faible    -> composite < 20   (protection exemplaire — engagement désarmement effectif)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "doctrine_nucleaire_escalade_civile": {
        "severity_fr": "Critique",
        "action_fr": "Désescalade immédiate — engagement diplomatique d'urgence, mécanismes hotline nucléaire, pression internationale maximale pour suspension doctrines d'emploi préventif",
        "signal_fr": "nuclear_deterrence_civilian_threat_score > 85 — doctrine nucléaire avec ciblage civil explicite ou implicite, menaces d'emploi en contexte de conflit conventionnel",
    },
    "modernisation_arsenal_proliferation": {
        "severity_fr": "Critique",
        "action_fr": "Gel des modernisations — négociations New START+, inspections AIEA élargies, sanctions économiques ciblées sur programmes nucléaires militaires",
        "signal_fr": "nuclear_arsenal_modernization_proliferation_scale_score > 85 — investissements massifs dans modernisation arsenaux avec nouvelles capacités de frappe et vecteurs hypersoniques",
    },
    "tests_nucleaires_populations_irradiees": {
        "severity_fr": "Critique",
        "action_fr": "Responsabilité et réparation — indemnisation populations irradiées, dépollution des sites d'essais, traitement médical des victimes et moratoire permanent sur les tests",
        "signal_fr": "nuclear_testing_radiation_civilian_harm_severity_score > 85 — tests nucléaires ayant exposé des populations civiles à des radiations massives sans consentement ni réparation",
    },
    "non_conformite_tpnw_npt": {
        "severity_fr": "Élevé",
        "action_fr": "Pression diplomatique — résolutions Assemblée Générale ONU, conditionnalité aide internationale, soutien aux États non-nucléaires pour adhésion TPNW",
        "signal_fr": "Refus de ratification TPNW, non-respect Art.VI TNP sur désarmement ou blocage actif des négociations multilatérales de contrôle des armements nucléaires",
    },
    "desarmement_engagement_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Amplifier standards — financement ICAN, soutien juridique aux victimes d'essais nucléaires et promotion TPNW auprès des États non-signataires",
        "signal_fr": "composite_score < 20 — engagement actif dans le désarmement nucléaire, ratification TPNW et soutien aux populations affectées par les tests",
    },
}


@dataclass
class NuclearWeaponsDisarmamentRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    nuclear_testing_radiation_civilian_harm_severity_score: float
    nuclear_arsenal_modernization_proliferation_scale_score: float
    nuclear_deterrence_civilian_threat_score: float
    tpnw_npt_disarmament_compliance_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_nuclear_weapons_disarmament_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.nuclear_testing_radiation_civilian_harm_severity_score * 0.30
            + self.nuclear_arsenal_modernization_proliferation_scale_score * 0.25
            + self.nuclear_deterrence_civilian_threat_score * 0.25
            + self.tpnw_npt_disarmament_compliance_deficit_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_nuclear_weapons_disarmament_rights_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.nuclear_deterrence_civilian_threat_score >= 85:
            return "doctrine_nucleaire_escalade_civile"
        if self.nuclear_arsenal_modernization_proliferation_scale_score >= 85:
            return "modernisation_arsenal_proliferation"
        if self.nuclear_testing_radiation_civilian_harm_severity_score >= 85:
            return "tests_nucleaires_populations_irradiees"
        if self.composite_score >= 20:
            return "non_conformite_tpnw_npt"
        return "desarmement_engagement_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Menace nucléaire critique de {n} — doctrine d'emploi des armes nucléaires intégrée dans les stratégies militaires actives, avec ciblage potentiel de populations civiles en violation du droit humanitaire international",
                "Violation existentielle des droits humains — les armes nucléaires constituent par nature une violation du droit à la vie et de l'intégrité physique des populations civiles, interdites par le TPNW 2017",
                "Escalade asymétrique incontrôlable — les arsenaux nucléaires modernisés avec vecteurs hypersoniques réduisent les délais d'alerte et augmentent le risque de déclenchement accidentel ou délibéré",
            ]
        if self.risk_level == "élevé":
            return [
                f"Prolifération nucléaire active de {n} — développement ou modernisation accéléré des capacités nucléaires militaires en violation de l'esprit du TNP et des normes de désarmement multilatéral",
                "Risque d'escalade régionale — la possession d'armes nucléaires en contexte de tensions bilatérales crée un risque de calcul erroné pouvant déclencher un conflit nucléaire régional",
                "Impunité de non-conformité — le refus de ratifier le TPNW et le non-respect de l'Art.VI TNP normalisent la possession permanente d'armes nucléaires comme droit acquis des grandes puissances",
            ]
        if self.risk_level == "modéré":
            return [
                f"Non-conformité désarmement de {n} — engagement insuffisant dans les mécanismes multilatéraux de contrôle des armements nucléaires malgré les obligations légales découlant du TNP",
                "Blocage diplomatique — le refus de progresser vers le désarmement nucléaire perpétue un système de sécurité fondé sur la dissuasion mutuellement assurée, menaçant structurellement les droits des populations",
                "Populations irradiées sans réparation — les victimes des essais nucléaires militaires attendent toujours une indemnisation complète et un accès aux soins médicaux spécialisés",
            ]
        return [
            f"{n} incarne l'engagement exemplaire pour le désarmement nucléaire — soutien actif au TPNW, plaidoyer pour les droits des populations affectées par les essais nucléaires et financement des programmes ICAN",
            "Normes humanitaires défendues — la campagne internationale pour l'abolition des armes nucléaires repose sur le droit humanitaire international et les droits fondamentaux à la vie et à la santé",
            "Modèle de désarmement exportable — soutien juridique aux victimes d'essais, promotion du TPNW auprès des États non-signataires et dialogue avec les puissances nucléaires",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "nuclear_testing_radiation_civilian_harm_severity_score": self.nuclear_testing_radiation_civilian_harm_severity_score,
            "nuclear_arsenal_modernization_proliferation_scale_score": self.nuclear_arsenal_modernization_proliferation_scale_score,
            "nuclear_deterrence_civilian_threat_score": self.nuclear_deterrence_civilian_threat_score,
            "tpnw_npt_disarmament_compliance_deficit_gap_score": self.tpnw_npt_disarmament_compliance_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_nuclear_weapons_disarmament_rights_index": self.estimated_nuclear_weapons_disarmament_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[NuclearWeaponsDisarmamentRightsEntity] = [
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-001",
        "Russie/Doctrine Armes Nucléaires Ukraine Escalade",
        "Europe de l'Est",
        "Suspension New START 2023, Menaces Nucléaires Explicites Ukraine, Doctrine Emploi Préventif Modifiée & Essais Missiles Sarmat",
        82.0, 88.0, 92.0, 85.0,
    ),
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-002",
        "USA/Modernisation 1.7 Trillion & Retrait Traités",
        "Amérique du Nord",
        "Plan 1.7T$ Modernisation 30 Ans, Retrait INF 2019 & Open Skies 2020, Trident II D5 & B61-12 Bombes Guidées Précision",
        78.0, 92.0, 82.0, 88.0,
    ),
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-003",
        "Corée du Nord/Tests Miniaturisation Missiles Balistiques",
        "Asie du Nord-Est",
        "6 Tests Nucléaires 2006-2017, Miniaturisation Ogives ICBM, Hwasong-17 Portée USA & Doctrine Emploi Préventif Déclaré",
        88.0, 85.0, 90.0, 80.0,
    ),
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-004",
        "Chine/Expansion Arsenal 350→1 000 Ogives 2030",
        "Asie de l'Est",
        "Arsenal 350 → 1000 Ogives 2030 Pentagon, Silos DF-41 Désert Gobi, Triade Nucléaire Modernisée & Refus Négociations Trilatérales",
        75.0, 90.0, 80.0, 85.0,
    ),
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-005",
        "Pakistan/Inde Kashmir Escalade Nucléaire",
        "Asie du Sud",
        "160 Vs 160 Ogives, Doctrine Première Frappe Pakistan, Nasr Missiles Tactiques, Kashmir Flashpoint & Pas De Hotline Nucléaire",
        55.0, 60.0, 65.0, 58.0,
    ),
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-006",
        "Iran/Enrichissement 84% AIEA Alerte",
        "MENA",
        "Enrichissement 84% Proche Niveau Militaire, AIEA Accès Réduit, JCPOA Mort, Missiles Balistiques & Soutien Proxies Régionaux",
        45.0, 62.0, 55.0, 68.0,
    ),
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-007",
        "ICAN/ICRC Campagne Désarmement & TPNW",
        "Global",
        "Nobel Paix 2017 ICAN, 93 États Ratifié TPNW, ICRC Droit Humanitaire & Plaidoyer Populations Irradiées Pacifique",
        28.0, 18.0, 18.0, 28.0,
    ),
    NuclearWeaponsDisarmamentRightsEntity(
        "NWDR-008",
        "ONU/TPNW 2017 & TNP Art.VI Désarmement",
        "Global",
        "TPNW Entrée Vigueur 2021, TNP 1970 Art.VI Obligation Désarmement, Conférence Désarmement & Mécanismes Vérification",
        5.0, 4.0, 3.0, 8.0,
    ),
]


def summary() -> dict[str, Any]:
    entities = MOCK_ENTITIES
    n = len(entities)
    avg = round(sum(e.composite_score for e in entities) / n, 2)

    risk_dist: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict[str, int] = {k: 0 for k in PATTERNS}
    critical_alerts: list[str] = []
    top_risk: list[str] = []

    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        if e.risk_level == "critique":
            critical_alerts.append(f"{e.name}: {e.primary_pattern.replace('_', ' ')}")
            top_risk.append(e.name)

    return {
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "domain": "nuclear_weapons_disarmament_rights",
        "confidence_score": 0.88,
        "data_sources": [
            "sipri_nuclear_forces_yearbook_2023",
            "ican_nuclear_weapons_ban_monitor",
            "iaea_safeguards_reports",
            "bulletin_atomic_scientists_nuclear_notebook",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_nuclear_weapons_disarmament_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_nuclear_weapons_disarmament_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Nuclear Weapons Disarmament Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
