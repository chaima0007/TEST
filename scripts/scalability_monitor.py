#!/usr/bin/env python3
"""
scalability_monitor.py — Protocole SCALABILITÉ & MONITORING multi-plateforme (P-SCALABILITE).

Se greffe SANS rien remplacer sur les briques existantes (scalability_guardian, prometheus,
health-latency…). Son rôle propre : une vue AGRÉGÉE de capacité par plateforme, une PRÉVISION
de saturation (à partir de l'historique incrémental) et une ALERTE AVANT d'atteindre les limites.

Garantit que l'infrastructure peut supporter durablement l'ensemble des agents IA autonomes et
des données, en prévoyant les besoins futurs et en évitant toute saturation multi-plateforme.

Usage :
  python3 scripts/scalability_monitor.py          # rapport + journal incrémental
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(BASE, "data", "scalability_monitor_report.json")
HISTORY = os.path.join(BASE, "data", "scalability_monitor_history.json")
INCR_HISTORY = os.path.join(BASE, "data", "incremental_history.json")
HISTORY_MAX = 300

# Dimensions de capacité : (plateforme, libellé, valeur_courante, seuil_alerte, seuil_critique)
# Seuils alignés sur scalability_guardian (OOM Vercel, lag React) + marges de sécurité.


def _compter_fichiers(dossier, suffixe=".json", exclure_underscore=True):
    try:
        noms = os.listdir(dossier)
    except FileNotFoundError:
        return 0
    return sum(1 for n in noms if n.endswith(suffixe) and not (exclure_underscore and n.startswith("_")))


def _max_lignes_json(dossier):
    m = 0
    try:
        for n in os.listdir(dossier):
            if n.endswith(".json") and not n.startswith("_"):
                with open(os.path.join(dossier, n), encoding="utf-8") as f:
                    m = max(m, sum(1 for _ in f))
    except FileNotFoundError:
        pass
    return m


def _compter(path_glob_dir, suffixe):
    """Compte récursif d'un suffixe sous un dossier."""
    total = 0
    for racine, _, fichiers in os.walk(os.path.join(BASE, path_glob_dir)):
        if "node_modules" in racine:
            continue
        total += sum(1 for f in fichiers if f.endswith(suffixe))
    return total


def collecter():
    dims = []
    # Flotte d'agents IA autonomes
    agents = _compter_fichiers(os.path.join(BASE, "scripts"), ".py", exclure_underscore=False)
    dims.append(("Flotte d'agents", "Agents IA (scripts .py)", agents, 320, 450))
    # La Loi Avec Moi (données citoyens)
    dims.append(("La Loi Avec Moi", "Modules juridiques", _compter_fichiers(os.path.join(BASE, "data", "belgium")), 400, 600))
    dims.append(("La Loi Avec Moi", "Plus gros JSON (lignes)", _max_lignes_json(os.path.join(BASE, "data", "belgium")), 40000, 50000))
    # Caelum (entreprises)
    dims.append(("Caelum", "Modules conformité", _compter_fichiers(os.path.join(BASE, "data", "caelum")), 60, 120))
    # Site (routes Next.js — partagé)
    routes = _compter("app", "page.tsx")
    dims.append(("Site (Next.js)", "Routes (page.tsx)", routes, 380, 480))
    sidebar = _compter_fichiers(os.path.join(BASE, "components"), ".tsx", exclure_underscore=False)
    dims.append(("Site (Next.js)", "Composants (.tsx)", sidebar, 600, 900))
    # Gouvernance / données
    dims.append(("Gouvernance", "Fichiers de données (governance)", _compter_fichiers(os.path.join(BASE, "data", "governance")), 80, 150))
    return dims


def statut(valeur, alerte, critique):
    if valeur >= critique:
        return "CRITIQUE"
    if valeur >= alerte:
        return "ALERTE"
    return "OK"


def prevision_runway():
    """Prévoit les besoins futurs à partir de l'historique incrémental (rythme d'ajout observé)."""
    try:
        hist = json.load(open(INCR_HISTORY, encoding="utf-8"))
    except Exception:
        return None, "historique incrémental indisponible"
    runs = len(hist)
    total_nouveaux = sum(len(e.get("nouveaux", [])) for e in hist)
    if runs < 2:
        return None, "historique insuffisant pour une prévision fiable (≥ 2 passages requis)"
    rythme = total_nouveaux / runs  # nouveaux fichiers par passage
    return rythme, f"rythme observé : {rythme:.1f} nouveau(x) module(s)/passage sur {runs} passages"


def charger(path, defaut):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return defaut


COST_MODEL = os.path.join(BASE, "data", "cost_model.json")


def latence_proxies():
    """Proxies de latence mesurables HORS-LIGNE (build/SSR/cold-start). La latence runtime
    réelle est mesurée séparément par scripts/health-latency-monitor-agent.py (serveur requis)."""
    routes = _compter("app", "page.tsx")
    plus_gros_json = max(_max_lignes_json(os.path.join(BASE, "data", "belgium")),
                         _max_lignes_json(os.path.join(BASE, "data", "caelum")))
    return [
        ("Site (Next.js)", "Routes (coût de build/cold-start)", routes, 380, 480),
        ("Données", "Plus gros JSON (coût de parse/SSR, lignes)", plus_gros_json, 40000, 50000),
    ]


def cout():
    """Lit le modèle de coût (data/cost_model.json). N'invente AUCUN montant : signale les postes
    non renseignés au lieu de les remplir."""
    m = charger(COST_MODEL, None)
    if not m:
        return None
    res = {"devise": m.get("devise", "EUR"), "periode": m.get("periode", "mensuel"),
           "plateformes": {}, "postes_a_completer": 0}
    for plat, postes in m.get("plateformes", {}).items():
        connus = [v for v in postes.values() if isinstance(v, (int, float))]
        manquants = [k for k, v in postes.items() if not isinstance(v, (int, float))]
        res["postes_a_completer"] += len(manquants)
        res["plateformes"][plat] = {
            "total_connu": round(sum(connus), 2) if connus else 0,
            "postes_manquants": manquants,
        }
    return res


def auto_test():
    assert statut(10, 5, 8) == "CRITIQUE"
    assert statut(6, 5, 8) == "ALERTE"
    assert statut(2, 5, 8) == "OK"
    assert collecter(), "collecte vide"
    return True


def main():
    if "--test" in sys.argv:
        auto_test()
        print("✓ Auto-test OK")
        return 0

    dims = collecter()
    resultats = []
    pire = "OK"
    ordre = {"OK": 0, "ALERTE": 1, "CRITIQUE": 2}
    for plateforme, libelle, val, al, cr in dims:
        st = statut(val, al, cr)
        pct = round(val / cr * 100, 1) if cr else 0
        resultats.append({"plateforme": plateforme, "dimension": libelle,
                          "valeur": val, "seuil_alerte": al, "seuil_critique": cr,
                          "pct_du_critique": pct, "statut": st})
        if ordre[st] > ordre[pire]:
            pire = st

    rythme, note_prev = prevision_runway()
    # Prévision de saturation sur les modules La Loi Avec Moi (la zone qui grandit le plus vite)
    runway = None
    if rythme and rythme > 0:
        mod = next((r for r in resultats if r["dimension"] == "Modules juridiques"), None)
        if mod:
            restant = mod["seuil_critique"] - mod["valeur"]
            runway = int(restant / rythme) if restant > 0 else 0

    # Latence (proxies hors-ligne)
    lat = []
    for plateforme, libelle, val, al, cr in latence_proxies():
        st = statut(val, al, cr)
        lat.append({"plateforme": plateforme, "proxy": libelle, "valeur": val, "statut": st})
        if ordre[st] > ordre[pire]:
            pire = st
    cm = cout()

    rapport = {
        "protocole": "P-SCALABILITE",
        "verdict_global": pire,
        "dimensions": resultats,
        "latence_proxies": lat,
        "cout": cm,
        "prevision": {"note": note_prev, "runway_passages_avant_saturation_modules": runway},
    }
    json.dump(rapport, open(REPORT, "w"), ensure_ascii=False, indent=2)

    hist = charger(HISTORY, [])
    hist.append({"verdict_global": pire,
                 "alertes": [r["dimension"] for r in resultats if r["statut"] != "OK"]})
    json.dump(hist[-HISTORY_MAX:], open(HISTORY, "w"), ensure_ascii=False, indent=2)

    print("═══ SCALABILITÉ & MONITORING MULTI-PLATEFORME ═══")
    for r in resultats:
        icone = {"OK": "✅", "ALERTE": "🟠", "CRITIQUE": "🔴"}[r["statut"]]
        print(f"  {icone} {r['plateforme']:18s} {r['dimension']:32s} {r['valeur']:>6} / {r['seuil_critique']} ({r['pct_du_critique']}%)")
    print("  — Latence (proxies build/SSR) —")
    for l in lat:
        icone = {"OK": "✅", "ALERTE": "🟠", "CRITIQUE": "🔴"}[l["statut"]]
        print(f"    {icone} {l['plateforme']:18s} {l['proxy']:42s} {l['valeur']}")
    print("    ↳ latence runtime réelle : scripts/health-latency-monitor-agent.py (serveur requis)")
    if cm:
        print("  — Coût (modèle, sans montants inventés) —")
        for plat, info in cm["plateformes"].items():
            manq = f"{len(info['postes_manquants'])} poste(s) à compléter" if info["postes_manquants"] else "complet"
            print(f"    • {plat:18s} {info['total_connu']} {cm['devise']}/{cm['periode']} ({manq})")
        if cm["postes_a_completer"]:
            print(f"    ⚠️ {cm['postes_a_completer']} poste(s) de coût à renseigner avec les vraies factures.")
    print(f"  Prévision : {note_prev}")
    if runway is not None:
        print(f"  Marge avant saturation des modules : ~{runway} passages au rythme actuel.")
    print(f"  → Verdict global : {pire}")
    return 1 if pire == "CRITIQUE" else 0


if __name__ == "__main__":
    sys.exit(main())
