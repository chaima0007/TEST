#!/usr/bin/env python3
"""
communaute_qa_agent.py — Section « Questions de la communauté » (Q&R publiques).
================================================================================
Construit un index PUBLIC et navigable des questions juridiques, à partir des
VRAIES questions des fiches officielles (data/belgium/*.json). Chaque entrée
renvoie vers la fiche source (réponse complète + base légale + contacts).

Honnêteté (protocole) :
- Aucune donnée personnelle, aucun utilisateur inventé : les questions proviennent
  exclusivement du corpus officiel déjà vérifié.
- Le champ `popularite` reste null tant qu'il n'y a pas de vraies métriques d'usage
  (jamais de chiffres fabriqués).
- Quand de vraies questions d'utilisateurs arriveront, elles seront ajoutées via le
  flux de modération (voir data/community/moderation_policy.json) — anonymisées.

Sortie : data/community/questions_publiques.json
Usage  : python3 scripts/communaute_qa_agent.py
"""
import json
import glob
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "belgium")
OUT_DIR = os.path.join(ROOT, "data", "community")
MIRROR_DIR = os.path.join(ROOT, "laloiavecmoi", "data", "community")


def mirror():
    # Double miroir : l'app laloiavecmoi/ lit data/ relativement à son cwd.
    if os.path.isdir(os.path.dirname(MIRROR_DIR)):
        os.makedirs(MIRROR_DIR, exist_ok=True)
        for f in os.listdir(OUT_DIR):
            if f.endswith(".json"):
                shutil.copy(os.path.join(OUT_DIR, f), os.path.join(MIRROR_DIR, f))


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:60]


def resume(txt, n=240):
    txt = (txt or "").strip()
    return txt if len(txt) <= n else txt[: n - 1].rsplit(" ", 1)[0] + "…"


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    questions = []
    cats = {}
    for f in sorted(glob.glob(os.path.join(SRC, "*.json"))):
        b = os.path.basename(f)
        if b.startswith("_") or b.endswith(".md"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict) or not d.get("faits"):
            continue
        domaine = d.get("domaine") or "Autres"
        cats[domaine] = cats.get(domaine, 0) + len(d["faits"])
        for fait in d["faits"]:
            q = fait.get("question")
            if not q:
                continue
            questions.append({
                "id": f"QPUB-{slug(d.get('module',''))}-{fait.get('id','')}",
                "question": q,
                "domaine": domaine,
                "module": d.get("module"),
                "titre_fiche": d.get("titre"),
                "reponse_resume": resume(fait.get("reponse")),
                "reference_legale": fait.get("reference_legale"),
                "lien_fiche": f"/fiche/{d.get('module')}#{fait.get('id')}",
                "source_officielle": (fait.get("sources") or [{}])[0].get("url"),
                "popularite": None,        # jamais de métrique inventée
                "origine": "corpus_officiel",
            })

    payload = {
        "registre": "Questions de la communauté — index public navigable",
        "principe": "Questions issues du corpus officiel vérifié ; réponse complète "
                    "dans la fiche liée. Les futures questions d'utilisateurs seront "
                    "anonymisées et modérées avant publication.",
        "genere_le": date.today().isoformat(),
        "total_questions": len(questions),
        "categories": dict(sorted(cats.items(), key=lambda x: -x[1])),
        "questions": questions,
    }
    out = os.path.join(OUT_DIR, "questions_publiques.json")
    json.dump(payload, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # Politique de modération / anonymisation (cadre pour les vraies questions à venir)
    policy = {
        "registre": "Politique de modération & anonymisation — Q&R publiques",
        "regles": [
            "Aucune donnée personnelle publiée (nom, adresse, n° national, e-mail, téléphone).",
            "Anonymisation obligatoire avant publication d'une question d'utilisateur.",
            "Réponses fondées EXCLUSIVEMENT sur sources officielles (cf. §16/§21).",
            "Pas de conseil juridique individualisé : information générale + renvoi aux services compétents.",
            "Modération a priori : une question n'est publique qu'après validation.",
            "Droit à l'effacement : retrait sur simple demande.",
        ],
        "champs_interdits_publication": ["nom", "prenom", "adresse", "nn", "email", "telephone", "donnees_sante_identifiantes"],
        "statut_flux_utilisateurs": "EN ATTENTE — activé quand la plateforme aura des utilisateurs réels.",
    }
    json.dump(policy, open(os.path.join(OUT_DIR, "moderation_policy.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return payload


if __name__ == "__main__":
    p = build()
    mirror()
    print("═══ Q&R PUBLIQUES (communauté) ═══")
    print(f"  Questions publiées : {p['total_questions']} | catégories : {len(p['categories'])}")
    top = list(p["categories"].items())[:5]
    for k, v in top:
        print(f"   - {k} : {v}")
    print("  → data/community/questions_publiques.json (+ moderation_policy.json)")
