import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[genocide-prevention-accountability-engine] SWARM_API_URL is not set — falling back to mock data");
}

function getMockData() {
  return {
    agent: "Genocide Prevention Accountability Engine Agent",
    domain: "genocide_prevention_accountability",
    total_entities: 8,
    avg_composite: 59.76,
    confidence_score: 0.89,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { risque_atrocites_masse_actif: 1, echec_prevention_internationale: 3, impunite_auteurs_crimes_masse: 4 },
    top_risk_entities: [
      "Myanmar/Génocide Rohingya 2017 — ICJ Procédures Actives, CPI Enquête Ouverte, 700K Réfugiés Bangladesh, Déshumanisation Systémique 'Kafirs' & Impunité Tatmadaw Totale",
      "Darfour/Soudan RSF 2023 — Atrocités Génocidaires Répétées, Villages Masla Brûlés, Rhétorique Ethnique Anti-Masalit & Conseil Sécurité Bloqué Russie Chine Veto",
      "Gaza/Rapporteurs Spéciaux ONU 2024 — Qualification Génocide Débattue ICJ Mesures Provisoires, Blocus Humanitaire, Discours Déshumanisation Officiels & Veto USA CS",
    ],
    critical_alerts: [
      "Myanmar/Génocide Rohingya 2017: risque_atrocites_masse_actif",
      "Darfour/Soudan RSF 2023: echec_prevention_internationale",
      "Gaza/Rapporteurs Spéciaux ONU 2024: echec_prevention_internationale",
      "Chine/Ouïghours: impunite_auteurs_crimes_masse",
    ],
    last_analysis: "2026-06-21",
    engine_version: "1.0.0",
    avg_estimated_genocide_prevention_accountability_index: 5.98,
    data_sources: [
      "genocide_watch_early_warning_indicators_2023",
      "un_office_genocide_prevention_report_2023",
      "international_criminal_court_annual_report_2023",
      "minority_rights_group_peoples_under_threat",
    ],
    entities: [
      { id: "GPA-001", name: "Myanmar/Génocide Rohingya 2017 — ICJ Procédures Actives, CPI Enquête Ouverte, 700K Réfugiés Bangladesh, Déshumanisation Systémique 'Kafirs' & Impunité Tatmadaw Totale", country: "Myanmar", sector: "Génocide Documenté Actif", mass_atrocity_risk_early_warning_score: 88.0, impunity_accountability_deficit_score: 92.0, incitement_hate_speech_dehumanization_score: 90.0, prevention_mechanism_international_response_gap_score: 85.0, composite_score: 88.9, risk_level: "critique", primary_pattern: "risque_atrocites_masse_actif", key_signals: ["Génocide documenté ICJ — la Cour Internationale de Justice a ordonné des mesures provisoires en 2020, reconnaissant le risque de génocide contre les Rohingya, violation de la Convention de 1948", "Impunité totale Tatmadaw — aucun général birman n'a été arrêté ou jugé, le coup d'État de 2021 a renforcé les auteurs du génocide au lieu de les affaiblir", "700.000 réfugiés sans solution — population Rohingya maintenue dans les camps de Cox's Bazar (Bangladesh) sans perspective de retour sécurisé ni réinstallation"], estimated_genocide_prevention_accountability_index: 8.89, last_updated: "2026-06-21" },
      { id: "GPA-002", name: "Darfour/Soudan RSF 2023 — Atrocités Génocidaires Répétées, Villages Masla Brûlés, Rhétorique Ethnique Anti-Masalit & Conseil Sécurité Bloqué Russie Chine Veto", country: "Soudan", sector: "Atrocités en Cours", mass_atrocity_risk_early_warning_score: 90.0, impunity_accountability_deficit_score: 85.0, incitement_hate_speech_dehumanization_score: 88.0, prevention_mechanism_international_response_gap_score: 82.0, composite_score: 86.65, risk_level: "critique", primary_pattern: "echec_prevention_internationale", key_signals: ["Répétition du Darfour — les RSF (héritiers des Janjaweed) commettent des atrocités à caractère ethnique contre les Masalit à partir de 2023, répétant les crimes de 2003-2005", "Rhétorique génocidaire documentée — discours déshumanisant les Masalit comme 'serviteurs' et 'esclaves', prélude historiquement associé aux génocides selon les indicateurs Genocide Watch", "Conseil Sécurité paralysé — double veto Russie-Chine bloque toute intervention internationale, laissant 8M déplacés sans protection effective"], estimated_genocide_prevention_accountability_index: 8.67, last_updated: "2026-06-21" },
      { id: "GPA-003", name: "Gaza/Rapporteurs Spéciaux ONU 2024 — Qualification Génocide Débattue ICJ Mesures Provisoires, Blocus Humanitaire, Discours Déshumanisation Officiels & Veto USA CS", country: "Palestine/Gaza", sector: "Débat Juridique Actif", mass_atrocity_risk_early_warning_score: 86.0, impunity_accountability_deficit_score: 80.0, incitement_hate_speech_dehumanization_score: 82.0, prevention_mechanism_international_response_gap_score: 88.0, composite_score: 83.9, risk_level: "critique", primary_pattern: "echec_prevention_internationale", key_signals: ["Mesures provisoires ICJ — la Cour Internationale de Justice a imposé des mesures provisoires en janvier 2024, reconnaissant un 'risque plausible' de génocide selon la Convention de 1948", "Discours officiels déshumanisants — déclarations de hauts responsables israéliens qualifiant les Gazaouis d'animaux documentées par le Bureau du HCDH comme incitations", "Veto américain au CS — 4 vetos américains bloquant des résolutions humanitaires, empêchant toute réponse collective internationale au titre du R2P"], estimated_genocide_prevention_accountability_index: 8.39, last_updated: "2026-06-21" },
      { id: "GPA-004", name: "Chine/Ouïghours — Convention Génocide Débat Juridique, 1M+ Détenus Xinjiang, Propagande Déshumanisation Islamophobie État & Aucun Mécanisme International Accès", country: "Chine", sector: "Crimes Contre l'Humanité Documentés", mass_atrocity_risk_early_warning_score: 82.0, impunity_accountability_deficit_score: 85.0, incitement_hate_speech_dehumanization_score: 88.0, prevention_mechanism_international_response_gap_score: 78.0, composite_score: 83.45, risk_level: "critique", primary_pattern: "impunite_auteurs_crimes_masse", key_signals: ["1M+ en détention arbitraire — camps d'internement documentés par satellite et témoignages, qualifiés de crimes contre l'humanité par le HCDH dans son rapport Xinjiang 2022", "Stérilisations forcées systémiques — taux de natalité Ouïghoure chutant de 84% entre 2015-2018 dans certaines régions, élément potentiel de génocide selon la Convention Art.2(d)", "Aucun accès indépendant — toutes les demandes d'enquête ONU refusées, rapporteurs spéciaux non autorisés à entrer dans le Xinjiang depuis 2005"], estimated_genocide_prevention_accountability_index: 8.35, last_updated: "2026-06-21" },
      { id: "GPA-005", name: "Bosnie/Srebrenica — Génocide Jugé TPIY, Impunité Partielle Dirigeants RS Toujours Actifs, Négationnisme État Srpska & Mémorialisation Contestée 30 Ans Après", country: "Bosnie-Herzégovine", sector: "Justice Post-Génocide Partielle", mass_atrocity_risk_early_warning_score: 45.0, impunity_accountability_deficit_score: 68.0, incitement_hate_speech_dehumanization_score: 55.0, prevention_mechanism_international_response_gap_score: 58.0, composite_score: 55.85, risk_level: "élevé", primary_pattern: "impunite_auteurs_crimes_masse", key_signals: ["Négationnisme institutionnel — le président de la Republika Srpska (Dodik) nie publiquement le génocide de Srebrenica, violant la loi bosniaque tout en bénéficiant de l'impunité politique", "Justice partielle — 47 condamnations TPIY mais des dizaines de responsables sont morts avant jugement ou ont bénéficié de remises de peine, laissant des victimes sans réparation", "Radicalisation résiduele — discours ethniques nationalistes en hausse dans la RS, réactivant les dynamiques identitaires qui ont précédé le génocide de 1995"], estimated_genocide_prevention_accountability_index: 5.58, last_updated: "2026-06-21" },
      { id: "GPA-006", name: "Rwanda/Post-Génocide 1994 — Justice Gacaca 1.9M Dossiers, Mémoire Nationale Institutionnalisée, Reconciliation Partielle & Risques Régionalisation Résiduel Est RDC", country: "Rwanda", sector: "Modèle Justice Transitionnelle", mass_atrocity_risk_early_warning_score: 25.0, impunity_accountability_deficit_score: 58.0, incitement_hate_speech_dehumanization_score: 50.0, prevention_mechanism_international_response_gap_score: 52.0, composite_score: 44.9, risk_level: "élevé", primary_pattern: "impunite_auteurs_crimes_masse", key_signals: ["Justice Gacaca innovante — 1.9M dossiers traités par les tribunaux communautaires entre 2002-2012, modèle unique de justice transitionnelle à grande échelle", "Risques de régionalisation — implication alléguée du Rwanda dans les groupes armés à l'Est de la RDC (CNDP, M23) complexifiant la réconciliation régionale", "Mémoire institutionnalisée mais autoritaire — commémoration obligatoire annuelle du génocide mais restriction des débats historiques alternatifs dans l'espace public"], estimated_genocide_prevention_accountability_index: 4.49, last_updated: "2026-06-21" },
      { id: "GPA-007", name: "Cambodge/ECCC — Procès Khmers Rouges Partiels, Accusés Vieillissants Décédés, Justice Limitée 3 Condamnations Définitives & Mémoire Institutionnelle Fragile Jeunes Générations", country: "Cambodge", sector: "Justice Tardive Incomplète", mass_atrocity_risk_early_warning_score: 15.0, impunity_accountability_deficit_score: 38.0, incitement_hate_speech_dehumanization_score: 28.0, prevention_mechanism_international_response_gap_score: 30.0, composite_score: 27.0, risk_level: "modéré", primary_pattern: "impunite_auteurs_crimes_masse", key_signals: ["Justice trop tardive — les ECCC (chambres extraordinaires) ont rendu 3 condamnations définitives pour un génocide qui a tué 1.7-2.5M personnes, coûtant 340M$ sur 15 ans", "Accusés décédés avant jugement — Pol Pot (1998), Ta Mok (2006), Ieng Thirith (2015) sont morts sans jamais être jugés, laissant 90% des responsables impunis", "Mémoire fragile jeunesse — 60% de la population cambodgienne née après 1979, avec éducation sur le génocide insuffisante et risque d'amnésie générationnelle"], estimated_genocide_prevention_accountability_index: 2.7, last_updated: "2026-06-21" },
      { id: "GPA-008", name: "CPI/Cour Pénale Internationale — Modèle Responsabilité Structurellement Limité, 3 États Non-Membres Permanents CS, 44 Situations Enquêtées & Seuls Africains Condamnés Biais Perçu", country: "International", sector: "Justice Internationale", mass_atrocity_risk_early_warning_score: 5.0, impunity_accountability_deficit_score: 8.0, incitement_hate_speech_dehumanization_score: 6.0, prevention_mechanism_international_response_gap_score: 12.0, composite_score: 7.4, risk_level: "faible", primary_pattern: "echec_prevention_internationale", key_signals: ["Architecture de responsabilité fonctionnelle — 44 situations enquêtées depuis 2002, mandats d'arrêt contre Poutine (2023) et Netanyahou (2024) démontrant l'extension de la portée de la Cour", "Limites structurelles — USA, Chine et Russie non-membres et 3 États permanents du CS peuvent bloquer les renvois, créant une justice à deux vitesses", "Biais africain en cours de correction — 8/10 premières condamnations concernaient l'Afrique, mais les situations Ukraine, Myanmar et Gaza marquent une extension géographique réelle"], estimated_genocide_prevention_accountability_index: 0.74, last_updated: "2026-06-21" },
    ],
  };
}

const MOCK = getMockData();

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/genocide-prevention-accountability-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
