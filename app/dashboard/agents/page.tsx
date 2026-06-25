"use client";

import { useState } from "react";
import { DIVISIONS } from "@/lib/swarm-data";
import type { SwarmAgent, Division } from "@/lib/swarm-data";

// ── Constants ─────────────────────────────────────────────────────────────────

const DIV_COLORS: Record<number, string> = {
  1: "#3B82F6",
  2: "#8B5CF6",
  3: "#F59E0B",
  4: "#10B981",
  5: "#EF4444",
  6: "#EC4899",
};

const STATUS_LABELS: Record<string, string> = {
  active: "Actif",
  idle: "Inactif",
  error: "Erreur",
  blocked: "Bloqué",
};

const STATUS_DOT: Record<string, string> = {
  active: "bg-green-400",
  idle: "bg-slate-300",
  error: "bg-red-400",
  blocked: "bg-orange-400",
};

// ── Icons ─────────────────────────────────────────────────────────────────────

function IconSearch({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
    </svg>
  );
}

// ── Agent Card ─────────────────────────────────────────────────────────────────

function AgentCard({ agent, divColor, divEmoji }: { agent: SwarmAgent; divColor: string; divEmoji: string }) {
  const dot = STATUS_DOT[agent.status] ?? "bg-slate-300";

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 hover:shadow-md transition-shadow flex flex-col gap-3">
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
          style={{ backgroundColor: `${divColor}18` }}
        >
          {agent.isManager ? "👑" : divEmoji}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-[11px] font-mono text-slate-400">Agent {agent.id}</p>
          <p className="text-[13px] font-semibold text-slate-900 leading-tight">{agent.role}</p>
        </div>
        <span className={`w-2 h-2 rounded-full flex-shrink-0 mt-1.5 ${dot} ${agent.status === "active" ? "animate-pulse" : ""}`} />
      </div>

      {/* Status + task */}
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <span
            className="text-[10px] font-bold px-2 py-0.5 rounded-full"
            style={{
              backgroundColor: `${divColor}18`,
              color: divColor,
            }}
          >
            {agent.isManager ? "Manager" : "Exécuteur"}
          </span>
          <span className="text-[10px] text-slate-400">{STATUS_LABELS[agent.status] ?? agent.status}</span>
        </div>
        {agent.currentTask && (
          <p className="text-[11px] text-slate-500 italic">{agent.currentTask}</p>
        )}
      </div>

      {/* Tasks completed */}
      <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
        <span className="text-[10px] text-slate-400">Tâches complétées</span>
        <span className="text-[13px] font-bold tabular-nums" style={{ color: divColor }}>
          {agent.tasksCompleted}
        </span>
      </div>
    </div>
  );
}

// ── Division Section ──────────────────────────────────────────────────────────

function DivisionSection({ div, agents }: { div: Division; agents: SwarmAgent[] }) {
  const color = DIV_COLORS[div.id] ?? "#6366F1";
  const active = agents.filter((a) => a.status === "active").length;

  return (
    <div className="mb-8">
      {/* Division header */}
      <div className="flex items-center gap-3 mb-4">
        <div
          className="w-9 h-9 rounded-xl flex items-center justify-center text-xl"
          style={{ backgroundColor: `${color}18` }}
        >
          {div.emoji}
        </div>
        <div className="flex-1">
          <h2 className="text-[15px] font-bold text-slate-900">
            Division {div.id} — {div.name}
          </h2>
          <p className="text-[11px] text-slate-400">
            {agents.length} agents · {active} actifs · {div.kpiValue} {div.kpiUnit}
          </p>
        </div>
        <div
          className="text-[11px] font-semibold px-3 py-1 rounded-full"
          style={{ backgroundColor: `${color}15`, color }}
        >
          {div.kpi}
        </div>
      </div>

      {/* Agent grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} divColor={color} divEmoji={div.emoji} />
        ))}
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function AgentsPage() {
  const [search, setSearch] = useState("");
  const [divFilter, setDivFilter] = useState<number | null>(null);
  const [statusFilter, setStatusFilter] = useState<string | null>(null);

  const allAgents = DIVISIONS.flatMap((d) => d.agents);

  const filtered = allAgents.filter((a) => {
    if (divFilter !== null && a.division !== divFilter) return false;
    if (statusFilter !== null && a.status !== statusFilter) return false;
    if (search) {
      const q = search.toLowerCase();
      return a.id.includes(q) || a.role.toLowerCase().includes(q);
    }
    return true;
  });

  const stats = {
    total: allAgents.length,
    active: allAgents.filter((a) => a.status === "active").length,
    idle: allAgents.filter((a) => a.status === "idle").length,
    error: allAgents.filter((a) => a.status === "error").length,
    managers: allAgents.filter((a) => a.isManager).length,
    totalTasks: allAgents.reduce((s, a) => s + a.tasksCompleted, 0),
  };

  const groupedByDivision = DIVISIONS.map((div) => ({
    div,
    agents: filtered.filter((a) => a.division === div.id),
  })).filter((g) => g.agents.length > 0);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-800 via-indigo-900 to-slate-900 px-6 py-10">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold text-white mb-1">Annuaire des 60 Agents</h1>
          <p className="text-sm text-white/60">6 divisions · 10 agents chacune · architecture autonome</p>

          {/* Stats strip */}
          <div className="grid grid-cols-3 sm:grid-cols-6 gap-3 mt-6">
            {[
              { label: "Total", value: stats.total, color: "text-white" },
              { label: "Actifs", value: stats.active, color: "text-green-400" },
              { label: "Inactifs", value: stats.idle, color: "text-slate-400" },
              { label: "Erreurs", value: stats.error, color: "text-red-400" },
              { label: "Managers", value: stats.managers, color: "text-yellow-400" },
              { label: "Tâches totales", value: stats.totalTasks.toLocaleString("fr-FR"), color: "text-indigo-300" },
            ].map((s) => (
              <div key={s.label} className="bg-white/10 rounded-xl px-3 py-3 text-center">
                <p className={`text-xl font-bold tabular-nums ${s.color}`}>{s.value}</p>
                <p className="text-[10px] text-white/50 mt-0.5">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-6">
        {/* Filters */}
        <div className="flex flex-wrap gap-3 mb-6">
          {/* Search */}
          <div className="relative flex-1 min-w-[200px]">
            <IconSearch className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Rechercher un agent…"
              className="w-full pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          {/* Division filter */}
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => setDivFilter(null)}
              className={`text-xs px-3 py-1.5 rounded-full border font-medium transition-colors ${divFilter === null ? "bg-indigo-600 text-white border-indigo-600" : "bg-white text-slate-600 border-slate-200 hover:border-slate-300"}`}
            >
              Toutes
            </button>
            {DIVISIONS.map((div) => {
              const color = DIV_COLORS[div.id];
              return (
                <button
                  key={div.id}
                  onClick={() => setDivFilter(divFilter === div.id ? null : div.id)}
                  className={`text-xs px-3 py-1.5 rounded-full border font-medium transition-colors ${divFilter === div.id ? "text-white border-transparent" : "bg-white text-slate-600 border-slate-200 hover:border-slate-300"}`}
                  style={divFilter === div.id ? { backgroundColor: color, borderColor: color } : {}}
                >
                  {div.emoji} Div {div.id}
                </button>
              );
            })}
          </div>

          {/* Status filter */}
          <div className="flex gap-1.5">
            {["active", "idle", "error"].map((s) => (
              <button
                key={s}
                onClick={() => setStatusFilter(statusFilter === s ? null : s)}
                className={`text-xs px-3 py-1.5 rounded-full border font-medium transition-colors ${
                  statusFilter === s
                    ? s === "active" ? "bg-green-500 text-white border-green-500"
                    : s === "error" ? "bg-red-500 text-white border-red-500"
                    : "bg-slate-500 text-white border-slate-500"
                    : "bg-white text-slate-600 border-slate-200"
                }`}
              >
                {STATUS_LABELS[s]}
              </button>
            ))}
          </div>
        </div>

        {/* Result count */}
        {(search || divFilter !== null || statusFilter !== null) && (
          <p className="text-xs text-slate-500 mb-4">
            {filtered.length} agent{filtered.length !== 1 ? "s" : ""} trouvé{filtered.length !== 1 ? "s" : ""}
            {search && ` pour "${search}"`}
          </p>
        )}

        {/* Grouped sections */}
        {groupedByDivision.map(({ div, agents }) => (
          <DivisionSection key={div.id} div={div} agents={agents} />
        ))}

        {filtered.length === 0 && (
          <div className="text-center py-16 text-slate-400 text-sm">
            Aucun agent ne correspond à ces filtres.
          </div>
        )}
      </div>
    </div>
  );
}
