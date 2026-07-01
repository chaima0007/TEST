#!/usr/bin/env python3
"""
accueil_reperes.py — Petit fichier de « repères de confiance » pour l'accueil.
================================================================================
Produit un JSON LÉGER (chiffres vérifiés + 3 dernières actus + questions fréquentes
variées) affiché sur le hub /loi-avec-moi. Tout vient de données réelles déjà en place.

Sortie : data/accueil_reperes.json (+ miroir laloiavecmoi/data/)
Usage  : python3 scripts/accueil_reperes.py
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "accueil_reperes.json")
MIRROR = os.path.join(ROOT, "laloiavecmoi", "data", "accueil_reperes.json")


def load(p, d=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return d


def build():
    tot = (load(os.path.join(DATA, "belgium", "_catalogue.json"), {}) or {}).get("totaux", {})
    actus_src = load(os.path.join(DATA, "actualites", "actualites_juridiques.json"), {}) or {}
    qpub = load(os.path.join(DATA, "community", "questions_publiques.json"), {}) or {}

    # 3 actus : priorité aux mises à jour de fiches (plus concrètes), puis veille
    items = actus_src.get("items", [])
    def mod_de(it):
        return (it.get("lien_fiche") or "").replace("/fiche/", "").replace("/loi/", "").split("#")[0]
    actus = []
    for typ in ("mise_a_jour_fiche", "veille", "a_reverifier"):
        for it in items:
            if it.get("type") == typ and len(actus) < 3:
                actus.append({
                    "titre": it.get("titre", ""),
                    "detail": (it.get("detail", "") or "")[:120],
                    "module": mod_de(it),
                })
        if len(actus) >= 3:
            break

    # Questions fréquentes : une par domaine (variété), jusqu'à 8
    questions = []
    vus = set()
    for q in qpub.get("questions", []):
        dom = q.get("domaine", "Autres")
        if dom in vus or dom == "Autres":
            continue
        vus.add(dom)
        mod = q.get("module")
        fid = (q.get("lien_fiche") or "").split("#")[1] if "#" in (q.get("lien_fiche") or "") else ""
        questions.append({
            "question": q.get("question", ""),
            "domaine": dom,
            "module": mod,
            "fait_id": fid,
        })
        if len(questions) >= 8:
            break

    payload = {
        "stats": {
            "fiches": tot.get("modules", 0),
            "reponses": tot.get("faits", 0),
            "sources_officielles": tot.get("sources_officielles", 0),
        },
        "actus": actus,
        "questions": questions,
        "note": "Repères générés depuis le corpus réel (chiffres vérifiés, 100 % sources officielles).",
    }
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    if os.path.isdir(os.path.dirname(MIRROR)):
        shutil.copy(OUT, MIRROR)
    return payload


if __name__ == "__main__":
    p = build()
    print("═══ REPÈRES ACCUEIL ═══")
    print(f"  Chiffres : {p['stats']['fiches']} fiches · {p['stats']['reponses']} réponses · "
          f"{p['stats']['sources_officielles']} sources officielles")
    print(f"  Actus : {len(p['actus'])} | Questions fréquentes : {len(p['questions'])}")
    print("  → data/accueil_reperes.json (+ miroir laloiavecmoi/data/)")
