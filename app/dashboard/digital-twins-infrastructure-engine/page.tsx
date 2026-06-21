"use client";
import { useEffect, useState } from "react";

type DTIEntity = {
  id: string;
  twin_domain: string;
  region: string;
  sync_score: number;
  security_score: number;
  dependency_score: number;
  sovereignty_score: number;
  composite_score: number;
  risk_level: string;
  twin_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  digital_physical_synchronization_gap: number;
  adversarial_twin_manipulation_risk: number;
};

type Summary = {
  module_id: number;
  module_name: string;
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_twin_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({
  title,
  counts,
  colors,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  twin_divergence_catastrophe: "#ef4444",
  adversarial_twin_attack: "#f97316",
  physical_twin_lock: "#dc2626",
  twin_vendor_monopoly: "#a855f7",
  cascading_twin_collapse: "#f59e0b",
};
const SEV_COLORS: Record<string, string> = {
  "jumeau_numérique_stable": "#10b981",
  "fragilité_jumeau_numérique_structurelle": "#f59e0b",
  "crise_infrastructure_jumeau_majeure": "#f97316",
  "effondrement_jumeau_numérique_critique": "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  "veille_jumeau_numérique_continue": "#10b981",
  "renforcement_indépendance_jumeau_numérique": "#06b6d4",
  "sécurisation_accélérée_infrastructure_jumeau": "#f97316",
  "intervention_urgente_résilience_jumeau": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: DTIEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{entity.twin_domain.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-cyan-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {(
              [
                ["Synchronisation", entity.sync_score, "#06b6d4"],
                ["Sécurité", entity.security_score, "#f97316"],
                ["Dépendance", entity.dependency_score, "#a855f7"],
                ["Souveraineté", entity.sovereignty_score, "#3b82f6"],
              ] as [string, number, string][]
            ).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(v, 100)}%`, background: c }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Jumeau</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}
              >
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-blue-900 text-blue-300">
                {entity.twin_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-400">
              <div>
                Écart sync:{" "}
                <span className="text-cyan-400 font-medium">
                  {(entity.digital_physical_synchronization_gap * 100).toFixed(0)}%
                </span>
              </div>
              <div>
                Risque adversarial:{" "}
                <span className="text-orange-400 font-medium">
                  {(entity.adversarial_twin_manipulation_risk * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">
                {entity.severity.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Domaine Jumeau</div>
              <div className="text-cyan-400 font-medium">
                {entity.twin_domain.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DigitalTwinsInfrastructureDashboard() {
  const [data, setData] = useState<{ entities: DTIEntity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DTIEntity | null>(null);

  useEffect(() => {
    fetch("/api/digital-twins-infrastructure-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-300 text-lg animate-pulse">
          Chargement Module 353 — Jumeaux Numériques...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    e =>
      (filter === "all" || e.risk_level === filter) &&
      (patFilter === "all" || e.twin_pattern === patFilter)
  );

  const avgSync = entities.length
    ? Math.round((entities.reduce((a, e) => a + e.sync_score, 0) / entities.length) * 10) / 10
    : 0;
  const avgSec = entities.length
    ? Math.round((entities.reduce((a, e) => a + e.security_score, 0) / entities.length) * 10) / 10
    : 0;
  const avgDep = entities.length
    ? Math.round((entities.reduce((a, e) => a + e.dependency_score, 0) / entities.length) * 10) / 10
    : 0;
  const avgSov = entities.length
    ? Math.round((entities.reduce((a, e) => a + e.sovereignty_score, 0) / entities.length) * 10) / 10
    : 0;

  const dists = [
    { title: "Distribution Risque", counts: summary.risk_distribution, colors: RISK_COLORS },
    { title: "Pattern Jumeau", counts: summary.pattern_distribution, colors: PAT_COLORS },
    { title: "Sévérité", counts: summary.severity_distribution, colors: SEV_COLORS },
    { title: "Action Recommandée", counts: summary.action_distribution, colors: ACT_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white">
          Jumeaux Numériques &amp; Infrastructure Physique-Digitale — Module 353
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Synchronisation · Sécurité · Dépendance · Souveraineté
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {(
          [
            ["Total Systèmes", summary.total_entities, "text-slate-300"],
            ["Effondrement Jumeau", summary.critical_count, "text-red-400"],
            ["Crise Infrastructure", summary.high_count, "text-orange-400"],
            ["Composite Moyen", summary.avg_composite, "text-cyan-400"],
            ["Index Risque Jumeau", summary.avg_estimated_twin_risk_index, "text-blue-400"],
            ["Synchronisation Moyenne", avgSync, "text-teal-400"],
          ] as [string, number, string][]
        ).map(([l, v, c]) => (
          <div
            key={l}
            className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgSync} label="Synchronisation" color="#06b6d4" />
          <GaugeRing value={avgSec}  label="Sécurité"        color="#f97316" />
          <GaugeRing value={avgDep}  label="Dépendance"      color="#a855f7" />
          <GaugeRing value={avgSov}  label="Souveraineté"    color="#3b82f6" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-cyan-700 border-cyan-600 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {[
          "all",
          "twin_divergence_catastrophe",
          "adversarial_twin_attack",
          "physical_twin_lock",
          "twin_vendor_monopoly",
          "cascading_twin_collapse",
          "none",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-slate-700 border-slate-600 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-cyan-400 mb-2">{e.twin_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}
              >
                {e.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-blue-900 text-blue-300">
                {e.twin_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="grid grid-cols-2 gap-1 mb-2">
              <div className="text-xs text-slate-500">
                Sync: <span className="text-cyan-400">{e.sync_score.toFixed(1)}</span>
              </div>
              <div className="text-xs text-slate-500">
                Sec: <span className="text-orange-400">{e.security_score.toFixed(1)}</span>
              </div>
              <div className="text-xs text-slate-500">
                Dép: <span className="text-purple-400">{e.dependency_score.toFixed(1)}</span>
              </div>
              <div className="text-xs text-slate-500">
                Souv: <span className="text-blue-400">{e.sovereignty_score.toFixed(1)}</span>
              </div>
            </div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
