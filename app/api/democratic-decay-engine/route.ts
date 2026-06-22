import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[democratic-decay-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Democratic Decay Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/democratic-decay-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Democratic Decay Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Democratic Decay Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "DD-001", name: "Russie & Biélorussie", country: "Europe de l'Est", sector: "Autoritarisme Électoral", composite_score: 89.25, institutional_erosion_score: 92.0, civil_liberties_decline_score: 88.0, electoral_integrity_score: 85.0, media_freedom_score: 90.0, risk_level: "critique", primary_pattern: "effondrement_democratique", key_signals: ["Effondrement démocratique critique — autocratisation avancée et irréversible", "Capture totale judiciaire, exécutif et médias sous contrôle politique", "Processus électoraux fondamentalement compromis"], estimated_demdecay_index: 8.93, last_updated: "2026-06-20" },
    { id: "DD-002", name: "Chine & Hong Kong", country: "Asie-Pacifique", sector: "Autocratie de Parti", composite_score: 88.5, institutional_erosion_score: 90.0, civil_liberties_decline_score: 85.0, electoral_integrity_score: 88.0, media_freedom_score: 92.0, risk_level: "critique", primary_pattern: "effondrement_democratique", key_signals: ["Effondrement démocratique — autocratie de parti institutionnalisée", "Hong Kong: démantèlement complet des libertés civiles", "Contrôle total des médias et répression de la société civile"], estimated_demdecay_index: 8.85, last_updated: "2026-06-20" },
    { id: "DD-003", name: "Hongrie & Serbie", country: "Europe Centrale", sector: "Illibéralisme Électoral", composite_score: 74.5, institutional_erosion_score: 78.0, civil_liberties_decline_score: 72.0, electoral_integrity_score: 70.0, media_freedom_score: 80.0, risk_level: "critique", primary_pattern: "capture_institutionnelle", key_signals: ["Capture institutionnelle critique — illibéralisme électoral enraciné", "Judiciaire et médias sous contrôle gouvernemental", "Érosion de l'état de droit au sein même de l'UE"], estimated_demdecay_index: 7.45, last_updated: "2026-06-20" },
    { id: "DD-004", name: "Turquie & Inde", country: "Asie Occidentale", sector: "Démocratie Illibérale", composite_score: 66.25, institutional_erosion_score: 68.0, civil_liberties_decline_score: 65.0, electoral_integrity_score: 62.0, media_freedom_score: 70.0, risk_level: "critique", primary_pattern: "capture_institutionnelle", key_signals: ["Démocratie illibérale avancée — institutions affaiblies mais élections maintenues", "Liberté de presse et société civile sous pression majeure", "Polarisation ethnicoreligieuse instrumentalisée"], estimated_demdecay_index: 6.63, last_updated: "2026-06-20" },
    { id: "DD-005", name: "Amérique Latine Fragile", country: "Amériques", sector: "Polarisation Démocratique", composite_score: 49.0, institutional_erosion_score: 52.0, civil_liberties_decline_score: 48.0, electoral_integrity_score: 50.0, media_freedom_score: 45.0, risk_level: "élevé", primary_pattern: "erosion_progressive", key_signals: ["Érosion démocratique élevée — institutions sous pression populiste", "Polarisation politique extrême fragilisant le consensus démocratique", "Liberté de presse en recul dans plusieurs pays"], estimated_demdecay_index: 4.90, last_updated: "2026-06-20" },
    { id: "DD-006", name: "États-Unis & Royaume-Uni", country: "Occident", sector: "Fragilité Institutionnelle", composite_score: 34.25, institutional_erosion_score: 38.0, civil_liberties_decline_score: 35.0, electoral_integrity_score: 32.0, media_freedom_score: 30.0, risk_level: "modéré", primary_pattern: "fragilite_democratique", key_signals: ["Fragilité démocratique modérée — polarisation et méfiance institutionnelle", "Désinformation et tensions électorales — vigilance nécessaire", "Démocraties robustes mais sous stress populiste"], estimated_demdecay_index: 3.43, last_updated: "2026-06-20" },
    { id: "DD-007", name: "Europe Occidentale", country: "Europe", sector: "Démocraties Établies", composite_score: 18.75, institutional_erosion_score: 20.0, civil_liberties_decline_score: 18.0, electoral_integrity_score: 15.0, media_freedom_score: 22.0, risk_level: "faible", primary_pattern: "democratie_consolidee", key_signals: ["Démocraties consolidées — institutions indépendantes et libertés préservées", "Montée modérée des populismes — résilience institutionnelle maintenue", "Veille démocratique active — aucune dégradation systémique"], estimated_demdecay_index: 1.88, last_updated: "2026-06-20" },
    { id: "DD-008", name: "Nordiques & Nouvelle-Zélande", country: "Modèles Démocratiques", sector: "Démocraties de Référence", composite_score: 5.75, institutional_erosion_score: 5.0, civil_liberties_decline_score: 8.0, electoral_integrity_score: 4.0, media_freedom_score: 6.0, risk_level: "faible", primary_pattern: "democratie_consolidee", key_signals: ["Démocraties de référence mondiale — libertés civiles et institutionnelles exemplaires", "Presse libre et indépendante — société civile florissante", "Processus électoraux les plus intègres au monde"], estimated_demdecay_index: 0.58, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 1, faible: 2 },
    pattern_distribution: { effondrement_democratique: 2, capture_institutionnelle: 2, erosion_progressive: 1, fragilite_democratique: 1, democratie_consolidee: 2 },
    top_risk_entities: ["Russie & Biélorussie", "Chine & Hong Kong", "Hongrie & Serbie"],
    critical_alerts: ["Russie & Biélorussie: effondrement démocratique", "Chine & Hong Kong: effondrement démocratique", "Hongrie & Serbie: capture institutionnelle"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "democrisis",
    confidence_score: 0.87,
    data_sources: ["v_dem_institute", "freedom_house_index", "electoral_integrity_project"],
    entities,
    avg_estimated_demdecay_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
