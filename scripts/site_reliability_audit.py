#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit de FIABILITÉ du grand site (app/ Next.js — La Loi Avec Moi).

But : vérifier que le contenu déjà en ligne s'appuie sur des sources OFFICIELLES.
On scanne les pages, on extrait les liens 'url: "..."', et on les classe selon la
liste blanche (tier1 officiel / tier2 institutionnel / hors liste).

Honnête : on mesure la PRÉSENCE et la QUALITÉ des sources citées ; on ne juge pas
ici l'exactitude juridique de chaque phrase (ça, c'est l'étape contenu).

Sortie : data/governance/site_reliability_report.md
"""
import re
import json
import pathlib
from datetime import date
from urllib.parse import urlparse

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
APP = REPO / "app"
GOV = REPO / "data" / "governance"
OUT = GOV / "site_reliability_report.md"

URL_RE = re.compile(r'https?://[^\s"\'<>)]+')


def charger_whitelist():
    wl = json.loads((GOV / "trusted_sources.json").read_text(encoding="utf-8"))
    return set(wl.get("tier1_officiel", [])), set(wl.get("tier2_institutionnel", []))


def domaine(url):
    try:
        net = urlparse(url).netloc.lower()
    except Exception:
        return ""
    if net.startswith("www."):
        net = net[4:]
    return net


def classe(dom, tier1, tier2):
    def match(s):
        return any(dom == d or dom.endswith("." + d) for d in s)
    if match(tier1):
        return "officiel"
    if match(tier2):
        return "institutionnel"
    return "hors_liste"


def auditer():
    tier1, tier2 = charger_whitelist()
    sections = {}  # section -> stats
    pages_sans_source = []
    domaines_hors = {}

    for fp in sorted(APP.rglob("*.tsx")):
        txt = fp.read_text(encoding="utf-8", errors="ignore")
        urls = URL_RE.findall(txt)
        # on ne garde que des liens "sources" plausibles (pas les assets/CDN)
        urls = [u for u in urls if not any(x in u for x in
                ("vercel", "googleapis", "gstatic", "fonts", "schema.org", "w3.org", "localhost"))]
        rel = fp.relative_to(APP)
        section = rel.parts[0] if len(rel.parts) > 1 else "(racine)"
        s = sections.setdefault(section, {"pages": 0, "pages_avec_source": 0,
                                          "off": 0, "inst": 0, "hors": 0})
        s["pages"] += 1
        if not urls:
            # seulement les vraies pages de contenu (page.tsx) comptent comme "sans source"
            if fp.name == "page.tsx":
                pages_sans_source.append(str(rel))
            continue
        s["pages_avec_source"] += 1
        for u in urls:
            d = domaine(u)
            c = classe(d, tier1, tier2)
            if c == "officiel":
                s["off"] += 1
            elif c == "institutionnel":
                s["inst"] += 1
            else:
                s["hors"] += 1
                domaines_hors[d] = domaines_hors.get(d, 0) + 1
    return sections, pages_sans_source, domaines_hors


def rapport(sections, pages_sans_source, domaines_hors):
    tot_off = sum(s["off"] for s in sections.values())
    tot_inst = sum(s["inst"] for s in sections.values())
    tot_hors = sum(s["hors"] for s in sections.values())
    tot_src = tot_off + tot_inst + tot_hors
    pct_off = round(100 * tot_off / tot_src) if tot_src else 0
    L = []
    L.append("# Audit de fiabilité — grand site (app/)")
    L.append("")
    L.append(f"*Généré le {date.today().isoformat()}. Mesure la présence et la qualité "
             "des sources citées dans les pages.*")
    L.append("")
    L.append(f"**Liens sources : {tot_src} · officiels : {tot_off} ({pct_off}%) · "
             f"institutionnels : {tot_inst} · hors liste : {tot_hors}**")
    L.append(f"**Pages de contenu sans aucune source : {len(pages_sans_source)}**")
    L.append("")
    L.append("## Par section")
    L.append("")
    L.append("| Section | Pages | Pages avec source | Off. | Inst. | Hors liste |")
    L.append("|---|---|---|---|---|---|")
    for nom in sorted(sections):
        s = sections[nom]
        L.append(f"| {nom} | {s['pages']} | {s['pages_avec_source']} | {s['off']} | "
                 f"{s['inst']} | {s['hors']} |")
    L.append("")
    if pages_sans_source:
        L.append("## ⚠️ Pages de contenu sans source citée (à enrichir)")
        for p in pages_sans_source[:80]:
            L.append(f"- {p}")
        L.append("")
    if domaines_hors:
        L.append("## Domaines cités hors liste blanche (à vérifier / classer)")
        for d, n in sorted(domaines_hors.items(), key=lambda x: -x[1])[:40]:
            L.append(f"- {d} ({n})")
        L.append("")
    L.append("## Lecture honnête")
    L.append("- Un % officiel élevé = bonne base de fiabilité. Les « hors liste » ne sont pas "
             "forcément faux : ce sont des domaines à vérifier puis à classer (tier1/2/3).")
    L.append("- Cet audit ne valide pas l'exactitude de chaque phrase : c'est l'étape suivante "
             "(revue de contenu par les protocoles juridiques).")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return tot_src, tot_off, pct_off, len(pages_sans_source)


if __name__ == "__main__":
    sections, sans, hors = auditer()
    tot_src, tot_off, pct_off, nb_sans = rapport(sections, sans, hors)
    print("═══ AUDIT FIABILITÉ — GRAND SITE (app/) ═══")
    print(f"  Sections analysées : {len(sections)}")
    print(f"  Liens sources : {tot_src} | officiels : {tot_off} ({pct_off}%)")
    print(f"  Pages de contenu sans source : {nb_sans}")
    print(f"  Domaines hors liste : {len(hors)}")
    print(f"  → {OUT}")
    print("✓ Audit terminé (présence/qualité des sources).")
