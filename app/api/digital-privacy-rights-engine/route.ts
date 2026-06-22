import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-privacy-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[digital-privacy-rights-engine] SWARM_API_URL not set — running in offline mode");

const MOCK = {
  agent: "Digital Privacy Rights Engine Agent",
  domain: "digital_privacy_rights",
  total_entities: 8,
  avg_composite: 62.86,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  entities: [
    {
      entity_id: "DPR-001",
      name: "Chine — SCS 1,4Mrd Personnes Notées, 700M Caméras IA & Surveillance Ouïghours Xinjiang Totale",
      country: "Chine",
      mass_surveillance_score: 99.0,
      facial_recognition_score: 99.0,
      data_rights_score: 97.0,
      encryption_restriction_score: 95.0,
      composite_score: 97.70,
      risk_level: "critique",
      estimated_digital_privacy_rights_index: 9.77,
      primary_pattern: "Système crédit social, reconnaissance faciale urbaine en temps réel, internement Ouïghours via IA",
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DPR-002",
      name: "Corée du Nord — Surveillance Totalitaire, Intranet Kwangmyong & Espionnage Citoyens Par Voisins",
      country: "Corée du Nord",
      mass_surveillance_score: 98.0,
      facial_recognition_score: 84.0,
      data_rights_score: 96.0,
      encryption_restriction_score: 97.0,
      composite_score: 93.80,
      risk_level: "critique",
      estimated_digital_privacy_rights_index: 9.38,
      primary_pattern: "Isolation digitale totale, intranet national, délateurs institutionnels, exécution pour contenu étranger",
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DPR-003",
      name: "Iran — FATA Cyber Police, Blocage VPN 99% & Surveillance IRIB Dissidents & Femmes Voilées",
      country: "Iran",
      mass_surveillance_score: 91.0,
      facial_recognition_score: 87.0,
      data_rights_score: 88.0,
      encryption_restriction_score: 86.0,
      composite_score: 88.25,
      risk_level: "critique",
      estimated_digital_privacy_rights_index: 8.82,
      primary_pattern: "Internet national isolé, arrestations VPN, reconnaissance faciale pour contrôle hijab depuis 2023",
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DPR-004",
      name: "Russie — Système SORM, Lois Yarovaya 2016 & RuNet Isolement Progressif Post-Invasion Ukraine",
      country: "Russie",
      mass_surveillance_score: 84.0,
      facial_recognition_score: 80.0,
      data_rights_score: 79.0,
      encryption_restriction_score: 77.0,
      composite_score: 80.35,
      risk_level: "critique",
      estimated_digital_privacy_rights_index: 8.04,
      primary_pattern: "SORM-3 interception obligatoire, filtrage DPI, arrestations VPN, blocage 300 000 sites",
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DPR-005",
      name: "USA — NSA PRISM & XKeyscore, Section 702 FISA, Clearview AI 30Mrd Photos & Absence Loi Fédérale",
      country: "États-Unis",
      mass_surveillance_score: 57.0,
      facial_recognition_score: 58.0,
      data_rights_score: 52.0,
      encryption_restriction_score: 53.0,
      composite_score: 55.20,
      risk_level: "élevé",
      estimated_digital_privacy_rights_index: 5.52,
      primary_pattern: "Surveillance NSA globale révélations Snowden, Clearview AI police, pas de loi fédérale vie privée",
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DPR-006",
      name: "Inde — NATGRID 11 Bases Données, Aadhaar Biométrie 1,3Mrd Forcé & Coupures Internet 100+/An",
      country: "Inde",
      mass_surveillance_score: 50.0,
      facial_recognition_score: 49.0,
      data_rights_score: 46.0,
      encryption_restriction_score: 46.0,
      composite_score: 47.95,
      risk_level: "élevé",
      estimated_digital_privacy_rights_index: 4.79,
      primary_pattern: "NATGRID interconnexion bases données, Aadhaar biométrie obligatoire, record coupures Internet mondial",
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DPR-007",
      name: "Union Européenne — RGPD Protecteur Mais DSA/DMA Tensions, Frontex Biométrie & Débat Chiffrement",
      country: "Union Européenne",
      mass_surveillance_score: 26.0,
      facial_recognition_score: 30.0,
      data_rights_score: 22.0,
      encryption_restriction_score: 35.0,
      composite_score: 27.80,
      risk_level: "modéré",
      estimated_digital_privacy_rights_index: 2.78,
      primary_pattern: "RGPD meilleur cadre mondial mais pressions Chat Control, Frontex biométrie migrants controversée",
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DPR-008",
      name: "Allemagne & Suisse — Protection Données Constitutionnelle, BVerfG Jurisprudence & Vie Privée Droit Fondamental",
      country: "Allemagne/Suisse",
      mass_surveillance_score: 11.0,
      facial_recognition_score: 13.0,
      data_rights_score: 10.0,
      encryption_restriction_score: 14.0,
      composite_score: 11.85,
      risk_level: "faible",
      estimated_digital_privacy_rights_index: 1.19,
      primary_pattern: "Mémoire Stasi intégrée loi, BVerfG arrêts fondateurs vie privée, chiffrement protégé constitutionnellement",
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  try {
    if (!UPSTREAM) throw new Error("offline");
    const res = await fetch(`${UPSTREAM}/api/digital-privacy-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(MOCK), { status: 200 }));
  }
}
