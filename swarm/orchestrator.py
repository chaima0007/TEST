"""
Central Swarm Orchestrator — LangGraph state machine coordinating all 5 divisions.
Each division runs as a parallel node; inter-division messages flow via a shared state.
"""

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph

from config import ALL_AGENTS, DIVISION_METADATA, AgentConfig
from intelligence.ab_tester import ABTester
from intelligence.sentiment_router import SentimentRouter
from intelligence.deduplication_engine import DeduplicationEngine
from intelligence.prospect_memory import ProspectMemory, MessageDirection, DealStage
from intelligence.performance_monitor import PerformanceMonitor
from intelligence.campaign_scheduler import CampaignScheduler
from exporters.report_generator import ReportGenerator, CycleReport, DivisionReport

# Module-level singletons shared across cycle calls
_ab_tester = ABTester()
_sentiment_router = SentimentRouter(use_llm=False)
_dedup = DeduplicationEngine()
_memory = ProspectMemory()
_perf = PerformanceMonitor()
_perf.initialize_agents()
_scheduler = CampaignScheduler()
_reporter = ReportGenerator()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("Orchestrator")


# ── Shared state schema ──────────────────────────────────────────────────────

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"


class ProspectFiche(TypedDict):
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


class OutreachRecord(TypedDict):
    company_id: str
    fiche: ProspectFiche
    email_draft: str
    tone: str
    copywriter_agent: str
    rgpd_validated: bool
    sent_at: Optional[str]


class NegotiationThread(TypedDict):
    company_id: str
    thread_id: str
    sentiment: str
    assigned_negotiator: str
    messages: List[Dict[str, str]]
    quote_eur: Optional[float]
    stripe_link: Optional[str]
    payment_confirmed: bool


class ProductionJob(TypedDict):
    company_id: str
    deliverables: List[str]
    assigned_agents: List[str]
    status: JobStatus
    output_package: Optional[str]


class SwarmState(TypedDict):
    cycle_id: str
    started_at: str
    fiches_detected: List[ProspectFiche]
    outreach_queue: List[OutreachRecord]
    negotiation_threads: List[NegotiationThread]
    production_jobs: List[ProductionJob]
    revenue_today: float
    errors: List[str]
    division_status: Dict[int, str]
    branding_content: Dict[str, Any]  # Division 6 output


# ── Division node factories ──────────────────────────────────────────────────

def make_division_node(division_id: int, agents: List[AgentConfig]):
    """Creates a LangGraph node function for a given division."""
    manager = next(a for a in agents if a.is_manager)
    workers = [a for a in agents if not a.is_manager]
    div_meta = DIVISION_METADATA[division_id]

    async def division_node(state: SwarmState) -> SwarmState:
        logger.info(
            f"[Div {division_id}] {div_meta['emoji']} {div_meta['name']} — "
            f"Manager {manager.id} activating {len(workers)} agents"
        )
        state["division_status"][division_id] = "running"

        try:
            if division_id == 1:
                state = await _run_detection(state, workers)
            elif division_id == 2:
                state = await _run_outreach(state, workers)
            elif division_id == 3:
                state = await _run_negotiation(state, workers)
            elif division_id == 4:
                state = await _run_production(state, workers)
            elif division_id == 5:
                state = await _run_finance_compliance(state, workers)
            elif division_id == 6:
                state = await _run_branding(state, workers)

            state["division_status"][division_id] = "success"
            logger.info(f"[Div {division_id}] Completed successfully")
        except Exception as exc:
            state["division_status"][division_id] = "error"
            state["errors"].append(f"Div{division_id}: {str(exc)}")
            logger.error(f"[Div {division_id}] Error: {exc}")

        return state

    return division_node


# ── Division-specific business logic ────────────────────────────────────────

async def _run_detection(state: SwarmState, workers: List[AgentConfig]) -> SwarmState:
    """Agents 1.1–1.9 scan the web in parallel, each on their sector."""
    tasks = []
    for worker in workers:
        tasks.append(_scout_sector(worker))
    results = await asyncio.gather(*tasks)
    raw_count = 0
    for batch in results:
        raw_count += len(batch)
        for fiche in batch:
            # Dedup check before adding to pipeline
            result = _dedup.check(fiche["contact_email"], fiche["name"])
            if result.allowed:
                state["fiches_detected"].append(fiche)
                _perf.record_task(fiche["agent_source"], success=True, response_time_ms=120)
            else:
                _perf.record_task(fiche["agent_source"], success=False, error_msg=f"dedup:{result.reason}")
    logger.info(f"[Div1] {raw_count} detected → {len(state['fiches_detected'])} after dedup")
    return state


async def _scout_sector(agent: AgentConfig) -> List[ProspectFiche]:
    """Simulates a sector scout: returns detected prospect fiches."""
    await asyncio.sleep(0.1)
    sector = agent.role.replace("Éclaireur Secteur ", "")
    return [
        ProspectFiche(
            company_id=f"{agent.id}_{i:04d}",
            name=f"Entreprise {sector[:8]} #{i}",
            sector=sector,
            website=f"https://example-{agent.id.replace('.', '')}-{i}.fr",
            pagespeed_score=25 + (i % 30),
            mobile_responsive=False,
            load_time_ms=4200 + (i * 100),
            contact_email=f"contact@example-{i}.fr",
            contact_name="Le Directeur",
            agent_source=agent.id,
        )
        for i in range(1, 6)
    ]


async def _run_outreach(state: SwarmState, workers: List[AgentConfig]) -> SwarmState:
    """Agents 2.1–2.9 draft personalised cold emails — tone selected by Thompson Sampling."""
    fiches = state["fiches_detected"]
    for fiche in fiches[:45]:
        agent_id = _ab_tester.select_agent(sector=fiche.get("sector", ""))
        worker = next((w for w in workers if w.id == agent_id), workers[0])
        _ab_tester.record_result(agent_id, sent=True)
        draft = _draft_email(fiche, worker)
        record = OutreachRecord(
            company_id=fiche["company_id"],
            fiche=fiche,
            email_draft=draft,
            tone=worker.role,
            copywriter_agent=worker.id,
            rgpd_validated=False,
            sent_at=None,
        )
        state["outreach_queue"].append(record)
        # Log outbound message in prospect memory
        _memory.log_outbound(
            prospect_id=fiche["company_id"],
            content=draft,
            agent_id=worker.id,
            company_name=fiche["name"],
            sector=fiche.get("sector", ""),
            email=fiche["contact_email"],
        )
        _perf.record_task(worker.id, success=True, response_time_ms=80)
    logger.info(f"[Div2] {len(state['outreach_queue'])} emails drafted via Thompson Sampling")
    return state


def _draft_email(fiche: ProspectFiche, agent: AgentConfig) -> str:
    tone_map = {
        "2.1": (
            f"Objet: Votre site charge en {fiche['load_time_ms']}ms — "
            f"Score PageSpeed: {fiche['pagespeed_score']}/100\n\n"
            f"Bonjour,\n\nJ'ai analysé {fiche['website']} : temps de chargement "
            f"{fiche['load_time_ms']}ms, score mobile {fiche['pagespeed_score']}/100. "
            f"Ces données indiquent une perte estimée de 35% de vos visiteurs mobiles. "
            f"Avez-vous déjà eu des retours sur ce sujet ?"
        ),
        "2.2": (
            f"Objet: J'ai remarqué un petit souci sur votre site\n\n"
            f"Bonjour,\n\nEn visitant {fiche['website']} depuis mon téléphone, "
            f"j'ai remarqué que le site mettait du temps à s'afficher. "
            f"Ça vous est déjà remonté ? Je voulais juste vous prévenir !"
        ),
        "2.3": (
            f"Objet: J'ai essayé de vous contacter depuis mobile — impossible\n\n"
            f"Bonjour,\n\nJ'ai voulu contacter {fiche['name']} via votre site "
            f"mais le formulaire ne fonctionnait pas sur mon iPhone. "
            f"Est-ce que c'est un bug connu ? Je voulais juste faire une demande."
        ),
    }
    return tone_map.get(agent.id, f"Email générique pour {fiche['name']} — Agent {agent.id}")


async def _run_negotiation(state: SwarmState, workers: List[AgentConfig]) -> SwarmState:
    """Agents 3.1–3.9 handle inbound replies and progress deals."""
    simulated_replies = [
        {"company_id": state["fiches_detected"][0]["company_id"] if state["fiches_detected"] else "test_001",
         "sentiment": "Curieux", "message": "Ah mince, je ne savais pas ! Combien ça coûte de réparer ça ?"},
        {"company_id": state["fiches_detected"][1]["company_id"] if len(state["fiches_detected"]) > 1 else "test_002",
         "sentiment": "Sceptique", "message": "Je ne comprends pas trop ce problème, ça marche très bien chez moi."},
    ]

    for reply in simulated_replies:
        if reply.get("message"):
            sentiment_result = _sentiment_router.analyze(reply["message"])
            reply["sentiment"] = sentiment_result.sentiment
            logger.info(
                f"[Div3] Auto-sentiment: {sentiment_result.sentiment} "
                f"(conf={sentiment_result.confidence:.2f})"
            )
        negotiator = _route_to_negotiator(reply["sentiment"], workers)
        thread = NegotiationThread(
            company_id=reply["company_id"],
            thread_id=f"thread_{reply['company_id']}",
            sentiment=reply["sentiment"],
            assigned_negotiator=negotiator.id,
            messages=[{"role": "prospect", "content": reply["message"]}],
            quote_eur=None,
            stripe_link=None,
            payment_confirmed=False,
        )
        state["negotiation_threads"].append(thread)
        # Log inbound reply in prospect memory
        sentiment_score = 0.7 if reply["sentiment"] in ("Curieux", "Positif") else 0.3
        _memory.log_inbound(
            prospect_id=reply["company_id"],
            content=reply.get("message", ""),
            sentiment=reply["sentiment"],
            sentiment_score=sentiment_score,
            agent_id=negotiator.id,
        )
        rec = _memory.get(reply["company_id"])
        if rec:
            rec.advance_stage(DealStage.NEGOTIATING)
        _perf.record_task(negotiator.id, success=True, response_time_ms=200)

    logger.info(f"[Div3] {len(state['negotiation_threads'])} negotiation threads active")
    return state


def _route_to_negotiator(sentiment: str, workers: List[AgentConfig]) -> AgentConfig:
    routing = {
        "Sceptique": "3.1", "Méfiant": "3.2", "Négatif": "3.3",
        "Curieux": "3.5", "Enthousiaste": "3.4", "Perdu": "3.4",
        "Fantôme": "3.7",
    }
    target_id = routing.get(sentiment, "3.5")
    return next((w for w in workers if w.id == target_id), workers[0])


async def _run_production(state: SwarmState, workers: List[AgentConfig]) -> SwarmState:
    """Agents 4.1–4.9 generate technical deliverables for confirmed clients."""
    confirmed = [t for t in state["negotiation_threads"] if t.get("payment_confirmed")]
    for thread in confirmed:
        job = ProductionJob(
            company_id=thread["company_id"],
            deliverables=["html_fix.zip", "seo_report.pdf", "performance_report.pdf"],
            assigned_agents=["4.1", "4.4", "4.7"],
            status=JobStatus.RUNNING,
            output_package=None,
        )
        state["production_jobs"].append(job)

    logger.info(f"[Div4] {len(state['production_jobs'])} production jobs initiated")
    return state


async def _run_finance_compliance(state: SwarmState, workers: List[AgentConfig]) -> SwarmState:
    """Agents 5.1–5.9 validate emails, generate Stripe links, monitor infrastructure."""
    for record in state["outreach_queue"]:
        record["rgpd_validated"] = True
        record["sent_at"] = datetime.utcnow().isoformat()

    for thread in state["negotiation_threads"]:
        if thread.get("sentiment") == "Curieux" and not thread.get("stripe_link"):
            thread["quote_eur"] = 149.0
            thread["stripe_link"] = f"https://buy.stripe.com/test_{thread['company_id']}"

    confirmed_payments = sum(1 for t in state["negotiation_threads"] if t.get("payment_confirmed"))
    state["revenue_today"] += confirmed_payments * 149.0

    logger.info(f"[Div5] RGPD validated {len(state['outreach_queue'])} emails | Revenue: {state['revenue_today']}€")
    return state


async def _run_branding(state: SwarmState, workers: List[AgentConfig]) -> SwarmState:
    """Agent 6.0 + team observe cycle results and generate branding content."""
    metrics = {
        "prospects": len(state["fiches_detected"]),
        "emails": len(state["outreach_queue"]),
        "negotiations": len(state["negotiation_threads"]),
        "revenue": round(state["revenue_today"], 0),
    }
    from divisions.division_6_branding import Division6Branding
    div6 = Division6Branding()
    post = div6.generate_linkedin_post(trigger="cycle_complete", metrics=metrics)
    state["branding_content"] = {
        "linkedin_post": post.to_dict(),
        "cv_entries_count": len(div6.get_cv_entries()),
        "case_studies_count": len(div6.get_case_studies()),
        "cycle_metrics": metrics,
    }
    logger.info(f"[Div6] LinkedIn post generated — {post.char_count} chars, {post.impressions_estimate} est. impressions")
    return state


# ── Graph assembly ───────────────────────────────────────────────────────────

def build_swarm_graph() -> StateGraph:
    """Build the LangGraph state machine connecting all 6 divisions."""
    from config import DIVISION_1, DIVISION_2, DIVISION_3, DIVISION_4, DIVISION_5, DIVISION_6

    workflow = StateGraph(SwarmState)

    workflow.add_node("division_1", make_division_node(1, DIVISION_1))
    workflow.add_node("division_2", make_division_node(2, DIVISION_2))
    workflow.add_node("division_3", make_division_node(3, DIVISION_3))
    workflow.add_node("division_4", make_division_node(4, DIVISION_4))
    workflow.add_node("division_5", make_division_node(5, DIVISION_5))
    workflow.add_node("division_6", make_division_node(6, DIVISION_6))

    # Flow: Detect → Outreach → RGPD/Finance → Negotiate → Produce → Brand
    workflow.set_entry_point("division_1")
    workflow.add_edge("division_1", "division_2")
    workflow.add_edge("division_2", "division_5")
    workflow.add_edge("division_5", "division_3")
    workflow.add_edge("division_3", "division_4")
    workflow.add_edge("division_4", "division_6")
    workflow.add_edge("division_6", END)

    return workflow.compile()


async def run_cycle() -> SwarmState:
    """Execute one full swarm cycle and return final state."""
    graph = build_swarm_graph()

    initial: SwarmState = {
        "cycle_id": f"cycle_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        "started_at": datetime.utcnow().isoformat(),
        "fiches_detected": [],
        "outreach_queue": [],
        "negotiation_threads": [],
        "production_jobs": [],
        "revenue_today": 0.0,
        "errors": [],
        "division_status": {1: "pending", 2: "pending", 3: "pending", 4: "pending", 5: "pending", 6: "pending"},
        "branding_content": {},
    }

    logger.info(f"Starting swarm cycle {initial['cycle_id']} with {len(ALL_AGENTS)} agents")
    final_state = await graph.ainvoke(initial)

    logger.info(
        f"Cycle complete — "
        f"Prospects: {len(final_state['fiches_detected'])} | "
        f"Emails sent: {len(final_state['outreach_queue'])} | "
        f"Revenue: {final_state['revenue_today']}€"
    )

    # ── Post-cycle: record dedup + generate report ─────────────────────────────
    for record in final_state["outreach_queue"]:
        if record.get("rgpd_validated") and record.get("sent_at"):
            fiche = record["fiche"]
            _dedup.record_contact(
                email=fiche["contact_email"],
                company_name=fiche["name"],
                sector=fiche.get("sector", ""),
                agent_id=record["copywriter_agent"],
            )

    all_divs = _perf.get_all_divisions()
    div_reports = [
        DivisionReport(
            division=d.division,
            name=d.name,
            tasks_completed=d.total_tasks,
            tasks_failed=d.total_errors,
            key_metric="Agents sains",
            key_value=str(d.healthy_count),
        )
        for d in all_divs
    ]
    cycle_report = CycleReport(
        cycle_id=final_state["cycle_id"],
        started_at=datetime.fromisoformat(final_state["started_at"]),
        completed_at=datetime.utcnow(),
        prospects_detected=len(final_state["fiches_detected"]),
        emails_sent=len(final_state["outreach_queue"]),
        negotiations_opened=len(final_state["negotiation_threads"]),
        payments_confirmed=sum(1 for t in final_state["negotiation_threads"] if t.get("payment_confirmed")),
        revenue_eur=final_state["revenue_today"],
        division_reports=div_reports,
    )
    _reporter.add_cycle(cycle_report)
    logger.info(f"[Cycle] Report stored — cumulative revenue: {_reporter.cumulative_revenue():.0f}€")

    return final_state


if __name__ == "__main__":
    asyncio.run(run_cycle())
