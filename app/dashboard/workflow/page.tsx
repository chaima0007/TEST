"use client";

import { useEffect, useState } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type DivisionTarget = "1" | "2" | "3" | "4" | "5" | "6";
type WorkflowAction =
  | "send_first_email" | "send_followup_email" | "handle_objection"
  | "schedule_demo" | "send_quote" | "follow_up_quote" | "negotiate"
  | "close" | "generate_invoice" | "enrich_prospect" | "nurture"
  | "archive" | "escalate" | "wait";
type Confidence = "high" | "medium" | "low";

interface WorkflowDecision {
  prospect_id: string;
  company_name: string;
  division: DivisionTarget;
  agent_id: string;
  action: WorkflowAction;
  urgency_score: number;
  confidence: Confidence;
  reasoning: string;
  signals_used: string[];
  created_at: string;
}

interface Summary {
  total: number;
  avg_urgency_score: number;
  division_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  confidence_distribution: Record<string, number>;
}

// ─── Constants ───────────────────────────────────────────────────────────────

const DIVISION_META: Record<DivisionTarget, { name: string; color: string; bg: string }> = {
  "1": { name: "Détection", color: "text-blue-400", bg: "bg-blue-900/40 border-blue-700" },
  "2": { name: "Outreach", color: "text-purple-400", bg: "bg-purple-900/40 border-purple-700" },
  "3": { name: "Négociation", color: "text-amber-400", bg: "bg-amber-900/40 border-amber-700" },
  "4": { name: "Production", color: "text-emerald-400", bg: "bg-emerald-900/40 border-emerald-700" },
  "5": { name: "Finance", color: "text-red-400", bg: "bg-red-900/40 border-red-700" },
  "6": { name: "Branding", color: "text-pink-400", bg: "bg-pink-900/40 border-pink-700" },
};

const ACTION_LABELS: Record<WorkflowAction, string> = {
  send_first_email: "Premier email",
  send_followup_email: "Relance email",
  handle_objection: "Gérer objection",
  schedule_demo: "Planifier démo",
  send_quote: "Envoyer devis",
  follow_up_quote: "Relancer devis",
  negotiate: "Négocier",
  close: "Closing",
  generate_invoice: "Générer facture",
  enrich_prospect: "Enrichir profil",
  nurture: "Nurture",
  archive: "Archiver",
  escalate: "Escalader",
  wait: "Attendre",
};

const ACTION_ICONS: Partial<Record<WorkflowAction, string>> = {
  send_first_email: "✉️", send_followup_email: "🔄", handle_objection: "🛡️",
  schedule_demo: "📅", send_quote: "📄", follow_up_quote: "📬",
  negotiate: "🤝", close: "✅", generate_invoice: "🧾",
  enrich_prospect: "🔍", nurture: "🌱", archive: "🗄️",
  escalate: "⚡", wait: "⏳",
};

const CONFIDENCE_COLORS: Record<Confidence, string> = {
  high: "text-emerald-400",
  medium: "text-yellow-400",
  low: "text-slate-400",
};

const DIVISION_FILTERS = [
  { key: "all", label: "Toutes" },
  { key: "1", label: "Div. 1" },
  { key: "2", label: "Div. 2" },
  { key: "3", label: "Div. 3" },
  { key: "4", label: "Div. 4" },
  { key: "5", label: "Div. 5" },
  { key: "6", label: "Div. 6" },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function DivisionBadge({ div }: { div: DivisionTarget }) {
  const meta = DIVISION_META[div];
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold border ${meta.bg}`}>
      <span className={meta.color}>D{div}</span>
      <span className="text-slate-300">{meta.name}</span>
    </span>
  );
}

function UrgencyBar({ score }: { score: number }) {
  const color =
    score >= 75 ? "bg-red-500"
    : score >= 50 ? "bg-orange-500"
    : score >= 25 ? "bg-yellow-500"
    : "bg-slate-600";
  const textColor =
    score >= 75 ? "text-red-400"
    : score >= 50 ? "text-orange-400"
    : score >= 25 ? "text-yellow-400"
    : "text-slate-400";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className={`text-xs font-bold tabular-nums w-6 text-right ${textColor}`}>{score}</span>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-1">
      <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500">{sub}</p>}
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ decision, onClose }: { decision: WorkflowDecision; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const meta = DIVISION_META[decision.division];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className={`bg-slate-900 border-2 rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 space-y-5 ${meta.bg.includes("border") ? "" : "border-slate-700"}`}
        style={{ borderColor: meta.color.replace("text-", "").replace("-400", "") }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <h2 className="text-white font-bold text-lg">{decision.company_name}</h2>
            <p className="text-slate-400 text-sm">{decision.prospect_id}</p>
          </div>
          <div className="flex flex-col items-end gap-1.5">
            <DivisionBadge div={decision.division} />
            <span className="text-xs text-slate-500">Agent {decision.agent_id}</span>
          </div>
        </div>

        {/* Action */}
        <div className="bg-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 mb-2 uppercase tracking-wider font-semibold">Action</p>
          <p className="text-white font-semibold text-base">
            {ACTION_ICONS[decision.action]} {ACTION_LABELS[decision.action]}
          </p>
        </div>

        {/* Urgency */}
        <div>
          <p className="text-xs text-slate-500 mb-2 font-medium">Score d'urgence</p>
          <UrgencyBar score={decision.urgency_score} />
        </div>

        {/* Confidence */}
        <div className="flex items-center gap-3">
          <p className="text-xs text-slate-500 font-medium">Confiance :</p>
          <span className={`text-sm font-bold ${CONFIDENCE_COLORS[decision.confidence]}`}>
            {decision.confidence.toUpperCase()}
          </span>
        </div>

        {/* Reasoning */}
        <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-4">
          <p className="text-xs text-indigo-400 font-semibold mb-2">Raisonnement</p>
          <p className="text-slate-300 text-sm leading-relaxed">{decision.reasoning}</p>
        </div>

        {/* Signals used */}
        {decision.signals_used.length > 0 && (
          <div>
            <p className="text-xs text-slate-500 mb-2 font-medium">Signaux utilisés</p>
            <div className="flex flex-wrap gap-1">
              {decision.signals_used.map((s) => (
                <span key={s} className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700">
                  {s}
                </span>
              ))}
            </div>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors"
        >
          Fermer
        </button>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function WorkflowPage() {
  const [decisions, setDecisions] = useState<WorkflowDecision[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<WorkflowDecision | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/workflow")
      .then((r) => r.json())
      .then((d) => {
        setDecisions(d.decisions ?? []);
        setSummary(d.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = filter === "all" ? decisions : decisions.filter((d) => d.division === filter);

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Orchestrateur de Workflows</h1>
        <p className="text-slate-400 text-sm mt-1">
          Décisions autonomes — quel agent, quelle action, pourquoi, dans quel ordre
        </p>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <KpiCard label="Décisions" value={summary.total} />
          <KpiCard label="Urgence moy." value={summary.avg_urgency_score} sub="/ 100" accent="text-indigo-400" />
          <KpiCard label="Div. Négociation" value={summary.division_distribution["3"] ?? 0} accent="text-amber-400" />
          <KpiCard label="Div. Outreach" value={summary.division_distribution["2"] ?? 0} accent="text-purple-400" />
          <KpiCard label="Haute confiance" value={summary.confidence_distribution["high"] ?? 0} accent="text-emerald-400" />
          <KpiCard label="En attente" value={summary.action_distribution["wait"] ?? 0} accent="text-slate-400" />
        </div>
      )}

      {/* Division repartition */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Répartition par division
          </h3>
          <div className="flex flex-wrap gap-3">
            {Object.entries(summary.division_distribution)
              .sort(([, a], [, b]) => b - a)
              .map(([div, count]) => {
                const meta = DIVISION_META[div as DivisionTarget];
                if (!meta) return null;
                const total = summary.total;
                const pct = total ? Math.round((count / total) * 100) : 0;
                return (
                  <div
                    key={div}
                    className={`flex items-center gap-3 px-4 py-3 rounded-xl border cursor-pointer transition-all ${meta.bg} ${filter === div ? "ring-2 ring-white/20" : "opacity-80 hover:opacity-100"}`}
                    onClick={() => setFilter(filter === div ? "all" : div)}
                  >
                    <div>
                      <p className={`text-sm font-bold ${meta.color}`}>Division {div} — {meta.name}</p>
                      <p className="text-xs text-slate-400">{count} prospect{count > 1 ? "s" : ""} · {pct}%</p>
                    </div>
                    <span className={`text-2xl font-black tabular-nums ${meta.color}`}>{count}</span>
                  </div>
                );
              })}
          </div>
        </div>
      )}

      {/* Division filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {DIVISION_FILTERS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors border ${
              filter === tab.key
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Decision queue */}
      {loading ? (
        <div className="text-slate-500 text-center py-16">Chargement…</div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-slate-800">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-900/80">
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider w-8">#</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Prospect</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Division</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Agent</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Action</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider min-w-[140px]">Urgence</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Confiance</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((d, i) => (
                <tr
                  key={d.prospect_id}
                  onClick={() => setSelected(d)}
                  className="border-b border-slate-800 hover:bg-slate-800/60 cursor-pointer transition-colors"
                >
                  <td className="px-4 py-3 text-slate-600 text-xs font-mono">{i + 1}</td>
                  <td className="px-4 py-3">
                    <p className="text-white font-medium">{d.company_name}</p>
                    <p className="text-slate-500 text-xs">{d.prospect_id}</p>
                  </td>
                  <td className="px-4 py-3">
                    <DivisionBadge div={d.division} />
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-xs font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-300">
                      Agent {d.agent_id}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-sm text-slate-200">
                      {ACTION_ICONS[d.action]} {ACTION_LABELS[d.action]}
                    </span>
                  </td>
                  <td className="px-4 py-3 min-w-[140px]">
                    <UrgencyBar score={d.urgency_score} />
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-xs font-bold ${CONFIDENCE_COLORS[d.confidence]}`}>
                      {d.confidence.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-4 py-12 text-center text-slate-500">
                    Aucune décision pour cette division.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Action distribution */}
      {summary && Object.keys(summary.action_distribution).length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Actions déclenchées
          </h3>
          <div className="flex flex-wrap gap-2">
            {Object.entries(summary.action_distribution)
              .sort(([, a], [, b]) => b - a)
              .map(([action, count]) => (
                <div
                  key={action}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-sm"
                >
                  <span className="text-slate-300">
                    {ACTION_ICONS[action as WorkflowAction]} {ACTION_LABELS[action as WorkflowAction] ?? action}
                  </span>
                  <span className="font-bold text-white tabular-nums">{count}</span>
                </div>
              ))}
          </div>
        </div>
      )}

      {selected && <DetailModal decision={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
