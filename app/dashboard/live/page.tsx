"use client";

import { useEffect, useRef, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface AgentEvent {
  id: number;
  type: string;
  timestamp: string;
  agent_id: string;
  division: number;
  division_name: string;
  color: string;
  severity: "info" | "success" | "warning" | "error";
  message: string;
}

// ── Constants ─────────────────────────────────────────────────────────────────

const MAX_EVENTS = 200;

const DIV_LABELS: Record<number, string> = {
  1: "Détection",
  2: "Rédaction",
  3: "Négociation",
  4: "Production",
  5: "Finance",
  6: "Branding",
};

const SEVERITY_STYLE: Record<string, { bg: string; text: string; dot: string; border: string }> = {
  info:    { bg: "bg-blue-500/5",    text: "text-blue-300",    dot: "bg-blue-400",    border: "border-blue-500/10"   },
  success: { bg: "bg-emerald-500/5", text: "text-emerald-300", dot: "bg-emerald-400", border: "border-emerald-500/10" },
  warning: { bg: "bg-amber-500/5",   text: "text-amber-300",   dot: "bg-amber-400",   border: "border-amber-500/10"  },
  error:   { bg: "bg-red-500/5",     text: "text-red-300",     dot: "bg-red-400",     border: "border-red-500/10"    },
};

// ── Event row ─────────────────────────────────────────────────────────────────

function EventRow({ ev, isNew }: { ev: AgentEvent; isNew: boolean }) {
  const s = SEVERITY_STYLE[ev.severity] || SEVERITY_STYLE.info;
  const time = new Date(ev.timestamp).toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  return (
    <div
      className={`flex items-start gap-3 px-4 py-2.5 rounded-xl border transition-all duration-500 ${s.bg} ${s.border} ${
        isNew ? "animate-pulse-once" : ""
      }`}
    >
      {/* Div color bar */}
      <div
        className="w-0.5 self-stretch rounded-full shrink-0 mt-0.5"
        style={{ backgroundColor: ev.color }}
      />

      {/* Severity dot */}
      <div className={`w-2 h-2 rounded-full shrink-0 mt-1.5 ${s.dot}`} />

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span
            className="text-xs font-mono px-1.5 py-0.5 rounded"
            style={{ backgroundColor: ev.color + "20", color: ev.color }}
          >
            {ev.agent_id}
          </span>
          <span className="text-xs text-gray-500">{ev.division_name}</span>
          <span className={`text-sm ${s.text} flex-1`}>{ev.message}</span>
        </div>
      </div>

      {/* Timestamp */}
      <span className="text-xs text-gray-600 shrink-0 font-mono">{time}</span>
    </div>
  );
}

// ── Stats strip ───────────────────────────────────────────────────────────────

function StatPill({ label, value, color }: { label: string; value: number | string; color: string }) {
  return (
    <div className="flex items-center gap-2 bg-white/5 border border-white/8 rounded-lg px-3 py-2">
      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
      <span className="text-xs text-gray-400">{label}</span>
      <span className="text-sm font-bold text-white ml-auto">{value}</span>
    </div>
  );
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function LiveFeedPage() {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [paused, setPaused] = useState(false);
  const [filterDiv, setFilterDiv] = useState<number | null>(null);
  const [filterSev, setFilterSev] = useState<string | null>(null);
  const [newIds, setNewIds] = useState<Set<number>>(new Set());
  const pausedRef = useRef(false);
  const listRef = useRef<HTMLDivElement>(null);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    const es = new EventSource("/api/swarm/live");
    esRef.current = es;

    es.onopen = () => setConnected(true);
    es.onerror = () => setConnected(false);

    es.onmessage = (e) => {
      if (pausedRef.current) return;
      const ev: AgentEvent = JSON.parse(e.data);
      if (ev.type !== "agent_event") return;

      setEvents((prev) => [ev, ...prev].slice(0, MAX_EVENTS));
      setNewIds((prev) => {
        const next = new Set(prev);
        next.add(ev.id);
        setTimeout(() => setNewIds((s) => { const n = new Set(s); n.delete(ev.id); return n; }), 1500);
        return next;
      });
    };

    return () => es.close();
  }, []);

  const togglePause = () => {
    setPaused((p) => {
      pausedRef.current = !p;
      return !p;
    });
  };

  const clearEvents = () => setEvents([]);

  const filtered = events.filter((ev) => {
    if (filterDiv !== null && ev.division !== filterDiv) return false;
    if (filterSev !== null && ev.severity !== filterSev) return false;
    return true;
  });

  // Per-division counts
  const divCounts: Record<number, number> = {};
  for (const ev of events) {
    divCounts[ev.division] = (divCounts[ev.division] || 0) + 1;
  }

  const DIV_COLORS: Record<number, string> = {
    1: "#6366f1", 2: "#8b5cf6", 3: "#ec4899",
    4: "#f59e0b", 5: "#10b981", 6: "#06b6d4",
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-5">

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="text-2xl">📡</span>
            <h1 className="text-2xl font-bold">Activité en direct</h1>
            <span
              className={`flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full border font-medium ${
                connected
                  ? "text-emerald-400 bg-emerald-400/10 border-emerald-400/20"
                  : "text-red-400 bg-red-400/10 border-red-400/20"
              }`}
            >
              <span className={`w-1.5 h-1.5 rounded-full ${connected ? "bg-emerald-400 animate-pulse" : "bg-red-400"}`} />
              {connected ? "Connecté" : "Déconnecté"}
            </span>
          </div>
          <p className="text-sm text-gray-400">
            Flux SSE en temps réel — {events.length} événements reçus · {filtered.length} affichés
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={togglePause}
            className={`px-4 py-2 rounded-lg text-sm font-medium border transition-all ${
              paused
                ? "bg-amber-500/20 border-amber-500/30 text-amber-300 hover:bg-amber-500/30"
                : "bg-white/5 border-white/10 text-gray-300 hover:bg-white/10"
            }`}
          >
            {paused ? "▶ Reprendre" : "⏸ Pause"}
          </button>
          <button
            onClick={clearEvents}
            className="px-4 py-2 rounded-lg text-sm font-medium border bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 transition-all"
          >
            🗑 Vider
          </button>
        </div>
      </div>

      {/* Stats strip */}
      <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
        {[1, 2, 3, 4, 5, 6].map((div) => (
          <button
            key={div}
            onClick={() => setFilterDiv(filterDiv === div ? null : div)}
            className={`transition-all ${filterDiv === div ? "ring-2 ring-white/20 scale-105" : ""}`}
          >
            <StatPill
              label={`Div. ${div}`}
              value={divCounts[div] || 0}
              color={DIV_COLORS[div]}
            />
          </button>
        ))}
      </div>

      {/* Severity filter */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-xs text-gray-500">Filtrer :</span>
        {(["info", "success", "warning", "error"] as const).map((sev) => {
          const s = SEVERITY_STYLE[sev];
          return (
            <button
              key={sev}
              onClick={() => setFilterSev(filterSev === sev ? null : sev)}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs border transition-all ${
                filterSev === sev
                  ? `${s.bg} ${s.border} ${s.text} font-semibold`
                  : "bg-white/3 border-white/8 text-gray-400 hover:bg-white/5"
              }`}
            >
              <span className={`w-1.5 h-1.5 rounded-full ${s.dot}`} />
              {sev}
            </button>
          );
        })}
        {(filterDiv !== null || filterSev !== null) && (
          <button
            onClick={() => { setFilterDiv(null); setFilterSev(null); }}
            className="text-xs text-gray-500 hover:text-gray-300 underline transition-colors ml-2"
          >
            Tout afficher
          </button>
        )}
      </div>

      {/* Event feed */}
      <div
        ref={listRef}
        className="space-y-1.5 max-h-[calc(100vh-280px)] overflow-y-auto pr-1 scrollbar-thin"
      >
        {filtered.length === 0 ? (
          <div className="text-center py-16 text-gray-500 text-sm">
            {connected ? "En attente des événements…" : "Connexion perdue — actualise la page"}
          </div>
        ) : (
          filtered.map((ev) => (
            <EventRow key={`${ev.id}-${ev.timestamp}`} ev={ev} isNew={newIds.has(ev.id)} />
          ))
        )}
      </div>

    </div>
  );
}
