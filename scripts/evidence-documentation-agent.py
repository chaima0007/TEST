#!/usr/bin/env python3
"""
Evidence Documentation Agent — Caelum Partners CaelumSwarm™
Expert documentation et archivage de preuves droits humains.
Structure les preuves selon standards légaux EU CSDDD / UNGP / ISO 30301.
"""

import hashlib
import sys
from datetime import datetime, timezone

EVIDENCE_TYPES = {
    "DOCUMENTARY": {
        "label": "Document officiel",
        "examples": ["Rapport ONG", "Document état", "Décision judiciaire", "Statistique officielle"],
        "reliability": 0.90,
        "legal_weight": "ÉLEVÉ",
    },
    "TESTIMONIAL": {
        "label": "Témoignage",
        "examples": ["Interview victime", "Déposition expert", "Rapport terrain"],
        "reliability": 0.70,
        "legal_weight": "MODÉRÉ",
    },
    "STATISTICAL": {
        "label": "Donnée statistique",
        "examples": ["Rapport UNHCR", "Données Banque Mondiale", "Enquête nationale"],
        "reliability": 0.85,
        "legal_weight": "ÉLEVÉ",
    },
    "MEDIA": {
        "label": "Média vérifié",
        "examples": ["Article presse internationale", "Reportage audiovisuel", "Photo géolocalisée"],
        "reliability": 0.65,
        "legal_weight": "MODÉRÉ",
    },
    "LEGAL": {
        "label": "Document juridique",
        "examples": ["Jugement tribunal", "Traité international", "Directive EU"],
        "reliability": 0.98,
        "legal_weight": "TRÈS ÉLEVÉ",
    },
    "SATELLITE": {
        "label": "Preuve satellitaire",
        "examples": ["Image satellite UNOSAT", "Analyse géospatiale", "Données environnementales"],
        "reliability": 0.92,
        "legal_weight": "ÉLEVÉ",
    },
}

ISO_30301_METADATA = [
    "record_id", "title", "creator", "date_created", "date_modified",
    "format", "language", "rights", "relation", "coverage",
    "authenticity_hash", "chain_of_custody",
]

CHAIN_OF_CUSTODY_STEPS = [
    "COLLECTED", "VERIFIED", "DIGITIZED", "HASHED", "STORED", "REVIEWED", "APPROVED"
]

LEGAL_STANDARDS = {
    "ICC_ROME_STATUTE": "Standard pénal international — preuve au-delà du doute raisonnable",
    "ICJ_RULES": "Cour internationale de justice — Article 43-44 du Statut",
    "CSDDD_ART8": "CSDDD Art.8 — Documentation impacts négatifs identifiés",
    "UNGP_COMMENTARY": "UNGP Commentary 15-24 — Documentation diligence raisonnable",
    "CSRD_ESRS": "CSRD ESRS S4 — Traçabilité données chaîne de valeur",
}


def generate_evidence_hash(evidence: dict) -> str:
    """Génère un hash cryptographique de la preuve pour intégrité."""
    content = f"{evidence.get('title', '')}{evidence.get('source', '')}{evidence.get('date', '')}{evidence.get('content_summary', '')}"
    return hashlib.sha256(content.encode()).hexdigest()[:16].upper()


def create_evidence_record(
    entity_id: str,
    entity_name: str,
    evidence_type: str,
    title: str,
    source: str,
    date: str,
    content_summary: str,
    reliability_override: float = None,
    legal_standards: list = None,
) -> dict:
    """Crée un enregistrement de preuve structuré selon ISO 30301."""
    ev_config = EVIDENCE_TYPES.get(evidence_type, EVIDENCE_TYPES["DOCUMENTARY"])
    reliability = reliability_override if reliability_override else ev_config["reliability"]

    evidence_draft = {
        "title": title, "source": source, "date": date, "content_summary": content_summary
    }
    auth_hash = generate_evidence_hash(evidence_draft)

    record_id = f"EV-{entity_id}-{evidence_type[:3]}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "record_id": record_id,
        "entity_id": entity_id,
        "entity_name": entity_name,
        "evidence_type": evidence_type,
        "evidence_type_label": ev_config["label"],
        "iso_30301_metadata": {
            "title": title,
            "creator": "CaelumSwarm™ Evidence Documentation Agent",
            "date_created": datetime.now(timezone.utc).isoformat(),
            "date_evidence": date,
            "source": source,
            "format": "JSON/Structured",
            "language": "FR",
            "authenticity_hash": f"SHA256:{auth_hash}",
            "chain_of_custody": CHAIN_OF_CUSTODY_STEPS[:4],
        },
        "content_summary": content_summary,
        "reliability_score": reliability,
        "legal_weight": ev_config["legal_weight"],
        "legal_standards_applicable": legal_standards or ["CSDDD_ART8", "UNGP_COMMENTARY"],
        "admissibility": {
            "csddd_art8": reliability >= 0.60,
            "csrd_disclosure": reliability >= 0.70,
            "icc_standard": reliability >= 0.90,
            "civil_litigation": reliability >= 0.65,
        },
        "verification_status": "PENDING_REVIEW",
        "cross_references": [],
        "retention_years": 10,
    }


def build_evidence_dossier(entity_id: str, entity_name: str, domain: str, evidences: list) -> dict:
    """Construit un dossier de preuves complet pour une entité."""
    if not evidences:
        return {}

    avg_reliability = sum(e["reliability_score"] for e in evidences) / len(evidences)
    legal_weight_rank = {"TRÈS ÉLEVÉ": 4, "ÉLEVÉ": 3, "MODÉRÉ": 2, "FAIBLE": 1}
    max_legal_weight = max(evidences, key=lambda e: legal_weight_rank.get(e["legal_weight"], 0))

    csddd_ready = all(e["admissibility"]["csddd_art8"] for e in evidences)
    csrd_ready = avg_reliability >= 0.70
    icc_ready = avg_reliability >= 0.85 and len(evidences) >= 3

    dossier_hash_content = "".join(e["iso_30301_metadata"]["authenticity_hash"] for e in evidences)
    dossier_hash = hashlib.sha256(dossier_hash_content.encode()).hexdigest()[:20].upper()

    return {
        "dossier_id": f"DOS-{entity_id}-{datetime.now().strftime('%Y%m%d')}",
        "entity_id": entity_id,
        "entity_name": entity_name,
        "domain": domain,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dossier_integrity_hash": f"SHA256:{dossier_hash}",
        "summary": {
            "total_evidences": len(evidences),
            "avg_reliability": round(avg_reliability, 3),
            "strongest_legal_weight": max_legal_weight["legal_weight"],
            "evidence_types": list({e["evidence_type"] for e in evidences}),
        },
        "legal_admissibility": {
            "csddd_art8_ready": csddd_ready,
            "csrd_disclosure_ready": csrd_ready,
            "icc_proceedings_ready": icc_ready,
            "civil_litigation_ready": avg_reliability >= 0.65,
        },
        "evidences": evidences,
        "retention_policy": {
            "minimum_years": 10,
            "regulation": "CSDDD Art.10 + CSRD ESRS + RGPD Art.17",
            "deletion_requires": "Board approval + legal clearance",
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — EVIDENCE DOCUMENTATION AGENT")
    print("  Expert Documentation & Archivage Preuves Droits Humains")
    print("  Standards: ISO 30301 | CSDDD Art.8 | UNGP Commentary | ICC")
    print("=" * 70)

    ev1 = create_evidence_record(
        entity_id="SDR-001",
        entity_name="Myanmar — Rohingyas 1M Apatrides",
        evidence_type="LEGAL",
        title="Arrêt CIJ — Gambie v. Myanmar (Mesures provisoires 2020)",
        source="Cour Internationale de Justice",
        date="2020-01-23",
        content_summary="La CIJ ordonne au Myanmar de prendre des mesures conservatoires pour protéger les Rohingyas contre le génocide. Constitue preuve légale niveau TRÈS ÉLEVÉ.",
        legal_standards=["ICC_ROME_STATUTE", "ICJ_RULES", "CSDDD_ART8"],
    )

    ev2 = create_evidence_record(
        entity_id="SDR-001",
        entity_name="Myanmar — Rohingyas 1M Apatrides",
        evidence_type="STATISTICAL",
        title="UNHCR Rapport Global Apatridie 2023 — Myanmar Section",
        source="UNHCR — Haut-Commissariat aux Réfugiés ONU",
        date="2023-11-01",
        content_summary="1.08 million de Rohingyas apatrides au Myanmar. 100% privés de citoyenneté depuis 1982 (Loi Citoyenneté Myanmar). 0 acte de naissance délivré depuis 2017.",
        reliability_override=0.95,
        legal_standards=["CSDDD_ART8", "CSRD_ESRS", "UNGP_COMMENTARY"],
    )

    ev3 = create_evidence_record(
        entity_id="SDR-001",
        entity_name="Myanmar — Rohingyas 1M Apatrides",
        evidence_type="SATELLITE",
        title="UNOSAT — Analyse destruction villages Rakhine 2017-2023",
        source="UNOSAT — UN Satellite Centre",
        date="2023-06-15",
        content_summary="392 villages détruits détectés par analyse satellite dans État Rakhine. Corrélation avec déplacement 700K Rohingyas confirmée. Données géoréférencées.",
        legal_standards=["ICC_ROME_STATUTE", "ICJ_RULES"],
    )

    dossier = build_evidence_dossier(
        "SDR-001",
        "Myanmar — Rohingyas 1M Apatrides",
        "statelessness-document-rights",
        [ev1, ev2, ev3],
    )

    print(f"\n📁 DOSSIER: {dossier['dossier_id']}")
    print(f"   Entité: {dossier['entity_id']} — {dossier['entity_name']}")
    print(f"   Hash intégrité: {dossier['dossier_integrity_hash']}")
    print(f"   Preuves: {dossier['summary']['total_evidences']}")
    print(f"   Fiabilité moyenne: {dossier['summary']['avg_reliability']*100:.1f}%")
    print(f"   Poids légal max: {dossier['summary']['strongest_legal_weight']}")

    print(f"\n⚖️  ADMISSIBILITÉ LÉGALE:")
    for standard, status in dossier["legal_admissibility"].items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {standard.replace('_', ' ')}")

    print(f"\n📋 PREUVES DOCUMENTÉES:")
    for ev in dossier["evidences"]:
        print(f"\n   [{ev['evidence_type']}] {ev['iso_30301_metadata']['title'][:55]}...")
        print(f"   Source: {ev['iso_30301_metadata']['source']}")
        print(f"   Hash: {ev['iso_30301_metadata']['authenticity_hash']}")
        print(f"   Fiabilité: {ev['reliability_score']*100:.0f}% | Poids: {ev['legal_weight']}")

    print(f"\n🗄️  POLITIQUE RÉTENTION: {dossier['retention_policy']['minimum_years']} ans minimum")
    print(f"   Règlement: {dossier['retention_policy']['regulation']}")
    print(f"\n✅ Evidence Documentation Agent — Dossier constitué avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
