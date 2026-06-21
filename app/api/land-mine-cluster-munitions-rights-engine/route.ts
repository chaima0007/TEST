import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[land-mine-cluster-munitions-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Land Mine Cluster Munitions Rights Engine Agent",
  domain: "land_mine_cluster_munitions_rights",
  total_entities: 8,
  avg_composite: 61.43,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { active_landmine_civilian_casualty_severity: 2, cluster_munition_unexploded_ordnance_scale: 2, mine_ban_treaty_non_compliance: 2, victim_assistance_demining_funding_deficit_gap: 2 },
  top_risk_entities: [
    "Afghanistan — 10M Mines Posées, 30+ Ans Contamination, 50 Victimes/Mois & HALO Trust Financement Insuffisant",
    "Yemen — Coalition Sous-Munitions 2015-22, Cluster CBU-87 Civils, Zones Contaminées Portuaires & Financement Déminage Bloqué",
    "Myanmar — Mines Tatmadaw Minorités Ethniques, Chin/Karen Villages Minés, Non-Signataire Ottawa & Victimes Enfants",
  ],
  critical_alerts: [
    "Afghanistan: active_landmine_civilian_casualty_severity",
    "Yemen: cluster_munition_unexploded_ordnance_scale",
    "Myanmar: mine_ban_treaty_non_compliance",
    "Ukraine/Russie: cluster_munition_unexploded_ordnance_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_land_mine_cluster_munitions_rights_index: 6.14,
  data_sources: [
    "icbl_landmine_monitor_report",
    "geneva_international_centre_demining_report",
    "human_rights_watch_cluster_munitions_report",
  ],
  entities: [
    { id: "LMC-001", name: "Afghanistan — 10M Mines Posées, 30+ Ans Contamination, 50 Victimes/Mois & HALO Trust Financement Insuffisant", country: "Afghanistan", composite_score: 93.55, active_landmine_civilian_casualty_severity_score: 95.0, cluster_munition_unexploded_ordnance_scale_score: 93.0, mine_ban_treaty_non_compliance_score: 92.0, victim_assistance_demining_funding_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "active_landmine_civilian_casualty_severity", estimated_land_mine_cluster_munitions_rights_index: 9.36, last_updated: "2026-06-21" },
    { id: "LMC-002", name: "Yemen — Coalition Sous-Munitions 2015-22, Cluster CBU-87 Civils, Zones Contaminées Portuaires & Financement Déminage Bloqué", country: "Yemen", composite_score: 90.3, active_landmine_civilian_casualty_severity_score: 91.0, cluster_munition_unexploded_ordnance_scale_score: 92.0, mine_ban_treaty_non_compliance_score: 88.0, victim_assistance_demining_funding_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "cluster_munition_unexploded_ordnance_scale", estimated_land_mine_cluster_munitions_rights_index: 9.03, last_updated: "2026-06-21" },
    { id: "LMC-003", name: "Myanmar — Mines Tatmadaw Minorités Ethniques, Chin/Karen Villages Minés, Non-Signataire Ottawa & Victimes Enfants", country: "Myanmar", composite_score: 86.55, active_landmine_civilian_casualty_severity_score: 87.0, cluster_munition_unexploded_ordnance_scale_score: 85.0, mine_ban_treaty_non_compliance_score: 88.0, victim_assistance_demining_funding_deficit_gap_score: 86.0, risk_level: "critique", primary_pattern: "mine_ban_treaty_non_compliance", estimated_land_mine_cluster_munitions_rights_index: 8.66, last_updated: "2026-06-21" },
    { id: "LMC-004", name: "Ukraine/Russie — Mines POM-3 Russes 2022, Cluster MLRS Civils, Zones Résidentielles Contaminées & Déminage 100 Ans Estimé", country: "Ukraine", composite_score: 82.6, active_landmine_civilian_casualty_severity_score: 83.0, cluster_munition_unexploded_ordnance_scale_score: 82.0, mine_ban_treaty_non_compliance_score: 84.0, victim_assistance_demining_funding_deficit_gap_score: 81.0, risk_level: "critique", primary_pattern: "cluster_munition_unexploded_ordnance_scale", estimated_land_mine_cluster_munitions_rights_index: 8.26, last_updated: "2026-06-21" },
    { id: "LMC-005", name: "Laos/Vietnam — Heritage Indochine Guerre, UXO Laos 30% Territoire 50 Ans, Agent Orange Victimes & Financement US Insuffisant", country: "Laos", composite_score: 55.45, active_landmine_civilian_casualty_severity_score: 56.0, cluster_munition_unexploded_ordnance_scale_score: 54.0, mine_ban_treaty_non_compliance_score: 55.0, victim_assistance_demining_funding_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "victim_assistance_demining_funding_deficit_gap", estimated_land_mine_cluster_munitions_rights_index: 5.55, last_updated: "2026-06-21" },
    { id: "LMC-006", name: "Colombie — FARC Mines Rurales, 2ème Mondial Victimes 2019-22, Accord Paix Déminage & Remine Post-Conflit", country: "Colombie", composite_score: 52.45, active_landmine_civilian_casualty_severity_score: 52.0, cluster_munition_unexploded_ordnance_scale_score: 51.0, mine_ban_treaty_non_compliance_score: 54.0, victim_assistance_demining_funding_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "active_landmine_civilian_casualty_severity", estimated_land_mine_cluster_munitions_rights_index: 5.25, last_updated: "2026-06-21" },
    { id: "LMC-007", name: "ICBL/GICHD — Campagne Internationale Mines, Geneva International Centre Déminage, Monitor Mines 2024 & Mécanisme Convention Ottawa", country: "Global", composite_score: 26.55, active_landmine_civilian_casualty_severity_score: 27.0, cluster_munition_unexploded_ordnance_scale_score: 25.0, mine_ban_treaty_non_compliance_score: 28.0, victim_assistance_demining_funding_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "victim_assistance_demining_funding_deficit_gap", estimated_land_mine_cluster_munitions_rights_index: 2.66, last_updated: "2026-06-21" },
    { id: "LMC-008", name: "ONU/Ottawa — Traité Ottawa 1997 163 États Parties, CCM Sous-Munitions 2008, Protocol V CCW & Mécanisme Revue Mise Oeuvre", country: "Global", composite_score: 4.0, active_landmine_civilian_casualty_severity_score: 4.0, cluster_munition_unexploded_ordnance_scale_score: 4.0, mine_ban_treaty_non_compliance_score: 4.0, victim_assistance_demining_funding_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "mine_ban_treaty_non_compliance", estimated_land_mine_cluster_munitions_rights_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/land-mine-cluster-munitions-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
