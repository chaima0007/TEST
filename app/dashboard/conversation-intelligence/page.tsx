"use client";

import { useEffect, useState } from "react";

interface Call {
  call_id: string;
  deal_id: string;
  rep_id: string;
  conversation_quality: string;
  conversation_pattern: string;
  qualification_depth: string;
  conversation_action: string;
  discovery_score: number;
  qualification_score: number;
  communication_score: number;
  value_articulation_score: number;
  conversation_composite: number;
  coaching_priority_score: number;
  deal_advancement_score: number;
  is_coachable_moment: boolean;
  is_exemplary_call: boolean;
  call_type: string;
  region: string;
}

interface Summary {
  total: number;
  quality_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  depth_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_conversation_composite: number;
  avg_deal_advancement_score: number;
  coachable_count: number;
  exemplary_count: number;
  avg_discovery_score: number;
  avg_qualification_score: number;
  avg_communication_score: number;
  avg_value_articulation_score: number;
}

const QUALITY_COLOR: Record<string, string> = {
  elite:      "#34d399",
  proficient: "#818cf8",
  developing: "#facc15",
  poor:       "#f87171",
};

const QUALITY_BG: Record<string, string> = {
  elite:      "bg-emerald-500/20 border-emerald-500/40",
  proficient: "bg-indigo-500/20 border-indigo-500/40",
  developing: "bg-yellow-500/20 border-yellow-500/40",
  poor:       "bg-red-500/20 border-red-500/40",
};

const PATTERN_ICONS: Record<string, string> = {
  challenger:       "⚡",
  consultative:     "🧠",
  balanced_dialogue:"⚖️",
  feature_dump:     "📦",
  shallow_discovery:"🔍",
  monologue:        "📢",
};

const ACTION_LABELS: Record<string, string> = {
  share_as_example:     "Share as Team Example",
  reinforce_strengths:  "Reinforce Strengths",
  structured_coaching:  "Structured Coaching",
  coach_immediately:    "Coach Immediately",
};

function ConvRing({ composite, quality }: { composite: number; quality: string }) {
  const r = 52;
  const circ = 2 * Math.PI * r;
  const fill = (composite / 100) * circ;
  const color = QUALITY_COLOR[quality] || "#64748b";
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
      <text x="64" y="78" textAnchor="middle" fill="#94a3b8" fontSize="10">Call Score</text>
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

function QualityDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  const order = ["elite", "proficient", "developing", "poor"];
  return (
    <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
      {order.map((k) =>
        (counts[k] || 0) > 0 ? (
          <div
            key={k}
            title={`${k}: ${counts[k]}`}
            style={{ width: `${((counts[k] || 0) / total) * 100}%`, backgroundColor: QUALITY_COLOR[k] }}
          />
        ) : null
      )}
    </div>
  );
}

function CallModal({ call, onClose }: { call: Call; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "coaching">("signals");

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
                {PATTERN_ICONS[call.conversation_pattern]} {call.deal_id}
              </h2>
              <p className="text-slate-400 text-sm mt-0.5">
                {call.rep_id} · {call.call_type} · {call.region}
              </p>
            </div>
            <span
              className={`text-xs font-bold uppercase px-2 py-1 rounded-full border ${QUALITY_BG[call.conversation_quality]}`}
              style={{ color: QUALITY_COLOR[call.conversation_quality] }}
            >
              {call.conversation_quality}
            </span>
          </div>
          <div className="flex gap-2 mt-4">
            {(["signals", "scores", "coaching"] as const).map((t) => (
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
                  ["Pattern", `${PATTERN_ICONS[call.conversation_pattern]} ${call.conversation_pattern.replace(/_/g, " ")}`],
                  ["Qual Depth", call.qualification_depth.replace(/_/g, " ")],
                  ["Deal Advancement", `${call.deal_advancement_score}%`],
                  ["Coaching Priority", `${call.coaching_priority_score}/100`],
                ].map(([label, value]) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <p className="text-xs text-slate-500">{label}</p>
                    <p className="text-sm font-semibold text-slate-100 capitalize mt-0.5">{value}</p>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 flex-wrap">
                {call.is_exemplary_call && (
                  <span className="text-xs bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 rounded-lg px-2 py-1">
                    ⭐ Exemplary Call
                  </span>
                )}
                {call.is_coachable_moment && (
                  <span className="text-xs bg-orange-500/15 text-orange-400 border border-orange-500/30 rounded-lg px-2 py-1">
                    🎯 Coaching Moment
                  </span>
                )}
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Discovery Score" value={call.discovery_score} color="#818cf8" />
              <ScoreBar label="Qualification Score" value={call.qualification_score} color="#34d399" />
              <ScoreBar label="Communication Score" value={call.communication_score} color="#fb923c" />
              <ScoreBar label="Value Articulation" value={call.value_articulation_score} color="#a78bfa" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Conversation Composite" value={call.conversation_composite} color={QUALITY_COLOR[call.conversation_quality]} />
              </div>
            </div>
          )}
          {tab === "coaching" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">Recommended Action</p>
                <p className="text-indigo-300 font-semibold">{ACTION_LABELS[call.conversation_action] || call.conversation_action}</p>
              </div>
              {call.conversation_action === "coach_immediately" && (
                <p className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-red-300 text-xs">
                  Critical coaching needed. Focus on discovery framework, talk-listen ratio, and securing defined next steps before the next customer call.
                </p>
              )}
              {call.conversation_action === "structured_coaching" && (
                <p className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 text-yellow-300 text-xs">
                  Schedule a dedicated coaching session this week. Review the call recording together and identify 2-3 specific improvement areas.
                </p>
              )}
              {call.conversation_action === "reinforce_strengths" && (
                <p className="bg-indigo-500/10 border border-indigo-500/20 rounded-lg p-3 text-indigo-300 text-xs">
                  Strong performance. Reinforce what worked — especially the discovery questions and value articulation. Keep momentum.
                </p>
              )}
              {call.conversation_action === "share_as_example" && (
                <p className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 text-emerald-300 text-xs">
                  Exemplary call. Share the recording with the full sales team as a best practice example in the next team meeting.
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

function CallCard({ call, onClick }: { call: Call; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`bg-slate-900 border rounded-2xl p-4 cursor-pointer hover:border-indigo-500/50 transition-all ${QUALITY_BG[call.conversation_quality]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="min-w-0">
          <p className="text-slate-100 font-semibold text-sm truncate">
            {PATTERN_ICONS[call.conversation_pattern]} {call.deal_id}
          </p>
          <p className="text-slate-500 text-xs mt-0.5">{call.rep_id} · {call.call_type} · {call.region}</p>
        </div>
        <span
          className="text-xs font-bold uppercase shrink-0"
          style={{ color: QUALITY_COLOR[call.conversation_quality] }}
        >
          {call.conversation_quality}
        </span>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <ConvRing composite={call.conversation_composite} quality={call.conversation_quality} />
        <div className="flex-1 space-y-2 min-w-0">
          <ScoreBar label="Discovery" value={call.discovery_score} color="#818cf8" />
          <ScoreBar label="Qualification" value={call.qualification_score} color="#34d399" />
          <ScoreBar label="Communication" value={call.communication_score} color="#fb923c" />
          <ScoreBar label="Value" value={call.value_articulation_score} color="#a78bfa" />
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">
          Deal Adv: <span style={{ color: QUALITY_COLOR[call.conversation_quality] }} className="font-medium">{call.deal_advancement_score}%</span>
        </span>
        <span className="text-slate-400">
          Coaching: <span className="text-orange-400 font-medium">{call.coaching_priority_score}</span>
        </span>
      </div>
      <div className="flex gap-1 mt-2 flex-wrap">
        {call.is_exemplary_call && (
          <span className="text-xs bg-emerald-500/15 text-emerald-400 rounded px-1.5 py-0.5">⭐ Exemplary</span>
        )}
        {call.is_coachable_moment && (
          <span className="text-xs bg-orange-500/15 text-orange-400 rounded px-1.5 py-0.5">🎯 Coach</span>
        )}
      </div>
    </div>
  );
}

export default function ConversationIntelligencePage() {
  const [data, setData] = useState<{ calls: Call[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Call | null>(null);
  const [filterQuality, setFilterQuality] = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (filterQuality !== "all") params.set("quality", filterQuality);
        if (filterPattern !== "all") params.set("pattern", filterPattern);
        const res = await fetch(`/api/conversation-intelligence?${params}`);
        setData(await res.json());
  }
    load();
  }, [filterQuality, filterPattern]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        <div>
          <h1 className="text-2xl font-bold text-slate-100">Conversation Intelligence</h1>
          <p className="text-slate-400 text-sm mt-1">Score sales calls for discovery quality, MEDDIC depth, communication, and value articulation</p>
        </div>

        {s && s.coachable_count > 0 && (
          <div className="bg-orange-500/10 border border-orange-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">🎯</span>
            <div>
              <p className="text-orange-300 font-semibold">
                {s.coachable_count} {s.coachable_count === 1 ? "call" : "calls"} identified as coachable moments
              </p>
              <p className="text-orange-400/80 text-xs mt-0.5">
                {s.exemplary_count} exemplary {s.exemplary_count === 1 ? "call" : "calls"} ready to share as team best practices
              </p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: "Total Calls", value: s?.total ?? "—", sub: "analyzed" },
            { label: "Avg Score", value: s ? `${s.avg_conversation_composite}` : "—", sub: "composite" },
            { label: "Coachable", value: s?.coachable_count ?? "—", sub: "need coaching" },
            { label: "Avg Advancement", value: s ? `${s.avg_deal_advancement_score}%` : "—", sub: "deal progress" },
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
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Quality Distribution</h3>
              <QualityDistBar counts={s.quality_counts} />
              <div className="flex flex-wrap gap-x-4 gap-y-1 mt-3">
                {Object.entries(s.quality_counts).map(([k, v]) => (
                  <span key={k} className="text-xs" style={{ color: QUALITY_COLOR[k] || "#94a3b8" }}>
                    {k}: {v}
                  </span>
                ))}
              </div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Score Breakdown</h3>
              <div className="space-y-2">
                <ScoreBar label="Discovery" value={s.avg_discovery_score} color="#818cf8" />
                <ScoreBar label="Qualification" value={s.avg_qualification_score} color="#34d399" />
                <ScoreBar label="Communication" value={s.avg_communication_score} color="#fb923c" />
                <ScoreBar label="Value Articulation" value={s.avg_value_articulation_score} color="#a78bfa" />
              </div>
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-2">
          <div className="flex gap-1 flex-wrap">
            {["all", "elite", "proficient", "developing", "poor"].map((q) => (
              <button
                key={q}
                onClick={() => setFilterQuality(q)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterQuality === q ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {q === "all" ? "All Quality" : q.charAt(0).toUpperCase() + q.slice(1)}
              </button>
            ))}
          </div>
          <div className="flex gap-1 flex-wrap">
            {["all", "challenger", "consultative", "balanced_dialogue", "feature_dump", "shallow_discovery", "monologue"].map((p) => (
              <button
                key={p}
                onClick={() => setFilterPattern(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterPattern === p ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {p === "all" ? "All Patterns" : `${PATTERN_ICONS[p] || ""} ${p.replace(/_/g, " ")}`}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {data?.calls.map((c) => (
            <CallCard key={c.call_id} call={c} onClick={() => setSelected(c)} />
          ))}
        </div>

        {data?.calls.length === 0 && (
          <div className="text-center py-16 text-slate-500">No calls match the selected filters.</div>
        )}
      </div>

      {selected && <CallModal call={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
