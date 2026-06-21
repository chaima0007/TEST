import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[water-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Water Rights Engine Agent",
  domain: "water_rights",
  total_entities: 8,
  avg_composite: 59.45,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { access_denial_scale: 3, privatization_commodification: 2, pollution_industrial_contamination: 1, transboundary_conflict_governance: 2 },
  top_risk_entities: [
    "Gaza/Palestine — Blocus Eau, Infrastructures Détruites, 90% Eau Non Potable & Déshydratation",
    "Yémen — Guerre Infrastructures Eau, Choléra 2.5M Cas & Puits Bombardés",
    "Afrique Sub-Saharienne — 400M Sans Eau Potable, Marche 6h/jour & Maladies Hydriques",
  ],
  critical_alerts: [
    "Gaza/Palestine: access_denial_scale",
    "Yémen: access_denial_scale",
    "Afrique Sub-Saharienne: privatization_commodification",
    "Bolivie/Cochabamba: privatization_commodification",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_water_rights_index: 5.95,
  data_sources: [
    "un_special_rapporteur_water_sanitation_annual_reports",
    "water_justice_coalition_global_privatization_audit",
    "who_unicef_jmp_water_sanitation_hygiene_progress_report",
  ],
  entities: [
    { id: "WR-001", name: "Gaza/Palestine — Blocus Eau, Infrastructures Détruites, 90% Eau Non Potable & Déshydratation", country: "Moyen-Orient", composite_score: 91.0, access_denial_scale_score: 95.0, privatization_commodification_score: 82.0, pollution_industrial_contamination_score: 92.0, transboundary_conflict_governance_score: 95.0, risk_level: "critique", primary_pattern: "access_denial_scale", estimated_water_rights_index: 9.1, last_updated: "2026-06-21" },
    { id: "WR-002", name: "Yémen — Guerre Infrastructures Eau, Choléra 2.5M Cas & Puits Bombardés", country: "Moyen-Orient", composite_score: 87.1, access_denial_scale_score: 92.0, privatization_commodification_score: 78.0, pollution_industrial_contamination_score: 88.0, transboundary_conflict_governance_score: 90.0, risk_level: "critique", primary_pattern: "access_denial_scale", estimated_water_rights_index: 8.71, last_updated: "2026-06-21" },
    { id: "WR-003", name: "Afrique Sub-Saharienne — 400M Sans Eau Potable, Marche 6h/jour & Maladies Hydriques", country: "Afrique Sub-Saharienne", composite_score: 84.15, access_denial_scale_score: 88.0, privatization_commodification_score: 85.0, pollution_industrial_contamination_score: 82.0, transboundary_conflict_governance_score: 80.0, risk_level: "critique", primary_pattern: "privatization_commodification", estimated_water_rights_index: 8.42, last_updated: "2026-06-21" },
    { id: "WR-004", name: "Bolivie/Cochabamba — Privatisation Suez, Guerre de l'Eau 2000 & Multinationales Ressources", country: "Amérique Latine", composite_score: 80.35, access_denial_scale_score: 80.0, privatization_commodification_score: 88.0, pollution_industrial_contamination_score: 75.0, transboundary_conflict_governance_score: 78.0, risk_level: "critique", primary_pattern: "privatization_commodification", estimated_water_rights_index: 8.04, last_updated: "2026-06-21" },
    { id: "WR-005", name: "Inde/Gange — Pollution Industrielle, Sécheresses Agricoles & Tensions Inter-États", country: "Asie du Sud", composite_score: 53.0, access_denial_scale_score: 52.0, privatization_commodification_score: 50.0, pollution_industrial_contamination_score: 58.0, transboundary_conflict_governance_score: 52.0, risk_level: "élevé", primary_pattern: "pollution_industrial_contamination", estimated_water_rights_index: 5.3, last_updated: "2026-06-21" },
    { id: "WR-006", name: "Nil/Barrage GERD — Éthiopie vs Égypte/Soudan, Traités Obsolètes & Crise Hydropolitique", country: "Afrique du Nord-Est", composite_score: 49.75, access_denial_scale_score: 48.0, privatization_commodification_score: 45.0, pollution_industrial_contamination_score: 50.0, transboundary_conflict_governance_score: 58.0, risk_level: "élevé", primary_pattern: "transboundary_conflict_governance", estimated_water_rights_index: 4.98, last_updated: "2026-06-21" },
    { id: "WR-007", name: "Water Justice Movement — Coalition Mondiale, Déprivatisation & Droit Constitutionnel Eau", country: "Global", composite_score: 25.85, access_denial_scale_score: 22.0, privatization_commodification_score: 28.0, pollution_industrial_contamination_score: 25.0, transboundary_conflict_governance_score: 30.0, risk_level: "modéré", primary_pattern: "access_denial_scale", estimated_water_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "WR-008", name: "ONU/Résolution 64/292 — Droit Humain à l'Eau 2010, Rapporteur Spécial & Mécanismes Suivi", country: "Global", composite_score: 4.4, access_denial_scale_score: 4.0, privatization_commodification_score: 5.0, pollution_industrial_contamination_score: 3.0, transboundary_conflict_governance_score: 6.0, risk_level: "faible", primary_pattern: "transboundary_conflict_governance", estimated_water_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
