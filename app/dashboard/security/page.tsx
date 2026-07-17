"use client";

import { useEffect, useState } from "react";

type ThreatSeverity = "info" | "low" | "medium" | "high" | "critical";
type RecommendedAction = "log" | "alert" | "block" | "ban";

interface SecurityEvent {
  event_id: string;
  timestamp: number;
  ip_address: string;
  endpoint: string;
  threat_type: string;
  severity: ThreatSeverity;
  recommended_action: RecommendedAction;
  matched_pattern: string;
  raw_input: string;
  details: string;
}

interface ThreatSummary {
  total_events: number;
  severity_counts: Record<ThreatSeverity, number>;
  blocked_ips: number;
  banned_ips: number;
  top_threat_types: { type: string; count: number }[];
}

interface SecurityData {
  events: SecurityEvent[];
  summary: ThreatSummary;
  blocked_ips: string[];
  banned_ips: string[];
  security_score: number;
  last_scan: string;
}

const SEV_STYLES: Record<ThreatSeverity, { bg: string; text: string; border: string; dot: string; label: string }> = {
  critical: { bg: "bg-red-900/50",    text: "text-red-300",    border: "border-red-700/60",    dot: "bg-red-500",    label: "CRITIQUE" },
  high:     { bg: "bg-orange-900/40", text: "text-orange-300", border: "border-orange-700/60", dot: "bg-orange-400", label: "ÉLEVÉ" },
  medium:   { bg: "bg-amber-900/30",  text: "text-amber-300",  border: "border-amber-700/40",  dot: "bg-amber-400",  label: "MOYEN" },
  low:      { bg: "bg-blue-900/30",   text: "text-blue-300",   border: "border-blue-700/40",   dot: "bg-blue-400",   label: "FAIBLE" },
  info:     { bg: "bg-slate-800",     text: "text-slate-400",  border: "border-slate-700",     dot: "bg-slate-500",  label: "INFO" },
};

const ACTION_STYLES: Record<RecommendedAction, string> = {
  log:   "text-slate-400",
  alert: "text-yellow-400",
  block: "text-orange-400",
  ban:   "text-red-400",
};

const THREAT_LABELS: Record<string, string> = {
  sql_injection:       "Injection SQL",
  xss_attempt:         "Tentative XSS",
  path_traversal:      "Path Traversal",
  command_injection:   "Injection Commande",
  template_injection:  "Injection Template",
  brute_force:         "Brute Force Auth",
  rate_limit_exceeded: "Abus Rate Limit",
  oversized_payload:   "Payload Surdimensionné",
  banned_ip_request:   "IP Bannie (tentative)",
  blocked_ip_request:  "IP Bloquée (tentative)",
};

function SeverityBadge({ severity }: { severity: ThreatSeverity }) {
  const s = SEV_STYLES[severity];
  return (
    <span className={`flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded border ${s.bg} ${s.text} ${s.border}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${s.dot} animate-pulse`} />
      {s.label}
    </span>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function SecurityScoreMeter({ score }: { score: number }) {
  const color = score >= 80 ? "text-emerald-400" : score >= 60 ? "text-amber-400" : "text-red-400";
  const barColor = score >= 80 ? "bg-emerald-500" : score >= 60 ? "bg-amber-400" : "bg-red-500";
  const label = score >= 80 ? "Bon" : score >= 60 ? "Moyen" : "Critique";
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Score de Sécurité</p>
      <div className="flex items-end gap-3 mb-3">
        <p className={`text-5xl font-bold ${color}`}>{score}</p>
        <p className="text-slate-500 text-sm mb-1">/100 — {label}</p>
      </div>
      <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full ${barColor} rounded-full transition-all`} style={{ width: `${score}%` }} />
      </div>
      <p className="text-xs text-slate-600 mt-2">Mis à jour en temps réel · surveillance 24/7</p>
    </div>
  );
}

function EventModal({ event, onClose }: { event: SecurityEvent; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const s = SEV_STYLES[event.severity];
  const ts = new Date(event.timestamp * 1000);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h2 className="text-base font-bold text-white font-mono">{event.event_id}</h2>
              <SeverityBadge severity={event.severity} />
            </div>
            <p className="text-xs text-slate-500">{ts.toLocaleString("fr-FR")} · {event.ip_address}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none flex-shrink-0">×</button>
        </div>
        <div className="p-6 space-y-4 text-sm">
          <div className="grid grid-cols-2 gap-3">
            {[
              ["Type de menace", THREAT_LABELS[event.threat_type] ?? event.threat_type],
              ["Action", event.recommended_action.toUpperCase()],
              ["Endpoint", event.endpoint],
              ["IP", event.ip_address],
            ].map(([k, v]) => (
              <div key={k} className="bg-slate-800 rounded-lg px-3 py-2">
                <p className="text-[10px] text-slate-500 mb-0.5">{k}</p>
                <p className="text-white font-medium font-mono text-xs truncate">{v}</p>
              </div>
            ))}
          </div>
          <div className="bg-slate-800 rounded-lg p-3">
            <p className="text-xs text-slate-500 mb-1">Pattern détecté</p>
            <code className="text-xs text-red-300 font-mono">{event.matched_pattern}</code>
          </div>
          {event.raw_input && (
            <div className="bg-slate-800 rounded-lg p-3">
              <p className="text-xs text-slate-500 mb-1">Entrée brute (tronquée)</p>
              <code className="text-xs text-amber-300 font-mono break-all">{event.raw_input}</code>
            </div>
          )}
          <div className="bg-slate-800 rounded-lg p-3">
            <p className="text-xs text-slate-500 mb-1">Détails</p>
            <p className="text-xs text-slate-300">{event.details}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function SecurityPage() {
  const [data, setData] = useState<SecurityData | null>(null);
  const [loading, setLoading] = useState(true);
  const [sevFilter, setSevFilter] = useState<ThreatSeverity | "all">("all");
  const [selected, setSelected] = useState<SecurityEvent | null>(null);

  useEffect(() => {
    fetch("/api/security")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6 text-slate-500 text-center py-16">Chargement…</div>;
  if (!data) return null;

  const { events, summary, blocked_ips, banned_ips, security_score } = data;

  const filtered = sevFilter === "all" ? events : events.filter((e) => e.severity === sevFilter);

  const sevTabs: { key: ThreatSeverity | "all"; label: string }[] = [
    { key: "all",      label: `Tous (${summary.total_events})` },
    { key: "critical", label: `Critique (${summary.severity_counts.critical})` },
    { key: "high",     label: `Élevé (${summary.severity_counts.high})` },
    { key: "medium",   label: `Moyen (${summary.severity_counts.medium})` },
    { key: "low",      label: `Faible (${summary.severity_counts.low})` },
  ];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      {selected && <EventModal event={selected} onClose={() => setSelected(null)} />}

      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <span className="text-red-400">🛡</span> Sécurité & Surveillance
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Détection temps réel — SQL injection, XSS, path traversal, brute force, rate abuse
          </p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs text-emerald-400 font-medium">ACTIF</span>
        </div>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          label="Événements détectés"
          value={summary.total_events}
          accent={summary.total_events > 0 ? "text-red-400" : "text-white"}
        />
        <KpiCard
          label="IPs bloquées"
          value={summary.blocked_ips}
          sub="temporairement"
          accent="text-orange-400"
        />
        <KpiCard
          label="IPs bannies"
          value={summary.banned_ips}
          sub="définitivement"
          accent="text-red-400"
        />
        <KpiCard
          label="Menaces critiques"
          value={summary.severity_counts.critical}
          accent={summary.severity_counts.critical > 0 ? "text-red-400" : "text-white"}
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Security score + top threats */}
        <div className="space-y-4">
          <SecurityScoreMeter score={security_score} />

          {/* Top threat types */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Top menaces</p>
            <div className="space-y-2">
              {summary.top_threat_types.map((t) => (
                <div key={t.type}>
                  <div className="flex justify-between text-xs mb-0.5">
                    <span className="text-slate-300">{THREAT_LABELS[t.type] ?? t.type}</span>
                    <span className="text-slate-500">{t.count}</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-red-500 rounded-full"
                      style={{ width: `${Math.min(100, (t.count / summary.total_events) * 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Banned IPs */}
          {banned_ips.length > 0 && (
            <div className="bg-slate-900 border border-red-900/30 rounded-xl p-4">
              <p className="text-xs text-red-400 uppercase tracking-wider font-semibold mb-2">IPs Bannies</p>
              <div className="space-y-1">
                {banned_ips.map((ip) => (
                  <div key={ip} className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-500 flex-shrink-0" />
                    <code className="text-xs text-red-300 font-mono">{ip}</code>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Blocked IPs */}
          {blocked_ips.length > 0 && (
            <div className="bg-slate-900 border border-orange-900/30 rounded-xl p-4">
              <p className="text-xs text-orange-400 uppercase tracking-wider font-semibold mb-2">IPs Bloquées</p>
              <div className="space-y-1">
                {blocked_ips.map((ip) => (
                  <div key={ip} className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-orange-400 flex-shrink-0" />
                    <code className="text-xs text-orange-300 font-mono">{ip}</code>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Event log */}
        <div className="xl:col-span-2 space-y-4">
          {/* Severity filter tabs */}
          <div className="flex flex-wrap gap-2">
            {sevTabs.map((t) => (
              <button
                key={t.key}
                onClick={() => setSevFilter(t.key)}
                className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                  sevFilter === t.key ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Event rows */}
          <div className="space-y-2">
            {filtered.map((evt) => {
              const s = SEV_STYLES[evt.severity];
              const ts = new Date(evt.timestamp * 1000);
              return (
                <button
                  key={evt.event_id}
                  onClick={() => setSelected(evt)}
                  className={`w-full text-left bg-slate-900 border rounded-xl p-3 hover:border-slate-600 transition-colors ${
                    evt.severity === "critical" ? "border-red-900/50" : evt.severity === "high" ? "border-orange-900/40" : "border-slate-800"
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <span className={`w-2 h-2 rounded-full ${s.dot} flex-shrink-0 mt-1.5`} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-0.5">
                        <SeverityBadge severity={evt.severity} />
                        <span className="text-xs text-slate-300 font-medium">
                          {THREAT_LABELS[evt.threat_type] ?? evt.threat_type}
                        </span>
                        <span className={`text-[10px] font-bold ${ACTION_STYLES[evt.recommended_action]}`}>
                          → {evt.recommended_action.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 truncate">
                        <code className="text-slate-400">{evt.ip_address}</code>
                        {" · "}{evt.endpoint}
                        {" · "}<code className="text-amber-500/80">{evt.matched_pattern}</code>
                      </p>
                    </div>
                    <span className="text-[10px] text-slate-600 flex-shrink-0">
                      {ts.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
                    </span>
                  </div>
                </button>
              );
            })}
            {filtered.length === 0 && (
              <div className="text-center py-12 text-slate-500">Aucun événement pour ce filtre</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
