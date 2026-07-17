"""
Caelum Partners — Configuration Hybride Local/Cloud
Agents de base → Ollama local (gratuit)
Agents Directeurs → API Cloud (Claude/Mistral Large)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class AgentTier(Enum):
    LOCAL = "local"       # Ollama — gratuit, vitesse raisonnable
    CLOUD = "cloud"       # API payante — uniquement arbitrages critiques


class AgentRole(Enum):
    SURVEILLANCE = "surveillance"
    WELLBEING = "wellbeing"
    DAILY_TASK = "daily_task"
    ANALYTICS = "analytics"
    DIRECTOR = "director"       # Tier CLOUD uniquement
    ARBITRATOR = "arbitrator"   # Tier CLOUD uniquement


@dataclass
class AgentProfile:
    agent_id: str
    name: str
    role: AgentRole
    tier: AgentTier
    model: str
    endpoint: str
    max_turns: int = 10             # Kill switch — stoppe les boucles infinies
    max_tokens_per_turn: int = 512
    sleep_enabled: bool = True
    description: str = ""

    @property
    def is_local(self) -> bool:
        return self.tier == AgentTier.LOCAL

    @property
    def is_cloud(self) -> bool:
        return self.tier == AgentTier.CLOUD


# ── Endpoints ─────────────────────────────────────────────────────────────────

OLLAMA_ENDPOINT = "http://localhost:11434"
OLLAMA_MODEL_DEFAULT = "mistral:7b"        # gratuit, ~4GB VRAM
OLLAMA_MODEL_FAST = "mistral-nemo"         # plus rapide, ~2GB VRAM

CLOUD_ENDPOINT_ANTHROPIC = "https://api.anthropic.com"
CLOUD_MODEL_CLAUDE = "claude-sonnet-4-6"

# ── Catalogue des agents ───────────────────────────────────────────────────────

AGENT_REGISTRY: Dict[str, AgentProfile] = {
    # ── AGENTS LOCAUX (gratuits) ────────────────────────────────────────────
    "surv-01": AgentProfile(
        agent_id="surv-01", name="Sentinel Surveillance Alpha",
        role=AgentRole.SURVEILLANCE, tier=AgentTier.LOCAL,
        model=OLLAMA_MODEL_FAST, endpoint=OLLAMA_ENDPOINT,
        max_turns=10, description="Surveillance continue des KPIs — alerte seuils"
    ),
    "surv-02": AgentProfile(
        agent_id="surv-02", name="Sentinel Surveillance Beta",
        role=AgentRole.SURVEILLANCE, tier=AgentTier.LOCAL,
        model=OLLAMA_MODEL_FAST, endpoint=OLLAMA_ENDPOINT,
        max_turns=10, description="Surveillance concurrents et marchés"
    ),
    "well-01": AgentProfile(
        agent_id="well-01", name="Bien-Être Équipe Alpha",
        role=AgentRole.WELLBEING, tier=AgentTier.LOCAL,
        model=OLLAMA_MODEL_DEFAULT, endpoint=OLLAMA_ENDPOINT,
        max_turns=10, description="Monitoring charge de travail équipe"
    ),
    "well-02": AgentProfile(
        agent_id="well-02", name="Bien-Être Performance Beta",
        role=AgentRole.WELLBEING, tier=AgentTier.LOCAL,
        model=OLLAMA_MODEL_DEFAULT, endpoint=OLLAMA_ENDPOINT,
        max_turns=10, description="Suivi satisfaction et engagement"
    ),
    "task-01": AgentProfile(
        agent_id="task-01", name="Planificateur Quotidien Alpha",
        role=AgentRole.DAILY_TASK, tier=AgentTier.LOCAL,
        model=OLLAMA_MODEL_FAST, endpoint=OLLAMA_ENDPOINT,
        max_turns=10, description="Orchestration tâches journalières automatiques"
    ),
    "task-02": AgentProfile(
        agent_id="task-02", name="Rapport Journalier Beta",
        role=AgentRole.DAILY_TASK, tier=AgentTier.LOCAL,
        model=OLLAMA_MODEL_FAST, endpoint=OLLAMA_ENDPOINT,
        max_turns=10, description="Génération rapports quotidiens"
    ),
    "anal-01": AgentProfile(
        agent_id="anal-01", name="Analytique Locale Gamma",
        role=AgentRole.ANALYTICS, tier=AgentTier.LOCAL,
        model=OLLAMA_MODEL_DEFAULT, endpoint=OLLAMA_ENDPOINT,
        max_turns=10, description="Analyse données CRM locale"
    ),

    # ── AGENTS DIRECTEURS (Cloud — usage restreint) ─────────────────────────
    "dir-01": AgentProfile(
        agent_id="dir-01", name="Directeur Stratégique Principal",
        role=AgentRole.DIRECTOR, tier=AgentTier.CLOUD,
        model=CLOUD_MODEL_CLAUDE, endpoint=CLOUD_ENDPOINT_ANTHROPIC,
        max_turns=5, max_tokens_per_turn=2048,
        description="Arbitrages stratégiques critiques uniquement"
    ),
    "dir-02": AgentProfile(
        agent_id="dir-02", name="Arbitreur Crises & Bugs Critiques",
        role=AgentRole.ARBITRATOR, tier=AgentTier.CLOUD,
        model=CLOUD_MODEL_CLAUDE, endpoint=CLOUD_ENDPOINT_ANTHROPIC,
        max_turns=5, max_tokens_per_turn=2048,
        description="Résolution bugs bloquants et crises système"
    ),
}


def get_local_agents() -> List[AgentProfile]:
    return [a for a in AGENT_REGISTRY.values() if a.is_local]


def get_cloud_agents() -> List[AgentProfile]:
    return [a for a in AGENT_REGISTRY.values() if a.is_cloud]


def get_agent(agent_id: str) -> AgentProfile:
    if agent_id not in AGENT_REGISTRY:
        raise KeyError(f"Agent inconnu: {agent_id}")
    return AGENT_REGISTRY[agent_id]
