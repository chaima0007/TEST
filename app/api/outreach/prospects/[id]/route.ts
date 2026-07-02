import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";

const VALID_STATUSES = [
  "new",
  "qualified",
  "contacted",
  "followup",
  "replied",
  "won",
  "lost",
  "optout",
] as const;

// GET /api/outreach/prospects/[id] — prospect + messages triés par étape.
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  const prospect = await prisma.prospect.findUnique({
    where: { id },
    include: { messages: { orderBy: { step: "asc" } } },
  });

  if (!prospect) {
    return NextResponse.json({ error: "Prospect introuvable" }, { status: 404 });
  }

  return NextResponse.json(prospect);
}

// PATCH /api/outreach/prospects/[id] — { status?, email?, phone?, notes? }
export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  let body: {
    status?: unknown;
    email?: unknown;
    phone?: unknown;
    notes?: unknown;
  };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const existing = await prisma.prospect.findUnique({ where: { id } });
  if (!existing) {
    return NextResponse.json({ error: "Prospect introuvable" }, { status: 404 });
  }

  const data: {
    status?: string;
    email?: string;
    phone?: string;
    notes?: string;
    optOut?: boolean;
  } = {};

  if (body.status !== undefined) {
    if (
      typeof body.status !== "string" ||
      !(VALID_STATUSES as readonly string[]).includes(body.status)
    ) {
      return NextResponse.json(
        {
          error: `Statut invalide. Valeurs acceptées : ${VALID_STATUSES.join(", ")}.`,
        },
        { status: 400 }
      );
    }
    data.status = body.status;
    if (body.status === "optout") data.optOut = true;
  }
  if (typeof body.email === "string") data.email = body.email;
  if (typeof body.phone === "string") data.phone = body.phone;
  if (typeof body.notes === "string") data.notes = body.notes;

  const updated = await prisma.prospect.update({ where: { id }, data });
  return NextResponse.json(updated);
}
