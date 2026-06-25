"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────
interface Account {
  account_id: string;
  account_name: string;
  rep_id: string;
  rep_name: string;
  penetration_level: string;
  stakeholder_risk: string;
  committee_gap: string;
  penetration_action: string;
  penetration_score: number;
  coverage_score: number;
  relationship_score: number;
  multithread_ratio: number;
  expansion_plays: string[];
  risk_signals: string[];
  manager_alerts: string[];
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_penetration_score: number;
  avg_coverage_score: number;
  avg_relationship_score: number;
  single_threaded_count: number;
  critical_risk_count: number;
}

// ── Colour helpers ─────────────────────────────────────────────────────────────
function levelColor(l: string) {
  return l === "deep"    ? "#22c55e"
       : l === "solid"   ? "#6366f1"
       : l === "partial" ? "#f59e0b"
       : l === "thin"    ? "#f97316"
       :                   "#ef4444"; // single
}

function riskColor(r: string) {
  return r === "secure"     ? "#22c55e"
       : r === "stable"     ? "#6366f1"
       : r === "vulnerable" ? "#f59e0b"
       :                      "#ef4444"; // critical
}

function levelBadge(l: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return l === "deep"    ? `${base} bg-emerald-500/20 text-emerald-300`
       : l === "solid"   ? `${base} bg-indigo-500/20 text-indigo-300`
       : l === "partial" ? `${base} bg-amber-500/20 text-amber-300`
       : l === "thin"    ? `${base} bg-orange-500/20 text-orange-300`
       :                   `${base} bg-red-500/20 text-red-300`;
}

function riskBadge(r: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return r === "secure"     ? `${base} bg-emerald-500/20 text-emerald-300`
       : r === "stable"     ? `${base} bg-indigo-500/20 text-indigo-300`
       : r === "vulnerable" ? `${base} bg-amber-500/20 text-amber-300`
       :                      `${base} bg-red-500/20 text-red-300`;
}

function levelLabel(l: string) {
  const map: Record<string, string> = {
    deep: "Profonde", solid: "Solide", partial: "Partielle", thin: "Faible", single: "Contact unique",
  };
  return map[l] ?? l;
}

function riskLabel(r: string) {
  const map: Record<string, string> = {
    secure: "Sécurisé", stable: "Stable", vulnerable: "Vulnérable", critical: "Critique",
  };
  return map[r] ?? r;
}

function gapLabel(g: string) {
  const map: Record<string, string> = {
    none: "Complet", missing_exec: "Exec manquant", missing_user: "Utilisateur manquant",
    missing_tech: "Tech manquant", missing_finance: "Finance manquant", multiple_gaps: "Gaps multiples",
  };
  return map[g] ?? g;
}

function actionLabel(a: string) {
  const map: Record<string, string> = {
    maintain: "Maintenir", expand_exec: "Élargir Exec", expand_user: "Élargir Utilisateurs",
    expand_tech: "Élargir Tech", expand_finance: "Élargir Finance",
    rebuild_champion: "Reconstruire Champion", multithread_now: "Multi-thread Urgent",
  };
  return map[a] ?? a;
}

// ── PenetrationRing SVG ────────────────────────────────────────────────────────
function PenetrationRing({ score, level }: { score: number; level: string }) {
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
      <text x={cx} y={cy - 3} textAnchor="middle" fill={color} fontSize="13" fontWeight="700">
        {Math.round(score)}
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">
        pénétr.
      </text>
    </svg>
  );
}

// ── LevelDistBar ───────────────────────────────────────────────────────────────
function LevelDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (total === 0) return null;
  const order = ["deep", "solid", "partial", "thin", "single"];
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden gap-0.5">
      {order.map((l) => {
        const pct = ((counts[l] ?? 0) / total) * 100;
        return pct > 0 ? (
          <div
            key={l}
            style={{ width: `${pct}%`, backgroundColor: levelColor(l) }}
            title={`${levelLabel(l)}: ${counts[l]}`}
          />
        ) : null;
      })}
    </div>
  );
}

// ── AccountModal ───────────────────────────────────────────────────────────────
function AccountModal({ a, onClose }: { a: Account; onClose: () => void }) {
  const [tab, setTab] = useState<"plays" | "risks" | "alerts">("plays");

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
              <h2 className="text-xl font-bold text-white">{a.account_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">{a.rep_name}</p>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-4">
            <span className={levelBadge(a.penetration_level)}>{levelLabel(a.penetration_level)}</span>
            <span className={riskBadge(a.stakeholder_risk)}>{riskLabel(a.stakeholder_risk)}</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-300">{gapLabel(a.committee_gap)}</span>
          </div>
          <div className="grid grid-cols-4 gap-3 mt-4">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-white">{Math.round(a.penetration_score)}</p>
              <p className="text-xs text-slate-400">Pénétration</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-indigo-400">{Math.round(a.coverage_score)}</p>
              <p className="text-xs text-slate-400">Couverture</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-violet-400">{Math.round(a.relationship_score)}</p>
              <p className="text-xs text-slate-400">Relation</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-lg font-bold text-emerald-400">{Math.round(a.multithread_ratio * 100)}%</p>
              <p className="text-xs text-slate-400">Ratio actif</p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["plays", "risks", "alerts"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "plays" ? "Plays expansion" : t === "risks" ? "Signaux de risque" : "Alertes manager"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6 space-y-3">
          {tab === "plays" && (
            a.expansion_plays.map((p, i) => (
              <div key={i} className="flex items-start gap-3 bg-slate-800/50 rounded-xl p-3">
                <span className="text-indigo-400 text-sm font-bold mt-0.5">{i + 1}</span>
                <p className="text-slate-200 text-sm">{p}</p>
              </div>
            ))
          )}
          {tab === "risks" && (
            a.risk_signals.length > 0 ? (
              a.risk_signals.map((r, i) => (
                <div key={i} className="flex items-start gap-2 bg-amber-900/20 border border-amber-800/30 rounded-xl p-3">
                  <span className="text-amber-400 text-sm mt-0.5">!</span>
                  <p className="text-slate-200 text-sm">{r}</p>
                </div>
              ))
            ) : (
              <div className="bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-4 text-center">
                <p className="text-emerald-400 text-sm font-medium">Aucun signal de risque</p>
                <p className="text-slate-400 text-xs mt-1">Pénétration compte saine</p>
              </div>
            )
          )}
          {tab === "alerts" && (
            a.manager_alerts.length > 0 ? (
              a.manager_alerts.map((al, i) => (
                <div key={i} className="flex items-start gap-2 bg-red-900/20 border border-red-800/40 rounded-xl p-3">
                  <span className="text-red-400 text-sm mt-0.5">⚠</span>
                  <p className="text-slate-200 text-sm">{al}</p>
                </div>
              ))
            ) : (
              <div className="bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-4 text-center">
                <p className="text-emerald-400 text-sm font-medium">Aucune alerte manager</p>
                <p className="text-slate-400 text-xs mt-1">Compte bien géré</p>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

// ── AccountCard ────────────────────────────────────────────────────────────────
function AccountCard({ a, onClick }: { a: Account; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-4 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4">
        <PenetrationRing score={a.penetration_score} level={a.penetration_level} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm">{a.account_name}</h3>
              <p className="text-slate-400 text-xs mt-0.5">{a.rep_name}</p>
            </div>
            <span className={riskBadge(a.stakeholder_risk)}>{riskLabel(a.stakeholder_risk)}</span>
          </div>

          <div className="flex gap-2 mt-2 flex-wrap">
            <span className={levelBadge(a.penetration_level)}>{levelLabel(a.penetration_level)}</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-300">{gapLabel(a.committee_gap)}</span>
          </div>

          {/* Coverage vs Relationship bars */}
          <div className="mt-3 space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-16">Couverture</span>
              <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div className="h-full rounded-full bg-indigo-500 transition-all" style={{ width: `${a.coverage_score}%` }} />
              </div>
              <span className="text-xs text-slate-400 w-6 text-right">{Math.round(a.coverage_score)}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-16">Relation</span>
              <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                <div className="h-full rounded-full bg-violet-500 transition-all" style={{ width: `${a.relationship_score}%` }} />
              </div>
              <span className="text-xs text-slate-400 w-6 text-right">{Math.round(a.relationship_score)}</span>
            </div>
          </div>

          {/* Action recommended */}
          <div className="mt-2 flex items-center gap-1.5 bg-indigo-900/20 border border-indigo-800/30 rounded-lg px-2.5 py-1.5">
            <p className="text-indigo-300 text-xs font-medium">{actionLabel(a.penetration_action)}</p>
          </div>

          {/* Manager alerts */}
          {a.manager_alerts.length > 0 && (
            <div className="mt-1.5 flex items-center gap-1.5 bg-red-900/20 border border-red-800/30 rounded-lg px-2.5 py-1.5">
              <span className="text-red-400 text-xs">⚠</span>
              <p className="text-red-300 text-xs line-clamp-1">{a.manager_alerts[0]}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────
export default function AccountPenetrationPage() {
  const [data, setData] = useState<{ accounts: Account[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Account | null>(null);
  const [levelFilter, setLevelFilter] = useState<string>("all");
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (levelFilter !== "all") params.set("level", levelFilter);
          if (riskFilter !== "all")  params.set("risk", riskFilter);
          const res = await fetch(`/api/account-penetration?${params.toString()}`);
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    fetchData();
  }, [levelFilter, riskFilter]);

  const s = data?.summary;

  const levelOptions = ["all", "deep", "solid", "partial", "thin", "single"];
  const riskOptions  = ["all", "secure", "stable", "vulnerable", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Pénétration Comptes</h1>
          <p className="text-slate-400 mt-1">Couverture comité d&apos;achat · multi-threading · risque stakeholder</p>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
          {[
            { label: "Comptes analysés",     value: s?.total ?? "—",                       accent: "text-white" },
            { label: "Score pénétr. moy.",   value: s ? `${s.avg_penetration_score}` : "—", accent: "text-indigo-400" },
            { label: "Score couverture moy.", value: s ? `${s.avg_coverage_score}` : "—",    accent: "text-violet-400" },
            { label: "Score relation moy.",   value: s ? `${s.avg_relationship_score}` : "—", accent: "text-emerald-400" },
            { label: "Contact unique",        value: s?.single_threaded_count ?? "—",        accent: "text-red-400" },
            { label: "Risque critique",       value: s?.critical_risk_count ?? "—",          accent: "text-orange-400" },
          ].map((kpi) => (
            <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <p className={`text-2xl font-bold ${kpi.accent}`}>{kpi.value}</p>
              <p className="text-slate-400 text-xs mt-1">{kpi.label}</p>
            </div>
          ))}
        </div>

        {/* Penetration level distribution */}
        {s && (
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-5 mb-8">
            <h2 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
              Distribution des niveaux de pénétration
            </h2>
            <LevelDistBar counts={s.level_counts} />
            <div className="flex flex-wrap gap-3 mt-3">
              {["deep", "solid", "partial", "thin", "single"].map((l) => (
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

        {/* Risk mini stats */}
        {s && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
            {["secure", "stable", "vulnerable", "critical"].map((r) => (
              <div
                key={r}
                className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 flex items-center gap-3"
              >
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: riskColor(r) }} />
                <div>
                  <p className="text-lg font-bold text-white">{s.risk_counts[r] ?? 0}</p>
                  <p className="text-xs text-slate-400">{riskLabel(r)}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Filters */}
        <div className="space-y-3 mb-6">
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Pénétration :</span>
            {levelOptions.map((l) => (
              <button
                key={l}
                onClick={() => setLevelFilter(l)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  levelFilter === l
                    ? "bg-indigo-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {l === "all" ? "Tous" : levelLabel(l)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Risque :</span>
            {riskOptions.map((r) => (
              <button
                key={r}
                onClick={() => setRiskFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  riskFilter === r
                    ? "bg-violet-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {r === "all" ? "Tous" : riskLabel(r)}
              </button>
            ))}
          </div>
        </div>

        {/* Account grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {data?.accounts.map((a) => (
              <AccountCard key={a.account_id} a={a} onClick={() => setSelected(a)} />
            ))}
          </div>
        )}

        {data?.accounts.length === 0 && !loading && (
          <div className="text-center py-16 text-slate-500">
            <p className="text-lg">Aucun compte trouvé pour ces filtres.</p>
          </div>
        )}
      </div>

      {selected && <AccountModal a={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
