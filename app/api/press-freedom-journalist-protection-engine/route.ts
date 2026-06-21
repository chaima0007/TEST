import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[press-freedom-journalist-protection-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Press Freedom Journalist Protection Engine Agent",
  domain: "press_freedom_journalist_protection",
  total_entities: 8,
  avg_composite: 60.86,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    journalist_killing_imprisonment_severity: 4,
    media_censorship_state_capture_scale: 2,
    surveillance_source_protection_violation: 1,
    online_journalist_harassment_slapp_gap: 1,
  },
  top_risk_entities: [
    "Mexique/Honduras — Journalistes Pays Non-Guerre Le Plus Meurtrier, Cartels Tuent Reporters, Impunité 99% & Autodéfense Journalistes",
    "Chine — 100+ Journalistes Emprisonnés, Presse Étrangère Expulsée, Porte-Parole Seul Autorisé & VPN Bloqué Presse",
    "Russie — Novaya Gazeta Fermée, Loi Agent Étranger, Khashoggi-Style Meurtres Abyan & Ukraine War Coverage Interdit",
  ],
  critical_alerts: [
    "Mexique/Honduras: journalist_killing_imprisonment_severity",
    "Chine: media_censorship_state_capture_scale",
    "Russie: journalist_killing_imprisonment_severity",
    "Arabie Saoudite: surveillance_source_protection_violation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_press_freedom_journalist_protection_index: 6.09,
  data_sources: [
    "rsf_press_freedom_index_annual_report",
    "cpj_journalist_imprisonment_global_census",
    "freedom_of_press_foundation_surveillance_report",
  ],
  entities: [
    {
      entity_id: "PFJ-001",
      name: "Mexique/Honduras — Journalistes Pays Non-Guerre Le Plus Meurtrier, Cartels Tuent Reporters, Impunité 99% & Autodéfense Journalistes",
      country: "Mexique/Honduras",
      journalist_killing_imprisonment_severity_score: 93.0,
      media_censorship_state_capture_scale_score: 91.0,
      surveillance_source_protection_violation_score: 90.0,
      online_journalist_harassment_slapp_gap_score: 92.0,
      composite_score: 91.55,
      risk_level: "critique",
      primary_pattern: "journalist_killing_imprisonment_severity",
      estimated_press_freedom_journalist_protection_index: 9.16,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PFJ-002",
      name: "Chine — 100+ Journalistes Emprisonnés, Presse Étrangère Expulsée, Porte-Parole Seul Autorisé & VPN Bloqué Presse",
      country: "Chine",
      journalist_killing_imprisonment_severity_score: 90.0,
      media_censorship_state_capture_scale_score: 88.0,
      surveillance_source_protection_violation_score: 89.0,
      online_journalist_harassment_slapp_gap_score: 91.0,
      composite_score: 89.45,
      risk_level: "critique",
      primary_pattern: "media_censorship_state_capture_scale",
      estimated_press_freedom_journalist_protection_index: 8.95,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PFJ-003",
      name: "Russie — Novaya Gazeta Fermée, Loi Agent Étranger, Khashoggi-Style Meurtres Abyan & Ukraine War Coverage Interdit",
      country: "Russie",
      journalist_killing_imprisonment_severity_score: 87.0,
      media_censorship_state_capture_scale_score: 85.0,
      surveillance_source_protection_violation_score: 86.0,
      online_journalist_harassment_slapp_gap_score: 88.0,
      composite_score: 86.45,
      risk_level: "critique",
      primary_pattern: "journalist_killing_imprisonment_severity",
      estimated_press_freedom_journalist_protection_index: 8.65,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PFJ-004",
      name: "Arabie Saoudite — Khashoggi Assassinat, Blogueurs Condamnés, Médias Indépendants Inexistants & Critiques Online Emprisonnés",
      country: "Arabie Saoudite",
      journalist_killing_imprisonment_severity_score: 84.0,
      media_censorship_state_capture_scale_score: 82.0,
      surveillance_source_protection_violation_score: 83.0,
      online_journalist_harassment_slapp_gap_score: 85.0,
      composite_score: 83.45,
      risk_level: "critique",
      primary_pattern: "surveillance_source_protection_violation",
      estimated_press_freedom_journalist_protection_index: 8.35,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PFJ-005",
      name: "Turquie/Israël — Journalistes Gaza Tués 100+, Turquie 2ème Prison Journalistes, Presse Pro-Gouvernement Monopole & SLAPP",
      country: "Turquie/Israël",
      journalist_killing_imprisonment_severity_score: 55.0,
      media_censorship_state_capture_scale_score: 53.0,
      surveillance_source_protection_violation_score: 54.0,
      online_journalist_harassment_slapp_gap_score: 56.0,
      composite_score: 54.45,
      risk_level: "élevé",
      primary_pattern: "journalist_killing_imprisonment_severity",
      estimated_press_freedom_journalist_protection_index: 5.45,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PFJ-006",
      name: "USA/Europe — Fox News/MSNBC Polarisation, Reporters Sans Protection Fédérale, SLAPP Suits Croissants & Propriété Oligarques",
      country: "USA/Europe",
      journalist_killing_imprisonment_severity_score: 52.0,
      media_censorship_state_capture_scale_score: 50.0,
      surveillance_source_protection_violation_score: 51.0,
      online_journalist_harassment_slapp_gap_score: 53.0,
      composite_score: 51.45,
      risk_level: "élevé",
      primary_pattern: "online_journalist_harassment_slapp_gap",
      estimated_press_freedom_journalist_protection_index: 5.15,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PFJ-007",
      name: "RSF/CPJ — Classement Liberté Presse, Committee Protect Journalists, Hotlines Urgence & Rapports Annuels",
      country: "Global",
      journalist_killing_imprisonment_severity_score: 27.0,
      media_censorship_state_capture_scale_score: 25.0,
      surveillance_source_protection_violation_score: 26.0,
      online_journalist_harassment_slapp_gap_score: 26.0,
      composite_score: 26.05,
      risk_level: "modéré",
      primary_pattern: "journalist_killing_imprisonment_severity",
      estimated_press_freedom_journalist_protection_index: 2.61,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PFJ-008",
      name: "ONU/Art.19 PIDCP — Liberté Expression Presse, Rapporteur Spécial & SDG 16.10 Accès Information",
      country: "Global",
      journalist_killing_imprisonment_severity_score: 5.0,
      media_censorship_state_capture_scale_score: 3.0,
      surveillance_source_protection_violation_score: 4.0,
      online_journalist_harassment_slapp_gap_score: 4.0,
      composite_score: 4.05,
      risk_level: "faible",
      primary_pattern: "media_censorship_state_capture_scale",
      estimated_press_freedom_journalist_protection_index: 0.41,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/press-freedom-journalist-protection-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
