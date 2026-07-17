import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[leads] SWARM_API_URL non défini — mode local");
}
// Route Handler — capture de leads (Caelum). AUCUN credential dans le code.
// La donnée est transmise au webhook défini par la variable d'environnement LEADS_WEBHOOK_URL
// (Zapier, Make, CRM, Google Form, etc.). Sans webhook configuré, la requête est acceptée
// (UX préservée) mais aucune donnée personnelle n'est stockée dans le dépôt.

export async function POST(request: Request) {
  let body: { email?: string; profil?: unknown; normes?: unknown };
  try {
    body = await request.json();
  } catch {
    return Response.json({ ok: false, error: "Requête invalide." }, { status: 400 });
  }

  const email = (body.email || "").toString().trim();
  const emailValide = email.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  if (!emailValide) {
    return Response.json({ ok: false, error: "Adresse e-mail invalide." }, { status: 422 });
  }

  // Garde-fou anti-abus (taille des champs) avant tout traitement/transfert.
  const source = ((body as { source?: string }).source ?? "site").toString().slice(0, 60);
  const tropGros = JSON.stringify(body.profil ?? "").length > 4000 || JSON.stringify(body.normes ?? "").length > 4000;
  if (tropGros) {
    return Response.json({ ok: false, error: "Charge utile trop volumineuse." }, { status: 413 });
  }

  const webhook = process.env.LEADS_WEBHOOK_URL;
  if (webhook) {
    try {
      await fetch(webhook, {
        method: "POST",
        cache: "no-store", // webhook POST : ne jamais mettre en cache
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          profil: body.profil ?? null,
          normes: body.normes ?? null,
          source,
          recu_le: new Date().toISOString(),
        }),
      });
    } catch {
      // On n'expose pas l'échec côté client : le lead reste « accepté », à reprendre côté webhook.
      return Response.json(sealResponse({ ok: true, stored: false }));
    }
    return Response.json(sealResponse({ ok: true, stored: true }));
  }

  // Pas de webhook configuré : on accepte sans stocker de données personnelles.
  return Response.json(sealResponse({ ok: true, stored: false }));
}
