import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[mental-health-social-media-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "MHS_ENGINE",
  domain: "mental_health_social_media_rights",
  total_entities: 8,
  avg_composite: 61.43,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["center_humane_technology", "who_mental_health_digital", "american_psychological_association"],
  entities: [
    { id: "MHS-001", name: "TikTok Algorithm", country: "Chine/USA", composite_score: 94.3, risk_level: "critique", primary_pattern: "addiction_enfants_boucle_dopamine", estimated_mental_health_social_media_rights_index: 9.43, last_updated: "2026-06-22" },
    { id: "MHS-002", name: "Instagram Meta", country: "USA", composite_score: 92.3, risk_level: "critique", primary_pattern: "image_corporelle_depression_ados", estimated_mental_health_social_media_rights_index: 9.23, last_updated: "2026-06-22" },
    { id: "MHS-003", name: "Snapchat", country: "USA", composite_score: 79.1, risk_level: "critique", primary_pattern: "ephemeral_content_anxiete_sociale", estimated_mental_health_social_media_rights_index: 7.91, last_updated: "2026-06-22" },
    { id: "MHS-004", name: "YouTube Shorts", country: "USA", composite_score: 75.1, risk_level: "critique", primary_pattern: "recommandations_radicalisantes", estimated_mental_health_social_media_rights_index: 7.51, last_updated: "2026-06-22" },
    { id: "MHS-005", name: "Facebook Community", country: "USA", composite_score: 57.0, risk_level: "élevé", primary_pattern: "désinformation_sante_mentale", estimated_mental_health_social_media_rights_index: 5.70, last_updated: "2026-06-22" },
    { id: "MHS-006", name: "Twitter/X Toxicité", country: "USA", composite_score: 53.95, risk_level: "élevé", primary_pattern: "harassment_systémique_monetise", estimated_mental_health_social_media_rights_index: 5.40, last_updated: "2026-06-22" },
    { id: "MHS-007", name: "Pinterest Wellness", country: "USA", composite_score: 29.3, risk_level: "modéré", primary_pattern: "contenu_partiel_bienveillant", estimated_mental_health_social_media_rights_index: 2.93, last_updated: "2026-06-22" },
    { id: "MHS-008", name: "Center for Humane Tech", country: "USA", composite_score: 9.3, risk_level: "faible", primary_pattern: "design_éthique_anti_addiction", estimated_mental_health_social_media_rights_index: 0.93, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/mental-health-social-media-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
