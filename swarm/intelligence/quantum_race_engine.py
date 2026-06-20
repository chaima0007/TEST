"""
Caelum Partners — Quantum Race Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La course à la suprématie quantique : la bataille technologique la plus
décisive du siècle. Un ordinateur quantique suffisamment puissant pourrait
briser en quelques heures tous les chiffrements qui protègent les banques,
les militaires et les communications mondiales — RSA, ECC, AES. Qui atteint
la suprématie quantique en premier dispose d'une capacité de déchiffrement
totale de toutes les communications adverses actuelles et passées.

La Chine a investi 15 milliards de dollars dans le calcul quantique, lancé
le satellite quantique MICIUS pour les communications QKD, et développe
des algorithmes quantiques pour optimiser ses armes autonomes. Les États-Unis
ont le National Quantum Initiative (1,2Md$), IBM Quantum Heron à 133 qubits,
Google Willow à 105 qubits, mais perdent leur avance exclusive. La Russie
intègre les technologies quantiques dans ses systèmes de défense via Rosatom
et l'Institut Kurchatov. L'UE investit 1Md€ dans le Quantum Flagship et
l'EuroQCI — infrastructure de communication quantique paneuropéenne.

La "récolte maintenant, décrypte plus tard" (harvest now, decrypt later)
signifie que des États stockent dès aujourd'hui des communications chiffrées
en attendant d'avoir l'outil quantique pour les ouvrir. La course est
existentielle : arriver second, c'est n'avoir aucun secret.

Risk levels (course à la suprématie quantique et militarisation) :
  critique  → composite ≥ 60  (programme quantique militaire avancé — menace cryptographique réelle)
  élevé     → composite ≥ 40  (investissements quantiques significatifs et capacités émergentes)
  modéré    → composite ≥ 20  (programme quantique civil — potentiel de conversion militaire)
  faible    → composite < 20  (retard technologique — fracture quantique)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "suprematie_quantique_course": {
        "severity_fr": "Critique",
        "action_fr": "Traité international de non-prolifération quantique et protection des infrastructures cryptographiques critiques",
        "signal_fr": "quantum_supremacy_investment_score > 80 AND cryptographic_vulnerability_exploitation_score > 80 — course à la suprématie",
    },
    "militarisation_quantique": {
        "severity_fr": "Critique",
        "action_fr": "Régulation internationale de l'intégration militaire des technologies quantiques et normes de non-première-frappe",
        "signal_fr": "Militarisation quantique — intégration offensive des technologies quantiques dans les arsenaux militaires",
    },
    "programme_quantique_avance": {
        "severity_fr": "Élevé",
        "action_fr": "Accélération de la migration post-quantique des infrastructures critiques et coopération R&D défensive",
        "signal_fr": "Programme quantique avancé — capacités significatives sans encore atteindre la suprématie opérationnelle",
    },
    "capacites_quantiques_emergentes": {
        "severity_fr": "Modéré",
        "action_fr": "Intégration dans les alliances quantiques et préparation préventive à la cryptographie post-quantique",
        "signal_fr": "Capacités quantiques émergentes — programmes civils avec potentiel de conversion militaire à moyen terme",
    },
    "fracture_quantique": {
        "severity_fr": "Faible",
        "action_fr": "Programmes de renforcement des capacités quantiques via transferts technologiques et coopération internationale",
        "signal_fr": "composite_score < 20 — fracture quantique — retard technologique majeur sans capacités quantiques significatives",
    },
}


@dataclass
class QuantumRaceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    quantum_supremacy_investment_score: float
    cryptographic_vulnerability_exploitation_score: float
    quantum_talent_monopolization_score: float
    quantum_weapons_integration_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_quantum_dominance_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.quantum_supremacy_investment_score * 0.30
            + self.cryptographic_vulnerability_exploitation_score * 0.25
            + self.quantum_talent_monopolization_score * 0.25
            + self.quantum_weapons_integration_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_quantum_dominance_index = round(self.composite_score / 100 * 10, 2)

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
        if self.quantum_supremacy_investment_score >= 80 and self.cryptographic_vulnerability_exploitation_score >= 80:
            return "suprematie_quantique_course"
        if self.quantum_weapons_integration_score >= 75:
            return "militarisation_quantique"
        if self.composite_score >= 40:
            return "programme_quantique_avance"
        if self.composite_score >= 20:
            return "capacites_quantiques_emergentes"
        return "fracture_quantique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Course à la suprématie quantique critique dans {n} — investissements massifs menaçant la cryptographie mondiale",
                "Stratégie 'récolte maintenant, décrypte plus tard' — stockage de communications chiffrées en attente de la clé quantique",
                "Militarisation quantique — ordinateurs quantiques intégrés dans les systèmes de renseignement et d'armement offensif",
            ]
        if self.risk_level == "élevé":
            return [
                f"Programme quantique avancé dans {n} — capacités significatives et course aux qubits en accélération",
                "Investissements en cryptographie post-quantique offensive — développement d'algorithmes quantiques de cassage",
                "Concentration des talents quantiques — recrutement mondial pour maintenir l'avantage technologique",
            ]
        if self.risk_level == "modéré":
            return [
                f"Capacités quantiques émergentes dans {n} — programme civil avec potentiel de conversion militaire",
                "Partenariats quantiques internationaux — accès aux ecosystèmes quantiques via alliances technologiques",
                "Migration post-quantique en cours — mise à jour progressive des infrastructures cryptographiques nationales",
            ]
        return [
            f"{n} accuse un retard technologique quantique significatif — fracture numérique à l'ère quantique",
            "Dépendance aux fournisseurs quantiques étrangers — vulnérabilité souveraine dans les communications sécurisées",
            "Opportunité de rattrapage — coopération internationale et transferts technologiques comme leviers de montée en puissance",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "quantum_supremacy_investment_score": self.quantum_supremacy_investment_score,
            "cryptographic_vulnerability_exploitation_score": self.cryptographic_vulnerability_exploitation_score,
            "quantum_talent_monopolization_score": self.quantum_talent_monopolization_score,
            "quantum_weapons_integration_score": self.quantum_weapons_integration_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_quantum_dominance_index": self.estimated_quantum_dominance_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[QuantumRaceEntity] = [
    QuantumRaceEntity("QR-001", "Chine — Programme Quantique Souverain & MICIUS", "Asie", "15Md$ Investis, Satellite MICIUS QKD & Algorithmes Quantiques Militaires", 95.0, 92.0, 90.0, 88.0),
    QuantumRaceEntity("QR-002", "USA — IBM/Google Willow & NSA Post-Quantum", "Amérique du Nord", "National Quantum Initiative 1.2Md$, Willow 105 Qubits & DARPA Quantum", 90.0, 88.0, 85.0, 82.0),
    QuantumRaceEntity("QR-003", "Russie — Rosatom Quantique & Intégration Défense", "Europe de l'Est", "Institut Kurchatov & Technopolis Quantique — Intégration Systèmes Militaires", 72.0, 68.0, 65.0, 78.0),
    QuantumRaceEntity("QR-004", "UE — EuroQCI & Quantum Flagship 1Md€", "Europe", "Infrastructure QCI Paneuropéenne & Partenariats IBM/Atos QuantumLeap", 65.0, 60.0, 58.0, 55.0),
    QuantumRaceEntity("QR-005", "Royaume-Uni — NQCC National Quantum Computing Centre", "Europe", "Oxford/Cambridge Quantum Hub & Partenariats Défense GCHQ Quantique", 55.0, 52.0, 50.0, 45.0),
    QuantumRaceEntity("QR-006", "Inde — National Mission on Quantum Technologies", "Asie du Sud", "6000Cr₹ Mission Quantique & IIT Recherche Algorithmes Quantiques", 48.0, 42.0, 45.0, 40.0),
    QuantumRaceEntity("QR-007", "Canada — Périmètre Institute & D-Wave", "Amériques", "D-Wave Recuit Quantique & Waterloo Institute for Quantum Computing", 35.0, 30.0, 38.0, 28.0),
    QuantumRaceEntity("QR-008", "Afrique & MENA — Fracture Quantique", "Global", "Absence d'Écosystème Quantique Local — Dépendance Totale aux Fournisseurs Étrangers", 8.0, 5.0, 6.0, 4.0),
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
        "domain": "quantum_race",
        "confidence_score": 0.76,
        "data_sources": ["mckinsey_quantum_technology_monitor", "national_quantum_initiative_tracker", "ieee_quantum_week_proceedings"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_quantum_dominance_index": round(avg / 100 * 10, 2),
    }


def analyze_quantum_race() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Quantum Race Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
