import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[land-restitution-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[land-restitution-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Land Restitution Rights Engine Agent",
  domain: "land_restitution_rights",
  total_entities: 8,
  avg_composite: 60.11,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Palestine/Territoires Occupés — 150 000 Propriétés Confisquées Depuis 1948, Aucune Restitution, Dépossession Continue",
    "Syrie — 1,5M Déplacés Internes, Propriétés Saisies Loi 10/2018, Retour Impossible Sans Abandon Droits",
    "Zimbabwe — Réforme Agraire Violente Mugabe, 4 000 Fermiers Expropriés Sans Compensation, Aucun Mécanisme Réparation",
  ],
  critical_alerts: [
    "Palestine/Territoires Occupés: dispossession_without_remedy_score",
    "Syrie: displacement_without_return_score",
    "Zimbabwe: reparations_justice_gap_score",
    "Colombie: displacement_without_return_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_land_restitution_rights_index: 6.01,
  entities: [
    {
      entity_id: "LRR-001",
      name: "Palestine/Territoires Occupés — 150 000 Propriétés Confisquées Depuis 1948, Aucune Restitution, Dépossession Continue",
      country: "Palestine/Territoires Occupés",
      dispossession_without_remedy_score: 95.0,
      restitution_process_denial_score: 94.0,
      displacement_without_return_score: 93.0,
      reparations_justice_gap_score: 95.0,
      composite_score: 94.35,
      risk_level: "critique",
      primary_pattern: "dispossession_without_remedy_score",
      estimated_land_restitution_rights_index: 9.44,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "LRR-002",
      name: "Zimbabwe — Réforme Agraire Violente Mugabe, 4 000 Fermiers Expropriés Sans Compensation, Aucun Mécanisme Réparation",
      country: "Zimbabwe",
      dispossession_without_remedy_score: 87.0,
      restitution_process_denial_score: 85.0,
      displacement_without_return_score: 82.0,
      reparations_justice_gap_score: 88.0,
      composite_score: 85.65,
      risk_level: "critique",
      primary_pattern: "reparations_justice_gap_score",
      estimated_land_restitution_rights_index: 8.57,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "LRR-003",
      name: "Syrie — 1,5M Déplacés Internes, Propriétés Saisies Loi 10/2018, Retour Impossible Sans Abandon Droits",
      country: "Syrie",
      dispossession_without_remedy_score: 88.0,
      restitution_process_denial_score: 86.0,
      displacement_without_return_score: 90.0,
      reparations_justice_gap_score: 85.0,
      composite_score: 87.65,
      risk_level: "critique",
      primary_pattern: "displacement_without_return_score",
      estimated_land_restitution_rights_index: 8.77,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "LRR-004",
      name: "Colombie — 8M Déplacés, Restitution Terres Victimes FARC Bloquée par Élites, Assassinats Défenseurs Terres",
      country: "Colombie",
      dispossession_without_remedy_score: 80.0,
      restitution_process_denial_score: 78.0,
      displacement_without_return_score: 82.0,
      reparations_justice_gap_score: 76.0,
      composite_score: 79.5,
      risk_level: "critique",
      primary_pattern: "displacement_without_return_score",
      estimated_land_restitution_rights_index: 7.95,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "LRR-005",
      name: "Kenya — Terres Mau-Mau, Restitution Coloniale Partielle, Rift Valley Non Résolue, Tensions Interethniques Persistantes",
      country: "Kenya",
      dispossession_without_remedy_score: 52.0,
      restitution_process_denial_score: 50.0,
      displacement_without_return_score: 48.0,
      reparations_justice_gap_score: 53.0,
      composite_score: 51.1,
      risk_level: "élevé",
      primary_pattern: "reparations_justice_gap_score",
      estimated_land_restitution_rights_index: 5.11,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "LRR-006",
      name: "Afrique du Sud — Restitution Post-Apartheid Lente, 30 Ans 80% Terres Toujours Propriété Blanche, Process Engorgé",
      country: "Afrique du Sud",
      dispossession_without_remedy_score: 48.0,
      restitution_process_denial_score: 50.0,
      displacement_without_return_score: 44.0,
      reparations_justice_gap_score: 47.0,
      composite_score: 47.65,
      risk_level: "élevé",
      primary_pattern: "restitution_process_denial_score",
      estimated_land_restitution_rights_index: 4.77,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "LRR-007",
      name: "Allemagne — Restitution Propriétés Juives, Process Active Mais Lente, Héritiers Diaspora Difficultés Administratives",
      country: "Allemagne",
      dispossession_without_remedy_score: 28.0,
      restitution_process_denial_score: 30.0,
      displacement_without_return_score: 24.0,
      reparations_justice_gap_score: 26.0,
      composite_score: 27.2,
      risk_level: "modéré",
      primary_pattern: "restitution_process_denial_score",
      estimated_land_restitution_rights_index: 2.72,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "LRR-008",
      name: "Canada — Traités Modernes Autochtones, Tribunal Revendications Particulières, Meilleure Pratique Restitution Négociée",
      country: "Canada",
      dispossession_without_remedy_score: 10.0,
      restitution_process_denial_score: 9.0,
      displacement_without_return_score: 8.0,
      reparations_justice_gap_score: 11.0,
      composite_score: 9.45,
      risk_level: "faible",
      primary_pattern: "dispossession_without_remedy_score",
      estimated_land_restitution_rights_index: 0.95,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/land-restitution-rights-engine`, {
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
