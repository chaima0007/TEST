import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[private-military-contractors-accountability-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "private_military_contractors_accountability_engine",
  domain: "private_military_contractors_accountability",
  total_entities: 8,
  avg_composite: 60.63,
  confidence_score: 0.90,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    documented_civilian_harm: 4,
    legal_immunity_impunity: 2,
    oversight_failure: 1,
    voluntary_framework: 1,
  },
  top_risk_entities: [
    { id: "PMC-001", name: "Wagner Group/Russie — Afrique Crimes Documentés ONU, Mali Moura 500 Civils, Impunité Totale", score: 95.6, risk: "critique" },
    { id: "PMC-002", name: "Blackwater/Nisour Square Irak — 17 Civils Tués 2007, Condamnations Annulées, Grâces Trump", score: 90.3, risk: "critique" },
    { id: "PMC-003", name: "DynCorp/Balkans — Trafic Humain Accusations Bosnia Kosovo, Non Poursuivies, Contrats Maintenus", score: 84.65, risk: "critique" },
  ],
  critical_alerts: [
    "PMC-001: Wagner Group/Russie — Afrique Crimes Documentés ONU, Mali Moura 500 Civils, Impunité Totale — composite 95.6",
    "PMC-002: Blackwater/Nisour Square Irak — 17 Civils Tués 2007, Condamnations Annulées, Grâces Trump — composite 90.3",
    "PMC-003: DynCorp/Balkans — Trafic Humain Accusations Bosnia Kosovo, Non Poursuivies, Contrats Maintenus — composite 84.65",
    "PMC-004: Aegis/Irak — Vidéos Tirs Civils Non Sanctionnés, Enquête PMSC Inexistante, Contrats Reconduits — composite 78.9",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_pmc_accountability_index: 6.06,
  data_sources: [
    "un_working_group_mercenaries_report_2023",
    "montreux_document_forum_icoca_report_2024",
    "human_rights_watch_private_military_contractors_2023",
    "amnesty_international_pmc_accountability_report_2024",
  ],
  entities: [
    {
      entity_id: "PMC-001",
      name: "Wagner Group/Russie — Afrique Crimes Documentés ONU, Mali Moura 500 Civils, Impunité Totale",
      country: "Russie/Mali/Centrafrique",
      documented_abuses_civilian_harm_score: 96.0,
      legal_immunity_impunity_gap_score: 97.0,
      oversight_transparency_failure_score: 95.0,
      international_regulatory_framework_gap_score: 94.0,
      composite_score: 95.6,
      risk_level: "critique",
      primary_pattern: "Wagner Moura massacre 500 civils Mali 2022, crimes contre humanité RCA, ONU rapport 2023, aucune poursuite Russie",
      estimated_pmc_accountability_index: 9.56,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PMC-002",
      name: "Blackwater/Nisour Square Irak — 17 Civils Tués 2007, Condamnations Annulées, Grâces Trump",
      country: "États-Unis/Irak",
      documented_abuses_civilian_harm_score: 91.0,
      legal_immunity_impunity_gap_score: 93.0,
      oversight_transparency_failure_score: 87.0,
      international_regulatory_framework_gap_score: 90.0,
      composite_score: 90.3,
      risk_level: "critique",
      primary_pattern: "Massacre Nisour Square 17 civils irakiens 2007, Ordre 17 CPA immunité, condamnés 2015 annulés, grâciés Trump 2020",
      estimated_pmc_accountability_index: 9.03,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PMC-003",
      name: "DynCorp/Balkans — Trafic Humain Accusations Bosnia Kosovo, Non Poursuivies, Contrats Maintenus",
      country: "États-Unis/Balkans",
      documented_abuses_civilian_harm_score: 82.0,
      legal_immunity_impunity_gap_score: 88.0,
      oversight_transparency_failure_score: 85.0,
      international_regulatory_framework_gap_score: 84.0,
      composite_score: 84.65,
      risk_level: "critique",
      primary_pattern: "Allégations trafic humain Bosnia 1999-2002, agent FBI dénonciation, DynCorp maintenu contrat USG, aucune poursuite pénale",
      estimated_pmc_accountability_index: 8.46,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PMC-004",
      name: "Aegis/Irak — Vidéos Tirs Civils Non Sanctionnés, Enquête PMSC Inexistante, Contrats Reconduits",
      country: "UK/Irak",
      documented_abuses_civilian_harm_score: 76.0,
      legal_immunity_impunity_gap_score: 80.0,
      oversight_transparency_failure_score: 82.0,
      international_regulatory_framework_gap_score: 78.0,
      composite_score: 78.9,
      risk_level: "critique",
      primary_pattern: "Vidéos 2005 tirs civils irakiens véhicules, enquête US Army classée, contrats Aegis reconduits 475M$, zéro sanction",
      estimated_pmc_accountability_index: 7.89,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PMC-005",
      name: "G4S/Prisons UK — Maltraitance Détenues Rapport 2017, Amendes Sans Poursuites Pénales",
      country: "Royaume-Uni",
      documented_abuses_civilian_harm_score: 54.0,
      legal_immunity_impunity_gap_score: 58.0,
      oversight_transparency_failure_score: 52.0,
      international_regulatory_framework_gap_score: 48.0,
      composite_score: 53.3,
      risk_level: "élevé",
      primary_pattern: "Maltraitance détenues Yarl's Wood, rapport 2017 violence, amendes contractuelles uniquement, aucune poursuite pénale dirigeants",
      estimated_pmc_accountability_index: 5.33,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PMC-006",
      name: "MPRI/Balkans — Entraînement Armées, Responsabilité Floue, Opérations Tempête Croatie 1995",
      country: "États-Unis/Balkans",
      documented_abuses_civilian_harm_score: 46.0,
      legal_immunity_impunity_gap_score: 52.0,
      oversight_transparency_failure_score: 50.0,
      international_regulatory_framework_gap_score: 48.0,
      composite_score: 48.9,
      risk_level: "élevé",
      primary_pattern: "MPRI entraînement armée croate, Opération Tempête 250K déplacés serbes, responsabilité PMSC jamais établie",
      estimated_pmc_accountability_index: 4.89,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PMC-007",
      name: "Montreux Document/Suisse — Cadre Volontaire PMC, 57 États Adhérents, Normes Non Contraignantes",
      country: "International",
      documented_abuses_civilian_harm_score: 22.0,
      legal_immunity_impunity_gap_score: 25.0,
      oversight_transparency_failure_score: 28.0,
      international_regulatory_framework_gap_score: 30.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "Document Montreux 2008 cadre volontaire, 57 États adhérents, bonnes pratiques sans mécanisme sanction, progrès limité",
      estimated_pmc_accountability_index: 2.58,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "PMC-008",
      name: "ICoC/Code Conduite Contractants Privés — Mécanisme Plaintes 2013, Portée Limitée, Modèle",
      country: "International",
      documented_abuses_civilian_harm_score: 6.0,
      legal_immunity_impunity_gap_score: 8.0,
      oversight_transparency_failure_score: 7.0,
      international_regulatory_framework_gap_score: 10.0,
      composite_score: 7.55,
      risk_level: "faible",
      primary_pattern: "ICoCA code conduite 100+ entreprises, mécanisme plaintes actif, audits tiers, meilleur standard sectoriel mais limites claires",
      estimated_pmc_accountability_index: 0.76,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/private-military-contractors-accountability-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
