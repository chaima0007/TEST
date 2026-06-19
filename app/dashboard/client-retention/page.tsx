"use client";

import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type RiskLevel = "critique" | "élevé" | "modéré" | "faible";
type LoyaltyTier = "bronze" | "silver" | "gold" | "platinum";
type ModalTab = "scores" | "signaux" | "actions";

interface ClientEntity {
  id: string;
  name: string;
  sector: string;
  months_active: number;
  contract_value_eur: number;
  last_invoice_days_ago: number;
  missed_meetings: number;
  delayed_payments: number;
  upsell_opportunities: number;
  support_ticket_frequency: number;
  engagement_score: number;
  loyalty_tier: LoyaltyTier;
  renewal_probability: number;
  composite_risk_score: number;
  risk_level: RiskLevel;
}

interface RetentionSummary {
  total_clients: number;
  avg_months_active: number;
  avg_contract_value: number;
  avg_renewal_probability: number;
  clients_critique: number;
  clients_eleve: number;
  clients_modere: number;
  clients_faible: number;
  top_risk_client: string;
  top_risk_score: number;
  patterns_detected: string[];
  avg_composite: number;
  avg_estimated_retention_index: number;
}

interface ApiData {
  data: {
    entities: ClientEntity[];
    summary: RetentionSummary;
  };
  _seal: { ts: string; origin: string; v: number };
}

// ── Constants ─────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; bg: string; dot: string }> = {
  critique: { label: "Critique", color: "text-red-400",    bg: "bg-red-500/10 border-red-500/30",    dot: "bg-red-400"    },
  "élevé":  { label: "Élevé",    color: "text-amber-400",  bg: "bg-amber-500/10 border-amber-500/30",  dot: "bg-amber-400"  },
  modéré:   { label: "Modéré",   color: "text-yellow-400", bg: "bg-yellow-500/10 border-yellow-500/30", dot: "bg-yellow-400" },
  faible:   { label: "Faible",   color: "text-emerald-400",bg: "bg-emerald-500/10 border-emerald-500/30",dot: "bg-emerald-400"},
};

const TIER_META: Record<LoyaltyTier, { label: string; style: string }> = {
  bronze:   { label: "Bronze",   style: "bg-orange-900/40 text-orange-300 border border-orange-700/40"  },
  silver:   { label: "Argent",   style: "bg-slate-700/50 text-slate-300 border border-slate-500/40"     },
  gold:     { label: "Or",       style: "bg-yellow-900/40 text-yellow-300 border border-yellow-700/40"  },
  platinum: { label: "Platine",  style: "bg-cyan-900/40 text-cyan-300 border border-cyan-700/40"        },
};

const FILTER_PILLS: { key: string; label: string }[] = [
  { key: "tous",     label: "Tous"     },
  { key: "critique", label: "Critique" },
  { key: "élevé",   label: "Élevé"    },
  { key: "modéré",  label: "Modéré"   },
  { key: "faible",  label: "Faible"   },
];

const RISK_COLORS: Record<RiskLevel, string> = {
  critique: "#f87171",
  "élevé":  "#fbbf24",
  modéré:   "#facc15",
  faible:   "#34d399",
};

// ── Helpers ───────────────────────────────────────────────────────────────────

function eur(n: number) {
  return `${n.toLocaleString("fr-FR", { maximumFractionDigits: 0 })} €`;
}

function pct(n: number) {
  return `${n}%`;
}

// ── KPI Card ──────────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  sub,
  accent = "#6366f1",
}: {
  label: string;
  value: string;
  sub?: string;
  accent?: string;
}) {
  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-5">
      <p className="text-xs text-slate-400 mb-2 uppercase tracking-wider">{label}</p>
      <p className="text-2xl font-bold" style={{ color: accent }}>
        {value}
      </p>
      {sub && <p className="text-xs text-slate-500 mt-1">{sub}</p>}
    </div>
  );
}

// ── GaugeRing SVG ─────────────────────────────────────────────────────────────

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
  const r = 36;
  const cx = 48;
  const cy = 48;
  const circumference = 2 * Math.PI * r;
  const fillPct = Math.min(value / max, 1);
  const dashOffset = circumference * (1 - fillPct);

  return (
    <div className="flex flex-col items-center gap-2 bg-slate-800/50 border border-slate-700/50 rounded-2xl p-4">
      <svg width={96} height={96} viewBox="0 0 96 96">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={8}
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          strokeLinecap="round"
          transform={`rotate(-90 ${cx} ${cy})`}
        />
        <text
          x={cx}
          y={cy + 5}
          textAnchor="middle"
          fill="white"
          fontSize={16}
          fontWeight="bold"
        >
          {Math.round(value)}
        </text>
      </svg>
      <p className="text-xs text-slate-400 text-center">{label}</p>
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
  const pctWidth = total > 0 ? (count / total) * 100 : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-20 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-slate-700/50 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${pctWidth}%`, backgroundColor: color }}
        />
      </div>
      <span className="text-xs font-mono text-slate-300 w-6 text-right">{count}</span>
    </div>
  );
}

// ── Entity Card ───────────────────────────────────────────────────────────────

function EntityCard({
  entity,
  onClick,
}: {
  entity: ClientEntity;
  onClick: () => void;
}) {
  const risk = RISK_META[entity.risk_level];
  const tier = TIER_META[entity.loyalty_tier];

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/50 border border-slate-700/50 hover:border-slate-500/60 rounded-2xl p-4 transition-all duration-200 group"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-sm text-white truncate group-hover:text-indigo-300 transition-colors">
            {entity.name}
          </p>
          <p className="text-xs text-slate-500 mt-0.5">{entity.sector}</p>
        </div>
        <span className={`ml-2 shrink-0 text-xs px-2 py-0.5 rounded-full border ${tier.style}`}>
          {tier.label}
        </span>
      </div>

      <div className="flex items-center gap-2 mb-3">
        <span className={`w-2 h-2 rounded-full ${risk.dot}`} />
        <span className={`text-xs font-medium ${risk.color}`}>{risk.label}</span>
        <span className="text-xs text-slate-500 ml-auto">
          Score: <span className="font-mono text-slate-300">{entity.composite_risk_score}</span>
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        <div>
          <span className="text-slate-500">Engagement</span>
          <div className="h-1 bg-slate-700 rounded-full mt-1 overflow-hidden">
            <div
              className="h-full bg-indigo-500 rounded-full"
              style={{ width: `${entity.engagement_score}%` }}
            />
          </div>
        </div>
        <div>
          <span className="text-slate-500">Renouvellement</span>
          <div className="h-1 bg-slate-700 rounded-full mt-1 overflow-hidden">
            <div
              className="h-full bg-emerald-500 rounded-full"
              style={{ width: `${entity.renewal_probability}%` }}
            />
          </div>
        </div>
      </div>

      <div className="flex justify-between mt-3 text-xs text-slate-500">
        <span>{entity.months_active} mois actif</span>
        <span>{eur(entity.contract_value_eur)}</span>
      </div>
    </button>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

function DetailModal({
  entity,
  onClose,
}: {
  entity: ClientEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<ModalTab>("scores");
  const risk = RISK_META[entity.risk_level];
  const tier = TIER_META[entity.loyalty_tier];

  const actions: string[] = [];
  if (entity.risk_level === "critique") {
    actions.push("Planifier un appel de récupération urgent avec le responsable compte");
    actions.push("Proposer un audit gratuit de satisfaction client");
    actions.push("Soumettre une offre de fidélisation avec remise de renouvellement");
  } else if (entity.risk_level === "élevé") {
    actions.push("Programmer un point mensuel de suivi régulier");
    actions.push("Envoyer un rapport de valeur personnalisé ce trimestre");
  } else if (entity.risk_level === "modéré") {
    actions.push("Identifier et proposer des opportunités d'upsell adaptées");
    actions.push("Inviter à un webinaire exclusif client");
  } else {
    actions.push("Lancer un programme de parrainage fidélité");
    actions.push("Proposer une extension de contrat à tarif préférentiel");
  }
  if (entity.upsell_opportunities >= 2) {
    actions.push(`Présenter ${entity.upsell_opportunities} opportunités upsell identifiées`);
  }
  if (entity.delayed_payments >= 3) {
    actions.push("Mettre en place un échéancier de paiement structuré");
  }

  const signals: { label: string; value: string; warn: boolean }[] = [
    { label: "Dernière facture",       value: `${entity.last_invoice_days_ago}j`,            warn: entity.last_invoice_days_ago >= 45 },
    { label: "Réunions manquées",      value: String(entity.missed_meetings),                warn: entity.missed_meetings >= 3        },
    { label: "Paiements retardés",     value: String(entity.delayed_payments),               warn: entity.delayed_payments >= 3       },
    { label: "Opportunités upsell",    value: String(entity.upsell_opportunities),           warn: false                              },
    { label: "Fréq. tickets support",  value: `${entity.support_ticket_frequency}/sem`,      warn: entity.support_ticket_frequency > 1},
  ];

  return (
    <div
      className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700/60 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-slate-900 border-b border-slate-700/40 p-5 z-10 flex items-start justify-between">
          <div>
            <h2 className="font-bold text-lg text-white">{entity.name}</h2>
            <div className="flex items-center gap-2 mt-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${tier.style}`}>{tier.label}</span>
              <span className={`text-xs font-medium ${risk.color}`}>{risk.label}</span>
              <span className="text-xs text-slate-500">{entity.id}</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white text-2xl leading-none ml-4 transition-colors"
          >
            ×
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-700/40 px-5">
          {(["scores", "signaux", "actions"] as ModalTab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`py-3 px-4 text-sm capitalize transition-colors border-b-2 -mb-px ${
                tab === t
                  ? "border-indigo-500 text-indigo-400 font-medium"
                  : "border-transparent text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-4">
          {tab === "scores" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Score d'engagement", value: entity.engagement_score, color: "#6366f1" },
                  { label: "Prob. renouvellement", value: entity.renewal_probability, color: "#10b981" },
                  { label: "Risque composite", value: entity.composite_risk_score, color: RISK_COLORS[entity.risk_level] },
                  { label: "Ancienneté (mois)", value: entity.months_active, max: 60, color: "#8b5cf6" },
                ].map((g) => (
                  <GaugeRing
                    key={g.label}
                    label={g.label}
                    value={g.value}
                    max={g.max ?? 100}
                    color={g.color}
                  />
                ))}
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4 text-sm space-y-2">
                <div className="flex justify-between">
                  <span className="text-slate-400">Valeur contrat</span>
                  <span className="text-white font-semibold">{eur(entity.contract_value_eur)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Secteur</span>
                  <span className="text-slate-300">{entity.sector}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Niveau de risque</span>
                  <span className={`font-medium ${risk.color}`}>{risk.label}</span>
                </div>
              </div>
            </>
          )}

          {tab === "signaux" && (
            <div className="space-y-3">
              {signals.map((s) => (
                <div
                  key={s.label}
                  className={`flex items-center justify-between rounded-xl p-3 border ${
                    s.warn
                      ? "bg-red-500/5 border-red-500/20"
                      : "bg-slate-800/40 border-slate-700/30"
                  }`}
                >
                  <span className="text-sm text-slate-400">{s.label}</span>
                  <span
                    className={`text-sm font-mono font-semibold ${
                      s.warn ? "text-red-400" : "text-slate-200"
                    }`}
                  >
                    {s.value}
                  </span>
                </div>
              ))}
              <div className="bg-slate-800/40 border border-slate-700/30 rounded-xl p-3">
                <p className="text-xs text-slate-500 mb-1">Opps. upsell ignorées</p>
                <div className="flex gap-1 flex-wrap">
                  {Array.from({ length: entity.upsell_opportunities }).map((_, i) => (
                    <span
                      key={i}
                      className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs px-2 py-0.5 rounded-full"
                    >
                      Upsell #{i + 1}
                    </span>
                  ))}
                  {entity.upsell_opportunities === 0 && (
                    <span className="text-xs text-slate-500 italic">Aucune détectée</span>
                  )}
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              {actions.map((action, i) => (
                <div
                  key={i}
                  className="flex items-start gap-3 bg-slate-800/40 border border-slate-700/30 rounded-xl p-3"
                >
                  <span className="shrink-0 w-5 h-5 rounded-full bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 text-xs flex items-center justify-center font-bold mt-0.5">
                    {i + 1}
                  </span>
                  <p className="text-sm text-slate-300">{action}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function ClientRetentionPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<ClientEntity | null>(null);

  useEffect(() => {
    fetch("/api/client-retention")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<ApiData>;
      })
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch((e: unknown) => {
        setError(e instanceof Error ? e.message : "Erreur inconnue");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-sm animate-pulse">Chargement de l&apos;intelligence rétention...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-sm">Erreur : {error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const { entities, summary } = data.data;

  const filtered =
    filter === "tous" ? entities : entities.filter((e) => e.risk_level === filter);

  const totalClients = summary.total_clients;

  // Gauges
  const avgEngagement =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.engagement_score, 0) / entities.length
      : 0;
  const avgPaymentRisk =
    entities.length > 0
      ? Math.max(0, 100 - (entities.reduce((s, e) => s + e.delayed_payments, 0) / entities.length) * 10)
      : 100;

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6 space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Rétention Client & Fidélisation</h1>
        <p className="text-slate-400 text-sm mt-1">
          Intelligence Swarm — Caelum Partners · {totalClients} clients actifs analysés
        </p>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <KpiCard
          label="Total Clients"
          value={String(summary.total_clients)}
          sub="Portefeuille actif"
          accent="#6366f1"
        />
        <KpiCard
          label="Ancienneté Moy."
          value={`${summary.avg_months_active} mois`}
          sub="Durée moyenne de contrat"
          accent="#8b5cf6"
        />
        <KpiCard
          label="Valeur Contrat Moy."
          value={eur(summary.avg_contract_value)}
          sub="Valeur annuelle moyenne"
          accent="#10b981"
        />
        <KpiCard
          label="Prob. Renouvellement"
          value={pct(summary.avg_renewal_probability)}
          sub="Probabilité moyenne"
          accent="#34d399"
        />
        <KpiCard
          label="Clients Critiques"
          value={String(summary.clients_critique)}
          sub={`Sur ${summary.total_clients} clients`}
          accent="#f87171"
        />
        <KpiCard
          label="Score Composite Moy."
          value={String(summary.avg_composite)}
          sub={`Index rétention: ${summary.avg_estimated_retention_index}/10`}
          accent="#fbbf24"
        />
      </div>

      {/* 4 GaugeRings */}
      <section>
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
          Indicateurs clés
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <GaugeRing
            label="Engagement Moyen"
            value={Math.round(avgEngagement)}
            color="#6366f1"
          />
          <GaugeRing
            label="Renouvellement Moy."
            value={summary.avg_renewal_probability}
            color="#10b981"
          />
          <GaugeRing
            label="Santé Paiement"
            value={Math.round(avgPaymentRisk)}
            color="#f59e0b"
          />
          <GaugeRing
            label="Rétention Globale"
            value={summary.avg_estimated_retention_index}
            max={10}
            color="#8b5cf6"
          />
        </div>
      </section>

      {/* 4 DistBars */}
      <section>
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
          Distribution par niveau de risque
        </h2>
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-5 space-y-3">
          <DistBar label="Critique" count={summary.clients_critique} total={totalClients} color="#f87171" />
          <DistBar label="Élevé"    count={summary.clients_eleve}   total={totalClients} color="#fbbf24" />
          <DistBar label="Modéré"   count={summary.clients_modere}  total={totalClients} color="#facc15" />
          <DistBar label="Faible"   count={summary.clients_faible}  total={totalClients} color="#34d399" />
        </div>
      </section>

      {/* Patterns detected */}
      {summary.patterns_detected.length > 0 && (
        <section>
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Patterns détectés
          </h2>
          <div className="flex flex-wrap gap-2">
            {summary.patterns_detected.map((p) => (
              <span
                key={p}
                className="bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-xs px-3 py-1 rounded-full"
              >
                {p}
              </span>
            ))}
          </div>
        </section>
      )}

      {/* Entity grid with filter pills */}
      <section>
        <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
            Clients ({filtered.length})
          </h2>
          <div className="flex gap-2 flex-wrap">
            {FILTER_PILLS.map((pill) => (
              <button
                key={pill.key}
                onClick={() => setFilter(pill.key)}
                className={`text-xs px-3 py-1.5 rounded-full border transition-all ${
                  filter === pill.key
                    ? "bg-indigo-600 border-indigo-500 text-white"
                    : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500 hover:text-slate-200"
                }`}
              >
                {pill.label}
              </button>
            ))}
          </div>
        </div>

        {filtered.length === 0 ? (
          <p className="text-slate-500 text-sm italic">Aucun client pour ce filtre.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((entity) => (
              <EntityCard
                key={entity.id}
                entity={entity}
                onClick={() => setSelected(entity)}
              />
            ))}
          </div>
        )}
      </section>

      {/* Detail Modal */}
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
