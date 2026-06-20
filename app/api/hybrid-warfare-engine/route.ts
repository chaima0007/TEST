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
    { entity_id: "HW-001", name: "Ukraine & Frontière Est-Européenne", country: "Europe de l'Est", sector: "Zone de Conflit Hybride", composite_score: 87.25, cyber_intensity_score: 92.0, proxy_activity_score: 88.0, info_operations_score: 85.0, subthreshold_coercion_score: 82.0, risk_level: "critique", primary_pattern: "offensive_hybride_totale", key_signals: ["Offensive hybride critique — cyber+info+proxy en opération coordonnée active", "Intensité cyber et activité proxy au-delà des seuils d'attribution directe", "Zone grise totale — attaque sans déclaration de guerre formelle"], estimated_hybrid_index: 8.73, last_updated: "2026-06-20" },
    { entity_id: "HW-002", name: "Mer de Chine Méridionale", country: "Asie-Pacifique", sector: "Contestation Maritime Hybride", composite_score: 82.25, cyber_intensity_score: 82.0, proxy_activity_score: 90.0, info_operations_score: 75.0, subthreshold_coercion_score: 78.0, risk_level: "critique", primary_pattern: "offensive_hybride_totale", key_signals: ["Offensive hybride maritime — milices maritimes et cyberops coordonnées", "Contestation des eaux territoriales via acteurs non-étatiques contrôlés", "Coercition sous-seuil systématique — salami slicing stratégique"], estimated_hybrid_index: 8.23, last_updated: "2026-06-20" },
    { entity_id: "HW-003", name: "Mer Baltique & Nordiques", country: "Europe du Nord", sector: "Campagne Russe Hybride", composite_score: 77.25, cyber_intensity_score: 78.0, proxy_activity_score: 72.0, info_operations_score: 85.0, subthreshold_coercion_score: 68.0, risk_level: "critique", primary_pattern: "campagne_grise_ciblee", key_signals: ["Campagne grise ciblée — désinformation + sabotage d'infrastructures", "Opérations hybrides sous attribution plausiblement niable", "Pression sur les câbles sous-marins et infrastructures critiques nordiques"], estimated_hybrid_index: 7.73, last_updated: "2026-06-20" },
    { entity_id: "HW-004", name: "Afrique Sahélienne", country: "Afrique", sector: "Présence Milices & Proxies", composite_score: 69.25, cyber_intensity_score: 60.0, proxy_activity_score: 80.0, info_operations_score: 65.0, subthreshold_coercion_score: 72.0, risk_level: "critique", primary_pattern: "campagne_grise_ciblee", key_signals: ["Campagne hybride — présence de Wagner/proxies et opérations info antifrançaises", "Coercition sous-seuil via milices et désinformation anti-MINUSMA", "Fragilité étatique exploitée pour installation de présences hybrides durables"], estimated_hybrid_index: 6.93, last_updated: "2026-06-20" },
    { entity_id: "HW-005", name: "Moyen-Orient Étendu", country: "MENA", sector: "Opérations Proxy Régionales", composite_score: 67.75, cyber_intensity_score: 65.0, proxy_activity_score: 75.0, info_operations_score: 70.0, subthreshold_coercion_score: 60.0, risk_level: "critique", primary_pattern: "pression_hybride_elevee", key_signals: ["Pression hybride élevée — réseau de proxies et cyberops offensives", "Hezbollah, Houthis, milices irakiennes — convergence hybride régionale", "Guerre de l'ombre Iran/Israël/USA à travers acteurs non-étatiques"], estimated_hybrid_index: 6.78, last_updated: "2026-06-20" },
    { entity_id: "HW-006", name: "Balkans Occidentaux", country: "Europe Centrale", sector: "Déstabilisation Graduelle", composite_score: 44.75, cyber_intensity_score: 48.0, proxy_activity_score: 42.0, info_operations_score: 52.0, subthreshold_coercion_score: 38.0, risk_level: "élevé", primary_pattern: "pression_hybride_elevee", key_signals: ["Pression hybride élevée — désinformation et instrumentalisation des fractures ethniques", "Présence russe et chinoise dans les espaces d'influence hybride", "Fragilité démocratique exploitée via ingérence électorale hybride"], estimated_hybrid_index: 4.48, last_updated: "2026-06-20" },
    { entity_id: "HW-007", name: "Amérique Latine", country: "Amériques", sector: "Influence Hybride Limitée", composite_score: 27.5, cyber_intensity_score: 30.0, proxy_activity_score: 25.0, info_operations_score: 35.0, subthreshold_coercion_score: 22.0, risk_level: "modéré", primary_pattern: "signaux_hybrides_detectes", key_signals: ["Signaux hybrides modérés — ingérence électorale et désinformation détectées", "Présence chinoise et russe croissante dans l'espace informationnel", "Attribution incertaine — surveillance multi-domaines recommandée"], estimated_hybrid_index: 2.75, last_updated: "2026-06-20" },
    { entity_id: "HW-008", name: "Pacifique Sud", country: "Océanie", sector: "Zone Relativement Stable", composite_score: 13.75, cyber_intensity_score: 12.0, proxy_activity_score: 15.0, info_operations_score: 18.0, subthreshold_coercion_score: 10.0, risk_level: "faible", primary_pattern: "securite_hybride", key_signals: ["Profil hybride favorable — activité minimale détectée", "Présence d'influence étrangère limitée et containable", "Résilience hybride confirmée — veille multi-domaines maintenue"], estimated_hybrid_index: 1.38, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { offensive_hybride_totale: 2, campagne_grise_ciblee: 2, pression_hybride_elevee: 2, signaux_hybrides_detectes: 1, securite_hybride: 1 },
    top_risk_entities: ["Ukraine & Frontière Est-Européenne", "Mer de Chine Méridionale", "Mer Baltique & Nordiques"],
    critical_alerts: ["Ukraine: offensive hybride totale", "Mer de Chine: offensive hybride maritime", "Baltique: campagne grise ciblée"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "hybridwar",
    confidence_score: 0.81,
    data_sources: ["nato_hybrid_tracker", "cyber_threat_intelligence", "proxy_activity_monitor"],
    entities,
    avg_estimated_hybrid_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
