"""
Celery task queue for the Swarm.

Queues:
  - swarm.cycle     : full detection → payment pipeline (hourly)
  - swarm.email     : individual outreach sends (immediate, rate-limited)
  - swarm.report    : nightly financial report generation

Start worker:
    celery -A tasks.celery_app worker --loglevel=info -Q swarm.cycle,swarm.email,swarm.report

Start beat scheduler:
    celery -A tasks.celery_app beat --loglevel=info
"""

import os
import asyncio
import logging
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

logger = logging.getLogger("swarm.celery")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "swarm",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.celery_app"],
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Paris",
    enable_utc=True,
    task_routes={
        "tasks.celery_app.run_swarm_cycle": {"queue": "swarm.cycle"},
        "tasks.celery_app.send_outreach_email": {"queue": "swarm.email"},
        "tasks.celery_app.generate_nightly_report": {"queue": "swarm.report"},
    },
    task_rate_limits={
        "tasks.celery_app.send_outreach_email": "120/m",
    },
)

# ── Periodic schedule ─────────────────────────────────────────────────────────

app.conf.beat_schedule = {
    "swarm-cycle-every-hour": {
        "task": "tasks.celery_app.run_swarm_cycle",
        "schedule": crontab(minute=0),
        "args": [],
    },
    "nightly-report-midnight": {
        "task": "tasks.celery_app.generate_nightly_report",
        "schedule": crontab(hour=0, minute=5),
        "args": [],
    },
}


# ── Tasks ─────────────────────────────────────────────────────────────────────

@app.task(bind=True, name="tasks.celery_app.run_swarm_cycle", max_retries=2)
def run_swarm_cycle(self):
    """Executes a full swarm cycle: detection → outreach → negotiation → payment."""
    from orchestrator import run_cycle
    try:
        result = asyncio.get_event_loop().run_until_complete(run_cycle())
        logger.info(
            "Cycle complete: %d prospects, %d emails, %.2f€ revenue",
            len(result.get("fiches_detected", [])),
            len(result.get("outreach_queue", [])),
            result.get("revenue_today", 0),
        )
        return result
    except Exception as exc:
        logger.error("Cycle failed: %s", exc)
        raise self.retry(exc=exc, countdown=300)


@app.task(name="tasks.celery_app.send_outreach_email")
def send_outreach_email(company_id: str, email: str, subject: str, body: str):
    """Sends a single RGPD-compliant outreach email via SMTP."""
    import smtplib
    from email.mime.text import MIMEText
    from divisions.division_5_finance import Division5Finance

    _fin = Division5Finance()
    if not _fin.validate_email_rgpd(email):
        logger.warning("RGPD block: %s refused for %s", email, company_id)
        return {"status": "blocked", "reason": "rgpd"}

    host = os.getenv("SMTP_HOST", "")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")

    if not host:
        logger.info("SMTP not configured — email to %s skipped (dev mode)", email)
        return {"status": "skipped", "reason": "no_smtp"}

    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = email
    msg["List-Unsubscribe"] = f"<mailto:{user}?subject=unsubscribe&body={company_id}>"

    try:
        with smtplib.SMTP(host, port) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.send_message(msg)
        logger.info("Email sent to %s for company %s", email, company_id)
        return {"status": "sent"}
    except Exception as exc:
        logger.error("Email failed: %s", exc)
        return {"status": "error", "error": str(exc)}


@app.task(name="tasks.celery_app.generate_nightly_report")
def generate_nightly_report():
    """Generates and saves the nightly financial summary."""
    from divisions.division_5_finance import Division5Finance
    _fin = Division5Finance()
    report = _fin.generate_daily_report()
    logger.info("Nightly report generated: %s", report)
    return report
