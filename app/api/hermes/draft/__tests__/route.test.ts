import { describe, it, expect } from "vitest";
import { POST } from "../route";
import { NOTE_CAP } from "@/lib/agents/hermes";

// Sans ANTHROPIC_API_KEY en test → HERMES retombe sur l'heuristique déterministe.
// Ces tests couvrent la GLUE de la route (validation + fusion d'offre), pas le
// rédacteur lui-même (déjà couvert par lib/agents/__tests__/hermes.test.ts).

function post(body: unknown): Request {
  return new Request("http://localhost/api/hermes/draft", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

describe("POST /api/hermes/draft", () => {
  it("rejette un corps JSON invalide (400)", async () => {
    const res = await POST(post("{pas du json") as never);
    expect(res.status).toBe(400);
  });

  it("exige prénom et entreprise (400)", async () => {
    const res = await POST(post({ prospect: { firstName: "Sophie" } }) as never);
    expect(res.status).toBe(400);
    const data = await res.json();
    expect(data.error).toMatch(/company/);
  });

  it("génère les 4 brouillons pour un prospect valide", async () => {
    const res = await POST(
      post({ prospect: { firstName: "Sophie", company: "Cabinet Durand" } }) as never,
    );
    expect(res.status).toBe(200);
    const d = await res.json();
    expect(d.connectionNote).toContain("Sophie");
    expect(d.connectionNote.length).toBeLessThanOrEqual(NOTE_CAP);
    expect(d.firstMessage).toContain("Cabinet Durand");
    expect(d.firstMessage).toMatch(/500\s?€/u);
    expect(d.followUp.length).toBeGreaterThan(0);
    expect(d.generatedBy).toBe("heuristic");
  });

  it("respecte une offre personnalisée (prix)", async () => {
    const res = await POST(
      post({
        prospect: { firstName: "Marc", company: "Studio K" },
        offer: { price: 1500 },
      }) as never,
    );
    expect(res.status).toBe(200);
    const d = await res.json();
    expect(d.firstMessage).toMatch(/1\s?500\s?€/u);
  });

  it("ignore un prix d'offre non numérique et garde 500 €", async () => {
    const res = await POST(
      post({
        prospect: { firstName: "Marc", company: "Studio K" },
        offer: { price: "gratuit" },
      }) as never,
    );
    expect(res.status).toBe(200);
    const d = await res.json();
    expect(d.firstMessage).toMatch(/500\s?€/u);
  });
});
