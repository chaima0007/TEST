import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[business-human-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Business Human Rights Engine Agent",
  domain: "business_human_rights",
  total_entities: 8,
  avg_composite: 59.56,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { supply_chain_abuse_scale: 2, corporate_impunity: 2, remedy_access_denial: 2, regulatory_framework_gap: 2 },
  top_risk_entities: [
    "Fast Fashion/Rana Plaza — H&M/Zara/Primark, Travail Forcé Bangladesh & Impunité Totale",
    "Tech/Minerais — Apple/Tesla/Samsung, Cobalt Enfants Congo & Chaînes Approvisionnement Opaques",
    "Agro-industrie/Palmier à Huile — Déforestation, Expulsion Peuples Indigènes & Travail Servile",
  ],
  critical_alerts: [
    "Fast Fashion/Rana Plaza: supply_chain_abuse_scale",
    "Tech/Minerais: corporate_impunity",
    "Agro-industrie/Palmier à Huile: remedy_access_denial",
    "Pétrole/Gaz: corporate_impunity",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_business_human_rights_index: 5.96,
  data_sources: [
    "business_human_rights_resource_centre_corporate_accountability_database",
    "un_working_group_business_human_rights_annual_report",
    "oecd_guidelines_multinational_enterprises_due_diligence_guidance",
  ],
  entities: [
    { entity_id: "BHR-001", name: "Fast Fashion/Rana Plaza — H&M/Zara/Primark, Travail Forcé Bangladesh & Impunité Totale", country: "Global/Asie du Sud", composite_score: 89.1, supply_chain_abuse_scale_score: 92.0, corporate_impunity_score: 88.0, remedy_access_denial_score: 90.0, regulatory_framework_gap_score: 85.0, risk_level: "critique", primary_pattern: "supply_chain_abuse_scale", estimated_business_human_rights_index: 8.91, last_updated: "2026-06-20" },
    { entity_id: "BHR-002", name: "Tech/Minerais — Apple/Tesla/Samsung, Cobalt Enfants Congo & Chaînes Approvisionnement Opaques", country: "Global/Afrique", composite_score: 86.55, supply_chain_abuse_scale_score: 88.0, corporate_impunity_score: 90.0, remedy_access_denial_score: 85.0, regulatory_framework_gap_score: 82.0, risk_level: "critique", primary_pattern: "corporate_impunity", estimated_business_human_rights_index: 8.66, last_updated: "2026-06-20" },
    { entity_id: "BHR-003", name: "Agro-industrie/Palmier à Huile — Déforestation, Expulsion Peuples Indigènes & Travail Servile", country: "Asie du Sud-Est/Amérique Latine", composite_score: 84.0, supply_chain_abuse_scale_score: 85.0, corporate_impunity_score: 82.0, remedy_access_denial_score: 88.0, regulatory_framework_gap_score: 80.0, risk_level: "critique", primary_pattern: "remedy_access_denial", estimated_business_human_rights_index: 8.4, last_updated: "2026-06-20" },
    { entity_id: "BHR-004", name: "Pétrole/Gaz — Shell Niger Delta, TotalEnergies Ouganda EACOP & Pollution Sans Réparation", country: "Afrique Sub-Saharienne", composite_score: 81.35, supply_chain_abuse_scale_score: 80.0, corporate_impunity_score: 85.0, remedy_access_denial_score: 82.0, regulatory_framework_gap_score: 78.0, risk_level: "critique", primary_pattern: "corporate_impunity", estimated_business_human_rights_index: 8.14, last_updated: "2026-06-20" },
    { entity_id: "BHR-005", name: "UE — Directive Devoir de Vigilance (CSDDD), Loi Française Vigilance & Application Partielle", country: "Europe", composite_score: 53.85, supply_chain_abuse_scale_score: 52.0, corporate_impunity_score: 55.0, remedy_access_denial_score: 58.0, regulatory_framework_gap_score: 50.0, risk_level: "élevé", primary_pattern: "regulatory_framework_gap", estimated_business_human_rights_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "BHR-006", name: "USA — Uyghur Forced Labor Prevention Act, FCPA & Lacunes Juridictionnelles Extraterritoriales", country: "Amérique du Nord", composite_score: 51.15, supply_chain_abuse_scale_score: 48.0, corporate_impunity_score: 52.0, remedy_access_denial_score: 55.0, regulatory_framework_gap_score: 50.0, risk_level: "élevé", primary_pattern: "regulatory_framework_gap", estimated_business_human_rights_index: 5.12, last_updated: "2026-06-20" },
    { entity_id: "BHR-007", name: "ONU — Principes Directeurs Ruggie, Traité Contraignant Entreprises & Droits Humains", country: "Global", composite_score: 26.1, supply_chain_abuse_scale_score: 22.0, corporate_impunity_score: 28.0, remedy_access_denial_score: 30.0, regulatory_framework_gap_score: 25.0, risk_level: "modéré", primary_pattern: "supply_chain_abuse_scale", estimated_business_human_rights_index: 2.61, last_updated: "2026-06-20" },
    { entity_id: "BHR-008", name: "OIT/OCDE — Conventions Travail, Principes Directeurs Multinationales & Mécanismes PCN", country: "Global", composite_score: 4.4, supply_chain_abuse_scale_score: 4.0, corporate_impunity_score: 5.0, remedy_access_denial_score: 3.0, regulatory_framework_gap_score: 6.0, risk_level: "faible", primary_pattern: "remedy_access_denial", estimated_business_human_rights_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/business-human-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
