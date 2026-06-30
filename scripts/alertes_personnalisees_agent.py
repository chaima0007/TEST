#!/usr/bin/env python3
"""
alertes_personnalisees_agent.py — Suivi de dossiers & alertes personnalisées.
================================================================================
Permet à un utilisateur de SUIVRE certains dossiers (modules / domaines) et de
recevoir une alerte quand l'un d'eux évolue. Branché sur les moteurs existants :
  - legal_change.json (capteur)  → fiches à re-vérifier
  - actualites_juridiques.json   → signaux de veille + mises à jour
  - dates de revue des fiches     → fraîcheur

Honnêteté (protocole) :
- Aucun utilisateur inventé. Le fichier d'abonnements contient un EXEMPLE clairement
  étiqueté (pas une personne réelle) + une liste réelle vide jusqu'à l'arrivée d'usagers.
- Aucune donnée personnelle : un abonnement = un identifiant opaque + une liste de suivis
  + un canal (à brancher plus tard : e-mail/push via webhook — décision réservée à Chaima).
- Les alertes ne sont calculées qu'à partir d'événements RÉELS détectés par les moteurs.

Sortie : data/alertes/abonnements.json (créé si absent) + data/alertes/alertes_a_envoyer.json
Usage  : python3 scripts/alertes_personnalisees_agent.py
"""
import json
import os
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT_DIR = os.path.join(DATA, "alertes")
MIRROR_DIR = os.path.join(ROOT, "laloiavecmoi", "data", "alertes")


def mirror():
    if os.path.isdir(os.path.dirname(MIRROR_DIR)):
        os.makedirs(MIRROR_DIR, exist_ok=True)
        for f in os.listdir(OUT_DIR):
            if f.endswith(".json"):
                shutil.copy(os.path.join(OUT_DIR, f), os.path.join(MIRROR_DIR, f))


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def ensure_abonnements():
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "abonnements.json")
    if os.path.exists(path):
        return path, load(path, {})
    seed = {
        "registre": "Abonnements — suivi personnalisé de dossiers",
        "principe": "Un abonnement = identifiant opaque + dossiers suivis + canal. "
                    "Aucune donnée personnelle. Le canal d'envoi (e-mail/push) sera "
                    "branché via webhook (décision réservée à Chaima).",
        "schema_abonnement": {
            "id": "opaque (uuid)", "suit_modules": ["module..."],
            "suit_domaines": ["domaine..."], "canal": "in_app|email|push",
            "actif": True, "cree_le": "YYYY-MM-DD",
        },
        "exemples_non_reels": [
            {"id": "EXEMPLE-001", "suit_modules": ["garantie_locative", "bail_*"],
             "suit_domaines": ["Logement & location"], "canal": "in_app",
             "actif": True, "cree_le": date.today().isoformat(),
             "_note": "EXEMPLE de démonstration — PAS un utilisateur réel."}
        ],
        "abonnements": [],   # vrais abonnements (vide jusqu'aux premiers usagers)
    }
    json.dump(seed, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return path, seed


def module_match(mod, patterns):
    for p in patterns or []:
        if p.endswith("*"):
            if (mod or "").startswith(p[:-1]):
                return True
        elif mod == p:
            return True
    return False


def build():
    path, abos = ensure_abonnements()

    # Événements réels disponibles
    lc = load(os.path.join(DATA, "legal_change.json"), {})
    a_reverifier = {(m.get("module") if isinstance(m, dict) else m) for m in lc.get("modules_a_reverifier", [])}
    actus = load(os.path.join(OUT_DIR.replace("alertes", "actualites"), "actualites_juridiques.json"), {})
    veille_domaines = set()
    for it in actus.get("items", []) if isinstance(actus, dict) else []:
        for r in it.get("regions", []):
            veille_domaines.add(r)

    # On évalue exemples + vrais abonnements ; on ne notifie QUE les vrais
    alertes = []
    evalues = (abos.get("exemples_non_reels", []) + abos.get("abonnements", []))
    for ab in evalues:
        reel = not str(ab.get("id", "")).startswith("EXEMPLE")
        decl = []
        for mod in ab.get("suit_modules", []):
            if any(module_match(m, [mod]) for m in a_reverifier):
                decl.append({"module": mod, "raison": "fiche signalée à re-vérifier"})
        if decl and reel:
            alertes.append({
                "abonnement_id": ab.get("id"),
                "canal": ab.get("canal", "in_app"),
                "declencheurs": decl,
                "statut": "à envoyer",
            })

    payload = {
        "genere_le": date.today().isoformat(),
        "abonnements_reels": len(abos.get("abonnements", [])),
        "exemples_demo": len(abos.get("exemples_non_reels", [])),
        "evenements_a_reverifier": len(a_reverifier),
        "alertes_a_envoyer": alertes,
        "canal_envoi": "NON CONNECTÉ — webhook e-mail/push réservé à une décision de Chaima.",
        "note": "Aucune alerte fabriquée ; seuls les vrais abonnements génèrent des envois.",
    }
    json.dump(payload, open(os.path.join(OUT_DIR, "alertes_a_envoyer.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return abos, payload


if __name__ == "__main__":
    abos, p = build()
    mirror()
    print("═══ ALERTES PERSONNALISÉES (suivi de dossiers) ═══")
    print(f"  Abonnements réels : {p['abonnements_reels']} | exemples démo : {p['exemples_demo']}")
    print(f"  Événements 'à re-vérifier' disponibles : {p['evenements_a_reverifier']}")
    print(f"  Alertes à envoyer : {len(p['alertes_a_envoyer'])}")
    print(f"  Canal : {p['canal_envoi']}")
    print("  → data/alertes/abonnements.json (+ alertes_a_envoyer.json)")
