import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pandemic-bioweapons-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Pandemic Bioweapons Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pandemic-bioweapons-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Pandemic Bioweapons Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Pandemic Bioweapons Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "PB-001", name: "Russie — Biopreparat & Arsenal BW Soviétique Hérité", country: "Europe de l'Est", sector: "Biopreparat 60K Chercheurs, Anthrax/Variole Modifiés & Installations Classifiées Toujours Actives", composite_score: 86.9, dual_use_research_score: 88.0, biosafety_breach_score: 92.0, bio_weapons_proliferation_score: 90.0, pandemic_preparedness_deficit_score: 75.0, risk_level: "critique", primary_pattern: "bioarmes_etatiques_actives", key_signals: ["Programme bioarmes étatique de Russie — recherche dual-use à des fins offensives avec déni de responsabilité institutionnel", "Arsenal biologique hérité ou développé — agents pathogènes modifiés génétiquement, production clandestine et vecteurs de dissémination", "Violation de la Convention des Armes Biologiques — absence de transparence, refus d'inspections et non-déclaration des installations"], estimated_pandemic_bioweapons_index: 8.69, last_updated: "2026-06-20" },
    { id: "PB-002", name: "Chine — BSL-4 Wuhan & Gain de Fonction Controversé", country: "Asie", sector: "WIV Wuhan BSL-4, EcoHealth Alliance Subventions & Origine Covid-19 Non Résolue Sous Enquête", composite_score: 84.0, dual_use_research_score: 85.0, biosafety_breach_score: 88.0, bio_weapons_proliferation_score: 82.0, pandemic_preparedness_deficit_score: 80.0, risk_level: "critique", primary_pattern: "bioarmes_etatiques_actives", key_signals: ["Programme bioarmes étatique de Chine — recherche dual-use à des fins offensives avec déni de responsabilité institutionnel", "Arsenal biologique hérité ou développé — agents pathogènes modifiés génétiquement, production clandestine et vecteurs de dissémination", "Violation de la Convention des Armes Biologiques — absence de transparence, refus d'inspections et non-déclaration des installations"], estimated_pandemic_bioweapons_index: 8.4, last_updated: "2026-06-20" },
    { id: "PB-003", name: "USA — DTRA, BARDA & Gain de Fonction Externalisé", country: "Amérique du Nord", sector: "DTRA Laboratoires Géorgie/Ukraine, Gain de Fonction via EcoHealth & Programme Biodefense Dual", composite_score: 81.1, dual_use_research_score: 82.0, biosafety_breach_score: 80.0, bio_weapons_proliferation_score: 78.0, pandemic_preparedness_deficit_score: 85.0, risk_level: "critique", primary_pattern: "risque_pandemique_emergent", key_signals: ["Programme bioarmes étatique de USA — recherche dual-use à des fins offensives avec déni de responsabilité institutionnel", "Arsenal biologique hérité ou développé — agents pathogènes modifiés génétiquement, production clandestine et vecteurs de dissémination", "Violation de la Convention des Armes Biologiques — absence de transparence, refus d'inspections et non-déclaration des installations"], estimated_pandemic_bioweapons_index: 8.11, last_updated: "2026-06-20" },
    { id: "PB-004", name: "RPDC — Programme BW Clandestin Anthrax/Variole", country: "Asie", sector: "Anthrax, Variole, Botulinum & Yersinia Suspectés — USGOV Estimations DIA Corée du Nord", composite_score: 76.1, dual_use_research_score: 75.0, biosafety_breach_score: 72.0, bio_weapons_proliferation_score: 88.0, pandemic_preparedness_deficit_score: 68.0, risk_level: "critique", primary_pattern: "programme_dual_use_offensif", key_signals: ["Programme bioarmes étatique de RPDC — recherche dual-use à des fins offensives avec déni de responsabilité institutionnel", "Arsenal biologique hérité ou développé — agents pathogènes modifiés génétiquement, production clandestine et vecteurs de dissémination", "Violation de la Convention des Armes Biologiques — absence de transparence, refus d'inspections et non-déclaration des installations"], estimated_pandemic_bioweapons_index: 7.61, last_updated: "2026-06-20" },
    { id: "PB-005", name: "Iran — IRGC Capacités BW & Dual-Use Biologique", country: "MENA", sector: "Instituts Pasteur Iran, IRGC Recherche BW Suspectée & Programme Vaccinal Dual-Use", composite_score: 54.45, dual_use_research_score: 52.0, biosafety_breach_score: 55.0, bio_weapons_proliferation_score: 62.0, pandemic_preparedness_deficit_score: 48.0, risk_level: "élevé", primary_pattern: "risque_pandemique_emergent", key_signals: ["Risque biologique élevé de Iran — capacités BW suspectées ou arsenaux hérités non vérifiés par les instances internationales", "Lacunes de biosécurité critiques — laboratoires BSL insuffisamment sécurisés exposant à des fuites accidentelles ou intentionnelles", "Prolifération d'agents pathogènes dangereux — transferts suspects de matériaux biologiques sans contrôle adéquat de l'AIEA-Bio"], estimated_pandemic_bioweapons_index: 5.45, last_updated: "2026-06-20" },
    { id: "PB-006", name: "Syrie & Irak — Restes Arsenaux Chimio-Bio", country: "MENA", sector: "Sarin Syrien Non Déclaré, Moutarde Soufre Daesh & Installations Non Démantelées OIAC", composite_score: 51.65, dual_use_research_score: 48.0, biosafety_breach_score: 58.0, bio_weapons_proliferation_score: 55.0, pandemic_preparedness_deficit_score: 45.0, risk_level: "élevé", primary_pattern: "risque_pandemique_emergent", key_signals: ["Risque biologique élevé de Syrie & Irak — capacités BW suspectées ou arsenaux hérités non vérifiés par les instances internationales", "Lacunes de biosécurité critiques — laboratoires BSL insuffisamment sécurisés exposant à des fuites accidentelles ou intentionnelles", "Prolifération d'agents pathogènes dangereux — transferts suspects de matériaux biologiques sans contrôle adéquat de l'AIEA-Bio"], estimated_pandemic_bioweapons_index: 5.17, last_updated: "2026-06-20" },
    { id: "PB-007", name: "Pays Émergents — Gaps Biosécurité Régionaux", country: "Global", sector: "GHS Index Lacunes Afrique/Asie du Sud, BSL-2 Sous-Standards & Surveillance Épidémique Déficiente", composite_score: 30.25, dual_use_research_score: 28.0, biosafety_breach_score: 32.0, bio_weapons_proliferation_score: 25.0, pandemic_preparedness_deficit_score: 38.0, risk_level: "modéré", primary_pattern: "risque_pandemique_emergent", key_signals: ["Vulnérabilité biosécurité de Pays Émergents — lacunes dans la préparation pandémique et les capacités de surveillance épidémique", "Faiblesse institutionnelle — systèmes de santé publique insuffisants pour détecter et contenir une émergence épidémique précoce", "Non-conformité RSI — obligations de notification internationale non respectées dans les délais requis par l'OMS"], estimated_pandemic_bioweapons_index: 3.03, last_updated: "2026-06-20" },
    { id: "PB-008", name: "OMS & BARDA — Résilience Biosécurité Multilatérale", country: "Global", sector: "RSI Révisé 2024, BARDA BPARDA, CEPI Vaccins & Fonds Pandémique G20 Doté 1.4Md$", composite_score: 4.45, dual_use_research_score: 5.0, biosafety_breach_score: 4.0, bio_weapons_proliferation_score: 3.0, pandemic_preparedness_deficit_score: 6.0, risk_level: "faible", primary_pattern: "resilience_biosecurite", key_signals: ["OMS & BARDA incarne la résilience biosécurité — cadres robustes de prévention, détection et réponse aux menaces biologiques", "Transparence épidémique exemplaire — notification immédiate à l'OMS et coopération internationale sur la surveillance pathogénique", "Modèle de préparation pandémique à universaliser — stockages stratégiques, plans de continuité et chaînes de distribution vaccinales"], estimated_pandemic_bioweapons_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { bioarmes_etatiques_actives: 2, programme_dual_use_offensif: 1, vulnerabilite_biosecurite_critique: 0, risque_pandemique_emergent: 4, resilience_biosecurite: 1 },
    top_risk_entities: ["Russie — Biopreparat & Arsenal BW Soviétique Hérité", "Chine — BSL-4 Wuhan & Gain de Fonction Controversé", "USA — DTRA, BARDA & Gain de Fonction Externalisé"],
    critical_alerts: ["Russie: bioarmes étatiques actives", "Chine: bioarmes étatiques actives", "RPDC: programme dual-use offensif", "USA: risque pandémique émergent"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "pandemic_bioweapons",
    confidence_score: 0.75,
    data_sources: ["ghs_index_global_biosecurity", "nuclear_threat_initiative_bio", "who_ihr_monitoring_framework"],
    entities,
    avg_estimated_pandemic_bioweapons_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
