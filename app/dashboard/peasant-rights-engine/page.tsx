"use client";
import { useState, useEffect } from "react";

const ACCENT = "#65a30d";
const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

interface PeasantRightsEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  land_dispossession_score: number;
  seed_criminalization_score: number;
  legal_framework_absence_score: number;
  corporate_agro_domination_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_peasant_rights_index: number;
  last_updated: string;
}

interface PeasantRightsSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  critical_alerts: number;
  last_analysis: string;
  engine_version: string;
  data_sources: string[];
  avg_estimated_peasant_rights_index: number;
}

interface PeasantRightsData {
  entities: PeasantRightsEntity[];
  summary: PeasantRightsSummary;
}

const RISK_CONFIG: Record<string, { label: string; color: string; bg: string; border: string; dot: string }> = {
  critique: { label: "Critique", color: "text-red-400", bg: "bg-red-500/10", border: "border-red-500/25", dot: "bg-red-500" },
  "élevé": { label: "Élevé", color: "text-orange-400", bg: "bg-orange-500/10", border: "border-orange-500/25", dot: "bg-orange-500" },
  modéré: { label: "Modéré", color: "text-yellow-400", bg: "bg-yellow-500/10", border: "border-yellow-500/25", dot: "bg-yellow-500" },
  faible: { label: "Faible", color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/25", dot: "bg-emerald-500" },
};

const FILTER_OPTIONS = [
  { key: "tous", label: "Tous" },
  { key: "critique", label: "Critique" },
  { key: "élevé", label: "Élevé" },
  { key: "modéré", label: "Modéré" },
  { key: "faible", label: "Faible" },
];

function GaugeRing({ value, max, label, color }: { value: number; max: number; label: string; color: string }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const r = 36;
  const circ = 226.19;
  const offset = circ - (pct / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8" strokeLinecap="round"
          strokeDasharray={`${(pct / 100) * 226.19} 226.19`} strokeDashoffset={offset} transform="rotate(-90 44 44)"
          style={{ transition: "stroke-dashoffset 0.7s ease" }} />
        <text x="44" y="48" textAnchor="middle" fontSize="13" fontWeight="700" fill="white">{Math.round(value)}</text>
      </svg>
      <span className="text-xs text-gray-400 text-center leading-tight">{label}</span>
    </div>
  );
}

function DistBar({ label, count, total, color }: { label: string; count: number; total: number; color: string }) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-gray-300">{label}</span>
        <span className="text-gray-400">{count} <span className="text-gray-600">({pct}%)</span></span>
      </div>
      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-white/4 border border-white/10 rounded-xl px-5 py-4 hover:bg-white/6 transition-colors">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function EntityCard({ entity, onClick }: { entity: PeasantRightsEntity; onClick: (e: PeasantRightsEntity) => void }) {
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  return (
    <button onClick={() => onClick(entity)}
      className={`w-full text-left bg-white/4 border ${cfg.border} rounded-xl p-4 hover:bg-white/7 transition-all`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="min-w-0">
          <p className="font-semibold text-white truncate">{entity.name}</p>
          <p className="text-xs text-gray-400 truncate mt-0.5">{entity.country} · {entity.sector}</p>
        </div>
        <span className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}>
          {cfg.label}
        </span>
      </div>
      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.land_dispossession_score}</p>
          <p className="text-[10px] text-gray-500">Dépossession</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.seed_criminalization_score}</p>
          <p className="text-[10px] text-gray-500">Semences</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.corporate_agro_domination_score}</p>
          <p className="text-[10px] text-gray-500">Agro-Corp</p>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">Score: <span className={`font-bold ${cfg.color}`}>{entity.composite_score}</span></span>
        <span className="text-gray-500 truncate ml-2">{entity.primary_pattern?.slice(0, 22)}…</span>
      </div>
    </button>
  );
}

function DetailModal({ entity, onClose }: { entity: PeasantRightsEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "signaux" | "contexte">("apercu");
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  const TABS = [
    { key: "apercu" as const, label: "Aperçu" },
    { key: "signaux" as const, label: "Signaux" },
    { key: "contexte" as const, label: "Contexte" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="w-full max-w-xl bg-slate-900 border border-white/12 rounded-2xl shadow-2xl overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="px-6 pt-6 pb-4 border-b border-white/8">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-white">{entity.name}</h2>
              <p className="text-sm text-gray-400 mt-0.5">{entity.country} · {entity.sector}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}>{cfg.label}</span>
              <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors ml-1">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
              </button>
            </div>
          </div>
          <div className="flex gap-1 mt-4">
            {TABS.map((t) => (
              <button key={t.key} onClick={() => setTab(t.key)}
                className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${tab === t.key ? "bg-white/10 text-white" : "text-gray-400 hover:text-white"}`}>
                {t.label}
              </button>
            ))}
          </div>
        </div>
        <div className="px-6 py-5 space-y-4 max-h-[60vh] overflow-y-auto">
          {tab === "apercu" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Dépossession Terres", value: `${entity.land_dispossession_score}/100` },
                  { label: "Criminalisation Semences", value: `${entity.seed_criminalization_score}/100` },
                  { label: "Absence Cadre Légal", value: `${entity.legal_framework_absence_score}/100` },
                  { label: "Domination Agro-Corp", value: `${entity.corporate_agro_domination_score}/100` },
                  { label: "Indice Droits Paysans", value: `${entity.estimated_peasant_rights_index}/10` },
                  { label: "Dernière mise à jour", value: entity.last_updated },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                    <p className="text-sm font-semibold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-white/4 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-300">Score Composite</span>
                  <span className={`text-xl font-bold ${cfg.color}`}>{entity.composite_score}</span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${Math.min(100, entity.composite_score)}%`, backgroundColor: ACCENT }} />
                </div>
                <p className="text-[11px] text-gray-500 mt-1.5">
                  Formule : dépossession×0.30 + semences×0.25 + cadre légal×0.25 + agro-corp×0.20
                </p>
              </div>
            </div>
          )}
          {tab === "signaux" && (
            <div className="space-y-3">
              {entity.key_signals?.map((signal, i) => (
                <div key={i} className={`rounded-xl border p-4 ${cfg.bg} ${cfg.border}`}>
                  <p className={`text-sm font-medium ${cfg.color}`}>{signal}</p>
                </div>
              ))}
              <div className={`rounded-xl border p-4 ${cfg.bg} ${cfg.border}`}>
                <p className={`text-sm font-semibold ${cfg.color}`}>{entity.primary_pattern}</p>
                <p className={`text-xs mt-1 ${cfg.color} opacity-70`}>Niveau de risque: {entity.risk_level}</p>
              </div>
            </div>
          )}
          {tab === "contexte" && (
            <div className="space-y-3">
              <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                <p className="text-xs text-gray-400"><span className="text-gray-300 font-medium">Région :</span> {entity.country}</p>
                <p className="text-xs text-gray-400 mt-1"><span className="text-gray-300 font-medium">Secteur :</span> {entity.sector}</p>
                <p className="text-xs text-gray-400 mt-1"><span className="text-gray-300 font-medium">Analyse :</span> {entity.last_updated}</p>
                <p className="text-xs text-gray-400 mt-1"><span className="text-gray-300 font-medium">Indice Droits Paysans :</span> {entity.estimated_peasant_rights_index}/10</p>
              </div>
              <div className={`rounded-xl border p-4 ${cfg.bg} ${cfg.border}`}>
                <p className={`text-sm font-semibold ${cfg.color}`}>{entity.primary_pattern}</p>
                <p className="text-xs text-gray-400 mt-2">Renforcer les droits fonciers, protéger la souveraineté semencière et encadrer les pratiques des multinationales agro-alimentaires.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function PeasantRightsEnginePage() {
  const [data, setData] = useState<PeasantRightsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<PeasantRightsEntity | null>(null);

  useEffect(() => {
    fetch("/api/peasant-rights-engine")
      .then((r) => r.json())
      .then((d) => {
        setData(d.data ?? d);
        setLoading(false);
      })
      .catch(console.error);
  }, []);

  const s = data?.summary;
  const entities = data?.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter((e) => e.risk_level === filter);
  const total = s?.total_entities ?? 0;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Droits des Paysans</h1>
            <p className="text-sm text-gray-400 mt-1">
              Droits Paysans &amp; Souveraineté Alimentaire
            </p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {total} entités analysées
          </span>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin" style={{ borderColor: ACCENT, borderTopColor: "transparent" }} />
          </div>
        )}

        {!loading && s && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              <KpiCard label="Entités analysées" value={s.total_entities} sub="zones surveillées" />
              <KpiCard label="Score composite moyen" value={s.avg_composite?.toFixed(1) ?? "—"} sub="indice agrégé"
                accent={s.avg_composite >= 60 ? "text-red-400" : s.avg_composite >= 40 ? "text-orange-400" : "text-emerald-400"} />
              <KpiCard label="Cas critiques" value={s.critical_alerts} sub="intervention urgente" accent="text-red-400" />
              <KpiCard label="Indice Droits Paysans Moyen" value={`${s.avg_estimated_peasant_rights_index ?? "—"}/10`} sub="peasant rights index" accent="text-lime-400" />
              <KpiCard label="Sources de données" value={s.data_sources?.length ?? 0} sub="organismes ONU/ONG" accent="text-violet-400" />
              <KpiCard label="Dernière analyse" value={s.last_analysis ?? "—"} sub="mise à jour" accent="text-gray-300" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs Droits des Paysans</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing value={s.avg_composite} max={100} label="Score Composite" color={ACCENT} />
                  <GaugeRing value={s.risk_distribution?.["critique"] ?? 0} max={s.total_entities} label="Critique" color="#ef4444" />
                  <GaugeRing value={s.risk_distribution?.["élevé"] ?? 0} max={s.total_entities} label="Élevé" color="#fb923c" />
                  <GaugeRing value={s.avg_estimated_peasant_rights_index ?? 0} max={10} label="Indice Droits" color={ACCENT} />
                </div>
              </div>

              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Distribution par Niveau de Risque</h2>
                <div className="space-y-4">
                  <DistBar label="Critique" count={s.risk_distribution?.["critique"] ?? 0} total={s.total_entities} color="#f87171" />
                  <DistBar label="Élevé" count={s.risk_distribution?.["élevé"] ?? 0} total={s.total_entities} color="#fb923c" />
                  <DistBar label="Modéré" count={s.risk_distribution?.["modéré"] ?? 0} total={s.total_entities} color="#fbbf24" />
                  <DistBar label="Faible" count={s.risk_distribution?.["faible"] ?? 0} total={s.total_entities} color="#34d399" />
                </div>
                <div className="mt-5 pt-4 border-t border-white/8 grid grid-cols-2 gap-3">
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Dernière analyse</p>
                    <p className="text-sm font-bold text-white mt-0.5">{s.last_analysis}</p>
                  </div>
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Version moteur</p>
                    <p className="text-lg font-bold mt-0.5" style={{ color: ACCENT }}>{s.engine_version}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {FILTER_OPTIONS.map((opt) => {
                const isActive = filter === opt.key;
                const cfg = opt.key !== "tous" ? RISK_CONFIG[opt.key] : null;
                const count = opt.key === "tous" ? s.total_entities : (s.risk_distribution?.[opt.key] ?? 0);
                return (
                  <button key={opt.key} onClick={() => setFilter(opt.key)}
                    className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${isActive
                      ? cfg ? `${cfg.bg} ${cfg.border} ${cfg.color}` : "bg-white/10 border-white/20 text-white"
                      : "bg-transparent border-white/10 text-gray-400 hover:text-white hover:border-white/20"}`}>
                    {opt.label}
                    <span className="ml-1.5 text-xs opacity-70">{count}</span>
                  </button>
                );
              })}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filtered.map((entity) => (
                <EntityCard key={entity.entity_id} entity={entity} onClick={setSelected} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400 text-sm">
                  Aucune entité dans ce niveau de risque
                </div>
              )}
            </div>

            {s.critical_alerts > 0 && (
              <div className="rounded-xl px-5 py-4 flex items-start gap-3" style={{ backgroundColor: "rgba(101,163,13,0.08)", border: "1px solid rgba(101,163,13,0.2)" }}>
                <div className="w-2 h-2 rounded-full mt-1.5 shrink-0 animate-pulse" style={{ backgroundColor: ACCENT }} />
                <div>
                  <p className="text-sm font-medium" style={{ color: ACCENT }}>
                    {s.critical_alerts} entité{s.critical_alerts > 1 ? "s" : ""} en situation critique de violation des droits paysans
                  </p>
                  <p className="text-xs mt-0.5" style={{ color: `${ACCENT}b3` }}>
                    Intervention immédiate requise — protection des droits fonciers et semenciers prioritaire
                  </p>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
