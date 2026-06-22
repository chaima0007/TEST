import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[access-medicine-inequality-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Access Medicine Inequality Engine Agent",
  domain: "access_medicine_inequality",
  total_entities: 8,
  avg_composite: 61.68,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { patent_barrier_essential_medicine_scale: 2, price_exclusion_low_income_severity: 2, generic_drug_access_suppression: 2, research_development_neglect_diseases_poor: 2 },
  top_risk_entities: [
    "Afrique Sub-Saharienne — 50% Sans Médicaments OMS, Brevets ARV/TB Bloqués & Paludisme Non Traité",
    "USA — Insuline 900$/Mois vs 98$ Canada, Evergreening Brevets & 30M Sans Couverture",
    "Inde — TRIPS-Plus Lobbying, Section 3d Contournée & Leishmaniose/Chagas Négligés 1Md Exposés",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne: patent_barrier_essential_medicine_scale",
    "USA: price_exclusion_low_income_severity",
    "Inde: generic_drug_access_suppression",
    "Afrique Francophone/UEMOA: research_development_neglect_diseases_poor",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_access_medicine_inequality_index: 6.17,
  data_sources: [
    "msf_access_campaign_essential_medicines_patent_barrier_report",
    "who_essential_medicines_list_trips_doha_declaration_review",
    "dndi_drugs_neglected_diseases_initiative_global_access_report",
  ],
  entities: [
    { id: "AMI-001", name: "Afrique Sub-Saharienne — 50% Sans Médicaments OMS, Brevets ARV/TB Bloqués & Paludisme Non Traité", country: "Afrique", composite_score: 92.75, patent_barrier_essential_medicine_scale_score: 92.0, price_exclusion_low_income_severity_score: 95.0, generic_drug_access_suppression_score: 92.0, research_development_neglect_diseases_poor_score: 92.0, risk_level: "critique", primary_pattern: "patent_barrier_essential_medicine_scale", estimated_access_medicine_inequality_index: 9.28, last_updated: "2026-06-21" },
    { id: "AMI-002", name: "USA — Insuline 900$/Mois vs 98$ Canada, Evergreening Brevets & 30M Sans Couverture", country: "Amérique du Nord", composite_score: 89.65, patent_barrier_essential_medicine_scale_score: 88.0, price_exclusion_low_income_severity_score: 95.0, generic_drug_access_suppression_score: 90.0, research_development_neglect_diseases_poor_score: 85.0, risk_level: "critique", primary_pattern: "price_exclusion_low_income_severity", estimated_access_medicine_inequality_index: 8.97, last_updated: "2026-06-21" },
    { id: "AMI-003", name: "Inde — TRIPS-Plus Lobbying, Section 3d Contournée & Leishmaniose/Chagas Négligés 1Md Exposés", country: "Asie du Sud", composite_score: 88.85, patent_barrier_essential_medicine_scale_score: 90.0, price_exclusion_low_income_severity_score: 85.0, generic_drug_access_suppression_score: 92.0, research_development_neglect_diseases_poor_score: 88.0, risk_level: "critique", primary_pattern: "generic_drug_access_suppression", estimated_access_medicine_inequality_index: 8.89, last_updated: "2026-06-21" },
    { id: "AMI-004", name: "Afrique Francophone/UEMOA — Doha Non Implémenté, Zéro Capacité Génériques & Dépendance Totale", country: "Afrique de l'Ouest", composite_score: 88.4, patent_barrier_essential_medicine_scale_score: 88.0, price_exclusion_low_income_severity_score: 92.0, generic_drug_access_suppression_score: 88.0, research_development_neglect_diseases_poor_score: 85.0, risk_level: "critique", primary_pattern: "research_development_neglect_diseases_poor", estimated_access_medicine_inequality_index: 8.84, last_updated: "2026-06-21" },
    { id: "AMI-005", name: "Europe de l'Est — Médicaments Cancer Hors Portée, Roumanie/Bulgarie 40% Accès Restreint", country: "Europe de l'Est", composite_score: 52.15, patent_barrier_essential_medicine_scale_score: 50.0, price_exclusion_low_income_severity_score: 55.0, generic_drug_access_suppression_score: 52.0, research_development_neglect_diseases_poor_score: 52.0, risk_level: "élevé", primary_pattern: "price_exclusion_low_income_severity", estimated_access_medicine_inequality_index: 5.22, last_updated: "2026-06-21" },
    { id: "AMI-006", name: "Amérique Latine/APC-USA — Accords TRIPS-Plus Guatemala/Colombie, Brevets Cancer Inaccessibles", country: "Amérique Latine", composite_score: 51.35, patent_barrier_essential_medicine_scale_score: 50.0, price_exclusion_low_income_severity_score: 52.0, generic_drug_access_suppression_score: 55.0, research_development_neglect_diseases_poor_score: 48.0, risk_level: "élevé", primary_pattern: "patent_barrier_essential_medicine_scale", estimated_access_medicine_inequality_index: 5.14, last_updated: "2026-06-21" },
    { id: "AMI-007", name: "MSF/DNDi/Campagne Accès — Licences Obligatoires, Push Génériques & Médicaments Maladies Oubliées", country: "Global", composite_score: 25.85, patent_barrier_essential_medicine_scale_score: 22.0, price_exclusion_low_income_severity_score: 28.0, generic_drug_access_suppression_score: 25.0, research_development_neglect_diseases_poor_score: 30.0, risk_level: "modéré", primary_pattern: "generic_drug_access_suppression", estimated_access_medicine_inequality_index: 2.59, last_updated: "2026-06-21" },
    { id: "AMI-008", name: "OMS/ONU — Liste Médicaments Essentiels, Résolution TRIPS Doha 2001 & SDG 3.8 Couverture", country: "Global", composite_score: 4.4, patent_barrier_essential_medicine_scale_score: 4.0, price_exclusion_low_income_severity_score: 5.0, generic_drug_access_suppression_score: 3.0, research_development_neglect_diseases_poor_score: 6.0, risk_level: "faible", primary_pattern: "research_development_neglect_diseases_poor", estimated_access_medicine_inequality_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/access-medicine-inequality-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
