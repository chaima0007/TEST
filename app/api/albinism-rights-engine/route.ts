import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[albinism-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Albinism Rights Engine Agent",
  domain: "albinism_rights",
  total_entities: 8,
  avg_composite: 61.11,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { ritual_killing_body_parts_trade: 2, legal_protection_enforcement_gap: 2, discrimination_exclusion_severity: 2, institutional_abandonment_scale: 2 },
  top_risk_entities: [
    "Tanzanie — 100+ Meurtres Rituels Depuis 2000, Membres Prélevés Vivants & Marché Noir Organes",
    "Mozambique — Vague Meurtres 2016-2021, Démembrement Rituels & Réponse Gouvernementale Tardive",
    "Malawi — Urgence Présidentielle 2017, 70+ Attaques/Disparitions & Impunité Persistante",
  ],
  critical_alerts: [
    "Tanzanie: ritual_killing_body_parts_trade",
    "Mozambique: ritual_killing_body_parts_trade",
    "Malawi: legal_protection_enforcement_gap",
    "Zimbabwe: discrimination_exclusion_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_albinism_rights_index: 6.11,
  data_sources: [
    "un_ohchr_independent_expert_albinism_ikponwosa_ero_report",
    "under_the_same_sun_albinism_killings_database_africa",
    "amnesty_international_end_attacks_persons_albinism_report",
  ],
  entities: [
    { id: "AL-001", name: "Tanzanie — 100+ Meurtres Rituels Depuis 2000, Membres Prélevés Vivants & Marché Noir Organes", country: "Afrique de l'Est", composite_score: 92.9, ritual_killing_body_parts_trade_score: 95.0, legal_protection_enforcement_gap_score: 92.0, discrimination_exclusion_severity_score: 92.0, institutional_abandonment_scale_score: 92.0, risk_level: "critique", primary_pattern: "ritual_killing_body_parts_trade", estimated_albinism_rights_index: 9.29, last_updated: "2026-06-21" },
    { id: "AL-002", name: "Mozambique — Vague Meurtres 2016-2021, Démembrement Rituels & Réponse Gouvernementale Tardive", country: "Afrique de l'Est", composite_score: 89.1, ritual_killing_body_parts_trade_score: 90.0, legal_protection_enforcement_gap_score: 90.0, discrimination_exclusion_severity_score: 88.0, institutional_abandonment_scale_score: 88.0, risk_level: "critique", primary_pattern: "ritual_killing_body_parts_trade", estimated_albinism_rights_index: 8.91, last_updated: "2026-06-21" },
    { id: "AL-003", name: "Malawi — Urgence Présidentielle 2017, 70+ Attaques/Disparitions & Impunité Persistante", country: "Afrique de l'Est", composite_score: 88.0, ritual_killing_body_parts_trade_score: 88.0, legal_protection_enforcement_gap_score: 88.0, discrimination_exclusion_severity_score: 88.0, institutional_abandonment_scale_score: 88.0, risk_level: "critique", primary_pattern: "legal_protection_enforcement_gap", estimated_albinism_rights_index: 8.8, last_updated: "2026-06-21" },
    { id: "AL-004", name: "Zimbabwe — Exclusion Emploi/Mariage, Soins Dermatologiques Absents & Préjugé Fantômes", country: "Afrique Australe", composite_score: 85.45, ritual_killing_body_parts_trade_score: 82.0, legal_protection_enforcement_gap_score: 85.0, discrimination_exclusion_severity_score: 88.0, institutional_abandonment_scale_score: 88.0, risk_level: "critique", primary_pattern: "discrimination_exclusion_severity", estimated_albinism_rights_index: 8.55, last_updated: "2026-06-21" },
    { id: "AL-005", name: "Nigéria/Afrique Ouest — Exclusion Scolaire, Mariage Refusé, Cancer Peau Non Traité & Stigmate", country: "Afrique de l'Ouest", composite_score: 52.9, ritual_killing_body_parts_trade_score: 50.0, legal_protection_enforcement_gap_score: 55.0, discrimination_exclusion_severity_score: 55.0, institutional_abandonment_scale_score: 52.0, risk_level: "élevé", primary_pattern: "discrimination_exclusion_severity", estimated_albinism_rights_index: 5.29, last_updated: "2026-06-21" },
    { id: "AL-006", name: "Burundi/Rwanda — Enfants Albinos Cachés par Familles, Abandon Scolaire & Isolement Communautaire", country: "Afrique Centrale", composite_score: 50.3, ritual_killing_body_parts_trade_score: 48.0, legal_protection_enforcement_gap_score: 50.0, discrimination_exclusion_severity_score: 52.0, institutional_abandonment_scale_score: 52.0, risk_level: "élevé", primary_pattern: "institutional_abandonment_scale", estimated_albinism_rights_index: 5.03, last_updated: "2026-06-21" },
    { id: "AL-007", name: "Under the Same Sun/UTSS — Base Données Meurtres Globale, Advocacy ONU & Kits Protection Solaire", country: "Global", composite_score: 25.85, ritual_killing_body_parts_trade_score: 22.0, legal_protection_enforcement_gap_score: 28.0, discrimination_exclusion_severity_score: 25.0, institutional_abandonment_scale_score: 30.0, risk_level: "modéré", primary_pattern: "institutional_abandonment_scale", estimated_albinism_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "AL-008", name: "ONU/OHCHR — Résolution 2015 Albinisme, Rapporteur Indépendant Ikponwosa Ero & CRPD Art.8", country: "Global", composite_score: 4.4, ritual_killing_body_parts_trade_score: 4.0, legal_protection_enforcement_gap_score: 5.0, discrimination_exclusion_severity_score: 3.0, institutional_abandonment_scale_score: 6.0, risk_level: "faible", primary_pattern: "legal_protection_enforcement_gap", estimated_albinism_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/albinism-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
