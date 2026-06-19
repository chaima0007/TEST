"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface WellbeingUnit {
  unit_id: string;
  workforce_segment: string;
  region: string;
  wellbeing_risk: string;
  emotional_pattern: string;
  wellbeing_severity: string;
  recommended_action: string;
  burnout_score: number;
  safety_score: number;
  meaning_score: number;
  connection_score: number;
  emotional_composite: number;
  has_burnout_alert: boolean;
  requires_emergency_support: boolean;
  estimated_burnout_risk_index: number;
  wellbeing_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_emotional_composite: number;
  burnout_alert_count: number;
  emergency_support_count: number;
  avg_burnout_score: number;
  avg_safety_score: number;
  avg_meaning_score: number;
  avg_connection_score: number;
  avg_estimated_burnout_risk_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-pink-400",
  moderate: "text-rose-300",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-pink-500/20 border-pink-500/40",
  moderate: "bg-rose-400/10 border-rose-400/30",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  crisis:      "text-rose-400",
  depleted:    "text-pink-400",
  recovering:  "text-rose-300",
  flourishing: "text-slate-300",
};

const PATTERN_ICON: Record<string, string> = {
  burnout_crisis:     "🔥",
  meaning_collapse:   "💔",
  isolation_epidemic: "🫥",
  safety_erosion:     "🛡️",
  joy_deficit:        "🌫️",
  none:               "—",
};

const SEGMENT_ICON: Record<string, string> = {
  executive_layer:   "👔",
  frontline_workers: "🏗️",
  remote_workforce:  "🏠",
  creative_teams:    "🎨",
  technical_staff:   "⚙️",
  customer_facing:   "🤝",
  caregiving_roles:  "💙",
  gig_workforce:     "🔄",
};

// ── GaugeRing ────────────────────────────────────────────────────────────────
function GaugeRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
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
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── ScoreBar ─────────────────────────────────────────────────────────────────
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

// ── DistBar ───────────────────────────────────────────────────────────────────
function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-pink-500/30 rounded-xl p-4">
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
}

// ── DetailModal ───────────────────────────────────────────────────────────────
function DetailModal({ unit, onClose }: { unit: WellbeingUnit; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    unit.emotional_composite >= 60 ? "#f43f5e"
    : unit.emotional_composite >= 40 ? "#ec4899"
    : unit.emotional_composite >= 20 ? "#fb7185"
    : "#64748b";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-pink-500/30 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <GaugeRing score={unit.emotional_composite} label="" color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {SEGMENT_ICON[unit.workforce_segment] || "👤"} {unit.unit_id}
            </h2>
            <p className="text-slate-400 text-sm">{unit.workforce_segment.replace(/_/g, " ")} · {unit.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[unit.wellbeing_risk]}`}>
                {unit.wellbeing_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[unit.wellbeing_severity]}`}>
                {unit.wellbeing_severity}
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
                tab === t ? "text-rose-400 border-b-2 border-rose-400" : "text-slate-500 hover:text-slate-300"
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
                  ["Pattern",             PATTERN_ICON[unit.emotional_pattern] + " " + unit.emotional_pattern.replace(/_/g, " ")],
                  ["Risque Burnout",      unit.estimated_burnout_risk_index.toFixed(2) + " / 10"],
                  ["Alerte Burnout",      unit.has_burnout_alert ? "🚨 Oui" : "Non"],
                  ["Support Urgence",     unit.requires_emergency_support ? "⚡ Oui" : "Non"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal de Capital Émotionnel</div>
                <div className="text-rose-300 text-sm leading-relaxed">{unit.wellbeing_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Prévention Burnout"       value={unit.burnout_score}    color="bg-rose-500" />
              <ScoreBar label="Sécurité Psychologique"   value={unit.safety_score}     color="bg-pink-500" />
              <ScoreBar label="Sens & Alignement"        value={unit.meaning_score}    color="bg-rose-400" />
              <ScoreBar label="Capital Connexion"        value={unit.connection_score} color="bg-pink-400" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4">
                <div className="text-xs text-rose-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg capitalize">
                  {unit.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {unit.requires_emergency_support && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  ⚡ Support d&apos;urgence requis — déclencher le protocole de crise immédiatement
                </div>
              )}
              {unit.has_burnout_alert && (
                <div className="bg-pink-500/10 border border-pink-500/30 rounded-xl p-3 text-sm text-pink-300">
                  🚨 Alerte burnout active — intervention prioritaire requise
                </div>
              )}
              {!unit.has_burnout_alert && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ Pas d&apos;alerte burnout — surveillance continue recommandée
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── UnitCard ──────────────────────────────────────────────────────────────────
function UnitCard({ unit, onClick }: { unit: WellbeingUnit; onClick: () => void }) {
  const ringColor =
    unit.emotional_composite >= 60 ? "#f43f5e"
    : unit.emotional_composite >= 40 ? "#ec4899"
    : unit.emotional_composite >= 20 ? "#fb7185"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-pink-500/30 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <GaugeRing score={unit.emotional_composite} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {SEGMENT_ICON[unit.workforce_segment] || "👤"} {unit.unit_id}
          </div>
          <div className="text-slate-400 text-xs">{unit.workforce_segment.replace(/_/g, " ")} · {unit.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[unit.wellbeing_risk]}`}>
              {unit.wellbeing_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {unit.requires_emergency_support && <div className="text-xs text-rose-400">⚡ Urgence</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[unit.wellbeing_severity]}`}>
            {unit.wellbeing_severity}
          </div>
          {unit.has_burnout_alert && (
            <div className="text-xs text-pink-400 mt-1">🚨</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[unit.emotional_pattern]} {unit.emotional_pattern.replace(/_/g, " ")} · risque: {unit.estimated_burnout_risk_index.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────
export default function EmotionalCapitalEnginePage() {
  const [units, setUnits]       = useState<WellbeingUnit[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<WellbeingUnit | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterRisk    !== "all") params.set("risk",    filterRisk);
    if (filterPattern !== "all") params.set("pattern", filterPattern);
    fetch(`/api/emotional-capital-engine?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setUnits(data.units);
        setSummary(data.summary);
        setLoading(false);
      });
  }, [filterRisk, filterPattern]);

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    {
      title: "Patterns Émotionnels",
      counts: summary?.pattern_counts ?? {},
      colors: { burnout_crisis: "bg-rose-500", meaning_collapse: "bg-pink-500", isolation_epidemic: "bg-rose-400", safety_erosion: "bg-pink-400", joy_deficit: "bg-rose-300", none: "bg-slate-500" },
    },
    {
      title: "Sévérité Bien-être",
      counts: summary?.severity_counts ?? {},
      colors: { crisis: "bg-rose-500", depleted: "bg-pink-500", recovering: "bg-rose-300", flourishing: "bg-slate-400" },
    },
    {
      title: "Distribution du Risque",
      counts: summary?.risk_counts ?? {},
      colors: { critical: "bg-rose-500", high: "bg-pink-500", moderate: "bg-rose-300", low: "bg-slate-500" },
    },
    {
      title: "Actions Prescrites",
      counts: summary?.action_counts ?? {},
      colors: { emergency_wellbeing: "bg-rose-500", burnout_intervention: "bg-pink-600", meaning_restoration: "bg-pink-400", connection_program: "bg-rose-300", wellbeing_monitoring: "bg-slate-400", no_action: "bg-slate-600" },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Emotional Capital & Wellbeing Economy Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Mesure le capital émotionnel comme actif stratégique organisationnel — suivi de l&apos;économie
            du bien-être, de la sécurité psychologique à l&apos;échelle et prescription d&apos;interventions
            avant que l&apos;épuisement ne devienne systémique.
          </p>
        </div>

        {/* KPI strip — 6 cards */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Unités",               value: summary.total },
              { label: "Composite Moy.",        value: summary.avg_emotional_composite.toFixed(1),          color: "text-rose-400" },
              { label: "Alertes Burnout",       value: summary.burnout_alert_count,                         color: "text-pink-400" },
              { label: "Support Urgence",       value: summary.emergency_support_count,                     color: "text-rose-500" },
              { label: "Risque Burnout Moy.",   value: summary.avg_estimated_burnout_risk_index.toFixed(2), color: "text-pink-300" },
              { label: "Score Sécurité Moy.",   value: summary.avg_safety_score.toFixed(1),                 color: "text-rose-300" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-pink-500/30 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 GaugeRings */}
        {summary && (
          <div className="bg-slate-900 border border-pink-500/30 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Dimensions du Capital Émotionnel</div>
            <div className="flex flex-wrap gap-6 justify-around">
              <GaugeRing score={summary.avg_burnout_score}    label="Prévention Burnout"     color="#f43f5e" />
              <GaugeRing score={summary.avg_safety_score}     label="Sécurité Psychologique" color="#ec4899" />
              <GaugeRing score={summary.avg_meaning_score}    label="Sens & Alignement"      color="#fb7185" />
              <GaugeRing score={summary.avg_connection_score} label="Capital Connexion"       color="#f9a8d4" />
            </div>
          </div>
        )}

        {/* 4 DistBars */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {distributions.map((d) => (
              <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
            ))}
          </div>
        )}

        {/* filter pills */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "Tous",            val: "all" },
            { label: "🔴 Critical",     val: "critical" },
            { label: "🩷 High",         val: "high" },
            { label: "🌸 Moderate",     val: "moderate" },
            { label: "⚫ Low",          val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-rose-700 text-white"
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
            {["burnout_crisis", "meaning_collapse", "isolation_epidemic", "safety_erosion", "joy_deficit", "none"].map((p) => (
              <option key={p} value={p}>{p.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* unit cards grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse du capital émotionnel…</div>
        ) : units.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune unité ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {units.map((u) => (
              <UnitCard key={u.unit_id} unit={u} onClick={() => setSelected(u)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal unit={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
