"""
SWARM — Point d'entrée principal.
Lance l'orchestrateur en mode continu ou exécute un cycle unique.

Usage:
    python main.py                   # Cycle unique
    python main.py --loop            # Mode continu (toutes les heures)
    python main.py --status          # Affiche le statut de tous les agents
    python main.py --simulate-sale   # Simule le dialogue Agent 3.5 ↔ Agent 5.1
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from config import ALL_AGENTS, DIVISION_METADATA
from orchestrator import run_cycle
from simulation import run_negotiation_simulation
from exporters.pdf_report import generate_pdf_report, generate_text_report

console = Console()


def print_banner():
    console.print(Panel.fit(
        "[bold blue]SWARM — ESSAIM DE 50 AGENTS AUTONOMES[/bold blue]\n"
        "[dim]Architecture: 5 Divisions × (1 Manager + 9 Exécuteurs)[/dim]",
        border_style="blue",
    ))


def print_agent_roster():
    table = Table(title="Cartographie des 50 Agents", box=box.ROUNDED, show_lines=True)
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Division", style="magenta", width=28)
    table.add_column("Rôle", style="white")
    table.add_column("Type", style="yellow", width=10)

    for agent in ALL_AGENTS:
        div = DIVISION_METADATA[agent.division]
        agent_type = "[bold]Manager[/bold]" if agent.is_manager else "Exécuteur"
        table.add_row(
            agent.id,
            f"{div['emoji']} {div['name']}",
            agent.role,
            agent_type,
        )

    console.print(table)
    console.print(f"\n[green]Total: {len(ALL_AGENTS)} agents configurés[/green]")


def print_cycle_results(state: dict):
    console.print("\n")
    console.print(Panel(
        f"[bold green]Cycle terminé : {state['cycle_id']}[/bold green]\n"
        f"Démarré : {state['started_at']}\n"
        f"Prospects détectés : [cyan]{len(state['fiches_detected'])}[/cyan]\n"
        f"Emails envoyés : [cyan]{len(state['outreach_queue'])}[/cyan]\n"
        f"Threads négociation : [cyan]{len(state['negotiation_threads'])}[/cyan]\n"
        f"Jobs production : [cyan]{len(state['production_jobs'])}[/cyan]\n"
        f"CA généré : [bold green]{state['revenue_today']}€[/bold green]\n"
        f"Erreurs : [red]{len(state['errors'])}[/red]",
        title="Résultats du Cycle",
        border_style="green",
    ))

    # Division status table
    table = Table(title="Statut des Divisions", box=box.SIMPLE)
    table.add_column("Division")
    table.add_column("Statut")
    for div_id, status in state["division_status"].items():
        meta = DIVISION_METADATA[div_id]
        color = "green" if status == "success" else "red" if status == "error" else "yellow"
        table.add_row(
            f"{meta['emoji']} {meta['name']}",
            f"[{color}]{status}[/{color}]",
        )
    console.print(table)

    if state["errors"]:
        console.print("\n[red]Erreurs détectées :[/red]")
        for err in state["errors"]:
            console.print(f"  • {err}")


async def main():
    parser = argparse.ArgumentParser(description="SWARM — Orchestrateur d'agents autonomes")
    parser.add_argument("--loop", action="store_true", help="Mode continu (cycle toutes les heures)")
    parser.add_argument("--status", action="store_true", help="Affiche la cartographie des 50 agents")
    parser.add_argument("--simulate-sale", action="store_true", help="Simule dialogue Agent 3.5 ↔ 5.1")
    parser.add_argument("--output-json", type=str, help="Exporte les résultats en JSON vers ce fichier")
    parser.add_argument("--output-pdf", type=str, help="Génère un rapport PDF/HTML dans ce dossier")
    args = parser.parse_args()

    print_banner()

    if args.status:
        print_agent_roster()
        return

    if args.simulate_sale:
        await run_negotiation_simulation(console)
        return

    if args.loop:
        console.print("[yellow]Mode continu activé — cycle toutes les 3600 secondes[/yellow]")
        while True:
            state = await run_cycle()
            print_cycle_results(state)
            if args.output_json:
                with open(args.output_json, "w") as f:
                    json.dump(state, f, indent=2, default=str)
            if args.output_pdf:
                path = generate_pdf_report(state, output_dir=args.output_pdf)
                console.print(f"[green]Rapport généré : {path}[/green]")
            console.print("[dim]Prochain cycle dans 3600s...[/dim]")
            await asyncio.sleep(3600)
    else:
        state = await run_cycle()
        print_cycle_results(state)
        if args.output_json:
            with open(args.output_json, "w") as f:
                json.dump(state, f, indent=2, default=str)
        if args.output_pdf:
            path = generate_pdf_report(state, output_dir=args.output_pdf)
            console.print(f"[green]Rapport généré : {path}[/green]")


if __name__ == "__main__":
    asyncio.run(main())
