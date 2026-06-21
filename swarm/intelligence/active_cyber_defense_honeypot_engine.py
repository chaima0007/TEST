from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CyberDefenseEntity:
    entity_id: str
    name: str
    threat_type: str
    threat_detection_speed: float
    honeypot_effectiveness: float
    forensic_evidence_quality: float
    legal_countermeasure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_active_cyber_defense_honeypot_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.threat_detection_speed * 0.30
            + self.honeypot_effectiveness * 0.25
            + self.forensic_evidence_quality * 0.25
            + self.legal_countermeasure_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_active_cyber_defense_honeypot_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ActiveCyberDefenseHoneypotEngineResult:
    agent: str = "Active Cyber Defense Honeypot Engine Agent"
    domain: str = "active_cyber_defense_honeypot"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.92
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_active_cyber_defense_honeypot_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    legal_framework: dict = field(default_factory=dict)
    entities: List[CyberDefenseEntity] = field(default_factory=list)


def run_active_cyber_defense_honeypot_engine() -> ActiveCyberDefenseHoneypotEngineResult:
    entities = [
        # ---- CRITIQUE (4) ----
        CyberDefenseEntity(
            entity_id="ACD-001",
            name="SQL Injection Bot — Exfiltration BDD Clients & Tokens Auth Caelum",
            threat_type="Database Attack",
            threat_detection_speed=92.0,
            honeypot_effectiveness=90.0,
            forensic_evidence_quality=95.0,
            legal_countermeasure_score=88.0,
            primary_pattern="honeypot_effectiveness",
        ),
        CyberDefenseEntity(
            entity_id="ACD-002",
            name="Credential Stuffing Attack — Bourrage Identifiants Volés 4M+ Comptes",
            threat_type="Authentication Attack",
            threat_detection_speed=88.0,
            honeypot_effectiveness=92.0,
            forensic_evidence_quality=85.0,
            legal_countermeasure_score=90.0,
            primary_pattern="legal_countermeasure_score",
        ),
        CyberDefenseEntity(
            entity_id="ACD-003",
            name="Data Scraping Crawler — Extraction Propriété Intellectuelle Moteurs IA Caelum",
            threat_type="IP Theft",
            threat_detection_speed=85.0,
            honeypot_effectiveness=88.0,
            forensic_evidence_quality=92.0,
            legal_countermeasure_score=85.0,
            primary_pattern="forensic_evidence_quality",
        ),
        CyberDefenseEntity(
            entity_id="ACD-004",
            name="Ransomware Delivery Attempt — Chiffrement Données ESG & Brevets Stratégiques",
            threat_type="Ransomware",
            threat_detection_speed=95.0,
            honeypot_effectiveness=88.0,
            forensic_evidence_quality=90.0,
            legal_countermeasure_score=92.0,
            primary_pattern="threat_detection_speed",
        ),
        # ---- ÉLEVÉ (2) ----
        CyberDefenseEntity(
            entity_id="ACD-005",
            name="DDoS Amplification — Saturation Infrastructure API Swarm & Dashboards",
            threat_type="DDoS",
            threat_detection_speed=72.0,
            honeypot_effectiveness=65.0,
            forensic_evidence_quality=58.0,
            legal_countermeasure_score=70.0,
            primary_pattern="threat_detection_speed",
        ),
        CyberDefenseEntity(
            entity_id="ACD-006",
            name="Phishing Campaign — Usurpation Identité Chaima Mhadbi & Ingénierie Sociale",
            threat_type="Social Engineering",
            threat_detection_speed=65.0,
            honeypot_effectiveness=70.0,
            forensic_evidence_quality=72.0,
            legal_countermeasure_score=68.0,
            primary_pattern="forensic_evidence_quality",
        ),
        # ---- MODÉRÉ (1) ----
        CyberDefenseEntity(
            entity_id="ACD-007",
            name="Port Scanning — Reconnaissance Infrastructure Serveurs Caelum Partners",
            threat_type="Reconnaissance",
            threat_detection_speed=42.0,
            honeypot_effectiveness=38.0,
            forensic_evidence_quality=35.0,
            legal_countermeasure_score=40.0,
            primary_pattern="threat_detection_speed",
        ),
        # ---- FAIBLE (1) ----
        CyberDefenseEntity(
            entity_id="ACD-008",
            name="Known CVE Exploit — Vulnérabilité Log4j/OpenSSL (Déjà Patché & Neutralisé)",
            threat_type="CVE Exploit",
            threat_detection_speed=10.0,
            honeypot_effectiveness=12.0,
            forensic_evidence_quality=8.0,
            legal_countermeasure_score=15.0,
            primary_pattern="legal_countermeasure_score",
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    legal_framework = {
        "allowed": [
            "Honeypots — pièges passifs légaux dans 180 pays",
            "Tarpit — ralentissement connexions suspectes (légal EU)",
            "IP blocking automatique (légal)",
            "Forensic collection — preuves pour poursuites (légal)",
            "Signalement Europol EC3 en 24h (obligatoire NIS2)",
            "Action en justice — Belgium Computer Crime Act 2000",
        ],
        "forbidden": [
            "Counter-attack directe sur IP attaquant (illégal EU Art. 2-6 Budapest Convention)",
            "Déploiement malware en retour (illégal partout)",
        ],
        "verdict": "Les honeypots + forensics + poursuites judiciaires sont légalement plus dévastateurs pour l'attaquant qu'une contre-attaque directe",
    }

    return ActiveCyberDefenseHoneypotEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_active_cyber_defense_honeypot_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "eu_nis2_directive_active_defense_2024",
            "owasp_honeypot_framework_2023",
            "europol_ec3_cybercrime_reporting_2024",
            "nist_sp800_61_incident_response_2024",
        ],
        legal_framework=legal_framework,
        entities=entities,
    )


if __name__ == "__main__":
    result = run_active_cyber_defense_honeypot_engine()
    print(f"Agent: {result.agent}")
    print(f"Domain: {result.domain}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"avg_estimated_active_cyber_defense_honeypot_index: {result.avg_estimated_active_cyber_defense_honeypot_index}")
    print(f"Confidence: {result.confidence_score}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Top risk entities: {result.top_risk_entities}")
    print(f"Critical alerts: {result.critical_alerts}")
    print("\n--- Entities ---")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.name[:60]}... | score={e.composite_score} [{e.risk_level}] | index={e.estimated_active_cyber_defense_honeypot_index}")
    print("\n--- Legal Framework ---")
    print(json.dumps(result.legal_framework, ensure_ascii=False, indent=2))
    print("\n--- Full JSON Output ---")
    output = {
        "agent": result.agent,
        "domain": result.domain,
        "total_entities": result.total_entities,
        "avg_composite": result.avg_composite,
        "confidence_score": result.confidence_score,
        "avg_estimated_active_cyber_defense_honeypot_index": result.avg_estimated_active_cyber_defense_honeypot_index,
        "risk_distribution": result.risk_distribution,
        "pattern_distribution": result.pattern_distribution,
        "top_risk_entities": result.top_risk_entities,
        "critical_alerts": result.critical_alerts,
        "last_analysis": result.last_analysis,
        "engine_version": result.engine_version,
        "data_sources": result.data_sources,
        "legal_framework": result.legal_framework,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "threat_type": e.threat_type,
                "threat_detection_speed": e.threat_detection_speed,
                "honeypot_effectiveness": e.honeypot_effectiveness,
                "forensic_evidence_quality": e.forensic_evidence_quality,
                "legal_countermeasure_score": e.legal_countermeasure_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_active_cyber_defense_honeypot_index": e.estimated_active_cyber_defense_honeypot_index,
                "last_updated": e.last_updated,
            }
            for e in result.entities
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
