import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[debt-bondage-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Debt Bondage Rights Engine Agent",
  domain: "debt_bondage_rights",
  total_entities: 8,
  avg_composite: 61.62,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { bonded_labor_debt_coercion_severity: 4, migrant_debt_recruitment_exploitation_scale: 3, legal_protection_debt_bondage_absence: 1 },
  top_risk_entities: [
    "Inde/Pakistan — 9M Travailleurs Liés Dette Briqueteries/Agricoles, Castes & Héritage Dette Inter-Générationnel",
    "Qatar/GCC — Kafala Sponsorship Passeports Confisqués, 2M Travailleurs Migrants, Frais Recrutement Illégaux",
    "Cambodge/Asie SE — Servitude Domestique Dette Agences, Usines Vêtements & Migrants Thaïlande Piégés",
  ],
  critical_alerts: [
    "Inde/Pakistan: bonded_labor_debt_coercion_severity",
    "Qatar/GCC: migrant_debt_recruitment_exploitation_scale",
    "Cambodge/Asie SE: migrant_debt_recruitment_exploitation_scale",
    "Bolivie/Pérou: bonded_labor_debt_coercion_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_debt_bondage_rights_index: 6.16,
  data_sources: [
    "ilo_global_estimates_modern_slavery_forced_labour_debt_bondage",
    "ilo_protocol_p029_forced_labour_convention_2014",
    "anti_slavery_international_bonded_labour_south_asia_report",
  ],
  entities: [
    { id: "DBR-001", name: "Inde/Pakistan — 9M Travailleurs Liés Dette Briqueteries/Agricoles, Castes & Héritage Dette Inter-Générationnel", country: "Inde/Pakistan", composite_score: 93.95, bonded_labor_debt_coercion_severity_score: 96.0, migrant_debt_recruitment_exploitation_scale_score: 93.0, legal_protection_debt_bondage_absence_score: 94.0, corporate_supply_chain_debt_bondage_gap_score: 92.0, risk_level: "critique", primary_pattern: "bonded_labor_debt_coercion_severity", estimated_debt_bondage_rights_index: 9.40, last_updated: "2026-06-21" },
    { id: "DBR-002", name: "Qatar/GCC — Kafala Sponsorship Passeports Confisqués, 2M Travailleurs Migrants, Frais Recrutement Illégaux", country: "Qatar/GCC", composite_score: 90.95, bonded_labor_debt_coercion_severity_score: 93.0, migrant_debt_recruitment_exploitation_scale_score: 91.0, legal_protection_debt_bondage_absence_score: 90.0, corporate_supply_chain_debt_bondage_gap_score: 89.0, risk_level: "critique", primary_pattern: "migrant_debt_recruitment_exploitation_scale", estimated_debt_bondage_rights_index: 9.10, last_updated: "2026-06-21" },
    { id: "DBR-003", name: "Cambodge/Asie SE — Servitude Domestique Dette Agences, Usines Vêtements & Migrants Thaïlande Piégés", country: "Cambodge/Asie SE", composite_score: 87.95, bonded_labor_debt_coercion_severity_score: 90.0, migrant_debt_recruitment_exploitation_scale_score: 88.0, legal_protection_debt_bondage_absence_score: 87.0, corporate_supply_chain_debt_bondage_gap_score: 86.0, risk_level: "critique", primary_pattern: "migrant_debt_recruitment_exploitation_scale", estimated_debt_bondage_rights_index: 8.80, last_updated: "2026-06-21" },
    { id: "DBR-004", name: "Bolivie/Pérou — Enganche Communautés Autochtones, Zafra Canne à Sucre & Dette Company Store", country: "Bolivie/Pérou", composite_score: 84.95, bonded_labor_debt_coercion_severity_score: 87.0, migrant_debt_recruitment_exploitation_scale_score: 85.0, legal_protection_debt_bondage_absence_score: 84.0, corporate_supply_chain_debt_bondage_gap_score: 83.0, risk_level: "critique", primary_pattern: "bonded_labor_debt_coercion_severity", estimated_debt_bondage_rights_index: 8.50, last_updated: "2026-06-21" },
    { id: "DBR-005", name: "Golfe Arabe — Employées Maison Asie/Afrique, Frais Migration Excessifs & Contrats Substitués à l'Arrivée", country: "Golfe Arabe", composite_score: 53.95, bonded_labor_debt_coercion_severity_score: 56.0, migrant_debt_recruitment_exploitation_scale_score: 54.0, legal_protection_debt_bondage_absence_score: 53.0, corporate_supply_chain_debt_bondage_gap_score: 52.0, risk_level: "élevé", primary_pattern: "migrant_debt_recruitment_exploitation_scale", estimated_debt_bondage_rights_index: 5.40, last_updated: "2026-06-21" },
    { id: "DBR-006", name: "UK/Europe — Travailleurs Roumains Bulgares Agriculture, Gangmasters & Hébergement-Dette Employeurs", country: "UK/Europe", composite_score: 50.95, bonded_labor_debt_coercion_severity_score: 53.0, migrant_debt_recruitment_exploitation_scale_score: 51.0, legal_protection_debt_bondage_absence_score: 50.0, corporate_supply_chain_debt_bondage_gap_score: 49.0, risk_level: "élevé", primary_pattern: "bonded_labor_debt_coercion_severity", estimated_debt_bondage_rights_index: 5.10, last_updated: "2026-06-21" },
    { id: "DBR-007", name: "IJM/Anti-Slavery Int'l — Libération Travailleurs Liés, Litiges Judiciaires & Formation Policière", country: "Global", composite_score: 26.05, bonded_labor_debt_coercion_severity_score: 27.0, migrant_debt_recruitment_exploitation_scale_score: 26.0, legal_protection_debt_bondage_absence_score: 25.0, corporate_supply_chain_debt_bondage_gap_score: 26.0, risk_level: "modéré", primary_pattern: "bonded_labor_debt_coercion_severity", estimated_debt_bondage_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "DBR-008", name: "OIT/Protocol P029 — Protocole Travail Forcé 2014, Indicateurs Dette & SDG 8.7 Fin Esclavage Moderne", country: "Global", composite_score: 4.25, bonded_labor_debt_coercion_severity_score: 4.0, migrant_debt_recruitment_exploitation_scale_score: 4.0, legal_protection_debt_bondage_absence_score: 5.0, corporate_supply_chain_debt_bondage_gap_score: 4.0, risk_level: "faible", primary_pattern: "legal_protection_debt_bondage_absence", estimated_debt_bondage_rights_index: 0.43, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/debt-bondage-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
