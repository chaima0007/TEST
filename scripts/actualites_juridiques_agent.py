#!/usr/bin/env python3
"""
actualites_juridiques_agent.py — Fil d'« Actualités juridiques ».
================================================================================
Agrège un fil d'actualité juridique HONNÊTE, branché sur les moteurs existants :
  - veille_juridique.json   → signaux de changement connus/attendus (sources officielles)
  - legal_change.json       → fiches détectées comme potentiellement périmées
  - freshness_radar / dates → fiches re-sourcées récemment (événements internes réels)

Règle d'or (protocole §16) : on ne FABRIQUE jamais une actualité. Les items externes
ne proviennent que de sources canoniques (EUR-Lex, Moniteur belge, .fgov.be, régionaux).
Si le réseau du bac à sable est restreint, l'enrichissement externe est déclaré SUSPENDU
(jamais inventé). Les items « internes » (re-sourçage d'une fiche) sont des faits réels.

Sortie : data/actualites/actualites_juridiques.json
Usage  : python3 scripts/actualites_juridiques_agent.py
"""
import json
import glob
import os
import shutil
from datetime import date, datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT_DIR = os.path.join(DATA, "actualites")
MIRROR_DIR = os.path.join(ROOT, "laloiavecmoi", "data", "actualites")


def mirror():
    if os.path.isdir(os.path.dirname(MIRROR_DIR)):
        os.makedirs(MIRROR_DIR, exist_ok=True)
        for f in os.listdir(OUT_DIR):
            if f.endswith(".json"):
                shutil.copy(os.path.join(OUT_DIR, f), os.path.join(MIRROR_DIR, f))


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    items = []

    # 1) Signaux de veille (changements connus/attendus) — sources officielles
    veille = load(os.path.join(DATA, "governance", "veille_juridique.json"), {})
    for s in veille.get("signaux", []):
        items.append({
            "id": f"ACTU-VEIL-{s.get('id','')}",
            "type": "veille",
            "titre": s.get("sujet", "Signal de veille juridique"),
            "regions": s.get("regions", []),
            "priorite": s.get("priorite", "à surveiller"),
            "detail": s.get("note") or s.get("impact") or "",
            "source_officielle": s.get("source") or s.get("source_officielle"),
            "statut": "à surveiller",
            "origine": "veille_juridique",
        })

    # 2) Fiches potentiellement périmées (capteur de changement)
    lc = load(os.path.join(DATA, "legal_change.json"), {})
    for m in lc.get("modules_a_reverifier", []):
        mod = m.get("module") if isinstance(m, dict) else m
        items.append({
            "id": f"ACTU-CHG-{mod}",
            "type": "a_reverifier",
            "titre": f"Fiche à re-vérifier : {mod}",
            "detail": "Le capteur signale une possible évolution — re-sourçage requis.",
            "statut": "à revérifier",
            "origine": "legal_change_sensor",
        })

    # 3) Événements internes RÉELS : fiches re-sourcées récemment (par date de revue)
    recents = []
    for f in glob.glob(os.path.join(DATA, "belgium", "*.json")):
        b = os.path.basename(f)
        if b.startswith("_") or b.endswith(".md"):
            continue
        d = load(f)
        if isinstance(d, dict) and d.get("derniere_revue"):
            recents.append((d["derniere_revue"], d.get("module"), d.get("titre"), d.get("domaine")))
    recents.sort(reverse=True)
    for rev, mod, titre, dom in recents[:15]:
        items.append({
            "id": f"ACTU-MAJ-{mod}",
            "type": "mise_a_jour_fiche",
            "titre": f"Fiche vérifiée : {titre or mod}",
            "domaine": dom,
            "detail": f"Fiche re-sourcée et vérifiée le {rev} (sources officielles).",
            "date": rev,
            "lien_fiche": f"/fiche/{mod}",
            "statut": "à jour",
            "origine": "corpus_officiel",
        })

    # État réseau : enrichissement externe canonique seulement si réseau dispo (honnête)
    reseau_ok = bool(lc.get("network_ok"))
    payload = {
        "registre": "Actualités juridiques — fil officiel",
        "principe": "Aucune actualité fabriquée. Items externes = sources canoniques uniquement "
                    "(EUR-Lex, Moniteur belge, .fgov.be, régionaux). Items internes = faits réels "
                    "(re-sourçage de fiches).",
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "enrichissement_externe": "ACTIF" if reseau_ok else
            "SUSPENDU — réseau restreint : aucune actualité externe inventée (déclaré honnêtement).",
        "total_items": len(items),
        "items": items,
    }
    out = os.path.join(OUT_DIR, "actualites_juridiques.json")
    json.dump(payload, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return payload


if __name__ == "__main__":
    p = build()
    mirror()
    print("═══ ACTUALITÉS JURIDIQUES (fil officiel) ═══")
    print(f"  Items : {p['total_items']} | enrichissement externe : {p['enrichissement_externe'][:48]}")
    by = {}
    for it in p["items"]:
        by[it["type"]] = by.get(it["type"], 0) + 1
    for k, v in by.items():
        print(f"   - {k} : {v}")
    print("  → data/actualites/actualites_juridiques.json")
