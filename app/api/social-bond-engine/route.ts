import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-bond-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Social Bond Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social-bond-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Social Bond Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Social Bond Agent"), { status: 502 });
  }
}

// ── Mock data (mirrors Python engine exactly) ─────────────────────────────────

function getMockData() {
  const entities: EntityDict[] = [
    // BON-001 — critique — social_washing (imd<70, gr=78>=70)
    // composite: 55*0.30 + 78*0.25 + 65*0.25 + 68*0.20 = 16.5+19.5+16.25+13.6 = 65.85
    {
      entity_id: "BON-001",
      name: "Obligation Sociale SNCF 2025",
      country: "France",
      sector: "Infrastructure",
      composite_score: 65.85,
      impact_measurement_deficit_score: 55.0,
      greenwashing_risk_score: 78.0,
      investor_trust_erosion_score: 65.0,
      regulatory_compliance_gap_score: 68.0,
      risk_level: "critique",
      primary_pattern: "social_washing",
      key_signals: [
        "Pratiques de social washing détectées — Obligation Sociale SNCF 2025",
        "Indice composite obligation sociale: 65.85/100 (critique)",
        "Certification tierce partie et transparence totale des données d'impact",
      ],
      estimated_bond_index: 6.59,
      last_updated: "2026-06-20",
      confidence_level: 0.84,
    },
    // BON-002 — critique — impact_fraud (imd=75>=70)
    // composite: 75*0.30 + 62*0.25 + 60*0.25 + 58*0.20 = 22.5+15.5+15+11.6 = 64.60
    {
      entity_id: "BON-002",
      name: "UK Social Housing Bond",
      country: "UK",
      sector: "Real Estate",
      composite_score: 64.6,
      impact_measurement_deficit_score: 75.0,
      greenwashing_risk_score: 62.0,
      investor_trust_erosion_score: 60.0,
      regulatory_compliance_gap_score: 58.0,
      risk_level: "critique",
      primary_pattern: "impact_fraud",
      key_signals: [
        "Déficit critique de mesure d'impact social réel — UK Social Housing Bond",
        "Indice composite obligation sociale: 64.6/100 (critique)",
        "Audit d'impact indépendant et restructuration des métriques ESG",
      ],
      estimated_bond_index: 6.46,
      last_updated: "2026-06-20",
      confidence_level: 0.80,
    },
    // BON-003 — critique — regulatory_breach (imd<70,gr<70,ite<70,rcg=72>=70)
    // composite: 55*0.30 + 58*0.25 + 62*0.25 + 72*0.20 = 16.5+14.5+15.5+14.4 = 60.90
    {
      entity_id: "BON-003",
      name: "Bundesanleihe Social Bond",
      country: "Germany",
      sector: "Government",
      composite_score: 60.9,
      impact_measurement_deficit_score: 55.0,
      greenwashing_risk_score: 58.0,
      investor_trust_erosion_score: 62.0,
      regulatory_compliance_gap_score: 72.0,
      risk_level: "critique",
      primary_pattern: "regulatory_breach",
      key_signals: [
        "Non-conformité réglementaire obligations sociales — Bundesanleihe Social Bond",
        "Indice composite obligation sociale: 60.9/100 (critique)",
        "Mise en conformité urgente SFDR et taxonomie UE",
      ],
      estimated_bond_index: 6.09,
      last_updated: "2026-06-20",
      confidence_level: 0.76,
    },
    // BON-004 — élevé — investor_confidence_collapse (imd<70,gr<70,ite=72>=70)
    // composite: 48*0.30 + 52*0.25 + 72*0.25 + 38*0.20 = 14.4+13+18+7.6 = 53.00
    {
      entity_id: "BON-004",
      name: "ABN AMRO ESG Bond",
      country: "Netherlands",
      sector: "Finance",
      composite_score: 53.0,
      impact_measurement_deficit_score: 48.0,
      greenwashing_risk_score: 52.0,
      investor_trust_erosion_score: 72.0,
      regulatory_compliance_gap_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "investor_confidence_collapse",
      key_signals: [
        "Érosion sévère de la confiance des investisseurs — ABN AMRO ESG Bond",
        "Indice composite obligation sociale: 53.0/100 (élevé)",
        "Communication de crise et plan de restauration de la confiance",
      ],
      estimated_bond_index: 5.3,
      last_updated: "2026-06-20",
      confidence_level: 0.79,
    },
    // BON-005 — élevé — bond_performing (no sub-score >= 70)
    // composite: 60*0.30 + 42*0.25 + 38*0.25 + 36*0.20 = 18+10.5+9.5+7.2 = 45.20
    {
      entity_id: "BON-005",
      name: "BNP Paribas Social Bond",
      country: "Belgium",
      sector: "Finance",
      composite_score: 45.2,
      impact_measurement_deficit_score: 60.0,
      greenwashing_risk_score: 42.0,
      investor_trust_erosion_score: 38.0,
      regulatory_compliance_gap_score: 36.0,
      risk_level: "élevé",
      primary_pattern: "bond_performing",
      key_signals: [
        "Obligation sociale à impact conforme aux objectifs — BNP Paribas Social Bond",
        "Indice composite obligation sociale: 45.2/100 (élevé)",
        "Maintien des standards et extension des programmes d'impact",
      ],
      estimated_bond_index: 4.52,
      last_updated: "2026-06-20",
      confidence_level: 0.77,
    },
    // BON-006 — modéré — bond_performing
    // composite: 32*0.30 + 28*0.25 + 26*0.25 + 22*0.20 = 9.6+7+6.5+4.4 = 27.50
    {
      entity_id: "BON-006",
      name: "Nordic Green Social Bond",
      country: "Sweden",
      sector: "Environment",
      composite_score: 27.5,
      impact_measurement_deficit_score: 32.0,
      greenwashing_risk_score: 28.0,
      investor_trust_erosion_score: 26.0,
      regulatory_compliance_gap_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "bond_performing",
      key_signals: [
        "Obligation sociale à impact conforme aux objectifs — Nordic Green Social Bond",
        "Indice composite obligation sociale: 27.5/100 (modéré)",
        "Maintien des standards et extension des programmes d'impact",
      ],
      estimated_bond_index: 2.75,
      last_updated: "2026-06-20",
      confidence_level: 0.82,
    },
    // BON-007 — faible — bond_performing
    // composite: 12*0.30 + 10*0.25 + 14*0.25 + 8*0.20 = 3.6+2.5+3.5+1.6 = 11.20
    {
      entity_id: "BON-007",
      name: "UBS Impact Bond",
      country: "Switzerland",
      sector: "Finance",
      composite_score: 11.2,
      impact_measurement_deficit_score: 12.0,
      greenwashing_risk_score: 10.0,
      investor_trust_erosion_score: 14.0,
      regulatory_compliance_gap_score: 8.0,
      risk_level: "faible",
      primary_pattern: "bond_performing",
      key_signals: [
        "Obligation sociale à impact conforme aux objectifs — UBS Impact Bond",
        "Indice composite obligation sociale: 11.2/100 (faible)",
        "Maintien des standards et extension des programmes d'impact",
      ],
      estimated_bond_index: 1.12,
      last_updated: "2026-06-20",
      confidence_level: 0.91,
    },
    // BON-008 — faible — bond_performing
    // composite: 8*0.30 + 6*0.25 + 10*0.25 + 5*0.20 = 2.4+1.5+2.5+1.0 = 7.40
    {
      entity_id: "BON-008",
      name: "European Investment Bank Social Bond",
      country: "Luxembourg",
      sector: "Finance",
      composite_score: 7.4,
      impact_measurement_deficit_score: 8.0,
      greenwashing_risk_score: 6.0,
      investor_trust_erosion_score: 10.0,
      regulatory_compliance_gap_score: 5.0,
      risk_level: "faible",
      primary_pattern: "bond_performing",
      key_signals: [
        "Obligation sociale à impact conforme aux objectifs — European Investment Bank Social Bond",
        "Indice composite obligation sociale: 7.4/100 (faible)",
        "Maintien des standards et extension des programmes d'impact",
      ],
      estimated_bond_index: 0.74,
      last_updated: "2026-06-20",
      confidence_level: 0.94,
    },
  ];

  // avg_composite = (65.85+64.6+60.9+53.0+45.2+27.5+11.2+7.4) / 8 = 335.65 / 8 = 41.96
  const avg_composite = 41.96;
  // avg_confidence = (0.84+0.80+0.76+0.79+0.77+0.82+0.91+0.94) / 8 = 6.63 / 8 = 0.83
  const confidence_score = 0.83;

  return {
    total_entities: entities.length,
    avg_composite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      impact_fraud: 1,
      social_washing: 1,
      investor_confidence_collapse: 1,
      regulatory_breach: 1,
      bond_performing: 4,
    },
    top_risk_entities: [
      "Obligation Sociale SNCF 2025",
      "UK Social Housing Bond",
      "Bundesanleihe Social Bond",
    ],
    critical_alerts: [
      "Obligation Sociale SNCF 2025",
      "UK Social Housing Bond",
      "Bundesanleihe Social Bond",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "bond",
    confidence_score,
    data_sources: [
      "ICMA Social Bond Principles",
      "EU Social Taxonomy Reports",
      "Bloomberg ESG Data",
    ],
    entities,
    avg_estimated_bond_index: 4.2,
  } satisfies SummaryDict;
}

// ── Types ─────────────────────────────────────────────────────────────────────

interface EntityDict {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  impact_measurement_deficit_score: number;
  greenwashing_risk_score: number;
  investor_trust_erosion_score: number;
  regulatory_compliance_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_bond_index: number;
  last_updated: string;
  confidence_level: number;
}

interface SummaryDict {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: EntityDict[];
  avg_estimated_bond_index: number;
}
