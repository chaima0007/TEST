#!/usr/bin/env python3
"""
Traceability & Blockchain Agent — Caelum Partners CaelumSwarm™
Traçabilité immuable des scores droits humains et preuves via registre distribué.
Simulation cryptographique de blockchain sans dépendance externe.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone

BLOCKCHAIN_CONFIG = {
    "chain_id": "caelum-human-rights-chain-v1",
    "consensus": "Proof of Authority (PoA) — Validateurs accrédités",
    "validators": [
        "Caelum Partners SPRL",
        "TÜV Rheinland — Auditeur Tier 1",
        "Bureau Veritas — Auditeur Tier 2",
        "KPMG ESG Audit",
    ],
    "block_time_seconds": 30,
    "hash_algorithm": "SHA-256",
    "standards": ["ISO/TS 23635:2022", "GS1 EPCIS 2.0", "W3C VC 1.1"],
    "smart_contract_platform": "Hyperledger Fabric (private chain)",
}

TOKENIZED_ASSETS = {
    "COMPLIANCE_CERTIFICATE": "NFT non-transférable — Certificat conformité droits humains",
    "AUDIT_PROOF": "NFT preuve d'audit terrain — Hash cryptographique signé",
    "SCORE_SNAPSHOT": "Token score CaelumSwarm™ — Horodaté et immuable",
    "GRIEVANCE_RECORD": "Token réclamation — Traçabilité complète traitement",
    "REMEDY_PROOF": "NFT preuve réparation — Validation victime requise",
}

VERIFIED_DATA_SOURCES = {
    "UNHCR": {"trust_level": 0.98, "blockchain_id": "src-unhcr-001"},
    "ILO": {"trust_level": 0.97, "blockchain_id": "src-ilo-002"},
    "WORLD_BANK": {"trust_level": 0.95, "blockchain_id": "src-wb-003"},
    "AMNESTY_INT": {"trust_level": 0.88, "blockchain_id": "src-ai-004"},
    "HUMAN_RIGHTS_WATCH": {"trust_level": 0.87, "blockchain_id": "src-hrw-005"},
    "SATELLITE_UNOSAT": {"trust_level": 0.96, "blockchain_id": "src-unosat-006"},
    "CAELUM_SWARM": {"trust_level": 0.93, "blockchain_id": "src-cs-007"},
}

PROVENANCE_CHAIN_LEVELS = [
    "L0_RAW_SOURCE",
    "L1_INGESTED",
    "L2_VERIFIED",
    "L3_SCORED",
    "L4_AUDITED",
    "L5_CERTIFIED",
    "L6_PUBLISHED",
]


def sha256_hash(data: str) -> str:
    """Hash SHA-256 d'une donnée."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def create_block(
    index: int,
    data: dict,
    previous_hash: str = "0" * 64,
    validator: str = "Caelum Partners SPRL",
) -> dict:
    """Crée un bloc de la blockchain."""
    timestamp = datetime.now(timezone.utc).isoformat()
    block_content = json.dumps({
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "previous_hash": previous_hash,
    }, sort_keys=True)

    block_hash = sha256_hash(block_content)
    merkle_root = sha256_hash(json.dumps(data, sort_keys=True))

    return {
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "previous_hash": previous_hash,
        "block_hash": block_hash,
        "merkle_root": merkle_root,
        "validator": validator,
        "consensus": BLOCKCHAIN_CONFIG["consensus"],
        "chain_id": BLOCKCHAIN_CONFIG["chain_id"],
    }


def verify_chain_integrity(chain: list) -> dict:
    """Vérifie l'intégrité de la chaîne de blocs."""
    if not chain:
        return {"valid": False, "reason": "Empty chain"}

    errors = []
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        if current["previous_hash"] != previous["block_hash"]:
            errors.append(f"Block {i}: previous_hash mismatch")

        expected_hash = sha256_hash(json.dumps({
            "index": current["index"],
            "timestamp": current["timestamp"],
            "data": current["data"],
            "previous_hash": current["previous_hash"],
        }, sort_keys=True))

        if current["block_hash"] != expected_hash:
            errors.append(f"Block {i}: hash tampered")

    return {
        "valid": len(errors) == 0,
        "blocks_verified": len(chain),
        "errors": errors,
        "chain_integrity": "INTACT" if not errors else "COMPROMIS",
    }


def record_score_on_chain(entity: dict, domain: str, wave: int, chain: list) -> tuple:
    """Enregistre le score d'une entité sur la blockchain."""
    score_record = {
        "type": "SCORE_SNAPSHOT",
        "token_id": f"CS-{entity.get('id', 'UNK')}-W{wave}",
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "domain": domain,
        "wave": wave,
        "composite_score": entity.get("composite_score"),
        "risk_level": entity.get("risk_level"),
        "recorded_by": "CaelumSwarm™ v1.0",
        "source_hashes": {
            src: VERIFIED_DATA_SOURCES[src]["blockchain_id"]
            for src in list(VERIFIED_DATA_SOURCES.keys())[:3]
        },
    }

    previous_hash = chain[-1]["block_hash"] if chain else "0" * 64
    block = create_block(len(chain), score_record, previous_hash)
    chain.append(block)
    return block, chain


def trace_data_provenance(entity_id: str, score: float, sources: list) -> dict:
    """Trace la provenance des données selon les niveaux L0-L6."""
    provenance_chain = []
    current_hash = "0" * 64

    for level in PROVENANCE_CHAIN_LEVELS:
        level_data = {
            "level": level,
            "entity_id": entity_id,
            "score_at_level": round(score * (PROVENANCE_CHAIN_LEVELS.index(level) + 1) / len(PROVENANCE_CHAIN_LEVELS), 2),
            "sources_used": sources[:PROVENANCE_CHAIN_LEVELS.index(level) + 1],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        level_hash = sha256_hash(json.dumps(level_data, sort_keys=True) + current_hash)
        provenance_chain.append({
            "level": level,
            "level_hash": level_hash,
            "previous_hash": current_hash,
            "data": level_data,
        })
        current_hash = level_hash

    final_hash = current_hash

    return {
        "entity_id": entity_id,
        "final_provenance_hash": final_hash,
        "provenance_chain": provenance_chain,
        "verifiable_credential": {
            "@context": "https://www.w3.org/2018/credentials/v1",
            "type": ["VerifiableCredential", "HumanRightsScoreCredential"],
            "issuer": "did:caelum:partners:human-rights-chain",
            "issuanceDate": datetime.now(timezone.utc).isoformat(),
            "credentialSubject": {
                "id": f"did:caelum:entity:{entity_id}",
                "humanRightsScore": score,
                "provenanceHash": final_hash,
            },
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — TRACEABILITY & BLOCKCHAIN AGENT")
    print("  Traçabilité Immuable & Provenance Cryptographique")
    print(f"  Chain: {BLOCKCHAIN_CONFIG['chain_id']}")
    print(f"  Consensus: {BLOCKCHAIN_CONFIG['consensus']}")
    print("=" * 70)

    entities = [
        {"id": "DSM-001", "name": "Russie — Deepfakes Guerre Ukraine", "composite_score": 93.45, "risk_level": "critique"},
        {"id": "DSM-004", "name": "États-Unis — Deepfakes Électoraux", "composite_score": 72.65, "risk_level": "critique"},
        {"id": "DSM-008", "name": "Corée du Sud — Législation IA", "composite_score": 7.85, "risk_level": "faible"},
    ]

    blockchain = []

    genesis_block = create_block(0, {
        "type": "GENESIS",
        "chain_id": BLOCKCHAIN_CONFIG["chain_id"],
        "standards": BLOCKCHAIN_CONFIG["standards"],
        "validators": BLOCKCHAIN_CONFIG["validators"],
    })
    blockchain.append(genesis_block)

    print(f"\n🔗 BLOCKCHAIN INITIALISÉE:")
    print(f"   Genesis Block: {genesis_block['block_hash'][:20]}...")
    print(f"   Validateurs: {len(BLOCKCHAIN_CONFIG['validators'])}")

    print(f"\n📦 ENREGISTREMENT SCORES SUR CHAIN:")
    for entity in entities:
        block, blockchain = record_score_on_chain(entity, "deepfake-synthetic-media-rights", 193, blockchain)
        print(f"\n   Block #{block['index']}: {entity['id']}")
        print(f"   Hash: {block['block_hash'][:20]}...")
        print(f"   Merkle Root: {block['merkle_root'][:20]}...")
        print(f"   Prev Hash: {block['previous_hash'][:20]}...")
        print(f"   Score: {entity['composite_score']} | Risk: {entity['risk_level']}")

    print(f"\n🔍 VÉRIFICATION INTÉGRITÉ CHAÎNE:")
    integrity = verify_chain_integrity(blockchain)
    print(f"   Blocs vérifiés: {integrity['blocks_verified']}")
    print(f"   Chaîne intègre: {'✅ OUI' if integrity['valid'] else '❌ COMPROMIS'}")
    print(f"   Statut: {integrity['chain_integrity']}")
    if integrity["errors"]:
        print(f"   Erreurs: {integrity['errors']}")

    print(f"\n📜 TRACE PROVENANCE (DSM-001):")
    provenance = trace_data_provenance("DSM-001", 93.45, list(VERIFIED_DATA_SOURCES.keys())[:4])
    print(f"   Hash final provenance: {provenance['final_provenance_hash'][:20]}...")
    print(f"   Niveaux tracés: {len(provenance['provenance_chain'])}")
    print(f"   Credential W3C VC: {provenance['verifiable_credential']['type']}")

    for level in provenance["provenance_chain"][:3]:
        print(f"     {level['level']}: {level['level_hash'][:16]}...")

    print(f"\n🏅 TOKENS DISPONIBLES:")
    for token_type, description in list(TOKENIZED_ASSETS.items())[:3]:
        print(f"   • {token_type}: {description}")

    print(f"\n📊 ÉTAT FINAL BLOCKCHAIN:")
    print(f"   Total blocs: {len(blockchain)}")
    print(f"   Dernier hash: {blockchain[-1]['block_hash'][:20]}...")
    print(f"   Standards: {', '.join(BLOCKCHAIN_CONFIG['standards'])}")

    print(f"\n✅ Traceability & Blockchain Agent — {len(blockchain)} blocs immuables créés")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
