#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capteur de changement juridique — 2ᵉ organe de la plateforme autonome.
=====================================================================
Détecte les fiches potentiellement périmées sur TOUT le corpus (≠ scripts existants
qui ne couvraient que `bail_*` ou 36 faits). Deux signaux combinés, honnêtes :

  1. FRAÎCHEUR LOCALE (toujours disponible, sans réseau) :
     âge depuis `date_verification` → frais / à revérifier / prioritaire.
  2. EMPREINTE DES SOURCES (mode --network, dégradation gracieuse) :
     SHA-256 de chaque page source officielle, comparé à la baseline mémorisée.
     Si l'empreinte change ET que la fiche est ancienne → priorité haute.
     Si le réseau est restreint, on le DÉTECTE (network_ok=false) sans rien inventer.

Sortie : data/legal_change.json  (+ baseline data/legal_change_state.json en mode réseau)
Usage :
    python3 scripts/legal_change_sensor.py                 # fraîcheur locale
    python3 scripts/legal_change_sensor.py --cadence 180   # seuil (jours)
    python3 scripts/legal_change_sensor.py --network       # + empreinte des sources
"""
from __future__ import annotations
import json
import os
import sys
import glob
import ssl
import hashlib
import urllib.request
from datetime import datetime, timezone, date
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "legal_change.json")
BASELINE = os.path.join(ROOT, "data", "legal_change_state.json")
TIMEOUT = 10


def _parse(d: str):
    try:
        return date.fromisoformat(d[:10])
    except Exception:
        return None


def collecter_modules() -> list:
    """Pour chaque module : date de vérif la plus ancienne + URLs officielles."""
    mods = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data/belgium/*.json"))):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        faits = d.get("faits") or []
        if not faits:
            continue
        dates = []
        if d.get("derniere_revue"):
            dates.append(_parse(d["derniere_revue"]))
        urls = set()
        bl = d.get("base_legale_principale", {})
        if bl.get("source_officielle"):
            urls.add(bl["source_officielle"])
        for fait in faits:
            if fait.get("date_verification"):
                dates.append(_parse(fait["date_verification"]))
            for s in fait.get("sources", []):
                if s.get("type") == "officiel" and s.get("url"):
                    urls.add(s["url"])
        dates = [x for x in dates if x]
        mods.append({
            "module": d.get("module"), "titre": d.get("titre"),
            "date_min": min(dates).isoformat() if dates else None,
            "urls": sorted(urls),
        })
    return mods


def _opener():
    handlers = []
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    ctx = ssl.create_default_context()
    if os.path.exists("/root/.ccr/ca-bundle.crt"):
        try:
            ctx.load_verify_locations("/root/.ccr/ca-bundle.crt")
        except Exception:
            pass
    handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def empreinte(opener, url: str):
    """Retourne (sha256, atteignable). atteignable=False si blocage réseau/proxy."""
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "CaelumLegalSensor/1.0"})
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            data = r.read(200_000)
        return hashlib.sha256(data).hexdigest(), True
    except urllib.error.HTTPError as e:
        # une page 404/410 est atteignable (réponse réelle) mais signale un souci
        return f"http-{e.code}", e.code in (404, 410)
    except Exception:
        return None, False


def main() -> int:
    args = sys.argv[1:]
    cadence = 180
    if "--cadence" in args:
        try:
            cadence = int(args[args.index("--cadence") + 1])
        except Exception:
            pass
    reseau = "--network" in args

    today = datetime.now(timezone.utc).date()
    mods = collecter_modules()

    frais, a_reverifier, prioritaire = [], [], []
    for m in mods:
        dmin = _parse(m["date_min"]) if m["date_min"] else None
        age = (today - dmin).days if dmin else 9999
        m["age_jours"] = age
        if age <= cadence:
            frais.append(m)
        elif age <= cadence * 2:
            a_reverifier.append(m)
        else:
            prioritaire.append(m)

    sources_modifiees = []
    network_ok = None
    if reseau:
        try:
            base = json.load(open(BASELINE, encoding="utf-8"))
        except Exception:
            base = {}
        atteints, total = 0, 0
        nouvelles = dict(base)
        taches = [(m, u) for m in mods for u in m["urls"]]
        opener = _opener()
        with ThreadPoolExecutor(max_workers=10) as ex:
            futs = {ex.submit(empreinte, opener, u): (m, u) for m, u in taches}
            for fut in as_completed(futs):
                m, u = futs[fut]
                h, atteignable = fut.result()
                total += 1
                if atteignable:
                    atteints += 1
                if h and atteignable and not h.startswith("http-"):
                    ancienne = base.get(u)
                    if ancienne and ancienne != h:
                        sources_modifiees.append({"module": m["module"], "url": u, "age_jours": m["age_jours"]})
                    nouvelles[u] = h
        network_ok = bool(total) and atteints / total >= 0.3
        if network_ok:
            json.dump(nouvelles, open(BASELINE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # Verdict (état actuel)
    if prioritaire or sources_modifiees:
        verdict = "ALERTE" if len(prioritaire) + len(sources_modifiees) < max(1, len(mods) // 10) else "CRITIQUE"
    else:
        verdict = "OK"

    rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "cadence_jours": cadence,
        "total_modules": len(mods),
        "frais": len(frais), "a_reverifier": len(a_reverifier), "prioritaire": len(prioritaire),
        "reseau_active": reseau, "network_ok": network_ok,
        "sources_modifiees": sources_modifiees,
        "modules_a_reverifier": [
            {"module": m["module"], "titre": m["titre"], "age_jours": m["age_jours"]}
            for m in sorted(a_reverifier + prioritaire, key=lambda x: -x["age_jours"])[:20]
        ],
        "verdict": verdict,
        "note": "Fraîcheur locale toujours fiable ; empreinte réseau seulement si network_ok.",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(rapport, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("═══ CAPTEUR DE CHANGEMENT JURIDIQUE ═══")
    print(f"  Modules : {len(mods)} · 🟢 frais {len(frais)} · 🟠 à revérifier {len(a_reverifier)} · 🔴 prioritaire {len(prioritaire)} (cadence {cadence}j)")
    if reseau:
        print(f"  Réseau : network_ok={network_ok} · sources modifiées détectées : {len(sources_modifiees)}")
    print(f"  Verdict : {verdict}")
    print(f"  → {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
