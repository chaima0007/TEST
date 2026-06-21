import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[online-censorship-platform-governance-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Online Censorship Platform Governance Engine Agent",
  domain: "online_censorship_platform_governance",
  total_entities: 8,
  avg_composite: 61.7,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { internet_shutdown_content_blocking_severity: 4, social_media_political_censorship_scale: 2, platform_transparency_accountability_deficit_gap: 2 },
  top_risk_entities: ["Chine/GFW — Grand Firewall Chine, 10 000 Sites Bloqués, WeChat Surveillance & Contenu Politique Filtré IA", "Iran — Internet Coupé Manifestations 2019/2022, Telegram Bloqué, Système Intranet National & Dissidents Arrêtés Posts", "Russie/RuNet — Loi Souveraineté Internet 2019, Twitter Ralenti, Meta Interdit & Blogueurs 15 Ans Prison Critique Guerre"],
  critical_alerts: ["Chine/GFW: internet_shutdown_content_blocking_severity", "Iran: internet_shutdown_content_blocking_severity", "Russie/RuNet: social_media_political_censorship_scale", "Inde/Shutdowns: internet_shutdown_content_blocking_severity"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_online_censorship_platform_governance_index: 6.17,
  data_sources: ["freedom_house_freedom_on_net_report", "access_now_shutdown_tracker", "article19_digital_expression_report"],
  entities: [
    { entity_id: "OCP-001", name: "Chine/GFW — Grand Firewall Chine, 10 000 Sites Bloqués, WeChat Surveillance & Contenu Politique Filtré IA", country: "Chine", composite_score: 94.65, internet_shutdown_content_blocking_severity_score: 96.0, social_media_political_censorship_scale_score: 94.0, algorithmic_manipulation_disinformation_state_score: 95.0, platform_transparency_accountability_deficit_gap_score: 93.0, risk_level: "critique", primary_pattern: "internet_shutdown_content_blocking_severity", estimated_online_censorship_platform_governance_index: 9.46, last_updated: "2026-06-21" },
    { entity_id: "OCP-002", name: "Iran — Internet Coupé Manifestations 2019/2022, Telegram Bloqué, Système Intranet National & Dissidents Arrêtés Posts", country: "Iran", composite_score: 90.3, internet_shutdown_content_blocking_severity_score: 91.0, social_media_political_censorship_scale_score: 92.0, algorithmic_manipulation_disinformation_state_score: 88.0, platform_transparency_accountability_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "internet_shutdown_content_blocking_severity", estimated_online_censorship_platform_governance_index: 9.03, last_updated: "2026-06-21" },
    { entity_id: "OCP-003", name: "Russie/RuNet — Loi Souveraineté Internet 2019, Twitter Ralenti, Meta Interdit & Blogueurs 15 Ans Prison Critique Guerre", country: "Russie", composite_score: 87.45, internet_shutdown_content_blocking_severity_score: 87.0, social_media_political_censorship_scale_score: 89.0, algorithmic_manipulation_disinformation_state_score: 86.0, platform_transparency_accountability_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "social_media_political_censorship_scale", estimated_online_censorship_platform_governance_index: 8.75, last_updated: "2026-06-21" },
    { entity_id: "OCP-004", name: "Inde/Shutdowns — 84 Coupures Internet 2022 Monde Leader, J&K 18 Mois Coupure, Farmers Protest Bloqué & Twitter Ordres Retrait", country: "Inde", composite_score: 82.65, internet_shutdown_content_blocking_severity_score: 84.0, social_media_political_censorship_scale_score: 82.0, algorithmic_manipulation_disinformation_state_score: 83.0, platform_transparency_accountability_deficit_gap_score: 81.0, risk_level: "critique", primary_pattern: "internet_shutdown_content_blocking_severity", estimated_online_censorship_platform_governance_index: 8.27, last_updated: "2026-06-21" },
    { entity_id: "OCP-005", name: "Turquie — Twitter Bloqué 2022 Tremblement Terre, Wikipedia 3 Ans Bloqué, Journalistes Arrêtés Tweets & 400k Sites Filtrés", country: "Turquie", composite_score: 55.55, internet_shutdown_content_blocking_severity_score: 56.0, social_media_political_censorship_scale_score: 54.0, algorithmic_manipulation_disinformation_state_score: 57.0, platform_transparency_accountability_deficit_gap_score: 55.0, risk_level: "élevé", primary_pattern: "social_media_political_censorship_scale", estimated_online_censorship_platform_governance_index: 5.55, last_updated: "2026-06-21" },
    { entity_id: "OCP-006", name: "Nigeria/Twitter — Twitter Suspendu 7 Mois 2021, SARS Hashtag Censuré, NCC Ordres Retrait & VPN Criminalisé Envisagé", country: "Nigeria", composite_score: 52.45, internet_shutdown_content_blocking_severity_score: 52.0, social_media_political_censorship_scale_score: 51.0, algorithmic_manipulation_disinformation_state_score: 54.0, platform_transparency_accountability_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "platform_transparency_accountability_deficit_gap", estimated_online_censorship_platform_governance_index: 5.25, last_updated: "2026-06-21" },
    { entity_id: "OCP-007", name: "EFF/Article 19 — Electronic Frontier Foundation, Article 19 Expression Numérique, Access Now Shutdowns & Rapporteur Spécial Expression", country: "Global", composite_score: 26.55, internet_shutdown_content_blocking_severity_score: 27.0, social_media_political_censorship_scale_score: 25.0, algorithmic_manipulation_disinformation_state_score: 28.0, platform_transparency_accountability_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "platform_transparency_accountability_deficit_gap", estimated_online_censorship_platform_governance_index: 2.66, last_updated: "2026-06-21" },
    { entity_id: "OCP-008", name: "ONU/A-HRC — Résolution Droits En Ligne = Hors Ligne, Rapporteur Spécial Liberté Expression, IGF & Standards Plateformes", country: "Global", composite_score: 4.0, internet_shutdown_content_blocking_severity_score: 4.0, social_media_political_censorship_scale_score: 4.0, algorithmic_manipulation_disinformation_state_score: 4.0, platform_transparency_accountability_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "internet_shutdown_content_blocking_severity", estimated_online_censorship_platform_governance_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/online-censorship-platform-governance-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
