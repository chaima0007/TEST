import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[critical-infra-cyber-engine] SWARM_API_URL non défini — mode mock activé");
}

// ── Mock entity type ──────────────────────────────────────────────────────────

interface CyberEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  vulnerability_score: number;
  threat_actor_score: number;
  incident_frequency_score: number;
  recovery_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_cyber_index: number;
  last_updated: string;
}

interface CyberSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: number;
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: CyberEntity[];
  avg_estimated_cyber_index: number;
}

interface MockData {
  entities: CyberEntity[];
  summary: CyberSummary;
}

// ── Mock data ─────────────────────────────────────────────────────────────────

function getMockData(): MockData {
  const entities: CyberEntity[] = [
    // ── CRITIQUE (3) ──────────────────────────────────────────────────────────
    {
      entity_id: "CYB-001",
      name: "RéseauElec National",
      country: "France",
      sector: "Énergie & Électricité",
      composite_score: 83.15,
      vulnerability_score: 88.0,
      threat_actor_score: 85.0,
      incident_frequency_score: 82.0,
      recovery_gap_score: 75.0,
      risk_level: "critique",
      primary_pattern: "Vulnérabilité Infrastructure SCADA",
      key_signals: [
        "14 CVE critiques SCADA non patchées",
        "APT Sandworm actif sur périmètre",
        "Délai reprise 72h estimé",
      ],
      estimated_cyber_index: 8.32,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CYB-002",
      name: "AquaGest Urbaine",
      country: "Belgique",
      sector: "Eau & Assainissement",
      composite_score: 79.9,
      vulnerability_score: 80.0,
      threat_actor_score: 88.0,
      incident_frequency_score: 78.0,
      recovery_gap_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Intrusion APT Étatique",
      key_signals: [
        "Tentative empoisonnement eau via cyberattaque",
        "Infrastructure OT connectée internet",
        "Absence segmentation IT/OT",
      ],
      estimated_cyber_index: 7.99,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CYB-003",
      name: "TransRail Connexion",
      country: "Allemagne",
      sector: "Transport & Rail",
      composite_score: 75.6,
      vulnerability_score: 75.0,
      threat_actor_score: 78.0,
      incident_frequency_score: 80.0,
      recovery_gap_score: 68.0,
      risk_level: "critique",
      primary_pattern: "Ransomware Infrastructure Critique",
      key_signals: [
        "3 incidents ransomware en 18 mois",
        "Systèmes signalisation vulnérables",
        "Backup insuffisant critiques",
      ],
      estimated_cyber_index: 7.56,
      last_updated: "2026-06-20",
    },
    // ── ÉLEVÉ (2) ─────────────────────────────────────────────────────────────
    {
      entity_id: "CYB-004",
      name: "TelecomHub SA",
      country: "Pays-Bas",
      sector: "Télécommunications",
      composite_score: 60.25,
      vulnerability_score: 60.0,
      threat_actor_score: 55.0,
      incident_frequency_score: 62.0,
      recovery_gap_score: 65.0,
      risk_level: "élevé",
      primary_pattern: "Exposition Chaîne Fournisseurs",
      key_signals: [
        "Fournisseur tiers compromis",
        "BGP hijacking tentatives",
        "Protocoles SS7 obsolètes",
      ],
      estimated_cyber_index: 6.03,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CYB-005",
      name: "FinClear Payments",
      country: "Luxembourg",
      sector: "Finance & Paiements",
      composite_score: 57.0,
      vulnerability_score: 55.0,
      threat_actor_score: 60.0,
      incident_frequency_score: 58.0,
      recovery_gap_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "Déficit Résilience Cyber",
      key_signals: [
        "RTO 48h non conforme",
        "Test DR annuel insuffisant",
        "Dépendance fournisseur unique",
      ],
      estimated_cyber_index: 5.7,
      last_updated: "2026-06-20",
    },
    // ── MODÉRÉ (1) ────────────────────────────────────────────────────────────
    {
      entity_id: "CYB-006",
      name: "HospitalNet Réseau",
      country: "Suisse",
      sector: "Santé & Hôpitaux",
      composite_score: 39.1,
      vulnerability_score: 42.0,
      threat_actor_score: 38.0,
      incident_frequency_score: 40.0,
      recovery_gap_score: 35.0,
      risk_level: "modéré",
      primary_pattern: "Déficit Résilience Cyber",
      key_signals: [
        "Plan cyber partiel",
        "Formation personnel cyber",
        "Segmentation réseau médicale",
      ],
      estimated_cyber_index: 3.91,
      last_updated: "2026-06-20",
    },
    // ── FAIBLE (2) ────────────────────────────────────────────────────────────
    {
      entity_id: "CYB-007",
      name: "NuclearSafe Systems",
      country: "Finlande",
      sector: "Énergie Nucléaire",
      composite_score: 11.45,
      vulnerability_score: 12.0,
      threat_actor_score: 15.0,
      incident_frequency_score: 10.0,
      recovery_gap_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Vulnérabilité Infrastructure SCADA",
      key_signals: [
        "Air-gap complet systèmes critiques",
        "Certification IEC 62443",
        "Red team annuel ANSSI",
      ],
      estimated_cyber_index: 1.15,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CYB-008",
      name: "DefenceGrid Command",
      country: "Norvège",
      sector: "Défense & Sécurité",
      composite_score: 9.3,
      vulnerability_score: 8.0,
      threat_actor_score: 10.0,
      incident_frequency_score: 8.0,
      recovery_gap_score: 12.0,
      risk_level: "faible",
      primary_pattern: "Intrusion APT Étatique",
      key_signals: [
        "SOC 24/7 opérationnel",
        "Zero trust architecture déployée",
        "Partage renseignement OTAN",
      ],
      estimated_cyber_index: 0.93,
      last_updated: "2026-06-20",
    },
  ];

  // avg_composite = (83.15+79.9+75.6+60.25+57.0+39.1+11.45+9.3) / 8
  //               = 415.75 / 8 = 51.97
  const avgComposite = 51.97;

  const summary: CyberSummary = {
    total_entities: 8,
    avg_composite: avgComposite,
    risk_distribution: {
      critique: 3,
      élevé: 2,
      modéré: 1,
      faible: 2,
    },
    pattern_distribution: {
      "Vulnérabilité Infrastructure SCADA": 2,
      "Intrusion APT Étatique": 2,
      "Ransomware Infrastructure Critique": 1,
      "Exposition Chaîne Fournisseurs": 1,
      "Déficit Résilience Cyber": 2,
    },
    top_risk_entities: ["RéseauElec National", "AquaGest Urbaine", "TransRail Connexion"],
    critical_alerts: 3,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "cyber",
    confidence_score: 0.91,
    data_sources: [
      "ENISA Threat Landscape 2026",
      "CERT-EU Incident Reports",
      "NVD CVE Database",
      "Mandiant APT Intelligence",
      "ICS-CERT Advisories",
    ],
    entities,
    avg_estimated_cyber_index: 5.2,
  };

  return { entities, summary };
}

// ── Route handler ─────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Critical Infrastructure Cyber Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/critical-infra-cyber-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Critical Infrastructure Cyber Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Critical Infrastructure Cyber Agent"),
      { status: 502 }
    );
  }
}
