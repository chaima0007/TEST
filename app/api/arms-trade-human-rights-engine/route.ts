import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[arms-trade-human-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[arms-trade-human-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Arms Trade Human Rights Engine Agent",
  domain: "arms_trade_human_rights",
  total_entities: 8,
  avg_composite: 60.12,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Russie — Ventes d'armes à régimes autoritaires & violations DIH",
    "Arabie Saoudite — Bombardements Yémen, importations massives",
    "Chine — Exportations armes légères vers zones de conflit",
  ],
  critical_alerts: [
    "Russie: Transfers to sanctioned regimes & systematic IHL violations",
    "Arabie Saoudite: Yemen airstrikes & civilian harm from Western arms",
    "Chine: Small arms flows to conflict zones with no end-use controls",
    "États-Unis: Export control failures enabling atrocity crimes",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_arms_trade_human_rights_index: 6.01,
  entities: [
    {
      entity_id: "ATH-001",
      name: "Russie — Ventes d'armes à régimes autoritaires & violations DIH",
      country: "Russie",
      arms_to_abusers_score: 97.0,
      civilian_harm_arms_score: 95.0,
      export_control_failure_score: 93.0,
      accountability_impunity_score: 98.0,
      composite_score: 95.85,
      risk_level: "critique",
      primary_pattern: "Transfers to sanctioned regimes & systematic IHL violations",
      estimated_arms_trade_human_rights_index: 9.59,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ATH-002",
      name: "Arabie Saoudite — Bombardements Yémen, importations massives",
      country: "Arabie Saoudite",
      arms_to_abusers_score: 90.0,
      civilian_harm_arms_score: 92.0,
      export_control_failure_score: 84.0,
      accountability_impunity_score: 89.0,
      composite_score: 88.85,
      risk_level: "critique",
      primary_pattern: "Yemen airstrikes & civilian harm from Western arms",
      estimated_arms_trade_human_rights_index: 8.89,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ATH-003",
      name: "Chine — Exportations armes légères vers zones de conflit",
      country: "Chine",
      arms_to_abusers_score: 85.0,
      civilian_harm_arms_score: 78.0,
      export_control_failure_score: 88.0,
      accountability_impunity_score: 82.0,
      composite_score: 83.35,
      risk_level: "critique",
      primary_pattern: "Small arms flows to conflict zones with no end-use controls",
      estimated_arms_trade_human_rights_index: 8.34,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ATH-004",
      name: "États-Unis — Défaillances contrôle export, armes utilisées contre civils",
      country: "États-Unis",
      arms_to_abusers_score: 78.0,
      civilian_harm_arms_score: 75.0,
      export_control_failure_score: 80.0,
      accountability_impunity_score: 76.0,
      composite_score: 77.35,
      risk_level: "critique",
      primary_pattern: "Export control failures enabling atrocity crimes",
      estimated_arms_trade_human_rights_index: 7.74,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ATH-005",
      name: "France — Ventes controversées Égypte, EAU malgré violations",
      country: "France",
      arms_to_abusers_score: 55.0,
      civilian_harm_arms_score: 52.0,
      export_control_failure_score: 58.0,
      accountability_impunity_score: 50.0,
      composite_score: 53.85,
      risk_level: "élevé",
      primary_pattern: "Controversial sales to Egypt and UAE despite documented violations",
      estimated_arms_trade_human_rights_index: 5.39,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ATH-006",
      name: "Turquie — Drones Bayraktar, conflits Azerbaïdjan & Libye",
      country: "Turquie",
      arms_to_abusers_score: 48.0,
      civilian_harm_arms_score: 50.0,
      export_control_failure_score: 45.0,
      accountability_impunity_score: 46.0,
      composite_score: 47.35,
      risk_level: "élevé",
      primary_pattern: "Bayraktar drone exports enabling civilian harm in conflict zones",
      estimated_arms_trade_human_rights_index: 4.74,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ATH-007",
      name: "Allemagne — Refus partiel ventes SA, contrôles partiels",
      country: "Allemagne",
      arms_to_abusers_score: 28.0,
      civilian_harm_arms_score: 25.0,
      export_control_failure_score: 30.0,
      accountability_impunity_score: 22.0,
      composite_score: 26.35,
      risk_level: "modéré",
      primary_pattern: "Partial export controls with ongoing controversial approvals",
      estimated_arms_trade_human_rights_index: 2.64,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ATH-008",
      name: "Norvège — ATT conforme, traçabilité armes, vérification solide",
      country: "Norvège",
      arms_to_abusers_score: 10.0,
      civilian_harm_arms_score: 8.0,
      export_control_failure_score: 12.0,
      accountability_impunity_score: 9.0,
      composite_score: 9.75,
      risk_level: "faible",
      primary_pattern: "ATT compliant, robust end-use verification framework",
      estimated_arms_trade_human_rights_index: 0.98,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/arms-trade-human-rights-engine`, {
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
