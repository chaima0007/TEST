import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[hybrid-warfare-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Hybrid Warfare Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/hybrid-warfare-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Hybrid Warfare Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Hybrid Warfare Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "HW-001", name: "Russie — Doctrine Gerasimov & Opérations GRU", country: "Europe de l'Est", sector: "NotPetya 10Md$, Skripal, Nord Stream & Proxies Wagner/Syrie/Ukraine/Mali", composite_score: 87.1, information_warfare_score: 92.0, cyber_sabotage_score: 88.0, proxy_warfare_score: 90.0, legal_warfare_score: 75.0, risk_level: "critique", primary_pattern: "guerre_hybride_integree", key_signals: ["Guerre hybride systémique de Russie — opérations multi-domaines coordonnées contre adversaires sans déclaration de guerre formelle", "Doctrine de la zone grise — exploitation des seuils légaux et militaires pour éviter la réponse collective de l'OTAN/ONU", "Déni plausible institutionnalisé — proxies, mercenaires et hackers sans uniforme permettant la dénégation étatique"], estimated_hybrid_warfare_index: 8.71, last_updated: "2026-06-20" },
    { entity_id: "HW-002", name: "Chine — APT41, TikTok & Milices Maritimes", country: "Asie", sector: "APT10/APT41, Ingérence TikTok/WeChat & Milice Maritime Mer de Chine du Sud", composite_score: 83.9, information_warfare_score: 88.0, cyber_sabotage_score: 90.0, proxy_warfare_score: 72.0, legal_warfare_score: 85.0, risk_level: "critique", primary_pattern: "guerre_hybride_integree", key_signals: ["Guerre hybride systémique de Chine — opérations multi-domaines coordonnées contre adversaires sans déclaration de guerre formelle", "Doctrine de la zone grise — exploitation des seuils légaux et militaires pour éviter la réponse collective de l'OTAN/ONU", "Déni plausible institutionnalisé — proxies, mercenaires et hackers sans uniforme permettant la dénégation étatique"], estimated_hybrid_warfare_index: 8.39, last_updated: "2026-06-20" },
    { entity_id: "HW-003", name: "Iran — IRGC, Hezbollah & Proxies Régionaux", country: "MENA", sector: "IRGC + Hezbollah + Houthis + Milices Irakiennes — Réseau Proxy Régional Intégré", composite_score: 77.75, information_warfare_score: 80.0, cyber_sabotage_score: 75.0, proxy_warfare_score: 88.0, legal_warfare_score: 65.0, risk_level: "critique", primary_pattern: "guerre_par_procuration", key_signals: ["Guerre hybride systémique de Iran — opérations multi-domaines coordonnées contre adversaires sans déclaration de guerre formelle", "Doctrine de la zone grise — exploitation des seuils légaux et militaires pour éviter la réponse collective de l'OTAN/ONU", "Déni plausible institutionnalisé — proxies, mercenaires et hackers sans uniforme permettant la dénégation étatique"], estimated_hybrid_warfare_index: 7.78, last_updated: "2026-06-20" },
    { entity_id: "HW-004", name: "Corée du Nord — Lazarus & Cyberfinancement Nucléaire", country: "Asie", sector: "Groupe Lazarus, 1.2Md$ Cryptos Volés & Cyberattaques Bancaires SWIFT pour Nucléaire", composite_score: 73.1, information_warfare_score: 75.0, cyber_sabotage_score: 88.0, proxy_warfare_score: 68.0, legal_warfare_score: 58.0, risk_level: "critique", primary_pattern: "sabotage_cyber_systemique", key_signals: ["Guerre hybride systémique de Corée du Nord — opérations multi-domaines coordonnées contre adversaires sans déclaration de guerre formelle", "Doctrine de la zone grise — exploitation des seuils légaux et militaires pour éviter la réponse collective de l'OTAN/ONU", "Déni plausible institutionnalisé — proxies, mercenaires et hackers sans uniforme permettant la dénégation étatique"], estimated_hybrid_warfare_index: 7.31, last_updated: "2026-06-20" },
    { entity_id: "HW-005", name: "Turquie — Opérations Cognitives & Diasporas", country: "MENA/Europe", sector: "Trolls AKP, DITIB Diaspora & Opérations Info Syrie/Libye/Azerbaïdjan", composite_score: 54.9, information_warfare_score: 58.0, cyber_sabotage_score: 52.0, proxy_warfare_score: 62.0, legal_warfare_score: 45.0, risk_level: "élevé", primary_pattern: "operations_cognitives_offensives", key_signals: ["Opérations cognitives offensives de Turquie — campagnes actives de désinformation et manipulation narrative ciblées", "Influence sur les élections et le débat public — bots, fermes à trolls et médias pro-régime dans les pays cibles", "Exploitation des fractures sociales — amplification des divisions identitaires et politiques pour déstabiliser les sociétés"], estimated_hybrid_warfare_index: 5.49, last_updated: "2026-06-20" },
    { entity_id: "HW-006", name: "Inde/Pakistan — Guerre Hybride Sous-Continentale", country: "Asie du Sud", sector: "ISI Proxies Cachemire, RAW Contre-Opérations & Cyberguerre Indo-Pak Permanente", composite_score: 50.5, information_warfare_score: 52.0, cyber_sabotage_score: 48.0, proxy_warfare_score: 58.0, legal_warfare_score: 42.0, risk_level: "élevé", primary_pattern: "operations_cognitives_offensives", key_signals: ["Opérations cognitives offensives de Inde/Pakistan — campagnes actives de désinformation et manipulation narrative ciblées", "Influence sur les élections et le débat public — bots, fermes à trolls et médias pro-régime dans les pays cibles", "Exploitation des fractures sociales — amplification des divisions identitaires et politiques pour déstabiliser les sociétés"], estimated_hybrid_warfare_index: 5.05, last_updated: "2026-06-20" },
    { entity_id: "HW-007", name: "UE — Fragmentation Contre-Hybride Nationale", country: "Europe", sector: "IA Act sans Volet Hybride, Positions OTAN Divisées & Insuffisance Résilience Info", composite_score: 27.9, information_warfare_score: 28.0, cyber_sabotage_score: 32.0, proxy_warfare_score: 22.0, legal_warfare_score: 30.0, risk_level: "modéré", primary_pattern: "operations_cognitives_offensives", key_signals: ["Vulnérabilité hybride de UE — exposition aux opérations d'influence sans contre-mesures systémiques", "Déficit de résilience informationnelle — sociétés polarisées vulnérables aux narratifs adversaires", "Lacunes de coordination défensive — absence de doctrine nationale cohérente de contre-hybride"], estimated_hybrid_warfare_index: 2.79, last_updated: "2026-06-20" },
    { entity_id: "HW-008", name: "Estonie & Finlande — Résilience Hybride Intégrée", country: "Europe du Nord", sector: "StratCom COE, X-Road Cyber Résilience & Education Médias Anti-Désinformation", composite_score: 5.7, information_warfare_score: 5.0, cyber_sabotage_score: 8.0, proxy_warfare_score: 4.0, legal_warfare_score: 6.0, risk_level: "faible", primary_pattern: "resilience_democratique", key_signals: ["Estonie & Finlande maintient une résilience hybride exemplaire — défenses multi-domaines et dissuasion intégrée efficaces", "Éducation aux médias et résilience informationnelle — populations formées à identifier la désinformation étrangère", "Modèle de contre-hybride à partager — coopération intelligence+cyber+info dans un cadre démocratique"], estimated_hybrid_warfare_index: 0.57, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { guerre_hybride_integree: 2, sabotage_cyber_systemique: 1, guerre_par_procuration: 1, operations_cognitives_offensives: 3, resilience_democratique: 1 },
    top_risk_entities: ["Russie — Doctrine Gerasimov & Opérations GRU", "Chine — APT41, TikTok & Milices Maritimes", "Iran — IRGC, Hezbollah & Proxies Régionaux"],
    critical_alerts: ["Russie: guerre hybride intégrée", "Chine: guerre hybride intégrée", "Iran: guerre par procuration", "Corée du Nord: sabotage cyber systémique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "hybrid_warfare",
    confidence_score: 0.83,
    data_sources: ["hybrid_coe_helsinki_monitor", "bellingcat_hybrid_warfare_tracker", "icds_tallinn_strategic_review"],
    entities,
    avg_estimated_hybrid_warfare_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
