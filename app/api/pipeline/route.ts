import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pipeline] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_PIPELINE = {
  source: "mock",
  updated_at: new Date().toISOString(),
  funnel: [
    { stage: "Détectés",      count: 847,  value_eur: 0,        color: "indigo",  icon: "🔍" },
    { stage: "Qualifiés ICP", count: 412,  value_eur: 0,        color: "blue",    icon: "🎯" },
    { stage: "Emailés",       count: 298,  value_eur: 0,        color: "violet",  icon: "✉️" },
    { stage: "Ouvert",        count: 143,  value_eur: 0,        color: "purple",  icon: "👁" },
    { stage: "Répondu",       count: 41,   value_eur: 1230000,  color: "fuchsia", icon: "💬" },
    { stage: "En négo",       count: 18,   value_eur: 640000,   color: "pink",    icon: "🤝" },
    { stage: "Payé",          count: 7,    value_eur: 218000,   color: "emerald", icon: "💳" },
    { stage: "Livré",         count: 5,    value_eur: 155000,   color: "green",   icon: "📦" },
  ],
  conversions: {
    detected_to_qualified: 0.487,
    qualified_to_emailed: 0.723,
    emailed_to_open: 0.480,
    open_to_reply: 0.287,
    reply_to_negotiation: 0.439,
    negotiation_to_payment: 0.389,
    payment_to_delivery: 0.714,
    end_to_end: 0.0059,
  },
  grade_breakdown: [
    { grade: "S", count: 12,  avg_score: 91.2, recommended_action: "Appel immédiat" },
    { grade: "A", count: 87,  avg_score: 76.4, recommended_action: "Email personnalisé Tier A" },
    { grade: "B", count: 203, avg_score: 58.1, recommended_action: "Email de masse secteur" },
    { grade: "C", count: 289, avg_score: 38.7, recommended_action: "Nurturing 3 emails" },
    { grade: "D", count: 256, avg_score: 18.3, recommended_action: "Exclure du pipeline" },
  ],
  top_leads: [
    { company_id: "1.1_0001", name: "Plomberie Leblanc SARL",    action_score: 93.4, grade: "S", sector: "Artisans & Bâtiment",         stage: "En négo" },
    { company_id: "1.2_0001", name: "Restaurant Le Gaulois",      action_score: 91.8, grade: "S", sector: "Restauration & Hôtellerie",   stage: "En négo" },
    { company_id: "1.3_0001", name: "Cabinet Médical Marchand",   action_score: 88.2, grade: "S", sector: "Médical & Cabinets de Soin",  stage: "Répondu" },
    { company_id: "1.4_0001", name: "Auto Garage Martin",         action_score: 82.5, grade: "A", sector: "Garages & Concessionnaires",  stage: "Répondu" },
    { company_id: "1.5_0001", name: "Maître Dupont Avocat",       action_score: 79.1, grade: "A", sector: "Services Juridiques",         stage: "Ouvert" },
    { company_id: "1.2_0002", name: "Hôtel Les Pins d'Or",        action_score: 87.6, grade: "S", sector: "Restauration & Hôtellerie",   stage: "Payé" },
    { company_id: "1.1_0002", name: "Menuiserie Artisan Bois",    action_score: 85.3, grade: "S", sector: "Artisans & Bâtiment",         stage: "Payé" },
  ],
};

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/pipeline/report`, {
        next: { revalidate: 30 },
      });
      if (res.ok) {
        return sealResponse(NextResponse.json({ source: "live", ...(await res.json()) }));
      }
    } catch {
      // fall through to mock
    }
  }
  return sealResponse(NextResponse.json(MOCK_PIPELINE));
}
