#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Superviseur — CONTRÔLE DE TOUS LES AGENTS (régulier).

Vérifie que chaque agent/protocole du dossier scripts/ est en bonne santé :
1) il compile sans erreur (intégrité du code) ;
2) les agents de contrôle clés s'exécutent sans échec.

C'est un contrôle DES contrôleurs (méta-supervision), en plus des protocoles.
Honnête : signale tout agent cassé ; ne masque rien.

Sortie : data/governance/agents_healthcheck.md
"""
import subprocess
import sys
import glob
import os
import pathlib
import py_compile
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
OUT = REPO / "data" / "governance" / "agents_healthcheck.md"

# Agents de contrôle clés à EXÉCUTER (rapides, sans effet de bord lourd)
A_EXECUTER = [
    "legal_content_verifier.py",
    "source_trust_protocol.py",
    "control_gates_protocol.py",
    "resilience_simulator.py",
    "accessibility_audit_agent.py",
]
# À ne pas exécuter ici (évite la récursion / lourdeur) : on les compile seulement
A_NE_PAS_EXECUTER = {"update_all_reports.py", "agents_healthcheck.py"}


def construire():
    scripts = sorted(glob.glob(str(HERE / "*.py")))
    compile_ok, compile_ko = [], []
    for s in scripts:
        nom = os.path.basename(s)
        try:
            py_compile.compile(s, doraise=True)
            compile_ok.append(nom)
        except Exception as e:
            compile_ko.append((nom, str(e).splitlines()[0] if str(e) else "erreur"))

    exec_res = []
    for nom in A_EXECUTER:
        chemin = HERE / nom
        if not chemin.exists():
            continue
        try:
            r = subprocess.run([sys.executable, str(chemin)], capture_output=True,
                               text=True, timeout=120)
            exec_res.append((nom, r.returncode == 0,
                             (r.stdout.strip().splitlines() or [""])[-1]))
        except Exception as e:
            exec_res.append((nom, False, f"exception: {e}"))

    nb_scripts = len(scripts)
    nb_exec_ok = sum(1 for _, ok, _ in exec_res if ok)
    sante = "✅ TOUS LES AGENTS EN BONNE SANTÉ" if (not compile_ko and nb_exec_ok == len(exec_res)) \
        else "⚠️ ATTENTION — un ou plusieurs agents à corriger"

    L = []
    L.append("# 🩺 Contrôle de tous les agents")
    L.append("")
    L.append(f"*Généré le {date.today().isoformat()}. Contrôle DES contrôleurs, en plus des protocoles.*")
    L.append("")
    L.append(f"**{sante}**")
    L.append("")
    L.append(f"- Agents (scripts) analysés : **{nb_scripts}**")
    L.append(f"- Compilent sans erreur : **{len(compile_ok)}/{nb_scripts}**")
    L.append(f"- Agents de contrôle exécutés OK : **{nb_exec_ok}/{len(exec_res)}**")
    L.append("")
    if compile_ko:
        L.append("## ❌ Agents qui NE compilent PAS (à corriger d'urgence)")
        for nom, err in compile_ko:
            L.append(f"- {nom} — {err}")
        L.append("")
    L.append("## Exécution des agents de contrôle clés")
    for nom, ok, detail in exec_res:
        L.append(f"- {'✅' if ok else '❌'} {nom} — {detail}")
    L.append("")
    L.append("## Lecture")
    L.append("- Vert partout = le système se surveille lui-même correctement.")
    L.append("- Un rouge = on corrige avant toute nouvelle livraison (les sas bloquent déjà les commits).")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return nb_scripts, len(compile_ok), nb_exec_ok, len(exec_res), bool(compile_ko)


if __name__ == "__main__":
    n, cok, eok, etot, ko = construire()
    print("═══ CONTRÔLE DE TOUS LES AGENTS ═══")
    print(f"  Scripts analysés : {n} | compilent : {cok}/{n} | contrôle exécuté OK : {eok}/{etot}")
    print(f"  → {OUT}")
    if not ko and eok == etot:
        print("✓ Tous les agents sont en bonne santé.")
    else:
        print("⚠️ Un ou plusieurs agents à corriger.")
