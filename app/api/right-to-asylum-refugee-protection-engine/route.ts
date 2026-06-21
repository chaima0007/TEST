import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-asylum-refugee-protection-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "right_to_asylum_refugee_protection_engine",
  domain: "right_to_asylum_refugee_protection",
  total_entities: 8,
  avg_composite: 61.34,
  confidence_score: 0.91,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    pushback_refoulement: 4,
    detention_conditions: 3,
    procedure_obstruction: 1,
  },
  top_risk_entities: [
    { id: "RAR-001", name: "Australie — Offshore Processing Nauru/PNG", score: 93.25, risk: "critique" },
    { id: "RAR-002", name: "Hongrie/UE — Clôtures Barbelées & Pushbacks Illégaux", score: 90.2, risk: "critique" },
    { id: "RAR-003", name: "Libye/EU — Garde-Côtes Financés & Centres Détention", score: 87.2, risk: "critique" },
  ],
  critical_alerts: [
    "RAR-001: Australie — Offshore Processing Nauru/PNG — composite 93.25",
    "RAR-002: Hongrie/UE — Clôtures Barbelées & Pushbacks Illégaux — composite 90.2",
    "RAR-003: Libye/EU — Garde-Côtes Financés & Centres Détention — composite 87.2",
    "RAR-004: USA/Trump — MPP/Attendre au Mexique & Titre 42 — composite 84.7",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_right_to_asylum_refugee_protection_index: 6.13,
  data_sources: [
    "unhcr_global_trends_forced_displacement_report",
    "amnesty_pushback_refoulement_documentation",
    "borderline_europe_camp_conditions_monitoring",
  ],
  entities: [
    {
      id: "RAR-001",
      name: "Australie — Offshore Processing Nauru/PNG",
      country: "Australie",
      pushback_refoulement_severity_score: 95.0,
      detention_asylum_seeker_conditions_scale_score: 92.0,
      refugee_camp_rights_violation_score: 93.0,
      asylum_procedure_denial_obstruction_gap_score: 91.0,
      composite_score: 93.25,
      risk_level: "critique",
      primary_pattern: "Détention Indéfinie, Refoulement & Bateaux Repoussés",
      estimated_right_to_asylum_refugee_protection_index: 9.33,
      last_updated: "2026-06-21",
    },
    {
      id: "RAR-002",
      name: "Hongrie/UE — Clôtures Barbelées & Pushbacks Illégaux",
      country: "Hongrie",
      pushback_refoulement_severity_score: 92.0,
      detention_asylum_seeker_conditions_scale_score: 89.0,
      refugee_camp_rights_violation_score: 90.0,
      asylum_procedure_denial_obstruction_gap_score: 88.0,
      composite_score: 90.2,
      risk_level: "critique",
      primary_pattern: "Pushbacks Illégaux Croatie, Hotspots Surpeuplés & Demandes Irrecevables",
      estimated_right_to_asylum_refugee_protection_index: 9.02,
      last_updated: "2026-06-21",
    },
    {
      id: "RAR-003",
      name: "Libye/EU — Garde-Côtes Financés & Centres Détention",
      country: "Libye",
      pushback_refoulement_severity_score: 89.0,
      detention_asylum_seeker_conditions_scale_score: 87.0,
      refugee_camp_rights_violation_score: 86.0,
      asylum_procedure_denial_obstruction_gap_score: 85.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "Retour Migrant Torture, Centres Détention Inhumains & OIM Financement",
      estimated_right_to_asylum_refugee_protection_index: 8.72,
      last_updated: "2026-06-21",
    },
    {
      id: "RAR-004",
      name: "USA/Trump — MPP/Attendre au Mexique & Titre 42",
      country: "USA",
      pushback_refoulement_severity_score: 86.0,
      detention_asylum_seeker_conditions_scale_score: 83.0,
      refugee_camp_rights_violation_score: 83.0,
      asylum_procedure_denial_obstruction_gap_score: 84.0,
      composite_score: 84.2,
      risk_level: "critique",
      primary_pattern: "Politique MPP, Expulsions COVID, Séparation Familles & Demandes Annulées",
      estimated_right_to_asylum_refugee_protection_index: 8.42,
      last_updated: "2026-06-21",
    },
    {
      id: "RAR-005",
      name: "Grèce — Pushbacks Égée & Camps Samos Surpeuplés",
      country: "Grèce",
      pushback_refoulement_severity_score: 57.0,
      detention_asylum_seeker_conditions_scale_score: 54.0,
      refugee_camp_rights_violation_score: 55.0,
      asylum_procedure_denial_obstruction_gap_score: 53.0,
      composite_score: 55.1,
      risk_level: "élevé",
      primary_pattern: "Pushbacks Égée Documentés, Demandeurs Asile Illégalement Expulsés",
      estimated_right_to_asylum_refugee_protection_index: 5.51,
      last_updated: "2026-06-21",
    },
    {
      id: "RAR-006",
      name: "Turquie — 3.5M Réfugiés Syriens & Déportations",
      country: "Turquie",
      pushback_refoulement_severity_score: 54.0,
      detention_asylum_seeker_conditions_scale_score: 51.0,
      refugee_camp_rights_violation_score: 52.0,
      asylum_procedure_denial_obstruction_gap_score: 50.0,
      composite_score: 52.15,
      risk_level: "élevé",
      primary_pattern: "Pression Retour Syriens, Déportations Forcées & Naturalisation Refusée",
      estimated_right_to_asylum_refugee_protection_index: 5.22,
      last_updated: "2026-06-21",
    },
    {
      id: "RAR-007",
      name: "HCR/OIM — Standards Protection Internationale",
      country: "International",
      pushback_refoulement_severity_score: 27.0,
      detention_asylum_seeker_conditions_scale_score: 25.0,
      refugee_camp_rights_violation_score: 26.0,
      asylum_procedure_denial_obstruction_gap_score: 25.0,
      composite_score: 25.9,
      risk_level: "modéré",
      primary_pattern: "Burden Sharing & Protocoles Détermination Statut",
      estimated_right_to_asylum_refugee_protection_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      id: "RAR-008",
      name: "ONU/Convention 1951 — Non-Refoulement & SDG 10.7",
      country: "International",
      pushback_refoulement_severity_score: 4.0,
      detention_asylum_seeker_conditions_scale_score: 4.0,
      refugee_camp_rights_violation_score: 4.0,
      asylum_procedure_denial_obstruction_gap_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "Convention Réfugiés, Protocole 1967 & Non-Refoulement",
      estimated_right_to_asylum_refugee_protection_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-asylum-refugee-protection-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
