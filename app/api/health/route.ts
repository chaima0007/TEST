/**
 * Health-check endpoint.
 *
 * Returns {"status":"ok","timestamp":"..."} — intentionally minimal to avoid
 * leaking system information.  Protected by a shared-secret header so that
 * only authorised monitoring systems (Uptime Robot, Datadog, etc.) can poll
 * it without triggering false-positive security alerts.
 *
 * Required header:  X-Health-Token: <value of HEALTH_CHECK_TOKEN env var>
 *
 * If HEALTH_CHECK_TOKEN is not set the endpoint is effectively disabled
 * (every request returns 401) — set it in your deployment environment.
 */

import { NextRequest, NextResponse } from "next/server";
import { getClientIp, logSecurityEvent } from "@/lib/security";

const SECURITY_HEADERS: Record<string, string> = {
  "X-Content-Type-Options": "nosniff",
  "Cache-Control": "no-store, no-cache",
};

export async function GET(request: NextRequest): Promise<NextResponse> {
  const expectedToken = process.env.HEALTH_CHECK_TOKEN;
  const providedToken = request.headers.get("x-health-token");

  if (!expectedToken || !providedToken || providedToken !== expectedToken) {
    logSecurityEvent({
      type: "UNAUTHORIZED_ACCESS",
      ip: getClientIp(request),
      path: "/api/health",
      details: "Invalid or missing X-Health-Token header",
    });
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401, headers: SECURITY_HEADERS }
    );
  }

  return NextResponse.json(
    { status: "ok", timestamp: new Date().toISOString() },
    { status: 200, headers: SECURITY_HEADERS }
  );
}
