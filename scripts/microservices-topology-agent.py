#!/usr/bin/env python3
"""Microservices Topology Agent — CaelumSwarm™ Dev Support
Cartographie la topologie de microservices : dépendances entre engines,
flux de données, points de défaillance uniques (SPOF), recommandations de résilience.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

AGENT_NAME = "MicroservicesTopologyAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

CSDDD_DOMAINS = {
    "forced_labor": ["prison_labor", "debt_bondage", "human_trafficking", "child_soldiers"],
    "environment": ["toxic_waste", "deforestation_palm_oil", "water_pollution", "crypto_energy"],
    "supply_chain": ["conflict_minerals", "artisanal_mining", "ocean_fishing", "land_grabbing"],
    "digital_rights": ["ai_algorithmic_bias", "biometric_surveillance", "genetic_data", "surveillance_capitalism"],
    "social_rights": ["gig_workers", "gender_pay_gap", "disability_rights", "mental_health"],
    "governance": ["corporate_tax_evasion", "colonial_reparations", "media_censorship", "dark_patterns"],
}


def map_engine_to_domain(engine_name: str) -> str:
    for domain, keywords in CSDDD_DOMAINS.items():
        for kw in keywords:
            if kw in engine_name:
                return domain
    return "other"


def analyze_topology(root: Path) -> dict:
    engine_files = list((root / "swarm" / "intelligence").glob("*_engine.py"))
    route_files = list((root / "app" / "api").rglob("route.ts"))

    # Grouper par domaine CSDDD
    domain_groups = defaultdict(list)
    for engine in engine_files:
        domain = map_engine_to_domain(engine.stem)
        domain_groups[domain].append(engine.stem)

    # Analyser le SWARM_API_URL comme SPOF
    spofs = []
    swarm_url_count = 0
    for route in route_files:
        source = route.read_text(encoding="utf-8", errors="ignore")
        if "SWARM_API_URL" in source:
            swarm_url_count += 1

    if swarm_url_count > 10:
        spofs.append({
            "component": "SWARM_API_URL",
            "severity": "HIGH",
            "impact": f"{swarm_url_count} routes dépendent d'un seul upstream",
            "mitigation": "Ajouter un circuit breaker et un fallback local (FALLBACK_ENTITIES)"
        })

    # Vérifier les fallbacks
    fallback_count = 0
    no_fallback = []
    for route in route_files:
        source = route.read_text(encoding="utf-8", errors="ignore")
        if "FALLBACK" in source or "fallback" in source or "entities: []" in source:
            fallback_count += 1
        else:
            no_fallback.append(route.parent.name)

    return {
        "total_engines": len(engine_files),
        "total_routes": len(route_files),
        "domain_groups": dict(domain_groups),
        "spofs": spofs,
        "fallback_coverage": f"{fallback_count}/{len(route_files)}",
        "no_fallback": no_fallback[:5],
    }


def generate_mermaid_diagram(topology: dict) -> str:
    """Génère un diagramme Mermaid de la topologie."""
    lines = [
        "```mermaid",
        "graph TD",
        "    Client[🌐 Browser] --> Sidebar[📋 Sidebar Navigation]",
        "    Sidebar --> Dashboard[📊 Dashboards]",
        "    Dashboard --> API[🔌 API Routes /api/*]",
        "    API --> Seal[🔒 sealResponse]",
        "    API --> SWARM[(🌐 SWARM_API_URL)]",
        "    API --> Fallback[⚡ FALLBACK_ENTITIES]",
        "    SWARM --> Engines[🤖 CaelumSwarm Engines]",
    ]

    for domain, engines in list(topology.get("domain_groups", {}).items())[:5]:
        domain_id = domain.replace("_", "")
        lines.append(f"    Engines --> {domain_id}[{domain}]")
        for eng in engines[:2]:
            eng_id = eng.replace("_", "")[:20]
            lines.append(f"    {domain_id} --> {eng_id}[{eng[:25]}]")

    lines.append("    style Fallback fill:#1e293b,stroke:#f97316")
    lines.append("    style Seal fill:#1e293b,stroke:#22c55e")
    lines.append("```")

    return "\n".join(lines)


def run_agent(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Microservices Topology Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    topology = analyze_topology(root)

    print(f"{BOLD}Topologie CaelumSwarm™ :{RESET}")
    print(f"  Total engines  : {topology['total_engines']}")
    print(f"  Total routes   : {topology['total_routes']}")
    print(f"  Fallback cover.: {topology['fallback_coverage']}")

    print(f"\n{BOLD}Groupes de domaines CSDDD :{RESET}")
    for domain, engines in topology["domain_groups"].items():
        print(f"  {domain:<20} {len(engines):3d} engines")

    if topology["spofs"]:
        print(f"\n{BOLD}{RED}Points de défaillance uniques (SPOF) :{RESET}")
        for spof in topology["spofs"]:
            print(f"  {RED}[{spof['severity']}]{RESET} {spof['component']}: {spof['impact']}")
            print(f"    → Mitigation: {spof['mitigation']}")

    if topology["no_fallback"]:
        print(f"\n{YELLOW}Routes sans fallback :{RESET}")
        for route in topology["no_fallback"]:
            print(f"  ⚠ {route}")

    print(f"\n{BOLD}Diagramme Mermaid :{RESET}")
    print(generate_mermaid_diagram(topology))

    print(f"\n{BOLD}Recommandations de résilience :{RESET}")
    recs = [
        "🔄 Implémenter un circuit breaker pour SWARM_API_URL (ex: avec opossum npm)",
        "⚡ Toutes les routes doivent avoir FALLBACK_ENTITIES avec données réalistes",
        "📊 Ajouter des health checks : /api/health retournant {status, version, engines_count}",
        "🔀 Envisager un load balancer si >5 instances SWARM_API_URL",
        "📈 Instrumenter avec OpenTelemetry pour tracer les appels engine→API→dashboard",
        "🛡️ Rate limiting sur /api/* avec next-rate-limit ou Vercel Edge middleware",
    ]
    for rec in recs:
        print(f"  {rec}")
    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "topology": topology,
        "mermaid_diagram": generate_mermaid_diagram(topology),
        "recommendations": recs,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_agent(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
