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

type GAEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  women_mobility_restriction_score: number;
  women_education_denial_score: number;
  women_legal_subjugation_score: number;
  gender_violence_institutionalized_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_gender_apartheid_index: number;
  last_updated: string;
};

type ApiResponse = {
  total_entities: number;
  avg_composite: number;
  avg_estimated_gender_apartheid_index: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  entities: GAEntity[];
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
      <span className="text-xs text-pink-400/70 text-center">{label}</span>
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
      <span className="text-xs text-pink-400/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#ec4899" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-pink-400/60">
            <span style={{ color: colors[k] || "#ec4899" }}>■</span> {k.replace(/_/g, " ")} {v}
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
  critique: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  "Apartheid de Genre Systémique": "#ec4899",
  "Restriction Mobilité Féminine": "#f43f5e",
  "Déni Éducation Institutionnalisé": "#a855f7",
  "Subjugation Légale Documentée": "#f97316",
  "Violence de Genre Structurelle": "#dc2626",
  "Surveillance Contrôlée": "#10b981",
};

function DetailModal({ entity, onClose }: { entity: GAEntity; onClose: () => void }) {
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
        className="bg-slate-950 border border-pink-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-pink-400 text-xs">{entity.country}</span>
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
                  ? "bg-pink-900 text-white"
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
              ["Restriction Mobilité", entity.women_mobility_restriction_score, "#ec4899"],
              ["Déni Éducation", entity.women_education_denial_score, "#a855f7"],
              ["Subjugation Légale", entity.women_legal_subjugation_score, "#f97316"],
              ["Violence Institutionnalisée", entity.gender_violence_institutionalized_score, "#dc2626"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-pink-700/20 rounded-lg p-3">
                <div className="text-pink-400/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-pink-700/20 rounded-lg p-3">
              <div className="text-pink-400/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
              <div className="text-pink-400/60 text-xs mt-1">
                Index Apartheid Genre:{" "}
                <span className="text-pink-300 font-medium">{entity.estimated_gender_apartheid_index}</span>
              </div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="bg-slate-900 border border-pink-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <p className="text-slate-400 text-xs mb-3">Signaux clés détectés</p>
            {entity.key_signals.map((sig, i) => (
              <div key={i} className="flex items-start gap-2 mb-2">
                <span className="text-pink-400 mt-0.5 text-xs">▶</span>
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
            <div className="bg-slate-900 border border-pink-700/20 rounded-lg p-3">
              <div className="text-pink-400/60 text-xs mb-1">Pattern Primaire</div>
              <div className="text-white font-medium">{entity.primary_pattern}</div>
            </div>
            <div className="bg-slate-900 border border-pink-700/20 rounded-lg p-3">
              <div className="text-pink-400/60 text-xs mb-1">Pays / Secteur</div>
              <div className="text-white font-medium">{entity.country} · {entity.sector}</div>
            </div>
            <div className="bg-slate-900 border border-pink-700/20 rounded-lg p-3">
              <div className="text-pink-400/60 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-slate-300 text-xs">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GenderApartheidDashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>("tous");
  const [selected, setSelected] = useState<GAEntity | null>(null);

  useEffect(() => {
    fetch("/api/gender-apartheid-engine")
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
        <div className="text-pink-400 text-lg animate-pulse">
          Initialisation du Moteur Apartheid de Genre…
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-pink-400 text-sm">Erreur: {error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const entities = data.entities ?? [];

  const avg = (key: keyof GAEntity) => {
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
        <h1 className="text-2xl font-bold" style={{ color: "#ec4899" }}>
          Gender Apartheid Engine
        </h1>
        <p className="text-pink-400/60 text-sm mt-1">
          Apartheid de genre, oppression systémique des femmes et discriminations institutionnalisées —{" "}
          Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées", entities.length, "text-white"],
          ["Score Moyen", (data.avg_composite ?? avg("composite_score")).toFixed(1), "text-pink-400"],
          ["Index Apartheid Genre Moyen", (data.avg_estimated_gender_apartheid_index ?? avg("estimated_gender_apartheid_index")).toFixed(2), "text-pink-300"],
          ["Critique", criticalCount, "text-red-400"],
          ["Élevé", highCount, "text-orange-400"],
          ["Modéré/Faible", moderateLowCount, "text-emerald-400"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-pink-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-pink-400/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-pink-700/30 rounded-xl p-5">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">Scores Moyens par Dimension</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <GaugeRing
            value={avg("women_mobility_restriction_score")}
            label="Restriction Mobilité"
            color="#ec4899"
          />
          <GaugeRing
            value={avg("women_education_denial_score")}
            label="Déni Éducation"
            color="#a855f7"
          />
          <GaugeRing
            value={avg("women_legal_subjugation_score")}
            label="Subjugation Légale"
            color="#f97316"
          />
          <GaugeRing
            value={avg("gender_violence_institutionalized_score")}
            label="Violence Institutionnalisée"
            color="#dc2626"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-pink-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-pink-900 border-pink-800 text-white"
                : "bg-slate-900 border-pink-700/30 text-pink-400/70 hover:text-white"
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
            className="bg-slate-900 border border-pink-700/30 rounded-xl p-4 cursor-pointer hover:border-pink-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm truncate">{entity.name}</span>
              <span className="text-xs text-pink-400/60 ml-2 flex-shrink-0">{entity.country}</span>
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
            <div className="text-xs text-pink-400/60 mb-2 capitalize">
              {entity.primary_pattern}
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden mb-2">
              <div
                className="h-full rounded-full"
                style={{
                  width: `${Math.min(entity.composite_score, 100)}%`,
                  background: RISK_COLORS[entity.risk_level] || "#ec4899",
                }}
              />
            </div>
            <div className="text-xs text-slate-500">
              Index Apartheid:{" "}
              <span className="text-pink-300 font-medium">{entity.estimated_gender_apartheid_index}</span>
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
