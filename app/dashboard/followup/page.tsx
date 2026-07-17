"use client";

import { useEffect, useState } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type Priority = "urgent" | "high" | "medium" | "low";
type ActionType =
  | "call"
  | "email"
  | "demo"
  | "send_quote"
  | "follow_quote"
  | "negotiate"
  | "check_in"
  | "close"
  | "skip";

interface FollowUpTask {
  prospect_id: string;
  company_name: string;
  sector: string;
  current_stage: string;
  urgency_score: number;
  priority: Priority;
  recommended_action: ActionType;
  days_since_contact: number;
  bant_score: number;
  touches: number;
  quote_value: number;
  notes: string;
  created_at: string;
}

interface Summary {
  total: number;
  urgent: number;
  high: number;
  medium: number;
  low: number;
  avg_urgency_score: number;
  overdue_7d: number;
  overdue_14d: number;
  total_pipeline_eur: number;
  action_breakdown: Record<string, number>;
}

// ─── Constants ───────────────────────────────────────────────────────────────

const PRIORITY_COLORS: Record<Priority, string> = {
  urgent: "bg-red-500 text-white",
  high: "bg-orange-500 text-white",
  medium: "bg-yellow-500 text-white",
  low: "bg-slate-500 text-white",
};

const PRIORITY_RING: Record<Priority, string> = {
  urgent: "ring-red-500",
  high: "ring-orange-500",
  medium: "ring-yellow-500",
  low: "ring-slate-600",
};

const PRIORITY_SCORE_COLOR: Record<Priority, string> = {
  urgent: "text-red-400",
  high: "text-orange-400",
  medium: "text-yellow-400",
  low: "text-slate-400",
};

const ACTION_LABELS: Record<ActionType, string> = {
  call: "Appeler",
  email: "Envoyer email",
  demo: "Planifier démo",
  send_quote: "Envoyer devis",
  follow_quote: "Relancer devis",
  negotiate: "Négocier",
  check_in: "Check-in léger",
  close: "Closing",
  skip: "Ignorer",
};

const ACTION_COLORS: Record<ActionType, string> = {
  call: "bg-green-900/60 text-green-300 border-green-700",
  email: "bg-indigo-900/60 text-indigo-300 border-indigo-700",
  demo: "bg-purple-900/60 text-purple-300 border-purple-700",
  send_quote: "bg-cyan-900/60 text-cyan-300 border-cyan-700",
  follow_quote: "bg-blue-900/60 text-blue-300 border-blue-700",
  negotiate: "bg-amber-900/60 text-amber-300 border-amber-700",
  check_in: "bg-slate-800 text-slate-300 border-slate-600",
  close: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
  skip: "bg-slate-900 text-slate-500 border-slate-700",
};

const STAGE_LABELS: Record<string, string> = {
  lead: "Lead",
  contacted: "Contacté",
  opened: "Ouvert",
  replied: "Répondu",
  demo: "Démo",
  quoted: "Devisé",
  negotiating: "Négo",
  won: "Gagné",
  lost: "Perdu",
};

const FILTER_TABS = [
  { key: "all", label: "Tous" },
  { key: "urgent", label: "Urgents" },
  { key: "high", label: "Haute" },
  { key: "medium", label: "Moyenne" },
  { key: "low", label: "Basse" },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function PriorityBadge({ priority }: { priority: Priority }) {
  const labels: Record<Priority, string> = {
    urgent: "URGENT",
    high: "HAUTE",
    medium: "MOY.",
    low: "BASSE",
  };
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold tracking-wider ${PRIORITY_COLORS[priority]}`}
    >
      {labels[priority]}
    </span>
  );
}

function ActionBadge({ action }: { action: ActionType }) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium border ${ACTION_COLORS[action]}`}
    >
      {ACTION_LABELS[action]}
    </span>
  );
}

function UrgencyBar({ score, priority }: { score: number; priority: Priority }) {
  const widths: Record<Priority, string> = {
    urgent: "bg-red-500",
    high: "bg-orange-500",
    medium: "bg-yellow-500",
    low: "bg-slate-500",
  };
  return (
    <div className="flex items-center gap-2 w-full">
      <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div
          className={`h-1.5 rounded-full transition-all ${widths[priority]}`}
          style={{ width: `${score}%` }}
        />
      </div>
      <span className={`text-xs font-bold tabular-nums w-6 text-right ${PRIORITY_SCORE_COLOR[priority]}`}>
        {score}
      </span>
    </div>
  );
}

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
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-1">
      <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500">{sub}</p>}
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ task, onClose }: { task: FollowUpTask; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className={`bg-slate-900 border-2 rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 space-y-5 ${PRIORITY_RING[task.priority]} ring-2`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-white font-bold text-lg leading-tight">{task.company_name}</h2>
            <p className="text-slate-400 text-sm">{task.sector} · {task.prospect_id}</p>
          </div>
          <div className="flex flex-col items-end gap-1 flex-shrink-0">
            <PriorityBadge priority={task.priority} />
            <span className={`text-2xl font-black ${PRIORITY_SCORE_COLOR[task.priority]}`}>
              {task.urgency_score}
              <span className="text-xs text-slate-500 font-normal">/100</span>
            </span>
          </div>
        </div>

        {/* Action recommended */}
        <div className="bg-slate-800 rounded-xl p-4 flex flex-col gap-2">
          <p className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Action recommandée</p>
          <ActionBadge action={task.recommended_action} />
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Stade</p>
            <p className="text-white font-semibold">{STAGE_LABELS[task.current_stage] ?? task.current_stage}</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Depuis contact</p>
            <p className="text-white font-semibold">
              {task.days_since_contact === 0
                ? "Aujourd'hui"
                : `${task.days_since_contact}j`}
            </p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Score BANT</p>
            <p className="text-white font-semibold">{task.bant_score}/100</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Touches</p>
            <p className="text-white font-semibold">{task.touches}</p>
          </div>
          {task.quote_value > 0 && (
            <div className="bg-slate-800/60 rounded-lg p-3 col-span-2">
              <p className="text-slate-500 text-xs mb-1">Valeur devis</p>
              <p className="text-emerald-400 font-bold text-base">
                {task.quote_value.toLocaleString("fr-FR", { style: "currency", currency: "EUR" })}
              </p>
            </div>
          )}
        </div>

        {/* Urgency bar */}
        <div>
          <p className="text-xs text-slate-500 mb-2 font-medium">Score d'urgence</p>
          <UrgencyBar score={task.urgency_score} priority={task.priority} />
        </div>

        {/* Notes */}
        {task.notes && (
          <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-3">
            <p className="text-xs text-indigo-400 font-semibold mb-1">Notes</p>
            <p className="text-slate-300 text-sm">{task.notes}</p>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full mt-2 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors"
        >
          Fermer
        </button>
      </div>
    </div>
  );
}

// ─── Main page ────────────────────────────────────────────────────────────────

export default function FollowUpPage() {
  const [tasks, setTasks] = useState<FollowUpTask[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<FollowUpTask | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/followup")
      .then((r) => r.json())
      .then((data) => {
        setTasks(data.tasks ?? []);
        setSummary(data.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered =
    filter === "all" ? tasks : tasks.filter((t) => t.priority === filter);

  const overdue14 = tasks.filter((t) => t.days_since_contact >= 14);

  return (
    <div className="p-6 space-y-6 text-slate-100">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Suivi Prioritaire</h1>
        <p className="text-slate-400 text-sm mt-1">
          Liste d'actions quotidiennes triée par score d'urgence
        </p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-4 xl:grid-cols-8 gap-3">
          <KpiCard label="Total" value={summary.total} />
          <KpiCard label="Urgents" value={summary.urgent} accent="text-red-400" />
          <KpiCard label="Haute" value={summary.high} accent="text-orange-400" />
          <KpiCard label="Moyenne" value={summary.medium} accent="text-yellow-400" />
          <KpiCard label="Basse" value={summary.low} accent="text-slate-400" />
          <KpiCard
            label="Score moy."
            value={summary.avg_urgency_score}
            sub="/ 100"
            accent="text-indigo-400"
          />
          <KpiCard
            label="En retard 7j+"
            value={summary.overdue_7d}
            accent={summary.overdue_7d > 0 ? "text-orange-400" : "text-slate-400"}
          />
          <KpiCard
            label="Pipeline"
            value={summary.total_pipeline_eur.toLocaleString("fr-FR", {
              style: "currency",
              currency: "EUR",
              maximumFractionDigits: 0,
            })}
            accent="text-emerald-400"
          />
        </div>
      )}

      {/* Overdue banner */}
      {overdue14.length > 0 && (
        <div className="bg-red-950/40 border border-red-900/50 rounded-xl px-4 py-3 flex items-center gap-3">
          <span className="text-red-400 text-lg">⚠</span>
          <p className="text-red-300 text-sm font-medium">
            {overdue14.length} prospect{overdue14.length > 1 ? "s" : ""} sans contact depuis 14+ jours —{" "}
            <button
              className="underline hover:text-red-200"
              onClick={() => setFilter("urgent")}
            >
              voir urgents
            </button>
          </p>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {FILTER_TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors border ${
              filter === tab.key
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
            }`}
          >
            {tab.label}
            {tab.key !== "all" && summary && (
              <span className="ml-1.5 opacity-70">
                {summary[tab.key as Priority]}
              </span>
            )}
            {tab.key === "all" && summary && (
              <span className="ml-1.5 opacity-70">{summary.total}</span>
            )}
          </button>
        ))}
      </div>

      {/* Table */}
      {loading ? (
        <div className="text-slate-500 py-16 text-center">Chargement…</div>
      ) : filtered.length === 0 ? (
        <div className="text-slate-500 py-16 text-center">Aucune tâche dans cette priorité.</div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-slate-800">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-900/80">
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider w-8">
                  #
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Société
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Priorité
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider min-w-[140px]">
                  Urgence
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Action
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Stade
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Sans contact
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Devis
                </th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((task, i) => (
                <tr
                  key={task.prospect_id}
                  onClick={() => setSelected(task)}
                  className="border-b border-slate-800 hover:bg-slate-800/60 cursor-pointer transition-colors"
                >
                  <td className="px-4 py-3 text-slate-600 text-xs font-mono">{i + 1}</td>
                  <td className="px-4 py-3">
                    <p className="text-white font-medium">{task.company_name}</p>
                    <p className="text-slate-500 text-xs">{task.sector}</p>
                  </td>
                  <td className="px-4 py-3">
                    <PriorityBadge priority={task.priority} />
                  </td>
                  <td className="px-4 py-3 min-w-[140px]">
                    <UrgencyBar score={task.urgency_score} priority={task.priority} />
                  </td>
                  <td className="px-4 py-3">
                    <ActionBadge action={task.recommended_action} />
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-slate-300 text-xs bg-slate-800 px-2 py-0.5 rounded">
                      {STAGE_LABELS[task.current_stage] ?? task.current_stage}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span
                      className={`text-sm font-semibold tabular-nums ${
                        task.days_since_contact >= 14
                          ? "text-red-400"
                          : task.days_since_contact >= 7
                          ? "text-orange-400"
                          : "text-slate-300"
                      }`}
                    >
                      {task.days_since_contact === 0 ? "Auj." : `${task.days_since_contact}j`}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    {task.quote_value > 0 ? (
                      <span className="text-emerald-400 text-sm font-semibold tabular-nums">
                        {task.quote_value.toLocaleString("fr-FR", {
                          style: "currency",
                          currency: "EUR",
                          maximumFractionDigits: 0,
                        })}
                      </span>
                    ) : (
                      <span className="text-slate-600 text-xs">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Action breakdown */}
      {summary && Object.keys(summary.action_breakdown).length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Répartition des actions
          </h3>
          <div className="flex flex-wrap gap-3">
            {Object.entries(summary.action_breakdown)
              .sort(([, a], [, b]) => b - a)
              .map(([action, count]) => (
                <div
                  key={action}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-sm ${
                    ACTION_COLORS[action as ActionType] ?? "bg-slate-800 text-slate-300 border-slate-700"
                  }`}
                >
                  <span className="font-medium">
                    {ACTION_LABELS[action as ActionType] ?? action}
                  </span>
                  <span className="font-bold tabular-nums">{count}</span>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {selected && <DetailModal task={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
