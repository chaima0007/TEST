"""Caelum Partners — Quantum Economic Disruption Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.quantum_economic_disruption")


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class EntityRecord:
    entity_id: str
    name: str
    country: str
    sector: str
    cryptographic_vulnerability_score: float   # 0–100, weight 0.30
    economic_disruption_score: float            # 0–100, weight 0.25
    quantum_readiness_gap_score: float          # 0–100, weight 0.25
    geopolitical_exposure_score: float          # 0–100, weight 0.20
    confidence_level: float                     # 0–1
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          cryptographic_vulnerability_score × 0.30
          + economic_disruption_score        × 0.25
          + quantum_readiness_gap_score      × 0.25
          + geopolitical_exposure_score      × 0.20
        """
        score = (
            self.cryptographic_vulnerability_score * 0.30
            + self.economic_disruption_score * 0.25
            + self.quantum_readiness_gap_score * 0.25
            + self.geopolitical_exposure_score * 0.20
        )
        return round(score, 2)

    def _compute_risk_level(self) -> str:
        if self.composite_score >= 60:
            return "critique"
        if self.composite_score >= 40:
            return "élevé"
        if self.composite_score >= 20:
            return "modéré"
        return "faible"

    def _primary_pattern(self) -> str:
        if self.cryptographic_vulnerability_score >= 70:
            return "cryptographic_collapse"
        if self.economic_disruption_score >= 70:
            return "economic_disruption_cascade"
        if self.quantum_readiness_gap_score >= 70:
            return "quantum_readiness_gap"
        if self.geopolitical_exposure_score >= 70:
            return "geopolitical_quantum_race"
        return "quantum_stable"

    def _key_signals(self) -> List[str]:
        """3 domain-specific signals per entity based on entity_id."""
        signals_map: Dict[str, List[str]] = {
            "QED-001": [
                "Algorithmes RSA-2048 exposés aux attaques quantiques",
                "Systèmes financiers sans protection post-quantique",
                "Délai de migration cryptographique insuffisant",
            ],
            "QED-002": [
                "Programme quantique militaire sino-américain en escalade",
                "Investissements quantiques étatiques multipliés par 5",
                "Alliances technologiques quantiques remises en question",
            ],
            "QED-003": [
                "Secteur défense exposé à la disruption économique quantique",
                "Infrastructure critique sans chiffrement post-quantique",
                "Capacités industrielles vulnérables aux avantages quantiques adverses",
            ],
            "QED-004": [
                "Industrie manufacturière en retard sur l'adoption quantique",
                "Chaînes d'approvisionnement non préparées aux perturbations quantiques",
                "Déficit de compétences quantiques dans le secteur industriel",
            ],
            "QED-005": [
                "Écosystème technologique en transition quantique partielle",
                "Adoption quantique insuffisante face aux concurrents asiatiques",
                "Programmes de formation quantique en phase de démarrage",
            ],
            "QED-006": [
                "Exposition modérée aux risques cryptographiques quantiques",
                "Marché financier brésilien en phase d'évaluation quantique",
                "Partenariats internationaux quantiques en cours de négociation",
            ],
            "QED-007": [
                "Système cryptographique partiellement mis à jour",
                "Investissements publics en informatique quantique en cours",
                "Cadre réglementaire quantique avancé et proactif",
            ],
            "QED-008": [
                "Infrastructure bancaire dotée de protections post-quantiques pilotes",
                "Recherche quantique académique de niveau mondial",
                "Stabilité géopolitique favorable à la coopération quantique",
            ],
        }
        return signals_map.get(self.entity_id, [
            "Signal quantique non spécifié",
            "Évaluation en cours",
            "Données insuffisantes",
        ])

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        pattern_name = self._primary_pattern()
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "cryptographic_vulnerability_score": self.cryptographic_vulnerability_score,
            "economic_disruption_score": self.economic_disruption_score,
            "quantum_readiness_gap_score": self.quantum_readiness_gap_score,
            "geopolitical_exposure_score": self.geopolitical_exposure_score,
            "risk_level": self.risk_level,
            "primary_pattern": pattern_name,
            "key_signals": self._key_signals(),
            "estimated_quantum_index": round(self.composite_score / 100 * 10, 2),
            "last_updated": "2026-06-20",
            "confidence_level": self.confidence_level,
        }


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "cryptographic_collapse",
        "severity_fr": "Effondrement Cryptographique",
        "action_fr": "Migration urgente vers cryptographie post-quantique",
        "signal_fr": "Vulnérabilité cryptographique critique détectée",
    },
    {
        "name": "economic_disruption_cascade",
        "severity_fr": "Cascade de Perturbation Économique",
        "action_fr": "Plan de résilience économique quantique prioritaire",
        "signal_fr": "Disruption économique quantique en cours",
    },
    {
        "name": "quantum_readiness_gap",
        "severity_fr": "Fossé de Préparation Quantique",
        "action_fr": "Programme d'adoption quantique accéléré",
        "signal_fr": "Retard critique dans la préparation quantique",
    },
    {
        "name": "geopolitical_quantum_race",
        "severity_fr": "Course Quantique Géopolitique",
        "action_fr": "Alignement stratégique sur les alliances quantiques",
        "signal_fr": "Tension géopolitique quantique élevée",
    },
    {
        "name": "quantum_stable",
        "severity_fr": "Stabilité Quantique",
        "action_fr": "Maintien de la veille quantique proactive",
        "signal_fr": "Système quantique sous contrôle",
    },
]


# ── Engine ────────────────────────────────────────────────────────────────────

class QuantumEconomicDisruptionEngine:
    """
    Swarm Intelligence module for Quantum Economic Disruption tracking.

    Computes composite scores, detects quantum disruption patterns,
    and surfaces actionable insights for the Caelum Partners intelligence platform.

    Composite formula verification:
      QED-001: 85*0.30 + 70*0.25 + 75*0.25 + 65*0.20
             = 25.5 + 17.5 + 18.75 + 13.0 = 74.75  → critique ✓ (cryptographic_collapse)
      QED-002: 60*0.30 + 65*0.25 + 65*0.25 + 80*0.20
             = 18.0 + 16.25 + 16.25 + 16.0 = 66.50  → critique ✓ (geopolitical_quantum_race)
      QED-003: 65*0.30 + 72*0.25 + 60*0.25 + 55*0.20
             = 19.5 + 18.0 + 15.0 + 11.0 = 63.50    → critique ✓ (economic_disruption_cascade)
      QED-004: 55*0.30 + 45*0.25 + 72*0.25 + 38*0.20
             = 16.5 + 11.25 + 18.0 + 7.6 = 53.35     → élevé ✓  (quantum_readiness_gap)
      QED-005: 45*0.30 + 40*0.25 + 75*0.25 + 30*0.20
             = 13.5 + 10.0 + 18.75 + 6.0 = 48.25     → élevé ✓  (quantum_readiness_gap)
      QED-006: 30*0.30 + 28*0.25 + 35*0.25 + 25*0.20
             = 9.0 + 7.0 + 8.75 + 5.0 = 29.75         → modéré ✓ (quantum_stable)
      QED-007: 10*0.30 + 12*0.25 + 15*0.25 + 20*0.20
             = 3.0 + 3.0 + 3.75 + 4.0 = 13.75          → faible ✓ (quantum_stable)
      QED-008: 8*0.30 + 8*0.25 + 10*0.25 + 12*0.20
             = 2.4 + 2.0 + 2.5 + 2.4 = 9.30             → faible ✓ (quantum_stable)
    """

    def __init__(self) -> None:
        self.entities: List[EntityRecord] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "QuantumEconomicDisruptionEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[EntityRecord]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible.
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # cv>=70 → cryptographic_collapse, composite ~74.75
            {
                "entity_id": "QED-001",
                "name": "Federal Reserve Quantum Division",
                "country": "USA",
                "sector": "Finance",
                "cryptographic_vulnerability_score": 85.0,
                "economic_disruption_score": 70.0,
                "quantum_readiness_gap_score": 75.0,
                "geopolitical_exposure_score": 65.0,
                "confidence_level": 0.87,
            },
            # ge>=70 → geopolitical_quantum_race, composite ~66.50
            {
                "entity_id": "QED-002",
                "name": "Sinoquantum Technologies Group",
                "country": "China",
                "sector": "Technology",
                "cryptographic_vulnerability_score": 60.0,
                "economic_disruption_score": 65.0,
                "quantum_readiness_gap_score": 65.0,
                "geopolitical_exposure_score": 80.0,
                "confidence_level": 0.82,
            },
            # ed>=70 → economic_disruption_cascade, composite ~63.50
            {
                "entity_id": "QED-003",
                "name": "Rostec Quantum Defense Systems",
                "country": "Russia",
                "sector": "Defense",
                "cryptographic_vulnerability_score": 65.0,
                "economic_disruption_score": 72.0,
                "quantum_readiness_gap_score": 60.0,
                "geopolitical_exposure_score": 55.0,
                "confidence_level": 0.79,
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # qr>=70 → quantum_readiness_gap, composite ~53.35
            {
                "entity_id": "QED-004",
                "name": "Bundesverband Industrie Quantique",
                "country": "Germany",
                "sector": "Manufacturing",
                "cryptographic_vulnerability_score": 55.0,
                "economic_disruption_score": 45.0,
                "quantum_readiness_gap_score": 72.0,
                "geopolitical_exposure_score": 38.0,
                "confidence_level": 0.84,
            },
            # qr>=70 → quantum_readiness_gap, composite ~48.25
            {
                "entity_id": "QED-005",
                "name": "Tata Quantum Innovation Labs",
                "country": "India",
                "sector": "Technology",
                "cryptographic_vulnerability_score": 45.0,
                "economic_disruption_score": 40.0,
                "quantum_readiness_gap_score": 75.0,
                "geopolitical_exposure_score": 30.0,
                "confidence_level": 0.76,
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            # no sub-score >= 70, composite ~29.75
            {
                "entity_id": "QED-006",
                "name": "Banco do Brasil Quantum Initiative",
                "country": "Brazil",
                "sector": "Finance",
                "cryptographic_vulnerability_score": 30.0,
                "economic_disruption_score": 28.0,
                "quantum_readiness_gap_score": 35.0,
                "geopolitical_exposure_score": 25.0,
                "confidence_level": 0.71,
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            # all low, composite ~13.75
            {
                "entity_id": "QED-007",
                "name": "Canadian Quantum Computing Initiative",
                "country": "Canada",
                "sector": "Technology",
                "cryptographic_vulnerability_score": 10.0,
                "economic_disruption_score": 12.0,
                "quantum_readiness_gap_score": 15.0,
                "geopolitical_exposure_score": 20.0,
                "confidence_level": 0.90,
            },
            # minimal exposure, composite ~9.30
            {
                "entity_id": "QED-008",
                "name": "Swiss National Bank Quantum Lab",
                "country": "Switzerland",
                "sector": "Finance",
                "cryptographic_vulnerability_score": 8.0,
                "economic_disruption_score": 8.0,
                "quantum_readiness_gap_score": 10.0,
                "geopolitical_exposure_score": 12.0,
                "confidence_level": 0.93,
            },
        ]

        return [EntityRecord(**d) for d in raw]  # type: ignore[arg-type]

    # ── Aggregates ────────────────────────────────────────────────────────────

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)
        avg_confidence = round(sum(e.confidence_level for e in self.entities) / n, 2)

        risk_distribution = {
            "critique": sum(1 for e in self.entities if e.risk_level == "critique"),
            "élevé":    sum(1 for e in self.entities if e.risk_level == "élevé"),
            "modéré":   sum(1 for e in self.entities if e.risk_level == "modéré"),
            "faible":   sum(1 for e in self.entities if e.risk_level == "faible"),
        }

        pattern_distribution = {
            p["name"]: sum(1 for e in self.entities if e._primary_pattern() == p["name"])
            for p in PATTERNS
        }

        sorted_entities = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)
        top_risk_entities = [e.name for e in sorted_entities[:3]]
        critical_alerts = [e.name for e in self.entities if e.risk_level == "critique"]

        avg_quantum_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20T00:00:00Z",
            "engine_version": "1.0.0",
            "domain": "quantum",
            "confidence_score": avg_confidence,
            "data_sources": [
                "IMF Quantum Economic Reports",
                "NIST Post-Quantum Standards",
                "Quantum Computing Market Data",
            ],
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_quantum_index": avg_quantum_index,
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[EntityRecord]:
        return [e for e in self.entities if e.risk_level == risk_level]


# ── Module-level function ─────────────────────────────────────────────────────

def analyze_quantum() -> dict:
    return QuantumEconomicDisruptionEngine().summary()
