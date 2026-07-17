#!/usr/bin/env python3
"""
prospect_scanner.py — Scanner de Prospects CaelumSwarm™ / Caelum
═════════════════════════════════════════════════════════════════
Prospection intelligente et HONNÊTE : à partir d'observations PUBLIQUES sur
un prospect (son site, sa présence en ligne), repère les lacunes digitales
où NOS services peuvent réellement l'aider, et génère un message de
prospection personnalisé.

⚠️ Éthique (intégrée) :
- Analyse uniquement de l'information PUBLIQUE (site web visible de tous).
- AUCUN scan de sécurité, AUCun piratage, AUCune intrusion.
- On ne propose une solution QUE si la lacune est réelle ET qu'on sait la
  traiter. Jamais de problème inventé.

Usage :
  python3 scripts/prospect_scanner.py --demo
  python3 scripts/prospect_scanner.py --name "Resto Le Soleil" \
      --no-site --manual-tasks --no-dashboard
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

LOG = Path("data/prospect_scans.json")

# Lacune observable (publique) → service Caelum qui la traite
GAPS = {
    "no_site": {
        "label": "Pas de site web (ou site absent/introuvable)",
        "service": "Site web",
        "pitch": "Vous n'avez pas encore de site : vos clients vous cherchent sur Google et ne vous trouvent pas. Un site moderne dès 500 € change la donne.",
    },
    "old_site": {
        "label": "Site daté / pas adapté au mobile / lent",
        "service": "Site web (refonte)",
        "pitch": "Votre site actuel mérite un coup de neuf : sur mobile et en rapidité, il fait perdre des clients. Une refonte rapide le remet au niveau.",
    },
    "no_dashboard": {
        "label": "Aucun suivi de données / pilotage à l'aveugle",
        "service": "Tableau de bord",
        "pitch": "Vous pilotez sans tableau de bord clair : ventes, clients, performance restent flous. On centralise vos chiffres clés en temps réel, dès 800 €.",
    },
    "manual_tasks": {
        "label": "Tâches répétitives faites à la main",
        "service": "Automatisation",
        "pitch": "Beaucoup de tâches manuelles = du temps et des erreurs. On les automatise (dès 300 €) pour vous rendre des heures chaque semaine.",
    },
    "no_business_plan": {
        "label": "Projet de croissance / levée sans business plan structuré",
        "service": "Business plan",
        "pitch": "Pour convaincre une banque ou des associés, un business plan clair fait la différence. On le structure pour vous, dès 400 €.",
    },
}


def scan(name: str, gaps: list) -> dict:
    matched = [GAPS[g] for g in gaps if g in GAPS]
    has_solution = len(matched) > 0
    return {
        "prospect": name,
        "gaps_found": [m["label"] for m in matched],
        "services_proposes": sorted({m["service"] for m in matched}),
        "has_solution": has_solution,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def build_message(name: str, gaps: list) -> str:
    matched = [GAPS[g] for g in gaps if g in GAPS]
    if not matched:
        return (f"Bonjour {name},\n\nAprès un rapide coup d'œil, votre présence en ligne semble "
                "déjà solide — bravo ! Si un jour vous avez un projet web, data ou d'automatisation, "
                "on sera ravis d'en discuter.\n\nBien à vous, Caelum")
    lines = [f"Bonjour {name},", "",
             "J'ai regardé votre présence en ligne (publique) et j'ai repéré "
             f"{'un point' if len(matched)==1 else 'quelques points'} où je pense pouvoir vous aider :"]
    for m in matched:
        lines.append(f"  • {m['pitch']}")
    lines += ["",
              "Si ça vous parle, je vous offre un audit express gratuit (24h, sans engagement). "
              "On en parle 10 minutes ?", "",
              "Bien à vous,", "Caelum — studio web & data, Bruxelles"]
    return "\n".join(lines)


def _log(rec):
    log = []
    if LOG.exists():
        try: log = json.loads(LOG.read_text())
        except Exception: log = []
    log.append(rec)
    if len(log) > 500: log = log[-500:]
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


def run(name, gaps):
    res = scan(name, gaps)
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       SCANNER DE PROSPECTS — Caelum                         ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    print(f"  Prospect : {name}")
    if res["gaps_found"]:
        print("  Lacunes repérées (publiques) :")
        for g in res["gaps_found"]:
            print(f"    • {g}")
        print(f"\n  ✅ On peut aider → {', '.join(res['services_proposes'])}")
    else:
        print("  Aucune lacune évidente — prospect déjà bien équipé.")
    print("\n  ── Message de prospection prêt à envoyer ──\n")
    print(build_message(name, gaps))
    print()
    _log(res)


def _demo():
    run("Resto Le Soleil", ["no_site", "manual_tasks"])
    run("Garage Martin", ["old_site", "no_dashboard"])


def main():
    ap = argparse.ArgumentParser(description="Scanner de prospects Caelum")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--name", type=str, default="Prospect")
    ap.add_argument("--no-site", action="store_true", help="Pas de site web")
    ap.add_argument("--old-site", action="store_true", help="Site daté/lent/non mobile")
    ap.add_argument("--no-dashboard", action="store_true", help="Aucun suivi de données")
    ap.add_argument("--manual-tasks", action="store_true", help="Tâches manuelles répétitives")
    ap.add_argument("--no-business-plan", action="store_true", help="Pas de business plan")
    args = ap.parse_args()

    if args.demo:
        _demo()
        return
    gaps = []
    if args.no_site: gaps.append("no_site")
    if args.old_site: gaps.append("old_site")
    if args.no_dashboard: gaps.append("no_dashboard")
    if args.manual_tasks: gaps.append("manual_tasks")
    if args.no_business_plan: gaps.append("no_business_plan")
    run(args.name, gaps)


if __name__ == "__main__":
    main()
