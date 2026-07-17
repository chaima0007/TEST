#!/usr/bin/env python3
"""
provider_arbitrage_protocol.py — Arbitrage des fournisseurs d'API/services (P-ARBITRAGE-API).

Les agents recherchent en continu le meilleur fournisseur par service (qualité/prix/latence)
et BASCULENT automatiquement : (1) failover si le fournisseur actif tombe (dispo=false),
(2) recommandation de changement si un autre fournisseur offre un meilleur rapport.

Honnête : pas de « négociation » magique avec des tiers — on arbitre parmi les fournisseurs
CONFIGURÉS (data/governance/api_providers.json), avec leurs vrais chiffres à calibrer.

Score (plus haut = mieux) :
  score = w_qualite*qualite - w_prix*prix_norm - w_latence*latence_norm   (prix/latence normalisés 0..1 par service)

Usage : python3 scripts/provider_arbitrage_protocol.py
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = os.path.join(BASE, "data", "governance", "api_providers.json")
REPORT = os.path.join(BASE, "data", "provider_arbitrage_report.json")


def _norm(vals):
    vmin, vmax = min(vals), max(vals)
    rng = (vmax - vmin) or 1.0
    return lambda v: (v - vmin) / rng


def arbitrer(conf):
    w = conf.get("ponderation", {"qualite": 0.5, "prix": 0.3, "latence": 0.2})
    decisions = []
    for svc in conf.get("services", []):
        fournisseurs = svc.get("fournisseurs", [])
        # données complètes requises pour scorer
        complets = [f for f in fournisseurs if all(f.get(k) is not None for k in ("prix", "qualite", "latence_ms"))]
        dispo = [f for f in complets if f.get("dispo", True)]
        actif = next((f for f in fournisseurs if f.get("actif")), None)

        if not complets:
            decisions.append({"service": svc["service"], "statut": "À COMPLÉTER", "detail": "chiffres fournisseurs manquants"})
            continue
        if not dispo:
            decisions.append({"service": svc["service"], "statut": "CRITIQUE", "detail": "aucun fournisseur disponible"})
            continue

        nprix = _norm([f["prix"] for f in dispo])
        nlat = _norm([f["latence_ms"] for f in dispo])
        for f in dispo:
            f["_score"] = round(w["qualite"] * f["qualite"] - w["prix"] * nprix(f["prix"]) - w["latence"] * nlat(f["latence_ms"]), 3)
        meilleur = max(dispo, key=lambda f: f["_score"])

        if actif is None or not actif.get("dispo", True):
            statut, detail = "BASCULE", f"failover → {meilleur['nom']} (actif indisponible)"
        elif meilleur["nom"] != actif["nom"]:
            statut, detail = "RECOMMANDATION", f"{actif['nom']} → {meilleur['nom']} (meilleur rapport)"
        else:
            statut, detail = "OPTIMAL", f"{actif['nom']} reste le meilleur choix"
        decisions.append({"service": svc["service"], "statut": statut, "meilleur": meilleur["nom"],
                          "score": meilleur["_score"], "detail": detail})
    return decisions


def main():
    try:
        conf = json.load(open(CONF, encoding="utf-8"))
    except Exception as e:
        print(f"⛔ Config fournisseurs illisible : {e}")
        return 1

    decisions = arbitrer(conf)
    print("═══ ARBITRAGE DES FOURNISSEURS D'API (qualité/prix/latence + failover) ═══")
    if conf.get("exemple"):
        print("  (config d'exemple — à calibrer avec les vrais contrats)")
    ic = {"OPTIMAL": "✅", "RECOMMANDATION": "🔁", "BASCULE": "🛟", "À COMPLÉTER": "✍️", "CRITIQUE": "🔴"}
    crit = 0
    for d in decisions:
        print(f"  {ic.get(d['statut'],'•')} {d['service']:14s} {d['statut']:14s} {d.get('detail','')}")
        if d["statut"] == "CRITIQUE":
            crit += 1
    json.dump({"ponderation": conf.get("ponderation"), "decisions": decisions},
              open(REPORT, "w"), ensure_ascii=False, indent=2)
    print(f"  → {len(decisions)} service(s) arbitré(s) · rapport : data/provider_arbitrage_report.json")
    return 1 if crit else 0


if __name__ == "__main__":
    sys.exit(main())
