import test from "node:test";
import assert from "node:assert/strict";
import { NextRequest } from "next/server";

import { middleware } from "@/middleware";

test("une route protégée sans session redirige vers /login", () => {
  const res = middleware(new NextRequest("http://localhost/dashboard"));
  assert.equal(res.status, 307);
  const location = new URL(res.headers.get("location") ?? "");
  assert.equal(location.pathname, "/login");
  assert.equal(location.searchParams.get("next"), "/dashboard");
});

test("une route API protégée sans session redirige aussi", () => {
  const res = middleware(new NextRequest("http://localhost/api/stats"));
  assert.equal(res.status, 307);
});

test("une route protégée avec session passe", () => {
  const req = new NextRequest("http://localhost/dashboard", {
    headers: { cookie: "ciq_session=authenticated" },
  });
  const res = middleware(req);
  assert.equal(res.status, 200);
  assert.equal(res.headers.get("x-middleware-next"), "1");
});

test("une route publique passe sans session", () => {
  const res = middleware(new NextRequest("http://localhost/login"));
  assert.equal(res.status, 200);
});
