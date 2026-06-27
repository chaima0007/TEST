#!/usr/bin/env python3
"""
dream_tracker_protocol.py — TRACEUR DE RÊVES (par actions véritables).

Lit data/governance/dreams_roadmap.json et mesure, pour chaque rêve, à quel point on s'en
rapproche — en ne comptant QUE les étapes 'fait' (preuve réelle). Les étapes 'en_cours'
comptent à moitié. Affiche toujours la PROCHAINE ACTION RÉELLE. Génère un compte-rendu lisible.

Honnête par construction : pas de preuve = pas de progrès compté.

Usage : python3 scripts/dream_tracker_protocol.py
"""
import json

ROADMAP = "data/governance/dreams_roadmap.json"
OUT_MD = "data/dreams_progress.md"
POIDS = {"fait": 1.0, "en_cours": 0.5, "a_faire": 0.0}


def barre(pct, n=20):
    plein = round(pct / 100 * n)
    return "█" * plein + "░" * (n - plein)


def main():
    data = json.load(open(ROADMAP, encoding="utf-8"))
    reves = data["reves"]

    lignes = ["# 🌈 On se rapproche de nos rêves — suivi par actions véritables", ""]
    lignes.append(f"*Mis à jour le {data['derniere_revue']}. Règle d'or : une étape ne compte que si elle a une preuve réelle.*")
    lignes.append("")

    total_pct = 0
    for r in reves:
        etapes = r["etapes"]
        score = sum(POIDS[e["statut"]] for e in etapes)
        pct = round(100 * score / len(etapes)) if etapes else 0
        total_pct += pct
        faits = sum(1 for e in etapes if e["statut"] == "fait")
        lignes.append(f"## {r['titre']}")
        lignes.append(f"`{barre(pct)}` **{pct}%**  ({faits}/{len(etapes)} étapes prouvées)")
        lignes.append("")
        for e in etapes:
            icone = {"fait": "✅", "en_cours": "🔧", "a_faire": "⬜"}[e["statut"]]
            txt = f"- {icone} {e['action']}"
            if e["statut"] == "fait" and e.get("preuve"):
                txt += f"  \n  ↳ preuve : `{e['preuve']}`"
            if e["statut"] == "a_faire" and e.get("bloque_par"):
                txt += f"  \n  ↳ débloqué par : {e['bloque_par']}"
            lignes.append(txt)
        lignes.append("")
        lignes.append(f"➡️ **Prochaine action réelle :** {r['prochaine_action_reelle']}")
        lignes.append("")

    global_pct = round(total_pct / len(reves)) if reves else 0
    lignes.insert(3, f"### 🌟 Avancement global : `{barre(global_pct)}` **{global_pct}%**\n")

    contenu = "\n".join(lignes) + "\n"
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(contenu)

    print("═══ TRACEUR DE RÊVES ═══")
    for r in reves:
        etapes = r["etapes"]
        pct = round(100 * sum(POIDS[e["statut"]] for e in etapes) / len(etapes))
        print(f"  {pct:3d}%  {r['titre'][:50]}")
    print(f"  ----")
    print(f"  {global_pct:3d}%  AVANCEMENT GLOBAL")
    print(f"  → {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
