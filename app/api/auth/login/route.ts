import { NextRequest, NextResponse } from "next/server";

const DEMO_EMAIL = process.env.DEMO_EMAIL ?? "demo@caelum.be";
const DEMO_PASSWORD = process.env.DEMO_PASSWORD ?? "demo123";

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({})) as { email?: string; password?: string };
  const { email, password } = body;

  if (
    typeof email !== "string" ||
    typeof password !== "string" ||
    email.trim().toLowerCase() !== DEMO_EMAIL.toLowerCase() ||
    password !== DEMO_PASSWORD
  ) {
    return NextResponse.json({ error: "Identifiants incorrects" }, { status: 401 });
  }

  const response = NextResponse.json({ ok: true });
  response.cookies.set("ciq_session", "authenticated", {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 24 * 7, // 7 days
    secure: process.env.NODE_ENV === "production",
  });
  return response;
}
