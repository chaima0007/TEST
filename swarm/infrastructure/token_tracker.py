"""
Caelum Partners — Token Tracker Local vs Cloud
Suit la consommation de tokens par agent, par tier, par session.
"""
from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# Coûts approximatifs en USD/1M tokens (input+output blended)
COST_PER_MILLION_LOCAL = 0.00      # Ollama — gratuit
COST_PER_MILLION_CLOUD_CLAUDE = 3.00  # claude-sonnet-4-6 (blended approx)
COST_PER_MILLION_CLOUD_MISTRAL = 2.00  # Mistral Large (blended approx)


@dataclass
class TokenBudget:
    local_limit: int = 10_000_000    # illimité en pratique
    cloud_limit: int = 100_000       # seuil d'alerte cloud


@dataclass
class TurnUsage:
    turn_index: int
    input_tokens: int
    output_tokens: int
    timestamp: float
    tier: str  # "local" | "cloud"
    model: str

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class AgentTokenStats:
    agent_id: str
    tier: str
    model: str
    turns: List[TurnUsage] = field(default_factory=list)
    session_start: float = field(default_factory=time.time)

    @property
    def total_input(self) -> int:
        return sum(t.input_tokens for t in self.turns)

    @property
    def total_output(self) -> int:
        return sum(t.output_tokens for t in self.turns)

    @property
    def total_tokens(self) -> int:
        return self.total_input + self.total_output

    @property
    def estimated_cost_usd(self) -> float:
        if self.tier == "local":
            return 0.0
        per_million = COST_PER_MILLION_CLOUD_CLAUDE
        return round(self.total_tokens / 1_000_000 * per_million, 6)

    def record(self, input_tokens: int, output_tokens: int, turn_index: int) -> None:
        self.turns.append(TurnUsage(
            turn_index=turn_index,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            timestamp=time.time(),
            tier=self.tier,
            model=self.model,
        ))

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "tier": self.tier,
            "model": self.model,
            "total_input": self.total_input,
            "total_output": self.total_output,
            "total_tokens": self.total_tokens,
            "turn_count": len(self.turns),
            "estimated_cost_usd": self.estimated_cost_usd,
            "session_duration_s": round(time.time() - self.session_start, 1),
        }


class TokenTracker:
    """Suivi centralisé de la consommation tokens de toute la flotte."""

    def __init__(self, budget: Optional[TokenBudget] = None) -> None:
        self._agents: Dict[str, AgentTokenStats] = {}
        self.budget = budget or TokenBudget()
        self._alerts: List[str] = []

    def register(self, agent_id: str, tier: str, model: str) -> None:
        if agent_id not in self._agents:
            self._agents[agent_id] = AgentTokenStats(
                agent_id=agent_id, tier=tier, model=model
            )

    def record(
        self,
        agent_id: str,
        input_tokens: int,
        output_tokens: int,
        turn_index: int = 0,
    ) -> None:
        if agent_id not in self._agents:
            raise KeyError(f"Agent non enregistré: {agent_id}")
        self._agents[agent_id].record(input_tokens, output_tokens, turn_index)
        self._check_budget_alerts()

    def _check_budget_alerts(self) -> None:
        cloud_total = self.total_cloud_tokens()
        if cloud_total > self.budget.cloud_limit:
            msg = f"ALERTE: tokens cloud = {cloud_total} > limite {self.budget.cloud_limit}"
            if msg not in self._alerts:
                self._alerts.append(msg)

    def total_local_tokens(self) -> int:
        return sum(
            s.total_tokens for s in self._agents.values() if s.tier == "local"
        )

    def total_cloud_tokens(self) -> int:
        return sum(
            s.total_tokens for s in self._agents.values() if s.tier == "cloud"
        )

    def total_cost_usd(self) -> float:
        return round(sum(s.estimated_cost_usd for s in self._agents.values()), 6)

    def summary(self) -> dict:
        return {
            "total_agents": len(self._agents),
            "local_agents": sum(1 for s in self._agents.values() if s.tier == "local"),
            "cloud_agents": sum(1 for s in self._agents.values() if s.tier == "cloud"),
            "total_local_tokens": self.total_local_tokens(),
            "total_cloud_tokens": self.total_cloud_tokens(),
            "total_cost_usd": self.total_cost_usd(),
            "budget_cloud_limit": self.budget.cloud_limit,
            "alerts": self._alerts.copy(),
            "agents": [s.to_dict() for s in self._agents.values()],
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.summary(), indent=2, ensure_ascii=False))

    @classmethod
    def load(cls, path: Path) -> "TokenTracker":
        tracker = cls()
        if not path.exists():
            return tracker
        data = json.loads(path.read_text())
        for agent_data in data.get("agents", []):
            tracker.register(
                agent_data["agent_id"],
                agent_data["tier"],
                agent_data["model"],
            )
        return tracker


# Singleton partagé
GLOBAL_TOKEN_TRACKER = TokenTracker()
