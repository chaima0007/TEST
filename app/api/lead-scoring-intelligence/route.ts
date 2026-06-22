import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[lead-scoring-intelligence] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockLeads = [
  {
    lead_id: "ls_001",
    company: "CloudScale Technologies",
    contact_name: "Sarah Mitchell",
    segment: "enterprise",
    lead_source: "inbound",
    lead_score: 88.0,
    fit_score_label: "excellent",
    intent_signal: "high_intent",
    tier: "hot",
    action: "call_now",
    fit_breakdown: { icp: 35.0, engagement: 28.0, qualification: 26.0 },
    strengths: [
      "Industrie alignée avec l'ICP cible",
      "Taille et revenu dans la cible — fit entreprise fort",
      "Stack technologique compatible — intégration facilitée",
      "Demo demandée — intention d'achat manifeste",
      "Visites répétées page tarifs — evaluation active",
      "Budget confirmé — deal qualifiable immédiatement",
      "Décideur identifié et engagé",
      "Besoin + timeline confirmés — deal en cours de qualification",
    ],
    weaknesses: [],
    recommended_steps: [
      "Appel de qualification immédiat — profil HOT avec forte intention",
      "Préparer deck personnalisé ROI selon l'industrie",
      "Identifier et confirmer le sponsor exécutif",
      "Proposer une demo technique dans les 48h",
    ],
    disqualification_reasons: [],
  },
  {
    lead_id: "ls_002",
    company: "DataVault Partners",
    contact_name: "Marc Fontaine",
    segment: "enterprise",
    lead_source: "referral",
    lead_score: 82.0,
    fit_score_label: "excellent",
    intent_signal: "high_intent",
    tier: "hot",
    action: "call_now",
    fit_breakdown: { icp: 35.0, engagement: 22.0, qualification: 26.0 },
    strengths: [
      "Industrie alignée avec l'ICP cible",
      "Taille et revenu dans la cible — fit entreprise fort",
      "Stack technologique compatible — intégration facilitée",
      "Demo demandée — intention d'achat manifeste",
      "Budget confirmé — deal qualifiable immédiatement",
      "Décideur identifié et engagé",
      "Lead issu de recommandation — taux de conversion x2",
    ],
    weaknesses: [],
    recommended_steps: [
      "Appel de qualification immédiat — profil HOT avec forte intention",
      "Préparer deck personnalisé ROI selon l'industrie",
      "Identifier et confirmer le sponsor exécutif",
      "Proposer une demo technique dans les 48h",
    ],
    disqualification_reasons: [],
  },
  {
    lead_id: "ls_003",
    company: "NexaRetail Group",
    contact_name: "Elena Vasquez",
    segment: "enterprise",
    lead_source: "outbound",
    lead_score: 72.0,
    fit_score_label: "excellent",
    intent_signal: "medium_intent",
    tier: "hot",
    action: "assign_ae",
    fit_breakdown: { icp: 35.0, engagement: 19.0, qualification: 18.0 },
    strengths: [
      "Industrie alignée avec l'ICP cible",
      "Taille et revenu dans la cible — fit entreprise fort",
      "Stack technologique compatible — intégration facilitée",
      "Décideur identifié et engagé",
    ],
    weaknesses: [
      "Budget non confirmé — risque disqualification BANT",
      "Besoin non confirmé — qualification discovery nécessaire",
    ],
    recommended_steps: [
      "Assigner à un AE senior — lead HOT qualifiable",
      "Transférer contexte complet et historique d'engagement",
      "Organiser une réunion de découverte approfondie",
      "Préparer une proposition commerciale sous 5 jours",
    ],
    disqualification_reasons: [],
  },
  {
    lead_id: "ls_004",
    company: "HealthBridge Systems",
    contact_name: "Thomas Grau",
    segment: "mid_market",
    lead_source: "event",
    lead_score: 71.0,
    fit_score_label: "excellent",
    intent_signal: "high_intent",
    tier: "hot",
    action: "call_now",
    fit_breakdown: { icp: 31.0, engagement: 24.0, qualification: 18.0 },
    strengths: [
      "Industrie alignée avec l'ICP cible",
      "Demo demandée — intention d'achat manifeste",
      "Visites répétées page tarifs — evaluation active",
      "Décideur identifié et engagé",
    ],
    weaknesses: [
      "Budget non confirmé — risque disqualification BANT",
    ],
    recommended_steps: [
      "Appel de qualification immédiat — profil HOT avec forte intention",
      "Préparer deck personnalisé ROI selon l'industrie",
      "Identifier et confirmer le sponsor exécutif",
      "Proposer une demo technique dans les 48h",
    ],
    disqualification_reasons: [],
  },
  {
    lead_id: "ls_005",
    company: "FinCore Solutions",
    contact_name: "Aisha Ndiaye",
    segment: "mid_market",
    lead_source: "content",
    lead_score: 58.0,
    fit_score_label: "good",
    intent_signal: "medium_intent",
    tier: "warm",
    action: "qualify",
    fit_breakdown: { icp: 23.0, engagement: 17.0, qualification: 18.0 },
    strengths: [
      "Industrie alignée avec l'ICP cible",
      "Budget confirmé — deal qualifiable immédiatement",
      "Décideur identifié et engagé",
    ],
    weaknesses: [
      "Profil entreprise hors cible (taille/revenu)",
    ],
    recommended_steps: [
      "Appel de qualification BANT — valider budget et timeline",
      "Confirmer le besoin métier et les critères de succès",
      "Identifier les parties prenantes clés",
      "Envoyer étude de cas sectorielle pertinente",
    ],
    disqualification_reasons: [],
  },
  {
    lead_id: "ls_006",
    company: "LogiFlux GmbH",
    contact_name: "Peter Hoffmann",
    segment: "mid_market",
    lead_source: "inbound",
    lead_score: 47.0,
    fit_score_label: "good",
    intent_signal: "medium_intent",
    tier: "warm",
    action: "nurture",
    fit_breakdown: { icp: 22.0, engagement: 14.0, qualification: 12.0 },
    strengths: [
      "Industrie alignée avec l'ICP cible",
      "Stack technologique compatible — intégration facilitée",
    ],
    weaknesses: [
      "Budget non confirmé — risque disqualification BANT",
      "Décideur non identifié — accès au sponsor requis",
      "Besoin non confirmé — qualification discovery nécessaire",
    ],
    recommended_steps: [
      "Intégrer dans une séquence nurture ciblée",
      "Envoyer du contenu éducatif adapté au secteur",
      "Relancer dans 2 semaines avec un angle business",
      "Monitorer les signaux d'intention (visites site, emails)",
    ],
    disqualification_reasons: [],
  },
  {
    lead_id: "ls_007",
    company: "EduSpark Ltd",
    contact_name: "Claire Joubert",
    segment: "smb",
    lead_source: "outbound",
    lead_score: 28.0,
    fit_score_label: "fair",
    intent_signal: "medium_intent",
    tier: "cold",
    action: "nurture",
    fit_breakdown: { icp: 15.0, engagement: 13.0, qualification: 0.0 },
    strengths: [],
    weaknesses: [
      "Profil entreprise hors cible (taille/revenu)",
      "Budget non confirmé — risque disqualification BANT",
      "Décideur non identifié — accès au sponsor requis",
      "Besoin non confirmé — qualification discovery nécessaire",
    ],
    recommended_steps: [
      "Intégrer dans une séquence nurture ciblée",
      "Envoyer du contenu éducatif adapté au secteur",
      "Relancer dans 2 semaines avec un angle business",
      "Monitorer les signaux d'intention (visites site, emails)",
    ],
    disqualification_reasons: [],
  },
  {
    lead_id: "ls_008",
    company: "PropLink AG",
    contact_name: "Ralf Steiner",
    segment: "smb",
    lead_source: "outbound",
    lead_score: 5.0,
    fit_score_label: "poor",
    intent_signal: "no_intent",
    tier: "dead",
    action: "disqualify",
    fit_breakdown: { icp: 5.0, engagement: 0.0, qualification: 0.0 },
    strengths: [],
    weaknesses: [
      "Industrie hors ICP — fit produit non confirmé",
      "Profil entreprise hors cible (taille/revenu)",
      "Engagement très faible — lead non activé",
      "Budget non confirmé — risque disqualification BANT",
      "Décideur non identifié — accès au sponsor requis",
    ],
    recommended_steps: [
      "Archiver le lead — critères de disqualification atteints",
      "Notifier le BDR pour mise à jour CRM",
    ],
    disqualification_reasons: [],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const action = searchParams.get("action");
  const intent = searchParams.get("intent");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/lead-scoring-intelligence`);
      if (tier) url.searchParams.set("tier", tier);
      if (action) url.searchParams.set("action", action);
      if (intent) url.searchParams.set("intent", intent);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let leads = [...mockLeads];
  if (tier) leads = leads.filter((l) => l.tier === tier);
  if (action) leads = leads.filter((l) => l.action === action);
  if (intent) leads = leads.filter((l) => l.intent_signal === intent);

  const tier_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const intent_counts: Record<string, number> = {};
  const fit_counts: Record<string, number> = {};
  let total_score = 0;

  for (const l of mockLeads) {
    tier_counts[l.tier] = (tier_counts[l.tier] || 0) + 1;
    action_counts[l.action] = (action_counts[l.action] || 0) + 1;
    intent_counts[l.intent_signal] = (intent_counts[l.intent_signal] || 0) + 1;
    fit_counts[l.fit_score_label] = (fit_counts[l.fit_score_label] || 0) + 1;
    total_score += l.lead_score;
  }

  const n = mockLeads.length;

  return sealResponse(NextResponse.json(sealResponse({
    leads,
    summary: {
      total: n,
      tier_counts,
      action_counts,
      intent_counts,
      fit_counts,
      avg_lead_score: Math.round((total_score / n) * 10) / 10,
      hot_count: mockLeads.filter((l) => l.tier === "hot").length,
      call_now_count: mockLeads.filter((l) => l.action === "call_now").length,
      disqualified_count: mockLeads.filter((l) => l.action === "disqualify").length,
      hot_rate_pct: Math.round((mockLeads.filter((l) => l.tier === "hot").length / n) * 1000) / 10,
    },
  } as Record<string,unknown>)));
}
