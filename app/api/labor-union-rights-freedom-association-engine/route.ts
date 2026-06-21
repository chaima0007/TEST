import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[labor-union-rights-freedom-association-engine] SWARM_API_URL is not set — falling back to mock data");
}

function getMockData() {
  return {
    agent: "Labor Union Rights Freedom Association Engine Agent",
    domain: "labor_union_rights_freedom_association",
    total_entities: 8,
    avg_composite: 59.07,
    confidence_score: 0.88,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { repression_syndicale_violente: 4, persecution_organisateurs_syndicaux: 1, interdiction_negociation_collective: 2, criminalisation_droit_greve: 1 },
    top_risk_entities: [
      "Chine/ACFTU Syndicats Contrôlés Parti — Grèves Illégales Réprimées Force, Négociation Collective Façade, Organisateurs Indépendants Arrêtés & Aucun Syndicat Autonome Toléré",
      "Égypte/Syndicats Indépendants Interdits — Arrestations Activistes Travail, Loi 2017 Dissolution Forcée Syndicats Autonomes, Grèves Poursuivies Pénalement & Sécurité État Surveillance",
      "Guatemala/Maquila — Assassinats Syndicalistes Impunité 95%, Travailleurs Listes Noires Secteur Textile, Licenciements Anti-Syndicaux Normalité & État Complice Violence Patronale",
    ],
    critical_alerts: [
      "Chine/ACFTU: repression_syndicale_violente",
      "Égypte/Syndicats Indépendants Interdits: interdiction_negociation_collective",
      "Guatemala/Maquila: persecution_organisateurs_syndicaux",
      "Bangladesh/Garment Secteur: repression_syndicale_violente",
    ],
    last_analysis: "2026-06-21",
    engine_version: "1.0.0",
    avg_estimated_labor_union_rights_freedom_association_index: 5.91,
    data_sources: [
      "ituc_global_rights_index_2023",
      "ilo_freedom_association_reports_2023",
      "frontline_defenders_labor_rights_2023",
      "solidarity_center_union_repression_database",
    ],
    entities: [
      { id: "LURFA-001", name: "Chine/ACFTU Syndicats Contrôlés Parti — Grèves Illégales Réprimées Force, Négociation Collective Façade, Organisateurs Indépendants Arrêtés & Aucun Syndicat Autonome Toléré", country: "Chine", sector: "Syndicats Parti État", union_busting_repression_severity_score: 95.0, collective_bargaining_prohibition_scale_score: 92.0, strike_right_criminalization_score: 90.0, labor_organizer_persecution_impunity_score: 88.0, composite_score: 91.6, risk_level: "critique", primary_pattern: "repression_syndicale_violente", key_signals: ["Monopole syndical étatique — l'ACFTU (290M membres) est le seul syndicat légal, contrôlé par le Parti Communiste, rendant impossible toute représentation indépendante des travailleurs", "Grèves illégales réprimées — 2.700+ grèves documentées 2015-2022 par China Labour Bulletin, toutes réprimées, organisateurs arrêtés et condamnés à 3-5 ans", "Négociation collective façade — les 'accords' sont négociés entre l'ACFTU et la direction sans participation réelle des travailleurs, violant la Convention OIT C98"], estimated_labor_union_rights_freedom_association_index: 9.16, last_updated: "2026-06-21" },
      { id: "LURFA-002", name: "Guatemala/Maquila — Assassinats Syndicalistes Impunité 95%, Travailleurs Listes Noires Secteur Textile, Licenciements Anti-Syndicaux Normalité & État Complice Violence Patronale", country: "Guatemala", sector: "Violence Anti-Syndicale", union_busting_repression_severity_score: 90.0, collective_bargaining_prohibition_scale_score: 78.0, strike_right_criminalization_score: 72.0, labor_organizer_persecution_impunity_score: 88.0, composite_score: 82.1, risk_level: "critique", primary_pattern: "persecution_organisateurs_syndicaux", key_signals: ["Assassinats en toute impunité — 7 syndicalistes assassinés en 2022, impunité dans 95% des cas, Guatemala classé #2 mondial pour meurtres de syndicalistes selon l'ITUC", "Listes noires secteur textile — les travailleurs organisés sont blacklistés et impossibles à employer dans tout le secteur maquila, détruisant leurs moyens de subsistance", "Complicité étatique — forces de sécurité documentées protégeant les intérêts des employeurs lors des grèves, violence des employeurs sans poursuites"], estimated_labor_union_rights_freedom_association_index: 8.21, last_updated: "2026-06-21" },
      { id: "LURFA-003", name: "Bangladesh/Garment Secteur — Syndicats Clandestins Post-Rana Plaza, Organisatrices Femmes Menacées Licenciées, Grèves Réprimées Police & Accords Bangladesh Accord Pressions Limites", country: "Bangladesh", sector: "Industrie Textile", union_busting_repression_severity_score: 82.0, collective_bargaining_prohibition_scale_score: 80.0, strike_right_criminalization_score: 78.0, labor_organizer_persecution_impunity_score: 80.0, composite_score: 80.1, risk_level: "critique", primary_pattern: "repression_syndicale_violente", key_signals: ["Organisations clandestines — malgré la catastrophe Rana Plaza (1.134 morts, 2013), 90% des usines textiles restent sans syndicat, les organisateurs étant licenciés ou menacés", "Violence contre les femmes syndicalistes — les organisatrices (80% de la main d'oeuvre) subissent harcèlement sexuel, menaces et licenciements ciblés pour activité syndicale", "Bangladesh Accord insuffisant — accord de sécurité des bâtiments signé par 200+ marques mais ne couvrant pas les droits syndicaux, laissant les travailleurs sans voix collective réelle"], estimated_labor_union_rights_freedom_association_index: 8.01, last_updated: "2026-06-21" },
      { id: "LURFA-004", name: "Égypte/Syndicats Indépendants Interdits — Arrestations Activistes Travail, Loi 2017 Dissolution Forcée Syndicats Autonomes, Grèves Poursuivies Pénalement & Sécurité État Surveillance", country: "Égypte", sector: "Répression Syndicale Étatique", union_busting_repression_severity_score: 85.0, collective_bargaining_prohibition_scale_score: 88.0, strike_right_criminalization_score: 82.0, labor_organizer_persecution_impunity_score: 80.0, composite_score: 84.0, risk_level: "critique", primary_pattern: "interdiction_negociation_collective", key_signals: ["Syndicats indépendants dissous par loi — la loi 213/2017 impose une fédération syndicale unique contrôlée par l'État, dissolvant légalement les 1.500+ syndicats indépendants apparus après 2011", "Grèves criminalisées — les participants aux grèves poursuivis pour 'perturbation de la production' et 'incitation au désordre', peines jusqu'à 5 ans d'emprisonnement", "Activistes en détention — 350+ syndicalistes et militants des droits du travail emprisonnés depuis 2013, dont plusieurs en isolement prolongé"], estimated_labor_union_rights_freedom_association_index: 8.4, last_updated: "2026-06-21" },
      { id: "LURFA-005", name: "Turquie/État Urgence — Licenciements Syndicaux Fonctionnaires Post-2016, Syndicats Secteur Public Dissous, Grève Interdite Services Essentiels Élargis & KESK Procès Militants", country: "Turquie", sector: "Restrictions Secteur Public", union_busting_repression_severity_score: 55.0, collective_bargaining_prohibition_scale_score: 60.0, strike_right_criminalization_score: 52.0, labor_organizer_persecution_impunity_score: 58.0, composite_score: 56.1, risk_level: "élevé", primary_pattern: "criminalisation_droit_greve", key_signals: ["Licenciements massifs post-2016 — 125.000 fonctionnaires licenciés par décrets d'urgence, dont des milliers membres de syndicats du secteur public (KESK, Eğitim-Sen)", "Grèves interdites secteurs élargis — définition excessivement large des 'services essentiels' interdisant les grèves dans l'éducation, la santé, l'énergie et le transport public", "Procès syndicaux — dirigeants du KESK et d'Eğitim-Sen poursuivis pour 'propagande terroriste' et 'financement d'organisation terroriste' pour des activités syndicales normales"], estimated_labor_union_rights_freedom_association_index: 5.61, last_updated: "2026-06-21" },
      { id: "LURFA-006", name: "USA/Amazon Starbucks — Campagnes Anti-Syndicat Agressives, NLRA Sanctions Insuffisantes Délais 3 Ans, Fermeture Magasins Syndicalisés & Résistance Patronale Légale Systémique", country: "USA", sector: "Union Busting Légal", union_busting_repression_severity_score: 45.0, collective_bargaining_prohibition_scale_score: 48.0, strike_right_criminalization_score: 42.0, labor_organizer_persecution_impunity_score: 50.0, composite_score: 46.0, risk_level: "élevé", primary_pattern: "repression_syndicale_violente", key_signals: ["Union busting légal systémique — Amazon et Starbucks dépensent 600M$/an en consultants anti-syndicats, réunions obligatoires d'entreprise et remplacements de grévistes légaux", "NLRA insuffisante — sanctions maximales de 3.200$ par infraction rendant les violations syndicales rentables pour les grandes entreprises, délais de procédure de 2-3 ans", "Fermetures ciblées — Starbucks a fermé 16 magasins après syndicalisation, Amazon a fermé une warehouse au Queens (NY) après vote positif, violant l'esprit mais pas la lettre de la NLRA"], estimated_labor_union_rights_freedom_association_index: 4.6, last_updated: "2026-06-21" },
      { id: "LURFA-007", name: "Brésil/Réforme Travail 2017 — Affaiblissement Financement Syndicats Cotisation Facultative, Négociation Individuelle Autorisée Surpasse Convention, CUT Perte 90% Ressources & Taux Syndicalisation Baisse", country: "Brésil", sector: "Réforme Anti-Syndicale", union_busting_repression_severity_score: 30.0, collective_bargaining_prohibition_scale_score: 28.0, strike_right_criminalization_score: 25.0, labor_organizer_persecution_impunity_score: 35.0, composite_score: 29.25, risk_level: "modéré", primary_pattern: "interdiction_negociation_collective", key_signals: ["Réforme Temer 2017 affaiblit le syndicalisme — cotisation syndicale devenue facultative, faisant chuter les revenus syndicaux de 90% et réduisant la capacité d'action des syndicats", "Négociation individuelle légalisée au-dessus de la convention — les accords individuels peuvent maintenant déroger aux conventions collectives, vidant la négociation collective de son sens", "Taux de syndicalisation en chute — de 20% en 2012 à 11% en 2023, la réforme ayant fragilisé les grandes centrales CUT, Força Sindical et CTB"], estimated_labor_union_rights_freedom_association_index: 2.92, last_updated: "2026-06-21" },
      { id: "LURFA-008", name: "Danemark/Flexicurité Modèle — Taux Affiliation Syndicale 67%, Négociation Collective Couvre 85% Travailleurs, Droit Grève Constitutionnel & Dialogue Social Institutionnalisé Tripartite", country: "Danemark", sector: "Modèle Flexicurité", union_busting_repression_severity_score: 3.0, collective_bargaining_prohibition_scale_score: 4.0, strike_right_criminalization_score: 2.0, labor_organizer_persecution_impunity_score: 5.0, composite_score: 3.4, risk_level: "faible", primary_pattern: "repression_syndicale_violente", key_signals: ["Modèle de flexicurité exporté — taux de syndicalisation à 67% (vs 10% USA), négociation collective couvrant 85% des travailleurs sans salaire minimum légal car les conventions suffisent", "Dialogue tripartite institutionnalisé — gouvernement, LO (syndicats) et DA (patronat) co-déterminent les politiques sociales, créant une stabilité industrielle avec 99% de conflits résolus sans grève", "Droit de grève constitutionnel effectif — les grèves sont légales, prévisibles (préavis 14 jours) et culturellement acceptées comme outil normal de régulation sociale"], estimated_labor_union_rights_freedom_association_index: 0.34, last_updated: "2026-06-21" },
    ],
  };
}

const MOCK = getMockData();

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/labor-union-rights-freedom-association-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
