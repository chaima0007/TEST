"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────
interface Meeting {
  meeting_id: string;
  deal_id: string;
  rep_id: string;
  rep_name: string;
  account_name: string;
  meeting_type: string;
  meeting_outcome: string;
  meeting_quality: string;
  buying_signal_strength: string;
  follow_up_urgency: string;
  quality_score: number;
  engagement_score: number;
  buying_signals_count: number;
  objections_count: number;
  next_step_agreed: boolean;
  next_step_days_out: number | null;
  positive_signals: string[];
  concerns: string[];
  follow_up_actions: string[];
  manager_alerts: string[];
}

interface Summary {
  total: number;
  outcome_counts: Record<string, number>;
  quality_counts: Record<string, number>;
  urgency_counts: Record<string, number>;
  signal_counts: Record<string, number>;
  avg_quality_score: number;
  avg_engagement_score: number;
  next_step_rate: number;
  advancement_rate: number;
  immediate_follow_up_count: number;
}

// ── Colour helpers ─────────────────────────────────────────────────────────────
function qualityColor(q: string) {
  return q === "excellent" ? "#6366f1"
       : q === "good"      ? "#22c55e"
       : q === "average"   ? "#f59e0b"
       :                     "#ef4444";
}

function outcomeColor(o: string) {
  return o === "advanced"    ? "#22c55e"
       : o === "maintained"  ? "#6366f1"
       : o === "no_decision" ? "#f59e0b"
       :                       "#ef4444";
}

function urgencyColor(u: string) {
  return u === "immediate"  ? "#ef4444"
       : u === "same_week"  ? "#f59e0b"
       : u === "standard"   ? "#6366f1"
       :                      "#22c55e";
}

function signalColor(s: string) {
  return s === "strong"   ? "#22c55e"
       : s === "moderate" ? "#6366f1"
       : s === "weak"     ? "#f59e0b"
       :                    "#ef4444";
}

function urgencyBadge(u: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return u === "immediate"  ? `${base} bg-red-500/20 text-red-300`
       : u === "same_week"  ? `${base} bg-amber-500/20 text-amber-300`
       : u === "standard"   ? `${base} bg-indigo-500/20 text-indigo-300`
       :                      `${base} bg-emerald-500/20 text-emerald-300`;
}

function outcomeBadge(o: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return o === "advanced"    ? `${base} bg-emerald-500/20 text-emerald-300`
       : o === "maintained"  ? `${base} bg-indigo-500/20 text-indigo-300`
       : o === "no_decision" ? `${base} bg-amber-500/20 text-amber-300`
       :                       `${base} bg-red-500/20 text-red-300`;
}

function signalBadge(s: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return s === "strong"   ? `${base} bg-emerald-500/20 text-emerald-300`
       : s === "moderate" ? `${base} bg-indigo-500/20 text-indigo-300`
       : s === "weak"     ? `${base} bg-amber-500/20 text-amber-300`
       :                    `${base} bg-red-500/20 text-red-300`;
}

function meetingTypeLabel(t: string) {
  const map: Record<string, string> = {
    intro: "Intro",
    discovery: "Découverte",
    demo: "Démo",
    proposal_review: "Revue Propale",
    negotiation: "Négociation",
    executive_review: "Revue Exec",
    follow_up: "Suivi",
    qbr: "QBR",
  };
  return map[t] ?? t;
}

function outcomeLabel(o: string) {
  const map: Record<string, string> = {
    advanced: "Avancé",
    maintained: "Maintenu",
    no_decision: "Sans décision",
    regressed: "Régressé",
  };
  return map[o] ?? o;
}

function signalLabel(s: string) {
  const map: Record<string, string> = {
    strong: "Fort",
    moderate: "Modéré",
    weak: "Faible",
    negative: "Négatif",
  };
  return map[s] ?? s;
}

function urgencyLabel(u: string) {
  const map: Record<string, string> = {
    immediate: "Immédiat",
    same_week: "Cette semaine",
    standard: "Standard",
    monitor: "À surveiller",
  };
  return map[u] ?? u;
}

// ── QualityRing SVG ────────────────────────────────────────────────────────────
function QualityRing({ score, quality }: { score: number; quality: string }) {
  const r = 30, cx = 38, cy = 38;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const color = qualityColor(quality);
  return (
    <svg width="76" height="76" viewBox="0 0 76 76">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke={color} strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={`${arc} ${circ - arc}`}
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy - 3} textAnchor="middle" fill={color} fontSize="13" fontWeight="700">
        {Math.round(score)}
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">
        qualité
      </text>
    </svg>
  );
}

// ── Signal bar ─────────────────────────────────────────────────────────────────
function SignalBar({ count, maxCount, strength }: { count: number; maxCount: number; strength: string }) {
  const pct = maxCount > 0 ? (count / maxCount) * 100 : 0;
  const color = signalColor(strength);
  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="w-20 text-right text-slate-400 capitalize">{signalLabel(strength)}</span>
      <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="w-4 text-slate-300 font-semibold">{count}</span>
    </div>
  );
}

// ── MeetingModal ───────────────────────────────────────────────────────────────
function MeetingModal({ m, onClose }: { m: Meeting; onClose: () => void }) {
  const [tab, setTab] = useState<"actions" | "signals" | "alerts">("actions");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[88vh] overflow-y-auto mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-white">{m.account_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">
                {m.rep_name} · {meetingTypeLabel(m.meeting_type)}
              </p>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-4">
            <span className={outcomeBadge(m.meeting_outcome)}>{outcomeLabel(m.meeting_outcome)}</span>
            <span className={signalBadge(m.buying_signal_strength)}>{signalLabel(m.buying_signal_strength)} signal</span>
            <span className={urgencyBadge(m.follow_up_urgency)}>{urgencyLabel(m.follow_up_urgency)}</span>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-white">{Math.round(m.quality_score)}</p>
              <p className="text-xs text-slate-400">Score qualité</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-white">{m.buying_signals_count}</p>
              <p className="text-xs text-slate-400">Signaux achat</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-white">{m.objections_count}</p>
              <p className="text-xs text-slate-400">Objections</p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["actions", "signals", "alerts"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "actions" ? "Plan de suivi" : t === "signals" ? "Signaux d'achat" : "Alertes & risques"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6 space-y-3">
          {tab === "actions" && (
            <>
              {m.follow_up_actions.length > 0 ? (
                m.follow_up_actions.map((a, i) => (
                  <div key={i} className="flex items-start gap-3 bg-slate-800/50 rounded-xl p-3">
                    <span className="text-indigo-400 text-sm font-bold mt-0.5">{i + 1}</span>
                    <p className="text-slate-200 text-sm">{a}</p>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucune action de suivi requise.</p>
              )}
              {m.next_step_agreed && m.next_step_days_out !== null && (
                <div className="bg-indigo-900/30 border border-indigo-800/50 rounded-xl p-3 mt-2">
                  <p className="text-indigo-300 text-sm font-semibold">
                    Prochaine étape dans {m.next_step_days_out} jour{m.next_step_days_out > 1 ? "s" : ""}
                  </p>
                </div>
              )}
            </>
          )}
          {tab === "signals" && (
            <>
              {m.positive_signals.length > 0 && (
                <div className="space-y-2">
                  <p className="text-emerald-400 text-xs font-semibold uppercase tracking-wider">Signaux positifs</p>
                  {m.positive_signals.map((s, i) => (
                    <div key={i} className="flex items-start gap-2 bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-3">
                      <span className="text-emerald-400 text-sm mt-0.5">✓</span>
                      <p className="text-slate-200 text-sm">{s}</p>
                    </div>
                  ))}
                </div>
              )}
              {m.concerns.length > 0 && (
                <div className="space-y-2 mt-4">
                  <p className="text-amber-400 text-xs font-semibold uppercase tracking-wider">Points de vigilance</p>
                  {m.concerns.map((c, i) => (
                    <div key={i} className="flex items-start gap-2 bg-amber-900/20 border border-amber-800/30 rounded-xl p-3">
                      <span className="text-amber-400 text-sm mt-0.5">!</span>
                      <p className="text-slate-200 text-sm">{c}</p>
                    </div>
                  ))}
                </div>
              )}
              {m.positive_signals.length === 0 && m.concerns.length === 0 && (
                <p className="text-slate-500 text-sm">Aucun signal détecté.</p>
              )}
            </>
          )}
          {tab === "alerts" && (
            <>
              {m.manager_alerts.length > 0 ? (
                <div className="space-y-2">
                  {m.manager_alerts.map((a, i) => (
                    <div key={i} className="flex items-start gap-2 bg-red-900/20 border border-red-800/40 rounded-xl p-3">
                      <span className="text-red-400 text-sm mt-0.5">⚠</span>
                      <p className="text-slate-200 text-sm">{a}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-4 text-center">
                  <p className="text-emerald-400 text-sm font-medium">Aucune alerte manager</p>
                  <p className="text-slate-400 text-xs mt-1">Réunion gérée correctement</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ── MeetingCard ────────────────────────────────────────────────────────────────
function MeetingCard({ m, onClick }: { m: Meeting; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-4 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4">
        <QualityRing score={m.quality_score} quality={m.meeting_quality} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm truncate">{m.account_name}</h3>
              <p className="text-slate-400 text-xs mt-0.5">{m.rep_name} · {meetingTypeLabel(m.meeting_type)}</p>
            </div>
            <span className={urgencyBadge(m.follow_up_urgency)}>{urgencyLabel(m.follow_up_urgency)}</span>
          </div>

          {/* outcome + signal */}
          <div className="flex gap-2 mt-2">
            <span className={outcomeBadge(m.meeting_outcome)}>{outcomeLabel(m.meeting_outcome)}</span>
            <span className={signalBadge(m.buying_signal_strength)}>{signalLabel(m.buying_signal_strength)}</span>
          </div>

          {/* Signals vs objections */}
          <div className="flex items-center gap-4 mt-3">
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-emerald-400" />
              <span className="text-slate-300 text-xs">{m.buying_signals_count} signal{m.buying_signals_count !== 1 ? "s" : ""}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-red-400" />
              <span className="text-slate-300 text-xs">{m.objections_count} objection{m.objections_count !== 1 ? "s" : ""}</span>
            </div>
            {m.next_step_agreed && m.next_step_days_out !== null && (
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full bg-indigo-400" />
                <span className="text-slate-300 text-xs">J+{m.next_step_days_out}</span>
              </div>
            )}
          </div>

          {/* Manager alerts */}
          {m.manager_alerts.length > 0 && (
            <div className="mt-2 flex items-center gap-1.5 bg-red-900/20 border border-red-800/30 rounded-lg px-2.5 py-1.5">
              <span className="text-red-400 text-xs">⚠</span>
              <p className="text-red-300 text-xs">{m.manager_alerts[0]}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────
export default function MeetingIntelligencePage() {
  const [data, setData] = useState<{ meetings: Meeting[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Meeting | null>(null);
  const [outcomeFilter, setOutcomeFilter] = useState<string>("all");
  const [urgencyFilter, setUrgencyFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (outcomeFilter !== "all") params.set("outcome", outcomeFilter);
      if (urgencyFilter !== "all") params.set("urgency", urgencyFilter);
      const res = await fetch(`/api/meeting-intelligence?${params.toString()}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [outcomeFilter, urgencyFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const s = data?.summary;
  const totalSignals = s
    ? Object.values(s.signal_counts).reduce((a, b) => a + b, 0)
    : 0;

  const outcomeOptions = ["all", "advanced", "maintained", "no_decision", "regressed"];
  const urgencyOptions = ["all", "immediate", "same_week", "standard", "monitor"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Intelligence Réunions</h1>
          <p className="text-slate-400 mt-1">Analyse qualité des réunions · signaux d&apos;achat · plan de suivi</p>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
          {[
            { label: "Réunions analysées", value: s?.total ?? "—", accent: "text-white" },
            { label: "Score qualité moy.", value: s ? `${s.avg_quality_score}` : "—", accent: "text-indigo-400" },
            { label: "Score engagement moy.", value: s ? `${s.avg_engagement_score}` : "—", accent: "text-violet-400" },
            { label: "Taux next step", value: s ? `${s.next_step_rate}%` : "—", accent: "text-emerald-400" },
            { label: "Taux avancement", value: s ? `${s.advancement_rate}%` : "—", accent: "text-sky-400" },
            { label: "Suivi immédiat", value: s?.immediate_follow_up_count ?? "—", accent: "text-red-400" },
          ].map((kpi) => (
            <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <p className={`text-2xl font-bold ${kpi.accent}`}>{kpi.value}</p>
              <p className="text-slate-400 text-xs mt-1">{kpi.label}</p>
            </div>
          ))}
        </div>

        {/* Signal strength distribution */}
        {s && (
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-5 mb-8">
            <h2 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">
              Distribution des signaux d&apos;achat
            </h2>
            <div className="space-y-2">
              {["strong", "moderate", "weak", "negative"].map((str) => (
                <SignalBar
                  key={str}
                  strength={str}
                  count={s.signal_counts[str] ?? 0}
                  maxCount={totalSignals}
                />
              ))}
            </div>
          </div>
        )}

        {/* Outcome mini-stats */}
        {s && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
            {["advanced", "maintained", "no_decision", "regressed"].map((o) => (
              <div
                key={o}
                className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 flex items-center gap-3"
              >
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: outcomeColor(o) }} />
                <div>
                  <p className="text-lg font-bold text-white">{s.outcome_counts[o] ?? 0}</p>
                  <p className="text-xs text-slate-400 capitalize">{outcomeLabel(o)}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Filters */}
        <div className="space-y-3 mb-6">
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Résultat :</span>
            {outcomeOptions.map((o) => (
              <button
                key={o}
                onClick={() => setOutcomeFilter(o)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  outcomeFilter === o
                    ? "bg-indigo-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {o === "all" ? "Tous" : outcomeLabel(o)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Urgence :</span>
            {urgencyOptions.map((u) => (
              <button
                key={u}
                onClick={() => setUrgencyFilter(u)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  urgencyFilter === u
                    ? "bg-violet-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {u === "all" ? "Tous" : urgencyLabel(u)}
              </button>
            ))}
          </div>
        </div>

        {/* Meeting grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {data?.meetings.map((m) => (
              <MeetingCard key={m.meeting_id} m={m} onClick={() => setSelected(m)} />
            ))}
          </div>
        )}

        {data?.meetings.length === 0 && !loading && (
          <div className="text-center py-16 text-slate-500">
            <p className="text-lg">Aucune réunion trouvée pour ces filtres.</p>
          </div>
        )}
      </div>

      {selected && <MeetingModal m={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
