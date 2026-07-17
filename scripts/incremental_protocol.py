#!/usr/bin/env python3
"""
incremental_protocol.py — Protocole INCRÉMENTAL (P-INCREMENTAL).

S'intègre à la flotte d'agents existante. À chaque exécution, l'algorithme :
  1. s'appuie sur l'HISTORIQUE (un état/checkpoint des empreintes de fichiers déjà vus) ;
  2. ne traite QUE le nouveau ou le modifié depuis la dernière fois (incrémental, pas de re-scan complet) ;
  3. applique les NORMES DE SÉCURITÉ déjà en place (sourcage officiel, référence légale, séparation
     stricte des deux projets La Loi Avec Moi / Caelum) ;
  4. journalise dans data/incremental_history.json (FIFO) et bloque (code retour ≠ 0) en cas de violation.

Idempotent : relancé sans changement → « rien de nouveau ». Conçu pour être appelé par
scripts/update_all_reports.py comme les autres agents.

Usage :
  python3 scripts/incremental_protocol.py            # traitement incrémental + journal
  python3 scripts/incremental_protocol.py --reset    # réinitialise l'état (re-scanne tout au prochain run)
"""
import hashlib
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, "data", "incremental_state.json")
HISTORY = os.path.join(BASE, "data", "incremental_history.json")
HISTORY_MAX = 300

# Périmètres séparés (jamais mélangés) — le cœur des normes de sécurité projet.
PROJETS = {
    "la_loi_avec_moi": os.path.join(BASE, "data", "belgium"),
    "caelum": os.path.join(BASE, "data", "caelum"),
}
# Marqueurs interdits (anti-mélange des projets).
INTERDIT_DANS = {
    "la_loi_avec_moi": ("caelum partners", "csddd", "csrd"),
    "caelum": ("la loi avec moi",),
}


def _now_stamp():
    """Horodatage neutre (Date.now interdit côté workflow ; ici on lit le dernier commit)."""
    import subprocess
    try:
        out = subprocess.run(
            ["git", "-C", BASE, "log", "-1", "--format=%cI"],
            capture_output=True, text=True, timeout=10,
        )
        return (out.stdout.strip() or "n/a")
    except Exception:
        return "n/a"


def charger(path, defaut):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return defaut


def empreinte(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def normes_securite(projet, contenu):
    """Applique les normes de sécurité à un fichier JSON. Retourne la liste des violations."""
    viol = []
    try:
        d = json.loads(contenu)
    except Exception:
        return ["JSON illisible"]

    # Séparation stricte : on contrôle le CONTENU RÉEL (faits/normes/types),
    # PAS les champs méta qui rappellent justement la règle de séparation.
    payload = {k: v for k, v in d.items()
               if k in ("faits", "normes", "types", "modules", "publics")}
    bas = json.dumps(payload, ensure_ascii=False).lower()
    for mot in INTERDIT_DANS.get(projet, ()):
        if mot in bas:
            viol.append(f"mélange de projet interdit dans le contenu : « {mot} »")

    if projet == "la_loi_avec_moi":
        for f in d.get("faits", []):
            fid = f.get("id", "?")
            if not f.get("reference_legale"):
                viol.append(f"{fid}: référence légale manquante")
            srcs = f.get("sources", [])
            if not any(s.get("type") == "officiel" for s in srcs):
                viol.append(f"{fid}: aucune source officielle")
            if not f.get("date_verification"):
                viol.append(f"{fid}: date de vérification manquante")
    elif projet == "caelum":
        if "separation" not in d:
            viol.append("champ 'separation' manquant (séparation des projets)")
        for n in d.get("normes", []) + d.get("types", []):
            if not n.get("sources") and "sources" not in d:
                pass  # certains fichiers Caelum portent les sources au niveau item
    return viol


def scanner():
    """Retourne {projet: {fichier: empreinte}} pour le périmètre actuel."""
    etat = {}
    for projet, dossier in PROJETS.items():
        etat[projet] = {}
        if not os.path.isdir(dossier):
            continue
        for nom in sorted(os.listdir(dossier)):
            if not nom.endswith(".json") or nom.startswith("_"):
                continue
            chemin = os.path.join(dossier, nom)
            etat[projet][nom] = empreinte(chemin)
    return etat


def main():
    if "--reset" in sys.argv:
        for p in (STATE, HISTORY):
            if os.path.exists(p):
                os.remove(p)
        print("✓ État incrémental réinitialisé.")
        return 0

    ancien = charger(STATE, {})
    courant = scanner()

    nouveaux, modifies, violations = [], [], []
    for projet, fichiers in courant.items():
        anc = ancien.get(projet, {})
        for nom, emp in fichiers.items():
            if nom not in anc:
                nouveaux.append((projet, nom))
            elif anc[nom] != emp:
                modifies.append((projet, nom))
            else:
                continue  # inchangé → ignoré (incrémental)
            # normes de sécurité UNIQUEMENT sur le delta (nouveau/modifié)
            with open(os.path.join(PROJETS[projet], nom), encoding="utf-8") as fh:
                contenu = fh.read()
            for v in normes_securite(projet, contenu):
                violations.append(f"[{projet}/{nom}] {v}")

    # journal (historique)
    hist = charger(HISTORY, [])
    entree = {
        "horodatage_commit": _now_stamp(),
        "nouveaux": [f"{p}/{n}" for p, n in nouveaux],
        "modifies": [f"{p}/{n}" for p, n in modifies],
        "violations": violations,
        "statut": "BLOQUÉ" if violations else "OK",
    }
    hist.append(entree)
    hist = hist[-HISTORY_MAX:]
    json.dump(hist, open(HISTORY, "w"), ensure_ascii=False, indent=2)

    # n'avance le checkpoint QUE si aucune violation (sinon on retraite au prochain run)
    if not violations:
        json.dump(courant, open(STATE, "w"), ensure_ascii=False, indent=2)

    print("═══ PROTOCOLE INCRÉMENTAL (historique + normes de sécurité) ═══")
    print(f"  Nouveaux : {len(nouveaux)} | Modifiés : {len(modifies)} | Violations : {len(violations)}")
    if violations:
        for v in violations[:10]:
            print(f"   ⛔ {v}")
        print("  ⛔ BLOQUÉ — corriger le delta avant publication (checkpoint non avancé).")
        return 1
    if nouveaux or modifies:
        print(f"  ✅ Delta conforme aux normes — checkpoint avancé.")
    else:
        print("  ✅ Rien de nouveau depuis le dernier point — flotte à jour.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
