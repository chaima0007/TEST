import { NextRequest, NextResponse } from "next/server";
import { competitors } from "@/lib/data";

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

  return NextResponse.json(competitors, { headers: SECURITY_HEADERS });
}

export async function POST(req: NextRequest) {
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
  const { name, website, industry, description, threatLevel } = payload;

  if (
    typeof name !== "string" ||
    typeof website !== "string" ||
    !name.trim() ||
    !website.trim()
  ) {
    return NextResponse.json(
      { error: "Name and website are required" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }

  if (name.length > 500 || website.length > 500) {
    return NextResponse.json(
      { error: "Champ trop long" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }

  const newCompetitor = {
    id: String(Date.now()),
    name,
    website,
    industry: typeof industry === "string" ? industry : "Non spécifié",
    description: typeof description === "string" ? description : "",
    threatLevel: (
      ["high", "medium", "low"].includes(String(threatLevel))
        ? threatLevel
        : "medium"
    ) as "high" | "medium" | "low",
    logo: name.slice(0, 2).toUpperCase(),
    color: "#6366f1",
    founded: new Date().getFullYear(),
    employees: "N/A",
    revenue: "N/A",
    marketShare: 0,
    lastUpdated: new Date().toISOString().split("T")[0],
    pricing: [],
    features: [],
    news: [],
    priceHistory: [],
  };

  return NextResponse.json(newCompetitor, {
    status: 201,
    headers: SECURITY_HEADERS,
  });
}
