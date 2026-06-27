"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface OrgUnit {
  unit_id: string;
  department: string;
  region: string;
  health_risk: string;
  culture_pattern: string;
  health_severity: string;
  recommended_action: string;
  engagement_score: number;
  leadership_score: number;
  culture_score: number;
  wellbeing_score: number;
  health_composite: number;
  has_culture_alert: boolean;
  requires_executive_intervention: boolean;
  estimated_culture_risk_index: number;
  health_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_health_composite: number;
  culture_alert_count: number;
  executive_intervention_count: number;
  avg_engagement_score: number;
  avg_leadership_score: number;
  avg_culture_score: number;
  avg_wellbeing_score: number;
  avg_estimated_culture_risk_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-emerald-400",
  moderate: "text-teal-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-emerald-500/20 border-emerald-500/40",
  moderate: "bg-teal-500/20 border-teal-500/40",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  critical:   "text-rose-400",
  concerning: "text-orange-400",
  stable:     "text-teal-400",
  thriving:   "text-emerald-400",
};

const PATTERN_ICON: Record<string, string> = {
  toxic_culture:        "☠️",
  disengagement_spiral: "📉",
  leadership_void:      "👤",
  change_resistance:    "🧱",
  diversity_gap:        "🌍",
  none:                 "—",
};

const DEPT_ICON: Record<string, string> = {
  sales:       "💼",
  engineering: "⚙️",
  ops:         "🏗️",
  finance:     "💰",
  marketing:   "📣",
  HR:          "🤝",
  product:     "🚀",
  logistics:   "🚚",
};

function CompositeRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={44} cy={44} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const order  = ["critical", "high", "moderate", "low"];
  const colors = ["bg-rose-500", "bg-emerald-500", "bg-teal-500", "bg-slate-500"];
  const total  = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex gap-1 h-3 rounded-full overflow-hidden">
      {order.map((k, i) => (
        <div
          key={k}
          className={colors[i]}
          style={{ width: `${((counts[k] || 0) / total) * 100}%` }}
          title={`${k}: ${counts[k] || 0}`}
        />
      ))}
    </div>
  );
}

// ── OrgModal ──────────────────────────────────────────────────────────────────
function OrgModal({ unit, onClose }: { unit: OrgUnit; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    unit.health_composite >= 60 ? "#f43f5e"
    : unit.health_composite >= 40 ? "#f97316"
    : unit.health_composite >= 20 ? "#14b8a6"
    : "#10b981";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <CompositeRing score={unit.health_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {DEPT_ICON[unit.department] || "🏢"} {unit.unit_id}
            </h2>
            <p className="text-slate-400 text-sm">{unit.department} · {unit.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[unit.health_risk]}`}>
                {unit.health_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[unit.health_severity]}`}>
                {unit.health_severity}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-emerald-400 border-b-2 border-emerald-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern",           PATTERN_ICON[unit.culture_pattern] + " " + unit.culture_pattern.replace(/_/g, " ")],
                  ["Risque Culture",    unit.estimated_culture_risk_index.toFixed(2) + " / 10"],
                  ["Alerte Culture",    unit.has_culture_alert ? "🚨 Oui" : "Non"],
                  ["Intervention Exec", unit.requires_executive_intervention ? "⚡ Oui" : "Non"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal de Santé</div>
                <div className="text-emerald-300 text-sm leading-relaxed">{unit.health_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Engagement"  value={unit.engagement_score}  color="bg-emerald-500" />
              <ScoreBar label="Leadership"  value={unit.leadership_score}  color="bg-teal-500" />
              <ScoreBar label="Culture"     value={unit.culture_score}     color="bg-green-500" />
              <ScoreBar label="Bien-être"   value={unit.wellbeing_score}   color="bg-emerald-700" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4">
                <div className="text-xs text-emerald-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg capitalize">
                  {unit.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {unit.requires_executive_intervention && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  ⚡ Intervention executive requise — escalader immédiatement à la direction
                </div>
              )}
              {unit.has_culture_alert && (
                <div className="bg-orange-500/10 border border-orange-500/30 rounded-xl p-3 text-sm text-orange-300">
                  🚨 Alerte culture active — déclencher le programme d&apos;intervention
                </div>
              )}
              {!unit.has_culture_alert && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ Pas d&apos;alerte culture — surveillance continue recommandée
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── OrgCard ───────────────────────────────────────────────────────────────────
function OrgCard({ unit, onClick }: { unit: OrgUnit; onClick: () => void }) {
  const ringColor =
    unit.health_composite >= 60 ? "#f43f5e"
    : unit.health_composite >= 40 ? "#f97316"
    : unit.health_composite >= 20 ? "#14b8a6"
    : "#10b981";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-emerald-700 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <CompositeRing score={unit.health_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {DEPT_ICON[unit.department] || "🏢"} {unit.unit_id}
          </div>
          <div className="text-slate-400 text-xs">{unit.department} · {unit.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[unit.health_risk]}`}>
              {unit.health_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {unit.requires_executive_intervention && <div className="text-xs text-rose-400">⚡ Exec</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[unit.health_severity]}`}>
            {unit.health_severity}
          </div>
          {unit.has_culture_alert && (
            <div className="text-xs text-orange-400 mt-1">🚨</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[unit.culture_pattern]} {unit.culture_pattern.replace(/_/g, " ")} · risque: {unit.estimated_culture_risk_index.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function OrganizationalHealthCultureEnginePage() {
  const [units, setUnits]       = useState<OrgUnit[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<OrgUnit | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterRisk    !== "all") params.set("risk",    filterRisk);
        if (filterPattern !== "all") params.set("pattern", filterPattern);
        const res  = await fetch(`/api/organizational-health-culture-engine?${params}`);
        const data = await res.json();
        setUnits(data.units);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterRisk, filterPattern]);

  const distributions = [
    { title: "Patterns Culture",  counts: summary?.pattern_counts ?? {},  colors: { toxic_culture: "bg-rose-500", disengagement_spiral: "bg-orange-500", leadership_void: "bg-amber-500", change_resistance: "bg-yellow-500", diversity_gap: "bg-teal-500", none: "bg-slate-500" } },
    { title: "Sévérité",          counts: summary?.severity_counts ?? {}, colors: { critical: "bg-rose-500", concerning: "bg-orange-500", stable: "bg-teal-500", thriving: "bg-emerald-500" } },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Organizational Health & Culture Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Surveille l&apos;engagement des collaborateurs, l&apos;efficacité du leadership, la sécurité
            psychologique, l&apos;alignement culturel et les signaux de bien-être — et prescrit des
            interventions ciblées avant que la dysfonction ne devienne systémique.
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Unités",              value: summary.total },
              { label: "Composite Moy.",      value: summary.avg_health_composite.toFixed(1),            color: "text-emerald-400" },
              { label: "Alertes Culture",     value: summary.culture_alert_count,                        color: "text-rose-400" },
              { label: "Interv. Exec",        value: summary.executive_intervention_count,               color: "text-orange-400" },
              { label: "Risque Culture Moy.", value: summary.avg_estimated_culture_risk_index.toFixed(2), color: "text-teal-400" },
              { label: "Moy. Engagement",     value: summary.avg_engagement_score.toFixed(1),            color: "text-green-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 gauge bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Scores Moyens par Dimension</div>
            <div className="space-y-3">
              <ScoreBar label="Engagement"  value={summary.avg_engagement_score}  color="bg-emerald-500" />
              <ScoreBar label="Leadership"  value={summary.avg_leadership_score}  color="bg-teal-500" />
              <ScoreBar label="Culture"     value={summary.avg_culture_score}     color="bg-green-500" />
              <ScoreBar label="Bien-être"   value={summary.avg_wellbeing_score}   color="bg-emerald-700" />
            </div>
          </div>
        )}

        {/* distribution bars */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {distributions.map(({ title, counts, colors }) => {
              const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
              return (
                <div key={title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                  <div className="text-xs text-slate-400 mb-2">{title}</div>
                  <div className="flex gap-1 h-3 rounded-full overflow-hidden">
                    {Object.entries(counts).map(([k, v]) => (
                      <div
                        key={k}
                        className={colors[k] ?? "bg-slate-600"}
                        style={{ width: `${(v / total) * 100}%` }}
                        title={`${k}: ${v}`}
                      />
                    ))}
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2 text-xs text-slate-500">
                    {Object.entries(counts).map(([k, v]) => (
                      <span key={k}>{k.replace(/_/g, " ")}: {v}</span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* risk distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Distribution du Risque Santé Org.</div>
            <RiskDistBar counts={summary.risk_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["critical", "high", "moderate", "low"].map((k) => (
                <span key={k} className={RISK_COLOR[k]}>{k}: {summary.risk_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "Tous",           val: "all" },
            { label: "🔴 Critical",    val: "critical" },
            { label: "🟢 High",        val: "high" },
            { label: "🩵 Moderate",    val: "moderate" },
            { label: "⚫ Low",         val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-emerald-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterPattern}
            onChange={(e) => setFilterPattern(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">Tous Patterns</option>
            {["toxic_culture", "disengagement_spiral", "leadership_void", "change_resistance", "diversity_gap", "none"].map((p) => (
              <option key={p} value={p}>{p.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* units grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse de la santé organisationnelle…</div>
        ) : units.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune unité ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {units.map((u) => (
              <OrgCard key={u.unit_id} unit={u} onClick={() => setSelected(u)} />
            ))}
          </div>
        )}
      </div>

      {selected && <OrgModal unit={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
