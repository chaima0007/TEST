#!/usr/bin/env python3
"""Libre & Accomplis — Gestion des feedbacks des experts (CSV, importable dans Airtable).

Colonnes : Agent, Action, Statut (✅/❌/⏳), Feedback, Expert, Date, Priorité.

Usage :
    # Ajouter un feedback
    python3 gerer_feedback_experts.py ajouter \
        --agent "Agent Nutrition" --action "Proposer recette aux noix" \
        --statut "❌" --feedback "Allergie non détectée" \
        --expert "Dr. Martin" --priorite haute

    # Lister les feedbacks en attente (statut ❌ ou ⏳) d'un expert
    python3 gerer_feedback_experts.py lister --expert "Dr. Martin"

    # Rappels : nombre de feedbacks en attente par expert
    python3 gerer_feedback_experts.py rappels
"""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

FICHIER_PAR_DEFAUT = Path(__file__).resolve().parent.parent / "modeles" / "feedback_experts.csv"
COLONNES = ["Agent", "Action", "Statut", "Feedback", "Expert", "Date", "Priorité"]
STATUTS_EN_ATTENTE = {"❌", "⏳"}


def charger(fichier: Path) -> list:
    if not fichier.exists():
        return []
    with fichier.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ajouter(fichier: Path, args) -> None:
    nouveau = fichier.exists() is False or fichier.stat().st_size == 0
    with fichier.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES)
        if nouveau:
            writer.writeheader()
        writer.writerow({
            "Agent": args.agent,
            "Action": args.action,
            "Statut": args.statut,
            "Feedback": args.feedback,
            "Expert": args.expert,
            "Date": args.date or date.today().isoformat(),
            "Priorité": args.priorite,
        })
    print(f"✅ Feedback ajouté pour {args.agent} (expert : {args.expert}).")


def lister(fichier: Path, args) -> None:
    en_attente = [
        ligne for ligne in charger(fichier)
        if ligne["Expert"] == args.expert and ligne["Statut"] in STATUTS_EN_ATTENTE
    ]
    if not en_attente:
        print(f"✅ Aucun feedback en attente pour {args.expert}.")
        return
    print(f"📋 {len(en_attente)} feedback(s) en attente pour {args.expert} :")
    for ligne in en_attente:
        print(f"  - [{ligne['Priorité']}] {ligne['Agent']} — {ligne['Action']} : {ligne['Feedback']}")


def rappels(fichier: Path, _args) -> None:
    compteurs = {}
    for ligne in charger(fichier):
        if ligne["Statut"] in STATUTS_EN_ATTENTE:
            compteurs[ligne["Expert"]] = compteurs.get(ligne["Expert"], 0) + 1
    if not compteurs:
        print("✅ Aucun feedback en attente, tous les experts sont à jour.")
        return
    for expert, nombre in sorted(compteurs.items(), key=lambda kv: -kv[1]):
        print(f"🔔 {expert} : {nombre} feedback(s) en attente.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fichier", type=Path, default=FICHIER_PAR_DEFAUT,
                        help="Chemin du CSV (défaut : modeles/feedback_experts.csv)")
    sous = parser.add_subparsers(dest="commande", required=True)

    p_ajouter = sous.add_parser("ajouter", help="Ajouter un feedback")
    p_ajouter.add_argument("--agent", required=True)
    p_ajouter.add_argument("--action", required=True)
    p_ajouter.add_argument("--statut", default="⏳", choices=["✅", "❌", "⏳"])
    p_ajouter.add_argument("--feedback", required=True)
    p_ajouter.add_argument("--expert", required=True)
    p_ajouter.add_argument("--date", default="", help="AAAA-MM-JJ (défaut : aujourd'hui)")
    p_ajouter.add_argument("--priorite", default="moyenne", choices=["haute", "moyenne", "basse"])
    p_ajouter.set_defaults(fonction=ajouter)

    p_lister = sous.add_parser("lister", help="Lister les feedbacks en attente d'un expert")
    p_lister.add_argument("--expert", required=True)
    p_lister.set_defaults(fonction=lister)

    p_rappels = sous.add_parser("rappels", help="Feedbacks en attente par expert")
    p_rappels.set_defaults(fonction=rappels)

    args = parser.parse_args()
    args.fonction(args.fichier, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
