import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[human-trafficking-modern-slavery-engine] SWARM_API_URL is not set — falling back to mock data");
}

function getMockData() {
  return {
    engine: "human-trafficking-modern-slavery-engine",
    generated_at: new Date().toISOString(),
    data_sources: [
      "unodc_global_report_trafficking_2022",
      "walk_free_global_slavery_index_2023",
      "us_state_dept_tip_report_2023",
      "ilo_forced_labour_statistics_2022",
    ],
    confidence_score: 0.89,
    avg_composite: 61.04,
    entities: [
      {
        entity_id: "HTMS-001",
        name: "Corée du Nord/Travail Forcé Exporté 100 000",
        country: "Asie du Nord-Est",
        sector: "100 000 Travailleurs Exportés Qatar/Russie/Chine, Salaires Confisqués État, Camp Kwalliso Travail Forcé & Rapport ONU 2014 Crimes Contre Humanité",
        trafficking_victim_scale_vulnerability_score: 96,
        labor_exploitation_debt_bondage_severity_score: 98,
        sex_trafficking_prosecution_impunity_score: 88,
        victim_identification_support_deficit_score: 99,
        composite_score: 95.10,
        risk_level: "critique",
        primary_pattern: "exploitation_travail_servitude_dette",
        key_signals: [
          "100 000 travailleurs exportés salaires confisqués",
          "Camp Kwalliso travail forcé",
          "ONU 2014 crimes contre humanité",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 9.51,
      },
      {
        entity_id: "HTMS-002",
        name: "Qatar/Kafala 1.8M Travailleurs Migrants",
        country: "MENA",
        sector: "Système Kafala Confiscation Passeports, 1.8M Travailleurs Migrants, Décès Chantiers Mondial 2022 & Walk Free Index Score Élevé",
        trafficking_victim_scale_vulnerability_score: 85,
        labor_exploitation_debt_bondage_severity_score: 92,
        sex_trafficking_prosecution_impunity_score: 78,
        victim_identification_support_deficit_score: 88,
        composite_score: 85.60,
        risk_level: "critique",
        primary_pattern: "exploitation_travail_servitude_dette",
        key_signals: [
          "Kafala confiscation passeports 1.8M migrants",
          "Décès chantiers Mondial 2022",
          "Walk Free Index score élevé",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 8.56,
      },
      {
        entity_id: "HTMS-003",
        name: "Inde/Esclavage Moderne 8M Walk Free Index",
        country: "Asie du Sud",
        sector: "8 Millions Esclaves Modernes Walk Free 2023, Servitude Castes, Travail Enfants Bonded Labor & Secteur Agricole Exploitation",
        trafficking_victim_scale_vulnerability_score: 88,
        labor_exploitation_debt_bondage_severity_score: 90,
        sex_trafficking_prosecution_impunity_score: 82,
        victim_identification_support_deficit_score: 78,
        composite_score: 85.00,
        risk_level: "critique",
        primary_pattern: "exploitation_travail_servitude_dette",
        key_signals: [
          "8 millions esclaves modernes Walk Free 2023",
          "Servitude castes bonded labor",
          "Secteur agricole exploitation enfants",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 8.50,
      },
      {
        entity_id: "HTMS-004",
        name: "Myanmar/Trafic Centres Arnaque Cyber Scam",
        country: "Asie du Sud-Est",
        sector: "100 000+ Trafiqués Centres Scam Frontières Thaïlande, 80 000 Réseaux Karen National Army, Electrocution & Crimes Cyber Forcés",
        trafficking_victim_scale_vulnerability_score: 90,
        labor_exploitation_debt_bondage_severity_score: 88,
        sex_trafficking_prosecution_impunity_score: 85,
        victim_identification_support_deficit_score: 92,
        composite_score: 88.65,
        risk_level: "critique",
        primary_pattern: "deficit_identification_soutien_victimes",
        key_signals: [
          "100 000+ trafiqués centres scam frontière Thaïlande",
          "80 000 réseaux Karen National Army",
          "Electrocution crimes cyber forcés",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 8.87,
      },
      {
        entity_id: "HTMS-005",
        name: "Russie/Trafic Femmes Europe Est Post-URSS",
        country: "Europe de l'Est",
        sector: "Principal Pays Origine Trafic Sexuel Europe, 2ème Mondiale Après Mexique, Réseaux Organisés & Faible Taux Condamnation",
        trafficking_victim_scale_vulnerability_score: 50,
        labor_exploitation_debt_bondage_severity_score: 48,
        sex_trafficking_prosecution_impunity_score: 58,
        victim_identification_support_deficit_score: 52,
        composite_score: 51.90,
        risk_level: "élevé",
        primary_pattern: "trafic_sexuel_impunite_poursuite",
        key_signals: [
          "Principal pays origine trafic sexuel Europe",
          "2ème mondiale trafic après Mexique",
          "Faible taux condamnation réseaux organisés",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 5.19,
      },
      {
        entity_id: "HTMS-006",
        name: "Mexique/Trafic Fentanyl Cartels Exploitation",
        country: "Amérique Centrale",
        sector: "Cartels Sinaloa & CJNG Diversification Trafic Humain, Femmes Migrantes Frontière, Exploitation Sexuelle & Travail Forcé Cannabis",
        trafficking_victim_scale_vulnerability_score: 55,
        labor_exploitation_debt_bondage_severity_score: 50,
        sex_trafficking_prosecution_impunity_score: 52,
        victim_identification_support_deficit_score: 48,
        composite_score: 51.60,
        risk_level: "élevé",
        primary_pattern: "trafic_victimes_echelle_massive",
        key_signals: [
          "Cartels Sinaloa CJNG diversification trafic",
          "Femmes migrantes exploitation frontière",
          "Travail forcé cannabis exploitation sexuelle",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 5.16,
      },
      {
        entity_id: "HTMS-007",
        name: "ONU/Protocole Palerme & UNODC Monitoring",
        country: "Global",
        sector: "Protocole Palerme 2000 Ratifié 180+ États, UNODC Rapport Mondial 2022, 49 000 Victimes Identifiées & 90 000 $ Profit/Victime/An",
        trafficking_victim_scale_vulnerability_score: 22,
        labor_exploitation_debt_bondage_severity_score: 20,
        sex_trafficking_prosecution_impunity_score: 25,
        victim_identification_support_deficit_score: 28,
        composite_score: 23.45,
        risk_level: "modéré",
        primary_pattern: "deficit_identification_soutien_victimes",
        key_signals: [
          "Protocole Palerme 2000 ratifié 180+ États",
          "UNODC 49 000 victimes identifiées 2022",
          "90 000 $ profit par victime par an",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 2.35,
      },
      {
        entity_id: "HTMS-008",
        name: "UE/Directive Anti-Traite 2011 & Mécanisme NRM",
        country: "Europe",
        sector: "Directive 2011/36/EU Anti-Traite, NRM National Referral Mechanism, GRETA Monitoring & Plan Action 2021-2025 Prévention",
        trafficking_victim_scale_vulnerability_score: 5,
        labor_exploitation_debt_bondage_severity_score: 6,
        sex_trafficking_prosecution_impunity_score: 8,
        victim_identification_support_deficit_score: 10,
        composite_score: 7.00,
        risk_level: "faible",
        primary_pattern: "deficit_identification_soutien_victimes",
        key_signals: [
          "Directive 2011/36/EU anti-traite NRM",
          "GRETA monitoring plan action 2021-2025",
          "Mécanisme référencement victimes EU",
        ],
        last_updated: "2024-01-15",
        estimated_human_trafficking_modern_slavery_index: 0.70,
      },
    ],
  };
}

const MOCK = getMockData();

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-trafficking-modern-slavery-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
