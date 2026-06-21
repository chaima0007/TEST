import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[slavery-reparations-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Slavery Reparations Engine Agent",
  domain: "slavery_reparations",
  total_entities: 8,
  avg_composite: 61.42,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { restitution_refusal_entrenchment: 3, historical_atrocity_scale: 1, intergenerational_harm_persistence: 1, institutional_accountability_gap: 3 },
  top_risk_entities: [
    "USA — 246 Ans Esclavage, 4M Afro-Américains, HR40 Bloqué 35 Ans & Écart Richesse 10:1",
    "UK/Caraïbes — CARICOM 14 Nations, £20M Indemnités Propriétaires 1833 & Zéro Réparation Descendants",
    "France/Haïti — Dette Odieuse 90M Francs 1825, 21 Milliards USD Modernes & Appauvrissement Durable",
  ],
  critical_alerts: [
    "USA: restitution_refusal_entrenchment",
    "UK/Caraïbes: restitution_refusal_entrenchment",
    "France/Haïti: historical_atrocity_scale",
    "Brésil: intergenerational_harm_persistence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_slavery_reparations_index: 6.14,
  data_sources: [
    "caricom_reparations_commission_ten_point_plan_report",
    "un_durban_declaration_programme_action_slavery_heritage",
    "thomas_craemer_slavery_reparations_economic_quantification_study",
  ],
  entities: [
    { entity_id: "SR-001", name: "USA — 246 Ans Esclavage, 4M Afro-Américains, HR40 Bloqué 35 Ans & Écart Richesse 10:1", country: "Amérique du Nord", composite_score: 93.25, historical_atrocity_scale_score: 95.0, intergenerational_harm_persistence_score: 95.0, restitution_refusal_entrenchment_score: 92.0, institutional_accountability_gap_score: 90.0, risk_level: "critique", primary_pattern: "restitution_refusal_entrenchment", estimated_slavery_reparations_index: 9.33, last_updated: "2026-06-21" },
    { entity_id: "SR-002", name: "UK/Caraïbes — CARICOM 14 Nations, £20M Indemnités Propriétaires 1833 & Zéro Réparation Descendants", country: "Caraïbes", composite_score: 90.7, historical_atrocity_scale_score: 92.0, intergenerational_harm_persistence_score: 90.0, restitution_refusal_entrenchment_score: 92.0, institutional_accountability_gap_score: 88.0, risk_level: "critique", primary_pattern: "restitution_refusal_entrenchment", estimated_slavery_reparations_index: 9.07, last_updated: "2026-06-21" },
    { entity_id: "SR-003", name: "France/Haïti — Dette Odieuse 90M Francs 1825, 21 Milliards USD Modernes & Appauvrissement Durable", country: "Caraïbes", composite_score: 88.6, historical_atrocity_scale_score: 90.0, intergenerational_harm_persistence_score: 88.0, restitution_refusal_entrenchment_score: 88.0, institutional_accountability_gap_score: 88.0, risk_level: "critique", primary_pattern: "historical_atrocity_scale", estimated_slavery_reparations_index: 8.86, last_updated: "2026-06-21" },
    { entity_id: "SR-004", name: "Brésil — 3.8M Esclaves Africains, 13 Mai 1888 Tardif, Inégalités Raciales Structurelles & Refus Etat", country: "Amérique Latine", composite_score: 85.3, historical_atrocity_scale_score: 88.0, intergenerational_harm_persistence_score: 85.0, restitution_refusal_entrenchment_score: 85.0, institutional_accountability_gap_score: 82.0, risk_level: "critique", primary_pattern: "intergenerational_harm_persistence", estimated_slavery_reparations_index: 8.53, last_updated: "2026-06-21" },
    { entity_id: "SR-005", name: "Portugal — Premier Négrier Européen, 5.8M Africains Déportés & Aucun Mécanisme Réparation", country: "Europe", composite_score: 53.65, historical_atrocity_scale_score: 55.0, intergenerational_harm_persistence_score: 52.0, restitution_refusal_entrenchment_score: 55.0, institutional_accountability_gap_score: 52.0, risk_level: "élevé", primary_pattern: "institutional_accountability_gap", estimated_slavery_reparations_index: 5.37, last_updated: "2026-06-21" },
    { entity_id: "SR-006", name: "Pays-Bas — NiNsee Fermé 2012, Excuses 2022 Sans Réparation & WIC Commerce Triangle", country: "Europe", composite_score: 49.6, historical_atrocity_scale_score: 50.0, intergenerational_harm_persistence_score: 48.0, restitution_refusal_entrenchment_score: 52.0, institutional_accountability_gap_score: 48.0, risk_level: "élevé", primary_pattern: "restitution_refusal_entrenchment", estimated_slavery_reparations_index: 4.96, last_updated: "2026-06-21" },
    { entity_id: "SR-007", name: "CARICOM/Commission Réparations — Plan 10 Points, Dialogue Diplomatique & Standards Réparatoires", country: "Global", composite_score: 25.85, historical_atrocity_scale_score: 22.0, intergenerational_harm_persistence_score: 28.0, restitution_refusal_entrenchment_score: 25.0, institutional_accountability_gap_score: 30.0, risk_level: "modéré", primary_pattern: "institutional_accountability_gap", estimated_slavery_reparations_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "SR-008", name: "ONU/DDPA — Durban 2001, Reconnaissance Esclavage Crime Humanité & Cadre Réparatoire International", country: "Global", composite_score: 4.4, historical_atrocity_scale_score: 4.0, intergenerational_harm_persistence_score: 5.0, restitution_refusal_entrenchment_score: 3.0, institutional_accountability_gap_score: 6.0, risk_level: "faible", primary_pattern: "institutional_accountability_gap", estimated_slavery_reparations_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/slavery-reparations-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
