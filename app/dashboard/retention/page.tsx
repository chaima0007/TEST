"use client";

import { useEffect, useState } from "react";

type ChurnRisk = "low" | "medium" | "high" | "critical";

interface CustomerSignals {
  customer_id: string;
  name: string;
  company: string;
  sector: string;
  days_since_last_login: number;
  open_support_tickets: number;
  contract_months_remaining: number;
  engagement_trend: number;
  nps_score: number;
  avg_monthly_revenue_eur: number;
  months_as_customer: number;
}

interface ScoreBreakdown {
  login_recency: number;
  support_tickets: number;
  contract_health: number;
  engagement_trend: number;
  nps_score: number;
}

interface RetentionProfile {
  signals: CustomerSignals;
  churn_score: number;
  churn_risk: ChurnRisk;
  ltv_eur: number;
  predicted_months_remaining: number;
  risk_factors: string[];
  retention_actions: string[];
  score_breakdown: ScoreBreakdown;
}

interface Summary {
  total: number;
  risk_counts: Record<ChurnRisk, number>;
  avg_churn_score: number;
  total_ltv_eur: number;
  total_monthly_revenue_eur: number;
  at_risk_revenue_eur: number;
  expiring_soon_count: number;
}

const RISK_STYLES: Record<ChurnRisk, { bg: string; text: string; border: string; bar: string; label: string }> = {
  critical: { bg: "bg-red-900/40",     text: "text-red-300",    border: "border-red-700/60",    bar: "bg-red-500",    label: "CRITIQUE" },
  high:     { bg: "bg-orange-900/40",  text: "text-orange-300", border: "border-orange-700/60", bar: "bg-orange-400", label: "ÉLEVÉ" },
  medium:   { bg: "bg-amber-900/30",   text: "text-amber-300",  border: "border-amber-700/40",  bar: "bg-amber-400",  label: "MOYEN" },
  low:      { bg: "bg-emerald-900/30", text: "text-emerald-300",border: "border-emerald-700/40",bar: "bg-emerald-500",label: "FAIBLE" },
};

const DIM_LABELS: Record<keyof ScoreBreakdown, string> = {
  login_recency:    "Inactivité",
  support_tickets:  "Tickets",
  contract_health:  "Contrat",
  engagement_trend: "Engagement",
  nps_score:        "NPS",
};

function RiskBadge({ risk }: { risk: ChurnRisk }) {
  const s = RISK_STYLES[risk];
  return (
    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${s.bg} ${s.text} ${s.border}`}>
      {s.label}
    </span>
  );
}

function ChurnBar({ label, value }: { label: string; value: number }) {
  const color = value >= 75 ? "bg-red-500" : value >= 55 ? "bg-orange-400" : value >= 35 ? "bg-amber-400" : "bg-emerald-500";
  return (
    <div>
      <div className="flex justify-between text-[10px] text-slate-400 mb-0.5">
        <span>{label}</span>
        <span className="font-mono">{Math.round(value)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function TrendIndicator({ trend }: { trend: number }) {
  const color = trend > 0.3 ? "text-emerald-400" : trend > -0.3 ? "text-amber-400" : "text-red-400";
  const label = trend > 0.3 ? "↑ Croissance" : trend > -0.3 ? "→ Stable" : "↓ Déclin";
  return <span className={`text-[10px] font-medium ${color}`}>{label}</span>;
}

function CustomerModal({ profile, onClose }: { profile: RetentionProfile; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const s = RISK_STYLES[profile.churn_risk];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h2 className="text-lg font-bold text-white">{profile.signals.name}</h2>
              <RiskBadge risk={profile.churn_risk} />
            </div>
            <p className="text-xs text-slate-500">{profile.signals.company} · {profile.signals.sector}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none flex-shrink-0">×</button>
        </div>

        <div className="p-6 space-y-5">
          {/* Churn score */}
          <div className={`rounded-xl p-4 border ${s.bg} ${s.border} text-center`}>
            <p className="text-xs text-slate-400 mb-1">Score de churn</p>
            <p className={`text-4xl font-bold ${s.text}`}>{profile.churn_score}</p>
            <p className="text-xs text-slate-500 mt-1">/100 — plus élevé = plus risqué</p>
          </div>

          {/* LTV & predicted */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-slate-800 rounded-xl p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">LTV prévisionnelle</p>
              <p className="text-lg font-bold text-emerald-400">
                {profile.ltv_eur.toLocaleString("fr-FR")}€
              </p>
            </div>
            <div className="bg-slate-800 rounded-xl p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Mois restants estimés</p>
              <p className="text-lg font-bold text-white">{profile.predicted_months_remaining}</p>
            </div>
          </div>

          {/* Churn breakdown */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Facteurs de risque (score)</p>
            <div className="space-y-2">
              {(Object.entries(profile.score_breakdown) as [keyof ScoreBreakdown, number][]).map(([k, v]) => (
                <ChurnBar key={k} label={DIM_LABELS[k]} value={v} />
              ))}
            </div>
          </div>

          {/* Risk factors */}
          {profile.risk_factors.length > 0 && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Signaux d'alerte</p>
              <ul className="space-y-1.5">
                {profile.risk_factors.map((f, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-red-400 flex-shrink-0 mt-0.5">⚠</span>
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Retention actions */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Actions de rétention</p>
            <ul className="space-y-1.5">
              {profile.retention_actions.map((a, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                  <span className="text-indigo-400 flex-shrink-0 mt-0.5">→</span>
                  {a}
                </li>
              ))}
            </ul>
          </div>

          {/* Raw signals */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Données client</p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              {[
                ["Dernière connexion", `${profile.signals.days_since_last_login}j`],
                ["Tickets ouverts", profile.signals.open_support_tickets],
                ["Mois contrat restants", profile.signals.contract_months_remaining],
                ["NPS", profile.signals.nps_score],
                ["MRR", `${profile.signals.avg_monthly_revenue_eur}€/mois`],
                ["Client depuis", `${profile.signals.months_as_customer} mois`],
              ].map(([k, v]) => (
                <div key={String(k)} className="bg-slate-800 rounded-lg px-3 py-2">
                  <p className="text-slate-500">{k}</p>
                  <p className="text-white font-mono font-medium">{v}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function RetentionPage() {
  const [data, setData] = useState<{ customers: RetentionProfile[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<ChurnRisk | "all">("all");
  const [selected, setSelected] = useState<RetentionProfile | null>(null);

  useEffect(() => {
    fetch("/api/retention")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6 text-slate-500 text-center py-16">Chargement…</div>;
  if (!data) return null;

  const { customers, summary } = data;
  const filtered = riskFilter === "all" ? customers : customers.filter((c) => c.churn_risk === riskFilter);

  const riskTabs: { key: ChurnRisk | "all"; label: string }[] = [
    { key: "all",      label: `Tous (${summary.total})` },
    { key: "critical", label: `Critique (${summary.risk_counts.critical})` },
    { key: "high",     label: `Élevé (${summary.risk_counts.high})` },
    { key: "medium",   label: `Moyen (${summary.risk_counts.medium})` },
    { key: "low",      label: `Faible (${summary.risk_counts.low})` },
  ];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      {selected && <CustomerModal profile={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Rétention Clients</h1>
        <p className="text-slate-400 text-sm mt-1">
          Analyse de churn — inactivité, support, contrat, engagement, NPS
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="Clients actifs" value={summary.total} />
        <KpiCard
          label="MRR total"
          value={`${summary.total_monthly_revenue_eur.toLocaleString("fr-FR")}€`}
          sub="par mois"
          accent="text-emerald-400"
        />
        <KpiCard
          label="Revenus à risque"
          value={`${summary.at_risk_revenue_eur.toLocaleString("fr-FR")}€`}
          sub="churn HIGH + CRITIQUE"
          accent={summary.at_risk_revenue_eur > 0 ? "text-red-400" : "text-white"}
        />
        <KpiCard
          label="LTV totale prévisionnelle"
          value={`${summary.total_ltv_eur.toLocaleString("fr-FR")}€`}
          accent="text-indigo-400"
        />
      </div>

      {/* Alert banner */}
      {summary.expiring_soon_count > 0 && (
        <div className="bg-amber-950/30 border border-amber-800/40 rounded-xl p-4 flex items-center gap-3">
          <span className="text-amber-400 text-lg">⚠</span>
          <p className="text-sm text-amber-300">
            <strong>{summary.expiring_soon_count} contrat{summary.expiring_soon_count > 1 ? "s" : ""}</strong> expirent dans les 3 prochains mois — action de renouvellement requise
          </p>
        </div>
      )}

      {/* Risk filter tabs */}
      <div className="flex flex-wrap gap-2">
        {riskTabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setRiskFilter(t.key)}
            className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
              riskFilter === t.key ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Customer grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        {filtered.map((profile) => {
          const s = RISK_STYLES[profile.churn_risk];
          return (
            <button
              key={profile.signals.customer_id}
              onClick={() => setSelected(profile)}
              className={`w-full text-left bg-slate-900 border rounded-xl p-4 hover:border-slate-600 transition-colors ${
                profile.churn_risk === "critical" ? "border-red-800/60" :
                profile.churn_risk === "high" ? "border-orange-800/40" : "border-slate-800"
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-3">
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5 flex-wrap mb-0.5">
                    <p className="text-sm font-semibold text-white truncate">{profile.signals.name}</p>
                    <RiskBadge risk={profile.churn_risk} />
                  </div>
                  <p className="text-xs text-slate-500 truncate">{profile.signals.company}</p>
                </div>
                <div className="flex-shrink-0 text-right">
                  <p className={`text-2xl font-bold ${s.text}`}>{profile.churn_score}</p>
                  <p className="text-[9px] text-slate-600">churn</p>
                </div>
              </div>

              <div className="space-y-1.5 mb-3">
                {(Object.entries(profile.score_breakdown) as [keyof ScoreBreakdown, number][]).map(([k, v]) => (
                  <ChurnBar key={k} label={DIM_LABELS[k]} value={v} />
                ))}
              </div>

              <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-800">
                <div>
                  <span className="text-slate-500">MRR </span>
                  <span className="text-slate-300 font-medium">{profile.signals.avg_monthly_revenue_eur}€</span>
                  <span className="text-slate-600 ml-2">· </span>
                  <TrendIndicator trend={profile.signals.engagement_trend} />
                </div>
                <span className="text-emerald-400 font-medium text-xs">
                  LTV {profile.ltv_eur.toLocaleString("fr-FR")}€
                </span>
              </div>

              {profile.risk_factors.length > 0 && (
                <p className="text-[10px] text-red-400 mt-2">
                  {profile.risk_factors.length} signal{profile.risk_factors.length > 1 ? "s" : ""} d'alerte
                </p>
              )}
            </button>
          );
        })}
        {filtered.length === 0 && (
          <div className="md:col-span-2 xl:col-span-3 text-center py-12 text-slate-500">
            Aucun client pour ce filtre
          </div>
        )}
      </div>
    </div>
  );
}
