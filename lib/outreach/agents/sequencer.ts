// Agent Sequencer : planifie les relances (étapes 2 à 4) des prospects
// déjà contactés, selon des délais absolus depuis le premier envoi.

import { prisma } from "../../db";
import { outreach } from "../config";
import { buildEmail } from "../templates";
import type { AgentSummary } from "../types";

const DAY_MS = 24 * 60 * 60 * 1000;

export async function runSequencer(): Promise<AgentSummary> {
  const now = new Date();

  const prospects = await prisma.prospect.findMany({
    where: {
      status: { in: ["contacted", "followup"] },
      optOut: false,
      email: { not: null },
    },
    include: { messages: true },
  });

  let created = 0;
  const details: string[] = [];

  for (const prospect of prospects) {
    const sentMessages = prospect.messages
      .filter((m) => m.status === "sent" && m.sentAt != null)
      .sort((a, b) => a.sentAt!.getTime() - b.sentAt!.getTime());

    // Premier envoi (étape 1) : point de référence de toute la séquence
    const firstSent = sentMessages[0];
    if (!firstSent) continue;

    const lastStep = Math.max(...sentMessages.map((m) => m.step));
    if (lastStep >= 4) continue;

    // Délais absolus depuis J0 : étape 2 à J+4, étape 3 à J+10, étape 4 à J+18
    const delayDays = outreach.stepDelaysDays[lastStep];
    if (now.getTime() - firstSent.sentAt!.getTime() < delayDays * DAY_MS) continue;

    const nextStep = (lastStep + 1) as 2 | 3 | 4;
    // Ne rien créer si un message (quel que soit son statut) existe déjà pour cette étape
    if (prospect.messages.some((m) => m.step === nextStep)) continue;

    const draft = buildEmail(nextStep, {
      name: prospect.name,
      category: prospect.category,
      city: prospect.city,
      optOutToken: prospect.optOutToken,
    });

    await prisma.outreachMessage.create({
      data: {
        prospectId: prospect.id,
        step: nextStep,
        subject: draft.subject,
        body: draft.body,
        status: "draft",
        scheduledFor: now,
      },
    });

    created++;
    details.push(`${prospect.name} → étape ${nextStep} planifiée`);
  }

  return { agent: "sequencer", processed: prospects.length, created, details };
}
