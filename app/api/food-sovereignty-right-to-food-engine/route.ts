import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Food Sovereignty Right to Food Engine Agent",
  domain: "food_sovereignty_right_to_food",
  total_entities: 8,
  avg_composite: 63.33,
  confidence_score: 0.86,
  avg_estimated_food_sovereignty_right_to_food_index: 6.33,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  data_sources: [
    "fao_sofi_2023",
    "wfp_global_report_food_crises_2023",
    "un_sr_right_to_food_2023",
    "ihh_humanitarian_right_food_2022",
  ],
  critical_alerts: [
    "Yémen/Famine IPC5: food_insecurity_famine_severity",
    "Somalie/Sécheresse & Al-Shabaab: food_system_collapse_conflict",
    "Éthiopie/Tigré: food_system_collapse_conflict",
    "Haïti/Crise Alimentaire & Gangs: food_insecurity_famine_severity",
  ],
  entities: [
    {
      id: "FSRF-001",
      name: "Yémen/Famine IPC5 — 21M en Insécurité Alimentaire, 160K Phase Catastrophe IPC5, Blocus Ports & Destruction Infrastructure Agricole par Coalition",
      country: "Yémen",
      composite_score: 91.6,
      food_insecurity_famine_severity_score: 95.0,
      right_to_food_legal_protection_gap_score: 90.0,
      food_system_collapse_conflict_score: 92.0,
      structural_hunger_exclusion_score: 88.0,
      risk_level: "critique",
      primary_pattern: "food_insecurity_famine_severity",
      estimated_food_sovereignty_right_to_food_index: 9.16,
      last_updated: "2026-06-21",
    },
    {
      id: "FSRF-002",
      name: "Somalie/Sécheresse & Al-Shabaab — Famine Récurrente, 6.5M en Crise Alimentaire, Sécheresses La Niña Cumulées & Insécurité Al-Shabaab Bloquant Aide Humanitaire",
      country: "Somalie",
      composite_score: 86.65,
      food_insecurity_famine_severity_score: 90.0,
      right_to_food_legal_protection_gap_score: 85.0,
      food_system_collapse_conflict_score: 88.0,
      structural_hunger_exclusion_score: 82.0,
      risk_level: "critique",
      primary_pattern: "food_system_collapse_conflict",
      estimated_food_sovereignty_right_to_food_index: 8.67,
      last_updated: "2026-06-21",
    },
    {
      id: "FSRF-003",
      name: "Éthiopie/Tigré — Famine Arme de Guerre, 900K Phase Urgence, Siège Militaire Tigré & Destruction Cultures par Forces Armées Documentée ONU",
      country: "Éthiopie",
      composite_score: 85.4,
      food_insecurity_famine_severity_score: 88.0,
      right_to_food_legal_protection_gap_score: 82.0,
      food_system_collapse_conflict_score: 90.0,
      structural_hunger_exclusion_score: 80.0,
      risk_level: "critique",
      primary_pattern: "food_system_collapse_conflict",
      estimated_food_sovereignty_right_to_food_index: 8.54,
      last_updated: "2026-06-21",
    },
    {
      id: "FSRF-004",
      name: "Haïti/Crise Alimentaire & Gangs — 5.2M en Insécurité Alimentaire Aigüe, Contrôle Gangs 85% Port-au-Prince, Effondrement Agriculture & Blocage Aide",
      country: "Haïti",
      composite_score: 81.6,
      food_insecurity_famine_severity_score: 85.0,
      right_to_food_legal_protection_gap_score: 80.0,
      food_system_collapse_conflict_score: 82.0,
      structural_hunger_exclusion_score: 78.0,
      risk_level: "critique",
      primary_pattern: "food_insecurity_famine_severity",
      estimated_food_sovereignty_right_to_food_index: 8.16,
      last_updated: "2026-06-21",
    },
    {
      id: "FSRF-005",
      name: "RCA/Conflit & 2.5M Déplacés — République Centrafricaine, 2.5M Déplacés Affamés, Groupes Armés Pillant Ressources Alimentaires & Effondrement Services Agricoles",
      country: "République Centrafricaine",
      composite_score: 54.15,
      food_insecurity_famine_severity_score: 58.0,
      right_to_food_legal_protection_gap_score: 52.0,
      food_system_collapse_conflict_score: 55.0,
      structural_hunger_exclusion_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "structural_hunger_exclusion",
      estimated_food_sovereignty_right_to_food_index: 5.42,
      last_updated: "2026-06-21",
    },
    {
      id: "FSRF-006",
      name: "Madagascar/Sécheresse Sud Kere — 1.3M Personnes Phase Crise-Urgence, Sécheresse Sud Grand-Sud Exceptionnelle, Kere (Famine Traditionnelle) & Malnutrition Enfants 20%",
      country: "Madagascar",
      composite_score: 58.65,
      food_insecurity_famine_severity_score: 60.0,
      right_to_food_legal_protection_gap_score: 55.0,
      food_system_collapse_conflict_score: 58.0,
      structural_hunger_exclusion_score: 62.0,
      risk_level: "élevé",
      primary_pattern: "structural_hunger_exclusion",
      estimated_food_sovereignty_right_to_food_index: 5.87,
      last_updated: "2026-06-21",
    },
    {
      id: "FSRF-007",
      name: "Venezuela/Effondrement Économique — Hyperinflation 2019-2023, 7.7M en Insécurité Alimentaire Modérée-Sévère, Pénuries Chroniques & Émigration 7.7M Réfugiés",
      country: "Venezuela",
      composite_score: 38.65,
      food_insecurity_famine_severity_score: 40.0,
      right_to_food_legal_protection_gap_score: 38.0,
      food_system_collapse_conflict_score: 35.0,
      structural_hunger_exclusion_score: 42.0,
      risk_level: "modéré",
      primary_pattern: "right_to_food_legal_protection_gap",
      estimated_food_sovereignty_right_to_food_index: 3.87,
      last_updated: "2026-06-21",
    },
    {
      id: "FSRF-008",
      name: "Brésil/Fome Zero 2.0 Lula — Programme Bolsa Família Relancé, 33M Sortis Faim Sous Lula 2023, Politique Alimentaire Nationale & Droit Constitutionnel à l&apos;Alimentation",
      country: "Brésil",
      composite_score: 9.9,
      food_insecurity_famine_severity_score: 8.0,
      right_to_food_legal_protection_gap_score: 12.0,
      food_system_collapse_conflict_score: 6.0,
      structural_hunger_exclusion_score: 15.0,
      risk_level: "faible",
      primary_pattern: "right_to_food_legal_protection_gap",
      estimated_food_sovereignty_right_to_food_index: 0.99,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[food-sovereignty-right-to-food-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/food-sovereignty-right-to-food-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
