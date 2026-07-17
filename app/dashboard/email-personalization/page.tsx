"use client";

import { useState, useEffect } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type EmailRecord = {
  prospect_id: string;
  campaign_id: string;
  rep_id: string;
  name: string;
  company: string;
  industry: string;
  company_size: string;
  personalization_score: number;
  personalization_level: string;
  email_tone: string;
  send_timing: string;
  recommended_action: string;
  predicted_open_rate: number;
  predicted_reply_rate: number;
  send_score: number;
  is_ready_to_send: boolean;
  personalization_tips: string[];
  subject_suggestions: string[];
  risk_flags: string[];
  optimization_score: number;
};

type Summary = {
  total: number;
  level_counts: Record<string, number>;
  tone_counts: Record<string, number>;
  timing_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_personalization_score: number;
  avg_send_score: number;
  avg_predicted_open_rate: number;
  avg_predicted_reply_rate: number;
  ready_to_send_count: number;
  needs_review_count: number;
  held_count: number;
  high_personalization_count: number;
};

// ── Helpers ───────────────────────────────────────────────────────────────────

const LEVEL_LABELS: Record<string, string> = {
  hyper_personalized:     "Hyper-Perso",
  highly_personalized:    "Très Perso",
  moderately_personalized:"Moyennement Perso",
  generic:                "Générique",
  template:               "Template",
};

const TONE_LABELS: Record<string, string> = {
  executive:    "Exécutif",
  consultative: "Consultatif",
  challenger:   "Challenger",
  educational:  "Éducatif",
  urgency:      "Urgence",
};

const TIMING_LABELS: Record<string, string> = {
  immediate:           "Immédiat",
  morning:             "Matin",
  midday:              "Midi",
  afternoon:           "Après-midi",
  next_business_day:   "Prochain jour ouvré",
  hold:                "En attente",
};

const ACTION_LABELS: Record<string, string> = {
  send_now:           "Envoyer",
  refine_and_send:    "Affiner & Envoyer",
  review_before_send: "Réviser avant envoi",
  rewrite_required:   "Réécriture requise",
  hold:               "Bloquer",
};

function levelColor(level: string) {
  return {
    hyper_personalized:     "bg-violet-500/20 text-violet-300 border-violet-500/30",
    highly_personalized:    "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
    moderately_personalized:"bg-blue-500/20 text-blue-300 border-blue-500/30",
    generic:                "bg-amber-500/20 text-amber-300 border-amber-500/30",
    template:               "bg-slate-500/20 text-slate-300 border-slate-500/30",
  }[level] ?? "bg-slate-500/20 text-slate-300 border-slate-500/30";
}

function actionColor(action: string) {
  return {
    send_now:           "text-emerald-400",
    refine_and_send:    "text-blue-400",
    review_before_send: "text-amber-400",
    rewrite_required:   "text-orange-400",
    hold:               "text-red-400",
  }[action] ?? "text-slate-400";
}

function toneColor(tone: string) {
  return {
    executive:    "bg-violet-500/20 text-violet-300",
    consultative: "bg-blue-500/20 text-blue-300",
    challenger:   "bg-orange-500/20 text-orange-300",
    educational:  "bg-slate-500/20 text-slate-300",
    urgency:      "bg-red-500/20 text-red-300",
  }[tone] ?? "bg-slate-500/20 text-slate-300";
}

// ── PersonalizationGauge ──────────────────────────────────────────────────────

function PersonalizationGauge({ score }: { score: number }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const strokeColor =
    score >= 80 ? "#a78bfa"
    : score >= 65 ? "#34d399"
    : score >= 45 ? "#60a5fa"
    : score >= 25 ? "#f59e0b"
    : "#64748b";

  return (
    <svg width="88" height="88" viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none" stroke={strokeColor} strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={`${arc} ${circ - arc}`}
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy - 3} textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
        {score}
      </text>
      <text x={cx} y={cy + 11} textAnchor="middle" fill="#94a3b8" fontSize="7.5">
        Perso
      </text>
    </svg>
  );
}

// ── LevelDistBar ──────────────────────────────────────────────────────────────

function LevelDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const palette: Record<string, string> = {
    hyper_personalized:     "#a78bfa",
    highly_personalized:    "#34d399",
    moderately_personalized:"#60a5fa",
    generic:                "#f59e0b",
    template:               "#64748b",
  };
  const order = ["hyper_personalized", "highly_personalized", "moderately_personalized", "generic", "template"];
  const entries = order.filter((k) => k in counts).map((k) => [k, counts[k]] as [string, number]);

  return (
    <div className="space-y-2">
      {entries.map(([lvl, count]) => (
        <div key={lvl} className="flex items-center gap-2">
          <span className="w-36 text-xs text-slate-400 truncate">{LEVEL_LABELS[lvl] ?? lvl}</span>
          <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: total ? `${(count / total) * 100}%` : "0%",
                backgroundColor: palette[lvl] ?? "#64748b",
              }}
            />
          </div>
          <span className="w-5 text-xs text-slate-400 text-right">{count}</span>
        </div>
      ))}
    </div>
  );
}

// ── EmailCard ─────────────────────────────────────────────────────────────────

function MiniBar({ label, value, max = 100, color }: { label: string; value: number; max?: number; color: string }) {
  const pct = (value / max) * 100;
  return (
    <div>
      <div className="flex justify-between mb-0.5">
        <span className="text-[10px] text-slate-400">{label}</span>
        <span className="text-[10px] text-slate-300">{value}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function EmailCard({ rec, onClick }: { rec: EmailRecord; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-3 mb-3">
        <PersonalizationGauge score={rec.personalization_score} />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-white truncate">{rec.name}</p>
          <p className="text-xs text-slate-400 truncate">{rec.company}</p>
          <p className="text-xs text-slate-500 truncate capitalize">{rec.industry} · {rec.company_size}</p>
          <div className="flex flex-wrap gap-1 mt-1.5">
            <span className={`text-[10px] px-2 py-0.5 rounded-full border ${levelColor(rec.personalization_level)}`}>
              {LEVEL_LABELS[rec.personalization_level] ?? rec.personalization_level}
            </span>
            <span className={`text-[10px] px-2 py-0.5 rounded-full ${toneColor(rec.email_tone)}`}>
              {TONE_LABELS[rec.email_tone] ?? rec.email_tone}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-1.5 mb-3">
        <MiniBar label="Score d'envoi"      value={rec.send_score}          color="#60a5fa" />
        <MiniBar label="Opt. score"         value={rec.optimization_score}   color="#a78bfa" />
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className={`font-medium ${actionColor(rec.recommended_action)}`}>
          {ACTION_LABELS[rec.recommended_action] ?? rec.recommended_action}
        </span>
        <span className="text-slate-500">{TIMING_LABELS[rec.send_timing] ?? rec.send_timing}</span>
      </div>

      {rec.risk_flags.length > 0 && (
        <div className="mt-2 text-[10px] text-red-400 bg-red-900/20 rounded px-2 py-1">
          ⚠ {rec.risk_flags[0]}
        </div>
      )}
    </div>
  );
}

// ── EmailModal ────────────────────────────────────────────────────────────────

function EmailModal({ rec, onClose }: { rec: EmailRecord; onClose: () => void }) {
  const [tab, setTab] = useState<"action" | "suggestions" | "tips">("action");

  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-center gap-3">
              <PersonalizationGauge score={rec.personalization_score} />
              <div>
                <p className="text-lg font-bold text-white">{rec.name}</p>
                <p className="text-sm text-slate-400">{rec.company}</p>
                <p className="text-xs text-slate-500 capitalize">{rec.industry} · {rec.company_size}</p>
              </div>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">×</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-3">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${levelColor(rec.personalization_level)}`}>
              {LEVEL_LABELS[rec.personalization_level] ?? rec.personalization_level}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full ${toneColor(rec.email_tone)}`}>
              {TONE_LABELS[rec.email_tone] ?? rec.email_tone}
            </span>
            <span className="text-xs text-slate-400">
              {TIMING_LABELS[rec.send_timing] ?? rec.send_timing}
            </span>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-3 p-5 border-b border-slate-800">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Score d'envoi</p>
            <p className="text-xl font-bold text-blue-400">{rec.send_score}</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Score d'optim.</p>
            <p className="text-xl font-bold text-violet-400">{rec.optimization_score}</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Ouverture prédite</p>
            <p className="text-xl font-bold text-emerald-400">{(rec.predicted_open_rate * 100).toFixed(1)}%</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Réponse prédite</p>
            <p className="text-xl font-bold text-amber-400">{(rec.predicted_reply_rate * 100).toFixed(1)}%</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["action", "suggestions", "tips"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-medium transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "action" ? "Action" : t === "suggestions" ? "Sujets" : "Conseils"}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "action" && (
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Action recommandée</p>
                <p className={`text-sm font-bold ${actionColor(rec.recommended_action)}`}>
                  {ACTION_LABELS[rec.recommended_action] ?? rec.recommended_action}
                </p>
              </div>
              {rec.risk_flags.length > 0 && (
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Alertes</p>
                  <ul className="space-y-1">
                    {rec.risk_flags.map((flag, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-red-300">
                        <span className="text-red-400 mt-0.5">!</span>
                        <span>{flag}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Prêt à envoyer</p>
                <p className={`text-sm font-bold ${rec.is_ready_to_send ? "text-emerald-400" : "text-red-400"}`}>
                  {rec.is_ready_to_send ? "Oui" : "Non"}
                </p>
              </div>
            </div>
          )}
          {tab === "suggestions" && (
            <div>
              {rec.subject_suggestions.length === 0 ? (
                <p className="text-sm text-slate-500 italic">Aucune suggestion disponible.</p>
              ) : (
                <ul className="space-y-2">
                  {rec.subject_suggestions.map((s, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300 bg-slate-800/50 rounded-lg p-2">
                      <span className="text-indigo-400 mt-0.5 text-xs font-bold">#{i + 1}</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
          {tab === "tips" && (
            <div>
              {rec.personalization_tips.length === 0 ? (
                <p className="text-sm text-slate-500 italic">Email bien personnalisé — aucune amélioration nécessaire.</p>
              ) : (
                <ul className="space-y-2">
                  {rec.personalization_tips.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-amber-400 mt-0.5">→</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function EmailPersonalizationPage() {
  const [data, setData] = useState<{ emails: EmailRecord[]; summary: Summary } | null>(null);
  const [loading, setLoading]           = useState(true);
  const [error, setError]               = useState<string | null>(null);
  const [levelFilter, setLevelFilter]   = useState<string>("all");
  const [actionFilter, setActionFilter] = useState<string>("all");
  const [selected, setSelected]         = useState<EmailRecord | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        setError(null);
        try {
          const params = new URLSearchParams();
          if (levelFilter  !== "all") params.set("level", levelFilter);
          if (actionFilter !== "all") params.set("action", actionFilter);
          const res = await fetch(`/api/email-personalization?${params}`);
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          setData(await res.json());
        } catch (e: unknown) {
          setError(e instanceof Error ? e.message : "Erreur inconnue");
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [levelFilter, actionFilter]);

  const s = data?.summary;

  const kpis = s
    ? [
        { label: "Total Emails",          value: s.total,                    color: "text-blue-400" },
        { label: "Prêts à envoyer",        value: s.ready_to_send_count,      color: "text-emerald-400" },
        { label: "Haute perso.",           value: s.high_personalization_count, color: "text-violet-400" },
        { label: "À réviser",              value: s.needs_review_count,       color: "text-amber-400" },
        { label: "Score perso. moy.",      value: s.avg_personalization_score, color: "text-blue-400" },
        { label: "En attente",             value: s.held_count,               color: "text-red-400" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Email Personalization Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">
          Score de personnalisation, timing optimal et suggestions pour chaque email outbound
        </p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/30 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-400 mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Rates */}
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
          <p className="text-sm font-semibold text-white mb-4">Taux Prédits Moyens</p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-slate-400 mb-1">Ouverture</p>
              <p className="text-2xl font-bold text-emerald-400">
                {s ? `${(s.avg_predicted_open_rate * 100).toFixed(1)}%` : "—"}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-400 mb-1">Réponse</p>
              <p className="text-2xl font-bold text-amber-400">
                {s ? `${(s.avg_predicted_reply_rate * 100).toFixed(1)}%` : "—"}
              </p>
            </div>
          </div>
        </div>

        {/* Level distribution */}
        <div className="lg:col-span-2 bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
          <p className="text-sm font-semibold text-white mb-4">Distribution de Personnalisation</p>
          {s ? (
            <LevelDistBar counts={s.level_counts} total={s.total} />
          ) : (
            <div className="h-24 bg-slate-700/30 rounded animate-pulse" />
          )}
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-5">
        <div className="flex flex-wrap gap-1">
          {["all", "hyper_personalized", "highly_personalized", "moderately_personalized", "generic", "template"].map((v) => (
            <button
              key={v}
              onClick={() => setLevelFilter(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                levelFilter === v
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {v === "all" ? "Tous les niveaux" : (LEVEL_LABELS[v] ?? v)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          {["all", "send_now", "refine_and_send", "review_before_send", "rewrite_required", "hold"].map((v) => (
            <button
              key={v}
              onClick={() => setActionFilter(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                actionFilter === v
                  ? "bg-violet-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {v === "all" ? "Toutes actions" : (ACTION_LABELS[v] ?? v)}
            </button>
          ))}
        </div>
      </div>

      {/* Cards */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-52 bg-slate-800/40 rounded-xl animate-pulse" />
          ))}
        </div>
      ) : (
        <>
          <p className="text-xs text-slate-500 mb-3">{data?.emails.length ?? 0} email(s) affiché(s)</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {(data?.emails ?? []).map((rec) => (
              <EmailCard key={rec.prospect_id} rec={rec} onClick={() => setSelected(rec)} />
            ))}
          </div>
        </>
      )}

      {selected && <EmailModal rec={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
