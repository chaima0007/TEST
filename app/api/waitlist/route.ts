import { NextResponse } from "next/server";

// Réception et lecture des demandes clients (liste d'attente / contact).
//
// ⚠️ Stockage en mémoire du process (volatile). Suffisant pour visualiser le
// fonctionnement et en développement. En PRODUCTION, brancher sur une vraie
// base (Prisma/LibSQL/Turso) ou un service email pour une persistance durable.
interface Lead {
  id: string;
  name: string;
  email: string;
  company?: string;
  message?: string;
  tier?: string;
  status: "nouveau" | "en_cours" | "termine";
  ts: string;
}

// Magasin en mémoire (partagé entre requêtes d'une même instance)
const globalStore = globalThis as unknown as { __leads?: Lead[] };
if (!globalStore.__leads) globalStore.__leads = [];
const leads = globalStore.__leads;

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
      id: Math.random().toString(36).slice(2, 10),
      name,
      email,
      company: String(body.company ?? "").trim() || undefined,
      message: String(body.message ?? "").trim() || undefined,
      tier: String(body.tier ?? "").trim() || undefined,
      status: "nouveau",
      ts: new Date().toISOString(),
    };

    leads.unshift(lead); // plus récent en premier
    if (leads.length > 500) leads.length = 500;
    console.log("[waitlist] nouvelle demande:", JSON.stringify(lead));

    return NextResponse.json({ ok: true, message: "Demande reçue. Merci !" });
  } catch {
    return NextResponse.json({ ok: false, error: "Requête invalide." }, { status: 400 });
  }
}

// Lecture pour l'espace de gestion
export async function GET() {
  return NextResponse.json({
    ok: true,
    leads,
    counts: {
      total: leads.length,
      nouveau: leads.filter((l) => l.status === "nouveau").length,
      en_cours: leads.filter((l) => l.status === "en_cours").length,
      termine: leads.filter((l) => l.status === "termine").length,
    },
  });
}
