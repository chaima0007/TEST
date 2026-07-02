// Agent Copywriter : rédige le brouillon de l'étape 1 pour chaque prospect
// qualifié qui n'a pas encore de premier contact. Les étapes 2-4 sont
// générées plus tard par le Sequencer via buildEmail.

import { prisma } from "../../db";
import type { AgentSummary } from "../types";
import { buildEmail } from "../templates";

export async function runCopywriter(): Promise<AgentSummary> {
  const prospects = await prisma.prospect.findMany({
    where: {
      status: "qualified",
      optOut: false,
      messages: { none: { step: 1 } },
    },
  });

  let created = 0;
  for (const prospect of prospects) {
    const draft = buildEmail(1, {
      name: prospect.name,
      category: prospect.category,
      city: prospect.city,
      optOutToken: prospect.optOutToken,
    });
    await prisma.outreachMessage.create({
      data: {
        prospectId: prospect.id,
        step: draft.step,
        channel: "email",
        subject: draft.subject,
        body: draft.body,
        status: "draft",
      },
    });
    created++;
  }

  return { agent: "copywriter", processed: prospects.length, created };
}
