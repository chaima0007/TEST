"""
Caelum Partners — Deep Sea Mining Geopolitics Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La course aux fonds marins : le dernier territoire non gouverné de la planète.
Les nodules polymétalliques et les sulfures hydrothermaux des grands fonds
recèlent des concentrations exceptionnelles de manganèse, nickel, cobalt,
cuivre et terres rares — les minerais critiques de la transition énergétique
et de la révolution technologique (batteries, aimants permanents, électronique).

La Zone internationale des fonds marins (Zone UNCLOS) est officiellement
"patrimoine commun de l'humanité" géré par l'Autorité Internationale des Fonds
Marins (AIFM/ISA). Mais la Chine a obtenu 5 contrats d'exploration (le plus
grand portefeuille mondial), développe des robots miniers autonomes de dernière
génération et contrôle 70% des terres rares terrestres — une domination
stratégique des minerais critiques qu'elle entend étendre aux fonds marins.
La Russie contrôle des zones dans l'Atlantique Nord et Pacifique, avec
l'avantage additionnel de ses sous-marins pour surveiller câbles et pipelines.

En 2021, Nauru a activé la "règle des deux ans" pour forcer l'ISA à approuver
les réglementations minières avant 2023 malgré l'opposition scientifique —
une tentative de contournement de la gouvernance multilatérale par des États
sponsorisés par des entreprises minières. L'exploitation commerciale des fonds
marins menace des écosystèmes uniques (nodules abritent des espèces endémiques)
et génère des panaches de sédiments potentiellement catastrophiques.

Risk levels (course aux fonds marins et capture géopolitique de la Zone) :
  critique  → composite ≥ 60  (course active — programmes miniers avancés et capture de gouvernance)
  élevé     → composite ≥ 40  (exploitation opportuniste — licences actives sans cadre éthique)
  modéré    → composite ≥ 20  (résistance — moratoires et plaidoyer pour gouvernance multilatérale)
  faible    → composite < 20  (gouvernance — UNCLOS et ISA comme cadre multilatéral préservé)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "course_fonds_marins_active": {
        "severity_fr": "Critique",
        "action_fr": "Moratoire international d'exploitation et réforme de l'ISA pour garantir une gouvernance indépendante des puissances minières",
        "signal_fr": "seabed_territorial_claim_score > 80 AND polymetallic_nodule_extraction_score > 80 — course active aux fonds marins avérée",
    },
    "infrastructure_sous_marine": {
        "severity_fr": "Critique",
        "action_fr": "Protection des câbles et infrastructures sous-marines critiques et surveillance accrue des activités de sous-marins militaires dans la Zone",
        "signal_fr": "Infrastructure sous-marine stratégique — contrôle des câbles, pipelines et corridors sous-marins comme levier géopolitique",
    },
    "extraction_opportuniste": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcer le cadre réglementaire de l'ISA et conditionner les licences d'exploration au respect des normes environnementales et éthiques",
        "signal_fr": "Extraction opportuniste — contrats d'exploration actifs sans garanties environnementales ou de partage équitable des bénéfices",
    },
    "resistance_gouvernance": {
        "severity_fr": "Modéré",
        "action_fr": "Soutenir les moratoires des petits États insulaires et renforcer leur représentation à l'ISA face aux puissances minières",
        "signal_fr": "Résistance à la gouvernance — plaidoyer pour moratoire et protection des écosystèmes des grands fonds contre l'extraction industrielle",
    },
    "gouvernance_multilaterale": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer l'autorité de l'ISA, garantir son indépendance et étendre le principe de patrimoine commun aux nouvelles zones d'exploration",
        "signal_fr": "composite_score < 20 — gouvernance multilatérale préservée — ISA/UNCLOS comme cadre équitable pour les fonds marins internationaux",
    },
}


@dataclass
class DeepSeaMiningEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    seabed_territorial_claim_score: float
    polymetallic_nodule_extraction_score: float
    submarine_infrastructure_control_score: float
    isa_governance_capture_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_deep_sea_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.seabed_territorial_claim_score * 0.30
            + self.polymetallic_nodule_extraction_score * 0.25
            + self.submarine_infrastructure_control_score * 0.25
            + self.isa_governance_capture_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_deep_sea_index = round(self.composite_score / 100 * 10, 2)

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
        if self.seabed_territorial_claim_score >= 80 and self.polymetallic_nodule_extraction_score >= 80:
            return "course_fonds_marins_active"
        if self.submarine_infrastructure_control_score >= 80:
            return "infrastructure_sous_marine"
        if self.composite_score >= 40:
            return "extraction_opportuniste"
        if self.composite_score >= 20:
            return "resistance_gouvernance"
        return "gouvernance_multilaterale"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Course aux fonds marins critique de {n} — programmes d'exploration avancés et stratégie de capture des ressources minières de la Zone",
                "Robots miniers autonomes déployés — technologies d'extraction des nodules polymétalliques et des sulfures hydrothermaux opérationnelles",
                "Capture de gouvernance ISA — influence disproportionnée sur l'Autorité Internationale des Fonds Marins pour accélérer les licences d'exploitation",
            ]
        if self.risk_level == "élevé":
            return [
                f"Extraction opportuniste significative dans {n} — contrats d'exploration actifs sans garanties environnementales suffisantes",
                "Licences ISA exploitées — zones d'exploration étendues sans partage équitable des bénéfices avec les pays en développement",
                "Risque environnemental élevé — panaches de sédiments et destruction d'écosystèmes endémiques des grands fonds non évalués",
            ]
        if self.risk_level == "modéré":
            return [
                f"Résistance à la gouvernance par {n} — plaidoyer pour un moratoire sur l'exploitation commerciale des fonds marins",
                "Protection des écosystèmes prioritaire — opposition scientifique et communautaire à l'extraction industrielle des nodules",
                "Coalition moratoire — alliances des petits États insulaires et ONG pour préserver le principe de patrimoine commun de l'humanité",
            ]
        return [
            f"{n} préserve le cadre multilatéral des fonds marins — gouvernance équitable et transparente de la Zone internationale",
            "UNCLOS comme bouclier multilatéral — principe de patrimoine commun de l'humanité défendu contre les captures unilatérales",
            "Modèle de gouvernance des communs à étendre — ISA réformé et indépendant des intérêts miniers nationaux",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "seabed_territorial_claim_score": self.seabed_territorial_claim_score,
            "polymetallic_nodule_extraction_score": self.polymetallic_nodule_extraction_score,
            "submarine_infrastructure_control_score": self.submarine_infrastructure_control_score,
            "isa_governance_capture_score": self.isa_governance_capture_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_deep_sea_index": self.estimated_deep_sea_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[DeepSeaMiningEntity] = [
    DeepSeaMiningEntity("DS-001", "Chine — Zone ZCC Pacifique & Robots Miniers Autonomes", "Asie", "5 Contrats ISA, Robots Miniers COMRA & 70% Terres Rares — Domination Minière Globale", 92.0, 88.0, 85.0, 80.0),
    DeepSeaMiningEntity("DS-002", "USA — NOAA & Infrastructure Deep Sea Monopole", "Amérique du Nord", "NOAA Exploration, Lockheed Martin Licences & Veto UNCLOS Ratification", 85.0, 90.0, 82.0, 72.0),
    DeepSeaMiningEntity("DS-003", "Russie — Zone Atlantique Nord & Câbles Sous-Marins", "Europe de l'Est", "ISA Contrat Atlantique, Sous-Marins Surveillance Câbles & Infrastructure Dual-Use", 80.0, 75.0, 88.0, 78.0),
    DeepSeaMiningEntity("DS-004", "Nauru — Activation Règle 2 Ans & Sponsored Mining", "Pacifique", "Nauru Ocean Resources & NORI Déclenchant Règle 2 Ans pour Contourner Moratoire ISA", 72.0, 80.0, 68.0, 85.0),
    DeepSeaMiningEntity("DS-005", "Norvège — Ouverture Fonds Marins Arctique", "Europe du Nord", "Licences Arctiques Controversées & 38Md$ Ressources Estimées Malgré Opposition Scientifique", 58.0, 55.0, 48.0, 45.0),
    DeepSeaMiningEntity("DS-006", "France — Zone Clipperton & IFREMER", "Europe/Pacifique", "Zone Clipperton, IFREMER Robotique & Projet Minerve d'Exploitation Fonds Marins", 52.0, 48.0, 45.0, 40.0),
    DeepSeaMiningEntity("DS-007", "Petits États Insulaires Pacifique — Moratoire ISA", "Pacifique", "Coalition Fidji/Palau/Micronésie pour Moratoire & Protection Patrimoine Commun Humanité", 28.0, 22.0, 25.0, 30.0),
    DeepSeaMiningEntity("DS-008", "ISA/UNCLOS — Gouvernance Internationale Fonds Marins", "Global", "Autorité Fonds Marins — 31 Contrats Exploration, Code Minier en Négociation & Réforme Governance", 5.0, 4.0, 6.0, 8.0),
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
        "domain": "deep_sea_mining",
        "confidence_score": 0.74,
        "data_sources": ["isa_exploration_contracts_registry", "deepgreenmetals_seabed_tracker", "greenpeace_deep_sea_mining_watch"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_deep_sea_index": round(avg / 100 * 10, 2),
    }


def analyze_deep_sea_mining() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Deep Sea Mining Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
