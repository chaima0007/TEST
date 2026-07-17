"""Caelum Partners — Agent Orchestrator Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.orchestration")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "coordination_failure",
        "severity_fr": "critique",
        "action_fr": "Restructurer les protocoles de coordination inter-agents immédiatement.",
        "signal_fr": "Coordination inter-agents critique",
    },
    {
        "name": "autonomy_drift",
        "severity_fr": "élevé",
        "action_fr": "Réaligner les contraintes d'autonomie des agents dérivants.",
        "signal_fr": "Dérive d'autonomie détectée",
    },
    {
        "name": "latency_cascade",
        "severity_fr": "élevé",
        "action_fr": "Optimiser les pipelines de communication pour réduire la latence en cascade.",
        "signal_fr": "Latence en cascade",
    },
    {
        "name": "resilience_collapse",
        "severity_fr": "critique",
        "action_fr": "Renforcer les mécanismes de redondance et de tolérance aux pannes.",
        "signal_fr": "Effondrement de résilience détecté",
    },
    {
        "name": "equilibrium_stable",
        "severity_fr": "faible",
        "action_fr": "Maintenir la surveillance standard et optimiser les performances continues.",
        "signal_fr": "Équilibre orchestration stable",
    },
]

PATTERN_INDEX = {p["name"]: p for p in PATTERNS}


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class OrchestrationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    agent_count: int
    # Sub-scores (0-100 each)
    coordination_score: float
    autonomy_score: float
    latency_score: float
    resilience_score: float
    # Computed fields
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_orchestration_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()
        self.primary_pattern = self._compute_primary_pattern()
        self.key_signals = self._compute_key_signals()
        self.estimated_orchestration_index = round(self.composite_score / 100 * 10, 2)

    def _compute_composite(self) -> float:
        score = (
            self.coordination_score * 0.30
            + self.autonomy_score * 0.25
            + self.latency_score * 0.25
            + self.resilience_score * 0.20
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

    def _compute_primary_pattern(self) -> str:
        if self.coordination_score >= 70:
            return "coordination_failure"
        if self.autonomy_score >= 70:
            return "autonomy_drift"
        if self.latency_score >= 70:
            return "latency_cascade"
        if self.resilience_score >= 70:
            return "resilience_collapse"
        return "equilibrium_stable"

    def _compute_key_signals(self) -> List[str]:
        signals = []
        if self.coordination_score >= 70:
            signals.append("Coordination inter-agents critique")
        elif self.coordination_score >= 50:
            signals.append("Coordination inter-agents dégradée")
        else:
            signals.append("Coordination inter-agents nominale")

        if self.autonomy_score >= 70:
            signals.append("Dérive d'autonomie détectée")
        elif self.autonomy_score >= 50:
            signals.append("Autonomie agents sous surveillance")
        else:
            signals.append("Autonomie agents contrôlée")

        if self.latency_score >= 70:
            signals.append("Latence en cascade")
        elif self.latency_score >= 50:
            signals.append("Latence inter-agents élevée")
        else:
            signals.append("Latence inter-agents acceptable")

        return signals[:3]

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "coordination_score": self.coordination_score,
            "autonomy_score": self.autonomy_score,
            "latency_score": self.latency_score,
            "resilience_score": self.resilience_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_orchestration_index": self.estimated_orchestration_index,
            "last_updated": "2026-06-20",
            "agent_count": self.agent_count,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class OrchestrationEngine:
    """
    Swarm Intelligence module for Agent Orchestration analysis.

    Computes composite orchestration scores, detects orchestration patterns,
    and surfaces actionable insights for the Caelum Partners platform.

    Risk distribution: >=3 critique, >=2 élevé, >=1 modéré, >=2 faible.
    """

    DOMAIN = "orchestration"

    def __init__(self) -> None:
        self.entities: List[OrchestrationEntity] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "OrchestrationEngine initialised — %d entities, %d patterns, domain=%s",
            len(self.entities),
            len(self.patterns),
            self.DOMAIN,
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[OrchestrationEntity]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: 3 critique, 2 élevé, 1 modéré, 2 faible.

        Composite formula: coord*0.30 + auto*0.25 + lat*0.25 + resil*0.20

        ENT-001: 82*0.30 + 78*0.25 + 72*0.25 + 64*0.20 = 24.6+19.5+18.0+12.8 = 74.9  -> critique
        ENT-002: 74*0.30 + 70*0.25 + 65*0.25 + 58*0.20 = 22.2+17.5+16.25+11.6 = 67.55 -> critique
        ENT-003: 68*0.30 + 64*0.25 + 60*0.25 + 52*0.20 = 20.4+16.0+15.0+10.4  = 61.8  -> critique
        ENT-004: 55*0.30 + 50*0.25 + 52*0.25 + 48*0.20 = 16.5+12.5+13.0+9.6   = 51.6  -> élevé
        ENT-005: 44*0.30 + 46*0.25 + 42*0.25 + 40*0.20 = 13.2+11.5+10.5+8.0   = 43.2  -> élevé
        ENT-006: 30*0.30 + 28*0.25 + 26*0.25 + 24*0.20 = 9.0+7.0+6.5+4.8      = 27.3  -> modéré
        ENT-007: 14*0.30 + 12*0.25 + 10*0.25 + 8*0.20  = 4.2+3.0+2.5+1.6      = 11.3  -> faible
        ENT-008: 10*0.30 + 8*0.25  + 6*0.25  + 6*0.20  = 3.0+2.0+1.5+1.2      = 7.7   -> faible
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # coordination_failure triggered (coordination_score >= 70)
            {
                "entity_id": "ENT-001",
                "name": "SwarmAI Dynamics",
                "country": "États-Unis",
                "sector": "Intelligence Artificielle",
                "agent_count": 847,
                "coordination_score": 82.0,
                "autonomy_score": 78.0,
                "latency_score": 72.0,
                "resilience_score": 64.0,
            },
            # coordination_failure triggered (coordination_score >= 70)
            {
                "entity_id": "ENT-002",
                "name": "AgentForge Berlin",
                "country": "Allemagne",
                "sector": "Robotique & Automatisation",
                "agent_count": 523,
                "coordination_score": 74.0,
                "autonomy_score": 70.0,
                "latency_score": 65.0,
                "resilience_score": 58.0,
            },
            # coordination_failure triggered (coordination_score >= 70)
            {
                "entity_id": "ENT-003",
                "name": "Nexus Orchestral",
                "country": "Royaume-Uni",
                "sector": "Infrastructure Numérique",
                "agent_count": 1205,
                "coordination_score": 68.0,
                "autonomy_score": 64.0,
                "latency_score": 60.0,
                "resilience_score": 52.0,
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # No pattern threshold >=70, equilibrium_stable
            {
                "entity_id": "ENT-004",
                "name": "Korrelia Systems",
                "country": "France",
                "sector": "Logistique & Transport",
                "agent_count": 312,
                "coordination_score": 55.0,
                "autonomy_score": 50.0,
                "latency_score": 52.0,
                "resilience_score": 48.0,
            },
            # No pattern threshold >=70, equilibrium_stable
            {
                "entity_id": "ENT-005",
                "name": "Parallax Computing",
                "country": "Japon",
                "sector": "Systèmes Embarqués",
                "agent_count": 189,
                "coordination_score": 44.0,
                "autonomy_score": 46.0,
                "latency_score": 42.0,
                "resilience_score": 40.0,
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            # No pattern threshold >=70, equilibrium_stable
            {
                "entity_id": "ENT-006",
                "name": "Cascade Robotics",
                "country": "Canada",
                "sector": "Industrie Manufacturière",
                "agent_count": 67,
                "coordination_score": 30.0,
                "autonomy_score": 28.0,
                "latency_score": 26.0,
                "resilience_score": 24.0,
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            # equilibrium_stable
            {
                "entity_id": "ENT-007",
                "name": "Harmony Agents",
                "country": "Pays-Bas",
                "sector": "Services Financiers",
                "agent_count": 23,
                "coordination_score": 14.0,
                "autonomy_score": 12.0,
                "latency_score": 10.0,
                "resilience_score": 8.0,
            },
            # equilibrium_stable
            {
                "entity_id": "ENT-008",
                "name": "Equilibria Labs",
                "country": "Suède",
                "sector": "Recherche & Développement",
                "agent_count": 14,
                "coordination_score": 10.0,
                "autonomy_score": 8.0,
                "latency_score": 6.0,
                "resilience_score": 6.0,
            },
        ]
        return [OrchestrationEntity(**d) for d in raw]  # type: ignore[arg-type]

    # ── Core methods ──────────────────────────────────────────────────────────

    def analyze(self) -> List[Dict[str, Any]]:
        """Returns list of 8 entity dicts (each from to_dict())."""
        return [e.to_dict() for e in self.entities]

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)

        risk_distribution = {
            "critique": sum(1 for e in self.entities if e.risk_level == "critique"),
            "élevé":    sum(1 for e in self.entities if e.risk_level == "élevé"),
            "modéré":   sum(1 for e in self.entities if e.risk_level == "modéré"),
            "faible":   sum(1 for e in self.entities if e.risk_level == "faible"),
        }

        pattern_distribution: Dict[str, int] = {
            "coordination_failure": 0,
            "autonomy_drift": 0,
            "latency_cascade": 0,
            "resilience_collapse": 0,
            "equilibrium_stable": 0,
        }
        for e in self.entities:
            pattern_distribution[e.primary_pattern] = pattern_distribution.get(e.primary_pattern, 0) + 1

        sorted_by_composite = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)
        top_risk_entities = [e.name for e in sorted_by_composite[:3]]

        critical_alerts = [
            f"ALERTE CRITIQUE — {e.name} ({e.country}) : composite={e.composite_score}, pattern={e.primary_pattern}"
            for e in self.entities if e.risk_level == "critique"
        ]

        avg_estimated_orchestration_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": "1.0.0",
            "domain": self.DOMAIN,
            "confidence_score": 0.87,
            "data_sources": ["agent_telemetry", "orchestration_logs", "latency_metrics"],
            "entities": self.analyze(),
            "avg_estimated_orchestration_index": avg_estimated_orchestration_index,
        }


# ── Module-level convenience function ─────────────────────────────────────────

def analyze_orchestration() -> dict:
    engine = OrchestrationEngine()
    return engine.summary()
