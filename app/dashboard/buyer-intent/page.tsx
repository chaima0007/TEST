"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────
interface Prospect {
  prospect_id: string;
  company_name: string;
  rep_id: string;
  rep_name: string;
  intent_level: string;
  intent_category: string;
  intent_trend: string;
  outreach_strategy: string;
  intent_score: number;
  digital_score: number;
  engagement_score: number;
  trigger_score: number;
  hot_signals: string[];
  cold_signals: string[];
  recommended_actions: string[];
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  category_counts: Record<string, number>;
  trend_counts: Record<string, number>;
  strategy_counts: Record<string, number>;
  avg_intent_score: number;
  avg_digital_score: number;
  avg_engagement_score: number;
  hot_count: number;
  immediate_outreach_count: number;
}

// ── Colour helpers ─────────────────────────────────────────────────────────────
function levelColor(l: string) {
  return l === "hot"      ? "#ef4444"
       : l === "warm"     ? "#f97316"
       : l === "lukewarm" ? "#f59e0b"
       : l === "cold"     ? "#6366f1"
       :                    "#475569"; // unknown
}

function trendColor(t: string) {
  return t === "spiked"       ? "#ef4444"
       : t === "accelerating" ? "#f97316"
       : t === "stable"       ? "#6366f1"
       : t === "declining"    ? "#f59e0b"
       :                        "#475569"; // dormant
}

function levelBadge(l: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return l === "hot"      ? `${base} bg-red-500/20 text-red-300`
       : l === "warm"     ? `${base} bg-orange-500/20 text-orange-300`
       : l === "lukewarm" ? `${base} bg-amber-500/20 text-amber-300`
       : l === "cold"     ? `${base} bg-indigo-500/20 text-indigo-300`
       :                    `${base} bg-slate-700 text-slate-400`;
}

function trendBadge(t: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return t === "spiked"       ? `${base} bg-red-500/20 text-red-300`
       : t === "accelerating" ? `${base} bg-orange-500/20 text-orange-300`
       : t === "stable"       ? `${base} bg-indigo-500/20 text-indigo-300`
       : t === "declining"    ? `${base} bg-amber-500/20 text-amber-300`
       :                        `${base} bg-slate-700 text-slate-400`;
}

function strategyBadge(s: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return s === "immediate_outreach"  ? `${base} bg-red-500/20 text-red-300`
       : s === "executive_outreach"  ? `${base} bg-orange-500/20 text-orange-300`
       : s === "value_content"       ? `${base} bg-indigo-500/20 text-indigo-300`
       : s === "nurture_sequence"    ? `${base} bg-violet-500/20 text-violet-300`
       : s === "event_invite"        ? `${base} bg-sky-500/20 text-sky-300`
       :                               `${base} bg-slate-700 text-slate-400`;
}

function levelLabel(l: string) {
  const map: Record<string, string> = {
    hot: "Chaud", warm: "Tiède", lukewarm: "Tiédasse", cold: "Froid", unknown: "Inconnu",
  };
  return map[l] ?? l;
}

function trendLabel(t: string) {
  const map: Record<string, string> = {
    spiked: "Spike", accelerating: "Accélère", stable: "Stable", declining: "Décline", dormant: "Dormant",
  };
  return map[t] ?? t;
}

function strategyLabel(s: string) {
  const map: Record<string, string> = {
    immediate_outreach: "Outreach Immédiat", executive_outreach: "Outreach Exec",
    value_content: "Contenu Valeur", nurture_sequence: "Nurture",
    event_invite: "Invitation Événement", wait_and_monitor: "Surveiller",
  };
  return map[s] ?? s;
}

function categoryLabel(c: string) {
  const map: Record<string, string> = {
    product_interest: "Intérêt Produit", competitive_eval: "Éval. Concurrentielle",
    budget_cycle: "Cycle Budget", pain_driven: "Pain Business",
    relationship: "Relation", event_triggered: "Événement",
  };
  return map[c] ?? c;
}

// ── IntentRing SVG ─────────────────────────────────────────────────────────────
function IntentRing({ score, level }: { score: number; level: string }) {
  const r = 30, cx = 38, cy = 38;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const color = levelColor(level);
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
      <text x={cx} y={cy - 3} textAnchor="middle" fill={color} fontSize="12" fontWeight="700">
        {Math.round(score)}
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">
        intent
      </text>
    </svg>
  );
}

// ── LevelDistBar ───────────────────────────────────────────────────────────────
function LevelDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (total === 0) return null;
  const order = ["hot", "warm", "lukewarm", "cold", "unknown"];
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden gap-0.5">
      {order.map((l) => {
        const pct = ((counts[l] ?? 0) / total) * 100;
        return pct > 0 ? (
          <div key={l} style={{ width: `${pct}%`, backgroundColor: levelColor(l) }} title={`${levelLabel(l)}: ${counts[l]}`} />
        ) : null;
      })}
    </div>
  );
}

// ── ProspectModal ──────────────────────────────────────────────────────────────
function ProspectModal({ p, onClose }: { p: Prospect; onClose: () => void }) {
  const [tab, setTab] = useState<"actions" | "hot" | "cold">("actions");

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
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-white">{p.company_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">{p.rep_name} · {categoryLabel(p.intent_category)}</p>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-4">
            <span className={levelBadge(p.intent_level)}>{levelLabel(p.intent_level)}</span>
            <span className={trendBadge(p.intent_trend)}>{trendLabel(p.intent_trend)}</span>
            <span className={strategyBadge(p.outreach_strategy)}>{strategyLabel(p.outreach_strategy)}</span>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-white">{Math.round(p.intent_score)}</p>
              <p className="text-xs text-slate-400">Intent</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-indigo-400">{Math.round(p.digital_score)}</p>
              <p className="text-xs text-slate-400">Digital</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-violet-400">{Math.round(p.engagement_score)}</p>
              <p className="text-xs text-slate-400">Engagement</p>
            </div>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {(["actions", "hot", "cold"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "actions" ? "Actions recommandées" : t === "hot" ? "Signaux chauds" : "Signaux froids"}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-3">
          {tab === "actions" && (
            p.recommended_actions.map((a, i) => (
              <div key={i} className="flex items-start gap-3 bg-slate-800/50 rounded-xl p-3">
                <span className="text-orange-400 text-sm font-bold mt-0.5">{i + 1}</span>
                <p className="text-slate-200 text-sm">{a}</p>
              </div>
            ))
          )}
          {tab === "hot" && (
            p.hot_signals.length > 0 ? (
              p.hot_signals.map((s, i) => (
                <div key={i} className="flex items-start gap-2 bg-orange-900/20 border border-orange-800/30 rounded-xl p-3">
                  <span className="text-orange-400 text-sm mt-0.5">🔥</span>
                  <p className="text-slate-200 text-sm">{s}</p>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-slate-500">
                <p className="text-sm">Aucun signal chaud détecté.</p>
              </div>
            )
          )}
          {tab === "cold" && (
            p.cold_signals.length > 0 ? (
              p.cold_signals.map((s, i) => (
                <div key={i} className="flex items-start gap-2 bg-slate-800/50 border border-slate-700/30 rounded-xl p-3">
                  <span className="text-slate-400 text-sm mt-0.5">❄</span>
                  <p className="text-slate-200 text-sm">{s}</p>
                </div>
              ))
            ) : (
              <div className="bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-4 text-center">
                <p className="text-emerald-400 text-sm font-medium">Aucun signal froid</p>
                <p className="text-slate-400 text-xs mt-1">Engagement positif maintenu</p>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

// ── ProspectCard ───────────────────────────────────────────────────────────────
function ProspectCard({ p, onClick }: { p: Prospect; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-4 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4">
        <IntentRing score={p.intent_score} level={p.intent_level} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm">{p.company_name}</h3>
              <p className="text-slate-400 text-xs mt-0.5">{p.rep_name} · {categoryLabel(p.intent_category)}</p>
            </div>
            <span className={trendBadge(p.intent_trend)}>{trendLabel(p.intent_trend)}</span>
          </div>

          <div className="flex gap-2 mt-2 flex-wrap">
            <span className={levelBadge(p.intent_level)}>{levelLabel(p.intent_level)}</span>
            <span className={strategyBadge(p.outreach_strategy)}>{strategyLabel(p.outreach_strategy)}</span>
          </div>

          {/* Digital / Engagement / Trigger mini bars */}
          <div className="mt-3 space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-14">Digital</span>
              <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div className="h-full rounded-full bg-indigo-500" style={{ width: `${p.digital_score}%` }} />
              </div>
              <span className="text-xs text-slate-400 w-6 text-right">{Math.round(p.digital_score)}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-14">Engage.</span>
              <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div className="h-full rounded-full bg-violet-500" style={{ width: `${p.engagement_score}%` }} />
              </div>
              <span className="text-xs text-slate-400 w-6 text-right">{Math.round(p.engagement_score)}</span>
            </div>
            {p.trigger_score > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 w-14">Trigger</span>
                <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                  <div className="h-full rounded-full bg-orange-500" style={{ width: `${p.trigger_score}%` }} />
                </div>
                <span className="text-xs text-slate-400 w-6 text-right">{Math.round(p.trigger_score)}</span>
              </div>
            )}
          </div>

          {/* Hot signals count */}
          {p.hot_signals.length > 0 && (
            <div className="mt-2 flex items-center gap-1.5">
              <span className="text-orange-400 text-xs">🔥</span>
              <span className="text-orange-300 text-xs font-medium">{p.hot_signals.length} signal{p.hot_signals.length > 1 ? "s" : ""} chaud{p.hot_signals.length > 1 ? "s" : ""}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────
export default function BuyerIntentPage() {
  const [data, setData] = useState<{ prospects: Prospect[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Prospect | null>(null);
  const [levelFilter, setLevelFilter] = useState<string>("all");
  const [trendFilter, setTrendFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (levelFilter !== "all") params.set("level", levelFilter);
      if (trendFilter !== "all") params.set("trend", trendFilter);
      const res = await fetch(`/api/buyer-intent?${params.toString()}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [levelFilter, trendFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const s = data?.summary;
  const levelOptions = ["all", "hot", "warm", "lukewarm", "cold", "unknown"];
  const trendOptions = ["all", "spiked", "accelerating", "stable", "declining", "dormant"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Buyer Intent Intelligence</h1>
          <p className="text-slate-400 mt-1">Signaux d&apos;intention d&apos;achat · scoring comportemental · stratégie d&apos;outreach</p>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
          {[
            { label: "Prospects scorés",    value: s?.total ?? "—",                   accent: "text-white" },
            { label: "Score intent moy.",   value: s ? `${s.avg_intent_score}` : "—", accent: "text-orange-400" },
            { label: "Score digital moy.",  value: s ? `${s.avg_digital_score}` : "—", accent: "text-indigo-400" },
            { label: "Engagement moy.",     value: s ? `${s.avg_engagement_score}` : "—", accent: "text-violet-400" },
            { label: "Prospects chauds",    value: s?.hot_count ?? "—",               accent: "text-red-400" },
            { label: "Outreach immédiat",   value: s?.immediate_outreach_count ?? "—", accent: "text-amber-400" },
          ].map((kpi) => (
            <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <p className={`text-2xl font-bold ${kpi.accent}`}>{kpi.value}</p>
              <p className="text-slate-400 text-xs mt-1">{kpi.label}</p>
            </div>
          ))}
        </div>

        {/* Level distribution */}
        {s && (
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-5 mb-8">
            <h2 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
              Distribution des niveaux d&apos;intention
            </h2>
            <LevelDistBar counts={s.level_counts} />
            <div className="flex flex-wrap gap-3 mt-3">
              {["hot", "warm", "lukewarm", "cold", "unknown"].map((l) => (
                (s.level_counts[l] ?? 0) > 0 && (
                  <div key={l} className="flex items-center gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: levelColor(l) }} />
                    <span className="text-xs text-slate-400">{levelLabel(l)} ({s.level_counts[l]})</span>
                  </div>
                )
              ))}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="space-y-3 mb-6">
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Intent :</span>
            {levelOptions.map((l) => (
              <button
                key={l}
                onClick={() => setLevelFilter(l)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  levelFilter === l ? "bg-orange-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {l === "all" ? "Tous" : levelLabel(l)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Tendance :</span>
            {trendOptions.map((t) => (
              <button
                key={t}
                onClick={() => setTrendFilter(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  trendFilter === t ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {t === "all" ? "Tous" : trendLabel(t)}
              </button>
            ))}
          </div>
        </div>

        {/* Prospect grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {data?.prospects.map((p) => (
              <ProspectCard key={p.prospect_id} p={p} onClick={() => setSelected(p)} />
            ))}
          </div>
        )}

        {data?.prospects.length === 0 && !loading && (
          <div className="text-center py-16 text-slate-500">
            <p className="text-lg">Aucun prospect trouvé pour ces filtres.</p>
          </div>
        )}
      </div>

      {selected && <ProspectModal p={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
