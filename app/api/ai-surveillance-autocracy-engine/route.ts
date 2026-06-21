import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ai-surveillance-autocracy-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "AI Surveillance Autocracy Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ai-surveillance-autocracy-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "AI Surveillance Autocracy Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "AI Surveillance Autocracy Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "AS-001", name: "Chine — Grand Firewall & Exportation Surveillance 80 Pays", country: "Asie", sector: "600M Caméras, Crédit Social 1.4Md Personnes, Hikvision/Dahua Export & SenseTime Reconnaissance Faciale", composite_score: 91.5, social_credit_score: 95.0, biometric_mass_surveillance_score: 92.0, surveillance_export_score: 88.0, internet_shutdown_censorship_score: 90.0, risk_level: "critique", primary_pattern: "surveillance_totale_citoyens", key_signals: ["Surveillance totale par Chine — appareil de contrôle IA systémique ciblant comportements, déplacements et communications de la population", "IA au service de la répression — reconnaissance faciale en temps réel, NLP surveillance réseaux sociaux et scoring prédictif de la dissidence", "Exportation du modèle autoritaire — transfert technologique de surveillance à des régimes partenaires pour consolider les autocraties mondiales"], estimated_ai_surveillance_index: 9.15, last_updated: "2026-06-20" },
    { id: "AS-002", name: "Russie — SORM, RuNet & Surveillance Orwell Moscou", country: "Europe de l'Est", sector: "SORM-3 Accès FSB Sans Mandat, Réseau Orwell Moscou Métro, RuNet Isolation 2019 & SIZO Numérique", composite_score: 83.6, social_credit_score: 85.0, biometric_mass_surveillance_score: 82.0, surveillance_export_score: 80.0, internet_shutdown_censorship_score: 88.0, risk_level: "critique", primary_pattern: "isolation_numerique_etatique", key_signals: ["Surveillance totale par Russie — appareil de contrôle IA systémique ciblant comportements, déplacements et communications de la population", "IA au service de la répression — reconnaissance faciale en temps réel, NLP surveillance réseaux sociaux et scoring prédictif de la dissidence", "Exportation du modèle autoritaire — transfert technologique de surveillance à des régimes partenaires pour consolider les autocraties mondiales"], estimated_ai_surveillance_index: 8.36, last_updated: "2026-06-20" },
    { id: "AS-003", name: "Corée du Nord — Kwangmyong Intranet Total Isolation", country: "Asie", sector: "Kwangmyong Intranet 28 Sites, Surveillance Totale Électronique, Koryolink 5M Abonnés Contrôlés", composite_score: 82.35, social_credit_score: 92.0, biometric_mass_surveillance_score: 88.0, surveillance_export_score: 55.0, internet_shutdown_censorship_score: 95.0, risk_level: "critique", primary_pattern: "surveillance_totale_citoyens", key_signals: ["Surveillance totale par Corée du Nord — appareil de contrôle IA systémique ciblant comportements, déplacements et communications de la population", "IA au service de la répression — reconnaissance faciale en temps réel, NLP surveillance réseaux sociaux et scoring prédictif de la dissidence", "Exportation du modèle autoritaire — transfert technologique de surveillance à des régimes partenaires pour consolider les autocraties mondiales"], estimated_ai_surveillance_index: 8.24, last_updated: "2026-06-20" },
    { id: "AS-004", name: "Iran — Halal Internet & Surveillance IRGC Politique", country: "MENA", sector: "Filtrage 50%+ Sites Web, IRGC Cyber Army, Pegasus Iranien DARIS & Shutdown 2019/2022 Protestations", composite_score: 78.5, social_credit_score: 80.0, biometric_mass_surveillance_score: 78.0, surveillance_export_score: 72.0, internet_shutdown_censorship_score: 85.0, risk_level: "critique", primary_pattern: "isolation_numerique_etatique", key_signals: ["Surveillance totale par Iran — appareil de contrôle IA systémique ciblant comportements, déplacements et communications de la population", "IA au service de la répression — reconnaissance faciale en temps réel, NLP surveillance réseaux sociaux et scoring prédictif de la dissidence", "Exportation du modèle autoritaire — transfert technologique de surveillance à des régimes partenaires pour consolider les autocraties mondiales"], estimated_ai_surveillance_index: 7.85, last_updated: "2026-06-20" },
    { id: "AS-005", name: "EAU & Arabie Saoudite — NSO Pegasus & Smart City Panoptique", country: "MENA", sector: "Pegasus 50+ Pays Clients, NEOM Smart City Surveillance & Project Raven Ex-NSA Ciblage Opposants", composite_score: 56.85, social_credit_score: 55.0, biometric_mass_surveillance_score: 58.0, surveillance_export_score: 65.0, internet_shutdown_censorship_score: 48.0, risk_level: "élevé", primary_pattern: "autoritarisme_numerique_emergent", key_signals: ["Autoritarisme numérique de EAU & Arabie Saoudite — surveillance politique ciblée et censure structurelle sans surveillance totale généralisée", "Restriction progressive des libertés — censure des médias, fermeture des applications VPN et filtrage du contenu politique contestataire", "Répression numérique des opposants — ciblage des journalistes, militants et minorités via des outils de surveillance IA"], estimated_ai_surveillance_index: 5.69, last_updated: "2026-06-20" },
    { id: "AS-006", name: "Turquie & Azerbaïdjan — Surveillance Politique Ciblée", country: "MENA/Europe", sector: "Turquie 400K+ Poursuites Réseaux Sociaux, AZ Pegasus Opposition & Coupures Internet Électorales", composite_score: 50.9, social_credit_score: 48.0, biometric_mass_surveillance_score: 52.0, surveillance_export_score: 58.0, internet_shutdown_censorship_score: 45.0, risk_level: "élevé", primary_pattern: "autoritarisme_numerique_emergent", key_signals: ["Autoritarisme numérique de Turquie & Azerbaïdjan — surveillance politique ciblée et censure structurelle sans surveillance totale généralisée", "Restriction progressive des libertés — censure des médias, fermeture des applications VPN et filtrage du contenu politique contestataire", "Répression numérique des opposants — ciblage des journalistes, militants et minorités via des outils de surveillance IA"], estimated_ai_surveillance_index: 5.09, last_updated: "2026-06-20" },
    { id: "AS-007", name: "Inde — NATGRID & Surveillance Biométrique Aadhaar", country: "Asie du Sud", sector: "Aadhaar 1.4Md Biométries, NATGRID 21 Bases Données & Shutdown Cachemire 552 Jours Record Mondial", composite_score: 31.6, social_credit_score: 30.0, biometric_mass_surveillance_score: 32.0, surveillance_export_score: 28.0, internet_shutdown_censorship_score: 38.0, risk_level: "modéré", primary_pattern: "autoritarisme_numerique_emergent", key_signals: ["Dérive surveillance de Inde — expansion des capacités de surveillance sans contre-pouvoirs judiciaires ou législatifs adéquats", "Zone grise réglementaire — technologies de surveillance déployées sans cadre légal clair sur la proportionnalité et les droits", "Risque de glissement autoritaire — capacités techniques disponibles pour une répression si le contexte politique change"], estimated_ai_surveillance_index: 3.16, last_updated: "2026-06-20" },
    { id: "AS-008", name: "Suède & Islande — Protection Données RGPD+ Modèle", country: "Europe du Nord", sector: "RGPD Application Exemplaire, DPA Indépendants, Transparence Algorithmique & Internet Ouvert Garanti", composite_score: 3.65, social_credit_score: 5.0, biometric_mass_surveillance_score: 4.0, surveillance_export_score: 3.0, internet_shutdown_censorship_score: 2.0, risk_level: "faible", primary_pattern: "protection_libertes_numeriques", key_signals: ["Suède & Islande incarne la protection des libertés numériques — RGPD strict, supervision indépendante et limites légales à la surveillance", "Contre-pouvoirs institutionnels — autorités de protection des données dotées de pouvoirs réels et indépendantes du pouvoir politique", "Modèle de surveillance proportionnée à diffuser — surveillance ciblée sur décision judiciaire, transparence et droits de recours effectifs"], estimated_ai_surveillance_index: 0.37, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { surveillance_totale_citoyens: 2, isolation_numerique_etatique: 2, exportation_surveillance_autocratique: 0, autoritarisme_numerique_emergent: 3, protection_libertes_numeriques: 1 },
    top_risk_entities: ["Chine — Grand Firewall & Exportation Surveillance 80 Pays", "Russie — SORM, RuNet & Surveillance Orwell Moscou", "Corée du Nord — Kwangmyong Intranet Total Isolation"],
    critical_alerts: ["Chine: surveillance totale citoyens", "Russie: isolation numérique étatique", "Corée du Nord: surveillance totale citoyens", "Iran: isolation numérique étatique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "ai_surveillance_autocracy",
    confidence_score: 0.83,
    data_sources: ["freedom_house_freedom_net", "citizenlab_surveillance_tracker", "carnegie_ai_global_surveillance_index"],
    entities,
    avg_estimated_ai_surveillance_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
