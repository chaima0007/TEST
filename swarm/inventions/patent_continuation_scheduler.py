#!/usr/bin/env python3
"""Patent Continuation Scheduler — Caelum Partners SPRL
Automatically schedules new patent generations every 6 months.
Strategy: 10-year patent forest that continuously renews itself.
"""
import datetime, hashlib

OWNER = {
    "inventor": "Chaima Mhadbi",
    "applicant": "Caelum Partners SPRL",
    "strategy": "Continuation + CIP (Continuation-in-Part) every 6 months",
    "target": "10 years of patent coverage ahead of competitors",
    "legal_basis": "Paris Convention Art.4 + 35 U.S.C. §120 (Continuation) + EPC Rule 36",
}

# Genealogy: each child invention extends the parent with new claims
PATENT_TREE = {
    "G1": {
        "filed_date": "2025-01-01",
        "inventions": [
            {"id": "CAE-INV-001", "title": "Scoring IA Droits Humains Automatisé", "ipc": "G06N 20/00"},
            {"id": "CAE-INV-002", "title": "Détection Précoce Crises par IA", "ipc": "G06N 5/04"},
        ],
        "spawns": ["G2"],
    },
    "G2": {
        "filed_date": "2025-07-01",  # 6 months after G1
        "inventions": [
            {"id": "CAE-INV-003", "title": "Apprentissage Fédéré Droits Humains", "ipc": "G06N 20/00"},
            {"id": "CAE-INV-004", "title": "Blockchain Preuves de Violations", "ipc": "H04L 9/32"},
        ],
        "parent": "G1",
        "continuation_type": "CIP",
        "spawns": ["G3"],
    },
    "G3": {
        "filed_date": "2026-01-01",  # 6 months after G2
        "inventions": [
            {"id": "CAE-INV-005", "title": "Plateforme ESG CSDDD Due Diligence", "ipc": "G06Q 10/06"},
            {"id": "CAE-INV-006", "title": "Indice Risque Conflit Multi-modal", "ipc": "G06N 20/00"},
        ],
        "parent": "G2",
        "continuation_type": "CIP",
        "spawns": ["G4"],
    },
    "G4": {
        "filed_date": "2026-07-01",  # PROCHAINE GÉNÉRATION — à déposer dans 6 mois
        "inventions": [
            {"id": "CAE-INV-007", "title": "Réseau Neuronal Graphe Violations DH", "ipc": "G06N 3/04"},
            {"id": "CAE-INV-008", "title": "Moteur Prédictif Génocide Préventif", "ipc": "G06N 5/04"},
            {"id": "CAE-INV-009", "title": "Système Alertes Précoces Multi-source", "ipc": "G06F 40/56"},
        ],
        "parent": "G3",
        "continuation_type": "CIP",
        "spawns": ["G5"],
        "status": "À DÉPOSER — Juillet 2026",
        "priority": "URGENT",
    },
    "G5": {
        "filed_date": "2027-01-01",
        "inventions": [
            {"id": "CAE-INV-011", "title": "IA Générative Rapports DH Automatisés", "ipc": "G06N 3/04"},
            {"id": "CAE-INV-012", "title": "Système Multi-agent Surveillance ODD", "ipc": "G06N 5/04"},
            {"id": "CAE-INV-013", "title": "Détection Deepfake Preuves Violations", "ipc": "G06V 10/80"},
        ],
        "parent": "G4",
        "continuation_type": "CIP",
        "spawns": ["G6"],
        "status": "PLANIFIÉ — Jan 2027",
    },
    "G6": {
        "filed_date": "2027-07-01",
        "inventions": [
            {"id": "CAE-INV-014", "title": "Protocole Zéro-Connaissance Données DH", "ipc": "H04L 9/32"},
            {"id": "CAE-INV-015", "title": "Algorithme Compensation Biais Culturel", "ipc": "G06N 20/00"},
            {"id": "CAE-INV-016", "title": "Interface Blockchain-IA Vérification DH", "ipc": "H04L 9/32"},
        ],
        "parent": "G5",
        "continuation_type": "CIP",
        "spawns": ["G7"],
        "status": "PLANIFIÉ — Juil 2027",
    },
    "G7": {
        "filed_date": "2028-01-01",
        "inventions": [
            {"id": "CAE-INV-017", "title": "Quantum-Safe Evidence Chain DH", "ipc": "H04L 9/32"},
            {"id": "CAE-INV-018", "title": "IA Multilingue Analyse Violations 200 pays", "ipc": "G06F 40/56"},
            {"id": "CAE-INV-019", "title": "Scoring ESG Temps Réel Satellite-IA", "ipc": "G06Q 10/06"},
        ],
        "parent": "G6",
        "continuation_type": "CIP",
        "status": "PLANIFIÉ — Jan 2028",
    },
    "G8": {
        "filed_date": "2028-07-01",
        "inventions": [
            {"id": "CAE-INV-020", "title": "IA Prédictive Crises Humanitaires 5 ans", "ipc": "G06N 5/04"},
            {"id": "CAE-INV-021", "title": "Système Traçabilité Chaîne Valeur DH", "ipc": "G06Q 10/06"},
            {"id": "CAE-INV-022", "title": "Protocole Interopérabilité ONU-IA DH", "ipc": "G06F 15/16"},
        ],
        "parent": "G7",
        "continuation_type": "CIP",
        "status": "PLANIFIÉ — Juil 2028",
    },
    "G9": {
        "filed_date": "2029-01-01",
        "inventions": [
            {"id": "CAE-INV-023", "title": "IA Conscience Contextuelle Droit International", "ipc": "G06N 3/04"},
            {"id": "CAE-INV-024", "title": "Méta-Modèle Alignement IA-Droits Humains", "ipc": "G06N 20/00"},
        ],
        "parent": "G8",
        "continuation_type": "CIP",
        "status": "PLANIFIÉ — Jan 2029",
    },
    "G10": {
        "filed_date": "2029-07-01",
        "inventions": [
            {"id": "CAE-INV-025", "title": "Système Autonome Monitoring DH Global", "ipc": "G06N 5/04"},
            {"id": "CAE-INV-026", "title": "IA Souveraineté Données DH Fédérées", "ipc": "G06N 20/00"},
        ],
        "parent": "G9",
        "continuation_type": "Continuation",
        "status": "PLANIFIÉ — Juil 2029",
    },
}

LICENSING_MODEL = {
    "tiers": [
        {"segment": "Startup / ONG", "fee_eur_year": "10,000 - 30,000", "terms": "non-exclusif"},
        {"segment": "PME ESG / Conseil", "fee_eur_year": "50,000 - 150,000", "terms": "non-exclusif"},
        {"segment": "Grande entreprise", "fee_eur_year": "200,000 - 500,000", "terms": "non-exclusif"},
        {"segment": "Banque / Assurance", "fee_eur_year": "300,000 - 800,000", "terms": "non-exclusif"},
        {"segment": "Gouvernement / OI", "fee_eur_year": "500,000 - 2,000,000", "terms": "contrat-cadre"},
        {"segment": "Exclusivité sectorielle", "fee_eur_year": "1,000,000 - 5,000,000", "terms": "exclusif / secteur"},
    ],
    "enforcement": "Tribunal de commerce Bruxelles + ITC (USA) + EUIPO",
    "note": "Toute utilisation sans licence = violation de brevets = procédure automatique",
}

def run():
    today = datetime.datetime.utcnow().date()
    print("=" * 70)
    print("CAELUM PARTNERS — PATENT CONTINUATION SCHEDULER")
    print(f"Inventrice : {OWNER['inventor']} | Titulaire : {OWNER['applicant']}")
    print(f"Stratégie  : {OWNER['strategy']}")
    print(f"Objectif   : {OWNER['target']}")
    print("=" * 70)

    total_inventions = 0
    for gen, data in PATENT_TREE.items():
        filed = datetime.datetime.strptime(data["filed_date"], "%Y-%m-%d").date()
        days_delta = (filed - today).days
        inv_count = len(data["inventions"])
        total_inventions += inv_count

        status = data.get("status", "DÉPOSÉ")
        priority = " ⚡ PRIORITÉ MAXIMALE" if data.get("priority") == "URGENT" else ""

        if days_delta < 0:
            timing = f"il y a {abs(days_delta)} jours"
        elif days_delta == 0:
            timing = "AUJOURD'HUI"
        else:
            months = days_delta // 30
            timing = f"dans {months} mois ({data['filed_date']})"

        print(f"\n{gen} [{status}]{priority}")
        print(f"  Date : {timing}")
        print(f"  Type : {data.get('continuation_type', 'Original')}")
        for inv in data["inventions"]:
            print(f"  → {inv['id']} — {inv['title']} [{inv['ipc']}]")

        # Protection until 20 years from filing
        expiry = datetime.datetime.strptime(data["filed_date"], "%Y-%m-%d").date()
        expiry = expiry.replace(year=expiry.year + 20)
        print(f"  Protection jusqu'à : {expiry}")

    print(f"\n{'='*70}")
    print(f"TOTAL : {total_inventions} inventions planifiées G1→G10")
    print(f"Couverture protection : jusqu'en 2049 minimum")

    print(f"\n[MODÈLE LICENSING]")
    for tier in LICENSING_MODEL["tiers"]:
        print(f"  {tier['segment']:<30} : €{tier['fee_eur_year']}/an ({tier['terms']})")

    print(f"\n[ENFORCEMENT] {LICENSING_MODEL['enforcement']}")
    print(f"[RÈGLE] {LICENSING_MODEL['note']}")

    print(f"\n[PROCHAINE ACTION]")
    print(f"  → DÉPOSER G4 (CAE-INV-007..009) avant Juillet 2026")
    print(f"  → Budget estimé : €2,000-€3,000 (BOIP BeNeLux)")
    print(f"  → Alternatives gratuites : PCT via PPH (Patent Prosecution Highway)")
    print(f"  → Clinique ULB pour accompagnement gratuit")

if __name__ == "__main__":
    run()
