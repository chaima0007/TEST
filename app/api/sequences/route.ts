import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sequences] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const SEQUENCES = [
  {
    sequence_id: "cold_outreach_standard",
    name: "Prospection standard",
    description: "Séquence froide multi-touches pour TPE/PME",
    max_touches: 5,
    step_count: 5,
    steps: [
      { step_index: 0, day_offset: 0,  template_id: "intro_value",   subject_variant: "A", channel: "email" },
      { step_index: 1, day_offset: 3,  template_id: "follow_up_1",   subject_variant: "B", channel: "email" },
      { step_index: 2, day_offset: 7,  template_id: "social_proof",  subject_variant: "A", channel: "email" },
      { step_index: 3, day_offset: 12, template_id: "urgency_close", subject_variant: "C", channel: "email" },
      { step_index: 4, day_offset: 18, template_id: "breakup",       subject_variant: "A", channel: "email" },
    ],
  },
  {
    sequence_id: "warm_reactivation",
    name: "Réactivation prospects chauds",
    description: "Pour prospects ayant déjà ouvert ou cliqué",
    max_touches: 3,
    step_count: 3,
    steps: [
      { step_index: 0, day_offset: 0, template_id: "warm_check_in", subject_variant: "A", channel: "email" },
      { step_index: 1, day_offset: 4, template_id: "case_study",    subject_variant: "B", channel: "email" },
      { step_index: 2, day_offset: 9, template_id: "demo_offer",    subject_variant: "A", channel: "email" },
    ],
  },
  {
    sequence_id: "post_quote",
    name: "Suivi post-devis",
    description: "Après envoi du devis, relances avec valeur",
    max_touches: 3,
    step_count: 3,
    steps: [
      { step_index: 0, day_offset: 2,  template_id: "quote_reminder", subject_variant: "A", channel: "email" },
      { step_index: 1, day_offset: 5,  template_id: "objection_faq",  subject_variant: "A", channel: "email" },
      { step_index: 2, day_offset: 10, template_id: "final_offer",    subject_variant: "B", channel: "email" },
    ],
  },
  {
    sequence_id: "quick_ping",
    name: "Ping rapide",
    description: "Séquence minimaliste pour secteurs très occupés",
    max_touches: 2,
    step_count: 2,
    steps: [
      { step_index: 0, day_offset: 0, template_id: "intro_value",  subject_variant: "A", channel: "email" },
      { step_index: 1, day_offset: 5, template_id: "follow_up_1",  subject_variant: "C", channel: "email" },
    ],
  },
];

type StepStatus = "pending" | "sent" | "skipped" | "failed";
type EnrStatus = "active" | "paused" | "completed" | "stopped";
type StopReason = "reply_received" | "opt_out" | "max_touches" | "manual" | "converted" | null;

interface MockEnrollment {
  enrollment_id: string;
  prospect_id: string;
  company_name: string;
  sequence_id: string;
  sequence_name: string;
  started_at: string;
  status: EnrStatus;
  stop_reason: StopReason;
  sent_count: number;
  opened_count: number;
  clicked_count: number;
  steps: { step_index: number; template_id: string; scheduled_at: string; status: StepStatus; sent_at: string | null; opened_at: string | null; clicked_at: string | null; error: string | null }[];
}

function daysAgo(d: number) {
  const dt = new Date();
  dt.setDate(dt.getDate() - d);
  return dt.toISOString();
}

function buildMockData() {
  const enrollments: MockEnrollment[] = [
    {
      enrollment_id: "enr_00001", prospect_id: "p001", company_name: "Plomberie Martin SARL",
      sequence_id: "cold_outreach_standard", sequence_name: "Prospection standard",
      started_at: daysAgo(20), status: "completed", stop_reason: null,
      sent_count: 5, opened_count: 3, clicked_count: 1,
      steps: [
        { step_index: 0, template_id: "intro_value",   scheduled_at: daysAgo(20), status: "sent", sent_at: daysAgo(20), opened_at: daysAgo(19), clicked_at: daysAgo(19), error: null },
        { step_index: 1, template_id: "follow_up_1",   scheduled_at: daysAgo(17), status: "sent", sent_at: daysAgo(17), opened_at: daysAgo(16), clicked_at: null,         error: null },
        { step_index: 2, template_id: "social_proof",  scheduled_at: daysAgo(13), status: "sent", sent_at: daysAgo(13), opened_at: daysAgo(13), clicked_at: null,         error: null },
        { step_index: 3, template_id: "urgency_close", scheduled_at: daysAgo(8),  status: "sent", sent_at: daysAgo(8),  opened_at: null,         clicked_at: null,         error: null },
        { step_index: 4, template_id: "breakup",       scheduled_at: daysAgo(2),  status: "sent", sent_at: daysAgo(2),  opened_at: null,         clicked_at: null,         error: null },
      ],
    },
    {
      enrollment_id: "enr_00002", prospect_id: "p002", company_name: "Restaurant La Cigale",
      sequence_id: "cold_outreach_standard", sequence_name: "Prospection standard",
      started_at: daysAgo(10), status: "stopped", stop_reason: "reply_received",
      sent_count: 2, opened_count: 2, clicked_count: 1,
      steps: [
        { step_index: 0, template_id: "intro_value",   scheduled_at: daysAgo(10), status: "sent",    sent_at: daysAgo(10), opened_at: daysAgo(9), clicked_at: daysAgo(9), error: null },
        { step_index: 1, template_id: "follow_up_1",   scheduled_at: daysAgo(7),  status: "sent",    sent_at: daysAgo(7),  opened_at: daysAgo(7), clicked_at: null,        error: null },
        { step_index: 2, template_id: "social_proof",  scheduled_at: daysAgo(3),  status: "skipped", sent_at: null,         opened_at: null,        clicked_at: null,        error: null },
        { step_index: 3, template_id: "urgency_close", scheduled_at: daysAgo(-2), status: "skipped", sent_at: null,         opened_at: null,        clicked_at: null,        error: null },
        { step_index: 4, template_id: "breakup",       scheduled_at: daysAgo(-8), status: "skipped", sent_at: null,         opened_at: null,        clicked_at: null,        error: null },
      ],
    },
    {
      enrollment_id: "enr_00003", prospect_id: "p003", company_name: "Cabinet Dr. Lefèvre",
      sequence_id: "warm_reactivation", sequence_name: "Réactivation prospects chauds",
      started_at: daysAgo(6), status: "active", stop_reason: null,
      sent_count: 2, opened_count: 1, clicked_count: 0,
      steps: [
        { step_index: 0, template_id: "warm_check_in", scheduled_at: daysAgo(6), status: "sent",    sent_at: daysAgo(6), opened_at: daysAgo(5), clicked_at: null, error: null },
        { step_index: 1, template_id: "case_study",    scheduled_at: daysAgo(2), status: "sent",    sent_at: daysAgo(2), opened_at: null,        clicked_at: null, error: null },
        { step_index: 2, template_id: "demo_offer",    scheduled_at: daysAgo(-3),status: "pending",  sent_at: null,        opened_at: null,        clicked_at: null, error: null },
      ],
    },
    {
      enrollment_id: "enr_00004", prospect_id: "p004", company_name: "Garage Dupont",
      sequence_id: "post_quote", sequence_name: "Suivi post-devis",
      started_at: daysAgo(3), status: "active", stop_reason: null,
      sent_count: 1, opened_count: 1, clicked_count: 0,
      steps: [
        { step_index: 0, template_id: "quote_reminder", scheduled_at: daysAgo(1),  status: "sent",    sent_at: daysAgo(1), opened_at: daysAgo(1), clicked_at: null, error: null },
        { step_index: 1, template_id: "objection_faq",  scheduled_at: daysAgo(-2), status: "pending",  sent_at: null,        opened_at: null,        clicked_at: null, error: null },
        { step_index: 2, template_id: "final_offer",    scheduled_at: daysAgo(-7), status: "pending",  sent_at: null,        opened_at: null,        clicked_at: null, error: null },
      ],
    },
    {
      enrollment_id: "enr_00005", prospect_id: "p005", company_name: "Immo Prestige",
      sequence_id: "quick_ping", sequence_name: "Ping rapide",
      started_at: daysAgo(8), status: "stopped", stop_reason: "opt_out",
      sent_count: 1, opened_count: 0, clicked_count: 0,
      steps: [
        { step_index: 0, template_id: "intro_value",  scheduled_at: daysAgo(8), status: "sent",    sent_at: daysAgo(8), opened_at: null, clicked_at: null, error: null },
        { step_index: 1, template_id: "follow_up_1",  scheduled_at: daysAgo(3), status: "skipped", sent_at: null,        opened_at: null, clicked_at: null, error: null },
      ],
    },
    {
      enrollment_id: "enr_00006", prospect_id: "p006", company_name: "Maître Rousseau",
      sequence_id: "cold_outreach_standard", sequence_name: "Prospection standard",
      started_at: daysAgo(2), status: "active", stop_reason: null,
      sent_count: 1, opened_count: 0, clicked_count: 0,
      steps: [
        { step_index: 0, template_id: "intro_value",   scheduled_at: daysAgo(2),  status: "sent",   sent_at: daysAgo(2), opened_at: null, clicked_at: null, error: null },
        { step_index: 1, template_id: "follow_up_1",   scheduled_at: daysAgo(-1), status: "pending", sent_at: null,        opened_at: null, clicked_at: null, error: null },
        { step_index: 2, template_id: "social_proof",  scheduled_at: daysAgo(-5), status: "pending", sent_at: null,        opened_at: null, clicked_at: null, error: null },
        { step_index: 3, template_id: "urgency_close", scheduled_at: daysAgo(-10),status: "pending", sent_at: null,        opened_at: null, clicked_at: null, error: null },
        { step_index: 4, template_id: "breakup",       scheduled_at: daysAgo(-16),status: "pending", sent_at: null,        opened_at: null, clicked_at: null, error: null },
      ],
    },
    {
      enrollment_id: "enr_00007", prospect_id: "p007", company_name: "Centre Formation Top",
      sequence_id: "warm_reactivation", sequence_name: "Réactivation prospects chauds",
      started_at: daysAgo(1), status: "active", stop_reason: null,
      sent_count: 1, opened_count: 1, clicked_count: 1,
      steps: [
        { step_index: 0, template_id: "warm_check_in", scheduled_at: daysAgo(1),  status: "sent",   sent_at: daysAgo(1), opened_at: daysAgo(0), clicked_at: daysAgo(0), error: null },
        { step_index: 1, template_id: "case_study",    scheduled_at: daysAgo(-3), status: "pending", sent_at: null,        opened_at: null,        clicked_at: null,        error: null },
        { step_index: 2, template_id: "demo_offer",    scheduled_at: daysAgo(-8), status: "pending", sent_at: null,        opened_at: null,        clicked_at: null,        error: null },
      ],
    },
    {
      enrollment_id: "enr_00008", prospect_id: "p008", company_name: "Salon Élite",
      sequence_id: "post_quote", sequence_name: "Suivi post-devis",
      started_at: daysAgo(14), status: "stopped", stop_reason: "converted",
      sent_count: 3, opened_count: 3, clicked_count: 2,
      steps: [
        { step_index: 0, template_id: "quote_reminder", scheduled_at: daysAgo(12), status: "sent",    sent_at: daysAgo(12), opened_at: daysAgo(12), clicked_at: daysAgo(11), error: null },
        { step_index: 1, template_id: "objection_faq",  scheduled_at: daysAgo(9),  status: "sent",    sent_at: daysAgo(9),  opened_at: daysAgo(9),  clicked_at: daysAgo(8),  error: null },
        { step_index: 2, template_id: "final_offer",    scheduled_at: daysAgo(4),  status: "sent",    sent_at: daysAgo(4),  opened_at: daysAgo(4),  clicked_at: null,         error: null },
      ],
    },
  ];

  const totalSent    = enrollments.reduce((s, e) => s + e.sent_count,    0);
  const totalOpened  = enrollments.reduce((s, e) => s + e.opened_count,  0);
  const totalClicked = enrollments.reduce((s, e) => s + e.clicked_count, 0);

  const byStatus: Record<string, number> = {};
  const stopReasons: Record<string, number> = {};
  for (const e of enrollments) {
    byStatus[e.status] = (byStatus[e.status] ?? 0) + 1;
    if (e.stop_reason) stopReasons[e.stop_reason] = (stopReasons[e.stop_reason] ?? 0) + 1;
  }

  return {
    source: "mock",
    sequences: SEQUENCES,
    enrollments,
    summary: {
      total_enrollments: enrollments.length,
      by_status: byStatus,
      total_sent: totalSent,
      total_opened: totalOpened,
      total_clicked: totalClicked,
      open_rate_pct:  totalSent ? Math.round(totalOpened  / totalSent * 1000) / 10 : 0,
      click_rate_pct: totalSent ? Math.round(totalClicked / totalSent * 1000) / 10 : 0,
      stop_reasons: stopReasons,
      sequences_count: SEQUENCES.length,
    },
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const [seqRes, sumRes] = await Promise.all([
        fetch(`${SWARM_API_URL}/sequences`, { next: { revalidate: 15 } }),
        fetch(`${SWARM_API_URL}/sequences/summary`, { next: { revalidate: 15 } }),
      ]);
      if (seqRes.ok && sumRes.ok) {
        return sealResponse(NextResponse.json({
          source: "live",
          sequences: await seqRes.json(),
          summary: await sumRes.json(),
        }));
      }
    } catch { /* fall through */ }
  }
  return sealResponse(NextResponse.json(buildMockData()));
}
