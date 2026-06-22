import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[transhumanist-ethics-engine] SWARM_API_URL non défini — mode mock activé");
}

// ── Types ──────────────────────────────────────────────────────────────────────

interface EntityDict {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  enhancement_score: number;
  consent_score: number;
  equity_score: number;
  governance_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_transhumanist_index: number;
  last_updated: string;
  recommended_action: string;
}

interface MockData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: EntityDict[];
  avg_estimated_transhumanist_index: number;
}

// ── Mock entities (scores mirror transhumanist_ethics_engine.py exactly) ───────
//
// composite = enhancement*0.30 + consent*0.25 + equity*0.25 + governance*0.20
//
// TRH-001: 85*0.30+70*0.25+75*0.25+72*0.20 = 25.5+17.5+18.75+14.4  = 76.15 → critique
// TRH-002: 78*0.30+65*0.25+70*0.25+68*0.20 = 23.4+16.25+17.5+13.6  = 70.75 → critique
// TRH-003: 72*0.30+60*0.25+65*0.25+62*0.20 = 21.6+15+16.25+12.4    = 65.25 → critique
// TRH-004: 55*0.30+45*0.25+48*0.25+50*0.20 = 16.5+11.25+12+10      = 49.75 → élevé
// TRH-005: 52*0.30+42*0.25+44*0.25+46*0.20 = 15.6+10.5+11+9.2      = 46.3  → élevé
// TRH-006: 35*0.30+28*0.25+30*0.25+32*0.20 = 10.5+7+7.5+6.4        = 31.4  → modéré
// TRH-007: 15*0.30+12*0.25+14*0.25+16*0.20 = 4.5+3+3.5+3.2         = 14.2  → faible
// TRH-008: 10*0.30+8*0.25+9*0.25+11*0.20   = 3+2+2.25+2.2          = 9.45  → faible
// avg_composite = (76.15+70.75+65.25+49.75+46.3+31.4+14.2+9.45)/8   = 363.25/8 = 45.41
// avg_estimated_transhumanist_index = round(45.41/100*10, 2)         = 4.54

const MOCK_ENTITIES: EntityDict[] = [
  {
    id: "TRH-001",
    name: "NeuralLink Corp",
    country: "USA",
    sector: "Neurotechnology",
    enhancement_score: 85,
    consent_score: 70,
    equity_score: 75,
    governance_score: 72,
    composite_score: 76.15,
    risk_level: "critique",
    primary_pattern: "Augmentation Non Consentie",
    key_signals: [
      "Expérimentations sans consentement éclairé détectées sur implants neuronaux",
      "Protocoles de consentement contournés lors des essais cliniques phase III",
      "Pression institutionnelle documentée sur les participants vulnérables",
    ],
    estimated_transhumanist_index: 7.62,
    recommended_action: "suspension_programme_augmentation_audit_indépendant",
    last_updated: new Date().toISOString(),
  },
  {
    id: "TRH-002",
    name: "GenEdit Therapeutics",
    country: "Chine",
    sector: "Biotechnology",
    enhancement_score: 78,
    consent_score: 65,
    equity_score: 70,
    governance_score: 68,
    composite_score: 70.75,
    risk_level: "critique",
    primary_pattern: "Dérive Eugéniste",
    key_signals: [
      "Modification génétique embryonnaire à visée de sélection phénotypique détectée",
      "Absence de supervision éthique indépendante pour les essais d'édition génomique",
      "Critères de sélection génétique alignés sur des préférences socio-culturelles dominantes",
    ],
    estimated_transhumanist_index: 7.08,
    recommended_action: "suspension_programme_augmentation_audit_indépendant",
    last_updated: new Date().toISOString(),
  },
  {
    id: "TRH-003",
    name: "BioEnhance Labs",
    country: "Émirats Arabes Unis",
    sector: "Biotechnology",
    enhancement_score: 72,
    consent_score: 60,
    equity_score: 65,
    governance_score: 62,
    composite_score: 65.25,
    risk_level: "critique",
    primary_pattern: "Inégalité d'Accès Transhumaniste",
    key_signals: [
      "Accès aux augmentations réservé aux populations fortunées — coût prohibitif",
      "Absence de programme public d'équité pour les thérapies d'amélioration cognitive",
      "Stratification sociale amplifiée par les technologies d'augmentation biologique",
    ],
    estimated_transhumanist_index: 6.53,
    recommended_action: "suspension_programme_augmentation_audit_indépendant",
    last_updated: new Date().toISOString(),
  },
  {
    id: "TRH-004",
    name: "CyberAugment Inc",
    country: "Japon",
    sector: "Cybernetics",
    enhancement_score: 55,
    consent_score: 45,
    equity_score: 48,
    governance_score: 50,
    composite_score: 49.75,
    risk_level: "élevé",
    primary_pattern: "Vide Réglementaire Critique",
    key_signals: [
      "Implants cybernétiques commercialisés sans cadre réglementaire de sécurité validé",
      "Lacunes juridiques exploitées pour contourner les obligations de traçabilité",
      "Absence de normes internationales appliquées pour les prothèses cognitives",
    ],
    estimated_transhumanist_index: 4.98,
    recommended_action: "engagement_urgent_régulateurs_cadre_juridique",
    last_updated: new Date().toISOString(),
  },
  {
    id: "TRH-005",
    name: "LifeExtension Pharma",
    country: "Russie",
    sector: "Pharmaceuticals",
    enhancement_score: 52,
    consent_score: 42,
    equity_score: 44,
    governance_score: 46,
    composite_score: 46.3,
    risk_level: "élevé",
    primary_pattern: "Vide Réglementaire Critique",
    key_signals: [
      "Protocoles de longévité administrés hors essais cliniques réglementés",
      "Commercialisation de thérapies anti-âge sans autorisation de mise sur le marché",
      "Supervision étatique insuffisante des programmes d'extension de vie expérimentaux",
    ],
    estimated_transhumanist_index: 4.63,
    recommended_action: "engagement_urgent_régulateurs_cadre_juridique",
    last_updated: new Date().toISOString(),
  },
  {
    id: "TRH-006",
    name: "EthicsFirst Biotech",
    country: "Allemagne",
    sector: "Biotechnology",
    enhancement_score: 35,
    consent_score: 28,
    equity_score: 30,
    governance_score: 32,
    composite_score: 31.4,
    risk_level: "modéré",
    primary_pattern: "Risque Éthique Émergent",
    key_signals: [
      "Indicateurs d'impact éthique en progression sur les programmes d'augmentation cognitive légère",
      "Consultations des comités d'éthique insuffisamment documentées pour certains essais",
      "Risque résiduel d'inégalité d'accès malgré les engagements d'équité affichés",
    ],
    estimated_transhumanist_index: 3.14,
    recommended_action: "veille_éthique_consultation_comités_spécialisés",
    last_updated: new Date().toISOString(),
  },
  {
    id: "TRH-007",
    name: "NordicBioEthics AS",
    country: "Norvège",
    sector: "Research",
    enhancement_score: 15,
    consent_score: 12,
    equity_score: 14,
    governance_score: 16,
    composite_score: 14.2,
    risk_level: "faible",
    primary_pattern: "Risque Éthique Émergent",
    key_signals: [
      "Protocoles de consentement rigoureux appliqués sur l'ensemble des recherches en augmentation",
      "Collaboration active avec les régulateurs pour l'élaboration de normes transhumanistes",
      "Programmes d'accès inclusif mis en place pour les populations défavorisées",
    ],
    estimated_transhumanist_index: 1.42,
    recommended_action: "veille_éthique_consultation_comités_spécialisés",
    last_updated: new Date().toISOString(),
  },
  {
    id: "TRH-008",
    name: "HumaneCyborg EU",
    country: "Suisse",
    sector: "Ethics Research",
    enhancement_score: 10,
    consent_score: 8,
    equity_score: 9,
    governance_score: 11,
    composite_score: 9.45,
    risk_level: "faible",
    primary_pattern: "Risque Éthique Émergent",
    key_signals: [
      "Cadre éthique exemplaire intégrant consentement, équité et gouvernance participative",
      "Recherche fondamentale sur les droits des cyborgs et la dignité humaine augmentée",
      "Transparence totale sur les objectifs et méthodes des programmes de recherche",
    ],
    estimated_transhumanist_index: 0.95,
    recommended_action: "veille_éthique_consultation_comités_spécialisés",
    last_updated: new Date().toISOString(),
  },
];

function getMockData(): MockData {
  return {
    total_entities: 8,
    avg_composite: 45.41,
    risk_distribution: {
      critique: 3,
      élevé: 2,
      modéré: 1,
      faible: 2,
    },
    pattern_distribution: {
      "Augmentation Non Consentie": 1,
      "Dérive Eugéniste": 1,
      "Inégalité d'Accès Transhumaniste": 1,
      "Vide Réglementaire Critique": 2,
      "Risque Éthique Émergent": 3,
    },
    top_risk_entities: [
      "NeuralLink Corp",
      "GenEdit Therapeutics",
      "BioEnhance Labs",
    ],
    critical_alerts: [
      "NeuralLink Corp",
      "GenEdit Therapeutics",
      "BioEnhance Labs",
    ],
    last_analysis: new Date().toISOString(),
    engine_version: "1.0.0",
    domain: "transhumanist",
    confidence_score: 0.87,
    data_sources: [
      "WHO Global Ethics Observatory",
      "UNESCO Bioethics Programme",
      "European Group on Ethics in Science and New Technologies (EGE)",
      "Hastings Center Bioethics Reports",
      "Journal of Medical Ethics — Transhumanist Studies",
      "Nuffield Council on Bioethics",
      "Global Observatory on Genome Editing",
      "International Neuroethics Society (INS)",
    ],
    entities: MOCK_ENTITIES,
    avg_estimated_transhumanist_index: 4.54,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Transhumanist Ethics Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/transhumanist-ethics-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Transhumanist Ethics Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Transhumanist Ethics Agent"), { status: 502 }));
  }
}
