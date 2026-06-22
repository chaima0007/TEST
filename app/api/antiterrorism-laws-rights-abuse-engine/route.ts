import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[antiterrorism-laws-rights-abuse-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Antiterrorism Laws Rights Abuse Engine Agent",
  domain: "antiterrorism_laws_rights_abuse",
  total_entities: 8,
  avg_composite: 63.20,
  confidence_score: 0.86,
  avg_estimated_antiterrorism_laws_rights_abuse_index: 6.32,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  data_sources: [
    "amnesty_international_counterterrorism_rights_2023",
    "human_rights_watch_antiterrorism_abuses_2023",
    "international_commission_jurists_emergency_powers_2023",
    "un_special_rapporteur_counterterrorism_2023",
  ],
  entities: [
    { id: "ALA-001", name: "Chine — Lois Sécurité Nationale: Désignation Terroriste Ouïghours, Tibet & Hong Kong Dissidents", country: "Asie du Nord-Est", composite_score: 95.10, risk_level: "critique", estimated_antiterrorism_laws_rights_abuse_index: 9.51, last_updated: "2026-06-21" },
    { id: "ALA-002", name: "Russie — Lois Antiterrorisme Yarova: Criminalisation Dissidence, VPN & Journalisme Indépendant", country: "Europe de l'Est", composite_score: 90.85, risk_level: "critique", estimated_antiterrorism_laws_rights_abuse_index: 9.09, last_updated: "2026-06-21" },
    { id: "ALA-003", name: "Égypte — État Urgence Permanent: Détentions Massives, Tribunaux Militaires & Défenseurs Droits", country: "Afrique du Nord", composite_score: 87.40, risk_level: "critique", estimated_antiterrorism_laws_rights_abuse_index: 8.74, last_updated: "2026-06-21" },
    { id: "ALA-004", name: "Inde — UAPA: Arrestations Militants Droits, Intellectuels Dalits & Journalistes Cachemire", country: "Asie du Sud", composite_score: 83.65, risk_level: "critique", estimated_antiterrorism_laws_rights_abuse_index: 8.37, last_updated: "2026-06-21" },
    { id: "ALA-005", name: "USA/Patriot Act — Surveillance NSA, FISA Court Secret & Profiling Communautés Musulmanes", country: "Amérique du Nord", composite_score: 55.20, risk_level: "élevé", estimated_antiterrorism_laws_rights_abuse_index: 5.52, last_updated: "2026-06-21" },
    { id: "ALA-006", name: "France — Lois SILT & Algos Surveillance: Risque Glissement Vers Contrôle Politique Minorités", country: "Europe", composite_score: 48.90, risk_level: "élevé", estimated_antiterrorism_laws_rights_abuse_index: 4.89, last_updated: "2026-06-21" },
    { id: "ALA-007", name: "Commission ICJ — Normes Due Process, Détention Sans Procès & Standards Juridiques Globaux", country: "Global", composite_score: 29.15, risk_level: "modéré", estimated_antiterrorism_laws_rights_abuse_index: 2.92, last_updated: "2026-06-21" },
    { id: "ALA-008", name: "ONU Rapporteur Spécial Antiterrorisme — Mandats, Revues Périodiques & Recommandations États", country: "Global", composite_score: 6.75, risk_level: "faible", estimated_antiterrorism_laws_rights_abuse_index: 0.68, last_updated: "2026-06-21" },
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/antiterrorism-laws-rights-abuse-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
