"use client";
import { useEffect, useState } from "react";

interface SAEntity {
  id: string; name: string; country: string; sector: string;
  composite_score: number; illicit_flow_score: number;
  stockpile_leakage_score: number; non_state_actor_arming_score: number;
  post_conflict_saturation_score: number; risk_level: string;
  primary_pattern: string; key_signals: string[];
  estimated_arms_risk_index: number; last_updated: string;
}
interface SASummary {
  total_entities: number; avg_composite: number;
  risk_distribution: Record<string, number>; pattern_distribution: Record<string, number>;
  top_risk_entities: string[]; critical_alerts: string[];
  last_analysis: string; engine_version: string; domain: string;
  confidence_score: number; data_sources: string[];
  entities: SAEntity[]; avg_estimated_arms_risk_index: number;
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

function DetailModal({ entity, onClose }: { entity: SAEntity; onClose: () => void }) {
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
              className={`px-3 py-1 rounded-full text-xs border ${tab === t ? "bg-orange-500 border-orange-400 text-white" : "bg-slate-800 border-slate-700 text-slate-400"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-3">
            {[
              { l: "Flux Illicites d'Armes", v: entity.illicit_flow_score, c: "#f97316" },
              { l: "Fuite des Stocks", v: entity.stockpile_leakage_score, c: "#eab308" },
              { l: "Armement Acteurs Non-Étatiques", v: entity.non_state_actor_arming_score, c: "#f97316" },
              { l: "Saturation Post-Conflit", v: entity.post_conflict_saturation_score, c: "#ef4444" },
            ].map(({ l, v, c }) => (
              <div key={l}>
                <div className="flex justify-between text-xs text-slate-400 mb-1"><span>{l}</span><span>{v}/100</span></div>
                <div className="h-2 bg-slate-800 rounded-full"><div className="h-full rounded-full" style={{ width: `${v}%`, backgroundColor: c }} /></div>
              </div>
            ))}
            <div className="pt-2 flex justify-between text-sm">
              <span className="text-slate-400">Index Risque Armes ALPC</span>
              <span className="text-orange-400 font-bold">{entity.estimated_arms_risk_index}</span>
            </div>
          </div>
        )}
        {tab === "signaux" && (
          <ul className="space-y-2">
            {entity.key_signals.map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-300"><span className="text-orange-400">›</span>{s}</li>
            ))}
          </ul>
        )}
        {tab === "actions" && (
          <div className="text-sm space-y-2 text-slate-300">
            <p className="text-xs text-slate-500 mb-2">Pattern: <span className="text-orange-400">{entity.primary_pattern}</span></p>
            {entity.risk_level === "critique" && <><p>› Programme d'urgence de collecte et destruction d'armes illicites</p><p>› Renforcement immédiat des contrôles aux frontières</p></>}
            {entity.risk_level === "élevé" && <><p>› Réforme des systèmes de contrôle des stocks d'armes</p><p>› Programmes DDR renforcés pour acteurs non-étatiques</p></>}
            {entity.risk_level === "modéré" && <><p>› Amélioration de la traçabilité des flux d'armes légères</p></>}
            {entity.risk_level === "faible" && <><p>› Maintien de la surveillance et coopération régionale ALPC</p></>}
          </div>
        )}
      </div>
    </div>
  );
}

export default function SmallArmsProliferationPage() {
  const [data, setData] = useState<SASummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("tous");
  const [sel, setSel] = useState<SAEntity | null>(null);

  useEffect(() => {
    const swarmUrl = process.env.NEXT_PUBLIC_SWARM_API_URL;
    if (!swarmUrl) { setError("SWARM_API_URL non configuré"); setLoading(false); return; }
    fetch("/api/small-arms-proliferation-engine")
      .then(r => { if (!r.ok) throw new Error(`${r.status}`); return r.json(); })
      .then(d => { setData(d.entities ? d : d.data ?? d); setLoading(false); })
      .catch(() => { setError("Erreur chargement données prolifération ALPC"); setLoading(false); });
  }, []);

  if (loading) return <div className="min-h-screen bg-slate-950 flex items-center justify-center"><div className="text-slate-400 animate-pulse">Analyse de la prolifération des armes légères…</div></div>;
  if (error || !data) return <div className="min-h-screen bg-slate-950 flex items-center justify-center"><div className="text-red-400">{error || "Données indisponibles"}</div></div>;

  const filtered = filter === "tous" ? data.entities : data.entities.filter(e => e.risk_level === filter);
  const avgScore = (k: keyof SAEntity) => Math.round(data.entities.reduce((s, e) => s + (e[k] as number), 0) / data.entities.length);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {sel && <DetailModal entity={sel} onClose={() => setSel(null)} />}
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold">Prolifération des Armes Légères (ALPC)</h1>
          <p className="text-slate-400 text-sm">Flux illicites d'armes légères alimentant conflits non-étatiques · v{data.engine_version}</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { l: "Zones Analysées", v: data.total_entities, g: "from-slate-700 to-slate-600", t: "text-white" },
            { l: "Score Composite Moyen", v: `${data.avg_composite}%`, g: "from-orange-900 to-orange-800", t: "text-orange-300" },
            { l: "Alertes Critiques", v: data.critical_alerts.length, g: "from-red-900 to-red-800", t: "text-red-300" },
            { l: "Index Risque Armes", v: data.avg_estimated_arms_risk_index, g: "from-amber-900 to-amber-800", t: "text-amber-300" },
            { l: "Sources", v: data.data_sources.length, g: "from-orange-900 to-orange-800", t: "text-orange-300" },
            { l: "Confiance", v: `${Math.round(data.confidence_score * 100)}%`, g: "from-slate-800 to-slate-700", t: "text-slate-300" },
          ].map(({ l, v, g, t }) => (
            <div key={l} className={`bg-gradient-to-br ${g} rounded-xl p-4 border border-white/5`}>
              <p className="text-slate-400 text-xs mb-1">{l}</p>
              <p className={`text-xl font-bold ${t}`}>{v}</p>
            </div>
          ))}
        </div>

        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Vecteurs de Prolifération ALPC Moyens</h2>
          <div className="flex flex-wrap justify-around gap-6">
            <GaugeRing value={avgScore("illicit_flow_score")} label="Flux Illicites d'Armes" color="#f97316" />
            <GaugeRing value={avgScore("stockpile_leakage_score")} label="Fuite des Stocks" color="#eab308" />
            <GaugeRing value={avgScore("non_state_actor_arming_score")} label="Armement Acteurs Non-Étatiques" color="#f97316" />
            <GaugeRing value={avgScore("post_conflict_saturation_score")} label="Saturation Post-Conflit" color="#ef4444" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Distribution Risques ALPC</h2>
            <div className="space-y-2">
              <DistBar label="Critique" value={data.risk_distribution.critique ?? 0} total={data.total_entities} color="#ef4444" />
              <DistBar label="Élevé" value={data.risk_distribution["élevé"] ?? 0} total={data.total_entities} color="#f97316" />
              <DistBar label="Modéré" value={data.risk_distribution["modéré"] ?? 0} total={data.total_entities} color="#eab308" />
              <DistBar label="Faible" value={data.risk_distribution.faible ?? 0} total={data.total_entities} color="#10b981" />
            </div>
          </div>
          <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Patterns de Prolifération Armée</h2>
            <div className="space-y-2">
              {Object.entries(data.pattern_distribution).map(([k, v], i) => (
                <DistBar key={k} label={k.replace(/_/g, " ")} value={v} total={data.total_entities} color={["#f97316", "#eab308", "#ef4444", "#10b981", "#f97316"][i % 5]} />
              ))}
            </div>
          </div>
        </div>

        {data.critical_alerts.length > 0 && (
          <div className="bg-orange-900/10 border border-orange-500/20 rounded-xl p-4">
            <h2 className="text-sm font-semibold text-orange-400 mb-2">Alertes Prolifération ALPC Critiques</h2>
            <ul className="space-y-1">{data.critical_alerts.map((a, i) => <li key={i} className="text-sm text-orange-300">› {a}</li>)}</ul>
          </div>
        )}

        <div className="flex gap-2 flex-wrap">
          {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
            <button key={f} onClick={() => setFilter(f)}
              className={`px-4 py-1.5 rounded-full text-sm border transition-all capitalize ${filter === f ? "bg-orange-500 border-orange-400 text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}>
              {f}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(entity => (
            <div key={entity.id} onClick={() => setSel(entity)}
              className={`bg-slate-900 rounded-xl p-4 border cursor-pointer hover:border-orange-500/50 transition-all ${RB[entity.risk_level] ?? "border-slate-800"}`}>
              <div className="flex justify-between mb-2">
                <div>
                  <p className="text-xs font-mono text-slate-500">{entity.id}</p>
                  <p className="text-sm font-semibold text-white">{entity.name}</p>
                  <p className="text-xs text-slate-500">{entity.country}</p>
                </div>
                <span className={`text-xs font-bold ${RC[entity.risk_level]}`}>{entity.composite_score.toFixed(1)}</span>
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full mb-2">
                <div className="h-full rounded-full bg-orange-500" style={{ width: `${entity.composite_score}%` }} />
              </div>
              <div className="flex justify-between text-xs text-slate-500">
                <span className={RC[entity.risk_level]}>{entity.risk_level}</span>
                <span>idx {entity.estimated_arms_risk_index}</span>
              </div>
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-600 text-center">Caelum Partners · Prolifération des Armes Légères (ALPC) · {data.last_analysis}</p>
      </div>
    </div>
  );
}
