import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[tax-justice-engine] SWARM_API_URL non défini — mode mock activé");
}

// ── mock entity type ─────────────────────────────────────────────────────────
// composite = evasion*0.30 + avoidance*0.25 + offshore*0.25 + inequality*0.20
//
// TAX-001  88*0.30 + 82*0.25 + 90*0.25 + 75*0.20 = 84.40  → critique
// TAX-002  72*0.30 + 85*0.25 + 78*0.25 + 68*0.20 = 75.95  → critique
// TAX-003  80*0.30 + 76*0.25 + 82*0.25 + 65*0.20 = 76.50  → critique
// TAX-004  55*0.30 + 60*0.25 + 52*0.25 + 45*0.20 = 53.50  → élevé
// TAX-005  58*0.30 + 62*0.25 + 55*0.25 + 42*0.20 = 55.05  → élevé
// TAX-006  28*0.30 + 32*0.25 + 25*0.25 + 38*0.20 = 30.25  → modéré
// TAX-007   8*0.30 + 12*0.25 +  6*0.25 + 10*0.20 =  8.90  → faible
// TAX-008   5*0.30 +  8*0.25 +  4*0.25 +  7*0.20 =  5.90  → faible

function computeRiskLevel(composite: number): string {
  if (composite >= 60) return "critique";
  if (composite >= 40) return "élevé";
  if (composite >= 20) return "modéré";
  return "faible";
}

function computeRecommendedAction(riskLevel: string): string {
  if (riskLevel === "critique") return "signalement_autorités_fiscales_enquête_internationale";
  if (riskLevel === "élevé") return "audit_conformité_fiscale_renforcé";
  if (riskLevel === "modéré") return "révision_politique_fiscale_équité";
  return "veille_réputation_fiscale_standard";
}

const mockEntities = [
  {
    entity_id:                    "TAX-001",
    name:                         "MegaCorp Cayman Holdings",
    country:                      "Cayman Islands",
    sector:                       "Finance",
    composite_score:              84.40,
    evasion_score:                88.0,
    avoidance_score:              82.0,
    offshore_score:               90.0,
    inequality_score:             75.0,
    risk_level:                   "critique",
    primary_pattern:              "Évasion Fiscale Systémique",
    key_signals: [
      "Transferts massifs vers paradis fiscal (Cayman Islands)",
      "Absence totale de substance économique locale",
      "Montages price-transfer vers filiales offshore",
    ],
    estimated_tax_justice_index:  8.44,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("critique"),
  },
  {
    entity_id:                    "TAX-002",
    name:                         "TechGiant Ireland LLC",
    country:                      "Ireland",
    sector:                       "Technology",
    composite_score:              75.95,
    evasion_score:                72.0,
    avoidance_score:              85.0,
    offshore_score:               78.0,
    inequality_score:             68.0,
    risk_level:                   "critique",
    primary_pattern:              "Optimisation Abusive Offshore",
    key_signals: [
      "Double Irish — structure hybride IP routing",
      "Taux effectif impôts < 2% sur bénéfices mondiaux",
      "Royalties IP transférées vers Bermudes sans activité réelle",
    ],
    estimated_tax_justice_index:  7.60,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("critique"),
  },
  {
    entity_id:                    "TAX-003",
    name:                         "LuxHolding SA",
    country:                      "Luxembourg",
    sector:                       "Real Estate",
    composite_score:              76.50,
    evasion_score:                80.0,
    avoidance_score:              76.0,
    offshore_score:               82.0,
    inequality_score:             65.0,
    risk_level:                   "critique",
    primary_pattern:              "Évasion Fiscale Systémique",
    key_signals: [
      "Rulings fiscaux secrets avec administration luxembourgeoise",
      "Structures holding opaques multi-couches",
      "Concentration immobilière sans imposition locale",
    ],
    estimated_tax_justice_index:  7.65,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("critique"),
  },
  {
    entity_id:                    "TAX-004",
    name:                         "ShellCompany BV",
    country:                      "Netherlands",
    sector:                       "Consulting",
    composite_score:              53.50,
    evasion_score:                55.0,
    avoidance_score:              60.0,
    offshore_score:               52.0,
    inequality_score:             45.0,
    risk_level:                   "élevé",
    primary_pattern:              "Contournement Réglementaire",
    key_signals: [
      "Utilisation des treaty networks néerlandais pour minimisation fiscale",
      "Facturation intergroupe avec marges artificielles",
      "Boite aux lettres — 0 employés effectifs déclarés",
    ],
    estimated_tax_justice_index:  5.35,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("élevé"),
  },
  {
    entity_id:                    "TAX-005",
    name:                         "PharmaOffset AG",
    country:                      "Switzerland",
    sector:                       "Pharmaceuticals",
    composite_score:              55.05,
    evasion_score:                58.0,
    avoidance_score:              62.0,
    offshore_score:               55.0,
    inequality_score:             42.0,
    risk_level:                   "élevé",
    primary_pattern:              "Optimisation Abusive Offshore",
    key_signals: [
      "Propriété intellectuelle pharmaceutique délocalisée en Suisse",
      "Transfer pricing agressif sur brevets médicaux",
      "Taux effectif 5% malgré marges opérationnelles >40%",
    ],
    estimated_tax_justice_index:  5.51,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("élevé"),
  },
  {
    entity_id:                    "TAX-006",
    name:                         "RetailGroup SARL",
    country:                      "France",
    sector:                       "Retail",
    composite_score:              30.25,
    evasion_score:                28.0,
    avoidance_score:              32.0,
    offshore_score:               25.0,
    inequality_score:             38.0,
    risk_level:                   "modéré",
    primary_pattern:              "Inégalité Fiscale Structurelle",
    key_signals: [
      "Crédit d'impôt recherche utilisé de manière abusive",
      "Taux d'imposition effectif inférieur à PME concurrentes",
      "Optimisation TVA sur e-commerce transfrontalier",
    ],
    estimated_tax_justice_index:  3.03,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("modéré"),
  },
  {
    entity_id:                    "TAX-007",
    name:                         "Nordic Fair AS",
    country:                      "Denmark",
    sector:                       "Renewable Energy",
    composite_score:              8.90,
    evasion_score:                8.0,
    avoidance_score:              12.0,
    offshore_score:               6.0,
    inequality_score:             10.0,
    risk_level:                   "faible",
    primary_pattern:              "Risque Réputation Fiscale",
    key_signals: [
      "Transparence fiscale conforme aux standards CbCR OCDE",
      "Taux effectif d'imposition aligné sur taux légal danois",
      "Aucune entité dans paradis fiscaux identifiés",
    ],
    estimated_tax_justice_index:  0.89,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("faible"),
  },
  {
    entity_id:                    "TAX-008",
    name:                         "Transparent Corp",
    country:                      "Germany",
    sector:                       "Manufacturing",
    composite_score:              5.90,
    evasion_score:                5.0,
    avoidance_score:              8.0,
    offshore_score:               4.0,
    inequality_score:             7.0,
    risk_level:                   "faible",
    primary_pattern:              "Risque Réputation Fiscale",
    key_signals: [
      "Rapports fiscaux publiés volontairement selon GRI 207",
      "Coopération complète avec les autorités fiscales allemandes",
      "Contribution fiscale totale représente 28% du résultat brut",
    ],
    estimated_tax_justice_index:  0.59,
    last_updated:                 "2026-06-20",
    recommended_action:           computeRecommendedAction("faible"),
  },
];

function getMockData(): Record<string, unknown> {
  const risk_distribution: Record<string, number>    = {};
  const pattern_distribution: Record<string, number> = {};
  let total_composite = 0;
  const critical_alerts: string[]  = [];
  const top_risk_entities: string[] = [];

  for (const e of mockEntities) {
    risk_distribution[e.risk_level]         = (risk_distribution[e.risk_level] || 0) + 1;
    pattern_distribution[e.primary_pattern] = (pattern_distribution[e.primary_pattern] || 0) + 1;
    total_composite += e.composite_score;
    if (e.risk_level === "critique") {
      critical_alerts.push(e.name);
      top_risk_entities.push(e.name);
    }
  }

  const n             = mockEntities.length;
  const avg_composite = Math.round((total_composite / n) * 100) / 100;

  return {
    total_entities:                   n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis:                    "2026-06-20",
    engine_version:                   "1.0.0",
    domain:                           "tax_justice",
    confidence_score:                 0.89,
    data_sources:                     ["OCDE CbCR", "Tax Justice Network", "OpenCorporates", "ICIJ Offshore Leaks"],
    entities:                         mockEntities,
    avg_estimated_tax_justice_index:  Math.round((avg_composite / 100 * 10) * 100) / 100,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Tax Justice Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/tax-justice-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Tax Justice Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Tax Justice Agent"),
      { status: 502 },
    );
  }
}
