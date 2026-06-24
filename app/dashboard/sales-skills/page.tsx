"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface RepData {
  rep_id: string;
  rep_name: string;
  manager_id: string;
  overall_skill_score: number;
  technical_score: number;
  operational_score: number;
  results_score: number;
  weakest_area: string;
  skill_level: string;
  skill_gap: string;
  coaching_priority: string;
  development_path: string;
  strengths: string[];
  gaps: string[];
  recommended_actions: string[];
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  gap_counts: Record<string, number>;
  priority_counts: Record<string, number>;
  path_counts: Record<string, number>;
  avg_overall_score: number;
  avg_technical_score: number;
  avg_operational_score: number;
  avg_results_score: number;
  top_performer_count: number;
  immediate_coaching_count: number;
  at_risk_count: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function levelColor(level: string) {
  switch (level) {
    case "expert":     return { ring: "#10b981", text: "text-emerald-400", bg: "bg-emerald-500/20", border: "border-emerald-500/30" };
    case "advanced":   return { ring: "#6366f1", text: "text-indigo-400",  bg: "bg-indigo-500/20",  border: "border-indigo-500/30" };
    case "proficient": return { ring: "#64748b", text: "text-slate-400",   bg: "bg-slate-500/20",   border: "border-slate-500/30" };
    case "developing": return { ring: "#f59e0b", text: "text-amber-400",   bg: "bg-amber-500/20",   border: "border-amber-500/30" };
    case "beginner":   return { ring: "#ef4444", text: "text-red-400",     bg: "bg-red-500/20",     border: "border-red-500/30" };
    default:           return { ring: "#64748b", text: "text-slate-400",   bg: "bg-slate-500/20",   border: "border-slate-500/30" };
  }
}

function levelLabel(level: string) {
  const map: Record<string, string> = {
    expert: "Expert", advanced: "Avancé", proficient: "Compétent", developing: "En dev.", beginner: "Débutant",
  };
  return map[level] ?? level;
}

function priorityColor(p: string) {
  switch (p) {
    case "immediate": return "text-red-400";
    case "high":      return "text-orange-400";
    case "medium":    return "text-amber-400";
    case "low":       return "text-slate-400";
    case "maintain":  return "text-emerald-400";
    default:          return "text-slate-400";
  }
}

function priorityLabel(p: string) {
  const map: Record<string, string> = {
    immediate: "Immédiat", high: "Élevé", medium: "Moyen", low: "Faible", maintain: "Maintenir",
  };
  return map[p] ?? p;
}

function pathLabel(path: string) {
  const map: Record<string, string> = {
    advanced_training: "Formation avancée",
    skills_coaching:   "Coaching individuel",
    peer_mentoring:    "Mentoring pair-à-pair",
    self_directed:     "Auto-dirigé",
    maintain:          "Maintenir",
  };
  return map[path] ?? path;
}

// ── Skill Radar Ring ─────────────────────────────────────────────────────────

function SkillRing({ score, level, size = 80 }: { score: number; level: string; size?: number }) {
  const { ring } = levelColor(level);
  const cx = size / 2, cy = size / 2, r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const sw = size * 0.09;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={ring} strokeWidth={sw}
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 4} textAnchor="middle" fill="white" fontSize={size * 0.18} fontWeight="700">
        {Math.round(score)}
      </text>
    </svg>
  );
}

// ── Level Dist Bar ────────────────────────────────────────────────────────────

function LevelDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const levels = [
    { key: "expert",     color: "#10b981" },
    { key: "advanced",   color: "#6366f1" },
    { key: "proficient", color: "#64748b" },
    { key: "developing", color: "#f59e0b" },
    { key: "beginner",   color: "#ef4444" },
  ];
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden gap-px bg-slate-800">
      {levels.map(({ key, color }) => {
        const pct = total > 0 ? ((counts[key] ?? 0) / total) * 100 : 0;
        return pct > 0 ? (
          <div key={key} style={{ width: `${pct}%`, background: color }} title={`${levelLabel(key)}: ${counts[key]}`} />
        ) : null;
      })}
    </div>
  );
}

// ── Score Bar ─────────────────────────────────────────────────────────────────

function ScoreBar({ value, color, label }: { value: number; color: string; label: string }) {
  return (
    <div>
      <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
        <span>{label}</span>
        <span className="text-slate-400">{Math.round(value)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${value}%`, background: color }} />
      </div>
    </div>
  );
}

// ── Rep Card ──────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: RepData; onClick: () => void }) {
  const col = levelColor(rep.skill_level);
  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border p-4 transition-all hover:brightness-110 ${col.bg} ${col.border}`}
    >
      <div className="flex items-start gap-4">
        <SkillRing score={rep.overall_skill_score} level={rep.skill_level} size={72} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="text-white font-semibold text-sm truncate">{rep.rep_name}</span>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${col.bg} ${col.text} border ${col.border}`}>
              {levelLabel(rep.skill_level)}
            </span>
          </div>
          <p className="text-xs text-slate-500 mb-2">Point faible : {rep.weakest_area}</p>
          <div className="grid grid-cols-3 gap-2 mb-2">
            <ScoreBar value={rep.technical_score}   color="#6366f1" label="Technique" />
            <ScoreBar value={rep.operational_score} color="#10b981" label="Opérationnel" />
            <ScoreBar value={rep.results_score}     color="#f59e0b" label="Résultats" />
          </div>
          <div className="flex items-center justify-between text-[10px]">
            <span className={`font-medium ${priorityColor(rep.coaching_priority)}`}>
              Coaching : {priorityLabel(rep.coaching_priority)}
            </span>
            <span className="text-slate-500 truncate ml-2">{pathLabel(rep.development_path)}</span>
          </div>
        </div>
      </div>
    </button>
  );
}

// ── Rep Modal ─────────────────────────────────────────────────────────────────

function RepModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const col = levelColor(rep.skill_level);
  const [tab, setTab] = useState<"actions" | "strengths" | "gaps">("actions");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" onClick={onClose}>
      <div
        className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <SkillRing score={rep.overall_skill_score} level={rep.skill_level} size={64} />
            <div>
              <h2 className="text-white font-bold text-lg">{rep.rep_name}</h2>
              <div className="flex items-center gap-2 mt-1 flex-wrap">
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${col.bg} ${col.text} border ${col.border}`}>
                  {levelLabel(rep.skill_level)}
                </span>
                <span className={`text-xs ${priorityColor(rep.coaching_priority)}`}>
                  Coaching {priorityLabel(rep.coaching_priority)}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1">Point faible : {rep.weakest_area}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl leading-none">×</button>
        </div>

        {/* Score breakdown */}
        <div className="grid grid-cols-3 gap-3 p-5 border-b border-slate-800">
          {[
            { label: "Technique",    value: rep.technical_score,   color: "#6366f1" },
            { label: "Opérationnel", value: rep.operational_score, color: "#10b981" },
            { label: "Résultats",    value: rep.results_score,     color: "#f59e0b" },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-slate-800/50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold" style={{ color }}>{Math.round(value)}</div>
              <div className="text-xs text-slate-400">{label}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800 px-5">
          {(["actions", "strengths", "gaps"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                tab === t ? "border-indigo-500 text-indigo-400" : "border-transparent text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "actions" ? "Plan de développement" : t === "strengths" ? "Points forts" : "Points à améliorer"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "actions" && (
            <>
              <div className={`text-sm font-medium px-3 py-2 rounded-lg ${col.bg} ${col.text} border ${col.border}`}>
                Parcours : {pathLabel(rep.development_path)}
              </div>
              {rep.recommended_actions.map((a, i) => (
                <div key={i} className="flex gap-2 text-sm text-slate-300 bg-slate-800/50 rounded-lg p-3">
                  <span className="text-indigo-400 flex-shrink-0">→</span>
                  <span>{a}</span>
                </div>
              ))}
            </>
          )}

          {tab === "strengths" && (
            <>
              {rep.strengths.length > 0 ? (
                rep.strengths.map((s, i) => (
                  <div key={i} className="flex gap-2 text-sm text-slate-300 bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3">
                    <span className="text-emerald-400 flex-shrink-0">✓</span>
                    <span>{s}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucun point fort significatif identifié.</p>
              )}
            </>
          )}

          {tab === "gaps" && (
            <>
              {rep.gaps.length > 0 ? (
                rep.gaps.map((g, i) => (
                  <div key={i} className="flex gap-2 text-sm text-slate-300 bg-amber-500/10 border border-amber-500/20 rounded-lg p-3">
                    <span className="text-amber-400 flex-shrink-0">⚠</span>
                    <span>{g}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucun gap critique identifié.</p>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function SalesSkillsPage() {
  const [reps, setReps]           = useState<RepData[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [error, setError]         = useState<string | null>(null);
  const [levelFilter, setLevel]   = useState("all");
  const [priorityFilter, setPrio] = useState("all");
  const [selected, setSelected]   = useState<RepData | null>(null);

  async function fetchData() {
      setLoading(true);
      setError(null);
      try {
        const params = new URLSearchParams();
        if (levelFilter !== "all")    params.set("level", levelFilter);
        if (priorityFilter !== "all") params.set("priority", priorityFilter);
        const res = await fetch(`/api/sales-skills?${params}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setReps(data.reps ?? []);
        setSummary(data.summary ?? null);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Erreur inconnue");
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    fetchData();
  }, [levelFilter, priorityFilter]);

  const levels     = ["all", "expert", "advanced", "proficient", "developing", "beginner"];
  const priorities = ["all", "immediate", "high", "medium", "low", "maintain"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Sales Skills Intelligence</h1>
            <p className="text-slate-400 text-sm mt-1">Évaluation et développement des compétences commerciales</p>
          </div>
          <button
            onClick={fetchData}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-lg transition-colors"
          >
            Actualiser
          </button>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3">
            {[
              { label: "Total reps",      value: summary.total,                    color: "text-white" },
              { label: "Top performers",  value: summary.top_performer_count,      color: "text-emerald-400" },
              { label: "Coaching urgent", value: summary.immediate_coaching_count, color: "text-red-400" },
              { label: "À risque",        value: summary.at_risk_count,            color: "text-orange-400" },
              { label: "Score moyen",     value: summary.avg_overall_score,        color: "text-indigo-400" },
              { label: "Score résultats", value: summary.avg_results_score,        color: "text-amber-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-center">
                <div className={`text-2xl font-bold ${color}`}>{value}</div>
                <div className="text-xs text-slate-500 mt-1">{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Distribution par niveau</span>
              <div className="flex gap-3 text-xs flex-wrap">
                {["expert", "advanced", "proficient", "developing", "beginner"].map((lvl) => (
                  (summary.level_counts[lvl] ?? 0) > 0 && (
                    <span key={lvl} className={`${levelColor(lvl).text}`}>
                      {levelLabel(lvl)}: {summary.level_counts[lvl]}
                    </span>
                  )
                ))}
              </div>
            </div>
            <LevelDistBar counts={summary.level_counts} total={summary.total} />
          </div>
        )}

        {/* Filters */}
        <div className="space-y-2">
          <div className="flex flex-wrap gap-2">
            {levels.map((l) => (
              <button
                key={l}
                onClick={() => setLevel(l)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  levelFilter === l ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {l === "all" ? "Tous les niveaux" : levelLabel(l)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            {priorities.map((p) => (
              <button
                key={p}
                onClick={() => setPrio(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  priorityFilter === p ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {p === "all" ? "Toutes priorités" : priorityLabel(p)}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {loading && <div className="text-center py-20 text-slate-400">Chargement...</div>}
        {error && <div className="text-center py-20 text-red-400">Erreur : {error}</div>}
        {!loading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {reps.map((rep) => (
              <RepCard key={rep.rep_id} rep={rep} onClick={() => setSelected(rep)} />
            ))}
            {reps.length === 0 && (
              <div className="col-span-2 text-center py-20 text-slate-500">
                Aucun commercial trouvé pour les filtres sélectionnés.
              </div>
            )}
          </div>
        )}
      </div>

      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
