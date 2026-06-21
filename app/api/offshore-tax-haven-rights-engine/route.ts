import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[offshore-tax-haven-rights-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  domain: "offshore_tax_haven_rights",
  generated_at: new Date().toISOString(),
  accent: "#0e7490",
  avg_composite: 62.26,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    { id: "OTH-001", name: "Îles Caïmans — 0% Impôt, 100K Entreprises, Services Publics Mondiaux Saignés", composite_score: 91.60, risk_level: "critique", tax_avoidance_scale_score: 94, public_service_underfunding_score: 91, inequality_amplification_score: 89, corporate_transparency_deficit_score: 92, estimated_offshore_tax_haven_rights_index: 9.16 },
    { id: "OTH-002", name: "Luxembourg — Rulings Fiscaux Secrets, 4000 Entreprises Fortune 500", composite_score: 87.40, risk_level: "critique", tax_avoidance_scale_score: 88, public_service_underfunding_score: 85, inequality_amplification_score: 87, corporate_transparency_deficit_score: 90, estimated_offshore_tax_haven_rights_index: 8.74 },
    { id: "OTH-003", name: "Îles Vierges Britanniques — 400K Sociétés Écrans, Corruption & Trafic", composite_score: 91.15, risk_level: "critique", tax_avoidance_scale_score: 92, public_service_underfunding_score: 88, inequality_amplification_score: 91, corporate_transparency_deficit_score: 94, estimated_offshore_tax_haven_rights_index: 9.11 },
    { id: "OTH-004", name: "Suisse — Secret Bancaire Résiduel, Évasion Milliardaires Globaux", composite_score: 82.90, risk_level: "critique", tax_avoidance_scale_score: 85, public_service_underfunding_score: 78, inequality_amplification_score: 86, corporate_transparency_deficit_score: 82, estimated_offshore_tax_haven_rights_index: 8.29 },
    { id: "OTH-005", name: "Dubai/EAU — Golden Visa Oligarques, Sanctionnés Russes & Blanchiment", composite_score: 58.55, risk_level: "élevé", tax_avoidance_scale_score: 58, public_service_underfunding_score: 55, inequality_amplification_score: 60, corporate_transparency_deficit_score: 62, estimated_offshore_tax_haven_rights_index: 5.86 },
    { id: "OTH-006", name: "Singapour — Hub Asie Évasion Fiscale, Familles Riches Chinoises & Indiennes", composite_score: 53.40, risk_level: "élevé", tax_avoidance_scale_score: 55, public_service_underfunding_score: 48, inequality_amplification_score: 58, corporate_transparency_deficit_score: 52, estimated_offshore_tax_haven_rights_index: 5.34 },
    { id: "OTH-007", name: "Irlande — Taux 12.5%, Apple 13B€ Remboursé, GAFA Optimisation", composite_score: 26.65, risk_level: "modéré", tax_avoidance_scale_score: 30, public_service_underfunding_score: 25, inequality_amplification_score: 28, corporate_transparency_deficit_score: 22, estimated_offshore_tax_haven_rights_index: 2.66 },
    { id: "OTH-008", name: "Danemark — Pilier 2 OCDE 15% Adopté, Registre Bénéficiaires Publics", composite_score: 6.45, risk_level: "faible", tax_avoidance_scale_score: 7, public_service_underfunding_score: 5, inequality_amplification_score: 6, corporate_transparency_deficit_score: 8, estimated_offshore_tax_haven_rights_index: 0.64 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/offshore-tax-haven-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
