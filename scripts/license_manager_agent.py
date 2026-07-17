#!/usr/bin/env python3
"""
license_manager_agent.py — Agent de Gestion des Licences CaelumSwarm™
═════════════════════════════════════════════════════════════════════
Crée et valide un modèle d'abonnement / de licence logicielle LOUABLE.
Génère des clés de licence signées (HMAC-SHA256), définit les tiers,
le catalogue des modules louables, et la validation côté serveur.

SÉCURITÉ : le secret de signature vient de l'environnement
(LICENSE_SIGNING_KEY) — JAMAIS dans le code (SOPS/Vault en prod).

Usage:
  python3 scripts/license_manager_agent.py --tiers
  python3 scripts/license_manager_agent.py --catalog
  python3 scripts/license_manager_agent.py --issue --tier pro --customer "ACME" --months 12
  python3 scripts/license_manager_agent.py --validate "CAEL-XXXX-..."
  python3 scripts/license_manager_agent.py --revenue
"""

import os
import sys
import json
import hmac
import base64
import hashlib
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
try:
    from decision_seal import seal_decision
    SEAL_AVAILABLE = True
except ImportError:
    SEAL_AVAILABLE = False

LICENSE_LOG = Path("data/license_registry.json")
LICENSE_LOG.parent.mkdir(exist_ok=True)

# Secret de signature — depuis l'environnement UNIQUEMENT
SIGNING_KEY = os.environ.get("LICENSE_SIGNING_KEY", "")

# ── Tiers de licence ───────────────────────────────────────────────────────────
LICENSE_TIERS = {
    "free": {
        "name": "Free / Découverte",
        "price_eur_month": 0,
        "price_eur_year": 0,
        "max_engines": 3,
        "max_seats": 1,
        "api_calls_month": 1_000,
        "support": "Communauté",
        "white_label": False,
        "sla": None,
        "features": ["3 dashboards droits humains", "Accès lecture seule", "Export PDF basique"],
    },
    "pro": {
        "name": "Pro / PME",
        "price_eur_month": 99,
        "price_eur_year": 990,   # 2 mois offerts
        "max_engines": 50,
        "max_seats": 10,
        "api_calls_month": 100_000,
        "support": "Email 48h",
        "white_label": False,
        "sla": "99.0%",
        "features": ["50 engines", "API REST complète", "Sceaux de protocole", "Alertes temps réel", "Export Canva/Gamma"],
    },
    "enterprise": {
        "name": "Enterprise / Institution",
        "price_eur_month": 990,
        "price_eur_year": 9_900,
        "max_engines": 500,
        "max_seats": 100,
        "api_calls_month": 5_000_000,
        "support": "Dédié 4h + téléphone",
        "white_label": False,
        "sla": "99.9%",
        "features": ["500 engines", "SSO/OIDC", "Audit RGPD", "Multivers + Multi-perspectives", "Conformité CSDDD", "Déploiement on-premise"],
    },
    "whitelabel": {
        "name": "White-Label / Revente",
        "price_eur_month": 4_900,
        "price_eur_year": 49_000,
        "max_engines": 9_999,
        "max_seats": 9_999,
        "api_calls_month": 100_000_000,
        "support": "Partenaire dédié + SLA sur mesure",
        "white_label": True,
        "sla": "99.95%",
        "features": ["Marque blanche complète", "Tous les engines", "Revente autorisée", "Code source sous licence", "Formation incluse"],
    },
}

# ── Catalogue des modules LOUABLES (unités de valeur) ──────────────────────────
RENTABLE_MODULES = {
    "human_rights_suite": {
        "label": "Suite Droits Humains (200+ engines)",
        "rent_eur_month": 490,
        "category": "compliance",
        "tiers_min": "pro",
    },
    "compliance_csddd": {
        "label": "Module Conformité CSDDD 2024/1760",
        "rent_eur_month": 690,
        "category": "compliance",
        "tiers_min": "enterprise",
    },
    "protocol_seal_engine": {
        "label": "Moteur Sceau de Protocole (audit décisions)",
        "rent_eur_month": 290,
        "category": "governance",
        "tiers_min": "pro",
    },
    "build_guard": {
        "label": "Build Guard (anti-récurrence CI/CD)",
        "rent_eur_month": 190,
        "category": "devops",
        "tiers_min": "pro",
    },
    "multiverse_simulation": {
        "label": "Simulation Multivers + Multi-Perspectives",
        "rent_eur_month": 390,
        "category": "analytics",
        "tiers_min": "enterprise",
    },
    "white_label_platform": {
        "label": "Plateforme complète marque blanche",
        "rent_eur_month": 4_900,
        "category": "platform",
        "tiers_min": "whitelabel",
    },
}


# ── Génération / validation de clés ────────────────────────────────────────────

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _sign(payload: str) -> str:
    if not SIGNING_KEY:
        # Mode dégradé : signature déterministe non-secrète (DEV uniquement)
        return _b64(hashlib.sha256(payload.encode()).digest())[:24]
    sig = hmac.new(SIGNING_KEY.encode(), payload.encode(), hashlib.sha256).digest()
    return _b64(sig)[:24]


def issue_license(tier: str, customer: str, months: int = 12) -> dict:
    if tier not in LICENSE_TIERS:
        raise ValueError(f"Tier inconnu : {tier}. Disponibles : {list(LICENSE_TIERS)}")

    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=30 * months)
    t = LICENSE_TIERS[tier]

    # Sceau protocole obligatoire (émission = décision business)
    seal_id = "NO-SEAL"
    if SEAL_AVAILABLE:
        rec = seal_decision(
            action=f"license-issue-{tier}",
            context=f"Émission licence {tier} pour {customer} ({months} mois)",
            verbose=False,
        )
        seal_id = rec.get("seal_id", "NO-SEAL")
        if rec.get("status") != "APPROUVÉ":
            raise ValueError(f"Sceau non approuvé — émission bloquée ({seal_id})")

    payload_obj = {
        "tier": tier,
        "customer": customer,
        "issued": now.isoformat(),
        "expires": expires.isoformat(),
        "max_engines": t["max_engines"],
        "max_seats": t["max_seats"],
        "seal": seal_id,
    }
    payload_str = json.dumps(payload_obj, sort_keys=True, separators=(",", ":"))
    payload_b64 = _b64(payload_str.encode())
    signature = _sign(payload_str)

    # Format clé : CAEL-<TIER>-<payload>-<sig>
    key = f"CAEL-{tier.upper()}-{payload_b64}-{signature}"

    record = {**payload_obj, "key": key, "signed": bool(SIGNING_KEY)}
    _append_log(record)
    return record


def validate_license(key: str) -> dict:
    try:
        key = key.strip()
        if not key.startswith("CAEL-"):
            return {"valid": False, "reason": "Préfixe invalide"}
        parts = key.split("-")
        # CAEL - TIER - payload - sig  (payload peut contenir des tirets? non, b64url sans =)
        if len(parts) < 4:
            return {"valid": False, "reason": "Format invalide"}
        payload_b64 = parts[2]
        signature = parts[3]
        pad = "=" * (-len(payload_b64) % 4)
        payload_str = base64.urlsafe_b64decode(payload_b64 + pad).decode()
        expected_sig = _sign(payload_str)
        if not hmac.compare_digest(signature, expected_sig):
            return {"valid": False, "reason": "Signature invalide (clé falsifiée)"}
        obj = json.loads(payload_str)
        expires = datetime.fromisoformat(obj["expires"])
        now = datetime.now(timezone.utc)
        if now > expires:
            return {"valid": False, "reason": "Licence expirée", "expired": obj["expires"], **obj}
        days_left = (expires - now).days
        return {"valid": True, "days_left": days_left, **obj}
    except Exception as e:
        return {"valid": False, "reason": f"Erreur parsing : {e}"}


def _append_log(record: dict):
    log = []
    if LICENSE_LOG.exists():
        try:
            log = json.loads(LICENSE_LOG.read_text())
        except Exception:
            log = []
    log.append(record)
    if len(log) > 1000:
        log = log[-1000:]
    LICENSE_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


# ── Affichage ──────────────────────────────────────────────────────────────────

def print_tiers():
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       TIERS DE LICENCE — CaelumSwarm™ (LOUABLE)             ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    for tid, t in LICENSE_TIERS.items():
        wl = " 🏷️ WHITE-LABEL" if t["white_label"] else ""
        print(f"  ▸ [{tid}] {t['name']}{wl}")
        print(f"      {t['price_eur_month']}€/mois  |  {t['price_eur_year']}€/an")
        print(f"      {t['max_engines']} engines · {t['max_seats']} sièges · {t['api_calls_month']:,} appels API/mois")
        print(f"      SLA: {t['sla'] or '—'} · Support: {t['support']}")
        print(f"      {', '.join(t['features'][:3])}…")
        print()


def print_catalog():
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       CATALOGUE MODULES LOUABLES — CaelumSwarm™            ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    by_cat = {}
    for mid, m in RENTABLE_MODULES.items():
        by_cat.setdefault(m["category"], []).append((mid, m))
    for cat, mods in sorted(by_cat.items()):
        print(f"  ── {cat.upper()} ──")
        for mid, m in mods:
            print(f"    • [{mid}] {m['label']}")
            print(f"      {m['rent_eur_month']}€/mois (tier min: {m['tiers_min']})")
        print()
    total = sum(m["rent_eur_month"] for m in RENTABLE_MODULES.values())
    print(f"  💰 Valeur catalogue complète : {total:,}€/mois (location à la carte)\n")


def print_revenue_projection():
    """Projection simple de revenus locatifs par mix de tiers."""
    print("\n  PROJECTION REVENUS LOCATIFS (exemple de mix clients)")
    print("  ─────────────────────────────────────────────────────")
    mix = {"free": 500, "pro": 80, "enterprise": 12, "whitelabel": 2}
    total_month = 0
    for tier, count in mix.items():
        rev = LICENSE_TIERS[tier]["price_eur_month"] * count
        total_month += rev
        print(f"    {tier:<12} × {count:>4}  =  {rev:>10,}€/mois")
    print("  ─────────────────────────────────────────────────────")
    print(f"    {'TOTAL':<12}          =  {total_month:>10,}€/mois")
    print(f"    {'ARR projeté':<12}          =  {total_month*12:>10,}€/an\n")


def main():
    ap = argparse.ArgumentParser(description="Agent de gestion des licences CaelumSwarm™")
    ap.add_argument("--tiers", action="store_true", help="Afficher les tiers de licence")
    ap.add_argument("--catalog", action="store_true", help="Afficher le catalogue de modules louables")
    ap.add_argument("--issue", action="store_true", help="Émettre une licence")
    ap.add_argument("--tier", type=str, default="pro", help="Tier (free/pro/enterprise/whitelabel)")
    ap.add_argument("--customer", type=str, default="DEMO", help="Nom du client")
    ap.add_argument("--months", type=int, default=12, help="Durée en mois")
    ap.add_argument("--validate", type=str, metavar="KEY", help="Valider une clé de licence")
    ap.add_argument("--revenue", action="store_true", help="Projection de revenus locatifs")
    args = ap.parse_args()

    if args.tiers:
        print_tiers()
    elif args.catalog:
        print_catalog()
    elif args.revenue:
        print_revenue_projection()
    elif args.issue:
        rec = issue_license(args.tier, args.customer, args.months)
        print(f"\n✅ Licence émise — tier {args.tier} pour {args.customer}")
        print(f"   Expire : {rec['expires'][:10]}")
        print(f"   Sceau  : {rec['seal']}")
        print(f"   Signée : {'oui (HMAC)' if rec['signed'] else 'non (DEV — définir LICENSE_SIGNING_KEY)'}")
        print(f"\n   CLÉ :\n   {rec['key']}\n")
    elif args.validate:
        res = validate_license(args.validate)
        if res["valid"]:
            print(f"\n✅ Licence VALIDE")
            print(f"   Client : {res.get('customer')}")
            print(f"   Tier   : {res.get('tier')}")
            print(f"   Expire : {res.get('expires','?')[:10]} ({res.get('days_left')} jours restants)")
        else:
            print(f"\n❌ Licence INVALIDE — {res['reason']}")
            sys.exit(1)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
