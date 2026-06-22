import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-tax-evasion-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[corporate-tax-evasion-rights-engine] SWARM_API_URL not set");

const MOCK = {
  agent: "Corporate Tax Evasion Rights Engine Agent",
  domain: "corporate_tax_evasion_rights",
  total_entities: 8,
  avg_composite: 62.04,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    tax_haven_exploitation: 4,
    profit_shifting: 1,
    public_services_defunding: 2,
    regulatory_arbitrage: 2,
  },
  top_risk_entities: [
    "Apple Inc. — 60 Mds$ Paradis Fiscaux, Condamné EU 13 Mds€",
    "Google/Alphabet — Double Irish Dutch Sandwich, 23 Mds$",
    "Amazon — Luxembourg Shell Companies, 0% Impôts Années",
  ],
  critical_alerts: [
    "Apple Inc.: tax_haven_exploitation",
    "Google/Alphabet: profit_shifting",
    "Amazon: tax_haven_exploitation",
    "Shell/BP: public_services_defunding",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_corporate_tax_evasion_rights_index: 6.20,
  data_sources: [
    "eu_commission_state_aid_decisions",
    "oxfam_tax_evasion_report_2024",
    "oecd_beps_monitoring_2024",
    "tax_justice_network_fsi_2024",
  ],
  entities: [
    {
      id: "CTE-001",
      name: "Apple Inc. — 60 Mds$ Paradis Fiscaux, Condamné EU 13 Mds€",
      country: "USA/Irlande",
      composite_score: 91.05,
      risk_level: "critique",
      primary_pattern: "tax_haven_exploitation",
      estimated_corporate_tax_evasion_rights_index: 9.11,
      last_updated: "2026-06-22",
    },
    {
      id: "CTE-002",
      name: "Google/Alphabet — Double Irish Dutch Sandwich, 23 Mds$",
      country: "USA/Pays-Bas/Irlande",
      composite_score: 90.00,
      risk_level: "critique",
      primary_pattern: "profit_shifting",
      estimated_corporate_tax_evasion_rights_index: 9.00,
      last_updated: "2026-06-22",
    },
    {
      id: "CTE-003",
      name: "Amazon — Luxembourg Shell Companies, 0% Impôts Années",
      country: "USA/Luxembourg",
      composite_score: 88.55,
      risk_level: "critique",
      primary_pattern: "tax_haven_exploitation",
      estimated_corporate_tax_evasion_rights_index: 8.86,
      last_updated: "2026-06-22",
    },
    {
      id: "CTE-004",
      name: "Shell/BP — Cayman/Bermudes, Sous-Déclaration Revenus",
      country: "UK/Pays-Bas",
      composite_score: 87.00,
      risk_level: "critique",
      primary_pattern: "public_services_defunding",
      estimated_corporate_tax_evasion_rights_index: 8.70,
      last_updated: "2026-06-22",
    },
    {
      id: "CTE-005",
      name: "Luxembourg/Cayman Islands — Hubs Tax Haven Globaux",
      country: "Luxembourg/Cayman",
      composite_score: 54.40,
      risk_level: "élevé",
      primary_pattern: "regulatory_arbitrage",
      estimated_corporate_tax_evasion_rights_index: 5.44,
      last_updated: "2026-06-22",
    },
    {
      id: "CTE-006",
      name: "Big 4 Accounting (Deloitte/EY/KPMG/PwC) — Architectes Évasion",
      country: "International",
      composite_score: 51.40,
      risk_level: "élevé",
      primary_pattern: "regulatory_arbitrage",
      estimated_corporate_tax_evasion_rights_index: 5.14,
      last_updated: "2026-06-22",
    },
    {
      id: "CTE-007",
      name: "BEPS OCDE — Pilier 15% Minimum, Application Partielle 2024",
      country: "International",
      composite_score: 28.40,
      risk_level: "modéré",
      primary_pattern: "public_services_defunding",
      estimated_corporate_tax_evasion_rights_index: 2.84,
      last_updated: "2026-06-22",
    },
    {
      id: "CTE-008",
      name: "EU Tax Transparency / CBCR — Reporting Pays par Pays",
      country: "Union Européenne",
      composite_score: 5.55,
      risk_level: "faible",
      primary_pattern: "tax_haven_exploitation",
      estimated_corporate_tax_evasion_rights_index: 0.56,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const upstream = await fetch(`${SWARM_API_URL}/corporate-tax-evasion-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 }));
  }
}
