"""
Caelum Partners — Wrapper Agent Local (Ollama)
Client HTTP léger vers http://localhost:11434
Agents de base : surveillance, wellbeing, daily_task, analytics
"""
from __future__ import annotations
import json
import logging
import time
import urllib.request
import urllib.error
from typing import Any, Dict, Iterator, Optional

from .agent_config import AgentProfile, AgentTier
from .agent_state import AgentState
from .circuit_breaker import GLOBAL_CIRCUIT_REGISTRY, CircuitCheckResult
from .token_tracker import GLOBAL_TOKEN_TRACKER

logger = logging.getLogger("caelum.local_agent")

OLLAMA_GENERATE_PATH = "/api/generate"
OLLAMA_CHAT_PATH = "/api/chat"
DEFAULT_TIMEOUT = 60


class OllamaConnectionError(RuntimeError):
    pass


class LocalAgent:
    """
    Agent Ollama local.
    - Gratuit (zéro coût API cloud)
    - Kill switch via CircuitBreaker (max_turns=10)
    - État persisté via AgentState (sleep/wake sans historique LLM)
    """

    def __init__(self, profile: AgentProfile) -> None:
        if profile.tier != AgentTier.LOCAL:
            raise ValueError(f"LocalAgent ne supporte que LOCAL, reçu: {profile.tier}")
        self.profile = profile
        self.state = AgentState.load_or_create(
            agent_id=profile.agent_id,
            name=profile.name,
            role=profile.role.value,
            tier=profile.tier.value,
            model=profile.model,
        )
        # Enregistrement circuit et tracker
        GLOBAL_CIRCUIT_REGISTRY.get_or_create(
            profile.agent_id, max_turns=profile.max_turns
        )
        GLOBAL_TOKEN_TRACKER.register(
            profile.agent_id, tier="local", model=profile.model
        )

    @property
    def agent_id(self) -> str:
        return self.profile.agent_id

    def is_alive(self) -> bool:
        circuit = GLOBAL_CIRCUIT_REGISTRY.get_or_create(self.agent_id)
        return circuit.is_alive

    def ping(self) -> bool:
        """Vérifie que le serveur Ollama est accessible."""
        try:
            url = f"{self.profile.endpoint}/api/tags"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5):
                return True
        except Exception:
            return False

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """
        Appel /api/generate Ollama.
        Retourne {"response": str, "tokens": int, "circuit": dict}
        """
        circuit = GLOBAL_CIRCUIT_REGISTRY.get_or_create(self.agent_id)

        # Vérif circuit avant exécution
        if not circuit.is_alive:
            return {
                "response": "",
                "tokens": 0,
                "circuit": circuit.to_dict(),
                "error": f"CIRCUIT_OPEN: {circuit.trip_reason}",
            }

        payload: Dict[str, Any] = {
            "model": self.profile.model,
            "prompt": self._build_prompt(prompt, system),
            "stream": False,
            "options": {"num_predict": self.profile.max_tokens_per_turn},
        }

        try:
            response_text, eval_count = self._http_post(
                OLLAMA_GENERATE_PATH, payload
            )
        except OllamaConnectionError as exc:
            logger.error("[%s] Ollama inaccessible: %s", self.agent_id, exc)
            return {
                "response": "",
                "tokens": 0,
                "circuit": circuit.to_dict(),
                "error": str(exc),
            }

        # Enregistrement circuit (loop detection + turn count)
        check = GLOBAL_CIRCUIT_REGISTRY.check(
            self.agent_id, response_text, token_count=eval_count
        )
        GLOBAL_TOKEN_TRACKER.record(
            self.agent_id,
            input_tokens=len(prompt.split()),
            output_tokens=eval_count,
            turn_index=self.state.turn_count,
        )
        self.state.turn_count += 1
        self.state.remember("result", response_text[:150])

        return {
            "response": response_text,
            "tokens": eval_count,
            "circuit": circuit.to_dict(),
            "allowed": check.allowed,
        }

    def sleep(self) -> None:
        """Endort l'agent — sauvegarde l'état sur disque."""
        self.state.sleep()
        self.state.save()
        logger.info("[%s] Endormi — état sauvegardé", self.agent_id)

    def wake(self) -> str:
        """Réveille l'agent — retourne contexte compact (< 500 tokens)."""
        ctx = self.state.wake()
        logger.info("[%s] Réveillé", self.agent_id)
        return ctx

    def status(self) -> dict:
        circuit = GLOBAL_CIRCUIT_REGISTRY.get_or_create(self.agent_id)
        return {
            "agent_id": self.agent_id,
            "name": self.profile.name,
            "tier": "local",
            "model": self.profile.model,
            "turn_count": self.state.turn_count,
            "max_turns": self.profile.max_turns,
            "is_sleeping": self.state.is_sleeping,
            "circuit_state": circuit.state.value,
            "is_alive": circuit.is_alive,
            "estimated_cost_usd": 0.0,
        }

    # ── Privé ─────────────────────────────────────────────────────────────────

    def _build_prompt(self, user_prompt: str, system: Optional[str]) -> str:
        parts = []
        if system:
            parts.append(f"[SYSTÈME] {system}")
        compact_ctx = self.state.get_compact_context()
        if compact_ctx:
            parts.append(f"[CONTEXTE]\n{compact_ctx}")
        parts.append(f"[UTILISATEUR] {user_prompt}")
        return "\n\n".join(parts)

    def _http_post(
        self, path: str, payload: Dict[str, Any]
    ) -> tuple[str, int]:
        url = f"{self.profile.endpoint}{path}"
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
                raw = json.loads(resp.read().decode())
                text = raw.get("response", "")
                tokens = raw.get("eval_count", len(text.split()))
                return text, tokens
        except urllib.error.URLError as exc:
            raise OllamaConnectionError(f"Ollama inaccessible ({url}): {exc}") from exc
