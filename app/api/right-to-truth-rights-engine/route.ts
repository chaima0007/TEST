import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-truth-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Right To Truth Rights Engine Agent",
  domain: "right_to_truth_rights",
  total_entities: 8,
  avg_composite: 60.11,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Syrie — Disparitions forcées massives, archives détruites",
    "Corée du Nord — Déni systématique, zéro commission vérité",
    "Chine — Tiananmen, Xinjiang: suppression totale vérité",
  ],
  critical_alerts: [
    "Syrie: Mass enforced disappearances & systematic archive destruction",
    "Corée du Nord: Total denial of truth mechanisms & victim reparation",
    "Chine: Tiananmen & Xinjiang truth suppression with no accountability",
    "Myanmar — Génocide Rohingya: impunité totale & refus commission",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_truth_rights_index: 6.01,
  entities: [
    {
      entity_id: "RTT-001",
      name: "Syrie — Disparitions forcées massives, archives détruites",
      country: "Syrie",
      truth_commission_denial_score: 98.0,
      enforced_disappearance_impunity_score: 97.0,
      archive_destruction_score: 95.0,
      victim_reparation_gap_score: 99.0,
      composite_score: 97.25,
      risk_level: "critique",
      primary_pattern: "Mass enforced disappearances & systematic archive destruction",
      estimated_right_to_truth_rights_index: 9.73,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTT-002",
      name: "Corée du Nord — Déni systématique, zéro commission vérité",
      country: "Corée du Nord",
      truth_commission_denial_score: 99.0,
      enforced_disappearance_impunity_score: 96.0,
      archive_destruction_score: 94.0,
      victim_reparation_gap_score: 98.0,
      composite_score: 96.95,
      risk_level: "critique",
      primary_pattern: "Total denial of truth mechanisms & victim reparation",
      estimated_right_to_truth_rights_index: 9.7,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTT-003",
      name: "Chine — Tiananmen, Xinjiang: suppression totale vérité",
      country: "Chine",
      truth_commission_denial_score: 95.0,
      enforced_disappearance_impunity_score: 88.0,
      archive_destruction_score: 92.0,
      victim_reparation_gap_score: 90.0,
      composite_score: 91.45,
      risk_level: "critique",
      primary_pattern: "Tiananmen & Xinjiang truth suppression with no accountability",
      estimated_right_to_truth_rights_index: 9.15,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTT-004",
      name: "Myanmar — Génocide Rohingya: impunité totale & refus commission",
      country: "Myanmar",
      truth_commission_denial_score: 90.0,
      enforced_disappearance_impunity_score: 86.0,
      archive_destruction_score: 82.0,
      victim_reparation_gap_score: 88.0,
      composite_score: 86.7,
      risk_level: "critique",
      primary_pattern: "Rohingya genocide denial & truth commission refusal",
      estimated_right_to_truth_rights_index: 8.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTT-005",
      name: "Brésil — Dictature militaire: archives partiellement ouvertes",
      country: "Brésil",
      truth_commission_denial_score: 55.0,
      enforced_disappearance_impunity_score: 58.0,
      archive_destruction_score: 52.0,
      victim_reparation_gap_score: 50.0,
      composite_score: 53.85,
      risk_level: "élevé",
      primary_pattern: "Partial truth commission with ongoing military archive restrictions",
      estimated_right_to_truth_rights_index: 5.39,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTT-006",
      name: "Turquie — Génocide arménien: déni officiel persistant",
      country: "Turquie",
      truth_commission_denial_score: 50.0,
      enforced_disappearance_impunity_score: 44.0,
      archive_destruction_score: 48.0,
      victim_reparation_gap_score: 46.0,
      composite_score: 47.1,
      risk_level: "élevé",
      primary_pattern: "Persistent official denial of Armenian genocide & archival access",
      estimated_right_to_truth_rights_index: 4.71,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTT-007",
      name: "Colombie — JEP active, vérité partielle sur FARC & paramilitaires",
      country: "Colombie",
      truth_commission_denial_score: 30.0,
      enforced_disappearance_impunity_score: 28.0,
      archive_destruction_score: 22.0,
      victim_reparation_gap_score: 26.0,
      composite_score: 26.7,
      risk_level: "modéré",
      primary_pattern: "Active JEP process with partial FARC & paramilitary truth-telling",
      estimated_right_to_truth_rights_index: 2.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTT-008",
      name: "Afrique du Sud — Commission Vérité & Réconciliation, modèle mondial",
      country: "Afrique du Sud",
      truth_commission_denial_score: 12.0,
      enforced_disappearance_impunity_score: 10.0,
      archive_destruction_score: 8.0,
      victim_reparation_gap_score: 14.0,
      composite_score: 10.9,
      risk_level: "faible",
      primary_pattern: "TRC model with public hearings & amnesty-for-truth framework",
      estimated_right_to_truth_rights_index: 1.09,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-truth-rights-engine`, {
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
