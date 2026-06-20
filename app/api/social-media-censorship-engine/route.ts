import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-media-censorship-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Social Media Censorship Engine Agent",
  domain: "social_media_censorship",
  total_entities: 8,
  avg_composite: 60.11,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { platform_blocking_scope: 2, content_removal_political: 2, user_data_state_access: 2, algorithmic_suppression: 2 },
  top_risk_entities: [
    "Chine — Grand Firewall, WeChat Surveillance & Toutes Plateformes Occidentales Bloquées",
    "Russie — Blocage Instagram/Facebook post-2022, RuNet & Loi Souveraineté Internet",
    "Iran — Blocage WhatsApp/Telegram, Shamr Filtre & Coupures lors Protestations",
  ],
  critical_alerts: [
    "Chine: platform_blocking_scope",
    "Russie: content_removal_political",
    "Iran: user_data_state_access",
    "Myanmar: platform_blocking_scope",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_social_media_censorship_index: 6.01,
  data_sources: [
    "freedom_house_freedom_on_the_net_platform_censorship_report",
    "citizenlab_internet_censorship_global_network_interference_dataset",
    "netblocks_internet_shutdown_observatory_social_media_blocking_monitor",
  ],
  entities: [
    { entity_id: "SMC-001", name: "Chine — Grand Firewall, WeChat Surveillance & Toutes Plateformes Occidentales Bloquées", country: "Asie du Nord-Est", composite_score: 95.15, platform_blocking_scope_score: 98.0, content_removal_political_score: 95.0, algorithmic_suppression_score: 92.0, user_data_state_access_score: 95.0, risk_level: "critique", primary_pattern: "platform_blocking_scope", estimated_social_media_censorship_index: 9.52, last_updated: "2026-06-20" },
    { entity_id: "SMC-002", name: "Russie — Blocage Instagram/Facebook post-2022, RuNet & Loi Souveraineté Internet", country: "Europe de l'Est", composite_score: 86.65, platform_blocking_scope_score: 88.0, content_removal_political_score: 88.0, algorithmic_suppression_score: 85.0, user_data_state_access_score: 85.0, risk_level: "critique", primary_pattern: "content_removal_political", estimated_social_media_censorship_index: 8.67, last_updated: "2026-06-20" },
    { entity_id: "SMC-003", name: "Iran — Blocage WhatsApp/Telegram, Shamr Filtre & Coupures lors Protestations", country: "Moyen-Orient", composite_score: 83.6, platform_blocking_scope_score: 85.0, content_removal_political_score: 82.0, algorithmic_suppression_score: 80.0, user_data_state_access_score: 88.0, risk_level: "critique", primary_pattern: "user_data_state_access", estimated_social_media_censorship_index: 8.36, last_updated: "2026-06-20" },
    { entity_id: "SMC-004", name: "Myanmar — Blocage Facebook/Twitter Coup 2021, Coupures Internet & Surveillance Militaire", country: "Asie du Sud-Est", composite_score: 80.5, platform_blocking_scope_score: 82.0, content_removal_political_score: 80.0, algorithmic_suppression_score: 78.0, user_data_state_access_score: 82.0, risk_level: "critique", primary_pattern: "platform_blocking_scope", estimated_social_media_censorship_index: 8.05, last_updated: "2026-06-20" },
    { entity_id: "SMC-005", name: "Meta/TikTok — Modération Opaque Contenu Politique, Biais Algorithmique & Rapports Transparence Lacunaires", country: "Global/USA", composite_score: 53.85, platform_blocking_scope_score: 52.0, content_removal_political_score: 55.0, algorithmic_suppression_score: 58.0, user_data_state_access_score: 50.0, risk_level: "élevé", primary_pattern: "algorithmic_suppression", estimated_social_media_censorship_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "SMC-006", name: "Inde — Blocages Temporaires Cachemire, Orders IT Rules 2021 & Takedowns Gouvernementaux", country: "Asie du Sud", composite_score: 50.9, platform_blocking_scope_score: 48.0, content_removal_political_score: 52.0, algorithmic_suppression_score: 50.0, user_data_state_access_score: 55.0, risk_level: "élevé", primary_pattern: "content_removal_political", estimated_social_media_censorship_index: 5.09, last_updated: "2026-06-20" },
    { entity_id: "SMC-007", name: "UE/DSA — Digital Services Act, Obligations Transparence & Mécanismes Recours Utilisateurs", country: "Europe", composite_score: 25.85, platform_blocking_scope_score: 22.0, content_removal_political_score: 25.0, algorithmic_suppression_score: 28.0, user_data_state_access_score: 30.0, risk_level: "modéré", primary_pattern: "algorithmic_suppression", estimated_social_media_censorship_index: 2.59, last_updated: "2026-06-20" },
    { entity_id: "SMC-008", name: "ONU/Rapporteur Expression — Lignes Directrices Modération, Standards Droits & Dialogue Plateformes", country: "Global", composite_score: 4.4, platform_blocking_scope_score: 4.0, content_removal_political_score: 5.0, algorithmic_suppression_score: 3.0, user_data_state_access_score: 6.0, risk_level: "faible", primary_pattern: "user_data_state_access", estimated_social_media_censorship_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social-media-censorship-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
