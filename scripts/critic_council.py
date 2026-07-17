#!/usr/bin/env python3
"""
critic_council.py — Conseil Critique (P-CRITIQUE).

Un collège d'« agents critiques » qui ne se contentent PAS du minimum (loi + source) :
ils cherchent activement ce qui empêche d'atteindre la PERFECTION et listent des
améliorations concrètes, priorisées. Chaque critique a une lentille exigeante :

  1. Profondeur      — réponses trop courtes (manque d'explication concrète).
  2. Délais          — la réponse évoque un délai/recours mais aucun « alerte_delai ».
  3. Contacts utiles — sujet sensible (urgence, violence, santé, aide) sans « contacts ».
  4. Robustesse source — un seul lien source (pas de second pour recouper).
  5. Fraîcheur       — date de vérification trop ancienne.
  6. Richesse module — module avec trop peu de faits.

Sortie : data/governance/critic_council_report.md (+ .json) et un SCORE DE PERFECTION (/100)
par projet, avec le top des améliorations à fort impact. Non bloquant (objectif : viser le sommet).

Usage : python3 scripts/critic_council.py
"""
import json
import os
import re
import glob
from datetime import date, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BELGIUM = os.path.join(BASE, "data", "belgium")
OUT_MD = os.path.join(BASE, "data", "governance", "critic_council_report.md")
OUT_JSON = os.path.join(BASE, "data", "governance", "critic_council_report.json")

MIN_REPONSE = 200          # caractères : en-dessous = jugé trop court
MIN_FAITS = 3              # un module en-dessous est jugé maigre
MAX_AGE_JOURS = 400        # fraîcheur
DELAI_MOTS = re.compile(r"\b(délai|delai|jours|mois|ans?|recours|prescription|introduire|au plus tard)\b", re.IGNORECASE)
SENSIBLE = re.compile(r"violenc|urgence|danger|santé|sante|suicide|abus|maltrait|aide|secours|112|détresse|detresse", re.IGNORECASE)


def jours_depuis(d):
    try:
        return (date.today() - datetime.strptime(d, "%Y-%m-%d").date()).days
    except Exception:
        return 0


def critiquer():
    findings = {"profondeur": [], "delais": [], "contacts": [], "source_unique": [], "fraicheur": [], "module_maigre": []}
    total_faits = 0
    for fp in sorted(glob.glob(os.path.join(BELGIUM, "*.json"))):
        name = os.path.basename(fp)
        if name.startswith("_"):
            continue
        try:
            d = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        faits = d.get("faits", [])
        if len(faits) < MIN_FAITS:
            findings["module_maigre"].append(f"{name} ({len(faits)} fait(s))")
        for f in faits:
            total_faits += 1
            fid = f.get("id", "?")
            rep = (f.get("reponse") or "")
            if len(rep) < MIN_REPONSE:
                findings["profondeur"].append(f"{fid} ({len(rep)} car.)")
            txt = (f.get("question", "") + " " + rep)
            if DELAI_MOTS.search(txt) and not f.get("alerte_delai"):
                findings["delais"].append(fid)
            if SENSIBLE.search(txt) and not f.get("contacts"):
                findings["contacts"].append(fid)
            if len([s for s in f.get("sources", []) if s.get("url")]) < 2:
                findings["source_unique"].append(fid)
            if jours_depuis(f.get("date_verification", "")) > MAX_AGE_JOURS:
                findings["fraicheur"].append(fid)
    return findings, total_faits


# Pondération de chaque critique dans le score de perfection (impact qualité perçue).
POIDS = {"profondeur": 0.30, "delais": 0.20, "contacts": 0.15, "source_unique": 0.15,
         "fraicheur": 0.10, "module_maigre": 0.10}
LABEL = {
    "profondeur": "Réponses à enrichir (trop courtes)",
    "delais": "Délais à signaler (alerte_delai manquante)",
    "contacts": "Sujets sensibles sans contacts d'aide",
    "source_unique": "Faits avec une seule source (recouper)",
    "fraicheur": "Faits à revérifier (anciens)",
    "module_maigre": "Modules à étoffer (peu de faits)",
}


def main():
    findings, total = critiquer()
    # Score : 100 − somme pondérée des taux d'éléments à améliorer (borné).
    penalite = 0.0
    for k, w in POIDS.items():
        n = len(findings[k])
        base = total if k != "module_maigre" else max(1, total // 4)
        taux = min(1.0, n / max(1, base))
        penalite += w * taux * 100
    score = max(0, round(100 - penalite, 1))

    L = ["# 🧠 Conseil Critique — viser le sommet de la perfection", ""]
    L.append(f"> {total} réponses passées au crible par 6 agents critiques. Objectif : zéro angle mort.")
    L.append("")
    L.append(f"## 🎯 Score de perfection (La Loi Avec Moi) : **{score}/100**")
    L.append("")
    L.append("## Améliorations prioritaires (par impact)")
    for k in sorted(POIDS, key=lambda x: -POIDS[x]):
        n = len(findings[k])
        if n == 0:
            L.append(f"- ✅ {LABEL[k]} : rien à signaler.")
        else:
            ex = ", ".join(findings[k][:8])
            L.append(f"- ⚠️ **{LABEL[k]} : {n}** — ex. : {ex}{' …' if n > 8 else ''}")
    L.append("")
    L.append("> Méthode : ces critiques vont AU-DELÀ du socle (loi + source). Les corriger fait passer "
             "la base d'« excellente » à « irréprochable ».")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump({"score_perfection": score, "total_faits": total,
               "findings": {k: len(v) for k, v in findings.items()},
               "exemples": {k: v[:20] for k, v in findings.items()}},
              open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("═══ CONSEIL CRITIQUE — viser le sommet ═══")
    print(f"  Score de perfection (La Loi Avec Moi) : {score}/100  ({total} réponses)")
    for k in sorted(POIDS, key=lambda x: -POIDS[x]):
        print(f"   {LABEL[k]:<42} : {len(findings[k])}")
    print(f"  → rapport : data/governance/critic_council_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
