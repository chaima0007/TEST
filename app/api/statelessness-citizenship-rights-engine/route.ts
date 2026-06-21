import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[statelessness-citizenship-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

function getMockData() {
  return {
    engine: "statelessness-citizenship-rights-engine",
    generated_at: new Date().toISOString(),
    data_sources: [
      "unhcr_statelessness_report_2023",
      "institute_statelessness_inclusion",
      "human_rights_watch_citizenship_rights",
      "international_law_commission_nationality",
    ],
    confidence_score: 0.88,
    avg_composite: 59.67,
    entities: [
      {
        id: "SCR-001",
        name: "Myanmar/Rohingyas 600 000 Apatrides",
        country: "Asie du Sud-Est",
        sector: "Loi Citoyenneté 1982 Exclut Rohingyas, 600 000 Sans Nationalité Au Myanmar, 1M+ Réfugiés Bangladesh & Génocide ONU 2018",
        stateless_population_scale_severity_score: 98,
        citizenship_deprivation_arbitrariness_score: 97,
        documentation_access_birth_registration_deficit_score: 95,
        stateless_rights_protection_mechanism_gap_score: 92,
        composite_score: 95.80,
        risk_level: "critique",
        primary_pattern: "apatridie_population_masse",
        key_signals: [
          "Loi 1982 exclut Rohingyas de la nationalité",
          "600 000 apatrides au Myanmar",
          "1M+ réfugiés Bangladesh génocide ONU 2018",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 9.58,
      },
      {
        id: "SCR-002",
        name: "Koweït/Bidun 100 000 Sans Nationalité",
        country: "MENA",
        sector: "100 000 Bidun Sans Citoyenneté Depuis Indépendance 1961, Résidents Depuis Génération, Sans Emploi Public, Éducation & Soins",
        stateless_population_scale_severity_score: 88,
        citizenship_deprivation_arbitrariness_score: 90,
        documentation_access_birth_registration_deficit_score: 85,
        stateless_rights_protection_mechanism_gap_score: 88,
        composite_score: 87.75,
        risk_level: "critique",
        primary_pattern: "privation_citoyennete_arbitraire",
        key_signals: [
          "100 000 Bidun sans citoyenneté depuis 1961",
          "Exclusion emploi public éducation soins",
          "Résidents depuis génération sans droits",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 8.78,
      },
      {
        id: "SCR-003",
        name: "République Dominicaine/Haïtiens Déchus 2013",
        country: "Caraïbes",
        sector: "Décision TC 168-13 Rétroactive Depuis 1929, 200 000 Haïtiens-Dominicains Déchus Nationalité, Génération Née Sur Place",
        stateless_population_scale_severity_score: 85,
        citizenship_deprivation_arbitrariness_score: 92,
        documentation_access_birth_registration_deficit_score: 80,
        stateless_rights_protection_mechanism_gap_score: 82,
        composite_score: 84.90,
        risk_level: "critique",
        primary_pattern: "privation_citoyennete_arbitraire",
        key_signals: [
          "Décision TC 168-13 rétroactive depuis 1929",
          "200 000 Haïtiens-Dominicains déchus nationalité",
          "Génération née sur place apatride",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 8.49,
      },
      {
        id: "SCR-004",
        name: "Thaïlande/Peuples Montagnards Highlanders",
        country: "Asie du Sud-Est",
        sector: "480 000 Peuples Autochtones Montagnards Sans Nationalité, Akha/Hmong/Karen, Sans Droit Vote, Travel & Services Publics",
        stateless_population_scale_severity_score: 82,
        citizenship_deprivation_arbitrariness_score: 78,
        documentation_access_birth_registration_deficit_score: 88,
        stateless_rights_protection_mechanism_gap_score: 80,
        composite_score: 82.10,
        risk_level: "critique",
        primary_pattern: "deficit_enregistrement_naissance",
        key_signals: [
          "480 000 peuples autochtones sans nationalité",
          "Akha Hmong Karen sans droit de vote",
          "Absence accès services publics",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 8.21,
      },
      {
        id: "SCR-005",
        name: "Lettonie/Estonies Non-Citoyens Russophones",
        country: "Europe du Nord",
        sector: "220 000 Passeports Non-Citoyens Lettonie, 70 000 Estonie, Russophones Post-URSS, Droits Politiques Limités & Naturalisation Difficile",
        stateless_population_scale_severity_score: 52,
        citizenship_deprivation_arbitrariness_score: 48,
        documentation_access_birth_registration_deficit_score: 35,
        stateless_rights_protection_mechanism_gap_score: 55,
        composite_score: 47.35,
        risk_level: "élevé",
        primary_pattern: "absence_mecanisme_protection_apatrides",
        key_signals: [
          "220 000 non-citoyens Lettonie passeports spéciaux",
          "70 000 non-citoyens Estonie post-URSS",
          "Naturalisation difficile droits politiques limités",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 4.74,
      },
      {
        id: "SCR-006",
        name: "Côte d'Ivoire/Populations Sans Actes Naissance",
        country: "Afrique de l'Ouest",
        sector: "750 000 Personnes Sans Actes Naissance, 25% Enfants Non Enregistrés, Conflit Post-Électoral 2010-2011 Aggravation",
        stateless_population_scale_severity_score: 52,
        citizenship_deprivation_arbitrariness_score: 45,
        documentation_access_birth_registration_deficit_score: 65,
        stateless_rights_protection_mechanism_gap_score: 52,
        composite_score: 53.50,
        risk_level: "élevé",
        primary_pattern: "deficit_enregistrement_naissance",
        key_signals: [
          "750 000 personnes sans actes naissance",
          "25% enfants non enregistrés",
          "Conflit 2010-2011 aggravation documentation",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 5.35,
      },
      {
        id: "SCR-007",
        name: "UNHCR/Plan #IBelong 2024 Éradication Apatridie",
        country: "Global",
        sector: "Plan 10 Ans Fin Apatridie 2014-2024, 10M Apatrides Documentés, Conventions 1954 & 1961 & 92 États Parties",
        stateless_population_scale_severity_score: 20,
        citizenship_deprivation_arbitrariness_score: 18,
        documentation_access_birth_registration_deficit_score: 22,
        stateless_rights_protection_mechanism_gap_score: 28,
        composite_score: 21.60,
        risk_level: "modéré",
        primary_pattern: "absence_mecanisme_protection_apatrides",
        key_signals: [
          "Plan #IBelong 10 ans éradication apatridie",
          "10M apatrides documentés mondialement",
          "Conventions 1954 1961 92 États parties",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 2.16,
      },
      {
        id: "SCR-008",
        name: "UE/Droit Citoyenneté & Naturalisation Modèle",
        country: "Europe",
        sector: "Directive Longue Durée Résidents, Naturalisation 5-10 Ans, Double Nationalité & CJUE Protection Perte Citoyenneté EU",
        stateless_population_scale_severity_score: 4,
        citizenship_deprivation_arbitrariness_score: 5,
        documentation_access_birth_registration_deficit_score: 3,
        stateless_rights_protection_mechanism_gap_score: 6,
        composite_score: 4.40,
        risk_level: "faible",
        primary_pattern: "absence_mecanisme_protection_apatrides",
        key_signals: [
          "Directive longue durée résidents naturalisation",
          "Double nationalité CJUE protection",
          "Modèle protection citoyenneté EU",
        ],
        last_updated: "2024-01-15",
        estimated_statelessness_citizenship_rights_index: 0.44,
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
    const res = await fetch(`${process.env.SWARM_API_URL}/statelessness-citizenship-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
