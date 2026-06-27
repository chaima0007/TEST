#!/usr/bin/env python3
"""
CaelumSwarm — Business Plan & Objectifs Journaliers par Infrastructure
Chaque infrastructure a son propre plan, ses KPIs et ses objectifs quotidiens.
"""

import json
from pathlib import Path
from datetime import datetime, date, timedelta

ROOT = Path(__file__).parent.parent
PLAN_LOG = ROOT / "data" / "business_plan_daily_log.json"

# ─── 7 Infrastructures de CaelumSwarm ────────────────────────────────────────

INFRASTRUCTURES = {

    "ENGINE": {
        "name": "Engine Infrastructure (Python Swarm)",
        "description": "Moteurs d'analyse IA — cerveau de CaelumSwarm",
        "business_objective": "Devenir la base de données CSDDD la plus complète au monde (objectif : 5 000 engines d'ici 2027)",
        "revenue_link": "Chaque engine = 1 domaine vendable à des clients compliance (€500-2000/domaine/an)",
        "daily_targets": {
            "engines_new": 3,              # Engines à créer par jour
            "avg_composite_target": 61.03, # Constante à maintenir
            "validation_passes": 3,        # 3 engines validés python3 engine.py ✓
            "zero_errors": True,           # Aucune erreur Python
        },
        "weekly_targets": {
            "engines_new": 21,
            "waves_completed": 7,
        },
        "kpis": {
            "total_engines": None,         # Rempli dynamiquement
            "target_2025": 2500,
            "target_2026": 4000,
            "target_2027": 5000,
        },
        "protocols": ["§9 constantes", "§10 tentatives d'étude", "§12 multi-POV", "§13 multivers"],
    },

    "API": {
        "name": "API Infrastructure (Next.js Routes)",
        "description": "Routes REST sécurisées — pont entre engines et dashboards",
        "business_objective": "API zéro downtime avec 100% de conformité sécurité",
        "revenue_link": "Les routes API permettent l'intégration client via webhook/API key (€200/mois/client)",
        "daily_targets": {
            "routes_new": 3,               # Routes à créer par wave
            "security_pattern_100pct": True,  # sealResponse + SWARM_API_URL + 502 + revalidate:30
            "zero_503": True,              # Jamais de 503 (seulement 502)
            "zero_credentials": True,      # Zéro credentials dans le code
        },
        "weekly_targets": {
            "routes_new": 21,
            "security_audit_passed": True,
        },
        "kpis": {
            "total_routes": None,
            "target_2025": 400,
            "target_2026": 700,
            "target_2027": 1000,
        },
        "protocols": ["Pattern sécurité API", "revalidate:30", "sealResponse"],
    },

    "DASHBOARD": {
        "name": "Dashboard Infrastructure (React Pages)",
        "description": "Tableaux de bord visuels — interface client CaelumSwarm",
        "business_objective": "UI/UX de référence pour la compliance CSDDD (NPS cible : >70)",
        "revenue_link": "Les dashboards sont le produit visible — conversion trial→payant dépend de leur qualité",
        "daily_targets": {
            "dashboards_new": 3,
            "use_client_100pct": True,
            "gaugering_r36": True,         # Pattern GaugeRing exact
            "zero_useCallback": True,
            "zero_useMemo": True,
            "payload_fallback": True,
        },
        "weekly_targets": {
            "dashboards_new": 21,
            "build_zero_errors": True,
        },
        "kpis": {
            "total_dashboards": None,
            "target_2025": 500,
            "target_2026": 800,
            "target_2027": 1200,
        },
        "protocols": ["use client", "GaugeRing r=36", "payload ??", "§fix_dashboard_hooks"],
    },

    "SIDEBAR": {
        "name": "Sidebar Infrastructure (Navigation)",
        "description": "Navigation principale — expérience utilisateur et découverte des domaines",
        "business_objective": "Navigation fluide <100ms pour 1200+ domaines sans OOM",
        "revenue_link": "La sidebar oriente vers les domaines achetés — impact direct sur upsell",
        "daily_targets": {
            "icons_new": 3,                # Icônes à ajouter par wave
            "zero_duplicates": True,       # Zéro doublon entre tous les fichiers
            "max_file_lines": 4400,        # Seuil alerte (80% OOM)
            "split_if_needed": True,       # Auto-split si > 4400L
        },
        "weekly_targets": {
            "icons_new": 21,
            "split_preventive": "si fichier > 4000L",
        },
        "kpis": {
            "total_icons": None,
            "icon_files": None,
            "max_file_lines_current": None,
            "target_zero_oom": True,
        },
        "protocols": ["§7 split automatique", "grep doublons", "scalability_guardian"],
    },

    "PROTOCOL": {
        "name": "Protocol Infrastructure (Scripts & Automation)",
        "description": "Cerveaux opérationnels — toutes les commandes intégrées dans le programme",
        "business_objective": "0 erreur manuelle, 100% automatisé, audit complet à chaque wave",
        "revenue_link": "La qualité du protocole = la fiabilité du produit = la confiance client",
        "daily_targets": {
            "guardian_passing": True,      # scalability_guardian.py → OK
            "constants_stable": True,      # constants_monitor.py → STABLE
            "multi_pov_validated": True,   # multi_perspective_simulator.py → OK
            "orchestrator_clean": True,    # wave_orchestrator.py --post → 8/8 checks OK
            "zero_uncommitted": True,      # git status --short → propre
        },
        "weekly_targets": {
            "protocol_docs_updated": True,
            "new_section_if_new_pattern": True,
        },
        "kpis": {
            "scripts_count": None,
            "protocol_sections": None,
            "last_audit_status": None,
        },
        "protocols": ["AGENTS.md", "wave-development-protocol.md", "§1→§13"],
    },

    "DATA": {
        "name": "Data Infrastructure (JSON Logs & Reports)",
        "description": "Mémoire persistante — historique des simulations, audits, rapports",
        "business_objective": "Traçabilité complète et données exploitables pour le reporting CSDDD",
        "revenue_link": "Les données historiques permettent le reporting automatique vendu aux clients (€500+/rapport)",
        "daily_targets": {
            "zero_file_over_50mb": True,   # Aucun fichier JSON > 50MB
            "study_attempts_logged": True, # Toutes tentatives dans study_attempts_log.json
            "mpov_logged": True,           # Tous multi-POV dans multi_perspective_log.json
            "max_log_entries": 500,        # Rotation automatique (500 entrées max)
        },
        "weekly_targets": {
            "archive_if_over_10mb": True,
            "cleanup_old_reports": True,
        },
        "kpis": {
            "total_data_mb": None,
            "study_attempts_count": None,
            "max_file_mb": None,
            "target_max_50mb": True,
        },
        "protocols": ["§10 study_attempts_log", "§13 multi_perspective_log", "rotation 500 entrées"],
    },

    "BUILD": {
        "name": "Build Infrastructure (Vercel CI/CD)",
        "description": "Pipeline de déploiement — qualité de production garantie",
        "business_objective": "Build vert en <120s, zéro erreur TypeScript/Turbopack en production",
        "revenue_link": "Un build cassé = indisponibilité produit = perte clients. SLA: 99.9% uptime",
        "daily_targets": {
            "build_green": True,           # CI Vercel verte
            "build_time_max_seconds": 120, # Build < 2 minutes
            "zero_typescript_errors": True,
            "zero_turbopack_errors": True,
            "node_options_set": True,      # NODE_OPTIONS=--max-old-space-size=4096
        },
        "weekly_targets": {
            "no_regression": True,
            "memory_audit": True,          # Vérifier heap usage avec --experimental-debug-memory-usage
        },
        "kpis": {
            "last_build_status": None,
            "last_build_seconds": None,
            "errors_this_week": None,
            "target_build_green": True,
        },
        "protocols": ["next.config.ts webpackMemoryOptimizations", "NODE_OPTIONS 4096", "productionBrowserSourceMaps:false"],
    },
}

# ─── Collecte des métriques dynamiques ───────────────────────────────────────

def collect_live_kpis() -> dict:
    kpis = {}

    # ENGINE
    engine_dir = ROOT / "swarm" / "intelligence"
    kpis["ENGINE"] = {
        "total_engines": len(list(engine_dir.glob("*_engine.py"))) if engine_dir.exists() else 0,
        "size_mb": round(sum(f.stat().st_size for f in engine_dir.glob("*.py")) / 1_048_576, 1) if engine_dir.exists() else 0,
    }

    # API
    api_dir = ROOT / "app" / "api"
    kpis["API"] = {
        "total_routes": len(list(api_dir.rglob("route.ts"))) if api_dir.exists() else 0,
    }

    # DASHBOARD
    dash_dir = ROOT / "app" / "dashboard"
    kpis["DASHBOARD"] = {
        "total_dashboards": len(list(dash_dir.rglob("page.tsx"))) if dash_dir.exists() else 0,
    }

    # SIDEBAR
    comp_dir = ROOT / "components"
    icon_files = list(comp_dir.glob("sidebar-icons*.tsx")) if comp_dir.exists() else []
    total_icons = 0
    max_lines = 0
    for f in icon_files:
        try:
            content = f.read_text()
            lines = len(content.splitlines())
            icons = len([l for l in content.splitlines() if l.startswith("export function Icon")])
            total_icons += icons
            max_lines = max(max_lines, lines)
        except Exception:
            pass
    kpis["SIDEBAR"] = {
        "total_icons": total_icons,
        "icon_files": len(icon_files),
        "max_file_lines": max_lines,
        "oom_risk_pct": round(max_lines / 5500 * 100, 1),
    }

    # PROTOCOL
    scripts_dir = ROOT / "scripts"
    kpis["PROTOCOL"] = {
        "scripts_count": len(list(scripts_dir.glob("*.py"))) if scripts_dir.exists() else 0,
    }

    # DATA
    data_dir = ROOT / "data"
    if data_dir.exists():
        files = list(data_dir.glob("*.json"))
        total_mb = sum(f.stat().st_size for f in files) / 1_048_576
        max_mb = max((f.stat().st_size / 1_048_576 for f in files), default=0)
        try:
            attempts = json.loads((data_dir / "study_attempts_log.json").read_text()) if (data_dir / "study_attempts_log.json").exists() else []
        except Exception:
            attempts = []
        kpis["DATA"] = {
            "total_data_mb": round(total_mb, 2),
            "max_file_mb": round(max_mb, 2),
            "study_attempts_count": len(attempts),
            "files_count": len(files),
        }
    else:
        kpis["DATA"] = {"total_data_mb": 0}

    # BUILD (statique — Vercel est externe)
    kpis["BUILD"] = {
        "node_options_set": "max-old-space-size" in (ROOT / "package.json").read_text() if (ROOT / "package.json").exists() else False,
        "webpack_opts": "webpackMemoryOptimizations" in (ROOT / "next.config.ts").read_text() if (ROOT / "next.config.ts").exists() else False,
    }

    return kpis

# ─── Calcul du score journalier par infrastructure ────────────────────────────

def compute_daily_score(infra_key: str, live_kpis: dict) -> dict:
    infra = INFRASTRUCTURES[infra_key]
    kpi = live_kpis.get(infra_key, {})
    targets = infra["daily_targets"]
    checks = {}

    if infra_key == "ENGINE":
        checks["engines_present"] = kpi.get("total_engines", 0) > 0
        checks["size_reasonable"] = kpi.get("size_mb", 0) < 50
    elif infra_key == "API":
        checks["routes_present"] = kpi.get("total_routes", 0) > 0
        checks["routes_growing"] = kpi.get("total_routes", 0) > 100
    elif infra_key == "DASHBOARD":
        checks["dashboards_present"] = kpi.get("total_dashboards", 0) > 0
        checks["dashboards_growing"] = kpi.get("total_dashboards", 0) > 100
    elif infra_key == "SIDEBAR":
        checks["icons_present"] = kpi.get("total_icons", 0) > 0
        checks["no_oom_risk"] = kpi.get("oom_risk_pct", 100) < 80
        checks["multiple_files"] = kpi.get("icon_files", 0) >= 5
    elif infra_key == "PROTOCOL":
        checks["scripts_present"] = kpi.get("scripts_count", 0) >= 5
        checks["key_scripts"] = all(
            (ROOT / "scripts" / s).exists()
            for s in ["scalability_guardian.py", "constants_monitor.py",
                      "multi_perspective_simulator.py", "wave_orchestrator.py"]
        )
    elif infra_key == "DATA":
        checks["data_exists"] = kpi.get("total_data_mb", 0) > 0
        checks["no_oversized_files"] = kpi.get("max_file_mb", 0) < 50
        checks["study_attempts_tracked"] = kpi.get("study_attempts_count", 0) > 0
    elif infra_key == "BUILD":
        checks["node_options_set"] = kpi.get("node_options_set", False)
        checks["webpack_optimized"] = kpi.get("webpack_opts", False)

    score = round(sum(checks.values()) / len(checks) * 100) if checks else 0
    return {"checks": checks, "score": score, "status": "✓" if score >= 80 else "⚠" if score >= 50 else "✗"}

# ─── Rapport journalier ───────────────────────────────────────────────────────

def run_daily_report(verbose: bool = True) -> dict:
    live_kpis = collect_live_kpis()
    today = date.today().isoformat()

    if verbose:
        print(f"\n{'═'*60}")
        print(f"  BUSINESS PLAN JOURNALIER — CaelumSwarm")
        print(f"  {today}")
        print(f"{'═'*60}")

    report = {"date": today, "timestamp": datetime.utcnow().isoformat(), "infrastructures": {}}

    for key, infra in INFRASTRUCTURES.items():
        score_data = compute_daily_score(key, live_kpis)
        kpi = live_kpis.get(key, {})

        report["infrastructures"][key] = {
            "name": infra["name"],
            "score": score_data["score"],
            "status": score_data["status"],
            "kpis_live": kpi,
            "daily_targets": infra["daily_targets"],
            "checks": score_data["checks"],
        }

        if verbose:
            s = score_data["status"]
            print(f"\n  {s} {infra['name']}")
            print(f"     Score : {score_data['score']}%")
            # KPIs live
            for k, v in kpi.items():
                print(f"     {k:<30} : {v}")
            # Objectifs journaliers clés
            print(f"     Objectifs/jour :", end="")
            targets_str = " · ".join(f"{k}={v}" for k, v in list(infra["daily_targets"].items())[:3])
            print(f" {targets_str}")
            # Lien revenus
            print(f"     💰 {infra['revenue_link'][:70]}")

    # Score global
    scores = [v["score"] for v in report["infrastructures"].values()]
    global_score = round(sum(scores) / len(scores))
    report["global_score"] = global_score
    report["global_status"] = "✓ OPTIMAL" if global_score >= 80 else "⚠ AMÉLIORATION" if global_score >= 60 else "✗ CRITIQUE"

    if verbose:
        print(f"\n{'─'*60}")
        print(f"  SCORE GLOBAL : {global_score}% — {report['global_status']}")
        print(f"\n  OBJECTIFS JOURNALIERS PRIORITAIRES")
        print(f"  1. 3 nouveaux engines (avg_composite=61.03 garanti)")
        print(f"  2. 3 routes API (pattern sécurité 100%)")
        print(f"  3. 3 dashboards React (zéro useCallback/useMemo)")
        print(f"  4. Build Vercel vert en <120s")
        print(f"  5. python3 scripts/wave_orchestrator.py --wave N --post → 8/8 OK")
        print(f"{'═'*60}")

    # Sauvegarder
    PLAN_LOG.parent.mkdir(parents=True, exist_ok=True)
    log = []
    if PLAN_LOG.exists():
        try:
            log = json.loads(PLAN_LOG.read_text())
        except Exception:
            log = []
    log.append(report)
    log = log[-90:]  # 90 jours d'historique
    PLAN_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))

    return report

# ─── Point d'entrée ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_daily_report(verbose=True)
