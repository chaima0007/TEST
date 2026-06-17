"""
PDF Report Exporter for the Swarm financial cycle.

Generates a clean PDF report from cycle results using Python's built-in
string formatting (no external PDF library required — uses HTML → PDF
via weasyprint if available, falls back to text report).

Usage:
    from exporters.pdf_report import generate_pdf_report
    path = generate_pdf_report(cycle_state, output_dir="./reports")
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Rapport Swarm — {cycle_id}</title>
<style>
  body {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #1e293b; margin: 40px; }}
  h1 {{ color: #4f46e5; font-size: 24px; margin-bottom: 4px; }}
  h2 {{ color: #64748b; font-size: 13px; font-weight: normal; margin-top: 0; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0; }}
  .kpi {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; }}
  .kpi-value {{ font-size: 28px; font-weight: 700; color: #4f46e5; }}
  .kpi-label {{ font-size: 11px; color: #94a3b8; margin-top: 2px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 16px; }}
  th {{ background: #f1f5f9; padding: 8px 12px; text-align: left; font-size: 10px;
        text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #f1f5f9; }}
  .green {{ color: #059669; font-weight: 600; }}
  .red {{ color: #dc2626; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 10px;
            font-weight: 600; background: #dcfce7; color: #166534; }}
  .badge.error {{ background: #fee2e2; color: #991b1b; }}
  footer {{ margin-top: 40px; font-size: 10px; color: #94a3b8; border-top: 1px solid #e2e8f0;
            padding-top: 12px; }}
</style>
</head>
<body>
<h1>Rapport Swarm — Cycle {cycle_id}</h1>
<h2>Généré le {generated_at} · Durée : {duration}</h2>

<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-value">{revenue_eur}€</div>
    <div class="kpi-label">CA généré</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">{prospects_count}</div>
    <div class="kpi-label">Prospects détectés</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">{emails_count}</div>
    <div class="kpi-label">Emails envoyés</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">{paid_count}</div>
    <div class="kpi-label">Paiements confirmés</div>
  </div>
</div>

<h3 style="font-size:14px;color:#1e293b;margin-top:32px;">Statut des Divisions</h3>
<table>
  <thead>
    <tr><th>Division</th><th>Nom</th><th>Statut</th></tr>
  </thead>
  <tbody>
    {division_rows}
  </tbody>
</table>

{production_jobs_section}

{errors_section}

<footer>
  Rapport généré automatiquement par le Swarm IA — Agent 5.9 · {generated_at}
</footer>
</body>
</html>"""


def _div_row(div_id: str, status: str, names: dict[str, str]) -> str:
    name = names.get(str(div_id), f"Division {div_id}")
    badge_cls = "" if status == "success" else "error"
    return f"<tr><td>{div_id}</td><td>{name}</td><td><span class='badge {badge_cls}'>{status}</span></td></tr>"


def _production_section(jobs: list[dict]) -> str:
    if not jobs:
        return ""
    rows = ""
    for j in jobs[:20]:
        amount = f"<td class='green'>{j.get('quote_eur', '—')}€</td>" if j.get("quote_eur") else "<td>—</td>"
        rows += f"<tr><td>{j.get('company_id','')}</td><td>{j.get('company_name','')}</td><td>{j.get('stage','')}</td>{amount}</tr>"
    return f"""
<h3 style="font-size:14px;color:#1e293b;margin-top:32px;">Jobs de Production</h3>
<table>
  <thead><tr><th>ID</th><th>Entreprise</th><th>Étape</th><th>Devis</th></tr></thead>
  <tbody>{rows}</tbody>
</table>"""


def _errors_section(errors: list[str]) -> str:
    if not errors:
        return ""
    items = "".join(f"<li class='red'>{e}</li>" for e in errors)
    return f"<h3 style='font-size:14px;color:#dc2626;margin-top:32px;'>Erreurs ({len(errors)})</h3><ul>{items}</ul>"


DIVISION_NAMES = {
    "1": "Détection & Scouting",
    "2": "Rédaction & Outreach",
    "3": "Relation & Négociation",
    "4": "Production & Design",
    "5": "Finance & Conformité",
    "6": "Personal Branding",
}


def generate_html_report(state: dict[str, Any]) -> str:
    """Generates the full HTML string for the cycle report."""
    cycle_id = state.get("cycle_id", "—")
    started = state.get("started_at", "")
    completed = state.get("completed_at", "")
    revenue = state.get("revenue_today", 0)
    fiches = state.get("fiches_detected", [])
    outreach = state.get("outreach_queue", [])
    jobs = state.get("production_jobs", [])
    errors = state.get("errors", [])
    div_statuses = state.get("division_status", {})

    # Duration
    duration = "—"
    if started and completed:
        try:
            s = datetime.fromisoformat(str(started))
            e = datetime.fromisoformat(str(completed))
            secs = int((e - s).total_seconds())
            duration = f"{secs // 60}m {secs % 60}s"
        except Exception:
            pass

    paid_count = sum(1 for j in jobs if j.get("payment_confirmed") or j.get("stage") == "paid")
    div_rows = "".join(_div_row(k, v, DIVISION_NAMES) for k, v in div_statuses.items())

    return HTML_TEMPLATE.format(
        cycle_id=cycle_id,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
        duration=duration,
        revenue_eur=f"{revenue:.0f}",
        prospects_count=len(fiches),
        emails_count=len(outreach),
        paid_count=paid_count,
        division_rows=div_rows,
        production_jobs_section=_production_section(jobs),
        errors_section=_errors_section(errors),
    )


def generate_pdf_report(state: dict[str, Any], output_dir: str = "./reports") -> str:
    """
    Generates a PDF report from cycle state.

    Returns the path to the generated file (.pdf if weasyprint is available,
    .html otherwise).
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    cycle_id = state.get("cycle_id", datetime.now().strftime("%Y%m%d_%H%M%S"))
    html = generate_html_report(state)

    # Try PDF via weasyprint
    try:
        from weasyprint import HTML as WeasyprintHTML  # type: ignore
        pdf_path = os.path.join(output_dir, f"rapport_swarm_{cycle_id}.pdf")
        WeasyprintHTML(string=html).write_pdf(pdf_path)
        return pdf_path
    except ImportError:
        pass

    # Fallback: save as HTML
    html_path = os.path.join(output_dir, f"rapport_swarm_{cycle_id}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path


def generate_text_report(state: dict[str, Any]) -> str:
    """Plain text version of the cycle report (for email/logs)."""
    cycle_id = state.get("cycle_id", "—")
    revenue = state.get("revenue_today", 0)
    fiches = state.get("fiches_detected", [])
    outreach = state.get("outreach_queue", [])
    errors = state.get("errors", [])
    div_statuses = state.get("division_status", {})

    lines = [
        f"=== RAPPORT SWARM — {cycle_id} ===",
        f"CA généré      : {revenue:.0f}€",
        f"Prospects      : {len(fiches)}",
        f"Emails envoyés : {len(outreach)}",
        f"Erreurs        : {len(errors)}",
        "",
        "DIVISIONS :",
    ]
    for k, v in div_statuses.items():
        name = DIVISION_NAMES.get(str(k), f"Div {k}")
        status_icon = "✓" if v == "success" else "✗"
        lines.append(f"  {status_icon} {name} [{v}]")

    if errors:
        lines += ["", "ERREURS :"] + [f"  • {e}" for e in errors]

    return "\n".join(lines)
