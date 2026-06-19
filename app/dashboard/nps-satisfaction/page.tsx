"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface ClientEntity {
  id: string;
  name: string;
  sector: string;
  nps_score: number;
  satisfaction_level: number;
  churn_risk: number;
  response_time_days: number;
  last_contact_date: string;
  total_spent_eur: number;
  project_count: number;
  support_tickets: number;
  recommendation_likelihood: number;
  contract_renewal_months: number;
  composite_risk_score: number;
  risk_level: string;
}

interface NPSSummary {
  total_clients: number;
  avg_nps: number;
  avg_satisfaction: number;
  avg_churn_risk: number;
  clients_critique: number;
  clients_eleve: number;
  clients_modere: number;
  clients_faible: number;
  top_risk_client: string;
  top_risk_score: number;
  patterns_detected: number;
  avg_composite: number;
  avg_estimated_satisfaction_index: number;
}

interface NPSData {
  entities: ClientEntity[];
  summary: NPSSummary;
}

// ── Risk level helpers ────────────────────────────────────────────────────────

const RISK_CONFIG: Record<string, { label: string; color: string; bg: string; border: string; dot: string }> = {
  critique: {
    label: "Critique",
    color: "text-red-400",
    bg: "bg-red-500/10",
    border: "border-red-500/25",
    dot: "bg-red-500",
  },
  "élevé": {
    label: "Élevé",
    color: "text-orange-400",
    bg: "bg-orange-500/10",
    border: "border-orange-500/25",
    dot: "bg-orange-500",
  },
  "modéré": {
    label: "Modéré",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    border: "border-amber-500/25",
    dot: "bg-amber-500",
  },
  faible: {
    label: "Faible",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    border: "border-emerald-500/25",
    dot: "bg-emerald-500",
  },
};

const FILTER_OPTIONS = [
  { key: "all", label: "Tous" },
  { key: "critique", label: "Critique" },
  { key: "élevé", label: "Élevé" },
  { key: "modéré", label: "Modéré" },
  { key: "faible", label: "Faible" },
];

// ── GaugeRing (inline SVG, no lib) ───────────────────────────────────────────

function GaugeRing({
  value,
  max,
  label,
  color,
  invert = false,
}: {
  value: number;
  max: number;
  label: string;
  color: string;
  invert?: boolean;
}) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const displayPct = invert ? 100 - pct : pct;
  const r = 36;
  const circ = 2 * Math.PI * r;
  const offset = circ - (displayPct / 100) * circ;

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="8" />
        <circle
          cx="48"
          cy="48"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          transform="rotate(-90 48 48)"
          style={{ transition: "stroke-dashoffset 0.7s ease" }}
        />
        <text
          x="48"
          y="52"
          textAnchor="middle"
          fontSize="14"
          fontWeight="700"
          fill="white"
        >
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-gray-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

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
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-gray-300">{label}</span>
        <span className="text-gray-400">
          {count} <span className="text-gray-600">({pct}%)</span>
        </span>
      </div>
      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

// ── KPI Card ──────────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  sub,
  accent,
}: {
  label: string;
  value: string | number;
  sub?: string;
  accent?: string;
}) {
  return (
    <div className="bg-white/4 border border-white/10 rounded-xl px-5 py-4 hover:bg-white/6 transition-colors">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Client Card ───────────────────────────────────────────────────────────────

function ClientCard({
  client,
  onClick,
}: {
  client: ClientEntity;
  onClick: (c: ClientEntity) => void;
}) {
  const cfg = RISK_CONFIG[client.risk_level] ?? RISK_CONFIG.faible;

  return (
    <button
      onClick={() => onClick(client)}
      className={`w-full text-left bg-white/4 border ${cfg.border} rounded-xl p-4 hover:bg-white/7 transition-all`}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="min-w-0">
          <p className="font-semibold text-white truncate">{client.name}</p>
          <p className="text-xs text-gray-400 truncate mt-0.5">{client.sector}</p>
        </div>
        <span
          className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}
        >
          {cfg.label}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{client.nps_score.toFixed(1)}</p>
          <p className="text-[10px] text-gray-500">NPS</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{client.satisfaction_level}%</p>
          <p className="text-[10px] text-gray-500">Satisfaction</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{client.churn_risk}%</p>
          <p className="text-[10px] text-gray-500">Churn</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">
          Score composite:{" "}
          <span className={`font-bold ${cfg.color}`}>{client.composite_risk_score}</span>
        </span>
        <span className="text-gray-500">{client.project_count} projets</span>
      </div>
    </button>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────

const PATTERNS = [
  {
    id: "P1",
    name: "Décrochage NPS",
    severity: "critique",
    description: "NPS inférieur à 5 combiné à une satisfaction en chute — risque de désabonnement imminent.",
    action: "Appel de rétention sous 48h par le responsable de compte senior.",
    signal: "nps_score < 5",
    test: (c: ClientEntity) => c.nps_score < 5,
  },
  {
    id: "P2",
    name: "Churn Risk Élevé",
    severity: "élevé",
    description: "Score de churn supérieur à 70 — le client évalue activement des alternatives concurrentes.",
    action: "Proposer un audit gratuit et une offre de renouvellement anticipé avec remise fidélité.",
    signal: "churn_risk > 70",
    test: (c: ClientEntity) => c.churn_risk > 70,
  },
  {
    id: "P3",
    name: "Surcharge Support",
    severity: "élevé",
    description: "Volume de tickets support anormalement élevé indiquant des frictions produit répétées.",
    action: "Session de formation dédiée + escalade vers l'équipe technique pour correction durable.",
    signal: "support_tickets ≥ 7",
    test: (c: ClientEntity) => c.support_tickets >= 7,
  },
  {
    id: "P4",
    name: "Silence Prolongé",
    severity: "modéré",
    description: "Aucun contact depuis plus de 60 jours — le client se désengage silencieusement.",
    action: "Envoyer un rapport de valeur personnalisé et planifier un check-in trimestriel.",
    signal: "response_time_days > 60",
    test: (c: ClientEntity) => c.response_time_days > 60,
  },
  {
    id: "P5",
    name: "Faible Recommandation",
    severity: "modéré",
    description: "Probabilité de recommandation inférieure à 40 — le client ne génère pas de bouche-à-oreille positif.",
    action: "Programme ambassadeur + cas client co-rédigé pour renforcer l'engagement.",
    signal: "recommendation_likelihood < 40",
    test: (c: ClientEntity) => c.recommendation_likelihood < 40,
  },
];

const SEVERITY_STYLE: Record<string, string> = {
  critique: "text-red-400 bg-red-500/10 border-red-500/25",
  "élevé": "text-orange-400 bg-orange-500/10 border-orange-500/25",
  "modéré": "text-amber-400 bg-amber-500/10 border-amber-500/25",
};

function DetailModal({
  client,
  onClose,
}: {
  client: ClientEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const cfg = RISK_CONFIG[client.risk_level] ?? RISK_CONFIG.faible;
  const triggered = PATTERNS.filter((p) => p.test(client));

  const TABS = [
    { key: "scores", label: "Scores" },
    { key: "signaux", label: "Signaux" },
    { key: "actions", label: "Actions" },
  ] as const;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="w-full max-w-xl bg-slate-900 border border-white/12 rounded-2xl shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="px-6 pt-6 pb-4 border-b border-white/8">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-white">{client.name}</h2>
              <p className="text-sm text-gray-400 mt-0.5">{client.sector}</p>
            </div>
            <div className="flex items-center gap-2">
              <span
                className={`text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}
              >
                {cfg.label}
              </span>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-white transition-colors ml-1"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
              </button>
            </div>
          </div>

          {/* Tab bar */}
          <div className="flex gap-1 mt-4">
            {TABS.map((t) => (
              <button
                key={t.key}
                onClick={() => setTab(t.key)}
                className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  tab === t.key
                    ? "bg-white/10 text-white"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Body */}
        <div className="px-6 py-5 space-y-4 max-h-[60vh] overflow-y-auto">

          {/* ── TAB: Scores ── */}
          {tab === "scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "NPS Score", value: `${client.nps_score}/10` },
                  { label: "Satisfaction", value: `${client.satisfaction_level}%` },
                  { label: "Risque Churn", value: `${client.churn_risk}%` },
                  { label: "Recommandation", value: `${client.recommendation_likelihood}%` },
                  { label: "Tickets support", value: client.support_tickets },
                  { label: "Délai réponse", value: `${client.response_time_days}j` },
                  { label: "Projets réalisés", value: client.project_count },
                  { label: "Dépenses totales", value: `${(client.total_spent_eur / 1000).toFixed(0)}k €` },
                  { label: "Renouvellement", value: `${client.contract_renewal_months} mois` },
                  { label: "Dernier contact", value: client.last_contact_date },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                    <p className="text-sm font-semibold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-white/4 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-300">Score Composite de Risque</span>
                  <span className={`text-xl font-bold ${cfg.color}`}>
                    {client.composite_risk_score}
                  </span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${Math.min(100, client.composite_risk_score)}%`,
                      backgroundColor:
                        client.risk_level === "critique"
                          ? "#f87171"
                          : client.risk_level === "élevé"
                          ? "#fb923c"
                          : client.risk_level === "modéré"
                          ? "#fbbf24"
                          : "#34d399",
                    }}
                  />
                </div>
                <p className="text-[11px] text-gray-500 mt-1.5">
                  Formule : churn×0.35 + (100−NPS×10)×0.30 + (100−sat)×0.25 + (tickets/10×100)×0.10
                </p>
              </div>
            </div>
          )}

          {/* ── TAB: Signaux ── */}
          {tab === "signaux" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="text-center py-8 text-gray-400 text-sm">
                  Aucun signal d&apos;alerte détecté — client sain
                </div>
              ) : (
                triggered.map((p) => (
                  <div
                    key={p.id}
                    className={`rounded-xl border p-4 ${SEVERITY_STYLE[p.severity] ?? ""}`}
                  >
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className="text-xs font-mono opacity-60">{p.id}</span>
                      <span className="font-semibold text-sm">{p.name}</span>
                      <span className="ml-auto text-[10px] font-medium uppercase tracking-wide opacity-70">
                        {p.severity}
                      </span>
                    </div>
                    <p className="text-xs leading-relaxed opacity-80">{p.description}</p>
                    <p className="text-[10px] font-mono opacity-50 mt-1.5">Signal : {p.signal}</p>
                  </div>
                ))
              )}

              {triggered.length === 0 && (
                <div className="mt-2 bg-emerald-500/10 border border-emerald-500/25 rounded-xl p-4">
                  <p className="text-emerald-400 text-sm font-medium">Client satisfait</p>
                  <p className="text-xs text-emerald-400/70 mt-1">
                    NPS {client.nps_score}/10 · Satisfaction {client.satisfaction_level}% ·
                    Churn {client.churn_risk}%
                  </p>
                </div>
              )}
            </div>
          )}

          {/* ── TAB: Actions ── */}
          {tab === "actions" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                  <p className="text-sm text-gray-300 font-medium">Plan de fidélisation</p>
                  <p className="text-xs text-gray-400 mt-1.5 leading-relaxed">
                    Client en bonne santé — maintenir la relation via un check-in trimestriel et
                    explorer les opportunités d&apos;upsell.
                  </p>
                </div>
              ) : (
                triggered.map((p, i) => (
                  <div key={p.id} className="bg-white/4 border border-white/10 rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-6 h-6 rounded-full bg-white/10 text-xs flex items-center justify-center text-gray-300 font-bold">
                        {i + 1}
                      </span>
                      <span className="text-sm font-medium text-white">{p.name}</span>
                    </div>
                    <p className="text-xs text-gray-300 leading-relaxed">{p.action}</p>
                  </div>
                ))
              )}

              <div className="bg-slate-800/60 border border-white/8 rounded-xl p-4">
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Renouvellement prévu :</span>{" "}
                  dans {client.contract_renewal_months} mois
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  <span className="text-gray-300 font-medium">Valeur client :</span>{" "}
                  {(client.total_spent_eur / 1000).toFixed(0)}k € investis sur {client.project_count} projets
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function NPSSatisfactionPage() {
  const [data, setData] = useState<NPSData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<ClientEntity | null>(null);

  useEffect(() => {
    fetch("/api/nps-satisfaction")
      .then((r) => r.json())
      .then((json) => {
        // Handle sealResponse wrapper
        const payload = json?.data ?? json;
        setData(payload as NPSData);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const s = data?.summary;
  const entities = data?.entities ?? [];

  const filtered =
    filter === "all" ? entities : entities.filter((c) => c.risk_level === filter);

  const totalClients = s?.total_clients ?? 0;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        {/* ── Page header ── */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Satisfaction Client & NPS</h1>
            <p className="text-sm text-gray-400 mt-1">
              Moteur d&apos;intelligence Swarm — analyse des risques de churn et de la fidélité client
            </p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {totalClients} clients analysés
          </span>
        </div>

        {/* ── Loading ── */}
        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && s && (
          <>
            {/* ── KPI Cards ── */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              <KpiCard
                label="Total Clients"
                value={s.total_clients}
                sub="portefeuille actif"
              />
              <KpiCard
                label="NPS Moyen"
                value={`${s.avg_nps}/10`}
                sub={s.avg_nps >= 7 ? "Promoteurs" : s.avg_nps >= 5 ? "Passifs" : "Détracteurs"}
                accent={s.avg_nps >= 7 ? "text-emerald-400" : s.avg_nps >= 5 ? "text-amber-400" : "text-red-400"}
              />
              <KpiCard
                label="Satisfaction Moyenne"
                value={`${s.avg_satisfaction}%`}
                sub="indice agrégé"
                accent={s.avg_satisfaction >= 70 ? "text-emerald-400" : s.avg_satisfaction >= 50 ? "text-amber-400" : "text-red-400"}
              />
              <KpiCard
                label="Risque Churn Moyen"
                value={`${s.avg_churn_risk}%`}
                sub="probabilité attrition"
                accent={s.avg_churn_risk >= 60 ? "text-red-400" : s.avg_churn_risk >= 40 ? "text-orange-400" : "text-emerald-400"}
              />
              <KpiCard
                label="Clients à Risque Critique"
                value={s.clients_critique}
                sub="action immédiate requise"
                accent="text-red-400"
              />
              <KpiCard
                label="Taux de Renouvellement"
                value={`${Math.round((s.clients_faible + s.clients_modere) / s.total_clients * 100)}%`}
                sub="clients stables ou sûrs"
                accent="text-indigo-400"
              />
            </div>

            {/* ── Gauges + Distribution ── */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

              {/* Gauges */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs Clés</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing
                    value={s.avg_nps}
                    max={10}
                    label="NPS Score"
                    color="#818cf8"
                  />
                  <GaugeRing
                    value={s.avg_satisfaction}
                    max={100}
                    label="Satisfaction"
                    color="#34d399"
                  />
                  <GaugeRing
                    value={s.avg_churn_risk}
                    max={100}
                    label="Churn Risk"
                    color="#f87171"
                  />
                  <GaugeRing
                    value={s.avg_composite}
                    max={100}
                    label="Risque Composite"
                    color="#fb923c"
                  />
                </div>
              </div>

              {/* Distribution bars */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">
                  Distribution par Niveau de Risque
                </h2>
                <div className="space-y-4">
                  <DistBar
                    label="Critique"
                    count={s.clients_critique}
                    total={s.total_clients}
                    color="#f87171"
                  />
                  <DistBar
                    label="Élevé"
                    count={s.clients_eleve}
                    total={s.total_clients}
                    color="#fb923c"
                  />
                  <DistBar
                    label="Modéré"
                    count={s.clients_modere}
                    total={s.total_clients}
                    color="#fbbf24"
                  />
                  <DistBar
                    label="Faible"
                    count={s.clients_faible}
                    total={s.total_clients}
                    color="#34d399"
                  />
                </div>

                <div className="mt-5 pt-4 border-t border-white/8 grid grid-cols-2 gap-3">
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Patterns détectés</p>
                    <p className="text-lg font-bold text-white mt-0.5">{s.patterns_detected} / 5</p>
                  </div>
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Index Satisfaction ESI</p>
                    <p className="text-lg font-bold text-indigo-400 mt-0.5">
                      {s.avg_estimated_satisfaction_index}/10
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* ── Filter pills ── */}
            <div className="flex flex-wrap gap-2">
              {FILTER_OPTIONS.map((opt) => {
                const isActive = filter === opt.key;
                const cfg = opt.key !== "all" ? RISK_CONFIG[opt.key] : null;
                return (
                  <button
                    key={opt.key}
                    onClick={() => setFilter(opt.key)}
                    className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                      isActive
                        ? cfg
                          ? `${cfg.bg} ${cfg.border} ${cfg.color}`
                          : "bg-white/10 border-white/20 text-white"
                        : "bg-transparent border-white/10 text-gray-400 hover:text-white hover:border-white/20"
                    }`}
                  >
                    {opt.label}
                    {opt.key === "critique" && (
                      <span className="ml-1.5 text-xs opacity-70">{s.clients_critique}</span>
                    )}
                    {opt.key === "élevé" && (
                      <span className="ml-1.5 text-xs opacity-70">{s.clients_eleve}</span>
                    )}
                    {opt.key === "modéré" && (
                      <span className="ml-1.5 text-xs opacity-70">{s.clients_modere}</span>
                    )}
                    {opt.key === "faible" && (
                      <span className="ml-1.5 text-xs opacity-70">{s.clients_faible}</span>
                    )}
                    {opt.key === "all" && (
                      <span className="ml-1.5 text-xs opacity-70">{s.total_clients}</span>
                    )}
                  </button>
                );
              })}
            </div>

            {/* ── Client cards grid ── */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filtered.map((client) => (
                <ClientCard key={client.id} client={client} onClick={setSelected} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400 text-sm">
                  Aucun client dans ce niveau de risque
                </div>
              )}
            </div>

            {/* ── Alert strip for top risk ── */}
            {s.clients_critique > 0 && (
              <div className="bg-red-500/8 border border-red-500/20 rounded-xl px-5 py-4 flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0 animate-pulse" />
                <div>
                  <p className="text-sm font-medium text-red-400">
                    {s.clients_critique} client{s.clients_critique > 1 ? "s" : ""} en situation critique
                  </p>
                  <p className="text-xs text-red-400/70 mt-0.5">
                    Client le plus à risque :{" "}
                    <span className="font-medium">{s.top_risk_client}</span> — score composite{" "}
                    {s.top_risk_score}/100
                  </p>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* ── Detail Modal ── */}
      {selected && (
        <DetailModal client={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
