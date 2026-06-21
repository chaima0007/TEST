import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Sexual Violence Conflict Accountability Engine Agent",
  domain: "sexual_violence_conflict_accountability",
  total_entities: 8,
  avg_composite: 63.52,
  confidence_score: 0.91,
  avg_estimated_crsv_accountability_index: 6.35,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_security_council_res_1820_crsv_reports_2023",
    "human_rights_watch_sexual_violence_conflict_2023",
    "amnesty_international_crsv_accountability_2022",
    "icc_crsv_prosecution_database_2023",
  ],
  critical_alerts: [],
  entities: [
    {
      id: "SD-RSF-001",
      name: "Sudan / RSF — Darfur & Khartoum",
      composite_score: 92.55,
      risk_level: "critique",
      estimated_crsv_accountability_index: 9.25,
    },
    {
      id: "CD-M23-002",
      name: "DRC / M23 — Eastern Congo",
      composite_score: 89.65,
      risk_level: "critique",
      estimated_crsv_accountability_index: 8.96,
    },
    {
      id: "MM-003",
      name: "Myanmar — Military Junta (Tatmadaw)",
      composite_score: 87.65,
      risk_level: "critique",
      estimated_crsv_accountability_index: 8.77,
    },
    {
      id: "UA-RU-004",
      name: "Russia — Ukraine Conflict CRSV",
      composite_score: 81.7,
      risk_level: "critique",
      estimated_crsv_accountability_index: 8.17,
    },
    {
      id: "ML-005",
      name: "Mali — Sahel Armed Groups",
      composite_score: 53.65,
      risk_level: "élevé",
      estimated_crsv_accountability_index: 5.37,
    },
    {
      id: "HT-006",
      name: "Haiti — Gang Violence CRSV",
      composite_score: 54.2,
      risk_level: "élevé",
      estimated_crsv_accountability_index: 5.42,
    },
    {
      id: "CO-007",
      name: "Colombia — Post-Accord Accountability",
      composite_score: 34.85,
      risk_level: "modéré",
      estimated_crsv_accountability_index: 3.49,
    },
    {
      id: "RW-008",
      name: "Rwanda — Post-Genocide Reconciliation",
      composite_score: 13.9,
      risk_level: "faible",
      estimated_crsv_accountability_index: 1.39,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[sexual-violence-conflict-accountability-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sexual-violence-conflict-accountability-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
