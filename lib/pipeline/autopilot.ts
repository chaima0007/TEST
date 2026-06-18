// ─── Agent « Auto-pilote » ───────────────────────────────────────────────────
//
// Orchestre les agents existants : à partir des recommandations du Conseiller
// (computeRanking), il déclenche automatiquement le Rédacteur + Négociateur
// (createWriter) pour préparer le dossier des opportunités jugées prioritaires.
//
// Limite de sécurité : l'auto-pilote PRÉPARE seulement. Il n'approuve, ne rejette
// et n'envoie jamais — ces actions restent à l'utilisateur.

import { prisma } from "@/lib/prisma";
import { createWriter } from "./writer";
import { computeRanking, type AdviceInput } from "./advisor";
import type { Recommendation, Seniority } from "./simulator";

const ORDER: Recommendation[] = ["skip", "consider", "strong"];

/** Vrai si `reco` est au moins aussi forte que `level`. */
export function meetsLevel(reco: Recommendation, level: Recommendation): boolean {
  return ORDER.indexOf(reco) >= ORDER.indexOf(level);
}

const SENIORITIES: Seniority[] = ["junior", "mid", "senior"];
const asSeniority = (s: string): Seniority =>
  SENIORITIES.includes(s as Seniority) ? (s as Seniority) : "mid";
const csv = (s: string) => s.split(",").map((x) => x.trim()).filter(Boolean);

export interface AutopilotReport {
  level: Recommendation;
  prepared: number;
  skipped: number;
  items: { id: string; title: string; recommendation: Recommendation; prepared: boolean }[];
}

/**
 * Prépare les dossiers des opportunités dont la recommandation atteint `level`
 * (défaut: "strong"). Idempotent : ne régénère pas un dossier déjà présent
 * sauf `force`.
 */
export async function runAutopilot(
  runId: string,
  opts: { level?: Recommendation; force?: boolean } = {},
): Promise<AutopilotReport> {
  const level = opts.level ?? "strong";

  const matches = await prisma.jobMatch.findMany({
    where: { runId, status: "proposed" },
    include: { analyzedJob: true, profile: true },
  });

  const items: AdviceInput[] = matches.map((m) => ({
    id: m.id,
    title: m.analyzedJob.title,
    profileName: m.profile.name,
    confidence: m.confidence,
    seniority: asSeniority(m.profile.seniority),
    budget: m.analyzedJob.budget,
  }));
  const recoById = new Map(computeRanking(items).ranked.map((r) => [r.id, r.recommendation]));

  const writer = createWriter();
  const report: AutopilotReport = { level, prepared: 0, skipped: 0, items: [] };

  for (const m of matches) {
    const reco = recoById.get(m.id) ?? "skip";
    const qualifies = meetsLevel(reco, level);
    const needsDraft = opts.force || !m.proposalDraft;

    if (qualifies && needsDraft) {
      const jobSkills = csv(m.analyzedJob.skills);
      const profSkills = new Set(csv(m.profile.skills).map((s) => s.toLowerCase()));
      const dossier = await writer.prepare({
        jobTitle: m.analyzedJob.title,
        jobDescription: m.analyzedJob.reason,
        budget: m.analyzedJob.budget,
        freelanceName: m.profile.name,
        freelanceBio: m.profile.bio,
        commonSkills: jobSkills.filter((s) => profSkills.has(s.toLowerCase())),
      });
      await prisma.jobMatch.update({
        where: { id: m.id },
        data: { proposalDraft: dossier.proposal, followupsDraft: JSON.stringify(dossier.followups) },
      });
      report.prepared++;
      report.items.push({ id: m.id, title: m.analyzedJob.title, recommendation: reco, prepared: true });
    } else {
      report.skipped++;
      report.items.push({ id: m.id, title: m.analyzedJob.title, recommendation: reco, prepared: false });
    }
  }

  return report;
}
