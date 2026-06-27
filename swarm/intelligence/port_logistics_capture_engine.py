"""
Caelum Partners — Port & Logistics Capture Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La capture des infrastructures portuaires et logistiques comme stratégie
de puissance douce et de projection militaire : celui qui contrôle les
ports contrôle les flux commerciaux, les routes de ravitaillement et
potentiellement la mobilité militaire des flottes adverses. La Chine a
construit un collier de perles (String of Pearls) — réseau de ports
stratégiques de la Mer Rouge à la Mer de Chine du Sud.

Le Port de Hambantota au Sri Lanka : incapable de rembourser la dette
chinoise, Sri Lanka a cédé le port pour 99 ans à China Merchants Port
Holdings en 2017. Le Port du Pirée en Grèce : COSCO contrôle 51% depuis
2016, faisant du Pirée la porte d'entrée de la Chine en Europe. Le Port
de Gwadar au Pakistan : terminus du Corridor Économique Chine-Pakistan
(CPEC 62Md$) avec présence navale chinoise croissante. Djibouti : première
base militaire étrangère chinoise depuis 2017, point de contrôle du
Bab-el-Mandeb par où transitent 12% du commerce mondial.

Les États-Unis s'alarment : l'entreprise chinoise SIPG avait obtenu une
concession sur le Port de Haïfa (Israël) jusqu'à ce que la pression
américaine conduise à son réexamen. L'Italie a signé des mémorandums BRI
pour Trieste et Augusta. L'Allemagne a débattu de la participation COSCO
à Hambourg. La logistique est le nouveau champ de bataille géopolitique.

Risk levels (capture portuaire et dépendance logistique stratégique) :
  critique  → composite ≥ 60  (capture portuaire avérée — présence militaire ou cession souveraine)
  élevé     → composite ≥ 40  (pénétration logistique significative — dépendance stratégique)
  modéré    → composite ≥ 20  (vulnérabilité partielle — acquisition minoritaire sans contrôle)
  faible    → composite < 20  (résilience infrastructurelle — résistance aux acquisitions étrangères)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "capture_portuaire_strategique": {
        "severity_fr": "Critique",
        "action_fr": "Audit des cessions portuaires à des acteurs étrangers et récupération de contrôle via rachats nationaux ou alliés",
        "signal_fr": "chinese_port_acquisition_score > 80 AND strategic_chokepoint_control_score > 85 — capture portuaire avérée",
    },
    "chokepoint_naval_dual": {
        "severity_fr": "Critique",
        "action_fr": "Déploiement de contre-présences navales alliées et audits de sécurité des infrastructures portuaires critiques",
        "signal_fr": "Chokepoint naval dual — port stratégique utilisé comme base militaire et levier de contrôle maritime mondial",
    },
    "penetration_logistique": {
        "severity_fr": "Élevé",
        "action_fr": "Screening renforcé des investissements étrangers dans les infrastructures portuaires et revue des concessions existantes",
        "signal_fr": "Pénétration logistique — acquisitions portuaires partielles créant des dépendances sans contrôle total",
    },
    "vulnerabilite_partielle": {
        "severity_fr": "Modéré",
        "action_fr": "Transparence des concessions portuaires et évaluation des risques géopolitiques des actionnariats étrangers",
        "signal_fr": "Vulnérabilité partielle — participations étrangères minoritaires dans des infrastructures logistiques sensibles",
    },
    "resilience_portuaire": {
        "severity_fr": "Faible",
        "action_fr": "Partager les bonnes pratiques de screening des investissements portuaires et de résilience logistique nationale",
        "signal_fr": "composite_score < 20 — résilience portuaire exemplaire et résistance aux acquisitions étrangères stratégiques",
    },
}


@dataclass
class PortLogisticsCaptureEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    chinese_port_acquisition_score: float
    strategic_chokepoint_control_score: float
    logistics_dependency_score: float
    dual_use_infrastructure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_port_capture_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.chinese_port_acquisition_score * 0.30
            + self.strategic_chokepoint_control_score * 0.25
            + self.logistics_dependency_score * 0.25
            + self.dual_use_infrastructure_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_port_capture_index = round(self.composite_score / 100 * 10, 2)

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
        if self.chinese_port_acquisition_score >= 80 and self.strategic_chokepoint_control_score >= 85:
            return "capture_portuaire_strategique"
        if self.strategic_chokepoint_control_score >= 88:
            return "chokepoint_naval_dual"
        if self.composite_score >= 40:
            return "penetration_logistique"
        if self.composite_score >= 20:
            return "vulnerabilite_partielle"
        return "resilience_portuaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Capture portuaire critique dans {n} — infrastructure stratégique sous contrôle ou influence étrangère décisive",
                "Cession souveraine d'infrastructure logistique — port ou terminal concédé à long terme à un acteur étatique étranger",
                "Risque de double usage — infrastructure portuaire potentiellement utilisable pour projection militaire adverse",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pénétration logistique significative dans {n} — participations étrangères créant des dépendances stratégiques",
                "Acquisitions portuaires partielles — prise de positions minoritaires dans des nœuds logistiques critiques",
                "Surveillance déficiente des investissements étrangers — insuffisance des mécanismes de screening géopolitique",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité portuaire partielle dans {n} — expositions limitées aux acquisitions étrangères sensibles",
                "Débat national sur la souveraineté logistique — réévaluation des concessions portuaires sous pression géopolitique",
                "Mécanismes de screening à renforcer — cadre réglementaire insuffisant face aux stratégies d'acquisition étrangères",
            ]
        return [
            f"{n} maintient une résilience portuaire exemplaire — résistance aux acquisitions étrangères stratégiques",
            "Screening rigoureux des investissements dans les infrastructures critiques — blocage des acquisitions géopolitiquement sensibles",
            "Modèle de souveraineté logistique à partager — gouvernance transparente et indépendante des infrastructures portuaires",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "chinese_port_acquisition_score": self.chinese_port_acquisition_score,
            "strategic_chokepoint_control_score": self.strategic_chokepoint_control_score,
            "logistics_dependency_score": self.logistics_dependency_score,
            "dual_use_infrastructure_score": self.dual_use_infrastructure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_port_capture_index": self.estimated_port_capture_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[PortLogisticsCaptureEntity] = [
    PortLogisticsCaptureEntity("PL-001", "Sri Lanka — Hambantota Cédé 99 Ans à Chine", "Asie du Sud", "Piège Dette CPEC — Hambantota à China Merchants Holdings 99 Ans en 2017", 92.0, 88.0, 90.0, 85.0),
    PortLogisticsCaptureEntity("PL-002", "Pakistan — Gwadar CPEC & Présence Navale Chinoise", "Asie du Sud", "62Md$ CPEC, Gwadar Port Opéré par Chine & Flotte PLAN en Expansion", 88.0, 85.0, 88.0, 82.0),
    PortLogisticsCaptureEntity("PL-003", "Grèce — Pirée COSCO 51% — Porte de l'UE", "Europe du Sud", "COSCO 51% Pirée depuis 2016 — Premier Port Européen Sous Contrôle Chinois", 80.0, 82.0, 78.0, 75.0),
    PortLogisticsCaptureEntity("PL-004", "Djibouti — Base Militaire Chinoise & Bab-el-Mandeb", "Afrique de l'Est", "1ère Base Militaire Chinoise à l'Étranger & 12% Commerce Mondial en Transit", 78.0, 92.0, 85.0, 88.0),
    PortLogisticsCaptureEntity("PL-005", "Israël — Haïfa SIPG & Pression USA", "MENA", "Concession SIPG Port Haïfa — USA Alarmés par Présence Chinoise Côte Maritime", 60.0, 55.0, 65.0, 58.0),
    PortLogisticsCaptureEntity("PL-006", "Italie — Trieste & Augusta dans BRI", "Europe du Sud", "Mémorandums BRI Ports Trieste/Augusta — Avant Retrait Meloni sous Pression OTAN", 55.0, 48.0, 58.0, 52.0),
    PortLogisticsCaptureEntity("PL-007", "Allemagne — Hamburg COSCO 24% Réduit", "Europe", "Débat National COSCO 35%→24% Hambourg — Compromis sous Pression Sécuritaire", 35.0, 30.0, 38.0, 28.0),
    PortLogisticsCaptureEntity("PL-008", "USA & Australie — Five Eyes Résistance Acquisitions", "Global/Pacifique", "CFIUS/FIRB Bloquant Acquisitions Chinoises & Infrastructure Defense Hardening", 6.0, 5.0, 8.0, 4.0),
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
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "port_logistics_capture",
        "confidence_score": 0.83,
        "data_sources": ["csis_china_port_tracker", "occrp_bri_port_investigation", "c4ads_strategic_infrastructure_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_port_capture_index": round(avg / 100 * 10, 2),
    }


def analyze_port_logistics_capture() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Port Logistics Capture Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
