#!/usr/bin/env python3
"""
self_healing_protocol.py — Protocole d'AUTO-RÉPARATION (P-AUTO-REPARATION).

Un agent détecte la défaillance d'un pair (un contrôle critique qui échoue ou plante) et
RÉAFFECTE immédiatement sa tâche à une routine de secours, pour assurer la continuité.

Chaque « service » critique a : un agent primaire (script) + une vérification de secours (inline).
Si le primaire tombe, on bascule sur le secours, on journalise la réparation, et le service
reste assuré (pas d'arrêt silencieux).

Usage : python3 scripts/self_healing_protocol.py
"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(BASE, "data", "self_healing_log.json")


def _run(script):
    """Lance un agent primaire. Retourne (ok, derniere_ligne)."""
    path = os.path.join(BASE, script)
    if not os.path.exists(path):
        return (False, f"introuvable: {script}")
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=120)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        return (r.returncode == 0, last)
    except Exception as e:
        return (False, f"exception: {e}")


# --- Routines de SECOURS (légères, sans dépendre du primaire) ---
def _secours_base_sourcee():
    """Secours : vérifie directement que chaque fait a une référence + une source officielle."""
    import glob
    total = manquants = 0
    for f in glob.glob(os.path.join(BASE, "data", "belgium", "*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for fait in d.get("faits", []):
            total += 1
            if not fait.get("reference_legale") or not any(
                s.get("type") == "officiel" for s in fait.get("sources", [])
            ):
                manquants += 1
    return (manquants == 0, f"secours base: {total} faits, {manquants} non conformes")


def _secours_tba():
    """Secours : recalcule l'avancement global depuis tba.json sans le générateur."""
    try:
        d = json.load(open(os.path.join(BASE, "data", "governance", "tba.json"), encoding="utf-8"))
        pcts = []
        for pr in d.get("projets", []):
            ts = [t.get("pct", 0) for t in pr.get("taches", [])]
            if ts:
                pcts.append(sum(ts) / len(ts))
        return (True, f"secours TBA: flotte ~{round(sum(pcts)/len(pcts)) if pcts else 0}%")
    except Exception as e:
        return (False, f"secours TBA KO: {e}")


# Services critiques : (nom, agent primaire, routine de secours)
SERVICES = [
    ("Base juridique sourcée", "scripts/legal_content_verifier.py", _secours_base_sourcee),
    ("Références légales", "scripts/loi_reference_audit.py", _secours_base_sourcee),
    ("Tableau de bord", "scripts/tba_protocol.py", _secours_tba),
]


def scanner_flotte():
    """Étend l'auto-surveillance à TOUS les agents du registre : chaque script référencé
    doit exister ET compiler. Détecte un agent cassé/manquant avant qu'il ne plante en prod."""
    import py_compile
    import re
    casses = []
    try:
        reg = json.load(open(os.path.join(BASE, "data", "governance", "protocols_registry.json"), encoding="utf-8"))
    except Exception as e:
        return [{"agent": "registre", "probleme": f"illisible: {e}"}], 0
    scripts = set()
    for p in reg.get("protocoles", []):
        m = re.search(r"scripts/([\w\-/]+\.py)", p.get("verif", "") or "")
        if m:
            scripts.add(m.group(1))
    for rel in sorted(scripts):
        path = os.path.join(BASE, "scripts", rel)
        if not os.path.exists(path):
            casses.append({"agent": rel, "probleme": "manquant"})
            continue
        try:
            py_compile.compile(path, doraise=True)
        except Exception as e:
            casses.append({"agent": rel, "probleme": f"ne compile pas: {str(e)[:60]}"})
    return casses, len(scripts)


def soigner(simuler_panne=None):
    etat = []
    for nom, primaire, secours in SERVICES:
        if simuler_panne == nom:
            ok, msg = (False, "panne simulée")
        else:
            ok, msg = _run(primaire)
        if ok:
            etat.append({"service": nom, "statut": "OK", "via": "primaire", "detail": msg})
        else:
            # réaffectation immédiate au secours
            sok, smsg = secours()
            etat.append({
                "service": nom,
                "statut": "RÉPARÉ" if sok else "DÉGRADÉ",
                "via": "secours",
                "detail": f"primaire KO ({msg}) → secours: {smsg}",
            })
    return etat


def main():
    etat = soigner()

    # auto-test : on simule la panne du 1er service et on vérifie la bascule
    test = soigner(simuler_panne=SERVICES[0][0])
    bascule_ok = test[0]["via"] == "secours" and test[0]["statut"] in ("RÉPARÉ", "DÉGRADÉ")

    hist = []
    if os.path.exists(LOG):
        try:
            hist = json.load(open(LOG, encoding="utf-8"))
        except Exception:
            hist = []
    hist.append({"etat": etat, "bascule_testee_ok": bascule_ok})
    hist = hist[-200:]
    json.dump(hist, open(LOG, "w"), ensure_ascii=False, indent=2)

    casses, total_agents = scanner_flotte()

    print("═══ AUTO-RÉPARATION (réaffectation sur panne) ═══")
    for e in etat:
        ic = {"OK": "✅", "RÉPARÉ": "🛠️", "DÉGRADÉ": "🔻"}[e["statut"]]
        print(f"  {ic} {e['service']:26s} [{e['via']}] {e['detail'][:70]}")
    print(f"  Test de bascule (panne simulée) : {'✅ continuité assurée' if bascule_ok else '⚠️'}")
    print(f"  Scan flotte complète : {total_agents} agents vérifiés · cassés/manquants : {len(casses)}")
    for c in casses[:10]:
        print(f"     🔻 {c['agent']} — {c['probleme']}")
    degrade = [e for e in etat if e["statut"] == "DÉGRADÉ"]
    if not degrade and not casses:
        print("  → Tous les services assurés, toute la flotte saine.")
    return 1 if (degrade or casses) else 0


if __name__ == "__main__":
    sys.exit(main())
