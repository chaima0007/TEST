import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[trust-economy-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Trust Economy Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/trust-economy-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Trust Economy Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Trust Economy Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "TE-001", name: "Yémen — Effondrement Étatique", country: "MENA", sector: "État Défaillant & Confiance Nulle", composite_score: 82.75, institutional_trust_score: 90.0, interpersonal_trust_score: 82.0, market_confidence_score: 88.0, digital_trust_score: 75.0, risk_level: "critique", primary_pattern: "effondrement_confiance", key_signals: ["Effondrement du capital-confiance au Yémen — déficit institutionnel critique", "Confiance interpersonnelle effondrée — coopération sociale compromise", "Zone de rupture civique — atomisation sociale et contractuelle avancée"], estimated_trust_index: 8.28, last_updated: "2026-06-20" },
    { id: "TE-002", name: "Russie — Défiance Post-Soviétique", country: "Europe de l'Est", sector: "Autoritarisme & Méfiance Systémique", composite_score: 80.0, institutional_trust_score: 85.0, interpersonal_trust_score: 78.0, market_confidence_score: 80.0, digital_trust_score: 72.0, risk_level: "critique", primary_pattern: "effondrement_confiance", key_signals: ["Effondrement du capital-confiance en Russie — déficit institutionnel critique", "Confiance interpersonnelle effondrée — coopération sociale compromise", "Zone de rupture civique — atomisation sociale et contractuelle avancée"], estimated_trust_index: 8.00, last_updated: "2026-06-20" },
    { id: "TE-003", name: "États-Unis — Polarisation Institutionnelle", country: "Amérique du Nord", sector: "Démocratie Fracturée", composite_score: 73.6, institutional_trust_score: 78.0, interpersonal_trust_score: 72.0, market_confidence_score: 70.0, digital_trust_score: 68.0, risk_level: "critique", primary_pattern: "effondrement_confiance", key_signals: ["Effondrement du capital-confiance aux États-Unis — déficit institutionnel critique", "Confiance interpersonnelle effondrée — coopération sociale compromise", "Zone de rupture civique — atomisation sociale et contractuelle avancée"], estimated_trust_index: 7.36, last_updated: "2026-06-20" },
    { id: "TE-004", name: "Liban — Trahison Institutionnelle", country: "MENA", sector: "Effondrement Systémique Multi-Couches", composite_score: 83.25, institutional_trust_score: 88.0, interpersonal_trust_score: 75.0, market_confidence_score: 92.0, digital_trust_score: 70.0, risk_level: "critique", primary_pattern: "effondrement_confiance", key_signals: ["Effondrement du capital-confiance au Liban — déficit institutionnel critique", "Confiance interpersonnelle effondrée — coopération sociale compromise", "Zone de rupture civique — atomisation sociale et contractuelle avancée"], estimated_trust_index: 8.33, last_updated: "2026-06-20" },
    { id: "TE-005", name: "Brésil — Défiance Démocratique", country: "Amériques", sector: "Polarisation Post-Bolsonaro", composite_score: 57.25, institutional_trust_score: 62.0, interpersonal_trust_score: 55.0, market_confidence_score: 58.0, digital_trust_score: 50.0, risk_level: "élevé", primary_pattern: "fragmentation_confiance", key_signals: ["Érosion avancée de la confiance au Brésil — légitimité institutionnelle fragilisée", "Déficit de confiance dans les marchés et l'espace numérique croissant", "Fragmentation sociale — groupes en silo, dialogue inter-communautaire limité"], estimated_trust_index: 5.73, last_updated: "2026-06-20" },
    { id: "TE-006", name: "France — Crise de Légitimité", country: "Europe", sector: "Fracture Élites/Peuple", composite_score: 51.5, institutional_trust_score: 58.0, interpersonal_trust_score: 48.0, market_confidence_score: 50.0, digital_trust_score: 45.0, risk_level: "élevé", primary_pattern: "fragmentation_confiance", key_signals: ["Érosion avancée de la confiance en France — légitimité institutionnelle fragilisée", "Déficit de confiance dans les marchés et l'espace numérique croissant", "Fragmentation sociale — groupes en silo, dialogue inter-communautaire limité"], estimated_trust_index: 5.15, last_updated: "2026-06-20" },
    { id: "TE-007", name: "Allemagne — Institutions Résilientes", country: "Europe", sector: "Capital Social Institutionnel", composite_score: 29.25, institutional_trust_score: 32.0, interpersonal_trust_score: 28.0, market_confidence_score: 30.0, digital_trust_score: 25.0, risk_level: "modéré", primary_pattern: "doute_croissant", key_signals: ["Doute croissant envers les institutions en Allemagne — vigilance recommandée", "Capital-confiance sous pression — signaux d'érosion à surveiller", "Mécanismes de reconstruction de la confiance à renforcer"], estimated_trust_index: 2.93, last_updated: "2026-06-20" },
    { id: "TE-008", name: "Danemark & Nordiques — Modèle Confiance", country: "Europe du Nord", sector: "Capital-Confiance Maximal", composite_score: 9.25, institutional_trust_score: 10.0, interpersonal_trust_score: 8.0, market_confidence_score: 12.0, digital_trust_score: 6.0, risk_level: "faible", primary_pattern: "capital_confiance", key_signals: ["Danemark & Nordiques — Modèle Confiance préserve un capital-confiance solide — tissu social robuste", "Confiance institutionnelle et interpersonnelle dans les normes", "Modèle de capital social à préserver et à exporter"], estimated_trust_index: 0.93, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { effondrement_confiance: 4, erosion_institutionnelle: 0, fragmentation_confiance: 2, doute_croissant: 1, capital_confiance: 1 },
    top_risk_entities: ["Liban — Trahison Institutionnelle", "Yémen — Effondrement Étatique", "Russie — Défiance Post-Soviétique"],
    critical_alerts: ["Liban: effondrement confiance", "Yémen: effondrement confiance", "Russie: effondrement confiance", "États-Unis: effondrement confiance"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "trust",
    confidence_score: 0.79,
    data_sources: ["edelman_trust_barometer", "world_values_survey", "interpersonal_trust_index"],
    entities,
    avg_estimated_trust_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
