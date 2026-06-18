import { NextRequest, NextResponse } from "next/server";
import { alerts } from "@/lib/data";

const ALLOWED_ORIGIN = process.env.NEXT_PUBLIC_APP_URL ?? "";

const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Cache-Control": "no-store",
};

function checkOrigin(req: NextRequest): NextResponse | null {
  const origin = req.headers.get("origin");
  if (origin && ALLOWED_ORIGIN && origin !== ALLOWED_ORIGIN) {
    return NextResponse.json(
      { error: "Forbidden" },
      { status: 403, headers: SECURITY_HEADERS }
    );
  }
  return null;
}

export async function GET(req: NextRequest) {
  const corsError = checkOrigin(req);
  if (corsError) return corsError;

  return NextResponse.json(alerts, { headers: SECURITY_HEADERS });
}

export async function PATCH(req: NextRequest) {
  const corsError = checkOrigin(req);
  if (corsError) return corsError;

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      { error: "Corps de requête invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }

  if (typeof body !== "object" || body === null || Array.isArray(body)) {
    return NextResponse.json(
      { error: "Requête invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }

  const payload = body as Record<string, unknown>;

  if (payload.markAllRead) {
    return NextResponse.json({ success: true }, { headers: SECURITY_HEADERS });
  }

  if (payload.id !== undefined) {
    if (typeof payload.id !== "string" || !/^[a-zA-Z0-9-_]+$/.test(payload.id)) {
      return NextResponse.json(
        { error: "Identifiant invalide" },
        { status: 400, headers: SECURITY_HEADERS }
      );
    }
    const alert = alerts.find((a) => a.id === payload.id);
    if (!alert) {
      return NextResponse.json(
        { error: "Alert not found" },
        { status: 404, headers: SECURITY_HEADERS }
      );
    }
    return NextResponse.json(
      { ...alert, isRead: true },
      { headers: SECURITY_HEADERS }
    );
  }

  return NextResponse.json(
    { error: "Requête invalide" },
    { status: 400, headers: SECURITY_HEADERS }
  );
}
