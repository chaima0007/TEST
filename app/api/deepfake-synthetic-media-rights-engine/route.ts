import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[deepfake-synthetic-media-rights-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  domain: "deepfake_synthetic_media_rights",
  generated_at: new Date().toISOString(),
  accent: "#7c3aed",
  avg_composite: 59.63,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    { id: "DSM-001", name: "Chine — Deepfakes Propagande État, Dissidents Ciblés & Fausses Preuves", composite_score: 91.40, risk_level: "critique", deepfake_identity_theft_scale_score: 91, victim_redress_legal_deficit_score: 90, state_weaponization_synthetic_media_score: 96, platform_accountability_gap_score: 88, estimated_deepfake_synthetic_media_rights_index: 9.14 },
    { id: "DSM-002", name: "Russie — Opérations Influence IA, Fabrication Preuves Judiciaires", composite_score: 90.10, risk_level: "critique", deepfake_identity_theft_scale_score: 88, victim_redress_legal_deficit_score: 92, state_weaponization_synthetic_media_score: 94, platform_accountability_gap_score: 86, estimated_deepfake_synthetic_media_rights_index: 9.01 },
    { id: "DSM-003", name: "Inde — Deepfake Pornographie Non-Consentie, 95% Victimes Femmes", composite_score: 85.20, risk_level: "critique", deepfake_identity_theft_scale_score: 90, victim_redress_legal_deficit_score: 88, state_weaponization_synthetic_media_score: 72, platform_accountability_gap_score: 91, estimated_deepfake_synthetic_media_rights_index: 8.52 },
    { id: "DSM-004", name: "USA — Élections Deepfake, Absence Loi Fédérale, Big Tech Autorégulation", composite_score: 77.35, risk_level: "critique", deepfake_identity_theft_scale_score: 82, victim_redress_legal_deficit_score: 75, state_weaponization_synthetic_media_score: 68, platform_accountability_gap_score: 85, estimated_deepfake_synthetic_media_rights_index: 7.73 },
    { id: "DSM-005", name: "Corée du Sud — Crise Deepfake Telegram, 80% Victimes Mineures", composite_score: 51.90, risk_level: "élevé", deepfake_identity_theft_scale_score: 58, victim_redress_legal_deficit_score: 52, state_weaponization_synthetic_media_score: 38, platform_accountability_gap_score: 60, estimated_deepfake_synthetic_media_rights_index: 5.19 },
    { id: "DSM-006", name: "Nigeria — Fraude Vocale IA, Arnaques Familiales & Romance Scams", composite_score: 51.90, risk_level: "élevé", deepfake_identity_theft_scale_score: 55, victim_redress_legal_deficit_score: 58, state_weaponization_synthetic_media_score: 42, platform_accountability_gap_score: 52, estimated_deepfake_synthetic_media_rights_index: 5.19 },
    { id: "DSM-007", name: "UE — AI Act Deepfake Watermarking, Protection Partielle En Cours", composite_score: 22.30, risk_level: "modéré", deepfake_identity_theft_scale_score: 26, victim_redress_legal_deficit_score: 22, state_weaponization_synthetic_media_score: 12, platform_accountability_gap_score: 30, estimated_deepfake_synthetic_media_rights_index: 2.23 },
    { id: "DSM-008", name: "Pays-Bas — C2PA Standard, Watermarking Obligatoire, Victimes Protégées", composite_score: 6.90, risk_level: "faible", deepfake_identity_theft_scale_score: 8, victim_redress_legal_deficit_score: 6, state_weaponization_synthetic_media_score: 4, platform_accountability_gap_score: 10, estimated_deepfake_synthetic_media_rights_index: 0.69 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/deepfake-synthetic-media-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
