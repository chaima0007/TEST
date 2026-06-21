import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[arms-trade-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Arms Trade Engine Agent",
  domain: "arms_trade",
  total_entities: 8,
  avg_composite: 61.64,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { atrocity_enabling_transfers: 2, civilian_harm_documentation: 2, export_control_circumvention: 2, arms_embargo_violation: 2 },
  top_risk_entities: [
    "USA/Arabie Saoudite — 100Mrd$ Armes Yémen, Bombes Écoles/Hôpitaux & Impunité Exportateur",
    "Russie/Ukraine — Bombardements Civils, Missiles Interdits & Violations DIH Documentées",
    "Israël/Gaza — Armes Occidentales Utilisées Populations Civiles & Génocide Allégué CIJ",
  ],
  critical_alerts: [
    "USA/Arabie Saoudite: atrocity_enabling_transfers",
    "Russie/Ukraine: civilian_harm_documentation",
    "Israël/Gaza: civilian_harm_documentation",
    "Chine/Myanmar: export_control_circumvention",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_arms_trade_index: 6.16,
  data_sources: [
    "sipri_arms_transfers_database_global_trends_report",
    "amnesty_international_arms_trade_atrocities_annual_report",
    "arms_control_association_treaty_compliance_global_monitor",
  ],
  entities: [
    { id: "AT-001", name: "USA/Arabie Saoudite — 100Mrd$ Armes Yémen, Bombes Écoles/Hôpitaux & Impunité Exportateur", country: "Amérique du Nord / Moyen-Orient", composite_score: 92.25, atrocity_enabling_transfers_score: 95.0, export_control_circumvention_score: 88.0, civilian_harm_documentation_score: 95.0, arms_embargo_violation_score: 90.0, risk_level: "critique", primary_pattern: "atrocity_enabling_transfers", estimated_arms_trade_index: 9.23, last_updated: "2026-06-21" },
    { id: "AT-002", name: "Russie/Ukraine — Bombardements Civils, Missiles Interdits & Violations DIH Documentées", country: "Europe de l'Est", composite_score: 90.25, atrocity_enabling_transfers_score: 92.0, export_control_circumvention_score: 85.0, civilian_harm_documentation_score: 92.0, arms_embargo_violation_score: 92.0, risk_level: "critique", primary_pattern: "civilian_harm_documentation", estimated_arms_trade_index: 9.03, last_updated: "2026-06-21" },
    { id: "AT-003", name: "Israël/Gaza — Armes Occidentales Utilisées Populations Civiles & Génocide Allégué CIJ", country: "Moyen-Orient", composite_score: 88.25, atrocity_enabling_transfers_score: 90.0, export_control_circumvention_score: 82.0, civilian_harm_documentation_score: 95.0, arms_embargo_violation_score: 85.0, risk_level: "critique", primary_pattern: "civilian_harm_documentation", estimated_arms_trade_index: 8.83, last_updated: "2026-06-21" },
    { id: "AT-004", name: "Chine/Myanmar — Armes Post-Coup, Junta Massacres & Complicité Transferts Embargo", country: "Asie du Nord-Est / Asie du Sud-Est", composite_score: 85.0, atrocity_enabling_transfers_score: 85.0, export_control_circumvention_score: 88.0, civilian_harm_documentation_score: 82.0, arms_embargo_violation_score: 85.0, risk_level: "critique", primary_pattern: "export_control_circumvention", estimated_arms_trade_index: 8.5, last_updated: "2026-06-21" },
    { id: "AT-005", name: "UE/Exportateurs — France/Allemagne/Italie Ventes Régimes Autoritaires & Contrôles Lacunaires", country: "Europe", composite_score: 54.0, atrocity_enabling_transfers_score: 55.0, export_control_circumvention_score: 58.0, civilian_harm_documentation_score: 52.0, arms_embargo_violation_score: 50.0, risk_level: "élevé", primary_pattern: "export_control_circumvention", estimated_arms_trade_index: 5.4, last_updated: "2026-06-21" },
    { id: "AT-006", name: "Courtiers Illicites — Réseaux Viktor Bout Type, États Faillis & Circuits Parallèles", country: "Global", composite_score: 53.1, atrocity_enabling_transfers_score: 52.0, export_control_circumvention_score: 58.0, civilian_harm_documentation_score: 48.0, arms_embargo_violation_score: 55.0, risk_level: "élevé", primary_pattern: "arms_embargo_violation", estimated_arms_trade_index: 5.31, last_updated: "2026-06-21" },
    { id: "AT-007", name: "CAAT/Amnesty Arms — Campagne Contre Commerce Armes, ATT Ratification & Plaidoyer Suspensions", country: "Global", composite_score: 25.85, atrocity_enabling_transfers_score: 22.0, export_control_circumvention_score: 25.0, civilian_harm_documentation_score: 28.0, arms_embargo_violation_score: 30.0, risk_level: "modéré", primary_pattern: "atrocity_enabling_transfers", estimated_arms_trade_index: 2.59, last_updated: "2026-06-21" },
    { id: "AT-008", name: "ONU/Traité Commerce Armes 2014 — ATT, Registre Armes Classiques & Comité États Parties", country: "Global", composite_score: 4.4, atrocity_enabling_transfers_score: 4.0, export_control_circumvention_score: 5.0, civilian_harm_documentation_score: 3.0, arms_embargo_violation_score: 6.0, risk_level: "faible", primary_pattern: "arms_embargo_violation", estimated_arms_trade_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arms-trade-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
