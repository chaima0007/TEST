import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-media-political-censorship-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Social Media Political Censorship Engine Agent",
  domain: "social_media_political_censorship",
  total_entities: 8,
  avg_composite: 63.7,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    platform_content_removal_political_severity: 2,
    internet_shutdown_election_suppression_scale: 3,
    state_disinformation_manipulation: 1,
    journalist_blogger_platform_ban_deficit_gap: 2,
  },
  top_risk_entities: [
    "Chine/Grande Muraille Feu — WeChat Weibo Contrôle Total, Algorithmes Surveillance & Mots-Clés Censurés Millions",
    "Russie/Blocages Twitter Meta — Loi Souveraineté Numérique RuNet, VPN Criminalisés & Blogueurs Emprisonnés Guerre",
    "Iran/VPN Généralisés — Coupures Élection Mahsa Amini, Instagram TikTok Bloqués & Cyber Police Arrestations",
  ],
  critical_alerts: [
    "Chine/Grande Muraille Feu: platform_content_removal_political_severity",
    "Russie/Blocages Twitter Meta: state_disinformation_manipulation",
    "Iran/VPN Généralisés: internet_shutdown_election_suppression_scale",
    "Inde/Shutdowns 2022: internet_shutdown_election_suppression_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_social_media_political_censorship_index: 6.37,
  data_sources: [
    "access_now_keepiton_internet_shutdown_tracker",
    "freedom_house_freedom_on_the_net_report",
    "eff_coercive_content_moderation_analysis",
  ],
  entities: [
    {
      id: "SMC-001",
      name: "Chine/Grande Muraille Feu — WeChat Weibo Contrôle Total, Algorithmes Surveillance & Mots-Clés Censurés Millions",
      country: "Chine",
      platform_content_removal_political_severity_score: 97.0,
      internet_shutdown_election_suppression_scale_score: 95.0,
      state_disinformation_manipulation_score: 96.0,
      journalist_blogger_platform_ban_deficit_gap_score: 94.0,
      composite_score: 95.65,
      risk_level: "critique",
      primary_pattern: "platform_content_removal_political_severity",
      estimated_social_media_political_censorship_index: 9.57,
      last_updated: "2026-06-21",
    },
    {
      id: "SMC-002",
      name: "Russie/Blocages Twitter Meta — Loi Souveraineté Numérique RuNet, VPN Criminalisés & Blogueurs Emprisonnés Guerre",
      country: "Russie",
      platform_content_removal_political_severity_score: 93.0,
      internet_shutdown_election_suppression_scale_score: 91.0,
      state_disinformation_manipulation_score: 94.0,
      journalist_blogger_platform_ban_deficit_gap_score: 92.0,
      composite_score: 92.55,
      risk_level: "critique",
      primary_pattern: "state_disinformation_manipulation",
      estimated_social_media_political_censorship_index: 9.26,
      last_updated: "2026-06-21",
    },
    {
      id: "SMC-003",
      name: "Iran/VPN Généralisés — Coupures Élection Mahsa Amini, Instagram TikTok Bloqués & Cyber Police Arrestations",
      country: "Iran",
      platform_content_removal_political_severity_score: 90.0,
      internet_shutdown_election_suppression_scale_score: 92.0,
      state_disinformation_manipulation_score: 89.0,
      journalist_blogger_platform_ban_deficit_gap_score: 91.0,
      composite_score: 90.45,
      risk_level: "critique",
      primary_pattern: "internet_shutdown_election_suppression_scale",
      estimated_social_media_political_censorship_index: 9.05,
      last_updated: "2026-06-21",
    },
    {
      id: "SMC-004",
      name: "Inde/Shutdowns 2022 — 584 Internet Coupures Record Mondial, Twitter Ordres Retrait & Farmer Protests Blocages",
      country: "Inde",
      platform_content_removal_political_severity_score: 87.0,
      internet_shutdown_election_suppression_scale_score: 89.0,
      state_disinformation_manipulation_score: 85.0,
      journalist_blogger_platform_ban_deficit_gap_score: 86.0,
      composite_score: 86.8,
      risk_level: "critique",
      primary_pattern: "internet_shutdown_election_suppression_scale",
      estimated_social_media_political_censorship_index: 8.68,
      last_updated: "2026-06-21",
    },
    {
      id: "SMC-005",
      name: "Éthiopie/Tigré — Coupures Internet 1 An Conflit, Journalistes Bloqués & Propagande État Réseaux Sociaux",
      country: "Éthiopie",
      platform_content_removal_political_severity_score: 57.0,
      internet_shutdown_election_suppression_scale_score: 60.0,
      state_disinformation_manipulation_score: 58.0,
      journalist_blogger_platform_ban_deficit_gap_score: 55.0,
      composite_score: 57.6,
      risk_level: "élevé",
      primary_pattern: "internet_shutdown_election_suppression_scale",
      estimated_social_media_political_censorship_index: 5.76,
      last_updated: "2026-06-21",
    },
    {
      id: "SMC-006",
      name: "Pakistan/Blocages PTI — Imran Khan Arrestations Twitter X Suspendu, TikTok Banni & Journalistes Disparus",
      country: "Pakistan",
      platform_content_removal_political_severity_score: 54.0,
      internet_shutdown_election_suppression_scale_score: 56.0,
      state_disinformation_manipulation_score: 55.0,
      journalist_blogger_platform_ban_deficit_gap_score: 57.0,
      composite_score: 55.35,
      risk_level: "élevé",
      primary_pattern: "journalist_blogger_platform_ban_deficit_gap",
      estimated_social_media_political_censorship_index: 5.54,
      last_updated: "2026-06-21",
    },
    {
      id: "SMC-007",
      name: "EFF/Access Now KeepItOn — Coalition Anti-Shutdown, Digital Rights Atlas & Rapport Annuel Coupures Internet",
      country: "Global",
      platform_content_removal_political_severity_score: 27.0,
      internet_shutdown_election_suppression_scale_score: 26.0,
      state_disinformation_manipulation_score: 25.0,
      journalist_blogger_platform_ban_deficit_gap_score: 28.0,
      composite_score: 26.45,
      risk_level: "modéré",
      primary_pattern: "journalist_blogger_platform_ban_deficit_gap",
      estimated_social_media_political_censorship_index: 2.65,
      last_updated: "2026-06-21",
    },
    {
      id: "SMC-008",
      name: "ONU/RES 32/13 — Internet Droit Fondamental, Rapporteur Spécial Expression En Ligne & GNI Principes",
      country: "Global",
      platform_content_removal_political_severity_score: 5.0,
      internet_shutdown_election_suppression_scale_score: 5.0,
      state_disinformation_manipulation_score: 4.0,
      journalist_blogger_platform_ban_deficit_gap_score: 5.0,
      composite_score: 4.75,
      risk_level: "faible",
      primary_pattern: "platform_content_removal_political_severity",
      estimated_social_media_political_censorship_index: 0.48,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/social-media-political-censorship-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
