#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent PRÉDICTIF & avant-gardiste — anticipe au lieu de subir.

Honnête : pas de divination. Il ANTICIPE à partir de données et de règles :
1) Maintenance prédictive : quels faits vont périmer bientôt (avant l'échéance) ;
2) Changements de loi attendus (depuis la veille juridique) ;
3) Prochains domaines prioritaires à construire (depuis la couverture) ;
4) Signaux saisonniers connus (indexations 1er janvier, rentrée scolaire, etc.).

Sortie : data/governance/predictions.md
"""
import json
import glob
import os
import pathlib
from datetime import date, datetime, timedelta

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
GOV = REPO / "data" / "governance"
DATA = REPO / "data" / "belgium"
OUT = GOV / "predictions.md"

HORIZON_JOURS = 60          # on prévient 60 j avant l'échéance de revue
CADENCE_JOURS = 180         # cadence de revue d'un fait


def lire(p, d=None):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except Exception:
        return d


def pdate(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def construire():
    today = date.today()
    # 1) maintenance prédictive
    bientot = []
    for fp in glob.glob(str(DATA / "*.json")):
        if os.path.basename(fp).startswith("_"):
            continue
        d = lire(fp, {})
        for f in d.get("faits", []):
            dv = pdate(f.get("date_verification", ""))
            if not dv:
                continue
            echeance = dv + timedelta(days=CADENCE_JOURS)
            reste = (echeance - today).days
            if 0 <= reste <= HORIZON_JOURS:
                bientot.append((os.path.basename(fp), f.get("id"), reste))
    bientot.sort(key=lambda x: x[2])

    # 2) changements de loi attendus
    veille = lire(GOV / "veille_juridique.json", {})
    signaux = veille.get("signaux", [])

    # 3) prochains domaines prioritaires
    taxo = lire(GOV / "domaines_droit_belge.json", {"domaines": []})
    a_venir = [d for d in taxo["domaines"] if d.get("statut") in ("a_venir", "partiel")]
    a_venir.sort(key=lambda d: {"haute": 0, "moyenne": 1, "basse": 2}.get(d.get("priorite"), 3))

    # 4) signaux saisonniers (règles connues)
    saison = [
        ("1er janvier", "Indexations annuelles (loyers, aide juridique, quotités, fiscalité) → revoir les montants."),
        ("Janvier–mars", "Déclarations fiscales à préparer → contenu impôts/délais."),
        ("Avril–juin", "Conflits de voisinage (haies, bruit, jardins) → pic saisonnier."),
        ("Août–septembre", "Rentrée scolaire (inscriptions, frais, refus) → pic enseignement."),
        ("Hiver", "Énergie : difficultés de paiement, coupures → renforcer le contenu énergie/CPAS."),
    ]

    L = []
    L.append("# 🔮 Agent prédictif — anticiper, pas subir")
    L.append("")
    L.append(f"*Généré le {today.isoformat()}. Anticipation par règles et signaux (pas de divination).*")
    L.append("")
    L.append(f"## 1. Maintenance prédictive — {len(bientot)} fait(s) à revoir dans les {HORIZON_JOURS} prochains jours")
    if bientot:
        for fichier, fid, reste in bientot[:50]:
            L.append(f"- {fichier} / {fid} — à revoir dans {reste} j")
    else:
        L.append("- Aucun fait n'arrive à échéance bientôt ✅")
    L.append("")
    L.append("## 2. Changements de loi attendus (veille)")
    for s in signaux:
        L.append(f"- **{s.get('sujet','')}** ({', '.join(s.get('regions', []))}) — {s.get('a_surveiller','')}")
    L.append("")
    L.append("## 3. Prochains domaines à construire (prédiction de besoin)")
    for d in a_venir:
        L.append(f"- {d['nom']} — priorité {d.get('priorite','')} ({d.get('statut')})")
    if not a_venir:
        L.append("- Tous les domaines prévus sont couverts ✅")
    L.append("")
    L.append("## 4. Signaux saisonniers (pics de demande à préparer à l'avance)")
    for periode, note in saison:
        L.append(f"- **{periode}** : {note}")
    L.append("")
    L.append("> Avant-gardiste = on prépare le contenu AVANT le pic de demande, et on met à jour AVANT la péremption.")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(bientot), len(signaux), len(a_venir)


if __name__ == "__main__":
    b, s, a = construire()
    print("═══ AGENT PRÉDICTIF ═══")
    print(f"  Faits à revoir bientôt : {b} | changements suivis : {s} | domaines à venir : {a}")
    print(f"  → {OUT}")
    print("✓ Prédictions générées (anticipation par règles & signaux).")
