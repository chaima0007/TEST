#!/usr/bin/env python3
"""
mistral_fiches_verifier.py — Double contrôle : Mistral vérifie les fiches juridiques.
====================================================================================
Applique le principe collab-ia (Claude PROPOSE / Mistral VÉRIFIE) au vrai corpus
La Loi Avec Moi : pour chaque réponse, un SECOND modèle indépendant (Mistral) contrôle
la cohérence entre la réponse, sa référence légale et sa source — et signale les doutes.

HONNÊTETÉ (protocole) :
- Mistral est un SECOND AVIS, jamais une autorité : il SIGNALE des points à re-vérifier
  à la source officielle. Il ne modifie JAMAIS une fiche automatiquement.
- AUCUN credential en dur : la clé vient de la variable d'environnement MISTRAL_API_KEY.
- Dégradation gracieuse : sans clé ou sans réseau, le contrôle est déclaré SUSPENDU
  (on ne fabrique aucun verdict).
- Pas de plafond silencieux : l'échantillon vérifié est journalisé explicitement.

Usage :
  set MISTRAL_API_KEY=...            (Windows)   /   export MISTRAL_API_KEY=...   (Linux/macOS)
  python3 scripts/mistral_fiches_verifier.py            # échantillon (défaut : 25 réponses)
  python3 scripts/mistral_fiches_verifier.py --all      # tout le corpus (plus long / plus de tokens)
  python3 scripts/mistral_fiches_verifier.py --limit 50
  python3 scripts/mistral_fiches_verifier.py --model mistral-large-latest

Sortie : data/governance/mistral_fiches_report.md (+ .json)
"""
import os
import re
import json
import glob
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "belgium")
OUT_DIR = os.path.join(ROOT, "data", "governance")
ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

SYSTEME = (
    "Tu es un vérificateur juridique indépendant pour de l'information juridique belge "
    "destinée au grand public. On te donne UNE question, sa réponse, la référence légale "
    "citée et la source. Tu ne disposes pas d'accès web : juge uniquement la COHÉRENCE et "
    "la PLAUSIBILITÉ internes. Signale notamment : référence légale vague ou incohérente "
    "avec la réponse, affirmation chiffrée invérifiable présentée comme certaine, source "
    "qui ne semble pas officielle. Tu ne tranches pas le droit : tu signales ce qu'un "
    "humain devrait re-vérifier à la source officielle. Réponds STRICTEMENT en JSON : "
    '{"verdict":"ok|douteux","confiance":0-100,"raison":"…"}'
)


def charger_faits():
    faits = []
    for f in sorted(glob.glob(os.path.join(SRC, "*.json"))):
        b = os.path.basename(f)
        if b.startswith("_") or b.endswith(".md"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for fait in (d.get("faits") or []):
            src = (fait.get("sources") or [{}])
            faits.append({
                "module": d.get("module"),
                "id": fait.get("id"),
                "question": fait.get("question", ""),
                "reponse": fait.get("reponse", ""),
                "reference_legale": fait.get("reference_legale", ""),
                "source": (src[0] or {}).get("url", ""),
            })
    return faits


def appel_mistral(api_key, model, fait, timeout=40):
    contenu = (
        f"Question : {fait['question']}\n"
        f"Réponse : {fait['reponse']}\n"
        f"Référence légale citée : {fait['reference_legale']}\n"
        f"Source : {fait['source']}"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEME},
            {"role": "user", "content": contenu},
        ],
        "temperature": 0.1,
        "max_tokens": 300,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    txt = data["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", txt, re.DOTALL)
    if not m:
        return {"verdict": "indetermine", "confiance": 0, "raison": "réponse non-JSON", "_brut": txt[:200]}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"verdict": "indetermine", "confiance": 0, "raison": "JSON invalide", "_brut": txt[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="vérifier tout le corpus")
    ap.add_argument("--limit", type=int, default=25, help="taille de l'échantillon (défaut 25)")
    ap.add_argument("--model", default="mistral-small-latest")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    api_key = os.environ.get("MISTRAL_API_KEY")
    faits = charger_faits()
    cible = faits if args.all else faits[: args.limit]

    # Dégradation honnête : pas de clé → SUSPENDU, on n'invente rien.
    if not api_key:
        msg = ("# Double contrôle Mistral — SUSPENDU\n\n"
               "**MISTRAL_API_KEY non définie.** Aucun verdict fabriqué.\n\n"
               "Pour activer : définir la variable d'environnement `MISTRAL_API_KEY` "
               "(jamais en dur dans le code), puis relancer ce script.\n\n"
               f"- Réponses dans le corpus : {len(faits)}\n"
               f"- Échantillon prévu : {len(cible)} (utiliser --all pour tout)\n")
        open(os.path.join(OUT_DIR, "mistral_fiches_report.md"), "w", encoding="utf-8").write(msg)
        print("═══ DOUBLE CONTRÔLE MISTRAL ═══")
        print("  ⏸  SUSPENDU — MISTRAL_API_KEY absente (aucun verdict inventé).")
        print(f"  Corpus : {len(faits)} réponses · échantillon prévu : {len(cible)}")
        print("  → data/governance/mistral_fiches_report.md")
        return

    resultats, douteux, erreurs = [], [], 0
    for i, fait in enumerate(cible, 1):
        try:
            v = appel_mistral(api_key, args.model, fait)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            erreurs += 1
            v = {"verdict": "reseau_indisponible", "confiance": 0, "raison": str(e)[:120]}
        item = {**{k: fait[k] for k in ("module", "id", "question", "reference_legale")}, **v}
        resultats.append(item)
        if v.get("verdict") == "douteux":
            douteux.append(item)
        print(f"  [{i}/{len(cible)}] {fait['module']}/{fait['id']} → {v.get('verdict')}")

    rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "modele": args.model,
        "corpus_total": len(faits),
        "verifies": len(cible),
        "couverture": f"{len(cible)}/{len(faits)}" + (" (échantillon)" if not args.all else " (intégral)"),
        "douteux": len(douteux),
        "erreurs_reseau": erreurs,
        "principe": "Mistral = second avis indépendant ; signale, ne tranche pas, ne modifie rien.",
        "resultats": resultats,
    }
    json.dump(rapport, open(os.path.join(OUT_DIR, "mistral_fiches_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    lignes = [f"# Double contrôle Mistral — fiches La Loi Avec Moi",
              f"- Modèle : `{args.model}`",
              f"- Couverture : **{rapport['couverture']}**  (corpus : {len(faits)} réponses)",
              f"- Signalés « douteux » : **{len(douteux)}**   |   erreurs réseau : {erreurs}",
              "",
              "> Mistral est un **second avis indépendant** : il signale des points à "
              "re-vérifier à la source officielle. Il ne tranche pas le droit et ne modifie aucune fiche.",
              ""]
    if douteux:
        lignes.append("## Points signalés à re-vérifier")
        for d in douteux:
            lignes.append(f"- **{d['module']}/{d['id']}** (confiance {d.get('confiance','?')}) — "
                          f"{d.get('raison','')}\n  - réf. citée : {d.get('reference_legale','')}")
    else:
        lignes.append("## Aucun point « douteux » signalé sur l'échantillon vérifié.")
    open(os.path.join(OUT_DIR, "mistral_fiches_report.md"), "w", encoding="utf-8").write("\n".join(lignes))

    print("═══ DOUBLE CONTRÔLE MISTRAL ═══")
    print(f"  Couverture : {rapport['couverture']} | douteux : {len(douteux)} | erreurs réseau : {erreurs}")
    print("  → data/governance/mistral_fiches_report.md (+ .json)")


if __name__ == "__main__":
    main()
