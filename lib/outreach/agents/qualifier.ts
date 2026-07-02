// Agent Qualifier : score les prospects "new" et qualifie ceux qui
// atteignent le score minimum de contact.

import { prisma } from "../../db";
import { outreach } from "../config";
import type { AgentSummary } from "../types";

export async function runQualifier(): Promise<AgentSummary> {
  const prospects = await prisma.prospect.findMany({
    where: { status: "new" },
  });

  let qualified = 0;

  for (const prospect of prospects) {
    let score = 0;
    if (prospect.phone) score += 30;
    if (prospect.rating != null && prospect.rating >= 4) score += 20;
    if (prospect.reviewCount >= 10) score += 20;
    if (prospect.email) score += 15;
    if (prospect.address) score += 15;
    score = Math.min(score, 100);

    const isQualified = score >= outreach.minScoreToContact;
    if (isQualified) qualified++;

    await prisma.prospect.update({
      where: { id: prospect.id },
      data: {
        score,
        status: isQualified ? "qualified" : "new",
      },
    });
  }

  return { agent: "qualifier", processed: prospects.length, created: qualified };
}
