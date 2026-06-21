import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "War Crimes Accountability Engine Agent",
  domain: "war_crimes_accountability",
  total_entities: 8,
  avg_composite: 62.40,
  confidence_score: 0.89,
  avg_estimated_war_crimes_accountability_index: 6.24,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "icc_annual_report_situations_2023",
    "un_commission_inquiry_war_crimes_2023",
    "human_rights_watch_ihl_violations_2023",
    "icrc_international_humanitarian_law_report_2023",
  ],
  critical_alerts: [],
  entities: [
    {
      entity_id: "WCA-001",
      name: "Syrie — 500K+ Morts, Armes Chimiques Impunies, 600+ Hôpitaux Bombardés, Veto Russie/Chine CPI & Aucun Jugement",
      country: "Syrie",
      composite_score: 96.05,
      risk_level: "critique",
      estimated_war_crimes_accountability_index: 9.61,
      primary_pattern: "chemical_biological_weapons_use",
    },
    {
      entity_id: "WCA-002",
      name: "Russie/Ukraine — Bucha Massacres Documentés, Bombes Sous-Munitions Civils, Centrales Nucléaires Ciblées & CPI Mandat Poutine Non-Exécuté",
      country: "Russie/Ukraine",
      composite_score: 89.10,
      risk_level: "critique",
      estimated_war_crimes_accountability_index: 8.91,
      primary_pattern: "accountability_icc_prosecution_gap",
    },
    {
      entity_id: "WCA-003",
      name: "Yémen/Coalition — Frappes Marchés/Hôpitaux/Mariages ONU Documentées, Armes US/UK Utilisées & Panel ONU Bloqué 2023",
      country: "Yémen",
      composite_score: 85.65,
      risk_level: "critique",
      estimated_war_crimes_accountability_index: 8.57,
      primary_pattern: "humanitarian_law_violations_impunity",
    },
    {
      entity_id: "WCA-004",
      name: "Israël/Gaza — 35K+ Morts Civils 2023-2024, CIJ Génocide Plausible, Blocus Humanitaire & 100+ Journalistes Tués",
      country: "Israël/Gaza",
      composite_score: 86.05,
      risk_level: "critique",
      estimated_war_crimes_accountability_index: 8.61,
      primary_pattern: "war_crimes_scale_civilian_harm",
    },
    {
      entity_id: "WCA-005",
      name: "Myanmar — Crimes Contre Rohingya Génocide CIJ, Junta Bombes Villages Karen/Chin & Armes Importées Malgré Embargo",
      country: "Myanmar",
      composite_score: 57.40,
      risk_level: "élevé",
      estimated_war_crimes_accountability_index: 5.74,
      primary_pattern: "accountability_icc_prosecution_gap",
    },
    {
      entity_id: "WCA-006",
      name: "Éthiopie — Tigré Blocus Alimentaire Crime de Guerre, Viols Systématiques Arme Guerre & Impunité Totale Commandants",
      country: "Éthiopie",
      composite_score: 53.40,
      risk_level: "élevé",
      estimated_war_crimes_accountability_index: 5.34,
      primary_pattern: "humanitarian_law_violations_impunity",
    },
    {
      entity_id: "WCA-007",
      name: "Colombie — FARC/Para Crimes Passés, JEP Réconciliation en Progrès & 30 Ans Conflit Quelques Jugements",
      country: "Colombie",
      composite_score: 26.50,
      risk_level: "modéré",
      estimated_war_crimes_accountability_index: 2.65,
      primary_pattern: "war_crimes_scale_civilian_harm",
    },
    {
      entity_id: "WCA-008",
      name: "Pays-Bas/CPI — Siège CPI La Haye, Jurisprudence Crimes Guerre, Contribution Financière Majeure & Pas en Conflit",
      country: "Pays-Bas",
      composite_score: 5.05,
      risk_level: "faible",
      estimated_war_crimes_accountability_index: 0.51,
      primary_pattern: "accountability_icc_prosecution_gap",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[war-crimes-accountability-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/war-crimes-accountability-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
