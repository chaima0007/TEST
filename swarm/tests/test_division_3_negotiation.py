"""
Tests for Division 3 — Relation & Négociation.
"""

import pytest
from divisions.division_3_negotiation import (
    Division3Negotiation,
    NegotiationThread,
    NegotiationMessage,
    SENTIMENT_ROUTING,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_thread(
    company_id: str = "co_001",
    prospect_name: str = "Jean-Paul Martin",
    sector: str = "plomberie",
    sentiment: str = "Positif",
    initial_message: str = "Je suis intéressé par vos services.",
) -> NegotiationThread:
    d = Division3Negotiation()
    return d.open_thread(
        company_id=company_id,
        prospect_name=prospect_name,
        sector=sector,
        initial_message=initial_message,
        sentiment=sentiment,
    )


# ── Initialisation ────────────────────────────────────────────────────────────

class TestDivision3Init:
    def test_has_sentiment_router(self):
        d = Division3Negotiation()
        assert d.sentiment_router is not None

    def test_has_manager(self):
        d = Division3Negotiation()
        assert d.manager is not None
        assert d.manager.is_manager is True

    def test_manager_is_3_0(self):
        d = Division3Negotiation()
        assert d.manager.id == "3.0"

    def test_has_nine_negotiators(self):
        d = Division3Negotiation()
        assert len(d.negotiators) == 9


# ── Sentiment routing ─────────────────────────────────────────────────────────

class TestSentimentRouting:
    def test_route_positif_returns_3_5(self):
        d = Division3Negotiation()
        agent = d.route("Positif")
        assert agent.id == "3.5"

    def test_route_curieux_returns_3_5(self):
        d = Division3Negotiation()
        assert d.route("Curieux").id == "3.5"

    def test_route_sceptique_returns_3_1(self):
        d = Division3Negotiation()
        assert d.route("Sceptique").id == "3.1"

    def test_route_mefiant_returns_3_2(self):
        d = Division3Negotiation()
        assert d.route("Méfiant").id == "3.2"

    def test_route_negatif_returns_3_3(self):
        d = Division3Negotiation()
        assert d.route("Négatif").id == "3.3"

    def test_route_fantome_returns_3_7(self):
        d = Division3Negotiation()
        assert d.route("Fantôme").id == "3.7"

    def test_route_unknown_defaults_to_3_5(self):
        d = Division3Negotiation()
        assert d.route("__UNKNOWN__").id == "3.5"


# ── open_thread ───────────────────────────────────────────────────────────────

class TestOpenThread:
    def test_returns_negotiation_thread(self):
        thread = make_thread()
        assert isinstance(thread, NegotiationThread)

    def test_thread_has_correct_company_id(self):
        thread = make_thread(company_id="xyz_42")
        assert thread.company_id == "xyz_42"

    def test_thread_has_initial_prospect_message(self):
        thread = make_thread(initial_message="Je veux en savoir plus.")
        assert len(thread.messages) == 1
        assert thread.messages[0].role == "prospect"
        assert "plus" in thread.messages[0].content

    def test_assigned_negotiator_matches_sentiment(self):
        d = Division3Negotiation()
        thread = d.open_thread("c1", "Marie", "coiffure", "Message", "Sceptique")
        assert thread.assigned_negotiator == "3.1"

    def test_thread_id_contains_company_id(self):
        thread = make_thread(company_id="co_abc")
        assert "co_abc" in thread.thread_id

    def test_thread_not_closed_initially(self):
        thread = make_thread()
        assert thread.closed is False
        assert thread.payment_confirmed is False


# ── analyze_and_open_thread ───────────────────────────────────────────────────

class TestAnalyzeAndOpenThread:
    def test_positive_text_routes_correctly(self):
        d = Division3Negotiation()
        thread = d.analyze_and_open_thread(
            "co_p1", "Paul", "restauration",
            "Oui je suis intéressé, quand peut-on commencer ?"
        )
        assert thread.assigned_negotiator in {"3.4", "3.5"}

    def test_skeptical_text_routes_to_3_1(self):
        d = Division3Negotiation()
        thread = d.analyze_and_open_thread(
            "co_s1", "Sophie", "e-commerce",
            "Vous avez des preuves de résultats ? Je ne suis pas convaincu."
        )
        assert thread.assigned_negotiator == "3.1"

    def test_suspicious_text_routes_to_3_2(self):
        d = Division3Negotiation()
        thread = d.analyze_and_open_thread(
            "co_m1", "Marc", "boulangerie",
            "C'est une arnaque ! Stop, je n'ai jamais demandé ce spam."
        )
        assert thread.assigned_negotiator == "3.2"

    def test_empty_text_routes_to_fantome(self):
        d = Division3Negotiation()
        thread = d.analyze_and_open_thread("co_ghost", "Ghost", "sector", "")
        assert thread.assigned_negotiator == "3.7"

    def test_initial_message_preserved_in_thread(self):
        d = Division3Negotiation()
        msg = "Je voudrais comprendre comment fonctionne votre service."
        thread = d.analyze_and_open_thread("co_x", "Alice", "retail", msg)
        assert thread.messages[0].content == msg


# ── generate_response ─────────────────────────────────────────────────────────

class TestGenerateResponse:
    def test_returns_non_empty_string(self):
        d = Division3Negotiation()
        thread = make_thread()
        reply = d.generate_response(thread)
        assert isinstance(reply, str) and len(reply) > 10

    def test_appends_agent_message_to_thread(self):
        d = Division3Negotiation()
        thread = make_thread()
        initial_len = len(thread.messages)
        d.generate_response(thread)
        assert len(thread.messages) == initial_len + 1
        assert thread.messages[-1].role == "agent"

    def test_response_mentions_prospect_name(self):
        d = Division3Negotiation()
        thread = make_thread(prospect_name="Monsieur Dupont")
        reply = d.generate_response(thread)
        assert "Dupont" in reply

    def test_ghost_response_is_a_relance(self):
        d = Division3Negotiation()
        thread = make_thread(sentiment="Fantôme")
        thread.assigned_negotiator = "3.7"
        reply = d.generate_response(thread)
        assert len(reply) > 10


# ── confirm_payment ───────────────────────────────────────────────────────────

class TestConfirmPayment:
    def test_marks_thread_as_closed(self):
        d = Division3Negotiation()
        thread = make_thread()
        d.confirm_payment(thread, 490.0)
        assert thread.closed is True

    def test_marks_payment_confirmed(self):
        d = Division3Negotiation()
        thread = make_thread()
        d.confirm_payment(thread, 490.0)
        assert thread.payment_confirmed is True

    def test_sets_quote_eur(self):
        d = Division3Negotiation()
        thread = make_thread()
        d.confirm_payment(thread, 750.0)
        assert thread.quote_eur == 750.0
