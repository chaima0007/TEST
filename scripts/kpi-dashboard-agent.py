#!/usr/bin/env python3
"""
KPI Dashboard Agent — Caelum Partners SPRL
Tableau de bord de performance et de croissance (Wave 209 — 42+ engines actifs)
"""

import json
import math
from datetime import datetime

# ── Données simulées réalistes (early startup ESG, juin 2026) ─────────────────

KPI_DATA = {
    "periode": "Juin 2026",
    "periode_precedente": "Mai 2026",
    "kpis": {
        # ── Financiers ────────────────────────────────────────────────────────
        "mrr_eur": {
            "label": "MRR (Monthly Recurring Revenue)",
            "unite": "EUR",
            "categorie": "Financier",
            "valeur_actuelle": 38_450,
            "valeur_precedente": 31_200,
            "seuil_alerte": 20_000,
            "seuil_objectif": 100_000,
            "description": "Revenus récurrents mensuels consolidés",
        },
        "arr_eur": {
            "label": "ARR (Annual Recurring Revenue)",
            "unite": "EUR",
            "categorie": "Financier",
            "valeur_actuelle": 461_400,
            "valeur_precedente": 374_400,
            "seuil_alerte": 240_000,
            "seuil_objectif": 1_200_000,
            "description": "Projection annuelle des revenus récurrents",
        },
        "chiffre_affaires_ytd_eur": {
            "label": "CA cumulé YTD",
            "unite": "EUR",
            "categorie": "Financier",
            "valeur_actuelle": 182_300,
            "valeur_precedente": 143_850,
            "seuil_alerte": 50_000,
            "seuil_objectif": 500_000,
            "description": "Chiffre d'affaires cumulé depuis janvier 2026",
        },
        # ── Clients ───────────────────────────────────────────────────────────
        "nb_clients_actifs": {
            "label": "Clients actifs",
            "unite": "clients",
            "categorie": "Clients",
            "valeur_actuelle": 47,
            "valeur_precedente": 38,
            "seuil_alerte": 20,
            "seuil_objectif": 200,
            "description": "Nombre de clients avec abonnement actif ce mois",
        },
        "nb_clients_enterprise": {
            "label": "Clients Enterprise (>2500 EUR/mois)",
            "unite": "clients",
            "categorie": "Clients",
            "valeur_actuelle": 8,
            "valeur_precedente": 6,
            "seuil_alerte": 3,
            "seuil_objectif": 30,
            "description": "Grands comptes plan Enterprise actifs",
        },
        "taux_churn_mensuel_pct": {
            "label": "Taux de churn mensuel",
            "unite": "%",
            "categorie": "Clients",
            "valeur_actuelle": 2.1,
            "valeur_precedente": 3.4,
            "seuil_alerte": 5.0,
            "seuil_objectif": 1.0,
            "description": "% clients perdus par rapport au mois précédent",
            "inverser_tendance": True,  # Baisse = amélioration
        },
        "nps_score": {
            "label": "NPS (Net Promoter Score)",
            "unite": "/100",
            "categorie": "Clients",
            "valeur_actuelle": 61,
            "valeur_precedente": 54,
            "seuil_alerte": 30,
            "seuil_objectif": 80,
            "description": "Indice de recommandation client (enquête mensuelle)",
        },
        "ltv_moyen_eur": {
            "label": "LTV moyen par client",
            "unite": "EUR",
            "categorie": "Clients",
            "valeur_actuelle": 22_800,
            "valeur_precedente": 19_500,
            "seuil_alerte": 5_000,
            "seuil_objectif": 50_000,
            "description": "Valeur vie client moyenne (LTV = ARPU / churn)",
        },
        # ── Produit / Technique ───────────────────────────────────────────────
        "nb_engines_actifs": {
            "label": "Engines swarm actifs",
            "unite": "engines",
            "categorie": "Produit",
            "valeur_actuelle": 42,
            "valeur_precedente": 39,
            "seuil_alerte": 20,
            "seuil_objectif": 60,
            "description": "Engines Python actifs dans CaelumSwarm (Wave 209)",
        },
        "nb_agents_support_actifs": {
            "label": "Agents support actifs",
            "unite": "agents",
            "categorie": "Produit",
            "valeur_actuelle": 18,
            "valeur_precedente": 15,
            "seuil_alerte": 5,
            "seuil_objectif": 30,
            "description": "Agents IA de support client actifs dans le système",
        },
        "couverture_csddd_pct": {
            "label": "Couverture CSDDD",
            "unite": "%",
            "categorie": "Produit",
            "valeur_actuelle": 84,
            "valeur_precedente": 78,
            "seuil_alerte": 60,
            "seuil_objectif": 100,
            "description": "% des 50 domaines CSDDD couverts par un engine dédié",
        },
        "api_latency_p95_ms": {
            "label": "Latence API P95",
            "unite": "ms",
            "categorie": "Technique",
            "valeur_actuelle": 142,
            "valeur_precedente": 198,
            "seuil_alerte": 500,
            "seuil_objectif": 100,
            "description": "Latence au 95ème percentile des appels API",
            "inverser_tendance": True,
        },
        "uptime_pct": {
            "label": "Disponibilité plateforme",
            "unite": "%",
            "categorie": "Technique",
            "valeur_actuelle": 99.87,
            "valeur_precedente": 99.61,
            "seuil_alerte": 99.0,
            "seuil_objectif": 99.95,
            "description": "Uptime mensuel de la plateforme CaelumSwarm",
        },
        "nb_appels_api_mois": {
            "label": "Appels API / mois",
            "unite": "appels",
            "categorie": "Technique",
            "valeur_actuelle": 2_847_000,
            "valeur_precedente": 2_103_000,
            "seuil_alerte": 500_000,
            "seuil_objectif": 10_000_000,
            "description": "Volume total d'appels API sur la période",
        },
        # ── Compliance / Impact ───────────────────────────────────────────────
        "score_conformite_moyen_clients": {
            "label": "Score conformité moyen portefeuille",
            "unite": "/10",
            "categorie": "Compliance",
            "valeur_actuelle": 6.84,
            "valeur_precedente": 6.31,
            "seuil_alerte": 5.0,
            "seuil_objectif": 8.0,
            "description": "Score de conformité CSDDD moyen sur l'ensemble des clients",
        },
        "nb_fournisseurs_analyses": {
            "label": "Fournisseurs analysés (cumulé)",
            "unite": "fournisseurs",
            "categorie": "Compliance",
            "valeur_actuelle": 14_820,
            "valeur_precedente": 11_350,
            "seuil_alerte": 1_000,
            "seuil_objectif": 50_000,
            "description": "Nombre total de fournisseurs évalués via CaelumSwarm",
        },
        "nb_alertes_droits_humains_emises": {
            "label": "Alertes droits humains émises",
            "unite": "alertes",
            "categorie": "Compliance",
            "valeur_actuelle": 387,
            "valeur_precedente": 298,
            "seuil_alerte": 50,
            "seuil_objectif": 1_000,
            "description": "Alertes automatiques émises aux clients sur risques droits humains",
        },
    },
}

# ── Seuils et niveaux ─────────────────────────────────────────────────────────

def compute_trend(kpi: dict) -> dict:
    """Calcule la tendance par rapport à la période précédente."""
    curr = kpi["valeur_actuelle"]
    prev = kpi["valeur_precedente"]
    inverser = kpi.get("inverser_tendance", False)

    if prev == 0:
        delta_pct = 0.0
    else:
        delta_pct = round((curr - prev) / prev * 100, 1)

    delta_abs = curr - prev

    if inverser:
        is_good = delta_abs <= 0
    else:
        is_good = delta_abs >= 0

    if abs(delta_pct) < 1:
        tendance = "STABLE"
        symbole = "→"
    elif is_good:
        tendance = "HAUSSE" if not inverser else "AMÉLIORATION"
        symbole = "▲"
    else:
        tendance = "BAISSE" if not inverser else "DÉGRADATION"
        symbole = "▼"

    return {
        "delta_abs": delta_abs,
        "delta_pct": delta_pct,
        "tendance": tendance,
        "symbole": symbole,
        "est_positif": is_good,
    }


def compute_progress(kpi: dict) -> float:
    """Calcule le % de progression vers l'objectif (0-100)."""
    curr = kpi["valeur_actuelle"]
    seuil = kpi["seuil_alerte"]
    obj = kpi["seuil_objectif"]
    inverser = kpi.get("inverser_tendance", False)

    if inverser:
        # Pour les métriques inversées (churn, latence) : min=objectif, max=alerte
        if obj >= seuil:
            return 50.0
        span = seuil - obj
        dist = curr - obj
        pct = max(0, min(100, 100 - (dist / span * 100)))
    else:
        if obj <= seuil:
            return 50.0
        span = obj - seuil
        dist = curr - seuil
        pct = max(0, min(100, dist / span * 100))

    return round(pct, 1)


def get_status(kpi: dict) -> str:
    """Détermine le statut du KPI."""
    curr = kpi["valeur_actuelle"]
    seuil = kpi["seuil_alerte"]
    obj = kpi["seuil_objectif"]
    inverser = kpi.get("inverser_tendance", False)

    if inverser:
        if curr <= obj:
            return "OBJECTIF"
        elif curr <= seuil:
            return "OK"
        else:
            return "ALERTE"
    else:
        if curr >= obj:
            return "OBJECTIF"
        elif curr >= seuil:
            return "OK"
        else:
            return "ALERTE"


def render_progress_bar(pct: float, width: int = 30) -> str:
    filled = round(pct / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct:.0f}%"


def format_value(kpi: dict) -> str:
    """Formate la valeur selon l'unité."""
    val = kpi["valeur_actuelle"]
    unit = kpi["unite"]
    if unit == "EUR":
        if val >= 1_000_000:
            return f"{val/1_000_000:.2f}M EUR"
        elif val >= 1_000:
            return f"{val/1_000:.1f}k EUR"
        return f"{val:.0f} EUR"
    elif unit == "%":
        return f"{val:.2f}%"
    elif unit == "appels":
        return f"{val/1_000:.0f}k"
    elif unit == "fournisseurs":
        return f"{val:,}"
    elif unit in ("/100", "/10", "ms"):
        return f"{val} {unit}"
    elif val >= 1_000:
        return f"{val:,} {unit}"
    return f"{val} {unit}"


def run_agent():
    now = datetime.now()
    print("=" * 68)
    print("  CAELUM PARTNERS — KPI DASHBOARD AGENT")
    print(f"  Période : {KPI_DATA['periode']}  |  Généré le : {now.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 68)

    kpis = KPI_DATA["kpis"]
    alerts = []
    objectives_reached = []
    enriched = {}

    # Calcul enrichissement
    for key, kpi in kpis.items():
        trend = compute_trend(kpi)
        progress = compute_progress(kpi)
        status = get_status(kpi)
        enriched[key] = {**kpi, "trend": trend, "progress": progress, "status": status}
        if status == "ALERTE":
            alerts.append(key)
        if status == "OBJECTIF":
            objectives_reached.append(key)

    # ── Résumé exécutif ──────────────────────────────────────────────────────
    print(f"\n{'─'*68}")
    print("  RÉSUMÉ EXÉCUTIF")
    print(f"{'─'*68}")
    mrr = enriched["mrr_eur"]
    clients = enriched["nb_clients_actifs"]
    churn = enriched["taux_churn_mensuel_pct"]
    engines = enriched["nb_engines_actifs"]
    csddd = enriched["couverture_csddd_pct"]

    print(f"  MRR actuel      : {format_value(mrr)}  ({mrr['trend']['symbole']} {mrr['trend']['delta_pct']:+.1f}%)")
    print(f"  Clients actifs  : {format_value(clients)}  ({clients['trend']['symbole']} {clients['trend']['delta_abs']:+.0f} ce mois)")
    print(f"  Churn mensuel   : {format_value(churn)}  ({churn['trend']['symbole']} {churn['trend']['delta_pct']:+.1f}%)")
    print(f"  Engines actifs  : {format_value(engines)}  (Wave 209)")
    print(f"  Couverture CSDDD: {format_value(csddd)}")
    print(f"\n  Alertes actives    : {len(alerts)} KPI(s) sous seuil")
    print(f"  Objectifs atteints : {len(objectives_reached)} KPI(s)")

    # ── Dashboard par catégorie ───────────────────────────────────────────────
    categories = {}
    for key, kpi in enriched.items():
        cat = kpi["categorie"]
        categories.setdefault(cat, []).append((key, kpi))

    for cat, items in categories.items():
        print(f"\n{'─'*68}")
        print(f"  {cat.upper()}")
        print(f"{'─'*68}")
        for key, kpi in items:
            trend = kpi["trend"]
            status = kpi["status"]
            progress = kpi["progress"]

            # Icône statut
            if status == "ALERTE":
                status_icon = "⚠ ALERTE"
            elif status == "OBJECTIF":
                status_icon = "✓ OBJECTIF"
            else:
                status_icon = "  OK     "

            val_str = format_value(kpi)
            trend_str = f"{trend['symbole']} {trend['delta_pct']:+.1f}%"

            print(f"\n  {status_icon} | {kpi['label']}")
            print(f"           Valeur    : {val_str}  {trend_str} vs {KPI_DATA['periode_precedente']}")
            print(f"           Vs objectif: {render_progress_bar(progress)}")
            print(f"           Seuil alerte: {kpi['seuil_alerte']} {kpi['unite']}  "
                  f"| Objectif: {kpi['seuil_objectif']} {kpi['unite']}")

    # ── Alertes ───────────────────────────────────────────────────────────────
    if alerts:
        print(f"\n{'─'*68}")
        print("  ALERTES — ACTION REQUISE")
        print(f"{'─'*68}")
        for key in alerts:
            kpi = enriched[key]
            print(f"\n  ⚠  {kpi['label']}")
            print(f"     Valeur actuelle : {format_value(kpi)}")
            print(f"     Seuil alerte    : {kpi['seuil_alerte']} {kpi['unite']}")
            print(f"     Description     : {kpi['description']}")
    else:
        print(f"\n  Aucune alerte — tous les KPIs sont au-dessus des seuils.")

    # ── Score santé global ────────────────────────────────────────────────────
    scores = [kpi["progress"] for kpi in enriched.values()]
    health_score = round(sum(scores) / len(scores), 1)
    nb_kpis = len(enriched)

    print(f"\n{'─'*68}")
    print("  SCORE DE SANTÉ GLOBAL")
    print(f"{'─'*68}")
    print(f"\n  {render_progress_bar(health_score, 40)}")
    print(f"\n  Basé sur {nb_kpis} KPIs — Score moyen de progression vers objectifs")
    print(f"  Alertes    : {len(alerts)}/{nb_kpis}")
    print(f"  Objectifs  : {len(objectives_reached)}/{nb_kpis}")

    if health_score >= 70:
        verdict = "SANTE BONNE — Croissance en ligne avec les objectifs"
    elif health_score >= 45:
        verdict = "SANTÉ MOYENNE — Actions prioritaires requises"
    else:
        verdict = "SANTÉ CRITIQUE — Revoir la stratégie immédiatement"
    print(f"  Verdict    : {verdict}")
    print(f"{'─'*68}\n")

    # ── JSON output ───────────────────────────────────────────────────────────
    output = {
        "agent": "kpi-dashboard-agent",
        "generated_at": now.isoformat(),
        "periode": KPI_DATA["periode"],
        "periode_precedente": KPI_DATA["periode_precedente"],
        "health_score_global": health_score,
        "nb_alertes": len(alerts),
        "nb_objectifs_atteints": len(objectives_reached),
        "kpis": {
            key: {
                **kpi,
                "valeur_formatee": format_value(kpi),
            }
            for key, kpi in enriched.items()
        },
        "alertes_actives": alerts,
        "objectifs_atteints": objectives_reached,
        "verdict": verdict,
    }

    output_path = "/home/user/TEST/scripts/kpi-dashboard-agent-output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  JSON sauvegardé → {output_path}")
    print()
    return output


if __name__ == "__main__":
    run_agent()
