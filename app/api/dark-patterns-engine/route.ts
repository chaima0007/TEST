import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[dark-patterns-engine] SWARM_API_URL non défini — mode mock activé");
}

const MOCK_ENTITIES = [
  {
    id: "DKP-001",
    name: "StreamTrap Media",
    country: "États-Unis",
    sector: "Streaming & Abonnement",
    composite_score: 87.25,
    deception_score: 92.0,
    coercion_score: 88.0,
    addiction_score: 85.0,
    exploitation_score: 82.0,
    risk_level: "critique",
    primary_pattern: "Déception Systématique Interface",
    key_signals: [
      "Résiliation cachée 7 clics — parcours délibérément obstrué",
      "Frais dissimulés révélés uniquement au paiement final",
      "Design confirmshaming sur 89% des tentatives annulation",
    ],
    estimated_darkpattern_index: 8.73,
    last_updated: "2026-06-20",
  },
  {
    id: "DKP-002",
    name: "SocialLoop Platform",
    country: "Chine",
    sector: "Réseau Social",
    composite_score: 83.95,
    deception_score: 88.0,
    coercion_score: 85.0,
    addiction_score: 82.0,
    exploitation_score: 79.0,
    risk_level: "critique",
    primary_pattern: "Ingénierie Addiction Comportementale",
    key_signals: [
      "Boucles dopaminergiques artificielles — push illimités 3h-5h",
      "Variable reward schedules copiés des machines à sous",
      "Suppression option limitation temps — bannie côté back-end",
    ],
    estimated_darkpattern_index: 8.4,
    last_updated: "2026-06-19",
  },
  {
    id: "DKP-003",
    name: "ConsentForge Analytics",
    country: "Irlande",
    sector: "AdTech & Analytics",
    composite_score: 78.25,
    deception_score: 82.0,
    coercion_score: 79.0,
    addiction_score: 78.0,
    exploitation_score: 72.0,
    risk_level: "critique",
    primary_pattern: "Coercition Consentement Numérique",
    key_signals: [
      "Bandeau cookie — refus caché sous 4 niveaux de menus",
      "Opt-in pré-coché pour 23 catégories partenaires publicitaires",
      "Mise à jour politique vie privée — consentement silencieux",
    ],
    estimated_darkpattern_index: 7.83,
    last_updated: "2026-06-18",
  },
  {
    id: "DKP-004",
    name: "GameLoop Mobile",
    country: "Japon",
    sector: "Gaming Mobile",
    composite_score: 61.1,
    deception_score: 62.0,
    coercion_score: 60.0,
    addiction_score: 58.0,
    exploitation_score: 65.0,
    risk_level: "élevé",
    primary_pattern: "Exploitation Psychologique Ciblée",
    key_signals: [
      "Loot boxes ciblant mineurs — mécaniques FOMO exploitées",
      "Faux minuteurs urgence sur achats in-app",
      "Personnages IA simulant liens affectifs pour monétisation",
    ],
    estimated_darkpattern_index: 6.11,
    last_updated: "2026-06-17",
  },
  {
    id: "DKP-005",
    name: "EcomTrick Marketplace",
    country: "Singapour",
    sector: "E-Commerce",
    composite_score: 57.05,
    deception_score: 58.0,
    coercion_score: 62.0,
    addiction_score: 55.0,
    exploitation_score: 52.0,
    risk_level: "élevé",
    primary_pattern: "Déception Systématique Interface",
    key_signals: [
      "Prix barrés fictifs — référence inventée non vérifiable",
      "Faux indicateurs stock ('Plus que 2 !') permanents",
      "Frais livraison apparus uniquement à la dernière étape checkout",
    ],
    estimated_darkpattern_index: 5.71,
    last_updated: "2026-06-16",
  },
  {
    id: "DKP-006",
    name: "NewsFlow Digital",
    country: "Allemagne",
    sector: "Médias & Information",
    composite_score: 36.55,
    deception_score: 38.0,
    coercion_score: 35.0,
    addiction_score: 40.0,
    exploitation_score: 32.0,
    risk_level: "modéré",
    primary_pattern: "Nudge Opaque Décisionnel",
    key_signals: [
      "Algorithme recommandation opaque amplifiant contenus polarisants",
      "Newsletter opt-out en 3 étapes non standardisées",
      "Autoplay vidéo activé par défaut — désactivation peu visible",
    ],
    estimated_darkpattern_index: 3.66,
    last_updated: "2026-06-15",
  },
  {
    id: "DKP-007",
    name: "EthicalShop Cooperative",
    country: "Suisse",
    sector: "Commerce Éthique",
    composite_score: 9.8,
    deception_score: 10.0,
    coercion_score: 12.0,
    addiction_score: 8.0,
    exploitation_score: 9.0,
    risk_level: "faible",
    primary_pattern: "Nudge Opaque Décisionnel",
    key_signals: [
      "Interface certifiée sans dark patterns — label EFF validé",
      "Résiliation en 1 clic — confirmé test utilisateurs tiers",
      "Transparence totale algorithme recommandation publié",
    ],
    estimated_darkpattern_index: 0.98,
    last_updated: "2026-06-14",
  },
  {
    id: "DKP-008",
    name: "OpenDesign Foundation",
    country: "Pays-Bas",
    sector: "Design Éthique & Standards",
    composite_score: 9.05,
    deception_score: 8.0,
    coercion_score: 10.0,
    addiction_score: 11.0,
    exploitation_score: 7.0,
    risk_level: "faible",
    primary_pattern: "Nudge Opaque Décisionnel",
    key_signals: [
      "Référentiel design éthique publié open source — 50k adoptions",
      "Audit indépendant annuel — zéro dark pattern confirmé",
      "Formation équipes UX — code déontologique numérique signé",
    ],
    estimated_darkpattern_index: 0.91,
    last_updated: "2026-06-13",
  },
];

function getMockData() {
  const entities = MOCK_ENTITIES;
  const n = entities.length;
  const avgComposite =
    Math.round((entities.reduce((s, e) => s + e.composite_score, 0) / n) * 100) / 100;

  const riskDistribution: Record<string, number> = { critique: 0, élevé: 0, modéré: 0, faible: 0 };
  const patternDistribution: Record<string, number> = {};

  for (const e of entities) {
    riskDistribution[e.risk_level] = (riskDistribution[e.risk_level] || 0) + 1;
    patternDistribution[e.primary_pattern] = (patternDistribution[e.primary_pattern] || 0) + 1;
  }

  const sorted = [...entities].sort((a, b) => b.composite_score - a.composite_score);
  const topRiskEntities = sorted.slice(0, 3).map((e) => e.name);
  const criticalAlerts = entities
    .filter((e) => e.risk_level === "critique")
    .map((e) => `${e.name} (${e.country}) — composite ${e.composite_score}`);

  const summary = {
    total_entities: n,
    avg_composite: avgComposite,
    risk_distribution: riskDistribution,
    pattern_distribution: patternDistribution,
    top_risk_entities: topRiskEntities,
    critical_alerts: criticalAlerts,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "darkpattern",
    confidence_score: 0.89,
    data_sources: [
      "EU DSA Dark Patterns Registry",
      "Norwegian Consumer Authority Reports",
      "CNIL Consentement Numérique Database",
      "Princeton WebTAP Dark Patterns Corpus",
      "Deceptive Design Hall of Shame",
    ],
    entities,
    avg_estimated_darkpattern_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
  };

  return { entities, summary };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Dark Patterns Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/dark-patterns-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Dark Patterns Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Dark Patterns Agent"),
      { status: 502 }
    );
  }
}
