"""
Tests for intelligence/email_tracker.py
"""

import pytest
from intelligence.email_tracker import EmailTracker, CampaignMetrics, TrackingEvent


# ── Helpers ───────────────────────────────────────────────────────────────────

def tracker() -> EmailTracker:
    return EmailTracker()


def seed(t: EmailTracker, campaign_id="c1", agent_id="2.1", sector="restaurant",
         sent=10, opens=5, clicks=2, replies=1):
    for i in range(sent):
        t.track(campaign_id, f"e{i}", agent_id, sector, "sent")
    for i in range(opens):
        t.track(campaign_id, f"e{i}", agent_id, sector, "open")
    for i in range(clicks):
        t.track(campaign_id, f"e{i}", agent_id, sector, "click")
    for i in range(replies):
        t.track(campaign_id, f"e{i}", agent_id, sector, "reply")
    return t


# ── track() ───────────────────────────────────────────────────────────────────

class TestTrack:
    def test_returns_tracking_event(self):
        t = tracker()
        ev = t.track("c1", "e1", "2.1", "restaurant", "sent")
        assert isinstance(ev, TrackingEvent)

    def test_event_fields_populated(self):
        t = tracker()
        ev = t.track("c1", "e1", "2.1", "restaurant", "sent", {"key": "val"})
        assert ev.campaign_id == "c1"
        assert ev.email_id == "e1"
        assert ev.agent_id == "2.1"
        assert ev.sector == "restaurant"
        assert ev.event_type == "sent"
        assert ev.metadata == {"key": "val"}

    def test_event_id_is_16_chars(self):
        ev = tracker().track("c1", "e1", "2.1", "r", "sent")
        assert len(ev.event_id) == 16

    def test_timestamp_set(self):
        import time
        before = time.time()
        ev = tracker().track("c1", "e1", "2.1", "r", "sent")
        assert ev.timestamp >= before

    def test_invalid_event_type_raises(self):
        with pytest.raises(ValueError):
            tracker().track("c1", "e1", "2.1", "r", "bounced")

    def test_all_valid_event_types_accepted(self):
        t = tracker()
        for ev_type in ("sent", "open", "click", "reply", "unsubscribe"):
            t.track("c1", "e1", "2.1", "r", ev_type)

    def test_events_accumulate(self):
        t = tracker()
        t.track("c1", "e1", "2.1", "r", "sent")
        t.track("c1", "e2", "2.1", "r", "sent")
        assert len(t.get_events("c1")) == 2


# ── metrics ───────────────────────────────────────────────────────────────────

class TestMetrics:
    def test_get_metrics_returns_campaign_metrics(self):
        t = seed(tracker())
        m = t.get_metrics("c1")
        assert isinstance(m, CampaignMetrics)

    def test_get_metrics_none_for_unknown(self):
        assert tracker().get_metrics("unknown") is None

    def test_sent_count_correct(self):
        t = seed(tracker(), sent=7)
        assert t.get_metrics("c1").sent == 7

    def test_opens_count_correct(self):
        t = seed(tracker(), sent=10, opens=4)
        assert t.get_metrics("c1").opens == 4

    def test_clicks_count_correct(self):
        t = seed(tracker(), sent=10, opens=5, clicks=3, replies=0)
        assert t.get_metrics("c1").clicks == 3

    def test_replies_count_correct(self):
        t = seed(tracker(), sent=10, replies=2)
        assert t.get_metrics("c1").replies == 2

    def test_unsubscribes_tracked(self):
        t = tracker()
        t.track("c1", "e1", "2.1", "r", "sent")
        t.track("c1", "e1", "2.1", "r", "unsubscribe")
        assert t.get_metrics("c1").unsubscribes == 1

    def test_open_rate_calculation(self):
        t = seed(tracker(), sent=10, opens=5)
        assert t.get_metrics("c1").open_rate == 0.5

    def test_click_rate_calculation(self):
        t = seed(tracker(), sent=10, clicks=2, opens=0, replies=0)
        assert t.get_metrics("c1").click_rate == 0.2

    def test_reply_rate_calculation(self):
        t = seed(tracker(), sent=10, replies=1, opens=0, clicks=0)
        assert t.get_metrics("c1").reply_rate == 0.1

    def test_zero_sent_rates_are_zero(self):
        m = CampaignMetrics("c", "2.1", "r")
        assert m.open_rate == 0.0
        assert m.click_rate == 0.0
        assert m.reply_rate == 0.0

    def test_conversion_score_reply_weighted_most(self):
        m = CampaignMetrics("c", "2.1", "r", sent=100, opens=0, clicks=0, replies=100)
        assert m.conversion_score == pytest.approx(0.60, abs=0.001)

    def test_conversion_score_zero_when_no_engagement(self):
        m = CampaignMetrics("c", "2.1", "r", sent=100)
        assert m.conversion_score == 0.0

    def test_to_dict_has_all_rate_keys(self):
        t = seed(tracker())
        d = t.get_metrics("c1").to_dict()
        for key in ("open_rate", "click_rate", "reply_rate", "conversion_score"):
            assert key in d


# ── agent / sector queries ────────────────────────────────────────────────────

class TestQueries:
    def test_get_agent_metrics_filters_correctly(self):
        t = seed(tracker(), campaign_id="c1", agent_id="2.1")
        seed(t, campaign_id="c2", agent_id="2.3", sector="plombier")
        results = t.get_agent_metrics("2.1")
        assert all(m.agent_id == "2.1" for m in results)
        assert len(results) == 1

    def test_get_sector_metrics_case_insensitive(self):
        t = seed(tracker(), sector="Restaurant")
        results = t.get_sector_metrics("restaurant")
        assert len(results) == 1

    def test_get_events_all_when_no_filter(self):
        t = seed(tracker(), sent=3, opens=0, clicks=0, replies=0)
        assert len(t.get_events()) == 3

    def test_get_events_filtered_by_campaign(self):
        t = seed(tracker(), campaign_id="c1", sent=3, opens=0, clicks=0, replies=0)
        seed(t, campaign_id="c2", sent=5, opens=0, clicks=0, replies=0)
        assert len(t.get_events("c1")) == 3
        assert len(t.get_events("c2")) == 5

    def test_top_campaigns_sorted_by_conversion(self):
        t = seed(tracker(), campaign_id="c1", sent=10, opens=1, clicks=0, replies=0)
        seed(t, campaign_id="c2", sent=10, opens=10, clicks=5, replies=5)
        top = t.top_campaigns(n=2)
        assert top[0].campaign_id == "c2"

    def test_top_campaigns_respects_n(self):
        t = tracker()
        for i in range(5):
            seed(t, campaign_id=f"c{i}", agent_id="2.1")
        top = t.top_campaigns(n=3)
        assert len(top) == 3


# ── agent_leaderboard ─────────────────────────────────────────────────────────

class TestLeaderboard:
    def test_leaderboard_returns_list(self):
        t = seed(tracker())
        lb = t.agent_leaderboard()
        assert isinstance(lb, list)

    def test_leaderboard_has_agent_ids(self):
        t = seed(tracker(), agent_id="2.1")
        seed(t, campaign_id="c2", agent_id="2.3")
        agent_ids = {row["agent_id"] for row in t.agent_leaderboard()}
        assert "2.1" in agent_ids
        assert "2.3" in agent_ids

    def test_leaderboard_sorted_by_conversion_desc(self):
        t = seed(tracker(), campaign_id="c1", agent_id="2.1", sent=10, replies=0)
        seed(t, campaign_id="c2", agent_id="2.5", sent=10, replies=5)
        lb = t.agent_leaderboard()
        scores = [row["conversion_score"] for row in lb]
        assert scores == sorted(scores, reverse=True)

    def test_leaderboard_aggregates_multiple_campaigns(self):
        t = seed(tracker(), campaign_id="c1", agent_id="2.1", sent=10)
        seed(t, campaign_id="c2", agent_id="2.1", sent=5)
        lb = t.agent_leaderboard()
        row = next(r for r in lb if r["agent_id"] == "2.1")
        assert row["total_sent"] == 15
        assert row["campaigns"] == 2


# ── pixel / tracked link ──────────────────────────────────────────────────────

class TestPixelAndLink:
    def test_tracking_pixel_url_contains_ids(self):
        t = tracker()
        url = t.tracking_pixel_url("https://swarm.io", "c1", "e42")
        assert "c1" in url
        assert "e42" in url
        assert "/track/open" in url

    def test_tracked_link_contains_destination(self):
        t = tracker()
        url = t.tracked_link("https://swarm.io", "c1", "e1", "https://client.fr")
        assert "client.fr" in url
        assert "/track/click" in url

    def test_tracked_link_contains_ids(self):
        t = tracker()
        url = t.tracked_link("https://swarm.io", "c1", "e1", "https://x.fr")
        assert "c1" in url
        assert "e1" in url


# ── summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_empty_tracker(self):
        s = tracker().summary()
        assert s["campaigns"] == 0
        assert s["emails_sent"] == 0

    def test_summary_counts_correctly(self):
        t = seed(tracker(), sent=10, opens=5, replies=2)
        s = t.summary()
        assert s["emails_sent"] == 10
        assert s["total_opens"] == 5
        assert s["total_replies"] == 2

    def test_summary_open_rate_correct(self):
        t = seed(tracker(), sent=10, opens=4, clicks=0, replies=0)
        s = t.summary()
        assert s["open_rate"] == pytest.approx(0.4, abs=0.001)


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_events(self):
        t = seed(tracker())
        t.reset()
        assert t.get_events() == []

    def test_reset_clears_metrics(self):
        t = seed(tracker())
        t.reset()
        assert t.get_metrics("c1") is None

    def test_reset_allows_fresh_tracking(self):
        t = seed(tracker(), sent=5)
        t.reset()
        seed(t, sent=3)
        assert t.get_metrics("c1").sent == 3
