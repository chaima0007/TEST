// ─── Les 5 étapes du pipeline ────────────────────────────────────────────────
//
// Chaque étape est une fonction isolée qui lit l'état persisté du run (scopé par
// runId) et écrit le suivant. Aucune étape n'appelle une autre : l'orchestrateur
// les enchaîne. Une étape renvoie un message court (journalisé + affiché dans
// l'UI comme "décision de l'IA").

import { prisma } from "@/lib/prisma";
import { MockJobBoardConnector, type SourceConnector } from "./connectors";
import { HeuristicAnalyzer, type Analyzer } from "./analyzer";
import { scoreMatch, buildSnippet } from "./matcher";
import { getMinBudgetThreshold } from "./settings";

export interface StepDeps {
  connector: SourceConnector;
  analyzer: Analyzer;
}

export const defaultDeps: StepDeps = {
  connector: new MockJobBoardConnector(),
  analyzer: new HeuristicAnalyzer(),
};

const csv = (s: string) => s.split(",").map((x) => x.trim()).filter(Boolean);

// Étape 1 — Ingestion : récupère les offres et les stocke en brut.
export async function ingestStep(runId: string, deps: StepDeps): Promise<string> {
  const jobs = await deps.connector.fetchJobs();
  for (const j of jobs) {
    await prisma.rawJob.upsert({
      where: { runId_source_externalId: { runId, source: j.source, externalId: j.externalId } },
      create: { runId, source: j.source, externalId: j.externalId, title: j.title, description: j.description, rawBudget: j.rawBudget },
      update: { title: j.title, description: j.description, rawBudget: j.rawBudget },
    });
  }
  return `${jobs.length} offre(s) ingérée(s) depuis « ${deps.connector.name} ».`;
}

// Étape 2 — Filtrage/Extraction : extrait les entités et qualifie/rejette.
export async function filterStep(runId: string, deps: StepDeps): Promise<string> {
  const threshold = await getMinBudgetThreshold();
  const raws = await prisma.rawJob.findMany({ where: { runId } });
  let qualified = 0;
  let rejected = 0;

  for (const raw of raws) {
    const fields = deps.analyzer.extract({
      externalId: raw.externalId,
      source: raw.source,
      title: raw.title,
      description: raw.description,
      rawBudget: raw.rawBudget ?? undefined,
    });

    let status = "qualified";
    let reason = "Offre qualifiée.";
    if (fields.skills.length === 0) {
      status = "rejected";
      reason = "Rejetée : aucune compétence technique identifiée.";
    } else if (fields.budget !== null && fields.budget < threshold) {
      status = "rejected";
      reason = `Rejetée : budget ${fields.budget}€ sous le seuil de ${threshold}€.`;
    } else if (fields.budget === null) {
      reason = "Qualifiée (budget non précisé, à confirmer).";
    } else {
      reason = `Qualifiée : budget ${fields.budget}€, ${fields.skills.length} compétence(s).`;
    }

    if (status === "qualified") qualified++;
    else rejected++;

    await prisma.analyzedJob.upsert({
      where: { runId_rawSource_rawExternal: { runId, rawSource: raw.source, rawExternal: raw.externalId } },
      create: {
        runId, rawSource: raw.source, rawExternal: raw.externalId, title: raw.title,
        status, reason, skills: fields.skills.join(", "),
        budget: fields.budget, durationDays: fields.durationDays, location: fields.location,
      },
      update: {
        status, reason, skills: fields.skills.join(", "),
        budget: fields.budget, durationDays: fields.durationDays, location: fields.location,
      },
    });
  }
  return `${qualified} qualifiée(s), ${rejected} rejetée(s) (seuil budget ${threshold}€).`;
}

// Étape 3 — Matching : compare les offres qualifiées aux profils freelance.
export async function matchStep(runId: string): Promise<string> {
  const jobs = await prisma.analyzedJob.findMany({ where: { runId, status: "qualified" } });
  const profiles = await prisma.freelanceProfile.findMany();
  if (profiles.length === 0) return "Aucun profil freelance en base — matching ignoré.";

  // On repart de zéro pour ce run (idempotent en cas de reprise).
  await prisma.jobMatch.deleteMany({ where: { runId } });

  let created = 0;
  for (const job of jobs) {
    for (const profile of profiles) {
      const result = scoreMatch(
        { skills: csv(job.skills), budget: job.budget, location: job.location },
        { skills: csv(profile.skills), minBudget: profile.minBudget, locations: csv(profile.locations) },
      );
      if (result.confidence < 0.4) continue; // seuil de bruit
      await prisma.jobMatch.create({
        data: { runId, analyzedJobId: job.id, profileId: profile.id, confidence: result.confidence, snippet: "" },
      });
      created++;
    }
  }
  return `${created} match(s) au-dessus du seuil de confiance.`;
}

// Étape 4 — Enrichissement : génère le "pourquoi ça matche" pour chaque match.
export async function enrichStep(runId: string): Promise<string> {
  const matches = await prisma.jobMatch.findMany({
    where: { runId },
    include: { analyzedJob: true, profile: true },
  });
  for (const m of matches) {
    const jobSkills = csv(m.analyzedJob.skills);
    const profSkills = new Set(csv(m.profile.skills).map((s) => s.toLowerCase()));
    const common = jobSkills.filter((s) => profSkills.has(s.toLowerCase()));
    const snippet = buildSnippet(
      m.analyzedJob.title,
      { confidence: m.confidence, breakdown: { skills: 0, budget: 0, location: 0 } },
      common,
    );
    await prisma.jobMatch.update({ where: { id: m.id }, data: { snippet } });
  }
  return `${matches.length} match(s) enrichi(s) d'une explication.`;
}

// Étape 5 — Notification : prépare la sortie pour le dashboard (validation humaine).
export async function notifyStep(runId: string): Promise<string> {
  const pending = await prisma.jobMatch.count({ where: { runId, status: "proposed" } });
  return `${pending} proposition(s) prête(s) pour validation humaine.`;
}
