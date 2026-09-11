import { describe, it, expect } from "vitest";
import { POST } from "../route";

// Sans ANTHROPIC_API_KEY → PACTE retombe sur l'heuristique déterministe.
// Ces tests couvrent la GLUE de la route (validation + fusion d'offre).

function post(body: unknown): Request {
  return new Request("http://localhost/api/pacte/draft", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

describe("POST /api/pacte/draft", () => {
  it("rejette un corps JSON invalide (400)", async () => {
    const res = await POST(post("{pas du json") as never);
    expect(res.status).toBe(400);
  });

  it("exige prénom et entreprise (400)", async () => {
    const res = await POST(post({ lead: { firstName: "Sophie" } }) as never);
    expect(res.status).toBe(400);
    const data = await res.json();
    expect(data.error).toMatch(/company/);
  });

  it("génère un devis pour un lead valide (prix 500 €, facturation À CONFIRMER)", async () => {
    const res = await POST(
      post({ lead: { firstName: "Sophie", company: "Cabinet Durand" } }) as never,
    );
    expect(res.status).toBe(200);
    const p = await res.json();
    expect(p.subject).toContain("Cabinet Durand");
    expect(p.priceLine).toMatch(/500\s?€/u);
    expect(p.terms.join("\n")).toMatch(/À CONFIRMER/);
    expect(p.generatedBy).toBe("heuristic");
  });

  it("respecte une offre personnalisée (prix)", async () => {
    const res = await POST(
      post({ lead: { firstName: "Marc", company: "Studio K" }, offer: { price: 3000 } }) as never,
    );
    expect(res.status).toBe(200);
    const p = await res.json();
    expect(p.priceLine).toMatch(/3\s?000\s?€/u);
  });
});
