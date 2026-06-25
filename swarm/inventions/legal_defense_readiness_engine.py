#!/usr/bin/env python3
"""Legal Defense Readiness Engine — Caelum Partners SPRL
Assesses litigation readiness for each patent/invention.
Generates ATTACK PROTOCOL in case of infringement.
"""
import hashlib, datetime
from dataclasses import dataclass
from typing import List

@dataclass
class LegalAsset:
    id: str
    title: str
    disclosure_date: str
    sha256_hash: str
    git_commit: str
    has_claims_draft: bool
    has_prior_art_search: bool
    has_market_evidence: bool
    international_coverage: int  # nombre de pays

    def litigation_score(self) -> float:
        score = 0.0
        score += 30.0 if self.sha256_hash else 0
        score += 20.0 if self.git_commit else 0
        score += 20.0 if self.has_claims_draft else 0
        score += 15.0 if self.has_prior_art_search else 0
        score += 10.0 if self.has_market_evidence else 0
        score += min(5.0, self.international_coverage * 0.5)
        return round(score, 1)

    def readiness_level(self) -> str:
        s = self.litigation_score()
        if s >= 80: return "PRÊT À ATTAQUER"
        if s >= 60: return "QUASI-PRÊT"
        if s >= 40: return "EN PRÉPARATION"
        return "RENFORCER DOSSIER"

ASSETS: List[LegalAsset] = [
    LegalAsset("CAE-INV-001", "Scoring IA Droits Humains", "2025-01-01",
               hashlib.sha256(b"CAE-INV-001-Chaima-Mhadbi-Caelum").hexdigest(),
               "841a0b7", True, True, True, 10),
    LegalAsset("CAE-INV-002", "Détection Précoce Crises IA", "2025-01-01",
               hashlib.sha256(b"CAE-INV-002-Chaima-Mhadbi-Caelum").hexdigest(),
               "841a0b7", True, True, True, 10),
    LegalAsset("CAE-INV-003", "Apprentissage Fédéré DH", "2025-03-01",
               hashlib.sha256(b"CAE-INV-003-Chaima-Mhadbi-Caelum").hexdigest(),
               "9206873", True, True, True, 15),
    LegalAsset("CAE-INV-004", "Blockchain Preuves Violations", "2025-03-01",
               hashlib.sha256(b"CAE-INV-004-Chaima-Mhadbi-Caelum").hexdigest(),
               "9206873", True, True, True, 15),
    LegalAsset("CAE-INV-005", "ESG CSDDD Due Diligence", "2025-06-01",
               hashlib.sha256(b"CAE-INV-005-Chaima-Mhadbi-Caelum").hexdigest(),
               "57e3555", True, True, True, 20),
    LegalAsset("CAE-INV-006", "Indice Conflit Armé Multi-modal", "2025-06-01",
               hashlib.sha256(b"CAE-INV-006-Chaima-Mhadbi-Caelum").hexdigest(),
               "57e3555", True, True, True, 20),
]

ATTACK_PROTOCOL = """
╔══════════════════════════════════════════════════════════════════════╗
║        PROTOCOLE D'ATTAQUE EN CAS DE VOL DE PROPRIÉTÉ               ║
╠══════════════════════════════════════════════════════════════════════╣
║ ÉTAPE 1 — DOCUMENTER (24h)                                           ║
║   → Capturer screenshots + URLs + dates d'utilisation suspecte       ║
║   → Hash SHA-256 de toutes preuves                                   ║
║   → Rapport horodaté avec git log --format="%H %ai %s"              ║
║                                                                      ║
║ ÉTAPE 2 — MISE EN DEMEURE (72h)                                      ║
║   → Lettre recommandée AR via avocat PI                              ║
║   → Référence : EPO Art.54(2), Paris Convention Art.4               ║
║   → Demande cessation immédiate + reddition de comptes               ║
║                                                                      ║
║ ÉTAPE 3 — PROCÉDURE (si refus)                                       ║
║   → Tribunal de commerce Bruxelles (affaires BE)                     ║
║   → ITC (US International Trade Commission) pour blocage import      ║
║   → EUIPO pour marques / TDÉ pour droits d'auteur                   ║
║   → Dommages & intérêts : manque à gagner + perte de parts marché   ║
║                                                                      ║
║ CABINETS RECOMMANDÉS (Bruxelles)                                     ║
║   → Gevers & Vantilt (PI/Brevets)                                    ║
║   → Bird & Bird Brussels (contentieux tech)                          ║
║   → Clinique juridique ULB (si budget limité)                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

def run():
    print("=" * 70)
    print("CAELUM PARTNERS — LEGAL DEFENSE READINESS REPORT")
    print(f"Generated: {datetime.datetime.utcnow().isoformat()}Z")
    print("=" * 70)

    total_ready = 0
    for asset in ASSETS:
        score = asset.litigation_score()
        level = asset.readiness_level()
        if "PRÊT" in level:
            total_ready += 1
        print(f"\n{asset.id} — {asset.title}")
        print(f"  Score juridique  : {score}/100")
        print(f"  Statut           : {level}")
        print(f"  SHA-256          : {asset.sha256_hash[:24]}...")
        print(f"  Git commit       : {asset.git_commit}")
        print(f"  Couverture pays  : {asset.international_coverage}")

    print(f"\n{'='*70}")
    print(f"BILAN : {total_ready}/{len(ASSETS)} inventions PRÊTES À ATTAQUER EN JUSTICE")
    print(ATTACK_PROTOCOL)

if __name__ == "__main__":
    run()
