import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[critical-infra-cyber-engine] SWARM_API_URL non défini — mode mock activé");
}

const MOCK_ENTITIES = [
  {
    id: "CYB-001",
    name: "Réseau Électrique National UKR",
    country: "Ukraine",
    sector: "Énergie & Réseaux Électriques",
    composite_score: 86.4,
    threat_exposure_score: 92.0,
    vulnerability_score: 88.0,
    resilience_score: 84.0,
    regulatory_gap_score: 79.0,
    risk_level: "critique",
    primary_pattern: "APT État-Nation sur Infrastructure Critique",
    key_signals: [
      "Groupe Sandworm détecté sur SCADA réseau haute tension",
      "Tentatives d'isolement des sous-stations électriques",
      "Exfiltration données topologie réseau confirmée",
    ],
    estimated_cyber_index: 8.64,
    last_updated: "2026-06-20",
  },
  {
    id: "CYB-002",
    name: "Water Authority Greater London",
    country: "Royaume-Uni",
    sector: "Eau & Traitement",
    composite_score: 82.85,
    threat_exposure_score: 87.0,
    vulnerability_score: 85.0,
    resilience_score: 82.0,
    regulatory_gap_score: 75.0,
    risk_level: "critique",
    primary_pattern: "Ransomware Systèmes ICS/SCADA",
    key_signals: [
      "LockBit 4.0 détecté sur contrôleurs traitement eau",
      "Systèmes de chloration accessibles depuis internet",
      "Absence de segmentation OT/IT confirmée",
    ],
    estimated_cyber_index: 8.29,
    last_updated: "2026-06-19",
  },
  {
    id: "CYB-003",
    name: "Port Autonome Rotterdam",
    country: "Pays-Bas",
    sector: "Transport & Logistique",
    composite_score: 78.25,
    threat_exposure_score: 82.0,
    vulnerability_score: 79.0,
    resilience_score: 78.0,
    regulatory_gap_score: 72.0,
    risk_level: "critique",
    primary_pattern: "Compromission Chaîne Approvisionnement",
    key_signals: [
      "Backdoor découverte dans logiciel gestion portuaire tiers",
      "Accès non autorisé systèmes de gestion conteneurs",
      "Perturbation opérations logistiques 72h documentée",
    ],
    estimated_cyber_index: 7.83,
    last_updated: "2026-06-18",
  },
  {
    id: "CYB-004",
    name: "Réseau Hospitalier CHU Paris",
    country: "France",
    sector: "Santé & Infrastructure Médicale",
    composite_score: 59.25,
    threat_exposure_score: 60.0,
    vulnerability_score: 58.0,
    resilience_score: 55.0,
    regulatory_gap_score: 65.0,
    risk_level: "élevé",
    primary_pattern: "Vide Réglementaire Cybersécurité OT",
    key_signals: [
      "Équipements médicaux IoT exposés sans authentification",
      "Conformité NIS2 insuffisante — 23% des exigences satisfaites",
      "Plan de reprise activité inexistant pour systèmes critiques",
    ],
    estimated_cyber_index: 5.93,
    last_updated: "2026-06-17",
  },
  {
    id: "CYB-005",
    name: "Infrastruktur Bahn AG Berlin",
    country: "Allemagne",
    sector: "Transport Ferroviaire",
    composite_score: 57.05,
    threat_exposure_score: 58.0,
    vulnerability_score: 55.0,
    resilience_score: 62.0,
    regulatory_gap_score: 52.0,
    risk_level: "élevé",
    primary_pattern: "Exposition Périphérique Non Sécurisée",
    key_signals: [
      "Systèmes signalisation ETCS exposés au réseau public",
      "Vulnérabilités CVE critiques non patchées > 180 jours",
      "Accès distant techniciens non sécurisé par MFA",
    ],
    estimated_cyber_index: 5.71,
    last_updated: "2026-06-16",
  },
  {
    id: "CYB-006",
    name: "Telecom Backbone Belge",
    country: "Belgique",
    sector: "Télécommunications",
    composite_score: 36.15,
    threat_exposure_score: 38.0,
    vulnerability_score: 35.0,
    resilience_score: 40.0,
    regulatory_gap_score: 30.0,
    risk_level: "modéré",
    primary_pattern: "Vide Réglementaire Cybersécurité OT",
    key_signals: [
      "Topologie réseau cœur partiellement exposée",
      "Audit sécurité annuel en cours de réalisation",
      "Conformité NIS2 à 68% — amélioration en cours",
    ],
    estimated_cyber_index: 3.62,
    last_updated: "2026-06-15",
  },
  {
    id: "CYB-007",
    name: "Swiss Federal Infrastructure Agency",
    country: "Suisse",
    sector: "Administration & Services Publics",
    composite_score: 11.45,
    threat_exposure_score: 12.0,
    vulnerability_score: 10.0,
    resilience_score: 15.0,
    regulatory_gap_score: 8.0,
    risk_level: "faible",
    primary_pattern: "Exposition Périphérique Non Sécurisée",
    key_signals: [
      "Programme Zero Trust Architecture déployé à 95%",
      "SOC 24/7 avec réponse incident < 15 minutes",
      "Conformité ISO 27001 et NIS2 certifiée et maintenue",
    ],
    estimated_cyber_index: 1.15,
    last_updated: "2026-06-14",
  },
  {
    id: "CYB-008",
    name: "Nordics Energy Grid Council",
    country: "Suède",
    sector: "Énergie & Réseaux Électriques",
    composite_score: 10.4,
    threat_exposure_score: 9.0,
    vulnerability_score: 12.0,
    resilience_score: 10.0,
    regulatory_gap_score: 11.0,
    risk_level: "faible",
    primary_pattern: "Exposition Périphérique Non Sécurisée",
    key_signals: [
      "Isolation complète OT/IT avec air-gap physique validé",
      "Exercices de crise cyber trimestriels avec scénarios APT",
      "Détection anomalies IA avec temps réponse < 5 minutes",
    ],
    estimated_cyber_index: 1.04,
    last_updated: "2026-06-13",
  },
];

function getMockData() {
  const entities = MOCK_ENTITIES;
  const n = entities.length;
  const avgComposite =
    Math.round((entities.reduce((s, e) => s + e.composite_score, 0) / n) * 100) / 100;

  const riskDistribution: Record<string, number> = { critique: 0, élevé: 0, modéré: 0, faible: 0 };
  const patternDistribution: Record<string, number> = {};

  for (const e of entities) {
    riskDistribution[e.risk_level] = (riskDistribution[e.risk_level] || 0) + 1;
    patternDistribution[e.primary_pattern] = (patternDistribution[e.primary_pattern] || 0) + 1;
  }

  const sorted = [...entities].sort((a, b) => b.composite_score - a.composite_score);
  const topRiskEntities = sorted.slice(0, 3).map((e) => e.name);
  const criticalAlerts = entities
    .filter((e) => e.risk_level === "critique")
    .map((e) => `${e.name} (${e.country}) — composite ${e.composite_score}`);

  const summary = {
    total_entities: n,
    avg_composite: avgComposite,
    risk_distribution: riskDistribution,
    pattern_distribution: patternDistribution,
    top_risk_entities: topRiskEntities,
    critical_alerts: criticalAlerts,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "cyber",
    confidence_score: 0.93,
    data_sources: [
      "ENISA Threat Landscape Report",
      "CISA Critical Infrastructure Alerts",
      "Europol Cybercrime Centre",
      "ICS-CERT Advisory Database",
      "NATO CCDCOE Intelligence Feed",
    ],
    entities,
    avg_estimated_cyber_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
  };

  return { entities, summary };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Critical Infra Cyber Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/critical-infra-cyber-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Critical Infra Cyber Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Critical Infra Cyber Agent"),
      { status: 502 }
    ));
  }
}
