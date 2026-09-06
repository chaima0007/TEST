/**
 * Parcours d'authentification — tests de non-régression.
 *
 * Périmètre : POST /api/auth/login, POST /api/auth/logout, et le middleware
 * qui garde les routes protégées. Ce sont les trois seuls points par lesquels
 * un utilisateur non authentifié peut atteindre les données.
 *
 * Aucune dépendance ajoutée : lanceur de tests natif de Node (`node:test`),
 * exécuté en TypeScript par `tsx`, déjà présent en devDependency.
 */
import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { NextRequest } from "next/server";

import { POST as login } from "../app/api/auth/login/route";
import { POST as logout } from "../app/api/auth/logout/route";
import { middleware } from "../middleware";

const ORIGIN = "http://localhost:3000";

// Identifiants par défaut du code (app/api/auth/login/route.ts).
const VALID = { email: "demo@competeiq.com", password: "demo123" };

function loginRequest(body: unknown): NextRequest {
  return new NextRequest(new URL("/api/auth/login", ORIGIN), {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

function pageRequest(path: string, cookie?: string): NextRequest {
  const req = new NextRequest(new URL(path, ORIGIN));
  if (cookie !== undefined) req.cookies.set("ciq_session", cookie);
  return req;
}

describe("POST /api/auth/login — refus", () => {
  test("mot de passe incorrect : 401 et aucun cookie de session", async () => {
    const res = await login(loginRequest({ ...VALID, password: "mauvais" }));
    assert.equal(res.status, 401);
    assert.equal(res.cookies.get("ciq_session"), undefined);
  });

  test("email inconnu : 401", async () => {
    const res = await login(loginRequest({ email: "autre@example.com", password: VALID.password }));
    assert.equal(res.status, 401);
  });

  test("corps JSON malformé : 401, jamais une erreur 500", async () => {
    // Un crash ici serait exploitable en déni de service : on vérifie la
    // dégradation propre, pas seulement l'absence de succès.
    const res = await login(loginRequest("{ pas du json"));
    assert.equal(res.status, 401);
  });

  test("corps vide : 401", async () => {
    const res = await login(loginRequest({}));
    assert.equal(res.status, 401);
  });

  test("types non-string : 401 (pas de comparaison entre objets)", async () => {
    for (const body of [
      { email: {}, password: {} },
      { email: [], password: [] },
      { email: VALID.email, password: null },
      { email: 0, password: 0 },
    ]) {
      const res = await login(loginRequest(body));
      assert.equal(res.status, 401, `devrait refuser : ${JSON.stringify(body)}`);
    }
  });

  test("le mot de passe est sensible à la casse", async () => {
    const res = await login(loginRequest({ ...VALID, password: VALID.password.toUpperCase() }));
    assert.equal(res.status, 401);
  });
});

describe("POST /api/auth/login — succès", () => {
  test("identifiants valides : 200 et cookie de session posé", async () => {
    const res = await login(loginRequest(VALID));
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true });
    assert.ok(res.cookies.get("ciq_session"), "le cookie ciq_session doit être posé");
  });

  test("le cookie de session est httpOnly, sameSite lax et sur tout le site", async () => {
    // httpOnly protège le cookie du vol par script injecté : régression silencieuse
    // si quelqu'un retire l'option un jour.
    const cookie = (await login(loginRequest(VALID))).cookies.get("ciq_session");
    assert.equal(cookie?.httpOnly, true);
    assert.equal(cookie?.sameSite, "lax");
    assert.equal(cookie?.path, "/");
    assert.equal(cookie?.maxAge, 60 * 60 * 24 * 7);
  });

  test("email insensible à la casse et aux espaces", async () => {
    const res = await login(loginRequest({ email: "  DEMO@CompeteIQ.com  ", password: VALID.password }));
    assert.equal(res.status, 200);
  });
});

describe("POST /api/auth/logout", () => {
  test("vide le cookie de session avec maxAge 0", async () => {
    const cookie = (await logout()).cookies.get("ciq_session");
    assert.equal(cookie?.value, "");
    assert.equal(cookie?.maxAge, 0);
    assert.equal(cookie?.path, "/", "sans le même path, le cookie n'est pas réellement supprimé");
  });
});

describe("middleware — garde des routes protégées", () => {
  test("laisse passer les routes publiques sans cookie", () => {
    for (const path of ["/", "/login", "/pitch", "/api/auth/login"]) {
      const res = middleware(pageRequest(path));
      assert.equal(res.headers.get("location"), null, `${path} ne doit pas rediriger`);
    }
  });

  test("redirige vers /login sans cookie, en conservant la destination", () => {
    const res = middleware(pageRequest("/dashboard/competitors"));
    const location = new URL(res.headers.get("location")!);
    assert.equal(location.pathname, "/login");
    assert.equal(location.searchParams.get("next"), "/dashboard/competitors");
  });

  test("protège les routes d'API de données, pas seulement les pages", () => {
    // Une redirection HTML sur un appel d'API est discutable, mais l'important
    // ici est qu'aucune donnée ne sorte : on vérifie qu'il n'y a pas de laissez-passer.
    for (const path of ["/api/competitors", "/api/alerts", "/api/reports", "/api/stats"]) {
      const res = middleware(pageRequest(path));
      assert.ok(res.headers.get("location"), `${path} doit être gardé`);
    }
  });

  test("cookie vide : traité comme non authentifié", () => {
    const res = middleware(pageRequest("/dashboard", ""));
    assert.ok(res.headers.get("location"), "un cookie vide ne doit pas valoir session");
  });

  test("cookie de session présent : accès autorisé", () => {
    const res = middleware(pageRequest("/dashboard", "authenticated"));
    assert.equal(res.headers.get("location"), null);
  });
});

describe("FAILLE CONNUE — session non signée (voir codex/A-DECIDER.md)", () => {
  test("n'importe quelle valeur de cookie ouvre les routes protégées", () => {
    // Ce test DOCUMENTE le comportement actuel, il ne le valide pas.
    // Le middleware ne vérifie que la PRÉSENCE du cookie, et sa valeur est la
    // constante "authenticated" : un visiteur peut la fabriquer lui-même.
    // Quand la session sera signée, ce test échouera — c'est voulu :
    // il faudra alors le remplacer par l'assertion inverse.
    const res = middleware(pageRequest("/dashboard", "n-importe-quoi"));
    assert.equal(
      res.headers.get("location"),
      null,
      "Si ce test échoue, la session est enfin validée : inverser l'assertion et supprimer ce bloc.",
    );
  });
});
