"use client";
import { useEffect, useState } from "react";

interface EntityResult {
  entity: string;
  composite_score: number;
  risk_level: string;
  [key: string]: unknown;
}
interface EngineData {
  entities: EntityResult[];
  avg_composite: number;
  distribution: Record<string, number>;
}

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

export default function DomainDashboard() {
  const [data, setData] = useState<EngineData | null>(null);
  const [selected, setSelected] = useState<EntityResult | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    fetch("/api/cottonseed-child-labor-rights")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return <div style={{ padding: 40, textAlign: "center" }}>Chargement...</div>;

  const riskColor = (r: string) =>
    r === "critique" ? "#dc2626" : r === "élevé" ? "#f97316" : r === "modéré" ? "#eab308" : "#22c55e";

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 32, fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 28, fontWeight: 800, marginBottom: 8 }}>Droits Enfants — Production Graines de Coton</h1>
      <p style={{ color: "#6b7280", marginBottom: 32 }}>Score moyen composite : <strong>{data.avg_composite}</strong>/100</p>
      <div style={{ display: "flex", gap: 16, marginBottom: 32, flexWrap: "wrap" }}>
        {Object.entries(data.distribution).map(([level, count]) => (
          <div key={level} style={{ background: riskColor(level), color: "#fff", borderRadius: 8, padding: "8px 20px", fontWeight: 700 }}>
            {level} : {count}
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 20 }}>
        {data.entities.map(e => (
          <div key={e.entity} onClick={() => { setSelected(e); setTab(0); }}
            style={{ background: "#fff", border: `2px solid ${riskColor(e.risk_level)}`, borderRadius: 12, padding: 20, cursor: "pointer", textAlign: "center" }}>
            <GaugeRing score={Math.round(e.composite_score)} />
            <div style={{ marginTop: 8, fontWeight: 700 }}>{e.entity}</div>
            <div style={{ color: riskColor(e.risk_level), fontSize: 13 }}>{e.risk_level}</div>
          </div>
        ))}
      </div>
      {selected && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}
          onClick={() => setSelected(null)}>
          <div style={{ background: "#fff", borderRadius: 16, padding: 32, maxWidth: 480, width: "90%", maxHeight: "80vh", overflow: "auto" }}
            onClick={e => e.stopPropagation()}>
            <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
              {["Aperçu", "Indicateurs", "Recommandations"].map((t, i) => (
                <button key={i} onClick={() => setTab(i)}
                  style={{ padding: "6px 16px", borderRadius: 8, border: "none", cursor: "pointer",
                    background: tab === i ? "#1e40af" : "#e5e7eb", color: tab === i ? "#fff" : "#374151", fontWeight: 600 }}>
                  {t}
                </button>
              ))}
            </div>
            {tab === 0 && (
              <div>
                <h2 style={{ fontWeight: 800, marginBottom: 8 }}>{selected.entity}</h2>
                <GaugeRing score={Math.round(selected.composite_score)} />
                <p style={{ marginTop: 12 }}>Niveau : <strong style={{ color: riskColor(selected.risk_level) }}>{selected.risk_level}</strong></p>
                <p>Score : <strong>{selected.composite_score}</strong></p>
              </div>
            )}
            {tab === 1 && (
              <div>
                <h3 style={{ fontWeight: 700 }}>Indicateurs</h3>
                <p>Score composite : {selected.composite_score}/100</p>
                <p>Niveau : {selected.risk_level}</p>
              </div>
            )}
            {tab === 2 && (
              <div>
                <h3 style={{ fontWeight: 700 }}>Recommandations CSDDD</h3>
                <p>Conformité EU 2024/1760 — audit obligatoire, risque {selected.risk_level}.</p>
              </div>
            )}
            <button onClick={() => setSelected(null)}
              style={{ marginTop: 20, padding: "8px 24px", background: "#1e40af", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: 600 }}>
              Fermer
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
