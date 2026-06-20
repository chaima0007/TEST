"use client";
import { useState, useEffect } from "react";

interface Entity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  criminalization_scale_score: number;
  extrajudicial_killings_score: number;
  treatment_access_denial_score: number;
  racial_marginalization_bias_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_drug_policy_human_rights_index: number;
  last_updated: string;
}

interface Data {
  entities: Entity[];
  total_entities: number;
  avg_composite: number;
  avg_estimated_drug_policy_human_rights_index: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  last_analysis: string;
  engine_version: string;
}

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#7c3aed";

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

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

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

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
            <p className="text-xs text-slate-500 font-mono">{entity.entity_id}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded-full text-xs border ${tab === t ? "text-white" : "bg-slate-800 border-slate-700 text-slate-400"}`}
              style={tab === t ? { backgroundColor: ACCENT, borderColor: ACCENT } : {}}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="space-y-3">
            {[
              { l: "Échelle de Criminalisation", v: entity.criminalization_scale_score, c: "#7c3aed" },
              { l: "Exécutions Extrajudiciaires", v: entity.extrajudicial_killings_score, c: "#6d28d9" },
              { l: "Déni d'Accès au Traitement", v: entity.treatment_access_denial_score, c: "#5b21b6" },
              { l: "Biais Racial & Marginalisation", v: entity.racial_marginalization_bias_score, c: "#4c1d95" },
            ].map(({ l, v, c }) => (
              <div key={l}>
                <div className="flex justify-between text-xs text-slate-400 mb-1"><span>{l}</span><span>{v}/100</span></div>
                <div className="h-2 bg-slate-800 rounded-full">
                  <div className="h-full rounded-full" style={{ width: `${v}%`, backgroundColor: c }} />
                </div>
              </div>
            ))}
            <div className="pt-2 flex justify-between text-sm">
              <span className="text-slate-400">Indice Politique Drogues Estimé</span>
              <span className="font-bold" style={{ color: ACCENT }}>{entity.estimated_drug_policy_human_rights_index}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Score Composite</span>
              <span className={`font-bold ${RC[entity.risk_level]}`}>{entity.composite_score.toFixed(1)}</span>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div>
            <p className="text-xs text-slate-500 mb-3">Pattern principal: <span style={{ color: ACCENT }}>{entity.primary_pattern}</span></p>
            <ul className="space-y-2">
              {entity.key_signals.map((s, i) => (
                <li key={i} className="flex gap-2 text-sm text-slate-300">
                  <span style={{ color: ACCENT }}>›</span>{s}
                </li>
              ))}
            </ul>
            <p className="text-xs text-slate-600 mt-4">Mis à jour: {entity.last_updated}</p>
          </div>
        )}

        {tab === "actions" && (
          <div className="text-sm space-y-2 text-slate-300">
            <p className="text-xs text-slate-500 mb-2">Niveau de risque: <span className={RC[entity.risk_level]}>{entity.risk_level}</span></p>
            {entity.risk_level === "critique" && (
              <>
                <p>› Intervention urgente pour mettre fin aux exécutions extrajudiciaires et aux violations massives des droits</p>
                <p>› Plaidoyer international pour une réforme immédiate des politiques pénales sur les drogues</p>
              </>
            )}
            {entity.risk_level === "élevé" && (
              <>
                <p>› Documentation des biais raciaux et accès aux soins pour les populations marginalisées</p>
                <p>› Appui aux réformes législatives vers des approches de santé publique plutôt que punitives</p>
              </>
            )}
            {entity.risk_level === "modéré" && (
              <p>› Surveillance des pratiques de criminalisation et soutien aux programmes de réduction des risques</p>
            )}
            {entity.risk_level === "faible" && (
              <p>› Maintien de la veille sur les évolutions législatives et appui aux initiatives communautaires</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default function DrugPolicyHumanRightsEnginePage() {
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("tous");
  const [sel, setSel] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/drug-policy-human-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.data ?? d); setLoading(false); })
      .catch(() => { setError("Erreur chargement données Drug Policy Human Rights Engine"); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Analyse de la politique des drogues et droits humains…</div>
    </div>
  );
  if (error || !data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400">{error || "Données indisponibles"}</div>
    </div>
  );

  const entities = data.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter);
  const dist = data.risk_distribution ?? {};
  const patDist = data.pattern_distribution ?? {};
  const avgScore = (k: keyof Entity) =>
    entities.length > 0 ? entities.reduce((s, e) => s + (e[k] as number), 0) / entities.length : 0;

  const kpis = [
    { l: "Entités Analysées", v: data.total_entities ?? entities.length, c: "text-white" },
    { l: "Score Moyen", v: `${(data.avg_composite ?? 0).toFixed(1)}`, c: "text-violet-400" },
    { l: "Indice Politique Drogues Moyen", v: `${(data.avg_estimated_drug_policy_human_rights_index ?? 0).toFixed(2)}`, c: "text-violet-300" },
    { l: "Critique", v: dist.critique ?? 0, c: "text-red-400" },
    { l: "Élevé", v: dist["élevé"] ?? 0, c: "text-orange-400" },
    { l: "Modéré/Faible", v: (dist.modéré ?? 0) + (dist.faible ?? 0), c: "text-emerald-400" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {sel && <DetailModal entity={sel} onClose={() => setSel(null)} />}
      <div className="max-w-7xl mx-auto space-y-6">

        <div>
          <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>Politique des Drogues & Droits Humains</h1>
          <p className="text-slate-400 text-sm mt-1">Criminalisation, exécutions extrajudiciaires et biais racial dans la guerre à la drogue</p>
          <p className="text-slate-600 text-xs mt-0.5">Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {kpis.map(({ l, v, c }) => (
            <div key={l} className="bg-slate-900 border border-violet-500/20 rounded-xl p-4 text-center">
              <p className={`text-xl font-bold ${c}`}>{v}</p>
              <p className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</p>
            </div>
          ))}
        </div>

        {/* Gauge Rings */}
        <div className="bg-slate-900 border border-violet-500/20 rounded-xl p-5">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4">Scores Politique Drogues & Droits Moyens</h2>
          <div className="flex flex-wrap justify-around gap-4">
            <GaugeRing value={avgScore("criminalization_scale_score")} label="Criminalisation" color={ACCENT} />
            <GaugeRing value={avgScore("extrajudicial_killings_score")} label="Exécutions Extra-jud." color="#6d28d9" />
            <GaugeRing value={avgScore("treatment_access_denial_score")} label="Déni de Traitement" color="#5b21b6" />
            <GaugeRing value={avgScore("racial_marginalization_bias_score")} label="Biais Racial" color="#4c1d95" />
          </div>
        </div>

        {/* Distribution Bars */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-violet-500/20 rounded-xl p-5">
            <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Distribution des Niveaux de Risque</h2>
            <div className="space-y-2">
              <DistBar label="Critique" value={dist.critique ?? 0} total={entities.length} color="#ef4444" />
              <DistBar label="Élevé" value={dist["élevé"] ?? 0} total={entities.length} color="#f97316" />
              <DistBar label="Modéré" value={dist.modéré ?? 0} total={entities.length} color="#eab308" />
              <DistBar label="Faible" value={dist.faible ?? 0} total={entities.length} color="#10b981" />
            </div>
          </div>
          <div className="bg-slate-900 border border-violet-500/20 rounded-xl p-5">
            <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Patterns de Politique Répressive</h2>
            <div className="space-y-2">
              {Object.entries(patDist).map(([k, v], i) => (
                <DistBar key={k} label={k.replace(/_/g, " ")} value={v} total={entities.length}
                  color={["#7c3aed", "#6d28d9", "#5b21b6", "#4c1d95", "#2e1065"][i % 5]} />
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
        </div>

        {/* Entity Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(entity => (
            <div key={entity.entity_id} onClick={() => setSel(entity)}
              className={`bg-slate-900 rounded-xl p-4 border cursor-pointer transition-all hover:border-violet-500/50 ${RB[entity.risk_level] ?? "border-slate-800"}`}>
              <div className="flex justify-between mb-2">
                <div>
                  <p className="text-xs font-mono text-slate-500">{entity.entity_id}</p>
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
                <span>idx {entity.estimated_drug_policy_human_rights_index}</span>
              </div>
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-600 text-center">Caelum Partners · Drug Policy Human Rights Engine · {data.last_analysis}</p>
      </div>
    </div>
  );
}
