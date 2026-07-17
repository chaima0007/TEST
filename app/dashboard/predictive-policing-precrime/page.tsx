"use client";
import { useEffect, useState } from "react";
function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36; const cx = 44; const cy = 44;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100);
  const dash = (pct / 100) * circ;
  return (
    <svg viewBox="0 0 88 88" className="w-24 h-24">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${dash} ${circ - dash}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize={14} fill={color} fontWeight="bold">{pct.toFixed(0)}%</text>
    </svg>
  );
}
export default function PredictivePolicingPrecrimeDashboard() {
  const [data, setData] = useState<{ entities?: { entity: string; composite: number; level: string }[]; avg_composite?: number } | null>(null);
  useEffect(() => { fetch("/api/predictivepolicingprecrime").then(r => r.json()).then(d => setData(d.payload ?? d)); }, []);
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">Predictive Policing &amp; Pre-Crime Rights</h1>
      <p className="text-gray-500 text-sm mb-6">Droits contre la police prédictive algorithmique et la criminalisation préventive</p>
      {!data ? <p className="text-gray-500">Chargement...</p> : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {(data.entities ?? []).map((e) => (
            <div key={e.entity} className="bg-white rounded-xl p-4 shadow text-center">
              <GaugeRing value={e.composite} color={e.level === "critique" ? "#ef4444" : e.level === "élevé" ? "#f97316" : e.level === "modéré" ? "#eab308" : "#22c55e"} />
              <p className="text-sm font-medium mt-2">{e.entity}</p>
              <p className="text-xs text-gray-500">{e.composite}</p>
            </div>
          ))}
        </div>
      )}
      {data?.avg_composite && <div className="mt-6 p-4 bg-gray-50 rounded-xl"><p className="font-bold">Score moyen: {data.avg_composite}</p></div>}
    </div>
  );
}
