"use client";
import { useEffect, useState } from "react";

type FWEEntity = {
  id: string;
  food_sector: string;
  region: string;
  waste_score: number;
  supply_chain_score: number;
  policy_score: number;
  circular_score: number;
  composite_score: number;
  risk_level: string;
  patterns: string[];
  economic_loss_per_capita: number;
  water_waste_embedded: number;
  carbon_footprint_waste: number;
  biodiversity_impact: number;
  estimated_food_waste_index: number;
};

type FWESummary = {
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  avg_waste_score: number;
  avg_supply_chain_score: number;
  avg_policy_score: number;
  avg_circular_score: number;
  avg_composite_score: number;
  top_patterns: Record<string, number>;
  risk_distribution: Record<string, number>;
  avg_estimated_food_waste_index: number;
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
      <span className="text-xs text-green-500/70 text-center">{label}</span>
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
      <span className="text-xs text-green-500/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#14532d" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-green-500/60">
            <span style={{ color: colors[k] || "#16a34a" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#16a34a",
  moderate: "#d97706",
  high: "#92400e",
  critical: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  retail_overproduction_dump: "#dc2626",
  cold_chain_collapse:        "#0891b2",
  date_label_confusion:       "#7c3aed",
  consumer_behavioral_waste:  "#d97706",
  policy_incentive_failure:   "#b45309",
};
const RISK_BADGE: Record<string, string> = {
  low:      "bg-green-900 text-green-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-amber-950 text-amber-500",
  critical: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: FWEEntity; onClose: () => void }) {
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
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-green-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-green-500 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.food_sector.replace(/_/g, " ")}
            </span>
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
                  ? "bg-green-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Gaspillage",        entity.waste_score,          "#dc2626"],
              ["Score Chaîne Logistique", entity.supply_chain_score,   "#0891b2"],
              ["Score Politique",         entity.policy_score,         "#7c3aed"],
              ["Score Économie Circulaire", entity.circular_score,     "#16a34a"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-green-700/20 rounded-lg p-3"
              >
                <div className="text-green-500/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-500/60 text-xs mb-1">Score Composite Gaspillage Alimentaire</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
              <div className="text-green-500/50 text-xs mt-1">
                Index Gaspillage: {entity.estimated_food_waste_index.toFixed(2)}/10
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-green-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <div className="flex gap-2 flex-wrap mb-3">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
            </div>
            <div className="mb-3">
              <div className="text-green-500/50 text-xs mb-1">Patrons Détectés</div>
              <div className="flex flex-wrap gap-1">
                {entity.patterns.length > 0 ? entity.patterns.map(p => (
                  <span
                    key={p}
                    className="px-2 py-0.5 rounded text-xs"
                    style={{ background: PATTERN_COLORS[p] || "#14532d", color: "white" }}
                  >
                    {p.replace(/_/g, " ")}
                  </span>
                )) : (
                  <span className="text-green-400 text-xs">Aucun patron critique détecté</span>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2 mt-3">
              <div className="bg-slate-800 rounded p-2">
                <div className="text-green-500/50 text-xs mb-0.5">Perte Éco./Capita</div>
                <div className="text-white text-sm font-medium">
                  {entity.economic_loss_per_capita.toFixed(0)} €
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-green-500/50 text-xs mb-0.5">Eau Gaspillée</div>
                <div className="text-white text-sm font-medium">
                  {entity.water_waste_embedded.toFixed(1)}
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-green-500/50 text-xs mb-0.5">Empreinte Carbone</div>
                <div className="text-white text-sm font-medium">
                  {entity.carbon_footprint_waste.toFixed(1)}
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-green-500/50 text-xs mb-0.5">Impact Biodiversité</div>
                <div className="text-white text-sm font-medium">
                  {entity.biodiversity_impact.toFixed(1)}
                </div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-500/60 text-xs mb-1">Secteur Alimentaire</div>
              <div className="text-white font-medium capitalize">
                {entity.food_sector.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-500/60 text-xs mb-1">Région</div>
              <div className="text-white font-medium">{entity.region}</div>
            </div>
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-500/60 text-xs mb-1">Index Gaspillage Alimentaire</div>
              <div className="text-amber-400 font-bold text-xl">
                {entity.estimated_food_waste_index.toFixed(2)}<span className="text-slate-500 text-sm font-normal">/10</span>
              </div>
            </div>
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-500/60 text-xs mb-1">Patrons Actifs</div>
              <div className="flex flex-wrap gap-1 mt-1">
                {entity.patterns.length > 0 ? entity.patterns.map(p => (
                  <span key={p} className="text-green-400 text-xs capitalize">
                    • {p.replace(/_/g, " ")}
                  </span>
                )) : (
                  <span className="text-green-400 text-xs">Aucun patron actif</span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function FoodWasteEconomyDashboard() {
  const [data, setData] = useState<{
    entities: FWEEntity[];
    summary: FWESummary;
  } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<FWEEntity | null>(null);

  useEffect(() => {
    fetch("/api/food-waste-economy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-green-500 text-lg animate-pulse">
          Initialisation du Moteur Gaspillage Alimentaire...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;
  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter === "all" || e.patterns.includes(patFilter))
  );

  const dists = [
    { title: "Niveau de Risque",      counts: summary.risk_distribution, colors: RISK_COLORS    },
    { title: "Patrons de Gaspillage", counts: summary.top_patterns,       colors: PATTERN_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const avgWasteScore        = entities.reduce((s, e) => s + e.waste_score, 0) / (entities.length || 1);
  const avgSupplyChainScore  = entities.reduce((s, e) => s + e.supply_chain_score, 0) / (entities.length || 1);
  const avgPolicyScore       = entities.reduce((s, e) => s + e.policy_score, 0) / (entities.length || 1);
  const avgCircularScore     = entities.reduce((s, e) => s + e.circular_score, 0) / (entities.length || 1);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-green-500">
          Gaspillage Alimentaire &amp; Économie Durable — Module 434
        </h1>
        <p className="text-amber-500/60 text-sm mt-1">
          Gaspillage · Chaîne Logistique · Politique · Économie Circulaire — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités",               summary.total_entities,                                              "text-green-500"],
          ["Crise Gaspillage",            summary.critical_count,                                              "text-red-400"],
          ["Risque Élevé",                summary.high_count,                                                  "text-amber-500"],
          ["Composite Moyen",             `${summary.avg_composite_score.toFixed(1)}`,                        "text-blue-400"],
          ["Index Gaspillage Alim.",      `${summary.avg_estimated_food_waste_index.toFixed(2)}/10`,          "text-green-500"],
          ["Entités Modérées",            summary.moderate_count,                                              "text-amber-400"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-green-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-green-500/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-green-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={avgWasteScore}
            label="Gaspillage Moy."
            color="#dc2626"
          />
          <GaugeRing
            value={avgSupplyChainScore}
            label="Chaîne Log. Moy."
            color="#0891b2"
          />
          <GaugeRing
            value={avgPolicyScore}
            label="Politique Moy."
            color="#7c3aed"
          />
          <GaugeRing
            value={avgCircularScore}
            label="Économie Circ. Moy."
            color="#16a34a"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-green-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-green-900 border-green-800 text-white"
                : "bg-slate-900 border-green-700/30 text-green-500/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-green-700/30" />
        {[
          "all",
          "retail_overproduction_dump",
          "cold_chain_collapse",
          "date_label_confusion",
          "consumer_behavioral_waste",
          "policy_incentive_failure",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-amber-950 border-amber-700 text-white"
                : "bg-slate-900 border-green-700/30 text-green-500/70 hover:text-white"
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
            className="bg-slate-900 border border-green-700/30 rounded-xl p-4 cursor-pointer hover:border-green-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-green-500/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.food_sector.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.composite_score.toFixed(1)}
            </div>
            <div className="text-xs text-amber-500/70 mb-2">
              Index: {e.estimated_food_waste_index.toFixed(2)}/10
            </div>
            <div className="text-xs text-green-400/70 font-medium mb-2">
              Déchets: {e.waste_score.toFixed(1)} · Log: {e.supply_chain_score.toFixed(1)}
            </div>
            {e.patterns.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-1">
                {e.patterns.slice(0, 2).map(p => (
                  <span
                    key={p}
                    className="px-1.5 py-0.5 rounded text-xs"
                    style={{ background: PATTERN_COLORS[p] || "#14532d", color: "white" }}
                  >
                    {p.replace(/_/g, " ")}
                  </span>
                ))}
                {e.patterns.length > 2 && (
                  <span className="text-xs text-slate-500">+{e.patterns.length - 2}</span>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
