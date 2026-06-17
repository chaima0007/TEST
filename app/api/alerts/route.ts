import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getDemoUser } from "@/lib/auth";

export async function GET() {
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const alerts = await prisma.alert.findMany({
    where: { userId: user.id },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json(alerts);
}

export async function PATCH(req: NextRequest) {
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const body = await req.json();

  if (body.markAllRead) {
    await prisma.alert.updateMany({
      where: { userId: user.id, isRead: false },
      data: { isRead: true },
    });
    return NextResponse.json({ success: true });
  }

  if (body.id) {
    const alert = await prisma.alert.update({
      where: { id: body.id },
      data: { isRead: true },
    });
    return NextResponse.json(alert);
  }

  return NextResponse.json({ error: "Invalid request" }, { status: 400 });
}
