"use client";

import { useState, useEffect, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type AgentStatus = "ACTIF" | "EN VEILLE" | "EN MISSION";

interface Agent {
  id: string;
  role: string;
  status: AgentStatus;
  action: string;
  metric: string;
  load: number;
}

interface Mission {
  code: string;
  title: string;
  agent: string;
  progress: number;
  elapsed: string;
  estimated: string;
  events: string[];
}

interface Alert {
  level: "CRITIQUE" | "HAUTE" | "NORMALE";
  title: string;
  action: string;
  time: string;
}

interface TerminalLine {
  type: "system" | "input" | "response";
  text: string;
}

// ─── Data ─────────────────────────────────────────────────────────────────────

const AGENTS: Agent[] = [
  { id: "SENTINEL", role: "Sécurité & Protection Zero-Trust", status: "ACTIF", action: "Scan ports entrants terminé", metric: "0 intrusions détectées", load: 23 },
  { id: "ORACLE", role: "Analytics & Intelligence", status: "EN MISSION", action: "Analyse Salesforce Q2 en cours", metric: "847 signaux analysés", load: 78 },
  { id: "HERMES", role: "Prospection & Vente LinkedIn", status: "ACTIF", action: "10 messages envoyés ce matin", metric: "3 réponses positives", load: 45 },
  { id: "NEXUS", role: "SEO & Indexation", status: "EN VEILLE", action: "Dernier crawl il y a 2h", metric: "Position #3 sur 'veille concurrentielle'", load: 12 },
  { id: "FORGE", role: "Développement & Déploiement", status: "ACTIF", action: "Build v2.4.1 déployé", metric: "99.8% uptime 30j", load: 34 },
  { id: "ECHO", role: "Support Client 24h/24", status: "ACTIF", action: "3 tickets résolus aujourd'hui", metric: "NPS +72 ce mois", load: 28 },
  { id: "PRISM", role: "Social Media & Viralité", status: "EN MISSION", action: "Campagne LinkedIn Q2 active", metric: "+340 impressions/j", load: 62 },
  { id: "ATLAS", role: "Veille Concurrentielle", status: "ACTIF", action: "Signal faible HubSpot détecté", metric: "5 concurrents surveillés", load: 55 },
  { id: "COMMANDANT", role: "Centre de Commandement", status: "ACTIF", action: "Supervision flotte complète", metric: "9/9 agents opérationnels", load: 41 },
];

const MISSIONS: Mission[] = [
  {
    code: "MISSION-2026-047",
    title: "Surveillance pricing Salesforce Q2 2026",
    agent: "ORACLE",
    progress: 67,
    elapsed: "14j 3h",
    estimated: "21j",
    events: [
      "Signal: modification page pricing détectée (J+12)",
      "Alerte: -18% sur plan Enterprise (J+13)",
      "Rapport intermédiaire généré et envoyé CODIR (J+14)",
    ],
  },
  {
    code: "MISSION-2026-051",
    title: "Campagne acquisition LinkedIn — Segment ETI",
    agent: "PRISM",
    progress: 34,
    elapsed: "6j",
    estimated: "18j",
    events: [
      "Ciblage 2 840 profils qualifiés (J+1)",
      "Séquence 5 messages configurée (J+2)",
      "Taux ouverture 34% — au-dessus de la moyenne (J+6)",
    ],
  },
];

const ALERTS: Alert[] = [
  { level: "CRITIQUE", title: "Prix Salesforce Enterprise -18%", action: "Activer plan de réponse tarifaire immédiate", time: "Il y a 2h" },
  { level: "HAUTE", title: "HubSpot recrute 23 ingénieurs NLP", action: "Escalade ORACLE pour analyse approfondie", time: "Il y a 6h" },
  { level: "NORMALE", title: "Pipedrive nouveau partenaire Microsoft", action: "Surveiller impact sur segment PME", time: "Il y a 1j" },
];

const INITIAL_TERMINAL: TerminalLine[] = [
  { type: "system", text: "╔══════════════════════════════════════════════╗" },
  { type: "system", text: "║  COMPETEIQ OPS CENTER — TERMINAL v4.2.1      ║" },
  { type: "system", text: "║  NIVEAU ACCÈS : COMMANDANT                   ║" },
  { type: "system", text: "╚══════════════════════════════════════════════╝" },
  { type: "system", text: "" },
  { type: "system", text: "[BOOT] Connexion sécurisée établie..." },
  { type: "system", text: "[BOOT] Chiffrement AES-256 actif" },
  { type: "system", text: "[BOOT] 9/9 agents en ligne" },
  { type: "system", text: "[OK]   Flotte opérationnelle — 0 incident détecté" },
  { type: "system", text: "" },
  { type: "input", text: "status --all" },
  { type: "response", text: "✓ SENTINEL: ACTIF [load:23%] · ORACLE: EN MISSION [load:78%] · HERMES: ACTIF [load:45%]" },
  { type: "response", text: "  NEXUS: EN VEILLE [load:12%] · FORGE: ACTIF [load:34%] · ECHO: ACTIF [load:28%]" },
  { type: "response", text: "  PRISM: EN MISSION [load:62%] · ATLAS: ACTIF [load:55%] · COMMANDANT: ACTIF [load:41%]" },
  { type: "system", text: "" },
  { type: "input", text: "alert list --level=CRITIQUE" },
  { type: "response", text: "✓ [CRITIQUE] Prix Salesforce Enterprise -18% — détecté il y a 2h" },
  { type: "response", text: "  Action recommandée: Activer plan de réponse tarifaire immédiate" },
  { type: "system", text: "" },
];

// ─── Helpers ──────────────────────────────────────────────────────────────────

function getStatusColor(status: AgentStatus): { border: string; text: string; bg: string; dot: string } {
  switch (status) {
    case "ACTIF":
      return { border: "border-l-emerald-500", text: "text-emerald-400", bg: "bg-emerald-500/10", dot: "bg-emerald-400" };
    case "EN MISSION":
      return { border: "border-l-cyan-500", text: "text-cyan-400", bg: "bg-cyan-500/10", dot: "bg-cyan-400" };
    case "EN VEILLE":
      return { border: "border-l-amber-500", text: "text-amber-400", bg: "bg-amber-500/10", dot: "bg-amber-500" };
  }
}

function getAlertColors(level: Alert["level"]): { border: string; badge: string; badgeBg: string; icon: string } {
  switch (level) {
    case "CRITIQUE":
      return { border: "border-l-red-500", badge: "text-red-400", badgeBg: "bg-red-500/10 border-red-500/30", icon: "text-red-400" };
    case "HAUTE":
      return { border: "border-l-amber-500", badge: "text-amber-400", badgeBg: "bg-amber-500/10 border-amber-500/30", icon: "text-amber-400" };
    case "NORMALE":
      return { border: "border-l-cyan-500", badge: "text-cyan-400", badgeBg: "bg-cyan-500/10 border-cyan-500/30", icon: "text-cyan-400" };
  }
}

function getLoadColor(load: number): string {
  if (load >= 70) return "bg-red-500";
  if (load >= 45) return "bg-amber-500";
  return "bg-emerald-500";
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function AgentCard({ agent }: { agent: Agent }) {
  const sc = getStatusColor(agent.status);
  const loadColor = getLoadColor(agent.load);
  const isMission = agent.status === "EN MISSION";

  return (
    <div
      className={`border-l-4 ${sc.border} rounded-r-lg p-4 relative overflow-hidden`}
      style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)", border: "1px solid rgba(255,255,255,0.06)", borderLeftWidth: "4px" }}
    >
      {/* Scan line overlay */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03]" style={{ backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.5) 2px, rgba(255,255,255,0.5) 3px)" }} />

      {/* Header */}
      <div className="flex items-start justify-between mb-3 relative">
        <div>
          <p className="font-mono font-bold text-white text-[13px] tracking-widest uppercase">{agent.id}</p>
          <p className="text-[10px] text-slate-500 font-medium mt-0.5 font-mono">{agent.role}</p>
        </div>
        <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-bold font-mono tracking-wide border ${sc.bg} ${sc.text}`} style={{ borderColor: "rgba(255,255,255,0.08)" }}>
          <span className={`w-1.5 h-1.5 rounded-full ${sc.dot} ${isMission ? "animate-pulse" : ""}`} />
          {agent.status}
        </span>
      </div>

      {/* Last action */}
      <p className="text-[11px] text-slate-400 font-mono mb-1 relative">
        <span className="text-slate-600">▸ </span>{agent.action}
      </p>

      {/* Metric */}
      <p className="text-[11px] font-mono mb-3 relative" style={{ color: "#06b6d4" }}>
        <span className="text-slate-600">◈ </span>{agent.metric}
      </p>

      {/* Load bar */}
      <div className="relative">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[9px] text-slate-600 font-mono uppercase tracking-widest">CHARGE</span>
          <span className="text-[9px] font-mono font-bold text-slate-400">{agent.load}%</span>
        </div>
        <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-700 ${loadColor}`}
            style={{ width: `${agent.load}%` }}
          />
        </div>
      </div>
    </div>
  );
}

function MissionCard({ mission }: { mission: Mission }) {
  const progressColor = mission.progress >= 60 ? "bg-emerald-500" : mission.progress >= 30 ? "bg-cyan-500" : "bg-amber-500";

  return (
    <div
      className="rounded-lg p-5 border"
      style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)", borderColor: "rgba(6,182,212,0.15)" }}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-[10px] font-mono text-cyan-500 tracking-widest uppercase mb-1">{mission.code}</p>
          <p className="text-[13px] font-semibold text-white leading-snug">{mission.title}</p>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-1 rounded border border-cyan-500/20 text-cyan-400 bg-cyan-500/10 whitespace-nowrap ml-3">
          AGENT: {mission.agent}
        </span>
      </div>

      {/* Progress */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">PROGRESSION</span>
          <span className="text-[12px] font-mono font-bold text-white">{mission.progress}%</span>
        </div>
        <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${progressColor} transition-all duration-700`}
            style={{ width: `${mission.progress}%`, boxShadow: `0 0 8px currentColor` }}
          />
        </div>
        <div className="flex items-center justify-between mt-1.5">
          <span className="text-[10px] font-mono text-slate-600">Écoulé : <span className="text-slate-400">{mission.elapsed}</span></span>
          <span className="text-[10px] font-mono text-slate-600">Estimé : <span className="text-slate-400">{mission.estimated}</span></span>
        </div>
      </div>

      {/* Events */}
      <div className="space-y-1.5">
        <p className="text-[9px] font-mono text-slate-600 uppercase tracking-widest mb-2">JOURNAL D&apos;ÉVÉNEMENTS</p>
        {mission.events.map((event, i) => (
          <div key={i} className="flex items-start gap-2">
            <span className="text-[10px] font-mono text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
            <p className="text-[11px] font-mono text-slate-400">{event}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function AlertCard({ alert }: { alert: Alert }) {
  const ac = getAlertColors(alert.level);

  return (
    <div
      className={`border-l-4 ${ac.border} rounded-r-lg p-4`}
      style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)", border: "1px solid rgba(255,255,255,0.06)", borderLeftWidth: "4px" }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1.5">
            <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded border ${ac.badgeBg} ${ac.badge}`}>
              {alert.level}
            </span>
            <span className="text-[10px] font-mono text-slate-600">{alert.time}</span>
          </div>
          <p className="text-[12px] font-semibold text-white mb-1">{alert.title}</p>
          <p className="text-[11px] font-mono text-slate-500">
            <span className="text-slate-600">→ </span>{alert.action}
          </p>
        </div>
        <svg viewBox="0 0 20 20" fill="currentColor" className={`w-4 h-4 flex-shrink-0 mt-0.5 ${ac.icon}`}>
          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function CommandantPage() {
  const [time, setTime] = useState<string>("--:--:--");
  const [terminalLines, setTerminalLines] = useState<TerminalLine[]>(INITIAL_TERMINAL);
  const [inputValue, setInputValue] = useState<string>("");
  const terminalEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Real-time clock
  useEffect(() => {
    const tick = () => {
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, "0");
      const mm = String(now.getMinutes()).padStart(2, "0");
      const ss = String(now.getSeconds()).padStart(2, "0");
      setTime(`${hh}:${mm}:${ss}`);
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  // Auto-scroll terminal
  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [terminalLines]);

  const handleTerminalSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    const cmd = inputValue.trim();
    setTerminalLines((prev) => [
      ...prev,
      { type: "input", text: cmd },
      { type: "response", text: `✓ Commande reçue · Traitement en cours…` },
    ]);
    setInputValue("");
  };

  const today = new Date("2026-06-18");
  const dateStr = today.toLocaleDateString("fr-FR", { weekday: "long", year: "numeric", month: "long", day: "numeric" });

  const activeAgents = AGENTS.filter((a) => a.status === "ACTIF").length;
  const missionAgents = AGENTS.filter((a) => a.status === "EN MISSION").length;

  return (
    <div className="space-y-6 pb-10">
      {/* Inline styles for animations */}
      <style>{`
        @keyframes scanline {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(100vh); }
        }
        @keyframes pulse-dot {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(0.85); }
        }
        @keyframes blink-cursor {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
        .scanline-anim::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 2px;
          background: linear-gradient(90deg, transparent, rgba(16,185,129,0.15), transparent);
          animation: scanline 8s linear infinite;
          pointer-events: none;
          z-index: 1;
        }
        .pulse-dot {
          animation: pulse-dot 1.2s ease-in-out infinite;
        }
        .blink-cursor {
          animation: blink-cursor 1s step-end infinite;
        }
      `}</style>

      {/* ─── WAR ROOM HEADER ──────────────────────────────────────────────────── */}
      <div
        className="rounded-2xl overflow-hidden relative scanline-anim"
        style={{ background: "#020617" }}
      >
        {/* Hexagonal SVG background pattern */}
        <div className="absolute inset-0 opacity-[0.04] pointer-events-none">
          <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="hex-pattern" x="0" y="0" width="56" height="48" patternUnits="userSpaceOnUse">
                <polygon points="28,4 52,18 52,30 28,44 4,30 4,18" fill="none" stroke="#10b981" strokeWidth="0.8" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#hex-pattern)" />
          </svg>
        </div>

        {/* Glow effects */}
        <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full pointer-events-none" style={{ background: "radial-gradient(circle, rgba(16,185,129,0.06) 0%, transparent 70%)" }} />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 rounded-full pointer-events-none" style={{ background: "radial-gradient(circle, rgba(6,182,212,0.05) 0%, transparent 70%)" }} />

        <div className="relative px-6 py-8">
          {/* Top row */}
          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
            <div>
              {/* Badge */}
              <div className="flex items-center gap-2 mb-4">
                <span className="text-[10px] font-mono font-bold tracking-[0.2em] uppercase px-3 py-1 rounded border" style={{ color: "#10b981", borderColor: "rgba(16,185,129,0.3)", background: "rgba(16,185,129,0.06)" }}>
                  NIVEAU ACCÈS STRATÉGIQUE
                </span>
              </div>

              {/* Title */}
              <h1 className="font-mono font-black text-white uppercase tracking-[0.12em] text-2xl lg:text-3xl mb-2">
                COMMANDANT
              </h1>
              <p className="font-mono text-[11px] tracking-[0.3em] uppercase mb-5" style={{ color: "#06b6d4" }}>
                — WAR ROOM — OPS CENTER —
              </p>

              {/* Ops active indicator */}
              <div className="flex items-center gap-2 mb-6">
                <span className="w-2.5 h-2.5 rounded-full pulse-dot" style={{ background: "#ef4444", boxShadow: "0 0 8px #ef4444" }} />
                <span className="font-mono text-[11px] font-bold tracking-widest uppercase" style={{ color: "#ef4444" }}>
                  OPS CENTER ACTIF
                </span>
              </div>

              {/* Global stats */}
              <div className="flex flex-wrap gap-6">
                {[
                  { label: "AGENTS", value: AGENTS.length.toString(), color: "#10b981" },
                  { label: "MISSIONS ACTIVES", value: MISSIONS.length.toString(), color: "#06b6d4" },
                  { label: "INCIDENTS", value: "0", color: "#f59e0b" },
                  { label: "ACTIFS", value: `${activeAgents}`, color: "#10b981" },
                  { label: "EN MISSION", value: `${missionAgents}`, color: "#06b6d4" },
                ].map((stat) => (
                  <div key={stat.label}>
                    <p className="font-mono font-black text-2xl tabular-nums" style={{ color: stat.color, textShadow: `0 0 12px ${stat.color}60` }}>
                      {stat.value}
                    </p>
                    <p className="font-mono text-[9px] tracking-widest uppercase mt-0.5" style={{ color: "rgba(255,255,255,0.3)" }}>
                      {stat.label}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: Clock + Date */}
            <div className="flex flex-col items-end gap-3">
              <div
                className="px-6 py-4 rounded-xl border font-mono"
                style={{ background: "rgba(10,10,20,0.8)", borderColor: "rgba(16,185,129,0.2)" }}
              >
                <p className="text-[10px] tracking-[0.3em] uppercase mb-1" style={{ color: "rgba(255,255,255,0.3)" }}>
                  HEURE LOCALE
                </p>
                <p className="text-4xl font-black tabular-nums tracking-wider" style={{ color: "#10b981", textShadow: "0 0 20px rgba(16,185,129,0.5)" }}>
                  {time}
                </p>
                <p className="text-[10px] mt-2 capitalize tracking-wide" style={{ color: "rgba(255,255,255,0.4)" }}>
                  {dateStr}
                </p>
              </div>

              {/* Mini status */}
              <div className="text-right">
                <p className="font-mono text-[10px] tracking-widest uppercase" style={{ color: "rgba(255,255,255,0.25)" }}>
                  FLOTTE
                </p>
                <p className="font-mono text-[13px] font-bold" style={{ color: "#10b981" }}>
                  9 AGENTS · 2 MISSIONS ACTIVES · 0 INCIDENTS
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ─── AGENT GRID ───────────────────────────────────────────────────────── */}
      <div>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-1 h-5 rounded-full" style={{ background: "#10b981" }} />
          <h2 className="font-mono font-bold text-white uppercase tracking-widest text-[12px]">
            FLOTTE D&apos;AGENTS — {AGENTS.length} UNITÉS
          </h2>
          <div className="flex-1 h-px" style={{ background: "rgba(255,255,255,0.05)" }} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
          {AGENTS.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      </div>

      {/* ─── MISSIONS + ALERTS ────────────────────────────────────────────────── */}
      <div className="grid xl:grid-cols-[1fr_380px] gap-6">

        {/* Missions actives */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-1 h-5 rounded-full" style={{ background: "#06b6d4" }} />
            <h2 className="font-mono font-bold text-white uppercase tracking-widest text-[12px]">
              MISSIONS ACTIVES — {MISSIONS.length}
            </h2>
            <div className="flex-1 h-px" style={{ background: "rgba(255,255,255,0.05)" }} />
          </div>
          <div className="space-y-4">
            {MISSIONS.map((mission) => (
              <MissionCard key={mission.code} mission={mission} />
            ))}
          </div>
        </div>

        {/* Alertes */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-1 h-5 rounded-full" style={{ background: "#ef4444" }} />
            <h2 className="font-mono font-bold text-white uppercase tracking-widest text-[12px]">
              ALERTES DE COMMANDEMENT
            </h2>
            <div className="flex-1 h-px" style={{ background: "rgba(255,255,255,0.05)" }} />
          </div>
          <div className="space-y-3">
            {ALERTS.map((alert, i) => (
              <AlertCard key={i} alert={alert} />
            ))}
          </div>

          {/* Legend */}
          <div
            className="mt-4 p-4 rounded-lg border"
            style={{ background: "rgba(2,6,23,0.8)", borderColor: "rgba(255,255,255,0.06)" }}
          >
            <p className="font-mono text-[9px] tracking-[0.2em] uppercase text-slate-600 mb-3">NIVEAUX D&apos;ALERTE</p>
            <div className="space-y-2">
              {[
                { level: "CRITIQUE", desc: "Action immédiate requise", color: "#ef4444" },
                { level: "HAUTE", desc: "Réponse sous 24h", color: "#f59e0b" },
                { level: "NORMALE", desc: "Surveillance renforcée", color: "#06b6d4" },
              ].map((item) => (
                <div key={item.level} className="flex items-center gap-2.5">
                  <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: item.color }} />
                  <span className="font-mono text-[10px] font-bold w-16" style={{ color: item.color }}>{item.level}</span>
                  <span className="font-mono text-[10px] text-slate-600">{item.desc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ─── TERMINAL ─────────────────────────────────────────────────────────── */}
      <div>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-1 h-5 rounded-full" style={{ background: "#f59e0b" }} />
          <h2 className="font-mono font-bold text-white uppercase tracking-widest text-[12px]">
            TERMINAL DE COMMANDEMENT
          </h2>
          <div className="flex-1 h-px" style={{ background: "rgba(255,255,255,0.05)" }} />
          <span className="font-mono text-[10px] px-2 py-0.5 rounded border" style={{ color: "#10b981", borderColor: "rgba(16,185,129,0.3)", background: "rgba(16,185,129,0.06)" }}>
            SHELL ACTIF
          </span>
        </div>

        <div
          className="rounded-xl overflow-hidden border"
          style={{ background: "#000000", borderColor: "rgba(0,255,65,0.15)" }}
        >
          {/* Terminal toolbar */}
          <div
            className="flex items-center gap-2 px-4 py-2.5 border-b"
            style={{ background: "rgba(0,20,0,0.8)", borderColor: "rgba(0,255,65,0.1)" }}
          >
            <div className="w-3 h-3 rounded-full bg-red-500 opacity-70" />
            <div className="w-3 h-3 rounded-full bg-amber-400 opacity-70" />
            <div className="w-3 h-3 rounded-full bg-emerald-400 opacity-70" />
            <span className="ml-3 font-mono text-[11px]" style={{ color: "rgba(0,255,65,0.5)" }}>
              competeiq-ops-terminal — COMMANDANT@competeiq
            </span>
          </div>

          {/* Terminal body */}
          <div
            className="p-4 h-80 overflow-y-auto font-mono text-[11px] leading-5 relative"
            style={{ color: "#00ff41" }}
            onClick={() => inputRef.current?.focus()}
          >
            {/* Scan line */}
            <div
              className="absolute inset-x-0 h-8 pointer-events-none opacity-[0.04]"
              style={{
                background: "linear-gradient(to bottom, transparent, #00ff41, transparent)",
                animation: "scanline 8s linear infinite",
                top: 0,
              }}
            />

            {/* Lines */}
            <div className="relative space-y-0.5">
              {terminalLines.map((line, i) => {
                if (line.type === "system") {
                  return (
                    <p key={i} style={{ color: line.text === "" ? undefined : "rgba(0,255,65,0.5)" }}>
                      {line.text || " "}
                    </p>
                  );
                }
                if (line.type === "input") {
                  return (
                    <p key={i}>
                      <span style={{ color: "rgba(0,255,65,0.6)" }}>COMMANDANT@competeiq:~$ </span>
                      <span style={{ color: "#00ff41" }}>{line.text}</span>
                    </p>
                  );
                }
                return (
                  <p key={i} style={{ color: "rgba(0,255,65,0.8)", paddingLeft: "0.5rem" }}>
                    {line.text}
                  </p>
                );
              })}
            </div>
            <div ref={terminalEndRef} />
          </div>

          {/* Input row */}
          <form
            onSubmit={handleTerminalSubmit}
            className="flex items-center gap-2 px-4 py-3 border-t"
            style={{ background: "rgba(0,10,0,0.9)", borderColor: "rgba(0,255,65,0.1)" }}
          >
            <span className="font-mono text-[11px] whitespace-nowrap flex-shrink-0" style={{ color: "rgba(0,255,65,0.6)" }}>
              COMMANDANT@competeiq:~$
            </span>
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="flex-1 bg-transparent outline-none font-mono text-[11px] caret-transparent"
              style={{ color: "#00ff41" }}
              spellCheck={false}
              autoComplete="off"
              placeholder="Entrez une commande…"
            />
            <span className="w-2 h-4 blink-cursor flex-shrink-0" style={{ background: "#00ff41" }} />
          </form>
        </div>

        {/* Terminal hint */}
        <p className="font-mono text-[10px] text-slate-700 mt-2 px-1">
          Commandes disponibles : <span className="text-slate-600">status --all · alert list · mission status · agent activate [ID] · help</span>
        </p>
      </div>
    </div>
  );
}
