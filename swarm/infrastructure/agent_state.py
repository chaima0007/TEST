"""
Caelum Partners — Sérialisation d'état Agent (Sleep/Wake)
Sauvegarde/restaure l'état minimal d'un agent sans brûler de tokens LLM.
PAS d'historique complet en mémoire LLM — uniquement résumé compact.
"""
from __future__ import annotations
import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

STATE_DIR = Path("swarm/state")


@dataclass
class AgentMemoryItem:
    """Un souvenir compact (pas un message complet)."""
    timestamp: float
    category: str        # "observation" | "decision" | "alert" | "result"
    summary: str         # 1 phrase max — jamais l'output brut du LLM
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentState:
    """État persisté d'un agent entre deux sessions."""
    agent_id: str
    name: str
    role: str
    tier: str
    model: str
    turn_count: int = 0
    is_sleeping: bool = False
    last_active: float = field(default_factory=time.time)
    memory: List[AgentMemoryItem] = field(default_factory=list)
    context_summary: str = ""   # Résumé compact du contexte courant
    pending_tasks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # ── Opérations mémoire ────────────────────────────────────────────────────

    def remember(self, category: str, summary: str, **meta: Any) -> None:
        """Ajoute un souvenir compact — jamais d'output LLM brut."""
        self.memory.append(AgentMemoryItem(
            timestamp=time.time(),
            category=category,
            summary=summary[:200],  # tronqué à 200 chars pour économie tokens
            metadata=meta,
        ))
        # Garde uniquement les 50 derniers souvenirs
        if len(self.memory) > 50:
            self.memory = self.memory[-50:]

    def get_compact_context(self) -> str:
        """Génère un contexte compact (< 500 tokens) pour le prochain wake."""
        lines = [f"Agent: {self.name} ({self.role})"]
        if self.context_summary:
            lines.append(f"Contexte: {self.context_summary}")
        if self.pending_tasks:
            lines.append("Tâches en attente: " + "; ".join(self.pending_tasks[:5]))
        recent = self.memory[-10:]
        if recent:
            lines.append("Souvenirs récents:")
            for m in recent:
                lines.append(f"  [{m.category}] {m.summary}")
        return "\n".join(lines)

    # ── Sleep / Wake ─────────────────────────────────────────────────────────

    def sleep(self) -> None:
        self.is_sleeping = True
        self.last_active = time.time()

    def wake(self) -> str:
        """Réveille l'agent et retourne son contexte compact."""
        self.is_sleeping = False
        self.last_active = time.time()
        return self.get_compact_context()

    # ── Persistance JSON ──────────────────────────────────────────────────────

    def save(self) -> Path:
        path = STATE_DIR / f"{self.agent_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "tier": self.tier,
            "model": self.model,
            "turn_count": self.turn_count,
            "is_sleeping": self.is_sleeping,
            "last_active": self.last_active,
            "context_summary": self.context_summary,
            "pending_tasks": self.pending_tasks,
            "metadata": self.metadata,
            "memory": [
                {
                    "timestamp": m.timestamp,
                    "category": m.category,
                    "summary": m.summary,
                    "metadata": m.metadata,
                }
                for m in self.memory
            ],
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return path

    @classmethod
    def load(cls, agent_id: str) -> Optional["AgentState"]:
        path = STATE_DIR / f"{agent_id}.json"
        if not path.exists():
            return None
        raw = json.loads(path.read_text())
        state = cls(
            agent_id=raw["agent_id"],
            name=raw["name"],
            role=raw["role"],
            tier=raw["tier"],
            model=raw["model"],
            turn_count=raw.get("turn_count", 0),
            is_sleeping=raw.get("is_sleeping", False),
            last_active=raw.get("last_active", time.time()),
            context_summary=raw.get("context_summary", ""),
            pending_tasks=raw.get("pending_tasks", []),
            metadata=raw.get("metadata", {}),
        )
        for m in raw.get("memory", []):
            state.memory.append(AgentMemoryItem(
                timestamp=m["timestamp"],
                category=m["category"],
                summary=m["summary"],
                metadata=m.get("metadata", {}),
            ))
        return state

    @classmethod
    def load_or_create(cls, agent_id: str, **kwargs: Any) -> "AgentState":
        existing = cls.load(agent_id)
        if existing:
            return existing
        return cls(agent_id=agent_id, **kwargs)

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "tier": self.tier,
            "model": self.model,
            "turn_count": self.turn_count,
            "is_sleeping": self.is_sleeping,
            "last_active": self.last_active,
            "memory_count": len(self.memory),
            "pending_tasks": self.pending_tasks,
            "context_summary": self.context_summary,
        }
