#!/usr/bin/env python3
"""
update_all_reports.py — ORCHESTRATEUR : un seul geste met TOUT à jour.

À lancer après chaque ajout de savoir. Enchaîne, dans l'ordre :
  1. certification_protocol      (vérifie que tout fonctionne + sceau + probabilité)
  2. learning_ledger_protocol    (registre d'apprentissage contrôlé + digest)
  3. progress_report_protocol    (compte-rendu d'avancement, agréable à lire)
  4. backup_protocol             (sauvegarde horodatée + manifeste)

Puis affiche les 2 fichiers à envoyer dans le Drive :
  - data/learning_digest.md      (« tout ce que je dois savoir »)
  - data/progress_report.md      (« nos réussites »)

NB honnête : l'envoi vers Google Drive se fait par l'assistant via la connexion sécurisée
Google (un script ne doit JAMAIS détenir tes identifiants — règle zéro credential). Cet
orchestrateur prépare tout ; l'assistant pousse ensuite les 2 fichiers dans le Drive.

Usage : python3 scripts/update_all_reports.py
"""
import subprocess
import sys

ETAPES = [
    ("Certification", "scripts/certification_protocol.py", ["--quiet"]),
    ("Registre d'apprentissage", "scripts/learning_ledger_protocol.py", []),
    ("Compte-rendu d'avancement", "scripts/progress_report_protocol.py", []),
    ("Traceur de rêves", "scripts/dream_tracker_protocol.py", []),
    ("Indice d'expertise", "scripts/expertise_index_protocol.py", []),
    ("Carnet de bord (travail)", "scripts/work_journal_protocol.py", []),
    ("Méta-audit expertise", "scripts/expertise_audit_protocol.py", []),
    ("Radar de fraicheur", "scripts/freshness_radar_protocol.py", []),
    ("Valorisation projets", "scripts/project_valuation_protocol.py", []),
    ("Transparence & decharge", "scripts/transparency_disclaimer_protocol.py", []),
    ("Détection du marché", "scripts/market_detection_protocol.py", []),
    ("Comité de direction", "scripts/direction_committee_protocol.py", []),
    ("Agent de résilience", "scripts/resilience_simulator.py", []),
    ("Audit accessibilité", "scripts/accessibility_audit_agent.py", []),
    ("Base unique (catalogue)", "scripts/build_kb_index.py", []),
    ("Spécialistes par domaine", "scripts/build_specialistes.py", []),
    ("Expertise rentabilité", "scripts/rentabilite_protocol.py", []),
    ("Analyse du travail", "scripts/travail_analyse_protocol.py", []),
    ("Suivi des revenus", "scripts/revenus_suivi_protocol.py", []),
    ("Contrôle de tous les agents", "scripts/agents_healthcheck.py", []),
    ("Agent prédictif", "scripts/agent_predictif.py", []),
    ("Audit références légales", "scripts/loi_reference_audit.py", []),
    ("Protocole incrémental", "scripts/incremental_protocol.py", []),
    ("Scalabilité & monitoring", "scripts/scalability_monitor.py", []),
    ("Point de reprise", "scripts/checkpoint_protocol.py", []),
    ("Audit fiabilité grand site", "scripts/site_reliability_audit.py", []),
    ("Veille juridique", "scripts/veille_juridique_protocol.py", []),

    ("Sauvegarde", "scripts/backup_protocol.py", []),
]


def main():
    print("═══ MISE À JOUR GLOBALE DES COMPTES-RENDUS ═══")
    echecs = 0
    for nom, script, extra in ETAPES:
        r = subprocess.run([sys.executable, script, *extra], capture_output=True, text=True)
        etat = "✓" if r.returncode == 0 else "✗"
        if r.returncode != 0:
            echecs += 1
        # dernière ligne utile de chaque protocole
        derniere = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"  {etat} {nom:30s} {derniere}")

    print("\n📂 À envoyer dans le Drive (l'assistant s'en charge via la connexion Google sécurisée) :")
    print("   - data/learning_digest.md   (tout ce que je dois savoir)")
    print("   - data/progress_report.md   (nos réussites)")
    if echecs:
        print(f"\n⚠️  {echecs} étape(s) en erreur — à vérifier avant publication.")
        return 1
    print("\n✓ Tout est à jour et cohérent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
