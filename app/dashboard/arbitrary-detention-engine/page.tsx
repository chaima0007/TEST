"use client";
import { useEffect, useState } from "react";

interface ADEntity {
  id: string; name: string; country: string; sector: string;
  composite_score: number; extrajudicial_detention_scale_score: number;
  incommunicado_torture_score: number; political_prisoner_profile_score: number;
  due_process_denial_score: number; risk_level: string; primary_pattern: string;
  key_signals: string[]; estimated_arbitrary_detention_index: number; last_updated: string;
}
interface ADSummary {
  total_entities: number; avg_composite: number;
  risk_distribution: Record<string, number>; pattern_distribution: Record<string, number>;
  top_risk_entities: string[]; critical_alerts: string[];
  last_analysis: string; engine_version: string; domain: string;
  confidence_score: number; data_sources: string[]; entities: ADEntity[];
  avg_estimated_arbitrary_detention_index: number;
}

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#be123c";

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36, c = 2 * Math.PI * r, d = Math.min(value / 100, 1);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={`${d * c} ${c}`} strokeDashoffset={c / 4} strokeLinecap="round"
          transform="rotate(-90 44 44)" style={{ transition: "stroke-dasharray .6s" }} />
        <text x="44" y="48" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">{Math.round(d * 100)}%</text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ label, value, total, color }: { label: string; value: number; total: number; color: string }) {
  const p = total > 0 ? Math.round(value / total * 100) : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-52 shrink-0">{label}</span>
      <div className="flex-1 h-2.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${p}%`, backgroundColor: color }} />
      </div>
      <span className="text-xs text-slate-300 w-6 text-right">{value}</span>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: ADEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"Aperçu" | "Signaux" | "Contexte">("Aperçu");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg mx-4 p-6" onClick={e => e.stopPropagation()}>
        <div className="flex justify-between mb-4">
          <div>
            <p className="font-bold text-white text-lg">{entity.name}</p>
            <p className="text-xs text-slate-400">{entity.country} · {entity.sector}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["Aperçu", "Signaux", "Contexte"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded-full text-xs border ${tab === t ? "text-white" : "bg-slate-800 border-slate-700 text-slate-400"}`}
              style={tab === t ? { backgroundColor: ACCENT, borderColor: ACCENT } : {}}>
              {t}
            </button>
          ))}
        </div>
        {tab === "Aperçu" && (
          <div className="space-y-3">
            {[
              { l: "Détention Extrajud.", v: entity.extrajudicial_detention_scale_score, c: "#ef4444" },
              { l: "Incommunicado/Torture", v: entity.incommunicado_torture_score, c: "#f97316" },
              { l: "Prisonnier Politique", v: entity.political_prisoner_profile_score, c: "#a855f7" },
              { l: "Déni Procès Équitable", v: entity.due_process_denial_score, c: "#f59e0b" },
            ].map(({ l, v, c }) => (
              <div key={l}>
                <div className="flex justify-between text-xs text-slate-400 mb-1"><span>{l}</span><span>{v}/100</span></div>
                <div className="h-2 bg-slate-800 rounded-full"><div className="h-full rounded-full" style={{ width: `${v}%`, backgroundColor: c }} /></div>
              </div>
            ))}
            <div className="pt-2 flex justify-between text-sm">
              <span className="text-slate-400">Indice Détention Arbitraire</span>
              <span className="font-bold" style={{ color: ACCENT }}>{entity.estimated_arbitrary_detention_index}</span>
            </div>
          </div>
        )}
        {tab === "Signaux" && (
          <ul className="space-y-2">
            {entity.key_signals.map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-300"><span style={{ color: ACCENT }}>›</span>{s}</li>
            ))}
          </ul>
        )}
        {tab === "Contexte" && (
          <div className="text-sm space-y-2 text-slate-300">
            <p className="text-xs text-slate-500 mb-2">Pattern: <span style={{ color: ACCENT }}>{entity.primary_pattern.replace(/_/g, " ")}</span></p>
            {entity.risk_level === "critique" && <><p>› Mécanismes d'urgence de libération des détenus politiques</p><p>› Pressions diplomatiques internationales contre les détentions arbitraires</p><p>› Programmes d'aide juridique d'urgence pour prisonniers politiques</p></>}
            {entity.risk_level === "élevé" && <><p>› Renforcement des garanties judiciaires contre la détention arbitraire</p><p>› Réseaux de soutien aux familles de détenus politiques</p></>}
            {entity.risk_level === "modéré" && <><p>› Surveillance accrue des conditions de détention</p><p>› Développement de mécanismes d'habeas corpus effectifs</p></>}
            {entity.risk_level === "faible" && <><p>› Maintien de la vigilance sur les droits des détenus</p><p>› Consolidation des garanties procédurales et du droit à un procès équitable</p></>}
          </div>
        )}
      </div>
    </div>
  );
}

const PATTERN_COLORS: Record<string, string> = {
  detention_arbitraire_systematique: "#ef4444",
  repression_politique_judiciaire: "#f97316",
  abus_detention_preventive: "#f59e0b",
  tensions_juridiques: "#eab308",
  justice_exemplaire: "#10b981",
};

export default function ArbitraryDetentionEnginePage() {
  const [data, setData] = useState<ADSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("tous");
  const [sel, setSel] = useState<ADEntity | null>(null);

  useEffect(() => {
    fetch("/api/arbitrary-detention-engine")
      .then(r => { if (!r.ok) throw new Error(`${r.status}`); return r.json(); })
      .then(d => { setData(d.entities ? d : d.data ?? d); setLoading(false); })
      .catch(() => { setError("Erreur chargement données détention arbitraire"); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Analyse des détentions arbitraires en cours…</div>
    </div>
  );
  if (error || !data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400">{error || "Données indisponibles"}</div>
    </div>
  );

  const filtered = filter === "tous" ? data.entities : data.entities.filter(e => e.risk_level === filter);
  const avgScore = (k: keyof ADEntity) => {
    if (!data.entities.length) return 0;
    return Math.round(data.entities.reduce((s, e) => s + (e[k] as number), 0) / data.entities.length);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {sel && <DetailModal entity={sel} onClose={() => setSel(null)} />}
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>Détention Arbitraire</h1>
          <p className="text-slate-400 text-sm mt-1">La détention sans procès comme outil de terreur politique — quand la loi devient l'arme du pouvoir contre ses opposants</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { l: "Entités Analysées", v: data.total_entities, t: "text-white" },
            { l: "Score Composite Moyen", v: `${data.avg_composite}%`, t: "text-rose-300" },
            { l: "Alertes Critiques", v: data.critical_alerts.length, t: "text-red-300" },
            { l: "Élevé", v: data.risk_distribution["élevé"] ?? 0, t: "text-orange-400" },
            { l: "Index Moyen Détention", v: data.avg_estimated_arbitrary_detention_index, t: "text-rose-400" },
            { l: "Confiance Analyse", v: `${Math.round((data.confidence_score ?? 0) * 100)}%`, t: "text-slate-300" },
          ].map(({ l, v, t }) => (
            <div key={l} className="bg-slate-900 border border-rose-500/20 rounded-xl p-4">
              <p className="text-slate-400 text-xs mb-1">{l}</p>
              <p className={`text-xl font-bold ${t}`}>{v}</p>
            </div>
          ))}
        </div>

        {/* Gauge Rings */}
        <div className="bg-slate-900 rounded-xl p-6 border border-rose-500/20">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Dimensions de la Répression — Scores Moyens</h2>
          <div className="flex flex-wrap justify-around gap-6">
            <GaugeRing value={avgScore("extrajudicial_detention_scale_score")} label="Détention Extrajud." color={ACCENT} />
            <GaugeRing value={avgScore("incommunicado_torture_score")} label="Incommunicado/Torture" color="#f97316" />
            <GaugeRing value={avgScore("political_prisoner_profile_score")} label="Prisonnier Politique" color="#a855f7" />
            <GaugeRing value={avgScore("due_process_denial_score")} label="Déni Procès Équitable" color="#f59e0b" />
          </div>
        </div>

        {/* Distribution Bars */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 rounded-xl p-5 border border-rose-500/20">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Distribution des Niveaux de Risque</h2>
            <div className="space-y-2">
              <DistBar label="Critique" value={data.risk_distribution.critique ?? 0} total={data.total_entities} color="#ef4444" />
              <DistBar label="Élevé" value={data.risk_distribution["élevé"] ?? 0} total={data.total_entities} color="#f97316" />
              <DistBar label="Modéré" value={data.risk_distribution["modéré"] ?? 0} total={data.total_entities} color="#eab308" />
              <DistBar label="Faible" value={data.risk_distribution.faible ?? 0} total={data.total_entities} color="#10b981" />
            </div>
          </div>
          <div className="bg-slate-900 rounded-xl p-5 border border-rose-500/20">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Patterns de Détention Arbitraire</h2>
            <div className="space-y-2">
              {Object.entries(data.pattern_distribution).map(([k, v]) => (
                <DistBar key={k} label={k.replace(/_/g, " ")} value={v} total={data.total_entities} color={PATTERN_COLORS[k] ?? "#94a3b8"} />
              ))}
            </div>
          </div>
        </div>

        {/* Critical Alerts */}
        {data.critical_alerts.length > 0 && (
          <div className="bg-rose-900/10 border border-rose-500/20 rounded-xl p-4">
            <h2 className="text-sm font-semibold mb-2" style={{ color: ACCENT }}>Alertes Critiques — Détention Arbitraire</h2>
            <ul className="space-y-1">{data.critical_alerts.map((a, i) => <li key={i} className="text-sm text-rose-300">› {a}</li>)}</ul>
          </div>
        )}

        {/* Filter Pills */}
        <div className="flex gap-2 flex-wrap">
          {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
            <button key={f} onClick={() => setFilter(f)}
              className={`px-4 py-1.5 rounded-full text-sm border transition-all capitalize ${filter === f ? "text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}
              style={filter === f ? { backgroundColor: ACCENT, borderColor: ACCENT } : {}}>
              {f}
            </button>
          ))}
        </div>

        {/* Entity Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(entity => (
            <div key={entity.id} onClick={() => setSel(entity)}
              className={`bg-slate-900 rounded-xl p-4 border cursor-pointer transition-all hover:border-rose-500/50 ${RB[entity.risk_level] ?? "border-slate-800"}`}>
              <div className="flex justify-between mb-2">
                <div>
                  <p className="text-xs font-mono text-slate-500">{entity.id}</p>
                  <p className="text-sm font-semibold text-white">{entity.name}</p>
                  <p className="text-xs text-slate-500">{entity.country}</p>
                </div>
                <span className={`text-xs font-bold ${RC[entity.risk_level]}`}>{entity.composite_score.toFixed(1)}</span>
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full mb-2">
                <div className="h-full rounded-full" style={{ width: `${entity.composite_score}%`, backgroundColor: ACCENT }} />
              </div>
              <div className="flex justify-between text-xs text-slate-500">
                <span className={RC[entity.risk_level]}>{entity.risk_level}</span>
                <span>idx {entity.estimated_arbitrary_detention_index}</span>
              </div>
              <p className="text-xs text-slate-600 mt-1 truncate">{entity.primary_pattern.replace(/_/g, " ")}</p>
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-600 text-center">Caelum Partners · Détention Arbitraire · {data.last_analysis}</p>
      </div>
    </div>
  );
}
