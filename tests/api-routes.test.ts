import test from "node:test";
import assert from "node:assert/strict";
import { NextRequest } from "next/server";

import { GET as getCompetitors, POST as postCompetitor } from "@/app/api/competitors/route";
import { GET as getAlerts, PATCH as patchAlerts } from "@/app/api/alerts/route";
import { GET as getStats } from "@/app/api/stats/route";
import { POST as postLogin } from "@/app/api/auth/login/route";

function jsonRequest(url: string, method: string, body: unknown) {
  return new NextRequest(url, {
    method,
    body: JSON.stringify(body),
    headers: { "content-type": "application/json" },
  });
}

test("GET /api/competitors retourne la liste complète", async () => {
  const res = await getCompetitors();
  assert.equal(res.status, 200);
  const data = await res.json();
  assert.equal(data.length, 5);
  assert.ok(data.every((c: { id: string; name: string }) => c.id && c.name));
});

test("POST /api/competitors sans nom -> 400", async () => {
  const res = await postCompetitor(
    jsonRequest("http://localhost/api/competitors", "POST", { website: "exemple.com" }),
  );
  assert.equal(res.status, 400);
});

test("POST /api/competitors valide -> 201 avec valeurs par défaut", async () => {
  const res = await postCompetitor(
    jsonRequest("http://localhost/api/competitors", "POST", {
      name: "Attio",
      website: "attio.com",
    }),
  );
  assert.equal(res.status, 201);
  const created = await res.json();
  assert.equal(created.logo, "AT");
  assert.equal(created.threatLevel, "medium");
  assert.equal(created.industry, "Non spécifié");
});

test("GET /api/alerts retourne les alertes", async () => {
  const res = await getAlerts();
  assert.equal(res.status, 200);
  const data = await res.json();
  assert.ok(Array.isArray(data) && data.length > 0);
});

test("PATCH /api/alerts markAllRead -> success", async () => {
  const res = await patchAlerts(
    jsonRequest("http://localhost/api/alerts", "PATCH", { markAllRead: true }),
  );
  assert.equal((await res.json()).success, true);
});

test("PATCH /api/alerts avec id connu -> isRead true", async () => {
  const res = await patchAlerts(jsonRequest("http://localhost/api/alerts", "PATCH", { id: "1" }));
  assert.equal(res.status, 200);
  assert.equal((await res.json()).isRead, true);
});

test("PATCH /api/alerts avec id inconnu -> 404", async () => {
  const res = await patchAlerts(
    jsonRequest("http://localhost/api/alerts", "PATCH", { id: "inexistant" }),
  );
  assert.equal(res.status, 404);
});

test("PATCH /api/alerts sans id ni markAllRead -> 400", async () => {
  const res = await patchAlerts(jsonRequest("http://localhost/api/alerts", "PATCH", {}));
  assert.equal(res.status, 400);
});

test("GET /api/stats retourne le tableau de bord", async () => {
  const res = await getStats();
  const data = await res.json();
  assert.equal(typeof data.competitors, "number");
  assert.ok(data.recentAlerts.length <= 3);
  assert.ok(data.recentCompetitors.length <= 5);
});

test("POST /api/auth/login avec mauvais identifiants -> 401", async () => {
  const res = await postLogin(
    jsonRequest("http://localhost/api/auth/login", "POST", {
      email: "intrus@exemple.com",
      password: "mauvais",
    }),
  );
  assert.equal(res.status, 401);
});

test("POST /api/auth/login avec identifiants démo -> cookie de session httpOnly", async () => {
  const res = await postLogin(
    jsonRequest("http://localhost/api/auth/login", "POST", {
      email: "demo@competeiq.com",
      password: "demo123",
    }),
  );
  assert.equal(res.status, 200);
  const cookie = res.headers.get("set-cookie") ?? "";
  assert.match(cookie, /ciq_session=authenticated/);
  assert.match(cookie, /HttpOnly/i);
});

test("POST /api/auth/login avec corps invalide -> 401 (pas de crash)", async () => {
  const res = await postLogin(
    new NextRequest("http://localhost/api/auth/login", { method: "POST", body: "pas du json" }),
  );
  assert.equal(res.status, 401);
});
