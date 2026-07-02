// CLI du module Prospection CompeteIQ.
//
// Usage :
//   npm run outreach:discover -- "plombier,restaurant" "Lyon,Villeurbanne"
//   npm run outreach:run     -> traite la file (relances/brouillons) en dry-run
//   npm run outreach:send    -> identique mais envoi réel (--live)
//
// Lancé via tsx (hors de Next.js) : on charge donc .env / .env.local
// manuellement avant d'importer le pipeline, sans écraser les variables
// déjà présentes dans l'environnement.

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import type { AgentSummary, OrchestratorReport } from "../lib/outreach/types";

function loadEnvFiles(): void {
  for (const file of [".env", ".env.local"]) {
    let content: string;
    try {
      content = readFileSync(resolve(process.cwd(), file), "utf8");
    } catch {
      continue; // fichier absent : rien à faire
    }
    for (const rawLine of content.split("\n")) {
      const line = rawLine.trim();
      if (!line || line.startsWith("#")) continue;
      const eq = line.indexOf("=");
      if (eq <= 0) continue;
      const key = line.slice(0, eq).trim();
      let value = line.slice(eq + 1).trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      if (key && process.env[key] === undefined) process.env[key] = value;
    }
  }
}

function parseList(raw: string | undefined): string[] {
  return (raw ?? "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function formatCounters(step: AgentSummary): string {
  const parts: string[] = [`processed=${step.processed}`];
  if (step.created !== undefined) parts.push(`created=${step.created}`);
  if (step.skipped !== undefined) parts.push(`skipped=${step.skipped}`);
  if (step.sent !== undefined) parts.push(`sent=${step.sent}`);
  if (step.failed !== undefined) parts.push(`failed=${step.failed}`);
  return parts.join("  ");
}

function printReport(report: OrchestratorReport): void {
  const mode = report.dryRun
    ? "DRY-RUN (aucun email envoyé)"
    : "LIVE (envoi réel)";
  console.log("");
  console.log(`Rapport du pipeline — mode ${mode}`);
  console.log(`Début : ${report.startedAt}`);
  console.log(`Fin   : ${report.finishedAt}`);
  console.log("");
  for (const step of report.steps) {
    console.log(`  ${step.agent.padEnd(14)} ${formatCounters(step)}`);
    for (const detail of step.details ?? []) {
      console.log(`      - ${detail}`);
    }
  }
  console.log("");
}

function printUsage(): void {
  console.log(
    [
      "Usage : tsx scripts/outreach.ts <commande>",
      "",
      "Commandes :",
      '  discover <catégories> <villes>   Découvre via Google Places, qualifie et',
      "                                   prépare les brouillons (toujours en dry-run).",
      "                                   Listes séparées par des virgules.",
      '                                   Ex : discover "plombier,restaurant" "Lyon,Villeurbanne"',
      "  run [--live]                     Traite la file (envois/relances dus).",
      "                                   Dry-run par défaut ; --live pour envoyer réellement.",
      "",
      "Scripts npm équivalents :",
      '  npm run outreach:discover -- "plombier,restaurant" "Lyon,Villeurbanne"',
      "  npm run outreach:run",
      "  npm run outreach:send            (= run --live)",
    ].join("\n")
  );
}

async function main(): Promise<void> {
  const [, , command, arg1, arg2] = process.argv;

  if (command !== "discover" && command !== "run") {
    if (command) console.error(`Commande inconnue : "${command}"`);
    printUsage();
    process.exitCode = 1;
    return;
  }

  loadEnvFiles();

  // Import dynamique APRÈS le chargement des .env : la config du module
  // (lib/outreach/config.ts) lit process.env au moment de l'import.
  const { runPipeline } = await import("../lib/outreach/agents/orchestrator");

  if (command === "discover") {
    const categories = parseList(arg1);
    const cities = parseList(arg2);
    if (categories.length === 0 || cities.length === 0) {
      console.error(
        'Erreur : la commande "discover" attend des catégories et des villes.'
      );
      printUsage();
      process.exitCode = 1;
      return;
    }
    console.log(
      `Découverte (dry-run) — catégories : ${categories.join(", ")} — villes : ${cities.join(", ")}`
    );
    const report = await runPipeline({ categories, cities, dryRun: true });
    printReport(report);
    return;
  }

  // command === "run"
  const live = process.argv.includes("--live");
  console.log(
    live
      ? "Traitement de la file — mode LIVE : les emails vont réellement partir."
      : "Traitement de la file — mode dry-run (utiliser --live pour envoyer)."
  );
  const report = await runPipeline({
    categories: [],
    cities: [],
    skipDiscovery: true,
    dryRun: !live,
  });
  printReport(report);
}

main().catch((error: unknown) => {
  console.error("Échec du pipeline :", error);
  process.exitCode = 1;
});
