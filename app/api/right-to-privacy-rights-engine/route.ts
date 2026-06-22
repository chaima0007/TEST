import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-privacy-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Right To Privacy Rights Engine Agent",
  domain: "right_to_privacy_rights",
  total_entities: 8,
  avg_composite: 60.59,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — NSA chinoise, surveillance totale 1.4Md, SCS notation comportementale",
    "Russie — SORM-3, Yarovaya retention totale, FSB accès direct serveurs",
    "Iran — Deep packet inspection, Pegasus dissidents, VPN 80% population",
  ],
  critical_alerts: [
    "Chine: mass_surveillance",
    "Russie: communication_interception",
    "Iran: communication_interception",
    "USA pré-2024: privacy_law_absence",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_privacy_rights_index: 6.06,
  entities: [
    {
      entity_id: "RTP-001",
      name: "Chine — NSA chinoise, surveillance totale 1.4Md, SCS notation comportementale",
      country: "Chine",
      mass_surveillance_score: 97.0,
      data_collection_without_consent_score: 96.0,
      communication_interception_score: 95.0,
      privacy_law_absence_score: 94.0,
      composite_score: 95.65,
      risk_level: "critique",
      primary_pattern: "mass_surveillance",
      estimated_right_to_privacy_rights_index: 9.57,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTP-002",
      name: "Russie — SORM-3, Yarovaya retention totale, FSB accès direct serveurs",
      country: "Russie",
      mass_surveillance_score: 91.0,
      data_collection_without_consent_score: 89.0,
      communication_interception_score: 93.0,
      privacy_law_absence_score: 88.0,
      composite_score: 90.4,
      risk_level: "critique",
      primary_pattern: "communication_interception",
      estimated_right_to_privacy_rights_index: 9.04,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTP-003",
      name: "Iran — Deep packet inspection, Pegasus dissidents, VPN 80% population",
      country: "Iran",
      mass_surveillance_score: 85.0,
      data_collection_without_consent_score: 83.0,
      communication_interception_score: 87.0,
      privacy_law_absence_score: 82.0,
      composite_score: 84.4,
      risk_level: "critique",
      primary_pattern: "communication_interception",
      estimated_right_to_privacy_rights_index: 8.44,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTP-004",
      name: "USA pré-2024 — NSA PRISM Snowden, FISA 702, bulk metadata collection",
      country: "USA",
      mass_surveillance_score: 76.0,
      data_collection_without_consent_score: 78.0,
      communication_interception_score: 74.0,
      privacy_law_absence_score: 80.0,
      composite_score: 76.8,
      risk_level: "critique",
      primary_pattern: "privacy_law_absence",
      estimated_right_to_privacy_rights_index: 7.68,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTP-005",
      name: "Israël — NSO Group Pegasus exporté 45 pays, journalistes/activistes ciblés",
      country: "Israël",
      mass_surveillance_score: 54.0,
      data_collection_without_consent_score: 56.0,
      communication_interception_score: 58.0,
      privacy_law_absence_score: 52.0,
      composite_score: 55.1,
      risk_level: "élevé",
      primary_pattern: "communication_interception",
      estimated_right_to_privacy_rights_index: 5.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTP-006",
      name: "Inde — UAPA wiretapping sans mandat, Pegasus politiciens/journalistes, PDPB retardé",
      country: "Inde",
      mass_surveillance_score: 46.0,
      data_collection_without_consent_score: 48.0,
      communication_interception_score: 50.0,
      privacy_law_absence_score: 44.0,
      composite_score: 47.1,
      risk_level: "élevé",
      primary_pattern: "data_collection_without_consent",
      estimated_right_to_privacy_rights_index: 4.71,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTP-007",
      name: "UK — GCHQ Tempora, Investigatory Powers Act 2016, bulk surveillance légalisée",
      country: "UK",
      mass_surveillance_score: 28.0,
      data_collection_without_consent_score: 30.0,
      communication_interception_score: 32.0,
      privacy_law_absence_score: 24.0,
      composite_score: 28.7,
      risk_level: "modéré",
      primary_pattern: "mass_surveillance",
      estimated_right_to_privacy_rights_index: 2.87,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTP-008",
      name: "UE/Allemagne — RGPD + Cour Constitutionnelle, Schrems II, BND réformé",
      country: "UE/Allemagne",
      mass_surveillance_score: 7.0,
      data_collection_without_consent_score: 6.0,
      communication_interception_score: 8.0,
      privacy_law_absence_score: 5.0,
      composite_score: 6.6,
      risk_level: "faible",
      primary_pattern: "privacy_law_absence",
      estimated_right_to_privacy_rights_index: 0.66,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-privacy-rights-engine`, {
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
