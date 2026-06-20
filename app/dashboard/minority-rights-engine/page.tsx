"use client";
import { useState, useEffect } from "react";

const ACCENT = "#0891b2";
const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

interface MREntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  cultural_linguistic_suppression_score: number;
  political_exclusion_score: number;
  economic_marginalization_score: number;
  physical_security_threat_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_minority_rights_index: number;
  last_updated: string;
}

interface MRSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  critical_alerts: number;
  last_analysis: string;
  engine_version: string;
  data_sources: string[];
  entities: MREntity[];
  avg_estimated_minority_rights_index: number;
}

interface MRData {
  entities: MREntity[];
  summary: MRSummary;
}

function GaugeRing({ value, max, label, color }: { value: number; max: number; label: string; color: string }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const r = 36;
  const circumference = 226.19;
  const offset = circumference - (pct / 100) * circumference;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8" strokeLinecap="round"
          strokeDasharray={circumference} strokeDashoffset={offset} transform="rotate(-90 44 44)"
          style={{ transition: "stroke-dashoffset 0.7s ease" }} />
        <text x="44" y="48" textAnchor="middle" fontSize="13" fontWeight="700" fill="white">{Math.round(value)}</text>
      </svg>
      <span className="text-xs text-gray-400 text-center leading-tight">{label}</span>
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

function EntityCard({ entity, onClick }: { entity: MREntity; onClick: (e: MREntity) => void }) {
  const rb = RB[entity.risk_level] ?? RB.faible;
  const rc = RC[entity.risk_level] ?? RC.faible;
  return (
    <button onClick={() => onClick(entity)}
      className={`w-full text-left bg-white/4 border rounded-xl p-4 hover:bg-white/7 transition-all ${rb}`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="min-w-0">
          <p className="font-semibold text-white truncate">{entity.name}</p>
          <p className="text-xs text-gray-400 truncate mt-0.5">{entity.country} · {entity.sector}</p>
        </div>
        <span className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${rb} ${rc}`}>
          {entity.risk_level}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.cultural_linguistic_suppression_score}</p>
          <p className="text-[10px] text-gray-500">Suppression Cult.</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.political_exclusion_score}</p>
          <p className="text-[10px] text-gray-500">Exclusion Polit.</p>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">Score: <span className={`font-bold ${rc}`}>{entity.composite_score}</span></span>
        <span className="text-gray-500 truncate ml-2">MR: {entity.estimated_minority_rights_index}/10</span>
      </div>
    </button>
  );
}

function DetailModal({ entity, onClose }: { entity: MREntity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "signaux" | "contexte">("apercu");
  const rb = RB[entity.risk_level] ?? RB.faible;
  const rc = RC[entity.risk_level] ?? RC.faible;
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
              <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${rb} ${rc}`}>{entity.risk_level}</span>
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
                  { label: "Suppression Culturelle & Linguistique", value: `${entity.cultural_linguistic_suppression_score}/100` },
                  { label: "Exclusion Politique", value: `${entity.political_exclusion_score}/100` },
                  { label: "Marginalisation Économique", value: `${entity.economic_marginalization_score}/100` },
                  { label: "Menace Sécurité Physique", value: `${entity.physical_security_threat_score}/100` },
                  { label: "Indice MR", value: `${entity.estimated_minority_rights_index}/10` },
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
                  <span className={`text-xl font-bold ${rc}`}>{entity.composite_score}</span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${Math.min(100, entity.composite_score)}%`, backgroundColor: ACCENT }} />
                </div>
              </div>
            </div>
          )}
          {tab === "signaux" && (
            <div className="space-y-3">
              {entity.key_signals.map((signal, i) => (
                <div key={i} className={`rounded-xl border p-4 ${rb}`}>
                  <p className={`text-sm font-medium ${rc}`}>{signal}</p>
                </div>
              ))}
              <div className={`rounded-xl border p-4 ${rb}`}>
                <p className={`text-sm font-semibold ${rc}`}>{entity.primary_pattern}</p>
                <p className={`text-xs mt-1 ${rc} opacity-70`}>Niveau de risque: {entity.risk_level}</p>
              </div>
            </div>
          )}
          {tab === "contexte" && (
            <div className="space-y-3">
              <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                <p className="text-sm font-medium text-white mb-2">{entity.primary_pattern}</p>
                <p className="text-xs text-gray-300 leading-relaxed">
                  Renforcer les mécanismes de protection des droits des minorités et mettre en œuvre des politiques inclusives contre la suppression culturelle systémique.
                </p>
              </div>
              <div className="bg-slate-800/60 border border-white/8 rounded-xl p-4 space-y-1">
                <p className="text-xs text-gray-400"><span className="text-gray-300 font-medium">Pays :</span> {entity.country}</p>
                <p className="text-xs text-gray-400"><span className="text-gray-300 font-medium">Secteur :</span> {entity.sector}</p>
                <p className="text-xs text-gray-400"><span className="text-gray-300 font-medium">Analyse :</span> {entity.last_updated}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function MinorityRightsEnginePage() {
  const [data, setData] = useState<MRData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<MREntity | null>(null);

  useEffect(() => {
    fetch("/api/minority-rights-engine")
      .then((r) => r.json())
      .then((json) => {
        const payload = json?.data ?? json;
        setData(payload as MRData);
        setLoading(false);
      })
      .catch(() => setLoading(false));
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
            <h1 className="text-2xl font-bold text-white">Minority Rights Engine</h1>
            <p className="text-sm text-gray-400 mt-1">Droits des Minorités &amp; Suppression Culturelle Systémique</p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {total} entités analysées
          </span>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin" style={{ borderColor: `${ACCENT} transparent transparent transparent` }} />
          </div>
        )}

        {!loading && s && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              <KpiCard label="Entités analysées" value={s.total_entities} sub="groupes surveillés" />
              <KpiCard label="Score composite moyen" value={s.avg_composite.toFixed(1)} sub="indice agrégé"
                accent={s.avg_composite >= 60 ? "text-red-400" : s.avg_composite >= 40 ? "text-orange-400" : "text-emerald-400"} />
              <KpiCard label="Cas critiques" value={s.critical_alerts} sub="intervention urgente" accent="text-red-400" />
              <KpiCard label="Indice MR moyen" value={`${s.avg_estimated_minority_rights_index?.toFixed(1) ?? "—"}/10`} sub="droits minorités" accent="text-cyan-400" />
              <KpiCard label="Sources de données" value={s.data_sources?.length ?? 0} sub="ONU/MRG/OSCE" accent="text-violet-400" />
              <KpiCard label="Dernière analyse" value={s.last_analysis ?? "—"} sub="mise à jour" accent="text-indigo-400" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs Droits des Minorités</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing value={s.avg_composite} max={100} label="Score Composite" color={ACCENT} />
                  <GaugeRing value={s.risk_distribution["critique"] ?? 0} max={s.total_entities} label="Critique" color="#ef4444" />
                  <GaugeRing value={s.risk_distribution["élevé"] ?? 0} max={s.total_entities} label="Élevé" color="#fb923c" />
                  <GaugeRing value={s.avg_estimated_minority_rights_index ?? 0} max={10} label="Indice MR" color="#22d3ee" />
                </div>
              </div>

              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Distribution par Niveau de Risque</h2>
                <div className="space-y-4">
                  <DistBar label="Critique" count={s.risk_distribution["critique"] ?? 0} total={s.total_entities} color="#f87171" />
                  <DistBar label="Élevé" count={s.risk_distribution["élevé"] ?? 0} total={s.total_entities} color="#fb923c" />
                  <DistBar label="Modéré" count={s.risk_distribution["modéré"] ?? 0} total={s.total_entities} color="#fbbf24" />
                  <DistBar label="Faible" count={s.risk_distribution["faible"] ?? 0} total={s.total_entities} color="#34d399" />
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
              {(["tous", "critique", "élevé", "modéré", "faible"] as const).map((key) => {
                const isActive = filter === key;
                const count = key === "tous" ? s.total_entities : (s.risk_distribution[key] ?? 0);
                return (
                  <button key={key} onClick={() => setFilter(key)}
                    className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${isActive
                      ? key !== "tous" ? `${RB[key]} ${RC[key]}` : "bg-white/10 border-white/20 text-white"
                      : "bg-transparent border-white/10 text-gray-400 hover:text-white hover:border-white/20"}`}>
                    {key.charAt(0).toUpperCase() + key.slice(1)}
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
              <div className="bg-red-500/8 border border-red-500/20 rounded-xl px-5 py-4 flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0 animate-pulse" />
                <div>
                  <p className="text-sm font-medium text-red-400">
                    {s.critical_alerts} entité{s.critical_alerts > 1 ? "s" : ""} en situation critique de suppression des droits des minorités
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
