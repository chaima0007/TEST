"use client";
import { useState, useEffect } from "react";

const RC: Record<string,string> = { critique:"text-red-400","élevé":"text-orange-400",modéré:"text-yellow-400",faible:"text-emerald-400" };
const RB: Record<string,string> = { critique:"border-red-500/30 bg-red-500/10","élevé":"border-orange-500/30 bg-orange-500/10",modéré:"border-yellow-500/30 bg-yellow-500/10",faible:"border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#f97316";

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

interface HSPREntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  online_hate_escalation_violence_severity_score: number;
  content_moderation_bias_minority_targeting_score: number;
  platform_impunity_accountability_gap_score: number;
  victim_legal_redress_absence_scale_score: number;
  estimated_hate_speech_platform_rights_index: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  last_updated: string;
  data_sources?: string[];
  [key: string]: unknown;
}

interface HSPRData {
  total_entities: number;
  avg_composite: number;
  avg_estimated_hate_speech_platform_rights_index: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  confidence_score: number;
  data_sources: string[];
  entities: HSPREntity[];
  [key: string]: unknown;
}

const SUB_KEYS = [
  { key: "online_hate_escalation_violence_severity_score",     label: "Escalade Haine → Violence" },
  { key: "content_moderation_bias_minority_targeting_score",   label: "Biais Modération Minorités" },
  { key: "platform_impunity_accountability_gap_score",         label: "Impunité Plateforme" },
  { key: "victim_legal_redress_absence_scale_score",           label: "Absence Recours Victimes" },
];

function DistBar({ label, value, total, color }: { label: string; value: number; total: number; color: string }) {
  const p = total > 0 ? Math.round((value / total) * 100) : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-44 shrink-0">{label}</span>
      <div className="flex-1 h-2.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${p}%`, backgroundColor: color }} />
      </div>
      <span className="text-xs text-slate-300 w-6 text-right">{value}</span>
    </div>
  );
}

function DetailModal({ entity, onClose, dataSources }: { entity: HSPREntity; onClose: () => void; dataSources: string[] }) {
  const [tab, setTab] = useState<"Aperçu" | "Métriques" | "Sources">("Aperçu");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-orange-500/30 rounded-2xl w-full max-w-lg mx-4 max-h-[85vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800 flex justify-between items-start">
          <div>
            <p className="text-xs font-mono text-slate-500 mb-1">{entity.entity_id}</p>
            <h3 className="font-bold text-lg text-white">{entity.name}</h3>
            <p className="text-xs text-slate-400 mt-1">{entity.country} · {entity.sector}</p>
            <p className={`text-xs font-bold uppercase mt-1 ${RC[entity.risk_level]}`}>{entity.risk_level}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">×</button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["Aperçu", "Métriques", "Sources"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${tab === t ? "border-b-2 text-orange-400" : "text-slate-500 hover:text-slate-300"}`}
              style={tab === t ? { borderColor: ACCENT } : {}}>
              {t}
            </button>
          ))}
        </div>

        <div className="p-6">
          {tab === "Aperçu" && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <GaugeRing value={entity.composite_score} stroke={ACCENT} />
                <div>
                  <div className="text-2xl font-bold" style={{ color: ACCENT }}>{entity.composite_score.toFixed(1)}</div>
                  <div className="text-xs text-slate-400">Score composite</div>
                  <div className="text-xs text-slate-500 mt-1">Pattern: {entity.primary_pattern}</div>
                </div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-500 mb-1">Index Discours de Haine &amp; Plateformes</div>
                <div className="text-lg font-bold" style={{ color: ACCENT }}>{entity.estimated_hate_speech_platform_rights_index} / 10</div>
              </div>
              <ul className="space-y-2">
                {entity.key_signals.map((s, i) => (
                  <li key={i} className="flex gap-2 text-sm text-slate-300">
                    <span style={{ color: ACCENT }} className="shrink-0 mt-0.5">›</span>{s}
                  </li>
                ))}
              </ul>
              <p className="text-xs text-slate-600">Mis à jour: {entity.last_updated}</p>
            </div>
          )}

          {tab === "Métriques" && (
            <div className="space-y-3">
              {SUB_KEYS.map(({ key, label }, i) => {
                const val = entity[key] as number;
                const colors = [ACCENT, "#fb923c", "#fdba74", "#fed7aa"];
                return (
                  <div key={key}>
                    <div className="flex justify-between text-xs text-slate-400 mb-1">
                      <span>{label}</span><span>{val}/100</span>
                    </div>
                    <div className="h-2 bg-slate-800 rounded-full">
                      <div className="h-full rounded-full" style={{ width: `${val}%`, backgroundColor: colors[i] }} />
                    </div>
                  </div>
                );
              })}
              <div className="pt-2 flex justify-between text-sm border-t border-slate-800">
                <span className="text-slate-400">Index estimé</span>
                <span className="font-bold" style={{ color: ACCENT }}>{entity.estimated_hate_speech_platform_rights_index} / 10</span>
              </div>
            </div>
          )}

          {tab === "Sources" && (
            <div className="space-y-3">
              <p className="text-xs text-slate-500 mb-2">Sources de données utilisées pour cette entité :</p>
              <div className="flex flex-wrap gap-2">
                {(entity.data_sources ?? dataSources).map((src, i) => (
                  <span key={i} className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs border border-slate-700">{src}</span>
                ))}
              </div>
              <div className="bg-slate-800 rounded-lg p-3 mt-3">
                <div className="text-xs text-slate-500 mb-1">Niveau de risque</div>
                <div className={`text-sm font-bold ${RC[entity.risk_level]}`}>{entity.risk_level.toUpperCase()}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-500 mb-1">Pattern principal détecté</div>
                <div className="text-sm font-mono text-orange-300">{entity.primary_pattern}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function HateSpeechPlatformRightsPage() {
  const [data, setData] = useState<HSPRData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [sel, setSel] = useState<HSPREntity | null>(null);

  useEffect(() => {
    fetch("/api/hate-speech-platform-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement des données sur les discours de haine…</div>
    </div>
  );
  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400">Données indisponibles</div>
    </div>
  );

  const entities = data.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter);
  const dist = data.risk_distribution ?? {};
  const patDist = data.pattern_distribution ?? {};

  const avgSub = (key: string) => {
    const vals = entities.map(e => e[key] as number).filter(v => typeof v === "number");
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {sel && <DetailModal entity={sel} onClose={() => setSel(null)} dataSources={data.data_sources ?? []} />}
      <div className="max-w-7xl mx-auto space-y-6">

        <div>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-3 h-3 rounded-full animate-pulse" style={{ backgroundColor: ACCENT }} />
            <h1 className="text-2xl font-bold tracking-tight" style={{ color: ACCENT }}>Discours de Haine &amp; Plateformes</h1>
          </div>
          <p className="text-slate-400 text-sm ml-6">Escalade de la haine en ligne, biais de modération et impunité des plateformes numériques</p>
          <p className="text-slate-600 text-xs ml-6 mt-0.5">Caelum Partners · Hate Speech Platform Rights Engine · {data.last_analysis}</p>
        </div>

        {/* Critical Alerts */}
        {(data.critical_alerts?.length ?? 0) > 0 && (
          <div className="border border-orange-500/30 bg-orange-500/10 rounded-xl p-4">
            <h2 className="text-sm font-semibold text-orange-400 mb-2">Alertes Critiques</h2>
            <ul className="space-y-1">
              {data.critical_alerts.map((a, i) => (
                <li key={i} className="text-sm text-slate-300 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: ACCENT }} />
                  {a}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* KPI Cards 3×2 */}
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "Entités Analysées", value: data.total_entities },
            { label: "Score Moyen",        value: (data.avg_composite ?? 0).toFixed(1) },
            { label: "Index Moyen",        value: (data.avg_estimated_hate_speech_platform_rights_index ?? 0).toFixed(2) },
            { label: "Critique",           value: dist.critique ?? 0 },
            { label: "Élevé",              value: dist["élevé"] ?? 0 },
            { label: "Confiance",          value: `${Math.round((data.confidence_score ?? 0) * 100)}%` },
          ].map(k => (
            <div key={k.label} className="bg-slate-900 border border-orange-500/20 rounded-xl p-4">
              <div className="text-xs text-slate-500 mb-1">{k.label}</div>
              <div className="text-xl font-bold" style={{ color: ACCENT }}>{k.value}</div>
            </div>
          ))}
        </div>

        {/* Gauge Rings */}
        <div className="bg-slate-900 border border-orange-500/20 rounded-xl p-6">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4">Sous-scores Moyens</h2>
          <div className="flex flex-wrap justify-around gap-6">
            {SUB_KEYS.map(({ key, label }, i) => {
              const colors = [ACCENT, "#fb923c", "#fdba74", "#fed7aa"];
              return (
                <div key={key} className="flex flex-col items-center gap-2">
                  <GaugeRing value={avgSub(key)} stroke={colors[i]} />
                  <span className="text-xs text-slate-400 text-center max-w-[100px]">{label}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Distribution Bars */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-orange-500/20 rounded-xl p-5">
            <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Distribution des Niveaux de Risque</h2>
            <div className="space-y-2">
              <DistBar label="Critique" value={dist.critique ?? 0} total={entities.length} color="#ef4444" />
              <DistBar label="Élevé"    value={dist["élevé"] ?? 0} total={entities.length} color="#f97316" />
              <DistBar label="Modéré"   value={dist.modéré ?? 0}   total={entities.length} color="#eab308" />
              <DistBar label="Faible"   value={dist.faible ?? 0}   total={entities.length} color="#10b981" />
            </div>
          </div>
          <div className="bg-slate-900 border border-orange-500/20 rounded-xl p-5">
            <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Patterns de Discours de Haine</h2>
            <div className="space-y-2">
              {Object.entries(patDist).map(([k, v], i) => (
                <DistBar key={k} label={k.replace(/_/g, " ")} value={v} total={entities.length}
                  color={[ACCENT, "#fb923c", "#fdba74", "#fed7aa", "#fff7ed"][i % 5]} />
              ))}
            </div>
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex gap-2 flex-wrap">
          {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
            <button key={f} onClick={() => setFilter(f)}
              className={`px-4 py-1.5 rounded-full text-sm border transition-all capitalize ${filter === f ? "text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}
              style={filter === f ? { backgroundColor: ACCENT, borderColor: ACCENT } : {}}>
              {f}
            </button>
          ))}
          <span className="ml-auto text-xs text-slate-500 self-center">
            {filtered.length} entité{filtered.length !== 1 ? "s" : ""}
          </span>
        </div>

        {/* Entity Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map(entity => (
            <div key={entity.entity_id} onClick={() => setSel(entity)}
              className={`bg-slate-900 border rounded-xl p-4 cursor-pointer hover:border-orange-500/50 transition-all ${RB[entity.risk_level] ?? "border-slate-800"}`}>
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-mono text-slate-500">{entity.entity_id}</p>
                  <p className="text-sm font-semibold text-white truncate">{entity.name}</p>
                  <p className="text-xs text-slate-500">{entity.country}</p>
                </div>
                <GaugeRing value={entity.composite_score} stroke={ACCENT} />
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full mb-2">
                <div className="h-full rounded-full" style={{ width: `${entity.composite_score}%`, backgroundColor: ACCENT }} />
              </div>
              <div className="flex justify-between text-xs">
                <span className={RC[entity.risk_level]}>{entity.risk_level}</span>
                <span className="text-slate-500">idx {entity.estimated_hate_speech_platform_rights_index}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Data Sources Footer */}
        {(data.data_sources?.length ?? 0) > 0 && (
          <div className="bg-slate-900 border border-orange-500/20 rounded-xl p-4">
            <p className="text-xs text-slate-500">
              Sources :{" "}
              {data.data_sources.map(src => (
                <span key={src} className="inline-block bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-xs mr-2 mb-1">{src}</span>
              ))}
              · v{data.engine_version} · Confiance {Math.round((data.confidence_score ?? 0) * 100)}%
            </p>
          </div>
        )}

        <p className="text-xs text-slate-600 text-center">Caelum Partners · Discours de Haine &amp; Plateformes · {data.last_analysis}</p>
      </div>
    </div>
  );
}
