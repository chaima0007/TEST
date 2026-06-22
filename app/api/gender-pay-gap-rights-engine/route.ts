import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[gender-pay-gap-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}
const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[gender-pay-gap-rights-engine] SWARM_API_URL not set");

const FALLBACK = {
  agent: "Gender Pay Gap Rights Engine",
  domain: "gender_pay_gap_rights",
  avg_composite: 61.33,
  confidence_score: 0.86,
  total_entities: 8,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  critical_alerts: [
    "Pakistan:wage_discrimination",
    "Yemen:occupational_segregation",
    "Afghanistan:glass_ceiling",
    "Saudi Arabia:wage_discrimination",
  ],
  data_sources: [
    "ilo_gender_pay_gap_report_2024",
    "wef_global_gender_gap_index_2024",
    "oxfam_womens_economic_rights_2024",
    "eu_gender_equality_index_2024",
  ],
  estimated_gender_pay_gap_rights_index: 6.13,
  entities: [
    { id: "GPG-001", name: "Pakistan — Femmes 82% Moins Payées, Participation 20%", country: "Pakistan", composite_score: 89.30, risk_level: "critique", primary_pattern: "wage_discrimination", estimated_gender_pay_gap_rights_index: 8.93 },
    { id: "GPG-002", name: "Yemen — 94% Femmes Exclues Économie Formelle Post-Guerre", country: "Yémen", composite_score: 88.10, risk_level: "critique", primary_pattern: "occupational_segregation", estimated_gender_pay_gap_rights_index: 8.81 },
    { id: "GPG-003", name: "Afghanistan — Femmes Interdites Travailler Post-Taliban", country: "Afghanistan", composite_score: 93.30, risk_level: "critique", primary_pattern: "glass_ceiling", estimated_gender_pay_gap_rights_index: 9.33 },
    { id: "GPG-004", name: "Saudi Arabia — Ségrégation Emploi, Dépendance Tuteur", country: "Arabie Saoudite", composite_score: 79.30, risk_level: "critique", primary_pattern: "wage_discrimination", estimated_gender_pay_gap_rights_index: 7.93 },
    { id: "GPG-005", name: "India — Écart Salarial 34%, Harcèlement, Verre Plafond", country: "Inde", composite_score: 53.60, risk_level: "élevé", primary_pattern: "glass_ceiling", estimated_gender_pay_gap_rights_index: 5.36 },
    { id: "GPG-006", name: "USA — 82 Cents/Dollar, STEM Gap, Maternité Non Rémunérée", country: "États-Unis", composite_score: 48.55, risk_level: "élevé", primary_pattern: "unpaid_care_work_gap", estimated_gender_pay_gap_rights_index: 4.86 },
    { id: "GPG-007", name: "EU Moyenne — Directive Parité, 14.1% Gap, Progrès Partiels", country: "Union Européenne", composite_score: 28.90, risk_level: "modéré", primary_pattern: "wage_discrimination", estimated_gender_pay_gap_rights_index: 2.89 },
    { id: "GPG-008", name: "Iceland — Loi Equal Pay 2018, Certification Légale, Rang 1", country: "Islande", composite_score: 9.55, risk_level: "faible", primary_pattern: "wage_discrimination", estimated_gender_pay_gap_rights_index: 0.96 },
  ],
};

export async function GET() {
  try {
    const upstream = await fetch(`${SWARM_API_URL}/gender-pay-gap-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(FALLBACK), { status: 502 }));
  }
}
