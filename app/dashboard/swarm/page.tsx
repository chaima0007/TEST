"use client";

import { useEffect, useState } from "react";
import type {
  Division,
  SwarmAgent,
  SwarmJob,
  SwarmMetrics,
  NegotiationMessage,
} from "@/lib/swarm-data";

// ── Types ────────────────────────────────────────────────────────────────────

interface SwarmData {
  metrics: SwarmMetrics;
  divisions: Division[];
  jobs: SwarmJob[];
  simulation: NegotiationMessage[];
  lastUpdated: string;
}

// ── Palette ──────────────────────────────────────────────────────────────────

const DIV_COLORS: Record<number, string> = {
  1: "#3B82F6",
  2: "#8B5CF6",
  3: "#F59E0B",
  4: "#10B981",
  5: "#EF4444",
};

const STAGE_LABELS: Record<string, string> = {
  detection: "Détection",
  outreach: "Outreach",
  negotiation: "Négociation",
  production: "Production",
  paid: "Payé ✓",
};

const STAGE_COLORS: Record<string, string> = {
  detection: "#3B82F6",
  outreach: "#8B5CF6",
  negotiation: "#F59E0B",
  production: "#10B981",
  paid: "#059669",
};

// ── Sub-components ────────────────────────────────────────────────────────────

function MetricCard({
  label,
  value,
  unit,
  color,
  icon,
}: {
  label: string;
  value: string | number;
  unit?: string;
  color: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="bg-white rounded-lg border border-slate-200 p-4 flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-sm"
          style={{ backgroundColor: color }}
        >
          {icon}
        </div>
        <span className="text-[12px] text-slate-500 font-medium">{label}</span>
      </div>
      <div className="flex items-baseline gap-1">
        <span className="text-2xl font-bold text-slate-900 tabular-nums">{value}</span>
        {unit && <span className="text-[12px] text-slate-400">{unit}</span>}
      </div>
    </div>
  );
}

function AgentDot({ status }: { status: string }) {
  const colors: Record<string, string> = {
    active: "bg-green-400",
    idle: "bg-slate-300",
    error: "bg-red-400",
    blocked: "bg-orange-400",
  };
  return (
    <span
      className={`inline-block w-2 h-2 rounded-full ${colors[status] ?? "bg-slate-300"} ${
        status === "active" ? "animate-pulse" : ""
      }`}
      title={status}
    />
  );
}

function DivisionCard({ division }: { division: Division }) {
  const [expanded, setExpanded] = useState(false);
  const activeCount = division.agents.filter((a) => a.status === "active").length;
  const errorCount = division.agents.filter((a) => a.status === "error").length;
  const color = DIV_COLORS[division.id];

  return (
    <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setExpanded((e) => !e)}
        className="w-full flex items-center gap-3 p-4 hover:bg-slate-50 transition-colors text-left"
      >
        <div
          className="w-10 h-10 rounded-lg flex items-center justify-center text-xl flex-shrink-0"
          style={{ backgroundColor: `${color}20` }}
        >
          {division.emoji}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-[13px] font-semibold text-slate-900">{division.name}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">
            {activeCount} actifs · {errorCount > 0 ? <span className="text-red-500">{errorCount} erreur{errorCount > 1 ? "s" : ""}</span> : "0 erreur"}
          </p>
        </div>
        <div className="text-right flex-shrink-0">
          <p className="text-[18px] font-bold tabular-nums" style={{ color }}>
            {division.kpiValue}
          </p>
          <p className="text-[10px] text-slate-400">{division.kpiUnit}</p>
        </div>
        <svg
          className={`w-4 h-4 text-slate-400 flex-shrink-0 transition-transform ${expanded ? "rotate-180" : ""}`}
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {/* Agent list */}
      {expanded && (
        <div className="border-t border-slate-100">
          {/* Progress bar */}
          <div className="flex h-1.5">
            {division.agents.map((a) => (
              <div
                key={a.id}
                className="flex-1"
                style={{
                  backgroundColor:
                    a.status === "active"
                      ? color
                      : a.status === "error"
                      ? "#EF4444"
                      : "#E2E8F0",
                }}
              />
            ))}
          </div>
          <div className="divide-y divide-slate-50">
            {division.agents.map((agent) => (
              <AgentRow key={agent.id} agent={agent} color={color} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function AgentRow({ agent, color }: { agent: SwarmAgent; color: string }) {
  return (
    <div className="flex items-center gap-3 px-4 py-2.5 hover:bg-slate-50/70 transition-colors">
      <AgentDot status={agent.status} />
      <div
        className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded flex-shrink-0`}
        style={{ backgroundColor: `${color}15`, color }}
      >
        {agent.id}
      </div>
      {agent.isManager && (
        <span className="text-[9px] font-bold text-white px-1.5 py-0.5 rounded"
          style={{ backgroundColor: color }}>
          MGR
        </span>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-[12px] text-slate-700 truncate">{agent.role}</p>
        {agent.currentTask && (
          <p className="text-[10px] text-slate-400 truncate">{agent.currentTask}</p>
        )}
      </div>
      <span className="text-[11px] font-semibold text-slate-400 tabular-nums flex-shrink-0">
        {agent.tasksCompleted}
      </span>
    </div>
  );
}

function JobFeed({ jobs }: { jobs: SwarmJob[] }) {
  return (
    <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-100 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
        <h3 className="text-[13px] font-semibold text-slate-900">File de jobs — temps réel</h3>
      </div>
      <div className="divide-y divide-slate-100">
        {jobs.map((job) => (
          <div key={job.id} className="flex items-center gap-3 px-4 py-3">
            <div
              className="w-2 h-2 rounded-full flex-shrink-0"
              style={{ backgroundColor: STAGE_COLORS[job.stage] ?? "#6B7280" }}
            />
            <div className="flex-1 min-w-0">
              <p className="text-[13px] font-medium text-slate-800 truncate">{job.companyName}</p>
              <p className="text-[11px] text-slate-400">{job.sector} · Agent {job.assignedAgent}</p>
            </div>
            <span
              className="text-[10px] font-semibold px-2 py-0.5 rounded-full flex-shrink-0"
              style={{
                backgroundColor: `${STAGE_COLORS[job.stage]}15`,
                color: STAGE_COLORS[job.stage],
              }}
            >
              {STAGE_LABELS[job.stage]}
            </span>
            {job.amount && (
              <span className="text-[12px] font-bold text-green-600 flex-shrink-0">
                {job.amount}€
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function SimulationPanel({ messages }: { messages: NegotiationMessage[] }) {
  const [visible, setVisible] = useState(3);

  return (
    <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-100">
        <h3 className="text-[13px] font-semibold text-slate-900">
          Simulation — Agent 3.5 (Vente) × Agent 5.1 (Finance)
        </h3>
        <p className="text-[11px] text-slate-400 mt-0.5">
          Négociation client difficile : M. Girard, Restaurateur Lyon
        </p>
      </div>
      <div className="p-4 space-y-3">
        {messages.slice(0, visible).map((msg, idx) => (
          <div
            key={idx}
            className={`rounded-lg p-3 text-[12px] leading-relaxed ${
              msg.role === "prospect"
                ? "bg-amber-50 border border-amber-100 ml-4"
                : msg.role === "system"
                ? "bg-slate-50 border border-slate-100 text-slate-500 italic"
                : "bg-slate-900 text-slate-100 mr-4"
            }`}
          >
            <div className="flex items-center gap-2 mb-1">
              <span
                className="text-[10px] font-bold"
                style={{ color: msg.role === "prospect" ? "#F59E0B" : msg.color }}
              >
                {msg.agentName}
              </span>
              <span className="text-[10px] text-slate-400 font-mono">{msg.timestamp}</span>
            </div>
            <p>{msg.content}</p>
          </div>
        ))}
        {visible < messages.length && (
          <button
            onClick={() => setVisible((v) => Math.min(v + 3, messages.length))}
            className="w-full text-[12px] text-blue-600 font-medium py-2 hover:bg-blue-50 rounded-lg transition-colors"
          >
            Afficher la suite ({messages.length - visible} messages)
          </button>
        )}
        {visible >= messages.length && (
          <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
            <span className="w-2 h-2 rounded-full bg-green-400" />
            <span className="text-[12px] font-medium text-green-700">
              Deal conclu — 149€ encaissés · Durée : 3min 35sec
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

function RevenueBar({ divisions }: { divisions: Division[] }) {
  const total = 2237;
  const shares = [
    { id: 5, label: "Finance/Infra", value: total, pct: 100, color: DIV_COLORS[5] },
  ];

  const divKpis = [
    { label: "Prospects", value: 847, unit: "sites", color: DIV_COLORS[1], emoji: "🔍" },
    { label: "Emails envoyés", value: 312, unit: "msg", color: DIV_COLORS[2], emoji: "✍️" },
    { label: "Négociations", value: 28, unit: "actives", color: DIV_COLORS[3], emoji: "🤝" },
    { label: "Livrables", value: 7, unit: "/h", color: DIV_COLORS[4], emoji: "⚙️" },
    { label: "CA du jour", value: "2 237€", unit: "", color: DIV_COLORS[5], emoji: "🛡️" },
  ];

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-4">
      <h3 className="text-[13px] font-semibold text-slate-900 mb-4">KPI par Division</h3>
      <div className="grid grid-cols-5 gap-3">
        {divKpis.map((d, i) => (
          <div key={i} className="text-center">
            <div
              className="w-10 h-10 rounded-xl mx-auto mb-2 flex items-center justify-center text-xl"
              style={{ backgroundColor: `${d.color}15` }}
            >
              {d.emoji}
            </div>
            <p className="text-[15px] font-bold tabular-nums" style={{ color: d.color }}>
              {d.value}
            </p>
            <p className="text-[10px] text-slate-400">{d.unit}</p>
            <p className="text-[10px] text-slate-500 font-medium mt-0.5">{d.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Skeletons ─────────────────────────────────────────────────────────────────

function Skeleton({ className }: { className?: string }) {
  return <div className={`animate-pulse bg-slate-100 rounded ${className}`} />;
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SwarmPage() {
  const [data, setData] = useState<SwarmData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"overview" | "divisions" | "jobs" | "simulation">(
    "overview"
  );
  const [triggerState, setTriggerState] = useState<"idle" | "running" | "done">("idle");

  useEffect(() => {
    fetch("/api/swarm")
      .then((r) => r.json())
      .then((d: SwarmData) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const triggerCycle = async () => {
    setTriggerState("running");
    try {
      await fetch("/api/swarm", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ action: "trigger_cycle" }) });
    } catch {}
    setTimeout(() => setTriggerState("done"), 800);
    setTimeout(() => setTriggerState("idle"), 3500);
  };

  const m = data?.metrics;

  const TABS = [
    { key: "overview", label: "Vue d'ensemble" },
    { key: "divisions", label: "Divisions (5×10)" },
    { key: "jobs", label: "File de jobs" },
    { key: "simulation", label: "Simulation Vente" },
  ] as const;

  return (
    <div className="space-y-5 pb-10">
      {/* Page header */}
      <div className="flex items-start justify-between pt-1">
        <div>
          <h1 className="text-[22px] font-semibold text-slate-900 tracking-tight">
            Essaim — 50 Agents Autonomes
          </h1>
          <p className="text-[13px] text-slate-500 mt-0.5">
            5 divisions opérationnelles · Orchestration LangGraph + CrewAI
          </p>
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          <span className="flex items-center gap-1.5 text-[11px] text-slate-400 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse inline-block" />
            {m?.agentsActive ?? "—"} agents actifs
          </span>
          {m?.agentsError ? (
            <span className="flex items-center gap-1.5 text-[11px] text-red-500 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-red-400 inline-block" />
              {m.agentsError} erreur{m.agentsError > 1 ? "s" : ""}
            </span>
          ) : null}
          <button
            onClick={triggerCycle}
            disabled={triggerState === "running"}
            className={`text-[12px] font-semibold px-4 py-2 rounded-lg transition-all ${
              triggerState === "done"
                ? "bg-green-500 text-white"
                : triggerState === "running"
                ? "bg-blue-400 text-white cursor-not-allowed opacity-80"
                : "bg-blue-600 hover:bg-blue-700 text-white"
            }`}
          >
            {triggerState === "running" ? "⚡ Lancement…" : triggerState === "done" ? "✓ Cycle lancé !" : "⚡ Lancer un cycle"}
          </button>
        </div>
      </div>

      {/* Metric strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {loading ? (
          Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="h-20" />)
        ) : (
          <>
            <MetricCard label="CA total" value={`${(m!.totalRevenue).toLocaleString("fr-FR")}€`} color="#059669" icon="💰" />
            <MetricCard label="CA aujourd'hui" value="2 237€" color="#10B981" icon="📈" />
            <MetricCard label="Prospects/jour" value={m!.prospectsToday} unit="sites" color="#3B82F6" icon="🔍" />
            <MetricCard label="Emails envoyés" value={m!.emailsSent} unit="auj." color="#8B5CF6" icon="✍️" />
            <MetricCard label="Négociations" value={m!.activeNegotiations} unit="actives" color="#F59E0B" icon="🤝" />
            <MetricCard label="Conversion" value={`${m!.conversionRate}%`} color="#EF4444" icon="🎯" />
          </>
        )}
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-slate-200">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-4 py-2 text-[13px] font-medium transition-colors border-b-2 -mb-px ${
              activeTab === tab.key
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-slate-500 hover:text-slate-700"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {loading ? (
        <div className="space-y-4">
          <Skeleton className="h-40" />
          <Skeleton className="h-40" />
        </div>
      ) : (
        <>
          {activeTab === "overview" && data && (
            <div className="space-y-4">
              <RevenueBar divisions={data.divisions} />

              {/* Division grid — summary only */}
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {data.divisions.map((div) => {
                  const active = div.agents.filter((a) => a.status === "active").length;
                  const errors = div.agents.filter((a) => a.status === "error").length;
                  const color = DIV_COLORS[div.id];
                  return (
                    <div
                      key={div.id}
                      className="bg-white rounded-lg border border-slate-200 p-4 flex items-center gap-4"
                    >
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"
                        style={{ backgroundColor: `${color}15` }}
                      >
                        {div.emoji}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-[13px] font-semibold text-slate-900 truncate">{div.name}</p>
                        <p className="text-[11px] text-slate-400">
                          {active}/10 actifs
                          {errors > 0 && (
                            <span className="text-red-500 ml-1">· {errors} err.</span>
                          )}
                        </p>
                        {/* Mini agent bar */}
                        <div className="flex gap-0.5 mt-2">
                          {div.agents.map((a) => (
                            <div
                              key={a.id}
                              className="flex-1 h-1.5 rounded-sm"
                              style={{
                                backgroundColor:
                                  a.status === "active"
                                    ? color
                                    : a.status === "error"
                                    ? "#EF4444"
                                    : "#E2E8F0",
                              }}
                            />
                          ))}
                        </div>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className="text-[17px] font-bold tabular-nums" style={{ color }}>
                          {div.kpiValue}
                        </p>
                        <p className="text-[10px] text-slate-400">{div.kpiUnit}</p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Workflow diagram */}
              <div className="bg-white rounded-lg border border-slate-200 p-5">
                <h3 className="text-[13px] font-semibold text-slate-900 mb-4">Flux de travail inter-divisions</h3>
                <div className="flex items-center gap-2 overflow-x-auto pb-2">
                  {[
                    { id: 1, emoji: "🔍", label: "Détection", sub: "1 000 sites/j" },
                    { id: 2, emoji: "✍️", label: "Outreach", sub: "Emails IA" },
                    { id: 5, emoji: "🛡️", label: "Compliance", sub: "RGPD check" },
                    { id: 3, emoji: "🤝", label: "Négociation", sub: "Stripe link" },
                    { id: 4, emoji: "⚙️", label: "Production", sub: "Livraison 4h" },
                  ].map((step, idx, arr) => (
                    <div key={step.id} className="flex items-center gap-2 flex-shrink-0">
                      <div className="flex flex-col items-center gap-1">
                        <div
                          className="w-14 h-14 rounded-xl flex items-center justify-center text-2xl border-2"
                          style={{
                            borderColor: DIV_COLORS[step.id],
                            backgroundColor: `${DIV_COLORS[step.id]}10`,
                          }}
                        >
                          {step.emoji}
                        </div>
                        <p className="text-[11px] font-semibold text-slate-700 text-center">{step.label}</p>
                        <p className="text-[10px] text-slate-400 text-center">{step.sub}</p>
                      </div>
                      {idx < arr.length - 1 && (
                        <svg className="w-5 h-5 text-slate-300 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                        </svg>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === "divisions" && data && (
            <div className="grid lg:grid-cols-2 gap-4">
              {data.divisions.map((div) => (
                <DivisionCard key={div.id} division={div} />
              ))}
            </div>
          )}

          {activeTab === "jobs" && data && <JobFeed jobs={data.jobs} />}

          {activeTab === "simulation" && data && (
            <SimulationPanel messages={data.simulation} />
          )}
        </>
      )}
    </div>
  );
}
