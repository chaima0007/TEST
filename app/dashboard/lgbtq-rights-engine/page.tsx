"use client";
import { useState, useEffect } from "react";

const ACCENT = "#a855f7";
const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

function GaugeRing({ value, stroke }: { value: number; stroke: string }) {
  const r = 36, cx = 44, cy = 44, circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100) / 100;
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={stroke} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={circ * (1 - pct)}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fill="white" fontSize={14} fontWeight="bold">{Math.round(value)}</text>
    </svg>
  );
}

interface Entity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  criminalization_violence_severity_score: number;
  legal_protection_recognition_absence_score: number;
  healthcare_access_discrimination_scale_score: number;
  asylum_refugee_lgbtq_protection_gap_score: number;
  estimated_lgbtq_rights_index: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  last_updated: string;
  data_sources: string[];
  [key: string]: unknown;
}

interface DashData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  critical_alerts: number;
  confidence_score: number;
  last_analysis: string;
  entities: Entity[];
  avg_estimated_lgbtq_rights_index: number;
  data_sources: string[];
  [key: string]: unknown;
}

const RISK_CONFIG: Record<string, { label: string; color: string; bg: string; border: string }> = {
  critique: { label: "Critique", color: "text-red-400", bg: "bg-red-500/10", border: "border-red-500/25" },
  "élevé": { label: "Élevé", color: "text-orange-400", bg: "bg-orange-500/10", border: "border-orange-500/25" },
  modéré: { label: "Modéré", color: "text-yellow-400", bg: "bg-yellow-500/10", border: "border-yellow-500/25" },
  faible: { label: "Faible", color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/25" },
};

const SUB_SCORES = [
  { key: "criminalization_violence_severity_score", label: "Criminalisation/Violence" },
  { key: "legal_protection_recognition_absence_score", label: "Protection Juridique" },
  { key: "healthcare_access_discrimination_scale_score", label: "Accès Soins" },
  { key: "asylum_refugee_lgbtq_protection_gap_score", label: "Asile/Réfugiés LGBTQ+" },
];

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-y-auto"
        onClick={e => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800 flex justify-between items-start">
          <div>
            <span className={`text-xs font-semibold uppercase ${cfg.color}`}>{cfg.label}</span>
            <h2 className="text-lg font-bold text-slate-100 mt-1">{entity.name}</h2>
            <p className="text-sm text-slate-400">{entity.country} · {entity.sector}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex border-b border-slate-800">
          {["Aperçu", "Métriques", "Sources"].map((t, i) => (
            <button key={t} onClick={() => setTab(i)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${tab === i ? "border-b-2 text-purple-400" : "text-slate-400 hover:text-white"}`}
              style={tab === i ? { borderColor: ACCENT } : {}}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 text-sm">Score composite</span>
                <span className="text-2xl font-bold" style={{ color: ACCENT }}>{entity.composite_score}/100</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-400">Index LGBTQ+</span>
                <span className="font-semibold" style={{ color: ACCENT }}>{entity.estimated_lgbtq_rights_index}/10</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-400">Niveau de risque</span>
                <span className={`font-semibold uppercase text-xs ${cfg.color}`}>{cfg.label}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-400">Patron principal</span>
                <span className="text-slate-200">{entity.primary_pattern?.replace(/_/g, " ")}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-400">Contexte</span>
                <span className="text-slate-200 text-right max-w-xs">{entity.sector}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-400">Dernière mise à jour</span>
                <span className="text-slate-200">{entity.last_updated}</span>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              {SUB_SCORES.map(({ key, label }) => (
                <div key={key}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-400">{label}</span>
                    <span className="text-slate-200">{entity[key] as number}/100</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${entity[key] as number}%`, backgroundColor: ACCENT }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === 2 && (
            <ul className="space-y-3">
              {(entity.data_sources ?? entity.key_signals ?? []).map((s: string, i: number) => (
                <li key={i} className="flex gap-3 text-sm">
                  <span className="mt-0.5 shrink-0" style={{ color: ACCENT }}>▸</span>
                  <span className="text-slate-300">{s}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Page() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/lgbtq-rights-engine").then(r => r.json()).then(d => { setData(d.payload ?? d); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin" style={{ borderColor: ACCENT, borderTopColor: "transparent" }} />
    </div>
  );
  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400">Données indisponibles</div>
    </div>
  );

  const entities = data.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {/* Header */}
      <div className="mb-8 flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>LGBTQ+ Rights Engine</h1>
          <p className="text-slate-400 mt-1 text-sm">Criminalisation · Protection Juridique · Accès Soins · Asile LGBTQ+</p>
        </div>
        <span className="text-xs text-slate-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
          {data.total_entities} entités analysées
        </span>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Critiques</p>
          <p className="text-3xl font-bold mt-1 text-red-400">{data.risk_distribution?.critique ?? 0}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col items-center">
          <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">Score Moyen</p>
          <GaugeRing value={data.avg_composite} stroke={ACCENT} />
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Index LGBTQ+</p>
          <p className="text-3xl font-bold mt-1" style={{ color: ACCENT }}>{data.avg_estimated_lgbtq_rights_index}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Entités</p>
          <p className="text-3xl font-bold mt-1" style={{ color: ACCENT }}>{data.total_entities}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Confiance</p>
          <p className="text-3xl font-bold mt-1 text-emerald-400">{Math.round((data.confidence_score ?? 0) * 100)}%</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Dernière Analyse</p>
          <p className="text-sm font-bold mt-1 text-slate-200">{data.last_analysis ?? "—"}</p>
        </div>
      </div>

      {/* Filter pills */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${filter === f
              ? f !== "tous" ? `${RB[f]} ${RC[f]}` : "bg-white/10 border-white/20 text-white"
              : "border-slate-700 text-slate-400 hover:border-slate-500"}`}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-8">
        {filtered.map(e => {
          const cfg = RISK_CONFIG[e.risk_level] ?? RISK_CONFIG.faible;
          return (
            <button key={e.entity_id} onClick={() => setSelected(e)}
              className={`text-left border rounded-xl p-4 transition-all hover:scale-[1.01] ${RB[e.risk_level]}`}>
              <div className="flex justify-between items-start mb-3">
                <div className="min-w-0">
                  <span className="text-xs font-mono text-slate-500">{e.entity_id}</span>
                  <p className="font-semibold text-sm text-slate-100 line-clamp-1 mt-0.5">{e.name}</p>
                  <p className="text-xs text-slate-400">{e.country}</p>
                </div>
                <div className="shrink-0 ml-3">
                  <GaugeRing value={e.composite_score} stroke={ACCENT} />
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-xs font-semibold uppercase ${cfg.color}`}>{cfg.label}</span>
                <span className="text-xs text-slate-500">Index: <span className="font-bold" style={{ color: ACCENT }}>{e.estimated_lgbtq_rights_index}</span></span>
              </div>
            </button>
          );
        })}
        {filtered.length === 0 && (
          <div className="col-span-full text-center py-12 text-slate-400 text-sm">
            Aucune entité dans ce niveau de risque
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
