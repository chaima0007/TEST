import test from "node:test";
import assert from "node:assert/strict";

import { competitors, alerts, reports, stats } from "@/lib/data";

test("les concurrents ont des ids uniques", () => {
  const ids = competitors.map((c) => c.id);
  assert.equal(new Set(ids).size, ids.length);
});

test("les niveaux de menace sont valides", () => {
  for (const c of competitors) {
    assert.ok(["high", "medium", "low"].includes(c.threatLevel), `${c.name}: ${c.threatLevel}`);
  }
});

test("chaque concurrent a 12 mois d'historique de prix", () => {
  for (const c of competitors) {
    assert.equal(c.priceHistory.length, 12, c.name);
  }
});

test("les prix des plans sont positifs ou nuls", () => {
  for (const c of competitors) {
    for (const plan of c.pricing) {
      assert.ok(plan.price >= 0, `${c.name} / ${plan.name}`);
    }
  }
});

test("stats.competitorsTracked correspond au nombre de concurrents", () => {
  assert.equal(stats.competitorsTracked, competitors.length);
});

test("les alertes et rapports ont des ids uniques", () => {
  const alertIds = alerts.map((a) => a.id);
  assert.equal(new Set(alertIds).size, alertIds.length);
  const reportIds = reports.map((r) => r.id);
  assert.equal(new Set(reportIds).size, reportIds.length);
});
