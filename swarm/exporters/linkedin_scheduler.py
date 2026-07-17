"""
LinkedIn Content Scheduler — exports the editorial calendar to JSON/CSV
so content can be imported into Buffer, Hootsuite, or LinkedIn Scheduler.

Usage:
    from exporters.linkedin_scheduler import export_schedule
    path = export_schedule(posts, output_dir="./exports")
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from divisions.division_6_branding import LinkedInPost


# Days of week (1=Mon ... 7=Sun) preferred for LinkedIn publishing
_PREFERRED_DAYS = {1, 3, 5}  # Monday, Wednesday, Friday
_POST_HOUR = 8  # 08:00 Paris time


def _next_preferred_date(from_date: datetime) -> datetime:
    """Returns the next Mon/Wed/Fri at 08:00 starting from from_date."""
    d = from_date.replace(hour=_POST_HOUR, minute=0, second=0, microsecond=0)
    for _ in range(14):
        if d.isoweekday() in _PREFERRED_DAYS:
            return d
        d += timedelta(days=1)
    return d


def schedule_posts(
    posts: list[LinkedInPost],
    start_date: datetime | None = None,
) -> list[dict[str, Any]]:
    """
    Assigns a scheduled_at datetime to each post (Mon/Wed/Fri at 08:00).
    Returns list of dicts ready for export.
    """
    start = start_date or datetime.now()
    scheduled: list[dict[str, Any]] = []
    cursor = start

    for post in posts:
        publish_at = _next_preferred_date(cursor)
        entry = {
            "post_id": post.post_id,
            "title": post.title,
            "hook": post.hook,
            "full_text": post.full_text(),
            "char_count": post.char_count,
            "hashtags": post.hashtags,
            "impressions_estimate": post.impressions_estimate,
            "scheduled_at": publish_at.strftime("%Y-%m-%d %H:%M"),
            "day_of_week": publish_at.strftime("%A"),
            "source_event": post.source_event,
            "status": "scheduled",
        }
        scheduled.append(entry)
        cursor = publish_at + timedelta(days=1)

    return scheduled


def export_schedule_json(
    posts: list[LinkedInPost],
    output_dir: str = "./exports",
    start_date: datetime | None = None,
) -> str:
    """Exports the schedule to a JSON file and returns its path."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    schedule = schedule_posts(posts, start_date)
    filename = f"linkedin_schedule_{datetime.now().strftime('%Y%m%d')}.json"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"posts": schedule, "exported_at": datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)
    return path


def export_schedule_csv(
    posts: list[LinkedInPost],
    output_dir: str = "./exports",
    start_date: datetime | None = None,
) -> str:
    """Exports the schedule to a CSV file compatible with Buffer/Hootsuite."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    schedule = schedule_posts(posts, start_date)
    filename = f"linkedin_schedule_{datetime.now().strftime('%Y%m%d')}.csv"
    path = os.path.join(output_dir, filename)

    fields = ["scheduled_at", "day_of_week", "title", "full_text", "char_count", "hashtags", "impressions_estimate", "status"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in schedule:
            row["hashtags"] = " ".join(f"#{h}" for h in row["hashtags"])
            writer.writerow(row)
    return path


def export_schedule(
    posts: list[LinkedInPost],
    output_dir: str = "./exports",
    start_date: datetime | None = None,
    fmt: str = "both",
) -> dict[str, str]:
    """
    Export schedule in one or both formats.
    fmt: "json" | "csv" | "both"
    Returns dict with paths for each format written.
    """
    result: dict[str, str] = {}
    if fmt in ("json", "both"):
        result["json"] = export_schedule_json(posts, output_dir, start_date)
    if fmt in ("csv", "both"):
        result["csv"] = export_schedule_csv(posts, output_dir, start_date)
    return result
