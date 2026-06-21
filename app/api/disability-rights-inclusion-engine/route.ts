import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Disability Rights Inclusion Engine Agent",
  domain: "disability_rights_inclusion",
  total_entities: 8,
  avg_composite: 62.36,
  confidence_score: 0.89,
  avg_estimated_disability_rights_inclusion_index: 6.24,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_crpd_committee_reports_2023",
    "human_rights_watch_disability_rights_2022",
    "disability_rights_international_2023",
    "who_world_report_on_disability_2023",
  ],
  critical_alerts: [],
  entities: [
    {
      entity_id: "AF-001",
      name: "Afghanistan — Taliban Disability Rights Rollback",
      composite_score: 89.1,
      risk_level: "critique",
      estimated_disability_rights_inclusion_index: 8.91,
    },
    {
      entity_id: "YE-002",
      name: "Yémen — Conflit & Handicap de Guerre",
      composite_score: 88.4,
      risk_level: "critique",
      estimated_disability_rights_inclusion_index: 8.84,
    },
    {
      entity_id: "ET-003",
      name: "Éthiopie — Déficit Structurel & Conflit Tigré",
      composite_score: 81.6,
      risk_level: "critique",
      estimated_disability_rights_inclusion_index: 8.16,
    },
    {
      entity_id: "SD-004",
      name: "Soudan — Guerre Civile & Populations Vulnérables",
      composite_score: 85.15,
      risk_level: "critique",
      estimated_disability_rights_inclusion_index: 8.52,
    },
    {
      entity_id: "MM-005",
      name: "Myanmar — Coup & Disability Policy Collapse",
      composite_score: 56.65,
      risk_level: "élevé",
      estimated_disability_rights_inclusion_index: 5.67,
    },
    {
      entity_id: "IN-R-006",
      name: "Inde Rurale — Lacunes RPWD & Exclusion",
      composite_score: 53.75,
      risk_level: "élevé",
      estimated_disability_rights_inclusion_index: 5.38,
    },
    {
      entity_id: "BR-007",
      name: "Brésil — Progrès Législatif, Exclusion Persistante",
      composite_score: 31.6,
      risk_level: "modéré",
      estimated_disability_rights_inclusion_index: 3.16,
    },
    {
      entity_id: "NL-008",
      name: "Pays-Bas — Modèle CDPH avec Lacunes Résiduelles",
      composite_score: 12.6,
      risk_level: "faible",
      estimated_disability_rights_inclusion_index: 1.26,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[disability-rights-inclusion-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-inclusion-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
