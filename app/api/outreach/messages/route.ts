import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";

// GET /api/outreach/messages?prospectId= ou ?status=
export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const prospectId = searchParams.get("prospectId");
  const status = searchParams.get("status");

  const messages = await prisma.outreachMessage.findMany({
    where: {
      ...(prospectId ? { prospectId } : {}),
      ...(status ? { status } : {}),
    },
    include: { prospect: { select: { name: true, email: true } } },
    orderBy: { createdAt: "desc" },
    take: 200,
  });

  return NextResponse.json(messages);
}
