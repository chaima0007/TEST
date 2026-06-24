import { NextResponse } from "next/server";

// Réception des inscriptions à la liste d'attente / demandes de contact.
// Stockage minimal en mémoire process (à brancher sur une vraie base ou un
// service email en production — ex: Resend, un webhook, ou Prisma).
interface Lead {
  name: string;
  email: string;
  company?: string;
  message?: string;
  tier?: string;
  ts: string;
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const name = String(body.name ?? "").trim();
    const email = String(body.email ?? "").trim();

    if (!name || !email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return NextResponse.json(
        { ok: false, error: "Nom et email valides requis." },
        { status: 400 },
      );
    }

    const lead: Lead = {
      name,
      email,
      company: String(body.company ?? "").trim() || undefined,
      message: String(body.message ?? "").trim() || undefined,
      tier: String(body.tier ?? "").trim() || undefined,
      ts: new Date().toISOString(),
    };

    // En production : persister (DB) ou notifier (email/webhook).
    // Ici on journalise simplement côté serveur.
    console.log("[waitlist] nouvelle inscription:", JSON.stringify(lead));

    return NextResponse.json({ ok: true, message: "Inscription reçue. Merci !" });
  } catch {
    return NextResponse.json(
      { ok: false, error: "Requête invalide." },
      { status: 400 },
    );
  }
}
