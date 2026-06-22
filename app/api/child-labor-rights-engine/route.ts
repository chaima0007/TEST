import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[child-labor-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Child Labor Rights Engine Agent",
  domain: "child_labor_rights",
  total_entities: 8,
  avg_composite: 62.99,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Mali — Enfants Mines Or Artisanales, Travail Forcé Conflits Armés & Déscolarisation 60%",
    "RD Congo — Enfants Mines Cobalt Katanga, Travail Danger Chaîne Apple/Tesla & Impunité Totale",
    "Myanmar — Enfants Soldats Tatmadaw, Conscription Forcée Post-Coup 2021 & Travail Plantations",
  ],
  critical_alerts: [
    "Mali: worst_forms_child_labor_score",
    "RD Congo: hazardous_work_exposure_score",
    "Myanmar: worst_forms_child_labor_score",
    "Bangladesh: child_labor_supply_chain_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_child_labor_rights_index: 6.30,
  entities: [
    {
      entity_id: "CLR-001",
      name: "Mali — Enfants Mines Or Artisanales, Travail Forcé Conflits Armés & Déscolarisation 60%",
      country: "Mali",
      worst_forms_child_labor_score: 96.0,
      hazardous_work_exposure_score: 94.0,
      school_exclusion_score: 93.0,
      child_labor_supply_chain_score: 92.0,
      composite_score: 93.95,
      risk_level: "critique",
      primary_pattern: "worst_forms_child_labor_score",
      estimated_child_labor_rights_index: 9.40,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CLR-002",
      name: "RD Congo — Enfants Mines Cobalt Katanga, Travail Danger Chaîne Apple/Tesla & Impunité Totale",
      country: "RD Congo",
      worst_forms_child_labor_score: 95.0,
      hazardous_work_exposure_score: 96.0,
      school_exclusion_score: 91.0,
      child_labor_supply_chain_score: 94.0,
      composite_score: 94.0,
      risk_level: "critique",
      primary_pattern: "hazardous_work_exposure_score",
      estimated_child_labor_rights_index: 9.40,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CLR-003",
      name: "Myanmar — Enfants Soldats Tatmadaw, Conscription Forcée Post-Coup 2021 & Travail Plantations",
      country: "Myanmar",
      worst_forms_child_labor_score: 94.0,
      hazardous_work_exposure_score: 90.0,
      school_exclusion_score: 92.0,
      child_labor_supply_chain_score: 89.0,
      composite_score: 91.55,
      risk_level: "critique",
      primary_pattern: "worst_forms_child_labor_score",
      estimated_child_labor_rights_index: 9.16,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CLR-004",
      name: "Bangladesh — Ateliers Textile, 5% Enfants Industrie Vêtement & Accidents Rana Plaza Récurrents",
      country: "Bangladesh",
      worst_forms_child_labor_score: 88.0,
      hazardous_work_exposure_score: 87.0,
      school_exclusion_score: 82.0,
      child_labor_supply_chain_score: 90.0,
      composite_score: 86.9,
      risk_level: "critique",
      primary_pattern: "child_labor_supply_chain_score",
      estimated_child_labor_rights_index: 8.69,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CLR-005",
      name: "Brésil — Travail Enfants Agriculture Canne à Sucre/Café, Zone Rurale & Lacunes Inspection",
      country: "Brésil",
      worst_forms_child_labor_score: 52.0,
      hazardous_work_exposure_score: 55.0,
      school_exclusion_score: 48.0,
      child_labor_supply_chain_score: 50.0,
      composite_score: 51.35,
      risk_level: "élevé",
      primary_pattern: "hazardous_work_exposure_score",
      estimated_child_labor_rights_index: 5.14,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CLR-006",
      name: "Inde — Enfants Industrie Tapis/Briques, 4,5 Millions Travailleurs & Faible Application Loi",
      country: "Inde",
      worst_forms_child_labor_score: 47.0,
      hazardous_work_exposure_score: 49.0,
      school_exclusion_score: 44.0,
      child_labor_supply_chain_score: 46.0,
      composite_score: 46.6,
      risk_level: "élevé",
      primary_pattern: "hazardous_work_exposure_score",
      estimated_child_labor_rights_index: 4.66,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CLR-007",
      name: "Pérou — Travail Informel Enfants Marchés Andins, Lacunes Scolarisation Zones Rurales",
      country: "Pérou",
      worst_forms_child_labor_score: 30.0,
      hazardous_work_exposure_score: 28.0,
      school_exclusion_score: 32.0,
      child_labor_supply_chain_score: 27.0,
      composite_score: 29.4,
      risk_level: "modéré",
      primary_pattern: "school_exclusion_score",
      estimated_child_labor_rights_index: 2.94,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CLR-008",
      name: "Finlande — Zéro Travail Enfants, Scolarité Obligatoire 18 Ans & Contrôles Chaînes Approvisionnement",
      country: "Finlande",
      worst_forms_child_labor_score: 11.0,
      hazardous_work_exposure_score: 10.0,
      school_exclusion_score: 9.0,
      child_labor_supply_chain_score: 12.0,
      composite_score: 10.55,
      risk_level: "faible",
      primary_pattern: "child_labor_supply_chain_score",
      estimated_child_labor_rights_index: 1.06,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/child-labor-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
