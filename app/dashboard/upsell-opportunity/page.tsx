"use client";

import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface UpsellEntity {
  id: string;
  client_name: string;
  sector: string;
  current_plan: "essentiel" | "performance" | "premium" | "entreprise";
  current_mrr_eur: number;
  recommended_upgrade: string;
  potential_mrr_eur: number;
  delta_mrr_eur: number;
  months_on_current_plan: number;
  last_upsell_attempt_days: number;
  engagement_signals: number;
  decision_maker_access: boolean;
  upsell_probability: number;
  composite_score: number;
  risk_level: "critique" | "élevé" | "modéré" | "faible";
}

interface UpsellSummary {
  total_opportunities: number;
  avg_current_mrr: number;
  avg_potential_mrr: number;
  total_delta_mrr: number;
  opps_critique: number;
  opps_eleve: number;
  opps_modere: number;
  opps_faible: number;
  top_opportunity_client: string;
  top_opportunity_score: number;
  patterns_detected: string[];
  avg_composite: number;
  avg_estimated_upsell_index: number;
}

interface ApiResponse {
  data?: { entities: UpsellEntity[]; summary: UpsellSummary };
  entities?: UpsellEntity[];
  summary?: UpsellSummary;
}

// ── Colour palettes ───────────────────────────────────────────────────────────

const RISK_META: Record<
  string,
  { label: string; bg: string; text: string; border: string; dot: string }
> = {
  critique: {
    label: "Critique",
    bg: "bg-red-500/15",
    text: "text-red-400",
    border: "border-red-500/30",
    dot: "bg-red-500",
  },
  élevé: {
    label: "Élevé",
    bg: "bg-orange-500/15",
    text: "text-orange-400",
    border: "border-orange-500/30",
    dot: "bg-orange-400",
  },
  modéré: {
    label: "Modéré",
    bg: "bg-yellow-500/15",
    text: "text-yellow-400",
    border: "border-yellow-500/30",
    dot: "bg-yellow-400",
  },
  faible: {
    label: "Faible",
    bg: "bg-slate-600/20",
    text: "text-slate-400",
    border: "border-slate-600/30",
    dot: "bg-slate-500",
  },
};

const PLAN_META: Record<string, { label: string; bg: string; text: string }> = {
  essentiel: { label: "Essentiel", bg: "bg-slate-700", text: "text-slate-300" },
  performance: { label: "Performance", bg: "bg-blue-700", text: "text-blue-200" },
  premium: { label: "Premium", bg: "bg-violet-700", text: "text-violet-200" },
  entreprise: { label: "Entreprise", bg: "bg-emerald-700", text: "text-emerald-200" },
};

// ── Sub-components ────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  sub,
  color = "#6366f1",
}: {
  label: string;
  value: string;
  sub?: string;
  color?: string;
}) {
  return (
    <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
      <p className="text-xs text-slate-400 mb-2 uppercase tracking-wide">{label}</p>
      <p className="text-3xl font-bold" style={{ color }}>
        {value}
      </p>
      {sub && <p className="text-xs text-slate-500 mt-1">{sub}</p>}
    </div>
  );
}

function GaugeRing({
  label,
  value,
  max = 100,
  color = "#6366f1",
}: {
  label: string;
  value: number;
  max?: number;
  color?: string;
}) {
  const pct = Math.min(value / max, 1);
  const r = 42;
  const circ = 2 * Math.PI * r;
  const dash = pct * circ;
  const displayVal = max === 100 ? `${Math.round(value)}%` : value.toFixed(1);

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="100" height="100" viewBox="0 0 100 100">
        {/* Track */}
        <circle
          cx="50"
          cy="50"
          r={r}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth="10"
        />
        {/* Arc */}
        <circle
          cx="50"
          cy="50"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
          style={{ transition: "stroke-dasharray 0.6s ease" }}
        />
        <text
          x="50"
          y="50"
          textAnchor="middle"
          dominantBaseline="central"
          fill="white"
          fontSize="13"
          fontWeight="700"
        >
          {displayVal}
        </text>
      </svg>
      <p className="text-xs text-slate-400 text-center">{label}</p>
    </div>
  );
}

function DistBar({
  label,
  count,
  total,
  color,
}: {
  label: string;
  count: number;
  total: number;
  color: string;
}) {
  const pct = total > 0 ? (count / total) * 100 : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-16 text-right">{label}</span>
      <div className="flex-1 h-4 bg-white/5 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
      <span className="text-xs font-bold text-white w-4 text-left">{count}</span>
    </div>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

function DetailModal({
  entity,
  onClose,
}: {
  entity: UpsellEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const risk = RISK_META[entity.risk_level] ?? RISK_META.faible;
  const plan = PLAN_META[entity.current_plan] ?? PLAN_META.essentiel;

  const actions: string[] = [];
  if (entity.engagement_signals >= 7)
    actions.push("Contacter par téléphone — signal d'engagement très élevé");
  if (entity.decision_maker_access)
    actions.push("Décideur identifié — proposer une démo personnalisée");
  if (entity.months_on_current_plan >= 12)
    actions.push("Client mature — présenter les bénéfices du plan supérieur");
  if (entity.last_upsell_attempt_days >= 60)
    actions.push("Dernière tentative ancienne — relancer avec nouvelle offre");
  if (entity.upsell_probability >= 70)
    actions.push("Probabilité élevée — inclure dans la prochaine campagne upsell");
  if (actions.length === 0)
    actions.push("Maintenir le suivi mensuel standard");

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-lg bg-slate-900 border border-white/10 rounded-2xl shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="px-6 py-4 border-b border-white/8 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-base font-bold text-white">{entity.client_name}</h2>
            <p className="text-xs text-slate-400 mt-0.5">{entity.sector}</p>
          </div>
          <div className="flex items-center gap-2">
            <span
              className={`text-xs font-semibold px-2 py-1 rounded-full ${risk.bg} ${risk.text} border ${risk.border}`}
            >
              {risk.label}
            </span>
            <button
              onClick={onClose}
              className="text-slate-500 hover:text-white transition-colors text-xl leading-none"
            >
              ×
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-white/8">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6">
          {tab === "scores" && (
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Score composite</span>
                <span className="font-bold text-white">{entity.composite_score}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Probabilité upsell</span>
                <span className="font-bold text-white">{entity.upsell_probability}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Plan actuel</span>
                <span className={`text-xs font-semibold px-2 py-0.5 rounded ${plan.bg} ${plan.text}`}>
                  {plan.label}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Upgrade recommandé</span>
                <span className="font-semibold text-indigo-300 capitalize">{entity.recommended_upgrade}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">MRR actuel</span>
                <span className="font-bold text-white">{entity.current_mrr_eur} €</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">MRR potentiel</span>
                <span className="font-bold text-emerald-400">{entity.potential_mrr_eur} €</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Delta MRR</span>
                <span className="font-bold text-emerald-400">+{entity.delta_mrr_eur} €</span>
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Signaux d'engagement</span>
                <span className="font-bold text-white">{entity.engagement_signals}/10</span>
              </div>
              <div className="w-full bg-white/5 rounded-full h-2 overflow-hidden">
                <div
                  className="h-full bg-indigo-500 rounded-full transition-all duration-700"
                  style={{ width: `${(entity.engagement_signals / 10) * 100}%` }}
                />
              </div>
              <div className="flex justify-between text-sm pt-2">
                <span className="text-slate-400">Accès décideur</span>
                <span className={entity.decision_maker_access ? "text-emerald-400 font-bold" : "text-slate-500"}>
                  {entity.decision_maker_access ? "Oui" : "Non"}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Mois sur le plan actuel</span>
                <span className="font-bold text-white">{entity.months_on_current_plan} mois</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Dernière tentative upsell</span>
                <span className="font-bold text-white">
                  {entity.last_upsell_attempt_days > 0
                    ? `Il y a ${entity.last_upsell_attempt_days} jours`
                    : "Aucune"}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Secteur</span>
                <span className="text-white">{entity.sector}</span>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <ul className="space-y-2">
              {actions.map((a, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="mt-0.5 w-4 h-4 rounded-full bg-indigo-600 flex items-center justify-center text-[10px] font-bold text-white flex-shrink-0">
                    {i + 1}
                  </span>
                  {a}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

type FilterLevel = "Tous" | "critique" | "élevé" | "modéré" | "faible";

export default function UpsellOpportunityPage() {
  const [data, setData] = useState<{ entities: UpsellEntity[]; summary: UpsellSummary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<FilterLevel>("Tous");
  const [selected, setSelected] = useState<UpsellEntity | null>(null);

  useEffect(() => {
    fetch("/api/upsell-opportunity")
      .then((r) => r.json())
      .then((resp: ApiResponse) => {
        if (resp.data) {
          setData(resp.data);
        } else if (resp.entities && resp.summary) {
          setData({ entities: resp.entities, summary: resp.summary });
        }
      })
      .finally(() => setLoading(false));
  }, []);

  const entities = data?.entities ?? [];
  const summary = data?.summary;

  const filtered =
    filter === "Tous" ? entities : entities.filter((e) => e.risk_level === filter);

  const filterOptions: FilterLevel[] = ["Tous", "critique", "élevé", "modéré", "faible"];

  // Gauge averages
  const avgUpsellProb =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.upsell_probability, 0) / entities.length
      : 0;
  const avgEngagement =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.engagement_signals, 0) / entities.length
      : 0;
  const accessPct =
    entities.length > 0
      ? (entities.filter((e) => e.decision_maker_access).length / entities.length) * 100
      : 0;
  const avgComposite = summary?.avg_composite ?? 0;

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <p className="text-slate-400 text-sm animate-pulse">
          Chargement des opportunités upsell…
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">
          Opportunités Upsell & Expansion
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Moteur d'intelligence — identification et scoring des opportunités de montée en gamme client
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <KpiCard
          label="Total Opportunités"
          value={String(summary?.total_opportunities ?? entities.length)}
          color="#6366f1"
        />
        <KpiCard
          label="MRR Actuel Moy."
          value={`${summary?.avg_current_mrr ?? "—"} €`}
          sub="par client"
          color="#94a3b8"
        />
        <KpiCard
          label="MRR Potentiel Moy."
          value={`${summary?.avg_potential_mrr ?? "—"} €`}
          sub="après upgrade"
          color="#10b981"
        />
        <KpiCard
          label="Delta MRR Total"
          value={`+${summary?.total_delta_mrr ?? "—"} €`}
          sub="expansion potentielle"
          color="#f59e0b"
        />
        <KpiCard
          label="Opportunités Critiques"
          value={String(summary?.opps_critique ?? 0)}
          sub="priorité maximale"
          color="#ef4444"
        />
        <KpiCard
          label="Score Composite Moy."
          value={summary ? `${summary.avg_composite}/100` : "—"}
          sub={`Index: ${summary?.avg_estimated_upsell_index ?? "—"}/10`}
          color="#a78bfa"
        />
      </div>

      {/* Gauges + Distribution */}
      <div className="grid lg:grid-cols-2 gap-5">
        {/* Gauge rings */}
        <div className="bg-white/3 border border-white/8 rounded-2xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-5">
            Indicateurs de performance
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <GaugeRing
              label="Probabilité Upsell"
              value={avgUpsellProb}
              max={100}
              color="#6366f1"
            />
            <GaugeRing
              label="Engagement Client"
              value={avgEngagement}
              max={10}
              color="#10b981"
            />
            <GaugeRing
              label="Accès Décideur"
              value={accessPct}
              max={100}
              color="#f59e0b"
            />
            <GaugeRing
              label="Score Global"
              value={avgComposite}
              max={100}
              color="#a78bfa"
            />
          </div>
        </div>

        {/* Distribution bars */}
        <div className="bg-white/3 border border-white/8 rounded-2xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-5">
            Distribution par niveau
          </h2>
          <div className="space-y-3">
            <DistBar
              label="Critique"
              count={summary?.opps_critique ?? 0}
              total={entities.length}
              color="#ef4444"
            />
            <DistBar
              label="Élevé"
              count={summary?.opps_eleve ?? 0}
              total={entities.length}
              color="#f97316"
            />
            <DistBar
              label="Modéré"
              count={summary?.opps_modere ?? 0}
              total={entities.length}
              color="#eab308"
            />
            <DistBar
              label="Faible"
              count={summary?.opps_faible ?? 0}
              total={entities.length}
              color="#64748b"
            />
          </div>
          {/* Patterns */}
          <div className="mt-5 pt-4 border-t border-white/8">
            <p className="text-xs text-slate-500 mb-2 uppercase tracking-wide">
              Patterns détectés
            </p>
            <div className="flex flex-wrap gap-1.5">
              {(summary?.patterns_detected ?? []).map((p) => (
                <span
                  key={p}
                  className="text-[11px] px-2 py-0.5 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/20"
                >
                  {p}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {filterOptions.map((f) => {
          const isActive = filter === f;
          const meta = f !== "Tous" ? RISK_META[f] : null;
          return (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`text-sm font-medium px-4 py-1.5 rounded-full border transition-all ${
                isActive
                  ? meta
                    ? `${meta.bg} ${meta.text} ${meta.border}`
                    : "bg-indigo-600 text-white border-indigo-600"
                  : "bg-white/4 text-slate-400 border-white/10 hover:bg-white/8 hover:text-white"
              }`}
            >
              {f === "Tous" ? "Tous" : RISK_META[f]?.label ?? f}
              {f !== "Tous" && (
                <span className="ml-1 opacity-70">
                  (
                  {f === "critique"
                    ? summary?.opps_critique
                    : f === "élevé"
                    ? summary?.opps_eleve
                    : f === "modéré"
                    ? summary?.opps_modere
                    : summary?.opps_faible}
                  )
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Entity cards grid */}
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {filtered.length === 0 && (
          <div className="col-span-full py-10 text-center text-slate-500 text-sm">
            Aucune opportunité pour ce filtre.
          </div>
        )}
        {filtered.map((entity) => {
          const risk = RISK_META[entity.risk_level] ?? RISK_META.faible;
          const plan = PLAN_META[entity.current_plan] ?? PLAN_META.essentiel;
          const upgradePlan = PLAN_META[entity.recommended_upgrade] ?? null;
          return (
            <button
              key={entity.id}
              onClick={() => setSelected(entity)}
              className="text-left bg-white/3 border border-white/8 rounded-2xl p-5 hover:bg-white/6 hover:border-white/15 transition-all group"
            >
              {/* Top row */}
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-white truncate">
                    {entity.client_name}
                  </p>
                  <p className="text-xs text-slate-500 mt-0.5 truncate">{entity.sector}</p>
                </div>
                <span
                  className={`flex-shrink-0 text-xs font-bold px-2 py-1 rounded-full ${risk.bg} ${risk.text} border ${risk.border}`}
                >
                  {risk.label}
                </span>
              </div>

              {/* Plan badges */}
              <div className="flex items-center gap-2 mb-4">
                <span className={`text-[11px] font-semibold px-2 py-0.5 rounded ${plan.bg} ${plan.text}`}>
                  {plan.label}
                </span>
                <span className="text-slate-600 text-xs">→</span>
                {upgradePlan ? (
                  <span className={`text-[11px] font-semibold px-2 py-0.5 rounded ${upgradePlan.bg} ${upgradePlan.text}`}>
                    {upgradePlan.label}
                  </span>
                ) : (
                  <span className="text-xs text-slate-400 capitalize">{entity.recommended_upgrade}</span>
                )}
              </div>

              {/* MRR row */}
              <div className="grid grid-cols-3 gap-2 text-center mb-4">
                <div>
                  <p className="text-[11px] text-slate-500">MRR actuel</p>
                  <p className="text-sm font-bold text-white">{entity.current_mrr_eur} €</p>
                </div>
                <div>
                  <p className="text-[11px] text-slate-500">Potentiel</p>
                  <p className="text-sm font-bold text-emerald-400">{entity.potential_mrr_eur} €</p>
                </div>
                <div>
                  <p className="text-[11px] text-slate-500">Delta</p>
                  <p className="text-sm font-bold text-emerald-400">+{entity.delta_mrr_eur} €</p>
                </div>
              </div>

              {/* Score bar */}
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-[11px] text-slate-500">Score composite</span>
                  <span className="text-[11px] font-bold text-white">
                    {entity.composite_score}/100
                  </span>
                </div>
                <div className="w-full h-1.5 bg-white/8 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${entity.composite_score}%`,
                      backgroundColor:
                        entity.composite_score >= 60
                          ? "#ef4444"
                          : entity.composite_score >= 40
                          ? "#f97316"
                          : entity.composite_score >= 20
                          ? "#eab308"
                          : "#64748b",
                    }}
                  />
                </div>
              </div>

              {/* Bottom row */}
              <div className="flex items-center justify-between mt-3 pt-3 border-t border-white/6">
                <div className="flex items-center gap-1">
                  <span
                    className={`w-2 h-2 rounded-full flex-shrink-0 ${risk.dot}`}
                  />
                  <span className="text-[11px] text-slate-500">
                    {entity.upsell_probability}% prob.
                  </span>
                </div>
                {entity.decision_maker_access && (
                  <span className="text-[11px] text-emerald-400 font-medium">
                    Décideur accessible
                  </span>
                )}
                <span className="text-[11px] text-slate-600 group-hover:text-indigo-400 transition-colors">
                  Voir détails →
                </span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Detail modal */}
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
