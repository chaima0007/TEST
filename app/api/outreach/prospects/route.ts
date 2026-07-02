import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";

// GET /api/outreach/prospects?status=&city=&q=
export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const status = searchParams.get("status");
  const city = searchParams.get("city");
  const q = searchParams.get("q");

  const prospects = await prisma.prospect.findMany({
    where: {
      ...(status ? { status } : {}),
      ...(city ? { city } : {}),
      ...(q ? { name: { contains: q } } : {}),
    },
    orderBy: [{ score: "desc" }, { createdAt: "desc" }],
    include: { _count: { select: { messages: true } } },
  });

  return NextResponse.json(prospects);
}

interface ProspectInput {
  name?: unknown;
  category?: unknown;
  city?: unknown;
  email?: unknown;
  phone?: unknown;
  address?: unknown;
  notes?: unknown;
}

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() !== "" ? value : undefined;
}

// POST /api/outreach/prospects — un objet OU un tableau de prospects manuels.
export async function POST(request: NextRequest) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const items: ProspectInput[] = Array.isArray(body)
    ? (body as ProspectInput[])
    : [(body ?? {}) as ProspectInput];

  if (items.length === 0) {
    return NextResponse.json(
      { error: "Aucun prospect fourni." },
      { status: 400 }
    );
  }

  // Validation en amont : tout ou rien.
  for (const [index, item] of items.entries()) {
    if (
      typeof item?.name !== "string" ||
      item.name.trim() === "" ||
      typeof item.category !== "string" ||
      item.category.trim() === "" ||
      typeof item.city !== "string" ||
      item.city.trim() === ""
    ) {
      return NextResponse.json(
        {
          error: `Prospect ${index + 1} : les champs "name", "category" et "city" sont obligatoires.`,
        },
        { status: 400 }
      );
    }
  }

  const created = [];
  for (const item of items) {
    const prospect = await prisma.prospect.create({
      data: {
        name: (item.name as string).trim(),
        category: (item.category as string).trim(),
        city: (item.city as string).trim(),
        email: optionalString(item.email),
        phone: optionalString(item.phone),
        address: optionalString(item.address),
        notes: optionalString(item.notes),
        source: "manual",
        status: "new",
      },
    });
    created.push(prospect);
  }

  return NextResponse.json(
    Array.isArray(body) ? created : created[0],
    { status: 201 }
  );
}
