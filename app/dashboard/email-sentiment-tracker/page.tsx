"use client";

import { useEffect, useState } from "react";

interface Thread {
  thread_id: string;
  deal_id: string;
  rep_id: string;
  thread_sentiment: string;
  sentiment_trajectory: string;
  buyer_engagement_signal: string;
  email_action: string;
  reply_quality_score: number;
  engagement_depth_score: number;
  sentiment_momentum_score: number;
  urgency_alignment_score: number;
  email_composite: number;
  predicted_open_probability: number;
  thread_health_index: number;
  is_thread_healthy: boolean;
  needs_intervention: boolean;
  region: string;
}

interface Summary {
  total: number;
  sentiment_counts: Record<string, number>;
  trajectory_counts: Record<string, number>;
  engagement_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_email_composite: number;
  avg_thread_health_index: number;
  healthy_count: number;
  intervention_count: number;
  avg_reply_quality_score: number;
  avg_engagement_depth_score: number;
  avg_sentiment_momentum_score: number;
  avg_urgency_alignment_score: number;
}

const SENTIMENT_COLOR: Record<string, string> = {
  enthusiastic: "#34d399",
  positive:     "#818cf8",
  neutral:      "#94a3b8",
  cooling:      "#facc15",
  negative:     "#f87171",
};

const SENTIMENT_BG: Record<string, string> = {
  enthusiastic: "bg-emerald-500/20 border-emerald-500/40",
  positive:     "bg-indigo-500/20 border-indigo-500/40",
  neutral:      "bg-slate-700/40 border-slate-600/40",
  cooling:      "bg-yellow-500/20 border-yellow-500/40",
  negative:     "bg-red-500/20 border-red-500/40",
};

const TRAJECTORY_ICONS: Record<string, string> = {
  improving:  "📈",
  stable:     "➡️",
  declining:  "📉",
  volatile:   "⚡",
  flatlined:  "💀",
};

const ENGAGEMENT_LABELS: Record<string, string> = {
  highly_engaged:    "Highly Engaged",
  engaged:           "Engaged",
  passively_engaged: "Passively Engaged",
  disengaging:       "Disengaging",
  disengaged:        "Disengaged",
};

const ACTION_LABELS: Record<string, string> = {
  keep_momentum: "Keep Momentum",
  reframe:       "Reframe Message",
  pattern_break: "Pattern Break",
  escalate_send: "Escalate Send",
};

function SentimentRing({ composite, sentiment }: { composite: number; sentiment: string }) {
  const r = 52;
  const circ = 2 * Math.PI * r;
  const fill = (composite / 100) * circ;
  const color = SENTIMENT_COLOR[sentiment] || "#64748b";
  return (
    <svg width="128" height="128" viewBox="0 0 128 128">
      <circle cx="64" cy="64" r={r} fill="none" stroke="#1e293b" strokeWidth="12" />
      <circle
        cx="64" cy="64" r={r} fill="none"
        stroke={color} strokeWidth="12"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 64 64)"
      />
      <text x="64" y="60" textAnchor="middle" fill={color} fontSize="22" fontWeight="bold">{composite}</text>
      <text x="64" y="78" textAnchor="middle" fill="#94a3b8" fontSize="10">Thread Score</text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-medium">{value}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${value}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function SentimentDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  const order = ["enthusiastic", "positive", "neutral", "cooling", "negative"];
  return (
    <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
      {order.map((k) =>
        (counts[k] || 0) > 0 ? (
          <div
            key={k}
            title={`${k}: ${counts[k]}`}
            style={{ width: `${((counts[k] || 0) / total) * 100}%`, backgroundColor: SENTIMENT_COLOR[k] }}
          />
        ) : null
      )}
    </div>
  );
}

function ThreadModal({ thread, onClose }: { thread: Thread; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-slate-100 font-semibold text-lg leading-tight">
                {TRAJECTORY_ICONS[thread.sentiment_trajectory]} {thread.deal_id}
              </h2>
              <p className="text-slate-400 text-sm mt-0.5">{thread.rep_id} · {thread.region}</p>
            </div>
            <span
              className={`text-xs font-bold uppercase px-2 py-1 rounded-full border ${SENTIMENT_BG[thread.thread_sentiment]}`}
              style={{ color: SENTIMENT_COLOR[thread.thread_sentiment] }}
            >
              {thread.thread_sentiment}
            </span>
          </div>
          <div className="flex gap-2 mt-4">
            {(["signals", "scores", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                  tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="p-5 space-y-4">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Trajectory", `${TRAJECTORY_ICONS[thread.sentiment_trajectory]} ${thread.sentiment_trajectory}`],
                  ["Engagement", ENGAGEMENT_LABELS[thread.buyer_engagement_signal] || thread.buyer_engagement_signal],
                  ["Open Prob.", `${thread.predicted_open_probability}%`],
                  ["Thread Health", `${thread.thread_health_index}/100`],
                ].map(([label, value]) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <p className="text-xs text-slate-500">{label}</p>
                    <p className="text-sm font-semibold text-slate-100 capitalize mt-0.5">{value}</p>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 flex-wrap">
                {thread.is_thread_healthy && (
                  <span className="text-xs bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 rounded-lg px-2 py-1">
                    ✅ Healthy Thread
                  </span>
                )}
                {thread.needs_intervention && (
                  <span className="text-xs bg-red-500/15 text-red-400 border border-red-500/30 rounded-lg px-2 py-1">
                    🚨 Needs Intervention
                  </span>
                )}
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Reply Quality" value={thread.reply_quality_score} color="#818cf8" />
              <ScoreBar label="Engagement Depth" value={thread.engagement_depth_score} color="#34d399" />
              <ScoreBar label="Sentiment Momentum" value={thread.sentiment_momentum_score} color="#fb923c" />
              <ScoreBar label="Urgency Alignment" value={thread.urgency_alignment_score} color="#f472b6" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Email Composite" value={thread.email_composite} color={SENTIMENT_COLOR[thread.thread_sentiment]} />
              </div>
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">Recommended Action</p>
                <p className="text-indigo-300 font-semibold">{ACTION_LABELS[thread.email_action] || thread.email_action}</p>
              </div>
              {thread.email_action === "escalate_send" && (
                <p className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-red-300 text-xs">
                  Thread is flatlined. Send a final breakup email from a senior executive. Create urgency with a hard deadline or close the deal.
                </p>
              )}
              {thread.email_action === "pattern_break" && (
                <p className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3 text-orange-300 text-xs">
                  Engagement is declining. Change communication channel (phone or video), update your subject line, or lead with a radically different value angle.
                </p>
              )}
              {thread.email_action === "reframe" && (
                <p className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 text-yellow-300 text-xs">
                  Thread is plateauing. Reframe with a new business case, customer story, or ROI calculation to re-spark interest.
                </p>
              )}
              {thread.email_action === "keep_momentum" && (
                <p className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 text-emerald-300 text-xs">
                  Buyer is engaged and responding positively. Maintain cadence and guide toward a next step or demo date.
                </p>
              )}
            </div>
          )}
        </div>

        <div className="p-4 border-t border-slate-800">
          <button onClick={onClose} className="w-full py-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function ThreadCard({ thread, onClick }: { thread: Thread; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`bg-slate-900 border rounded-2xl p-4 cursor-pointer hover:border-indigo-500/50 transition-all ${SENTIMENT_BG[thread.thread_sentiment]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="min-w-0">
          <p className="text-slate-100 font-semibold text-sm truncate">
            {TRAJECTORY_ICONS[thread.sentiment_trajectory]} {thread.deal_id}
          </p>
          <p className="text-slate-500 text-xs mt-0.5">{thread.region} · {thread.rep_id}</p>
        </div>
        <span
          className="text-xs font-bold uppercase shrink-0"
          style={{ color: SENTIMENT_COLOR[thread.thread_sentiment] }}
        >
          {thread.thread_sentiment}
        </span>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <SentimentRing composite={thread.email_composite} sentiment={thread.thread_sentiment} />
        <div className="flex-1 space-y-2 min-w-0">
          <ScoreBar label="Reply Quality" value={thread.reply_quality_score} color="#818cf8" />
          <ScoreBar label="Eng. Depth" value={thread.engagement_depth_score} color="#34d399" />
          <ScoreBar label="Momentum" value={thread.sentiment_momentum_score} color="#fb923c" />
          <ScoreBar label="Urgency" value={thread.urgency_alignment_score} color="#f472b6" />
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">
          Open Prob: <span style={{ color: SENTIMENT_COLOR[thread.thread_sentiment] }} className="font-medium">{thread.predicted_open_probability}%</span>
        </span>
        <span className="text-slate-400">
          Health: <span className="text-indigo-300 font-medium">{thread.thread_health_index}</span>
        </span>
      </div>
      <div className="flex gap-1 mt-2 flex-wrap">
        {thread.is_thread_healthy && (
          <span className="text-xs bg-emerald-500/15 text-emerald-400 rounded px-1.5 py-0.5">✅ Healthy</span>
        )}
        {thread.needs_intervention && (
          <span className="text-xs bg-red-500/15 text-red-400 rounded px-1.5 py-0.5">🚨 Intervene</span>
        )}
      </div>
    </div>
  );
}

export default function EmailSentimentTrackerPage() {
  const [data, setData] = useState<{ threads: Thread[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Thread | null>(null);
  const [filterSentiment, setFilterSentiment] = useState("all");
  const [filterTrajectory, setFilterTrajectory] = useState("all");

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (filterSentiment !== "all")  params.set("sentiment", filterSentiment);
        if (filterTrajectory !== "all") params.set("trajectory", filterTrajectory);
        const res = await fetch(`/api/email-sentiment-tracker?${params}`);
        setData(await res.json());
  }
    load();
  }, [filterSentiment, filterTrajectory]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        <div>
          <h1 className="text-2xl font-bold text-slate-100">Email Sentiment Tracker</h1>
          <p className="text-slate-400 text-sm mt-1">Monitor the emotional trajectory of email threads to detect waning interest before deals go cold</p>
        </div>

        {s && s.intervention_count > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">📧</span>
            <div>
              <p className="text-red-300 font-semibold">
                {s.intervention_count} {s.intervention_count === 1 ? "thread" : "threads"} need immediate intervention
              </p>
              <p className="text-red-400/80 text-xs mt-0.5">
                {s.healthy_count} {s.healthy_count === 1 ? "thread" : "threads"} are healthy with strong buyer engagement
              </p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: "Total Threads", value: s?.total ?? "—", sub: "monitored" },
            { label: "Avg Score", value: s ? `${s.avg_email_composite}` : "—", sub: "email composite" },
            { label: "Need Intervention", value: s?.intervention_count ?? "—", sub: "threads" },
            { label: "Avg Health", value: s ? `${s.avg_thread_health_index}` : "—", sub: "thread health index" },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <p className="text-xs text-slate-500">{label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{value}</p>
              <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
            </div>
          ))}
        </div>

        {s && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Sentiment Distribution</h3>
              <SentimentDistBar counts={s.sentiment_counts} />
              <div className="flex flex-wrap gap-x-4 gap-y-1 mt-3">
                {Object.entries(s.sentiment_counts).map(([k, v]) => (
                  <span key={k} className="text-xs" style={{ color: SENTIMENT_COLOR[k] || "#94a3b8" }}>
                    {k}: {v}
                  </span>
                ))}
              </div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Score Breakdown</h3>
              <div className="space-y-2">
                <ScoreBar label="Reply Quality" value={s.avg_reply_quality_score} color="#818cf8" />
                <ScoreBar label="Engagement Depth" value={s.avg_engagement_depth_score} color="#34d399" />
                <ScoreBar label="Sentiment Momentum" value={s.avg_sentiment_momentum_score} color="#fb923c" />
                <ScoreBar label="Urgency Alignment" value={s.avg_urgency_alignment_score} color="#f472b6" />
              </div>
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-2">
          <div className="flex gap-1 flex-wrap">
            {["all", "enthusiastic", "positive", "neutral", "cooling", "negative"].map((s) => (
              <button
                key={s}
                onClick={() => setFilterSentiment(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterSentiment === s ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {s === "all" ? "All Sentiment" : s.charAt(0).toUpperCase() + s.slice(1)}
              </button>
            ))}
          </div>
          <div className="flex gap-1 flex-wrap">
            {["all", "improving", "stable", "declining", "volatile", "flatlined"].map((t) => (
              <button
                key={t}
                onClick={() => setFilterTrajectory(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterTrajectory === t ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {t === "all" ? "All Trajectories" : `${TRAJECTORY_ICONS[t] || ""} ${t}`}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {data?.threads.map((t) => (
            <ThreadCard key={t.thread_id} thread={t} onClick={() => setSelected(t)} />
          ))}
        </div>

        {data?.threads.length === 0 && (
          <div className="text-center py-16 text-slate-500">No threads match the selected filters.</div>
        )}
      </div>

      {selected && <ThreadModal thread={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
