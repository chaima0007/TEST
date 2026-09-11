import { describe, it, expect } from "vitest";
import { POST } from "../route";

function post(body: unknown): Request {
  return new Request("http://localhost/api/relance/draft", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

describe("POST /api/relance/draft", () => {
  it("rejette un corps JSON invalide (400)", async () => {
    const res = await POST(post("{pas du json") as never);
    expect(res.status).toBe(400);
  });

  it("exige prénom et entreprise (400)", async () => {
    const res = await POST(post({ quote: { firstName: "Sophie" } }) as never);
    expect(res.status).toBe(400);
    const data = await res.json();
    expect(data.error).toMatch(/company/);
  });

  it("génère une séquence de 3 relances", async () => {
    const res = await POST(
      post({ quote: { firstName: "Sophie", company: "Cabinet Durand" } }) as never,
    );
    expect(res.status).toBe(200);
    const s = await res.json();
    expect(s.messages).toHaveLength(3);
    expect(s.generatedBy).toBe("heuristic");
  });

  it("prend en compte l'objection prix", async () => {
    const res = await POST(
      post({ quote: { firstName: "Marc", company: "Studio K", objection: "price" } }) as never,
    );
    expect(res.status).toBe(200);
    const s = await res.json();
    expect(s.messages[1].body).toMatch(/périmètre|budget|enveloppe/i);
  });
});
