import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pension-collapse-engine] SWARM_API_URL non défini — mode mock activé");
}

const NOW = new Date().toISOString().slice(0, 10);

interface PCEntity {
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
  estimated_pension_index: number;
  last_updated: string;
}

function riskLevel(c: number): string {
  if (c >= 60) return "critique";
  if (c >= 40) return "élevé";
  if (c >= 20) return "modéré";
  return "faible";
}

function computePattern(s1: number, s2: number, s4: number): string {
  if (s1 >= 60 && s2 >= 55) return "pension_insolvency_crisis";
  if (s2 >= 55 && s4 >= 55) return "demographic_collapse";
  if (s1 >= 45 && s4 >= 50) return "reform_paralysis";
  if (s1 >= 45) return "generational_burden_spiral";
  return "none";
}

function keySignals(risk: string, country: string): string {
  if (risk === "critique") return "🔴 ALERTE CRITIQUE — Effondrement systémique retraites détecté (" + country + ")";
  if (risk === "élevé") return "🟠 RISQUE ÉLEVÉ — Intervention urgente requise (" + country + ")";
  if (risk === "modéré") return "🟡 RISQUE MODÉRÉ — Surveillance renforcée recommandée (" + country + ")";
  return "🟢 RISQUE FAIBLE — Système de retraite stable (" + country + ")";
}

function buildEntity(
  id: string, name: string, country: string, sector: string,
  s1: number, s2: number, s3: number, s4: number
): PCEntity {
  const composite = Math.round((s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20) * 100) / 100;
  const risk = riskLevel(composite);
  const pattern = computePattern(s1, s2, s4);
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
    key_signals: keySignals(risk, country),
    estimated_pension_index: Math.round(composite / 10 * 100) / 100,
    last_updated: NOW,
  };
}

function getMockData() {
  const entities: PCEntity[] = [
    buildEntity("PCE-001", "Japon — Système de Retraite", "Japon", "retraite_publique", 78, 82, 65, 70),
    buildEntity("PCE-002", "Italie — INPS", "Italie", "retraite_sociale", 74, 68, 72, 78),
    buildEntity("PCE-003", "Grèce — IKA Pension", "Grèce", "retraite_nationale", 80, 72, 68, 75),
    buildEntity("PCE-004", "Allemagne — DRV Bund", "Allemagne", "retraite_publique", 52, 55, 48, 58),
    buildEntity("PCE-005", "France — Assurance Retraite", "France", "retraite_sociale", 48, 50, 55, 60),
    buildEntity("PCE-006", "États-Unis — Social Security", "États-Unis", "retraite_fédérale", 30, 28, 35, 32),
    buildEntity("PCE-007", "Brésil — INSS", "Brésil", "retraite_mixte", 12, 10, 15, 14),
    buildEntity("PCE-008", "Chine — Retraite Nationale", "Chine", "retraite_publique", 14, 12, 10, 16),
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
    domain: "pension",
    confidence_score: 0.91,
    data_sources: ["OCDE Pension Outlook", "Eurostat", "IMF Pension Statistics", "BIT Social Security"],
    entities,
    avg_estimated_pension_index: Math.round(avg_composite / 10 * 100) / 100,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Pension Collapse Engine Agent")));
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pension-collapse-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Pension Collapse Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Pension Collapse Engine Agent"),
      { status: 502 }
    ));
  }
}
