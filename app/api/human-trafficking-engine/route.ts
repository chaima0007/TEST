import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[human-trafficking-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Human Trafficking Engine Agent",
  domain: "human_trafficking",
  total_entities: 8,
  avg_composite: 59.63,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { border_recruitment_deception: 2, labor_sex_exploitation_scale: 2, victim_identification_failure: 2, prosecution_conviction_gap: 2 },
  top_risk_entities: [
    "Asie du Sud-Est/Arnaques Téléphoniques — Esclavage Moderne Myanmar/Cambodge, 100K Forcés Centres Fraude",
    "Moyen-Orient/Kafala — Travailleurs Domestiques Piégés, Passeports Confisqués & Travail Forcé",
    "Europe/Balkans — Réseaux Prostitution Forcée Roumanie/Bulgarie, Mafia & Corridors Trafic",
  ],
  critical_alerts: [
    "Asie du Sud-Est/Arnaques Téléphoniques: border_recruitment_deception",
    "Moyen-Orient/Kafala: labor_sex_exploitation_scale",
    "Europe/Balkans: border_recruitment_deception",
    "Libye/Méditerranée: victim_identification_failure",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_human_trafficking_index: 5.96,
  data_sources: [
    "unodc_global_report_trafficking_persons_2024",
    "ilo_forced_labour_modern_slavery_global_estimates_report",
    "polaris_project_human_trafficking_trends_annual_report",
  ],
  entities: [
    { id: "HT-001", name: "Asie du Sud-Est/Arnaques Téléphoniques — Esclavage Moderne Myanmar/Cambodge, 100K Forcés Centres Fraude", country: "Asie du Sud-Est", composite_score: 91.45, labor_sex_exploitation_scale_score: 92.0, border_recruitment_deception_score: 95.0, victim_identification_failure_score: 90.0, prosecution_conviction_gap_score: 88.0, risk_level: "critique", primary_pattern: "border_recruitment_deception", estimated_human_trafficking_index: 9.15, last_updated: "2026-06-20" },
    { id: "HT-002", name: "Moyen-Orient/Kafala — Travailleurs Domestiques Piégés, Passeports Confisqués & Travail Forcé", country: "Moyen-Orient", composite_score: 86.65, labor_sex_exploitation_scale_score: 88.0, border_recruitment_deception_score: 85.0, victim_identification_failure_score: 88.0, prosecution_conviction_gap_score: 85.0, risk_level: "critique", primary_pattern: "labor_sex_exploitation_scale", estimated_human_trafficking_index: 8.67, last_updated: "2026-06-20" },
    { id: "HT-003", name: "Europe/Balkans — Réseaux Prostitution Forcée Roumanie/Bulgarie, Mafia & Corridors Trafic", country: "Europe", composite_score: 82.35, labor_sex_exploitation_scale_score: 82.0, border_recruitment_deception_score: 85.0, victim_identification_failure_score: 82.0, prosecution_conviction_gap_score: 80.0, risk_level: "critique", primary_pattern: "border_recruitment_deception", estimated_human_trafficking_index: 8.24, last_updated: "2026-06-20" },
    { id: "HT-004", name: "Libye/Méditerranée — Migrants Torturés/Vendus Geôliers, Rançons Familles & Travail Forcé", country: "Afrique du Nord", composite_score: 81.15, labor_sex_exploitation_scale_score: 80.0, border_recruitment_deception_score: 78.0, victim_identification_failure_score: 85.0, prosecution_conviction_gap_score: 82.0, risk_level: "critique", primary_pattern: "victim_identification_failure", estimated_human_trafficking_index: 8.12, last_updated: "2026-06-20" },
    { id: "HT-005", name: "USA — Travail Agricole Forcé, Exploitation Sexuelle Mineurs & Identification Victimes Lacunaire", country: "Amérique du Nord", composite_score: 53.85, labor_sex_exploitation_scale_score: 52.0, border_recruitment_deception_score: 55.0, victim_identification_failure_score: 58.0, prosecution_conviction_gap_score: 50.0, risk_level: "élevé", primary_pattern: "victim_identification_failure", estimated_human_trafficking_index: 5.39, last_updated: "2026-06-20" },
    { id: "HT-006", name: "Inde/Népal — Traite Femmes/Filles Vers Mumbai/Delhi, Mariages Forcés & Travail Domestique", country: "Asie du Sud", composite_score: 51.35, labor_sex_exploitation_scale_score: 50.0, border_recruitment_deception_score: 52.0, victim_identification_failure_score: 55.0, prosecution_conviction_gap_score: 48.0, risk_level: "élevé", primary_pattern: "prosecution_conviction_gap", estimated_human_trafficking_index: 5.14, last_updated: "2026-06-20" },
    { id: "HT-007", name: "La Strada/Polaris — ONG Anti-Traite, Lignes Écoute, Refuges & Plaidoyer Politique", country: "Global", composite_score: 25.85, labor_sex_exploitation_scale_score: 22.0, border_recruitment_deception_score: 25.0, victim_identification_failure_score: 28.0, prosecution_conviction_gap_score: 30.0, risk_level: "modéré", primary_pattern: "labor_sex_exploitation_scale", estimated_human_trafficking_index: 2.59, last_updated: "2026-06-20" },
    { id: "HT-008", name: "ONU/Protocole Palermo — Convention Crime Organisé, Définition Traite & Standards Protection", country: "Global", composite_score: 4.4, labor_sex_exploitation_scale_score: 4.0, border_recruitment_deception_score: 5.0, victim_identification_failure_score: 3.0, prosecution_conviction_gap_score: 6.0, risk_level: "faible", primary_pattern: "prosecution_conviction_gap", estimated_human_trafficking_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-trafficking-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
