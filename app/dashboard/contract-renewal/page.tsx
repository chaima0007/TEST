"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ──────────────────────────────────────────────────────────────────

type RenewalRisk = "green" | "yellow" | "orange" | "red";
type RenewalAction = "close_renewal" | "accelerate" | "intervene" | "save" | "early_renew";
type UpliftPotential = "high" | "medium" | "low";

interface Contract {
  contract_id: string;
  account_name: string;
  segment: string;
  arr_eur: number;
  days_to_renewal: number;
  renewal_risk: RenewalRisk;
  renewal_action: RenewalAction;
  uplift_potential: UpliftPotential;
  renewal_score: number;
  uplift_score: number;
  recommended_uplift_pct: number;
  churn_signals: string[];
  retention_levers: string[];
  negotiation_tactics: string[];
  timeline_steps: string[];
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  uplift_counts: Record<string, number>;
  avg_renewal_score: number;
  total_arr_at_risk_eur: number;
  total_arr_renewing_eur: number;
  total_potential_uplift_eur: number;
  needs_save_count: number;
  high_uplift_count: number;
}

interface ApiResponse {
  contracts: Contract[];
  summary: Summary;
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function fmtEur(n: number) {
  if (n >= 1_000_000) return `€${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `€${Math.round(n / 1_000)}k`;
  return `€${n}`;
}

function riskColor(r: RenewalRisk) {
  if (r === "green") return "#10b981";
  if (r === "yellow") return "#eab308";
  if (r === "orange") return "#f97316";
  return "#ef4444";
}

function riskBg(r: RenewalRisk) {
  if (r === "green") return "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30";
  if (r === "yellow") return "bg-yellow-500/15 text-yellow-300 border border-yellow-500/30";
  if (r === "orange") return "bg-orange-500/15 text-orange-300 border border-orange-500/30";
  return "bg-red-500/15 text-red-300 border border-red-500/30";
}

function actionBg(a: RenewalAction) {
  if (a === "early_renew") return "bg-emerald-500/20 text-emerald-200";
  if (a === "close_renewal") return "bg-sky-500/20 text-sky-200";
  if (a === "accelerate") return "bg-indigo-500/20 text-indigo-200";
  if (a === "intervene") return "bg-orange-500/20 text-orange-200";
  return "bg-red-500/20 text-red-200";
}

function upliftBg(u: UpliftPotential) {
  if (u === "high") return "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30";
  if (u === "medium") return "bg-amber-500/15 text-amber-300 border border-amber-500/30";
  return "bg-slate-500/15 text-slate-400 border border-slate-500/30";
}

function riskLabel(r: RenewalRisk) {
  if (r === "green") return "Vert";
  if (r === "yellow") return "Jaune";
  if (r === "orange") return "Orange";
  return "Rouge";
}

function actionLabel(a: RenewalAction) {
  if (a === "early_renew") return "Anticiper";
  if (a === "close_renewal") return "Closer";
  if (a === "accelerate") return "Accélérer";
  if (a === "intervene") return "Intervenir";
  return "Sauvetage";
}

function upliftLabel(u: UpliftPotential) {
  if (u === "high") return "Uplift élevé";
  if (u === "medium") return "Uplift moyen";
  return "Uplift faible";
}

function daysColor(d: number) {
  if (d <= 15) return "text-red-400";
  if (d <= 45) return "text-orange-400";
  if (d <= 90) return "text-amber-400";
  return "text-slate-300";
}

// ─── Renewal Ring ─────────────────────────────────────────────────────────────

function RenewalRingComp({ score, risk }: { score: number; risk: RenewalRisk }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;

  return (
    <svg viewBox="0 0 80 80" className="w-20 h-20" aria-hidden="true">
      <circle cx="40" cy="40" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="40"
        cy="40"
        r={r}
        fill="none"
        stroke={riskColor(risk)}
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
  const gr = summary.risk_counts["green"] || 0;
  const ye = summary.risk_counts["yellow"] || 0;
  const or = summary.risk_counts["orange"] || 0;
  const re = summary.risk_counts["red"] || 0;
  return (
    <div className="flex h-2 rounded-full overflow-hidden gap-px bg-slate-800">
      {gr > 0 && <div className="bg-emerald-500 h-full" style={{ width: `${(gr / n) * 100}%` }} />}
      {ye > 0 && <div className="bg-yellow-500 h-full" style={{ width: `${(ye / n) * 100}%` }} />}
      {or > 0 && <div className="bg-orange-500 h-full" style={{ width: `${(or / n) * 100}%` }} />}
      {re > 0 && <div className="bg-red-500 h-full" style={{ width: `${(re / n) * 100}%` }} />}
    </div>
  );
}

// ─── Detail Modal ────────────────────────────────────────────────────────────

function RenewalModal({ contract, onClose }: { contract: Contract; onClose: () => void }) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) { if (e.key === "Escape") onClose(); }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const upliftEur = contract.arr_eur * contract.recommended_uplift_pct / 100;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-100">{contract.account_name}</h2>
            <p className="text-slate-400 text-sm mt-0.5">{contract.segment.toUpperCase()} · ARR {fmtEur(contract.arr_eur)}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 transition-colors text-xl leading-none">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* Summary row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Risque</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${riskBg(contract.renewal_risk)}`}>
                {riskLabel(contract.renewal_risk)}
              </span>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Action</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${actionBg(contract.renewal_action)}`}>
                {actionLabel(contract.renewal_action)}
              </span>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Uplift rec.</div>
              <div className="text-base font-bold text-emerald-400">
                {contract.recommended_uplift_pct > 0 ? `+${contract.recommended_uplift_pct}%` : "0%"}
              </div>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">ARR uplift</div>
              <div className="text-base font-bold text-emerald-400">{fmtEur(upliftEur)}</div>
            </div>
          </div>

          {/* Renewal & uplift scores */}
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400">Score renouvellement</span>
                <span className="text-slate-200 font-medium">{contract.renewal_score}/100</span>
              </div>
              <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${
                    contract.renewal_risk === "green" ? "bg-emerald-500" :
                    contract.renewal_risk === "yellow" ? "bg-yellow-500" :
                    contract.renewal_risk === "orange" ? "bg-orange-500" : "bg-red-500"
                  }`}
                  style={{ width: `${contract.renewal_score}%` }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400">Score uplift</span>
                <span className="text-slate-200 font-medium">{contract.uplift_score}/100</span>
              </div>
              <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${
                    contract.uplift_potential === "high" ? "bg-emerald-500" :
                    contract.uplift_potential === "medium" ? "bg-amber-500" : "bg-slate-500"
                  }`}
                  style={{ width: `${contract.uplift_score}%` }}
                />
              </div>
            </div>
          </div>

          {/* Churn signals */}
          {contract.churn_signals.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-3">Signaux de churn</div>
              <ul className="space-y-2">
                {contract.churn_signals.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-red-400 mt-0.5 shrink-0">⚠</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Retention levers */}
          {contract.retention_levers.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-3">Leviers de rétention</div>
              <ul className="space-y-2">
                {contract.retention_levers.map((l, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-emerald-400 mt-0.5 shrink-0">✓</span>
                    <span>{l}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Negotiation tactics */}
          <div>
            <div className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-3">Tactiques de négociation</div>
            <ul className="space-y-2">
              {contract.negotiation_tactics.map((t, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-indigo-400 mt-0.5 shrink-0">→</span>
                  <span>{t}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Timeline */}
          <div>
            <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-3">Plan d'action</div>
            <ol className="space-y-2">
              {contract.timeline_steps.map((s, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-slate-300">
                  <span className="text-amber-500 font-bold shrink-0 w-4">{i + 1}</span>
                  <span>{s}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Contract Card ────────────────────────────────────────────────────────────

function ContractCard({ contract, onClick }: { contract: Contract; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 hover:border-slate-600 rounded-2xl p-5 transition-all duration-200 group"
    >
      <div className="flex items-start gap-4">
        <RenewalRingComp score={contract.renewal_score} risk={contract.renewal_risk} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${riskBg(contract.renewal_risk)}`}>
              {riskLabel(contract.renewal_risk)}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${actionBg(contract.renewal_action)}`}>
              {actionLabel(contract.renewal_action)}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${upliftBg(contract.uplift_potential)}`}>
              {upliftLabel(contract.uplift_potential)}
            </span>
          </div>
          <h3 className="text-sm font-semibold text-slate-100 truncate group-hover:text-indigo-300 transition-colors">
            {contract.account_name}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">{fmtEur(contract.arr_eur)} ARR</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 text-center">
        <div>
          <div className="text-xs text-slate-500 mb-0.5">J restants</div>
          <div className={`text-sm font-bold ${daysColor(contract.days_to_renewal)}`}>
            {contract.days_to_renewal}j
          </div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Uplift rec.</div>
          <div className="text-sm font-bold text-emerald-400">
            {contract.recommended_uplift_pct > 0 ? `+${contract.recommended_uplift_pct}%` : "—"}
          </div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Signaux churn</div>
          <div className={`text-sm font-bold ${contract.churn_signals.length > 2 ? "text-red-400" : contract.churn_signals.length > 0 ? "text-amber-400" : "text-emerald-400"}`}>
            {contract.churn_signals.length}
          </div>
        </div>
      </div>

      <div className="mt-3">
        <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${
              contract.renewal_risk === "green" ? "bg-emerald-500" :
              contract.renewal_risk === "yellow" ? "bg-yellow-500" :
              contract.renewal_risk === "orange" ? "bg-orange-500" : "bg-red-500"
            }`}
            style={{ width: `${contract.renewal_score}%` }}
          />
        </div>
      </div>
    </button>
  );
}

// ─── Page ────────────────────────────────────────────────────────────────────

type RiskFilter = "all" | RenewalRisk;

const RISK_TABS: { id: RiskFilter; label: string }[] = [
  { id: "all", label: "Tous" },
  { id: "red", label: "Rouge" },
  { id: "orange", label: "Orange" },
  { id: "yellow", label: "Jaune" },
  { id: "green", label: "Vert" },
];

const UPLIFT_TABS: { id: "all" | UpliftPotential; label: string }[] = [
  { id: "all", label: "Tout uplift" },
  { id: "high", label: "Élevé" },
  { id: "medium", label: "Moyen" },
  { id: "low", label: "Faible" },
];

export default function ContractRenewalPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [upliftFilter, setUpliftFilter] = useState<"all" | UpliftPotential>("all");
  const [selected, setSelected] = useState<Contract | null>(null);

  const fetchData = useCallback(async (risk: RiskFilter, uplift: "all" | UpliftPotential) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (risk !== "all") params.set("risk", risk);
      if (uplift !== "all") params.set("uplift", uplift);
      const res = await fetch(`/api/contract-renewal${params.size ? `?${params}` : ""}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(riskFilter, upliftFilter); }, [riskFilter, upliftFilter, fetchData]);

  const summary = data?.summary;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {selected && <RenewalModal contract={selected} onClose={() => setSelected(null)} />}

      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-100">Intelligence Renouvellements</h1>
        <p className="text-slate-400 mt-1 text-sm">Scoring de risque, uplift tarifaire et tactiques de négociation pour chaque contrat</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Score moyen</div>
            <div className="text-2xl font-bold text-sky-400">{summary.avg_renewal_score}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">ARR total</div>
            <div className="text-2xl font-bold text-slate-300">{fmtEur(summary.total_arr_renewing_eur)}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">ARR à risque</div>
            <div className="text-2xl font-bold text-red-400">{fmtEur(summary.total_arr_at_risk_eur)}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Uplift potentiel</div>
            <div className="text-2xl font-bold text-emerald-400">{fmtEur(summary.total_potential_uplift_eur)}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">En sauvetage</div>
            <div className="text-2xl font-bold text-red-400">{summary.needs_save_count}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Uplift élevé</div>
            <div className="text-2xl font-bold text-emerald-400">{summary.high_uplift_count}</div>
          </div>
        </div>
      )}

      {/* Risk distribution bar */}
      {summary && (
        <div className="mb-6 bg-slate-800/30 border border-slate-700/50 rounded-xl p-4">
          <div className="flex justify-between text-xs text-slate-400 mb-2">
            <span>Distribution du risque de renouvellement</span>
            <span>{summary.total} contrats</span>
          </div>
          <RiskDistBar summary={summary} />
          <div className="flex gap-4 mt-2 text-xs flex-wrap">
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block" />
              Vert {summary.risk_counts["green"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-yellow-400">
              <span className="w-2 h-2 rounded-full bg-yellow-500 inline-block" />
              Jaune {summary.risk_counts["yellow"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-orange-400">
              <span className="w-2 h-2 rounded-full bg-orange-500 inline-block" />
              Orange {summary.risk_counts["orange"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-red-400">
              <span className="w-2 h-2 rounded-full bg-red-500 inline-block" />
              Rouge {summary.risk_counts["red"] || 0}
            </span>
          </div>
        </div>
      )}

      {/* Risk filter tabs */}
      <div className="flex gap-2 flex-wrap mb-3">
        {RISK_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setRiskFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              riskFilter === t.id
                ? "bg-indigo-600 text-white"
                : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}
          >
            {t.label}
            {summary && t.id !== "all" && (
              <span className="ml-1.5 text-xs opacity-70">{summary.risk_counts[t.id] || 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* Uplift filter tabs */}
      <div className="flex gap-2 flex-wrap mb-6">
        {UPLIFT_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setUpliftFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              upliftFilter === t.id
                ? "bg-slate-600 text-white"
                : "bg-slate-800/50 text-slate-500 hover:text-slate-300"
            }`}
          >
            {t.label}
            {summary && t.id !== "all" && (
              <span className="ml-1.5 text-xs opacity-70">{summary.uplift_counts[t.id] || 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* Contract Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Chargement…</div>
      ) : !data?.contracts.length ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Aucun contrat pour ce filtre.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {data.contracts.map((contract) => (
            <ContractCard key={contract.contract_id} contract={contract} onClick={() => setSelected(contract)} />
          ))}
        </div>
      )}
    </main>
  );
}
