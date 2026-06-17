"""
Tests for intelligence/prospect_memory.py
"""

import datetime
import pytest
from intelligence.prospect_memory import (
    ProspectMemory, ProspectRecord, Message, SentimentSnapshot,
    MessageDirection, DealStage,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def mem() -> ProspectMemory:
    m = ProspectMemory()
    m.reset()
    return m


def make_record(pid="p001", company="Acme SARL", sector="artisan", email="contact@acme.fr") -> ProspectRecord:
    return ProspectRecord(
        prospect_id=pid,
        company_name=company,
        sector=sector,
        email=email,
    )


NOW   = datetime.datetime(2026, 2, 1, 10, 0, 0)
PAST3 = NOW - datetime.timedelta(days=3)
PAST8 = NOW - datetime.timedelta(days=8)


# ── DealStage ─────────────────────────────────────────────────────────────────

class TestDealStage:
    def test_detected_is_default(self):
        assert make_record().stage == DealStage.DETECTED

    def test_stage_values_are_strings(self):
        for s in DealStage:
            assert isinstance(s.value, str)


# ── Message ───────────────────────────────────────────────────────────────────

class TestMessage:
    def _msg(self):
        return Message(
            direction=MessageDirection.OUTBOUND,
            content="Bonjour, nous avons analysé votre site...",
            timestamp=NOW,
            agent_id="2.1",
            sentiment="neutre",
            objection_type="none",
        )

    def test_to_dict_keys(self):
        d = self._msg().to_dict()
        for key in ("direction", "content", "timestamp", "agent_id", "sentiment", "objection_type"):
            assert key in d

    def test_direction_value_is_string(self):
        assert self._msg().to_dict()["direction"] == "outbound"

    def test_content_truncated_to_500(self):
        long_content = "x" * 600
        msg = Message(MessageDirection.INBOUND, long_content, NOW)
        assert len(msg.to_dict()["content"]) == 500


# ── SentimentSnapshot ─────────────────────────────────────────────────────────

class TestSentimentSnapshot:
    def test_to_dict_keys(self):
        s = SentimentSnapshot("positif", 0.8, NOW)
        d = s.to_dict()
        for key in ("sentiment", "score", "timestamp"):
            assert key in d

    def test_score_rounded(self):
        s = SentimentSnapshot("neutre", 0.55555, NOW)
        assert s.to_dict()["score"] == pytest.approx(0.556, abs=0.001)


# ── ProspectRecord — basic ────────────────────────────────────────────────────

class TestProspectRecordBasic:
    def test_initial_stage_detected(self):
        assert make_record().stage == DealStage.DETECTED

    def test_touch_count_zero_initially(self):
        assert make_record().touch_count == 0

    def test_reply_count_zero_initially(self):
        assert make_record().reply_count == 0

    def test_latest_sentiment_none_initially(self):
        assert make_record().latest_sentiment is None

    def test_sentiment_trend_unknown_initially(self):
        assert make_record().sentiment_trend == "unknown"

    def test_days_since_contact_none_when_not_contacted(self):
        assert make_record().days_since_contact is None

    def test_to_dict_has_required_keys(self):
        d = make_record().to_dict()
        for key in ("prospect_id", "company_name", "sector", "email", "stage",
                    "touch_count", "reply_count", "latest_sentiment",
                    "sentiment_trend", "objections_seen", "message_count"):
            assert key in d

    def test_to_dict_messages_limited_to_5(self):
        r = make_record()
        for i in range(8):
            r.add_message(MessageDirection.OUTBOUND, f"msg {i}", timestamp=NOW)
        assert len(r.to_dict()["messages"]) == 5

    def test_summary_returns_string(self):
        assert isinstance(make_record().summary(), str)

    def test_summary_contains_company(self):
        assert "Acme SARL" in make_record().summary()


# ── ProspectRecord — add_message ──────────────────────────────────────────────

class TestAddMessage:
    def test_outbound_increments_touch_count(self):
        r = make_record()
        r.add_message(MessageDirection.OUTBOUND, "Hello", timestamp=NOW)
        assert r.touch_count == 1

    def test_inbound_increments_reply_count(self):
        r = make_record()
        r.add_message(MessageDirection.INBOUND, "Merci", timestamp=NOW)
        assert r.reply_count == 1

    def test_returns_message_object(self):
        r = make_record()
        msg = r.add_message(MessageDirection.OUTBOUND, "Hi", timestamp=NOW)
        assert isinstance(msg, Message)

    def test_last_contacted_updated_on_outbound(self):
        r = make_record()
        r.add_message(MessageDirection.OUTBOUND, "Hi", timestamp=NOW)
        assert r.last_contacted_at == NOW

    def test_last_contacted_not_updated_on_inbound(self):
        r = make_record()
        r.last_contacted_at = PAST3
        r.add_message(MessageDirection.INBOUND, "Réponse", timestamp=NOW)
        assert r.last_contacted_at == PAST3

    def test_objection_added_to_seen_list(self):
        r = make_record()
        r.add_message(MessageDirection.INBOUND, "c'est trop cher", objection_type="price", timestamp=NOW)
        assert "price" in r.objections_seen

    def test_duplicate_objection_not_added_twice(self):
        r = make_record()
        r.add_message(MessageDirection.INBOUND, "cher", objection_type="price", timestamp=NOW)
        r.add_message(MessageDirection.INBOUND, "toujours cher", objection_type="price", timestamp=NOW)
        assert r.objections_seen.count("price") == 1

    def test_empty_objection_not_added(self):
        r = make_record()
        r.add_message(MessageDirection.INBOUND, "ok", objection_type="", timestamp=NOW)
        assert r.objections_seen == []

    def test_none_objection_not_added(self):
        r = make_record()
        r.add_message(MessageDirection.INBOUND, "super", objection_type="none", timestamp=NOW)
        assert r.objections_seen == []


# ── ProspectRecord — sentiment ────────────────────────────────────────────────

class TestSentiment:
    def test_record_sentiment_stored(self):
        r = make_record()
        r.record_sentiment("positif", 0.8, NOW)
        assert r.latest_sentiment == "positif"

    def test_latest_sentiment_is_most_recent(self):
        r = make_record()
        r.record_sentiment("négatif", 0.2, PAST3)
        r.record_sentiment("positif", 0.9, NOW)
        assert r.latest_sentiment == "positif"

    def test_sentiment_clamped_to_0_1(self):
        r = make_record()
        r.record_sentiment("positif", 1.5, NOW)
        assert r.sentiment_history[-1].score == 1.0

    def test_sentiment_trend_improving(self):
        r = make_record()
        r.record_sentiment("négatif", 0.2, PAST3)
        r.record_sentiment("positif", 0.9, NOW)
        assert r.sentiment_trend == "improving"

    def test_sentiment_trend_declining(self):
        r = make_record()
        r.record_sentiment("positif", 0.9, PAST3)
        r.record_sentiment("négatif", 0.2, NOW)
        assert r.sentiment_trend == "declining"

    def test_sentiment_trend_stable(self):
        r = make_record()
        r.record_sentiment("neutre", 0.5, PAST3)
        r.record_sentiment("neutre", 0.52, NOW)
        assert r.sentiment_trend == "stable"


# ── ProspectRecord — stage & tags ────────────────────────────────────────────

class TestStageAndTags:
    def test_advance_stage(self):
        r = make_record()
        r.advance_stage(DealStage.NEGOTIATING)
        assert r.stage == DealStage.NEGOTIATING

    def test_add_tag(self):
        r = make_record()
        r.add_tag("urgent")
        assert "urgent" in r.tags

    def test_duplicate_tag_not_added(self):
        r = make_record()
        r.add_tag("hot")
        r.add_tag("hot")
        assert r.tags.count("hot") == 1


# ── ProspectMemory — get_or_create ────────────────────────────────────────────

class TestGetOrCreate:
    def test_creates_new_record(self):
        m = mem()
        rec = m.get_or_create("p1", "Acme", "artisan", "a@a.fr")
        assert rec.prospect_id == "p1"

    def test_returns_existing_record(self):
        m = mem()
        r1 = m.get_or_create("p1", "Acme", "artisan", "a@a.fr")
        r2 = m.get_or_create("p1")
        assert r1 is r2

    def test_get_returns_record(self):
        m = mem()
        m.get_or_create("p1", "Acme", "artisan", "a@a.fr")
        assert m.get("p1") is not None

    def test_get_unknown_returns_none(self):
        assert mem().get("missing") is None

    def test_count_increments(self):
        m = mem()
        m.get_or_create("p1")
        m.get_or_create("p2")
        assert m.count() == 2

    def test_upsert_replaces(self):
        m = mem()
        r = make_record("p1")
        m.upsert(r)
        assert m.get("p1") is r

    def test_delete_returns_true(self):
        m = mem()
        m.get_or_create("p1")
        assert m.delete("p1") is True

    def test_delete_unknown_returns_false(self):
        assert mem().delete("ghost") is False


# ── ProspectMemory — log helpers ──────────────────────────────────────────────

class TestLogHelpers:
    def test_log_outbound_advances_to_contacted(self):
        m = mem()
        m.log_outbound("p1", "Bonjour", company_name="X", sector="s", email="x@x.fr")
        assert m.get("p1").stage == DealStage.CONTACTED

    def test_log_outbound_touch_count(self):
        m = mem()
        m.log_outbound("p1", "msg1", email="a@a.fr")
        m.log_outbound("p1", "msg2")
        assert m.get("p1").touch_count == 2

    def test_log_inbound_advances_to_replied(self):
        m = mem()
        m.get_or_create("p1")
        m.log_inbound("p1", "Merci de votre email")
        assert m.get("p1").stage == DealStage.REPLIED

    def test_log_inbound_records_sentiment(self):
        m = mem()
        m.get_or_create("p1")
        m.log_inbound("p1", "Intéressant", sentiment="positif", sentiment_score=0.8)
        assert m.get("p1").latest_sentiment == "positif"


# ── ProspectMemory — queries ──────────────────────────────────────────────────

class TestQueries:
    def _setup(self):
        m = mem()
        r1 = m.get_or_create("p1", "A", "artisan", "a@a.fr")
        r1.advance_stage(DealStage.NEGOTIATING)
        r1.assigned_agent = "2.1"
        r1.add_tag("hot")

        r2 = m.get_or_create("p2", "B", "restaurant", "b@b.fr")
        r2.advance_stage(DealStage.WON)
        r2.quote_eur = 1200.0

        r3 = m.get_or_create("p3", "C", "artisan", "c@c.fr")
        r3.advance_stage(DealStage.CONTACTED)
        r3.last_contacted_at = datetime.datetime.utcnow() - datetime.timedelta(days=10)
        r3.add_message(MessageDirection.INBOUND, "cher", objection_type="price",
                       timestamp=datetime.datetime.utcnow())

        return m

    def test_by_stage(self):
        m = self._setup()
        assert len(m.by_stage(DealStage.WON)) == 1

    def test_by_sector(self):
        m = self._setup()
        assert len(m.by_sector("artisan")) == 2

    def test_by_agent(self):
        m = self._setup()
        assert len(m.by_agent("2.1")) == 1

    def test_with_objection(self):
        m = self._setup()
        assert len(m.with_objection("price")) == 1

    def test_cold_prospects(self):
        m = self._setup()
        cold = m.cold_prospects(idle_days=7.0)
        assert any(r.prospect_id == "p3" for r in cold)

    def test_won_deals(self):
        m = self._setup()
        assert len(m.won_deals()) == 1

    def test_active_negotiations(self):
        m = self._setup()
        active = m.active_negotiations()
        assert any(r.prospect_id == "p1" for r in active)

    def test_top_by_reply_count(self):
        m = self._setup()
        m.get("p1").add_message(MessageDirection.INBOUND, "r1", timestamp=NOW)
        m.get("p1").add_message(MessageDirection.INBOUND, "r2", timestamp=NOW)
        top = m.top_by_reply_count(n=1)
        assert top[0].prospect_id == "p1"

    def test_all_records_count(self):
        m = self._setup()
        assert len(m.all_records()) == 3


# ── ProspectMemory — summary ──────────────────────────────────────────────────

class TestSummary:
    def test_summary_keys(self):
        s = mem().summary()
        for key in ("total_prospects", "by_stage", "active_negotiations",
                    "won_deals", "total_won_revenue_eur", "total_messages", "avg_touches"):
            assert key in s

    def test_total_prospects_zero(self):
        assert mem().summary()["total_prospects"] == 0

    def test_won_revenue_sums_correctly(self):
        m = mem()
        r = m.get_or_create("p1", "X", "s", "x@x.fr")
        r.advance_stage(DealStage.WON)
        r.quote_eur = 2000.0
        r2 = m.get_or_create("p2", "Y", "s", "y@y.fr")
        r2.advance_stage(DealStage.WON)
        r2.quote_eur = 1500.0
        assert m.summary()["total_won_revenue_eur"] == pytest.approx(3500.0)

    def test_avg_touches_calculation(self):
        m = mem()
        r = m.get_or_create("p1")
        r.add_message(MessageDirection.OUTBOUND, "a", timestamp=NOW)
        r.add_message(MessageDirection.OUTBOUND, "b", timestamp=NOW)
        assert m.summary()["avg_touches"] == pytest.approx(2.0)


# ── ProspectMemory — reset ────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_all(self):
        m = mem()
        m.get_or_create("p1")
        m.reset()
        assert m.count() == 0

    def test_reset_allows_fresh_start(self):
        m = mem()
        m.get_or_create("p1")
        m.reset()
        m.get_or_create("p2")
        assert m.count() == 1
