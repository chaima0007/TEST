import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-food-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Right to Food Engine Agent",
  domain: "right_to_food",
  total_entities: 8,
  avg_composite: 58.24,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { hunger_malnutrition: 2, corporate_land_grab: 1, legal_framework_absence: 2, food_access_affordability: 3 },
  top_risk_entities: [
    "Yémen/Gaza — Famine Arme de Guerre, Blocus & 2,2M Enfants Malnutris",
    "Éthiopie/Soudan/Sahel — Crise Alimentaire, Conflits & 40M En Urgence",
    "Inde — 194M Sous-Alimentés, Loi Droit Alimentaire & Malnutrition Enfants",
  ],
  critical_alerts: [
    "Yémen/Gaza: hunger_malnutrition",
    "Éthiopie/Soudan/Sahel: hunger_malnutrition",
    "Afrique/Asie: corporate_land_grab",
    "Inde: legal_framework_absence",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_right_to_food_index: 5.82,
  data_sources: [
    "fao_state_of_food_security_nutrition_world_annual_report",
    "global_hunger_index_welthungerhilfe_annual_report",
    "un_special_rapporteur_right_to_food_country_reports",
  ],
  entities: [
    {
      id: "RF-001",
      name: "Yémen/Gaza — Famine Arme de Guerre, Blocus & 2,2M Enfants Malnutris",
      country: "MENA",
      sector: "Yémen 17M Insécurité Alimentaire Sévère Blocus Coalition, Gaza Famine Artificielle 1M+ Hamas/Blocus Israël 2024, 2,2M Enfants Malnutris Yémen & FAO Stade 5 IPC Catastrophe Alimentaire",
      composite_score: 92.65,
      hunger_malnutrition_score: 98.0,
      food_access_affordability_score: 95.0,
      legal_framework_absence_score: 90.0,
      corporate_land_grab_score: 85.0,
      risk_level: "critique",
      primary_pattern: "hunger_malnutrition",
      estimated_right_to_food_index: 9.27,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation du droit à l'alimentation documentée — Yémen/Gaza avec score composite 92.65/100 révélant l'utilisation délibérée de la famine comme arme de guerre au Yémen (blocus) et à Gaza (restrictions d'aide alimentaire), avec 2,2M enfants malnutris au Yémen classés en IPC Phase 5 Catastrophe, violant l'Article 11 PIDESC et le droit international humanitaire",
        "Faim/Malnutrition (98.0/100) — l'utilisation de la famine comme arme de guerre par le blocus saoudien au Yémen et les restrictions d'aide humanitaire à Gaza constitue un crime de guerre selon l'Article 8(2)(b)(xxv) du Statut de Rome et viole l'obligation de permettre l'accès humanitaire du droit international humanitaire coutumier",
        "Activer d'urgence le mécanisme de la Cour Pénale Internationale pour la famine comme crime de guerre au Yémen et à Gaza et exiger la levée immédiate de tous les obstacles à l'aide alimentaire conformément aux résolutions du Conseil de sécurité ONU 2417 (2018) sur la famine dans les conflits armés",
      ],
    },
    {
      id: "RF-002",
      name: "Éthiopie/Soudan/Sahel — Crise Alimentaire, Conflits & 40M En Urgence",
      country: "Afrique Sub-Saharienne",
      sector: "Éthiopie Tigray 900 000 Famine Conflit 2022, Soudan 18M Insécurité Alimentaire Sévère 2024, Sahel 40M En Urgence Alimentaire & Changement Climatique Sécheresses Récurrentes",
      composite_score: 86.65,
      hunger_malnutrition_score: 90.0,
      food_access_affordability_score: 88.0,
      legal_framework_absence_score: 85.0,
      corporate_land_grab_score: 82.0,
      risk_level: "critique",
      primary_pattern: "hunger_malnutrition",
      estimated_right_to_food_index: 8.67,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation du droit à l'alimentation documentée — Éthiopie/Sahel avec score composite 86.65/100 révélant la famine de masse au Tigray (2021-2022) utilisée comme arme de guerre, 40M de personnes en urgence alimentaire dans le Sahel et les effets combinés des conflits et du changement climatique sur l'accès à l'alimentation",
        "Faim/Malnutrition (90.0/100) — les 900 000 Tigréens en situation de famine en 2022 résultant du blocus éthiopien/érythréen documenté par l'ONU, combiné aux 40M de personnes en insécurité alimentaire sévère dans le Sahel, révèlent une violation systémique du droit à l'alimentation (Article 11 PIDESC) dans la région",
        "Renforcer le Système d'alerte précoce famine (FEWS NET) avec une réponse humanitaire en moins de 72h pour les situations de niveau IPC 4-5 et adopter une résolution du Conseil de sécurité ONU contraignante sur la famine comme crime de guerre conformément à la résolution 2417 (2018)",
      ],
    },
    {
      id: "RF-003",
      name: "Afrique/Asie — Land Grab, 200M Ha Accaparés & Paysans Expulsés Sans Compensation",
      country: "Global Sud",
      sector: "Accaparement Terres 200M Ha Depuis 2008 Land Matrix, Foncier Africain 70% Transactions Étrangères, Paysans Expulsés Sans Compensation, Entreprises Chine/Golfe/USA & Semences OGM Dépendance",
      composite_score: 70.15,
      hunger_malnutrition_score: 58.0,
      food_access_affordability_score: 65.0,
      legal_framework_absence_score: 70.0,
      corporate_land_grab_score: 95.0,
      risk_level: "critique",
      primary_pattern: "corporate_land_grab",
      estimated_right_to_food_index: 7.02,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation du droit à l'alimentation documentée — Afrique/Asie avec score composite 70.15/100 révélant 200M d'hectares accaparés depuis 2008 selon la Land Matrix, avec des expulsions massives de paysans sans compensation adéquate constituant une violation du droit à l'alimentation (Article 11 PIDESC) et des Directives volontaires FAO sur la gouvernance foncière",
        "Accaparement terres/entreprises (95.0/100) — les transactions foncières à grande échelle par des États (Chine, pays du Golfe) et des entreprises multinationales en Afrique et en Asie, expulsant des millions de paysans de leurs terres ancestrales sans consultation ni compensation adéquate, violent les Directives volontaires FAO de 2012 sur la gouvernance foncière",
        "Adopter un instrument international contraignant sur les droits fonciers paysans intégrant les Directives FAO 2012 et renforcer les mécanismes de contrôle des investissements fonciers étrangers dans les pays en développement, conformément aux recommandations du Rapporteur Spécial ONU sur le droit à l'alimentation",
      ],
    },
    {
      id: "RF-004",
      name: "Inde — 194M Sous-Alimentés, Loi Droit Alimentaire & Malnutrition Enfants",
      country: "Asie du Sud",
      sector: "Inde 194M Sous-Alimentés GHI 2023 Rang 111/125, Malnutrition Infantile 35% Retard Croissance, National Food Security Act 2013 Partiellement Appliqué & Pertes Post-Récoltes 40% Céréales",
      composite_score: 78.85,
      hunger_malnutrition_score: 72.0,
      food_access_affordability_score: 75.0,
      legal_framework_absence_score: 90.0,
      corporate_land_grab_score: 80.0,
      risk_level: "critique",
      primary_pattern: "legal_framework_absence",
      estimated_right_to_food_index: 7.89,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation du droit à l'alimentation documentée — Inde avec score composite 78.85/100 révélant 194M de personnes sous-alimentées (2ème rang mondial), 35% d'enfants souffrant de retard de croissance et une application partielle du National Food Security Act 2013 malgré son existence formelle",
        "Absence cadre légal effectif (90.0/100) — bien que l'Inde ait adopté le National Food Security Act en 2013, sa mise en œuvre inégale entre États et les 40% de pertes post-récoltes révèlent un écart entre le cadre juridique formel et la réalisation effective du droit à l'alimentation garanti par l'Article 11 PIDESC ratifié par l'Inde en 1979",
        "Renforcer l'application du National Food Security Act en uniformisant les allocations alimentaires entre États et adopter une stratégie nationale de réduction des pertes post-récoltes, conformément aux recommandations du Rapporteur Spécial ONU sur le droit à l'alimentation après sa visite en Inde et aux ODD 2.1 et 2.2",
      ],
    },
    {
      id: "RF-005",
      name: "USA — 44M En Insécurité Alimentaire, SNAP Cuts & Deserts Alimentaires",
      country: "Amérique du Nord",
      sector: "USA 44M Insécurité Alimentaire USDA 2023, SNAP Coupures Budgétaires, Food Deserts 23M Personnes Accès Limité Nourriture Saine, Obésité Pauvreté Corrélation & Banques Alimentaires Saturées",
      composite_score: 52.35,
      hunger_malnutrition_score: 45.0,
      food_access_affordability_score: 50.0,
      legal_framework_absence_score: 60.0,
      corporate_land_grab_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "legal_framework_absence",
      estimated_right_to_food_index: 5.24,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation du droit à l'alimentation documentée — USA avec score composite 52.35/100 révélant 44M d'Américains en insécurité alimentaire, 23M dans des déserts alimentaires sans accès à une nourriture saine et l'absence d'une loi constitutionnelle reconnaissant le droit à l'alimentation, contrairement à la quasi-totalité des constitutions mondiales",
        "Absence cadre légal (60.0/100) — les États-Unis, qui n'ont pas ratifié le PIDESC, n'ont pas de droit constitutionnel à l'alimentation, laissant 44M de personnes sans garantie légale exécutoire d'accès à une alimentation adéquate, en contradiction avec l'Article 11 PIDESC et les engagements du Sommet mondial de l'alimentation de 1996",
        "Ratifier le PIDESC et adopter une loi fédérale reconnaissant le droit à l'alimentation comme droit exécutoire, et renforcer le programme SNAP avec un financement indexé sur l'inflation conformément aux recommandations du Rapporteur Spécial ONU sur le droit à l'alimentation après sa visite aux États-Unis en 2019",
      ],
    },
    {
      id: "RF-006",
      name: "Brésil/Amérique Latine — Agribusiness, Déforestation & Accès Alimentation",
      country: "Amérique Latine",
      sector: "Brésil Agribusiness Exportateur Soja/Bœuf Déforestation Amazonie, 33M Insécurité Alimentaire Bolsonaro 2022, Venezuela 25% Malnutrition & Haïti 5M IPC 4-5 Urgence Alimentaire",
      composite_score: 53.00,
      hunger_malnutrition_score: 45.0,
      food_access_affordability_score: 62.0,
      legal_framework_absence_score: 52.0,
      corporate_land_grab_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "food_access_affordability",
      estimated_right_to_food_index: 5.30,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation du droit à l'alimentation documentée — Brésil/Amérique Latine avec score composite 53.0/100 révélant 33M de Brésiliens en insécurité alimentaire en 2022 (période Bolsonaro), 5M d'Haïtiens en urgence alimentaire IPC 4-5 et la contradiction entre le Brésil premier exportateur agricole mondial et ses 33M d'affamés",
        "Accès/Abordabilité alimentaire (62.0/100) — la contradiction entre le Brésil, premier exportateur mondial de soja et de bœuf, et les 33M de Brésiliens qui n'avaient pas accès à une alimentation suffisante en 2022 révèle que la production agricole ne garantit pas le droit à l'alimentation sans politiques redistributives conformes à l'Article 11 PIDESC",
        "Renforcer le programme Bolsa Família brésilien et adopter une politique régionale d'accès à l'alimentation dans le cadre de l'Alliance sans Faim (Lula 2023) conforme aux Directives volontaires FAO sur le droit à l'alimentation (2004) et à l'Article 11 PIDESC sur le droit à un niveau de vie suffisant",
      ],
    },
    {
      id: "RF-007",
      name: "UE/PAC — Politique Agricole Commune, Farm to Fork & Accès Alimentation",
      country: "Europe",
      sector: "UE PAC 387B€ Subventions 2023-2027, Farm To Fork Stratégie Durabilité, 42M Européens Incapables Repas Protéiné/2 Jours & Inflation Alimentaire 2022-2023 Record 20%",
      composite_score: 27.60,
      hunger_malnutrition_score: 22.0,
      food_access_affordability_score: 32.0,
      legal_framework_absence_score: 28.0,
      corporate_land_grab_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "food_access_affordability",
      estimated_right_to_food_index: 2.76,
      last_updated: "2026-06-20",
      key_signals: [
        "Défis d'accès à l'alimentation en Europe — la PAC avec 387Md€ de subventions agricoles concentrées sur les grandes exploitations et 42M d'Européens incapables de s'offrir un repas protéiné tous les deux jours révèlent des lacunes dans la réalisation du droit à l'alimentation même dans les pays à haut revenu",
        "Accès/Abordabilité alimentaire (32.0/100) — l'inflation alimentaire record de 20% en 2022-2023 en Europe a poussé 42M de personnes dans l'incapacité de se nourrir adéquatement, révélant une vulnérabilité systémique des ménages pauvres au droit à l'alimentation malgré les richesses agricoles européennes",
        "Réformer la PAC pour conditionner les aides à des critères de durabilité sociale (accès alimentaire local) et adopter une directive européenne sur le droit à l'alimentation garantissant un minimum alimentaire pour tous les résidents de l'UE, conformément à la Charte des droits fondamentaux de l'UE (Article 34) et aux ODD 2",
      ],
    },
    {
      id: "RF-008",
      name: "ONU/PIDESC Art.11 — Droit Alimentation, Directives FAO & Rapporteur Spécial",
      country: "Global",
      sector: "PIDESC Article 11 Droit Alimentation Adéquate 171 Ratifications, Directives Volontaires FAO 2004, Rapporteur Spécial ONU Droit Alimentation & Déclaration ONU Droits Paysans UNDROP 2018",
      composite_score: 4.40,
      hunger_malnutrition_score: 4.0,
      food_access_affordability_score: 5.0,
      legal_framework_absence_score: 3.0,
      corporate_land_grab_score: 6.0,
      risk_level: "faible",
      primary_pattern: "food_access_affordability",
      estimated_right_to_food_index: 0.44,
      last_updated: "2026-06-20",
      key_signals: [
        "ONU/PIDESC Art.11 incarne le cadre normatif exemplaire du droit à l'alimentation — l'Article 11 PIDESC ratifié par 171 États reconnaissant le droit à une alimentation adéquate et les Directives volontaires FAO sur le droit à l'alimentation (2004) créant un cadre opérationnel pour les politiques alimentaires nationales",
        "Déclaration ONU sur les droits des paysans (UNDROP 2018) — premier instrument international dédié aux droits des paysans, travailleurs ruraux et petits agriculteurs, reconnaissant leur droit aux semences, à la terre et à l'alimentation, créant de nouvelles obligations étatiques de protection des systèmes alimentaires paysans",
        "Universaliser la ratification du PIDESC (25 États encore non-parties) et adopter un mécanisme de plainte individuel au titre de l'Article 11 PIDESC pour les violations du droit à l'alimentation, conformément au Protocole facultatif au PIDESC entré en vigueur en 2013 permettant les plaintes individuelles",
      ],
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-food-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
