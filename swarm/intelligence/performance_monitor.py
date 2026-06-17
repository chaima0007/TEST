"""
Performance Monitor — tracks agent health and task metrics across all 6 divisions.

Monitors:
  - Tasks completed / failed / queued per agent
  - Average response time per agent
  - Uptime / error rate
  - Division-level aggregates
  - Alert generation for degraded agents

Does NOT use async — polling is handled by the caller (celery beat / FastAPI background).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


# ── Status ────────────────────────────────────────────────────────────────────

class AgentHealth(str, Enum):
    HEALTHY   = "healthy"
    DEGRADED  = "degraded"
    CRITICAL  = "critical"
    OFFLINE   = "offline"


# ── Agent metrics ─────────────────────────────────────────────────────────────

@dataclass
class AgentStats:
    agent_id: str
    division: int
    tasks_completed: int = 0
    tasks_failed: int = 0
    tasks_queued: int = 0
    total_response_time_ms: float = 0.0
    last_heartbeat: float = field(default_factory=time.time)
    last_error: Optional[str] = None

    @property
    def error_rate(self) -> float:
        total = self.tasks_completed + self.tasks_failed
        return self.tasks_failed / total if total else 0.0

    @property
    def avg_response_time_ms(self) -> float:
        return self.total_response_time_ms / self.tasks_completed if self.tasks_completed else 0.0

    @property
    def health(self) -> AgentHealth:
        age = time.time() - self.last_heartbeat
        if age > 300:      return AgentHealth.OFFLINE
        if self.error_rate >= 0.25: return AgentHealth.CRITICAL
        if self.error_rate >= 0.10: return AgentHealth.DEGRADED
        return AgentHealth.HEALTHY

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "division": self.division,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "tasks_queued": self.tasks_queued,
            "error_rate": round(self.error_rate, 4),
            "avg_response_time_ms": round(self.avg_response_time_ms, 1),
            "health": self.health.value,
            "last_error": self.last_error,
            "seconds_since_heartbeat": round(time.time() - self.last_heartbeat, 1),
        }


@dataclass
class DivisionStats:
    division: int
    name: str
    agents: List[AgentStats] = field(default_factory=list)

    @property
    def healthy_count(self) -> int:
        return sum(1 for a in self.agents if a.health == AgentHealth.HEALTHY)

    @property
    def total_tasks(self) -> int:
        return sum(a.tasks_completed for a in self.agents)

    @property
    def total_errors(self) -> int:
        return sum(a.tasks_failed for a in self.agents)

    @property
    def division_error_rate(self) -> float:
        total = self.total_tasks + self.total_errors
        return self.total_errors / total if total else 0.0

    @property
    def avg_response_time_ms(self) -> float:
        active = [a for a in self.agents if a.tasks_completed > 0]
        return sum(a.avg_response_time_ms for a in active) / len(active) if active else 0.0

    @property
    def health(self) -> AgentHealth:
        healths = [a.health for a in self.agents]
        if all(h == AgentHealth.OFFLINE for h in healths):
            return AgentHealth.OFFLINE
        if any(h == AgentHealth.CRITICAL for h in healths):
            return AgentHealth.CRITICAL
        if any(h == AgentHealth.DEGRADED for h in healths):
            return AgentHealth.DEGRADED
        return AgentHealth.HEALTHY

    def to_dict(self) -> dict:
        return {
            "division": self.division,
            "name": self.name,
            "healthy_agents": self.healthy_count,
            "total_agents": len(self.agents),
            "total_tasks": self.total_tasks,
            "total_errors": self.total_errors,
            "division_error_rate": round(self.division_error_rate, 4),
            "avg_response_time_ms": round(self.avg_response_time_ms, 1),
            "health": self.health.value,
            "agents": [a.to_dict() for a in self.agents],
        }


@dataclass
class Alert:
    agent_id: str
    division: int
    level: str   # "warning" | "critical"
    message: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "division": self.division,
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp,
        }


# ── Monitor ───────────────────────────────────────────────────────────────────

_DIVISION_NAMES = {
    1: "Détection & Scouting",
    2: "Rédaction & Outreach",
    3: "Relation & Négociation",
    4: "Production & Design",
    5: "Finance & Paiement",
    6: "Personal Branding",
}


class PerformanceMonitor:
    """
    Central performance monitor for all 60 swarm agents.
    Records task events and computes health metrics.
    """

    def __init__(self):
        self._agents: Dict[str, AgentStats] = {}
        self._alerts: List[Alert] = []
        self._initialized = False

    def initialize_agents(self, agent_ids: Optional[List[str]] = None) -> None:
        """Pre-register all 60 agents. If no list given, auto-generates 6×10."""
        if agent_ids is None:
            agent_ids = [
                f"{div}.{i}" if i > 0 else f"{div}.0"
                for div in range(1, 7)
                for i in range(10)
            ]
        for aid in agent_ids:
            div = int(aid.split(".")[0])
            self._agents[aid] = AgentStats(agent_id=aid, division=div)
        self._initialized = True

    def record_task(
        self,
        agent_id: str,
        success: bool,
        response_time_ms: float = 0.0,
        error_msg: Optional[str] = None,
    ) -> None:
        """Record a completed (or failed) task for an agent."""
        if agent_id not in self._agents:
            div = int(agent_id.split(".")[0]) if "." in agent_id else 0
            self._agents[agent_id] = AgentStats(agent_id=agent_id, division=div)

        stats = self._agents[agent_id]
        stats.last_heartbeat = time.time()

        if success:
            stats.tasks_completed += 1
            stats.total_response_time_ms += response_time_ms
        else:
            stats.tasks_failed += 1
            stats.last_error = error_msg

        self._check_and_alert(stats)

    def heartbeat(self, agent_id: str) -> None:
        """Update last seen timestamp for an agent."""
        if agent_id not in self._agents:
            return
        self._agents[agent_id].last_heartbeat = time.time()

    def set_queued(self, agent_id: str, count: int) -> None:
        if agent_id in self._agents:
            self._agents[agent_id].tasks_queued = count

    # ── Queries ────────────────────────────────────────────────────────────────

    def get_agent(self, agent_id: str) -> Optional[AgentStats]:
        return self._agents.get(agent_id)

    def get_division(self, division: int) -> DivisionStats:
        name = _DIVISION_NAMES.get(division, f"Division {division}")
        agents = [a for a in self._agents.values() if a.division == division]
        return DivisionStats(division=division, name=name, agents=agents)

    def get_all_divisions(self) -> List[DivisionStats]:
        divisions = sorted(_DIVISION_NAMES.keys())
        return [self.get_division(d) for d in divisions]

    def critical_agents(self) -> List[AgentStats]:
        return [a for a in self._agents.values() if a.health == AgentHealth.CRITICAL]

    def offline_agents(self) -> List[AgentStats]:
        return [a for a in self._agents.values() if a.health == AgentHealth.OFFLINE]

    def healthy_agent_count(self) -> int:
        return sum(1 for a in self._agents.values() if a.health == AgentHealth.HEALTHY)

    def get_alerts(self, level: Optional[str] = None) -> List[Alert]:
        if level:
            return [a for a in self._alerts if a.level == level]
        return list(self._alerts)

    def global_summary(self) -> dict:
        total = len(self._agents)
        healthy = self.healthy_agent_count()
        all_tasks = sum(a.tasks_completed for a in self._agents.values())
        all_errors = sum(a.tasks_failed for a in self._agents.values())
        return {
            "total_agents": total,
            "healthy_agents": healthy,
            "degraded_agents": sum(1 for a in self._agents.values() if a.health == AgentHealth.DEGRADED),
            "critical_agents": sum(1 for a in self._agents.values() if a.health == AgentHealth.CRITICAL),
            "offline_agents": sum(1 for a in self._agents.values() if a.health == AgentHealth.OFFLINE),
            "total_tasks_completed": all_tasks,
            "total_tasks_failed": all_errors,
            "global_error_rate": round(all_errors / (all_tasks + all_errors), 4) if (all_tasks + all_errors) else 0.0,
            "open_alerts": len(self._alerts),
        }

    def reset(self) -> None:
        self._agents.clear()
        self._alerts.clear()
        self._initialized = False

    # ── Internal ──────────────────────────────────────────────────────────────

    def _check_and_alert(self, stats: AgentStats) -> None:
        health = stats.health
        if health == AgentHealth.CRITICAL:
            self._alerts.append(Alert(
                agent_id=stats.agent_id,
                division=stats.division,
                level="critical",
                message=f"Agent {stats.agent_id} error rate {stats.error_rate:.0%} — intervention requise",
            ))
        elif health == AgentHealth.DEGRADED:
            self._alerts.append(Alert(
                agent_id=stats.agent_id,
                division=stats.division,
                level="warning",
                message=f"Agent {stats.agent_id} dégradé — error rate {stats.error_rate:.0%}",
            ))
