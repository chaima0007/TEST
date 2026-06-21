import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[esg-greenwash-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "ESG Greenwash Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/esg-greenwash-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "ESG Greenwash Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "ESG Greenwash Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    {
      id: "GW-001",
      name: "EnergiVerde S.p.A.",
      country: "Italie",
      sector: "Énergie & Utilities",
      composite_score: 82.75,
      emissions_discrepancy_score: 92.0,
      certification_fraud_score: 85.0,
      reporting_opacity_score: 78.0,
      supply_chain_deception_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Fraude Carbone",
      key_signals: [
        "Émissions réelles CO2 supérieures de 340% aux déclarations officielles",
        "Certification ISO 14001 obtenue via un auditeur partenaire non indépendant",
        "Rapports durabilité excluant délibérément les émissions Scope 3",
      ],
      estimated_greenwash_index: 8.28,
      last_updated: "2026-06-20",
    },
    {
      id: "GW-002",
      name: "GreenFashion International",
      country: "Bangladesh",
      sector: "Mode & Textile",
      composite_score: 75.7,
      emissions_discrepancy_score: 82.0,
      certification_fraud_score: 76.0,
      reporting_opacity_score: 74.0,
      supply_chain_deception_score: 68.0,
      risk_level: "critique",
      primary_pattern: "Fraude Carbone",
      key_signals: [
        "Label 'coton bio' sur des produits issus de cultures conventionnelles vérifiées",
        "Usines sous-traitantes fonctionnant au charbon non mentionnées dans les rapports",
        "Programme de recyclage publicitaire sans infrastructure réelle de collecte",
      ],
      estimated_greenwash_index: 7.57,
      last_updated: "2026-06-20",
    },
    {
      id: "GW-003",
      name: "PetroGreen Holdings Ltd",
      country: "Royaume-Uni",
      sector: "Pétrole & Gaz",
      composite_score: 70.9,
      emissions_discrepancy_score: 78.0,
      certification_fraud_score: 70.0,
      reporting_opacity_score: 68.0,
      supply_chain_deception_score: 65.0,
      risk_level: "critique",
      primary_pattern: "Fraude Carbone",
      key_signals: [
        "Compensation carbone via des projets forestiers non vérifiables",
        "Objectifs net-zéro 2050 sans feuille de route intermédiaire publiée",
        "Marketing 'hydrogène vert' pour des installations fonctionnant au méthane",
      ],
      estimated_greenwash_index: 7.09,
      last_updated: "2026-06-20",
    },
    {
      id: "GW-004",
      name: "AgroSustain Corporation",
      country: "Brésil",
      sector: "Agroalimentaire",
      composite_score: 58.9,
      emissions_discrepancy_score: 58.0,
      certification_fraud_score: 62.0,
      reporting_opacity_score: 60.0,
      supply_chain_deception_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "Déception Chaîne d'Approvisionnement",
      key_signals: [
        "Certification Rainforest Alliance sur des parcelles non auditées",
        "Déforestation non déclarée dans les zones d'approvisionnement soja",
        "Indicateurs biodiversité auto-déclarés sans vérification indépendante",
      ],
      estimated_greenwash_index: 5.89,
      last_updated: "2026-06-20",
    },
    {
      id: "GW-005",
      name: "AutoEco Mobility Group",
      country: "Allemagne",
      sector: "Automobile",
      composite_score: 53.7,
      emissions_discrepancy_score: 52.0,
      certification_fraud_score: 56.0,
      reporting_opacity_score: 58.0,
      supply_chain_deception_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "Communication Trompeuse",
      key_signals: [
        "Tests d'émissions en conditions réelles supérieurs aux homologations de 45%",
        "Batterie EV sourçant du lithium de mines sans standard social vérifié",
        "Rapport ESG 2025 ne mentionnant pas les contentieux réglementaires en cours",
      ],
      estimated_greenwash_index: 5.37,
      last_updated: "2026-06-20",
    },
    {
      id: "GW-006",
      name: "BioPack Solutions SA",
      country: "France",
      sector: "Emballage & Chimie",
      composite_score: 29.1,
      emissions_discrepancy_score: 32.0,
      certification_fraud_score: 28.0,
      reporting_opacity_score: 30.0,
      supply_chain_deception_score: 25.0,
      risk_level: "modéré",
      primary_pattern: "Aucun",
      key_signals: [
        "Emballages 'biodégradables' nécessitant des conditions industrielles spécifiques",
        "Taux de recyclabilité réelle inférieur de 20pts aux allégations marketing",
        "Ambiguïtés dans la définition des matériaux recyclés utilisés",
      ],
      estimated_greenwash_index: 2.91,
      last_updated: "2026-06-20",
    },
    {
      id: "GW-007",
      name: "Interface Inc. Europe",
      country: "Pays-Bas",
      sector: "Matériaux & Construction",
      composite_score: 9.7,
      emissions_discrepancy_score: 8.0,
      certification_fraud_score: 10.0,
      reporting_opacity_score: 12.0,
      supply_chain_deception_score: 9.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Rapport GRI Standards complet avec vérification tierce indépendante",
        "Chaîne d'approvisionnement 100% traçable avec données publiques",
        "Objectifs Science Based Targets validés et révisés annuellement",
      ],
      estimated_greenwash_index: 0.97,
      last_updated: "2026-06-20",
    },
    {
      id: "GW-008",
      name: "Patagonia EMEA",
      country: "Suisse",
      sector: "Mode & Textile",
      composite_score: 10.9,
      emissions_discrepancy_score: 12.0,
      certification_fraud_score: 8.0,
      reporting_opacity_score: 10.0,
      supply_chain_deception_score: 14.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Transparence totale sur les fournisseurs avec audits sociaux publiés",
        "Engagement de réparation et revente documenté avec données de volume",
        "Empreinte carbone par produit publiée avec méthodologie détaillée",
      ],
      estimated_greenwash_index: 1.09,
      last_updated: "2026-06-20",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 48.96,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Fraude Carbone": 3,
      "Certification Fictive": 2,
      "Opacité des Rapports": 3,
      "Déception Chaîne d'Approvisionnement": 3,
      "Communication Trompeuse": 5,
    },
    top_risk_entities: [
      "EnergiVerde S.p.A.",
      "GreenFashion International",
      "PetroGreen Holdings Ltd",
    ],
    critical_alerts: [
      "ALERTE CRITIQUE: EnergiVerde S.p.A. (Italie) — score greenwash 82.75/100",
      "ALERTE CRITIQUE: GreenFashion International (Bangladesh) — score greenwash 75.70/100",
      "ALERTE CRITIQUE: PetroGreen Holdings Ltd (Royaume-Uni) — score greenwash 70.90/100",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "greenwash",
    confidence_score: 89.0,
    data_sources: [
      "CSRD Non-Financial Reporting Database EU",
      "CDP Carbon Disclosure Project",
      "InfluenceMap Corporate Climate Accountability",
      "Ecovadis ESG Rating Reports",
    ],
    entities,
    avg_estimated_greenwash_index: 4.9,
  };

  return { entities, summary };
}
