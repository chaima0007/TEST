import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prospects] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_PROSPECTS = {
  source: "mock",
  total: 847,
  tier_a: 94,
  tier_b: 267,
  tier_c: 486,
  last_cycle: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  prospects: [
    { company_id: "1.1_0001", name: "Plomberie Leblanc SARL", sector: "Artisans & Bâtiment", website: "http://plomberie-leblanc.fr", pagespeed_score: 12, load_time_ms: 8400, priority_score: 92, tier: "A", icp_fit: 0.90, urgency_label: "critique", estimated_revenue_impact_eur: 28000, contact_email: "contact@plomberie-leblanc.fr", company_size: "PME" },
    { company_id: "1.2_0001", name: "Restaurant Le Gaulois", sector: "Restauration & Hôtellerie", website: "http://legaulois-restaurant.fr", pagespeed_score: 18, load_time_ms: 7200, priority_score: 89, tier: "A", icp_fit: 0.95, urgency_label: "critique", estimated_revenue_impact_eur: 52000, contact_email: "contact@legaulois.fr", company_size: "PME" },
    { company_id: "1.3_0001", name: "Cabinet Médical Marchand", sector: "Médical & Cabinets de Soin", website: "http://cabinet-marchand.fr", pagespeed_score: 24, load_time_ms: 6100, priority_score: 85, tier: "A", icp_fit: 0.85, urgency_label: "critique", estimated_revenue_impact_eur: 43000, contact_email: "secretariat@marchand.fr", company_size: "PME" },
    { company_id: "1.4_0001", name: "Auto Garage Martin", sector: "Garages & Concessionnaires", website: "http://garage-martin.fr", pagespeed_score: 31, load_time_ms: 5600, priority_score: 78, tier: "A", icp_fit: 0.70, urgency_label: "mauvais", estimated_revenue_impact_eur: 18000, contact_email: "contact@garage-martin.fr", company_size: "PME" },
    { company_id: "1.5_0001", name: "Maître Dupont Avocat", sector: "Services Juridiques & Comptabilité", website: "http://dupont-avocat.fr", pagespeed_score: 28, load_time_ms: 5900, priority_score: 77, tier: "A", icp_fit: 0.82, urgency_label: "critique", estimated_revenue_impact_eur: 35000, contact_email: "cabinet@dupont-avocat.fr", company_size: "PME" },
    { company_id: "1.6_0001", name: "Coiff & Style", sector: "Boutiques & Beauté", website: "http://coiff-style.fr", pagespeed_score: 35, load_time_ms: 4800, priority_score: 65, tier: "B", icp_fit: 0.72, urgency_label: "mauvais", estimated_revenue_impact_eur: 12000, contact_email: "contact@coiff-style.fr", company_size: "TPE" },
    { company_id: "1.7_0001", name: "Immo Provence", sector: "Agences Immobilières", website: "http://immo-provence.fr", pagespeed_score: 42, load_time_ms: 4200, priority_score: 58, tier: "B", icp_fit: 0.75, urgency_label: "mauvais", estimated_revenue_impact_eur: 22000, contact_email: "info@immo-provence.fr", company_size: "PME" },
    { company_id: "1.8_0001", name: "École de Langues LinguaMax", sector: "Écoles & Formation", website: "http://linguamax.fr", pagespeed_score: 48, load_time_ms: 4100, priority_score: 45, tier: "B", icp_fit: 0.55, urgency_label: "mauvais", estimated_revenue_impact_eur: 8000, contact_email: "contact@linguamax.fr", company_size: "PME" },
    { company_id: "1.9_0001", name: "Boulangerie Du Pain Quotidien", sector: "Artisans Boulangers", website: "http://boulangerie-dupain.fr", pagespeed_score: 52, load_time_ms: 3900, priority_score: 38, tier: "C", icp_fit: 0.60, urgency_label: "moyen", estimated_revenue_impact_eur: 5000, contact_email: "contact@dupain.fr", company_size: "TPE" },
    { company_id: "1.1_0002", name: "Menuiserie Artisan Bois", sector: "Artisans & Bâtiment", website: "http://menuiserie-bois.fr", pagespeed_score: 19, load_time_ms: 7800, priority_score: 88, tier: "A", icp_fit: 0.88, urgency_label: "critique", estimated_revenue_impact_eur: 31000, contact_email: "contact@menuiserie-bois.fr", company_size: "PME" },
    { company_id: "1.2_0002", name: "Hôtel Les Pins d'Or", sector: "Restauration & Hôtellerie", website: "http://hotel-pinsdor.fr", pagespeed_score: 22, load_time_ms: 6800, priority_score: 86, tier: "A", icp_fit: 0.95, urgency_label: "critique", estimated_revenue_impact_eur: 78000, contact_email: "reception@hotel-pinsdor.fr", company_size: "PME" },
    { company_id: "1.3_0002", name: "Dr. Leclerc Dentiste", sector: "Médical & Cabinets de Soin", website: "http://leclerc-dentiste.fr", pagespeed_score: 27, load_time_ms: 6300, priority_score: 84, tier: "A", icp_fit: 0.85, urgency_label: "critique", estimated_revenue_impact_eur: 41000, contact_email: "cabinet@leclerc-dentiste.fr", company_size: "PME" },
  ],
};

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const tier = searchParams.get("tier");
  const search = searchParams.get("q")?.toLowerCase();

  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/prospects?tier=${tier || ""}`, {
        next: { revalidate: 30 },
      });
      if (res.ok) {
        return sealResponse(NextResponse.json({ source: "live", ...(await res.json()) }));
      }
    } catch {
      // fall through
    }
  }

  let prospects = MOCK_PROSPECTS.prospects;
  if (tier && tier !== "all") {
    prospects = prospects.filter((p) => p.tier === tier.toUpperCase());
  }
  if (search) {
    prospects = prospects.filter(
      (p) =>
        p.name.toLowerCase().includes(search) ||
        p.sector.toLowerCase().includes(search)
    );
  }

  return sealResponse(NextResponse.json({ ...MOCK_PROSPECTS, prospects, source: "mock" }));
}
