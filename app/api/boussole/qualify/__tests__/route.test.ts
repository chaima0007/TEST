import { describe, it, expect } from "vitest";
import { POST } from "../route";

function post(body: unknown): Request {
  return new Request("http://localhost/api/boussole/qualify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

describe("POST /api/boussole/qualify", () => {
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

  it("qualifie un lead chaud en fit ÉLEVÉE", async () => {
    const res = await POST(
      post({
        lead: {
          firstName: "Sophie",
          company: "Cabinet Durand",
          needClear: true,
          budgetSignal: true,
          timing: "now",
          decisionMaker: true,
          hasWebsite: "outdated",
        },
      }) as never,
    );
    expect(res.status).toBe(200);
    const q = await res.json();
    expect(q.fit).toBe("ÉLEVÉE");
    expect(q.priority).toBe("haute");
    expect(Array.isArray(q.reasons)).toBe(true);
  });

  it("ignore un timing invalide (traité comme inconnu)", async () => {
    const res = await POST(
      post({ lead: { firstName: "Marc", company: "Studio K", timing: "demain" } }) as never,
    );
    expect(res.status).toBe(200);
    const q = await res.json();
    expect(q.fit).toBe("FAIBLE");
  });
});
