import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[transnational-crime-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Transnational Crime Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/transnational-crime-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Transnational Crime Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Transnational Crime Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "TC-001", name: "Mexique — CJNG/Sinaloa & Capture Étatique Narco", country: "Amérique du Nord", sector: "CJNG 35 Pays Export Fentanyl, Sinaloa 4 Continents & 30% Territoire sous Contrôle Cartel Effectif", composite_score: 87.1, narco_state_capture_score: 92.0, money_laundering_score: 88.0, human_trafficking_network_score: 82.0, criminal_governance_score: 85.0, risk_level: "critique", primary_pattern: "capture_etatique_criminelle", key_signals: ["Capture étatique criminelle de Mexique — CJNG et Sinaloa ont infiltré les institutions, contrôlent 30% du territoire et opèrent une économie parallèle supérieure aux revenus fiscaux", "Narco-État ou État mafieux — complicité institutionnelle systémique entre élites politiques et réseaux criminels transnationaux", "Déstabilisation régionale — les capacités financières et militaires des cartels dépassent celles de l'État dans certaines zones"], estimated_transnational_crime_index: 8.71, last_updated: "2026-06-20" },
    { id: "TC-002", name: "Myanmar — Scam Compounds & Traite 100K Travailleurs Forcés", country: "Asie du Sud-Est", sector: "KK Park/Myawaddy 100K+ Travailleurs Forcés, 64Md$ Fraude Annuelle & Junte Complice Recrutement", composite_score: 84.1, narco_state_capture_score: 85.0, money_laundering_score: 82.0, human_trafficking_network_score: 90.0, criminal_governance_score: 78.0, risk_level: "critique", primary_pattern: "traite_humaine_industrielle", key_signals: ["Capture étatique criminelle de Myanmar — la junte militaire a institutionnalisé la traite humaine via les Scam Compounds générant 64Md$ de fraudes annuelles", "Narco-État ou État mafieux — complicité institutionnelle systémique entre élites politiques et réseaux criminels transnationaux", "Déstabilisation régionale — les capacités financières et militaires des cartels dépassent celles de l'État dans certaines zones"], estimated_transnational_crime_index: 8.41, last_updated: "2026-06-20" },
    { id: "TC-003", name: "Venezuela & RDC — Narco-État & Minerais Illicites", country: "Amérique du Sud/Afrique", sector: "Maduro FARC TREN DE ARAGUA, RDC FDLR/M23 Coltan & Gold Mining Milices Sans Poursuite", composite_score: 81.65, narco_state_capture_score: 88.0, money_laundering_score: 85.0, human_trafficking_network_score: 72.0, criminal_governance_score: 80.0, risk_level: "critique", primary_pattern: "capture_etatique_criminelle", key_signals: ["Capture étatique criminelle de Venezuela & RDC — régimes de Maduro et milices congolaises ont transformé leurs territoires en plateformes criminelles mondiales", "Narco-État ou État mafieux — complicité institutionnelle systémique entre élites politiques et réseaux criminels transnationaux", "Déstabilisation régionale — les capacités financières et militaires des cartels dépassent celles de l'État dans certaines zones"], estimated_transnational_crime_index: 8.17, last_updated: "2026-06-20" },
    { id: "TC-004", name: "Albanie & Balkans — Ndrangheta & Cocaïne Europe", country: "Europe du Sud-Est", sector: "Ndrangheta 80% Cocaïne Europe 37Md$, Clans Albanais Dubaï/Duisbourg & Clandestins Via Balkans", composite_score: 79.9, narco_state_capture_score: 80.0, money_laundering_score: 88.0, human_trafficking_network_score: 78.0, criminal_governance_score: 72.0, risk_level: "critique", primary_pattern: "blanchiment_systematique", key_signals: ["Capture étatique criminelle de Albanie & Balkans — la Ndrangheta calabraise contrôle 80% du marché européen de la cocaïne via des réseaux balkano-albanais", "Narco-État ou État mafieux — complicité institutionnelle systémique entre élites politiques et réseaux criminels transnationaux", "Déstabilisation régionale — les capacités financières et militaires des cartels dépassent celles de l'État dans certaines zones"], estimated_transnational_crime_index: 7.99, last_updated: "2026-06-20" },
    { id: "TC-005", name: "Nigéria — Yahoo Boys & Fraude BEC 10Md$ Mondial", country: "Afrique de l'Ouest", sector: "BEC Business Email Compromise 10Md$/An, Romance Scam Diaspora & Pig Butchering Crypto Nigérian", composite_score: 54.4, narco_state_capture_score: 55.0, money_laundering_score: 62.0, human_trafficking_network_score: 48.0, criminal_governance_score: 52.0, risk_level: "élevé", primary_pattern: "criminalite_transnationale_active", key_signals: ["Criminalité transnationale active de Nigéria — les Yahoo Boys ont industrialisé la fraude numérique à l'échelle mondiale avec 10Md$/an de pertes pour les victimes", "Corridors criminels prospères — trafic de drogues, d'armes et d'êtres humains transitant sans entrave par le territoire", "Blanchiment facilité — secteur bancaire ou immobilier utilisé pour recycler les produits du crime organisé"], estimated_transnational_crime_index: 5.44, last_updated: "2026-06-20" },
    { id: "TC-006", name: "Maroc & Turquie — Transit Hash & Héroïne Europe", country: "MENA/Europe", sector: "Maroc 70% Cannabis Européen, Turquie Route Balkanique Héroïne Afghane & Blanchiment Istanbul", composite_score: 53.45, narco_state_capture_score: 52.0, money_laundering_score: 55.0, human_trafficking_network_score: 58.0, criminal_governance_score: 48.0, risk_level: "élevé", primary_pattern: "criminalite_transnationale_active", key_signals: ["Criminalité transnationale active de Maroc & Turquie — corridors de transit du cannabis marocain et de l'héroïne afghane vers les marchés européens", "Corridors criminels prospères — trafic de drogues, d'armes et d'êtres humains transitant sans entrave par le territoire", "Blanchiment facilité — secteur bancaire ou immobilier utilisé pour recycler les produits du crime organisé"], estimated_transnational_crime_index: 5.35, last_updated: "2026-06-20" },
    { id: "TC-007", name: "Libye & Sahel — Corridors Migrants & Crime Organisé", country: "Afrique du Nord", sector: "Libye Hub Migration Irrégulière, Sahel Corridors Cocaïne/Or & Djihadisme-Crime Nexus GSIM", composite_score: 32.5, narco_state_capture_score: 30.0, money_laundering_score: 28.0, human_trafficking_network_score: 38.0, criminal_governance_score: 35.0, risk_level: "modéré", primary_pattern: "criminalite_transnationale_active", key_signals: ["Corridors criminels de Libye & Sahel — transit de flux illicites sans contrôle effectif mais sans capture étatique établie", "Vulnérabilités institutionnelles — corruption localisée et déficits de gouvernance exploités par les réseaux criminels", "Risque d'aggravation — conditions économiques et sécuritaires favorisant l'implantation d'organisations criminelles"], estimated_transnational_crime_index: 3.25, last_updated: "2026-06-20" },
    { id: "TC-008", name: "INTERPOL & ONUDC — Coopération Judiciaire Mondiale", country: "Global", sector: "INTERPOL 196 Membres, ONUDC Conventions Palerme/Vienne & FATF Standards AML/CFT", composite_score: 4.45, narco_state_capture_score: 5.0, money_laundering_score: 4.0, human_trafficking_network_score: 3.0, criminal_governance_score: 6.0, risk_level: "faible", primary_pattern: "cooperation_judiciaire_exemplaire", key_signals: ["INTERPOL & ONUDC incarne la coopération judiciaire exemplaire — INTERPOL efficace, entraide pénale active et conformité FATF", "Lutte anti-blanchiment rigoureuse — registres des bénéficiaires effectifs et coopération financière internationale sur les avoirs criminels", "Modèle de justice transnationale à exporter — formation des procureurs, protection des témoins et confiscation systématique des avoirs illicites"], estimated_transnational_crime_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { capture_etatique_criminelle: 2, traite_humaine_industrielle: 1, blanchiment_systematique: 1, criminalite_transnationale_active: 3, cooperation_judiciaire_exemplaire: 1 },
    top_risk_entities: ["Mexique — CJNG/Sinaloa & Capture Étatique Narco", "Myanmar — Scam Compounds & Traite 100K Travailleurs Forcés", "Venezuela & RDC — Narco-État & Minerais Illicites"],
    critical_alerts: ["Mexique: capture étatique criminelle", "Myanmar: traite humaine industrielle", "Venezuela & RDC: capture étatique criminelle", "Albanie & Balkans: blanchiment systématique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "transnational_crime",
    confidence_score: 0.82,
    data_sources: ["unodc_world_drug_report", "global_initiative_organized_crime", "fatf_money_laundering_monitor"],
    entities,
    avg_estimated_transnational_crime_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
