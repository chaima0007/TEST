"use client";

import { useEffect, useState } from "react";

type Health = "healthy" | "degraded" | "critical" | "offline";

interface AgentStats {
  agent_id: string;
  division: number;
  tasks_completed: number;
  tasks_failed: number;
  tasks_queued: number;
  error_rate: number;
  avg_response_time_ms: number;
  health: Health;
  last_error: string | null;
}

interface DivisionData {
  division: number;
  name: string;
  healthy_agents: number;
  total_agents: number;
  total_tasks: number;
  total_errors: number;
  division_error_rate: number;
  avg_response_time_ms: number;
  health: Health;
  agents: AgentStats[];
}

interface Summary {
  total_agents: number;
  healthy_agents: number;
  degraded_agents: number;
  critical_agents: number;
  offline_agents: number;
  total_tasks_completed: number;
  total_tasks_failed: number;
  global_error_rate: number;
  open_alerts: number;
}

interface ApiData {
  divisions: DivisionData[];
  summary: Summary;
}

const HEALTH_STYLES: Record<Health, { bg: string; text: string; dot: string }> = {
  healthy:  { bg: "bg-emerald-900/40", text: "text-emerald-300", dot: "bg-emerald-400" },
  degraded: { bg: "bg-amber-900/40",   text: "text-amber-300",   dot: "bg-amber-400" },
  critical: { bg: "bg-red-900/40",     text: "text-red-300",     dot: "bg-red-400" },
  offline:  { bg: "bg-slate-700",      text: "text-slate-400",   dot: "bg-slate-500" },
};

const HEALTH_LABELS: Record<Health, string> = {
  healthy:  "Sain",
  degraded: "Dégradé",
  critical: "Critique",
  offline:  "Hors ligne",
};

const DIV_COLORS: Record<number, string> = {
  1: "#3B82F6",
  2: "#8B5CF6",
  3: "#F59E0B",
  4: "#10B981",
  5: "#EF4444",
  6: "#EC4899",
};

function HealthBadge({ health }: { health: Health }) {
  const s = HEALTH_STYLES[health];
  return (
    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-semibold ${s.bg} ${s.text}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${s.dot} ${health === "healthy" ? "animate-pulse" : ""}`} />
      {HEALTH_LABELS[health]}
    </span>
  );
}

function ErrorRateBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = pct >= 25 ? "bg-red-500" : pct >= 10 ? "bg-amber-500" : "bg-emerald-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${Math.min(pct, 100)}%` }} />
      </div>
      <span className="text-[11px] text-slate-400 w-8 text-right">{pct}%</span>
    </div>
  );
}

function AgentRow({ agent }: { agent: AgentStats }) {
  return (
    <tr className="border-b border-slate-700/40 hover:bg-slate-700/20 transition-colors">
      <td className="px-4 py-2 font-mono text-[12px] text-slate-300">{agent.agent_id}</td>
      <td className="px-4 py-2">
        <HealthBadge health={agent.health} />
      </td>
      <td className="px-4 py-2 text-[12px] text-slate-300 text-right">{agent.tasks_completed.toLocaleString("fr-FR")}</td>
      <td className="px-4 py-2 text-[12px] text-slate-400 text-right">{agent.tasks_failed.toLocaleString("fr-FR")}</td>
      <td className="px-4 py-2 w-32">
        <ErrorRateBar value={agent.error_rate} />
      </td>
      <td className="px-4 py-2 text-[12px] text-slate-400 text-right">
        {agent.avg_response_time_ms > 0 ? `${agent.avg_response_time_ms} ms` : "—"}
      </td>
      <td className="px-4 py-2 text-[11px] text-slate-500 max-w-xs">
        {agent.last_error ? (
          <span className="text-red-400">{agent.last_error}</span>
        ) : (
          <span className="text-slate-600">—</span>
        )}
      </td>
    </tr>
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
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex flex-col gap-1">
      <p className="text-[11px] text-slate-400 uppercase tracking-wide">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-[11px] text-slate-500">{sub}</p>}
    </div>
  );
}

function DivisionCard({
  div,
  expanded,
  onToggle,
}: {
  div: DivisionData;
  expanded: boolean;
  onToggle: () => void;
}) {
  const color = DIV_COLORS[div.division] ?? "#64748B";
  const healthyPct = (div.healthy_agents / div.total_agents) * 100;

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
      <button
        onClick={onToggle}
        className="w-full text-left p-5 hover:bg-slate-700/40 transition-colors focus:outline-none"
      >
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-2">
            <span
              className="text-[11px] font-bold px-2 py-0.5 rounded"
              style={{ backgroundColor: `${color}25`, color }}
            >
              Div {div.division}
            </span>
            <span className="text-sm font-semibold text-slate-200">{div.name}</span>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <HealthBadge health={div.health} />
            <span className="text-slate-500 text-lg">{expanded ? "▴" : "▾"}</span>
          </div>
        </div>

        <div className="mb-3">
          <div className="flex justify-between text-[11px] text-slate-400 mb-1">
            <span>Agents sains</span>
            <span>{div.healthy_agents}/{div.total_agents}</span>
          </div>
          <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: `${healthyPct}%`,
                backgroundColor: healthyPct >= 80 ? "#10B981" : healthyPct >= 50 ? "#F59E0B" : "#EF4444",
              }}
            />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2 text-center">
          <div>
            <p className="text-[10px] text-slate-500 uppercase">Tâches</p>
            <p className="text-sm font-semibold text-slate-200">{div.total_tasks.toLocaleString("fr-FR")}</p>
          </div>
          <div>
            <p className="text-[10px] text-slate-500 uppercase">Err. rate</p>
            <p className={`text-sm font-semibold ${div.division_error_rate >= 0.25 ? "text-red-400" : div.division_error_rate >= 0.10 ? "text-amber-400" : "text-emerald-400"}`}>
              {Math.round(div.division_error_rate * 1000) / 10}%
            </p>
          </div>
          <div>
            <p className="text-[10px] text-slate-500 uppercase">Latence</p>
            <p className="text-sm font-semibold text-slate-200">{div.avg_response_time_ms} ms</p>
          </div>
        </div>
      </button>

      {expanded && (
        <div className="border-t border-slate-700 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700/60 bg-slate-900/40">
                <th className="text-left px-4 py-2 text-[10px] text-slate-500 uppercase tracking-wide font-medium">Agent</th>
                <th className="text-left px-4 py-2 text-[10px] text-slate-500 uppercase tracking-wide font-medium">Santé</th>
                <th className="text-right px-4 py-2 text-[10px] text-slate-500 uppercase tracking-wide font-medium">Terminées</th>
                <th className="text-right px-4 py-2 text-[10px] text-slate-500 uppercase tracking-wide font-medium">Échouées</th>
                <th className="text-left px-4 py-2 text-[10px] text-slate-500 uppercase tracking-wide font-medium w-32">Err. rate</th>
                <th className="text-right px-4 py-2 text-[10px] text-slate-500 uppercase tracking-wide font-medium">Latence</th>
                <th className="text-left px-4 py-2 text-[10px] text-slate-500 uppercase tracking-wide font-medium">Dernière erreur</th>
              </tr>
            </thead>
            <tbody>
              {div.agents.map((agent) => (
                <AgentRow key={agent.agent_id} agent={agent} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default function PerformancePage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  useEffect(() => {
    fetch("/api/performance")
      .then((r) => r.json())
      .then((d: ApiData) => { setData(d); setLoading(false); })
      .catch(() => { setError("Impossible de charger les données de performance."); setLoading(false); });
  }, []);

  function toggleDiv(div: number) {
    setExpanded((prev) => {
      const next = new Set(prev);
      next.has(div) ? next.delete(div) : next.add(div);
      return next;
    });
  }

  const alerts = data
    ? data.divisions.flatMap((d) =>
        d.agents
          .filter((a) => a.health === "critical" || a.health === "offline")
          .map((a) => ({ ...a, division_name: d.name }))
      )
    : [];

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Performance des Agents</h1>
        <p className="text-sm text-slate-400 mt-1">
          60 agents surveillés · 6 divisions · santé en temps réel
        </p>
      </div>

      {loading && (
        <div className="text-center py-16 text-slate-500">Chargement des métriques…</div>
      )}
      {error && (
        <div className="text-center py-16 text-red-400">{error}</div>
      )}

      {data && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            <KpiCard label="Total agents" value={data.summary.total_agents} />
            <KpiCard
              label="Agents sains"
              value={data.summary.healthy_agents}
              accent="text-emerald-400"
            />
            <KpiCard
              label="Agents dégradés"
              value={data.summary.degraded_agents}
              accent={data.summary.degraded_agents > 0 ? "text-amber-400" : "text-white"}
            />
            <KpiCard
              label="Critiques / hors ligne"
              value={data.summary.critical_agents + data.summary.offline_agents}
              accent={data.summary.critical_agents + data.summary.offline_agents > 0 ? "text-red-400" : "text-white"}
            />
            <KpiCard
              label="Taux d'erreur global"
              value={`${Math.round(data.summary.global_error_rate * 1000) / 10}%`}
              sub={`${data.summary.total_tasks_failed.toLocaleString("fr-FR")} échouées`}
              accent={data.summary.global_error_rate >= 0.10 ? "text-amber-400" : "text-emerald-400"}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.divisions.map((div) => (
              <DivisionCard
                key={div.division}
                div={div}
                expanded={expanded.has(div.division)}
                onToggle={() => toggleDiv(div.division)}
              />
            ))}
          </div>

          {alerts.length > 0 && (
            <div className="bg-slate-800 border border-red-800/60 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-red-300 uppercase tracking-wide mb-4">
                Alertes actives ({alerts.length})
              </h2>
              <div className="space-y-2">
                {alerts.map((a) => (
                  <div
                    key={a.agent_id}
                    className="flex items-start gap-3 bg-slate-900/60 border border-slate-700 rounded-lg px-4 py-3"
                  >
                    <HealthBadge health={a.health} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-0.5">
                        <span className="font-mono text-[12px] text-slate-200">Agent {a.agent_id}</span>
                        <span className="text-[11px] text-slate-500">{a.division_name}</span>
                      </div>
                      <p className="text-[12px] text-slate-400">
                        {a.last_error ?? (a.health === "offline" ? "Agent hors ligne — aucune réponse" : "Taux d'erreur critique dépassé")}
                      </p>
                    </div>
                    <span className={`text-[11px] font-semibold ${a.health === "offline" ? "text-slate-400" : "text-red-400"}`}>
                      {a.health === "offline" ? "OFFLINE" : `${Math.round(a.error_rate * 100)}% err`}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
