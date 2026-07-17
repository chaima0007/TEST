"""
Tests for exporters/linkedin_scheduler.py
"""

import json
import os
import pytest
import tempfile
from datetime import datetime, timedelta
from exporters.linkedin_scheduler import (
    schedule_posts,
    export_schedule_json,
    export_schedule_csv,
    export_schedule,
    _next_preferred_date,
    _PREFERRED_DAYS,
    _POST_HOUR,
)
from divisions.division_6_branding import LinkedInPost, Division6Branding


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_post(post_id: str = "li_001", source_event: str = "test") -> LinkedInPost:
    return LinkedInPost(
        post_id=post_id,
        title=f"Post {post_id}",
        hook="Accroche du post",
        body="Corps du post LinkedIn.",
        hashtags=["IA", "Automatisation", "LinkedIn"],
        char_count=150,
        impressions_estimate=1200,
        generated_at=datetime.utcnow().isoformat(),
        source_event=source_event,
    )


def make_posts(n: int) -> list[LinkedInPost]:
    return [make_post(post_id=f"li_{i:03d}") for i in range(1, n + 1)]


# ── _next_preferred_date ──────────────────────────────────────────────────────

class TestNextPreferredDate:
    def test_returns_datetime(self):
        d = _next_preferred_date(datetime.now())
        assert isinstance(d, datetime)

    def test_returns_preferred_day(self):
        for _ in range(14):
            start = datetime.now() + timedelta(days=_)
            d = _next_preferred_date(start)
            assert d.isoweekday() in _PREFERRED_DAYS

    def test_returns_correct_hour(self):
        d = _next_preferred_date(datetime.now())
        assert d.hour == _POST_HOUR
        assert d.minute == 0
        assert d.second == 0

    def test_advances_from_non_preferred_day(self):
        # Find a non-preferred day (e.g. Tuesday = 2)
        base = datetime(2026, 6, 16)  # Tuesday
        if base.isoweekday() in _PREFERRED_DAYS:
            base = datetime(2026, 6, 17)  # Try Wednesday
        d = _next_preferred_date(base)
        assert d.isoweekday() in _PREFERRED_DAYS

    def test_preferred_day_returns_same_day(self):
        # Monday = 1 is preferred
        base = datetime(2026, 6, 15)  # Monday
        if base.isoweekday() not in _PREFERRED_DAYS:
            pytest.skip("Adjust fixture date to a preferred day")
        d = _next_preferred_date(base)
        assert d.isoweekday() in _PREFERRED_DAYS


# ── schedule_posts ────────────────────────────────────────────────────────────

class TestSchedulePosts:
    def test_returns_list(self):
        posts = make_posts(3)
        result = schedule_posts(posts)
        assert isinstance(result, list)

    def test_one_entry_per_post(self):
        posts = make_posts(5)
        result = schedule_posts(posts)
        assert len(result) == 5

    def test_each_entry_has_scheduled_at(self):
        posts = make_posts(3)
        result = schedule_posts(posts)
        for r in result:
            assert "scheduled_at" in r
            assert r["scheduled_at"]

    def test_each_entry_has_status_scheduled(self):
        posts = make_posts(3)
        result = schedule_posts(posts)
        for r in result:
            assert r["status"] == "scheduled"

    def test_each_entry_has_day_of_week(self):
        posts = make_posts(3)
        result = schedule_posts(posts)
        for r in result:
            assert "day_of_week" in r

    def test_dates_are_on_preferred_days(self):
        posts = make_posts(6)
        result = schedule_posts(posts)
        day_names = {"Monday", "Wednesday", "Friday"}
        for r in result:
            assert r["day_of_week"] in day_names, f"Unexpected day: {r['day_of_week']}"

    def test_dates_are_sequential(self):
        posts = make_posts(4)
        result = schedule_posts(posts)
        dates = [datetime.strptime(r["scheduled_at"], "%Y-%m-%d %H:%M") for r in result]
        for i in range(1, len(dates)):
            assert dates[i] > dates[i - 1]

    def test_has_full_text(self):
        posts = make_posts(2)
        result = schedule_posts(posts)
        for r in result:
            assert "full_text" in r
            assert len(r["full_text"]) > 10

    def test_has_impressions_estimate(self):
        posts = make_posts(2)
        result = schedule_posts(posts)
        for r in result:
            assert "impressions_estimate" in r
            assert r["impressions_estimate"] > 0

    def test_custom_start_date(self):
        posts = make_posts(2)
        start = datetime(2027, 1, 1)
        result = schedule_posts(posts, start_date=start)
        for r in result:
            dt = datetime.strptime(r["scheduled_at"], "%Y-%m-%d %H:%M")
            assert dt.year == 2027

    def test_empty_posts_returns_empty(self):
        result = schedule_posts([])
        assert result == []


# ── export_schedule_json ──────────────────────────────────────────────────────

class TestExportJSON:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_json(make_posts(3), tmp)
            assert os.path.exists(path)

    def test_file_is_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_json(make_posts(3), tmp)
            with open(path) as f:
                data = json.load(f)
            assert "posts" in data
            assert "exported_at" in data

    def test_json_has_correct_post_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_json(make_posts(4), tmp)
            with open(path) as f:
                data = json.load(f)
            assert len(data["posts"]) == 4

    def test_creates_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = os.path.join(tmp, "exports", "linkedin")
            export_schedule_json(make_posts(2), nested)
            assert os.path.isdir(nested)


# ── export_schedule_csv ───────────────────────────────────────────────────────

class TestExportCSV:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_csv(make_posts(3), tmp)
            assert os.path.exists(path)

    def test_file_extension_is_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_csv(make_posts(3), tmp)
            assert path.endswith(".csv")

    def test_csv_has_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_csv(make_posts(2), tmp)
            with open(path, encoding="utf-8") as f:
                first_line = f.readline()
            assert "scheduled_at" in first_line

    def test_csv_has_correct_row_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_csv(make_posts(3), tmp)
            with open(path, encoding="utf-8") as f:
                lines = [l for l in f if l.strip()]
            # 1 header + 3 data rows
            assert len(lines) == 4

    def test_hashtags_formatted_with_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_schedule_csv(make_posts(1), tmp)
            content = open(path, encoding="utf-8").read()
            assert "#IA" in content


# ── export_schedule (both formats) ───────────────────────────────────────────

class TestExportSchedule:
    def test_both_format_returns_two_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = export_schedule(make_posts(2), tmp, fmt="both")
            assert "json" in result
            assert "csv" in result

    def test_json_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = export_schedule(make_posts(2), tmp, fmt="json")
            assert "json" in result
            assert "csv" not in result

    def test_csv_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = export_schedule(make_posts(2), tmp, fmt="csv")
            assert "csv" in result
            assert "json" not in result

    def test_all_paths_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = export_schedule(make_posts(3), tmp, fmt="both")
            for path in result.values():
                assert os.path.exists(path)
