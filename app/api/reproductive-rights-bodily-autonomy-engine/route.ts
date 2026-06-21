import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[reproductive-rights-bodily-autonomy-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Reproductive Rights Bodily Autonomy Engine Agent",
  domain: "reproductive_rights_bodily_autonomy",
  total_entities: 8,
  avg_composite: 61.51,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { abortion_criminalization_ban_severity: 3, maternal_mortality_healthcare_denial: 1, reproductive_autonomy_legal_protection_deficit_gap: 2, forced_sterilization_contraception_coercion_scale: 2 },
  top_risk_entities: ["El Salvador — Avortement Interdit Même Viol/Vie Mère, 30+ Femmes Emprisonnées Fausses Couches, Peines 40 Ans & ONG Criminalisées", "Nicaragua — Avortement Zéro Exception Post-2006, Femmes Mortes Chimiothérapie Refusée, Médecins Poursuivis & Opposition Étouffée", "Pologne/Post-Roe — Quasi-Interdiction Avortement 2021, Izabela Décédée Sepsis, Médecins Refusant Soins & Femmes Voyageant Étranger"],
  critical_alerts: ["El Salvador: abortion_criminalization_ban_severity", "Nicaragua: abortion_criminalization_ban_severity", "Pologne/Post-Roe: maternal_mortality_healthcare_denial", "USA/Dobbs: reproductive_autonomy_legal_protection_deficit_gap"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_reproductive_rights_bodily_autonomy_index: 6.15,
  data_sources: ["who_safe_abortion_guidelines", "center_reproductive_rights_global_report", "amnesty_international_reproductive_rights_report"],
  entities: [
    { id: "RBA-001", name: "El Salvador — Avortement Interdit Même Viol/Vie Mère, 30+ Femmes Emprisonnées Fausses Couches, Peines 40 Ans & ONG Criminalisées", country: "El Salvador", composite_score: 93.55, abortion_criminalization_ban_severity_score: 95.0, forced_sterilization_contraception_coercion_scale_score: 93.0, maternal_mortality_healthcare_denial_score: 92.0, reproductive_autonomy_legal_protection_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "abortion_criminalization_ban_severity", estimated_reproductive_rights_bodily_autonomy_index: 9.36, last_updated: "2026-06-21" },
    { id: "RBA-002", name: "Nicaragua — Avortement Zéro Exception Post-2006, Femmes Mortes Chimiothérapie Refusée, Médecins Poursuivis & Opposition Étouffée", country: "Nicaragua", composite_score: 89.65, abortion_criminalization_ban_severity_score: 91.0, forced_sterilization_contraception_coercion_scale_score: 89.0, maternal_mortality_healthcare_denial_score: 90.0, reproductive_autonomy_legal_protection_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "abortion_criminalization_ban_severity", estimated_reproductive_rights_bodily_autonomy_index: 8.96, last_updated: "2026-06-21" },
    { id: "RBA-003", name: "Pologne/Post-Roe — Quasi-Interdiction Avortement 2021, Izabela Décédée Sepsis, Médecins Refusant Soins & Femmes Voyageant Étranger", country: "Pologne", composite_score: 86.8, abortion_criminalization_ban_severity_score: 87.0, forced_sterilization_contraception_coercion_scale_score: 85.0, maternal_mortality_healthcare_denial_score: 89.0, reproductive_autonomy_legal_protection_deficit_gap_score: 86.0, risk_level: "critique", primary_pattern: "maternal_mortality_healthcare_denial", estimated_reproductive_rights_bodily_autonomy_index: 8.68, last_updated: "2026-06-21" },
    { id: "RBA-004", name: "USA/Dobbs — Roe v. Wade Renversé 2022, 14 États Interdiction Totale, Femmes Traversant Frontières & Médecins Poursuite Criminelle", country: "USA", composite_score: 83.45, abortion_criminalization_ban_severity_score: 84.0, forced_sterilization_contraception_coercion_scale_score: 82.0, maternal_mortality_healthcare_denial_score: 83.0, reproductive_autonomy_legal_protection_deficit_gap_score: 85.0, risk_level: "critique", primary_pattern: "reproductive_autonomy_legal_protection_deficit_gap", estimated_reproductive_rights_bodily_autonomy_index: 8.35, last_updated: "2026-06-21" },
    { id: "RBA-005", name: "Inde/Stérilisation — Camps Stérilisation Forcée Femmes Pauvres, Décès Post-Op 2014 Chhattisgarh, Quotas Gouvernement & Dalits Ciblées", country: "Inde", composite_score: 55.55, abortion_criminalization_ban_severity_score: 56.0, forced_sterilization_contraception_coercion_scale_score: 57.0, maternal_mortality_healthcare_denial_score: 54.0, reproductive_autonomy_legal_protection_deficit_gap_score: 55.0, risk_level: "élevé", primary_pattern: "forced_sterilization_contraception_coercion_scale", estimated_reproductive_rights_bodily_autonomy_index: 5.55, last_updated: "2026-06-21" },
    { id: "RBA-006", name: "Chine/Politique — Fin Politique Enfant Unique, Naissances Forcées 3 Enfants, Stérilisation Uyghures 2019-20 & Avortements Tardifs Forcés", country: "Chine", composite_score: 52.45, abortion_criminalization_ban_severity_score: 52.0, forced_sterilization_contraception_coercion_scale_score: 54.0, maternal_mortality_healthcare_denial_score: 51.0, reproductive_autonomy_legal_protection_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "forced_sterilization_contraception_coercion_scale", estimated_reproductive_rights_bodily_autonomy_index: 5.25, last_updated: "2026-06-21" },
    { id: "RBA-007", name: "OMS/IPPF — Standards OMS Avortement Sécurisé 2022, IPPF Global, CEDAW Comité & Lignes Directrices Contraception", country: "Global", composite_score: 26.6, abortion_criminalization_ban_severity_score: 27.0, forced_sterilization_contraception_coercion_scale_score: 26.0, maternal_mortality_healthcare_denial_score: 28.0, reproductive_autonomy_legal_protection_deficit_gap_score: 25.0, risk_level: "modéré", primary_pattern: "reproductive_autonomy_legal_protection_deficit_gap", estimated_reproductive_rights_bodily_autonomy_index: 2.66, last_updated: "2026-06-21" },
    { id: "RBA-008", name: "ONU/PIDESC — PIDESC Art.12 Santé, CEDAW Art.12 Femmes, Comité DESC & SDG 3.1 Mortalité Maternelle", country: "Global", composite_score: 4.0, abortion_criminalization_ban_severity_score: 4.0, forced_sterilization_contraception_coercion_scale_score: 4.0, maternal_mortality_healthcare_denial_score: 4.0, reproductive_autonomy_legal_protection_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "abortion_criminalization_ban_severity", estimated_reproductive_rights_bodily_autonomy_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/reproductive-rights-bodily-autonomy-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
