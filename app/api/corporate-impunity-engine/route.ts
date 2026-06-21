import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-impunity-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Corporate Impunity Engine Agent",
  domain: "corporate_impunity",
  total_entities: 8,
  avg_composite: 60.8,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { supply_chain_abuse_scale: 2, accountability_remedy_gap: 2, environmental_social_harm: 2, legal_jurisdiction_evasion: 2 },
  top_risk_entities: [
    "Extractives/Congo — Cobalt Apple/Tesla, Travail Enfants Mines & Chaînes Sans Traçabilité",
    "Fast Fashion/Bangladesh — Rana Plaza 1134 Morts, Marques Non Poursuivies & Due Diligence Absente",
    "Big Oil/Nigeria — Shell Delta Ogoni, Marée Noires 50 Ans & Procès Hors Territoire",
  ],
  critical_alerts: [
    "Extractives/Congo: supply_chain_abuse_scale",
    "Fast Fashion/Bangladesh: accountability_remedy_gap",
    "Big Oil/Nigeria: environmental_social_harm",
    "Tech/Surveillance: legal_jurisdiction_evasion",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_corporate_impunity_index: 6.08,
  data_sources: [
    "business_human_rights_resource_centre_corporate_abuse_tracker",
    "global_witness_corporate_accountability_annual_investigation_report",
    "un_working_group_business_human_rights_state_reports_review",
  ],
  entities: [
    { entity_id: "CI-001", name: "Extractives/Congo — Cobalt Apple/Tesla, Travail Enfants Mines & Chaînes Sans Traçabilité", country: "Afrique Centrale", composite_score: 91.9, supply_chain_abuse_scale_score: 95.0, legal_jurisdiction_evasion_score: 88.0, environmental_social_harm_score: 92.0, accountability_remedy_gap_score: 92.0, risk_level: "critique", primary_pattern: "supply_chain_abuse_scale", estimated_corporate_impunity_index: 9.19, last_updated: "2026-06-21" },
    { entity_id: "CI-002", name: "Fast Fashion/Bangladesh — Rana Plaza 1134 Morts, Marques Non Poursuivies & Due Diligence Absente", country: "Asie du Sud", composite_score: 88.95, supply_chain_abuse_scale_score: 92.0, legal_jurisdiction_evasion_score: 90.0, environmental_social_harm_score: 85.0, accountability_remedy_gap_score: 88.0, risk_level: "critique", primary_pattern: "accountability_remedy_gap", estimated_corporate_impunity_index: 8.9, last_updated: "2026-06-21" },
    { entity_id: "CI-003", name: "Big Oil/Nigeria — Shell Delta Ogoni, Marée Noires 50 Ans & Procès Hors Territoire", country: "Afrique de l'Ouest", composite_score: 87.65, supply_chain_abuse_scale_score: 88.0, legal_jurisdiction_evasion_score: 85.0, environmental_social_harm_score: 92.0, accountability_remedy_gap_score: 85.0, risk_level: "critique", primary_pattern: "environmental_social_harm", estimated_corporate_impunity_index: 8.77, last_updated: "2026-06-21" },
    { entity_id: "CI-004", name: "Tech/Surveillance — NSO/Palantir Ventes Régimes, Export Contrôle Insuffisant & Complicité", country: "Global", composite_score: 83.1, supply_chain_abuse_scale_score: 82.0, legal_jurisdiction_evasion_score: 88.0, environmental_social_harm_score: 78.0, accountability_remedy_gap_score: 85.0, risk_level: "critique", primary_pattern: "legal_jurisdiction_evasion", estimated_corporate_impunity_index: 8.31, last_updated: "2026-06-21" },
    { entity_id: "CI-005", name: "Agro-Industrie/Brésil — Déforestation Amazonie, Expulsions Peuples Indigènes & Soja/Élevage", country: "Amérique Latine", composite_score: 54.0, supply_chain_abuse_scale_score: 55.0, legal_jurisdiction_evasion_score: 52.0, environmental_social_harm_score: 58.0, accountability_remedy_gap_score: 50.0, risk_level: "élevé", primary_pattern: "environmental_social_harm", estimated_corporate_impunity_index: 5.4, last_updated: "2026-06-21" },
    { entity_id: "CI-006", name: "Finance/Paradis Fiscaux — Évasion Multinationales, Ressources États Appauvries & OCDE Lacunes", country: "Global", composite_score: 50.55, supply_chain_abuse_scale_score: 48.0, legal_jurisdiction_evasion_score: 58.0, environmental_social_harm_score: 45.0, accountability_remedy_gap_score: 52.0, risk_level: "élevé", primary_pattern: "legal_jurisdiction_evasion", estimated_corporate_impunity_index: 5.06, last_updated: "2026-06-21" },
    { entity_id: "CI-007", name: "OCCRP/Global Witness — Journalisme Enquête Corruption Corporate & Plaidoyer Due Diligence", country: "Global", composite_score: 25.85, supply_chain_abuse_scale_score: 22.0, legal_jurisdiction_evasion_score: 28.0, environmental_social_harm_score: 25.0, accountability_remedy_gap_score: 30.0, risk_level: "modéré", primary_pattern: "supply_chain_abuse_scale", estimated_corporate_impunity_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "CI-008", name: "ONU/Principes Directeurs Ruggie — Cadre Entreprises & Droits Humains 2011, Traité Négocié", country: "Global", composite_score: 4.4, supply_chain_abuse_scale_score: 4.0, legal_jurisdiction_evasion_score: 5.0, environmental_social_harm_score: 3.0, accountability_remedy_gap_score: 6.0, risk_level: "faible", primary_pattern: "accountability_remedy_gap", estimated_corporate_impunity_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporate-impunity-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
