import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[statelessness-document-rights-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  domain: "statelessness_document_rights",
  generated_at: new Date().toISOString(),
  accent: "#b45309",
  avg_composite: 62.29,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    { id: "SDR-001", name: "Myanmar — Rohingyas 1M Apatrides, Génocide Documentaire & Juridique", composite_score: 94.40, risk_level: "critique", stateless_population_scale_score: 95, documentation_access_denial_score: 96, legal_protection_framework_gap_score: 94, political_will_resolution_deficit_score: 92, estimated_statelessness_document_rights_index: 9.44 },
    { id: "SDR-002", name: "Côte d'Ivoire — 700K Apatrides Post-Conflit, Enfants Sans Acte de Naissance", composite_score: 87.65, risk_level: "critique", stateless_population_scale_score: 88, documentation_access_denial_score: 90, legal_protection_framework_gap_score: 87, political_will_resolution_deficit_score: 85, estimated_statelessness_document_rights_index: 8.77 },
    { id: "SDR-003", name: "Bangladesh — Bihari 300K Apatrides 50 Ans, Camps Génération Perdue", composite_score: 87.00, risk_level: "critique", stateless_population_scale_score: 85, documentation_access_denial_score: 88, legal_protection_framework_gap_score: 86, political_will_resolution_deficit_score: 90, estimated_statelessness_document_rights_index: 8.70 },
    { id: "SDR-004", name: "Kuwait — Bidun 100K Résidents Sans Citoyenneté Depuis 1961", composite_score: 83.45, risk_level: "critique", stateless_population_scale_score: 82, documentation_access_denial_score: 85, legal_protection_framework_gap_score: 80, political_will_resolution_deficit_score: 88, estimated_statelessness_document_rights_index: 8.34 },
    { id: "SDR-005", name: "République Dominicaine — Dénationalisation Haïtiens, Arrêt TC 168-13", composite_score: 57.50, risk_level: "élevé", stateless_population_scale_score: 55, documentation_access_denial_score: 58, legal_protection_framework_gap_score: 62, political_will_resolution_deficit_score: 55, estimated_statelessness_document_rights_index: 5.75 },
    { id: "SDR-006", name: "Thaïlande — Peuples Montagnards 500K Sans Papiers, Bouddhistes Exclus", composite_score: 53.45, risk_level: "élevé", stateless_population_scale_score: 52, documentation_access_denial_score: 55, legal_protection_framework_gap_score: 50, political_will_resolution_deficit_score: 58, estimated_statelessness_document_rights_index: 5.34 },
    { id: "SDR-007", name: "Ukraine — Réfugiés Post-Guerre, Enregistrement Civil Ukrainien Partiel", composite_score: 26.55, risk_level: "modéré", stateless_population_scale_score: 28, documentation_access_denial_score: 25, legal_protection_framework_gap_score: 30, political_will_resolution_deficit_score: 22, estimated_statelessness_document_rights_index: 2.65 },
    { id: "SDR-008", name: "Lettonie — Résolution Apatridie Soviet, Naturalisation Facilitée Récente", composite_score: 8.30, risk_level: "faible", stateless_population_scale_score: 10, documentation_access_denial_score: 8, legal_protection_framework_gap_score: 6, political_will_resolution_deficit_score: 9, estimated_statelessness_document_rights_index: 0.83 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/statelessness-document-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
