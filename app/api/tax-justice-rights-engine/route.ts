import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[tax-justice-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[tax-justice-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Tax Justice Rights Engine Agent",
  domain: "tax_justice_rights",
  total_entities: 8,
  avg_composite: 60.67,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Îles Caïmans — Paradis Fiscal #1 FSI, 0% Impôt Sociétés & 1600 Milliards USD Offshore",
    "Panama — Pandora Papers, 336k Sociétés Fantômes & Déprivation Services Publics Populations",
    "Luxembourg — Double Irish Dutch Sandwich, Rulings Apple/Amazon & Manque à Gagner 120 Mds€ UE",
  ],
  critical_alerts: [
    "Îles Caïmans: tax_haven_exploitation_score",
    "Panama: corporate_tax_evasion_score",
    "Luxembourg: corporate_tax_evasion_score",
    "Nigeria: public_service_deprivation_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_tax_justice_rights_index: 6.07,
  entities: [
    {
      entity_id: "TJR-001",
      name: "Îles Caïmans — Paradis Fiscal #1 FSI, 0% Impôt Sociétés & 1600 Milliards USD Offshore",
      country: "Îles Caïmans",
      tax_haven_exploitation_score: 90.0,
      public_service_deprivation_score: 87.0,
      corporate_tax_evasion_score: 89.0,
      wealth_inequality_gap_score: 86.0,
      composite_score: 88.45,
      risk_level: "critique",
      primary_pattern: "tax_haven_exploitation_score",
      estimated_tax_justice_rights_index: 8.85,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "TJR-002",
      name: "Panama — Pandora Papers, 336k Sociétés Fantômes & Déprivation Services Publics Populations",
      country: "Panama",
      tax_haven_exploitation_score: 86.0,
      public_service_deprivation_score: 84.0,
      corporate_tax_evasion_score: 88.0,
      wealth_inequality_gap_score: 83.0,
      composite_score: 85.5,
      risk_level: "critique",
      primary_pattern: "corporate_tax_evasion_score",
      estimated_tax_justice_rights_index: 8.55,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "TJR-003",
      name: "Luxembourg — Double Irish Dutch Sandwich, Rulings Apple/Amazon & Manque à Gagner 120 Mds€ UE",
      country: "Luxembourg",
      tax_haven_exploitation_score: 84.0,
      public_service_deprivation_score: 81.0,
      corporate_tax_evasion_score: 86.0,
      wealth_inequality_gap_score: 80.0,
      composite_score: 82.95,
      risk_level: "critique",
      primary_pattern: "corporate_tax_evasion_score",
      estimated_tax_justice_rights_index: 8.30,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "TJR-004",
      name: "Nigeria — Évasion Fiscale 15 Mds USD/An Multinationales Pétrolières, Inégalités Extrêmes",
      country: "Nigeria",
      tax_haven_exploitation_score: 80.0,
      public_service_deprivation_score: 83.0,
      corporate_tax_evasion_score: 79.0,
      wealth_inequality_gap_score: 82.0,
      composite_score: 80.85,
      risk_level: "critique",
      primary_pattern: "public_service_deprivation_score",
      estimated_tax_justice_rights_index: 8.09,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "TJR-005",
      name: "USA — Déductions Fiscales Corporations, Gini 0.49 & Sous-Investissement Services Sociaux",
      country: "USA",
      tax_haven_exploitation_score: 54.0,
      public_service_deprivation_score: 56.0,
      corporate_tax_evasion_score: 58.0,
      wealth_inequality_gap_score: 57.0,
      composite_score: 56.15,
      risk_level: "élevé",
      primary_pattern: "corporate_tax_evasion_score",
      estimated_tax_justice_rights_index: 5.62,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "TJR-006",
      name: "Pays-Bas — Boîtes aux Lettres Multinationales, 4500 Milliards Flux Passifs & BEPS Partiel",
      country: "Pays-Bas",
      tax_haven_exploitation_score: 49.0,
      public_service_deprivation_score: 42.0,
      corporate_tax_evasion_score: 51.0,
      wealth_inequality_gap_score: 44.0,
      composite_score: 46.8,
      risk_level: "élevé",
      primary_pattern: "corporate_tax_evasion_score",
      estimated_tax_justice_rights_index: 4.68,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "TJR-007",
      name: "Brésil — Exemption Dividendes, Inégalité Fiscale Revenus Travail vs Capital & Réforme Partielle",
      country: "Brésil",
      tax_haven_exploitation_score: 33.0,
      public_service_deprivation_score: 35.0,
      corporate_tax_evasion_score: 31.0,
      wealth_inequality_gap_score: 36.0,
      composite_score: 33.45,
      risk_level: "modéré",
      primary_pattern: "wealth_inequality_gap_score",
      estimated_tax_justice_rights_index: 3.35,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "TJR-008",
      name: "Danemark — Taux Imposition Effectif Élevé, Transparence Registres & OCDE BEPS Conforme",
      country: "Danemark",
      tax_haven_exploitation_score: 12.0,
      public_service_deprivation_score: 10.0,
      corporate_tax_evasion_score: 11.0,
      wealth_inequality_gap_score: 13.0,
      composite_score: 11.55,
      risk_level: "faible",
      primary_pattern: "tax_haven_exploitation_score",
      estimated_tax_justice_rights_index: 1.16,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/tax-justice-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
