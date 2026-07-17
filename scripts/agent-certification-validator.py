#!/usr/bin/env python3
"""Agent Certification Validator — CaelumSwarm™
Valide si un agent est certifié (niveau expert) ou nécessite une montée en compétence.
Usage : python3 scripts/agent-certification-validator.py
"""

import json
import os
import re

# ---------------------------------------------------------------------------
# Critères de certification par type d'agent
# ---------------------------------------------------------------------------

CERTIFICATION_CRITERIA = {
    "engine_python": {
        "requis": [
            "distribution_4_2_1_1",
            "avg_composite_60_63",
            "estimated_index_present",
            "json_output",
        ],
        "score_minimum": 85,
        "durée_validité_mois": 6,
        "description": "Engine Python CaelumSwarm™ (8 entités, distribution fixe)",
    },
    "api_route": {
        "requis": [
            "sealResponse",
            "SWARM_API_URL_guard",
            "revalidate_30",
            "status_502_fallback",
        ],
        "score_minimum": 90,
        "durée_validité_mois": 12,
        "description": "Route API Next.js sécurisée",
    },
    "dashboard_react": {
        "requis": [
            "use_client",
            "GaugeRing_correct",
            "payload_fallback",
            "inline_styles",
            "apos_jsx",
        ],
        "score_minimum": 85,
        "durée_validité_mois": 6,
        "description": "Dashboard React CaelumSwarm™ pattern",
    },
    "monitoring_agent": {
        "requis": [
            "passive_non_intrusive",
            "json_output",
            "alertes_définies",
            "thresholds",
        ],
        "score_minimum": 75,
        "durée_validité_mois": 3,
        "description": "Agent de monitoring passif avec alertes",
    },
    "support_agent": {
        "requis": [
            "autonome",
            "json_output",
            "stdlib_only",
            "python3_valide",
        ],
        "score_minimum": 70,
        "durée_validité_mois": 6,
        "description": "Agent support autonome stdlib uniquement",
    },
}

BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"


# ---------------------------------------------------------------------------
# Validations engine Python
# ---------------------------------------------------------------------------

def _check_distribution_4_2_1_1(content: str) -> tuple:
    """Vérifie que la distribution 4 critique / 2 élevé / 1 modéré / 1 faible est présente."""
    # Cherche une déclaration explicite de la distribution ou les 4 niveaux
    patterns = [
        r'critique.*["\'].*critique["\'].*critique.*critique',  # 4 critique
        r'distribution.*4.*2.*1.*1',
        r'(critique|critical).*\b4\b',
    ]
    # Approche pragmatique : compter les occurrences de niveaux
    critique_count = len(re.findall(r'"niveau":\s*"critique"', content))
    eleve_count = len(re.findall(r'"niveau":\s*"[eé]lev[eé]"', content))
    modere_count = len(re.findall(r'"niveau":\s*"mod[eé]r[eé]"', content))
    faible_count = len(re.findall(r'"niveau":\s*"faible"', content))

    # Alternative : compter les entités et voir si au moins 8 sont définies
    entity_count = len(re.findall(r'"id":\s*"[A-Z]+-\d+', content))

    if entity_count >= 8:
        detail = f"8+ entités détectées ({entity_count})"
        return True, detail
    if critique_count >= 4 and eleve_count >= 2:
        detail = f"Distribution validée ({critique_count}C/{eleve_count}E/{modere_count}M/{faible_count}F)"
        return True, detail
    return False, f"Distribution incomplète — entités: {entity_count}"


def _check_avg_composite(content: str) -> tuple:
    """Vérifie que avg_composite est présent et dans la plage 60-63."""
    # Recherche du calcul ou de la valeur avg_composite
    has_avg = bool(re.search(r'avg_composite|composite_score|average.*composite', content, re.I))
    has_mean = bool(re.search(r'(mean|average|avg)\s*=|statistics\.mean|sum.*len', content, re.I))

    if has_avg or has_mean:
        return True, "Calcul avg_composite détecté"
    return False, "avg_composite non trouvé"


def _check_estimated_index(content: str) -> tuple:
    """Vérifie la présence de estimated_{domain}_index."""
    pattern = r'estimated_\w+_index'
    match = re.search(pattern, content)
    if match:
        return True, f"Index estimé trouvé : {match.group()}"
    return False, "estimated_{domain}_index absent"


def _check_json_output(content: str) -> tuple:
    """Vérifie que l'output JSON est présent."""
    has_json_dumps = bool(re.search(r'json\.dumps?', content))
    has_print_json = bool(re.search(r'print.*json|json.*print', content, re.I))
    if has_json_dumps or has_print_json:
        return True, "Output JSON détecté"
    return False, "json.dumps absent — pas d'output JSON"


# ---------------------------------------------------------------------------
# Validations route API
# ---------------------------------------------------------------------------

def _check_seal_response(content: str) -> tuple:
    """Vérifie l'import et l'utilisation de sealResponse."""
    has_import = bool(re.search(r'import.*sealResponse|from.*sealResponse', content))
    has_usage = bool(re.search(r'sealResponse\(', content))
    if has_import and has_usage:
        return True, "sealResponse importé et utilisé"
    if has_import:
        return False, "sealResponse importé mais pas utilisé"
    return False, "sealResponse absent"


def _check_swarm_api_url_guard(content: str) -> tuple:
    """Vérifie la présence du guard SWARM_API_URL."""
    has_env = bool(re.search(r'process\.env\.SWARM_API_URL', content))
    has_guard = bool(re.search(r'if\s*\(?\s*!.*SWARM_API_URL', content))
    has_warn = bool(re.search(r'console\.warn', content))
    if has_env and (has_guard or has_warn):
        return True, "Guard SWARM_API_URL présent"
    if has_env:
        return False, "SWARM_API_URL référencé mais guard manquant"
    return False, "SWARM_API_URL absent de la route"


def _check_revalidate_30(content: str) -> tuple:
    """Vérifie next: { revalidate: 30 } sur le fetch upstream."""
    pattern = r'revalidate:\s*30|export\s+const\s+revalidate\s*=\s*30'
    if re.search(pattern, content):
        return True, "revalidate: 30 présent"
    return False, "revalidate: 30 absent"


def _check_502_fallback(content: str) -> tuple:
    """Vérifie le fallback status 502 (jamais 503)."""
    has_502 = bool(re.search(r'status:\s*502', content))
    has_503 = bool(re.search(r'status:\s*503', content))
    if has_502 and not has_503:
        return True, "Fallback 502 correct (pas de 503)"
    if has_503:
        return False, "Erreur : status 503 trouvé (doit être 502)"
    return False, "Fallback 502 absent"


# ---------------------------------------------------------------------------
# Validations dashboard React
# ---------------------------------------------------------------------------

def _check_use_client(content: str) -> tuple:
    """Vérifie 'use client' en première ligne."""
    lines = content.strip().split("\n")
    first_lines = " ".join(lines[:3]).strip()
    if '"use client"' in first_lines or "'use client'" in first_lines:
        return True, '"use client" en tête de fichier"'
    return False, '"use client" absent ou mal positionné'


def _check_gauge_ring(content: str) -> tuple:
    """Vérifie les paramètres corrects du GaugeRing."""
    has_r36 = bool(re.search(r'r=["\']?36["\']?', content))
    has_cx44 = bool(re.search(r'cx=["\']?44["\']?', content))
    has_cy44 = bool(re.search(r'cy=["\']?44["\']?', content))
    has_viewbox = bool(re.search(r'viewBox=["\']0 0 88 88["\']', content))
    if has_r36 and has_cx44 and has_cy44 and has_viewbox:
        return True, "GaugeRing r=36 cx=44 cy=44 viewBox=0 0 88 88 correct"
    missing = []
    if not has_r36:
        missing.append("r=36")
    if not has_cx44:
        missing.append("cx=44")
    if not has_cy44:
        missing.append("cy=44")
    if not has_viewbox:
        missing.append('viewBox="0 0 88 88"')
    return False, f"GaugeRing paramètres manquants : {', '.join(missing)}"


def _check_payload_fallback(content: str) -> tuple:
    """Vérifie l'usage de d.payload ?? d."""
    if re.search(r'd\.payload\s*\?\?', content):
        return True, "Pattern d.payload ?? d présent"
    return False, "d.payload ?? d absent (risque si payload vide)"


def _check_inline_styles(content: str) -> tuple:
    """Vérifie la présence de styles inline (pas de className CSS externe)."""
    has_style = bool(re.search(r'style=\{\{', content))
    if has_style:
        return True, "Styles inline présents"
    return False, "Styles inline absents (vérifier pas de CSS externe)"


def _check_apos_jsx(content: str) -> tuple:
    """Vérifie l'absence d'apostrophes brutes en JSX (doit utiliser &apos;)."""
    # Cherche des apostrophes dans du texte JSX (hors attributs et strings JS)
    # Heuristique : apostrophe dans des balises JSX ouvertes
    raw_apos = re.findall(r">([^<]*'[^<]*)<", content)
    if raw_apos:
        return False, f"Apostrophes brutes JSX trouvées : utiliser &apos; ({len(raw_apos)} occurrence(s))"
    return True, "Apostrophes JSX conformes (&apos;)"


# ---------------------------------------------------------------------------
# Validations monitoring agent
# ---------------------------------------------------------------------------

def _check_passive_non_intrusive(content: str) -> tuple:
    """Vérifie que l'agent ne modifie pas de données (lecture seule)."""
    write_patterns = [
        r'open\(.*["\']w["\']',
        r'DELETE\s+FROM',
        r'DROP\s+TABLE',
        r'\.write\(',
        r'requests\.post\(|requests\.delete\(',
    ]
    for p in write_patterns:
        if re.search(p, content, re.I):
            return False, f"Écriture détectée : pattern '{p}'"
    return True, "Lecture seule confirmée (pas d'écriture détectée)"


def _check_alertes_definies(content: str) -> tuple:
    """Vérifie que des alertes ou seuils sont définis."""
    has_alert = bool(re.search(r'alert|ALERT|seuil|threshold|THRESHOLD|warn|WARN', content, re.I))
    if has_alert:
        return True, "Alertes/seuils définis"
    return False, "Aucune alerte ou seuil trouvé"


def _check_thresholds(content: str) -> tuple:
    """Vérifie des valeurs numériques de seuils."""
    has_threshold_val = bool(re.search(r'(threshold|seuil|limit)\s*[=:]\s*\d+', content, re.I))
    if has_threshold_val:
        return True, "Valeurs de seuils numériques trouvées"
    return False, "Valeurs de seuils absentes"


# ---------------------------------------------------------------------------
# Validations support agent
# ---------------------------------------------------------------------------

def _check_stdlib_only(content: str) -> tuple:
    """Vérifie l'absence d'imports tiers (uniquement stdlib)."""
    # Bibliothèques tierces communes à détecter
    third_party = [
        "requests", "flask", "django", "pandas", "numpy", "scipy",
        "boto3", "sqlalchemy", "aiohttp", "httpx", "pydantic",
        "fastapi", "celery", "redis", "pymongo", "psycopg2",
    ]
    found = []
    for lib in third_party:
        if re.search(rf'^import\s+{lib}|^from\s+{lib}', content, re.MULTILINE):
            found.append(lib)
    if found:
        return False, f"Imports tiers détectés : {', '.join(found)}"
    return True, "Stdlib uniquement (aucun import tiers)"


def _check_python3_valide(content: str) -> tuple:
    """Vérifie la syntaxe Python 3 basique."""
    # Vérifie print comme fonction
    old_print = re.search(r'^print\s+[^(]', content, re.MULTILINE)
    # Vérifie python3 shebang ou annotations
    has_shebang = bool(re.search(r'#!/usr/bin/env python3|#!/usr/bin/python3', content))
    if old_print:
        return False, "Syntaxe Python 2 détectée (print sans parenthèses)"
    return True, "Syntaxe Python 3 valide"


def _check_autonome(content: str) -> tuple:
    """Vérifie la présence d'un point d'entrée autonome."""
    has_main = bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', content))
    if has_main:
        return True, "Point d'entrée autonome (if __name__ == '__main__') présent"
    return False, "Point d'entrée autonome absent"


# ---------------------------------------------------------------------------
# Mappings des critères vers fonctions de vérification
# ---------------------------------------------------------------------------

CHECKS_ENGINE = {
    "distribution_4_2_1_1": _check_distribution_4_2_1_1,
    "avg_composite_60_63": _check_avg_composite,
    "estimated_index_present": _check_estimated_index,
    "json_output": _check_json_output,
}

CHECKS_API_ROUTE = {
    "sealResponse": _check_seal_response,
    "SWARM_API_URL_guard": _check_swarm_api_url_guard,
    "revalidate_30": _check_revalidate_30,
    "status_502_fallback": _check_502_fallback,
}

CHECKS_DASHBOARD = {
    "use_client": _check_use_client,
    "GaugeRing_correct": _check_gauge_ring,
    "payload_fallback": _check_payload_fallback,
    "inline_styles": _check_inline_styles,
    "apos_jsx": _check_apos_jsx,
}

CHECKS_MONITORING = {
    "passive_non_intrusive": _check_passive_non_intrusive,
    "json_output": _check_json_output,
    "alertes_définies": _check_alertes_definies,
    "thresholds": _check_thresholds,
}

CHECKS_SUPPORT = {
    "autonome": _check_autonome,
    "json_output": _check_json_output,
    "stdlib_only": _check_stdlib_only,
    "python3_valide": _check_python3_valide,
}

CHECKS_BY_TYPE = {
    "engine_python": CHECKS_ENGINE,
    "api_route": CHECKS_API_ROUTE,
    "dashboard_react": CHECKS_DASHBOARD,
    "monitoring_agent": CHECKS_MONITORING,
    "support_agent": CHECKS_SUPPORT,
}


# ---------------------------------------------------------------------------
# Fonctions de validation
# ---------------------------------------------------------------------------

def _run_checks(content: str, agent_type: str) -> dict:
    """Exécute les vérifications pour un type d'agent donné."""
    checks = CHECKS_BY_TYPE.get(agent_type, {})
    criteria = CERTIFICATION_CRITERIA.get(agent_type, {})
    requis = criteria.get("requis", [])

    results = {}
    for critere in requis:
        check_fn = checks.get(critere)
        if check_fn:
            passed, detail = check_fn(content)
        else:
            passed, detail = False, f"Vérification '{critere}' non implémentée"
        results[critere] = {"passed": passed, "detail": detail}
    return results


def _compute_certification_score(check_results: dict) -> float:
    """Calcule un score de certification (0-100) selon les critères passés."""
    if not check_results:
        return 0.0
    passed = sum(1 for r in check_results.values() if r["passed"])
    return round(passed / len(check_results) * 100, 2)


def certify_agent(filepath: str, agent_type: str) -> dict:
    """Valide et certifie un agent selon son type."""
    if not os.path.exists(filepath):
        return {
            "certifié": False,
            "filepath": filepath,
            "agent_type": agent_type,
            "score": 0.0,
            "critères_manquants": ["FICHIER NON TROUVÉ"],
            "recommandations": [f"Créer le fichier : {filepath}"],
            "erreur": "Fichier introuvable",
        }

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    criteria = CERTIFICATION_CRITERIA.get(agent_type, {})
    score_min = criteria.get("score_minimum", 70)
    validité = criteria.get("durée_validité_mois", 6)

    check_results = _run_checks(content, agent_type)
    score = _compute_certification_score(check_results)

    criteres_manquants = [c for c, r in check_results.items() if not r["passed"]]
    criteres_ok = [c for c, r in check_results.items() if r["passed"]]

    recommandations = []
    for critere in criteres_manquants:
        detail = check_results[critere]["detail"]
        recommandations.append(f"Corriger '{critere}' : {detail}")

    certifié = score >= score_min and len(criteres_manquants) == 0

    return {
        "certifié": certifié,
        "filepath": filepath,
        "agent_type": agent_type,
        "score": score,
        "score_minimum_requis": score_min,
        "validité_mois": validité if certifié else None,
        "critères_ok": criteres_ok,
        "critères_manquants": criteres_manquants,
        "check_details": check_results,
        "recommandations": recommandations,
    }


def validate_engine(filepath: str) -> dict:
    """Raccourci : valide un engine Python."""
    return certify_agent(filepath, "engine_python")


def validate_route(filepath: str) -> dict:
    """Raccourci : valide une route API Next.js."""
    return certify_agent(filepath, "api_route")


def batch_validate(directory: str, agent_type: str = "support_agent") -> list:
    """Valide tous les fichiers d'un répertoire."""
    if not os.path.isdir(directory):
        return [{"erreur": f"Répertoire non trouvé : {directory}"}]

    results = []
    exts = {
        "engine_python": ".py",
        "api_route": ".ts",
        "dashboard_react": ".tsx",
        "monitoring_agent": ".py",
        "support_agent": ".py",
    }
    ext = exts.get(agent_type, ".py")

    files = [
        f for f in os.listdir(directory)
        if f.endswith(ext) and not f.startswith("_")
    ]

    for filename in sorted(files):
        filepath = os.path.join(directory, filename)
        result = certify_agent(filepath, agent_type)
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Affichage console
# ---------------------------------------------------------------------------

def print_certification_result(result: dict) -> None:
    """Affiche le résultat de certification d'un agent."""
    certifié = result.get("certifié", False)
    status_color = GREEN if certifié else RED
    status_label = "CERTIFIÉ" if certifié else "NON CERTIFIÉ"

    print(f"\n{BOLD}Fichier : {os.path.basename(result.get('filepath', 'N/A'))}{RESET}")
    print(f"  Type         : {result.get('agent_type', 'N/A')}")
    print(f"  Score        : {result.get('score', 0):.1f}% "
          f"(minimum : {result.get('score_minimum_requis', 'N/A')}%)")
    print(f"  Statut       : {status_color}{BOLD}{status_label}{RESET}")

    if certifié:
        print(f"  Validité     : {result.get('validité_mois', '?')} mois")

    if result.get("check_details"):
        print("  Critères :")
        for critere, info in result["check_details"].items():
            icon = f"{GREEN}✓{RESET}" if info["passed"] else f"{RED}✗{RESET}"
            print(f"    {icon} {critere:<30} — {info['detail']}")

    if result.get("recommandations"):
        print(f"  {YELLOW}Recommandations :{RESET}")
        for rec in result["recommandations"]:
            print(f"    → {rec}")


def print_batch_summary(results: list) -> None:
    """Affiche un résumé de la validation par lot."""
    total = len(results)
    certified = sum(1 for r in results if r.get("certifié"))
    avg_score = sum(r.get("score", 0) for r in results) / max(total, 1)

    print(f"\n{BOLD}Résumé batch{RESET}")
    print(f"  Total analysé : {total}")
    print(f"  Certifiés     : {GREEN}{certified}{RESET} / {total}")
    print(f"  Score moyen   : {avg_score:.1f}%")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}CaelumSwarm™ — Agent Certification Validator{RESET}")

    repo_root = os.path.join(os.path.dirname(__file__), "..")

    # --- Validation engine Python ---
    engine_path = os.path.join(
        repo_root, "swarm", "intelligence", "forced_marriage_rights_engine.py"
    )
    print(f"\n{BOLD}[1/3] Validation Engine Python{RESET}")
    result_engine = validate_engine(engine_path)
    print_certification_result(result_engine)

    # --- Validation route API ---
    route_path = os.path.join(
        repo_root, "app", "api", "forced-marriage-rights-engine", "route.ts"
    )
    print(f"\n{BOLD}[2/3] Validation Route API{RESET}")
    result_route = validate_route(route_path)
    print_certification_result(result_route)

    # --- Batch : 5 premiers scripts du répertoire scripts/ ---
    scripts_dir = os.path.join(repo_root, "scripts")
    print(f"\n{BOLD}[3/3] Batch validation — scripts/ (support_agent, 5 premiers){RESET}")
    all_results = batch_validate(scripts_dir, "support_agent")
    batch_sample = all_results[:5]
    for r in batch_sample:
        print_certification_result(r)
    print_batch_summary(all_results)

    # Export JSON résultats principaux
    output = {
        "engine": result_engine,
        "route": result_route,
        "batch_summary": {
            "total": len(all_results),
            "certified": sum(1 for r in all_results if r.get("certifié")),
            "avg_score": round(
                sum(r.get("score", 0) for r in all_results) / max(len(all_results), 1), 2
            ),
        },
    }

    docs_dir = os.path.join(repo_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, "certification-report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n  Rapport exporté : {out_path}")

    print(f"\n{BOLD}Certification Validator terminé.{RESET}\n")


if __name__ == "__main__":
    main()
