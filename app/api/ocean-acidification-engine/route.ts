import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Module 372 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Acidification Oceanique & Effondrement des Ecosystemes Marins Intelligence Engine

if (!process.env.SWARM_API_URL) {
  console.warn("[ocean-acidification-engine] SWARM_API_URL non défini — mode mock activé");
}

type OAEEntity = {
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
  estimated_acidification_index: number;
  last_updated: string;
};

const MOCK_ENTITIES_RAW = [
  // OAE-001 — critique — France — coral_reef_mass_extinction
  // coral=0.90>=0.85, ph=0.85>=0.80 => coral_reef_mass_extinction
  // composite = 0.90*30 + 0.85*25 + 0.78*25 + 0.72*20 = 27+21.25+19.5+14.4 = 82.15
  { id: "OAE-001", name: "IFREMER Institut Francais de Recherche", country: "France",
    sector: "recherche_marine", s1: 0.90, s2: 0.85, s3: 0.78, s4: 0.72 },
  // OAE-002 — critique — USA — fishery_ecosystem_collapse
  // biodiv=0.92>=0.85, carbon=0.88>=0.80 => fishery_ecosystem_collapse
  // composite = 0.78*30 + 0.72*25 + 0.92*25 + 0.88*20 = 23.4+18+23+17.6 = 82.0
  { id: "OAE-002", name: "NOAA Ocean Acidification Program", country: "USA",
    sector: "agence_marine", s1: 0.78, s2: 0.72, s3: 0.92, s4: 0.88 },
  // OAE-003 — critique — Australie — carbon_sink_failure
  // carbon=0.85>=0.80, ph=0.88>=0.75 => carbon_sink_failure
  // composite = 0.82*30 + 0.88*25 + 0.75*25 + 0.85*20 = 24.6+22+18.75+17 = 82.35
  { id: "OAE-003", name: "Australian Institute of Marine Science", country: "Australie",
    sector: "recherche_marine", s1: 0.82, s2: 0.88, s3: 0.75, s4: 0.85 },
  // OAE-004 — eleve — Norvege — none
  // composite = 0.42*30 + 0.68*25 + 0.58*25 + 0.40*20 = 12.6+17+14.5+8 = 52.1
  { id: "OAE-004", name: "Institute of Marine Research Norway", country: "Norvège",
    sector: "recherche_marine", s1: 0.42, s2: 0.68, s3: 0.58, s4: 0.40 },
  // OAE-005 — eleve — Japon — marine_biodiversity_crisis
  // biodiv=0.72>=0.70, coral=0.50 (not>=0.65 for pattern)
  // composite = 0.50*30 + 0.52*25 + 0.72*25 + 0.45*20 = 15+13+18+9 = 55
  { id: "OAE-005", name: "Japan Agency for Marine-Earth Science", country: "Japon",
    sector: "agence_marine", s1: 0.50, s2: 0.52, s3: 0.72, s4: 0.45 },
  // OAE-006 — modere — Canada
  // composite = 0.30*30 + 0.28*25 + 0.32*25 + 0.25*20 = 9+7+8+5 = 29
  { id: "OAE-006", name: "Fisheries and Oceans Canada", country: "Canada",
    sector: "agence_gouvernementale", s1: 0.30, s2: 0.28, s3: 0.32, s4: 0.25 },
  // OAE-007 — faible — Allemagne
  // composite = 0.12*30 + 0.10*25 + 0.14*25 + 0.10*20 = 3.6+2.5+3.5+2 = 11.6
  { id: "OAE-007", name: "GEOMAR Helmholtz Centre Ocean Research", country: "Allemagne",
    sector: "recherche_marine", s1: 0.12, s2: 0.10, s3: 0.14, s4: 0.10 },
  // OAE-008 — faible — Bresil
  // composite = 0.10*30 + 0.12*25 + 0.08*25 + 0.14*20 = 3+3+2+2.8 = 10.8
  { id: "OAE-008", name: "Instituto Oceanografico USP", country: "Brésil",
    sector: "recherche_universitaire", s1: 0.10, s2: 0.12, s3: 0.08, s4: 0.14 },
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
  if (raw.s1 >= 0.85 && raw.s2 >= 0.80) return "coral_reef_mass_extinction";
  if (raw.s3 >= 0.85 && raw.s4 >= 0.80) return "fishery_ecosystem_collapse";
  if (raw.s4 >= 0.80 && raw.s2 >= 0.75) return "carbon_sink_failure";
  if (raw.s2 >= 0.75 && raw.s3 >= 0.70) return "shellfish_industry_extinction";
  if (raw.s3 >= 0.70 && raw.s1 >= 0.65) return "marine_biodiversity_crisis";
  return "none";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_ecosystemes_marins_critiques";
  if (risk === "eleve") return "restauration_marine_acceleree";
  if (risk === "modere") return "renforcement_protection_milieux_marins";
  return "veille_acidification_oceanique_continue";
}

function keySignals(risk: string, pattern: string, comp: number): string {
  const labels: Record<string, string> = {
    coral_reef_mass_extinction:    "Extinction massive recifs coralliens",
    fishery_ecosystem_collapse:    "Effondrement ecosysteme halieutique",
    carbon_sink_failure:           "Defaillance puits carbone oceanique",
    shellfish_industry_extinction: "Extinction industrie coquillages",
    marine_biodiversity_crisis:    "Crise biodiversite marine systemique",
    none:                          "Acidification controlee",
  };
  const label = labels[pattern] ?? pattern;
  if (risk === "critique") return `Crise acidification oceanique systemique — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "eleve") return `Crise acidification oceanique majeure — ${label} — composite ${comp.toFixed(1)}`;
  if (risk === "modere") return `Acidification oceanique structurelle — ${label} — composite ${comp.toFixed(1)}`;
  return `Ecosystemes marins sous surveillance — composite ${comp.toFixed(1)}`;
}

function getMockData() {
  const entities: OAEEntity[] = MOCK_ENTITIES_RAW.map(raw => {
    const { s1, s2, s3, s4, comp } = calcScores(raw);
    const risk = riskLevel(comp);
    const pat = primaryPattern(raw);
    return {
      id:                     raw.id,
      name:                          raw.name,
      country:                       raw.country,
      sector:                        raw.sector,
      score1:                        s1,
      score2:                        s2,
      score3:                        s3,
      score4:                        s4,
      composite_score:               comp,
      risk_level:                    risk,
      primary_pattern:               pat,
      key_signals:                   keySignals(risk, pat, comp),
      recommended_action:            recommendedAction(risk),
      estimated_acidification_index: Math.round(comp / 100 * 10 * 100) / 100,
      last_updated:                  new Date().toISOString(),
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
    totalIdx += e.estimated_acidification_index;
    if (e.risk_level === "critique") {
      top_risk_entities.push({ id: e.entity_id, name: e.name, composite_score: e.composite_score });
      critical_alerts.push(e.key_signals);
    }
  }

  const n = entities.length;
  const avg_composite = Math.round(totalComp / n * 100) / 100;
  const avg_estimated_acidification_index = Math.round(totalIdx / n * 100) / 100;

  return {
    total_entities:                    n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis:                     new Date().toISOString(),
    engine_version:                    "372.2.0",
    domain:                            "acidification",
    confidence_score:                  0.92,
    data_sources:                      ["IFREMER", "NOAA", "AIMS", "IMR", "JAMSTEC", "DFO-Canada", "GEOMAR", "IO-USP"],
    entities,
    avg_estimated_acidification_index,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Ocean Acidification Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ocean-acidification-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Ocean Acidification Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Ocean Acidification Agent"), { status: 502 }));
  }
}
