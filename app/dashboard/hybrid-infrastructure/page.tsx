"use client";
import { useEffect, useState } from "react";

interface AgentStatus {
  agent_id: string;
  name: string;
  tier: "local" | "cloud";
  model: string;
  turn_count: number;
  max_turns: number;
  is_sleeping: boolean;
  circuit_state: "closed" | "open" | "half_open";
  is_alive: boolean;
  estimated_cost_usd: number;
  total_tokens?: number;
}

interface FleetStatus {
  orchestrator: {
    uptime_s: number;
    total_agents: number;
    local_agents: number;
    cloud_directors: number;
    alive_local: number;
    alive_directors: number;
    tripped_circuits: number;
    tripped_agent_ids: string[];
  };
  token_usage: {
    local_tokens: number;
    cloud_tokens: number;
    total_cost_usd: number;
    cloud_budget_limit: number;
    alerts: string[];
  };
  local_agents: AgentStatus[];
  directors: AgentStatus[];
  recommendations: string[];
}

function GaugeRing({ value, max, label, color }: { value: number; max: number; label: string; color: string }) {
  const pct = Math.min(value / max, 1);
  const r = 36;
  const circ = 2 * Math.PI * r;
  const dash = pct * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ}`} strokeDashoffset={circ / 4}
          strokeLinecap="round" transform="rotate(-90 48 48)" style={{ transition: "stroke-dasharray .6s" }} />
        <text x="48" y="52" textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">{Math.round(pct * 100)}%</text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function TurnBar({ current, max, isAlive }: { current: number; max: number; isAlive: boolean }) {
  const pct = Math.min(current / max, 1) * 100;
  const color = !isAlive ? "#ef4444" : pct > 80 ? "#f59e0b" : pct > 50 ? "#3b82f6" : "#10b981";
  return (
    <div className="w-full">
      <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <div className="flex justify-between text-xs text-slate-500 mt-0.5">
        <span>{current} tours</span><span>/{max}</span>
      </div>
    </div>
  );
}

function CircuitBadge({ state }: { state: string }) {
  const map: Record<string, { label: string; color: string }> = {
    closed: { label: "ACTIF", color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
    open: { label: "DÉCLENCHÉ", color: "bg-red-500/20 text-red-400 border-red-500/30" },
    half_open: { label: "RÉCUP.", color: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
  };
  const { label, color } = map[state] ?? map.open;
  return <span className={`text-xs px-2 py-0.5 rounded-full border font-mono ${color}`}>{label}</span>;
}

function formatUptime(s: number): string {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = Math.floor(s % 60);
  return `${h}h ${m}m ${sec}s`;
}

export default function HybridInfrastructurePage() {
  const [data, setData] = useState<FleetStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filterTier, setFilterTier] = useState<"all" | "local" | "cloud">("all");

  useEffect(() => {
    fetch("/api/hybrid-infrastructure")
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => { setError("Erreur chargement flotte"); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement flotte hybride…</div>
    </div>
  );
  if (error || !data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400">{error || "Données indisponibles"}</div>
    </div>
  );

  const { orchestrator: orch, token_usage: tok, local_agents, directors, recommendations } = data;
  const allAgents = [...local_agents, ...directors];
  const filtered = filterTier === "all" ? allAgents : allAgents.filter(a => a.tier === filterTier);

  const cloudPct = tok.cloud_budget_limit > 0 ? (tok.cloud_tokens / tok.cloud_budget_limit) * 100 : 0;
  const aliveLocalPct = orch.local_agents > 0 ? (orch.alive_local / orch.local_agents) * 100 : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <div className="flex items-center gap-3 mb-1">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
              <circle cx="14" cy="14" r="4" fill="#6366f1"/>
              <circle cx="4" cy="8" r="3" fill="#10b981"/>
              <circle cx="24" cy="8" r="3" fill="#10b981"/>
              <circle cx="4" cy="20" r="3" fill="#10b981"/>
              <circle cx="24" cy="20" r="3" fill="#10b981"/>
              <line x1="10" y1="12" x2="7" y2="9" stroke="#475569" strokeWidth="1.5"/>
              <line x1="18" y1="12" x2="21" y2="9" stroke="#475569" strokeWidth="1.5"/>
              <line x1="10" y1="16" x2="7" y2="19" stroke="#475569" strokeWidth="1.5"/>
              <line x1="18" y1="16" x2="21" y2="19" stroke="#475569" strokeWidth="1.5"/>
            </svg>
            <h1 className="text-2xl font-bold text-white">Infrastructure Hybride — Flotte Multi-Agents</h1>
          </div>
          <p className="text-slate-400 text-sm">
            {orch.local_agents} agents locaux Ollama (gratuits) + {orch.cloud_directors} Directeurs cloud · Uptime {formatUptime(orch.uptime_s)}
          </p>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { label: "Agents Total", value: orch.total_agents, color: "from-slate-700 to-slate-600", text: "text-white" },
            { label: "Agents Locaux", value: orch.alive_local + "/" + orch.local_agents, color: "from-emerald-900 to-emerald-800", text: "text-emerald-300" },
            { label: "Directeurs Cloud", value: orch.alive_directors + "/" + orch.cloud_directors, color: "from-violet-900 to-violet-800", text: "text-violet-300" },
            { label: "Circuits Déclenchés", value: orch.tripped_circuits, color: orch.tripped_circuits > 0 ? "from-red-900 to-red-800" : "from-slate-700 to-slate-600", text: orch.tripped_circuits > 0 ? "text-red-300" : "text-white" },
            { label: "Tokens Cloud", value: tok.cloud_tokens.toLocaleString(), color: "from-blue-900 to-blue-800", text: "text-blue-300" },
            { label: "Coût Session", value: `$${tok.total_cost_usd.toFixed(4)}`, color: "from-amber-900 to-amber-800", text: "text-amber-300" },
          ].map(({ label, value, color, text }) => (
            <div key={label} className={`bg-gradient-to-br ${color} rounded-xl p-4 border border-white/5`}>
              <p className="text-slate-400 text-xs mb-1">{label}</p>
              <p className={`text-xl font-bold ${text}`}>{value}</p>
            </div>
          ))}
        </div>

        {/* Gauges */}
        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Indicateurs de Santé Flotte</h2>
          <div className="flex flex-wrap justify-around gap-6">
            <GaugeRing value={aliveLocalPct} max={100} label="Agents Locaux Actifs" color="#10b981" />
            <GaugeRing value={cloudPct} max={100} label="Budget Cloud Utilisé" color="#6366f1" />
            <GaugeRing value={orch.tripped_circuits} max={orch.total_agents} label="Circuits Déclenchés" color="#ef4444" />
            <GaugeRing value={tok.total_cost_usd * 100} max={CLOUD_COST_HARD_LIMIT_USD_CLIENT * 100} label={`Coût vs Limite $${CLOUD_COST_HARD_LIMIT_USD_CLIENT}`} color="#f59e0b" />
          </div>
        </div>

        {/* Recommandations */}
        {recommendations && recommendations.length > 0 && (
          <div className="bg-slate-900 rounded-xl p-5 border border-indigo-500/20">
            <h2 className="text-sm font-semibold text-indigo-400 uppercase tracking-wider mb-3">Recommandations Orchestrateur</h2>
            <ul className="space-y-2">
              {recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-indigo-400 mt-0.5">›</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Alertes budget */}
        {tok.alerts.length > 0 && (
          <div className="bg-red-900/20 border border-red-500/30 rounded-xl p-4">
            <h2 className="text-sm font-semibold text-red-400 mb-2">Alertes Budget Cloud</h2>
            {tok.alerts.map((a, i) => <p key={i} className="text-sm text-red-300">{a}</p>)}
          </div>
        )}

        {/* Circuits déclenchés */}
        {orch.tripped_agent_ids.length > 0 && (
          <div className="bg-red-900/10 border border-red-500/20 rounded-xl p-4">
            <h2 className="text-sm font-semibold text-red-400 mb-2">Circuits Déclenchés (Kill Switch Activé)</h2>
            <div className="flex flex-wrap gap-2">
              {orch.tripped_agent_ids.map(id => (
                <span key={id} className="text-xs px-3 py-1 bg-red-500/20 text-red-300 rounded-full font-mono border border-red-500/30">{id}</span>
              ))}
            </div>
          </div>
        )}

        {/* Filtre tier */}
        <div className="flex gap-2">
          {(["all", "local", "cloud"] as const).map(t => (
            <button key={t} onClick={() => setFilterTier(t)}
              className={`px-4 py-1.5 rounded-full text-sm border transition-all ${filterTier === t ? "bg-indigo-500 border-indigo-400 text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}>
              {t === "all" ? "Tous" : t === "local" ? "Locaux (Ollama)" : "Cloud (Director)"}
            </button>
          ))}
        </div>

        {/* Grille agents */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((agent) => (
            <div key={agent.agent_id}
              className={`bg-slate-900 rounded-xl p-5 border transition-all ${!agent.is_alive ? "border-red-500/40 bg-red-900/5" : agent.tier === "cloud" ? "border-violet-500/30" : "border-slate-800"}`}>
              {/* Header agent */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`w-2 h-2 rounded-full ${!agent.is_alive ? "bg-red-500" : agent.is_sleeping ? "bg-amber-500" : "bg-emerald-500"}`} />
                    <span className="text-xs font-mono text-slate-500">{agent.agent_id}</span>
                    <span className={`text-xs px-1.5 py-0.5 rounded font-mono ${agent.tier === "local" ? "bg-emerald-500/15 text-emerald-400" : "bg-violet-500/15 text-violet-400"}`}>
                      {agent.tier === "local" ? "LOCAL" : "CLOUD"}
                    </span>
                  </div>
                  <p className="text-sm font-semibold text-white leading-tight">{agent.name}</p>
                </div>
                <CircuitBadge state={agent.circuit_state} />
              </div>

              {/* Modèle */}
              <p className="text-xs text-slate-500 mb-3 font-mono">{agent.model}</p>

              {/* Barre tours */}
              <TurnBar current={agent.turn_count} max={agent.max_turns} isAlive={agent.is_alive} />

              {/* Infos */}
              <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-800">
                <div className="flex items-center gap-3 text-xs text-slate-500">
                  {agent.is_sleeping && <span className="text-amber-400">💤 Endormi</span>}
                  {agent.tier === "cloud" && agent.total_tokens !== undefined && (
                    <span>{agent.total_tokens.toLocaleString()} tokens</span>
                  )}
                </div>
                <span className={`text-xs font-semibold ${agent.tier === "local" ? "text-emerald-400" : "text-amber-400"}`}>
                  {agent.tier === "local" ? "GRATUIT" : `$${agent.estimated_cost_usd.toFixed(6)}`}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Répartition tokens */}
        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Répartition Tokens — Local vs Cloud</h2>
          <div className="space-y-3">
            {[
              { label: "Local (Ollama — Gratuit)", tokens: tok.local_tokens, color: "bg-emerald-500", note: "$0.00" },
              { label: `Cloud (Director — $${tok.total_cost_usd.toFixed(4)})`, tokens: tok.cloud_tokens, color: "bg-violet-500", note: `$${tok.total_cost_usd.toFixed(4)}` },
            ].map(({ label, tokens, color, note }) => {
              const total = tok.local_tokens + tok.cloud_tokens;
              const pct = total > 0 ? (tokens / total) * 100 : 0;
              return (
                <div key={label}>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>{label}</span>
                    <span>{tokens.toLocaleString()} tokens · {note}</span>
                  </div>
                  <div className="h-3 bg-slate-800 rounded-full overflow-hidden">
                    <div className={`h-full ${color} rounded-full transition-all`} style={{ width: `${Math.max(pct, 0.5)}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <p className="text-xs text-slate-600 text-center">
          Caelum Partners — Architecture Hybride Ollama Local + Cloud · Kill Switch max_turns=10 actif · {new Date().toLocaleString("fr-FR")}
        </p>
      </div>
    </div>
  );
}

const CLOUD_COST_HARD_LIMIT_USD_CLIENT = 5.0;
