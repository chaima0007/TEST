import { NextResponse } from "next/server";
import { LINKEDIN_POSTS, CV_ENTRIES, CASE_STUDIES, AGENT_PROFILE } from "@/lib/branding-data";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[branding] SWARM_API_URL non défini — mode local");
}

export async function GET() {
  try {
    return NextResponse.json(sealResponse({
      agent: AGENT_PROFILE,
      linkedin_posts: LINKEDIN_POSTS,
      cv_entries: CV_ENTRIES,
      case_studies: CASE_STUDIES,
      generated_at: new Date().toISOString(),
    }));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}
