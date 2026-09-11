import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { execSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import { resolve } from "node:path";

// Test d'intégration de la state machine contre une base SQLite ISOLÉE
// (jamais dev.db). On câble DATABASE_URL avant d'importer Prisma, puis on
// pousse le schéma sur ce fichier temporaire.

const TEST_DB = ".tmp-test-orchestrator.db";
const TEST_DB_PATH = resolve(__dirname, "../../..", TEST_DB);

// Modules importés dynamiquement APRÈS avoir fixé DATABASE_URL.
type Mods = {
  startRun: typeof import("../orchestrator").startRun;
  resumeRun: typeof import("../orchestrator").resumeRun;
  prisma: typeof import("@/lib/prisma").prisma;
  setMinBudgetThreshold: typeof import("../settings").setMinBudgetThreshold;
  MockJobBoardConnector: typeof import("../connectors").MockJobBoardConnector;
  HeuristicAnalyzer: typeof import("../analyzer").HeuristicAnalyzer;
};
let m: Mods;

beforeAll(async () => {
  process.env.DATABASE_URL = `file:${TEST_DB_PATH}`;
  if (existsSync(TEST_DB_PATH)) rmSync(TEST_DB_PATH);
  execSync(`npx prisma db push --url "file:${TEST_DB_PATH}" --accept-data-loss`, {
    stdio: "ignore",
  });

  const [orch, prismaMod, settings, connectors, analyzer] = await Promise.all([
    import("../orchestrator"),
    import("@/lib/prisma"),
    import("../settings"),
    import("../connectors"),
    import("../analyzer"),
  ]);
  m = {
    startRun: orch.startRun,
    resumeRun: orch.resumeRun,
    prisma: prismaMod.prisma,
    setMinBudgetThreshold: settings.setMinBudgetThreshold,
    MockJobBoardConnector: connectors.MockJobBoardConnector,
    HeuristicAnalyzer: analyzer.HeuristicAnalyzer,
  };

  await m.prisma.freelanceProfile.create({
    data: { name: "Test Dev", skills: "Next.js, TypeScript, Prisma", seniority: "senior", minBudget: 5000, locations: "remote" },
  });
}, 60000);

afterAll(async () => {
  await m?.prisma.$disconnect();
  if (existsSync(TEST_DB_PATH)) rmSync(TEST_DB_PATH);
});

describe("orchestrator (intégration)", () => {
  it("exécute les 5 étapes et produit des matchs", async () => {
    const id = await m.startRun();
    const run = await m.prisma.pipelineRun.findUnique({
      where: { id },
      include: { steps: true, matches: true, analyzed: true },
    });
    expect(run?.status).toBe("completed");
    expect(run?.steps).toHaveLength(5);
    expect(run?.steps.every((s) => s.status === "ok")).toBe(true);
    expect(run?.matches.length).toBeGreaterThan(0);
    // L'offre "scraping Python 200€" doit être rejetée (sous le seuil par défaut 500€).
    expect(run?.analyzed.some((j) => j.status === "rejected")).toBe(true);
  });

  it("marque le run en échec à l'étape fautive PUIS le reprend avec succès", async () => {
    const boom = { extract() { throw new Error("LLM indisponible"); } };
    const id = await m.startRun({ connector: new m.MockJobBoardConnector(), analyzer: boom });

    const failed = await m.prisma.pipelineRun.findUnique({ where: { id }, include: { steps: true, rawJobs: true } });
    expect(failed?.status).toBe("failed");
    expect(failed?.currentStep).toBe(1); // échoue à "filter"
    expect(failed?.rawJobs.length).toBeGreaterThan(0); // l'ingestion (étape 0) a bien persisté
    expect(failed?.error).toContain("filter");

    // Reprise depuis l'étape fautive avec un analyzer sain.
    await m.resumeRun(id);
    const resumed = await m.prisma.pipelineRun.findUnique({ where: { id }, include: { steps: true } });
    expect(resumed?.status).toBe("completed");
    expect(resumed?.steps.filter((s) => s.step === "filter" && s.status === "ok")).toHaveLength(1);
  });

  it("applique la boucle de rétroaction : un seuil élevé rejette davantage d'offres", async () => {
    await m.setMinBudgetThreshold(50000); // au-dessus de toutes les offres mock
    const id = await m.startRun();
    const run = await m.prisma.pipelineRun.findUnique({ where: { id }, include: { analyzed: true } });
    const qualified = run?.analyzed.filter((j) => j.status === "qualified") ?? [];
    // Seules les offres SANS budget précisé peuvent rester qualifiées.
    expect(qualified.every((j) => j.budget === null)).toBe(true);
  });
});
