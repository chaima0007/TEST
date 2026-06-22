import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[antifragility-index-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Antifragility Index Engine Agent"),
    ));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/antifragility-index-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Antifragility Index Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Antifragility Index Engine Agent"),
      { status: 502 },
    ));
  }
}

function getMockData() {
  const entities = [
    {
      id: "AF-001",
      name: "Singapour",
      country: "Singapour",
      sector: "Nation-État",
      composite_score: 88.85,
      stress_response_score: 92.0,
      adaptive_capacity_score: 88.0,
      optionality_score: 85.0,
      convexity_score: 90.0,
      risk_level: "faible",
      primary_pattern: "systeme_antifragile",
      key_signals: [
        "Réponse au stress excellente — score 92.0/100 : renforcement sous pression",
        "Capacité adaptive élevée — 88.0/100 — institutions agiles",
        "Optionnalité stratégique forte — indice 85.0/100 : asymétrie positive",
      ],
      estimated_antifragility_index: 8.89,
      last_updated: "2026-06-20",
    },
    {
      id: "AF-002",
      name: "Suisse",
      country: "Suisse",
      sector: "Nation-État",
      composite_score: 88.9,
      stress_response_score: 88.0,
      adaptive_capacity_score: 90.0,
      optionality_score: 92.0,
      convexity_score: 85.0,
      risk_level: "faible",
      primary_pattern: "systeme_antifragile",
      key_signals: [
        "Réponse au stress excellente — score 88.0/100 : renforcement sous pression",
        "Capacité adaptive élevée — 90.0/100 — institutions agiles",
        "Optionnalité stratégique forte — indice 92.0/100 : asymétrie positive",
      ],
      estimated_antifragility_index: 8.89,
      last_updated: "2026-06-20",
    },
    {
      id: "AF-003",
      name: "Israël",
      country: "Israël",
      sector: "Nation-État",
      composite_score: 83.1,
      stress_response_score: 85.0,
      adaptive_capacity_score: 82.0,
      optionality_score: 78.0,
      convexity_score: 88.0,
      risk_level: "faible",
      primary_pattern: "systeme_antifragile",
      key_signals: [
        "Réponse au stress excellente — score 85.0/100 : renforcement sous pression",
        "Capacité adaptive élevée — 82.0/100 — institutions agiles",
        "Optionnalité stratégique forte — indice 78.0/100 : asymétrie positive",
      ],
      estimated_antifragility_index: 8.31,
      last_updated: "2026-06-20",
    },
    {
      id: "AF-004",
      name: "États-Unis",
      country: "États-Unis",
      sector: "Nation-État",
      composite_score: 71.35,
      stress_response_score: 72.0,
      adaptive_capacity_score: 68.0,
      optionality_score: 75.0,
      convexity_score: 70.0,
      risk_level: "modéré",
      primary_pattern: "resilience_adaptive",
      key_signals: [
        "Réponse au stress modérée — score 72.0/100 : résilience partielle",
        "Capacité adaptive fonctionnelle — 68.0/100 — amélioration possible",
        "Optionnalité satisfaisante — indice 75.0/100 : renforcement recommandé",
      ],
      estimated_antifragility_index: 7.14,
      last_updated: "2026-06-20",
    },
    {
      id: "AF-005",
      name: "Allemagne",
      country: "Allemagne",
      sector: "Nation-État",
      composite_score: 66.4,
      stress_response_score: 65.0,
      adaptive_capacity_score: 70.0,
      optionality_score: 68.0,
      convexity_score: 62.0,
      risk_level: "élevé",
      primary_pattern: "resilience_adaptive",
      key_signals: [
        "Réponse au stress faible — score 65.0/100 : fragilité préoccupante",
        "Capacité adaptive limitée — 70.0/100 — adaptation lente",
        "Optionnalité restreinte — indice 68.0/100 : diversification nécessaire",
      ],
      estimated_antifragility_index: 6.64,
      last_updated: "2026-06-20",
    },
    {
      id: "AF-006",
      name: "Brésil",
      country: "Brésil",
      sector: "Nation-État",
      composite_score: 44.15,
      stress_response_score: 48.0,
      adaptive_capacity_score: 42.0,
      optionality_score: 45.0,
      convexity_score: 40.0,
      risk_level: "élevé",
      primary_pattern: "fragilite_cachee",
      key_signals: [
        "Réponse au stress faible — score 48.0/100 : fragilité préoccupante",
        "Capacité adaptive limitée — 42.0/100 — adaptation lente",
        "Optionnalité restreinte — indice 45.0/100 : diversification nécessaire",
      ],
      estimated_antifragility_index: 4.42,
      last_updated: "2026-06-20",
    },
    {
      id: "AF-007",
      name: "Pakistan",
      country: "Pakistan",
      sector: "Nation-État",
      composite_score: 26.4,
      stress_response_score: 28.0,
      adaptive_capacity_score: 22.0,
      optionality_score: 30.0,
      convexity_score: 25.0,
      risk_level: "critique",
      primary_pattern: "vulnerabilite_systemique",
      key_signals: [
        "Réponse au stress critique — score 28.0/100 : Fragilité systémique confirmée — tout choc majeur risque l'effondrement systémique",
        "Capacité adaptive insuffisante — 22.0/100 — institutions rigides",
        "Optionnalité stratégique quasi nulle — indice 30.0/100 : intervention urgente requise",
      ],
      estimated_antifragility_index: 2.64,
      last_updated: "2026-06-20",
    },
    {
      id: "AF-008",
      name: "Venezuela",
      country: "Venezuela",
      sector: "Nation-État",
      composite_score: 14.0,
      stress_response_score: 15.0,
      adaptive_capacity_score: 12.0,
      optionality_score: 18.0,
      convexity_score: 10.0,
      risk_level: "critique",
      primary_pattern: "fragilite_critique",
      key_signals: [
        "Réponse au stress critique — score 15.0/100 : Fragilité critique — tout choc majeur risque l'effondrement systémique",
        "Capacité adaptive insuffisante — 12.0/100 — institutions rigides",
        "Optionnalité stratégique quasi nulle — indice 18.0/100 : intervention urgente requise",
      ],
      estimated_antifragility_index: 1.4,
      last_updated: "2026-06-20",
    },
  ];

  const avgComposite =
    Math.round((entities.reduce((s, e) => s + e.composite_score, 0) / entities.length) * 100) / 100;

  return {
    total_entities: 8,
    avg_composite: avgComposite,
    risk_distribution: { critique: 2, "élevé": 2, "modéré": 1, faible: 3 },
    pattern_distribution: {
      systeme_antifragile: 3,
      resilience_adaptive: 2,
      fragilite_cachee: 1,
      vulnerabilite_systemique: 1,
      fragilite_critique: 1,
    },
    top_risk_entities: ["Venezuela", "Pakistan", "Brésil"],
    critical_alerts: [
      "[ALERTE CRITIQUE] Venezuela (Venezuela) — Score antifragilité 14.0/100 — Fragilité systémique avérée",
      "[ALERTE CRITIQUE] Pakistan (Pakistan) — Score antifragilité 26.4/100 — Fragilité systémique avérée",
    ],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "antifragility",
    confidence_score: 0.79,
    data_sources: ["resilience_tracker", "institutional_quality_index", "adaptive_capacity_monitor"],
    entities,
    avg_estimated_antifragility_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
  };
}
