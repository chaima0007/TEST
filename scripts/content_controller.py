#!/usr/bin/env python3
"""
content_controller.py — Contrôleur de contenu & viabilité (P-CONTROLE-CONTENU).

Un seul tableau de bord de fiabilité pour les DEUX projets, strictement séparés :
  • La Loi Avec Moi  → data/belgium/*.json  (faits juridiques citoyens)
  • Caelum           → data/caelum/conformite_entreprises.json (normes entreprises)

Pour chaque élément, le contrôleur vérifie le socle de viabilité :
  1. un texte de réponse/explication non vide ;
  2. une référence légale CONCRÈTE (loi, code, arrêté, décret, règlement, directive, convention…) ;
  3. au moins une SOURCE OFFICIELLE de confiance (tier-1, liste blanche trusted_sources.json) ;
  4. une date de vérification présente.

Sortie : data/governance/content_control_report.md (+ .json) et un score de viabilité par projet.
Code retour ≠ 0 si un projet n'est pas 100 % viable (garde-fou avant publication).

Usage : python3 scripts/content_controller.py
"""
import json
import os
import re
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BELGIUM = os.path.join(BASE, "data", "belgium")
CAELUM = os.path.join(BASE, "data", "caelum", "conformite_entreprises.json")
TRUSTED = os.path.join(BASE, "data", "governance", "trusted_sources.json")
OUT_MD = os.path.join(BASE, "data", "governance", "content_control_report.md")
OUT_JSON = os.path.join(BASE, "data", "governance", "content_control_report.json")

INSTRUMENT = re.compile(
    r"\b(loi|code|décret|decret|decreet|woninghuurdecreet|wooncode|arrêté|arrete|"
    r"ordonnance|règlement|reglement|constitution|directive|RGPD|convention|statut social)\b",
    re.IGNORECASE,
)


def tier1():
    try:
        return [d.lower() for d in json.load(open(TRUSTED, encoding="utf-8")).get("tier1_officiel", [])]
    except Exception:
        return []


T1 = tier1()


def est_officielle(src):
    if src.get("type") != "officiel":
        return False
    url = (src.get("url") or "").lower()
    host = re.sub(r"^https?://", "", url).split("/")[0]
    return any(host == d or host.endswith("." + d) for d in T1)


def controle_fait(f, champ_texte):
    pb = []
    if not (f.get(champ_texte) or "").strip():
        pb.append("texte vide")
    ref = f.get("reference_legale") or ""
    if not INSTRUMENT.search(ref):
        pb.append("référence légale vague")
    if not any(est_officielle(s) for s in f.get("sources", [])):
        pb.append("pas de source officielle (tier-1)")
    if not (f.get("date_verification") or "").strip():
        pb.append("date de vérification absente")
    return pb


def controle_projet(nom, items, champ_texte, label_item):
    total = len(items)
    conformes, problemes = 0, []
    for it in items:
        pb = controle_fait(it, champ_texte)
        if pb:
            problemes.append({"id": it.get("id"), "problemes": pb})
        else:
            conformes += 1
    score = round(100 * conformes / total) if total else 100
    return {"projet": nom, "total": total, "conformes": conformes,
            "viabilite_pct": score, "label_item": label_item, "problemes": problemes}


def main():
    # La Loi Avec Moi
    faits = []
    for fp in sorted(glob.glob(os.path.join(BELGIUM, "*.json"))):
        if os.path.basename(fp).startswith("_"):
            continue
        try:
            faits += json.load(open(fp, encoding="utf-8")).get("faits", [])
        except Exception:
            pass
    r_llam = controle_projet("La Loi Avec Moi", faits, "reponse", "réponses")

    # Caelum
    try:
        normes = json.load(open(CAELUM, encoding="utf-8")).get("normes", [])
    except Exception:
        normes = []
    r_cael = controle_projet("Caelum", normes, "changement", "normes")

    rapports = [r_llam, r_cael]
    global_ok = all(r["viabilite_pct"] == 100 for r in rapports)

    # Rapport Markdown
    L = ["# 🧪 Contrôleur de contenu & viabilité", ""]
    L.append("> Deux projets séparés. Viabilité = % d'éléments avec réponse + loi concrète + source officielle + date.")
    L.append("")
    for r in rapports:
        jauge = "█" * (r["viabilite_pct"] // 10) + "░" * (10 - r["viabilite_pct"] // 10)
        L.append(f"## {r['projet']}")
        L.append(f"- Viabilité : **{r['viabilite_pct']}%** `{jauge}` ({r['conformes']}/{r['total']} {r['label_item']})")
        if r["problemes"]:
            L.append(f"- ⚠️ À corriger ({len(r['problemes'])}) :")
            for p in r["problemes"][:20]:
                L.append(f"   - {p['id']} : {', '.join(p['problemes'])}")
        else:
            L.append("- ✅ Tout est viable (aucun problème).")
        L.append("")
    L.append("---")
    L.append("✅ **Contenu publiable**" if global_ok else "⛔ **Corriger les éléments ci-dessus avant publication**")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump({"rapports": rapports, "global_ok": global_ok}, open(OUT_JSON, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("═══ CONTRÔLEUR DE CONTENU & VIABILITÉ (2 projets) ═══")
    for r in rapports:
        print(f"  {r['projet']:<18} viabilité {r['viabilite_pct']}%  ({r['conformes']}/{r['total']} {r['label_item']})")
    print(f"  → rapport : data/governance/content_control_report.md")
    print("  ✅ Tout est viable et publiable." if global_ok else "  ⛔ Des éléments doivent être corrigés.")
    return 0 if global_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
