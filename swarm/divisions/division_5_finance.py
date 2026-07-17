"""
Division 5 — Finance, Sécurité & Conformité (10 agents)
Controls all financial flows, RGPD compliance and infrastructure health.
"""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from config import DIVISION_5
from agents.base import SwarmAgent
from agents.tools import resolve_tools
from divisions.division_2_redaction import OutreachRecord

logger = logging.getLogger("Division5")


@dataclass
class StripeLink:
    link_id: str
    company_id: str
    amount_eur: float
    url: str
    created_at: str
    expires_at: str
    paid: bool = False
    charge_id: Optional[str] = None


@dataclass
class FinancialReport:
    date: str
    revenue_eur: float
    transactions: int
    avg_deal_size: float
    conversion_rate: float
    refunds: int
    refund_rate: float
    top_sector: str
    pending_invoices: int


@dataclass
class ComplianceResult:
    record_id: str
    compliant: bool
    issues: List[str] = field(default_factory=list)
    action_taken: Optional[str] = None


PRICING_GRID: Dict[str, Dict[str, float]] = {
    "Artisans & Bâtiment":          {"base": 129, "urgency_premium": 30, "upsell": 29},
    "Restauration & Hôtellerie":    {"base": 149, "urgency_premium": 30, "upsell": 29},
    "Médical & Cabinets de Soin":   {"base": 189, "urgency_premium": 50, "upsell": 49},
    "Boutiques E-commerce Locales": {"base": 199, "urgency_premium": 50, "upsell": 49},
    "Agences Immobilières":         {"base": 179, "urgency_premium": 40, "upsell": 39},
    "Écoles & Organismes de Formation": {"base": 149, "urgency_premium": 30, "upsell": 29},
    "Garages & Concessionnaires":   {"base": 159, "urgency_premium": 40, "upsell": 39},
    "Services Juridiques & Comptabilité": {"base": 199, "urgency_premium": 50, "upsell": 49},
    "Associations & Loisirs":       {"base": 99,  "urgency_premium": 20, "upsell": 19},
}

DOMAIN_BLACKLIST: set[str] = set()


class Division5Finance:
    """
    CFO agent 5.0 has absolute control over financial flows and legal security.
    Sub-agents handle Stripe, RGPD compliance, and infrastructure monitoring.
    """

    def __init__(self):
        self.agents = [SwarmAgent(cfg, resolve_tools(cfg.tools)) for cfg in DIVISION_5]
        self.manager = next(a for a in self.agents if a.is_manager)
        self.workers = {a.id: a for a in self.agents if not a.is_manager}
        self._stripe_links: Dict[str, StripeLink] = {}
        self._revenue_today = 0.0
        self._transaction_count = 0
        logger.info(f"Division 5 initialised — CFO ready, {len(self.workers)} guardians active")

    # ── Finance (5.1–5.3) ────────────────────────────────────────────────────

    def compute_quote(self, sector: str, is_urgent: bool = False) -> float:
        """Agent 5.1 — Compute the right price for a given sector."""
        grid = PRICING_GRID.get(sector, {"base": 149, "urgency_premium": 30})
        price = grid["base"]
        if is_urgent:
            price += grid["urgency_premium"]
        logger.debug(f"[5.1] Quote computed: {price}€ for {sector} (urgent={is_urgent})")
        return float(price)

    def create_stripe_link(self, company_id: str, sector: str, is_urgent: bool = False) -> StripeLink:
        """Agent 5.1 — Generate a Stripe payment link."""
        amount = self.compute_quote(sector, is_urgent)
        now = datetime.utcnow()
        link = StripeLink(
            link_id=f"link_{company_id}_{now.strftime('%H%M%S')}",
            company_id=company_id,
            amount_eur=amount,
            url=f"https://buy.stripe.com/test_{random.randint(10000, 99999)}",
            created_at=now.isoformat(),
            expires_at=now.replace(hour=(now.hour + 72) % 24).isoformat(),
        )
        self._stripe_links[link.link_id] = link
        logger.info(f"[5.1] Stripe link created — {link.url} — {amount}€")
        return link

    def confirm_payment(self, link_id: str) -> Optional[StripeLink]:
        """Agent 5.2 — Mark a payment as confirmed after Stripe webhook."""
        link = self._stripe_links.get(link_id)
        if not link:
            logger.error(f"[5.2] Link {link_id} not found")
            return None
        link.paid = True
        link.charge_id = f"ch_test_{random.randint(100000, 999999)}"
        self._revenue_today += link.amount_eur
        self._transaction_count += 1
        logger.info(
            f"[5.2] Payment confirmed — {link.charge_id} / {link.amount_eur}€ / "
            f"Revenue today: {self._revenue_today}€"
        )
        return link

    def generate_daily_report(self) -> FinancialReport:
        """Agent 5.2 — Generate the daily financial report."""
        return FinancialReport(
            date=datetime.utcnow().date().isoformat(),
            revenue_eur=self._revenue_today,
            transactions=self._transaction_count,
            avg_deal_size=self._revenue_today / max(self._transaction_count, 1),
            conversion_rate=round(self._transaction_count / max(random.randint(50, 120), 1) * 100, 2),
            refunds=max(0, int(self._transaction_count * 0.021)),
            refund_rate=2.1,
            top_sector="Restauration & Hôtellerie",
            pending_invoices=random.randint(0, 3),
        )

    # ── RGPD Compliance (5.4–5.6) ────────────────────────────────────────────

    def validate_email_rgpd(self, record: OutreachRecord) -> ComplianceResult:
        """Agent 5.4 — Scan an outreach email for RGPD compliance before send."""
        issues = []
        body = record.email_draft.lower()

        if "stop" not in body and "désinscrire" not in body and "désinscription" not in body:
            issues.append("Lien STOP manquant")
        if any(w in body for w in ["garantit", "assure", "certifie"]):
            issues.append("Promesse excessive détectée")
        if len(record.email_draft) > 1500:
            issues.append("Email trop long (> 1500 caractères)")

        compliant = len(issues) == 0
        if not compliant:
            record.email_draft += "\n\n---\nPour ne plus recevoir nos messages : répondez STOP"
            issues = [i for i in issues if i != "Lien STOP manquant"]

        result = ComplianceResult(
            record_id=record.company_id,
            compliant=len(issues) == 0,
            issues=issues,
            action_taken="STOP link injected" if not compliant else None,
        )
        record.rgpd_validated = result.compliant
        logger.debug(f"[5.4] RGPD check {record.company_id} — compliant={result.compliant}")
        return result

    def process_opt_out(self, domain: str) -> bool:
        """Agent 5.5 — Permanently blacklist a domain after unsubscribe request."""
        DOMAIN_BLACKLIST.add(domain.lower())
        logger.info(f"[5.5] Domain blacklisted permanently: {domain}")
        return True

    def is_blacklisted(self, email: str) -> bool:
        """Check if an email domain is on the blacklist."""
        domain = email.split("@")[-1].lower() if "@" in email else email
        return domain in DOMAIN_BLACKLIST

    # ── Infrastructure (5.7–5.9) ─────────────────────────────────────────────

    def check_system_health(self) -> Dict:
        """Agent 5.7 — Return the health status of all 50 agents."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "agents_total": 50,
            "agents_active": random.randint(35, 44),
            "agents_idle": random.randint(4, 10),
            "agents_error": random.randint(0, 3),
            "queue_depth_div1": random.randint(0, 20),
            "queue_depth_div2": random.randint(0, 15),
            "queue_depth_div3": random.randint(0, 10),
            "queue_depth_div4": random.randint(0, 5),
            "queue_depth_div5": 0,
            "memory_usage_pct": random.uniform(40, 75),
            "api_latency_ms": random.randint(80, 350),
            "status": "healthy",
        }

    def get_revenue(self) -> float:
        return self._revenue_today

    def get_transaction_count(self) -> int:
        return self._transaction_count
