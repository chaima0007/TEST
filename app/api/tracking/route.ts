import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_TRACKING = {
  source: "mock",
  summary: {
    campaigns: 24,
    emails_sent: 1847,
    open_rate: 0.412,
    reply_rate: 0.087,
    total_opens: 761,
    total_replies: 161,
  },
  top_campaigns: [
    { campaign_id: "camp_plmb_001", agent_id: "2.1", sector: "Artisans & Bâtiment", sent: 120, opens: 68, clicks: 22, replies: 14, open_rate: 0.567, click_rate: 0.183, reply_rate: 0.117, conversion_score: 0.171 },
    { campaign_id: "camp_rest_001", agent_id: "2.3", sector: "Restauration & Hôtellerie", sent: 95, opens: 51, clicks: 18, replies: 11, open_rate: 0.537, click_rate: 0.189, reply_rate: 0.116, conversion_score: 0.168 },
    { campaign_id: "camp_med_001",  agent_id: "2.5", sector: "Médical & Cabinets de Soin", sent: 80, opens: 42, clicks: 14, replies: 9, open_rate: 0.525, click_rate: 0.175, reply_rate: 0.113, conversion_score: 0.163 },
    { campaign_id: "camp_immo_001", agent_id: "2.2", sector: "Agences Immobilières", sent: 110, opens: 47, clicks: 15, replies: 7, open_rate: 0.427, click_rate: 0.136, reply_rate: 0.064, conversion_score: 0.116 },
    { campaign_id: "camp_gar_001",  agent_id: "2.4", sector: "Garages & Concessionnaires", sent: 75, opens: 28, clicks: 9, replies: 4, open_rate: 0.373, click_rate: 0.12, reply_rate: 0.053, conversion_score: 0.092 },
  ],
  agent_leaderboard: [
    { agent_id: "2.1", campaigns: 6, total_sent: 412, total_opens: 198, total_replies: 48, conversion_score: 0.168 },
    { agent_id: "2.3", campaigns: 5, total_sent: 380, total_opens: 171, total_replies: 39, conversion_score: 0.149 },
    { agent_id: "2.5", campaigns: 4, total_sent: 290, total_opens: 128, total_replies: 31, conversion_score: 0.148 },
    { agent_id: "2.7", campaigns: 3, total_sent: 210, total_opens: 89, total_replies: 18, conversion_score: 0.121 },
    { agent_id: "2.2", campaigns: 3, total_sent: 195, total_opens: 74, total_replies: 14, conversion_score: 0.109 },
    { agent_id: "2.4", campaigns: 2, total_sent: 180, total_opens: 61, total_replies: 7, conversion_score: 0.083 },
    { agent_id: "2.6", campaigns: 1, total_sent: 110, total_opens: 31, total_replies: 4, conversion_score: 0.064 },
    { agent_id: "2.8", campaigns: 1, total_sent: 80, total_opens: 19, total_replies: 0, conversion_score: 0.024 },
    { agent_id: "2.9", campaigns: 0, total_sent: 0, total_opens: 0, total_replies: 0, conversion_score: 0.0 },
  ],
};

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/tracking/report`, {
        next: { revalidate: 30 },
      });
      if (res.ok) {
        return NextResponse.json({ source: "live", ...(await res.json()) });
      }
    } catch {
      // fall through to mock
    }
  }
  return NextResponse.json(MOCK_TRACKING);
}
