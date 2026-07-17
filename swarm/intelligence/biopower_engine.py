"""
Caelum Partners — Bio-Power Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le bio-pouvoir au XXIe siècle : contrôle des populations via les corps,
la biométrie, les données génomiques et les politiques reproductives.

Michel Foucault avait théorisé le bio-pouvoir — le contrôle politique
des corps vivants comme nouvelle forme de gouvernance. À l'ère numérique,
ce contrôle s'intensifie : surveillance biométrique de masse, banques
de données génomiques étatiques, politique nataliste/anti-nataliste,
et dépendances pharmaceutiques comme instruments de pouvoir.

Score élevé = intensité élevée du BIO-POUVOIR = risque pour l'autonomie corporelle.

Risk levels :
  critique  → composite ≥ 60  (biopolitique totale)
  élevé     → composite ≥ 40  (surveillance biologique avancée)
  modéré    → composite ≥ 20  (contrôle corporel partiel)
  faible    → composite < 20  (autonomie corporelle préservée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "biopolitique_totale": {
        "severity_fr": "Critique",
        "action_fr": "Droits fondamentaux corporels d'urgence — moratoire sur la surveillance génomique et biométrique",
        "signal_fr": "biometric_surveillance > 80 AND genetic_control > 75 — biopolitique totale en cours",
    },
    "surveillance_biologique": {
        "severity_fr": "Critique",
        "action_fr": "Cadre légal de protection de l'intégrité corporelle et des données biométriques",
        "signal_fr": "Surveillance biologique critique — corps des citoyens sous contrôle étatique ou corporate",
    },
    "controle_corporel_avance": {
        "severity_fr": "Élevé",
        "action_fr": "Régulation de la biométrie et garantie du consentement éclairé pour les données corporelles",
        "signal_fr": "Contrôle corporel avancé — politiques biopolitiques structurant les choix reproductifs",
    },
    "tension_biopolitique": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement des droits à l'intégrité corporelle et encadrement des technologies biométriques",
        "signal_fr": "Tensions biopolitiques modérées — bio-surveillance croissante mais cadre légal présent",
    },
    "autonomie_corporelle": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des protections de l'autonomie corporelle et veille sur les nouvelles biotechnologies",
        "signal_fr": "composite_score < 20 — autonomie corporelle préservée, bio-pouvoir limité par les droits",
    },
}


@dataclass
class BiopowerEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    biometric_surveillance_intensity_score: float
    genetic_data_control_score: float
    pharmaceutical_dependency_score: float
    reproductive_control_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_biopower_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.biometric_surveillance_intensity_score * 0.30
            + self.genetic_data_control_score * 0.25
            + self.pharmaceutical_dependency_score * 0.25
            + self.reproductive_control_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_biopower_index = round(self.composite_score / 100 * 10, 2)

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
        if self.biometric_surveillance_intensity_score >= 80 and self.genetic_data_control_score >= 75:
            return "biopolitique_totale"
        if self.biometric_surveillance_intensity_score >= 65:
            return "surveillance_biologique"
        if self.composite_score >= 45:
            return "controle_corporel_avance"
        if self.composite_score >= 25:
            return "tension_biopolitique"
        return "autonomie_corporelle"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Biopolitique totale dans {n} — corps des citoyens sous surveillance génomique/biométrique",
                "Banques de données génomiques étatiques et biométrie obligatoire systémique",
                "Autonomie reproductive et corporelle structurellement contrainte par l'État",
            ]
        if self.risk_level == "élevé":
            return [
                f"Surveillance biologique avancée dans {n} — contrôle corporel institutionnel",
                "Données biométriques collectées massivement — droits corporels fragilisés",
                "Politiques biopolitiques structurant les comportements reproductifs et sanitaires",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions biopolitiques modérées dans {n} — bio-surveillance croissante",
                "Équilibre fragile entre santé publique et autonomie corporelle individuelle",
                "Régulation biométrique insuffisante face à l'expansion des biotechnologies",
            ]
        return [
            f"{n} préserve l'autonomie corporelle — droits fondamentaux biopolitiques protégés",
            "Cadre légal robuste limitant la bio-surveillance et protégeant les données génomiques",
            "Modèle de résistance au bio-pouvoir à valoriser et diffuser",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "biometric_surveillance_intensity_score": self.biometric_surveillance_intensity_score,
            "genetic_data_control_score": self.genetic_data_control_score,
            "pharmaceutical_dependency_score": self.pharmaceutical_dependency_score,
            "reproductive_control_score": self.reproductive_control_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_biopower_index": self.estimated_biopower_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[BiopowerEntity] = [
    BiopowerEntity("BP-001", "Chine — Biopolitique Totale", "Asie", "Surveillance Génomique & Biométrique Maximale", 98.0, 95.0, 72.0, 90.0),
    BiopowerEntity("BP-002", "Inde — Aadhaar Biométrique", "Asie du Sud", "Biométrie Obligatoire 1.4Md Personnes", 88.0, 82.0, 75.0, 78.0),
    BiopowerEntity("BP-003", "Russie — Bio-Pouvoir Militarisé", "Europe de l'Est", "Contrôle Reproductif & Biométrique d'État", 80.0, 78.0, 70.0, 85.0),
    BiopowerEntity("BP-004", "Moyen-Orient Autoritaire", "MENA", "Contrôle Corporel Religieux & Étatique", 75.0, 70.0, 65.0, 88.0),
    BiopowerEntity("BP-005", "États-Unis — Surveillance Privée", "Amérique du Nord", "Big Pharma & Biométrie Corporative", 65.0, 60.0, 80.0, 55.0),
    BiopowerEntity("BP-006", "Europe — GDPR Partiel", "Europe", "Tension Santé Publique & Droits Corporels", 40.0, 35.0, 45.0, 32.0),
    BiopowerEntity("BP-007", "Corée du Sud — Digital Health", "Asie du Nord-Est", "Santé Numérique Avancée avec Garde-fous", 35.0, 30.0, 38.0, 25.0),
    BiopowerEntity("BP-008", "Nordiques — Autonomie Maximale", "Europe du Nord", "Droits Corporels Exemplaires", 12.0, 10.0, 15.0, 8.0),
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
        "domain": "biopower",
        "confidence_score": 0.74,
        "data_sources": ["biometric_surveillance_index", "genomic_data_tracker", "reproductive_rights_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_biopower_index": round(avg / 100 * 10, 2),
    }


def analyze_biopower() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Bio-Power Engine — {r['total_entities']} zones, avg intensité: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
