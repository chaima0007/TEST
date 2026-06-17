// ─── Orchestrateur — state machine séquentielle reprenable ───────────────────
//
// Enchaîne les 5 étapes. L'état vit en base (PipelineRun.currentStep + logs),
// donc si une étape échoue, le run est marqué "failed" à l'étape fautive et
// peut être REPRIS plus tard via resumeRun() sans tout recommencer.

import { prisma } from "@/lib/prisma";
import { defaultDeps, ingestStep, filterStep, matchStep, enrichStep, notifyStep, type StepDeps } from "./steps";

type StepFn = (runId: string, deps: StepDeps) => Promise<string>;

export const STEPS: { name: string; run: StepFn }[] = [
  { name: "ingest", run: (id, d) => ingestStep(id, d) },
  { name: "filter", run: (id, d) => filterStep(id, d) },
  { name: "match", run: (id) => matchStep(id) },
  { name: "enrich", run: (id) => enrichStep(id) },
  { name: "notify", run: (id) => notifyStep(id) },
];

async function runFrom(runId: string, fromIndex: number, deps: StepDeps): Promise<string> {
  for (let i = fromIndex; i < STEPS.length; i++) {
    const step = STEPS[i];
    await prisma.pipelineRun.update({ where: { id: runId }, data: { currentStep: i } });
    const started = Date.now();
    try {
      const message = await step.run(runId, deps);
      await prisma.pipelineStepLog.create({
        data: { runId, step: step.name, status: "ok", message, durationMs: Date.now() - started },
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      await prisma.pipelineStepLog.create({
        data: { runId, step: step.name, status: "failed", message, durationMs: Date.now() - started },
      });
      await prisma.pipelineRun.update({
        where: { id: runId },
        data: { status: "failed", error: `Étape « ${step.name} » : ${message}`, finishedAt: new Date() },
      });
      return runId;
    }
  }
  await prisma.pipelineRun.update({
    where: { id: runId },
    data: { status: "completed", currentStep: STEPS.length, finishedAt: new Date() },
  });
  return runId;
}

/** Démarre un nouveau run complet et renvoie son id. */
export async function startRun(deps: StepDeps = defaultDeps): Promise<string> {
  const run = await prisma.pipelineRun.create({ data: { status: "running", currentStep: 0 } });
  return runFrom(run.id, 0, deps);
}

/** Reprend un run en échec depuis l'étape fautive. */
export async function resumeRun(runId: string, deps: StepDeps = defaultDeps): Promise<string> {
  const run = await prisma.pipelineRun.findUnique({ where: { id: runId } });
  if (!run) throw new Error(`Run introuvable : ${runId}`);
  if (run.status === "completed") return runId;
  await prisma.pipelineRun.update({ where: { id: runId }, data: { status: "running", error: null } });
  return runFrom(runId, run.currentStep, deps);
}
