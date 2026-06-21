import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[minority-religious-freedom-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Minority Religious Freedom Rights Engine Agent",
  domain: "minority_religious_freedom_rights",
  total_entities: 8,
  avg_composite: 61.81,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { religious_persecution_imprisonment_severity: 4, blasphemy_apostasy_law_prosecution: 2, place_of_worship_destruction_ban_scale: 2 },
  top_risk_entities: [
    "Chine — Ouïghours Mosquées Détruites, Tibétains Bouddhisme Persécuté, Falun Gong 1M Détenus & Crosses Église Retirées",
    "Pakistan — Blasphème Loi 295-C Peine Mort, Ahmadis Minorité Persécutée, Chrétiens Villages Brûlés & Asia Bibi",
    "Iran — Baha'is Propriétés Confisquées, Évangéliques Emprisonnés, Juifs Discrimination & Convertis Apostasie",
  ],
  critical_alerts: [
    "Chine: religious_persecution_imprisonment_severity",
    "Pakistan: blasphemy_apostasy_law_prosecution",
    "Iran: blasphemy_apostasy_law_prosecution",
    "Birmanie/Myanmar: place_of_worship_destruction_ban_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_minority_religious_freedom_rights_index: 6.18,
  data_sources: [
    "uscirf_annual_report_religious_freedom_violations",
    "open_doors_world_watch_list_christian_persecution",
    "forum18_central_asia_religious_freedom_monitoring",
  ],
  entities: [
    { id: "MRF-001", name: "Chine — Ouïghours Mosquées Détruites, Tibétains Bouddhisme Persécuté, Falun Gong 1M Détenus & Crosses Église Retirées", country: "Chine", composite_score: 93.35, religious_persecution_imprisonment_severity_score: 96.0, place_of_worship_destruction_ban_scale_score: 93.0, blasphemy_apostasy_law_prosecution_score: 90.0, religious_minority_civil_rights_exclusion_gap_score: 94.0, risk_level: "critique", primary_pattern: "religious_persecution_imprisonment_severity", estimated_minority_religious_freedom_rights_index: 9.34, last_updated: "2026-06-21" },
    { id: "MRF-002", name: "Pakistan — Blasphème Loi 295-C Peine Mort, Ahmadis Minorité Persécutée, Chrétiens Villages Brûlés & Asia Bibi", country: "Pakistan", composite_score: 90.7, religious_persecution_imprisonment_severity_score: 92.0, place_of_worship_destruction_ban_scale_score: 89.0, blasphemy_apostasy_law_prosecution_score: 93.0, religious_minority_civil_rights_exclusion_gap_score: 88.0, risk_level: "critique", primary_pattern: "blasphemy_apostasy_law_prosecution", estimated_minority_religious_freedom_rights_index: 9.07, last_updated: "2026-06-21" },
    { id: "MRF-003", name: "Iran — Baha&apos;is Propriétés Confisquées, Évangéliques Emprisonnés, Juifs Discrimination & Convertis Apostasie", country: "Iran", composite_score: 87.5, religious_persecution_imprisonment_severity_score: 89.0, place_of_worship_destruction_ban_scale_score: 86.0, blasphemy_apostasy_law_prosecution_score: 90.0, religious_minority_civil_rights_exclusion_gap_score: 84.0, risk_level: "critique", primary_pattern: "blasphemy_apostasy_law_prosecution", estimated_minority_religious_freedom_rights_index: 8.75, last_updated: "2026-06-21" },
    { id: "MRF-004", name: "Birmanie/Myanmar — Rohingyas Musulmans Génocide, Mosquées Brûlées, Statut Apatride & Lois Bouddhisme National Race", country: "Myanmar", composite_score: 84.3, religious_persecution_imprisonment_severity_score: 86.0, place_of_worship_destruction_ban_scale_score: 84.0, blasphemy_apostasy_law_prosecution_score: 82.0, religious_minority_civil_rights_exclusion_gap_score: 85.0, risk_level: "critique", primary_pattern: "place_of_worship_destruction_ban_scale", estimated_minority_religious_freedom_rights_index: 8.43, last_updated: "2026-06-21" },
    { id: "MRF-005", name: "Inde/Modi — Loi CAA Discrimination Musulmans, Lynchage Vache, Destructions Mosquées & RSS Violence Minorités", country: "Inde", composite_score: 55.55, religious_persecution_imprisonment_severity_score: 57.0, place_of_worship_destruction_ban_scale_score: 55.0, blasphemy_apostasy_law_prosecution_score: 54.0, religious_minority_civil_rights_exclusion_gap_score: 56.0, risk_level: "élevé", primary_pattern: "religious_persecution_imprisonment_severity", estimated_minority_religious_freedom_rights_index: 5.56, last_updated: "2026-06-21" },
    { id: "MRF-006", name: "Russie/Biélorussie — Témoins Jéhovah Interdits, Propriétés Saisies, Catholicisme Réprimé & Sectes Loi Lutte", country: "Russie/Biélorussie", composite_score: 52.45, religious_persecution_imprisonment_severity_score: 54.0, place_of_worship_destruction_ban_scale_score: 53.0, blasphemy_apostasy_law_prosecution_score: 52.0, religious_minority_civil_rights_exclusion_gap_score: 50.0, risk_level: "élevé", primary_pattern: "religious_persecution_imprisonment_severity", estimated_minority_religious_freedom_rights_index: 5.25, last_updated: "2026-06-21" },
    { id: "MRF-007", name: "USCIRF/Forum 18 — Commission Liberté Religieuse Internationale, Monitoring Pays Préoccupants & Rapports Annuels", country: "Global", composite_score: 26.15, religious_persecution_imprisonment_severity_score: 24.0, place_of_worship_destruction_ban_scale_score: 28.0, blasphemy_apostasy_law_prosecution_score: 27.0, religious_minority_civil_rights_exclusion_gap_score: 26.0, risk_level: "modéré", primary_pattern: "place_of_worship_destruction_ban_scale", estimated_minority_religious_freedom_rights_index: 2.62, last_updated: "2026-06-21" },
    { id: "MRF-008", name: "ONU/Art.18 PIDCP — Liberté Conscience Religion, Déclaration 1981 Minorités Religieuses & SDG 16.3", country: "Global", composite_score: 4.45, religious_persecution_imprisonment_severity_score: 4.0, place_of_worship_destruction_ban_scale_score: 5.0, blasphemy_apostasy_law_prosecution_score: 4.0, religious_minority_civil_rights_exclusion_gap_score: 5.0, risk_level: "faible", primary_pattern: "religious_persecution_imprisonment_severity", estimated_minority_religious_freedom_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/minority-religious-freedom-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
