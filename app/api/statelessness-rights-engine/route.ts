import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[statelessness-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Statelessness Rights Engine Agent",
  domain: "statelessness_rights",
  total_entities: 8,
  avg_composite: 61.23,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { statelessness_legal_vulnerability_severity: 2, documentation_citizenship_denial_scale: 3, stateless_detention_expulsion_risk: 1, reduced_social_rights_access_barrier: 2 },
  top_risk_entities: [
    "Rohingya/Myanmar — 600 000 Apatrides, Génocide Reconnu ICJ 2019, Cambodge/Thaïlande Refoulements & Camps UNHCR",
    "Apatrides Golfe/Bidoun — Kuwait/UAE 100 000 Bidoun Sans Nationalité, Zéro Droit Légal & Arrestations Arbitraires",
    "Syrie/Conflit — 1M Nés Hors Registres Guerre, Déplacés Apatrides Région & Bureaucratie Accès Documents",
  ],
  critical_alerts: [
    "Rohingya/Myanmar: statelessness_legal_vulnerability_severity",
    "Apatrides Golfe/Bidoun: documentation_citizenship_denial_scale",
    "Syrie/Conflit: documentation_citizenship_denial_scale",
    "Afrique Subsaharienne: statelessness_legal_vulnerability_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_statelessness_rights_index: 6.12,
  data_sources: [
    "unhcr_ibelong_statelessness_campaign_report",
    "human_rights_watch_stateless_bidoun_gulf_report",
    "amnesty_international_rohingya_statelessness_report",
  ],
  entities: [
    { id: "STL-001", name: "Rohingya/Myanmar — 600 000 Apatrides, Génocide Reconnu ICJ 2019, Cambodge/Thaïlande Refoulements & Camps UNHCR", country: "Myanmar", composite_score: 93.15, statelessness_legal_vulnerability_severity_score: 95.0, documentation_citizenship_denial_scale_score: 93.0, stateless_detention_expulsion_risk_score: 92.0, reduced_social_rights_access_barrier_score: 92.0, risk_level: "critique", primary_pattern: "statelessness_legal_vulnerability_severity", estimated_statelessness_rights_index: 9.32, last_updated: "2026-06-21" },
    { id: "STL-002", name: "Apatrides Golfe/Bidoun — Kuwait/UAE 100 000 Bidoun Sans Nationalité, Zéro Droit Légal & Arrestations Arbitraires", country: "Kuwait", composite_score: 90.15, statelessness_legal_vulnerability_severity_score: 92.0, documentation_citizenship_denial_scale_score: 90.0, stateless_detention_expulsion_risk_score: 89.0, reduced_social_rights_access_barrier_score: 89.0, risk_level: "critique", primary_pattern: "documentation_citizenship_denial_scale", estimated_statelessness_rights_index: 9.02, last_updated: "2026-06-21" },
    { id: "STL-003", name: "Syrie/Conflit — 1M Nés Hors Registres Guerre, Déplacés Apatrides Région & Bureaucratie Accès Documents", country: "Syrie", composite_score: 86.75, statelessness_legal_vulnerability_severity_score: 89.0, documentation_citizenship_denial_scale_score: 87.0, stateless_detention_expulsion_risk_score: 86.0, reduced_social_rights_access_barrier_score: 84.0, risk_level: "critique", primary_pattern: "documentation_citizenship_denial_scale", estimated_statelessness_rights_index: 8.68, last_updated: "2026-06-21" },
    { id: "STL-004", name: "Afrique Subsaharienne — Communautés Nomades Kenya/Éthiopie, Migrations Sans Documents & Discrimination Ethnique", country: "Kenya", composite_score: 84.15, statelessness_legal_vulnerability_severity_score: 86.0, documentation_citizenship_denial_scale_score: 84.0, stateless_detention_expulsion_risk_score: 83.0, reduced_social_rights_access_barrier_score: 83.0, risk_level: "critique", primary_pattern: "statelessness_legal_vulnerability_severity", estimated_statelessness_rights_index: 8.42, last_updated: "2026-06-21" },
    { id: "STL-005", name: "Europe/Roms — 12 000 Apatrides Roms Balkans, Non-Enregistrement Naissance & Discrimination Accès Droits", country: "Balkans", composite_score: 53.95, statelessness_legal_vulnerability_severity_score: 56.0, documentation_citizenship_denial_scale_score: 54.0, stateless_detention_expulsion_risk_score: 53.0, reduced_social_rights_access_barrier_score: 52.0, risk_level: "élevé", primary_pattern: "documentation_citizenship_denial_scale", estimated_statelessness_rights_index: 5.4, last_updated: "2026-06-21" },
    { id: "STL-006", name: "Haïtiens Dominicains — Décision TC168/13 Rétroactive, 200 000 Dénaturalisés & Expulsions Sans Procédure", country: "République Dominicaine", composite_score: 51.4, statelessness_legal_vulnerability_severity_score: 53.0, documentation_citizenship_denial_scale_score: 51.0, stateless_detention_expulsion_risk_score: 51.0, reduced_social_rights_access_barrier_score: 50.0, risk_level: "élevé", primary_pattern: "stateless_detention_expulsion_risk", estimated_statelessness_rights_index: 5.14, last_updated: "2026-06-21" },
    { id: "STL-007", name: "UNHCR/IBelong — Campagne #IBelong Fin Apatridie 2024, Plans Action & Enregistrements Naissances", country: "Global", composite_score: 26.05, statelessness_legal_vulnerability_severity_score: 27.0, documentation_citizenship_denial_scale_score: 26.0, stateless_detention_expulsion_risk_score: 25.0, reduced_social_rights_access_barrier_score: 26.0, risk_level: "modéré", primary_pattern: "reduced_social_rights_access_barrier", estimated_statelessness_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "STL-008", name: "ONU/Convention 1954 — Convention Statut Apatrides 1954/1961, Mécanismes Identification & SDG 16.9 Identité Légale", country: "Global", composite_score: 4.2, statelessness_legal_vulnerability_severity_score: 4.0, documentation_citizenship_denial_scale_score: 4.0, stateless_detention_expulsion_risk_score: 4.0, reduced_social_rights_access_barrier_score: 5.0, risk_level: "faible", primary_pattern: "reduced_social_rights_access_barrier", estimated_statelessness_rights_index: 0.42, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/statelessness-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
