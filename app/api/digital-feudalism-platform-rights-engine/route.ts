import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-feudalism-platform-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "digital_feudalism_platform_rights_engine",
  domain: "digital_feudalism_platform_rights",
  total_entities: 8,
  avg_composite: 62.49,
  confidence_score: 0.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    platform_monopoly_dependency: 3,
    algorithmic_wage_theft: 2,
    data_extraction_labor: 2,
    regulatory_capture: 1,
  },
  top_risk_entities: [
    { id: "DFP-001", name: "États-Unis — Big Tech Monopole, Travailleurs Gig Sans Droits, Capture Régulatoire", score: 91.25, risk: "critique" },
    { id: "DFP-002", name: "Pakistan — Freelancers Plateformes Occidentales, Frais Extraction 30%, Zéro Recours", score: 90.7, risk: "critique" },
    { id: "DFP-003", name: "Inde — 15M Livreurs Algorithmiques, Salaires Déprimés par IA, Surveillance Totale", score: 90.2, risk: "critique" },
  ],
  critical_alerts: [
    "DFP-001: États-Unis — Big Tech Monopole, Travailleurs Gig Sans Droits, Capture Régulatoire — composite 91.25",
    "DFP-002: Pakistan — Freelancers Plateformes Occidentales, Frais Extraction 30%, Zéro Recours — composite 90.7",
    "DFP-003: Inde — 15M Livreurs Algorithmiques, Salaires Déprimés par IA, Surveillance Totale — composite 90.2",
    "DFP-004: Nigeria — Banning Content Créateurs Africains, Monétisation Bloquée, Neo-Colonialisme Digital — composite 87.3",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_digital_feudalism_platform_rights_index: 6.25,
  data_sources: [
    "ilo_platform_work_global_report_2023",
    "fairwork_foundation_gig_economy_2024",
    "eu_platform_workers_directive_2024",
    "un_special_rapporteur_digital_rights_2023",
  ],
  entities: [
    {
      id: "DFP-001",
      name: "États-Unis — Big Tech Monopole, Travailleurs Gig Sans Droits, Capture Régulatoire",
      country: "États-Unis",
      platform_monopoly_dependency_score: 93.0,
      algorithmic_wage_theft_score: 91.0,
      data_extraction_labor_rights_score: 90.0,
      regulatory_capture_accountability_score: 89.0,
      composite_score: 91.25,
      risk_level: "critique",
      primary_pattern: "Amazon/Meta/Google monopole 70% marché publicitaire, Uber/DoorDash 1.7M gig workers sans protection sociale, lobbying 800M$ anti-régulation",
      estimated_digital_feudalism_platform_rights_index: 9.13,
      last_updated: "2026-06-21",
    },
    {
      id: "DFP-002",
      name: "Pakistan — Freelancers Plateformes Occidentales, Frais Extraction 30%, Zéro Recours",
      country: "Pakistan",
      platform_monopoly_dependency_score: 89.0,
      algorithmic_wage_theft_score: 93.0,
      data_extraction_labor_rights_score: 91.0,
      regulatory_capture_accountability_score: 87.0,
      composite_score: 90.7,
      risk_level: "critique",
      primary_pattern: "4M freelancers sur Upwork/Fiverr, commissions 20-30% extraites vers Silicon Valley, désactivations algorithmiques arbitraires sans appel, protections travail inexistantes",
      estimated_digital_feudalism_platform_rights_index: 9.07,
      last_updated: "2026-06-21",
    },
    {
      id: "DFP-003",
      name: "Inde — 15M Livreurs Algorithmiques, Salaires Déprimés par IA, Surveillance Totale",
      country: "Inde",
      platform_monopoly_dependency_score: 88.0,
      algorithmic_wage_theft_score: 90.0,
      data_extraction_labor_rights_score: 92.0,
      regulatory_capture_accountability_score: 86.0,
      composite_score: 89.7,
      risk_level: "critique",
      primary_pattern: "Zomato/Swiggy 15M gig workers, algorithme fixe tarifs sous salaire minimum, tracking GPS continu 24h, contrats imposés unilatéralement sans syndicat",
      estimated_digital_feudalism_platform_rights_index: 8.97,
      last_updated: "2026-06-21",
    },
    {
      id: "DFP-004",
      name: "Nigeria — Banning Content Créateurs Africains, Monétisation Bloquée, Neo-Colonialisme Digital",
      country: "Nigeria",
      platform_monopoly_dependency_score: 85.0,
      algorithmic_wage_theft_score: 87.0,
      data_extraction_labor_rights_score: 88.0,
      regulatory_capture_accountability_score: 90.0,
      composite_score: 87.3,
      risk_level: "critique",
      primary_pattern: "TikTok/YouTube démonétisation 10x plus fréquente créateurs africains, algorithme biaisé réduisant portée contenus africains 68%, valeur extraite sans redistribution",
      estimated_digital_feudalism_platform_rights_index: 8.73,
      last_updated: "2026-06-21",
    },
    {
      id: "DFP-005",
      name: "Union Européenne — DSA/DMA Résistance Plateformes, Amendes Insuffisantes",
      country: "Union Européenne",
      platform_monopoly_dependency_score: 52.0,
      algorithmic_wage_theft_score: 50.0,
      data_extraction_labor_rights_score: 54.0,
      regulatory_capture_accountability_score: 55.0,
      composite_score: 52.65,
      risk_level: "élevé",
      primary_pattern: "DSA/DMA adopté mais Meta/Google résistent application, amendes RGPD plafonnées 4% CA mondiales insuffisantes, Platform Workers Directive négociée sous pression",
      estimated_digital_feudalism_platform_rights_index: 5.27,
      last_updated: "2026-06-21",
    },
    {
      id: "DFP-006",
      name: "Royaume-Uni — Gig Economy Post-Brexit, Uber Arrêt Cour Suprême Non Appliqué",
      country: "Royaume-Uni",
      platform_monopoly_dependency_score: 54.0,
      algorithmic_wage_theft_score: 56.0,
      data_extraction_labor_rights_score: 51.0,
      regulatory_capture_accountability_score: 53.0,
      composite_score: 53.7,
      risk_level: "élevé",
      primary_pattern: "Arrêt Cour Suprême 2021 Uber partiellement contourné, 5.5M gig workers, Employment Rights Bill 2024 sous pression lobby plateforme, CMA insuffisant",
      estimated_digital_feudalism_platform_rights_index: 5.37,
      last_updated: "2026-06-21",
    },
    {
      id: "DFP-007",
      name: "Mexique — Rappi/DiDi Sans Sécurité Sociale, Accident = Ruine pour Livreurs",
      country: "Mexique",
      platform_monopoly_dependency_score: 29.0,
      algorithmic_wage_theft_score: 31.0,
      data_extraction_labor_rights_score: 27.0,
      regulatory_capture_accountability_score: 28.0,
      composite_score: 28.95,
      risk_level: "modéré",
      primary_pattern: "800k livreurs Rappi/DiDi/Uber sans IMSS, accidents non couverts, réforme travail plateforme bloquée par lobbying, dépendance économique totale sans recours",
      estimated_digital_feudalism_platform_rights_index: 2.9,
      last_updated: "2026-06-21",
    },
    {
      id: "DFP-008",
      name: "France — Charte Uber Refusée, Statut ARPE Protections Partielles",
      country: "France",
      platform_monopoly_dependency_score: 8.0,
      algorithmic_wage_theft_score: 7.0,
      data_extraction_labor_rights_score: 9.0,
      regulatory_capture_accountability_score: 6.0,
      composite_score: 7.75,
      risk_level: "faible",
      primary_pattern: "Cour Cassation requalification salariés, ARPE protection accidents, charte Uber refusée conseil constitutionnel, modèle avancé Europe protection gig workers",
      estimated_digital_feudalism_platform_rights_index: 0.78,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-feudalism-platform-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data.payload ?? data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
