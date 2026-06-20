import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Module 326 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Nuclear Risk & Proliferation Intelligence Engine

if (!process.env.SWARM_API_URL) {
  console.warn("[nuclear-risk-engine] SWARM_API_URL non défini — mode mock activé");
}

type NUCEntity = {
  entity_id: string;
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
  estimated_nuclear_index: number;
  last_updated: string;
};

const MOCK_ENTITIES_RAW = [
  // NUC-001 — critique — France — aging_reactor_crisis
  // s1>=0.85, s2>=0.80 => aging_reactor_crisis
  // composite = 0.88*30 + 0.85*25 + 0.78*25 + 0.72*20 = 26.4+21.25+19.5+14.4 = 81.55
  { id: "NUC-001", name: "EDF Parc Nucléaire France", country: "France",
    sector: "energie_nucleaire", s1: 0.88, s2: 0.85, s3: 0.78, s4: 0.72 },
  // NUC-002 — critique — États-Unis — waste_storage_failure
  // s2>=0.85, s3>=0.80 => waste_storage_failure
  // composite = 0.80*30 + 0.88*25 + 0.85*25 + 0.76*20 = 24+22+21.25+15.2 = 82.45
  { id: "NUC-002", name: "US NRC Nuclear Safety Division", country: "États-Unis",
    sector: "agence_surete", s1: 0.80, s2: 0.88, s3: 0.85, s4: 0.76 },
  // NUC-003 — critique — Russie — proliferation_leak
  // s3>=0.85, s4>=0.80 => proliferation_leak
  // composite = 0.75*30 + 0.72*25 + 0.88*25 + 0.85*20 = 22.5+18+22+17 = 79.5
  { id: "NUC-003", name: "Rosatom Nuclear Corporation", country: "Russie",
    sector: "industrie_nucleaire", s1: 0.75, s2: 0.72, s3: 0.88, s4: 0.85 },
  // NUC-004 — eleve — Chine
  // composite = 0.60*30 + 0.58*25 + 0.55*25 + 0.48*20 = 18+14.5+13.75+9.6 = 55.85
  { id: "NUC-004", name: "China National Nuclear Corporation", country: "Chine",
    sector: "industrie_nucleaire", s1: 0.60, s2: 0.58, s3: 0.55, s4: 0.48 },
  // NUC-005 — eleve — Corée du Sud
  // composite = 0.55*30 + 0.52*25 + 0.50*25 + 0.55*20 = 16.5+13+12.5+11 = 53.0
  { id: "NUC-005", name: "KEPCO Nuclear Korea", country: "Corée du Sud",
    sector: "energie_nucleaire", s1: 0.55, s2: 0.52, s3: 0.50, s4: 0.55 },
  // NUC-006 — modere — Japon
  // composite = 0.38*30 + 0.35*25 + 0.32*25 + 0.28*20 = 11.4+8.75+8+5.6 = 33.75
  { id: "NUC-006", name: "TEPCO Nuclear Management", country: "Japon",
    sector: "energie_nucleaire", s1: 0.38, s2: 0.35, s3: 0.32, s4: 0.28 },
  // NUC-007 — faible — Inde
  // composite = 0.14*30 + 0.12*25 + 0.10*25 + 0.14*20 = 4.2+3+2.5+2.8 = 12.5
  { id: "NUC-007", name: "Nuclear Power Corporation of India", country: "Inde",
    sector: "energie_nucleaire", s1: 0.14, s2: 0.12, s3: 0.10, s4: 0.14 },
  // NUC-008 — faible — Ukraine
  // composite = 0.10*30 + 0.14*25 + 0.12*25 + 0.10*20 = 3+3.5+3+2 = 11.5
  { id: "NUC-008", name: "Energoatom Ukraine", country: "Ukraine",
    sector: "energie_nucleaire", s1: 0.10, s2: 0.14, s3: 0.12, s4: 0.10 },
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
  if (raw.s1 >= 0.85 && raw.s2 >= 0.80) return "aging_reactor_crisis";
  if (raw.s2 >= 0.85 && raw.s3 >= 0.80) return "waste_storage_failure";
  if (raw.s3 >= 0.85 && raw.s4 >= 0.80) return "proliferation_leak";
  if (raw.s2 >= 0.70 && raw.s3 >= 0.65) return "dual_use_technology_breach";
  if (raw.s3 >= 0.70 && raw.s4 >= 0.65) return "emergency_response_collapse";
  return "none";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_surete_nucleaire_critique";
  if (risk === "eleve") return "renforcement_controle_nucleaire_accelere";
  if (risk === "modere") return "surveillance_renforcee_installations_nucleaires";
  return "veille_nucleaire_continue";
}

function keySignals(risk: string, pattern: string, comp: number): string {
  const labels: Record<string, string> = {
    aging_reactor_crisis:          "Crise réacteurs vieillissants",
    waste_storage_failure:         "Défaillance stockage déchets nucléaires",
    proliferation_leak:            "Fuite prolifération matières fissiles",
    dual_use_technology_breach:    "Brèche technologie double usage",
    emergency_response_collapse:   "Effondrement réponse urgence nucléaire",
    none:                          "Risque nucléaire sous contrôle",
  };
  const label = labels[pattern] ?? pattern;
  if (risk === "critique") return `Crise nucléaire systémique — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "eleve") return `Risque nucléaire élevé — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "modere") return `Tension nucléaire structurelle — ${label} — composite ${comp.toFixed(1)}`;
  return `Domaine nucléaire surveillé — composite ${comp.toFixed(1)}`;
}

function getMockData() {
  const entities: NUCEntity[] = MOCK_ENTITIES_RAW.map(raw => {
    const { s1, s2, s3, s4, comp } = calcScores(raw);
    const risk = riskLevel(comp);
    const pat = primaryPattern(raw);
    return {
      entity_id:               raw.id,
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
      estimated_nuclear_index: Math.round(comp / 100 * 10 * 100) / 100,
      last_updated:            new Date().toISOString(),
    };
  });

  const risk_distribution: Record<string, number> = {};
  const pattern_distribution: Record<string, number> = {};
  const top_risk_entities: Array<{ entity_id: string; name: string; composite_score: number }> = [];
  const critical_alerts: string[] = [];
  let totalComp = 0;
  let totalIdx = 0;

  for (const e of entities) {
    risk_distribution[e.risk_level] = (risk_distribution[e.risk_level] ?? 0) + 1;
    pattern_distribution[e.primary_pattern] = (pattern_distribution[e.primary_pattern] ?? 0) + 1;
    totalComp += e.composite_score;
    totalIdx += e.estimated_nuclear_index;
    if (e.risk_level === "critique") {
      top_risk_entities.push({ entity_id: e.entity_id, name: e.name, composite_score: e.composite_score });
      critical_alerts.push(e.key_signals);
    }
  }

  const n = entities.length;
  const avg_composite = Math.round(totalComp / n * 100) / 100;
  const avg_estimated_nuclear_index = Math.round(totalIdx / n * 100) / 100;

  return {
    total_entities:              n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis:               new Date().toISOString(),
    engine_version:              "326.2.0",
    domain:                      "nuclear",
    confidence_score:            0.93,
    data_sources:                ["EDF", "US-NRC", "Rosatom", "CNNC", "KEPCO", "TEPCO", "NPCIL", "Energoatom"],
    entities,
    avg_estimated_nuclear_index,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Nuclear Risk Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nuclear-risk-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Nuclear Risk Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Nuclear Risk Agent"), { status: 502 });
  }
}
