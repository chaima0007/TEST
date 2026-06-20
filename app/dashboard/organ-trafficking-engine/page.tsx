"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = {
  critique: "text-red-400",
  "élevé": "text-orange-400",
  modéré: "text-yellow-400",
  faible: "text-emerald-400",
};
const RB: Record<string, string> = {
  critique: "border-red-500/30 bg-red-500/10",
  "élevé": "border-orange-500/30 bg-orange-500/10",
  modéré: "border-yellow-500/30 bg-yellow-500/10",
  faible: "border-emerald-500/30 bg-emerald-500/10",
};

type OTEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  forced_organ_harvesting_score: number;
  transplant_tourism_infrastructure_score: number;
  state_complicity_organ_trade_score: number;
  black_market_organ_network_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_organ_trafficking_index: number;
  last_updated: string;
};

type ApiResponse = {
  total_entities: number;
  avg_composite: number;
  avg_estimated_organ_trafficking_index: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  entities: OTEntity[];
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c1521" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-red-400/70 text-center">{label}</span>
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
      <span className="text-xs text-red-400/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#dc2626" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-red-400/60">
            <span style={{ color: colors[k] || "#dc2626" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  faible: "#10b981",
  modéré: "#eab308",
  "élevé": "#f97316",
  critique: "#dc2626",
};

const PATTERN_COLORS: Record<string, string> = {
  "Prélèvement Forcé Systémique": "#dc2626",
  "Tourisme Transplantation Illicite": "#f97316",
  "Complicité Étatique Documentée": "#7c3aed",
  "Réseau Marché Noir Organes": "#0891b2",
  "Surveillance Contrôlée": "#10b981",
};

function DetailModal({ entity, onClose }: { entity: OTEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-red-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.country}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.sector}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-red-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Prélèvement Forcé", entity.forced_organ_harvesting_score, "#dc2626"],
              ["Tourisme Transplantation", entity.transplant_tourism_infrastructure_score, "#f97316"],
              ["Complicité Étatique", entity.state_complicity_organ_trade_score, "#7c3aed"],
              ["Réseau Marché Noir", entity.black_market_organ_network_score, "#0891b2"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
                <div className="text-red-400/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-400/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
              <div className="text-red-400/60 text-xs mt-1">
                Index Trafic Organes:{" "}
                <span className="text-red-300 font-medium">{entity.estimated_organ_trafficking_index}</span>
              </div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="bg-slate-900 border border-red-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <p className="text-slate-400 text-xs mb-3">Signaux clés détectés</p>
            {entity.key_signals.map((sig, i) => (
              <div key={i} className="flex items-start gap-2 mb-2">
                <span className="text-red-400 mt-0.5 text-xs">▶</span>
                <span className="text-slate-200 text-sm">{sig}</span>
              </div>
            ))}
            <div className="mt-3">
              <span className={`px-2 py-0.5 rounded text-xs font-medium border ${RB[entity.risk_level] || "bg-slate-700 text-slate-300"} ${RC[entity.risk_level] || ""}`}>
                {entity.risk_level}
              </span>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-400/60 text-xs mb-1">Pattern Primaire</div>
              <div className="text-white font-medium">{entity.primary_pattern}</div>
            </div>
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-400/60 text-xs mb-1">Pays / Secteur</div>
              <div className="text-white font-medium">{entity.country} · {entity.sector}</div>
            </div>
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-400/60 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-slate-300 text-xs">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function OrganTraffickingDashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>("tous");
  const [selected, setSelected] = useState<OTEntity | null>(null);

  useEffect(() => {
    fetch("/api/organ-trafficking-engine")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((json) => setData(json?.data ?? json))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-lg animate-pulse">
          Initialisation du Moteur Trafic d&apos;Organes…
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-sm">Erreur: {error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const entities = data.entities ?? [];

  const avg = (key: keyof OTEntity) => {
    if (entities.length === 0) return 0;
    const nums = entities.map((e) => Number(e[key]));
    return nums.reduce((a, b) => a + b, 0) / nums.length;
  };

  const filtered =
    filterRisk === "tous"
      ? entities
      : entities.filter((e) => e.risk_level === filterRisk);

  const riskDist = data.risk_distribution ?? {};
  const criticalCount = riskDist["critique"] ?? 0;
  const highCount = riskDist["élevé"] ?? 0;
  const moderateLowCount = (riskDist["modéré"] ?? 0) + (riskDist["faible"] ?? 0);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold" style={{ color: "#dc2626" }}>
          Organ Trafficking Engine
        </h1>
        <p className="text-red-400/60 text-sm mt-1">
          Trafic d&apos;organes, prélèvements forcés et tourisme de transplantation illicite —{" "}
          Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées", entities.length, "text-white"],
          ["Score Moyen", (data.avg_composite ?? avg("composite_score")).toFixed(1), "text-red-400"],
          ["Index Trafic Organes Moyen", (data.avg_estimated_organ_trafficking_index ?? avg("estimated_organ_trafficking_index")).toFixed(2), "text-red-300"],
          ["Critique", criticalCount, "text-red-400"],
          ["Élevé", highCount, "text-orange-400"],
          ["Modéré/Faible", moderateLowCount, "text-emerald-400"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-red-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-red-400/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">Scores Moyens par Dimension</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <GaugeRing
            value={avg("forced_organ_harvesting_score")}
            label="Prélèvement Forcé"
            color="#dc2626"
          />
          <GaugeRing
            value={avg("transplant_tourism_infrastructure_score")}
            label="Tourisme Transplantation"
            color="#f97316"
          />
          <GaugeRing
            value={avg("state_complicity_organ_trade_score")}
            label="Complicité Étatique"
            color="#7c3aed"
          />
          <GaugeRing
            value={avg("black_market_organ_network_score")}
            label="Réseau Marché Noir"
            color="#0891b2"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar title="Niveau de Risque" counts={riskDist} colors={RISK_COLORS} />
        <DistBar title="Patterns Détectés" counts={data.pattern_distribution ?? {}} colors={PATTERN_COLORS} />
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["tous", "critique", "élevé", "modéré", "faible"].map((r) => (
          <button
            key={r}
            onClick={() => setFilterRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filterRisk === r
                ? "bg-red-900 border-red-800 text-white"
                : "bg-slate-900 border-red-700/30 text-red-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((entity) => (
          <div
            key={entity.entity_id}
            onClick={() => setSelected(entity)}
            className="bg-slate-900 border border-red-700/30 rounded-xl p-4 cursor-pointer hover:border-red-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm truncate">{entity.name}</span>
              <span className="text-xs text-red-400/60 ml-2 flex-shrink-0">{entity.country}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{entity.sector}</div>
            <div className="mb-2">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium border ${RB[entity.risk_level] || "bg-slate-700 text-slate-300"} ${RC[entity.risk_level] || ""}`}
              >
                {entity.risk_level}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {entity.composite_score.toFixed(1)}
            </div>
            <div className="text-xs text-red-400/60 mb-2 capitalize">
              {entity.primary_pattern}
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden mb-2">
              <div
                className="h-full rounded-full"
                style={{
                  width: `${Math.min(entity.composite_score, 100)}%`,
                  background: RISK_COLORS[entity.risk_level] || "#dc2626",
                }}
              />
            </div>
            <div className="text-xs text-slate-500">
              Index Trafic:{" "}
              <span className="text-red-300 font-medium">{entity.estimated_organ_trafficking_index}</span>
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12 text-slate-500 text-sm">
          Aucune entité pour ce niveau de risque.
        </div>
      )}
    </div>
  );
}
