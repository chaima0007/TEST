import { NextRequest, NextResponse } from "next/server";
import { reports } from "@/lib/data";

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

  return NextResponse.json(reports, { headers: SECURITY_HEADERS });
}

export async function POST(req: NextRequest) {
  const corsError = checkOrigin(req);
  if (corsError) return corsError;

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    body = {};
  }

  const payload =
    typeof body === "object" && body !== null && !Array.isArray(body)
      ? (body as Record<string, unknown>)
      : {};

  const rawTitle = payload.title;
  const rawDescription = payload.description;
  const rawPages = payload.pages;

  // Validate optional fields
  if (rawTitle !== undefined && (typeof rawTitle !== "string" || rawTitle.length > 500)) {
    return NextResponse.json(
      { error: "Champ 'title' invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }
  if (rawDescription !== undefined && (typeof rawDescription !== "string" || rawDescription.length > 500)) {
    return NextResponse.json(
      { error: "Champ 'description' invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }
  if (rawPages !== undefined && (typeof rawPages !== "number" || !Number.isFinite(rawPages) || rawPages < 1)) {
    return NextResponse.json(
      { error: "Champ 'pages' invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }

  const title = typeof rawTitle === "string" ? rawTitle : undefined;
  const description = typeof rawDescription === "string" ? rawDescription : undefined;
  const pages = typeof rawPages === "number" ? rawPages : undefined;

  const now = new Date();
  const dateStr = now.toISOString().split("T")[0];

  const report = {
    id: String(Date.now()),
    title: title || `Rapport Concurrentiel — ${dateStr}`,
    description:
      description ||
      "Rapport généré automatiquement avec les dernières données du marché.",
    createdAt: dateStr,
    pages: pages || 15,
    status: "ready",
  };

  return NextResponse.json(report, {
    status: 201,
    headers: SECURITY_HEADERS,
  });
}
