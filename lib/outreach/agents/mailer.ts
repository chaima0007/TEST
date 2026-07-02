// Agent Mailer : envoie les messages en attente via SMTP, dans la limite
// du quota journalier. En dry-run (défaut), rien n'est envoyé ni modifié.

import nodemailer from "nodemailer";
import { prisma } from "../../db";
import { outreach } from "../config";
import type { AgentSummary } from "../types";

const sleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

export async function runMailer(dryRunOverride?: boolean): Promise<AgentSummary> {
  const dryRun = dryRunOverride ?? outreach.dryRun;
  const now = new Date();

  const messages = await prisma.outreachMessage.findMany({
    where: {
      status: { in: ["draft", "scheduled"] },
      OR: [{ scheduledFor: null }, { scheduledFor: { lte: now } }],
      prospect: {
        email: { not: null },
        optOut: false,
        status: { notIn: ["replied", "won", "lost", "optout"] },
      },
    },
    include: { prospect: true },
    orderBy: { createdAt: "asc" },
  });

  // Quota : on décompte les envois réels effectués depuis minuit
  const midnight = new Date(now);
  midnight.setHours(0, 0, 0, 0);
  const sentToday = await prisma.outreachMessage.count({
    where: { status: "sent", sentAt: { gte: midnight } },
  });
  const remaining = Math.max(0, outreach.dailySendLimit - sentToday);

  const toSend = messages.slice(0, remaining);
  const skipped = messages.length - toSend.length;

  const details: string[] = [];
  if (skipped > 0) {
    details.push(
      `Quota journalier (${outreach.dailySendLimit}) atteint : ${skipped} message(s) laissé(s) en attente`
    );
  }

  if (dryRun) {
    for (const message of toSend) {
      details.push(`[DRY-RUN] à: ${message.prospect.email} — ${message.subject}`);
    }
    return { agent: "mailer", processed: messages.length, sent: 0, skipped, details };
  }

  const transport = nodemailer.createTransport({
    host: outreach.smtp.host,
    port: outreach.smtp.port,
    secure: outreach.smtp.port === 465,
    auth: outreach.smtp.user
      ? { user: outreach.smtp.user, pass: outreach.smtp.pass }
      : undefined,
  });

  let sent = 0;
  let failed = 0;

  for (let i = 0; i < toSend.length; i++) {
    const message = toSend[i];
    try {
      await transport.sendMail({
        from: outreach.smtp.from,
        to: message.prospect.email!,
        subject: message.subject,
        text: message.body,
        headers: {
          "List-Unsubscribe": `<${outreach.publicBaseUrl}/api/outreach/unsubscribe?token=${message.prospect.optOutToken}>`,
        },
      });

      await prisma.outreachMessage.update({
        where: { id: message.id },
        data: { status: "sent", sentAt: new Date() },
      });
      await prisma.prospect.update({
        where: { id: message.prospectId },
        data: { status: message.step === 1 ? "contacted" : "followup" },
      });
      sent++;
    } catch (err) {
      failed++;
      const reason = err instanceof Error ? err.message : String(err);
      await prisma.outreachMessage.update({
        where: { id: message.id },
        data: { status: "failed", error: reason.slice(0, 500) },
      });
      details.push(`Échec ${message.prospect.email} (étape ${message.step}) : ${reason.slice(0, 200)}`);
    }

    // Espacement des envois pour ménager le serveur SMTP
    if (i < toSend.length - 1) await sleep(1500);
  }

  return { agent: "mailer", processed: messages.length, sent, failed, skipped, details };
}
