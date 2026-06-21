"use client";
import { useEffect, useState } from "react";

const ACCENT = "#2a2a0a";
const SLUG = "elderly-abuse-care-home-rights-engine";

const RC: Record<string, string> = {
  critique: "#dc2626", élevé: "#f97316", modéré: "#eab308", faible: "#22c55e",
};
const RB: Record<string, string> = {
  critique: "#450a0a", élevé: "#431407", modéré: "#422006", faible: "#052e16",
};

function GaugeRing({ score, color }: { score: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={`${dash} ${circ - dash}`} strokeDashoffset={circ / 4}
        strokeLinecap="round" transform="rotate(0 44 44)" />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize="13" fontWeight="bold" fill={color}>
        {score.toFixed(0)}
      </text>
    </svg>
  );
}

type Entity = Record<string, unknown>;
type ApiData = { entities: Entity[]; avg_composite: number; risk_distribution: Record<string, number>; confidence_score: number; critical_alerts: string[] };

export default function ElderlyAbuseCareHomeRightsPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch(`/api/${SLUG}`).then(r => r.json()).then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement...</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between p-6 border-b border-slate-700">
              <div>
                <h2 className="text-lg font-bold text-white">{selected.name as string}</h2>
                <span className="inline-block mt-1 px-2 py-0.5 rounded text-xs font-semibold"
                  style={{ background: RB[selected.risk_level as string], color: RC[selected.risk_level as string] }}>
                  {selected.risk_level as string}
                </span>
              </div>
              <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-white text-2xl leading-none">×</button>
            </div>
            <div className="p-6 space-y-3">
              <div className="flex items-center gap-3">
                <GaugeRing score={selected.composite_score as number} color={RC[selected.risk_level as string]} />
                <div>
                  <p className="text-white font-semibold">Score composite: {(selected.composite_score as number).toFixed(2)}</p>
                  <p className="text-slate-400 text-sm">Pays: {selected.country as string}</p>
                  <p className="text-slate-400 text-sm">Signal: {selected.signal as string}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Maltraitance &amp; Droits en Maison de Retraite</h1>
          <p className="text-slate-400 mt-1">Elder Abuse · EHPAD · Dignité · WHO · Protection Personnes Âgées</p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
            <p className="text-slate-400 text-xs mb-1">Score Moyen</p>
            <p className="text-2xl font-bold" style={{ color: ACCENT }}>{data.avg_composite.toFixed(2)}</p>
          </div>
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
            <p className="text-slate-400 text-xs mb-1">Confiance</p>
            <p className="text-2xl font-bold text-white">{(data.confidence_score * 100).toFixed(0)}%</p>
          </div>
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
            <p className="text-slate-400 text-xs mb-1">Critique</p>
            <p className="text-2xl font-bold text-red-500">{data.risk_distribution["critique"] ?? 0}</p>
          </div>
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
            <p className="text-slate-400 text-xs mb-1">Alertes</p>
            <p className="text-2xl font-bold text-orange-400">{data.critical_alerts?.length ?? 0}</p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {data.entities.map((e) => {
            const rl = e.risk_level as string;
            return (
              <button key={e.entity_id as string} onClick={() => setSelected(e)}
                className="bg-slate-900 border border-slate-700 rounded-xl p-4 text-left hover:border-slate-500 transition-colors">
                <div className="flex items-start gap-3">
                  <GaugeRing score={e.composite_score as number} color={RC[rl]} />
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-sm font-medium line-clamp-2">{e.name as string}</p>
                    <span className="inline-block mt-1 px-2 py-0.5 rounded text-xs font-semibold"
                      style={{ background: RB[rl], color: RC[rl] }}>{rl}</span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
