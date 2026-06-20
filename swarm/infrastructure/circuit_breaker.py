"""
Caelum Partners — Circuit Breaker & Kill Switch
Détecte les boucles infinies, stoppe les agents hors contrôle.
"""
from __future__ import annotations
import time
import hashlib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

logger = logging.getLogger("caelum.circuit_breaker")


class CircuitState(Enum):
    CLOSED = "closed"        # Fonctionnement normal
    OPEN = "open"            # Kill switch déclenché — agent stoppé
    HALF_OPEN = "half_open"  # Tentative de récupération


@dataclass
class TurnRecord:
    turn_index: int
    content_hash: str
    timestamp: float
    token_count: int = 0


@dataclass
class AgentCircuit:
    agent_id: str
    max_turns: int = 10
    loop_detection_window: int = 3   # Nb de tours pour détecter répétition
    state: CircuitState = CircuitState.CLOSED
    turns: List[TurnRecord] = field(default_factory=list)
    trip_reason: str = ""
    tripped_at: Optional[float] = None
    total_tokens: int = 0

    @property
    def turn_count(self) -> int:
        return len(self.turns)

    @property
    def is_alive(self) -> bool:
        return self.state == CircuitState.CLOSED

    def record_turn(self, content: str, token_count: int = 0) -> "CircuitCheckResult":
        """Enregistre un tour et vérifie les conditions de déclenchement."""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        record = TurnRecord(
            turn_index=self.turn_count,
            content_hash=content_hash,
            timestamp=time.time(),
            token_count=token_count,
        )
        self.turns.append(record)
        self.total_tokens += token_count

        # Kill switch: max_turns dépassé
        if self.turn_count >= self.max_turns:
            return self._trip(f"MAX_TURNS_EXCEEDED: {self.turn_count}/{self.max_turns}")

        # Détection boucle: mêmes hashes sur les N derniers tours
        if self.turn_count >= self.loop_detection_window:
            recent = self.turns[-self.loop_detection_window:]
            hashes = [r.content_hash for r in recent]
            if len(set(hashes)) == 1:
                return self._trip(
                    f"INFINITE_LOOP: contenu identique répété {self.loop_detection_window} fois"
                )

        return CircuitCheckResult(allowed=True, state=self.state)

    def _trip(self, reason: str) -> "CircuitCheckResult":
        self.state = CircuitState.OPEN
        self.trip_reason = reason
        self.tripped_at = time.time()
        logger.warning("[CIRCUIT OPEN] Agent %s — %s", self.agent_id, reason)
        return CircuitCheckResult(allowed=False, state=self.state, reason=reason)

    def reset(self) -> None:
        """Réinitialise le circuit (usage manuel ou après correction)."""
        self.state = CircuitState.CLOSED
        self.turns.clear()
        self.trip_reason = ""
        self.tripped_at = None
        self.total_tokens = 0

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "state": self.state.value,
            "turn_count": self.turn_count,
            "max_turns": self.max_turns,
            "total_tokens": self.total_tokens,
            "trip_reason": self.trip_reason,
            "tripped_at": self.tripped_at,
            "is_alive": self.is_alive,
        }


@dataclass
class CircuitCheckResult:
    allowed: bool
    state: CircuitState
    reason: str = ""


class CircuitBreakerRegistry:
    """Registre global des circuits — un par agent_id."""

    def __init__(self) -> None:
        self._circuits: Dict[str, AgentCircuit] = {}

    def get_or_create(self, agent_id: str, max_turns: int = 10) -> AgentCircuit:
        if agent_id not in self._circuits:
            self._circuits[agent_id] = AgentCircuit(
                agent_id=agent_id, max_turns=max_turns
            )
        return self._circuits[agent_id]

    def check(self, agent_id: str, content: str, token_count: int = 0) -> CircuitCheckResult:
        circuit = self._circuits.get(agent_id)
        if circuit is None:
            logger.error("Circuit inconnu pour agent %s", agent_id)
            return CircuitCheckResult(allowed=False, state=CircuitState.OPEN, reason="UNREGISTERED_AGENT")
        return circuit.record_turn(content, token_count)

    def status_all(self) -> List[dict]:
        return [c.to_dict() for c in self._circuits.values()]

    def tripped_agents(self) -> List[str]:
        return [
            agent_id
            for agent_id, c in self._circuits.items()
            if c.state == CircuitState.OPEN
        ]


# Singleton partagé
GLOBAL_CIRCUIT_REGISTRY = CircuitBreakerRegistry()
