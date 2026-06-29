#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capteur de santé des sources — organe de la plateforme autonome.
================================================================
Teste RÉELLEMENT si les URL sources officielles répondent encore (vs simulation).

Honnêteté intégrée :
  - Distingue MORTE (404/410, vraiment cassée) de INDÉTERMINÉ (403/407/timeout/réseau).
  - Si l'environnement n'a pas d'accès réseau (proxy restreint, sandbox), il le DÉTECTE
    et ne déclare AUCUNE source morte à tort : il écrit network_ok=false.
  - Respecte le proxy HTTPS_PROXY et le CA bundle s'ils existent.

Conçu pour tourner là où le réseau est ouvert (production, machine de Chaima, CI).

Usage :
    python3 scripts/source_health_sensor.py            # toutes les URLs officielles
    python3 scripts/source_health_sensor.py --max 50   # limite (test rapide)
    python3 scripts/source_health_sensor.py --all       # officielles + secondaires
"""
from __future__ import annotations
import json
import os
import ssl
import sys
import glob
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "source_health.json")
TIMEOUT = 10


def collecter_urls(officiel_seulement=True) -> list:
    urls = set()
    for f in glob.glob(os.path.join(ROOT, "data/belgium/*.json")) + glob.glob(os.path.join(ROOT, "data/caelum/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        bl = d.get("base_legale_principale", {})
        if bl.get("source_officielle"):
            urls.add(bl["source_officielle"])
        for it in (d.get("faits") or d.get("normes") or []):
            so = it.get("source_officielle", {})
            if isinstance(so, dict) and so.get("url"):
                urls.add(so["url"])
            for s in it.get("sources", []):
                u = s.get("url")
                if not u:
                    continue
                if officiel_seulement and s.get("type") != "officiel":
                    continue
                urls.add(u)
    return sorted(urls)


def _opener() -> urllib.request.OpenerDirector:
    handlers = []
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    ctx = ssl.create_default_context()
    ca = "/root/.ccr/ca-bundle.crt"
    if os.path.exists(ca):
        try:
            ctx.load_verify_locations(ca)
        except Exception:
            pass
    handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def sonder(opener, url: str) -> dict:
    """Retourne {url, code, etat}. etat ∈ {OK, MORTE, INDÉTERMINÉ}."""
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "CaelumSourceSensor/1.0"})
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            code = r.status
            r.read(64)  # lit un peu pour valider la réponse
        etat = "OK" if 200 <= code < 400 else ("MORTE" if code in (404, 410) else "INDÉTERMINÉ")
        return {"url": url, "code": code, "etat": etat}
    except urllib.error.HTTPError as e:
        etat = "MORTE" if e.code in (404, 410) else "INDÉTERMINÉ"
        return {"url": url, "code": e.code, "etat": etat}
    except Exception as e:  # timeout, refus, DNS, proxy bloqué → jamais "morte"
        return {"url": url, "code": 0, "etat": "INDÉTERMINÉ", "erreur": type(e).__name__}


def main() -> int:
    args = sys.argv[1:]
    officiel = "--all" not in args
    mx = None
    if "--max" in args:
        try:
            mx = int(args[args.index("--max") + 1])
        except Exception:
            pass

    urls = collecter_urls(officiel)
    if mx:
        urls = urls[:mx]
    print(f"🔎 Capteur de sources : {len(urls)} URL à sonder (timeout {TIMEOUT}s)…")

    opener = _opener()
    resultats = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(sonder, opener, u): u for u in urls}
        for fut in as_completed(futs):
            resultats.append(fut.result())

    ok = [r for r in resultats if r["etat"] == "OK"]
    mortes = [r for r in resultats if r["etat"] == "MORTE"]
    indet = [r for r in resultats if r["etat"] == "INDÉTERMINÉ"]

    # Détection d'un réseau restreint : 0/407/403 = blocage proxy/connexion.
    # Le réseau est jugé OUVERT seulement si on a réellement atteint des sites (assez de OK).
    bloque = [r for r in indet if r.get("code") in (0, 403, 407)]
    reachable = len(ok) + len(mortes)  # réponses HTTP réellement interprétables (hors blocage)
    network_ok = bool(urls) and (reachable / len(urls) >= 0.3) and (len(bloque) / len(urls) < 0.5)

    pct_ok = round(100 * len(ok) / len(urls), 1) if urls else 0.0
    if network_ok:
        verdict = "OK" if not mortes else "ALERTE" if len(mortes) / len(urls) < 0.05 else "CRITIQUE"
    else:
        verdict = "INDÉTERMINÉ"

    rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "total": len(urls), "ok": len(ok), "mortes": len(mortes), "indetermines": len(indet),
        "pct_ok": pct_ok, "network_ok": network_ok, "verdict": verdict,
        "urls_mortes": [{"url": r["url"], "code": r["code"]} for r in mortes],
        "note": ("Réseau restreint détecté : aucune source déclarée morte à tort."
                 if not network_ok else "Sondage réseau réel."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(rapport, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"  OK={len(ok)} · MORTES={len(mortes)} · INDÉTERMINÉ={len(indet)} · network_ok={network_ok}")
    print(f"  Verdict : {verdict}" + (f" · {pct_ok}% vivantes" if network_ok else " (réseau indisponible ici)"))
    if mortes:
        print("  ⚰️  Sources mortes :")
        for r in mortes[:10]:
            print(f"     {r['code']}  {r['url']}")
    print(f"  → {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
