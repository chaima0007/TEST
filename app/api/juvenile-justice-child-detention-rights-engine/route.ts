import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[juvenile-justice-child-detention-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Juvenile Justice Child Detention Rights Engine Agent",
  domain: "juvenile_justice_child_detention_rights",
  total_entities: 8,
  avg_composite: 58.21,
  confidence_score: 0.87,
  avg_estimated_juvenile_justice_child_detention_rights_index: 5.82,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unicef_juvenile_justice_2023",
    "un_crc_detention_report_2022",
    "defence_for_children_2023",
    "iachr_juvenile_justice_2022",
  ],
  critical_alerts: [
    "Philippines: detention_massive_enfants_guerre_drogue",
    "USA: detention_enfants_migrants_centres_privatises",
    "Pakistan: enfants_detenus_adultes_torture",
    "Kenya: detention_preventive_prolongee_mineurs",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  entities: [
    {
      id: "JJD-001",
      name: "Philippines — détention massive d'enfants, guerre anti-drogue et centres surpeuplés",
      country: "Philippines",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 90.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 88.0,
      conditions_detention_violence_abus_education_sante_score: 86.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 82.0,
      composite_score: 86.90,
      risk_level: "critique",
      primary_pattern: "detention_enfants_preventive_longue_duree_mixte_adultes",
      estimated_juvenile_justice_child_detention_rights_index: 8.69,
      last_updated: "2026-06-21",
    },
    {
      id: "JJD-002",
      name: "États-Unis — détention d'enfants migrants, centres privatisés, isolement cellulaire",
      country: "États-Unis",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 84.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 80.0,
      conditions_detention_violence_abus_education_sante_score: 82.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 78.0,
      composite_score: 81.30,
      risk_level: "critique",
      primary_pattern: "conditions_detention_violence_abus_education_sante",
      estimated_juvenile_justice_child_detention_rights_index: 8.13,
      last_updated: "2026-06-21",
    },
    {
      id: "JJD-003",
      name: "Pakistan — enfants détenus avec adultes, torture documentée, système féodal informel",
      country: "Pakistan",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 82.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 85.0,
      conditions_detention_violence_abus_education_sante_score: 80.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 76.0,
      composite_score: 81.05,
      risk_level: "critique",
      primary_pattern: "manque_alternatives_detention_absence_tribunaux_specialises",
      estimated_juvenile_justice_child_detention_rights_index: 8.11,
      last_updated: "2026-06-21",
    },
    {
      id: "JJD-004",
      name: "Kenya — détention préventive prolongée de mineurs, manque de tribunaux pour enfants",
      country: "Kenya",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 76.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 78.0,
      conditions_detention_violence_abus_education_sante_score: 74.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 70.0,
      composite_score: 74.80,
      risk_level: "critique",
      primary_pattern: "manque_alternatives_detention_absence_tribunaux_specialises",
      estimated_juvenile_justice_child_detention_rights_index: 7.48,
      last_updated: "2026-06-21",
    },
    {
      id: "JJD-005",
      name: "Brésil (FEBEM/CASE) — violences institutionnelles dans centres socio-éducatifs",
      country: "Brésil",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 55.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 52.0,
      conditions_detention_violence_abus_education_sante_score: 58.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 48.0,
      composite_score: 53.60,
      risk_level: "élevé",
      primary_pattern: "conditions_detention_violence_abus_education_sante",
      estimated_juvenile_justice_child_detention_rights_index: 5.36,
      last_updated: "2026-06-21",
    },
    {
      id: "JJD-006",
      name: "Inde — détention arbitraire de mineurs tribaux et Dalits, accès défenseur rare",
      country: "Inde",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 52.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 50.0,
      conditions_detention_violence_abus_education_sante_score: 54.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 46.0,
      composite_score: 50.80,
      risk_level: "élevé",
      primary_pattern: "conditions_detention_violence_abus_education_sante",
      estimated_juvenile_justice_child_detention_rights_index: 5.08,
      last_updated: "2026-06-21",
    },
    {
      id: "JJD-007",
      name: "France — quartiers mineurs surpeuplés, durées de détention provisoire en hausse",
      country: "France",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 30.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 28.0,
      conditions_detention_violence_abus_education_sante_score: 26.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 24.0,
      composite_score: 27.30,
      risk_level: "modéré",
      primary_pattern: "detention_enfants_preventive_longue_duree_mixte_adultes",
      estimated_juvenile_justice_child_detention_rights_index: 2.73,
      last_updated: "2026-06-21",
    },
    {
      id: "JJD-008",
      name: "Norvège — justice restaurative, alternatives systématiques, recours indépendants",
      country: "Norvège",
      detention_enfants_preventive_longue_duree_mixte_adultes_score: 10.0,
      manque_alternatives_detention_absence_tribunaux_specialises_score: 8.0,
      conditions_detention_violence_abus_education_sante_score: 10.0,
      acces_representation_juridique_recours_effectifs_mineurs_score: 12.0,
      composite_score: 9.90,
      risk_level: "faible",
      primary_pattern: "acces_representation_juridique_recours_effectifs_mineurs",
      estimated_juvenile_justice_child_detention_rights_index: 0.99,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/juvenile-justice-child-detention-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
