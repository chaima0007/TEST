import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[uranium-mining-indigenous-rights] SWARM_API_URL non défini");
}

const MOCK = {
  agent: "Uranium Mining Indigenous Rights Engine Agent",
  domain: "uranium_mining_indigenous_rights",
  total_entities: 8,
  avg_composite: 61.34,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { land_dispossession_without_consent: 2, radioactive_contamination_exposure: 2, sacred_site_destruction_pattern: 2, legal_protection_denial_scale: 2 },
  top_risk_entities: [
    "Niger — Communautés Touareg Arlit, Contamination Uranium AREVA & Terres Ancestrales Spoliées",
    "Australie — Pays Mirrar/Kakadu, Mines Ranger, Opposition Consentement Préalable FPIC Ignorée",
    "Kazakhstan — Populations Rurales ISL, Nappes Phréatiques Contaminées & Consultation Nulle",
  ],
  critical_alerts: [
    "Niger: land_dispossession_without_consent",
    "Australie: sacred_site_destruction_pattern",
    "Kazakhstan: radioactive_contamination_exposure",
    "Canada Athabasca: legal_protection_denial_scale",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_uranium_mining_indigenous_rights_index: 6.13,
  data_sources: [
    "un_special_rapporteur_indigenous_peoples_extractive_industries_report",
    "iaea_radiation_protection_uranium_mining_communities_standards",
    "undrip_fpic_implementation_uranium_affected_communities_review",
  ],
  entities: [
    { id: "UM-001", name: "Niger — Communautés Touareg Arlit, Contamination Uranium AREVA & Terres Ancestrales Spoliées", country: "Afrique de l'Ouest", composite_score: 93.2, land_dispossession_without_consent_score: 96.0, radioactive_contamination_exposure_score: 92.0, sacred_site_destruction_pattern_score: 90.0, legal_protection_denial_scale_score: 94.0, risk_level: "critique", primary_pattern: "land_dispossession_without_consent", estimated_uranium_mining_indigenous_rights_index: 9.32, last_updated: "2026-06-22" },
    { id: "UM-002", name: "Australie — Pays Mirrar/Kakadu, Mines Ranger, Opposition Consentement Préalable FPIC Ignorée", country: "Océanie", composite_score: 88.7, land_dispossession_without_consent_score: 88.0, radioactive_contamination_exposure_score: 85.0, sacred_site_destruction_pattern_score: 95.0, legal_protection_denial_scale_score: 86.0, risk_level: "critique", primary_pattern: "sacred_site_destruction_pattern", estimated_uranium_mining_indigenous_rights_index: 8.87, last_updated: "2026-06-22" },
    { id: "UM-003", name: "Kazakhstan — Populations Rurales ISL, Nappes Phréatiques Contaminées & Consultation Nulle", country: "Asie Centrale", composite_score: 85.4, land_dispossession_without_consent_score: 84.0, radioactive_contamination_exposure_score: 92.0, sacred_site_destruction_pattern_score: 80.0, legal_protection_denial_scale_score: 86.0, risk_level: "critique", primary_pattern: "radioactive_contamination_exposure", estimated_uranium_mining_indigenous_rights_index: 8.54, last_updated: "2026-06-22" },
    { id: "UM-004", name: "Canada — Athabasca Denesuline, Lac Athabasca Pollué, Maladies & Droits Traités Violés", country: "Amérique du Nord", composite_score: 83.1, land_dispossession_without_consent_score: 82.0, radioactive_contamination_exposure_score: 85.0, sacred_site_destruction_pattern_score: 80.0, legal_protection_denial_scale_score: 86.0, risk_level: "critique", primary_pattern: "legal_protection_denial_scale", estimated_uranium_mining_indigenous_rights_index: 8.31, last_updated: "2026-06-22" },
    { id: "UM-005", name: "Namibie — San/Herero Erongo, Expansion Rossing/Husab, Pas de FPIC & Eau Souterraine Menacée", country: "Afrique Australe", composite_score: 52.8, land_dispossession_without_consent_score: 52.0, radioactive_contamination_exposure_score: 55.0, sacred_site_destruction_pattern_score: 50.0, legal_protection_denial_scale_score: 54.0, risk_level: "élevé", primary_pattern: "radioactive_contamination_exposure", estimated_uranium_mining_indigenous_rights_index: 5.28, last_updated: "2026-06-22" },
    { id: "UM-006", name: "USA — Navajo Nation Grand Canyon, 500 Mines Abandonnées, Eau Contaminée & Clean-Up Insuffisant", country: "Amérique du Nord", composite_score: 50.3, land_dispossession_without_consent_score: 48.0, radioactive_contamination_exposure_score: 58.0, sacred_site_destruction_pattern_score: 45.0, legal_protection_denial_scale_score: 50.0, risk_level: "élevé", primary_pattern: "radioactive_contamination_exposure", estimated_uranium_mining_indigenous_rights_index: 5.03, last_updated: "2026-06-22" },
    { id: "UM-007", name: "IAEA/UNDRIP Coalition — Standards Radioprotection Communautés & FPIC Uranium Mining Guide", country: "Global", composite_score: 26.5, land_dispossession_without_consent_score: 24.0, radioactive_contamination_exposure_score: 28.0, sacred_site_destruction_pattern_score: 26.0, legal_protection_denial_scale_score: 28.0, risk_level: "modéré", primary_pattern: "land_dispossession_without_consent", estimated_uranium_mining_indigenous_rights_index: 2.65, last_updated: "2026-06-22" },
    { id: "UM-008", name: "Réseau Mondial Peuples Autochtones Uranium — Surveillance Indépendante & Plaidoyer Non-Prolifération", country: "Global", composite_score: 4.7, land_dispossession_without_consent_score: 4.0, radioactive_contamination_exposure_score: 5.0, sacred_site_destruction_pattern_score: 5.0, legal_protection_denial_scale_score: 5.0, risk_level: "faible", primary_pattern: "sacred_site_destruction_pattern", estimated_uranium_mining_indigenous_rights_index: 0.47, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/uranium_mining_indigenous_rights_engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
