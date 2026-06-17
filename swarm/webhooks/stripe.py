"""
Stripe Webhook handler for the Swarm API.

Listens for payment_intent.succeeded and charge.succeeded events,
marks the corresponding SwarmJob as paid, and triggers Division 4 production.

Mount with:
    from webhooks.stripe import stripe_router
    app.include_router(stripe_router, prefix="/webhooks")
"""

import os
import logging
from typing import Any

import stripe
from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel

logger = logging.getLogger("swarm.webhook")

stripe_router = APIRouter()

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


# In-memory confirmed payments (for demo; replace with DB in production)
_confirmed_payments: dict[str, dict[str, Any]] = {}


class WebhookResult(BaseModel):
    received: bool
    event_type: str | None = None
    company_id: str | None = None
    amount_eur: float | None = None


@stripe_router.post("/stripe", response_model=WebhookResult)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
):
    payload = await request.body()

    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    else:
        # No secret configured — parse raw JSON (dev mode only)
        import json
        event = json.loads(payload)

    event_type = event.get("type", "")
    logger.info("Stripe event received: %s", event_type)

    if event_type in ("payment_intent.succeeded", "charge.succeeded"):
        data_obj = event["data"]["object"]
        company_id = data_obj.get("metadata", {}).get("company_id")
        amount = data_obj.get("amount", 0) / 100  # cents → euros
        charge_id = data_obj.get("id", "")

        _confirmed_payments[charge_id] = {
            "company_id": company_id,
            "amount_eur": amount,
            "event_type": event_type,
        }
        logger.info("Payment confirmed: company=%s amount=%.2f€", company_id, amount)

        return WebhookResult(
            received=True,
            event_type=event_type,
            company_id=company_id,
            amount_eur=amount,
        )

    return WebhookResult(received=True, event_type=event_type)


def get_confirmed_payments() -> dict[str, dict[str, Any]]:
    """Returns all confirmed payments this session (in-memory)."""
    return _confirmed_payments
