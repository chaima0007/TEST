#!/usr/bin/env python3
"""
Funding Opportunities Monitor Agent — Caelum Partners SPRL
Agent mémoire/monitoring des opportunités de financement.
Lit, compare, met à jour et alerte sur les opportunités de financement.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
TRACKER_FILE = Path("/home/user/TEST/docs/candidatures/opportunities_tracker.json")
ALERT_DEADLINE_DAYS = 30  # Alerte si deadline dans moins de 30 jours

# Statuts possibles pour chaque opportunité
STATUTS_VALIDES = ["nouveau", "en_cours", "traite", "candidaté", "rejeté", "obtenu"]


# ─────────────────────────────────────────────
# Données simulées — nouvelles opportunités détectées
# ─────────────────────────────────────────────
def get_new_opportunities():
    today = datetime.now()
    return [
        {
            "id": "innoviris_bridge_2026",
            "nom": "Innoviris Bridge — Projets de transition numérique ESG",
            "organisme": "Innoviris",
            "type": "subvention",
            "montant_max": 250000,
            "deadline": (today + timedelta(days=45)).strftime("%Y-%m-%d"),
            "url": "https://innoviris.brussels/fr/nos-soutiens/bridge",
            "score_pertinence": 88,
            "score_eligibilite": 92,
            "region": "Bruxelles-Capitale",
            "statut": "nouveau",
            "date_detection": today.strftime("%Y-%m-%d"),
            "notes": "",
            "contacts": [],
            "documents_soumis": [],
        },
        {
            "id": "eic_accelerator_2026",
            "nom": "EIC Accelerator 2026 — Tech for Social Impact",
            "organisme": "EIC Accelerator",
            "type": "grant + equity",
            "montant_max": 2500000,
            "deadline": (today + timedelta(days=62)).strftime("%Y-%m-%d"),
            "url": "https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en",
            "score_pertinence": 95,
            "score_eligibilite": 78,
            "region": "Union Européenne",
            "statut": "nouveau",
            "date_detection": today.strftime("%Y-%m-%d"),
            "notes": "",
            "contacts": [],
            "documents_soumis": [],
        },
        {
            "id": "horizon_europe_cluster6",
            "nom": "Horizon Europe — Cluster 6 : Droits humains & supply chain",
            "organisme": "Horizon Europe",
            "type": "subvention R&D",
            "montant_max": 3000000,
            "deadline": (today + timedelta(days=78)).strftime("%Y-%m-%d"),
            "url": "https://research-and-innovation.ec.europa.eu/funding",
            "score_pertinence": 82,
            "score_eligibilite": 55,
            "region": "Union Européenne",
            "statut": "nouveau",
            "date_detection": today.strftime("%Y-%m-%d"),
            "notes": "Nécessite consortium 3 partenaires EU. À lancer rapidement.",
            "contacts": [],
            "documents_soumis": [],
        },
        {
            "id": "plan_relance_numerique",
            "nom": "Plan de Relance Belge — Axe Numérique PME",
            "organisme": "Plan de relance belge",
            "type": "subvention",
            "montant_max": 500000,
            "deadline": (today + timedelta(days=22)).strftime("%Y-%m-%d"),
            "url": "https://planderelance.belgique.be/fr/numerique",
            "score_pertinence": 79,
            "score_eligibilite": 85,
            "region": "Belgique",
            "statut": "nouveau",
            "date_detection": today.strftime("%Y-%m-%d"),
            "notes": "URGENT — deadline dans 22 jours. Dossier à préparer immédiatement.",
            "contacts": [],
            "documents_soumis": [],
        },
        {
            "id": "feder_brussels_2026",
            "nom": "FEDER Brussels Invest — Innovation Sociale & Tech",
            "organisme": "FEDER/FSE+",
            "type": "subvention FEDER",
            "montant_max": 800000,
            "deadline": (today + timedelta(days=110)).strftime("%Y-%m-%d"),
            "url": "https://feder.brussels/fr/appels-projets",
            "score_pertinence": 91,
            "score_eligibilite": 88,
            "region": "Bruxelles-Capitale",
            "statut": "nouveau",
            "date_detection": today.strftime("%Y-%m-%d"),
            "notes": "Très bon alignement. Priorité après Plan de Relance.",
            "contacts": [],
            "documents_soumis": [],
        },
        {
            "id": "bei_investeu_compliance",
            "nom": "BEI InvestEU — RegTech & Compliance Tech",
            "organisme": "BEI",
            "type": "prêt + garantie",
            "montant_max": 5000000,
            "deadline": (today + timedelta(days=180)).strftime("%Y-%m-%d"),
            "url": "https://www.eib.org/fr/products/investeu",
            "score_pertinence": 72,
            "score_eligibilite": 45,
            "region": "Union Européenne",
            "statut": "nouveau",
            "date_detection": today.strftime("%Y-%m-%d"),
            "notes": "CA actuel insuffisant. À recandidater en 2027 après montée en ARR.",
            "contacts": [],
            "documents_soumis": [],
        },
        {
            "id": "wallonie_entreprendre_tech",
            "nom": "Wallonie Entreprendre — Prêt Coup de Pouce Numérique",
            "organisme": "Wallonie Entreprendre",
            "type": "prêt participatif",
            "montant_max": 150000,
            "deadline": (today + timedelta(days=90)).strftime("%Y-%m-%d"),
            "url": "https://www.wallonie-entreprendre.be/financement",
            "score_pertinence": 58,
            "score_eligibilite": 62,
            "region": "Wallonie",
            "statut": "nouveau",
            "date_detection": today.strftime("%Y-%m-%d"),
            "notes": "Hors région principale mais potentiellement cumulable. À étudier.",
            "contacts": [],
            "documents_soumis": [],
        },
    ]


# ─────────────────────────────────────────────
# Lecture du tracker existant
# ─────────────────────────────────────────────
def load_tracker() -> dict:
    """Charge le fichier tracker existant ou crée une structure vide."""
    if TRACKER_FILE.exists():
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"[Monitor] Tracker existant chargé : {len(data.get('opportunites', []))} opportunités.")
            return data
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[Monitor] Erreur lecture tracker ({e}), création d'un nouveau.")

    return {
        "meta": {
            "societe": "Caelum Partners SPRL",
            "version": "1.0.0",
            "date_creation": datetime.now().isoformat(),
            "derniere_mise_a_jour": None,
        },
        "statistiques_globales": {
            "total_detectees": 0,
            "total_candidatees": 0,
            "total_obtenues": 0,
            "total_rejetees": 0,
            "montant_total_obtenu_eur": 0,
            "montant_total_soumis_eur": 0,
            "taux_succes_pct": 0.0,
        },
        "opportunites": [],
        "historique_mises_a_jour": [],
    }


# ─────────────────────────────────────────────
# Déduplication des opportunités
# ─────────────────────────────────────────────
def deduplicate(existing: list[dict], new_ones: list[dict]) -> tuple[list[dict], list[str], list[str]]:
    """
    Compare les nouvelles opportunités avec les existantes.
    Retourne (liste_merged, ids_nouveaux, ids_mis_a_jour).
    """
    existing_index = {opp["id"]: opp for opp in existing}
    ids_nouveaux = []
    ids_mis_a_jour = []

    for new_opp in new_ones:
        opp_id = new_opp["id"]
        if opp_id not in existing_index:
            # Nouvelle opportunité — l'ajouter
            existing_index[opp_id] = new_opp
            ids_nouveaux.append(opp_id)
        else:
            # Déjà connue — mettre à jour uniquement les champs non-éditoriaux
            existing_opp = existing_index[opp_id]
            updated = False
            for field in ["montant_max", "deadline", "url", "score_pertinence", "score_eligibilite"]:
                if existing_opp.get(field) != new_opp.get(field):
                    existing_opp[field] = new_opp[field]
                    updated = True
            if updated:
                ids_mis_a_jour.append(opp_id)
                existing_opp["date_derniere_mise_a_jour"] = datetime.now().strftime("%Y-%m-%d")

    merged = list(existing_index.values())
    return merged, ids_nouveaux, ids_mis_a_jour


# ─────────────────────────────────────────────
# Détection des alertes urgentes
# ─────────────────────────────────────────────
def detect_alerts(opportunites: list[dict]) -> list[dict]:
    """Détecte les opportunités avec deadline imminente et statut actif."""
    today = datetime.now()
    alerts = []
    actifs_statuts = {"nouveau", "en_cours", "traite"}

    for opp in opportunites:
        if opp.get("statut") not in actifs_statuts:
            continue
        try:
            deadline_dt = datetime.strptime(opp["deadline"], "%Y-%m-%d")
            days_left = (deadline_dt - today).days
            if days_left < 0:
                alerts.append({
                    "id": opp["id"],
                    "nom": opp["nom"],
                    "type_alerte": "EXPIREE",
                    "message": f"Deadline dépassée depuis {abs(days_left)} jours — à archiver",
                    "priorite": "HAUTE",
                    "jours_restants": days_left,
                })
            elif days_left <= ALERT_DEADLINE_DAYS:
                priorite = "CRITIQUE" if days_left <= 7 else ("HAUTE" if days_left <= 14 else "NORMALE")
                alerts.append({
                    "id": opp["id"],
                    "nom": opp["nom"],
                    "organisme": opp.get("organisme"),
                    "type_alerte": "DEADLINE_PROCHE",
                    "message": (
                        f"Deadline dans {days_left} jour(s) — "
                        f"{opp['deadline']} — Statut: {opp.get('statut', '?')}"
                    ),
                    "priorite": priorite,
                    "jours_restants": days_left,
                    "score_pertinence": opp.get("score_pertinence", 0),
                    "score_eligibilite": opp.get("score_eligibilite", 0),
                    "montant_max": opp.get("montant_max", 0),
                    "url": opp.get("url", ""),
                })
        except (ValueError, KeyError):
            pass

    alerts.sort(key=lambda x: x["jours_restants"])
    return alerts


# ─────────────────────────────────────────────
# Calcul des statistiques globales
# ─────────────────────────────────────────────
def compute_stats(opportunites: list[dict]) -> dict:
    total = len(opportunites)
    candidatees = [o for o in opportunites if o.get("statut") == "candidaté"]
    obtenues = [o for o in opportunites if o.get("statut") == "obtenu"]
    rejetees = [o for o in opportunites if o.get("statut") == "rejeté"]
    en_cours = [o for o in opportunites if o.get("statut") in ("nouveau", "en_cours", "traite")]

    montant_soumis = sum(o.get("montant_max", 0) for o in candidatees + obtenues + rejetees)
    montant_obtenu = sum(o.get("montant_max", 0) for o in obtenues)
    taux_succes = (len(obtenues) / len(candidatees + obtenues + rejetees) * 100) if (candidatees + obtenues + rejetees) else 0.0

    scores_pertinence = [o.get("score_pertinence", 0) for o in opportunites if o.get("score_pertinence")]
    scores_eligibilite = [o.get("score_eligibilite", 0) for o in opportunites if o.get("score_eligibilite")]

    return {
        "total_detectees": total,
        "en_cours": len(en_cours),
        "total_candidatees": len(candidatees),
        "total_obtenues": len(obtenues),
        "total_rejetees": len(rejetees),
        "montant_total_soumis_eur": montant_soumis,
        "montant_total_obtenu_eur": montant_obtenu,
        "taux_succes_pct": round(taux_succes, 1),
        "score_pertinence_moyen": round(sum(scores_pertinence) / len(scores_pertinence), 1) if scores_pertinence else 0,
        "score_eligibilite_moyen": round(sum(scores_eligibilite) / len(scores_eligibilite), 1) if scores_eligibilite else 0,
        "montant_potentiel_actif_eur": sum(o.get("montant_max", 0) for o in en_cours),
    }


# ─────────────────────────────────────────────
# Sauvegarde du tracker
# ─────────────────────────────────────────────
def save_tracker(tracker: dict):
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(tracker, f, ensure_ascii=False, indent=2)
    print(f"[Monitor] Tracker sauvegardé : {TRACKER_FILE}")


# ─────────────────────────────────────────────
# Rapport console
# ─────────────────────────────────────────────
def print_monitor_report(tracker: dict, alerts: list[dict], ids_nouveaux: list[str], ids_mis_a_jour: list[str]):
    stats = tracker["statistiques_globales"]
    opps = tracker["opportunites"]

    print("\n" + "=" * 70)
    print("  CAELUM PARTNERS — MONITORING OPPORTUNITÉS DE FINANCEMENT")
    print("  Funding Opportunities Monitor Agent")
    print("=" * 70)
    print(f"  Date du rapport : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Fichier tracker : {TRACKER_FILE}")
    print("=" * 70)

    print("\n  --- STATISTIQUES GLOBALES ---")
    print(f"  Total opportunites detectées  : {stats['total_detectees']}")
    print(f"  En cours (actives)            : {stats['en_cours']}")
    print(f"  Dossiers soumis               : {stats['total_candidatees']}")
    print(f"  Financements obtenus          : {stats['total_obtenues']}")
    print(f"  Refus reçus                   : {stats['total_rejetees']}")
    print(f"  Taux de succès                : {stats['taux_succes_pct']}%")
    print(f"  Montant potentiel actif       : {stats.get('montant_potentiel_actif_eur', 0):,}€".replace(",", "."))
    print(f"  Montant total soumis          : {stats['montant_total_soumis_eur']:,}€".replace(",", "."))
    print(f"  Montant total obtenu          : {stats['montant_total_obtenu_eur']:,}€".replace(",", "."))
    print(f"  Score pertinence moyen        : {stats.get('score_pertinence_moyen', 0)}/100")
    print(f"  Score eligibilite moyen       : {stats.get('score_eligibilite_moyen', 0)}/100")

    if ids_nouveaux:
        print(f"\n  --- NOUVELLES OPPORTUNITÉS DÉTECTÉES ({len(ids_nouveaux)}) ---")
        for opp_id in ids_nouveaux:
            opp = next((o for o in opps if o["id"] == opp_id), None)
            if opp:
                print(f"    + {opp['nom'][:55]}")
                print(f"      Organisme: {opp['organisme']} | Max: {opp['montant_max']:,}€ | Score: {opp['score_pertinence']}/100".replace(",", "."))

    if ids_mis_a_jour:
        print(f"\n  --- OPPORTUNITÉS MISES À JOUR ({len(ids_mis_a_jour)}) ---")
        for opp_id in ids_mis_a_jour:
            print(f"    ~ {opp_id}")

    if alerts:
        print(f"\n  *** ALERTES URGENTES ({len(alerts)}) ***")
        for alert in alerts:
            emoji_map = {"CRITIQUE": "!!!", "HAUTE": "!!", "NORMALE": "!"}
            marker = emoji_map.get(alert["priorite"], "!")
            print(f"\n  {marker} [{alert['priorite']}] {alert['nom'][:55]}")
            print(f"    {alert['message']}")
            if alert.get("montant_max"):
                print(f"    Montant max : {alert['montant_max']:,}€ | URL: {alert.get('url', '')}".replace(",", "."))
    else:
        print("\n  Aucune alerte urgente (toutes les deadlines > 30 jours).")

    print("\n  --- TABLEAU DE BORD PAR STATUT ---")
    by_status = {}
    for opp in opps:
        s = opp.get("statut", "inconnu")
        by_status.setdefault(s, []).append(opp)

    for statut, opps_list in sorted(by_status.items()):
        print(f"\n  [{statut.upper()}] — {len(opps_list)} opportunité(s)")
        for opp in sorted(opps_list, key=lambda x: x.get("score_pertinence", 0), reverse=True):
            deadline_dt = datetime.strptime(opp["deadline"], "%Y-%m-%d")
            days = (deadline_dt - datetime.now()).days
            deadline_str = f"{opp['deadline']} ({days}j)" if days >= 0 else f"{opp['deadline']} (EXPIRÉE)"
            print(f"    - {opp['nom'][:50]:<50} | Score: {opp['score_pertinence']}/100 | {deadline_str}")

    print("\n" + "=" * 70 + "\n")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    print("[Funding Monitor Agent] Démarrage du monitoring des opportunités...")

    # 1. Charger le tracker existant
    tracker = load_tracker()

    # 2. Récupérer les nouvelles opportunités
    new_opportunities = get_new_opportunities()
    print(f"[Monitor] {len(new_opportunities)} opportunités scannées.")

    # 3. Fusionner avec déduplication
    merged, ids_nouveaux, ids_mis_a_jour = deduplicate(
        tracker["opportunites"], new_opportunities
    )
    tracker["opportunites"] = merged

    # 4. Calcul des stats
    stats = compute_stats(merged)
    tracker["statistiques_globales"] = stats

    # 5. Détection des alertes
    alerts = detect_alerts(merged)

    # 6. Mise à jour des métadonnées
    tracker["meta"]["derniere_mise_a_jour"] = datetime.now().isoformat()
    tracker["historique_mises_a_jour"].append({
        "date": datetime.now().isoformat(),
        "nouvelles": len(ids_nouveaux),
        "mises_a_jour": len(ids_mis_a_jour),
        "alertes": len(alerts),
        "total_actives": stats["en_cours"],
    })

    # 7. Sauvegarder le tracker
    save_tracker(tracker)

    # 8. Afficher le rapport
    print_monitor_report(tracker, alerts, ids_nouveaux, ids_mis_a_jour)

    # 9. Sortie JSON
    output = {
        "agent": "funding-opportunities-monitor-agent",
        "version": "1.0.0",
        "date_rapport": datetime.now().isoformat(),
        "tracker_file": str(TRACKER_FILE),
        "nouvelles_opportunites": len(ids_nouveaux),
        "mises_a_jour": len(ids_mis_a_jour),
        "alertes_urgentes": len(alerts),
        "alertes": alerts,
        "statistiques": stats,
        "resume_opportunites": [
            {
                "id": o["id"],
                "nom": o["nom"],
                "organisme": o["organisme"],
                "montant_max": o["montant_max"],
                "deadline": o["deadline"],
                "statut": o["statut"],
                "score_pertinence": o.get("score_pertinence", 0),
                "score_eligibilite": o.get("score_eligibilite", 0),
            }
            for o in sorted(merged, key=lambda x: -x.get("score_pertinence", 0))
        ],
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output


if __name__ == "__main__":
    main()
