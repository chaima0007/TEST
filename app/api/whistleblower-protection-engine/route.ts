import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[whistleblower-protection-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Whistleblower Protection Engine Agent",
  domain: "whistleblower_protection",
  total_entities: 8,
  avg_composite: 61.43,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { state_surveillance_chilling: 2, retaliation_prosecution: 2, media_source_protection_failure: 2, legal_framework_absence: 2 },
  top_risk_entities: [
    "Chine — Aucune Protection, Médecins COVID Arrêtés, Lanceurs Alerte Disparus",
    "USA — Espionage Act, Snowden/Manning/Assange & Criminalisation Divulgations Intérêt Public",
    "Russie — Répression Totale, Journalistes Tués, FSB Surveillance & Navalny Empoisonné",
  ],
  critical_alerts: [
    "Chine: state_surveillance_chilling",
    "USA: retaliation_prosecution",
    "Russie: retaliation_prosecution",
    "Arabie Saoudite/Golfe: state_surveillance_chilling",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_whistleblower_protection_index: 6.14,
  data_sources: [
    "government_accountability_project_whistleblower_protection_global_report",
    "rsf_reporters_without_borders_press_freedom_index_annual",
    "council_of_europe_recommendation_protection_whistleblowers_cm_rec_2014_7",
  ],
  entities: [
    { id: "WP-001", name: "Chine — Aucune Protection, Médecins COVID Arrêtés, Lanceurs Alerte Disparus", country: "Asie du Nord-Est", composite_score: 92.5, legal_framework_absence_score: 90.0, retaliation_prosecution_score: 95.0, state_surveillance_chilling_score: 95.0, media_source_protection_failure_score: 90.0, risk_level: "critique", primary_pattern: "state_surveillance_chilling", estimated_whistleblower_protection_index: 9.25, last_updated: "2026-06-20" },
    { id: "WP-002", name: "Russie — Répression Totale, Journalistes Tués, FSB Surveillance & Navalny Empoisonné", country: "Europe de l'Est", composite_score: 88.9, legal_framework_absence_score: 88.0, retaliation_prosecution_score: 92.0, state_surveillance_chilling_score: 90.0, media_source_protection_failure_score: 85.0, risk_level: "critique", primary_pattern: "retaliation_prosecution", estimated_whistleblower_protection_index: 8.89, last_updated: "2026-06-20" },
    { id: "WP-003", name: "Arabie Saoudite/Golfe — Khashoggi Assassiné, NSO Pegasus & Surveillance Dissidents", country: "Moyen-Orient", composite_score: 83.65, legal_framework_absence_score: 80.0, retaliation_prosecution_score: 85.0, state_surveillance_chilling_score: 88.0, media_source_protection_failure_score: 82.0, risk_level: "critique", primary_pattern: "state_surveillance_chilling", estimated_whistleblower_protection_index: 8.37, last_updated: "2026-06-20" },
    { id: "WP-004", name: "USA — Espionage Act, Snowden/Manning/Assange & Criminalisation Divulgations Intérêt Public", country: "Amérique du Nord", composite_score: 88.6, legal_framework_absence_score: 85.0, retaliation_prosecution_score: 90.0, state_surveillance_chilling_score: 92.0, media_source_protection_failure_score: 88.0, risk_level: "critique", primary_pattern: "retaliation_prosecution", estimated_whistleblower_protection_index: 8.86, last_updated: "2026-06-20" },
    { id: "WP-005", name: "Inde — UAPA Journalistes, Gauri Lankesh Assassinée & Pression Médias Indépendants", country: "Asie du Sud", composite_score: 53.85, legal_framework_absence_score: 52.0, retaliation_prosecution_score: 58.0, state_surveillance_chilling_score: 55.0, media_source_protection_failure_score: 50.0, risk_level: "élevé", primary_pattern: "media_source_protection_failure", estimated_whistleblower_protection_index: 5.39, last_updated: "2026-06-20" },
    { id: "WP-006", name: "UE/France/Allemagne — Luxleaks, Directives Partielles & SLAPP Contre Journalistes", country: "Europe", composite_score: 50.9, legal_framework_absence_score: 48.0, retaliation_prosecution_score: 52.0, state_surveillance_chilling_score: 50.0, media_source_protection_failure_score: 55.0, risk_level: "élevé", primary_pattern: "legal_framework_absence", estimated_whistleblower_protection_index: 5.09, last_updated: "2026-06-20" },
    { id: "WP-007", name: "UK — Official Secrets Act, Réforme Partielle & Collaboration NSA/GCHQ Surveillance", country: "Europe de l'Ouest", composite_score: 28.6, legal_framework_absence_score: 25.0, retaliation_prosecution_score: 30.0, state_surveillance_chilling_score: 32.0, media_source_protection_failure_score: 28.0, risk_level: "modéré", primary_pattern: "legal_framework_absence", estimated_whistleblower_protection_index: 2.86, last_updated: "2026-06-20" },
    { id: "WP-008", name: "ONU/CoE — Résolution 2300, Recommandation CoE & Protection Sources Journalistiques", country: "Global", composite_score: 4.4, legal_framework_absence_score: 4.0, retaliation_prosecution_score: 5.0, state_surveillance_chilling_score: 3.0, media_source_protection_failure_score: 6.0, risk_level: "faible", primary_pattern: "media_source_protection_failure", estimated_whistleblower_protection_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/whistleblower-protection-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
