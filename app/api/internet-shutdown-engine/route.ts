import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[internet-shutdown-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Internet Shutdown Engine Agent",
  domain: "internet_shutdown",
  total_entities: 8,
  avg_composite: 60.84,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { shutdown_duration_frequency: 3, political_protest_targeting: 3, legal_accountability_gap: 2 },
  top_risk_entities: [
    "Myanmar — Coupures Post-Coup 2021, 4 Ans Restrictions & Populations Rurales Isolées",
    "Éthiopie/Tigray — Coupure 2 Ans Guerre, Génocide Sans Témoins & Humanitaire Aveugle",
    "Inde/Cachemire — Coupure 213 Jours Record Mondial, Répression Post-Art.370 & Presse Muselée",
  ],
  critical_alerts: [
    "Myanmar: shutdown_duration_frequency",
    "Éthiopie/Tigray: political_protest_targeting",
    "Inde/Cachemire: shutdown_duration_frequency",
    "Iran: political_protest_targeting",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_internet_shutdown_index: 6.08,
  data_sources: [
    "access_now_keepiton_internet_shutdowns_annual_report",
    "netblocks_cost_internet_shutdowns_global_tracker",
    "freedom_house_freedom_net_global_internet_freedom_report",
  ],
  entities: [
    { id: "IS-001", name: "Myanmar — Coupures Post-Coup 2021, 4 Ans Restrictions & Populations Rurales Isolées", country: "Asie du Sud-Est", composite_score: 93.15, shutdown_duration_frequency_score: 95.0, economic_civil_harm_score: 90.0, political_protest_targeting_score: 95.0, legal_accountability_gap_score: 92.0, risk_level: "critique", primary_pattern: "shutdown_duration_frequency", estimated_internet_shutdown_index: 9.32, last_updated: "2026-06-21" },
    { id: "IS-002", name: "Éthiopie/Tigray — Coupure 2 Ans Guerre, Génocide Sans Témoins & Humanitaire Aveugle", country: "Afrique de l'Est", composite_score: 89.0, shutdown_duration_frequency_score: 88.0, economic_civil_harm_score: 88.0, political_protest_targeting_score: 92.0, legal_accountability_gap_score: 88.0, risk_level: "critique", primary_pattern: "political_protest_targeting", estimated_internet_shutdown_index: 8.9, last_updated: "2026-06-21" },
    { id: "IS-003", name: "Inde/Cachemire — Coupure 213 Jours Record Mondial, Répression Post-Art.370 & Presse Muselée", country: "Asie du Sud", composite_score: 86.65, shutdown_duration_frequency_score: 90.0, economic_civil_harm_score: 85.0, political_protest_targeting_score: 88.0, legal_accountability_gap_score: 82.0, risk_level: "critique", primary_pattern: "shutdown_duration_frequency", estimated_internet_shutdown_index: 8.67, last_updated: "2026-06-21" },
    { id: "IS-004", name: "Iran — Coupures Systématiques Protestations, Mahsa Amini 2022 & Blocages Plateformes", country: "Moyen-Orient", composite_score: 82.25, shutdown_duration_frequency_score: 82.0, economic_civil_harm_score: 80.0, political_protest_targeting_score: 85.0, legal_accountability_gap_score: 82.0, risk_level: "critique", primary_pattern: "political_protest_targeting", estimated_internet_shutdown_index: 8.23, last_updated: "2026-06-21" },
    { id: "IS-005", name: "Afrique/Élections — Coupures Cameroun/Mali/Tchad Périodes Électorales & Manipulation Info", country: "Afrique Sub-Saharienne", composite_score: 54.25, shutdown_duration_frequency_score: 52.0, economic_civil_harm_score: 55.0, political_protest_targeting_score: 58.0, legal_accountability_gap_score: 52.0, risk_level: "élevé", primary_pattern: "political_protest_targeting", estimated_internet_shutdown_index: 5.43, last_updated: "2026-06-21" },
    { id: "IS-006", name: "Russie/Ukraine — Blocages RT/Médias, DPI Technologie Surveillance & Internet Souverain RuNet", country: "Europe de l'Est", composite_score: 51.15, shutdown_duration_frequency_score: 48.0, economic_civil_harm_score: 52.0, political_protest_targeting_score: 55.0, legal_accountability_gap_score: 50.0, risk_level: "élevé", primary_pattern: "legal_accountability_gap", estimated_internet_shutdown_index: 5.12, last_updated: "2026-06-21" },
    { id: "IS-007", name: "Access Now/NetBlocks — ONG Détection Coupures, Alertes Temps Réel & Plaidoyer Global", country: "Global", composite_score: 25.85, shutdown_duration_frequency_score: 22.0, economic_civil_harm_score: 25.0, political_protest_targeting_score: 28.0, legal_accountability_gap_score: 30.0, risk_level: "modéré", primary_pattern: "shutdown_duration_frequency", estimated_internet_shutdown_index: 2.59, last_updated: "2026-06-21" },
    { id: "IS-008", name: "ONU/IGF — Forum Gouvernance Internet, Résolutions Liberté Expression & Normes Non Contraignantes", country: "Global", composite_score: 4.4, shutdown_duration_frequency_score: 4.0, economic_civil_harm_score: 5.0, political_protest_targeting_score: 3.0, legal_accountability_gap_score: 6.0, risk_level: "faible", primary_pattern: "legal_accountability_gap", estimated_internet_shutdown_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/internet-shutdown-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
