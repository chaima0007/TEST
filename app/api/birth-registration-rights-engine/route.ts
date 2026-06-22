import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[birth-registration-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Birth Registration Rights Engine Agent",
  domain: "birth_registration_rights",
  total_entities: 8,
  avg_composite: 60.19,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    civil_registry_collapse: 2,
    documentation_access_barrier: 2,
    unregistered_births: 2,
    stateless_children_risk: 2,
  },
  top_risk_entities: [
    "Somalia — 60% Naissances Non Enregistrées, Effondrement État Civil & Génération Apatride",
    "RDC — 75% Naissances Sans Acte, Zones Rurales Sans Registre Civil & Enfants Invisibles",
    "Yémen — 40% Naissances Non Enregistrées en Temps de Guerre & Déni d'Existence Légale",
  ],
  critical_alerts: [
    "Somalia — 60% Naissances Non Enregistrées, Effondrement État Civil & Génération Apatride: civil_registry_collapse",
    "Yémen — 40% Naissances Non Enregistrées en Temps de Guerre & Déni d'Existence Légale: documentation_access_barrier",
    "RDC — 75% Naissances Sans Acte, Zones Rurales Sans Registre Civil & Enfants Invisibles: unregistered_births",
    "Tchad — 67% Naissances Non Enregistrées, Mariages Précoces Sans Trace & Invisibilité Légale: unregistered_births",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_birth_registration_rights_index: 6.02,
  data_sources: [
    "unicef_birth_registration_global_database_2024",
    "unhcr_global_trends_statelessness_2024",
    "world_bank_id4d_identification_development_initiative",
    "un_committee_rights_child_periodic_reviews",
  ],
  entities: [
    {
      entity_id: "BRR-001",
      name: "Somalia — 60% Naissances Non Enregistrées, Effondrement État Civil & Génération Apatride",
      country: "Somalie",
      sector: "60% naissances non enregistrées UNICEF 2024, registres civils détruits guerre civile depuis 1991, enfants nés zones al-Shabaab sans aucun document, apatridie transgénérationnelle",
      composite_score: 90.8,
      unregistered_births_score: 92.0,
      stateless_children_risk_score: 90.0,
      documentation_access_barrier_score: 88.0,
      civil_registry_collapse_score: 92.0,
      risk_level: "critique",
      primary_pattern: "civil_registry_collapse",
      estimated_birth_registration_rights_index: 9.08,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BRR-002",
      name: "Yémen — 40% Naissances Non Enregistrées en Temps de Guerre & Déni d'Existence Légale",
      country: "Yémen",
      sector: "40% naissances non enregistrées pendant conflit armé, bureaux état civil fermés 70% territoire",
      composite_score: 87.25,
      unregistered_births_score: 85.0,
      stateless_children_risk_score: 88.0,
      documentation_access_barrier_score: 90.0,
      civil_registry_collapse_score: 85.0,
      risk_level: "critique",
      primary_pattern: "documentation_access_barrier",
      estimated_birth_registration_rights_index: 8.73,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BRR-003",
      name: "RDC — 75% Naissances Sans Acte, Zones Rurales Sans Registre Civil & Enfants Invisibles",
      country: "République Démocratique du Congo",
      sector: "75% naissances non enregistrées UNICEF 2023, registres civils absents dans 80% des zones rurales",
      composite_score: 85.85,
      unregistered_births_score: 88.0,
      stateless_children_risk_score: 82.0,
      documentation_access_barrier_score: 85.0,
      civil_registry_collapse_score: 88.0,
      risk_level: "critique",
      primary_pattern: "unregistered_births",
      estimated_birth_registration_rights_index: 8.59,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BRR-004",
      name: "Tchad — 67% Naissances Non Enregistrées, Mariages Précoces Sans Trace & Invisibilité Légale",
      country: "Tchad",
      sector: "67% naissances non enregistrées UNICEF 2024, zones pastorales sans accès registre civil",
      composite_score: 80.0,
      unregistered_births_score: 80.0,
      stateless_children_risk_score: 78.0,
      documentation_access_barrier_score: 82.0,
      civil_registry_collapse_score: 80.0,
      risk_level: "critique",
      primary_pattern: "unregistered_births",
      estimated_birth_registration_rights_index: 8.0,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BRR-005",
      name: "Pakistan — 30% Enfants Non Enregistrés, Baloutchistan/FATA & Discrimination Religieuse",
      country: "Pakistan",
      sector: "30% enfants non enregistrés estimation UNICEF, minorités ahmadies exclues système enregistrement",
      composite_score: 53.5,
      unregistered_births_score: 55.0,
      stateless_children_risk_score: 52.0,
      documentation_access_barrier_score: 58.0,
      civil_registry_collapse_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "documentation_access_barrier",
      estimated_birth_registration_rights_index: 5.35,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BRR-006",
      name: "Bangladesh — Bidonvilles Dhaka & Réfugiés Rohingyas Sans Papiers, 200 000 Enfants Invisibles",
      country: "Bangladesh",
      sector: "Réfugiés rohingyas 200 000 enfants nés camps Cox's Bazar sans nationalité",
      composite_score: 51.5,
      unregistered_births_score: 50.0,
      stateless_children_risk_score: 58.0,
      documentation_access_barrier_score: 52.0,
      civil_registry_collapse_score: 45.0,
      risk_level: "élevé",
      primary_pattern: "stateless_children_risk",
      estimated_birth_registration_rights_index: 5.15,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BRR-007",
      name: "Inde — Assam/NRC Exclusions, 1,9M Sans Nationalité & Couverture Aadhaar Inégale",
      country: "Inde",
      sector: "NRC Assam 1,9M personnes exclues registre national citoyens 2019",
      composite_score: 30.25,
      unregistered_births_score: 30.0,
      stateless_children_risk_score: 35.0,
      documentation_access_barrier_score: 32.0,
      civil_registry_collapse_score: 25.0,
      risk_level: "modéré",
      primary_pattern: "stateless_children_risk",
      estimated_birth_registration_rights_index: 3.03,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "BRR-008",
      name: "Estonie — e-Residency, Registre Civil Digital & Meilleure Pratique Mondiale",
      country: "Estonie",
      sector: "e-Residency programme mondial 100 000 participants, enregistrement naissance numérique 99.9% couverture",
      composite_score: 2.05,
      unregistered_births_score: 2.0,
      stateless_children_risk_score: 3.0,
      documentation_access_barrier_score: 2.0,
      civil_registry_collapse_score: 1.0,
      risk_level: "faible",
      primary_pattern: "civil_registry_collapse",
      estimated_birth_registration_rights_index: 0.21,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/api/birth-registration-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
