import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[whistleblower-leaker-protection-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Whistleblower Leaker Protection Engine Agent",
  domain: "whistleblower_leaker_protection",
  total_entities: 8,
  avg_composite: 61.39,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { retaliation_prosecution_espionage_severity: 2, source_journalist_surveillance_exposure_scale: 2, whistleblower_legal_protection_absence: 2, public_interest_disclosure_mechanism_deficit_gap: 2 },
  top_risk_entities: ["USA/Snowden — NSA PRISM Révélé 2013, Snowden Exilé Russie, Manning 35 Ans Prison & Espionage Act Poursuite 14 Lanceurs", "UK/Julian Assange — WikiLeaks Extradition 14 Ans, Section 23 Official Secrets, Journalistes GCHQ Espionnés & Guardian Disques Durs Détruits", "Russie/FSB — Système Filtrage Internet, Journalistes Empoisonnés/Tués, Sources Livraison FSB & Lanceurs Trahison 20 Ans"],
  critical_alerts: ["USA/Snowden: retaliation_prosecution_espionage_severity", "UK/Julian Assange: source_journalist_surveillance_exposure_scale", "Russie/FSB: retaliation_prosecution_espionage_severity", "Chine/Cybersec: whistleblower_legal_protection_absence"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_whistleblower_leaker_protection_index: 6.14,
  data_sources: ["government_accountability_project_report", "cpj_journalist_source_protection_report", "un_special_rapporteur_whistleblower_protection"],
  entities: [
    { id: "WLP-001", name: "USA/Snowden — NSA PRISM Révélé 2013, Snowden Exilé Russie, Manning 35 Ans Prison & Espionage Act Poursuite 14 Lanceurs", country: "USA", composite_score: 92.65, retaliation_prosecution_espionage_severity_score: 94.0, source_journalist_surveillance_exposure_scale_score: 92.0, whistleblower_legal_protection_absence_score: 93.0, public_interest_disclosure_mechanism_deficit_gap_score: 91.0, risk_level: "critique", primary_pattern: "retaliation_prosecution_espionage_severity", estimated_whistleblower_leaker_protection_index: 9.27, last_updated: "2026-06-21" },
    { id: "WLP-002", name: "UK/Julian Assange — WikiLeaks Extradition 14 Ans, Section 23 Official Secrets, Journalistes GCHQ Espionnés & Guardian Disques Durs Détruits", country: "UK", composite_score: 90.0, retaliation_prosecution_espionage_severity_score: 90.0, source_journalist_surveillance_exposure_scale_score: 92.0, whistleblower_legal_protection_absence_score: 88.0, public_interest_disclosure_mechanism_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "source_journalist_surveillance_exposure_scale", estimated_whistleblower_leaker_protection_index: 9.0, last_updated: "2026-06-21" },
    { id: "WLP-003", name: "Russie/FSB — Système Filtrage Internet, Journalistes Empoisonnés/Tués, Sources Livraison FSB & Lanceurs Trahison 20 Ans", country: "Russie", composite_score: 86.55, retaliation_prosecution_espionage_severity_score: 87.0, source_journalist_surveillance_exposure_scale_score: 85.0, whistleblower_legal_protection_absence_score: 88.0, public_interest_disclosure_mechanism_deficit_gap_score: 86.0, risk_level: "critique", primary_pattern: "retaliation_prosecution_espionage_severity", estimated_whistleblower_leaker_protection_index: 8.65, last_updated: "2026-06-21" },
    { id: "WLP-004", name: "Chine/Cybersec — Lois Secrets État Larges, Journalistes Weibo Arrêtés, VPN Criminalisé & Dissident Chiffrement 10 Ans", country: "Chine", composite_score: 83.45, retaliation_prosecution_espionage_severity_score: 84.0, source_journalist_surveillance_exposure_scale_score: 82.0, whistleblower_legal_protection_absence_score: 83.0, public_interest_disclosure_mechanism_deficit_gap_score: 85.0, risk_level: "critique", primary_pattern: "whistleblower_legal_protection_absence", estimated_whistleblower_leaker_protection_index: 8.35, last_updated: "2026-06-21" },
    { id: "WLP-005", name: "France/HADOPI — Secret Défense Journalistes Visés, Terry Gontier Affaire, DGSI Sources & Loi 2019 Renseignement Sources Affaiblies", country: "France", composite_score: 55.45, retaliation_prosecution_espionage_severity_score: 55.0, source_journalist_surveillance_exposure_scale_score: 54.0, whistleblower_legal_protection_absence_score: 57.0, public_interest_disclosure_mechanism_deficit_gap_score: 56.0, risk_level: "élevé", primary_pattern: "source_journalist_surveillance_exposure_scale", estimated_whistleblower_leaker_protection_index: 5.54, last_updated: "2026-06-21" },
    { id: "WLP-006", name: "Inde/OSA — Official Secrets Act Colonial 1923, RTI Activistes Tués 80, Journalistes Séditieux Arrêtés & UAPA Lanceurs", country: "Inde", composite_score: 52.4, retaliation_prosecution_espionage_severity_score: 52.0, source_journalist_surveillance_exposure_scale_score: 51.0, whistleblower_legal_protection_absence_score: 53.0, public_interest_disclosure_mechanism_deficit_gap_score: 54.0, risk_level: "élevé", primary_pattern: "public_interest_disclosure_mechanism_deficit_gap", estimated_whistleblower_leaker_protection_index: 5.24, last_updated: "2026-06-21" },
    { id: "WLP-007", name: "CPJ/RSF — Comité Protection Journalistes, Reporters Sans Frontières Sources, Government Accountability Project & Whistleblower Aid", country: "Global", composite_score: 26.6, retaliation_prosecution_espionage_severity_score: 27.0, source_journalist_surveillance_exposure_scale_score: 26.0, whistleblower_legal_protection_absence_score: 28.0, public_interest_disclosure_mechanism_deficit_gap_score: 25.0, risk_level: "modéré", primary_pattern: "public_interest_disclosure_mechanism_deficit_gap", estimated_whistleblower_leaker_protection_index: 2.66, last_updated: "2026-06-21" },
    { id: "WLP-008", name: "ONU/PACE — Résolution ONU Lanceurs Alerte 2015, PACE Recommandation 2006, Principes Tshwane & Standards Juridiques Protection", country: "Global", composite_score: 4.0, retaliation_prosecution_espionage_severity_score: 4.0, source_journalist_surveillance_exposure_scale_score: 4.0, whistleblower_legal_protection_absence_score: 4.0, public_interest_disclosure_mechanism_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "whistleblower_legal_protection_absence", estimated_whistleblower_leaker_protection_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/whistleblower-leaker-protection-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
