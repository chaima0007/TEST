"use client";

import { useEffect, useState } from "react";

interface Rep {
  rep_id: string;
  rep_name: string;
  segment: string;
  region: string;
  coaching_score: number;
  intensity: string;
  primary_focus: string;
  quota_attainment: number;
  pipeline_coverage: number;
  avg_deal_size_eur: number;
  top_skill_gaps: string[];
  strengths: string[];
  development_areas: string[];
  coaching_actions: string[];
  session_plan: string[];
  kpis_to_track: string[];
}

interface Summary {
  total: number;
  intensity_counts: Record<string, number>;
  focus_counts: Record<string, number>;
  gap_counts: Record<string, number>;
  avg_coaching_score: number;
  critical_count: number;
  star_count: number;
}

const INTENSITY_COLOR: Record<string, string> = {
  light: "emerald",
  moderate: "sky",
  intensive: "amber",
  critical: "red",
};

const FOCUS_COLOR: Record<string, string> = {
  strategy: "indigo",
  skills: "violet",
  pipeline: "sky",
  mindset: "amber",
  process: "teal",
};

function CoachingRing({ score, intensity }: { score: number; intensity: string }) {
  const r = 40;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = INTENSITY_COLOR[intensity] || "slate";
  const stroke =
    color === "emerald"
      ? "#10b981"
      : color === "sky"
      ? "#38bdf8"
      : color === "amber"
      ? "#f59e0b"
      : color === "red"
      ? "#ef4444"
      : "#64748b";
  return (
    <svg width="96" height="96" viewBox="0 0 96 96">
      <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
      <circle
        cx="48"
        cy="48"
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth="10"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 48 48)"
      />
      <text x="48" y="53" textAnchor="middle" fill="#f1f5f9" fontSize="18" fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function IntensityBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (!total) return null;
  const segments = [
    { key: "light", label: "Light", color: "bg-emerald-500" },
    { key: "moderate", label: "Moderate", color: "bg-sky-500" },
    { key: "intensive", label: "Intensive", color: "bg-amber-500" },
    { key: "critical", label: "Critical", color: "bg-red-500" },
  ];
  return (
    <div className="mb-6">
      <div className="flex rounded-full overflow-hidden h-3 mb-2">
        {segments.map(({ key, color }) => {
          const pct = ((counts[key] || 0) / total) * 100;
          return pct > 0 ? (
            <div key={key} className={`${color} h-3`} style={{ width: `${pct}%` }} title={`${key}: ${counts[key]}`} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 text-xs text-slate-400">
        {segments.map(({ key, label, color }) => (
          <span key={key} className="flex items-center gap-1">
            <span className={`inline-block w-2 h-2 rounded-full ${color}`} />
            {label} ({counts[key] || 0})
          </span>
        ))}
      </div>
    </div>
  );
}

function intensityBadge(intensity: string) {
  const map: Record<string, string> = {
    light: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
    moderate: "bg-sky-900/60 text-sky-300 border-sky-700",
    intensive: "bg-amber-900/60 text-amber-300 border-amber-700",
    critical: "bg-red-900/60 text-red-300 border-red-700",
  };
  return map[intensity] || "bg-slate-800 text-slate-300 border-slate-600";
}

function focusBadge(focus: string) {
  const map: Record<string, string> = {
    strategy: "bg-indigo-900/60 text-indigo-300 border-indigo-700",
    skills: "bg-violet-900/60 text-violet-300 border-violet-700",
    pipeline: "bg-sky-900/60 text-sky-300 border-sky-700",
    mindset: "bg-amber-900/60 text-amber-300 border-amber-700",
    process: "bg-teal-900/60 text-teal-300 border-teal-700",
  };
  return map[focus] || "bg-slate-800 text-slate-300 border-slate-600";
}

function RepCard({ rep, onClick }: { rep: Rep; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-5 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4 mb-4">
        <CoachingRing score={rep.coaching_score} intensity={rep.intensity} />
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-100 text-base truncate">{rep.rep_name}</h3>
          <p className="text-slate-400 text-sm truncate">{rep.region} · {rep.segment}</p>
          <div className="flex flex-wrap gap-1 mt-2">
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${intensityBadge(rep.intensity)}`}>
              {rep.intensity}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${focusBadge(rep.primary_focus)}`}>
              {rep.primary_focus}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 mb-4 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">{rep.quota_attainment}%</div>
          <div className="text-slate-500 text-xs">Quota</div>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">{rep.pipeline_coverage}x</div>
          <div className="text-slate-500 text-xs">Pipeline</div>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">
            {rep.avg_deal_size_eur >= 1000 ? `${(rep.avg_deal_size_eur / 1000).toFixed(0)}k` : rep.avg_deal_size_eur}€
          </div>
          <div className="text-slate-500 text-xs">Deal Moy.</div>
        </div>
      </div>

      {rep.top_skill_gaps.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {rep.top_skill_gaps.slice(0, 3).map((gap) => (
            <span key={gap} className="text-xs px-2 py-0.5 bg-slate-900/60 border border-slate-700 text-slate-400 rounded-full capitalize">
              {gap.replace(/_/g, " ")}
            </span>
          ))}
          {rep.top_skill_gaps.length > 3 && (
            <span className="text-xs px-2 py-0.5 bg-slate-900/60 border border-slate-700 text-slate-500 rounded-full">
              +{rep.top_skill_gaps.length - 3}
            </span>
          )}
        </div>
      )}

      <div className="mt-3">
        <div className="flex justify-between text-xs text-slate-500 mb-1">
          <span>Score coaching</span>
          <span>{Math.round(rep.coaching_score)}/100</span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-1.5 rounded-full ${
              rep.intensity === "light"
                ? "bg-emerald-500"
                : rep.intensity === "moderate"
                ? "bg-sky-500"
                : rep.intensity === "intensive"
                ? "bg-amber-500"
                : "bg-red-500"
            }`}
            style={{ width: `${rep.coaching_score}%` }}
          />
        </div>
      </div>
    </div>
  );
}

function CoachingModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
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
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start gap-4">
          <CoachingRing score={rep.coaching_score} intensity={rep.intensity} />
          <div className="flex-1">
            <h2 className="text-xl font-bold text-slate-100">{rep.rep_name}</h2>
            <p className="text-slate-400 text-sm">{rep.region} · {rep.segment}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${intensityBadge(rep.intensity)}`}>
                {rep.intensity}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${focusBadge(rep.primary_focus)}`}>
                Focus: {rep.primary_focus}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">&times;</button>
        </div>

        <div className="p-6 space-y-5">
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="bg-slate-800 rounded-xl p-3">
              <div className="text-lg font-bold text-slate-100">{rep.quota_attainment}%</div>
              <div className="text-xs text-slate-400">Quota Attainment</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-3">
              <div className="text-lg font-bold text-slate-100">{rep.pipeline_coverage}x</div>
              <div className="text-xs text-slate-400">Pipeline Coverage</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-3">
              <div className="text-lg font-bold text-slate-100">
                {rep.avg_deal_size_eur >= 1000 ? `${(rep.avg_deal_size_eur / 1000).toFixed(0)}k€` : `${rep.avg_deal_size_eur}€`}
              </div>
              <div className="text-xs text-slate-400">Deal Moyen</div>
            </div>
          </div>

          {rep.strengths.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
                Points forts
              </h3>
              <ul className="space-y-1.5">
                {rep.strengths.map((s, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-emerald-900/20 border border-emerald-800/40 rounded-lg px-3 py-2">
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {rep.development_areas.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-red-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-red-400 inline-block" />
                Axes de développement
              </h3>
              <ul className="space-y-1.5">
                {rep.development_areas.map((d, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-red-900/20 border border-red-800/40 rounded-lg px-3 py-2">
                    {d}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {rep.coaching_actions.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-amber-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 inline-block" />
                Actions de coaching
              </h3>
              <ul className="space-y-1.5">
                {rep.coaching_actions.map((a, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-amber-900/20 border border-amber-800/40 rounded-lg px-3 py-2">
                    {a}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {rep.session_plan.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-indigo-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 inline-block" />
                Plan de session
              </h3>
              <ol className="space-y-1.5">
                {rep.session_plan.map((step, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-indigo-900/20 border border-indigo-800/40 rounded-lg px-3 py-2 flex gap-2">
                    <span className="text-indigo-400 font-bold shrink-0">{i + 1}.</span>
                    {step}
                  </li>
                ))}
              </ol>
            </div>
          )}

          {rep.kpis_to_track.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-slate-400 inline-block" />
                KPIs à suivre
              </h3>
              <div className="flex flex-wrap gap-2">
                {rep.kpis_to_track.map((kpi, i) => (
                  <span key={i} className="text-xs text-slate-300 bg-slate-800 border border-slate-700 rounded-full px-3 py-1">
                    {kpi}
                  </span>
                ))}
              </div>
            </div>
          )}

          {rep.top_skill_gaps.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-violet-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-violet-400 inline-block" />
                Gaps compétences détectés
              </h3>
              <div className="flex flex-wrap gap-2">
                {rep.top_skill_gaps.map((gap) => (
                  <span key={gap} className="text-xs text-violet-300 bg-violet-900/30 border border-violet-800/50 rounded-full px-3 py-1 capitalize">
                    {gap.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const INTENSITIES = ["all", "light", "moderate", "intensive", "critical"];
const FOCUSES = ["all", "strategy", "skills", "pipeline", "mindset", "process"];

export default function SalesCoachingEnginePage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedRep, setSelectedRep] = useState<Rep | null>(null);
  const [intensityFilter, setIntensityFilter] = useState("all");
  const [focusFilter, setFocusFilter] = useState("all");

  useEffect(() => {
    async function load() {
      const params = new URLSearchParams();
      if (intensityFilter !== "all") params.set("intensity", intensityFilter);
      if (focusFilter !== "all") params.set("focus", focusFilter);
      const res = await fetch(`/api/sales-coaching?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    }
    load();
  }, [intensityFilter, focusFilter]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 animate-pulse">Chargement coaching...</div>
      </div>
    );
  }

  const s = data!.summary;

  const kpis = [
    { label: "Score Moyen", value: s.avg_coaching_score.toFixed(1), sub: "/ 100" },
    { label: "Stars", value: s.star_count, sub: "top performers" },
    { label: "Critiques", value: s.critical_count, sub: "intervention urgente" },
    { label: "Total Reps", value: s.total, sub: "évalués" },
    { label: "Intensive", value: (s.intensity_counts["intensive"] || 0) + (s.intensity_counts["critical"] || 0), sub: "coaching intensif" },
    { label: "Strategy Focus", value: s.focus_counts["strategy"] || 0, sub: "focus stratégie" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Coaching Ventes</h1>
          <p className="text-slate-400 mt-1">Analyse IA des compétences commerciales et plans de développement personnalisés</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          {kpis.map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
              <div className="text-2xl font-bold text-slate-100">{value}</div>
              <div className="text-xs text-slate-400 mt-0.5">{label}</div>
              <div className="text-xs text-slate-600 mt-0.5">{sub}</div>
            </div>
          ))}
        </div>

        <IntensityBar counts={s.intensity_counts} total={s.total} />

        <div className="flex flex-wrap gap-2 mb-3">
          {INTENSITIES.map((v) => (
            <button
              key={v}
              onClick={() => setIntensityFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors capitalize ${
                intensityFilter === v
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Toutes intensités" : v}
              {v !== "all" && s.intensity_counts[v] ? ` (${s.intensity_counts[v]})` : ""}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap gap-2 mb-8">
          {FOCUSES.map((v) => (
            <button
              key={v}
              onClick={() => setFocusFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors capitalize ${
                focusFilter === v
                  ? "bg-violet-600 border-violet-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Tous les focus" : v}
              {v !== "all" && s.focus_counts[v] ? ` (${s.focus_counts[v]})` : ""}
            </button>
          ))}
        </div>

        {data!.reps.length === 0 ? (
          <div className="text-center text-slate-500 py-20">Aucun commercial pour ces filtres</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {data!.reps.map((rep) => (
              <RepCard key={rep.rep_id} rep={rep} onClick={() => setSelectedRep(rep)} />
            ))}
          </div>
        )}
      </div>

      {selectedRep && <CoachingModal rep={selectedRep} onClose={() => setSelectedRep(null)} />}
    </div>
  );
}
