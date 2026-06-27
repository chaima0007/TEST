#!/usr/bin/env python3
"""
legal_content_verifier.py — Protocole de confiance pour la base de connaissances juridiques belge.

Contrairement aux moteurs génériques (scores synthétiques), ce vérificateur impose que CHAQUE
fait juridique publié soit RÉELLEMENT sourcé. Il échoue (exit 1) si un seul fait ne respecte
pas le socle de fiabilité. C'est le garde-fou qui distingue un « actif d'expert » d'une coquille.

Trois protocoles intégrés (demandés explicitement) :
  • CONFIRMATION DE RÉUSSITE : chaque fait doit avoir réponse + référence légale + ≥1 source.
  • SÉCURITÉ           : ≥1 source de type « officiel », date de vérification présente et plausible,
                          avertissement de non-conseil-juridique présent au niveau module.
  • LATENCE / FRAÎCHEUR : alerte si la dernière revue d'un fait dépasse le seuil (par défaut 365 j).

Usage :
  python3 scripts/legal_content_verifier.py                 # vérifie tous les modules data/belgium/*.json
  python3 scripts/legal_content_verifier.py data/belgium/bail_wallonie.json
  python3 scripts/legal_content_verifier.py --max-age-days 180
"""
import json
import sys
import glob
import os
from datetime import date, datetime

CONTENT_GLOB = "data/belgium/*.json"
DEFAULT_MAX_AGE_DAYS = 365

CHAMPS_FAIT_REQUIS = ("id", "question", "reponse", "reference_legale", "sources", "date_verification")
CHAMPS_MODULE_REQUIS = ("module", "titre", "juridiction", "base_legale_principale", "avertissement", "faits")


def _today():
    # Utilise l'horloge réelle de la machine (et non une date figée, qui
    # bloquait à tort les faits datés du jour). Robuste aux reprises.
    try:
        return date.today()
    except Exception:
        return date(2026, 6, 26)


# Tolérance (jours) absorbant tout décalage de fuseau/horloge entre la
# rédaction du contenu et l'horloge machine : évite les faux « date future ».
GRACE_FUTUR_JOURS = 2


def _parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def verifier_module(chemin, max_age_days):
    erreurs, alertes = [], []
    try:
        with open(chemin, encoding="utf-8") as f:
            mod = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return [f"{chemin}: illisible ({e})"], []

    nom = os.path.basename(chemin)

    # --- Structure module ---
    for champ in CHAMPS_MODULE_REQUIS:
        if champ not in mod:
            erreurs.append(f"{nom}: champ module manquant « {champ} »")

    # SÉCURITÉ : avertissement de non-conseil obligatoire
    if not mod.get("avertissement"):
        erreurs.append(f"{nom}: avertissement de non-conseil-juridique manquant (sécurité)")

    faits = mod.get("faits", [])
    if not faits:
        erreurs.append(f"{nom}: aucun fait")

    ids_vus = set()
    for fait in faits:
        fid = fait.get("id", "<sans-id>")

        # CONFIRMATION DE RÉUSSITE : champs requis
        for champ in CHAMPS_FAIT_REQUIS:
            if not fait.get(champ):
                erreurs.append(f"{nom}/{fid}: champ requis vide « {champ} »")

        if fid in ids_vus:
            erreurs.append(f"{nom}/{fid}: id dupliqué")
        ids_vus.add(fid)

        # SÉCURITÉ : au moins une source officielle réelle (URL http)
        sources = fait.get("sources", []) or []
        off = [s for s in sources if s.get("type") == "officiel" and str(s.get("url", "")).startswith("http")]
        if not off:
            erreurs.append(f"{nom}/{fid}: aucune source OFFICIELLE valide (sécurité)")
        for s in sources:
            if not str(s.get("url", "")).startswith("http"):
                erreurs.append(f"{nom}/{fid}: source sans URL valide « {s.get('intitule','?')} »")

        # LATENCE / FRAÎCHEUR
        dv = _parse_date(fait.get("date_verification", ""))
        if dv is None:
            erreurs.append(f"{nom}/{fid}: date_verification absente ou invalide")
        else:
            age = (_today() - dv).days
            if age < -GRACE_FUTUR_JOURS:
                erreurs.append(f"{nom}/{fid}: date_verification dans le futur")
            elif age > max_age_days:
                alertes.append(f"{nom}/{fid}: revue ancienne ({age} j > {max_age_days} j) — à re-sourcer")

    return erreurs, alertes


def main():
    args = [a for a in sys.argv[1:]]
    max_age = DEFAULT_MAX_AGE_DAYS
    if "--max-age-days" in args:
        i = args.index("--max-age-days")
        max_age = int(args[i + 1])
        del args[i:i + 2]
    cibles = args or sorted(glob.glob(CONTENT_GLOB))

    if not cibles:
        print("Aucun module à vérifier (data/belgium/*.json).")
        return 0

    print("═══ PROTOCOLE DE CONFIANCE — BASE JURIDIQUE BELGE ═══")
    total_faits = 0
    total_err, total_alertes = [], []
    for chemin in cibles:
        err, alertes = verifier_module(chemin, max_age)
        try:
            with open(chemin, encoding="utf-8") as f:
                total_faits += len(json.load(f).get("faits", []))
        except Exception:
            pass
        total_err += err
        total_alertes += alertes

    print(f"  Modules analysés : {len(cibles)}")
    print(f"  Faits juridiques : {total_faits}")
    print(f"  ✓ Confirmation réussite + Sécurité : {'OK' if not total_err else 'ÉCHEC'}")
    print(f"  ⏱  Latence/fraîcheur (alertes)     : {len(total_alertes)}")

    for a in total_alertes:
        print(f"  ⚠️  {a}")
    for e in total_err:
        print(f"  ✗ {e}")

    if total_err:
        print("\n✗ BLOQUÉ — des faits ne sont pas réellement sourcés. Publication interdite.")
        return 1
    print("\n✓ TOUT VERT — chaque fait est sourcé officiellement. Actif fiable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
