import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[counterterrorism-abuse-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Counterterrorism Abuse Engine Agent",
  domain: "counterterrorism_abuse",
  total_entities: 8,
  avg_composite: 59.61,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { minorities_targeting: 2, civil_rights_dismantlement: 2, arbitrary_detention_torture: 2, judicial_oversight_absence: 2 },
  top_risk_entities: [
    "Chine/Xinjiang — Camps Rééducation Ouïghours, XUAR & Antiterrorisme Prétexte État",
    "USA/Post-9/11 — Patriot Act, NDAA, Guantánamo & Surveillance Masse NSA",
    "Égypte/Al-Sissi — 60 000 Détenus Politiques, Loi Antiterror & Journalistes Emprisonnés",
  ],
  critical_alerts: [
    "Chine/Xinjiang: minorities_targeting",
    "USA/Post-9/11: civil_rights_dismantlement",
    "Égypte/Al-Sissi: arbitrary_detention_torture",
    "Inde: minorities_targeting",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_counterterrorism_abuse_index: 5.96,
  data_sources: [
    "amnesty_international_antiterrorism_double_standards_report",
    "un_special_rapporteur_promotion_protection_human_rights_counter_terrorism_annual",
    "icj_assessing_damage_urging_action_eminent_jurists_panel_terrorism_report",
  ],
  entities: [
    { entity_id: "CA-001", name: "Chine/Xinjiang — Camps Rééducation Ouïghours, XUAR & Antiterrorisme Prétexte État", country: "Asie du Nord-Est", composite_score: 94.0, arbitrary_detention_torture_score: 95.0, civil_rights_dismantlement_score: 92.0, minorities_targeting_score: 98.0, judicial_oversight_absence_score: 90.0, risk_level: "critique", primary_pattern: "minorities_targeting", estimated_counterterrorism_abuse_index: 9.4, last_updated: "2026-06-20" },
    { entity_id: "CA-002", name: "USA/Post-9/11 — Patriot Act, NDAA, Guantánamo & Surveillance Masse NSA", country: "Amérique du Nord", composite_score: 82.85, arbitrary_detention_torture_score: 80.0, civil_rights_dismantlement_score: 88.0, minorities_targeting_score: 85.0, judicial_oversight_absence_score: 78.0, risk_level: "critique", primary_pattern: "civil_rights_dismantlement", estimated_counterterrorism_abuse_index: 8.29, last_updated: "2026-06-20" },
    { entity_id: "CA-003", name: "Égypte/Al-Sissi — 60 000 Détenus Politiques, Loi Antiterror & Journalistes Emprisonnés", country: "Afrique du Nord", composite_score: 81.4, arbitrary_detention_torture_score: 85.0, civil_rights_dismantlement_score: 80.0, minorities_targeting_score: 78.0, judicial_oversight_absence_score: 82.0, risk_level: "critique", primary_pattern: "arbitrary_detention_torture", estimated_counterterrorism_abuse_index: 8.14, last_updated: "2026-06-20" },
    { entity_id: "CA-004", name: "Inde — UAPA, Loi Sédition Coloniale, Accusés Kashmir & Militants Droits Humains", country: "Asie du Sud", composite_score: 76.6, arbitrary_detention_torture_score: 72.0, civil_rights_dismantlement_score: 78.0, minorities_targeting_score: 82.0, judicial_oversight_absence_score: 75.0, risk_level: "critique", primary_pattern: "minorities_targeting", estimated_counterterrorism_abuse_index: 7.66, last_updated: "2026-06-20" },
    { entity_id: "CA-005", name: "France/Europe — Loi Renseignement, État Urgence Permanent & Surveillance Communautés", country: "Europe", composite_score: 56.1, arbitrary_detention_torture_score: 52.0, civil_rights_dismantlement_score: 58.0, minorities_targeting_score: 60.0, judicial_oversight_absence_score: 55.0, risk_level: "élevé", primary_pattern: "judicial_oversight_absence", estimated_counterterrorism_abuse_index: 5.61, last_updated: "2026-06-20" },
    { entity_id: "CA-006", name: "Turquie — Coup 2016, 150 000 Arrêtés, HDP Kurdes Emprisonnés & Professeurs Épurés", country: "Europe de l'Est", composite_score: 54.0, arbitrary_detention_torture_score: 55.0, civil_rights_dismantlement_score: 52.0, minorities_targeting_score: 58.0, judicial_oversight_absence_score: 50.0, risk_level: "élevé", primary_pattern: "arbitrary_detention_torture", estimated_counterterrorism_abuse_index: 5.4, last_updated: "2026-06-20" },
    { entity_id: "CA-007", name: "ONU/CDH — Résolutions Antiterrorisme & Droits, Procédures Spéciales & HCDH Monitoring", country: "Global", composite_score: 27.5, arbitrary_detention_torture_score: 22.0, civil_rights_dismantlement_score: 28.0, minorities_targeting_score: 30.0, judicial_oversight_absence_score: 32.0, risk_level: "modéré", primary_pattern: "civil_rights_dismantlement", estimated_counterterrorism_abuse_index: 2.75, last_updated: "2026-06-20" },
    { entity_id: "CA-008", name: "ONU/ONUDC/CTITF — Task Force Contre-Terrorisme, Droits Fondamentaux & Garanties", country: "Global", composite_score: 4.4, arbitrary_detention_torture_score: 4.0, civil_rights_dismantlement_score: 5.0, minorities_targeting_score: 3.0, judicial_oversight_absence_score: 6.0, risk_level: "faible", primary_pattern: "judicial_oversight_absence", estimated_counterterrorism_abuse_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/counterterrorism-abuse-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
