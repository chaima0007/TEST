"""
A/B Tester for outreach email variants.

Tracks which copywriting tone (agent) gets the best reply rates,
and progressively routes more prospects to the winning variant
using Thompson Sampling (Bayesian A/B testing).

Usage:
    from intelligence.ab_tester import ABTester
    tester = ABTester()
    agent_id = tester.select_agent()
    # ... send email with agent_id ...
    tester.record_result(agent_id, opened=True, replied=True)
    report = tester.get_report()
"""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger("swarm.ab_tester")


@dataclass
class AgentVariant:
    agent_id: str
    tone_name: str
    sent: int = 0
    opened: int = 0
    replied: int = 0
    paid: int = 0
    # Beta distribution params for Thompson sampling
    alpha: float = 1.0  # successes + 1
    beta: float = 1.0   # failures + 1

    @property
    def open_rate(self) -> float:
        return self.opened / self.sent if self.sent > 0 else 0.0

    @property
    def reply_rate(self) -> float:
        return self.replied / self.sent if self.sent > 0 else 0.0

    @property
    def conversion_rate(self) -> float:
        return self.paid / self.sent if self.sent > 0 else 0.0

    def sample(self) -> float:
        """Draw from the Beta posterior (Thompson sampling)."""
        return random.betavariate(self.alpha, self.beta)

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "tone_name": self.tone_name,
            "sent": self.sent,
            "opened": self.opened,
            "replied": self.replied,
            "paid": self.paid,
            "open_rate": round(self.open_rate * 100, 1),
            "reply_rate": round(self.reply_rate * 100, 1),
            "conversion_rate": round(self.conversion_rate * 100, 1),
        }


# ── Default variants matching Division 2 agents ───────────────────────────────

DEFAULT_VARIANTS = [
    AgentVariant("2.1", "Le Factuel"),
    AgentVariant("2.2", "L'Amical"),
    AgentVariant("2.3", "Le Client Perdu"),
    AgentVariant("2.4", "Région Nord"),
    AgentVariant("2.5", "Région Sud"),
    AgentVariant("2.6", "Paris & IDF"),
    AgentVariant("2.7", "Secteur Premium"),
    AgentVariant("2.8", "Artisans & TPE"),
    AgentVariant("2.9", "Relance & Suivi"),
]


class ABTester:
    def __init__(self, variants: Optional[List[AgentVariant]] = None):
        self.variants: Dict[str, AgentVariant] = {
            v.agent_id: v for v in (variants or DEFAULT_VARIANTS)
        }
        self._started_at = datetime.now().isoformat()
        logger.info("ABTester initialised — %d variants", len(self.variants))

    def select_agent(self, sector: Optional[str] = None) -> str:
        """
        Select an agent using Thompson Sampling.
        If sector is provided, biases toward regional/sector-specific agents.
        """
        # Sector-specific bias
        if sector:
            s = sector.lower()
            if "paris" in s or "île-de-france" in s or "idf" in s:
                if "2.6" in self.variants and self.variants["2.6"].sent < 5:
                    return "2.6"
            elif any(w in s for w in ["nord", "lille", "hauts-de-france"]):
                if "2.4" in self.variants and self.variants["2.4"].sent < 5:
                    return "2.4"
            elif any(w in s for w in ["sud", "marseille", "nice", "toulouse", "bordeaux"]):
                if "2.5" in self.variants and self.variants["2.5"].sent < 5:
                    return "2.5"
            elif any(w in s for w in ["artisan", "plomb", "electr", "carrel", "bâtiment", "maçon"]):
                if "2.8" in self.variants and self.variants["2.8"].sent < 5:
                    return "2.8"

        # Ensure every variant gets at least 3 sends (exploration phase)
        unexplored = [v for v in self.variants.values() if v.sent < 3]
        if unexplored:
            chosen = random.choice(unexplored)
            logger.debug("Exploration: picked %s (%s)", chosen.agent_id, chosen.tone_name)
            return chosen.agent_id

        # Thompson Sampling exploitation
        samples = {vid: v.sample() for vid, v in self.variants.items()}
        best = max(samples, key=samples.__getitem__)
        logger.debug("Thompson sampling: picked %s (score=%.3f)", best, samples[best])
        return best

    def record_result(
        self,
        agent_id: str,
        sent: bool = True,
        opened: bool = False,
        replied: bool = False,
        paid: bool = False,
    ) -> None:
        """Record the outcome of an email sent by agent_id."""
        v = self.variants.get(agent_id)
        if not v:
            logger.warning("Unknown agent_id: %s", agent_id)
            return

        if sent:
            v.sent += 1
        if opened:
            v.opened += 1
        if replied:
            v.replied += 1
            v.alpha += 1  # success for Thompson
        else:
            v.beta += 0.5  # partial failure
        if paid:
            v.paid += 1
            v.alpha += 2  # strong success signal

    def get_winner(self) -> Optional[AgentVariant]:
        """Returns the current best-performing variant by reply rate."""
        eligible = [v for v in self.variants.values() if v.sent >= 10]
        if not eligible:
            return None
        return max(eligible, key=lambda v: v.reply_rate)

    def get_report(self) -> dict:
        """Full A/B test report."""
        winner = self.get_winner()
        variants_sorted = sorted(
            self.variants.values(), key=lambda v: v.reply_rate, reverse=True
        )
        return {
            "started_at": self._started_at,
            "total_sent": sum(v.sent for v in self.variants.values()),
            "total_replied": sum(v.replied for v in self.variants.values()),
            "winner": winner.to_dict() if winner else None,
            "variants": [v.to_dict() for v in variants_sorted],
        }

    def reset(self) -> None:
        """Reset all variant stats (start a new test period)."""
        for v in self.variants.values():
            v.sent = v.opened = v.replied = v.paid = 0
            v.alpha = 1.0
            v.beta = 1.0
        self._started_at = datetime.now().isoformat()
        logger.info("ABTester reset")
