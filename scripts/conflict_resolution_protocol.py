#!/usr/bin/env python3
"""
conflict_resolution_protocol.py — Résolution de conflit DÉCENTRALISÉE & PONDÉRÉE (P-CONFLIT).

Règle inspirée de la théorie des jeux, étendue aux SOURCES PONDÉRÉES :
chaque source a un poids de confiance selon son niveau (tier officiel > institutionnel >
secondaire). Quand des sources divergent sur une valeur, on additionne les poids par valeur
candidate et l'on retient celle de **poids cumulé maximal** (issue stable type Nash : aucune
coalition de poids inférieur ne peut renverser le résultat). Égalité de poids → version la
plus récente → à défaut, vote majoritaire.

Deux usages combinés :
  A) Conflit de DONNÉES : base canonique (data/belgium, poids 1.0) vs copie site
     (laloiavecmoi/data/belgium, poids 0.8) — la canonique l'emporte.
  B) FORCE PROBANTE : pour chaque fait, on pondère ses sources par leur tier (liste blanche)
     et l'on signale les faits dont la preuve est faible (aucune source de poids fort).

Usage :
  python3 scripts/conflict_resolution_protocol.py          # détecte + résout (rapport)
  python3 scripts/conflict_resolution_protocol.py --heal   # aligne la copie sur la canonique
"""
import glob
import json
import os
import sys
from collections import defaultdict
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Poids de confiance par niveau de source (théorie des jeux : payoff).
POIDS_TIER = {"tier1": 1.0, "tier2": 0.6, "tier3": 0.3, "inconnu": 0.1}

# « Agents » de données et leur poids global.
SOURCES = [
    {"id": "canonique", "dir": os.path.join(BASE, "data", "belgium"), "confiance": 1.0},
    {"id": "copie_site", "dir": os.path.join(BASE, "laloiavecmoi", "data", "belgium"), "confiance": 0.8},
]


def _charger_tiers():
    """Charge les domaines par tier depuis la liste blanche pour pondérer les sources."""
    try:
        t = json.load(open(os.path.join(BASE, "data", "governance", "trusted_sources.json"), encoding="utf-8"))
    except Exception:
        return {}, {}, {}
    return (set(t.get("tier1_officiel", [])),
            set(t.get("tier2_institutionnel", [])),
            set(t.get("tier3_secondaire_complement", [])))


T1, T2, T3 = _charger_tiers()


def poids_url(url):
    """Poids d'une source d'après le tier de son domaine (match suffixe, comme source_trust)."""
    try:
        dom = (urlparse(url).hostname or "").lower()
        if dom.startswith("www."):
            dom = dom[4:]
    except Exception:
        return POIDS_TIER["inconnu"]

    def match(ens):
        return any(dom == d or dom.endswith("." + d) for d in ens)

    if match(T1):
        return POIDS_TIER["tier1"]
    if match(T2):
        return POIDS_TIER["tier2"]
    if match(T3):
        return POIDS_TIER["tier3"]
    return POIDS_TIER["inconnu"]


def resoudre_pondere(candidats):
    """candidats = [{valeur, poids, date}] → (valeur_gagnante, poids_total, marge, stable).
    Issue stable : la valeur au poids cumulé le plus élevé ; égalité → plus récente."""
    if not candidats:
        return None
    score = defaultdict(float)
    recent = defaultdict(str)
    for c in candidats:
        score[c["valeur"]] += c["poids"]
        if c.get("date", "") > recent[c["valeur"]]:
            recent[c["valeur"]] = c.get("date", "")
    classement = sorted(score.items(), key=lambda kv: (kv[1], recent[kv[0]]), reverse=True)
    gagnant, poids_g = classement[0]
    poids_2 = classement[1][1] if len(classement) > 1 else 0.0
    # Stable au sens de Nash : aucune autre valeur (poids inférieur) ne peut renverser.
    stable = poids_g > poids_2
    return {"valeur": gagnant, "poids": round(poids_g, 2), "marge": round(poids_g - poids_2, 2), "stable": stable}


def charger(dossier):
    faits = {}
    for f in glob.glob(os.path.join(dossier, "*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for fait in d.get("faits", []):
            if fait.get("id"):
                faits[fait["id"]] = {
                    "reponse": fait.get("reponse", ""),
                    "date": fait.get("date_verification", ""),
                    "fichier": os.path.basename(f),
                    "sources": fait.get("sources", []),
                }
    return faits


def analyser_donnees():
    """A) Conflits entre la base canonique et la copie site, résolus par poids pondéré."""
    (sa, fa), (sb, fb) = [(s, charger(s["dir"])) for s in SOURCES]
    conflits = []
    for fid in sorted(set(fa) & set(fb)):
        if fa[fid]["reponse"] == fb[fid]["reponse"]:
            continue
        verdict = resoudre_pondere([
            {"valeur": sa["id"], "poids": sa["confiance"], "date": fa[fid]["date"]},
            {"valeur": sb["id"], "poids": sb["confiance"], "date": fb[fid]["date"]},
        ])
        conflits.append({"fait": fid, "fichier": fa[fid]["fichier"], "gagnant": verdict["valeur"], "marge": verdict["marge"]})
    return conflits, sa, sb, fa, fb


def auditer_force_probante(faits):
    """B) Pour chaque fait, poids de sa meilleure source. Signale les preuves faibles."""
    faibles = []
    for fid, f in faits.items():
        poids = [poids_url(s.get("url", "")) for s in f.get("sources", [])]
        meilleur = max(poids) if poids else 0.0
        if meilleur < POIDS_TIER["tier2"]:  # aucune source institutionnelle/officielle forte
            faibles.append({"fait": fid, "fichier": f["fichier"], "poids_max": round(meilleur, 2)})
    return faibles


def main():
    heal = "--heal" in sys.argv
    conflits, sa, sb, fa, fb = analyser_donnees()
    faibles = auditer_force_probante(fa)

    print("═══ RÉSOLUTION DE CONFLIT — MULTI-SOURCES PONDÉRÉES (théorie des jeux) ═══")
    print(f"  Poids : tier1={POIDS_TIER['tier1']} · tier2={POIDS_TIER['tier2']} · tier3={POIDS_TIER['tier3']} · inconnu={POIDS_TIER['inconnu']}")
    print(f"  A) Données : {len(set(fa) & set(fb))} faits comparés · conflits : {len(conflits)}")
    for c in conflits[:8]:
        print(f"     ⚖️  {c['fait']} ({c['fichier']}) → {c['gagnant']} (marge {c['marge']})")
    print(f"  B) Force probante : {len(fa)} faits évalués · preuves faibles : {len(faibles)}")
    for w in faibles[:8]:
        print(f"     ⚠️  {w['fait']} ({w['fichier']}) — poids source max {w['poids_max']}")

    if conflits and heal:
        import shutil
        fichiers = {c["fichier"] for c in conflits if c["gagnant"] == "canonique"}
        for f in fichiers:
            src, dst = os.path.join(sa["dir"], f), os.path.join(sb["dir"], f)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        print(f"  🛠️  {len(fichiers)} fichier(s) réalignés sur la source canonique.")

    json.dump(
        {"regle": "poids cumulé par tier > récence > majorité",
         "poids_tier": POIDS_TIER, "conflits_donnees": conflits, "preuves_faibles": faibles},
        open(os.path.join(BASE, "data", "conflict_resolution_report.json"), "w"),
        ensure_ascii=False, indent=2,
    )
    if not conflits and not faibles:
        print("  ✅ Sources cohérentes et toutes les preuves sont fortes.")
    elif conflits and not heal:
        print("  → Relancer avec --heal pour aligner automatiquement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
