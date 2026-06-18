import { NextResponse } from "next/server";

/**
 * Returns demo login credentials so they are never hardcoded in the client JS bundle.
 * In production, set DEMO_EMAIL and DEMO_PASSWORD env vars.
 * This endpoint is intentionally public — it only exposes demo/throwaway credentials.
 */
export async function GET() {
  return NextResponse.json({
    email: process.env.DEMO_EMAIL ?? "demo@competeiq.com",
    password: process.env.DEMO_PASSWORD ?? "demo123",
  });
}
