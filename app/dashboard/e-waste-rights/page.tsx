"use client";
import { useEffect, useState } from "react";

function GaugeRing({ score }: { score: number }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(100, score));
  const offset = circ * (1 - pct / 100);
  const color = score >= 60 ? "#dc2626" : score >= 40 ? "#f97316" : score >= 20 ? "#eab308" : "#22c55e";
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        style={{ fontSize: 16, fontWeight: 700, fill: color }}>{score}</text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: any; onClose: () => void }) {
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center" }} onClick={onClose}>
      <div style={{ background: "#fff", borderRadius: 12, padding: 24, maxWidth: 480, width: "90%", maxHeight: "80vh", overflowY: "auto" }} onClick={e => e.stopPropagation()}>
        <h3 style={{ fontWeight: 700, fontSize: 18, marginBottom: 12 }}>{entity.entity}</h3>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {["Analyse", "Entités", "Méthodologie"].map(tab => (
            <span key={tab} style={{ padding: "4px 12px", borderRadius: 20, background: "#f1f5f9", fontSize: 13 }}>{tab}</span>
          ))}
        </div>
        <p style={{ color: "#64748b", fontSize: 14 }}>Score composite : <strong>{entity.composite_score}</strong></p>
        <p style={{ color: "#64748b", fontSize: 14 }}>Niveau de risque : <strong>{entity.risk_level}</strong></p>
        <button onClick={onClose} style={{ marginTop: 16, padding: "8px 20px", background: "#1e293b", color: "#fff", borderRadius: 8, border: "none", cursor: "pointer" }}>Fermer</button>
      </div>
    </div>
  );
}

export default function EWasteRightsDashboard() {
  const [data, setData] = useState<any>(null);
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => {
    fetch("/api/e-waste-rights")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return <div style={{ padding: 40, textAlign: "center" }}>Chargement...</div>;

  const entities = data.entities ?? [];
  const avg = data.avg_composite ?? 0;

  return (
    <main style={{ minHeight: "100vh", background: "#f8fafc", padding: 32 }}>
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "#1e293b", marginBottom: 8 }}>
        Droits contre les Déchets Électroniques
      </h1>
      <p style={{ color: "#64748b", marginBottom: 32 }}>Analyse CaelumSwarm™ — Gestion des déchets électroniques</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 16, marginBottom: 32 }}>
        {entities.map((e: any) => (
          <div key={e.entity} onClick={() => setSelected(e)}
            style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
            <GaugeRing score={Math.round(e.composite_score)} />
            <div style={{ textAlign: "center" }}>
              <div style={{ fontWeight: 700, fontSize: 15 }}>{e.entity}</div>
              <div style={{ fontSize: 12, color: e.risk_level === "critique" ? "#dc2626" : e.risk_level === "élevé" ? "#f97316" : e.risk_level === "modéré" ? "#eab308" : "#22c55e" }}>
                {e.risk_level}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", display: "inline-block" }}>
        <div style={{ fontSize: 13, color: "#64748b" }}>Score moyen</div>
        <div style={{ fontSize: 32, fontWeight: 800, color: "#1e293b" }}>{avg.toFixed(2)}</div>
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </main>
  );
}
