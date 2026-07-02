import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";

// GET /api/outreach/unsubscribe?token=
// Route PUBLIQUE (aucune authentification) : désinscription en un clic.

function page(title: string, message: string): string {
  return `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
</head>
<body style="margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#f4f5f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;">
  <main style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.05);max-width:420px;margin:24px;padding:40px 32px;text-align:center;">
    <h1 style="font-size:20px;color:#111827;margin:0 0 12px;">${title}</h1>
    <p style="font-size:15px;color:#4b5563;line-height:1.6;margin:0;">${message}</p>
  </main>
</body>
</html>`;
}

const HTML_HEADERS = { "Content-Type": "text/html; charset=utf-8" };

export async function GET(request: NextRequest) {
  const token = request.nextUrl.searchParams.get("token");

  if (!token) {
    return new NextResponse(
      page("Lien invalide", "Ce lien de désinscription est incomplet ou invalide."),
      { status: 404, headers: HTML_HEADERS }
    );
  }

  const prospect = await prisma.prospect.findUnique({
    where: { optOutToken: token },
  });

  if (!prospect) {
    return new NextResponse(
      page("Lien invalide", "Ce lien de désinscription est invalide ou a expiré."),
      { status: 404, headers: HTML_HEADERS }
    );
  }

  await prisma.prospect.update({
    where: { id: prospect.id },
    data: { optOut: true, status: "optout" },
  });

  return new NextResponse(
    page(
      "Désinscription confirmée",
      "Vous ne recevrez plus de messages de notre part."
    ),
    { status: 200, headers: HTML_HEADERS }
  );
}
