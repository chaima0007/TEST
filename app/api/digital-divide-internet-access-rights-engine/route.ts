import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Digital Divide Internet Access Rights Engine Agent",
  domain: "digital_divide_internet_access_rights",
  total_entities: 8,
  avg_composite: 62.76,
  confidence_score: 0.90,
  avg_estimated_digital_divide_internet_access_index: 6.28,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "itu_digital_development_report_2023",
    "freedom_house_freedom_on_the_net_2023",
    "a4ai_affordability_report_2023",
    "article19_internet_shutdowns_tracker_2023",
  ],
  critical_alerts: [],
  entities: [
    {
      id: "DD-001",
      name: "Corée du Nord — Intranet-Only Population",
      composite_score: 93.85,
      risk_level: "critique",
      estimated_digital_divide_internet_access_index: 9.38,
    },
    {
      id: "DD-002",
      name: "Érythrée — Blackout Numérique Structurel",
      composite_score: 89.75,
      risk_level: "critique",
      estimated_digital_divide_internet_access_index: 8.97,
    },
    {
      id: "DD-003",
      name: "Turkménistan — Contrôle Internet Totalitaire",
      composite_score: 83.95,
      risk_level: "critique",
      estimated_digital_divide_internet_access_index: 8.39,
    },
    {
      id: "DD-004",
      name: "Myanmar — Shutdowns Post-Coup & Rural Exclusion",
      composite_score: 79.15,
      risk_level: "critique",
      estimated_digital_divide_internet_access_index: 7.92,
    },
    {
      id: "DD-005",
      name: "RDC Rurale — Fracture Numérique Structurelle",
      composite_score: 56.45,
      risk_level: "élevé",
      estimated_digital_divide_internet_access_index: 5.64,
    },
    {
      id: "DD-006",
      name: "Éthiopie — Guerre du Tigré & Coupures Réseau",
      composite_score: 54.75,
      risk_level: "élevé",
      estimated_digital_divide_internet_access_index: 5.47,
    },
    {
      id: "DD-007",
      name: "Cuba — Accès Contrôlé et Coûteux",
      composite_score: 30.25,
      risk_level: "modéré",
      estimated_digital_divide_internet_access_index: 3.02,
    },
    {
      id: "DD-008",
      name: "Afrique Sub-Saharienne Urbaine — Accès Croissant",
      composite_score: 13.9,
      risk_level: "faible",
      estimated_digital_divide_internet_access_index: 1.39,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[digital-divide-internet-access-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-divide-internet-access-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
