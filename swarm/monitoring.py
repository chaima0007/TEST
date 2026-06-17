"""
SWARM MONITORING — Live terminal dashboard.

Polls the FastAPI server every 3 seconds and renders a Rich Live display
showing division statuses, active agents, revenue, and last errors.

Usage:
    python monitoring.py
    python monitoring.py --url http://localhost:8001
    python monitoring.py --interval 5
"""

import argparse
import asyncio
import time

import httpx
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

console = Console()

DIVISION_COLORS = {
    1: "blue",
    2: "magenta",
    3: "yellow",
    4: "green",
    5: "red",
    6: "pink1",
}


def make_header(data: dict) -> Panel:
    revenue = data.get("revenue_today", 0)
    agents_active = data.get("agents_active", 0)
    agents_idle = data.get("agents_idle", 0)
    agents_error = data.get("agents_error", 0)
    ts = data.get("timestamp", "—")

    text = (
        f"[bold green]💰 CA aujourd'hui: {revenue:.0f}€[/bold green]   "
        f"[green]⚡ {agents_active} actifs[/green]   "
        f"[dim]{agents_idle} inactifs[/dim]   "
        f"[red]{agents_error} erreurs[/red]   "
        f"[dim]Mis à jour: {ts[:19]}[/dim]"
    )
    return Panel(Text.from_markup(text), title="[bold blue]🐝 SWARM INTELLIGENCE — LIVE[/bold blue]", border_style="blue")


def make_divisions_table(data: dict) -> Table:
    table = Table(title="Divisions & Agents", box=box.ROUNDED, show_lines=False, expand=True)
    table.add_column("Div.", width=5, style="bold")
    table.add_column("Nom", width=22)
    table.add_column("Agents actifs", width=16)
    table.add_column("KPI", width=14)
    table.add_column("Statut", width=12)

    for div in data.get("divisions", []):
        div_id = div.get("id", 0)
        color = DIVISION_COLORS.get(div_id, "white")
        agents = div.get("agents", [])
        active_count = sum(1 for a in agents if a.get("status") == "active")
        error_count = sum(1 for a in agents if a.get("status") == "error")

        # Mini bar: ● for active, ○ for idle, ✕ for error
        dots = ""
        for a in agents[:10]:
            s = a.get("status", "idle")
            if s == "active":
                dots += f"[{color}]●[/{color}]"
            elif s == "error":
                dots += "[red]✕[/red]"
            else:
                dots += "[dim]○[/dim]"

        status_text = "[green]OK[/green]" if error_count == 0 else f"[red]{error_count} err[/red]"

        table.add_row(
            f"[{color}]{div.get('emoji', '')} {div_id}[/{color}]",
            div.get("name", ""),
            dots,
            f"[{color}]{div.get('kpiValue', '—')} {div.get('kpiUnit', '')}[/{color}]",
            status_text,
        )

    return table


def make_errors_panel(data: dict) -> Panel:
    errors = data.get("errors", [])
    if not errors:
        content = "[dim green]Aucune erreur[/dim green]"
    else:
        content = "\n".join(f"[red]• {e}[/red]" for e in errors[-5:])
    return Panel(content, title="Erreurs récentes", border_style="red", height=8)


def make_cycle_panel(data: dict) -> Panel:
    cycle = data.get("active_cycle", {})
    if not cycle:
        content = "[dim]Aucun cycle en cours[/dim]"
    else:
        cid = cycle.get("cycle_id", "—")
        fiches = cycle.get("fiches_detected", 0)
        outreach = cycle.get("outreach_queue", 0)
        threads = cycle.get("negotiation_threads", 0)
        revenue = cycle.get("revenue_today", 0)
        content = (
            f"[bold]Cycle:[/bold] {cid}\n"
            f"[blue]Prospects:[/blue] {fiches}  "
            f"[magenta]Emails:[/magenta] {outreach}  "
            f"[yellow]Négos:[/yellow] {threads}  "
            f"[green]CA:[/green] {revenue:.0f}€"
        )
    return Panel(content, title="Cycle actif", border_style="yellow", height=8)


async def poll_and_display(url: str, interval: int):
    async with httpx.AsyncClient(timeout=5.0) as client:
        with Live(console=console, refresh_per_second=1, screen=False) as live:
            while True:
                try:
                    resp = await client.get(f"{url}/swarm/status")
                    data = resp.json() if resp.status_code == 200 else {}
                except Exception as e:
                    data = {"error": str(e)}

                layout = Layout()
                layout.split_column(
                    Layout(make_header(data), size=3),
                    Layout(name="body"),
                )
                layout["body"].split_row(
                    Layout(make_divisions_table(data), ratio=2),
                    Layout(name="side"),
                )
                layout["side"].split_column(
                    Layout(make_cycle_panel(data)),
                    Layout(make_errors_panel(data)),
                )
                live.update(layout)
                await asyncio.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Swarm live monitoring dashboard")
    parser.add_argument("--url", default="http://localhost:8001", help="Swarm API URL")
    parser.add_argument("--interval", type=int, default=3, help="Refresh interval in seconds")
    args = parser.parse_args()

    console.print(Panel.fit(
        f"[bold]Connexion à l'API Swarm :[/bold] {args.url}\n"
        f"[dim]Intervalle de refresh : {args.interval}s — Ctrl+C pour quitter[/dim]",
        border_style="blue",
    ))

    asyncio.run(poll_and_display(args.url, args.interval))


if __name__ == "__main__":
    main()
