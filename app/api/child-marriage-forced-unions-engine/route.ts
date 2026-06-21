import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-marriage-forced-unions-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Child Marriage Forced Unions Engine Agent",
  domain: "child_marriage_forced_unions",
  total_entities: 8,
  avg_composite: 60.23,
  confidence_score: 0.88,
  avg_estimated_child_marriage_forced_unions_index: 6.02,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  data_sources: [
    "girls_not_brides_global_data_2023",
    "unicef_child_marriage_data_2023",
    "icrw_child_marriage_atlas_2023",
    "human_rights_watch_child_marriage_reports_2023",
  ],
  entities: [
    { entity_id: "CMF-001", name: "Niger — Taux Mondial Mariage Enfants le Plus Élevé: 76% Filles Mariées Avant 18 Ans", country: "Afrique de l'Ouest", composite_score: 93.80, risk_level: "critique", estimated_child_marriage_forced_unions_index: 9.38, last_updated: "2026-06-21" },
    { entity_id: "CMF-002", name: "Bangladesh — Loi Exceptions 2017: Mariage Sans Âge Minimum & Consentement Parental Forcé", country: "Asie du Sud", composite_score: 89.45, risk_level: "critique", estimated_child_marriage_forced_unions_index: 8.95, last_updated: "2026-06-21" },
    { entity_id: "CMF-003", name: "République Centrafricaine — Conflits Armés: Mariages Forcés Comme Arme Guerre & Survie", country: "Afrique Centrale", composite_score: 86.20, risk_level: "critique", estimated_child_marriage_forced_unions_index: 8.62, last_updated: "2026-06-21" },
    { entity_id: "CMF-004", name: "Pakistan — Mariage Précoce Rural, Vani/Swara Pratiques Tribales & Impunité Systémique", country: "Asie du Sud", composite_score: 82.55, risk_level: "critique", estimated_child_marriage_forced_unions_index: 8.26, last_updated: "2026-06-21" },
    { entity_id: "CMF-005", name: "Éthiopie — Mariage Enfants Régions Amhara/Afar: Pauvreté, Dot & Pression Communautaire", country: "Afrique de l'Est", composite_score: 53.70, risk_level: "élevé", estimated_child_marriage_forced_unions_index: 5.37, last_updated: "2026-06-21" },
    { entity_id: "CMF-006", name: "Yémen — Guerre & Effondrement Système: Hausse Mariages Enfants Comme Mécanisme Survie", country: "Moyen-Orient", composite_score: 50.40, risk_level: "élevé", estimated_child_marriage_forced_unions_index: 5.04, last_updated: "2026-06-21" },
    { entity_id: "CMF-007", name: "Girls Not Brides — Coalition 1400+ ONG, Plaidoyer Législatif & Programmes Éducation Filles", country: "Global", composite_score: 26.85, risk_level: "modéré", estimated_child_marriage_forced_unions_index: 2.69, last_updated: "2026-06-21" },
    { entity_id: "CMF-008", name: "UNICEF/ONU Femmes — SDG 5.3, Mécanismes Suivi & Programmes Prévention Mariage Enfants", country: "Global", composite_score: 5.95, risk_level: "faible", estimated_child_marriage_forced_unions_index: 0.60, last_updated: "2026-06-21" },
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-marriage-forced-unions-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
