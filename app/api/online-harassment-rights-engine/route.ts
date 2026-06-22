import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[online-harassment-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[online-harassment-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Online Harassment Rights Engine Agent",
  domain: "online_harassment_rights",
  total_entities: 8,
  avg_composite: 60.07,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Inde — 58% femmes harcelées ligne, revenge porn 20 000 cas/an, IT Act insuffisant",
    "Pakistan — Cyberviolence féministes, blasphème utilisé comme harcèlement, PECA loi abusive",
    "Brésil — LeakNude sites, 88% femmes harcelées politiques ligne, Marielle Franco doxxing",
  ],
  critical_alerts: [
    "Inde: cyber_gender_violence",
    "Pakistan: legal_protection_gap",
    "Brésil: doxxing_impunity",
    "Philippines: platform_inaction",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_online_harassment_rights_index: 6.01,
  entities: [
    {
      entity_id: "OHR-001",
      name: "Inde — 58% femmes harcelées ligne, revenge porn 20 000 cas/an, IT Act insuffisant",
      country: "Inde",
      cyber_gender_violence_score: 96.0,
      doxxing_impunity_score: 94.0,
      platform_inaction_score: 95.0,
      legal_protection_gap_score: 93.0,
      composite_score: 94.65,
      risk_level: "critique",
      primary_pattern: "cyber_gender_violence",
      estimated_online_harassment_rights_index: 9.47,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-002",
      name: "Pakistan — Cyberviolence féministes, blasphème utilisé comme harcèlement, PECA loi abusive",
      country: "Pakistan",
      cyber_gender_violence_score: 90.0,
      doxxing_impunity_score: 92.0,
      platform_inaction_score: 89.0,
      legal_protection_gap_score: 91.0,
      composite_score: 90.45,
      risk_level: "critique",
      primary_pattern: "legal_protection_gap",
      estimated_online_harassment_rights_index: 9.05,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-003",
      name: "Brésil — LeakNude sites, 88% femmes harcelées politiques ligne, Marielle Franco doxxing",
      country: "Brésil",
      cyber_gender_violence_score: 84.0,
      doxxing_impunity_score: 86.0,
      platform_inaction_score: 83.0,
      legal_protection_gap_score: 82.0,
      composite_score: 83.85,
      risk_level: "critique",
      primary_pattern: "doxxing_impunity",
      estimated_online_harassment_rights_index: 8.39,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-004",
      name: "Philippines — 72% journalistes femmes quittent réseaux, trolls armée Duterte, Maria Ressa",
      country: "Philippines",
      cyber_gender_violence_score: 76.0,
      doxxing_impunity_score: 78.0,
      platform_inaction_score: 80.0,
      legal_protection_gap_score: 74.0,
      composite_score: 77.1,
      risk_level: "critique",
      primary_pattern: "platform_inaction",
      estimated_online_harassment_rights_index: 7.71,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-005",
      name: "USA — 41% adultes harcelés ligne, revenge porn lois 48 États seulement, Twitter/X modération zéro",
      country: "USA",
      cyber_gender_violence_score: 54.0,
      doxxing_impunity_score: 56.0,
      platform_inaction_score: 58.0,
      legal_protection_gap_score: 52.0,
      composite_score: 55.1,
      risk_level: "élevé",
      primary_pattern: "platform_inaction",
      estimated_online_harassment_rights_index: 5.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-006",
      name: "UK — Online Safety Act 2023 tardif, 46% femmes harcelées, deepfakes non-criminalisés avant 2024",
      country: "UK",
      cyber_gender_violence_score: 44.0,
      doxxing_impunity_score: 42.0,
      platform_inaction_score: 46.0,
      legal_protection_gap_score: 48.0,
      composite_score: 44.8,
      risk_level: "élevé",
      primary_pattern: "platform_inaction",
      estimated_online_harassment_rights_index: 4.48,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-007",
      name: "France — Loi Avia partiellement censurée, cyberviolence femmes +30%, PHAROS insuffisant",
      country: "France",
      cyber_gender_violence_score: 28.0,
      doxxing_impunity_score: 26.0,
      platform_inaction_score: 30.0,
      legal_protection_gap_score: 24.0,
      composite_score: 27.2,
      risk_level: "modéré",
      primary_pattern: "cyber_gender_violence",
      estimated_online_harassment_rights_index: 2.72,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-008",
      name: "Allemagne/Finlande — NetzDG effectif, formations modération, sanctions plateformes réelles",
      country: "Allemagne/Finlande",
      cyber_gender_violence_score: 7.0,
      doxxing_impunity_score: 8.0,
      platform_inaction_score: 6.0,
      legal_protection_gap_score: 9.0,
      composite_score: 7.4,
      risk_level: "faible",
      primary_pattern: "legal_protection_gap",
      estimated_online_harassment_rights_index: 0.74,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/online-harassment-rights-engine`, {
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
