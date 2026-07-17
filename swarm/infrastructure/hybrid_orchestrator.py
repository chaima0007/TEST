"""
Caelum Partners — Orchestrateur Hybride Local/Cloud
Coordonne la flotte d'agents locaux + directeurs cloud.
Décide automatiquement quand escalader vers le cloud.
"""
from __future__ import annotations
import logging
import time
from typing import Any, Dict, List, Optional

from .agent_config import (
    AGENT_REGISTRY,
    AgentRole,
    AgentTier,
    get_cloud_agents,
    get_local_agents,
)
from .agent_state import AgentState
from .circuit_breaker import GLOBAL_CIRCUIT_REGISTRY
from .director_agent import DirectorAgent
from .local_agent import LocalAgent
from .token_tracker import GLOBAL_TOKEN_TRACKER

logger = logging.getLogger("caelum.orchestrator")

# Seuil de coût cloud au-delà duquel on bloque les nouvelles requêtes director
CLOUD_COST_HARD_LIMIT_USD = 5.0

# Criticité minimale pour escalader vers le directeur cloud
ESCALATION_KEYWORDS = [
    "critique", "urgent", "bloquant", "crise",
    "panne", "faille", "sécurité", "fraude",
]


class HybridOrchestrator:
    """
    Cerveau central de la flotte hybride.
    - Lance et surveille tous les agents locaux
    - Escalade vers un Director cloud si criticité élevée
    - Stoppe automatiquement les agents dont le circuit est déclenché
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self._local_agents: Dict[str, LocalAgent] = {}
        self._directors: Dict[str, DirectorAgent] = {}
        self._api_key = api_key
        self._started_at = time.time()
        self._init_agents()

    def _init_agents(self) -> None:
        for profile in get_local_agents():
            self._local_agents[profile.agent_id] = LocalAgent(profile)
            logger.info("Agent local initialisé: %s", profile.agent_id)

        for profile in get_cloud_agents():
            self._directors[profile.agent_id] = DirectorAgent(profile, api_key=self._api_key)
            logger.info("Director cloud initialisé: %s", profile.agent_id)

    # ── API publique ──────────────────────────────────────────────────────────

    def run_local(self, agent_id: str, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Exécute un agent local."""
        agent = self._local_agents.get(agent_id)
        if not agent:
            return {"error": f"Agent local inconnu: {agent_id}"}
        return agent.generate(prompt, system=system)

    def escalate_to_director(
        self,
        situation: str,
        options: List[str],
        preferred_director: str = "dir-01",
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Escalade une situation critique au Director cloud.
        Vérifie le budget avant d'appeler.
        """
        cost = GLOBAL_TOKEN_TRACKER.total_cost_usd()
        if cost >= CLOUD_COST_HARD_LIMIT_USD:
            return {
                "decision": "BUDGET_EXCEEDED",
                "rationale": f"Coût cloud {cost:.4f}$ ≥ limite {CLOUD_COST_HARD_LIMIT_USD}$",
                "tokens_used": 0,
                "error": "Hard limit atteinte — pas d'appel cloud",
            }

        director = self._directors.get(preferred_director)
        if not director:
            # Fallback sur le premier director disponible
            alive = [d for d in self._directors.values() if d.is_alive()]
            if not alive:
                return {"decision": "NO_DIRECTOR", "error": "Aucun Director disponible"}
            director = alive[0]

        if not director.is_alive():
            return {"decision": "DIRECTOR_CIRCUIT_OPEN", "error": "Director circuit déclenché"}

        return director.arbitrate(situation, options, context=context)

    def auto_dispatch(
        self, agent_id: str, prompt: str, system: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatch automatique : local par défaut,
        escalade cloud si mots-clés critiques détectés.
        """
        is_critical = any(kw in prompt.lower() for kw in ESCALATION_KEYWORDS)

        if is_critical:
            logger.warning("[ESCALADE] Situation critique détectée — Director cloud")
            return self.escalate_to_director(
                situation=prompt,
                options=["Résolution immédiate", "Analyse approfondie", "Alerte équipe"],
                context=system,
            )

        return self.run_local(agent_id, prompt, system=system)

    def sleep_all(self) -> List[str]:
        """Endort tous les agents locaux — sauvegarde les états."""
        slept = []
        for agent_id, agent in self._local_agents.items():
            agent.sleep()
            slept.append(agent_id)
        logger.info("Flotte locale endormie: %d agents", len(slept))
        return slept

    def wake_all(self) -> Dict[str, str]:
        """Réveille tous les agents locaux — retourne leurs contextes compacts."""
        contexts = {}
        for agent_id, agent in self._local_agents.items():
            contexts[agent_id] = agent.wake()
        logger.info("Flotte locale réveillée: %d agents", len(contexts))
        return contexts

    def fleet_status(self) -> Dict[str, Any]:
        """Statut complet de toute la flotte."""
        local_statuses = [a.status() for a in self._local_agents.values()]
        director_statuses = [d.status() for d in self._directors.values()]
        token_summary = GLOBAL_TOKEN_TRACKER.summary()
        tripped = GLOBAL_CIRCUIT_REGISTRY.tripped_agents()

        alive_local = sum(1 for s in local_statuses if s["is_alive"])
        alive_directors = sum(1 for s in director_statuses if s["is_alive"])

        return {
            "orchestrator": {
                "uptime_s": round(time.time() - self._started_at, 1),
                "total_agents": len(self._local_agents) + len(self._directors),
                "local_agents": len(self._local_agents),
                "cloud_directors": len(self._directors),
                "alive_local": alive_local,
                "alive_directors": alive_directors,
                "tripped_circuits": len(tripped),
                "tripped_agent_ids": tripped,
            },
            "token_usage": {
                "local_tokens": token_summary["total_local_tokens"],
                "cloud_tokens": token_summary["total_cloud_tokens"],
                "total_cost_usd": token_summary["total_cost_usd"],
                "cloud_budget_limit": token_summary["budget_cloud_limit"],
                "alerts": token_summary["alerts"],
            },
            "local_agents": local_statuses,
            "directors": director_statuses,
        }

    def get_recommendations(self) -> List[str]:
        """Génère des recommandations basées sur l'état de la flotte."""
        recs = []
        status = self.fleet_status()
        tripped = status["orchestrator"]["tripped_circuits"]
        cost = status["token_usage"]["total_cost_usd"]
        cloud_tokens = status["token_usage"]["cloud_tokens"]

        if tripped > 0:
            recs.append(f"{tripped} circuit(s) déclenchés — vérifiez les agents bloqués")
        if cost > CLOUD_COST_HARD_LIMIT_USD * 0.8:
            recs.append(f"Coût cloud {cost:.4f}$ proche de la limite — réduire les escalades")
        if cloud_tokens > 50_000:
            recs.append("Volume cloud élevé — basculer davantage de tâches vers Ollama local")
        if not recs:
            recs.append("Flotte opérationnelle — aucune action requise")
        return recs


# Singleton lazy
_ORCHESTRATOR: Optional[HybridOrchestrator] = None


def get_orchestrator(api_key: Optional[str] = None) -> HybridOrchestrator:
    global _ORCHESTRATOR
    if _ORCHESTRATOR is None:
        _ORCHESTRATOR = HybridOrchestrator(api_key=api_key)
    return _ORCHESTRATOR
