"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────
interface Deal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  rep_name: string;
  account_name: string;
  competitor_name: string;
  competitor_category: string;
  competitor_threat: string;
  competitive_position: string;
  competitive_action: string;
  threat_score: number;
  position_score: number;
  win_probability_pct: number;
  battle_tactics: string[];
  differentiators: string[];
  risk_signals: string[];
  manager_alerts: string[];
}

interface Summary {
  total: number;
  threat_counts: Record<string, number>;
  position_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_threat_score: number;
  avg_position_score: number;
  avg_win_probability: number;
  critical_count: number;
  losing_count: number;
  escalation_count: number;
}

// ── Colour helpers ─────────────────────────────────────────────────────────────
function threatColor(t: string) {
  return t === "critical" ? "#ef4444"
       : t === "high"     ? "#f97316"
       : t === "moderate" ? "#f59e0b"
       : t === "low"      ? "#6366f1"
       :                    "#22c55e";
}

function positionColor(p: string) {
  return p === "winning"  ? "#22c55e"
       : p === "leading"  ? "#6366f1"
       : p === "tied"     ? "#f59e0b"
       : p === "trailing" ? "#f97316"
       :                    "#ef4444";
}

function threatBadge(t: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return t === "critical" ? `${base} bg-red-500/20 text-red-300`
       : t === "high"     ? `${base} bg-orange-500/20 text-orange-300`
       : t === "moderate" ? `${base} bg-amber-500/20 text-amber-300`
       : t === "low"      ? `${base} bg-indigo-500/20 text-indigo-300`
       :                    `${base} bg-emerald-500/20 text-emerald-300`;
}

function positionBadge(p: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return p === "winning"  ? `${base} bg-emerald-500/20 text-emerald-300`
       : p === "leading"  ? `${base} bg-indigo-500/20 text-indigo-300`
       : p === "tied"     ? `${base} bg-amber-500/20 text-amber-300`
       : p === "trailing" ? `${base} bg-orange-500/20 text-orange-300`
       :                    `${base} bg-red-500/20 text-red-300`;
}

function actionBadge(a: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return a === "escalate"         ? `${base} bg-red-500/20 text-red-300`
       : a === "defend_and_close" ? `${base} bg-orange-500/20 text-orange-300`
       : a === "price_protect"    ? `${base} bg-amber-500/20 text-amber-300`
       : a === "differentiate"    ? `${base} bg-violet-500/20 text-violet-300`
       : a === "maintain"         ? `${base} bg-indigo-500/20 text-indigo-300`
       :                            `${base} bg-emerald-500/20 text-emerald-300`;
}

function threatLabel(t: string) {
  const map: Record<string, string> = {
    critical: "Critique", high: "Élevé", moderate: "Modéré", low: "Faible", none: "Aucun",
  };
  return map[t] ?? t;
}

function positionLabel(p: string) {
  const map: Record<string, string> = {
    winning: "Gagnant", leading: "En tête", tied: "Égalité", trailing: "En retard", losing: "Perdant",
  };
  return map[p] ?? p;
}

function actionLabel(a: string) {
  const map: Record<string, string> = {
    escalate: "Escalade", defend_and_close: "Défendre & Clore", price_protect: "Protéger Prix",
    differentiate: "Différencier", maintain: "Maintenir", monitor: "Surveiller",
  };
  return map[a] ?? a;
}

function categoryLabel(c: string) {
  const map: Record<string, string> = {
    enterprise: "Enterprise", mid_market: "Mid-Market", startup: "Startup",
    open_source: "Open Source", in_house: "Dev Interne", unknown: "Inconnu",
  };
  return map[c] ?? c;
}

// ── WinProbGauge ───────────────────────────────────────────────────────────────
function WinProbGauge({ prob, position }: { prob: number; position: string }) {
  const r = 30, cx = 38, cy = 38;
  const circ = 2 * Math.PI * r;
  const arc  = (prob / 100) * circ;
  const color = positionColor(position);
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
        {Math.round(prob)}%
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">
        victoire
      </text>
    </svg>
  );
}

// ── ThreatDistBar ──────────────────────────────────────────────────────────────
function ThreatDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (total === 0) return null;
  const order = ["critical", "high", "moderate", "low", "none"];
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden gap-0.5">
      {order.map((t) => {
        const pct = ((counts[t] ?? 0) / total) * 100;
        return pct > 0 ? (
          <div key={t} style={{ width: `${pct}%`, backgroundColor: threatColor(t) }} title={`${threatLabel(t)}: ${counts[t]}`} />
        ) : null;
      })}
    </div>
  );
}

// ── DealModal ──────────────────────────────────────────────────────────────────
function DealModal({ d, onClose }: { d: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"tactics" | "diff" | "risk">("tactics");

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
              <h2 className="text-xl font-bold text-white">{d.deal_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">
                {d.rep_name} · {d.account_name}
              </p>
              <p className="text-indigo-300 text-sm mt-0.5 font-medium">
                vs {d.competitor_name} · <span className="text-slate-400">{categoryLabel(d.competitor_category)}</span>
              </p>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-4">
            <span className={threatBadge(d.competitor_threat)}>{threatLabel(d.competitor_threat)}</span>
            <span className={positionBadge(d.competitive_position)}>{positionLabel(d.competitive_position)}</span>
            <span className={actionBadge(d.competitive_action)}>{actionLabel(d.competitive_action)}</span>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-red-400">{Math.round(d.threat_score)}</p>
              <p className="text-xs text-slate-400">Score menace</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-indigo-400">{Math.round(d.position_score)}</p>
              <p className="text-xs text-slate-400">Score position</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-emerald-400">{d.win_probability_pct}%</p>
              <p className="text-xs text-slate-400">Prob. victoire</p>
            </div>
          </div>
          {d.manager_alerts.length > 0 && (
            <div className="mt-4 space-y-2">
              {d.manager_alerts.map((a, i) => (
                <div key={i} className="flex items-start gap-2 bg-red-900/20 border border-red-800/40 rounded-xl p-3">
                  <span className="text-red-400 text-sm mt-0.5">⚠</span>
                  <p className="text-slate-200 text-sm">{a}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["tactics", "diff", "risk"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "tactics" ? "Tactiques" : t === "diff" ? "Différenciateurs" : "Signaux risque"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6 space-y-3">
          {tab === "tactics" && (
            d.battle_tactics.map((tac, i) => (
              <div key={i} className="flex items-start gap-3 bg-slate-800/50 rounded-xl p-3">
                <span className="text-orange-400 text-sm font-bold mt-0.5">{i + 1}</span>
                <p className="text-slate-200 text-sm">{tac}</p>
              </div>
            ))
          )}
          {tab === "diff" && (
            d.differentiators.length > 0 ? (
              d.differentiators.map((diff, i) => (
                <div key={i} className="flex items-start gap-2 bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-3">
                  <span className="text-emerald-400 text-sm mt-0.5">✓</span>
                  <p className="text-slate-200 text-sm">{diff}</p>
                </div>
              ))
            ) : <p className="text-slate-500 text-sm">Aucun différenciateur identifié.</p>
          )}
          {tab === "risk" && (
            d.risk_signals.length > 0 ? (
              d.risk_signals.map((r, i) => (
                <div key={i} className="flex items-start gap-2 bg-red-900/20 border border-red-800/30 rounded-xl p-3">
                  <span className="text-red-400 text-sm mt-0.5">!</span>
                  <p className="text-slate-200 text-sm">{r}</p>
                </div>
              ))
            ) : (
              <div className="bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-4 text-center">
                <p className="text-emerald-400 text-sm font-medium">Aucun signal de risque</p>
                <p className="text-slate-400 text-xs mt-1">Position compétitive saine</p>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

// ── DealCard ───────────────────────────────────────────────────────────────────
function DealCard({ d, onClick }: { d: Deal; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-4 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4">
        <WinProbGauge prob={d.win_probability_pct} position={d.competitive_position} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm truncate">{d.deal_name}</h3>
              <p className="text-slate-400 text-xs mt-0.5">{d.account_name} · {d.rep_name}</p>
              <p className="text-indigo-300 text-xs mt-0.5 font-medium">
                vs {d.competitor_name}
                <span className="text-slate-500 ml-1">({categoryLabel(d.competitor_category)})</span>
              </p>
            </div>
            <span className={threatBadge(d.competitor_threat)}>{threatLabel(d.competitor_threat)}</span>
          </div>

          <div className="flex gap-2 mt-2 flex-wrap">
            <span className={positionBadge(d.competitive_position)}>{positionLabel(d.competitive_position)}</span>
            <span className={actionBadge(d.competitive_action)}>{actionLabel(d.competitive_action)}</span>
          </div>

          {/* Threat vs Position mini-bars */}
          <div className="mt-3 space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-16">Menace</span>
              <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div className="h-full rounded-full bg-red-500 transition-all" style={{ width: `${d.threat_score}%` }} />
              </div>
              <span className="text-xs text-slate-400 w-6 text-right">{Math.round(d.threat_score)}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-16">Position</span>
              <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div className="h-full rounded-full bg-indigo-500 transition-all" style={{ width: `${d.position_score}%` }} />
              </div>
              <span className="text-xs text-slate-400 w-6 text-right">{Math.round(d.position_score)}</span>
            </div>
          </div>

          {/* Manager alerts */}
          {d.manager_alerts.length > 0 && (
            <div className="mt-2 flex items-center gap-1.5 bg-red-900/20 border border-red-800/30 rounded-lg px-2.5 py-1.5">
              <span className="text-red-400 text-xs">⚠</span>
              <p className="text-red-300 text-xs line-clamp-1">{d.manager_alerts[0]}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────
export default function CompetitiveIntelligencePage() {
  const [data, setData] = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [threatFilter, setThreatFilter] = useState<string>("all");
  const [positionFilter, setPositionFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (threatFilter !== "all")   params.set("threat", threatFilter);
          if (positionFilter !== "all") params.set("position", positionFilter);
          const res = await fetch(`/api/competitive-intelligence?${params.toString()}`);
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    fetchData();
  }, [threatFilter, positionFilter]);

  const s = data?.summary;

  const threatOptions   = ["all", "critical", "high", "moderate", "low", "none"];
  const positionOptions = ["all", "winning", "leading", "tied", "trailing", "losing"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Intelligence Compétitive</h1>
          <p className="text-slate-400 mt-1">Analyse des menaces concurrentes · positioning stratégique · battlecard tactics</p>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
          {[
            { label: "Deals analysés",       value: s?.total ?? "—",                 accent: "text-white" },
            { label: "Menaces critiques",     value: s?.critical_count ?? "—",         accent: "text-red-400" },
            { label: "Deals perdants",        value: s?.losing_count ?? "—",           accent: "text-orange-400" },
            { label: "Escalades requises",    value: s?.escalation_count ?? "—",       accent: "text-amber-400" },
            { label: "Score menace moy.",     value: s ? `${s.avg_threat_score}` : "—", accent: "text-red-300" },
            { label: "Prob. victoire moy.",   value: s ? `${s.avg_win_probability}%` : "—", accent: "text-emerald-400" },
          ].map((kpi) => (
            <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <p className={`text-2xl font-bold ${kpi.accent}`}>{kpi.value}</p>
              <p className="text-slate-400 text-xs mt-1">{kpi.label}</p>
            </div>
          ))}
        </div>

        {/* Threat distribution */}
        {s && (
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-5 mb-8">
            <h2 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
              Distribution des niveaux de menace
            </h2>
            <ThreatDistBar counts={s.threat_counts} />
            <div className="flex flex-wrap gap-3 mt-3">
              {["critical", "high", "moderate", "low", "none"].map((t) => (
                (s.threat_counts[t] ?? 0) > 0 && (
                  <div key={t} className="flex items-center gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: threatColor(t) }} />
                    <span className="text-xs text-slate-400">{threatLabel(t)} ({s.threat_counts[t]})</span>
                  </div>
                )
              ))}
            </div>
          </div>
        )}

        {/* Position mini stats */}
        {s && (
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 mb-8">
            {["winning", "leading", "tied", "trailing", "losing"].map((p) => (
              <div
                key={p}
                className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 flex items-center gap-3"
              >
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: positionColor(p) }} />
                <div>
                  <p className="text-lg font-bold text-white">{s.position_counts[p] ?? 0}</p>
                  <p className="text-xs text-slate-400">{positionLabel(p)}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Filters */}
        <div className="space-y-3 mb-6">
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Menace :</span>
            {threatOptions.map((t) => (
              <button
                key={t}
                onClick={() => setThreatFilter(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  threatFilter === t
                    ? "bg-red-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {t === "all" ? "Tous" : threatLabel(t)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Position :</span>
            {positionOptions.map((p) => (
              <button
                key={p}
                onClick={() => setPositionFilter(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  positionFilter === p
                    ? "bg-indigo-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {p === "all" ? "Tous" : positionLabel(p)}
              </button>
            ))}
          </div>
        </div>

        {/* Deal grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-2 border-red-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {data?.deals.map((d) => (
              <DealCard key={d.deal_id} d={d} onClick={() => setSelected(d)} />
            ))}
          </div>
        )}

        {data?.deals.length === 0 && !loading && (
          <div className="text-center py-16 text-slate-500">
            <p className="text-lg">Aucun deal trouvé pour ces filtres.</p>
          </div>
        )}
      </div>

      {selected && <DealModal d={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
