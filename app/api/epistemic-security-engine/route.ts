import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[epistemic-security-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Epistemic Security Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/epistemic-security-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Epistemic Security Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Epistemic Security Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "ES-001", name: "Russie — Machine de Propagande", country: "Europe de l'Est", sector: "Désinformation d'État Systémique", composite_score: 89.9, disinformation_saturation_score: 95.0, reality_consensus_deficit_score: 88.0, media_ecosystem_fragmentation_score: 85.0, epistemic_vulnerability_score: 90.0, risk_level: "critique", primary_pattern: "chaos_epistemique_total", key_signals: ["Chaos épistémique critique en Russie — réalité partagée en effondrement", "Désinformation industrielle saturant l'espace informationnel public", "Fragmentation cognitive irréversible — bulles de réalité incompatibles coexistant"], estimated_epistemic_index: 8.99, last_updated: "2026-06-20" },
    { id: "ES-002", name: "Myanmar — Génocide Algorithmique", country: "Asie du Sud-Est", sector: "Manipulation Plateforme & Violence", composite_score: 84.25, disinformation_saturation_score: 88.0, reality_consensus_deficit_score: 85.0, media_ecosystem_fragmentation_score: 82.0, epistemic_vulnerability_score: 80.0, risk_level: "critique", primary_pattern: "chaos_epistemique_total", key_signals: ["Chaos épistémique critique au Myanmar — réalité partagée en effondrement", "Désinformation industrielle saturant l'espace informationnel public", "Fragmentation cognitive irréversible — bulles de réalité incompatibles coexistant"], estimated_epistemic_index: 8.43, last_updated: "2026-06-20" },
    { id: "ES-003", name: "États-Unis — Post-Vérité", country: "Amérique du Nord", sector: "Polarisation Épistémique Extrême", composite_score: 81.75, disinformation_saturation_score: 82.0, reality_consensus_deficit_score: 80.0, media_ecosystem_fragmentation_score: 88.0, epistemic_vulnerability_score: 75.0, risk_level: "critique", primary_pattern: "fracture_cognitive", key_signals: ["Chaos épistémique critique aux États-Unis — réalité partagée en effondrement", "Désinformation industrielle saturant l'espace informationnel public", "Fragmentation cognitive irréversible — bulles de réalité incompatibles coexistant"], estimated_epistemic_index: 8.18, last_updated: "2026-06-20" },
    { id: "ES-004", name: "Espace Numérique Global (TikTok/X)", country: "Cyberespace", sector: "Algorithmes & Bulles Cognitives", composite_score: 82.65, disinformation_saturation_score: 85.0, reality_consensus_deficit_score: 78.0, media_ecosystem_fragmentation_score: 90.0, epistemic_vulnerability_score: 72.0, risk_level: "critique", primary_pattern: "chaos_epistemique_total", key_signals: ["Chaos épistémique critique dans Espace Numérique Global (TikTok/X) — réalité partagée en effondrement", "Désinformation industrielle saturant l'espace informationnel public", "Fragmentation cognitive irréversible — bulles de réalité incompatibles coexistant"], estimated_epistemic_index: 8.27, last_updated: "2026-06-20" },
    { id: "ES-005", name: "Brésil — WhatsApp & Désinformation", country: "Amériques", sector: "Crise Informationnelle Endémique", composite_score: 64.35, disinformation_saturation_score: 68.0, reality_consensus_deficit_score: 62.0, media_ecosystem_fragmentation_score: 65.0, epistemic_vulnerability_score: 58.0, risk_level: "élevé", primary_pattern: "guerre_narrative", key_signals: ["Guerre narrative intense au Brésil — manipulation de l'information à grande échelle", "Écosystème médiatique fragmenté — algorithmes amplifiant les biais cognitifs", "Vulnérabilité épistémique élevée aux attaques de désinformation coordonnées"], estimated_epistemic_index: 6.44, last_updated: "2026-06-20" },
    { id: "ES-006", name: "Philippines — Ère Duterte", country: "Asie du Sud-Est", sector: "Désinformation Politique Organisée", composite_score: 59.85, disinformation_saturation_score: 62.0, reality_consensus_deficit_score: 58.0, media_ecosystem_fragmentation_score: 60.0, epistemic_vulnerability_score: 55.0, risk_level: "élevé", primary_pattern: "guerre_narrative", key_signals: ["Guerre narrative intense aux Philippines — manipulation de l'information à grande échelle", "Écosystème médiatique fragmenté — algorithmes amplifiant les biais cognitifs", "Vulnérabilité épistémique élevée aux attaques de désinformation coordonnées"], estimated_epistemic_index: 5.99, last_updated: "2026-06-20" },
    { id: "ES-007", name: "Europe Occidentale — DSA & Régulation", country: "Europe", sector: "Résilience Institutionnelle Partielle", composite_score: 33.1, disinformation_saturation_score: 35.0, reality_consensus_deficit_score: 30.0, media_ecosystem_fragmentation_score: 38.0, epistemic_vulnerability_score: 28.0, risk_level: "modéré", primary_pattern: "brouillard_informationnel", key_signals: ["Brouillard informationnel modéré en Europe Occidentale — saturation sans orchestration claire", "Littératie médiatique insuffisante face à la complexité de l'espace info", "Signaux de fragmentation narrative à surveiller"], estimated_epistemic_index: 3.31, last_updated: "2026-06-20" },
    { id: "ES-008", name: "Nordiques & Estonie — Littératie Max", country: "Europe du Nord", sector: "Résilience Épistémique Exemplaire", composite_score: 11.1, disinformation_saturation_score: 12.0, reality_consensus_deficit_score: 10.0, media_ecosystem_fragmentation_score: 14.0, epistemic_vulnerability_score: 8.0, risk_level: "faible", primary_pattern: "resilience_epistemique", key_signals: ["Nordiques & Estonie — Littératie Max maintient une résilience épistémique solide — réalité partagée préservée", "Littératie médiatique et fact-checking opérationnels", "Écosystème informationnel relativement sain — veille épistémique maintenue"], estimated_epistemic_index: 1.11, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { chaos_epistemique_total: 3, fracture_cognitive: 1, guerre_narrative: 2, brouillard_informationnel: 1, resilience_epistemique: 1 },
    top_risk_entities: ["Russie — Machine de Propagande", "Espace Numérique Global (TikTok/X)", "Myanmar — Génocide Algorithmique"],
    critical_alerts: ["Russie: chaos épistémique total", "Espace numérique global: chaos épistémique total", "Myanmar: chaos épistémique total", "États-Unis: fracture cognitive"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "epistemic",
    confidence_score: 0.77,
    data_sources: ["reuters_institute_digital_news", "disinfo_tracker", "cognitive_security_monitor"],
    entities,
    avg_estimated_epistemic_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
