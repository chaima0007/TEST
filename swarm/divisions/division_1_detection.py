"""
Division 1 — Détection & Scouting (10 agents)
Scans the web 24/7 by business sector to find sites with performance issues.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import List

from crewai import Crew, Process, Task

from config import DIVISION_1
from agents.base import SwarmAgent
from agents.tools import resolve_tools
from intelligence.prospect_enricher import ProspectEnricher

logger = logging.getLogger("Division1")

SECTORS = [
    "Artisans & Bâtiment",
    "Restauration & Hôtellerie",
    "Médical & Cabinets de Soin",
    "Boutiques E-commerce Locales",
    "Agences Immobilières",
    "Écoles & Organismes de Formation",
    "Garages & Concessionnaires",
    "Services Juridiques & Comptabilité",
    "Associations & Loisirs",
]


@dataclass
class ProspectFiche:
    company_id: str
    name: str
    sector: str
    website: str
    pagespeed_score: int
    mobile_responsive: bool
    load_time_ms: int
    contact_email: str
    contact_name: str
    agent_source: str
    detected_issues: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class Division1Detection:
    """
    Manager 1.0 orchestrates 9 sector scouts (1.1–1.9).
    Each scout targets one business sector and returns suspect fiches.
    """

    def __init__(self):
        self.agents = [SwarmAgent(cfg, resolve_tools(cfg.tools)) for cfg in DIVISION_1]
        self.manager = next(a for a in self.agents if a.is_manager)
        self.scouts = [a for a in self.agents if not a.is_manager]
        self.enricher = ProspectEnricher()
        logger.info(f"Division 1 initialised — Manager: {self.manager.id}, Scouts: {[s.id for s in self.scouts]}")

    def build_crew(self) -> Crew:
        """Build a CrewAI Crew with manager + 9 scouts in hierarchical mode."""
        scout_tasks = [
            Task(
                description=(
                    f"Tu es l'Agent Éclaireur spécialisé sur le secteur '{SECTORS[i % len(SECTORS)]}'. "
                    f"Scanne le Web via Google Maps pour trouver 100 entreprises dans ce secteur. "
                    f"Analyse chaque site : identifie ceux avec un PageSpeed mobile < 50 ou un temps "
                    f"de chargement > 4 000ms. Retourne la liste au format JSON avec les champs : "
                    f"company_name, website, pagespeed_score, load_time_ms, mobile_responsive, contact_email."
                ),
                expected_output="JSON array de fiches prospects qualifiés",
                agent=scout.build(),
            )
            for i, scout in enumerate(self.scouts)
        ]

        manager_task = Task(
            description=(
                "En tant que Manager de la Division 1, récupère les listes JSON de tous tes 9 agents éclaireurs. "
                "Déduplique par domaine, trie par score de priorité (PageSpeed le plus bas en premier), "
                "et retourne une liste unifiée des 100 meilleures fiches à traiter en priorité."
            ),
            expected_output="JSON array unifié et dédupliqué de 100 fiches prospects prioritaires",
            agent=self.manager.build(),
            context=scout_tasks,
        )

        return Crew(
            agents=[a.build() for a in self.agents],
            tasks=[*scout_tasks, manager_task],
            process=Process.hierarchical,
            manager_agent=self.manager.build(),
            verbose=False,
        )

    async def run(self, target_per_scout: int = 100) -> List[ProspectFiche]:
        """Execute all scouts in parallel and aggregate results."""
        logger.info(f"[Div1] Starting detection — target {target_per_scout * len(self.scouts)} prospects")

        tasks = [self._scout_sector(scout, SECTORS[i % len(SECTORS)]) for i, scout in enumerate(self.scouts)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        fiches: List[ProspectFiche] = []
        for batch in results:
            if isinstance(batch, Exception):
                logger.error(f"[Div1] Scout error: {batch}")
                continue
            fiches.extend(batch)

        seen = set()
        unique: List[ProspectFiche] = []
        for f in fiches:
            if f.website not in seen:
                seen.add(f.website)
                unique.append(f)

        # Enrich and sort by priority score (Tier A first)
        enriched = self.enricher.enrich_batch(unique)
        # Re-sort original fiches by the enriched priority order
        priority_map = {e.company_id: e.priority_score for e in enriched}
        unique.sort(key=lambda f: priority_map.get(f.company_id, 0), reverse=True)

        tier_a = sum(1 for e in enriched if e.tier == "A")
        logger.info(f"[Div1] Detection complete — {len(unique)} unique prospects ({tier_a} Tier A)")
        return unique

    async def _scout_sector(self, agent: SwarmAgent, sector: str) -> List[ProspectFiche]:
        """Simulate a sector scout (replace with real API call in production)."""
        await asyncio.sleep(0.05)
        import random
        return [
            ProspectFiche(
                company_id=f"{agent.id}_{i:04d}",
                name=f"{sector[:12]} Entreprise #{i}",
                sector=sector,
                website=f"https://site-{agent.id.replace('.', '')}-{i}.fr",
                pagespeed_score=random.randint(8, 49),
                mobile_responsive=False,
                load_time_ms=random.randint(4100, 9800),
                contact_email=f"contact@site-{i}.fr",
                contact_name="Le Directeur",
                agent_source=agent.id,
                detected_issues=["Non-responsive mobile", "PageSpeed critique"],
            )
            for i in range(1, 11)
        ]
