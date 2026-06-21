import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-cohesion-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Social Cohesion Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social-cohesion-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Social Cohesion Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Social Cohesion Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "SC-001", name: "États-Unis — Polarisation Extrême", country: "Amérique du Nord", sector: "Démocratie Fracturée", composite_score: 85.5, trust_deficit_score: 88.0, polarization_score: 92.0, inequality_fracture_score: 75.0, identity_fragmentation_score: 80.0, risk_level: "critique", primary_pattern: "dissolution_sociale", key_signals: ["Dissolution sociale critique — polarisation bi-partisane au niveau de rupture civile", "Déficit de confiance institutionnel historiquement bas depuis les années 1970", "Fractures raciales et économiques se renforçant mutuellement"], estimated_cohesion_index: 8.55, last_updated: "2026-06-20" },
    { id: "SC-002", name: "Brésil — Inégalités Structurelles", country: "Amériques", sector: "Société Polarisée", composite_score: 78.5, trust_deficit_score: 80.0, polarization_score: 78.0, inequality_fracture_score: 85.0, identity_fragmentation_score: 72.0, risk_level: "critique", primary_pattern: "fragmentation_identitaire", key_signals: ["Fragmentation identitaire critique — inégalités Gini parmi les plus élevées au monde", "Polarisation politique post-Bolsonaro persistante et institutionnalisée", "Fractures raciales et régionales amplifiant la fragmentation sociale"], estimated_cohesion_index: 7.85, last_updated: "2026-06-20" },
    { id: "SC-003", name: "Liban — Collapse Communitaire", country: "MENA", sector: "Fragmentation Multi-Confessionnelle", composite_score: 86.5, trust_deficit_score: 92.0, polarization_score: 85.0, inequality_fracture_score: 82.0, identity_fragmentation_score: 90.0, risk_level: "critique", primary_pattern: "dissolution_sociale", key_signals: ["Dissolution sociale totale — système confessionnel en effondrement économique et politique", "Crise de confiance absolue envers toutes les institutions de l'État", "Fragmentation identitaire multi-confessionnelle — société atomisée"], estimated_cohesion_index: 8.65, last_updated: "2026-06-20" },
    { id: "SC-004", name: "Afrique du Sud — Post-Apartheid", country: "Afrique", sector: "Fractures Raciales & Économiques", composite_score: 74.75, trust_deficit_score: 75.0, polarization_score: 70.0, inequality_fracture_score: 88.0, identity_fragmentation_score: 68.0, risk_level: "critique", primary_pattern: "fragmentation_identitaire", key_signals: ["Fragmentation identitaire critique — inégalités raciales héritées de l'apartheid", "Inégalités économiques parmi les plus extrêmes au monde (Gini > 0.63)", "Déficit de confiance post-apartheid persistant après 30 ans de démocratie"], estimated_cohesion_index: 7.48, last_updated: "2026-06-20" },
    { id: "SC-005", name: "Royaume-Uni — Post-Brexit", country: "Europe", sector: "Fracture Identitaire Nationale", composite_score: 59.5, trust_deficit_score: 58.0, polarization_score: 65.0, inequality_fracture_score: 55.0, identity_fragmentation_score: 62.0, risk_level: "élevé", primary_pattern: "polarisation_croissante", key_signals: ["Polarisation croissante — Brexit a cristallisé des fractures générationnelles et régionales", "Questionnement de l'identité nationale britannique (Écosse, Irlande du Nord)", "Confiance institutionnelle en érosion progressive depuis le referendum"], estimated_cohesion_index: 5.95, last_updated: "2026-06-20" },
    { id: "SC-006", name: "France — Fractures Territoriales", country: "Europe", sector: "Fracture Territoriale & Culturelle", composite_score: 54.5, trust_deficit_score: 52.0, polarization_score: 58.0, inequality_fracture_score: 62.0, identity_fragmentation_score: 48.0, risk_level: "élevé", primary_pattern: "polarisation_croissante", key_signals: ["Polarisation élevée — fracture Paris/périphérie amplifiée par les Gilets Jaunes", "Déficit de confiance envers les élites politiques — abstentionnisme record", "Tensions identitaires autour de la laïcité et de l'intégration"], estimated_cohesion_index: 5.45, last_updated: "2026-06-20" },
    { id: "SC-007", name: "Allemagne & Europe Centrale", country: "Europe", sector: "Cohésion Institutionnelle", composite_score: 30.0, trust_deficit_score: 28.0, polarization_score: 32.0, inequality_fracture_score: 35.0, identity_fragmentation_score: 25.0, risk_level: "modéré", primary_pattern: "tensions_latentes", key_signals: ["Tensions latentes — montée de l'AfD et fracture Est/Ouest persistante", "Cohésion maintenue grâce aux institutions solides et à l'État social", "Signaux de polarisation à surveiller — résilience encore préservée"], estimated_cohesion_index: 3.00, last_updated: "2026-06-20" },
    { id: "SC-008", name: "Scandinavie — Modèle Social", country: "Europe du Nord", sector: "Haute Cohésion Sociale", composite_score: 9.0, trust_deficit_score: 10.0, polarization_score: 8.0, inequality_fracture_score: 12.0, identity_fragmentation_score: 6.0, risk_level: "faible", primary_pattern: "cohesion_consolidee", key_signals: ["Cohésion sociale exemplaire — confiance interpersonnelle parmi les plus hautes au monde", "Inégalités faibles et État providence robuste — capital social maximal", "Modèle de référence mondiale en matière de cohésion civique"], estimated_cohesion_index: 0.90, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { dissolution_sociale: 2, fragmentation_identitaire: 2, polarisation_croissante: 2, tensions_latentes: 1, cohesion_consolidee: 1 },
    top_risk_entities: ["Liban — Collapse Communitaire", "États-Unis — Polarisation Extrême", "Brésil — Inégalités Structurelles"],
    critical_alerts: ["Liban: dissolution sociale totale", "États-Unis: dissolution sociale", "Brésil: fragmentation identitaire critique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "cohesion",
    confidence_score: 0.83,
    data_sources: ["social_cohesion_index", "trust_barometer", "polarization_tracker"],
    entities,
    avg_estimated_cohesion_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
