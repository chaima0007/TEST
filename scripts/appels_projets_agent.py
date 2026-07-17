#!/usr/bin/env python3
"""
Agent « Appels & Financements » — Caelum Partners (projet ENTREPRISES, séparé de La Loi Avec Moi).

Capacités :
  1. Veille     : charge le catalogue sourcé des aides & marchés (data/caelum/appels_projets.json).
  2. Matching   : « Quelle aide pour mon profil ? » (région, taille, secteur, besoin).
  3. Go/No-Go   : score pondéré d'un appel avant d'investir du temps.
  4. Conformité : relie au catalogue des normes (le cheat code : conformité = clé des marchés publics).

Usage :
  python3 scripts/appels_projets_agent.py                 # auto-test + démo
  python3 scripts/appels_projets_agent.py --match wallonie pme numerique cybersecurite
  python3 scripts/appels_projets_agent.py --gonogo 0.8 0.6 0.7 0.5
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = os.path.join(BASE, "data", "caelum", "appels_projets.json")
NORMES = os.path.join(BASE, "data", "caelum", "conformite_entreprises.json")

REGIONS = {"wallonie", "bruxelles", "flandre"}
TAILLES = {"independant", "pme", "grande"}
BESOINS = {"numerique", "cybersecurite", "conformite", "innovation", "marches_publics"}


def charger(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def matcher_aides(region, taille, secteur, besoin):
    """Retourne la liste des dispositifs pertinents pour un profil donné."""
    region = (region or "").lower()
    taille = (taille or "").lower()
    besoin = (besoin or "").lower()
    reco = []

    # --- Subventions régionales ---
    if region == "wallonie":
        reco.append(("Chèques-entreprises (Wallonie)",
                     "Maturité numérique, cybersécurité, conseil stratégique — prise en charge d'une part des honoraires.",
                     "https://www.digitalwallonia.be/fr/publications/aides-transformation-numerique/"))
    elif region == "bruxelles":
        reco.append(("Innoviris (Bruxelles)",
                     "Recherche & innovation. ⚠️ Budget limité en 2026 : vérifier la disponibilité AVANT de s'engager.",
                     "https://innoviris.brussels"))
    elif region == "flandre":
        reco.append(("VLAIO (Flandre)",
                     "Subsides innovation/numérique. Réforme 2026 : volet conseil recentré sur la cybersécurité.",
                     "https://www.vlaio.be"))

    # --- UE selon besoin / taille ---
    if besoin == "innovation" and taille in {"pme", "grande"}:
        reco.append(("Horizon Europe / EIC Accelerator (UE)",
                     "Innovation deep-tech. Montants élevés, très compétitif, souvent en consortium.",
                     "https://eic.ec.europa.eu"))
    if besoin in {"numerique", "cybersecurite"}:
        reco.append(("Digital Europe / EDIH (UE)",
                     "Pôles d'innovation numérique : accompagnent les PME sur la transfo numérique, l'IA et la cyber.",
                     "https://digital-strategy.ec.europa.eu"))

    # --- Marchés publics ---
    if besoin == "marches_publics" or taille in {"pme", "grande"}:
        reco.append(("e-Procurement (publicprocurement.be)",
                     "Plateforme fédérale officielle des marchés publics belges. Gratuite. Pensez aux LOTS réservés aux PME.",
                     "https://bosa.belgium.be/fr/applications/e-procurement"))
        reco.append(("TED — Tenders Electronic Daily (UE)",
                     "Marchés publics européens. Seuils revus à la baisse = davantage d'opportunités publiées.",
                     "https://ted.europa.eu"))

    # --- Cheat code conformité ---
    if besoin in {"conformite", "marches_publics"}:
        reco.append(("🔑 Conformité = clé des marchés publics",
                     "Le RGPD s'applique à TOUS les marchés publics et la cybersécurité est de plus en plus exigée. "
                     "Être conforme (via Caelum) vous rend éligible et mieux noté.",
                     "https://marchespublics.wallonie.be"))

    return reco


def go_nogo(eligibilite, proba_gain, valeur, effort_inverse):
    """Score pondéré (0..1) d'un appel. Poids alignés sur le catalogue.
    effort_inverse = 1 - effort (1 = peu d'effort, 0 = énorme effort)."""
    score = (eligibilite * 0.30 + proba_gain * 0.25 + valeur * 0.25 + effort_inverse * 0.20)
    if score >= 0.65:
        verdict = "GO ✅"
    elif score >= 0.45:
        verdict = "À ÉTUDIER 🟠"
    else:
        verdict = "NO-GO 🛑"
    return round(score, 3), verdict


def auto_test():
    cat = charger(CATALOGUE)
    assert cat["projet"] == "Caelum Partners"
    assert len(cat["types"]) == 2
    assert len(cat["process_caelum"]) == 4
    poids = sum(c["poids"] for c in cat["go_nogo_criteres"])
    assert abs(poids - 1.0) < 1e-9, f"poids Go/No-Go = {poids} (≠ 1.0)"
    normes = charger(NORMES)
    assert len(normes["normes"]) >= 6
    # matching renvoie quelque chose pour un profil type
    assert matcher_aides("wallonie", "pme", "numerique", "cybersecurite")
    # go/no-go cohérent
    s_hi, v_hi = go_nogo(0.9, 0.8, 0.8, 0.7)
    s_lo, v_lo = go_nogo(0.2, 0.2, 0.3, 0.2)
    assert s_hi > s_lo and v_hi.startswith("GO")
    print("✓ Auto-test OK — catalogue valide, poids = 1.0, matching + Go/No-Go cohérents.")
    return cat


def demo(cat):
    print("\n=== DÉMO : profil PME wallonne, besoin cybersécurité ===")
    for nom, why, url in matcher_aides("wallonie", "pme", "numerique", "cybersecurite"):
        print(f"  • {nom}\n      {why}\n      → {url}")
    print("\n=== DÉMO : Go/No-Go d'un appel (élig.=0.8, gain=0.6, valeur=0.7, effort faible=0.5) ===")
    score, verdict = go_nogo(0.8, 0.6, 0.7, 0.5)
    print(f"  Score = {score}  →  {verdict}")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--match" and len(args) == 5:
        for nom, why, url in matcher_aides(args[1], args[2], args[3], args[4]):
            print(f"• {nom}\n    {why}\n    → {url}")
        return
    if args and args[0] == "--gonogo" and len(args) == 5:
        vals = [float(x) for x in args[1:]]
        score, verdict = go_nogo(*vals)
        print(f"Score = {score}  →  {verdict}")
        return
    cat = auto_test()
    demo(cat)


if __name__ == "__main__":
    main()
