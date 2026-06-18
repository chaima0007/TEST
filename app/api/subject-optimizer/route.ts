import { NextRequest, NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type OptimizationTier = "weak" | "fair" | "good" | "excellent";

interface SubjectLine {
  subject_id: string;
  text: string;
  template_id?: string;
  variant_key: string;
  send_hour: number;
}

interface OptimizedSubject {
  subject: SubjectLine;
  predicted_open_rate: number;
  optimization_tier: OptimizationTier;
  dimension_scores: {
    length: number;
    personalization: number;
    urgency: number;
    clarity: number;
    question: number;
    emoji_balance: number;
  };
  suggestions: string[];
  emoji_count: number;
  word_count: number;
  char_count: number;
  has_personalization: boolean;
  has_urgency: boolean;
  has_question: boolean;
}

const URGENCY_WORDS = ["urgent", "dernière chance", "expire", "limite", "maintenant", "aujourd'hui",
  "offre", "exclusif", "seulement", "immédiat", "critique", "alerte"];
const SPAM_WORDS = ["fwd:", "re:", "important!!!", "attention!!!", "cliquez"];
const BASELINE = 0.15;
const SUGGESTIONS: Record<string, string> = {
  too_long: "Raccourcir le sujet à moins de 60 caractères",
  too_short: "Allonger le sujet — au moins 20 caractères pour donner du contexte",
  no_personalization: "Ajouter {contact_name} ou {company_name} pour personnaliser",
  no_urgency: "Inclure un mot d'urgence (offre, limite, aujourd'hui…)",
  no_question: "Formuler comme une question pour susciter la curiosité",
  spam_risk: "Retirer les mots spam (fwd, re:, !!!)",
  too_many_emojis: "Limiter à 1-2 emojis maximum",
  no_emoji: "Un emoji en début ou fin peut augmenter le taux d'ouverture de 15%",
};

const EMOJI_RE = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}]/gu;
const TOKEN_RE = /\{(\w+)\}/g;

function countEmojis(text: string): number { return (text.match(EMOJI_RE) ?? []).length; }

function lengthScore(text: string): [number, string[]] {
  const len = text.length;
  if (len < 20) return [30, ["too_short"]];
  if (len <= 40) return [100, []];
  if (len <= 60) return [80, []];
  return [Math.max(0, 80 - (len - 60) * 2), ["too_long"]];
}

function personalizationScore(text: string): [number, string[]] {
  const tokens = [...text.matchAll(TOKEN_RE)];
  if (!tokens.length) return [0, ["no_personalization"]];
  return [Math.min(100, tokens.length * 50), []];
}

function urgencyScore(text: string): [number, string[]] {
  const lower = text.toLowerCase();
  const hits = URGENCY_WORDS.filter((w) => lower.includes(w)).length;
  if (!hits) return [20, ["no_urgency"]];
  return [Math.min(100, 40 + hits * 30), []];
}

function clarityScore(text: string): [number, string[]] {
  const lower = text.toLowerCase();
  const penalties = SPAM_WORDS.filter((w) => lower.includes(w)).length;
  if (penalties > 0) return [Math.max(0, 100 - penalties * 40), ["spam_risk"]];
  return [100, []];
}

function questionScore(text: string): [number, string[]] {
  return text.includes("?") ? [100, []] : [30, ["no_question"]];
}

function emojiBalanceScore(text: string): [number, string[]] {
  const count = countEmojis(text);
  if (count === 0) return [50, ["no_emoji"]];
  if (count <= 2) return [100, []];
  return [Math.max(0, 100 - (count - 2) * 20), ["too_many_emojis"]];
}

function sendHourMultiplier(hour: number): number {
  if (hour >= 8 && hour <= 10) return 1.15;
  if (hour >= 11 && hour <= 13) return 1.05;
  if (hour >= 14 && hour <= 16) return 1.0;
  if ((hour >= 6 && hour <= 7) || (hour >= 17 && hour <= 19)) return 0.90;
  return 0.75;
}

function computeOpenRate(dims: OptimizedSubject["dimension_scores"], hour: number): number {
  const composite = dims.length * 0.20 + dims.personalization * 0.25 + dims.urgency * 0.20 +
    dims.clarity * 0.15 + dims.question * 0.10 + dims.emoji_balance * 0.10;
  const rate = (BASELINE + (composite / 100) * 0.35) * sendHourMultiplier(hour);
  return Math.round(Math.max(0, Math.min(1, rate)) * 10000) / 10000;
}

function classifyTier(rate: number): OptimizationTier {
  if (rate >= 0.38) return "excellent";
  if (rate >= 0.28) return "good";
  if (rate >= 0.18) return "fair";
  return "weak";
}

function optimizeSubject(s: SubjectLine): OptimizedSubject {
  const [ls, lt] = lengthScore(s.text);
  const [ps, pt] = personalizationScore(s.text);
  const [us, ut] = urgencyScore(s.text);
  const [cs, ct] = clarityScore(s.text);
  const [qs, qt] = questionScore(s.text);
  const [es, et] = emojiBalanceScore(s.text);

  const dimension_scores = { length: ls, personalization: ps, urgency: us, clarity: cs, question: qs, emoji_balance: es };
  const allTips = [...lt, ...pt, ...ut, ...ct, ...qt, ...et];
  const suggestions = allTips.map((t) => SUGGESTIONS[t]).filter(Boolean);
  const rate = computeOpenRate(dimension_scores, s.send_hour);

  return {
    subject: s,
    predicted_open_rate: rate,
    optimization_tier: classifyTier(rate),
    dimension_scores,
    suggestions,
    emoji_count: countEmojis(s.text),
    word_count: s.text.split(/\s+/).filter(Boolean).length,
    char_count: s.text.length,
    has_personalization: TOKEN_RE.test(s.text),
    has_urgency: URGENCY_WORDS.some((w) => s.text.toLowerCase().includes(w)),
    has_question: s.text.includes("?"),
  };
}

const SAMPLE_SUBJECTS: SubjectLine[] = [
  { subject_id: "s001", text: "Votre site {company_name} perd du trafic chaque jour 📉", template_id: "intro_value", variant_key: "A", send_hour: 9 },
  { subject_id: "s002", text: "J'ai analysé le site de {company_name}", template_id: "intro_value", variant_key: "B", send_hour: 9 },
  { subject_id: "s003", text: "Score PageSpeed : {pagespeed}/100 — on peut faire mieux ⚡", template_id: "intro_value", variant_key: "C", send_hour: 10 },
  { subject_id: "s004", text: "Re: {company_name} — avez-vous vu mon message ?", template_id: "follow_up_1", variant_key: "A", send_hour: 8 },
  { subject_id: "s005", text: "Une question rapide sur votre site 🤔", template_id: "follow_up_1", variant_key: "B", send_hour: 11 },
  { subject_id: "s006", text: "Votre concurrent a déjà agi — et vous ? Offre limitée aujourd'hui", template_id: "follow_up_1", variant_key: "C", send_hour: 9 },
  { subject_id: "s007", text: "Dernière chance : offre limitée pour {company_name} ⏰", template_id: "urgency_close", variant_key: "A", send_hour: 9 },
  { subject_id: "s008", text: "Je ferme votre dossier vendredi — un mot avant ?", template_id: "urgency_close", variant_key: "C", send_hour: 14 },
  { subject_id: "s009", text: "Comment {case_company} a gagné +{case_traffic}% de trafic en 30 jours 📊", template_id: "social_proof", variant_key: "A", send_hour: 9 },
  { subject_id: "s010", text: "Démo personnalisée pour {company_name} — 20 minutes ✅", template_id: "demo_offer", variant_key: "A", send_hour: 10 },
  { subject_id: "s011", text: "FWD: important!!! cliquez maintenant", template_id: "spam_test", variant_key: "A", send_hour: 22 },
  { subject_id: "s012", text: "ok", template_id: "short_test", variant_key: "A", send_hour: 9 },
];

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/subject-optimizer`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch { /* fall through */ }
  }

  const optimized = SAMPLE_SUBJECTS.map(optimizeSubject).sort((a, b) => b.predicted_open_rate - a.predicted_open_rate);
  const tierCounts = { weak: 0, fair: 0, good: 0, excellent: 0 };
  for (const o of optimized) tierCounts[o.optimization_tier]++;

  const avgRate = optimized.reduce((s, o) => s + o.predicted_open_rate, 0) / optimized.length;

  return NextResponse.json({
    subjects: optimized,
    summary: {
      total: optimized.length,
      tier_counts: tierCounts,
      avg_open_rate: Math.round(avgRate * 10000) / 10000,
      best_open_rate: optimized[0]?.predicted_open_rate ?? 0,
      pct_with_personalization: Math.round(optimized.filter((o) => o.has_personalization).length / optimized.length * 1000) / 1000,
    },
  });
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { text, send_hour = 9, template_id, variant_key = "A" } = body;

  if (!text || typeof text !== "string") {
    return NextResponse.json({ error: "text is required" }, { status: 400 });
  }

  const subject: SubjectLine = {
    subject_id: `live_${Date.now()}`,
    text,
    template_id,
    variant_key,
    send_hour: Number(send_hour),
  };

  return NextResponse.json(optimizeSubject(subject));
}
