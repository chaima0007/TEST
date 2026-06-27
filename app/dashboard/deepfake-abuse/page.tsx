"use client";
import { useEffect, useState } from "react";

interface Entity { entity: string; risk_level: string; avg_composite: number; estimated_deepfake_abuse_index: number; }
interface SwarmData { engine: string; avg_composite: number; distribution: Record<string, number>; entities: Entity[]; }

function GaugeRing({ value, max = 100, color = "#6366f1" }: { value: number; max?: number; color?: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  return (
    <svg viewBox="0 0 88 88" className="w-full h-full">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={10} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={10}
        strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
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

export default function DeepfakeAbusePage() {
  const [data, setData] = useState<SwarmData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/deepfakeabuse");
        const d = await res.json();
        setData(d.payload ?? d);
      } finally { setLoading(false); }
    }
    load();
  }, []);

  if (loading) return <div className="p-8 text-slate-500 text-center">Analyse en cours…</div>;
  if (!data) return <div className="p-8 text-red-400 text-center">Erreur de chargement</div>;

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Abus par Deepfake &amp; Médias Synthétiques</h1>
        <p className="text-slate-400 text-sm mt-1">Images non-consenties, fraude identitaire et violence numérique par IA</p>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {data.entities.map((e) => (
          <div key={e.entity} className={`rounded-xl border p-4 ${RISK_COLORS[e.risk_level] ?? "text-slate-400 bg-slate-900 border-slate-800"}`}>
            <div className="w-20 h-20 mx-auto mb-3">
              <GaugeRing value={e.avg_composite}
                color={e.risk_level === "critique" ? "#ef4444" : e.risk_level === "élevé" ? "#f97316" : e.risk_level === "modéré" ? "#eab308" : "#22c55e"} />
            </div>
            <p className="text-xs font-semibold text-center">{e.entity.replace(/_/g, " ")}</p>
            <p className="text-xs text-center opacity-70 mt-1 capitalize">{e.risk_level}</p>
          </div>
        ))}
      </div>
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <p className="text-sm text-slate-400">Score composite moyen : <span className="text-white font-bold">{data.avg_composite}</span></p>
        <div className="flex gap-4 mt-3 flex-wrap">
          {Object.entries(data.distribution).map(([k, v]) => (
            <span key={k} className="text-xs bg-slate-800 px-3 py-1 rounded-full">{k}: <strong>{v}</strong></span>
          ))}
        </div>
      </div>
    </div>
  );
}
