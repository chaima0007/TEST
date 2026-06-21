import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[lgbtq-rights-criminalization-engine] SWARM_API_URL not set — returning mock");
}

const MOCK = {
  agent: "LGBTQ+ Rights Criminalization Engine Agent",
  domain: "lgbtq_rights_criminalization",
  total_entities: 8,
  avg_composite: 63.67,
  confidence_score: 0.85,
  avg_estimated_lgbtq_rights_criminalization_index: 6.37,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { state_criminalization_imprisonment_severity: 3, legal_identity_recognition_denial: 2, violence_persecution_impunity_scale: 1, anti_lgbtq_legislation_rollback_deficit_gap: 2 },
  top_risk_entities: [
    "Ouganda/Anti-Homosexuality Act 2023 — Peine Mort Homosexualité Aggravée, Perpétuité Simple, Dénonciation Obligatoire & 1 000+ Arrestations",
    "Iran/République Islamique — Peine Mort Sodomie Codifiée Penal, 4 000+ Exécutions LGBTQ+ depuis 1979, Conversion Forcée & Chirurgie Trans Coercitive",
    "Arabie Saoudite/Châtiments Corporels — Flagellation & Décapitation Charia, Aucun Statut Légal, Police Morale & Expatriés LGBTQ+ Expulsés",
  ],
  critical_alerts: [
    "Ouganda/Anti-Homosexuality Act 2023: state_criminalization_imprisonment_severity",
    "Iran/République Islamique: state_criminalization_imprisonment_severity",
    "Arabie Saoudite/Châtiments Corporels: legal_identity_recognition_denial",
    "Tchétchénie/Camps Purge: violence_persecution_impunity_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  data_sources: [
    "ilga_world_state_sponsored_homophobia_report",
    "hrw_lgbtq_rights_violations_global_documentation",
    "amnesty_international_lgbtq_persecution_annual_report",
  ],
  entities: [
    { id: "LRC-001", name: "Ouganda/Anti-Homosexuality Act 2023 — Peine Mort Homosexualité Aggravée, Perpétuité Simple, Dénonciation Obligatoire & 1 000+ Arrestations", country: "Ouganda", state_criminalization_imprisonment_severity_score: 97.0, violence_persecution_impunity_scale_score: 95.0, legal_identity_recognition_denial_score: 96.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 94.0, composite_score: 95.65, risk_level: "critique", primary_pattern: "state_criminalization_imprisonment_severity", estimated_lgbtq_rights_criminalization_index: 9.57, last_updated: "2026-06-21" },
    { id: "LRC-002", name: "Iran/République Islamique — Peine Mort Sodomie Codifiée Penal, 4 000+ Exécutions LGBTQ+ depuis 1979, Conversion Forcée & Chirurgie Trans Coercitive", country: "Iran", state_criminalization_imprisonment_severity_score: 94.0, violence_persecution_impunity_scale_score: 93.0, legal_identity_recognition_denial_score: 92.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 91.0, composite_score: 92.65, risk_level: "critique", primary_pattern: "state_criminalization_imprisonment_severity", estimated_lgbtq_rights_criminalization_index: 9.27, last_updated: "2026-06-21" },
    { id: "LRC-003", name: "Arabie Saoudite/Châtiments Corporels — Flagellation & Décapitation Charia, Aucun Statut Légal, Police Morale & Expatriés LGBTQ+ Expulsés", country: "Arabie Saoudite", state_criminalization_imprisonment_severity_score: 91.0, violence_persecution_impunity_scale_score: 90.0, legal_identity_recognition_denial_score: 93.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 89.0, composite_score: 90.85, risk_level: "critique", primary_pattern: "legal_identity_recognition_denial", estimated_lgbtq_rights_criminalization_index: 9.09, last_updated: "2026-06-21" },
    { id: "LRC-004", name: "Tchétchénie/Camps Purge — Opération Nettoyage 2017-2019, 150+ Hommes Détenus Camps Secrets, Tortures & Familles Invitées Tuer Membres LGBTQ+", country: "Russie/Tchétchénie", state_criminalization_imprisonment_severity_score: 88.0, violence_persecution_impunity_scale_score: 92.0, legal_identity_recognition_denial_score: 87.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 90.0, composite_score: 89.15, risk_level: "critique", primary_pattern: "violence_persecution_impunity_scale", estimated_lgbtq_rights_criminalization_index: 8.92, last_updated: "2026-06-21" },
    { id: "LRC-005", name: "Russie/Loi Propagande — Propagande LGBTQ+ Interdite Tous Âges 2023, Organisations Liquidées, Médias Censurés & Amendes Massives", country: "Russie", state_criminalization_imprisonment_severity_score: 57.0, violence_persecution_impunity_scale_score: 55.0, legal_identity_recognition_denial_score: 58.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 56.0, composite_score: 56.55, risk_level: "élevé", primary_pattern: "anti_lgbtq_legislation_rollback_deficit_gap", estimated_lgbtq_rights_criminalization_index: 5.66, last_updated: "2026-06-21" },
    { id: "LRC-006", name: "Nigeria/Sharia Peine Mort — 12 États Sharia Peine Mort Homosexualité, Loi Same-Sex Prohibition 14 Ans Prison & Lynchages Communautaires", country: "Nigeria", state_criminalization_imprisonment_severity_score: 54.0, violence_persecution_impunity_scale_score: 52.0, legal_identity_recognition_denial_score: 55.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 53.0, composite_score: 53.55, risk_level: "élevé", primary_pattern: "state_criminalization_imprisonment_severity", estimated_lgbtq_rights_criminalization_index: 5.36, last_updated: "2026-06-21" },
    { id: "LRC-007", name: "ILGA/Rainbow Europe — Cartographie 64 Pays Criminalisation, Baromètre Droits LGBTQ+, Score Moyen Europe 49% & Rapport Annuel Violations", country: "Global", state_criminalization_imprisonment_severity_score: 27.0, violence_persecution_impunity_scale_score: 25.0, legal_identity_recognition_denial_score: 26.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 28.0, composite_score: 26.45, risk_level: "modéré", primary_pattern: "anti_lgbtq_legislation_rollback_deficit_gap", estimated_lgbtq_rights_criminalization_index: 2.65, last_updated: "2026-06-21" },
    { id: "LRC-008", name: "ONU/Principes Yogyakarta — 29 Principes Application Droit International Orientation Sexuelle 2006, Résolution UNHRC & Expert Indépendant SOGI", country: "Global", state_criminalization_imprisonment_severity_score: 5.0, violence_persecution_impunity_scale_score: 4.0, legal_identity_recognition_denial_score: 4.0, anti_lgbtq_legislation_rollback_deficit_gap_score: 5.0, composite_score: 4.5, risk_level: "faible", primary_pattern: "legal_identity_recognition_denial", estimated_lgbtq_rights_criminalization_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/lgbtq-rights-criminalization-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data));
  } catch {
    return NextResponse.json(sealResponse(MOCK), { status: 502 });
  }
}
