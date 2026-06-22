import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[illegal-fishing-forced-labor-rights] SWARM_API_URL non défini");
}

const MOCK = {
  agent: "Illegal Fishing Forced Labor Rights Engine Agent",
  domain: "illegal_fishing_forced_labor_rights",
  total_entities: 8,
  avg_composite: 61.52,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_labor_at_sea_confinement: 2, illegal_unreported_fishing_scale: 2, debt_bondage_recruitment_pattern: 2, flag_state_oversight_failure: 2 },
  top_risk_entities: [
    "Thaïlande/Indonésie — Flotte Pêche Hauturière, Travailleurs Migrants Séquestrés Bateaux Fantômes",
    "Chine — PPDM Flotte Lointaine 17K Navires, INN Massive & Équipages Traite Afrique/Pacifique",
    "Corée du Nord — Bateaux Fantômes Travailleurs Forcés, Évasion Sanctions & Pêche Illégale Russie",
  ],
  critical_alerts: [
    "Thaïlande: forced_labor_at_sea_confinement",
    "Chine PPDM: illegal_unreported_fishing_scale",
    "Birmanie: debt_bondage_recruitment_pattern",
    "Pavillons Complaisance: flag_state_oversight_failure",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_illegal_fishing_forced_labor_rights_index: 6.15,
  data_sources: [
    "ilo_c188_work_in_fishing_convention_implementation_review",
    "unodc_trafficking_persons_fishing_industry_global_report",
    "fao_ipoa_iuu_fishing_flag_state_responsibility_framework",
  ],
  entities: [
    { id: "IF-001", name: "Thaïlande/Indonésie — Flotte Pêche Hauturière, Travailleurs Migrants Séquestrés Bateaux Fantômes", country: "Asie du Sud-Est", composite_score: 93.8, forced_labor_at_sea_confinement_score: 96.0, illegal_unreported_fishing_scale_score: 90.0, debt_bondage_recruitment_pattern_score: 94.0, flag_state_oversight_failure_score: 95.0, risk_level: "critique", primary_pattern: "forced_labor_at_sea_confinement", estimated_illegal_fishing_forced_labor_rights_index: 9.38, last_updated: "2026-06-22" },
    { id: "IF-002", name: "Chine — PPDM Flotte 17K Navires, INN Massive Afrique/Amérique du Sud & Équipages Traite", country: "Asie de l'Est", composite_score: 89.2, forced_labor_at_sea_confinement_score: 86.0, illegal_unreported_fishing_scale_score: 96.0, debt_bondage_recruitment_pattern_score: 88.0, flag_state_oversight_failure_score: 87.0, risk_level: "critique", primary_pattern: "illegal_unreported_fishing_scale", estimated_illegal_fishing_forced_labor_rights_index: 8.92, last_updated: "2026-06-22" },
    { id: "IF-003", name: "Birmanie — Courtiers Recrutement Dette, Travailleurs Vente Navires & Captivité Haute Mer", country: "Asie du Sud-Est", composite_score: 86.7, forced_labor_at_sea_confinement_score: 84.0, illegal_unreported_fishing_scale_score: 82.0, debt_bondage_recruitment_pattern_score: 96.0, flag_state_oversight_failure_score: 85.0, risk_level: "critique", primary_pattern: "debt_bondage_recruitment_pattern", estimated_illegal_fishing_forced_labor_rights_index: 8.67, last_updated: "2026-06-22" },
    { id: "IF-004", name: "Pavillons Complaisance — Panama/Vanuatu/Belize Registres, Contrôle Nul & Impunité Armateurs INN", country: "Global", composite_score: 83.5, forced_labor_at_sea_confinement_score: 80.0, illegal_unreported_fishing_scale_score: 85.0, debt_bondage_recruitment_pattern_score: 82.0, flag_state_oversight_failure_score: 90.0, risk_level: "critique", primary_pattern: "flag_state_oversight_failure", estimated_illegal_fishing_forced_labor_rights_index: 8.35, last_updated: "2026-06-22" },
    { id: "IF-005", name: "Afrique Occidentale — Sénégal/Ghana/Mauritanie, Flotte Étrangère INN Épuise Stocks & Pêcheurs Locaux Ruinés", country: "Afrique de l'Ouest", composite_score: 53.4, forced_labor_at_sea_confinement_score: 50.0, illegal_unreported_fishing_scale_score: 58.0, debt_bondage_recruitment_pattern_score: 52.0, flag_state_oversight_failure_score: 54.0, risk_level: "élevé", primary_pattern: "illegal_unreported_fishing_scale", estimated_illegal_fishing_forced_labor_rights_index: 5.34, last_updated: "2026-06-22" },
    { id: "IF-006", name: "Corée du Nord — Bateaux Fantômes Travailleurs Forcés, Évasion Sanctions & Pêche Illégale Mer du Japon", country: "Asie de l'Est", composite_score: 51.2, forced_labor_at_sea_confinement_score: 55.0, illegal_unreported_fishing_scale_score: 52.0, debt_bondage_recruitment_pattern_score: 48.0, flag_state_oversight_failure_score: 50.0, risk_level: "élevé", primary_pattern: "forced_labor_at_sea_confinement", estimated_illegal_fishing_forced_labor_rights_index: 5.12, last_updated: "2026-06-22" },
    { id: "IF-007", name: "ILO C188/FAO IPOA-INN — Convention Travail Pêche, Registre Mondial Navires & Traçabilité Captures", country: "Global", composite_score: 26.2, forced_labor_at_sea_confinement_score: 24.0, illegal_unreported_fishing_scale_score: 28.0, debt_bondage_recruitment_pattern_score: 26.0, flag_state_oversight_failure_score: 27.0, risk_level: "modéré", primary_pattern: "flag_state_oversight_failure", estimated_illegal_fishing_forced_labor_rights_index: 2.62, last_updated: "2026-06-22" },
    { id: "IF-008", name: "Environmental Justice Foundation/Sustainable Fisheries Partnership — Documentation INN & Droits Pêcheurs", country: "Global", composite_score: 4.5, forced_labor_at_sea_confinement_score: 4.0, illegal_unreported_fishing_scale_score: 5.0, debt_bondage_recruitment_pattern_score: 4.0, flag_state_oversight_failure_score: 5.0, risk_level: "faible", primary_pattern: "illegal_unreported_fishing_scale", estimated_illegal_fishing_forced_labor_rights_index: 0.45, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/illegal_fishing_forced_labor_rights_engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
