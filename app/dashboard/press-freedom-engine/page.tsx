"use client";
import { useEffect, useState } from "react";

interface PFEntity {
  id: string; name: string; country: string; sector: string;
  composite_score: number; journalist_imprisonment_score: number;
  media_censorship_ownership_score: number; physical_safety_threats_score: number;
  legal_harassment_lawfare_score: number; risk_level: string; primary_pattern: string;
  key_signals: string[]; avg_estimated_press_freedom_index: number; last_updated: string;
}
interface PFSummary {
  total_entities: number; avg_composite: number;
  risk_distribution: Record<string, number>; pattern_distribution: Record<string, number>;
  top_risk_entities: string[]; critical_alerts: string[];
  last_analysis: string; engine_version: string; domain: string;
  confidence_score: number; data_sources: string[]; entities: PFEntity[];
  avg_estimated_press_freedom_index: number;
}

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#d97706";

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

function DetailModal({ entity, onClose }: { entity: PFEntity; onClose: () => void }) {
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
              { l: "Emprisonnement Journalistes", v: entity.journalist_imprisonment_score, c: "#ef4444" },
              { l: "Censure/Concentration Médias", v: entity.media_censorship_ownership_score, c: "#f97316" },
              { l: "Menaces Sécurité Physique", v: entity.physical_safety_threats_score, c: "#a855f7" },
              { l: "Harcèlement Juridique", v: entity.legal_harassment_lawfare_score, c: "#f59e0b" },
            ].map(({ l, v, c }) => (
              <div key={l}>
                <div className="flex justify-between text-xs text-slate-400 mb-1"><span>{l}</span><span>{v}/100</span></div>
                <div className="h-2 bg-slate-800 rounded-full"><div className="h-full rounded-full" style={{ width: `${v}%`, backgroundColor: c }} /></div>
              </div>
            ))}
            <div className="pt-2 flex justify-between text-sm">
              <span className="text-slate-400">Index Liberté Presse</span>
              <span className="font-bold" style={{ color: ACCENT }}>{entity.avg_estimated_press_freedom_index}</span>
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
            {entity.risk_level === "critique" && <><p>› Mécanismes d'urgence de protection des journalistes emprisonnés</p><p>› Pressions internationales pour la libération des journalistes détenus</p><p>› Alerte aux instances internationales de défense de la presse</p></>}
            {entity.risk_level === "élevé" && <><p>› Renforcement des réseaux de sécurité des journalistes</p><p>› Documentation systématique des pressions sur les médias</p></>}
            {entity.risk_level === "modéré" && <><p>› Surveillance accrue de la concentration des médias</p><p>› Développement de mécanismes légaux de protection</p></>}
            {entity.risk_level === "faible" && <><p>› Maintien de la vigilance sur la liberté de la presse</p><p>› Consolidation des cadres légaux de protection</p></>}
          </div>
        )}
      </div>
    </div>
  );
}

const PATTERN_COLORS: Record<string, string> = {
  repression_severe: "#ef4444",
  censure_systematique: "#f97316",
  pression_juridique: "#f59e0b",
  tensions_presse: "#eab308",
  liberte_exemplaire: "#10b981",
};

export default function PressFreedomEnginePage() {
  const [data, setData] = useState<PFSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("tous");
  const [sel, setSel] = useState<PFEntity | null>(null);

  useEffect(() => {
    fetch("/api/press-freedom-engine")
      .then(r => { if (!r.ok) throw new Error(`${r.status}`); return r.json(); })
      .then(d => { setData(d.entities ? d : d.data ?? d); setLoading(false); })
      .catch(() => { setError("Erreur chargement données liberté de la presse"); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Analyse de la liberté de la presse en cours…</div>
    </div>
  );
  if (error || !data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400">{error || "Données indisponibles"}</div>
    </div>
  );

  const filtered = filter === "tous" ? data.entities : data.entities.filter(e => e.risk_level === filter);
  const avgScore = (k: keyof PFEntity) => {
    if (!data.entities.length) return 0;
    return Math.round(data.entities.reduce((s, e) => s + (e[k] as number), 0) / data.entities.length);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {sel && <DetailModal entity={sel} onClose={() => setSel(null)} />}
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>Press Freedom Engine</h1>
          <p className="text-slate-400 text-sm mt-1">La liberté de la presse comme baromètre démocratique — quand les journalistes sont emprisonnés, la vérité est la première victime</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { l: "Total Entités", v: data.total_entities, t: "text-white" },
            { l: "Score Moyen", v: `${data.avg_composite}%`, t: "text-amber-300" },
            { l: "Critiques", v: data.risk_distribution["critique"] ?? 0, t: "text-red-300" },
            { l: "Élevés", v: data.risk_distribution["élevé"] ?? 0, t: "text-orange-400" },
            { l: "Index Moyen Presse", v: data.avg_estimated_press_freedom_index, t: "text-amber-400" },
            { l: "Confiance", v: `${Math.round((data.confidence_score ?? 0) * 100)}%`, t: "text-slate-300" },
          ].map(({ l, v, t }) => (
            <div key={l} className="bg-slate-900 border border-amber-500/20 rounded-xl p-4">
              <p className="text-slate-400 text-xs mb-1">{l}</p>
              <p className={`text-xl font-bold ${t}`}>{v}</p>
            </div>
          ))}
        </div>

        {/* Gauge Rings */}
        <div className="bg-slate-900 rounded-xl p-6 border border-amber-500/20">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Dimensions de la Répression — Scores Moyens</h2>
          <div className="flex flex-wrap justify-around gap-6">
            <GaugeRing value={avgScore("journalist_imprisonment_score")} label="Emprisonnement Journalistes" color={ACCENT} />
            <GaugeRing value={avgScore("media_censorship_ownership_score")} label="Censure/Concentration Médias" color="#f97316" />
            <GaugeRing value={avgScore("physical_safety_threats_score")} label="Menaces Sécurité Physique" color="#a855f7" />
            <GaugeRing value={avgScore("legal_harassment_lawfare_score")} label="Harcèlement Juridique" color="#f59e0b" />
          </div>
        </div>

        {/* Distribution Bars */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 rounded-xl p-5 border border-amber-500/20">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Distribution des Niveaux de Risque</h2>
            <div className="space-y-2">
              <DistBar label="Critique" value={data.risk_distribution.critique ?? 0} total={data.total_entities} color="#ef4444" />
              <DistBar label="Élevé" value={data.risk_distribution["élevé"] ?? 0} total={data.total_entities} color="#f97316" />
              <DistBar label="Modéré" value={data.risk_distribution["modéré"] ?? 0} total={data.total_entities} color="#eab308" />
              <DistBar label="Faible" value={data.risk_distribution.faible ?? 0} total={data.total_entities} color="#10b981" />
            </div>
          </div>
          <div className="bg-slate-900 rounded-xl p-5 border border-amber-500/20">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Patterns de Répression Médiatique</h2>
            <div className="space-y-2">
              {Object.entries(data.pattern_distribution).map(([k, v]) => (
                <DistBar key={k} label={k.replace(/_/g, " ")} value={v} total={data.total_entities} color={PATTERN_COLORS[k] ?? "#94a3b8"} />
              ))}
            </div>
          </div>
        </div>

        {/* Critical Alerts */}
        {data.critical_alerts.length > 0 && (
          <div className="bg-amber-900/10 border border-amber-500/20 rounded-xl p-4">
            <h2 className="text-sm font-semibold mb-2" style={{ color: ACCENT }}>Alertes Critiques — Liberté de la Presse</h2>
            <ul className="space-y-1">{data.critical_alerts.map((a, i) => <li key={i} className="text-sm text-amber-300">› {a}</li>)}</ul>
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
              className={`bg-slate-900 rounded-xl p-4 border cursor-pointer transition-all hover:border-amber-500/50 ${RB[entity.risk_level] ?? "border-slate-800"}`}>
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
                <span>idx {entity.avg_estimated_press_freedom_index}</span>
              </div>
              <p className="text-xs text-slate-600 mt-1 truncate">{entity.primary_pattern.replace(/_/g, " ")}</p>
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-600 text-center">Caelum Partners · Press Freedom Engine · {data.last_analysis}</p>
      </div>
    </div>
  );
}
