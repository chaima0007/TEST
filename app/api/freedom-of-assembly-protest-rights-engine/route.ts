import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[freedom-of-assembly-protest-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "freedom_of_assembly_protest_rights_engine",
  domain: "freedom_of_assembly_protest_rights",
  total_entities: 8,
  avg_composite: 60.8,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    repression_violente_manifestants: 2,
    criminalisation_totale_assemblee: 1,
    persecution_leaders_protestataires: 1,
    legislation_anti_manifestation: 2,
    protection_droit_assemblee: 2,
  },
  top_risk_entities: [
    "Belarus/Loukachenko — 35 000 Arrestations Post-2020, Manifestants Torturés, Dirigeants Exilés & Lois Anti-Extrémisme",
    "Myanmar/Junta — Manifestants Tués 3 000+, Syndicats Bannis, Couvre-Feu Permanent & Internet Coupé",
    "Chine/HK — NSL Hong Kong Manifestants, Article 23 Assemblées Illégales, Dirigeants 47 Condamnés & Tiananmen Commémoration Interdite",
    "Égypte/Sissi — Loi 107/2013 Rassemblements, 60 000 Prisonniers Politiques, Sit-In Rabaa 2013 Massacre & ONG Étrangères Interdites",
  ],
  critical_alerts: [
    "Belarus/Loukachenko — 35 000 Arrestations Post-2020, Manifestants Torturés, Dirigeants Exilés & Lois Anti-Extrémisme: repression violente manifestants",
    "Myanmar/Junta — Manifestants Tués 3 000+, Syndicats Bannis, Couvre-Feu Permanent & Internet Coupé: repression violente manifestants",
    "Chine/HK — NSL Hong Kong Manifestants, Article 23 Assemblées Illégales, Dirigeants 47 Condamnés & Tiananmen Commémoration Interdite: criminalisation totale assemblee",
    "Égypte/Sissi — Loi 107/2013 Rassemblements, 60 000 Prisonniers Politiques, Sit-In Rabaa 2013 Massacre & ONG Étrangères Interdites: persecution leaders protestataires",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_freedom_of_assembly_protest_rights_index: 6.08,
  data_sources: [
    "civicus_monitor_civic_space_annual_report",
    "amnesty_protest_repression_crackdown_documentation",
    "human_rights_watch_assembly_criminalization_report",
  ],
  entities: [
    {
      id: "FAP-001",
      name: "Belarus/Loukachenko — 35 000 Arrestations Post-2020, Manifestants Torturés, Dirigeants Exilés & Lois Anti-Extrémisme",
      country: "Belarus",
      composite_score: 92.3,
      protest_violent_repression_severity_score: 96.0,
      assembly_ban_criminalization_scale_score: 90.0,
      protest_leader_arrest_persecution_score: 92.0,
      counter_terrorism_law_assembly_misuse_gap_score: 90.0,
      risk_level: "critique",
      primary_pattern: "repression_violente_manifestants",
      estimated_freedom_of_assembly_protest_rights_index: 9.23,
      last_updated: "2026-06-21",
    },
    {
      id: "FAP-002",
      name: "Myanmar/Junta — Manifestants Tués 3 000+, Syndicats Bannis, Couvre-Feu Permanent & Internet Coupé",
      country: "Myanmar",
      composite_score: 89.35,
      protest_violent_repression_severity_score: 95.0,
      assembly_ban_criminalization_scale_score: 88.0,
      protest_leader_arrest_persecution_score: 85.0,
      counter_terrorism_law_assembly_misuse_gap_score: 88.0,
      risk_level: "critique",
      primary_pattern: "repression_violente_manifestants",
      estimated_freedom_of_assembly_protest_rights_index: 8.94,
      last_updated: "2026-06-21",
    },
    {
      id: "FAP-003",
      name: "Chine/HK — NSL Hong Kong Manifestants, Article 23 Assemblées Illégales, Dirigeants 47 Condamnés & Tiananmen Commémoration Interdite",
      country: "Chine/Hong Kong",
      composite_score: 86.6,
      protest_violent_repression_severity_score: 82.0,
      assembly_ban_criminalization_scale_score: 92.0,
      protest_leader_arrest_persecution_score: 88.0,
      counter_terrorism_law_assembly_misuse_gap_score: 85.0,
      risk_level: "critique",
      primary_pattern: "criminalisation_totale_assemblee",
      estimated_freedom_of_assembly_protest_rights_index: 8.66,
      last_updated: "2026-06-21",
    },
    {
      id: "FAP-004",
      name: "Égypte/Sissi — Loi 107/2013 Rassemblements, 60 000 Prisonniers Politiques, Sit-In Rabaa 2013 Massacre & ONG Étrangères Interdites",
      country: "Égypte",
      composite_score: 83.3,
      protest_violent_repression_severity_score: 88.0,
      assembly_ban_criminalization_scale_score: 82.0,
      protest_leader_arrest_persecution_score: 80.0,
      counter_terrorism_law_assembly_misuse_gap_score: 82.0,
      risk_level: "critique",
      primary_pattern: "persecution_leaders_protestataires",
      estimated_freedom_of_assembly_protest_rights_index: 8.33,
      last_updated: "2026-06-21",
    },
    {
      id: "FAP-005",
      name: "France/UK — Loi Sécurité Globale, Anti-Protest Policing Powers UK, BRAV-M Violences & Extinction Rebellion Interdit",
      country: "France/Royaume-Uni",
      composite_score: 53.6,
      protest_violent_repression_severity_score: 52.0,
      assembly_ban_criminalization_scale_score: 58.0,
      protest_leader_arrest_persecution_score: 50.0,
      counter_terrorism_law_assembly_misuse_gap_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "legislation_anti_manifestation",
      estimated_freedom_of_assembly_protest_rights_index: 5.36,
      last_updated: "2026-06-21",
    },
    {
      id: "FAP-006",
      name: "USA — Anti-BLM Laws 34 États, COINTELPRO Legacy, Poursuites RICO Manifestants & Stand Your Ground Contre Protestataires",
      country: "États-Unis",
      composite_score: 51.5,
      protest_violent_repression_severity_score: 55.0,
      assembly_ban_criminalization_scale_score: 52.0,
      protest_leader_arrest_persecution_score: 48.0,
      counter_terrorism_law_assembly_misuse_gap_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "legislation_anti_manifestation",
      estimated_freedom_of_assembly_protest_rights_index: 5.15,
      last_updated: "2026-06-21",
    },
    {
      id: "FAP-007",
      name: "CIVICUS/FIDH — Monitor Espace Civique, Rapports Liberté Réunion, Défense Manifestants & Lobbying Nations Unies",
      country: "International",
      composite_score: 25.8,
      protest_violent_repression_severity_score: 25.0,
      assembly_ban_criminalization_scale_score: 26.0,
      protest_leader_arrest_persecution_score: 28.0,
      counter_terrorism_law_assembly_misuse_gap_score: 24.0,
      risk_level: "modéré",
      primary_pattern: "protection_droit_assemblee",
      estimated_freedom_of_assembly_protest_rights_index: 2.58,
      last_updated: "2026-06-21",
    },
    {
      id: "FAP-008",
      name: "ONU/Art.20 DUDH — Liberté Réunion Pacifique, Rapporteur Spécial & SDG 16.7 Gouvernance Inclusive",
      country: "International",
      composite_score: 3.95,
      protest_violent_repression_severity_score: 4.0,
      assembly_ban_criminalization_scale_score: 3.0,
      protest_leader_arrest_persecution_score: 4.0,
      counter_terrorism_law_assembly_misuse_gap_score: 5.0,
      risk_level: "faible",
      primary_pattern: "protection_droit_assemblee",
      estimated_freedom_of_assembly_protest_rights_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/freedom-of-assembly-protest-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
