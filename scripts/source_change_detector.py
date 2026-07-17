#!/usr/bin/env python3
"""
source_change_detector.py — DÉTECTEUR DE CHANGEMENT DES SOURCES.

Lit chaque source officielle (tier1) de nos modules, télécharge la page et calcule une
empreinte (SHA-256). Compare à la dernière empreinte connue : si elle a changé, la loi/page
a peut-être évolué → à re-vérifier. Honnête : nécessite un accès réseau au moment de l'exécution.

POUR UNE VÉRIFICATION QUOTIDIENNE AUTOMATIQUE, il faut un planificateur persistant
(cron sur un serveur, ou une tâche planifiée). Cet environnement éphémère ne le permet pas
seul : ce script est prêt, mais doit être déclenché par un planificateur externe.

Sortie : data/governance/source_change_report.md (+ baseline data/governance/source_hashes.json)
Usage : python3 scripts/source_change_detector.py
"""
import json
import glob
import hashlib
import urllib.request
import urllib.error

BASE = "data/governance/source_hashes.json"
OUT = "data/governance/source_change_report.md"
TIER1 = set(json.load(open("data/governance/trusted_sources.json", encoding="utf-8"))["tier1_officiel"])


def urls_officielles():
    urls = set()
    for f in glob.glob("data/belgium/bail_*.json"):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for fait in mod.get("faits", []):
            for s in fait.get("sources", []) or []:
                if s.get("type") == "officiel":
                    urls.add(s.get("url"))
    return sorted(u for u in urls if u)


def empreinte(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (veille-fiabilite)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return hashlib.sha256(r.read()).hexdigest(), None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        return None, str(e)[:80]


def main():
    base = {}
    try:
        base = json.load(open(BASE, encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        base = {}

    changes, inchanges, injoignables = [], [], []
    nouveau = dict(base)
    for url in urls_officielles():
        h, err = empreinte(url)
        if err is not None:
            injoignables.append((url, err))
            continue
        if url in base and base[url] != h:
            changes.append(url)
        elif url not in base:
            inchanges.append(url)  # 1re mesure = référence
        else:
            inchanges.append(url)
        nouveau[url] = h

    json.dump(nouveau, open(BASE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    L = ["# 🔔 Détecteur de changement des sources officielles", ""]
    L.append("*Compare l'empreinte de chaque source à la dernière connue. Nécessite un accès réseau + un planificateur pour tourner quotidiennement.*")
    L.append("")
    L.append(f"- 🔴 Sources CHANGÉES (à re-vérifier d'urgence) : **{len(changes)}**")
    for u in changes:
        L.append(f"  - {u}")
    L.append(f"- 🟢 Inchangées / référence posée : **{len(inchanges)}**")
    L.append(f"- ⚪ Injoignables au moment du test : **{len(injoignables)}**")
    for u, e in injoignables[:10]:
        L.append(f"  - {u} ({e})")
    L.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print("═══ DÉTECTEUR DE CHANGEMENT DES SOURCES ═══")
    print(f"  Changées : {len(changes)} | inchangées : {len(inchanges)} | injoignables : {len(injoignables)}")
    print(f"  → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
