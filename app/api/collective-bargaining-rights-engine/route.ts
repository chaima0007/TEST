import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[collective-bargaining-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[collective-bargaining-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Collective Bargaining Rights Engine Agent",
  domain: "collective_bargaining_rights",
  total_entities: 8,
  avg_composite: 60.06,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — Syndicats Indépendants Bannis, ACFTU Contrôlé État & Militants Arrêtés Systématiquement",
    "Arabie Saoudite — Syndicats Totalement Interdits, Kafala System & Travailleurs Migrants Sans Droits",
    "Bangladesh — Zones Export Syndicats Réprimés Violemment, Meurtres Organisateurs & Usines Rana Plaza",
  ],
  critical_alerts: [
    "Chine: union_suppression_score",
    "Arabie Saoudite: union_suppression_score",
    "Bangladesh: worker_representative_persecution_score",
    "Pakistan: worker_representative_persecution_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_collective_bargaining_rights_index: 6.01,
  entities: [
    {
      entity_id: "CBR-001",
      name: "Chine — Syndicats Indépendants Bannis, ACFTU Contrôlé État & Militants Arrêtés Systématiquement",
      country: "Chine",
      union_suppression_score: 91.0,
      strike_criminalization_score: 89.0,
      collective_agreement_refusal_score: 88.0,
      worker_representative_persecution_score: 90.0,
      composite_score: 89.55,
      risk_level: "critique",
      primary_pattern: "union_suppression_score",
      estimated_collective_bargaining_rights_index: 8.96,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CBR-002",
      name: "Arabie Saoudite — Syndicats Totalement Interdits, Kafala System & Travailleurs Migrants Sans Droits",
      country: "Arabie Saoudite",
      union_suppression_score: 90.0,
      strike_criminalization_score: 88.0,
      collective_agreement_refusal_score: 87.0,
      worker_representative_persecution_score: 89.0,
      composite_score: 88.55,
      risk_level: "critique",
      primary_pattern: "union_suppression_score",
      estimated_collective_bargaining_rights_index: 8.86,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CBR-003",
      name: "Bangladesh — Zones Export Syndicats Réprimés Violemment, Meurtres Organisateurs & Usines Rana Plaza",
      country: "Bangladesh",
      union_suppression_score: 85.0,
      strike_criminalization_score: 84.0,
      collective_agreement_refusal_score: 82.0,
      worker_representative_persecution_score: 86.0,
      composite_score: 84.2,
      risk_level: "critique",
      primary_pattern: "worker_representative_persecution_score",
      estimated_collective_bargaining_rights_index: 8.42,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CBR-004",
      name: "Pakistan — Syndicats Persécutés Zones Franches, Lois Anti-Grève & Représailles Patronales Impunies",
      country: "Pakistan",
      union_suppression_score: 82.0,
      strike_criminalization_score: 81.0,
      collective_agreement_refusal_score: 80.0,
      worker_representative_persecution_score: 83.0,
      composite_score: 81.45,
      risk_level: "critique",
      primary_pattern: "worker_representative_persecution_score",
      estimated_collective_bargaining_rights_index: 8.15,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CBR-005",
      name: "Cambodge — Dissolution Syndicats Garment Workers, Loi Syndicats 2016 Restrictive & Meurtres Impunis",
      country: "Cambodge",
      union_suppression_score: 54.0,
      strike_criminalization_score: 52.0,
      collective_agreement_refusal_score: 50.0,
      worker_representative_persecution_score: 55.0,
      composite_score: 52.7,
      risk_level: "élevé",
      primary_pattern: "worker_representative_persecution_score",
      estimated_collective_bargaining_rights_index: 5.27,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CBR-006",
      name: "Colombie — 150+ Syndicalistes Assassinés/An Historique, Impunité 97% & Paramilitaires Anti-Syndicaux",
      country: "Colombie",
      union_suppression_score: 46.0,
      strike_criminalization_score: 44.0,
      collective_agreement_refusal_score: 43.0,
      worker_representative_persecution_score: 48.0,
      composite_score: 45.15,
      risk_level: "élevé",
      primary_pattern: "worker_representative_persecution_score",
      estimated_collective_bargaining_rights_index: 4.52,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CBR-007",
      name: "USA — Taft-Hartley Restrictions, Amazon & Starbucks Union-Busting & Droit de Grève Limité",
      country: "USA",
      union_suppression_score: 30.0,
      strike_criminalization_score: 29.0,
      collective_agreement_refusal_score: 31.0,
      worker_representative_persecution_score: 28.0,
      composite_score: 29.6,
      risk_level: "modéré",
      primary_pattern: "collective_agreement_refusal_score",
      estimated_collective_bargaining_rights_index: 2.96,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CBR-008",
      name: "Danemark — Syndicalisation 67%, Négociation Collective Référence Nordique & Grèves Légales Protégées",
      country: "Danemark",
      union_suppression_score: 10.0,
      strike_criminalization_score: 9.0,
      collective_agreement_refusal_score: 8.0,
      worker_representative_persecution_score: 10.0,
      composite_score: 9.25,
      risk_level: "faible",
      primary_pattern: "union_suppression_score",
      estimated_collective_bargaining_rights_index: 0.93,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/collective-bargaining-rights-engine`, {
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
