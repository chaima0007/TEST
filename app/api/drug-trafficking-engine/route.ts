import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[drug-trafficking-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Drug Trafficking Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/drug-trafficking-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Drug Trafficking Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Drug Trafficking Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "DT-001", name: "Corridor Andin — Route Coca Pacifique", country: "Colombie", sector: "Trafic Stupéfiants", composite_score: 83.85, supply_route_risk: 92, laundering_risk: 85, corruption_index: 80, enforcement_gap: 75, risk_level: "critique", primary_pattern: "Corridor Trafic Critique", key_signals: ["2 200 tonnes cocaïne produites en 2025 — record historique", "150 sous-marins narco interceptés en mer Pacifique", "FARC dissidentes contrôlent 40% routes d'export"], estimated_trafficking_index: 8.39, last_updated: "2026-06-20" },
    { entity_id: "DT-002", name: "Triangle d'Or — Trafic Héroïne Asie", country: "Myanmar", sector: "Blanchiment Capitaux", composite_score: 75.50, supply_route_risk: 78, laundering_risk: 82, corruption_index: 72, enforcement_gap: 68, risk_level: "critique", primary_pattern: "Blanchiment Massif", key_signals: ["Production opium Myanmar +180% post-coup 2021", "Casinos Myawaddy — blanchiment 50Mds$ annuels estimés", "Milices ethniques armées contrôlent corridors vers Thaïlande"], estimated_trafficking_index: 7.55, last_updated: "2026-06-20" },
    { entity_id: "DT-003", name: "Route Sahélienne — Cocaine vers Europe", country: "Mali", sector: "Corruption Institutionnelle", composite_score: 72.50, supply_route_risk: 75, laundering_risk: 70, corruption_index: 78, enforcement_gap: 65, risk_level: "critique", primary_pattern: "Capture Institutionnelle", key_signals: ["Corridor sahélien transit 30% cocaïne Europe-Amérique", "Officiers douane corrompus — 70% saisies escortées", "JNIM contrôle péages trafic drogue Bamako-Alger"], estimated_trafficking_index: 7.25, last_updated: "2026-06-20" },
    { entity_id: "DT-004", name: "Route Balkanique — Héroïne Afghanistan", country: "Albanie", sector: "Répression Douanière", composite_score: 60.55, supply_route_risk: 58, laundering_risk: 55, corruption_index: 68, enforcement_gap: 62, risk_level: "critique", primary_pattern: "Capture Institutionnelle", key_signals: ["80% héroïne européenne transite par route balkanique", "Clans albanais — 3e organisation criminelle EU selon Europol", "Ports Durrës et Vlorë — inspection < 2% conteneurs"], estimated_trafficking_index: 6.06, last_updated: "2026-06-20" },
    { entity_id: "DT-005", name: "Cartel Sinaloa — Réseau Fentanyl", country: "Mexique", sector: "Trafic Stupéfiants", composite_score: 52.35, supply_route_risk: 50, laundering_risk: 48, corruption_index: 55, enforcement_gap: 58, risk_level: "élevé", primary_pattern: "Réseau Trafic Émergent", key_signals: ["Fentanyl mexicain : 90 000 morts/an aux USA", "Précurseurs chimiques Chine → Mexique non contrôlés", "Corridors US-Mexique : 3 passages terrestres majeurs infiltrés"], estimated_trafficking_index: 5.24, last_updated: "2026-06-20" },
    { entity_id: "DT-006", name: "Réseau Ecstasy Benelux-Pays-Bas", country: "Pays-Bas", sector: "Blanchiment Capitaux", composite_score: 46.10, supply_route_risk: 45, laundering_risk: 42, corruption_index: 50, enforcement_gap: 48, risk_level: "élevé", primary_pattern: "Réseau Trafic Émergent", key_signals: ["Pays-Bas : 1er producteur mondial MDMA/amphétamines EU", "Liquidation criminalité organisée Taghi — réseau toujours actif", "Port Rotterdam — 180 tonnes cocaïne saisies 2025"], estimated_trafficking_index: 4.61, last_updated: "2026-06-20" },
    { entity_id: "DT-007", name: "Réseau Cannabis Maghreb-Espagne", country: "Maroc", sector: "Trafic Stupéfiants", composite_score: 26.55, supply_route_risk: 28, laundering_risk: 25, corruption_index: 30, enforcement_gap: 22, risk_level: "modéré", primary_pattern: "Réseau Trafic Émergent", key_signals: ["Maroc : 1er producteur mondial cannabis résine", "Détroit Gibraltar — 2 000 go-fast interceptés/an", "Légalisation partielle usage personnel — impact criminel limité"], estimated_trafficking_index: 2.66, last_updated: "2026-06-20" },
    { entity_id: "DT-008", name: "Agence Anti-Narcotiques Islande", country: "Islande", sector: "Répression Douanière", composite_score: 9.60, supply_route_risk: 10, laundering_risk: 8, corruption_index: 12, enforcement_gap: 8, risk_level: "faible", primary_pattern: "Contrôle Trafic Satisfaisant", key_signals: ["Indice corruption CPI = 3 — parmi les plus bas au monde", "Trafic stupéfiants minime — géographie insulaire avantageuse", "Coopération Europol exemplaire — partage renseignements systématique"], estimated_trafficking_index: 0.96, last_updated: "2026-06-20" },
  ];

  const n = entities.length;
  const avg_composite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / n * 100) / 100;

  return {
    total_entities: n,
    avg_composite,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { "Corridor Trafic Critique": 1, "Blanchiment Massif": 1, "Capture Institutionnelle": 2, "Réseau Trafic Émergent": 3, "Contrôle Trafic Satisfaisant": 1 },
    top_risk_entities: ["Corridor Andin — Route Coca Pacifique", "Triangle d'Or — Trafic Héroïne Asie", "Route Sahélienne — Cocaine vers Europe"],
    critical_alerts: 4,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "trafficking",
    confidence_score: 91.0,
    data_sources: ["UNODC — Rapport Mondial Drogues 2025", "Europol — SOCTA Crime Organisé 2026", "INCSR — Contrôle International Stupéfiants 2026"],
    entities,
    avg_estimated_trafficking_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
  };
}
