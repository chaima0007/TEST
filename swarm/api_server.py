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
from divisions.division_6_branding import Division6Branding
from webhooks.stripe import stripe_router
from intelligence.performance_monitor import PerformanceMonitor
from intelligence.sector_analyzer import SectorAnalyzer
from intelligence.email_tracker import EmailTracker
from intelligence.lead_scorer import LeadScorer
from intelligence.campaign_scheduler import CampaignScheduler
from intelligence.deduplication_engine import DeduplicationEngine, SuppressionReason

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

app.include_router(stripe_router, prefix="/webhooks", tags=["Webhooks"])

# ── Singleton division instances ──────────────────────────────────────────────

_div1 = Division1Detection()
_div2 = Division2Redaction()
_div3 = Division3Negotiation()
_div4 = Division4Production()
_div5 = Division5Finance()
_div6 = Division6Branding()

# In-memory store (replace with Redis/DB in production)
_active_threads: Dict[str, NegotiationThread] = {}
_cycle_running = False
_last_cycle_summary: Optional[Dict] = None

# Intelligence singletons
_perf_monitor = PerformanceMonitor()
_perf_monitor.initialize_agents()
_sector_analyzer = SectorAnalyzer()
_email_tracker = EmailTracker()
_lead_scorer = LeadScorer()
_campaign_scheduler = CampaignScheduler()
_dedup_engine = DeduplicationEngine()


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
    sentiment: Optional[str] = None  # if omitted, auto-detected by SentimentRouter


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
    posts_count = len(_div6.get_all_content().get("linkedin_posts", []))
    kpi_map = {
        1: ("Prospects/jour", 847),
        2: ("Emails envoyés", 312),
        3: ("Taux de réponse", "23.4%"),
        4: ("Livrables/h", 7),
        5: ("CA aujourd'hui", f"{_div5.get_revenue():.0f}€"),
        6: ("Posts LinkedIn", posts_count),
    }
    kpi_label, kpi_value = kpi_map.get(div_id, ("—", "—"))
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
        divisions=[_division_status(i) for i in range(1, 7)],
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

    if payload.sentiment:
        thread = _div3.open_thread(
            company_id=payload.company_id,
            prospect_name=payload.prospect_name,
            sector=payload.sector,
            initial_message=payload.message,
            sentiment=payload.sentiment,
        )
    else:
        thread = _div3.analyze_and_open_thread(
            company_id=payload.company_id,
            prospect_name=payload.prospect_name,
            sector=payload.sector,
            initial_message=payload.message,
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


@app.get("/branding/content", tags=["Branding"])
def get_branding_content():
    """Division 6 — LinkedIn posts, CV entries, and case studies."""
    return _div6.get_all_content()


@app.post("/branding/generate", tags=["Branding"])
def generate_branding_content(trigger: str = "cycle_complete"):
    """Division 6 — Generate a new LinkedIn post for the given event trigger."""
    metrics = {"prospects": 847, "emails": 312, "negotiations": 28, "revenue": 2237}
    post = _div6.generate_linkedin_post(trigger=trigger, metrics=metrics)
    return post.to_dict()


@app.get("/abtesting/report", tags=["Intelligence"])
def get_ab_report():
    """Division 2 — Current A/B test performance across 9 copywriting tones."""
    return _div2.get_ab_report()


@app.post("/abtesting/record", tags=["Intelligence"])
def record_ab_result(agent_id: str, opened: bool = False, replied: bool = False, paid: bool = False):
    """Feed email outcome back to Thompson Sampling posteriors."""
    _div2.record_reply(agent_id, opened=opened, replied=replied, paid=paid)
    return {"status": "recorded", "agent_id": agent_id}


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


# ── Performance monitor ───────────────────────────────────────────────────────

@app.get("/agents/health", tags=["Monitoring"])
def agents_health():
    """Global health summary + per-division stats for all 60 agents."""
    divisions = [d.to_dict() for d in _perf_monitor.get_all_divisions()]
    alerts = [a.to_dict() for a in _perf_monitor.get_alerts()]
    return {
        "source": "live",
        "summary": _perf_monitor.global_summary(),
        "divisions": divisions,
        "alerts": alerts[:10],
    }


@app.post("/agents/{agent_id}/task", tags=["Monitoring"])
def record_agent_task(agent_id: str, success: bool = True, response_time_ms: int = 0, error_msg: str = ""):
    """Record a task outcome for an agent — updates health metrics."""
    _perf_monitor.record_task(
        agent_id=agent_id,
        success=success,
        response_time_ms=response_time_ms if response_time_ms else None,
        error_msg=error_msg or None,
    )
    return {"status": "recorded", "agent_id": agent_id}


@app.post("/agents/{agent_id}/heartbeat", tags=["Monitoring"])
def agent_heartbeat(agent_id: str):
    """Mark an agent alive."""
    _perf_monitor.heartbeat(agent_id)
    return {"status": "ok", "agent_id": agent_id}


# ── Sector analyzer ───────────────────────────────────────────────────────────

@app.get("/sectors", tags=["Intelligence"])
def get_sectors(sort_by: str = "opportunity"):
    """All French business sectors ranked by opportunity score."""
    ranked = _sector_analyzer.ranked_by_opportunity()
    return {
        "sectors": [
            {
                "sector_id": s.sector_id,
                "name": s.name,
                "tags": s.tags,
                "market_size_eur": s.market_size_eur,
                "competition_density": s.competition_density,
                "roi_multiplier": s.roi_multiplier,
                "avg_ticket_eur": s.avg_ticket_eur,
                "icp_priority": s.icp_priority(),
                "recommended_volume": s.recommended_volume(),
                "opportunity_score": round(s.roi_multiplier / s.competition_density, 3),
            }
            for s in ranked
        ],
        "total_addressable_market": _sector_analyzer.total_addressable_market(),
        "priority_sectors": _sector_analyzer.s_priority_sectors(),
        "weekly_plan": _sector_analyzer.weekly_outreach_plan(),
    }


@app.get("/sectors/{sector_name}", tags=["Intelligence"])
def get_sector(sector_name: str):
    """Fetch a specific sector by tag or name."""
    profile = _sector_analyzer.get_by_name(sector_name)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Sector '{sector_name}' not found")
    return {
        "sector_id": profile.sector_id,
        "name": profile.name,
        "tags": profile.tags,
        "market_size_eur": profile.market_size_eur,
        "competition_density": profile.competition_density,
        "roi_multiplier": profile.roi_multiplier,
        "avg_ticket_eur": profile.avg_ticket_eur,
        "icp_priority": profile.icp_priority(),
        "recommended_volume": profile.recommended_volume(),
    }


# ── Email tracking ────────────────────────────────────────────────────────────

@app.get("/tracking/report", tags=["Tracking"])
def tracking_report(n: int = 10):
    """Email campaign performance overview."""
    return {
        "summary": _email_tracker.summary(),
        "top_campaigns": [m.to_dict() for m in _email_tracker.top_campaigns(n=n)],
        "agent_leaderboard": _email_tracker.agent_leaderboard(n=n),
    }


@app.post("/tracking/event", tags=["Tracking"])
def record_tracking_event(
    campaign_id: str,
    agent_id: str = "",
    opened: bool = False,
    clicked: bool = False,
    replied: bool = False,
    paid: bool = False,
):
    """Record an email tracking event (open / click / reply / payment)."""
    _email_tracker.track(
        campaign_id=campaign_id,
        agent_id=agent_id,
        opened=opened,
        clicked=clicked,
        replied=replied,
        paid=paid,
    )
    return {"status": "tracked", "campaign_id": campaign_id}


@app.get("/tracking/campaign/{campaign_id}", tags=["Tracking"])
def campaign_metrics(campaign_id: str):
    """Metrics for a specific campaign."""
    m = _email_tracker.get_metrics(campaign_id)
    if not m:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return m.to_dict()


# ── Campaign scheduler ────────────────────────────────────────────────────────

class CampaignPlanIn(BaseModel):
    sector: str
    total_leads: int
    agent_id: str
    tier_filter: str = "A"
    priority: str = "normal"


class MultiSectorPlanIn(BaseModel):
    sector_volumes: Dict[str, int]
    agent_assignments: Optional[Dict[str, str]] = None


@app.post("/campaigns/plan", tags=["Campaigns"])
def create_campaign_plan(payload: CampaignPlanIn):
    """Plan a campaign for a single sector."""
    plan = _campaign_scheduler.plan(
        sector=payload.sector,
        total_leads=payload.total_leads,
        agent_id=payload.agent_id,
        tier_filter=payload.tier_filter,
        priority=payload.priority,
    )
    return plan.to_dict()


@app.post("/campaigns/plan-multi", tags=["Campaigns"])
def create_multi_sector_plan(payload: MultiSectorPlanIn):
    """Plan campaigns for multiple sectors at once."""
    plans = _campaign_scheduler.plan_multi_sector(
        sector_volumes=payload.sector_volumes,
        agent_assignments=payload.agent_assignments,
    )
    return [p.to_dict() for p in plans]


@app.get("/campaigns/pending", tags=["Campaigns"])
def pending_waves():
    """Waves due to be sent now."""
    return [w.to_dict() for w in _campaign_scheduler.pending_waves()]


@app.get("/campaigns/summary", tags=["Campaigns"])
def campaigns_summary():
    return _campaign_scheduler.summary()


@app.post("/campaigns/{plan_id}/waves/{wave_id}/done", tags=["Campaigns"])
def mark_wave_done(plan_id: str, wave_id: str):
    ok = _campaign_scheduler.mark_wave_done(plan_id, wave_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Wave not found")
    return {"status": "done", "wave_id": wave_id}


@app.post("/campaigns/{plan_id}/waves/{wave_id}/cancel", tags=["Campaigns"])
def cancel_wave(plan_id: str, wave_id: str):
    ok = _campaign_scheduler.cancel_wave(plan_id, wave_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Wave not found")
    return {"status": "cancelled", "wave_id": wave_id}


# ── Deduplication ─────────────────────────────────────────────────────────────

class SuppressIn(BaseModel):
    key: str
    key_type: str = "email"
    reason: str = "opt_out"
    note: str = ""


class CheckIn(BaseModel):
    email: str
    company_name: str = ""
    city: str = ""
    phone: str = ""


@app.post("/dedup/check", tags=["Deduplication"])
def dedup_check(payload: CheckIn):
    """Check if a prospect can be contacted now."""
    result = _dedup_engine.check(
        email=payload.email,
        company_name=payload.company_name,
        city=payload.city,
        phone=payload.phone,
    )
    return result.to_dict()


@app.post("/dedup/record", tags=["Deduplication"])
def dedup_record(payload: CheckIn, agent_id: str = "", sector: str = ""):
    """Log that a prospect was contacted."""
    _dedup_engine.record_contact(
        email=payload.email,
        company_name=payload.company_name,
        city=payload.city,
        phone=payload.phone,
        agent_id=agent_id,
        sector=sector,
    )
    return {"status": "recorded"}


@app.post("/dedup/suppress", tags=["Deduplication"])
def suppress_contact(payload: SuppressIn):
    """Permanently suppress a contact (opt-out, bounce, spam…)."""
    try:
        reason = SuppressionReason(payload.reason)
    except ValueError:
        reason = SuppressionReason.MANUAL
    _dedup_engine.suppress(payload.key, payload.key_type, reason, payload.note)
    return {"status": "suppressed", "key": payload.key}


@app.delete("/dedup/suppress/{key}", tags=["Deduplication"])
def remove_suppression(key: str):
    """Remove a key from the suppression list."""
    removed = _dedup_engine.unsuppress(key)
    if not removed:
        raise HTTPException(status_code=404, detail="Key not in suppression list")
    return {"status": "removed", "key": key}


@app.get("/dedup/suppression-list", tags=["Deduplication"])
def get_suppression_list():
    return {
        "entries": _dedup_engine.export_suppression_list(),
        "summary": _dedup_engine.summary(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
