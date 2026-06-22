import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[biometric-data-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[biometric-data-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Biometric Data Rights Engine Agent",
  domain: "biometric_data_rights",
  total_entities: 8,
  avg_composite: 60.09,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — Collecte biométrique de masse Ouïghours & Social Credit",
    "Russie — Reconnaissance faciale urbaine sans cadre consentement",
    "Inde — Aadhaar 1.4Md: fuites massives, absence recours",
  ],
  critical_alerts: [
    "Chine: Mass biometric collection targeting Uyghurs & social scoring",
    "Russie: Blanket facial recognition with no consent or oversight",
    "Inde: Aadhaar biometric leaks affecting 1.4 billion individuals",
    "Iran — Reconnaissance faciale hijab: surveillance corps femmes",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_biometric_data_rights_index: 6.01,
  entities: [
    {
      entity_id: "BDR-001",
      name: "Chine — Collecte biométrique de masse Ouïghours & Social Credit",
      country: "Chine",
      mass_biometric_collection_score: 99.0,
      facial_recognition_misuse_score: 97.0,
      biometric_database_leak_score: 88.0,
      consent_framework_gap_score: 99.0,
      composite_score: 96.0,
      risk_level: "critique",
      primary_pattern: "Mass biometric collection targeting Uyghurs & social scoring",
      estimated_biometric_data_rights_index: 9.6,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BDR-002",
      name: "Russie — Reconnaissance faciale urbaine sans cadre consentement",
      country: "Russie",
      mass_biometric_collection_score: 92.0,
      facial_recognition_misuse_score: 94.0,
      biometric_database_leak_score: 85.0,
      consent_framework_gap_score: 93.0,
      composite_score: 91.25,
      risk_level: "critique",
      primary_pattern: "Blanket facial recognition with no consent or oversight",
      estimated_biometric_data_rights_index: 9.13,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BDR-003",
      name: "Inde — Aadhaar 1.4Md: fuites massives, absence recours",
      country: "Inde",
      mass_biometric_collection_score: 85.0,
      facial_recognition_misuse_score: 78.0,
      biometric_database_leak_score: 90.0,
      consent_framework_gap_score: 82.0,
      composite_score: 83.75,
      risk_level: "critique",
      primary_pattern: "Aadhaar biometric leaks affecting 1.4 billion individuals",
      estimated_biometric_data_rights_index: 8.38,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BDR-004",
      name: "Iran — Reconnaissance faciale hijab: surveillance corps femmes",
      country: "Iran",
      mass_biometric_collection_score: 80.0,
      facial_recognition_misuse_score: 85.0,
      biometric_database_leak_score: 70.0,
      consent_framework_gap_score: 88.0,
      composite_score: 80.75,
      risk_level: "critique",
      primary_pattern: "Facial recognition deployed against women for hijab enforcement",
      estimated_biometric_data_rights_index: 8.08,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BDR-005",
      name: "États-Unis — Clearview AI, manque cadre fédéral biométrique",
      country: "États-Unis",
      mass_biometric_collection_score: 55.0,
      facial_recognition_misuse_score: 60.0,
      biometric_database_leak_score: 52.0,
      consent_framework_gap_score: 58.0,
      composite_score: 56.25,
      risk_level: "élevé",
      primary_pattern: "Clearview AI mass scraping & absence of federal biometric law",
      estimated_biometric_data_rights_index: 5.63,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BDR-006",
      name: "Royaume-Uni — Déploiement LFR police sans base légale claire",
      country: "Royaume-Uni",
      mass_biometric_collection_score: 48.0,
      facial_recognition_misuse_score: 52.0,
      biometric_database_leak_score: 40.0,
      consent_framework_gap_score: 46.0,
      composite_score: 46.7,
      risk_level: "élevé",
      primary_pattern: "Police live facial recognition without clear legal basis",
      estimated_biometric_data_rights_index: 4.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BDR-007",
      name: "Brésil — LGPD adoption, fuites bases données biométriques",
      country: "Brésil",
      mass_biometric_collection_score: 30.0,
      facial_recognition_misuse_score: 28.0,
      biometric_database_leak_score: 35.0,
      consent_framework_gap_score: 25.0,
      composite_score: 29.5,
      risk_level: "modéré",
      primary_pattern: "LGPD framework with ongoing biometric database breach incidents",
      estimated_biometric_data_rights_index: 2.95,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BDR-008",
      name: "UE — AI Act: interdiction reconnaissance faciale espaces publics",
      country: "Union Européenne",
      mass_biometric_collection_score: 10.0,
      facial_recognition_misuse_score: 8.0,
      biometric_database_leak_score: 12.0,
      consent_framework_gap_score: 6.0,
      composite_score: 9.1,
      risk_level: "faible",
      primary_pattern: "AI Act ban on public facial recognition, GDPR biometric protections",
      estimated_biometric_data_rights_index: 0.91,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/biometric-data-rights-engine`, {
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
