"""
Report Generator — creates structured performance reports for completed swarm cycles.

Generates:
  - Cycle summary (prospects detected, emails sent, conversions, revenue)
  - Division-by-division breakdown
  - Top performing agents
  - HTML and plain-text formats

Does NOT use external PDF libraries — HTML output can be printed to PDF from browser.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Data models ───────────────────────────────────────────────────────────────

@dataclass
class DivisionReport:
    division: int
    name: str
    tasks_completed: int
    tasks_failed: int
    key_metric: str     # human-readable main KPI label
    key_value: str      # human-readable main KPI value
    notes: str = ""

    @property
    def success_rate(self) -> float:
        total = self.tasks_completed + self.tasks_failed
        return self.tasks_completed / total if total else 0.0


@dataclass
class CycleReport:
    cycle_id: str
    started_at: datetime.datetime
    completed_at: datetime.datetime
    division_reports: List[DivisionReport] = field(default_factory=list)
    prospects_detected: int = 0
    emails_sent: int = 0
    emails_opened: int = 0
    emails_replied: int = 0
    negotiations_opened: int = 0
    payments_confirmed: int = 0
    revenue_eur: float = 0.0
    top_sector: str = ""
    top_agent_id: str = ""
    notes: str = ""

    @property
    def duration_minutes(self) -> float:
        return (self.completed_at - self.started_at).total_seconds() / 60

    @property
    def open_rate(self) -> float:
        return self.emails_opened / self.emails_sent if self.emails_sent else 0.0

    @property
    def reply_rate(self) -> float:
        return self.emails_replied / self.emails_sent if self.emails_sent else 0.0

    @property
    def conversion_rate(self) -> float:
        return self.payments_confirmed / self.emails_sent if self.emails_sent else 0.0

    def to_dict(self) -> dict:
        return {
            "cycle_id": self.cycle_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
            "duration_minutes": round(self.duration_minutes, 1),
            "prospects_detected": self.prospects_detected,
            "emails_sent": self.emails_sent,
            "emails_opened": self.emails_opened,
            "emails_replied": self.emails_replied,
            "negotiations_opened": self.negotiations_opened,
            "payments_confirmed": self.payments_confirmed,
            "revenue_eur": round(self.revenue_eur, 2),
            "open_rate": round(self.open_rate, 4),
            "reply_rate": round(self.reply_rate, 4),
            "conversion_rate": round(self.conversion_rate, 4),
            "top_sector": self.top_sector,
            "top_agent_id": self.top_agent_id,
            "notes": self.notes,
            "division_reports": [
                {
                    "division": d.division,
                    "name": d.name,
                    "tasks_completed": d.tasks_completed,
                    "tasks_failed": d.tasks_failed,
                    "success_rate": round(d.success_rate, 4),
                    "key_metric": d.key_metric,
                    "key_value": d.key_value,
                }
                for d in self.division_reports
            ],
        }


# ── Generator ─────────────────────────────────────────────────────────────────

class ReportGenerator:
    """Generates HTML and text performance reports for completed swarm cycles."""

    def __init__(self):
        self._history: List[CycleReport] = []

    def add_cycle(self, report: CycleReport) -> None:
        """Store a completed cycle report."""
        self._history.append(report)

    def get_cycle(self, cycle_id: str) -> Optional[CycleReport]:
        return next((r for r in self._history if r.cycle_id == cycle_id), None)

    def last_cycle(self) -> Optional[CycleReport]:
        return self._history[-1] if self._history else None

    def all_cycles(self) -> List[CycleReport]:
        return list(self._history)

    def cumulative_revenue(self) -> float:
        return sum(r.revenue_eur for r in self._history)

    def cumulative_emails(self) -> int:
        return sum(r.emails_sent for r in self._history)

    def best_cycle(self) -> Optional[CycleReport]:
        return max(self._history, key=lambda r: r.revenue_eur, default=None)

    def generate_text(self, report: CycleReport) -> str:
        """Generate a plain-text summary of a cycle report."""
        lines = [
            f"═══════════════════════════════════════",
            f"  RAPPORT CYCLE {report.cycle_id}",
            f"═══════════════════════════════════════",
            f"Début    : {report.started_at.strftime('%d/%m/%Y %H:%M')}",
            f"Fin      : {report.completed_at.strftime('%d/%m/%Y %H:%M')}",
            f"Durée    : {report.duration_minutes:.0f} min",
            f"",
            f"── FUNNEL ──────────────────────────────",
            f"Prospects détectés : {report.prospects_detected}",
            f"Emails envoyés     : {report.emails_sent}",
            f"Emails ouverts     : {report.emails_opened} ({report.open_rate:.1%})",
            f"Réponses           : {report.emails_replied} ({report.reply_rate:.1%})",
            f"Négociations       : {report.negotiations_opened}",
            f"Paiements          : {report.payments_confirmed}",
            f"Revenu             : {report.revenue_eur:,.0f} €",
            f"",
            f"── DIVISIONS ───────────────────────────",
        ]
        for d in report.division_reports:
            lines.append(
                f"  Div {d.division} {d.name[:25]:<25} "
                f"✓{d.tasks_completed} ✗{d.tasks_failed} "
                f"({d.success_rate:.0%}) | {d.key_metric}: {d.key_value}"
            )
        lines += [
            f"",
            f"── TOP ─────────────────────────────────",
            f"Secteur   : {report.top_sector}",
            f"Meilleur  : Agent {report.top_agent_id}",
            f"Notes     : {report.notes or '—'}",
            f"═══════════════════════════════════════",
        ]
        return "\n".join(lines)

    def generate_html(self, report: CycleReport) -> str:
        """Generate a self-contained HTML report page."""
        pct = lambda n: f"{n:.1%}"
        eur = lambda n: f"{n:,.0f} €"
        rows = "".join(
            f"<tr>"
            f"<td>{d.division}</td><td>{d.name}</td>"
            f"<td>{d.tasks_completed}</td><td>{d.tasks_failed}</td>"
            f"<td>{pct(d.success_rate)}</td>"
            f"<td>{d.key_metric} : {d.key_value}</td>"
            f"</tr>"
            for d in report.division_reports
        )
        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Cycle {report.cycle_id} — Rapport Swarm</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background: #0a0a0f; color: #e5e7eb; margin: 0; padding: 2rem; }}
  h1 {{ color: #818cf8; }} h2 {{ color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0; }}
  .kpi {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 0.75rem; padding: 1rem; }}
  .kpi-label {{ font-size: 0.75rem; color: #6b7280; }} .kpi-value {{ font-size: 1.5rem; font-weight: bold; margin-top: 0.25rem; }}
  .emerald {{ color: #34d399; }} .indigo {{ color: #818cf8; }} .amber {{ color: #fbbf24; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th {{ text-align: left; padding: 0.5rem 0.75rem; font-size: 0.75rem; color: #6b7280; border-bottom: 1px solid rgba(255,255,255,0.08); }}
  td {{ padding: 0.5rem 0.75rem; font-size: 0.875rem; border-bottom: 1px solid rgba(255,255,255,0.05); }}
  @media print {{ body {{ background: white; color: #111; }} .kpi {{ background: #f9fafb; border-color: #e5e7eb; }} }}
</style>
</head>
<body>
<h1>🤖 Rapport Cycle {report.cycle_id}</h1>
<p style="color:#6b7280">{report.started_at.strftime('%d/%m/%Y %H:%M')} → {report.completed_at.strftime('%H:%M')} ({report.duration_minutes:.0f} min)</p>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Prospects détectés</div><div class="kpi-value">{report.prospects_detected:,}</div></div>
  <div class="kpi"><div class="kpi-label">Emails envoyés</div><div class="kpi-value indigo">{report.emails_sent:,}</div></div>
  <div class="kpi"><div class="kpi-label">Taux de réponse</div><div class="kpi-value amber">{pct(report.reply_rate)}</div></div>
  <div class="kpi"><div class="kpi-label">Revenu</div><div class="kpi-value emerald">{eur(report.revenue_eur)}</div></div>
</div>
<h2>Résultats par Division</h2>
<table><thead><tr><th>#</th><th>Division</th><th>Réussies</th><th>Échecs</th><th>Taux</th><th>KPI</th></tr></thead>
<tbody>{rows}</tbody></table>
<p style="margin-top:2rem;color:#6b7280;font-size:0.75rem">
  Meilleur secteur : {report.top_sector} | Agent top : {report.top_agent_id}
</p>
</body></html>"""

    def generate_summary_table(self, n: int = 10) -> str:
        """Plain text table of last N cycles."""
        cycles = self._history[-n:]
        header = f"{'Cycle':<20} {'Envoyés':>8} {'Rép.':>6} {'Payé':>5} {'Revenu €':>10}"
        sep = "─" * len(header)
        rows = [
            f"{r.cycle_id:<20} {r.emails_sent:>8} {r.reply_rate:>6.1%} "
            f"{r.payments_confirmed:>5} {r.revenue_eur:>10,.0f}"
            for r in reversed(cycles)
        ]
        return "\n".join([header, sep, *rows])

    def reset(self) -> None:
        self._history.clear()
