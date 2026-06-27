"""
Division 4 — Production & Design (10 agents)
Generates all technical deliverables instantly after payment confirmation.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from config import DIVISION_4
from agents.base import SwarmAgent
from agents.tools import resolve_tools

logger = logging.getLogger("Division4")


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Deliverable:
    filename: str
    content_type: str
    description: str
    agent_id: str
    size_kb: int = 0
    download_url: Optional[str] = None


@dataclass
class ProductionJob:
    job_id: str
    company_id: str
    company_name: str
    sector: str
    issues: List[str]
    deliverables: List[Deliverable] = field(default_factory=list)
    assigned_agents: List[str] = field(default_factory=list)
    status: JobStatus = JobStatus.PENDING
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    output_package_url: Optional[str] = None

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["deliverables"] = [dl.__dict__ for dl in self.deliverables]
        d["status"] = self.status.value
        return d


ISSUE_TO_AGENTS: Dict[str, List[str]] = {
    "Non-responsive mobile": ["4.1", "4.2"],
    "PageSpeed critique": ["4.7", "4.9"],
    "SEO manquant": ["4.4", "4.5", "4.6"],
    "SSL absent": ["4.8"],
    "WordPress non-responsive": ["4.3"],
    "Core Web Vitals": ["4.9", "4.7"],
}

DELIVERABLE_TEMPLATES: Dict[str, List[dict]] = {
    "4.1": [{"filename": "responsive_fix.html", "content_type": "text/html", "description": "HTML/CSS corrigé mobile-first"}],
    "4.2": [{"filename": "scripts_fix.js", "content_type": "application/javascript", "description": "JS réparé — menus et formulaires mobiles"}],
    "4.3": [{"filename": "child_theme_fix.zip", "content_type": "application/zip", "description": "Thème WordPress enfant corrigé"}],
    "4.4": [{"filename": "seo_balises.txt", "content_type": "text/plain", "description": "Meta-titles, meta-descriptions, H1-H6 optimisés"}],
    "4.5": [{"filename": "contenu_optimise.docx", "content_type": "application/vnd.openxmlformats", "description": "Textes SEO réécrits"}],
    "4.6": [{"filename": "local_seo_config.json", "content_type": "application/json", "description": "Données structurées LocalBusiness + maillage interne"}],
    "4.7": [{"filename": "image_optimizer.sh", "content_type": "text/x-shellscript", "description": "Script de compression WebP + lazy loading"}],
    "4.8": [{"filename": "ssl_headers.nginx", "content_type": "text/plain", "description": "Config Nginx — HTTPS, HSTS, CSP headers"}],
    "4.9": [{"filename": "cwv_report.pdf", "content_type": "application/pdf", "description": "Rapport Core Web Vitals avant/après"}],
}


class Division4Production:
    """
    CTO agent 4.0 receives production jobs from Division 3 (payment confirmed)
    and distributes work to 9 specialist agents (dev, SEO, performance).
    """

    def __init__(self):
        self.agents = [SwarmAgent(cfg, resolve_tools(cfg.tools)) for cfg in DIVISION_4]
        self.manager = next(a for a in self.agents if a.is_manager)
        self.workers = {a.id: a for a in self.agents if not a.is_manager}
        logger.info(f"Division 4 initialised — {len(self.workers)} specialists ready")

    def assign_agents(self, issues: List[str]) -> List[str]:
        """Determine which specialist agents are needed based on detected issues."""
        needed: set[str] = set()
        for issue in issues:
            for key, agents in ISSUE_TO_AGENTS.items():
                if key.lower() in issue.lower():
                    needed.update(agents)
        if not needed:
            needed = {"4.1", "4.4", "4.7"}
        return sorted(needed)

    async def execute_job(self, job: ProductionJob) -> ProductionJob:
        """Execute a production job: assign agents and generate deliverables in parallel."""
        import datetime

        job.status = JobStatus.RUNNING
        job.started_at = datetime.datetime.utcnow().isoformat()
        job.assigned_agents = self.assign_agents(job.issues)

        logger.info(
            f"[Div4] Job {job.job_id} started — "
            f"Company: {job.company_name} — Agents: {job.assigned_agents}"
        )

        tasks = [self._generate_deliverable(agent_id, job) for agent_id in job.assigned_agents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.error(f"[Div4] Deliverable error: {result}")
            elif result:
                job.deliverables.extend(result)

        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.datetime.utcnow().isoformat()
        job.output_package_url = f"https://cdn.swarm.internal/packages/{job.job_id}.zip"

        logger.info(
            f"[Div4] Job {job.job_id} complete — "
            f"{len(job.deliverables)} deliverables in "
            f"{(datetime.datetime.fromisoformat(job.completed_at) - datetime.datetime.fromisoformat(job.started_at)).seconds}s"
        )
        return job

    async def _generate_deliverable(self, agent_id: str, job: ProductionJob) -> List[Deliverable]:
        """Simulate deliverable generation by a specialist agent."""
        await asyncio.sleep(0.1)
        templates = DELIVERABLE_TEMPLATES.get(agent_id, [])
        return [
            Deliverable(
                filename=t["filename"],
                content_type=t["content_type"],
                description=t["description"],
                agent_id=agent_id,
                size_kb=12 + hash(t["filename"]) % 200,
                download_url=f"https://cdn.swarm.internal/{job.job_id}/{t['filename']}",
            )
            for t in templates
        ]

    def create_job(self, company_id: str, company_name: str, sector: str, issues: List[str]) -> ProductionJob:
        """Create a new production job after payment confirmation."""
        import datetime
        return ProductionJob(
            job_id=f"job_{company_id}_{datetime.datetime.utcnow().strftime('%H%M%S')}",
            company_id=company_id,
            company_name=company_name,
            sector=sector,
            issues=issues,
        )
