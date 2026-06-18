import { NextRequest, NextResponse } from "next/server";
import { competitors } from "@/lib/data";

const ALLOWED_ORIGIN = process.env.NEXT_PUBLIC_APP_URL ?? "";

const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Cache-Control": "no-store",
};

const ID_PATTERN = /^[a-zA-Z0-9-_]+$/;

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

function validateId(id: string): NextResponse | null {
  if (!id || id.length > 500 || !ID_PATTERN.test(id)) {
    return NextResponse.json(
      { error: "Identifiant invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }
  return null;
}

export async function GET(
  req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const corsError = checkOrigin(req);
  if (corsError) return corsError;

  const { id } = await props.params;
  const idError = validateId(id);
  if (idError) return idError;

  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) {
    return NextResponse.json(
      { error: "Competitor not found" },
      { status: 404, headers: SECURITY_HEADERS }
    );
  }

  return NextResponse.json(competitor, { headers: SECURITY_HEADERS });
}

export async function PATCH(
  req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const corsError = checkOrigin(req);
  if (corsError) return corsError;

  const { id } = await props.params;
  const idError = validateId(id);
  if (idError) return idError;

  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) {
    return NextResponse.json(
      { error: "Competitor not found" },
      { status: 404, headers: SECURITY_HEADERS }
    );
  }

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

  const payload = body as {
    name?: string;
    website?: string;
    industry?: string;
    description?: string;
    threatLevel?: string;
  };

  // Validate field lengths
  for (const field of ["name", "website", "industry", "description", "threatLevel"] as const) {
    const val = payload[field];
    if (val !== undefined && (typeof val !== "string" || val.length > 500)) {
      return NextResponse.json(
        { error: `Champ invalide : ${field}` },
        { status: 400, headers: SECURITY_HEADERS }
      );
    }
  }

  const updated = {
    ...competitor,
    ...(payload.name && { name: payload.name }),
    ...(payload.website && { website: payload.website }),
    ...(payload.industry !== undefined && { industry: payload.industry }),
    ...(payload.description !== undefined && { description: payload.description }),
    ...(payload.threatLevel &&
      ["high", "medium", "low"].includes(payload.threatLevel) && {
        threatLevel: payload.threatLevel as "high" | "medium" | "low",
      }),
    lastUpdated: new Date().toISOString().split("T")[0],
  };

  return NextResponse.json(updated, { headers: SECURITY_HEADERS });
}

export async function DELETE(
  req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const corsError = checkOrigin(req);
  if (corsError) return corsError;

  const { id } = await props.params;
  const idError = validateId(id);
  if (idError) return idError;

  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) {
    return NextResponse.json(
      { error: "Competitor not found" },
      { status: 404, headers: SECURITY_HEADERS }
    );
  }

  return NextResponse.json({ success: true }, { headers: SECURITY_HEADERS });
}
