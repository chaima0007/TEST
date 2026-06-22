import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[minority-religious-rights-persecution-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Minority Religious Rights Persecution Engine Agent",
  domain: "minority_religious_rights_persecution",
  total_entities: 8,
  avg_composite: 63.81,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    state_religious_persecution_severity: 3,
    blasphemy_apostasy_law_enforcement_scale: 2,
    minority_worship_restriction_destruction: 2,
    religious_conversion_prohibition_deficit_gap: 1,
  },
  top_risk_entities: [
    "Chine/Ouïghours — Mosquées Détruites Reeducation Camps Xinjiang, Prières Interdites & Hajj Contrôlé État",
    "Iran/Bahais Chrétiens — Emprisonnés Apostasie Peine Mort, Eglises Maisons Fermées & Convertis Torturés",
    "Pakistan/Ahmadis Chrétiens — Blasphème Peine Mort, Ahmadis Déclarés Non-Musulmans & Eglises Brûlées Foules",
  ],
  critical_alerts: [
    "Chine/Ouïghours: state_religious_persecution_severity",
    "Iran/Bahais Chrétiens: blasphemy_apostasy_law_enforcement_scale",
    "Pakistan/Ahmadis Chrétiens: blasphemy_apostasy_law_enforcement_scale",
    "Inde/Lynchages Minorités: religious_conversion_prohibition_deficit_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_minority_religious_rights_persecution_index: 6.38,
  data_sources: [
    "uscirf_annual_report_religious_freedom",
    "forum_18_religious_freedom_monitoring",
    "hrw_religious_persecution_documentation",
  ],
  entities: [
    {
      id: "MRR-001",
      name: "Chine/Ouïghours — Mosquées Détruites Reeducation Camps Xinjiang, Prières Interdites & Hajj Contrôlé État",
      country: "Chine",
      state_religious_persecution_severity_score: 96.0,
      blasphemy_apostasy_law_enforcement_scale_score: 94.0,
      minority_worship_restriction_destruction_score: 95.0,
      religious_conversion_prohibition_deficit_gap_score: 93.0,
      composite_score: 94.65,
      risk_level: "critique",
      primary_pattern: "state_religious_persecution_severity",
      estimated_minority_religious_rights_persecution_index: 9.47,
      last_updated: "2026-06-21",
    },
    {
      id: "MRR-002",
      name: "Iran/Bahais Chrétiens — Emprisonnés Apostasie Peine Mort, Eglises Maisons Fermées & Convertis Torturés",
      country: "Iran",
      state_religious_persecution_severity_score: 93.0,
      blasphemy_apostasy_law_enforcement_scale_score: 95.0,
      minority_worship_restriction_destruction_score: 91.0,
      religious_conversion_prohibition_deficit_gap_score: 92.0,
      composite_score: 92.8,
      risk_level: "critique",
      primary_pattern: "blasphemy_apostasy_law_enforcement_scale",
      estimated_minority_religious_rights_persecution_index: 9.28,
      last_updated: "2026-06-21",
    },
    {
      id: "MRR-003",
      name: "Pakistan/Ahmadis Chrétiens — Blasphème Peine Mort, Ahmadis Déclarés Non-Musulmans & Eglises Brûlées Foules",
      country: "Pakistan",
      state_religious_persecution_severity_score: 91.0,
      blasphemy_apostasy_law_enforcement_scale_score: 93.0,
      minority_worship_restriction_destruction_score: 89.0,
      religious_conversion_prohibition_deficit_gap_score: 90.0,
      composite_score: 90.8,
      risk_level: "critique",
      primary_pattern: "blasphemy_apostasy_law_enforcement_scale",
      estimated_minority_religious_rights_persecution_index: 9.08,
      last_updated: "2026-06-21",
    },
    {
      id: "MRR-004",
      name: "Inde/Lynchages Minorités — BJP Lois Anti-Conversion, Muslimans Lynchés Vache & Démolitions Mosquées Bulldozer",
      country: "Inde",
      state_religious_persecution_severity_score: 88.0,
      blasphemy_apostasy_law_enforcement_scale_score: 85.0,
      minority_worship_restriction_destruction_score: 87.0,
      religious_conversion_prohibition_deficit_gap_score: 89.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "religious_conversion_prohibition_deficit_gap",
      estimated_minority_religious_rights_persecution_index: 8.72,
      last_updated: "2026-06-21",
    },
    {
      id: "MRR-005",
      name: "Myanmar/Rohingya — Mosquées Brûlées Génocide, Statut Apatride 1982 & Moine Wirathu Haine Anti-Islam",
      country: "Myanmar",
      state_religious_persecution_severity_score: 58.0,
      blasphemy_apostasy_law_enforcement_scale_score: 55.0,
      minority_worship_restriction_destruction_score: 60.0,
      religious_conversion_prohibition_deficit_gap_score: 57.0,
      composite_score: 57.55,
      risk_level: "élevé",
      primary_pattern: "minority_worship_restriction_destruction",
      estimated_minority_religious_rights_persecution_index: 5.76,
      last_updated: "2026-06-21",
    },
    {
      id: "MRR-006",
      name: "Égypte/Coptes — Discriminés Emploi État, Eglises Démolies Permis Refusés & Blasphème Procès Chrétiens",
      country: "Égypte",
      state_religious_persecution_severity_score: 55.0,
      blasphemy_apostasy_law_enforcement_scale_score: 57.0,
      minority_worship_restriction_destruction_score: 58.0,
      religious_conversion_prohibition_deficit_gap_score: 54.0,
      composite_score: 56.05,
      risk_level: "élevé",
      primary_pattern: "minority_worship_restriction_destruction",
      estimated_minority_religious_rights_persecution_index: 5.61,
      last_updated: "2026-06-21",
    },
    {
      id: "MRR-007",
      name: "USCIRF/Forum 18 — Monitoring Liberté Religieuse, Rapport Annuel Violations & Commission Internationale",
      country: "Global",
      state_religious_persecution_severity_score: 28.0,
      blasphemy_apostasy_law_enforcement_scale_score: 27.0,
      minority_worship_restriction_destruction_score: 26.0,
      religious_conversion_prohibition_deficit_gap_score: 25.0,
      composite_score: 26.65,
      risk_level: "modéré",
      primary_pattern: "state_religious_persecution_severity",
      estimated_minority_religious_rights_persecution_index: 2.67,
      last_updated: "2026-06-21",
    },
    {
      id: "MRR-008",
      name: "ONU/PIDCP Art.18 — Liberté Religion & Déclaration 1981 Intolérance Religieuse Rapporteur Spécial",
      country: "Global",
      state_religious_persecution_severity_score: 5.0,
      blasphemy_apostasy_law_enforcement_scale_score: 5.0,
      minority_worship_restriction_destruction_score: 5.0,
      religious_conversion_prohibition_deficit_gap_score: 4.0,
      composite_score: 4.8,
      risk_level: "faible",
      primary_pattern: "state_religious_persecution_severity",
      estimated_minority_religious_rights_persecution_index: 0.48,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/minority-religious-rights-persecution-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
