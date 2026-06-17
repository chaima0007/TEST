"""
Base agent wrapper around CrewAI Agent.
All 50 swarm agents inherit from this class.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from crewai import Agent as CrewAgent
from crewai.tools import BaseTool

from config import AgentConfig, ANTHROPIC_MODEL

logger = logging.getLogger("SwarmAgent")


class SwarmAgent:
    """Thin wrapper that pairs an AgentConfig with an instantiated CrewAI Agent."""

    def __init__(self, config: AgentConfig, tools: Optional[List[BaseTool]] = None):
        self.config = config
        self._tools = tools or []
        self._crew_agent: Optional[CrewAgent] = None

    def build(self) -> CrewAgent:
        """Lazily instantiate the CrewAI agent (deferred until first use)."""
        if self._crew_agent is None:
            self._crew_agent = CrewAgent(
                role=self.config.role,
                goal=self.config.goal,
                backstory=self.config.backstory,
                tools=self._tools,
                llm=f"anthropic/{ANTHROPIC_MODEL}",
                verbose=False,
                allow_delegation=self.config.is_manager,
                max_iter=5,
                memory=True,
            )
            logger.debug(f"[Agent {self.config.id}] Built — {self.config.role}")
        return self._crew_agent

    @property
    def id(self) -> str:
        return self.config.id

    @property
    def division(self) -> int:
        return self.config.division

    @property
    def is_manager(self) -> bool:
        return self.config.is_manager

    def __repr__(self) -> str:
        return f"<SwarmAgent {self.id} | {self.config.role}>"
