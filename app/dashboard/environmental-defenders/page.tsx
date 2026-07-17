"use client";
import { useEffect, useState } from "react";

interface Entity { entity: string; level: string; final: number; }
interface SwarmData { engine: string; avg_composite: number; distribution: Record<string, number>; entities: Entity[]; estimated_environmental_defenders_index: number; }

function GaugeRing({ value, max = 100, color = "#6366f1" }: { value: number; max?: number; color?: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  return (
    <svg viewBox="0 0 88 88" className="w-full h-full">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={10} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={10}
        strokeDasharray={`${pct * circ} ${circ}`}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="middle" fill="#f1f5f9" fontSize={14} fontWeight={700}>
        {value.toFixed(1)}
      </text>
    </svg>
  );
}

const RISK_COLORS: Record<string, string> = {
  critique: "text-red-400 bg-red-950/30 border-red-800/40",
  élevé: "text-orange-400 bg-orange-950/30 border-orange-800/40",
  modéré: "text-yellow-400 bg-yellow-950/30 border-yellow-800/40",
  faible: "text-green-400 bg-green-950/30 border-green-800/40",
};

const RISK_GAUGE: Record<string, string> = {
  critique: "#ef4444",
  élevé: "#f97316",
  modéré: "#eab308",
  faible: "#22c55e",
};

export default function EnvironmentalDefendersPage() {
  const [data, setData] = useState<SwarmData | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      const res = await fetch("/api/environmentaldefenders");
      const d = await res.json();
      setData(d.payload ?? d);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  if (loading) return <div className="p-8 text-slate-500 text-center">Analyse en cours…</div>;
  if (!data) return <div className="p-8 text-red-400 text-center">Erreur de chargement</div>;

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Défenseurs des Droits Environnementaux</h1>
        <p className="text-slate-400 text-sm mt-1">Assassinats, criminalisation et intimidation des militants écologistes</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {data.entities.map((e) => (
          <div key={e.entity} className={`rounded-xl border p-4 ${RISK_COLORS[e.level] ?? "text-slate-400 bg-slate-900 border-slate-800"}`}>
            <div className="w-20 h-20 mx-auto mb-3">
              <GaugeRing value={e.final} color={RISK_GAUGE[e.level] ?? "#6366f1"} />
            </div>
            <p className="text-xs font-semibold text-center">{e.entity}</p>
            <p className="text-xs text-center opacity-70 mt-1 capitalize">{e.level}</p>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-3">
          <p className="text-sm text-slate-400">Score composite moyen</p>
          <span className="text-white font-bold text-lg">{data.avg_composite}</span>
        </div>
        <div className="flex gap-4 flex-wrap">
          {Object.entries(data.distribution).map(([k, v]) => (
            <span key={k} className="text-xs bg-slate-800 px-3 py-1 rounded-full capitalize">{k}: <strong>{v}</strong></span>
          ))}
        </div>
        {data.estimated_environmental_defenders_index != null && (
          <p className="text-xs text-slate-500 mt-3">Indice défenseurs environnement : <span className="text-indigo-300 font-semibold">{data.estimated_environmental_defenders_index}/10</span></p>
        )}
      </div>
    </div>
  );
}
