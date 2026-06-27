"""
Division 3 — Relation & Négociation (10 agents)
Handles all inbound replies in real-time with sentiment-based routing.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from config import DIVISION_3
from agents.base import SwarmAgent
from agents.tools import resolve_tools
from intelligence.sentiment_router import SentimentRouter
from intelligence.reply_classifier import ReplyClassifier

logger = logging.getLogger("Division3")


@dataclass
class NegotiationMessage:
    role: str  # "agent" | "prospect"
    agent_id: str
    content: str
    timestamp: str


@dataclass
class NegotiationThread:
    company_id: str
    thread_id: str
    prospect_name: str
    sector: str
    sentiment: str
    assigned_negotiator: str
    messages: List[NegotiationMessage] = field(default_factory=list)
    quote_eur: Optional[float] = None
    stripe_link: Optional[str] = None
    payment_confirmed: bool = False
    closed: bool = False

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["messages"] = [m.__dict__ for m in self.messages]
        return d


SENTIMENT_ROUTING: Dict[str, str] = {
    "Positif": "3.5",
    "Curieux": "3.5",
    "Enthousiaste": "3.4",
    "Perdu": "3.4",
    "Sceptique": "3.1",
    "Méfiant": "3.2",
    "Négatif": "3.3",
    "Urgent": "3.5",
    "Fantôme": "3.7",
    "Fantôme_J10": "3.8",
    "Fantôme_J21": "3.9",
}


class Division3Negotiation:
    """
    Manager 3.0 monitors inbound email and routes each reply to the
    most suitable negotiator based on sentiment analysis.
    """

    def __init__(self):
        self.agents = [SwarmAgent(cfg, resolve_tools(cfg.tools)) for cfg in DIVISION_3]
        self.manager = next(a for a in self.agents if a.is_manager)
        self.negotiators = {a.id: a for a in self.agents if not a.is_manager}
        self.sentiment_router = SentimentRouter()
        self.reply_classifier = ReplyClassifier()
        logger.info(f"Division 3 initialised — {len(self.negotiators)} negotiators ready")

    def route(self, sentiment: str) -> SwarmAgent:
        """Route an inbound reply to the appropriate negotiator."""
        target_id = SENTIMENT_ROUTING.get(sentiment, "3.5")
        return self.negotiators.get(target_id, self.negotiators["3.5"])

    def classify_reply(self, text: str):
        """Classify a prospect reply for objection type, timeline, and buying signal."""
        return self.reply_classifier.classify(text)

    def analyze_and_open_thread(
        self,
        company_id: str,
        prospect_name: str,
        sector: str,
        initial_message: str,
    ) -> NegotiationThread:
        """Analyze raw prospect text, detect sentiment, then open a routed thread."""
        result = self.sentiment_router.analyze(initial_message)
        logger.info(
            f"[Div3] Sentiment detected: {result.sentiment} "
            f"(confidence={result.confidence:.2f}, keywords={result.keywords_matched})"
        )
        return self.open_thread(
            company_id=company_id,
            prospect_name=prospect_name,
            sector=sector,
            initial_message=initial_message,
            sentiment=result.sentiment,
        )

    def open_thread(
        self,
        company_id: str,
        prospect_name: str,
        sector: str,
        initial_message: str,
        sentiment: str,
    ) -> NegotiationThread:
        """Create a new negotiation thread for an inbound reply."""
        import datetime
        negotiator = self.route(sentiment)
        thread = NegotiationThread(
            company_id=company_id,
            thread_id=f"thread_{company_id}_{datetime.datetime.utcnow().strftime('%H%M%S')}",
            prospect_name=prospect_name,
            sector=sector,
            sentiment=sentiment,
            assigned_negotiator=negotiator.id,
            messages=[
                NegotiationMessage(
                    role="prospect",
                    agent_id="prospect",
                    content=initial_message,
                    timestamp=datetime.datetime.utcnow().isoformat(),
                )
            ],
        )
        logger.info(
            f"[Div3] Thread {thread.thread_id} opened — "
            f"Sentiment: {sentiment} → Negotiator: {negotiator.id}"
        )
        return thread

    def generate_response(self, thread: NegotiationThread, quote_eur: Optional[float] = None) -> str:
        """Generate a negotiator response for a thread."""
        import datetime

        negotiator = self.negotiators.get(thread.assigned_negotiator, list(self.negotiators.values())[0])
        last_prospect_msg = next(
            (m.content for m in reversed(thread.messages) if m.role == "prospect"), ""
        )

        responses = {
            "3.5": (
                f"Bonjour {thread.prospect_name},\n\n"
                f"Je comprends tout à fait votre situation. Pour un site dans le secteur "
                f"{thread.sector}, chaque seconde perdue représente environ 7 % de visiteurs "
                f"mobiles qui repartent. Nous intervenons en moins de 4 heures avec une "
                f"garantie satisfait-ou-remboursé 30 jours.\n\n"
                + (f"Je vous propose un lien de paiement sécurisé à {quote_eur}€ : "
                   f"{thread.stripe_link}" if thread.stripe_link else
                   "Souhaitez-vous que je vous envoie un devis rapide ?")
            ),
            "3.1": (
                f"Bonjour {thread.prospect_name},\n\n"
                f"Je comprends votre scepticisme — vous avez raison d'être prudent. "
                f"Voici 3 cas clients similaires dans le secteur {thread.sector} qui ont "
                f"constaté une hausse de 28 % de leurs demandes mobiles après intervention. "
                f"Une démo gratuite de 10 minutes vous convaincra mieux que n'importe quel argument."
            ),
            "3.7": (
                f"Bonjour {thread.prospect_name},\n\n"
                f"Je reviens vers vous car votre site a encore une vitesse de chargement "
                f"critique. Y a-t-il une question à laquelle je n'ai pas répondu ?"
            ),
        }

        reply = responses.get(thread.assigned_negotiator, responses["3.5"])
        thread.messages.append(NegotiationMessage(
            role="agent",
            agent_id=thread.assigned_negotiator,
            content=reply,
            timestamp=datetime.datetime.utcnow().isoformat(),
        ))
        return reply

    def confirm_payment(self, thread: NegotiationThread, amount_eur: float) -> NegotiationThread:
        """Mark a thread as payment confirmed and trigger Division 4."""
        thread.payment_confirmed = True
        thread.quote_eur = amount_eur
        thread.closed = True
        logger.info(
            f"[Div3] Payment confirmed — {thread.company_id} / {amount_eur}€ / "
            f"Thread {thread.thread_id}"
        )
        return thread
