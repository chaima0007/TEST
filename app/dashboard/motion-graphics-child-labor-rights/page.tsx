"use client";
import { useEffect, useState } from "react";

const API_URL = "/api/motion-graphics-child-labor-rights";
const TITLE = "Droits Enfants Motion Graphics";
const COLOR = "#0e7490";

type Entity = { entity: string; composite_score: number; risk_level: string };
type ApiData = { entities: Entity[]; avg_composite: number; distribution: Record<string, number> };

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100);
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={`${(pct / 100) * circ} ${circ}`}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize={14} fontWeight="bold" fill={color}>{Math.round(pct)}</text>
    </svg>
  );
}

function DetailModal({ entity, color, onClose }: { entity: Entity; color: string; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "indicateurs" | "recommandations">("apercu");
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}>
      <div style={{ background: "#fff", borderRadius: 12, padding: 24, width: 480, maxWidth: "90vw" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
          <h2 style={{ fontWeight: "bold", fontSize: 18 }}>{entity.entity}</h2>
          <button onClick={onClose} style={{ cursor: "pointer", fontSize: 20 }}>×</button>
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {(["apercu", "indicateurs", "recommandations"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              style={{ padding: "4px 12px", borderRadius: 6, border: "1px solid #e5e7eb",
                background: tab === t ? color : "#f9fafb", color: tab === t ? "#fff" : "#374151", cursor: "pointer" }}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "apercu" && <div><p style={{ marginBottom: 8 }}>Score : <strong>{entity.composite_score}</strong></p><p>Risque : <strong style={{ color }}>{entity.risk_level}</strong></p></div>}
        {tab === "indicateurs" && <p>Conformité CSDDD 2024/1760 — surveillance active requise.</p>}
        {tab === "recommandations" && <p>Renforcer la surveillance des chaînes d&apos;approvisionnement et appliquer les normes CSDDD 2024/1760.</p>}
      </div>
    </div>
  );
}

export default function Page() {
  const [data, setData] = useState<ApiData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  useEffect(() => {
    fetch(API_URL).then(r => r.json()).then(d => setData(d.payload ?? d)).catch(console.error);
  }, []);
  if (!data) return <div style={{ padding: 32, textAlign: "center" }}>Chargement…</div>;
  const riskColors: Record<string, string> = { critique: "#dc2626", élevé: "#ea580c", modéré: "#d97706", faible: "#16a34a" };
  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 900, margin: "0 auto" }}>
      <h1 style={{ fontSize: 28, fontWeight: "bold", color: COLOR, marginBottom: 8 }}>{TITLE}</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Score moyen composite : <strong>{data.avg_composite}</strong></p>
      <div style={{ display: "flex", gap: 16, marginBottom: 32, flexWrap: "wrap" }}>
        {Object.entries(data.distribution).map(([level, count]) => (
          <div key={level} style={{ background: "#f9fafb", border: "1px solid #e5e7eb", borderRadius: 8, padding: "12px 20px", minWidth: 120, textAlign: "center" }}>
            <div style={{ fontSize: 24, fontWeight: "bold", color: riskColors[level] ?? "#374151" }}>{count as number}</div>
            <div style={{ fontSize: 12, color: "#6b7280", textTransform: "capitalize" }}>{level}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16 }}>
        {data.entities.map(e => (
          <div key={e.entity} onClick={() => setSelected(e)}
            style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 16, cursor: "pointer", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
              <span style={{ fontWeight: 600, fontSize: 13 }}>{e.entity}</span>
              <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 9999, background: (riskColors[e.risk_level] ?? "#374151") + "20", color: riskColors[e.risk_level] ?? "#374151" }}>{e.risk_level}</span>
            </div>
            <GaugeRing value={e.composite_score} color={riskColors[e.risk_level] ?? COLOR} />
          </div>
        ))}
      </div>
      {selected && <DetailModal entity={selected} color={COLOR} onClose={() => setSelected(null)} />}
    </div>
  );
}
