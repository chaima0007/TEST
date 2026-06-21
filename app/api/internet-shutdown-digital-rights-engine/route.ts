import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[internet-shutdown-digital-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

function getMockData() {
  return {
    engine: "internet-shutdown-digital-rights-engine",
    generated_at: new Date().toISOString(),
    data_sources: [
      "accessnow_keepiton_report_2023",
      "netblocks_internet_shutdowns_tracker",
      "freedom_house_freedom_net_2023",
      "article19_digital_expression_report",
    ],
    confidence_score: 0.87,
    avg_composite: 62.69,
    avg_estimated_internet_shutdown_digital_rights_index: 6.27,
    entities: [
      {
        id: "ISDR-001",
        name: "Myanmar/Coup État 2021 Blackout Total Internet",
        country: "Asie du Sud-Est",
        sector: "Coup Militaire Février 2021, Coupure Internet 77 Jours, Facebook Principal Media Coupé & 40+ Millions Privés Connectivité",
        internet_shutdown_frequency_severity_score: 96,
        social_media_platform_blocking_score: 94,
        vpn_encryption_criminalization_score: 88,
        digital_expression_persecution_score: 92,
        composite_score: 92.70,
        risk_level: "critique",
        primary_pattern: "coupure_internet_totale",
        key_signals: [
          "Coupure internet totale 77 jours post-coup",
          "Facebook et réseaux sociaux bloqués",
          "Criminalisation VPN et chiffrement",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 9.27,
      },
      {
        id: "ISDR-002",
        name: "Corée du Nord/Intranet Kwangmyong Isolement Total",
        country: "Asie du Nord-Est",
        sector: "Internet Mondial Accessible <0.1% Population, Intranet Étatique Contrôlé, VPN Peine De Mort & Totale Désinformation",
        internet_shutdown_frequency_severity_score: 99,
        social_media_platform_blocking_score: 99,
        vpn_encryption_criminalization_score: 99,
        digital_expression_persecution_score: 95,
        composite_score: 98.20,
        risk_level: "critique",
        primary_pattern: "criminalisation_vpn_chiffrement",
        key_signals: [
          "Intranet Kwangmyong totalement isolé",
          "VPN puni de peine de mort",
          "Désinformation totale population",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 9.82,
      },
      {
        id: "ISDR-003",
        name: "Iran/Mahsa Amini Coupure 2022 & Filtrage",
        country: "MENA",
        sector: "Coupure Internet Pendant Manifestations 2022, Instagram/WhatsApp Bloqués, VPN Criminalisés & 76 Millions Touchés",
        internet_shutdown_frequency_severity_score: 88,
        social_media_platform_blocking_score: 90,
        vpn_encryption_criminalization_score: 85,
        digital_expression_persecution_score: 86,
        composite_score: 87.35,
        risk_level: "critique",
        primary_pattern: "blocage_plateformes_reseaux_sociaux",
        key_signals: [
          "Coupure internet manifestations Mahsa Amini 2022",
          "Instagram et WhatsApp bloqués",
          "VPN criminalisés 76 millions touchés",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 8.74,
      },
      {
        id: "ISDR-004",
        name: "Éthiopie/Tigré 2020-2022 Zone de Guerre",
        country: "Afrique de l'Est",
        sector: "18 Mois Sans Internet Région Tigré, Blackout Pendant Conflit, Populations Coupées Aide Humanitaire & Journalistes Exclus",
        internet_shutdown_frequency_severity_score: 90,
        social_media_platform_blocking_score: 82,
        vpn_encryption_criminalization_score: 80,
        digital_expression_persecution_score: 88,
        composite_score: 85.10,
        risk_level: "critique",
        primary_pattern: "coupure_internet_totale",
        key_signals: [
          "18 mois sans internet région Tigré",
          "Populations coupées aide humanitaire",
          "Journalistes exclus de la zone",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 8.51,
      },
      {
        id: "ISDR-005",
        name: "Russie/Blocage Twitter VK Censuré Ukraine",
        country: "Europe de l'Est",
        sector: "Twitter/Facebook Bloqués Mars 2022, Loi Roskomnadzor, 200+ Sites Censurés, VPN Légaux Sous Pression & Propagande RuTube",
        internet_shutdown_frequency_severity_score: 45,
        social_media_platform_blocking_score: 65,
        vpn_encryption_criminalization_score: 48,
        digital_expression_persecution_score: 55,
        composite_score: 52.75,
        risk_level: "élevé",
        primary_pattern: "blocage_plateformes_reseaux_sociaux",
        key_signals: [
          "Twitter et Facebook bloqués mars 2022",
          "Loi Roskomnadzor 200+ sites censurés",
          "VPN légaux sous pression",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 5.28,
      },
      {
        id: "ISDR-006",
        name: "Inde/Cachemire 552 Jours Sans Internet",
        country: "Asie du Sud",
        sector: "552 Jours Coupure Cachemire 2019-2021, Monde Record, 4G Bloqué, 7M Habitants & Économie Locale Dévastée",
        internet_shutdown_frequency_severity_score: 78,
        social_media_platform_blocking_score: 55,
        vpn_encryption_criminalization_score: 42,
        digital_expression_persecution_score: 60,
        composite_score: 59.65,
        risk_level: "élevé",
        primary_pattern: "coupure_internet_totale",
        key_signals: [
          "552 jours coupure Cachemire record mondial",
          "4G bloqué 7 millions habitants",
          "Économie locale dévastée",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 5.97,
      },
      {
        id: "ISDR-007",
        name: "USA/Section 230 & Big Tech Modération",
        country: "Amérique du Nord",
        sector: "Section 230 Débat, Modération Contenu Big Tech, CLOUD Act Surveillance, Patriot Act & NSA Mass Surveillance Revelations",
        internet_shutdown_frequency_severity_score: 18,
        social_media_platform_blocking_score: 22,
        vpn_encryption_criminalization_score: 20,
        digital_expression_persecution_score: 35,
        composite_score: 22.90,
        risk_level: "modéré",
        primary_pattern: "persecution_expression_numerique",
        key_signals: [
          "Débat Section 230 modération Big Tech",
          "CLOUD Act et Patriot Act surveillance",
          "NSA mass surveillance révélations",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 2.29,
      },
      {
        id: "ISDR-008",
        name: "UE/GDPR & Digital Services Act Régulation",
        country: "Europe",
        sector: "GDPR 2018 Protection Données, DSA 2022 Modération Transparente, NIS2 Cybersécurité & Droits Numériques Renforcés",
        internet_shutdown_frequency_severity_score: 2,
        social_media_platform_blocking_score: 3,
        vpn_encryption_criminalization_score: 2,
        digital_expression_persecution_score: 5,
        composite_score: 2.85,
        risk_level: "faible",
        primary_pattern: "persecution_expression_numerique",
        key_signals: [
          "GDPR 2018 protection données renforcée",
          "DSA 2022 modération transparente",
          "NIS2 cybersécurité droits numériques",
        ],
        last_updated: "2024-01-15",
        estimated_internet_shutdown_digital_rights_index: 0.29,
      },
    ],
  };
}

const MOCK = getMockData();

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/internet-shutdown-digital-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
