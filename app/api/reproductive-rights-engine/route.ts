import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[reproductive-rights-engine] SWARM_API_URL non défini — mode mock activé");
}

const MOCK = {
  agent: "Reproductive Rights Engine Agent",
  domain: "reproductive_rights",
  total_entities: 8,
  avg_composite: 61.11,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: { abortion_access_criminalization_severity: 5, maternal_mortality_healthcare_gap: 2, contraception_sex_education_exclusion: 1 },
  top_risk_entities: [
    "Afrique Sub-Saharienne — Avortement Illégal 90% Pays, Mortalité 545/100k & Stérilisation Forcée",
    "Amérique Latine — El Salvador/Nicaragua Avortement Total Ban & Emprisonnement Fausses Couches",
    "Asie du Sud/Inde — Stérilisation Forcée Femmes Pauvres, Mortalité Rurale & Contraception Inégale",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne: abortion_access_criminalization_severity",
    "Amérique Latine: abortion_access_criminalization_severity",
    "Asie du Sud/Inde: maternal_mortality_healthcare_gap",
    "USA post-Dobbs: abortion_access_criminalization_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_reproductive_rights_index: 6.11,
  data_sources: [
    "who_global_abortion_policies_database_unsafe_abortion_report",
    "guttmacher_institute_abortion_worldwide_report_incidence_safety",
    "amnesty_international_bodily_autonomy_reproductive_rights_report",
  ],
  entities: [
    { id: "RPR-001", name: "Afrique Sub-Saharienne — Avortement Illégal 90% Pays, Mortalité 545/100k & Stérilisation Forcée", country: "Afrique Sub-Saharienne", sector: "Avortement Illégal ou Très Restreint 90% Pays Afrique Sub-Saharienne WHO, Mortalité Maternelle 545/100 000 Naissances OMS 2023, Stérilisation Forcée Femmes Pauvres & Accès Contraception 25%", composite_score: 92.75, abortion_access_criminalization_severity_score: 96.0, maternal_mortality_healthcare_gap_score: 92.0, contraception_sex_education_exclusion_score: 91.0, forced_sterilization_coercion_scale_score: 91.0, risk_level: "critique", primary_pattern: "abortion_access_criminalization_severity", estimated_reproductive_rights_index: 9.28, last_updated: "2026-06-21" },
    { id: "RPR-002", name: "Amérique Latine — El Salvador/Nicaragua Avortement Total Ban & Emprisonnement Fausses Couches", country: "Amérique Latine", sector: "El Salvador/Nicaragua Avortement Total Interdit Sans Exception, Femmes Emprisonnées Pour Fausses Couches, Violences Obstétriques Systématiques Honduras/Guatemala & Mortalité Maternelle 193/100k", composite_score: 90.0, abortion_access_criminalization_severity_score: 93.0, maternal_mortality_healthcare_gap_score: 89.0, contraception_sex_education_exclusion_score: 89.0, forced_sterilization_coercion_scale_score: 88.0, risk_level: "critique", primary_pattern: "abortion_access_criminalization_severity", estimated_reproductive_rights_index: 9.0, last_updated: "2026-06-21" },
    { id: "RPR-003", name: "Asie du Sud/Inde — Stérilisation Forcée Femmes Pauvres, Mortalité Rurale & Contraception Inégale", country: "Asie du Sud", sector: "Inde Stérilisation Forcée Femmes Pauvres/Dalit Camps NHRC, Mortalité Maternelle Rurale 197/100k, Accès Contraception Inégal Rural/Urbain & Mariage Précoce 23% Filles", composite_score: 87.3, abortion_access_criminalization_severity_score: 88.0, maternal_mortality_healthcare_gap_score: 88.0, contraception_sex_education_exclusion_score: 86.0, forced_sterilization_coercion_scale_score: 87.0, risk_level: "critique", primary_pattern: "maternal_mortality_healthcare_gap", estimated_reproductive_rights_index: 8.73, last_updated: "2026-06-21" },
    { id: "RPR-004", name: "USA post-Dobbs — 14 États Ban Total Avortement, Criminalisation Médecins & Contraception Menacée", country: "Amérique du Nord", sector: "USA 14 États Ban Total Avortement Post-Dobbs 2022, Médecins Poursuivis Pénalement, Pillules Contraceptives Remises en Question & Femmes Forcées Voyager 1 000+ Km Pour Soins", composite_score: 83.75, abortion_access_criminalization_severity_score: 87.0, maternal_mortality_healthcare_gap_score: 82.0, contraception_sex_education_exclusion_score: 83.0, forced_sterilization_coercion_scale_score: 82.0, risk_level: "critique", primary_pattern: "abortion_access_criminalization_severity", estimated_reproductive_rights_index: 8.38, last_updated: "2026-06-21" },
    { id: "RPR-005", name: "Europe de l'Est/Pologne — Quasi-Ban Avortement, Femmes Décédées & Pression Église", country: "Europe de l'Est", sector: "Pologne Quasi-Ban Avortement 2021 Arrêt Tribunal Constitutionnel, 5 Femmes Décédées Faute Soins Documentées, Pression Église Catholique & Femmes Contraintes Avorter Étranger", composite_score: 53.75, abortion_access_criminalization_severity_score: 57.0, maternal_mortality_healthcare_gap_score: 52.0, contraception_sex_education_exclusion_score: 53.0, forced_sterilization_coercion_scale_score: 52.0, risk_level: "élevé", primary_pattern: "abortion_access_criminalization_severity", estimated_reproductive_rights_index: 5.38, last_updated: "2026-06-21" },
    { id: "RPR-006", name: "Moyen-Orient — Avortement Illégal Majorité Pays, Mariage Forcé Précoce & Honour Crimes", country: "Moyen-Orient", sector: "Avortement Illégal 90% Pays MENA Sauf Tunisie/Turquie, Mariage Enfants 40% Filles Yemen, Honour Crimes Impunis Jordanie/Irak & Mortalité Maternelle 210/100k", composite_score: 51.15, abortion_access_criminalization_severity_score: 53.0, maternal_mortality_healthcare_gap_score: 50.0, contraception_sex_education_exclusion_score: 51.0, forced_sterilization_coercion_scale_score: 50.0, risk_level: "élevé", primary_pattern: "abortion_access_criminalization_severity", estimated_reproductive_rights_index: 5.12, last_updated: "2026-06-21" },
    { id: "RPR-007", name: "IPPF/UNFPA — Plaidoyer Droits Reproductifs, Accès Planning Familial & ICPD+30", country: "Global", sector: "IPPF International Planned Parenthood Federation 120 Pays, UNFPA Fonds Population ONU, Accès Planning Familial Universel SDG 3.7 & ICPD+30 Programme Action 2024", composite_score: 26.1, abortion_access_criminalization_severity_score: 28.0, maternal_mortality_healthcare_gap_score: 25.0, contraception_sex_education_exclusion_score: 25.0, forced_sterilization_coercion_scale_score: 26.0, risk_level: "modéré", primary_pattern: "contraception_sex_education_exclusion", estimated_reproductive_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "RPR-008", name: "ONU/CEDAW — Convention Discrimination Femmes, Rapporteur Santé & SDG 3.1 Mortalité", country: "Global", sector: "CEDAW Convention Élimination Discrimination Femmes 189 États, Rapporteur Spécial ONU Droit Santé, SDG 3.1 Mortalité Maternelle <70/100k 2030 & Comité CEDAW Recommandation Générale 24", composite_score: 4.05, abortion_access_criminalization_severity_score: 5.0, maternal_mortality_healthcare_gap_score: 3.0, contraception_sex_education_exclusion_score: 4.0, forced_sterilization_coercion_scale_score: 4.0, risk_level: "faible", primary_pattern: "maternal_mortality_healthcare_gap", estimated_reproductive_rights_index: 0.41, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/reproductive-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
