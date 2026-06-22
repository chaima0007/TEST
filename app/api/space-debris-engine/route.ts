import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Module 370 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Space Debris & Kessler Syndrome Intelligence Engine

if (!process.env.SWARM_API_URL) {
  console.warn("[space-debris-engine] SWARM_API_URL non défini — mode mock activé");
}

type SDEEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  score1: number;
  score2: number;
  score3: number;
  score4: number;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string;
  recommended_action: string;
  estimated_kessler_index: number;
  last_updated: string;
};

const MOCK_ENTITIES_RAW = [
  // SDE-001 — critique — États-Unis — kessler_onset
  // s1>=0.85, s2>=0.80 => kessler_onset
  // composite = 0.90*30 + 0.88*25 + 0.82*25 + 0.76*20 = 27+22+20.5+15.2 = 84.7
  { id: "SDE-001", name: "SpaceX Starlink LEO Operations", country: "États-Unis",
    sector: "operateur_mega_constellation", s1: 0.90, s2: 0.88, s3: 0.82, s4: 0.76 },
  // SDE-002 — critique — Russie — collision_cascade
  // s2>=0.85, s3>=0.80 => collision_cascade
  // composite = 0.82*30 + 0.88*25 + 0.85*25 + 0.76*20 = 24.6+22+21.25+15.2 = 83.05
  { id: "SDE-002", name: "Roscosmos Debris Management", country: "Russie",
    sector: "agence_spatiale", s1: 0.82, s2: 0.88, s3: 0.85, s4: 0.76 },
  // SDE-003 — critique — Chine — asat_debris_field
  // s3>=0.85, s4>=0.80 => asat_debris_field
  // composite = 0.78*30 + 0.80*25 + 0.88*25 + 0.85*20 = 23.4+20+22+17 = 82.4
  { id: "SDE-003", name: "CNSA Space Debris Command", country: "Chine",
    sector: "agence_spatiale", s1: 0.78, s2: 0.80, s3: 0.88, s4: 0.85 },
  // SDE-004 — eleve — Europe
  // composite = 0.58*30 + 0.55*25 + 0.60*25 + 0.50*20 = 17.4+13.75+15+10 = 56.15
  { id: "SDE-004", name: "ESA Space Safety Programme", country: "Europe",
    sector: "agence_spatiale", s1: 0.58, s2: 0.55, s3: 0.60, s4: 0.50 },
  // SDE-005 — eleve — Japon
  // composite = 0.52*30 + 0.50*25 + 0.55*25 + 0.55*20 = 15.6+12.5+13.75+11 = 52.85
  { id: "SDE-005", name: "JAXA Space Debris Research", country: "Japon",
    sector: "agence_spatiale", s1: 0.52, s2: 0.50, s3: 0.55, s4: 0.55 },
  // SDE-006 — modere — Inde
  // composite = 0.35*30 + 0.30*25 + 0.32*25 + 0.28*20 = 10.5+7.5+8+5.6 = 31.6
  { id: "SDE-006", name: "ISRO Space Situational Awareness", country: "Inde",
    sector: "agence_spatiale", s1: 0.35, s2: 0.30, s3: 0.32, s4: 0.28 },
  // SDE-007 — faible — Canada
  // composite = 0.12*30 + 0.10*25 + 0.14*25 + 0.10*20 = 3.6+2.5+3.5+2 = 11.6
  { id: "SDE-007", name: "MDA Space Debris Monitoring", country: "Canada",
    sector: "industrie_spatiale", s1: 0.12, s2: 0.10, s3: 0.14, s4: 0.10 },
  // SDE-008 — faible — Royaume-Uni
  // composite = 0.10*30 + 0.12*25 + 0.10*25 + 0.14*20 = 3+3+2.5+2.8 = 11.3
  { id: "SDE-008", name: "UK Space Agency Debris Division", country: "Royaume-Uni",
    sector: "agence_spatiale", s1: 0.10, s2: 0.12, s3: 0.10, s4: 0.14 },
];

function calcScores(raw: typeof MOCK_ENTITIES_RAW[0]) {
  const s1 = Math.round(raw.s1 * 100 * 100) / 100;
  const s2 = Math.round(raw.s2 * 100 * 100) / 100;
  const s3 = Math.round(raw.s3 * 100 * 100) / 100;
  const s4 = Math.round(raw.s4 * 100 * 100) / 100;
  const comp = Math.round((s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20) * 100) / 100;
  return { s1, s2, s3, s4, comp };
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critique";
  if (comp >= 40) return "eleve";
  if (comp >= 20) return "modere";
  return "faible";
}

function primaryPattern(raw: typeof MOCK_ENTITIES_RAW[0]): string {
  if (raw.s1 >= 0.85 && raw.s2 >= 0.80) return "kessler_onset";
  if (raw.s2 >= 0.85 && raw.s3 >= 0.80) return "collision_cascade";
  if (raw.s3 >= 0.85 && raw.s4 >= 0.80) return "asat_debris_field";
  if (raw.s2 >= 0.70 && raw.s3 >= 0.65) return "mega_constellation_saturation";
  if (raw.s3 >= 0.70 && raw.s4 >= 0.65) return "governance_remediation_failure";
  return "none";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_debris_orbitaux_critiques";
  if (risk === "eleve") return "retrait_debris_actifs_accelere";
  if (risk === "modere") return "renforcement_gouvernance_orbitale";
  return "veille_debris_spatiaux_continue";
}

function keySignals(risk: string, pattern: string, comp: number): string {
  const labels: Record<string, string> = {
    kessler_onset:                  "Déclenchement syndrome Kessler",
    collision_cascade:              "Cascade collisions orbitales",
    asat_debris_field:              "Champ de débris ASAT",
    mega_constellation_saturation:  "Saturation méga-constellation",
    governance_remediation_failure: "Défaillance gouvernance et remédiation",
    none:                           "Débris sous surveillance",
  };
  const label = labels[pattern] ?? pattern;
  if (risk === "critique") return `Crise débris orbitaux systémique — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "eleve") return `Crise débris majeure — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "modere") return `Saturation orbitale structurelle — ${label} — composite ${comp.toFixed(1)}`;
  return `Débris spatiaux surveillés — composite ${comp.toFixed(1)}`;
}

function getMockData() {
  const entities: SDEEntity[] = MOCK_ENTITIES_RAW.map(raw => {
    const { s1, s2, s3, s4, comp } = calcScores(raw);
    const risk = riskLevel(comp);
    const pat = primaryPattern(raw);
    return {
      id:               raw.id,
      name:                    raw.name,
      country:                 raw.country,
      sector:                  raw.sector,
      score1:                  s1,
      score2:                  s2,
      score3:                  s3,
      score4:                  s4,
      composite_score:         comp,
      risk_level:              risk,
      primary_pattern:         pat,
      key_signals:             keySignals(risk, pat, comp),
      recommended_action:      recommendedAction(risk),
      estimated_kessler_index: Math.round(comp / 100 * 10 * 100) / 100,
      last_updated:            new Date().toISOString(),
    };
  });

  const risk_distribution: Record<string, number> = {};
  const pattern_distribution: Record<string, number> = {};
  const top_risk_entities: Array<{ id: string; name: string; composite_score: number }> = [];
  const critical_alerts: string[] = [];
  let totalComp = 0;
  let totalIdx = 0;

  for (const e of entities) {
    risk_distribution[e.risk_level] = (risk_distribution[e.risk_level] ?? 0) + 1;
    pattern_distribution[e.primary_pattern] = (pattern_distribution[e.primary_pattern] ?? 0) + 1;
    totalComp += e.composite_score;
    totalIdx += e.estimated_kessler_index;
    if (e.risk_level === "critique") {
      top_risk_entities.push({ id: e.entity_id, name: e.name, composite_score: e.composite_score });
      critical_alerts.push(e.key_signals);
    }
  }

  const n = entities.length;
  const avg_composite = Math.round(totalComp / n * 100) / 100;
  const avg_estimated_kessler_index = Math.round(totalIdx / n * 100) / 100;

  return {
    total_entities:              n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis:               new Date().toISOString(),
    engine_version:              "370.2.0",
    domain:                      "space",
    confidence_score:            0.90,
    data_sources:                ["SpaceX", "Roscosmos", "CNSA", "ESA", "JAXA", "ISRO", "MDA", "UKSA"],
    entities,
    avg_estimated_kessler_index,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Space Debris Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/space-debris-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Space Debris Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Space Debris Agent"), { status: 502 }));
  }
}
