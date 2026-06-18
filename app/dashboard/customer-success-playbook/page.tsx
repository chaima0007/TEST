"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ──────────────────────────────────────────────────────────────────

type LifecycleStage = "onboarding" | "adoption" | "growth" | "mature" | "at_risk";
type PlaybookMotion = "expand" | "retain" | "rescue" | "onboard" | "accelerate";
type RiskLevel = "low" | "medium" | "high" | "critical";

interface CSAccount {
  account_id: string;
  account_name: string;
  segment: string;
  arr_eur: number;
  lifecycle_stage: LifecycleStage;
  risk_level: RiskLevel;
  playbook_motion: PlaybookMotion;
  overall_health_score: number;
  renewal_urgency: string;
  expansion_readiness: string;
  key_risks: string[];
  immediate_actions: string[];
  playbook_steps: string[];
  success_metrics: string[];
}

interface Summary {
  total: number;
  motion_counts: Record<string, number>;
  stage_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  avg_health_score: number;
  total_arr_at_risk_eur: number;
  total_arr_expansion_ready_eur: number;
  rescue_count: number;
  expand_ready_count: number;
  renewal_urgent_count: number;
}

interface ApiResponse {
  accounts: CSAccount[];
  summary: Summary;
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function fmtEur(n: number) {
  if (n >= 1_000_000) return `€${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `€${Math.round(n / 1_000)}k`;
  return `€${n}`;
}

function motionColor(m: PlaybookMotion) {
  if (m === "expand") return "bg-emerald-500/20 text-emerald-200 border border-emerald-500/30";
  if (m === "retain") return "bg-sky-500/20 text-sky-200 border border-sky-500/30";
  if (m === "rescue") return "bg-red-500/20 text-red-200 border border-red-500/30";
  if (m === "onboard") return "bg-indigo-500/20 text-indigo-200 border border-indigo-500/30";
  return "bg-amber-500/20 text-amber-200 border border-amber-500/30";
}

function riskColor(r: RiskLevel) {
  if (r === "low") return "text-emerald-400";
  if (r === "medium") return "text-amber-400";
  if (r === "high") return "text-orange-400";
  return "text-red-400";
}

function riskBg(r: RiskLevel) {
  if (r === "low") return "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30";
  if (r === "medium") return "bg-amber-500/15 text-amber-300 border border-amber-500/30";
  if (r === "high") return "bg-orange-500/15 text-orange-300 border border-orange-500/30";
  return "bg-red-500/15 text-red-300 border border-red-500/30";
}

function healthBarColor(score: number) {
  if (score >= 75) return "bg-emerald-500";
  if (score >= 50) return "bg-amber-500";
  if (score >= 25) return "bg-orange-500";
  return "bg-red-500";
}

function motionLabel(m: PlaybookMotion) {
  if (m === "expand") return "Expansion";
  if (m === "retain") return "Rétention";
  if (m === "rescue") return "Sauvetage";
  if (m === "onboard") return "Onboarding";
  return "Accélération";
}

function stageLabel(s: LifecycleStage) {
  if (s === "onboarding") return "Onboarding";
  if (s === "adoption") return "Adoption";
  if (s === "growth") return "Croissance";
  if (s === "mature") return "Mature";
  return "À risque";
}

function stageBg(s: LifecycleStage) {
  if (s === "onboarding") return "bg-indigo-500/15 text-indigo-300";
  if (s === "adoption") return "bg-sky-500/15 text-sky-300";
  if (s === "growth") return "bg-emerald-500/15 text-emerald-300";
  if (s === "mature") return "bg-slate-500/15 text-slate-300";
  return "bg-red-500/15 text-red-300";
}

function urgencyLabel(u: string) {
  if (u === "immediate") return "Urgent";
  if (u === "high") return "Élevé";
  if (u === "medium") return "Moyen";
  return "Faible";
}

function urgencyColor(u: string) {
  if (u === "immediate") return "text-red-400";
  if (u === "high") return "text-orange-400";
  if (u === "medium") return "text-amber-400";
  return "text-slate-400";
}

function readinessLabel(r: string) {
  if (r === "ready") return "Prêt";
  if (r === "building") return "En construction";
  return "Non prêt";
}

function readinessColor(r: string) {
  if (r === "ready") return "text-emerald-400";
  if (r === "building") return "text-amber-400";
  return "text-slate-500";
}

// ─── Health Ring ──────────────────────────────────────────────────────────────

function HealthRing({ score, motion }: { score: number; motion: PlaybookMotion }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;

  const stroke =
    motion === "rescue" ? "#ef4444" :
    motion === "expand" ? "#10b981" :
    motion === "onboard" ? "#6366f1" :
    motion === "accelerate" ? "#f59e0b" : "#38bdf8";

  return (
    <svg viewBox="0 0 80 80" className="w-20 h-20" aria-hidden="true">
      <circle cx="40" cy="40" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="40"
        cy="40"
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth="7"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 40 40)"
      />
      <text x="40" y="44" textAnchor="middle" fontSize="15" fontWeight="700" fill="#f1f5f9">
        {score}
      </text>
    </svg>
  );
}

// ─── Risk Distribution Bar ────────────────────────────────────────────────────

function RiskDistBar({ summary }: { summary: Summary }) {
  const n = summary.total || 1;
  const low = summary.risk_counts["low"] || 0;
  const med = summary.risk_counts["medium"] || 0;
  const high = summary.risk_counts["high"] || 0;
  const crit = summary.risk_counts["critical"] || 0;
  return (
    <div className="flex h-2 rounded-full overflow-hidden gap-px bg-slate-800">
      {low > 0 && <div className="bg-emerald-500 h-full" style={{ width: `${(low / n) * 100}%` }} />}
      {med > 0 && <div className="bg-amber-500 h-full" style={{ width: `${(med / n) * 100}%` }} />}
      {high > 0 && <div className="bg-orange-500 h-full" style={{ width: `${(high / n) * 100}%` }} />}
      {crit > 0 && <div className="bg-red-500 h-full" style={{ width: `${(crit / n) * 100}%` }} />}
    </div>
  );
}

// ─── Detail Modal ────────────────────────────────────────────────────────────

function CSModal({ account, onClose }: { account: CSAccount; onClose: () => void }) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) { if (e.key === "Escape") onClose(); }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-100">{account.account_name}</h2>
            <p className="text-slate-400 text-sm mt-0.5">{account.segment.toUpperCase()} · ARR {fmtEur(account.arr_eur)}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 transition-colors text-xl leading-none">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* Summary row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Motion</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${motionColor(account.playbook_motion)}`}>
                {motionLabel(account.playbook_motion)}
              </span>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Étape</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${stageBg(account.lifecycle_stage)}`}>
                {stageLabel(account.lifecycle_stage)}
              </span>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Renouvellement</div>
              <div className={`text-sm font-bold ${urgencyColor(account.renewal_urgency)}`}>
                {urgencyLabel(account.renewal_urgency)}
              </div>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Expansion</div>
              <div className={`text-sm font-bold ${readinessColor(account.expansion_readiness)}`}>
                {readinessLabel(account.expansion_readiness)}
              </div>
            </div>
          </div>

          {/* Health bar */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-slate-400">Score de santé global</span>
              <span className="text-slate-200 font-medium">{account.overall_health_score}/100</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${healthBarColor(account.overall_health_score)}`}
                style={{ width: `${account.overall_health_score}%` }}
              />
            </div>
          </div>

          {/* Key risks */}
          {account.key_risks.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-3">Risques clés</div>
              <ul className="space-y-2">
                {account.key_risks.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-red-400 mt-0.5 shrink-0">⚠</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Immediate actions */}
          <div>
            <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-3">Actions immédiates</div>
            <ul className="space-y-2">
              {account.immediate_actions.map((a, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-amber-400 mt-0.5 shrink-0">→</span>
                  <span>{a}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Playbook steps */}
          <div>
            <div className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-3">Étapes du playbook</div>
            <ol className="space-y-2">
              {account.playbook_steps.map((s, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-slate-300">
                  <span className="text-indigo-500 font-bold shrink-0 w-4">{i + 1}</span>
                  <span>{s.replace(/^S\d+ : /, "")}</span>
                </li>
              ))}
            </ol>
          </div>

          {/* Success metrics */}
          <div>
            <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-3">Métriques de succès</div>
            <ul className="space-y-2">
              {account.success_metrics.map((m, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-emerald-400 mt-0.5 shrink-0">✓</span>
                  <span>{m}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Account Card ─────────────────────────────────────────────────────────────

function CSCard({ account, onClick }: { account: CSAccount; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 hover:border-slate-600 rounded-2xl p-5 transition-all duration-200 group"
    >
      <div className="flex items-start gap-4">
        <HealthRing score={account.overall_health_score} motion={account.playbook_motion} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${motionColor(account.playbook_motion)}`}>
              {motionLabel(account.playbook_motion)}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${stageBg(account.lifecycle_stage)}`}>
              {stageLabel(account.lifecycle_stage)}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${riskBg(account.risk_level)}`}>
              {account.risk_level === "low" ? "Faible risque" :
               account.risk_level === "medium" ? "Risque moyen" :
               account.risk_level === "high" ? "Risque élevé" : "Critique"}
            </span>
          </div>
          <h3 className="text-sm font-semibold text-slate-100 truncate group-hover:text-indigo-300 transition-colors">
            {account.account_name}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">{fmtEur(account.arr_eur)} ARR</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 text-center">
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Renouvellement</div>
          <div className={`text-sm font-bold ${urgencyColor(account.renewal_urgency)}`}>
            {urgencyLabel(account.renewal_urgency)}
          </div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Expansion</div>
          <div className={`text-sm font-bold ${readinessColor(account.expansion_readiness)}`}>
            {readinessLabel(account.expansion_readiness)}
          </div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Risques</div>
          <div className={`text-sm font-bold ${account.key_risks.length > 0 ? "text-red-400" : "text-emerald-400"}`}>
            {account.key_risks.length}
          </div>
        </div>
      </div>

      {/* Mini health bar */}
      <div className="mt-3">
        <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${healthBarColor(account.overall_health_score)}`}
            style={{ width: `${account.overall_health_score}%` }}
          />
        </div>
      </div>
    </button>
  );
}

// ─── Page ────────────────────────────────────────────────────────────────────

type MotionFilter = "all" | PlaybookMotion;
type RiskFilter = "all" | RiskLevel;

const MOTION_TABS: { id: MotionFilter; label: string }[] = [
  { id: "all", label: "Tous" },
  { id: "rescue", label: "Sauvetage" },
  { id: "retain", label: "Rétention" },
  { id: "expand", label: "Expansion" },
  { id: "accelerate", label: "Accélération" },
  { id: "onboard", label: "Onboarding" },
];

const RISK_TABS: { id: RiskFilter; label: string }[] = [
  { id: "all", label: "Tous risques" },
  { id: "critical", label: "Critique" },
  { id: "high", label: "Élevé" },
  { id: "medium", label: "Moyen" },
  { id: "low", label: "Faible" },
];

export default function CustomerSuccessPlaybookPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [motionFilter, setMotionFilter] = useState<MotionFilter>("all");
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [selected, setSelected] = useState<CSAccount | null>(null);

  const fetchData = useCallback(async (motion: MotionFilter, risk: RiskFilter) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (motion !== "all") params.set("motion", motion);
      if (risk !== "all") params.set("risk", risk);
      const res = await fetch(`/api/customer-success-playbook${params.size ? `?${params}` : ""}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(motionFilter, riskFilter); }, [motionFilter, riskFilter, fetchData]);

  const summary = data?.summary;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {selected && <CSModal account={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-100">Playbook Customer Success</h1>
        <p className="text-slate-400 mt-1 text-sm">Motion CS prescrite par compte — expansion, rétention, sauvetage et activation</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Santé moy.</div>
            <div className="text-2xl font-bold text-sky-400">{summary.avg_health_score}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">ARR à risque</div>
            <div className="text-2xl font-bold text-red-400">{fmtEur(summary.total_arr_at_risk_eur)}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">ARR expansion</div>
            <div className="text-2xl font-bold text-emerald-400">{fmtEur(summary.total_arr_expansion_ready_eur)}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">En sauvetage</div>
            <div className="text-2xl font-bold text-red-400">{summary.rescue_count}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Prêts expansion</div>
            <div className="text-2xl font-bold text-emerald-400">{summary.expand_ready_count}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Renouvellement urgent</div>
            <div className="text-2xl font-bold text-amber-400">{summary.renewal_urgent_count}</div>
          </div>
        </div>
      )}

      {/* Risk distribution bar */}
      {summary && (
        <div className="mb-6 bg-slate-800/30 border border-slate-700/50 rounded-xl p-4">
          <div className="flex justify-between text-xs text-slate-400 mb-2">
            <span>Distribution du risque</span>
            <span>{summary.total} comptes</span>
          </div>
          <RiskDistBar summary={summary} />
          <div className="flex gap-4 mt-2 text-xs flex-wrap">
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block" />
              Faible {summary.risk_counts["low"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-amber-400">
              <span className="w-2 h-2 rounded-full bg-amber-500 inline-block" />
              Moyen {summary.risk_counts["medium"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-orange-400">
              <span className="w-2 h-2 rounded-full bg-orange-500 inline-block" />
              Élevé {summary.risk_counts["high"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-red-400">
              <span className="w-2 h-2 rounded-full bg-red-500 inline-block" />
              Critique {summary.risk_counts["critical"] || 0}
            </span>
          </div>
        </div>
      )}

      {/* Motion filter tabs */}
      <div className="flex gap-2 flex-wrap mb-3">
        {MOTION_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setMotionFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              motionFilter === t.id
                ? "bg-indigo-600 text-white"
                : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}
          >
            {t.label}
            {summary && t.id !== "all" && (
              <span className="ml-1.5 text-xs opacity-70">{summary.motion_counts[t.id] || 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* Risk filter tabs */}
      <div className="flex gap-2 flex-wrap mb-6">
        {RISK_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setRiskFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              riskFilter === t.id
                ? "bg-slate-600 text-white"
                : "bg-slate-800/50 text-slate-500 hover:text-slate-300"
            }`}
          >
            {t.label}
            {summary && t.id !== "all" && (
              <span className="ml-1.5 text-xs opacity-70">{summary.risk_counts[t.id] || 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* Account Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Chargement…</div>
      ) : !data?.accounts.length ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Aucun compte pour ce filtre.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {data.accounts.map((account) => (
            <CSCard key={account.account_id} account={account} onClick={() => setSelected(account)} />
          ))}
        </div>
      )}
    </main>
  );
}
