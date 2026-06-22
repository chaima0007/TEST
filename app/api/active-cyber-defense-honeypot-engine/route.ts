import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[active-cyber-defense-honeypot-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Active Cyber Defense Honeypot Engine Agent",
  domain: "active_cyber_defense_honeypot",
  total_entities: 8,
  avg_composite: 62.98,
  confidence_score: 0.92,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    honeypot_effectiveness: 1,
    legal_countermeasure_score: 2,
    forensic_evidence_quality: 2,
    threat_detection_speed: 3,
  },
  top_risk_entities: [
    "SQL Injection Bot — Exfiltration BDD Clients & Tokens Auth Caelum",
    "Ransomware Delivery Attempt — Chiffrement Données ESG & Brevets Stratégiques",
    "Credential Stuffing Attack — Bourrage Identifiants Volés 4M+ Comptes",
  ],
  critical_alerts: [
    "SQL Injection Bot: honeypot_effectiveness",
    "Ransomware Delivery Attempt: threat_detection_speed",
    "Credential Stuffing Attack: legal_countermeasure_score",
    "Data Scraping Crawler: forensic_evidence_quality",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_active_cyber_defense_honeypot_index: 6.3,
  data_sources: [
    "eu_nis2_directive_active_defense_2024",
    "owasp_honeypot_framework_2023",
    "europol_ec3_cybercrime_reporting_2024",
    "nist_sp800_61_incident_response_2024",
  ],
  legal_framework: {
    allowed: [
      "Honeypots — pièges passifs légaux dans 180 pays",
      "Tarpit — ralentissement connexions suspectes (légal EU)",
      "IP blocking automatique (légal)",
      "Forensic collection — preuves pour poursuites (légal)",
      "Signalement Europol EC3 en 24h (obligatoire NIS2)",
      "Action en justice — Belgium Computer Crime Act 2000",
    ],
    forbidden: [
      "Counter-attack directe sur IP attaquant (illégal EU Art. 2-6 Budapest Convention)",
      "Déploiement malware en retour (illégal partout)",
    ],
    verdict:
      "Les honeypots + forensics + poursuites judiciaires sont légalement plus dévastateurs pour l'attaquant qu'une contre-attaque directe",
  },
  entities: [
    {
      id: "ACD-001",
      name: "SQL Injection Bot — Exfiltration BDD Clients & Tokens Auth Caelum",
      threat_type: "Database Attack",
      threat_detection_speed: 92.0,
      honeypot_effectiveness: 90.0,
      forensic_evidence_quality: 95.0,
      legal_countermeasure_score: 88.0,
      composite_score: 91.45,
      risk_level: "critique",
      primary_pattern: "honeypot_effectiveness",
      estimated_active_cyber_defense_honeypot_index: 9.14,
      last_updated: "2026-06-21",
    },
    {
      id: "ACD-002",
      name: "Credential Stuffing Attack — Bourrage Identifiants Volés 4M+ Comptes",
      threat_type: "Authentication Attack",
      threat_detection_speed: 88.0,
      honeypot_effectiveness: 92.0,
      forensic_evidence_quality: 85.0,
      legal_countermeasure_score: 90.0,
      composite_score: 88.65,
      risk_level: "critique",
      primary_pattern: "legal_countermeasure_score",
      estimated_active_cyber_defense_honeypot_index: 8.87,
      last_updated: "2026-06-21",
    },
    {
      id: "ACD-003",
      name: "Data Scraping Crawler — Extraction Propriété Intellectuelle Moteurs IA Caelum",
      threat_type: "IP Theft",
      threat_detection_speed: 85.0,
      honeypot_effectiveness: 88.0,
      forensic_evidence_quality: 92.0,
      legal_countermeasure_score: 85.0,
      composite_score: 87.5,
      risk_level: "critique",
      primary_pattern: "forensic_evidence_quality",
      estimated_active_cyber_defense_honeypot_index: 8.75,
      last_updated: "2026-06-21",
    },
    {
      id: "ACD-004",
      name: "Ransomware Delivery Attempt — Chiffrement Données ESG & Brevets Stratégiques",
      threat_type: "Ransomware",
      threat_detection_speed: 95.0,
      honeypot_effectiveness: 88.0,
      forensic_evidence_quality: 90.0,
      legal_countermeasure_score: 92.0,
      composite_score: 91.4,
      risk_level: "critique",
      primary_pattern: "threat_detection_speed",
      estimated_active_cyber_defense_honeypot_index: 9.14,
      last_updated: "2026-06-21",
    },
    {
      id: "ACD-005",
      name: "DDoS Amplification — Saturation Infrastructure API Swarm & Dashboards",
      threat_type: "DDoS",
      threat_detection_speed: 52.0,
      honeypot_effectiveness: 45.0,
      forensic_evidence_quality: 38.0,
      legal_countermeasure_score: 50.0,
      composite_score: 46.6,
      risk_level: "élevé",
      primary_pattern: "threat_detection_speed",
      estimated_active_cyber_defense_honeypot_index: 4.66,
      last_updated: "2026-06-21",
    },
    {
      id: "ACD-006",
      name: "Phishing Campaign — Usurpation Identité Chaima Mhadbi & Ingénierie Sociale",
      threat_type: "Social Engineering",
      threat_detection_speed: 45.0,
      honeypot_effectiveness: 50.0,
      forensic_evidence_quality: 52.0,
      legal_countermeasure_score: 48.0,
      composite_score: 48.4,
      risk_level: "élevé",
      primary_pattern: "forensic_evidence_quality",
      estimated_active_cyber_defense_honeypot_index: 4.84,
      last_updated: "2026-06-21",
    },
    {
      id: "ACD-007",
      name: "Port Scanning — Reconnaissance Infrastructure Serveurs Caelum Partners",
      threat_type: "Reconnaissance",
      threat_detection_speed: 42.0,
      honeypot_effectiveness: 38.0,
      forensic_evidence_quality: 35.0,
      legal_countermeasure_score: 40.0,
      composite_score: 38.85,
      risk_level: "modéré",
      primary_pattern: "threat_detection_speed",
      estimated_active_cyber_defense_honeypot_index: 3.89,
      last_updated: "2026-06-21",
    },
    {
      id: "ACD-008",
      name: "Known CVE Exploit — Vulnérabilité Log4j/OpenSSL (Déjà Patché & Neutralisé)",
      threat_type: "CVE Exploit",
      threat_detection_speed: 10.0,
      honeypot_effectiveness: 12.0,
      forensic_evidence_quality: 8.0,
      legal_countermeasure_score: 15.0,
      composite_score: 11.0,
      risk_level: "faible",
      primary_pattern: "legal_countermeasure_score",
      estimated_active_cyber_defense_honeypot_index: 1.1,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/active-cyber-defense-honeypot-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
