"use client";
import { useEffect, useState } from "react";

interface ESEntity {
  id: string; name: string; country: string; sector: string;
  composite_score: number; disinformation_saturation_score: number;
  reality_consensus_deficit_score: number; media_ecosystem_fragmentation_score: number;
  epistemic_vulnerability_score: number; risk_level: string;
  primary_pattern: string; key_signals: string[];
  estimated_epistemic_index: number; last_updated: string;
}
interface ESSummary {
  total_entities: number; avg_composite: number;
  risk_distribution: Record<string, number>; pattern_distribution: Record<string, number>;
  top_risk_entities: string[]; critical_alerts: string[];
  last_analysis: string; engine_version: string; domain: string;
  confidence_score: number; data_sources: string[];
  entities: ESEntity[]; avg_estimated_epistemic_index: number;
}

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36, c = 2 * Math.PI * r, d = Math.min(value / 100, 1);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={`${d * c} ${c}`} strokeDashoffset={c / 4} strokeLinecap="round"
          transform="rotate(-90 48 48)" style={{ transition: "stroke-dasharray .6s" }} />
        <text x="48" y="52" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">{Math.round(d * 100)}%</text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ label, value, total, color }: { label: string; value: number; total: number; color: string }) {
  const p = total > 0 ? Math.round(value / total * 100) : 0;
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

function DetailModal({ entity, onClose }: { entity: ESEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
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
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded-full text-xs border ${tab === t ? "bg-fuchsia-500 border-fuchsia-400 text-white" : "bg-slate-800 border-slate-700 text-slate-400"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-3">
            {[
              { l: "Saturation Désinformation", v: entity.disinformation_saturation_score, c: "#ef4444" },
              { l: "Consensus Réalité", v: entity.reality_consensus_deficit_score, c: "#f97316" },
              { l: "Fragmentation Médias", v: entity.media_ecosystem_fragmentation_score, c: "#eab308" },
              { l: "Vulnérabilité Épistémique", v: entity.epistemic_vulnerability_score, c: "#d946ef" },
            ].map(({ l, v, c }) => (
              <div key={l}>
                <div className="flex justify-between text-xs text-slate-400 mb-1"><span>{l}</span><span>{v}/100</span></div>
                <div className="h-2 bg-slate-800 rounded-full"><div className="h-full rounded-full" style={{ width: `${v}%`, backgroundColor: c }} /></div>
              </div>
            ))}
            <div className="pt-2 flex justify-between text-sm">
              <span className="text-slate-400">Index Épistémique Caelum</span>
              <span className="text-fuchsia-400 font-bold">{entity.estimated_epistemic_index}</span>
            </div>
          </div>
        )}
        {tab === "signaux" && (
          <ul className="space-y-2">
            {entity.key_signals.map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-300"><span className="text-fuchsia-400">›</span>{s}</li>
            ))}
          </ul>
        )}
        {tab === "actions" && (
          <div className="text-sm space-y-2 text-slate-300">
            <p className="text-xs text-slate-500 mb-2">Pattern: <span className="text-fuchsia-400">{entity.primary_pattern}</span></p>
            {entity.risk_level === "critique" && <><p>› Intervention d&apos;urgence contre les opérations de désinformation massives</p><p>› Restauration des mécanismes de consensus sur la réalité partagée</p><p>› Déploiement de contre-narratifs épistémiques coordonnés</p></>}
            {entity.risk_level === "élevé" && <><p>› Renforcement des systèmes de fact-checking et vérification</p><p>› Programmes de résilience cognitive et d&apos;éducation médiatique</p></>}
            {entity.risk_level === "modéré" && <><p>› Surveillance accrue des vecteurs de fragmentation médiatique</p><p>› Politiques de renforcement de la sécurité épistémique</p></>}
            {entity.risk_level === "faible" && <><p>› Maintien de la veille sur les indicateurs épistémiques</p><p>› Consolidation des institutions garantes de la réalité partagée</p></>}
          </div>
        )}
      </div>
    </div>
  );
}

export default function EpistemicSecurityPage() {
  const [data, setData] = useState<ESSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("tous");
  const [sel, setSel] = useState<ESEntity | null>(null);

  useEffect(() => {
    fetch("/api/epistemic-security-engine")
      .then(r => r.json())
      .then(d => { setData(d.entities ? d : d.data ?? d); setLoading(false); })
      .catch(() => { setError("Erreur chargement données de sécurité épistémique"); setLoading(false); });
  }, []);

  if (loading) return <div className="min-h-screen bg-slate-950 flex items-center justify-center"><div className="text-slate-400 animate-pulse">Analyse de la sécurité épistémique mondiale…</div></div>;
  if (error || !data) return <div className="min-h-screen bg-slate-950 flex items-center justify-center"><div className="text-red-400">{error}</div></div>;

  const filtered = filter === "tous" ? data.entities : data.entities.filter(e => e.risk_level === filter);
  const avgScore = (k: keyof ESEntity) => Math.round(data.entities.reduce((s, e) => s + (e[k] as number), 0) / data.entities.length);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {sel && <DetailModal entity={sel} onClose={() => setSel(null)} />}
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold">Epistemic Security Engine — Sécurité Cognitive &amp; Réalité Partagée</h1>
          <p className="text-slate-400 text-sm">Détection des attaques épistémiques : désinformation · fracture cognitive · guerre narrative · v{data.engine_version}</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { l: "Zones Analysées", v: data.total_entities, g: "from-slate-700 to-slate-600", t: "text-white" },
            { l: "Score Déficit Moyen", v: `${data.avg_composite}%`, g: "from-violet-900 to-violet-800", t: "text-violet-300" },
            { l: "Alertes Critiques", v: data.critical_alerts.length, g: "from-red-900 to-red-800", t: "text-red-300" },
            { l: "Index Épistémique", v: data.avg_estimated_epistemic_index, g: "from-purple-900 to-purple-800", t: "text-purple-300" },
            { l: "Sources", v: data.data_sources.length, g: "from-indigo-900 to-indigo-800", t: "text-indigo-300" },
            { l: "Confiance", v: `${Math.round(data.confidence_score * 100)}%`, g: "from-slate-800 to-slate-700", t: "text-slate-300" },
          ].map(({ l, v, g, t }) => (
            <div key={l} className={`bg-gradient-to-br ${g} rounded-xl p-4 border border-white/5`}>
              <p className="text-slate-400 text-xs mb-1">{l}</p>
              <p className={`text-xl font-bold ${t}`}>{v}</p>
            </div>
          ))}
        </div>

        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Vecteurs Épistémiques Moyens</h2>
          <div className="flex flex-wrap justify-around gap-6">
            <GaugeRing value={avgScore("disinformation_saturation_score")} label="Saturation Désinformation" color="#ef4444" />
            <GaugeRing value={avgScore("reality_consensus_deficit_score")} label="Déficit Consensus Réalité" color="#f97316" />
            <GaugeRing value={avgScore("media_ecosystem_fragmentation_score")} label="Fragmentation Médiatique" color="#eab308" />
            <GaugeRing value={avgScore("epistemic_vulnerability_score")} label="Vulnérabilité Épistémique" color="#d946ef" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Distribution Risques</h2>
            <div className="space-y-2">
              <DistBar label="Critique" value={data.risk_distribution.critique ?? 0} total={data.total_entities} color="#ef4444" />
              <DistBar label="Élevé" value={data.risk_distribution["élevé"] ?? 0} total={data.total_entities} color="#f97316" />
              <DistBar label="Modéré" value={data.risk_distribution["modéré"] ?? 0} total={data.total_entities} color="#eab308" />
              <DistBar label="Faible" value={data.risk_distribution.faible ?? 0} total={data.total_entities} color="#10b981" />
            </div>
          </div>
          <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Patterns Épistémiques Détectés</h2>
            <div className="space-y-2">
              {Object.entries(data.pattern_distribution).map(([k, v], i) => (
                <DistBar key={k} label={k.replace(/_/g, " ")} value={v} total={data.total_entities} color={["#ef4444", "#f97316", "#eab308", "#10b981", "#8b5cf6"][i % 5]} />
              ))}
            </div>
          </div>
        </div>

        {data.critical_alerts.length > 0 && (
          <div className="bg-fuchsia-900/10 border border-fuchsia-500/20 rounded-xl p-4">
            <h2 className="text-sm font-semibold text-fuchsia-400 mb-2">Alertes Épistémiques Critiques</h2>
            <ul className="space-y-1">{data.critical_alerts.map((a, i) => <li key={i} className="text-sm text-fuchsia-300">› {a}</li>)}</ul>
          </div>
        )}

        <div className="flex gap-2 flex-wrap">
          {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
            <button key={f} onClick={() => setFilter(f)}
              className={`px-4 py-1.5 rounded-full text-sm border transition-all capitalize ${filter === f ? "bg-fuchsia-500 border-fuchsia-400 text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}>
              {f}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(entity => (
            <div key={entity.id} onClick={() => setSel(entity)}
              className={`bg-slate-900 rounded-xl p-4 border cursor-pointer hover:border-fuchsia-500/50 transition-all ${RB[entity.risk_level] ?? "border-slate-800"}`}>
              <div className="flex justify-between mb-2">
                <div>
                  <p className="text-xs font-mono text-slate-500">{entity.id}</p>
                  <p className="text-sm font-semibold text-white">{entity.name}</p>
                  <p className="text-xs text-slate-500">{entity.country}</p>
                </div>
                <span className={`text-xs font-bold ${RC[entity.risk_level]}`}>{entity.composite_score.toFixed(1)}</span>
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full mb-2">
                <div className="h-full rounded-full bg-fuchsia-500" style={{ width: `${entity.composite_score}%` }} />
              </div>
              <div className="flex justify-between text-xs text-slate-500">
                <span className={RC[entity.risk_level]}>{entity.risk_level}</span>
                <span>idx {entity.estimated_epistemic_index}</span>
              </div>
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-600 text-center">Caelum Partners · Sécurité Épistémique &amp; Réalité Partagée · {data.last_analysis}</p>
      </div>
    </div>
  );
}
