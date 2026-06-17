import { NextResponse } from "next/server";
import { LINKEDIN_POSTS, CV_ENTRIES, CASE_STUDIES, AGENT_PROFILE } from "@/lib/branding-data";

export async function GET() {
  return NextResponse.json({
    agent: AGENT_PROFILE,
    linkedin_posts: LINKEDIN_POSTS,
    cv_entries: CV_ENTRIES,
    case_studies: CASE_STUDIES,
    generated_at: new Date().toISOString(),
  });
}
