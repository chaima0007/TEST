"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface GeoEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  unilateral_deployment_score: number;
  ecological_risk_score: number;
  governance_deficit_score: number;
  dual_use_weaponization_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_geoengineering_index: number;
  last_updated: string;
}

interface GeoSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: GeoEntity[];
  avg_estimated_geoengineering_index: number;
}

interface GeoData {
  entities: GeoEntity[];
  summary: GeoSummary;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const RISK_CONFIG: Record<string, { label: string; color: string; bg: string; border: string }> = {
  critique: { label: "Critique", color: "text-red-400", bg: "bg-red-500/10", border: "border-red-500/25" },
  "élevé": { label: "Élevé", color: "text-orange-400", bg: "bg-orange-500/10", border: "border-orange-500/25" },
  "modéré": { label: "Modéré", color: "text-amber-400", bg: "bg-amber-500/10", border: "border-amber-500/25" },
  faible: { label: "Faible", color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/25" },
};

const FILTER_OPTIONS = [
  { key: "all", label: "Tous" },
  { key: "critique", label: "Critique" },
  { key: "élevé", label: "Élevé" },
  { key: "modéré", label: "Modéré" },
  { key: "faible", label: "Faible" },
];

const PATTERNS = [
  { name: "Déploiement Unilatéral", severity: "critique", signal: "unilateral_deployment_score > 70", action: "Traité international de moratoire sur la géo-ingénierie solaire", test: (e: GeoEntity) => e.unilateral_deployment_score > 70 },
  { name: "Risque Écosystémique", severity: "critique", signal: "ecological_risk_score > 65", action: "Évaluation d'impact environnemental obligatoire transfrontalière", test: (e: GeoEntity) => e.ecological_risk_score > 65 },
  { name: "Vide Gouvernanciel", severity: "élevé", signal: "governance_deficit_score > 60", action: "Création d'un organe ONU de supervision de la géo-ingénierie", test: (e: GeoEntity) => e.governance_deficit_score > 60 },
  { name: "Militarisation Climatique", severity: "élevé", signal: "dual_use_weaponization_score > 55", action: "Renforcement de la Convention ENMOD", test: (e: GeoEntity) => e.dual_use_weaponization_score > 55 },
  { name: "Expérimentation Non Consentie", severity: "modéré", signal: "composite_score > 40", action: "Protocole de consentement préalable des populations affectées", test: (e: GeoEntity) => e.composite_score > 40 },
];

const SEVERITY_STYLE: Record<string, string> = {
  critique: "text-red-400 bg-red-500/10 border-red-500/25",
  "élevé": "text-orange-400 bg-orange-500/10 border-orange-500/25",
  "modéré": "text-amber-400 bg-amber-500/10 border-amber-500/25",
};

// ── Components ────────────────────────────────────────────────────────────────

function GaugeRing({ value, max, label, color }: { value: number; max: number; label: string; color: string }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const r = 36;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="8" />
        <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="8" strokeLinecap="round"
          strokeDasharray={circ} strokeDashoffset={offset} transform="rotate(-90 48 48)"
          style={{ transition: "stroke-dashoffset 0.7s ease" }} />
        <text x="48" y="52" textAnchor="middle" fontSize="14" fontWeight="700" fill="white">{Math.round(value)}</text>
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

function EntityCard({ entity, onClick }: { entity: GeoEntity; onClick: (e: GeoEntity) => void }) {
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  return (
    <button onClick={() => onClick(entity)}
      className={`w-full text-left bg-white/4 border ${cfg.border} rounded-xl p-4 hover:bg-white/7 transition-all`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="min-w-0">
          <p className="font-semibold text-white truncate">{entity.name}</p>
          <p className="text-xs text-gray-400 truncate mt-0.5">{entity.country} · {entity.sector}</p>
        </div>
        <span className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}>{cfg.label}</span>
      </div>
      <div className="grid grid-cols-2 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.unilateral_deployment_score}</p>
          <p className="text-[10px] text-gray-500">Déploiement</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.ecological_risk_score}</p>
          <p className="text-[10px] text-gray-500">Écosystème</p>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">Score: <span className={`font-bold ${cfg.color}`}>{entity.composite_score}</span></span>
        <span className="text-gray-500 truncate ml-2">{entity.primary_pattern}</span>
      </div>
    </button>
  );
}

function DetailModal({ entity, onClose }: { entity: GeoEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  const triggered = PATTERNS.filter((p) => p.test(entity));
  const TABS = [{ key: "scores" as const, label: "Scores" }, { key: "signaux" as const, label: "Signaux" }, { key: "actions" as const, label: "Actions" }];

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
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" /></svg>
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
          {tab === "scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Déploiement Unilatéral", value: `${entity.unilateral_deployment_score}/100` },
                  { label: "Risque Écosystémique", value: `${entity.ecological_risk_score}/100` },
                  { label: "Vide Gouvernanciel", value: `${entity.governance_deficit_score}/100` },
                  { label: "Militarisation", value: `${entity.dual_use_weaponization_score}/100` },
                  { label: "Index Géo-ingénierie", value: `${entity.estimated_geoengineering_index}/10` },
                  { label: "Mis à jour", value: entity.last_updated },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                    <p className="text-sm font-semibold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-white/4 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-300">Score Composite Géo-ingénierie</span>
                  <span className={`text-xl font-bold ${cfg.color}`}>{entity.composite_score}</span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${Math.min(100, entity.composite_score)}%`,
                      backgroundColor: entity.risk_level === "critique" ? "#f87171" : entity.risk_level === "élevé" ? "#fb923c" : entity.risk_level === "modéré" ? "#fbbf24" : "#34d399" }} />
                </div>
                <p className="text-[11px] text-gray-500 mt-1.5">Formule : déploiement×0.30 + écosystème×0.25 + gouvernance×0.25 + militarisation×0.20</p>
              </div>
              <div className="space-y-2">
                <p className="text-xs text-gray-400 font-medium">Signaux Clés</p>
                {entity.key_signals.map((signal, i) => (
                  <div key={i} className="bg-white/4 rounded-lg px-3 py-2 text-xs text-gray-300">{signal}</div>
                ))}
              </div>
            </div>
          )}
          {tab === "signaux" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="text-center py-8 text-gray-400 text-sm">Aucun risque géo-ingénierie critique détecté</div>
              ) : triggered.map((p) => (
                <div key={p.name} className={`rounded-xl border p-4 ${SEVERITY_STYLE[p.severity] ?? ""}`}>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="font-semibold text-sm">{p.name}</span>
                    <span className="ml-auto text-[10px] font-medium uppercase tracking-wide opacity-70">{p.severity}</span>
                  </div>
                  <p className="text-[10px] font-mono opacity-50 mt-1">Signal : {p.signal}</p>
                </div>
              ))}
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="bg-emerald-500/10 border border-emerald-500/25 rounded-xl p-4">
                  <p className="text-sm text-emerald-400 font-medium">Gouvernance Climatique Conforme</p>
                  <p className="text-xs text-emerald-400/70 mt-1">Maintenir les protocoles de surveillance et de transparence internationale.</p>
                </div>
              ) : triggered.map((p, i) => (
                <div key={p.name} className="bg-white/4 border border-white/10 rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="w-6 h-6 rounded-full bg-white/10 text-xs flex items-center justify-center text-gray-300 font-bold">{i + 1}</span>
                    <span className="text-sm font-medium text-white">{p.name}</span>
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed">{p.action}</p>
                </div>
              ))}
              <div className="bg-slate-800/60 border border-white/8 rounded-xl p-4">
                <p className="text-xs text-gray-400"><span className="text-gray-300 font-medium">Pattern Principal :</span> {entity.primary_pattern}</p>
                <p className="text-xs text-gray-400 mt-1"><span className="text-gray-300 font-medium">Index Géo-ingénierie :</span> {entity.estimated_geoengineering_index}/10</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function GeoEngineeringPage() {
  const [data, setData] = useState<GeoData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<GeoEntity | null>(null);

  useEffect(() => {
    fetch("/api/geoengineering-engine")
      .then((r) => r.json())
      .then((json) => {
        const payload = json?.data ?? json;
        setData(payload as GeoData);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const s = data?.summary;
  const entities = data?.entities ?? [];
  const filtered = filter === "all" ? entities : entities.filter((e) => e.risk_level === filter);
  const total = s?.total_entities ?? 0;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Géo-ingénierie & Gouvernance Climatique</h1>
            <p className="text-sm text-gray-400 mt-1">Moteur d&apos;intelligence Swarm — analyse des risques de déploiement unilatéral et de militarisation climatique</p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">{total} entités analysées</span>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && s && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              <KpiCard label="Total Entités" value={s.total_entities} sub="programmes analysés" />
              <KpiCard label="Score Composite Moyen" value={`${s.avg_composite}`}
                sub="sur 100" accent={s.avg_composite >= 60 ? "text-red-400" : s.avg_composite >= 40 ? "text-orange-400" : "text-emerald-400"} />
              <KpiCard label="Entités Critiques" value={s.risk_distribution["critique"] ?? 0} sub="déploiements illicites" accent="text-red-400" />
              <KpiCard label="Index Géo-ingénierie Moyen" value={`${s.avg_estimated_geoengineering_index}/10`} sub="indice de risque" accent="text-indigo-400" />
              <KpiCard label="Confiance Analyse" value={`${s.confidence_score}%`} sub="fiabilité des données" accent="text-emerald-400" />
              <KpiCard label="Alertes Critiques" value={s.critical_alerts.length} sub="interventions urgentes" accent="text-red-400" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs Géo-ingénierie</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing value={s.avg_composite} max={100} label="Score Global" color="#f87171" />
                  <GaugeRing value={s.avg_estimated_geoengineering_index} max={10} label="Index GEO" color="#818cf8" />
                  <GaugeRing value={s.confidence_score} max={100} label="Confiance" color="#34d399" />
                  <GaugeRing value={(s.risk_distribution["critique"] ?? 0) / s.total_entities * 100} max={100} label="% Critique" color="#fb923c" />
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
                    <p className="text-[11px] text-gray-500">Sources de données</p>
                    <p className="text-lg font-bold text-white mt-0.5">{s.data_sources.length}</p>
                  </div>
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Domaine</p>
                    <p className="text-lg font-bold text-indigo-400 mt-0.5">{s.domain}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {FILTER_OPTIONS.map((opt) => {
                const isActive = filter === opt.key;
                const cfg = opt.key !== "all" ? RISK_CONFIG[opt.key] : null;
                const count = opt.key === "all" ? s.total_entities : (s.risk_distribution[opt.key] ?? 0);
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
                <EntityCard key={entity.id} entity={entity} onClick={setSelected} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400 text-sm">Aucune entité dans ce niveau de risque</div>
              )}
            </div>

            {(s.risk_distribution["critique"] ?? 0) > 0 && (
              <div className="bg-red-500/8 border border-red-500/20 rounded-xl px-5 py-4 flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0 animate-pulse" />
                <div>
                  <p className="text-sm font-medium text-red-400">
                    {s.risk_distribution["critique"]} programme{(s.risk_distribution["critique"] ?? 0) > 1 ? "s" : ""} en situation critique de déploiement unilatéral
                  </p>
                  <p className="text-xs text-red-400/70 mt-0.5">
                    Programme le plus à risque : <span className="font-medium">{s.top_risk_entities[0]}</span>
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
