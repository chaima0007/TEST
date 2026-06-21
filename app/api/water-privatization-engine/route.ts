import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[water-privatization-engine] SWARM_API_URL non défini — mode mock activé");
}

const NOW = new Date().toISOString().slice(0, 10);

interface WPEEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  score1: number;
  score2: number;
  score3: number;
  score4: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string;
  estimated_water_index: number;
  last_updated: string;
}

function riskLevel(c: number): string {
  if (c >= 60) return "critique";
  if (c >= 40) return "élevé";
  if (c >= 20) return "modéré";
  return "faible";
}

function computePattern(s1: number, s3: number): string {
  if (s1 >= 65 && s3 >= 65) return "corporate_water_monopoly";
  if (s1 >= 55 && s3 >= 50) return "affordability_crisis_collapse";
  if (s3 >= 55) return "community_access_denial";
  if (s1 >= 45) return "regulatory_capture_spiral";
  return "water_commons_erosion";
}

function keySignals(risk: string, name: string): string {
  if (risk === "critique") return "🔴 ALERTE CRITIQUE — Accaparement eau systémique détecté (" + name + ")";
  if (risk === "élevé") return "🟠 RISQUE ÉLEVÉ — Privatisation hydrique intensive (" + name + ")";
  if (risk === "modéré") return "🟡 RISQUE MODÉRÉ — Surveillance gouvernance eau (" + name + ")";
  return "🟢 RISQUE FAIBLE — Bien commun hydrique préservé (" + name + ")";
}

function buildEntity(
  id: string, name: string, country: string, sector: string,
  s1: number, s2: number, s3: number, s4: number
): WPEEntity {
  const composite = Math.round((s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20) * 100) / 100;
  const risk = riskLevel(composite);
  const pattern = computePattern(s1, s3);
  return {
    id: id,
    name,
    country,
    sector,
    composite_score: composite,
    score1: Math.round(s1 * 100) / 100,
    score2: Math.round(s2 * 100) / 100,
    score3: Math.round(s3 * 100) / 100,
    score4: Math.round(s4 * 100) / 100,
    risk_level: risk,
    primary_pattern: pattern,
    key_signals: keySignals(risk, name),
    estimated_water_index: Math.round(composite / 10 * 100) / 100,
    last_updated: NOW,
  };
}

function getMockData() {
  const entities: WPEEntity[] = [
    buildEntity("WPE-001", "Nestlé Waters",        "Suisse",      "eau_embouteillée",       78, 72, 80, 68),
    buildEntity("WPE-002", "Veolia Water",          "France",      "gestion_eau_municipale",  74, 68, 72, 75),
    buildEntity("WPE-003", "Thames Water",          "Royaume-Uni", "distribution_eau",        70, 75, 65, 78),
    buildEntity("WPE-004", "Suez Water",            "France",      "gestion_eau_mixte",       52, 48, 55, 45),
    buildEntity("WPE-005", "SAUR Group",            "France",      "concession_eau",          48, 55, 50, 42),
    buildEntity("WPE-006", "American Water Works",  "États-Unis",  "eau_réglementée",         30, 28, 32, 25),
    buildEntity("WPE-007", "Aguas Andinas",         "Chili",       "eau_publique_mixte",      12, 10, 14, 11),
    buildEntity("WPE-008", "Manila Water",          "Philippines", "eau_concession",          15, 12, 10, 13),
  ];

  const risk_distribution: Record<string, number> = {};
  const pattern_distribution: Record<string, number> = {};
  let totalComp = 0;
  const critical_alerts: string[] = [];

  for (const e of entities) {
    risk_distribution[e.risk_level] = (risk_distribution[e.risk_level] || 0) + 1;
    pattern_distribution[e.primary_pattern] = (pattern_distribution[e.primary_pattern] || 0) + 1;
    totalComp += e.composite_score;
    if (e.risk_level === "critique") critical_alerts.push(e.key_signals);
  }

  const n = entities.length;
  const avg_composite = Math.round(totalComp / n * 100) / 100;
  const top_risk_entities = [...entities]
    .sort((a, b) => b.composite_score - a.composite_score)
    .slice(0, 3)
    .map(e => e.name);

  return {
    total_entities: n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis: NOW,
    engine_version: "2.0.0",
    domain: "water",
    confidence_score: 0.88,
    data_sources: ["ONU-Eau", "OCDE Water Governance", "Global Water Intelligence", "WHO/UNICEF JMP"],
    entities,
    avg_estimated_water_index: Math.round(avg_composite / 10 * 100) / 100,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Water Privatization Engine Agent"));
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-privatization-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Water Privatization Engine Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Water Privatization Engine Agent"),
      { status: 502 }
    );
  }
}
