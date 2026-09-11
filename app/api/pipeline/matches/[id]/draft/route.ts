import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { createWriter, type WriterInput } from "@/lib/pipeline/writer";

export const dynamic = "force-dynamic";

const csv = (s: string) => s.split(",").map((x) => x.trim()).filter(Boolean);

// POST /api/pipeline/matches/[id]/draft
// Action des agents Rédacteur + Négociateur : prépare la proposition et les
// réponses de suivi, puis les enregistre sur le match (validation humaine ensuite).
export async function POST(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> },
) {
  const { id } = await props.params;
  const match = await prisma.jobMatch.findUnique({
    where: { id },
    include: { analyzedJob: true, profile: true },
  });
  if (!match) return NextResponse.json({ error: "Match introuvable" }, { status: 404 });

  const jobSkills = csv(match.analyzedJob.skills);
  const profSkills = new Set(csv(match.profile.skills).map((s) => s.toLowerCase()));
  const commonSkills = jobSkills.filter((s) => profSkills.has(s.toLowerCase()));

  const input: WriterInput = {
    jobTitle: match.analyzedJob.title,
    jobDescription: match.analyzedJob.reason,
    budget: match.analyzedJob.budget,
    freelanceName: match.profile.name,
    freelanceBio: match.profile.bio,
    commonSkills,
  };

  const dossier = await createWriter().prepare(input);

  const updated = await prisma.jobMatch.update({
    where: { id },
    data: {
      proposalDraft: dossier.proposal,
      followupsDraft: JSON.stringify(dossier.followups),
    },
  });

  return NextResponse.json({
    proposalDraft: updated.proposalDraft,
    followups: dossier.followups,
    generatedBy: dossier.generatedBy,
  });
}
