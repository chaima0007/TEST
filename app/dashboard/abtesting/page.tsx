"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface ABVariant {
  agent_id: string;
  tone_name: string;
  sent: number;
  opened: number;
  replied: number;
  paid: number;
  open_rate: number;
  reply_rate: number;
  conversion_rate: number;
  alpha?: number;
  beta?: number;
}

interface ABReport {
  source: string;
  started_at: string;
  total_sent: number;
  total_replied: number;
  winner: ABVariant | null;
  variants: ABVariant[];
}

// ── Metric bar ───────────────────────────────────────────────────────────────

function MetricBar({ value, max, color }: { value: number; max: number; color: string }) {
  const pct = max > 0 ? Math.min(100, (value / max) * 100) : 0;
  return (
    <div className="w-full h-1.5 rounded-full bg-white/10 overflow-hidden">
      <div
        className="h-full rounded-full transition-all duration-700"
        style={{ width: `${pct}%`, backgroundColor: color }}
      />
    </div>
  );
}

// ── Stat chip ─────────────────────────────────────────────────────────────────

function Chip({ label, value, sub }: { label: string; value: string | number; sub?: string }) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl px-5 py-4">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Confidence badge (Thompson Sampling posterior) ────────────────────────────

function ConfidenceBadge({ alpha, beta }: { alpha?: number; beta?: number }) {
  if (!alpha || !beta) return null;
  const mean = alpha / (alpha + beta);
  const pct = Math.round(mean * 100);
  const color =
    pct >= 30 ? "text-emerald-400 bg-emerald-400/10 border-emerald-400/20"
    : pct >= 20 ? "text-amber-400 bg-amber-400/10 border-amber-400/20"
    : "text-gray-400 bg-white/5 border-white/10";
  return (
    <span className={`text-xs font-mono px-2 py-0.5 rounded-full border ${color}`}>
      μ={pct}%
    </span>
  );
}

// ── Variant row ───────────────────────────────────────────────────────────────

function VariantRow({
  v,
  rank,
  maxReply,
  isWinner,
}: {
  v: ABVariant;
  rank: number;
  maxReply: number;
  isWinner: boolean;
}) {
  const replyColor = isWinner ? "#10b981" : rank <= 3 ? "#6366f1" : "#6b7280";

  return (
    <div
      className={`grid grid-cols-[2rem_1fr_6rem_6rem_6rem_6rem_7rem] gap-3 items-center px-4 py-3 rounded-xl border transition-all ${
        isWinner
          ? "bg-emerald-500/10 border-emerald-500/30"
          : "bg-white/3 border-white/5 hover:bg-white/5"
      }`}
    >
      {/* Rank */}
      <span className={`text-sm font-bold ${isWinner ? "text-emerald-400" : "text-gray-500"}`}>
        {isWinner ? "🏆" : `#${rank}`}
      </span>

      {/* Agent info */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-mono text-gray-400 bg-white/5 px-1.5 py-0.5 rounded">
            {v.agent_id}
          </span>
          <span className="text-sm font-medium text-white">{v.tone_name}</span>
          <ConfidenceBadge alpha={v.alpha} beta={v.beta} />
          {isWinner && (
            <span className="text-xs font-semibold text-emerald-300 bg-emerald-400/10 px-2 py-0.5 rounded-full border border-emerald-400/20">
              Gagnant
            </span>
          )}
        </div>
        <MetricBar value={v.reply_rate} max={maxReply} color={replyColor} />
      </div>

      {/* Stats */}
      <div className="text-center">
        <p className="text-sm font-semibold text-white">{v.sent}</p>
        <p className="text-xs text-gray-500">envoyés</p>
      </div>
      <div className="text-center">
        <p className="text-sm font-semibold text-blue-300">{v.open_rate}%</p>
        <p className="text-xs text-gray-500">ouverture</p>
      </div>
      <div className="text-center">
        <p className={`text-sm font-semibold ${isWinner ? "text-emerald-300" : "text-indigo-300"}`}>
          {v.reply_rate}%
        </p>
        <p className="text-xs text-gray-500">réponse</p>
      </div>
      <div className="text-center">
        <p className="text-sm font-semibold text-amber-300">{v.conversion_rate}%</p>
        <p className="text-xs text-gray-500">conversion</p>
      </div>
      <div className="text-center">
        <p className="text-sm font-semibold text-purple-300">{v.paid}</p>
        <p className="text-xs text-gray-500">payés</p>
      </div>
    </div>
  );
}

// ── Sentiment routing card ─────────────────────────────────────────────────────

const SENTIMENT_ROUTING = [
  { sentiment: "Positif",   agent: "3.5", desc: "Closing rapide + upsell",       color: "text-emerald-400", dot: "bg-emerald-400" },
  { sentiment: "Curieux",   agent: "3.5", desc: "Nurture & éducation",            color: "text-blue-400",    dot: "bg-blue-400"    },
  { sentiment: "Sceptique", agent: "3.1", desc: "Gestion objections — preuves",   color: "text-amber-400",   dot: "bg-amber-400"   },
  { sentiment: "Méfiant",   agent: "3.2", desc: "Gestion objections — garanties", color: "text-orange-400",  dot: "bg-orange-400"  },
  { sentiment: "Négatif",   agent: "3.3", desc: "Empathie + urgence douce",       color: "text-red-400",     dot: "bg-red-400"     },
  { sentiment: "Fantôme",   agent: "3.7", desc: "Relance J+4",                    color: "text-gray-400",    dot: "bg-gray-400"    },
  { sentiment: "Pressé",    agent: "3.5", desc: "Quick close",                    color: "text-purple-400",  dot: "bg-purple-400"  },
];

// ── Page ─────────────────────────────────────────────────────────────────────

export default function ABTestingPage() {
  const [report, setReport] = useState<ABReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/abtesting")
      .then((r) => r.json())
      .then((d) => setReport(d))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400 text-sm animate-pulse">Chargement du rapport A/B…</div>
      </div>
    );
  }

  if (!report) return null;

  const maxReply = Math.max(...report.variants.map((v) => v.reply_rate), 1);
  const overallReplyRate =
    report.total_sent > 0
      ? ((report.total_replied / report.total_sent) * 100).toFixed(1)
      : "0.0";

  const startDate = new Date(report.started_at).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-6">

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="text-2xl">🧪</span>
            <h1 className="text-2xl font-bold">A/B Testing</h1>
            <span
              className={`text-xs px-2 py-0.5 rounded-full border font-medium ${
                report.source === "live"
                  ? "text-emerald-400 bg-emerald-400/10 border-emerald-400/20"
                  : "text-amber-400 bg-amber-400/10 border-amber-400/20"
              }`}
            >
              {report.source === "live" ? "● Live" : "◎ Demo"}
            </span>
          </div>
          <p className="text-sm text-gray-400">
            Thompson Sampling — 9 agents copywriting · Depuis le {startDate}
          </p>
        </div>
      </div>

      {/* Stats strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Chip label="Emails envoyés" value={report.total_sent.toLocaleString("fr-FR")} />
        <Chip label="Réponses" value={report.total_replied.toLocaleString("fr-FR")} sub={`${overallReplyRate}% de taux`} />
        <Chip
          label="Variante gagnante"
          value={report.winner ? report.winner.tone_name : "—"}
          sub={report.winner ? `Agent ${report.winner.agent_id}` : "Pas encore"}
        />
        <Chip
          label="Meilleur taux réponse"
          value={report.winner ? `${report.winner.reply_rate}%` : "—"}
          sub={report.winner ? `${report.winner.replied} réponses` : ""}
        />
      </div>

      {/* Winner highlight */}
      {report.winner && (
        <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-2xl p-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs text-emerald-400 font-semibold uppercase tracking-widest mb-1">
                🏆 Variante gagnante (Thompson Sampling)
              </p>
              <p className="text-xl font-bold text-white">
                Agent {report.winner.agent_id} — {report.winner.tone_name}
              </p>
              <p className="text-sm text-gray-400 mt-1">
                {report.winner.sent} envois · {report.winner.replied} réponses · {report.winner.paid} conversions
              </p>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center shrink-0">
              <div>
                <p className="text-2xl font-bold text-emerald-300">{report.winner.reply_rate}%</p>
                <p className="text-xs text-gray-500">Réponse</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-blue-300">{report.winner.open_rate}%</p>
                <p className="text-xs text-gray-500">Ouverture</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-amber-300">{report.winner.conversion_rate}%</p>
                <p className="text-xs text-gray-500">Conversion</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Variants table */}
      <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-base font-semibold">Classement des variantes</span>
          <span className="text-xs text-gray-500 ml-auto">
            Trié par taux de réponse · μ = moyenne postérieure Beta(α,β)
          </span>
        </div>

        {/* Column headers */}
        <div className="grid grid-cols-[2rem_1fr_6rem_6rem_6rem_6rem_7rem] gap-3 px-4 py-2 text-xs text-gray-500 uppercase tracking-wide mb-2">
          <div />
          <div>Agent / Tone</div>
          <div className="text-center">Envois</div>
          <div className="text-center">Ouverture</div>
          <div className="text-center">Réponse</div>
          <div className="text-center">Conversion</div>
          <div className="text-center">Payés</div>
        </div>

        <div className="space-y-2">
          {report.variants.map((v, i) => (
            <VariantRow
              key={v.agent_id}
              v={v}
              rank={i + 1}
              maxReply={maxReply}
              isWinner={report.winner?.agent_id === v.agent_id}
            />
          ))}
        </div>
      </div>

      {/* Sentiment routing table */}
      <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
        <p className="text-base font-semibold mb-4">
          Routage sentiment → Agent Division 3
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {SENTIMENT_ROUTING.map((s) => (
            <div
              key={s.sentiment}
              className="flex items-center gap-3 bg-white/3 border border-white/5 rounded-xl px-4 py-3"
            >
              <div className={`w-2 h-2 rounded-full shrink-0 ${s.dot}`} />
              <span className={`text-sm font-semibold w-24 shrink-0 ${s.color}`}>
                {s.sentiment}
              </span>
              <span className="text-xs text-gray-400 flex-1">{s.desc}</span>
              <span className="text-xs font-mono text-gray-500 bg-white/5 px-2 py-0.5 rounded">
                Agent {s.agent}
              </span>
            </div>
          ))}
        </div>
        <p className="text-xs text-gray-500 mt-3">
          Le SentimentRouter analyse le texte brut des prospects avec heuristiques + Claude API (fallback) et route automatiquement vers le négociateur optimal.
        </p>
      </div>

      {/* How it works */}
      <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
        <p className="text-base font-semibold mb-3">Comment fonctionne le Thompson Sampling</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-400">
          <div>
            <p className="text-white font-medium mb-1">1. Exploration</p>
            <p>Chaque agent reçoit au minimum 3 envois avant d'entrer en compétition — garantit une base statistique valide.</p>
          </div>
          <div>
            <p className="text-white font-medium mb-1">2. Mise à jour Bayésienne</p>
            <p>Chaque réponse met à jour les paramètres Beta(α, β). Une réponse = +1α. Pas de réponse = +0.5β. Paiement = +2α.</p>
          </div>
          <div>
            <p className="text-white font-medium mb-1">3. Exploitation progressive</p>
            <p>L'agent avec le meilleur échantillon Beta reçoit plus d'envois — converge naturellement vers le gagnant sans abandonner les autres.</p>
          </div>
        </div>
      </div>

    </div>
  );
}
