#!/usr/bin/env python3
"""Bundle Size Monitor Agent — CaelumSwarm™ Dev Support
Analyse la taille du bundle Next.js, détecte les pages/composants lourds,
suggère des optimisations (dynamic import, image optimization, tree-shaking).
"""
import os
import json
import re
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "BundleSizeMonitorAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

SIZE_WARNING_KB = 100
SIZE_CRITICAL_KB = 250


def get_file_size_kb(path: Path) -> float:
    return path.stat().st_size / 1024


def analyze_next_build(root: Path) -> dict:
    """Analyse le dossier .next/static si disponible."""
    next_dir = root / ".next"
    if not next_dir.exists():
        return {"status": "no_build", "message": "Pas de build .next trouvé — lancer 'npm run build' d'abord"}

    results = {"status": "analyzed", "chunks": [], "pages": []}

    # Analyse des chunks JS
    chunks_dir = next_dir / "static" / "chunks"
    if chunks_dir.exists():
        for f in sorted(chunks_dir.rglob("*.js")):
            size_kb = get_file_size_kb(f)
            results["chunks"].append({
                "file": f.name,
                "size_kb": round(size_kb, 2),
                "severity": "CRITICAL" if size_kb > SIZE_CRITICAL_KB else "WARNING" if size_kb > SIZE_WARNING_KB else "OK"
            })
        results["chunks"].sort(key=lambda x: x["size_kb"], reverse=True)

    return results


def analyze_source_size(root: Path) -> dict:
    """Analyse la taille des fichiers source pour identifier les fichiers lourds."""
    results = {"heavy_files": [], "total_dashboard_kb": 0, "total_api_kb": 0}

    # Dashboards
    for f in sorted((root / "app" / "dashboard").rglob("page.tsx")):
        size_kb = get_file_size_kb(f)
        results["total_dashboard_kb"] += size_kb
        if size_kb > 15:  # Dashboard > 15KB = potentiellement lourd
            parent = f.parent.name
            results["heavy_files"].append({
                "file": f"dashboard/{parent}/page.tsx",
                "size_kb": round(size_kb, 2),
                "issue": "Dashboard trop lourd — envisager découpage en composants"
            })

    # API routes
    for f in sorted((root / "app" / "api").rglob("route.ts")):
        size_kb = get_file_size_kb(f)
        results["total_api_kb"] += size_kb

    # Sidebar (fichier le plus critique)
    sidebar = root / "components" / "Sidebar.tsx"
    if sidebar.exists():
        size_kb = get_file_size_kb(sidebar)
        results["sidebar_size_kb"] = round(size_kb, 2)
        if size_kb > 200:
            results["heavy_files"].append({
                "file": "components/Sidebar.tsx",
                "size_kb": round(size_kb, 2),
                "issue": f"Sidebar {size_kb:.1f}KB — envisager lazy loading des icônes SVG"
            })

    results["total_dashboard_kb"] = round(results["total_dashboard_kb"], 2)
    results["total_api_kb"] = round(results["total_api_kb"], 2)

    return results


def generate_recommendations(source_analysis: dict, build_analysis: dict) -> list[str]:
    recs = []

    if source_analysis.get("sidebar_size_kb", 0) > 100:
        recs.append("🔧 Sidebar.tsx > 100KB : utiliser React.lazy() pour les icônes SVG rarement utilisées")

    if source_analysis.get("heavy_files"):
        recs.append(f"📦 {len(source_analysis['heavy_files'])} dashboards lourds : extraire FALLBACK_ENTITIES dans des fichiers data séparés")

    if build_analysis.get("status") == "no_build":
        recs.append("🏗️ Lancer 'npm run build' pour analyser le bundle de production")
    else:
        critical_chunks = [c for c in build_analysis.get("chunks", []) if c["severity"] == "CRITICAL"]
        if critical_chunks:
            recs.append(f"⚠️ {len(critical_chunks)} chunks > {SIZE_CRITICAL_KB}KB : envisager code splitting dynamique")

    recs.append("💡 Utiliser 'next/dynamic' pour les composants lourds chargés conditionnellement")
    recs.append("🖼️ Vérifier que toutes les images utilisent next/image avec sizes appropriés")
    recs.append("📊 Activer 'bundleAnalyzer' dans next.config.js pour visualisation complète")

    return recs


def run_monitor(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Bundle Size Monitor v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}\n")

    source_analysis = analyze_source_size(root)
    build_analysis = analyze_next_build(root)
    recommendations = generate_recommendations(source_analysis, build_analysis)

    print(f"{BOLD}Analyse des sources :{RESET}")
    print(f"  Dashboards   : {source_analysis['total_dashboard_kb']:.1f} KB total")
    print(f"  API Routes   : {source_analysis['total_api_kb']:.1f} KB total")
    if "sidebar_size_kb" in source_analysis:
        sidebar_kb = source_analysis['sidebar_size_kb']
        color = RED if sidebar_kb > 200 else YELLOW if sidebar_kb > 100 else GREEN
        print(f"  Sidebar.tsx  : {color}{sidebar_kb:.1f} KB{RESET}")

    if source_analysis["heavy_files"]:
        print(f"\n{YELLOW}Fichiers lourds :{RESET}")
        for f in source_analysis["heavy_files"][:5]:
            print(f"  {YELLOW}⚠{RESET} {f['file']} ({f['size_kb']:.1f}KB) — {f['issue']}")

    if build_analysis["status"] != "no_build":
        print(f"\n{BOLD}Build .next analysé :{RESET}")
        for chunk in build_analysis.get("chunks", [])[:5]:
            color = RED if chunk["severity"] == "CRITICAL" else YELLOW if chunk["severity"] == "WARNING" else GREEN
            print(f"  {color}{chunk['size_kb']:7.1f}KB{RESET}  {chunk['file']}")
    else:
        print(f"\n{YELLOW}{build_analysis['message']}{RESET}")

    print(f"\n{BOLD}Recommandations :{RESET}")
    for rec in recommendations:
        print(f"  {rec}")

    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "source_analysis": source_analysis,
        "build_analysis": build_analysis,
        "recommendations": recommendations,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_monitor(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
