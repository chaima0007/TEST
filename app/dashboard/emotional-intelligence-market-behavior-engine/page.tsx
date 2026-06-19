"use client";

import { useState, useEffect } from "react";

interface SegmentData {
  segment_id: string;
  region: string;
  emotional_risk: string;
  behavior_pattern: string;
  emotional_severity: string;
  recommended_action: string;
  sentiment_score: number;
  rationality_score: number;
  bias_score: number;
  resilience_score: number;
  emotional_composite: number;
  has_emotional_crisis: boolean;
  requires_behavioral_intervention: boolean;
  estimated_sentiment_disruption_index: number;
  emotional_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_emotional_composite: number;
  emotional_crisis_count: number;
  behavioral_intervention_count: number;
  avg_sentiment_score: number;
  avg_rationality_score: number;
  avg_bias_score: number;
  avg_resilience_score: number;
  avg_estimated_sentiment_disruption_index: number;
}

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  moderate: "bg-amber-500/20 border-amber-500/30 text-amber-300",
  high:     "bg-orange-500/20 border-orange-500/30 text-orange-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  low:      "#34d399",
  moderate: "#fbbf24",
  high:     "#f97316",
  critical: "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  low:      "Low",
  moderate: "Moderate",
  high:     "High",
  critical: "Critical",
};
const SEVERITY_BG: Record<string, string> = {
  rational:  "bg-emerald-500/15 text-emerald-300",
  watchful:  "bg-amber-500/15 text-amber-300",
  volatile:  "bg-orange-500/15 text-orange-300",
  chaotic:   "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  rational:  "Rationnel",
  watchful:  "Vigilant",
  volatile:  "Volatile",
  chaotic:   "Chaotique",
};
const ACTION_BG: Record<string, string> = {
  no_action:                    "bg-emerald-500/15 text-emerald-300",
  sentiment_monitoring:         "bg-sky-500/15 text-sky-300",
  behavioral_alert:             "bg-blue-500/15 text-blue-300",
  bias_correction:              "bg-amber-500/15 text-amber-300",
  stakeholder_reframing:        "bg-yellow-500/15 text-yellow-300",
  sentiment_intervention:       "bg-orange-500/15 text-orange-300",
  behavior_circuit_breaker:     "bg-orange-600/15 text-orange-300",
  crisis_communication:         "bg-rose-500/15 text-rose-300",
  emergency_sentiment_reset:    "bg-red-500/15 text-red-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:                    "Aucune Action",
  sentiment_monitoring:         "Surveillance Sentiment",
  behavioral_alert:             "Alerte Comportementale",
  bias_correction:              "Correction Biais",
  stakeholder_reframing:        "Recadrage Parties Prenantes",
  sentiment_intervention:       "Intervention Sentiment",
  behavior_circuit_breaker:     "Disjoncteur Comportemental",
  crisis_communication:         "Communication de Crise",
  emergency_sentiment_reset:    "Reset Sentiment Urgence",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                   "Aucun",
  sentiment_collapse:     "Effondrement Sentiment",
  panic_cascade:          "Cascade Panique",
  irrational_exuberance:  "Exubérance Irrationnelle",
  herding_behavior:       "Comportement Moutonnier",
  cognitive_bias_surge:   "Surge Biais Cognitif",
};

function GaugeRing({ pct, color, label, size = 90 }: { pct: number; color: string; label: string; size?: number }) {
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (Math.min(pct, 100) / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
        <circle
          cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke={color} strokeWidth={size * 0.1}
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={color} fontSize={size * 0.20} fontWeight="bold">
          {pct.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400">{label}</span>
    </div>
  );
}

function ScoreBar({ score, label }: { score: number; label: string }) {
  const color = score <= 20 ? "#34d399" : score <= 40 ? "#fbbf24" : score <= 60 ? "#f97316" : "#f87171";
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-xs text-slate-400">{label}</span>
        <span className="text-xs font-medium" style={{ color }}>{score.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(score, 100)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

type DistBarItem = { title: string; counts: Record<string, number>; colors: Record<string, string> };

function DistBar({ title, counts, colors }: DistBarItem) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (!total) return null;
  return (
    <div>
      <p className="text-xs text-slate-400 mb-1">{title}</p>
      <div className="flex h-2 rounded-full overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) =>
          v > 0 ? (
            <div key={k} style={{ width: `${(v / total) * 100}%`, backgroundColor: colors[k] ?? "#94a3b8" }} title={`${k}: ${v}`} />
          ) : null
        )}
      </div>
      <div className="flex flex-wrap gap-2 mt-1.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs" style={{ color: colors[k] ?? "#94a3b8" }}>
            {k}: {v}
          </span>
        ))}
      </div>
    </div>
  );
}

interface ModalProps { segment: SegmentData; onClose: () => void }

function DetailModal({ segment, onClose }: ModalProps) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[segment.emotional_risk] ?? "#94a3b8";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[segment.emotional_risk] ?? ""}`}>
                {RISK_LABEL[segment.emotional_risk] ?? segment.emotional_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[segment.emotional_severity] ?? ""}`}>
                {SEVERITY_LABEL[segment.emotional_severity] ?? segment.emotional_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{segment.segment_id}</h2>
            <p className="text-slate-400 text-sm">
              {segment.region} · Composite: <span style={{ color: riskColor }}>{segment.emotional_composite}</span>
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 transition-colors" aria-label="Close">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-rose-400 border-b-2 border-rose-500 bg-slate-800/40" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={segment.sentiment_score} label="Sentiment (30%)" />
              <ScoreBar score={segment.rationality_score} label="Rationalité (25%)" />
              <ScoreBar score={segment.bias_score} label="Biais (25%)" />
              <ScoreBar score={segment.resilience_score} label="Résilience (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Composite Émotionnel</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{segment.emotional_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Score composite risque émotionnel (0–100)</p>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GaugeRing pct={segment.emotional_composite} color={riskColor} label="Composite" size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Signal Émotionnel</p>
                <p className="text-sm text-white">{segment.emotional_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Disruption Sentiment</p>
                  <p className="text-lg font-bold text-rose-400">{segment.estimated_sentiment_disruption_index.toFixed(2)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Crise Émotionnelle</p>
                  <p className={`text-lg font-bold ${segment.has_emotional_crisis ? "text-rose-400" : "text-emerald-400"}`}>
                    {segment.has_emotional_crisis ? "Détectée" : "Absente"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Intervention</p>
                  <p className={`text-sm font-medium ${segment.requires_behavioral_intervention ? "text-orange-400" : "text-emerald-400"}`}>
                    {segment.requires_behavioral_intervention ? "Requise" : "Non requise"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium text-slate-200">{PATTERN_LABEL[segment.behavior_pattern] ?? segment.behavior_pattern}</p>
                </div>
              </div>
            </>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Action Recommandée</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[segment.recommended_action] ?? ""}`}>
                  {ACTION_LABEL[segment.recommended_action] ?? segment.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[segment.behavior_pattern] ?? segment.behavior_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[segment.emotional_severity] ?? segment.emotional_severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Disruption Sentiment</span>
                  <span className="text-xs text-rose-400 font-medium">{segment.estimated_sentiment_disruption_index.toFixed(2)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Intervention Comport.</span>
                  <span className={`text-xs font-medium ${segment.requires_behavioral_intervention ? "text-orange-400" : "text-emerald-400"}`}>
                    {segment.requires_behavioral_intervention ? "Requise" : "Non requise"}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const RISK_FILTERS = ["all", "low", "moderate", "high", "critical"] as const;
type RiskFilter = typeof RISK_FILTERS[number];
const PATTERN_FILTERS = ["all", "none", "sentiment_collapse", "panic_cascade", "irrational_exuberance", "herding_behavior", "cognitive_bias_surge"] as const;
type PatternFilter = typeof PATTERN_FILTERS[number];

export default function EmotionalIntelligenceMarketBehaviorEnginePage() {
  const [data, setData] = useState<{ segments: SegmentData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [patternFilter, setPatternFilter] = useState<PatternFilter>("all");
  const [selected, setSelected] = useState<SegmentData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const params = new URLSearchParams();
      if (riskFilter !== "all")    params.set("risk",    riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const res = await fetch(`/api/emotional-intelligence-market-behavior-engine?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    };
    fetchData();
  }, [riskFilter, patternFilter]);

  const s = data?.summary;
  const segments = data?.segments ?? [];

  const riskColors: Record<string, string> = {
    low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171",
  };
  const severityColors: Record<string, string> = {
    rational: "#34d399", watchful: "#fbbf24", volatile: "#f97316", chaotic: "#f87171",
  };
  const patternColors: Record<string, string> = {
    none: "#64748b", sentiment_collapse: "#f87171", panic_cascade: "#f97316",
    irrational_exuberance: "#fbbf24", herding_behavior: "#a78bfa", cognitive_bias_surge: "#fb7185",
  };

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risque", counts: s?.risk_counts ?? {}, colors: riskColors },
    { title: "Sévérité", counts: s?.severity_counts ?? {}, colors: severityColors },
    { title: "Pattern", counts: s?.pattern_counts ?? {}, colors: patternColors },
    { title: "Action", counts: s?.action_counts ?? {}, colors: {} },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal segment={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Intelligence Émotionnelle & Comportement Marché</h1>
        <p className="text-slate-400 text-sm mt-1">
          Sentiment · Rationalité · Biais · Résilience — détection des dynamiques comportementales et émotionnelles
        </p>
      </div>

      {/* KPI Strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Segments</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Composite</p>
          <p className="text-2xl font-bold text-rose-400">{s?.avg_emotional_composite ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Crises Émot.</p>
          <p className="text-2xl font-bold text-rose-400">{s?.emotional_crisis_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Interv. Comport.</p>
          <p className="text-2xl font-bold text-orange-400">{s?.behavioral_intervention_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Disruption Sent.</p>
          <p className="text-2xl font-bold text-pink-400">{s?.avg_estimated_sentiment_disruption_index ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Moy Sentiment</p>
          <p className="text-2xl font-bold text-amber-400">{s?.avg_sentiment_score ?? "—"}</p>
        </div>
      </div>

      {/* Gauge Rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-slate-300 mb-4">Scores Moyens (risque émotionnel)</h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={s?.avg_sentiment_score ?? 0} color="#fb7185" label="Sentiment" />
          <GaugeRing pct={s?.avg_rationality_score ?? 0} color="#f97316" label="Rationalité" />
          <GaugeRing pct={s?.avg_bias_score ?? 0} color="#a78bfa" label="Biais" />
          <GaugeRing pct={s?.avg_resilience_score ?? 0} color="#60a5fa" label="Résilience" />
        </div>
      </div>

      {/* Distribution bars — 4 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <DistBar title={d.title} counts={d.counts} colors={d.colors} />
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="mb-4 space-y-3">
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-slate-500 mr-1">Risque:</span>
          {RISK_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setRiskFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                riskFilter === f
                  ? "bg-rose-700 border-rose-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-rose-700"
              }`}
            >
              {f === "all" ? "Tous" : RISK_LABEL[f] ?? f}
              {f !== "all" && s?.risk_counts?.[f] !== undefined && (
                <span className="ml-1 opacity-70">({s.risk_counts[f]})</span>
              )}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-slate-500 mr-1">Pattern:</span>
          {PATTERN_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setPatternFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                patternFilter === f
                  ? "bg-rose-700 border-rose-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-rose-700"
              }`}
            >
              {f === "all" ? "Tous" : PATTERN_LABEL[f] ?? f}
            </button>
          ))}
        </div>
      </div>

      {/* Segment cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-rose-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {segments.map((segment) => {
            const color = RISK_COLOR[segment.emotional_risk] ?? "#94a3b8";
            return (
              <div
                key={segment.segment_id}
                onClick={() => setSelected(segment)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-rose-700 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1 min-w-0 pr-2">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[segment.emotional_risk] ?? ""}`}>
                        {RISK_LABEL[segment.emotional_risk] ?? segment.emotional_risk}
                      </span>
                      {segment.has_emotional_crisis && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                          CRISE ÉMOT.
                        </span>
                      )}
                      {segment.requires_behavioral_intervention && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-orange-500/20 border border-orange-500/30 text-orange-300 font-medium">
                          INTERV.
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{segment.segment_id}</h3>
                    <p className="text-slate-400 text-xs">{segment.region}</p>
                  </div>
                  <div className="flex-shrink-0">
                    <GaugeRing pct={segment.emotional_composite} color={color} label="" size={72} />
                  </div>
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={segment.sentiment_score} label="Sentiment" />
                  <ScoreBar score={segment.rationality_score} label="Rationalité" />
                  <ScoreBar score={segment.bias_score} label="Biais" />
                  <ScoreBar score={segment.resilience_score} label="Résilience" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[segment.recommended_action] ?? ""}`}>
                    {ACTION_LABEL[segment.recommended_action] ?? segment.recommended_action}
                  </span>
                  <span className="text-xs text-rose-400 font-medium">
                    disr {segment.estimated_sentiment_disruption_index.toFixed(2)}
                  </span>
                </div>
                <div className="flex items-center gap-1.5 mt-2">
                  <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${SEVERITY_BG[segment.emotional_severity] ?? ""}`}>
                    {SEVERITY_LABEL[segment.emotional_severity] ?? segment.emotional_severity}
                  </span>
                  <span className="text-xs text-slate-500 truncate">{PATTERN_LABEL[segment.behavior_pattern] ?? segment.behavior_pattern}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1.5 truncate">{segment.emotional_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
