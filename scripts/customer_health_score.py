#!/usr/bin/env python3
"""
customer_health_score.py — Score de Santé Client CaelumSwarm™
══════════════════════════════════════════════════════════════
Détecte les clients à risque de départ AVANT qu'ils résilient — le levier
n°1 de rétention, donc de revenu récurrent.

Pour chaque client, calcule un score de santé (0–100) à partir de signaux
pondérés, classe le risque (sain / à surveiller / à risque / critique),
estime la probabilité de churn et recommande une action concrète.

Stdlib uniquement. Sans dépendance — branche-le sur tes vraies données.

Signaux pris en compte (pondérés) :
  - adoption (utilisation réelle vs sièges payés)     30 %
  - fréquence de connexion (récence)                  20 %
  - tickets support non résolus                       15 %
  - NPS / satisfaction                                15 %
  - jours avant renouvellement                        10 %
  - tendance d'usage (hausse/baisse)                  10 %

Usage :
  python3 scripts/customer_health_score.py --demo
  python3 scripts/customer_health_score.py --score \
      --adoption 0.4 --login-recency-days 21 --open-tickets 3 \
      --nps 10 --renewal-days 25 --usage-trend -0.3 --arr 11880 --name "ACME"
"""

import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

HEALTH_LOG = Path("data/customer_health_log.json")

WEIGHTS = {
    "adoption":     0.30,
    "recency":      0.20,
    "support":      0.15,
    "nps":          0.15,
    "renewal":      0.10,
    "trend":        0.10,
}


def _clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))


def _sub_scores(signals: dict) -> dict:
    """Convertit chaque signal brut en sous-score 0–100 (plus haut = plus sain)."""
    # adoption : 0..1 → 0..100
    adoption = _clamp(signals.get("adoption", 0.5) * 100)

    # recency : jours depuis dernière connexion. 0j=100, 30j+=0
    rd = signals.get("login_recency_days", 7)
    recency = _clamp(100 - (rd / 30.0) * 100)

    # support : tickets ouverts non résolus. 0=100, 5+=0
    ot = signals.get("open_tickets", 0)
    support = _clamp(100 - (ot / 5.0) * 100)

    # nps : -100..+100 → 0..100
    nps = _clamp((signals.get("nps", 0) + 100) / 2.0)

    # renewal : jours avant renouvellement. <15j = risque (fenêtre de décision)
    rnd = signals.get("renewal_days", 180)
    if rnd <= 0:
        renewal = 0.0
    elif rnd < 30:
        renewal = _clamp((rnd / 30.0) * 60)      # proche = sous pression
    else:
        renewal = _clamp(60 + min(40, (rnd - 30) / 6))
    # tendance d'usage : -1..+1 → 0..100 (centré 50)
    tr = signals.get("usage_trend", 0.0)
    trend = _clamp(50 + tr * 50)

    return {"adoption": round(adoption, 1), "recency": round(recency, 1),
            "support": round(support, 1), "nps": round(nps, 1),
            "renewal": round(renewal, 1), "trend": round(trend, 1)}


def health_score(signals: dict) -> dict:
    subs = _sub_scores(signals)
    score = round(sum(subs[k] * WEIGHTS[k] for k in WEIGHTS), 1)

    if score >= 75:
        level, churn = "sain", "faible"
    elif score >= 55:
        level, churn = "à surveiller", "modéré"
    elif score >= 35:
        level, churn = "à risque", "élevé"
    else:
        level, churn = "critique", "très élevé"

    # Probabilité de churn approximée (inverse du score, bornée)
    churn_pct = round(_clamp((100 - score) * 0.9, 2, 95), 1)

    # Action recommandée selon le signal le plus faible
    weakest = min(subs, key=lambda k: subs[k])
    actions = {
        "adoption":  "Relancer l'adoption : formation ciblée + cas d'usage concret.",
        "recency":   "Client inactif — email de réengagement + appel du CSM.",
        "support":   "Tickets en souffrance — prioriser la résolution sous 48h.",
        "nps":       "Insatisfaction — entretien de feedback avec un responsable.",
        "renewal":   "Renouvellement proche — proposer un QBR et sécuriser le renouvellement.",
        "trend":     "Usage en baisse — diagnostic d'usage + plan de relance.",
    }

    # Valeur en jeu (si ARR fourni)
    arr = signals.get("arr")
    value_at_risk = round(arr * churn_pct / 100) if arr else None

    return {
        "name": signals.get("name", "client"),
        "score": score,
        "level": level,
        "churn_risk": churn,
        "churn_pct": churn_pct,
        "sub_scores": subs,
        "weakest_signal": weakest,
        "recommended_action": actions[weakest],
        "value_at_risk_eur": value_at_risk,
    }


def _log(rec: dict):
    log = []
    if HEALTH_LOG.exists():
        try:
            log = json.loads(HEALTH_LOG.read_text())
        except Exception:
            log = []
    log.append({"ts": datetime.now(timezone.utc).isoformat(), **{k: rec[k] for k in ("name", "score", "level", "churn_pct", "value_at_risk_eur")}})
    if len(log) > 1000:
        log = log[-1000:]
    HEALTH_LOG.parent.mkdir(exist_ok=True)
    HEALTH_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


LEVEL_ICON = {"sain": "🟢", "à surveiller": "🟡", "à risque": "🟠", "critique": "🔴"}


def print_one(r: dict):
    icon = LEVEL_ICON.get(r["level"], "⚪")
    print(f"\n  {icon} {r['name']} — score {r['score']}/100 ({r['level']})")
    print(f"     Risque de churn : {r['churn_pct']}% ({r['churn_risk']})")
    if r["value_at_risk_eur"] is not None:
        print(f"     💶 Valeur en jeu : {r['value_at_risk_eur']:,} €")
    print(f"     Signaux : " + "  ".join(f"{k}={v}" for k, v in r["sub_scores"].items()))
    print(f"     ⚠️  Point faible : {r['weakest_signal']}")
    print(f"     ➡️  Action : {r['recommended_action']}")


def _demo():
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       CUSTOMER HEALTH SCORE — CaelumSwarm™                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    clients = [
        {"name": "Hôpital Bruxelles (Enterprise)", "adoption": 0.85, "login_recency_days": 2,
         "open_tickets": 0, "nps": 60, "renewal_days": 120, "usage_trend": 0.2, "arr": 9900},
        {"name": "PME TechStart (Pro)", "adoption": 0.30, "login_recency_days": 25,
         "open_tickets": 3, "nps": -10, "renewal_days": 20, "usage_trend": -0.4, "arr": 990},
        {"name": "Cabinet Conseil (White-label)", "adoption": 0.6, "login_recency_days": 10,
         "open_tickets": 1, "nps": 30, "renewal_days": 60, "usage_trend": 0.0, "arr": 49000},
    ]
    results = [health_score(c) for c in clients]
    for r in results:
        print_one(r)
        _log(r)
    # Synthèse
    at_risk = [r for r in results if r["level"] in ("à risque", "critique")]
    total_risk = sum(r["value_at_risk_eur"] or 0 for r in results)
    print("\n  " + "─" * 58)
    print(f"  Clients à risque : {len(at_risk)}/{len(results)}")
    print(f"  💶 Valeur totale en jeu : {total_risk:,} € — à protéger en priorité")
    print("  " + "─" * 58 + "\n")


def main():
    ap = argparse.ArgumentParser(description="Customer Health Score CaelumSwarm™")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--score", action="store_true", help="Scorer un client (avec les --signaux)")
    ap.add_argument("--name", type=str, default="client")
    ap.add_argument("--adoption", type=float, default=0.5, help="0..1 (utilisation/sièges)")
    ap.add_argument("--login-recency-days", type=float, default=7)
    ap.add_argument("--open-tickets", type=int, default=0)
    ap.add_argument("--nps", type=float, default=0, help="-100..+100")
    ap.add_argument("--renewal-days", type=float, default=180)
    ap.add_argument("--usage-trend", type=float, default=0.0, help="-1..+1")
    ap.add_argument("--arr", type=float, default=None, help="ARR en € (optionnel)")
    args = ap.parse_args()

    if args.demo:
        _demo()
    elif args.score:
        r = health_score({
            "name": args.name, "adoption": args.adoption,
            "login_recency_days": args.login_recency_days, "open_tickets": args.open_tickets,
            "nps": args.nps, "renewal_days": args.renewal_days,
            "usage_trend": args.usage_trend, "arr": args.arr,
        })
        print_one(r)
        _log(r)
        print()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
