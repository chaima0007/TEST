#!/usr/bin/env python3
"""
work_journal_protocol.py — CARNET DE BORD du TRAVAIL (pas les bavardages).

Lit l'historique git (qui ne contient QUE du travail réel, daté) et produit un carnet de
bord propre, par jour : ce qui a été mis en place, à quelle heure, et le temps de mise en
place. Pour la confiance en soi et comme preuve pour l'école.

Filtre : ne garde que les livraisons de travail (feat/fix/docs/refactor), pas le bruit
technique (chore de régénération de rapports).

Sortie : data/work_journal.md

Usage : python3 scripts/work_journal_protocol.py
"""
import subprocess

OUT = "data/work_journal.md"
GARDER_PREFIXES = ("feat", "fix", "docs", "refactor", "perf")
EXCLURE_MOTS = ("re-sceau", "rapport de certification", "mise à jour scalabilit")


def git_log():
    r = subprocess.run(
        ["git", "log", "--date=format:%Y-%m-%d|%H:%M", "--pretty=format:%ad|%s"],
        capture_output=True, text=True
    )
    return r.stdout.splitlines()


def garder(sujet):
    s = sujet.lower()
    if any(m in s for m in EXCLURE_MOTS):
        return False
    return s.startswith(GARDER_PREFIXES)


def hhmm_to_min(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def main():
    jours = {}  # date -> list of (heure, sujet)
    for ligne in git_log():
        parts = ligne.split("|", 2)
        if len(parts) < 3:
            continue
        d, heure, sujet = parts
        if not garder(sujet):
            continue
        jours.setdefault(d, []).append((heure, sujet))

    L = ["# 🗂️ Mon carnet de bord — le travail réalisé", ""]
    L.append("*Généré depuis l'historique git (uniquement le travail concret, daté — aucun bavardage). "
             "Preuve fiable de ce qui a été mis en place et du temps pris.*")
    L.append("")

    total = 0
    for d in sorted(jours.keys(), reverse=True):
        items = sorted(jours[d])  # par heure croissante
        total += len(items)
        heures = [hhmm_to_min(h) for h, _ in items]
        duree = max(heures) - min(heures) if len(heures) > 1 else 0
        h, mn = divmod(duree, 60)
        L.append(f"## {d}")
        L.append(f"**{len(items)} réalisations** · de **{items[0][0]}** à **{items[-1][0]}** "
                 f"(fenêtre de travail : {h}h{mn:02d})")
        L.append("")
        for heure, sujet in items:
            # nettoyer le préfixe conventional-commit pour la lisibilité
            propre = sujet.split(":", 1)[1].strip() if ":" in sujet else sujet
            L.append(f"- 🕒 {heure} — {propre}")
        L.append("")

    L.insert(3, f"### 📌 Total : {total} réalisations concrètes enregistrées\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print("═══ CARNET DE BORD ═══")
    print(f"  Jours travaillés : {len(jours)} | Réalisations : {total}")
    print(f"  → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
