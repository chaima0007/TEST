import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[albinism-persecution-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Albinism Persecution Rights Engine Agent",
  domain: "albinism_persecution_rights",
  total_entities: 8,
  avg_composite: 57.96,
  confidence_score: 0.87,
  avg_estimated_albinism_persecution_rights_index: 5.80,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_independent_expert_albinism_2023",
    "usibc_albinism_report_2022",
    "amnesty_witchcraft_ritual_2023",
    "who_albinism_africa_2022",
  ],
  critical_alerts: [
    "Tanzanie: violence_rituelle_meurtre_membres",
    "Malawi: exhumations_trafic_albinos",
    "Mozambique: medecine_traditionnelle_trafic_transfrontalier",
    "Zambie: stigmatisation_violences_rurales",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  entities: [
    {
      entity_id: "APR-001",
      name: "Tanzanie — meurtres rituels et trafic de membres albinos parmi les plus documentés",
      country: "Tanzanie",
      violence_physique_meurtres_rituels_trafic_score: 92.0,
      impunite_judiciaire_absence_poursuites_score: 85.0,
      stigmatisation_sociale_exclusion_communautaire_score: 88.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 80.0,
      composite_score: 86.85,
      risk_level: "critique",
      primary_pattern: "violence_physique_meurtres_rituels_trafic",
      estimated_albinism_persecution_rights_index: 8.68,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "APR-002",
      name: "Malawi — vague d'attaques 2014-2018, exhumations de tombes albinos",
      country: "Malawi",
      violence_physique_meurtres_rituels_trafic_score: 88.0,
      impunite_judiciaire_absence_poursuites_score: 82.0,
      stigmatisation_sociale_exclusion_communautaire_score: 84.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 76.0,
      composite_score: 83.10,
      risk_level: "critique",
      primary_pattern: "violence_physique_meurtres_rituels_trafic",
      estimated_albinism_persecution_rights_index: 8.31,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "APR-003",
      name: "Mozambique — persécutions liées à la médecine traditionnelle et trafic transfrontalier",
      country: "Mozambique",
      violence_physique_meurtres_rituels_trafic_score: 82.0,
      impunite_judiciaire_absence_poursuites_score: 78.0,
      stigmatisation_sociale_exclusion_communautaire_score: 80.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 70.0,
      composite_score: 78.10,
      risk_level: "critique",
      primary_pattern: "impunite_judiciaire_absence_poursuites",
      estimated_albinism_persecution_rights_index: 7.81,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "APR-004",
      name: "Zambie — stigmatisation extrême et violences rituelles dans les zones rurales isolées",
      country: "Zambie",
      violence_physique_meurtres_rituels_trafic_score: 76.0,
      impunite_judiciaire_absence_poursuites_score: 72.0,
      stigmatisation_sociale_exclusion_communautaire_score: 78.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 65.0,
      composite_score: 73.30,
      risk_level: "critique",
      primary_pattern: "stigmatisation_sociale_exclusion_communautaire",
      estimated_albinism_persecution_rights_index: 7.33,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "APR-005",
      name: "Rwanda — discrimination sociale persistante malgré législation anti-discrimination",
      country: "Rwanda",
      violence_physique_meurtres_rituels_trafic_score: 52.0,
      impunite_judiciaire_absence_poursuites_score: 48.0,
      stigmatisation_sociale_exclusion_communautaire_score: 58.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 44.0,
      composite_score: 50.90,
      risk_level: "élevé",
      primary_pattern: "stigmatisation_sociale_exclusion_communautaire",
      estimated_albinism_persecution_rights_index: 5.09,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "APR-006",
      name: "Kenya — harcèlement communautaire et abandon scolaire des enfants albinos",
      country: "Kenya",
      violence_physique_meurtres_rituels_trafic_score: 50.0,
      impunite_judiciaire_absence_poursuites_score: 46.0,
      stigmatisation_sociale_exclusion_communautaire_score: 54.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 42.0,
      composite_score: 48.40,
      risk_level: "élevé",
      primary_pattern: "stigmatisation_sociale_exclusion_communautaire",
      estimated_albinism_persecution_rights_index: 4.84,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "APR-007",
      name: "Cameroun — exclusion familiale et accès limité aux soins dermatologiques",
      country: "Cameroun",
      violence_physique_meurtres_rituels_trafic_score: 32.0,
      impunite_judiciaire_absence_poursuites_score: 28.0,
      stigmatisation_sociale_exclusion_communautaire_score: 35.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 24.0,
      composite_score: 30.15,
      risk_level: "modéré",
      primary_pattern: "stigmatisation_sociale_exclusion_communautaire",
      estimated_albinism_persecution_rights_index: 3.01,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "APR-008",
      name: "Afrique du Sud — cadre juridique renforcé, accès aux soins amélioré",
      country: "Afrique du Sud",
      violence_physique_meurtres_rituels_trafic_score: 14.0,
      impunite_judiciaire_absence_poursuites_score: 10.0,
      stigmatisation_sociale_exclusion_communautaire_score: 12.0,
      acces_soins_protection_uv_soutien_psychosocial_score: 16.0,
      composite_score: 12.90,
      risk_level: "faible",
      primary_pattern: "acces_soins_protection_uv_soutien_psychosocial",
      estimated_albinism_persecution_rights_index: 1.29,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/albinism-persecution-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
