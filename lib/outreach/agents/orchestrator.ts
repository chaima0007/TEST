// Orchestrateur : enchaîne les agents (scout → qualifier → copywriter →
// sequencer → mailer) et trace chaque exécution dans AgentRun.
// Une erreur d'un agent n'interrompt jamais la suite du pipeline.

import { prisma } from "../../db";
import { outreach } from "../config";
import type { AgentName, AgentSummary, OrchestratorReport } from "../types";
import { runScout } from "./scout";
import { runQualifier } from "./qualifier";
import { runCopywriter } from "./copywriter";
import { runSequencer } from "./sequencer";
import { runMailer } from "./mailer";

export async function withAgentRun<T>(
  agentName: AgentName,
  input: unknown,
  fn: () => Promise<T>
): Promise<T> {
  const run = await prisma.agentRun.create({
    data: {
      agent: agentName,
      status: "running",
      input: JSON.stringify(input ?? null),
    },
  });

  try {
    const result = await fn();
    await prisma.agentRun.update({
      where: { id: run.id },
      data: {
        status: "success",
        output: JSON.stringify(result ?? null),
        finishedAt: new Date(),
      },
    });
    return result;
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    await prisma.agentRun.update({
      where: { id: run.id },
      data: { status: "error", error: message, finishedAt: new Date() },
    });
    throw err;
  }
}

export async function runPipeline(params: {
  categories: string[];
  cities: string[];
  dryRun?: boolean;
  skipDiscovery?: boolean;
}): Promise<OrchestratorReport> {
  const dryRun = params.dryRun ?? outreach.dryRun;

  return withAgentRun("orchestrator", params, async () => {
    const startedAt = new Date().toISOString();
    const steps: AgentSummary[] = [];

    // Exécute un agent tracé ; en cas d'erreur, on logge et on continue
    const safeRun = async (
      agent: AgentName,
      input: unknown,
      fn: () => Promise<AgentSummary>
    ) => {
      try {
        steps.push(await withAgentRun(agent, input, fn));
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        steps.push({ agent, processed: 0, details: [message] });
      }
    };

    const discover =
      !params.skipDiscovery && params.categories.length > 0 && params.cities.length > 0;

    if (discover) {
      const scoutParams = { categories: params.categories, cities: params.cities };
      await safeRun("scout", scoutParams, () => runScout(scoutParams));
      await safeRun("qualifier", null, runQualifier);
    }

    await safeRun("copywriter", null, runCopywriter);
    await safeRun("sequencer", null, runSequencer);
    await safeRun("mailer", { dryRun }, () => runMailer(dryRun));

    return {
      startedAt,
      finishedAt: new Date().toISOString(),
      dryRun,
      steps,
    };
  });
}
