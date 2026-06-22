import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-health-sovereignty-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Digital Health Sovereignty Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-health-sovereignty-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Digital Health Sovereignty Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Digital Health Sovereignty Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "DHS-001", name: "Système Santé Numérique Éthiopie", country: "Éthiopie", sector: "Infrastructure Santé Numérique", composite_score: 80.30, data_sovereignty_gap: 88, cyber_resilience_gap: 80, platform_dependency: 78, interoperability_gap: 72, risk_level: "critique", primary_pattern: "Fuite Données Médicales", key_signals: ["95% données médicales stockées AWS/Azure hors frontières", "0 SOC santé national — incidents non détectés 72h moy.", "Aucun standard interopérabilité entre 50 hôpitaux régionaux"], estimated_health_index: 8.03, last_updated: "2026-06-20" },
    { id: "DHS-002", name: "Réseau Santé Numérique Pakistan", country: "Pakistan", sector: "Cybersécurité Médicale", composite_score: 74.10, data_sovereignty_gap: 75, cyber_resilience_gap: 82, platform_dependency: 70, interoperability_gap: 68, risk_level: "critique", primary_pattern: "Vulnérabilité Cybersécurité Hospitalière", key_signals: ["3 cyberattaques majeures hôpitaux en 2025 — données exposées", "Ransomware Karachi Teaching Hospital — 48h d'interruption soins", "Dossiers patients 80M stockés sans chiffrement souverain"], estimated_health_index: 7.41, last_updated: "2026-06-20" },
    { id: "DHS-003", name: "Direction Numérique Santé Algérie", country: "Algérie", sector: "Données Médicales", composite_score: 71.10, data_sovereignty_gap: 72, cyber_resilience_gap: 68, platform_dependency: 78, interoperability_gap: 65, risk_level: "critique", primary_pattern: "Dépendance Plateformes Étrangères", key_signals: ["100% logiciels hospitaliers importés — dépendance SAP/Oracle", "Absence loi données santé conforme au droit international", "18 systèmes HIS incompatibles entre CHU et cliniques privées"], estimated_health_index: 7.11, last_updated: "2026-06-20" },
    { id: "DHS-004", name: "Agence e-Santé Maroc", country: "Maroc", sector: "Interopérabilité Santé", composite_score: 59.50, data_sovereignty_gap: 55, cyber_resilience_gap: 52, platform_dependency: 72, interoperability_gap: 60, risk_level: "élevé", primary_pattern: "Dépendance Plateformes Étrangères", key_signals: ["Plateforme nationale santé hébergée en dehors du Maroc", "Dossier médical partagé non déployé après 4 ans de projet", "Cyber incidents santé +180% en 2025 vs 2024"], estimated_health_index: 5.95, last_updated: "2026-06-20" },
    { id: "DHS-005", name: "Ministère Santé Numérique Sénégal", country: "Sénégal", sector: "Infrastructure Santé Numérique", composite_score: 54.10, data_sovereignty_gap: 50, cyber_resilience_gap: 48, platform_dependency: 62, interoperability_gap: 58, risk_level: "élevé", primary_pattern: "Dépendance Plateformes Étrangères", key_signals: ["Programme Touba Digital Health dépend à 80% d'OpenMRS US", "Budget cybersécurité santé < 0.1% budget IT total", "Données vaccination COVID stockées Google Cloud EU"], estimated_health_index: 5.41, last_updated: "2026-06-20" },
    { id: "DHS-006", name: "Agence Santé Numérique Pologne", country: "Pologne", sector: "Cybersécurité Médicale", composite_score: 33.10, data_sovereignty_gap: 35, cyber_resilience_gap: 30, platform_dependency: 38, interoperability_gap: 28, risk_level: "modéré", primary_pattern: "Risque Souveraineté Santé Numérique", key_signals: ["IKP — dossier patient en ligne déployé 70% établissements", "CERT santé national opérationnel mais sous-dimensionné", "Interopérabilité partielle : 3 standards coexistants"], estimated_health_index: 3.31, last_updated: "2026-06-20" },
    { id: "DHS-007", name: "Agence Nationale e-Santé France", country: "France", sector: "Données Médicales", composite_score: 14.00, data_sovereignty_gap: 15, cyber_resilience_gap: 12, platform_dependency: 18, interoperability_gap: 10, risk_level: "faible", primary_pattern: "Souveraineté Santé Numérique Maîtrisée", key_signals: ["Mon Espace Santé — hébergement HDS souverain certifié", "ANSSI cybersécurité santé — 500M€ plan cyber 2025-2027", "SEGUR numérique — interopérabilité nationale déployée"], estimated_health_index: 1.40, last_updated: "2026-06-20" },
    { id: "DHS-008", name: "Myndigheten för digital förvaltning Suède", country: "Suède", sector: "Interopérabilité Santé", composite_score: 9.60, data_sovereignty_gap: 10, cyber_resilience_gap: 8, platform_dependency: 12, interoperability_gap: 8, risk_level: "faible", primary_pattern: "Souveraineté Santé Numérique Maîtrisée", key_signals: ["Journalen — dossier national interopérable 100% établissements", "NCSC cybersécurité santé — réponse incidents < 4h", "Open source public : dépendance GAFAM < 15%"], estimated_health_index: 0.96, last_updated: "2026-06-20" },
  ];

  const n = entities.length;
  const avg_composite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / n * 100) / 100;

  return {
    total_entities: n,
    avg_composite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: { "Fuite Données Médicales": 1, "Vulnérabilité Cybersécurité Hospitalière": 1, "Dépendance Plateformes Étrangères": 3, "Risque Souveraineté Santé Numérique": 1, "Souveraineté Santé Numérique Maîtrisée": 2 },
    top_risk_entities: ["Système Santé Numérique Éthiopie", "Réseau Santé Numérique Pakistan", "Direction Numérique Santé Algérie"],
    critical_alerts: 3,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "health",
    confidence_score: 89.3,
    data_sources: ["OMS — Rapport Santé Numérique Mondiale 2025", "ENISA — Cybersécurité Santé Europe 2026", "ITU — Indice Gouvernance Données Santé 2026"],
    entities,
    avg_estimated_health_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
  };
}
