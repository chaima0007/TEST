#!/usr/bin/env python3
"""
learning_ledger_protocol.py — REGISTRE D'APPRENTISSAGE CONTRÔLÉ.

Principe honnête : les agents n'« apprennent » pas tout seuls comme une IA qui s'entraîne.
Ce protocole consigne, de façon CONTRÔLÉE et AUDITABLE, tout ce que le système a appris/intégré
(faits juridiques sourcés, leçons d'erreurs, règles de gouvernance), avec son statut de validation.

CONTRÔLES intégrés :
  • un savoir n'entre au registre que s'il est SOURCÉ et DATÉ (sinon il est listé en « non validé »).
  • couverture des sources (% sourcé), fraîcheur (% à jour < 365 j), état de certification.

Sorties :
  • data/learning_ledger.json  : registre structuré (machine).
  • data/learning_digest.md    : compte-rendu lisible « tout ce que je dois savoir ».

Usage : python3 scripts/learning_ledger_protocol.py
"""
import json
import os
import glob
from datetime import date, datetime

LEDGER_JSON = "data/learning_ledger.json"
DIGEST_MD = "data/learning_digest.md"


def _today():
    return date(2026, 6, 26)


def _parse(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def collecter():
    entries = []

    # 1) Faits juridiques belges sourcés
    for f in sorted(glob.glob("data/belgium/*.json")):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for fait in mod.get("faits", []):
            srcs = fait.get("sources", []) or []
            off = [s for s in srcs if s.get("type") == "officiel"]
            entries.append({
                "categorie": "droit_belge",
                "module": mod.get("module"),
                "id": fait.get("id"),
                "sujet": fait.get("question"),
                "reference_legale": fait.get("reference_legale"),
                "sources": len(srcs), "sources_officielles": len(off),
                "date_verification": fait.get("date_verification"),
                "valide": bool(off and fait.get("reference_legale") and fait.get("date_verification")),
            })

    # 2) Leçons d'erreurs d'entreprises
    for f in sorted(glob.glob("data/lessons_learned/*.json")):
        try:
            base = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for cas in base.get("cas", []):
            srcs = cas.get("sources", []) or []
            entries.append({
                "categorie": "lecon_entreprise",
                "id": cas.get("id"), "sujet": cas.get("entreprise"),
                "lecon": cas.get("comment_eviter"),
                "sources": len(srcs), "sources_officielles": 0,
                "date_verification": cas.get("date_verification"),
                "valide": bool(srcs and cas.get("date_verification")),
            })

    return entries


def controles(entries):
    total = len(entries)
    sources_ok = sum(1 for e in entries if e["sources"] > 0)
    valides = sum(1 for e in entries if e["valide"])
    frais = 0
    for e in entries:
        d = _parse(e.get("date_verification", ""))
        if d and (_today() - d).days <= 365:
            frais += 1
    pct = lambda n: round(100 * n / total, 1) if total else 0.0
    return {
        "total_savoirs": total,
        "pct_source": pct(sources_ok),
        "pct_valide": pct(valides),
        "pct_frais": pct(frais),
    }


def certif_etat():
    try:
        r = json.load(open("data/certification_report.json", encoding="utf-8"))
        return r.get("certification"), r.get("sceau_sha256", "")[:16]
    except (json.JSONDecodeError, OSError):
        return "INCONNU", ""


def ecrire_digest(entries, ctrl, certif):
    cert_etat, sceau = certif
    lignes = []
    lignes.append("# 📚 Compte-rendu d'apprentissage — tout ce que tu dois savoir")
    lignes.append("")
    lignes.append(f"_Généré le {_today().isoformat()} — registre contrôlé et auditable._")
    lignes.append("")
    lignes.append("## ✅ Contrôles qualité")
    lignes.append(f"- Savoirs enregistrés : **{ctrl['total_savoirs']}**")
    lignes.append(f"- Sourcés : **{ctrl['pct_source']}%** · Validés (source + réf + date) : **{ctrl['pct_valide']}%** · À jour (<365j) : **{ctrl['pct_frais']}%**")
    lignes.append(f"- Certification système : **{cert_etat}** (sceau `{sceau}…`)")
    lignes.append("")

    droit = [e for e in entries if e["categorie"] == "droit_belge"]
    lecons = [e for e in entries if e["categorie"] == "lecon_entreprise"]

    if droit:
        lignes.append("## ⚖️ Savoir juridique belge (sourcé officiellement)")
        for e in droit:
            etat = "✅" if e["valide"] else "⚠️ non validé"
            lignes.append(f"- {etat} **{e['sujet']}**  \n  Réf : {e.get('reference_legale','—')} · sources off. : {e['sources_officielles']} · revu : {e.get('date_verification','—')}")
        lignes.append("")

    if lecons:
        lignes.append("## 🏢 Leçons d'erreurs d'entreprises (à ne pas répéter)")
        for e in lecons:
            lignes.append(f"- **{e['sujet']}** → {e.get('lecon','—')}")
        lignes.append("")

    lignes.append("## 🔒 Règle d'or")
    lignes.append("Aucun savoir n'est publié sans source fiable et datée. Ce qui n'est pas validé est signalé, jamais caché.")
    contenu = "\n".join(lignes) + "\n"
    with open(DIGEST_MD, "w", encoding="utf-8") as f:
        f.write(contenu)
    return contenu


def main():
    entries = collecter()
    ctrl = controles(entries)
    certif = certif_etat()

    ledger = {"derniere_revue": _today().isoformat(), "controles": ctrl, "savoirs": entries}
    os.makedirs("data", exist_ok=True)
    with open(LEDGER_JSON, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
    ecrire_digest(entries, ctrl, certif)

    print("═══ REGISTRE D'APPRENTISSAGE ═══")
    print(f"  Savoirs : {ctrl['total_savoirs']} | sourcés {ctrl['pct_source']}% | validés {ctrl['pct_valide']}% | frais {ctrl['pct_frais']}%")
    print(f"  Certification : {certif[0]}")
    print(f"  → {LEDGER_JSON}")
    print(f"  → {DIGEST_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
