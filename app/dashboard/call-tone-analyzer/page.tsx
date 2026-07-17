"use client";

import { useEffect, useState } from "react";

// ── types ──────────────────────────────────────────────────────────────────────
interface CallRecord {
  call_id: string;
  deal_name: string;
  rep_id: string;
  tone_sentiment: string;
  dominant_tone: string;
  conversation_control: string;
  tone_action: string;
  rep_confidence_score: number;
  buyer_engagement_score: number;
  objection_handling_score: number;
  conversation_quality_score: number;
  call_tone_composite: number;
  deal_advancement_probability: number;
  call_coaching_priority: number;
  is_positive_call: boolean;
  needs_immediate_coaching: boolean;
  call_duration_minutes: number;
  region: string;
}

interface Summary {
  total: number;
  sentiment_counts: Record<string, number>;
  tone_counts: Record<string, number>;
  control_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_call_tone_composite: number;
  positive_call_count: number;
  coaching_needed_count: number;
  avg_rep_confidence_score: number;
  avg_buyer_engagement_score: number;
  avg_objection_handling_score: number;
  avg_deal_advancement_probability: number;
  avg_coaching_priority: number;
}

// ── helpers ────────────────────────────────────────────────────────────────────
const SENT_COLOR: Record<string, string> = {
  positive: "text-emerald-400",
  neutral:  "text-blue-400",
  cautious: "text-yellow-400",
  negative: "text-red-400",
};
const SENT_BG: Record<string, string> = {
  positive: "bg-emerald-900/30 border-emerald-700",
  neutral:  "bg-blue-900/30 border-blue-700",
  cautious: "bg-yellow-900/30 border-yellow-700",
  negative: "bg-red-900/30 border-red-700",
};
const ACTION_BADGE: Record<string, string> = {
  reinforce: "bg-emerald-900/50 text-emerald-300 border-emerald-700",
  nurture:   "bg-blue-900/50 text-blue-300 border-blue-700",
  reframe:   "bg-yellow-900/50 text-yellow-300 border-yellow-700",
  intervene: "bg-red-900/50 text-red-300 border-red-700",
};
const TONE_EMOJI: Record<string, string> = {
  enthusiastic:  "🔥",
  authoritative: "💼",
  hesitant:      "😰",
  evasive:       "🔄",
  resistant:     "🛡",
  panic_signal:  "🚨",
};
const TONE_LABEL: Record<string, string> = {
  enthusiastic:  "Enthusiastic",
  authoritative: "Authoritative",
  hesitant:      "Hesitant",
  evasive:       "Evasive",
  resistant:     "Resistant",
  panic_signal:  "Panic Signal",
};

// ── ToneRing ──────────────────────────────────────────────────────────────────
function ToneRing({ score, size = 88 }: { score: number; size?: number }) {
  const r = (size - 14) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = score >= 65 ? "#34d399" : score >= 45 ? "#60a5fa" : score >= 30 ? "#facc15" : "#f87171";
  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={9} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={9}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        style={{ transition: "stroke-dasharray 0.6s ease" }}
      />
    </svg>
  );
}

// ── ScoreBar ──────────────────────────────────────────────────────────────────
function ScoreBar({ label, score, color }: { label: string; score: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="font-semibold" style={{ color }}>{score.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-500" style={{ width: `${score}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

// ── SentimentBar ──────────────────────────────────────────────────────────────
function SentimentBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order  = ["positive", "neutral", "cautious", "negative"];
  const colors = ["#34d399", "#60a5fa", "#facc15", "#f87171"];
  const labels = ["Positive", "Neutral", "Cautious", "Negative"];
  return (
    <div>
      <div className="flex h-4 rounded-full overflow-hidden mb-2 gap-0.5">
        {order.map((k, i) => {
          const pct = total > 0 ? ((counts[k] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={k} style={{ width: `${pct}%`, backgroundColor: colors[i] }} title={labels[i]} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 flex-wrap">
        {order.map((k, i) => (
          <div key={k} className="flex items-center gap-1.5 text-xs text-slate-400">
            <span className="w-2 h-2 rounded-full inline-block" style={{ backgroundColor: colors[i] }} />
            {labels[i]}: {counts[k] || 0}
          </div>
        ))}
      </div>
    </div>
  );
}

// ── CallCard ──────────────────────────────────────────────────────────────────
function CallCard({ call, onClick }: { call: CallRecord; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:brightness-110 ${SENT_BG[call.tone_sentiment]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="font-semibold text-slate-100 text-sm">{call.deal_name}</p>
          <p className="text-xs text-slate-400">{call.rep_id} · {call.region} · {call.call_duration_minutes}min</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${ACTION_BADGE[call.tone_action]}`}>
            {call.tone_action.toUpperCase()}
          </span>
          {call.needs_immediate_coaching && (
            <span className="text-xs text-orange-400 font-semibold">🎯 COACH NOW</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-3 mt-2">
        <div className="relative flex-shrink-0">
          <ToneRing score={call.call_tone_composite} size={52} />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xs font-bold text-slate-200">{call.call_tone_composite.toFixed(0)}</span>
          </div>
        </div>
        <div className="flex-1 space-y-1 text-xs text-slate-300">
          <div className="flex justify-between">
            <span>Tone</span>
            <span className="font-semibold text-slate-200">{TONE_EMOJI[call.dominant_tone]} {TONE_LABEL[call.dominant_tone]}</span>
          </div>
          <div className="flex justify-between">
            <span>Advancement</span>
            <span className={`font-semibold ${call.deal_advancement_probability >= 60 ? "text-emerald-400" : "text-red-400"}`}>
              {call.deal_advancement_probability.toFixed(0)}%
            </span>
          </div>
          <div className="flex justify-between">
            <span>Coaching</span>
            <span className={`font-semibold ${call.call_coaching_priority >= 65 ? "text-orange-400" : "text-slate-400"}`}>
              {call.call_coaching_priority.toFixed(0)}/100
            </span>
          </div>
        </div>
      </div>
    </button>
  );
}

// ── CallModal ─────────────────────────────────────────────────────────────────
function CallModal({ call, onClose }: { call: CallRecord; onClose: () => void }) {
  const [tab, setTab] = useState<"tone" | "scores" | "coaching">("tone");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden">
        {/* header */}
        <div className={`px-6 py-4 border-b border-slate-700 flex items-start justify-between ${SENT_BG[call.tone_sentiment]}`}>
          <div>
            <h2 className="text-lg font-bold text-slate-100">{call.deal_name}</h2>
            <p className="text-sm text-slate-400">{call.rep_id} · {call.region} · {call.call_duration_minutes} min call</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-700">
          {(["tone", "scores", "coaching"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${tab === t ? "text-violet-400 border-b-2 border-violet-400" : "text-slate-400 hover:text-slate-200"}`}
            >
              {t === "tone" ? "Tone Analysis" : t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* body */}
        <div className="p-6 space-y-4">
          {tab === "tone" && (
            <>
              <div className="flex items-center gap-6">
                <div className="relative">
                  <ToneRing score={call.call_tone_composite} size={100} />
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-lg font-bold ${SENT_COLOR[call.tone_sentiment]}`}>{call.call_tone_composite.toFixed(1)}</span>
                    <span className="text-xs text-slate-400">Score</span>
                  </div>
                </div>
                <div className="flex-1 grid grid-cols-2 gap-3 text-sm">
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Sentiment</p>
                    <p className={`font-bold capitalize ${SENT_COLOR[call.tone_sentiment]}`}>{call.tone_sentiment}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Dominant Tone</p>
                    <p className="font-bold text-slate-200 text-xs">{TONE_EMOJI[call.dominant_tone]} {TONE_LABEL[call.dominant_tone]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Control</p>
                    <p className="font-bold text-slate-200 text-xs capitalize">{call.conversation_control.replace(/_/g, " ")}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Advancement</p>
                    <p className={`font-bold ${call.deal_advancement_probability >= 60 ? "text-emerald-400" : "text-red-400"}`}>
                      {call.deal_advancement_probability.toFixed(0)}%
                    </p>
                  </div>
                </div>
              </div>
              {call.needs_immediate_coaching && (
                <div className="bg-orange-950 border border-orange-700 rounded-lg p-3 text-sm text-orange-300">
                  🎯 Immediate coaching session recommended — this rep&apos;s call pattern shows signals that need urgent attention.
                </div>
              )}
              {call.dominant_tone === "panic_signal" && (
                <div className="bg-red-950 border border-red-700 rounded-lg p-3 text-sm text-red-300">
                  🚨 Panic signal detected — deal may be in serious jeopardy. Manager escalation recommended.
                </div>
              )}
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Rep Confidence"      score={call.rep_confidence_score}      color="#60a5fa" />
              <ScoreBar label="Buyer Engagement"    score={call.buyer_engagement_score}    color="#34d399" />
              <ScoreBar label="Objection Handling"  score={call.objection_handling_score}  color="#a78bfa" />
              <ScoreBar label="Conversation Quality" score={call.conversation_quality_score} color="#facc15" />
              <div className="pt-2 border-t border-slate-700 flex justify-between text-sm">
                <span className="text-slate-400">Positive Call?</span>
                <span className={`font-semibold ${call.is_positive_call ? "text-emerald-400" : "text-slate-400"}`}>
                  {call.is_positive_call ? "Yes ✓" : "No"}
                </span>
              </div>
            </div>
          )}

          {tab === "coaching" && (
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <div className="flex-1">
                  <p className="text-xs text-slate-400 mb-1">Coaching Priority</p>
                  <div className="h-3 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{
                        width: `${call.call_coaching_priority}%`,
                        backgroundColor: call.call_coaching_priority >= 65 ? "#f97316" : "#60a5fa",
                      }}
                    />
                  </div>
                </div>
                <span className={`text-lg font-bold ${call.call_coaching_priority >= 65 ? "text-orange-400" : "text-blue-400"}`}>
                  {call.call_coaching_priority.toFixed(0)}
                </span>
              </div>
              <div className={`rounded-xl p-4 border ${ACTION_BADGE[call.tone_action]}`}>
                <p className="text-xs font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="font-bold text-lg capitalize">{call.tone_action}</p>
              </div>
              {call.tone_action === "intervene" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Schedule 1:1 coaching session within 48 hours</li>
                  <li>Review call recording together — identify hesitation and objection handling gaps</li>
                  <li>Role-play objection responses before next call with this account</li>
                  <li>Consider shadowing next call or bringing manager to next meeting</li>
                </ul>
              )}
              {call.tone_action === "reframe" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Reframe the narrative — help rep shift tone to value-led conversation</li>
                  <li>Coach on using buyer language and matching their energy level</li>
                  <li>Practice open-ended discovery questions to regain conversational momentum</li>
                </ul>
              )}
              {call.tone_action === "nurture" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Call is performing adequately — review what&apos;s working before next call</li>
                  <li>Coach rep to improve buyer engagement with more active listening techniques</li>
                  <li>Add a clear closing question to improve deal advancement</li>
                </ul>
              )}
              {call.tone_action === "reinforce" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Excellent call — reinforce these behaviors in team review</li>
                  <li>Use this call recording as training example for other reps</li>
                  <li>Maintain this energy and approach in follow-up calls</li>
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────
export default function CallToneAnalyzerPage() {
  const [calls, setCalls]       = useState<CallRecord[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<CallRecord | null>(null);
  const [sentFilter, setSentFilter] = useState("all");
  const [toneFilter, setToneFilter] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (sentFilter !== "all") params.set("sentiment", sentFilter);
          if (toneFilter !== "all") params.set("tone", toneFilter);
          const r = await fetch(`/api/call-tone-analyzer?${params}`);
          const j = await r.json();
          setCalls(j.calls);
          setSummary(j.summary);
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [sentFilter, toneFilter]);

  const urgentCoaching = calls.filter((c) => c.needs_immediate_coaching);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Call Tone Analyzer</h1>
        <p className="text-slate-400 text-sm mt-1">AI emotional tone signals from sales calls — confidence, engagement, objection handling, and coaching priority</p>
      </div>

      {/* coaching alert */}
      {urgentCoaching.length > 0 && (
        <div className="bg-orange-950 border border-orange-700 rounded-xl p-4 flex items-start gap-3">
          <span className="text-orange-400 text-xl">🎯</span>
          <div>
            <p className="text-orange-300 font-semibold text-sm">{urgentCoaching.length} rep{urgentCoaching.length > 1 ? "s" : ""} need immediate coaching intervention</p>
            <p className="text-orange-400/80 text-xs mt-0.5">{urgentCoaching.map((c) => `${c.rep_id} (${c.deal_name})`).join(" · ")}</p>
          </div>
        </div>
      )}

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Total Calls",        value: summary.total },
            { label: "Positive Calls",     value: `${summary.positive_call_count} / ${summary.total}` },
            { label: "Coaching Needed",    value: summary.coaching_needed_count },
            { label: "Avg Tone Score",     value: summary.avg_call_tone_composite.toFixed(1) },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-400">{k.label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{k.value}</p>
            </div>
          ))}
        </div>
      )}

      {/* sentiment distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Call Sentiment Distribution</h2>
          <SentimentBar counts={summary.sentiment_counts} total={summary.total} />
        </div>
      )}

      {/* filters */}
      <div className="flex flex-wrap gap-2">
        {["all", "positive", "neutral", "cautious", "negative"].map((s) => (
          <button
            key={s}
            onClick={() => setSentFilter(s)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              sentFilter === s ? "bg-violet-600 border-violet-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {s === "all" ? "All Sentiments" : s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
        <div className="w-px bg-slate-700 mx-1" />
        {["all", "enthusiastic", "authoritative", "hesitant", "evasive", "resistant", "panic_signal"].map((t) => (
          <button
            key={t}
            onClick={() => setToneFilter(t)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              toneFilter === t ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {t === "all" ? "All Tones" : `${TONE_EMOJI[t]} ${TONE_LABEL[t]}`}
          </button>
        ))}
      </div>

      {/* avg scores */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
          <h2 className="text-sm font-semibold text-slate-300">Average Call Scores</h2>
          <ScoreBar label="Rep Confidence"     score={summary.avg_rep_confidence_score}     color="#60a5fa" />
          <ScoreBar label="Buyer Engagement"   score={summary.avg_buyer_engagement_score}   color="#34d399" />
          <ScoreBar label="Objection Handling" score={summary.avg_objection_handling_score} color="#a78bfa" />
          <div className="flex justify-between text-xs text-slate-400 pt-1">
            <span>Avg Deal Advancement Probability</span>
            <span className="text-emerald-400 font-semibold">{summary.avg_deal_advancement_probability.toFixed(1)}%</span>
          </div>
        </div>
      )}

      {/* call grid */}
      {loading ? (
        <p className="text-slate-400 text-sm">Analyzing calls…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {calls.map((c) => (
            <CallCard key={c.call_id} call={c} onClick={() => setSelected(c)} />
          ))}
        </div>
      )}

      {selected && <CallModal call={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
