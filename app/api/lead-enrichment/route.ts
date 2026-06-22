import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[lead-enrichment] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockLeads = [
  {
    lead_id: "lead_001",
    lead_name: "Sophie Laurent",
    source: "inbound",
    data_quality: "excellent",
    quality_score: 88.5,
    contact_score: 100.0,
    company_score: 91.4,
    intent_score: 88.0,
    engagement_score: 82.0,
    enrichment_priority: "none",
    gaps: [],
    outreach_ready: true,
    quality_signals: [
      "Email vérifié — délivrabilité garantie",
      "Lead entrant — forte intention d'achat",
      "Point de douleur identifié : Inefficacité CRM actuel",
      "Signal budget capté — décision proche",
      "Décideur de haut niveau identifié (c_suite)",
      "2 téléchargements de contenu — intérêt prouvé",
    ],
    risk_flags: [],
    suggested_enrichment_sources: [],
  },
  {
    lead_id: "lead_002",
    lead_name: "Thomas Dubois",
    source: "referral",
    data_quality: "good",
    quality_score: 74.2,
    contact_score: 87.5,
    company_score: 82.9,
    intent_score: 72.0,
    engagement_score: 35.0,
    enrichment_priority: "low",
    gaps: [
      { field: "has_phone", description: "Téléphone manquant — canal de contact limité", impact_score: 8 },
      { field: "has_budget_signal", description: "Signal budget absent", impact_score: 5 },
      { field: "has_timeline", description: "Timeline non identifiée", impact_score: 5 },
    ],
    outreach_ready: true,
    quality_signals: [
      "Lead par recommandation — taux de conversion 3x supérieur",
      "Email vérifié — délivrabilité garantie",
      "Point de douleur identifié : Migration legacy vers cloud",
      "Décideur de haut niveau identifié (vp)",
      "Engagement modéré — lead tiède, à relancer",
    ],
    risk_flags: [
      "Email non vérifié — risque de bounce",
    ],
    suggested_enrichment_sources: [
      "Lusha / ZoomInfo — trouver numéro direct",
      "Gong / Chorus — analyser les appels de découverte précédents",
    ],
  },
  {
    lead_id: "lead_003",
    lead_name: "Camille Martin",
    source: "event",
    data_quality: "good",
    quality_score: 67.8,
    contact_score: 75.0,
    company_score: 77.1,
    intent_score: 56.0,
    engagement_score: 42.0,
    enrichment_priority: "low",
    gaps: [
      { field: "has_phone", description: "Téléphone manquant — canal de contact limité", impact_score: 8 },
      { field: "has_linkedin", description: "LinkedIn manquant — social selling impossible", impact_score: 10 },
      { field: "has_annual_revenue", description: "CA annuel manquant — potentiel deal inconnu", impact_score: 7 },
      { field: "has_use_case", description: "Cas d'usage non identifié", impact_score: 7 },
      { field: "has_budget_signal", description: "Signal budget absent", impact_score: 5 },
    ],
    outreach_ready: true,
    quality_signals: [
      "Point de douleur identifié : Automatisation des ventes insuffisante",
      "Engagement modéré — lead tiède, à relancer",
    ],
    risk_flags: [
      "Email non vérifié — risque de bounce",
    ],
    suggested_enrichment_sources: [
      "LinkedIn Sales Navigator — trouver profil et titre",
      "Lusha / ZoomInfo — trouver numéro direct",
      "Clearbit / Apollo — enrichissement firmographique",
      "Gong / Chorus — analyser les appels de découverte précédents",
    ],
  },
  {
    lead_id: "lead_004",
    lead_name: "Alexandre Petit",
    source: "outbound",
    data_quality: "fair",
    quality_score: 54.1,
    contact_score: 62.5,
    company_score: 60.0,
    intent_score: 40.0,
    engagement_score: 25.0,
    enrichment_priority: "medium",
    gaps: [
      { field: "has_phone", description: "Téléphone manquant — canal de contact limité", impact_score: 8 },
      { field: "has_linkedin", description: "LinkedIn manquant — social selling impossible", impact_score: 10 },
      { field: "has_company_size", description: "Taille entreprise manquante — ICP inconnu", impact_score: 7 },
      { field: "has_annual_revenue", description: "CA annuel manquant — potentiel deal inconnu", impact_score: 7 },
      { field: "has_pain_point", description: "Point de douleur non identifié", impact_score: 8 },
      { field: "has_use_case", description: "Cas d'usage non identifié", impact_score: 7 },
      { field: "has_timeline", description: "Timeline non identifiée", impact_score: 5 },
    ],
    outreach_ready: true,
    quality_signals: [
      "Signal budget capté — décision proche",
    ],
    risk_flags: [
      "Email non vérifié — risque de bounce",
    ],
    suggested_enrichment_sources: [
      "LinkedIn Sales Navigator — trouver profil et titre",
      "Lusha / ZoomInfo — trouver numéro direct",
      "Clearbit / Apollo — enrichissement firmographique",
      "Gong / Chorus — analyser les appels de découverte précédents",
    ],
  },
  {
    lead_id: "lead_005",
    lead_name: "Isabelle Bernard",
    source: "content",
    data_quality: "fair",
    quality_score: 47.6,
    contact_score: 55.0,
    company_score: 48.6,
    intent_score: 36.0,
    engagement_score: 37.0,
    enrichment_priority: "medium",
    gaps: [
      { field: "has_phone", description: "Téléphone manquant — canal de contact limité", impact_score: 8 },
      { field: "has_linkedin", description: "LinkedIn manquant — social selling impossible", impact_score: 10 },
      { field: "has_job_title", description: "Titre manquant — personnalisation impossible", impact_score: 10 },
      { field: "has_industry", description: "Secteur manquant — segmentation impossible", impact_score: 8 },
      { field: "has_company_size", description: "Taille entreprise manquante — ICP inconnu", impact_score: 7 },
      { field: "has_annual_revenue", description: "CA annuel manquant — potentiel deal inconnu", impact_score: 7 },
      { field: "has_use_case", description: "Cas d'usage non identifié", impact_score: 7 },
      { field: "has_budget_signal", description: "Signal budget absent", impact_score: 5 },
      { field: "has_timeline", description: "Timeline non identifiée", impact_score: 5 },
    ],
    outreach_ready: true,
    quality_signals: [
      "Point de douleur identifié : Faible taux de conversion pipeline",
    ],
    risk_flags: [
      "Email non vérifié — risque de bounce",
      "Domaine email ne correspond pas à l'entreprise — valider l'identité",
    ],
    suggested_enrichment_sources: [
      "LinkedIn Sales Navigator — trouver profil et titre",
      "Lusha / ZoomInfo — trouver numéro direct",
      "Clearbit / Apollo — enrichissement firmographique",
      "Crunchbase / LinkedIn Company — valider secteur",
      "Gong / Chorus — analyser les appels de découverte précédents",
    ],
  },
  {
    lead_id: "lead_006",
    lead_name: "Marc Lefevre",
    source: "paid",
    data_quality: "poor",
    quality_score: 36.4,
    contact_score: 42.5,
    company_score: 34.3,
    intent_score: 20.0,
    engagement_score: 12.0,
    enrichment_priority: "high",
    gaps: [
      { field: "has_phone", description: "Téléphone manquant — canal de contact limité", impact_score: 8 },
      { field: "has_linkedin", description: "LinkedIn manquant — social selling impossible", impact_score: 10 },
      { field: "has_job_title", description: "Titre manquant — personnalisation impossible", impact_score: 10 },
      { field: "has_industry", description: "Secteur manquant — segmentation impossible", impact_score: 8 },
      { field: "has_company_size", description: "Taille entreprise manquante — ICP inconnu", impact_score: 7 },
      { field: "has_annual_revenue", description: "CA annuel manquant — potentiel deal inconnu", impact_score: 7 },
      { field: "has_website", description: "Site web manquant — impossible de valider l'entreprise", impact_score: 5 },
      { field: "has_pain_point", description: "Point de douleur non identifié", impact_score: 8 },
      { field: "has_use_case", description: "Cas d'usage non identifié", impact_score: 7 },
      { field: "has_budget_signal", description: "Signal budget absent", impact_score: 5 },
      { field: "has_timeline", description: "Timeline non identifiée", impact_score: 5 },
    ],
    outreach_ready: true,
    quality_signals: [],
    risk_flags: [
      "Email non vérifié — risque de bounce",
      "Données insuffisantes — enrichissement obligatoire avant contact",
    ],
    suggested_enrichment_sources: [
      "LinkedIn Sales Navigator — trouver profil et titre",
      "Lusha / ZoomInfo — trouver numéro direct",
      "Clearbit / Apollo — enrichissement firmographique",
      "Crunchbase / LinkedIn Company — valider secteur",
      "Gong / Chorus — analyser les appels de découverte précédents",
    ],
  },
  {
    lead_id: "lead_007",
    lead_name: "Nathalie Rousseau",
    source: "outbound",
    data_quality: "poor",
    quality_score: 27.9,
    contact_score: 25.0,
    company_score: 37.1,
    intent_score: 20.0,
    engagement_score: 18.0,
    enrichment_priority: "high",
    gaps: [
      { field: "has_email", description: "Email manquant — impossible de contacter", impact_score: 12 },
      { field: "has_phone", description: "Téléphone manquant — canal de contact limité", impact_score: 8 },
      { field: "has_job_title", description: "Titre manquant — personnalisation impossible", impact_score: 10 },
      { field: "has_company_size", description: "Taille entreprise manquante — ICP inconnu", impact_score: 7 },
      { field: "has_annual_revenue", description: "CA annuel manquant — potentiel deal inconnu", impact_score: 7 },
      { field: "has_website", description: "Site web manquant — impossible de valider l'entreprise", impact_score: 5 },
      { field: "has_pain_point", description: "Point de douleur non identifié", impact_score: 8 },
      { field: "has_use_case", description: "Cas d'usage non identifié", impact_score: 7 },
      { field: "has_budget_signal", description: "Signal budget absent", impact_score: 5 },
      { field: "has_timeline", description: "Timeline non identifiée", impact_score: 5 },
    ],
    outreach_ready: true,
    quality_signals: [],
    risk_flags: [
      "2 bounces antérieurs — vérifier l'email",
      "Données insuffisantes — enrichissement obligatoire avant contact",
    ],
    suggested_enrichment_sources: [
      "LinkedIn Sales Navigator — trouver profil et titre",
      "Hunter.io / Apollo.io — trouver email professionnel",
      "Lusha / ZoomInfo — trouver numéro direct",
      "Clearbit / Apollo — enrichissement firmographique",
      "Gong / Chorus — analyser les appels de découverte précédents",
    ],
  },
  {
    lead_id: "lead_008",
    lead_name: "Pierre Fontaine",
    source: "outbound",
    data_quality: "incomplete",
    quality_score: 15.8,
    contact_score: 12.5,
    company_score: 22.9,
    intent_score: 0.0,
    engagement_score: 0.0,
    enrichment_priority: "immediate",
    gaps: [
      { field: "has_email", description: "Email manquant — impossible de contacter", impact_score: 12 },
      { field: "has_phone", description: "Téléphone manquant — canal de contact limité", impact_score: 8 },
      { field: "has_linkedin", description: "LinkedIn manquant — social selling impossible", impact_score: 10 },
      { field: "has_company_size", description: "Taille entreprise manquante — ICP inconnu", impact_score: 7 },
      { field: "has_annual_revenue", description: "CA annuel manquant — potentiel deal inconnu", impact_score: 7 },
      { field: "has_website", description: "Site web manquant — impossible de valider l'entreprise", impact_score: 5 },
      { field: "has_pain_point", description: "Point de douleur non identifié", impact_score: 8 },
      { field: "has_use_case", description: "Cas d'usage non identifié", impact_score: 7 },
      { field: "has_budget_signal", description: "Signal budget absent", impact_score: 5 },
      { field: "has_timeline", description: "Timeline non identifiée", impact_score: 5 },
    ],
    outreach_ready: false,
    quality_signals: [],
    risk_flags: [
      "Données insuffisantes — enrichissement obligatoire avant contact",
      "Lead dupliqué — déprioritiser, déjà dans le CRM",
    ],
    suggested_enrichment_sources: [
      "LinkedIn Sales Navigator — trouver profil et titre",
      "Hunter.io / Apollo.io — trouver email professionnel",
      "Lusha / ZoomInfo — trouver numéro direct",
      "Clearbit / Apollo — enrichissement firmographique",
      "Crunchbase / LinkedIn Company — valider secteur",
      "Gong / Chorus — analyser les appels de découverte précédents",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const priority = searchParams.get("priority");
  const quality = searchParams.get("quality");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/lead-enrichment`);
      if (priority) url.searchParams.set("priority", priority);
      if (quality) url.searchParams.set("quality", quality);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let leads = [...mockLeads];
  if (priority) leads = leads.filter((l) => l.enrichment_priority === priority);
  if (quality) leads = leads.filter((l) => l.data_quality === quality);

  const quality_counts: Record<string, number> = {};
  const priority_counts: Record<string, number> = {};
  let total_score = 0;
  let outreach_ready_count = 0;
  let needs_enrichment_count = 0;

  for (const l of mockLeads) {
    quality_counts[l.data_quality] = (quality_counts[l.data_quality] || 0) + 1;
    priority_counts[l.enrichment_priority] = (priority_counts[l.enrichment_priority] || 0) + 1;
    total_score += l.quality_score;
    if (l.outreach_ready) outreach_ready_count++;
    if (l.enrichment_priority === "immediate" || l.enrichment_priority === "high") needs_enrichment_count++;
  }

  const n = mockLeads.length;

  return sealResponse(NextResponse.json({
    leads,
    summary: {
      total: n,
      quality_counts,
      priority_counts,
      avg_quality_score: Math.round((total_score / n) * 10) / 10,
      outreach_ready_count,
      needs_enrichment_count,
    },
  }));
}
