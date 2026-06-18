import { describe, it, expect } from "vitest";
import { decide, simulatePlan, type Plan } from "../commandant";
import { checkPlan } from "../compliance";
import { diagnose } from "../resolveur";
import { FLEET, premiumAgents } from "../registry";

const compliantPlan: Plan = {
  id: "cible",
  label: "Prospection ciblée conforme",
  price: 500,
  cost: 50,
  funnel: { messagesTotal: 25, replyRate: 0.18, callRate: 0.4, closeRate: 0.35 },
  actions: [{ agent: "HERMES", channel: "linkedin", outboundPerDay: 5, gdprLawfulBasis: true }],
};

const nonCompliantPlan: Plan = {
  id: "scraping",
  label: "Volume par scraping",
  price: 500,
  cost: 0,
  funnel: { messagesTotal: 400, replyRate: 0.05, callRate: 0.2, closeRate: 0.2 },
  actions: [{ agent: "HERMES", channel: "linkedin", outboundPerDay: 200, automatedScraping: true }],
};

describe("compliance", () => {
  it("rejette le scraping et le dépassement de plafond", () => {
    const r = checkPlan(nonCompliantPlan.actions);
    expect(r.compliant).toBe(false);
    expect(r.violations.length).toBeGreaterThanOrEqual(2);
  });
  it("accepte une prospection manuelle conforme", () => {
    expect(checkPlan(compliantPlan.actions).compliant).toBe(true);
  });
});

describe("COMMANDANT.simulatePlan", () => {
  it("est déterministe à seed fixe", () => {
    const a = simulatePlan(compliantPlan, { trials: 50, seed: 3 });
    const b = simulatePlan(compliantPlan, { trials: 50, seed: 3 });
    expect(a).toEqual(b);
  });
  it("calcule le profit attendu = revenu − coût", () => {
    const s = simulatePlan(compliantPlan, { trials: 200, seed: 1 });
    expect(s.expectedProfit).toBe(s.expectedRevenue - s.cost);
  });
});

describe("COMMANDANT.decide", () => {
  it("écarte les plans non conformes et recommande un plan conforme", () => {
    const d = decide("1 client à 500€", [compliantPlan, nonCompliantPlan], { trials: 50, seed: 1 });
    expect(d.recommended?.planId).toBe("cible");
    expect(d.eligible.every((p) => p.compliance.compliant)).toBe(true);
    expect(d.eligible.find((p) => p.planId === "scraping")).toBeUndefined();
  });
});

describe("RÉSOLVEUR.diagnose", () => {
  it("propose une reprise pour un run en échec", () => {
    const r = diagnose({ type: "run_failed", runId: "r1", failedStep: "filter" });
    expect(r.autoApplicable).toBe(true);
    expect(r.fix.toLowerCase()).toContain("reprendre");
  });
});

describe("registry", () => {
  it("contient 11 agents dont 2 premium (COMMANDANT, RÉSOLVEUR)", () => {
    expect(FLEET).toHaveLength(11);
    expect(premiumAgents().map((a) => a.id).sort()).toEqual(["commandant", "resolveur"]);
  });
});
