import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sportwashing-geopolitics-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Sportwashing Geopolitics Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sportwashing-geopolitics-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Sportwashing Geopolitics Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Sportwashing Geopolitics Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "SG-001", name: "Qatar — Coupe du Monde 2022 & PSG Soft Power", country: "MENA", sector: "220Md$ CDM 2022, 6500 Morts Migrants & PSG comme Instrument d'Influence", composite_score: 91.4, sportwashing_investment_score: 95.0, sports_rights_acquisition_score: 90.0, soft_power_narrative_score: 88.0, human_rights_whitewash_score: 92.0, risk_level: "critique", primary_pattern: "sportwashing_systematique", key_signals: ["Sportwashing systémique de Qatar — investissements massifs dans le sport mondial pour blanchir l'image du régime", "Achats de légitimité sportive — clubs, droits de diffusion et événements utilisés pour contourner les critiques diplomatiques", "Silence sportif sur les droits humains — athlètes et institutions achetés ou intimidés pour éviter toute condamnation publique"], estimated_sport_geopolitics_index: 9.14, last_updated: "2026-06-20" },
    { id: "SG-002", name: "Arabie Saoudite — LIV Golf, Newcastle & PIF Sport", country: "MENA", sector: "LIV Golf, Newcastle United, F1 ARAMCO & Ronaldo 75M€/an malgré 196 Exécutions", composite_score: 90.6, sportwashing_investment_score: 92.0, sports_rights_acquisition_score: 95.0, soft_power_narrative_score: 85.0, human_rights_whitewash_score: 90.0, risk_level: "critique", primary_pattern: "sportwashing_systematique", key_signals: ["Sportwashing systémique de Arabie Saoudite — investissements massifs dans le sport mondial pour blanchir l'image du régime", "Achats de légitimité sportive — clubs, droits de diffusion et événements utilisés pour contourner les critiques diplomatiques", "Silence sportif sur les droits humains — athlètes et institutions achetés ou intimidés pour éviter toute condamnation publique"], estimated_sport_geopolitics_index: 9.06, last_updated: "2026-06-20" },
    { id: "SG-003", name: "Émirats Arabes — Manchester City & City Football Group", country: "MENA", sector: "ADCB Manchester City, 12 Clubs Mondiaux & Formule 1 Abu Dhabi GP", composite_score: 86.9, sportwashing_investment_score: 88.0, sports_rights_acquisition_score: 92.0, soft_power_narrative_score: 82.0, human_rights_whitewash_score: 85.0, risk_level: "critique", primary_pattern: "sportwashing_systematique", key_signals: ["Sportwashing systémique de Émirats Arabes — investissements massifs dans le sport mondial pour blanchir l'image du régime", "Achats de légitimité sportive — clubs, droits de diffusion et événements utilisés pour contourner les critiques diplomatiques", "Silence sportif sur les droits humains — athlètes et institutions achetés ou intimidés pour éviter toute condamnation publique"], estimated_sport_geopolitics_index: 8.69, last_updated: "2026-06-20" },
    { id: "SG-004", name: "Chine — JO Pékin 2008/2022 & Soft Power Global", country: "Asie", sector: "2 JO pour Légitimer PCC, Achats Clubs Européens & Droits Diffusion Mondiaux", composite_score: 81.35, sportwashing_investment_score: 80.0, sports_rights_acquisition_score: 82.0, soft_power_narrative_score: 85.0, human_rights_whitewash_score: 78.0, risk_level: "critique", primary_pattern: "soft_power_sport_offensif", key_signals: ["Sportwashing systémique de Chine — investissements massifs dans le sport mondial pour blanchir l'image du régime", "Achats de légitimité sportive — clubs, droits de diffusion et événements utilisés pour contourner les critiques diplomatiques", "Silence sportif sur les droits humains — athlètes et institutions achetés ou intimidés pour éviter toute condamnation publique"], estimated_sport_geopolitics_index: 8.14, last_updated: "2026-06-20" },
    { id: "SG-005", name: "Russie — Dopage d'État & Manipulation CAS", country: "Europe de l'Est", sector: "Programme Dopage McLaren, Exclusion Partielle & Corruption WADA/FIFA", composite_score: 57.5, sportwashing_investment_score: 55.0, sports_rights_acquisition_score: 60.0, soft_power_narrative_score: 52.0, human_rights_whitewash_score: 65.0, risk_level: "élevé", primary_pattern: "manipulation_sportive", key_signals: ["Manipulation sportive significative de Russie — instrumentalisation politisée des compétitions et des institutions sportives", "Dopage d'État ou corruption sportive — manipulation des règles compétitives pour des objectifs de prestige national", "Sport comme exutoire national — détournement de l'attention populaire des problèmes internes via la victoire sportive"], estimated_sport_geopolitics_index: 5.75, last_updated: "2026-06-20" },
    { id: "SG-006", name: "Azerbaïdjan/Belarus — JO Bakou & Sports Autoritaires", country: "Caucase/Europe", sector: "Bakou 2015 JO Européens & Belarus Sport Mobilisé pour Légitimer Loukachenko", composite_score: 52.75, sportwashing_investment_score: 50.0, sports_rights_acquisition_score: 48.0, soft_power_narrative_score: 55.0, human_rights_whitewash_score: 60.0, risk_level: "élevé", primary_pattern: "manipulation_sportive", key_signals: ["Manipulation sportive significative de Azerbaïdjan/Belarus — instrumentalisation politisée des compétitions et des institutions sportives", "Dopage d'État ou corruption sportive — manipulation des règles compétitives pour des objectifs de prestige national", "Sport comme exutoire national — détournement de l'attention populaire des problèmes internes via la victoire sportive"], estimated_sport_geopolitics_index: 5.28, last_updated: "2026-06-20" },
    { id: "SG-007", name: "USA — NBA/NFL Mondialisation Culturelle", country: "Amérique du Nord", sector: "NBA Chine, FIFA World Cup 2026 & Soft Power Culturel par le Sport Global", composite_score: 29.0, sportwashing_investment_score: 25.0, sports_rights_acquisition_score: 30.0, soft_power_narrative_score: 40.0, human_rights_whitewash_score: 20.0, risk_level: "modéré", primary_pattern: "puissance_douce_sportive", key_signals: ["Soft power sportif de USA — utilisation du sport comme vecteur de projection culturelle et d'influence mondiale", "Diplomatie sportive active — organisation d'événements et investissements dans les fédérations pour améliorer l'image", "Ambiguïté éthique — distinction floue entre soft power sportif légitime et sportwashing sans droits humains"], estimated_sport_geopolitics_index: 2.9, last_updated: "2026-06-20" },
    { id: "SG-008", name: "Finlande & Nouvelle-Zélande — Sport Éthique", country: "Europe/Pacifique", sector: "Politique Sport Transparente, Droits Humains dans Attribution & Gouvernance", composite_score: 5.1, sportwashing_investment_score: 5.0, sports_rights_acquisition_score: 4.0, soft_power_narrative_score: 8.0, human_rights_whitewash_score: 3.0, risk_level: "faible", primary_pattern: "sport_valeurs_democratiques", key_signals: ["Finlande & Nouvelle-Zélande incarne un modèle de sport éthique — compétitions transparentes et gouvernance respectueuse des droits", "Sport comme vecteur de valeurs démocratiques — fair play, inclusion et intégrité compétitive institutionnalisés", "Modèle de gouvernance sportive à diffuser — résistance au sportwashing et conditionnalité droits humains dans l'attribution"], estimated_sport_geopolitics_index: 0.51, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { sportwashing_systematique: 3, soft_power_sport_offensif: 1, manipulation_sportive: 2, puissance_douce_sportive: 1, sport_valeurs_democratiques: 1 },
    top_risk_entities: ["Qatar — Coupe du Monde 2022 & PSG Soft Power", "Arabie Saoudite — LIV Golf, Newcastle & PIF Sport", "Émirats Arabes — Manchester City & City Football Group"],
    critical_alerts: ["Qatar: sportwashing systématique", "Arabie Saoudite: sportwashing systématique", "Émirats Arabes: sportwashing systématique", "Chine: soft power sport offensif"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "sport_geopolitics",
    confidence_score: 0.86,
    data_sources: ["amnesty_sport_washing_tracker", "play_the_game_integrity_monitor", "human_rights_watch_sport_political_use"],
    entities,
    avg_estimated_sport_geopolitics_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
