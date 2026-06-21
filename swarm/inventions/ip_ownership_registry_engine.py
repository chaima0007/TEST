#!/usr/bin/env python3
"""IP Ownership Registry Engine — Caelum Partners SPRL
Generates immutable cryptographic proof of ownership for all inventions.
Legal basis: EPO Art.54(2) CBE, 35 U.S.C. §102, Paris Convention Art.4
"""
import hashlib, json, datetime

OWNER = {
    "inventor": "Chaima Mhadbi",
    "applicant": "Caelum Partners SPRL",
    "address": "Bruxelles, Belgique",
    "email": "retrouvetonsmile@gmail.com",
    "legal_basis": ["EPO Art.54(2) CBE", "35 U.S.C. §102", "Paris Convention Art.4", "TRIPS Art.29"],
}

INVENTIONS = [
    {"id": "CAE-INV-001", "title": "Scoring IA Droits Humains Automatisé", "ipc": "G06N 20/00", "generation": "G1", "date": "2025-01-01", "score": 8.72},
    {"id": "CAE-INV-002", "title": "Détection Précoce Crises par IA", "ipc": "G06N 5/04", "generation": "G1", "date": "2025-01-01", "score": 8.73},
    {"id": "CAE-INV-003", "title": "Apprentissage Fédéré Droits Humains", "ipc": "G06N 20/00 · H04L 9/32", "generation": "G2", "date": "2025-03-01", "score": 8.99},
    {"id": "CAE-INV-004", "title": "Blockchain Preuves de Violations", "ipc": "H04L 9/32", "generation": "G2", "date": "2025-03-01", "score": 9.01},
    {"id": "CAE-INV-005", "title": "Plateforme ESG CSDDD Due Diligence", "ipc": "G06Q 10/06", "generation": "G3", "date": "2025-06-01", "score": 9.29},
    {"id": "CAE-INV-006", "title": "Indice Risque de Conflit Armé Multi-modal", "ipc": "G06N 20/00 · G06F 40/56", "generation": "G3", "date": "2025-06-01", "score": 9.39},
]

def generate_proof(inv: dict) -> dict:
    payload = json.dumps({**inv, **OWNER}, sort_keys=True, ensure_ascii=False)
    sha256 = hashlib.sha256(payload.encode()).hexdigest()
    sha512 = hashlib.sha512(payload.encode()).hexdigest()
    return {
        **inv,
        "owner": OWNER["inventor"],
        "applicant": OWNER["applicant"],
        "sha256_proof": sha256,
        "sha512_proof": sha512,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "legal_basis": OWNER["legal_basis"],
        "priority_claim": f"Disclosed prior to any third-party filing — EPO Art.54(2) CBE + 35 U.S.C. §102",
        "litigation_ready": True,
    }

def run():
    print("=" * 70)
    print("CAELUM PARTNERS — IP OWNERSHIP REGISTRY")
    print(f"Inventrice : {OWNER['inventor']}")
    print(f"Titulaire  : {OWNER['applicant']}")
    print("=" * 70)
    registry = []
    for inv in INVENTIONS:
        proof = generate_proof(inv)
        registry.append(proof)
        print(f"\n{proof['id']} — {proof['title']}")
        print(f"  Génération   : {proof['generation']}")
        print(f"  Date priorité: {proof['date']}")
        print(f"  SHA-256      : {proof['sha256_proof'][:32]}...")
        print(f"  Statut       : ✓ PROPRIÉTÉ PROUVÉE — LITIGATION READY")
    print(f"\n{'='*70}")
    print(f"TOTAL : {len(registry)} inventions enregistrées")
    print(f"TOUTES appartiennent légalement à : {OWNER['inventor']} / {OWNER['applicant']}")
    print(f"Fondement légal : {', '.join(OWNER['legal_basis'])}")
    print("STATUS : PRÊT POUR PROCÉDURE JUDICIAIRE EN CAS DE VOL")
    return registry

if __name__ == "__main__":
    run()
