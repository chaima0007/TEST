import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Module 345 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Methane Crisis & Arctic Methane Bomb Intelligence Engine

if (!process.env.SWARM_API_URL) {
  console.warn("[methane-crisis-engine] SWARM_API_URL non défini — mode mock activé");
}

type MCEEntity = {
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
  estimated_methane_index: number;
  last_updated: string;
};

const MOCK_ENTITIES_RAW = [
  // MCE-001 — critique — États-Unis — fossil_methane_surge
  // s1>=0.85, s2>=0.80 => fossil_methane_surge
  // composite = 0.90*30 + 0.88*25 + 0.82*25 + 0.76*20 = 27+22+20.5+15.2 = 84.7
  { id: "MCE-001", name: "US EPA Methane Monitoring", country: "États-Unis",
    sector: "agence_federale", s1: 0.90, s2: 0.88, s3: 0.82, s4: 0.76 },
  // MCE-002 — critique — Russie — arctic_methane_bomb
  // s2>=0.85, s3>=0.80 => arctic_methane_bomb
  // composite = 0.86*30 + 0.92*25 + 0.88*25 + 0.80*20 = 25.8+23+22+16 = 86.8
  { id: "MCE-002", name: "Gazprom Environmental Division", country: "Russie",
    sector: "industrie_gaziere", s1: 0.86, s2: 0.92, s3: 0.88, s4: 0.80 },
  // MCE-003 — critique — Arabie Saoudite — flaring_crisis
  // s1>=0.85, s4>=0.80 => flaring_crisis
  // composite = 0.88*30 + 0.78*25 + 0.72*25 + 0.85*20 = 26.4+19.5+18+17 = 80.9
  { id: "MCE-003", name: "Saudi Aramco Gas Operations", country: "Arabie Saoudite",
    sector: "industrie_petroliere", s1: 0.88, s2: 0.78, s3: 0.72, s4: 0.85 },
  // MCE-004 — eleve — Australie
  // composite = 0.62*30 + 0.58*25 + 0.55*25 + 0.50*20 = 18.6+14.5+13.75+10 = 56.85
  { id: "MCE-004", name: "Australian Gas Infrastructure Group", country: "Australie",
    sector: "infrastructure_gaz", s1: 0.62, s2: 0.58, s3: 0.55, s4: 0.50 },
  // MCE-005 — eleve — Kazakhstan
  // composite = 0.55*30 + 0.60*25 + 0.58*25 + 0.45*20 = 16.5+15+14.5+9 = 55.0
  { id: "MCE-005", name: "KazMunayGas Environmental", country: "Kazakhstan",
    sector: "industrie_gaziere", s1: 0.55, s2: 0.60, s3: 0.58, s4: 0.45 },
  // MCE-006 — modere — Canada
  // composite = 0.35*30 + 0.30*25 + 0.28*25 + 0.32*20 = 10.5+7.5+7+6.4 = 31.4
  { id: "MCE-006", name: "Canada Energy Regulator", country: "Canada",
    sector: "agence_reglementation", s1: 0.35, s2: 0.30, s3: 0.28, s4: 0.32 },
  // MCE-007 — faible — Pays-Bas
  // composite = 0.12*30 + 0.10*25 + 0.14*25 + 0.10*20 = 3.6+2.5+3.5+2 = 11.6
  { id: "MCE-007", name: "Nederlandse Gasunie", country: "Pays-Bas",
    sector: "infrastructure_gaz", s1: 0.12, s2: 0.10, s3: 0.14, s4: 0.10 },
  // MCE-008 — faible — Iran
  // composite = 0.10*30 + 0.14*25 + 0.12*25 + 0.08*20 = 3+3.5+3+1.6 = 11.1
  { id: "MCE-008", name: "National Iranian Gas Company", country: "Iran",
    sector: "industrie_gaziere", s1: 0.10, s2: 0.14, s3: 0.12, s4: 0.08 },
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
  if (raw.s1 >= 0.85 && raw.s2 >= 0.80) return "fossil_methane_surge";
  if (raw.s2 >= 0.85 && raw.s3 >= 0.80) return "arctic_methane_bomb";
  if (raw.s1 >= 0.85 && raw.s4 >= 0.80) return "flaring_crisis";
  if (raw.s2 >= 0.70 && raw.s3 >= 0.65) return "regulatory_failure_cascade";
  if (raw.s3 >= 0.70 && raw.s4 >= 0.65) return "climate_feedback_loop";
  return "none";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_emissions_methane_critiques";
  if (risk === "eleve") return "reduction_methane_acceleree";
  if (risk === "modere") return "renforcement_surveillance_methane";
  return "veille_methane_continue";
}

function keySignals(risk: string, pattern: string, comp: number): string {
  const labels: Record<string, string> = {
    fossil_methane_surge:        "Surge émissions méthane fossile",
    arctic_methane_bomb:         "Bombe méthane arctique",
    flaring_crisis:              "Crise torchage méthane",
    regulatory_failure_cascade:  "Cascade défaillance réglementaire",
    climate_feedback_loop:       "Boucle rétroaction climatique méthane",
    none:                        "Émissions méthane sous contrôle",
  };
  const label = labels[pattern] ?? pattern;
  if (risk === "critique") return `Crise méthane systémique — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "eleve") return `Crise méthane majeure — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "modere") return `Méthane structurel — ${label} — composite ${comp.toFixed(1)}`;
  return `Émissions méthane surveillées — composite ${comp.toFixed(1)}`;
}

function getMockData() {
  const entities: MCEEntity[] = MOCK_ENTITIES_RAW.map(raw => {
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
      estimated_methane_index: Math.round(comp / 100 * 10 * 100) / 100,
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
    totalIdx += e.estimated_methane_index;
    if (e.risk_level === "critique") {
      top_risk_entities.push({ id: e.entity_id, name: e.name, composite_score: e.composite_score });
      critical_alerts.push(e.key_signals);
    }
  }

  const n = entities.length;
  const avg_composite = Math.round(totalComp / n * 100) / 100;
  const avg_estimated_methane_index = Math.round(totalIdx / n * 100) / 100;

  return {
    total_entities:              n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis:               new Date().toISOString(),
    engine_version:              "345.2.0",
    domain:                      "methane",
    confidence_score:            0.91,
    data_sources:                ["US-EPA", "Gazprom", "Aramco", "AEMO", "KMG", "CER", "Gasunie", "NIGC"],
    entities,
    avg_estimated_methane_index,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Methane Crisis Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/methane-crisis-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Methane Crisis Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Methane Crisis Agent"), { status: 502 }));
  }
}
