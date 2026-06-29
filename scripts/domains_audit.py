#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit domaines & DNS — détecte la fragilité et le degré de consolidation.
========================================================================
Lit data/governance/domains_inventory.json (source de vérité, à compléter) et signale :
  - FRAGMENTATION : plusieurs registrars / plusieurs fournisseurs DNS,
  - SÉCURITÉ : transfer_lock / 2FA / auto_renew / DNSSEC manquants,
  - DONNÉES À COMPLÉTER : champs non renseignés.

Honnête : ce script n'accède PAS aux comptes registrars (pas d'API/identifiants ici).
Il audite l'inventaire déclaré ; renseignez les vraies valeurs pour un audit complet.

Usage : python3 scripts/domains_audit.py [--json]
"""
from __future__ import annotations
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, "data", "governance", "domains_inventory.json")
BASE = ["transfer_lock", "auto_renew", "dnssec", "2fa_compte"]


def main() -> int:
    try:
        d = json.load(open(INV, encoding="utf-8"))
    except Exception as e:
        print(f"⛔ Inventaire illisible : {e}")
        return 1
    doms = d.get("domaines", [])
    registrars = {x.get("registrar_actuel") for x in doms if x.get("registrar_actuel") and "confirmer" not in str(x.get("registrar_actuel"))}
    dns = {x.get("dns_actuel") for x in doms if x.get("dns_actuel") and "confirmer" not in str(x.get("dns_actuel"))}
    constates = d.get("registrars_constates", [])

    alertes, manques = [], []
    fragmentation = len(registrars) > 1 or len(constates) > 1
    if fragmentation:
        alertes.append(f"FRAGMENTATION registrar : {sorted(registrars) or constates} → cible = 1 seul")
    if len(dns) > 1:
        alertes.append(f"FRAGMENTATION DNS : {sorted(dns)} → cible = 1 seul (Cloudflare)")
    for x in doms:
        for k in BASE:
            if x.get(k) in (None, False):
                manques.append(f"{x.get('domaine')} : {k} non confirmé/absent")

    a_completer = sum(1 for x in doms for v in x.values() if v in (None,) or "confirmer" in str(v))
    verdict = "CRITIQUE" if fragmentation else ("ALERTE" if manques else "OK")

    if "--json" in sys.argv:
        print(json.dumps({"verdict": verdict, "fragmentation": fragmentation,
                          "registrars": sorted(registrars) or constates, "dns": sorted(dns),
                          "alertes": alertes, "manques": len(manques), "a_completer": a_completer}, ensure_ascii=False))
        return 0

    print("═══ AUDIT DOMAINES & DNS ═══")
    print(f"  Domaines inventoriés : {len(doms)} · registrars constatés : {constates}")
    print(f"  Cible : 1 registrar ({d.get('cible_consolidation',{}).get('registrar_unique','?')}) + 1 DNS (Cloudflare)")
    if alertes:
        print("\n  🛑 Points de fragilité :")
        for a in alertes:
            print(f"     - {a}")
    if manques:
        print(f"\n  🔐 Sécurité à confirmer ({len(manques)}) :")
        for m in manques[:12]:
            print(f"     - {m}")
    if a_completer:
        print(f"\n  📝 Champs à compléter dans l'inventaire : {a_completer}")
    print(f"\n  Verdict : {verdict}")
    print(f"  → {os.path.relpath(INV, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
