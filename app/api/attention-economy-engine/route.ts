import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[attention-economy-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Attention Economy Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/attention-economy-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Attention Economy Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Attention Economy Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "AE-001", name: "Espace Numérique Global (Meta/TikTok)", country: "Cyberespace", sector: "Plateformes Prédatrices de l'Attention", composite_score: 91.75, platform_capture_score: 95.0, algorithmic_manipulation_score: 92.0, cognitive_bandwidth_erosion_score: 88.0, behavioral_modification_score: 90.0, risk_level: "critique", primary_pattern: "colonisation_cognitive", key_signals: ["Colonisation cognitive critique dans Espace Numérique Global — autonomie attentionnelle compromise", "Algorithmes d'optimisation de l'engagement modifiant les comportements à grande échelle", "Capture de l'attention par les plateformes — infrastructure de manipulation opérationnelle"], estimated_attention_index: 9.18, last_updated: "2026-06-20" },
    { id: "AE-002", name: "Adolescents Mondiaux — Crise Mentale", country: "Global", sector: "Génération Z & Santé Mentale Numérique", composite_score: 86.75, platform_capture_score: 90.0, algorithmic_manipulation_score: 85.0, cognitive_bandwidth_erosion_score: 88.0, behavioral_modification_score: 82.0, risk_level: "critique", primary_pattern: "colonisation_cognitive", key_signals: ["Colonisation cognitive critique des Adolescents Mondiaux — autonomie attentionnelle compromise", "Algorithmes d'optimisation de l'engagement modifiant les comportements à grande échelle", "Capture de l'attention par les plateformes — infrastructure de manipulation opérationnelle"], estimated_attention_index: 8.68, last_updated: "2026-06-20" },
    { id: "AE-003", name: "États-Unis — Empire de l'Attention", country: "Amérique du Nord", sector: "Silicon Valley & Capture Cognitive", composite_score: 82.75, platform_capture_score: 88.0, algorithmic_manipulation_score: 80.0, cognitive_bandwidth_erosion_score: 82.0, behavioral_modification_score: 78.0, risk_level: "critique", primary_pattern: "colonisation_cognitive", key_signals: ["Colonisation cognitive critique aux États-Unis — autonomie attentionnelle compromise", "Algorithmes d'optimisation de l'engagement modifiant les comportements à grande échelle", "Capture de l'attention par les plateformes — infrastructure de manipulation opérationnelle"], estimated_attention_index: 8.28, last_updated: "2026-06-20" },
    { id: "AE-004", name: "Chine — Export d'Attention (TikTok)", country: "Asie", sector: "Géopolitique de l'Attention Numérique", composite_score: 79.75, platform_capture_score: 82.0, algorithmic_manipulation_score: 78.0, cognitive_bandwidth_erosion_score: 75.0, behavioral_modification_score: 80.0, risk_level: "critique", primary_pattern: "colonisation_cognitive", key_signals: ["Colonisation cognitive critique en Chine — autonomie attentionnelle compromise", "Algorithmes d'optimisation de l'engagement modifiant les comportements à grande échelle", "Capture de l'attention par les plateformes — infrastructure de manipulation opérationnelle"], estimated_attention_index: 7.98, last_updated: "2026-06-20" },
    { id: "AE-005", name: "Inde & Asie du Sud-Est", country: "Asie", sector: "Disruption Numérique à Grande Vitesse", composite_score: 61.25, platform_capture_score: 65.0, algorithmic_manipulation_score: 60.0, cognitive_bandwidth_erosion_score: 62.0, behavioral_modification_score: 55.0, risk_level: "élevé", primary_pattern: "fragmentation_attentionnelle", key_signals: ["Fragmentation attentionnelle élevée en Inde & Asie du Sud-Est — capacité de concentration dégradée", "Addiction algorithmique normalisée — dark patterns omniprésents", "Érosion de la bande passante cognitive collective — vulnérabilité à la manipulation"], estimated_attention_index: 6.13, last_updated: "2026-06-20" },
    { id: "AE-006", name: "Europe — GDPR & DSA Partiels", country: "Europe", sector: "Régulation vs Capture Attentionnelle", composite_score: 46.75, platform_capture_score: 50.0, algorithmic_manipulation_score: 45.0, cognitive_bandwidth_erosion_score: 48.0, behavioral_modification_score: 42.0, risk_level: "élevé", primary_pattern: "fragmentation_attentionnelle", key_signals: ["Fragmentation attentionnelle élevée en Europe — capacité de concentration dégradée", "Addiction algorithmique normalisée — dark patterns omniprésents", "Érosion de la bande passante cognitive collective — vulnérabilité à la manipulation"], estimated_attention_index: 4.68, last_updated: "2026-06-20" },
    { id: "AE-007", name: "Corée du Sud — Conscience Numérique", country: "Asie du Nord-Est", sector: "Hygiène Numérique en Construction", composite_score: 30.75, platform_capture_score: 35.0, algorithmic_manipulation_score: 28.0, cognitive_bandwidth_erosion_score: 32.0, behavioral_modification_score: 25.0, risk_level: "modéré", primary_pattern: "stress_informationnel", key_signals: ["Stress informationnel modéré en Corée du Sud — surcharge sans capture totale", "Tensions entre autonomie numérique et capture attentionnelle", "Conscience croissante des risques — régulation partielle en cours"], estimated_attention_index: 3.08, last_updated: "2026-06-20" },
    { id: "AE-008", name: "Finlande & Pays-Bas — Modèle Numérique", country: "Europe du Nord", sector: "Souveraineté Attentionnelle Exemplaire", composite_score: 13.0, platform_capture_score: 15.0, algorithmic_manipulation_score: 12.0, cognitive_bandwidth_erosion_score: 14.0, behavioral_modification_score: 10.0, risk_level: "faible", primary_pattern: "hygiene_numerique", key_signals: ["Finlande & Pays-Bas — Modèle Numérique préserve une hygiène numérique satisfaisante — autonomie cognitive maintenue", "Régulation efficace des plateformes et littératie numérique développée", "Modèle de souveraineté attentionnelle à étudier et diffuser"], estimated_attention_index: 1.30, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { colonisation_cognitive: 4, addiction_systematique: 0, fragmentation_attentionnelle: 2, stress_informationnel: 1, hygiene_numerique: 1 },
    top_risk_entities: ["Espace Numérique Global (Meta/TikTok)", "Adolescents Mondiaux — Crise Mentale", "États-Unis — Empire de l'Attention"],
    critical_alerts: ["Espace numérique global: colonisation cognitive", "Adolescents: colonisation cognitive", "États-Unis: colonisation cognitive", "Chine: colonisation cognitive"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "attention",
    confidence_score: 0.75,
    data_sources: ["screen_time_data", "attention_economy_research", "digital_wellbeing_index"],
    entities,
    avg_estimated_attention_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
