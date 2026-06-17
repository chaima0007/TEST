"""
FastAPI REST server exposing swarm status to the Next.js dashboard.
Run: uvicorn api_server:app --host 0.0.0.0 --port 8001 --reload

Next.js API route at /api/swarm proxies to http://localhost:8001/swarm
when SWARM_API_URL env var is set; falls back to mock data otherwise.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import ALL_AGENTS, DIVISION_METADATA
from divisions.division_1_detection import Division1Detection
from divisions.division_2_redaction import Division2Redaction
from divisions.division_3_negotiation import Division3Negotiation, NegotiationThread
from divisions.division_4_production import Division4Production
from divisions.division_5_finance import Division5Finance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SwarmAPI")

app = FastAPI(
    title="Swarm Intelligence API",
    description="REST interface for the 50-agent autonomous swarm",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Singleton division instances ──────────────────────────────────────────────

_div1 = Division1Detection()
_div2 = Division2Redaction()
_div3 = Division3Negotiation()
_div4 = Division4Production()
_div5 = Division5Finance()

# In-memory store (replace with Redis/DB in production)
_active_threads: Dict[str, NegotiationThread] = {}
_cycle_running = False
_last_cycle_summary: Optional[Dict] = None


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class AgentStatusOut(BaseModel):
    id: str
    division: int
    role: str
    is_manager: bool
    status: str
    tasks_completed: int


class DivisionStatusOut(BaseModel):
    id: int
    name: str
    color: str
    emoji: str
    agents: List[AgentStatusOut]
    kpi_label: str
    kpi_value: Any


class SwarmStatusOut(BaseModel):
    timestamp: str
    cycle_running: bool
    agents_total: int
    agents_active: int
    agents_idle: int
    agents_error: int
    revenue_today: float
    transactions_today: int
    active_threads: int
    divisions: List[DivisionStatusOut]


class TriggerCycleOut(BaseModel):
    message: str
    cycle_id: str


class ProspectIn(BaseModel):
    company_id: str
    company_name: str
    sector: str
    website: str
    contact_email: str
    issues: List[str]


class InboundReplyIn(BaseModel):
    company_id: str
    prospect_name: str
    sector: str
    message: str
    sentiment: str


class PaymentConfirmIn(BaseModel):
    thread_id: str
    amount_eur: float
    stripe_charge_id: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _agent_status(agent_id: str, division: int) -> AgentStatusOut:
    import random
    statuses = ["active", "active", "active", "idle", "active", "active", "idle", "active", "active", "error"]
    cfg = next((a for a in ALL_AGENTS if a.id == agent_id), None)
    slot = int(agent_id.split(".")[-1])
    return AgentStatusOut(
        id=agent_id,
        division=division,
        role=cfg.role if cfg else f"Agent {agent_id}",
        is_manager=cfg.is_manager if cfg else (slot == 0),
        status=statuses[slot % len(statuses)],
        tasks_completed=random.randint(10, 90),
    )


def _division_status(div_id: int) -> DivisionStatusOut:
    meta = DIVISION_METADATA[div_id]
    agents = [_agent_status(f"{div_id}.{i}", div_id) for i in range(10)]
    kpi_map = {
        1: ("Prospects/jour", 847),
        2: ("Emails envoyés", 312),
        3: ("Taux de réponse", "23.4%"),
        4: ("Livrables/h", 7),
        5: ("CA aujourd'hui", f"{_div5.get_revenue():.0f}€"),
    }
    kpi_label, kpi_value = kpi_map[div_id]
    return DivisionStatusOut(
        id=div_id,
        name=meta["name"],
        color=meta["color"],
        emoji=meta["emoji"],
        agents=agents,
        kpi_label=kpi_label,
        kpi_value=kpi_value,
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "online", "agents": len(ALL_AGENTS), "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return _div5.check_system_health()


@app.get("/swarm/status", response_model=SwarmStatusOut, tags=["Swarm"])
def get_status():
    health = _div5.check_system_health()
    return SwarmStatusOut(
        timestamp=datetime.utcnow().isoformat(),
        cycle_running=_cycle_running,
        agents_total=50,
        agents_active=health["agents_active"],
        agents_idle=health["agents_idle"],
        agents_error=health["agents_error"],
        revenue_today=_div5.get_revenue(),
        transactions_today=_div5.get_transaction_count(),
        active_threads=len([t for t in _active_threads.values() if not t.closed]),
        divisions=[_division_status(i) for i in range(1, 6)],
    )


@app.post("/swarm/cycle/trigger", response_model=TriggerCycleOut, tags=["Swarm"])
async def trigger_cycle(background_tasks: BackgroundTasks):
    global _cycle_running
    if _cycle_running:
        raise HTTPException(status_code=409, detail="A cycle is already running")

    cycle_id = f"cycle_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    background_tasks.add_task(_run_full_cycle, cycle_id)
    return TriggerCycleOut(message="Cycle started", cycle_id=cycle_id)


async def _run_full_cycle(cycle_id: str):
    global _cycle_running, _last_cycle_summary
    _cycle_running = True
    try:
        logger.info(f"[API] Cycle {cycle_id} started")
        fiches = await _div1.run()
        records = _div2.draft_all(fiches)
        for record in records:
            _div5.validate_email_rgpd(record)
        _last_cycle_summary = {
            "cycle_id": cycle_id,
            "completed_at": datetime.utcnow().isoformat(),
            "fiches_detected": len(fiches),
            "emails_drafted": len(records),
            "revenue": _div5.get_revenue(),
        }
        logger.info(f"[API] Cycle {cycle_id} complete — {len(fiches)} fiches, {len(records)} emails")
    finally:
        _cycle_running = False


@app.get("/swarm/cycle/last", tags=["Swarm"])
def get_last_cycle():
    if not _last_cycle_summary:
        raise HTTPException(status_code=404, detail="No cycle has run yet")
    return _last_cycle_summary


@app.post("/negotiation/inbound", tags=["Negotiation"])
def handle_inbound_reply(payload: InboundReplyIn):
    """Division 3 — Handle an inbound prospect reply and open a negotiation thread."""
    if _div5.is_blacklisted(payload.company_id):
        return {"status": "blacklisted", "action": "ignored"}

    thread = _div3.open_thread(
        company_id=payload.company_id,
        prospect_name=payload.prospect_name,
        sector=payload.sector,
        initial_message=payload.message,
        sentiment=payload.sentiment,
    )

    stripe_link = _div5.create_stripe_link(payload.company_id, payload.sector)
    thread.stripe_link = stripe_link.url
    thread.quote_eur = stripe_link.amount_eur

    reply = _div3.generate_response(thread, quote_eur=stripe_link.amount_eur)
    _active_threads[thread.thread_id] = thread

    return {
        "thread_id": thread.thread_id,
        "assigned_negotiator": thread.assigned_negotiator,
        "quote_eur": stripe_link.amount_eur,
        "stripe_link": stripe_link.url,
        "reply_preview": reply[:200],
    }


@app.post("/payment/confirm", tags=["Finance"])
async def confirm_payment(payload: PaymentConfirmIn):
    """Division 5 → Division 4 — Confirm payment and trigger production."""
    thread = next((t for t in _active_threads.values() if t.thread_id == payload.thread_id), None)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    _div3.confirm_payment(thread, payload.amount_eur)

    job = _div4.create_job(
        company_id=thread.company_id,
        company_name=thread.prospect_name,
        sector=thread.sector,
        issues=["Non-responsive mobile", "PageSpeed critique"],
    )
    completed_job = await _div4.execute_job(job)

    return {
        "status": "production_complete",
        "job_id": completed_job.job_id,
        "deliverables": len(completed_job.deliverables),
        "package_url": completed_job.output_package_url,
        "revenue_today": _div5.get_revenue(),
    }


@app.get("/finance/report", tags=["Finance"])
def get_financial_report():
    return _div5.generate_daily_report().__dict__


@app.post("/compliance/opt-out", tags=["Compliance"])
def process_opt_out(domain: str):
    _div5.process_opt_out(domain)
    return {"status": "blacklisted", "domain": domain}


@app.get("/agents", tags=["Agents"])
def list_agents():
    return [
        {
            "id": a.id,
            "division": a.division,
            "role": a.role,
            "goal": a.goal[:120],
            "is_manager": a.is_manager,
            "tools": a.tools,
        }
        for a in ALL_AGENTS
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
