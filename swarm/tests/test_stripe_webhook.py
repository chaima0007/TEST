"""
Tests for webhooks/stripe.py
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from webhooks.stripe import stripe_router, get_confirmed_payments, _confirmed_payments


# ── Test App Setup ────────────────────────────────────────────────────────────

def make_app() -> FastAPI:
    app = FastAPI()
    app.include_router(stripe_router, prefix="/webhooks")
    return app


def client() -> TestClient:
    return TestClient(make_app())


def payment_intent_payload(
    company_id: str = "co_001",
    amount_cents: int = 50000,
    charge_id: str = "pi_test_123",
) -> dict:
    return {
        "type": "payment_intent.succeeded",
        "data": {
            "object": {
                "id": charge_id,
                "amount": amount_cents,
                "metadata": {"company_id": company_id},
            }
        },
    }


def charge_payload(
    company_id: str = "co_002",
    amount_cents: int = 29900,
    charge_id: str = "ch_test_456",
) -> dict:
    return {
        "type": "charge.succeeded",
        "data": {
            "object": {
                "id": charge_id,
                "amount": amount_cents,
                "metadata": {"company_id": company_id},
            }
        },
    }


# ── No secret (dev mode) ──────────────────────────────────────────────────────

class TestDevModeNoSecret:
    def setup_method(self):
        _confirmed_payments.clear()

    def test_payment_intent_returns_200(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload()),
                headers={"content-type": "application/json"},
            )
        assert resp.status_code == 200

    def test_payment_intent_received_true(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload()),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["received"] is True

    def test_payment_intent_returns_company_id(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload(company_id="co_xyz")),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["company_id"] == "co_xyz"

    def test_payment_intent_returns_amount_in_euros(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload(amount_cents=50000)),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["amount_eur"] == 500.0

    def test_charge_succeeded_also_handled(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(charge_payload()),
                headers={"content-type": "application/json"},
            )
        assert resp.status_code == 200
        assert resp.json()["received"] is True

    def test_charge_returns_company_id(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(charge_payload(company_id="co_rest")),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["company_id"] == "co_rest"

    def test_charge_cents_converted_to_euros(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(charge_payload(amount_cents=29900)),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["amount_eur"] == pytest.approx(299.0)

    def test_unknown_event_type_acknowledged(self):
        payload = {"type": "customer.created", "data": {"object": {}}}
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payload),
                headers={"content-type": "application/json"},
            )
        assert resp.status_code == 200
        assert resp.json()["received"] is True
        assert resp.json()["event_type"] == "customer.created"

    def test_unknown_event_has_no_company_id(self):
        payload = {"type": "refund.created", "data": {"object": {}}}
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payload),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["company_id"] is None

    def test_event_type_echoed_in_response(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload()),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["event_type"] == "payment_intent.succeeded"


# ── _confirmed_payments store ─────────────────────────────────────────────────

class TestConfirmedPayments:
    def setup_method(self):
        _confirmed_payments.clear()

    def test_payment_stored_after_success(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload(charge_id="pi_abc")),
                headers={"content-type": "application/json"},
            )
        assert "pi_abc" in get_confirmed_payments()

    def test_stored_payment_has_company_id(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload(company_id="co_plmb", charge_id="pi_xyz")),
                headers={"content-type": "application/json"},
            )
        assert get_confirmed_payments()["pi_xyz"]["company_id"] == "co_plmb"

    def test_stored_payment_has_amount_eur(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload(amount_cents=100000, charge_id="pi_100")),
                headers={"content-type": "application/json"},
            )
        assert get_confirmed_payments()["pi_100"]["amount_eur"] == 1000.0

    def test_multiple_payments_all_stored(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            c = client()
            c.post("/webhooks/stripe", content=json.dumps(payment_intent_payload(charge_id="pi_1")), headers={"content-type": "application/json"})
            c.post("/webhooks/stripe", content=json.dumps(charge_payload(charge_id="ch_2")), headers={"content-type": "application/json"})
        confirmed = get_confirmed_payments()
        assert "pi_1" in confirmed
        assert "ch_2" in confirmed

    def test_unknown_event_not_stored(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            client().post(
                "/webhooks/stripe",
                content=json.dumps({"type": "customer.created", "data": {"object": {}}}),
                headers={"content-type": "application/json"},
            )
        assert len(get_confirmed_payments()) == 0

    def test_get_confirmed_payments_returns_dict(self):
        assert isinstance(get_confirmed_payments(), dict)


# ── Signature verification ────────────────────────────────────────────────────

class TestSignatureVerification:
    def setup_method(self):
        _confirmed_payments.clear()

    def test_invalid_signature_returns_400(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": "whsec_test"}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload()),
                headers={
                    "content-type": "application/json",
                    "stripe-signature": "invalid_sig",
                },
            )
        assert resp.status_code == 400

    def test_valid_signature_accepted(self):
        import time
        import hmac
        import hashlib

        secret = "whsec_testsecret"
        payload_bytes = json.dumps(payment_intent_payload()).encode()
        timestamp = str(int(time.time()))
        signed_payload = f"{timestamp}.{payload_bytes.decode()}"
        signature = hmac.new(
            secret.encode(), signed_payload.encode(), hashlib.sha256
        ).hexdigest()
        stripe_sig = f"t={timestamp},v1={signature}"

        mock_event = payment_intent_payload()

        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": secret}):
            with patch("stripe.Webhook.construct_event", return_value=mock_event):
                resp = client().post(
                    "/webhooks/stripe",
                    content=payload_bytes,
                    headers={
                        "content-type": "application/json",
                        "stripe-signature": stripe_sig,
                    },
                )
        assert resp.status_code == 200

    def test_missing_signature_header_falls_back_to_json_parse(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payment_intent_payload()),
                headers={"content-type": "application/json"},
            )
        assert resp.status_code == 200

    def test_no_secret_bypasses_stripe_verification(self):
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            with patch("stripe.Webhook.construct_event") as mock_verify:
                client().post(
                    "/webhooks/stripe",
                    content=json.dumps(payment_intent_payload()),
                    headers={"content-type": "application/json"},
                )
                mock_verify.assert_not_called()


# ── Missing metadata ──────────────────────────────────────────────────────────

class TestMissingMetadata:
    def setup_method(self):
        _confirmed_payments.clear()

    def test_payment_without_company_id_metadata(self):
        payload = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_no_meta",
                    "amount": 10000,
                    "metadata": {},
                }
            },
        }
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payload),
                headers={"content-type": "application/json"},
            )
        assert resp.status_code == 200
        assert resp.json()["company_id"] is None

    def test_payment_without_amount_defaults_to_zero(self):
        payload = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_no_amount",
                    "metadata": {"company_id": "co_1"},
                }
            },
        }
        with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}):
            resp = client().post(
                "/webhooks/stripe",
                content=json.dumps(payload),
                headers={"content-type": "application/json"},
            )
        assert resp.json()["amount_eur"] == 0.0
