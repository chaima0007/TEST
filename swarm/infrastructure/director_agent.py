"""
Caelum Partners — Agent Directeur (Cloud API)
Usage RESTREINT : arbitrages stratégiques critiques uniquement.
Chaque token coûte — utiliser avec parcimonie.
"""
from __future__ import annotations
import json
import logging
import os
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

from .agent_config import AgentProfile, AgentTier
from .agent_state import AgentState
from .circuit_breaker import GLOBAL_CIRCUIT_REGISTRY
from .token_tracker import GLOBAL_TOKEN_TRACKER

logger = logging.getLogger("caelum.director_agent")

ANTHROPIC_MESSAGES_PATH = "/v1/messages"
DEFAULT_TIMEOUT = 120


class CloudAPIError(RuntimeError):
    pass


class DirectorAgent:
    """
    Agent Directeur — Claude via API Anthropic.
    COÛTE DE L'ARGENT : appeler uniquement pour arbitrages critiques.
    - max_turns=5 (plus strict que agents locaux)
    - Contexte compact uniquement (pas d'historique complet)
    - Circuit breaker actif
    """

    def __init__(self, profile: AgentProfile, api_key: Optional[str] = None) -> None:
        if profile.tier != AgentTier.CLOUD:
            raise ValueError(f"DirectorAgent ne supporte que CLOUD, reçu: {profile.tier}")
        self.profile = profile
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.state = AgentState.load_or_create(
            agent_id=profile.agent_id,
            name=profile.name,
            role=profile.role.value,
            tier=profile.tier.value,
            model=profile.model,
        )
        GLOBAL_CIRCUIT_REGISTRY.get_or_create(
            profile.agent_id, max_turns=profile.max_turns
        )
        GLOBAL_TOKEN_TRACKER.register(
            profile.agent_id, tier="cloud", model=profile.model
        )

    @property
    def agent_id(self) -> str:
        return self.profile.agent_id

    def is_alive(self) -> bool:
        circuit = GLOBAL_CIRCUIT_REGISTRY.get_or_create(self.agent_id)
        return circuit.is_alive

    def arbitrate(
        self,
        situation: str,
        options: List[str],
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Demande un arbitrage stratégique au Directeur.
        Retourne {"decision": str, "rationale": str, "tokens_used": int}
        """
        circuit = GLOBAL_CIRCUIT_REGISTRY.get_or_create(self.agent_id)
        if not circuit.is_alive:
            return {
                "decision": "CIRCUIT_OPEN",
                "rationale": circuit.trip_reason,
                "tokens_used": 0,
                "error": "Director circuit breaker déclenché",
            }

        if not self.api_key:
            return {
                "decision": "NO_API_KEY",
                "rationale": "ANTHROPIC_API_KEY manquante",
                "tokens_used": 0,
                "error": "Clé API absente",
            }

        system_prompt = self._build_system()
        user_message = self._build_arbitration_prompt(situation, options, context)

        try:
            result = self._call_anthropic(system_prompt, user_message)
        except CloudAPIError as exc:
            logger.error("[%s] Erreur API: %s", self.agent_id, exc)
            return {
                "decision": "API_ERROR",
                "rationale": str(exc),
                "tokens_used": 0,
                "error": str(exc),
            }

        input_tokens = result.get("input_tokens", 0)
        output_tokens = result.get("output_tokens", 0)
        response_text = result.get("content", "")

        # Circuit breaker check
        GLOBAL_CIRCUIT_REGISTRY.check(
            self.agent_id, response_text, token_count=input_tokens + output_tokens
        )
        GLOBAL_TOKEN_TRACKER.record(
            self.agent_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            turn_index=self.state.turn_count,
        )
        self.state.turn_count += 1
        self.state.remember("decision", response_text[:150])
        self.state.save()

        return {
            "decision": response_text,
            "rationale": f"Arbitrage par {self.profile.name}",
            "tokens_used": input_tokens + output_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": round((input_tokens + output_tokens) / 1_000_000 * 3.0, 6),
        }

    def status(self) -> dict:
        circuit = GLOBAL_CIRCUIT_REGISTRY.get_or_create(self.agent_id)
        tracker_data = GLOBAL_TOKEN_TRACKER._agents.get(self.agent_id)
        total_tokens = tracker_data.total_tokens if tracker_data else 0
        cost = round(total_tokens / 1_000_000 * 3.0, 6)
        return {
            "agent_id": self.agent_id,
            "name": self.profile.name,
            "tier": "cloud",
            "model": self.profile.model,
            "turn_count": self.state.turn_count,
            "max_turns": self.profile.max_turns,
            "is_sleeping": self.state.is_sleeping,
            "circuit_state": circuit.state.value,
            "is_alive": circuit.is_alive,
            "total_tokens": total_tokens,
            "estimated_cost_usd": cost,
        }

    # ── Privé ─────────────────────────────────────────────────────────────────

    def _build_system(self) -> str:
        return (
            f"Tu es {self.profile.name}, Agent Directeur Stratégique de Caelum Partners. "
            "Tu n'interviens QUE pour des arbitrages critiques. "
            "Chaque token que tu génères a un coût réel — sois concis et décisif. "
            "Réponds TOUJOURS en JSON avec les clés: decision, rationale, confidence (0-100), next_action."
        )

    def _build_arbitration_prompt(
        self, situation: str, options: List[str], context: Optional[str]
    ) -> str:
        compact_ctx = self.state.get_compact_context()
        parts = [f"SITUATION CRITIQUE: {situation}"]
        if context:
            parts.append(f"CONTEXTE: {context}")
        if compact_ctx:
            parts.append(f"HISTORIQUE COMPACT: {compact_ctx}")
        parts.append("OPTIONS:")
        for i, opt in enumerate(options, 1):
            parts.append(f"  {i}. {opt}")
        parts.append("Rends ton arbitrage en JSON.")
        return "\n".join(parts)

    def _call_anthropic(self, system: str, user: str) -> Dict[str, Any]:
        payload = {
            "model": self.profile.model,
            "max_tokens": self.profile.max_tokens_per_turn,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        body = json.dumps(payload).encode()
        url = f"{self.profile.endpoint}{ANTHROPIC_MESSAGES_PATH}"
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
                raw = json.loads(resp.read().decode())
                content = raw.get("content", [{}])[0].get("text", "")
                usage = raw.get("usage", {})
                return {
                    "content": content,
                    "input_tokens": usage.get("input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                }
        except urllib.error.HTTPError as exc:
            body_err = exc.read().decode()
            raise CloudAPIError(f"HTTP {exc.code}: {body_err}") from exc
        except urllib.error.URLError as exc:
            raise CloudAPIError(f"Connexion échouée: {exc}") from exc
