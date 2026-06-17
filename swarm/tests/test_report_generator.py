"""
Tests for exporters/report_generator.py
"""

import datetime
import pytest
from exporters.report_generator import ReportGenerator, CycleReport, DivisionReport


# ── Helpers ───────────────────────────────────────────────────────────────────

def gen() -> ReportGenerator:
    g = ReportGenerator()
    g.reset()
    return g


def make_div(division=1, completed=100, failed=5) -> DivisionReport:
    return DivisionReport(
        division=division,
        name=f"Division {division}",
        tasks_completed=completed,
        tasks_failed=failed,
        key_metric="Prospects",
        key_value="150",
    )


def make_cycle(
    cycle_id: str = "cycle_001",
    emails_sent: int = 500,
    emails_opened: int = 200,
    emails_replied: int = 50,
    payments_confirmed: int = 7,
    revenue_eur: float = 24500.0,
    minutes: int = 30,
) -> CycleReport:
    start = datetime.datetime(2026, 1, 1, 8, 0, 0)
    end = start + datetime.timedelta(minutes=minutes)
    return CycleReport(
        cycle_id=cycle_id,
        started_at=start,
        completed_at=end,
        prospects_detected=1200,
        emails_sent=emails_sent,
        emails_opened=emails_opened,
        emails_replied=emails_replied,
        negotiations_opened=25,
        payments_confirmed=payments_confirmed,
        revenue_eur=revenue_eur,
        top_sector="Artisans & Bâtiment",
        top_agent_id="2.1",
        division_reports=[make_div(i) for i in range(1, 7)],
    )


# ── DivisionReport ────────────────────────────────────────────────────────────

class TestDivisionReport:
    def test_success_rate_calculation(self):
        d = make_div(completed=95, failed=5)
        assert d.success_rate == pytest.approx(0.95, abs=0.001)

    def test_success_rate_zero_when_no_tasks(self):
        d = DivisionReport(1, "T", 0, 0, "KPI", "0")
        assert d.success_rate == 0.0

    def test_success_rate_one_when_no_failures(self):
        d = make_div(completed=100, failed=0)
        assert d.success_rate == 1.0


# ── CycleReport properties ────────────────────────────────────────────────────

class TestCycleReportProperties:
    def test_duration_minutes(self):
        r = make_cycle(minutes=45)
        assert r.duration_minutes == pytest.approx(45.0, abs=0.01)

    def test_open_rate(self):
        r = make_cycle(emails_sent=500, emails_opened=200)
        assert r.open_rate == pytest.approx(0.4, abs=0.001)

    def test_reply_rate(self):
        r = make_cycle(emails_sent=500, emails_replied=50)
        assert r.reply_rate == pytest.approx(0.1, abs=0.001)

    def test_conversion_rate(self):
        r = make_cycle(emails_sent=500, payments_confirmed=5)
        assert r.conversion_rate == pytest.approx(0.01, abs=0.0001)

    def test_open_rate_zero_when_no_emails(self):
        r = make_cycle(emails_sent=0, emails_opened=0)
        assert r.open_rate == 0.0

    def test_reply_rate_zero_when_no_emails(self):
        r = make_cycle(emails_sent=0, emails_replied=0)
        assert r.reply_rate == 0.0

    def test_to_dict_has_all_keys(self):
        d = make_cycle().to_dict()
        for key in ("cycle_id", "started_at", "completed_at", "duration_minutes",
                    "prospects_detected", "emails_sent", "emails_opened", "emails_replied",
                    "payments_confirmed", "revenue_eur", "open_rate", "reply_rate",
                    "conversion_rate", "division_reports"):
            assert key in d

    def test_to_dict_division_reports_list(self):
        d = make_cycle().to_dict()
        assert isinstance(d["division_reports"], list)
        assert len(d["division_reports"]) == 6


# ── ReportGenerator — add / get ───────────────────────────────────────────────

class TestAddGet:
    def test_add_and_get_cycle(self):
        g = gen()
        r = make_cycle("c1")
        g.add_cycle(r)
        assert g.get_cycle("c1") is not None

    def test_get_unknown_returns_none(self):
        assert gen().get_cycle("missing") is None

    def test_last_cycle_returns_most_recent(self):
        g = gen()
        g.add_cycle(make_cycle("c1"))
        g.add_cycle(make_cycle("c2"))
        assert g.last_cycle().cycle_id == "c2"

    def test_last_cycle_none_when_empty(self):
        assert gen().last_cycle() is None

    def test_all_cycles_returns_list(self):
        g = gen()
        g.add_cycle(make_cycle("c1"))
        g.add_cycle(make_cycle("c2"))
        assert len(g.all_cycles()) == 2


# ── cumulative / best ─────────────────────────────────────────────────────────

class TestCumulativeAndBest:
    def test_cumulative_revenue(self):
        g = gen()
        g.add_cycle(make_cycle("c1", revenue_eur=10000))
        g.add_cycle(make_cycle("c2", revenue_eur=15000))
        assert g.cumulative_revenue() == pytest.approx(25000.0)

    def test_cumulative_emails(self):
        g = gen()
        g.add_cycle(make_cycle("c1", emails_sent=300))
        g.add_cycle(make_cycle("c2", emails_sent=400))
        assert g.cumulative_emails() == 700

    def test_best_cycle_returns_highest_revenue(self):
        g = gen()
        g.add_cycle(make_cycle("c1", revenue_eur=5000))
        g.add_cycle(make_cycle("c2", revenue_eur=50000))
        assert g.best_cycle().cycle_id == "c2"

    def test_best_cycle_none_when_empty(self):
        assert gen().best_cycle() is None


# ── generate_text ─────────────────────────────────────────────────────────────

class TestGenerateText:
    def test_returns_string(self):
        text = gen().generate_text(make_cycle())
        assert isinstance(text, str)

    def test_contains_cycle_id(self):
        text = gen().generate_text(make_cycle("cycle_xyz"))
        assert "cycle_xyz" in text

    def test_contains_revenue(self):
        text = gen().generate_text(make_cycle(revenue_eur=24500))
        assert "24" in text

    def test_contains_division_rows(self):
        text = gen().generate_text(make_cycle())
        assert "Div 1" in text or "Division 1" in text

    def test_contains_email_stats(self):
        text = gen().generate_text(make_cycle(emails_sent=500))
        assert "500" in text

    def test_contains_top_agent(self):
        text = gen().generate_text(make_cycle())
        assert "2.1" in text


# ── generate_html ─────────────────────────────────────────────────────────────

class TestGenerateHTML:
    def test_returns_string(self):
        html = gen().generate_html(make_cycle())
        assert isinstance(html, str)

    def test_is_valid_html(self):
        html = gen().generate_html(make_cycle())
        assert "<!DOCTYPE html>" in html
        assert "</html>" in html

    def test_contains_cycle_id(self):
        html = gen().generate_html(make_cycle("cycle_html"))
        assert "cycle_html" in html

    def test_contains_revenue_value(self):
        html = gen().generate_html(make_cycle(revenue_eur=24500))
        assert "24" in html

    def test_contains_division_table(self):
        html = gen().generate_html(make_cycle())
        assert "<table>" in html
        assert "<tbody>" in html

    def test_has_print_media_query(self):
        html = gen().generate_html(make_cycle())
        assert "@media print" in html

    def test_has_6_division_rows(self):
        html = gen().generate_html(make_cycle())
        assert html.count("<tr>") >= 6


# ── generate_summary_table ────────────────────────────────────────────────────

class TestSummaryTable:
    def test_returns_string(self):
        g = gen()
        g.add_cycle(make_cycle("c1"))
        assert isinstance(g.generate_summary_table(), str)

    def test_contains_cycle_ids(self):
        g = gen()
        g.add_cycle(make_cycle("c1"))
        g.add_cycle(make_cycle("c2"))
        table = g.generate_summary_table()
        assert "c1" in table
        assert "c2" in table

    def test_respects_n_limit(self):
        g = gen()
        for i in range(5):
            g.add_cycle(make_cycle(f"c{i}"))
        table = g.generate_summary_table(n=3)
        assert "c0" not in table or "c1" not in table  # only last 3


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_history(self):
        g = gen()
        g.add_cycle(make_cycle("c1"))
        g.reset()
        assert g.all_cycles() == []

    def test_reset_allows_fresh_start(self):
        g = gen()
        g.add_cycle(make_cycle("c1"))
        g.reset()
        g.add_cycle(make_cycle("c2"))
        assert len(g.all_cycles()) == 1
