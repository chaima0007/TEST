"""
Tool stubs for swarm agents.
In production, replace with real API implementations.
"""

from __future__ import annotations

import json
import random
from typing import Any, Optional

from crewai.tools import BaseTool
from pydantic import Field


class GoogleMapsAPITool(BaseTool):
    name: str = "google_maps_api"
    description: str = "Search Google Maps for businesses in a sector and location. Returns a list of business names, addresses and websites."

    def _run(self, query: str) -> str:
        results = [
            {"name": f"Entreprise {i}", "website": f"https://example-{i}.fr", "address": f"{i} rue du Commerce, Paris"}
            for i in range(1, 11)
        ]
        return json.dumps(results)


class PageSpeedCheckerTool(BaseTool):
    name: str = "pagespeed_checker"
    description: str = "Check PageSpeed Insights score and load time for a given URL. Returns score (0-100), load time in ms, and mobile responsive status."

    def _run(self, url: str) -> str:
        score = random.randint(10, 55)
        load_ms = random.randint(3500, 9000)
        responsive = score > 45
        return json.dumps({"url": url, "score": score, "load_time_ms": load_ms, "mobile_responsive": responsive})


class JSONAggregatorTool(BaseTool):
    name: str = "json_aggregator"
    description: str = "Aggregate multiple JSON lists from sub-agents into a single deduplicated list."

    def _run(self, data: str) -> str:
        return json.dumps({"status": "aggregated", "count": random.randint(40, 100)})


class TerritorySplitterTool(BaseTool):
    name: str = "territory_splitter"
    description: str = "Split a list of sectors or regions among N agents to avoid duplication."

    def _run(self, sectors: str) -> str:
        splits = {"agent_1.1": "Artisans", "agent_1.2": "Restauration", "agent_1.3": "Médical"}
        return json.dumps(splits)


class EmailTemplateEngineTool(BaseTool):
    name: str = "email_template_engine"
    description: str = "Generate a personalised cold email given company name, sector, detected issues, and tone."

    def _run(self, context: str) -> str:
        return f"Email généré pour : {context[:80]}..."


class SentimentAnalyzerTool(BaseTool):
    name: str = "sentiment_analyzer"
    description: str = "Analyze the sentiment of an inbound email. Returns: Positif, Curieux, Sceptique, Négatif, or Urgent."

    def _run(self, email_body: str) -> str:
        sentiments = ["Curieux", "Sceptique", "Enthousiaste", "Négatif", "Urgent"]
        return random.choice(sentiments)


class EmailRouterTool(BaseTool):
    name: str = "email_router"
    description: str = "Route an inbound email to the most suitable negotiator agent based on sentiment and sector."

    def _run(self, context: str) -> str:
        return json.dumps({"assigned_to": "3.5", "reason": "Prospect curieux, profil standard"})


class StripePriceLinkTool(BaseTool):
    name: str = "stripe_payment_link"
    description: str = "Create a Stripe payment link for a given amount in EUR. Returns the payment URL."

    def _run(self, amount_eur: str) -> str:
        return json.dumps({"url": f"https://buy.stripe.com/test_{random.randint(1000,9999)}", "amount": amount_eur})


class RGPDScannerTool(BaseTool):
    name: str = "rgpd_email_scanner"
    description: str = "Scan an email draft for RGPD compliance: checks for unsubscribe link, no aggressive tone, no personal data without consent."

    def _run(self, email_draft: str) -> str:
        has_stop = "STOP" in email_draft or "désinscrire" in email_draft.lower()
        return json.dumps({"compliant": has_stop, "issues": [] if has_stop else ["Missing STOP link"]})


class AgentHealthDashboardTool(BaseTool):
    name: str = "agent_health_dashboard"
    description: str = "Return the health status of all 50 agents: active count, error count, queue depths."

    def _run(self, _: str = "") -> str:
        return json.dumps({
            "total": 50, "active": 38, "idle": 10, "error": 2,
            "queue_depth": random.randint(0, 25),
        })


class LogAggregatorTool(BaseTool):
    name: str = "log_aggregator"
    description: str = "Aggregate and summarise logs from all 50 agents for the last N minutes."

    def _run(self, minutes: str = "60") -> str:
        return json.dumps({
            "period_minutes": int(minutes),
            "total_events": random.randint(500, 2000),
            "errors": random.randint(0, 5),
            "warnings": random.randint(5, 30),
        })


# ── Tool registry ─────────────────────────────────────────────────────────────

TOOL_REGISTRY: dict[str, BaseTool] = {
    "google_maps_api": GoogleMapsAPITool(),
    "pagespeed_checker": PageSpeedCheckerTool(),
    "json_aggregator": JSONAggregatorTool(),
    "territory_splitter": TerritorySplitterTool(),
    "email_template_engine": EmailTemplateEngineTool(),
    "sentiment_analyzer": SentimentAnalyzerTool(),
    "email_router": EmailRouterTool(),
    "stripe_payment_link": StripePriceLinkTool(),
    "stripe_price_creator": StripePriceLinkTool(),
    "stripe_webhook_listener": StripePriceLinkTool(),
    "rgpd_email_scanner": RGPDScannerTool(),
    "agent_health_dashboard": AgentHealthDashboardTool(),
    "log_aggregator": LogAggregatorTool(),
}


def resolve_tools(tool_names: list[str]) -> list[BaseTool]:
    """Return instantiated tool objects for a list of tool name strings."""
    return [TOOL_REGISTRY[name] for name in tool_names if name in TOOL_REGISTRY]
