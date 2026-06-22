import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-be-forgotten-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-be-forgotten-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Right To Be Forgotten Rights Engine Agent",
  domain: "right_to_be_forgotten_rights",
  total_entities: 8,
  avg_composite: 59.92,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — Surveillance permanente, aucun droit à l'effacement des données",
    "Russie — Rétention forcée données dissidents, dossiers FSB perpétuels",
    "Corée du Nord — Archives d'État totalitaires, effacement impossible",
  ],
  critical_alerts: [
    "Chine: State surveillance apparatus with zero data erasure rights",
    "Russie: FSB perpetual data retention & dissident profiling",
    "Corée du Nord: Totalitarian state archives with permanent citizen records",
    "Inde: Aadhaar biometric database without robust erasure mechanisms",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_be_forgotten_rights_index: 5.99,
  entities: [
    {
      entity_id: "RBF-001",
      name: "Chine — Surveillance permanente, aucun droit à l&apos;effacement",
      country: "Chine",
      data_erasure_denial_score: 98.0,
      surveillance_data_retention_score: 97.0,
      digital_reputation_harm_score: 95.0,
      platform_compliance_gap_score: 96.0,
      composite_score: 96.7,
      risk_level: "critique",
      primary_pattern: "State surveillance apparatus with zero data erasure rights",
      estimated_right_to_be_forgotten_rights_index: 9.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RBF-002",
      name: "Russie — Rétention forcée données dissidents, dossiers FSB perpétuels",
      country: "Russie",
      data_erasure_denial_score: 88.0,
      surveillance_data_retention_score: 92.0,
      digital_reputation_harm_score: 85.0,
      platform_compliance_gap_score: 87.0,
      composite_score: 88.0,
      risk_level: "critique",
      primary_pattern: "FSB perpetual data retention & dissident profiling",
      estimated_right_to_be_forgotten_rights_index: 8.80,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RBF-003",
      name: "Corée du Nord — Archives d&apos;État totalitaires, effacement impossible",
      country: "Corée du Nord",
      data_erasure_denial_score: 95.0,
      surveillance_data_retention_score: 94.0,
      digital_reputation_harm_score: 90.0,
      platform_compliance_gap_score: 93.0,
      composite_score: 93.25,
      risk_level: "critique",
      primary_pattern: "Totalitarian state archives with permanent citizen records",
      estimated_right_to_be_forgotten_rights_index: 9.33,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RBF-004",
      name: "Inde — Aadhaar biométrique sans mécanisme d&apos;effacement robuste",
      country: "Inde",
      data_erasure_denial_score: 68.0,
      surveillance_data_retention_score: 72.0,
      digital_reputation_harm_score: 65.0,
      platform_compliance_gap_score: 70.0,
      composite_score: 68.9,
      risk_level: "critique",
      primary_pattern: "Aadhaar biometric database without robust erasure mechanisms",
      estimated_right_to_be_forgotten_rights_index: 6.89,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RBF-005",
      name: "USA — Absence loi fédérale RTBF, patchwork étatique",
      country: "États-Unis",
      data_erasure_denial_score: 52.0,
      surveillance_data_retention_score: 55.0,
      digital_reputation_harm_score: 48.0,
      platform_compliance_gap_score: 50.0,
      composite_score: 51.35,
      risk_level: "élevé",
      primary_pattern: "No federal RTBF law, state-level patchwork only",
      estimated_right_to_be_forgotten_rights_index: 5.14,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RBF-006",
      name: "Brésil — LGPD partielle, lacunes enforcement plateformes",
      country: "Brésil",
      data_erasure_denial_score: 44.0,
      surveillance_data_retention_score: 46.0,
      digital_reputation_harm_score: 42.0,
      platform_compliance_gap_score: 48.0,
      composite_score: 44.7,
      risk_level: "élevé",
      primary_pattern: "LGPD partial enforcement & platform compliance gaps",
      estimated_right_to_be_forgotten_rights_index: 4.47,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RBF-007",
      name: "Canada — LPRPDE, délais effacement lents, lacunes sectorielles",
      country: "Canada",
      data_erasure_denial_score: 28.0,
      surveillance_data_retention_score: 30.0,
      digital_reputation_harm_score: 26.0,
      platform_compliance_gap_score: 32.0,
      composite_score: 28.9,
      risk_level: "modéré",
      primary_pattern: "PIPEDA framework with slow erasure timelines & sectoral gaps",
      estimated_right_to_be_forgotten_rights_index: 2.89,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RBF-008",
      name: "UE — RGPD article 17, cadre RTBF le plus avancé au monde",
      country: "Union Européenne",
      data_erasure_denial_score: 10.0,
      surveillance_data_retention_score: 12.0,
      digital_reputation_harm_score: 9.0,
      platform_compliance_gap_score: 14.0,
      composite_score: 11.15,
      risk_level: "faible",
      primary_pattern: "GDPR Article 17 RTBF — most advanced erasure rights framework",
      estimated_right_to_be_forgotten_rights_index: 1.12,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-be-forgotten-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
