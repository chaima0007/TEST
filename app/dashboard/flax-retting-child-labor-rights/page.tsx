"use client";
import { useEffect, useState } from "react";

const API_URL = "/api/flax-retting-child-labor-rights";
const TITLE = "Droits Enfants Rouissage Lin";
const COLOR = "#0369a1";

type Entity = { entity: string; composite_score: number; risk_level: string; estimated_flax_retting_child_labor_rights_index: number };
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
      <div style={{ background: "#fff", borderRadius: 12, padding: 24, width: 480, maxHeight: "80vh", overflowY: "auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <h3 style={{ fontWeight: 700, fontSize: 16 }}>{entity.entity}</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer" }}>×</button>
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {(["apercu", "indicateurs", "recommandations"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)} style={{ padding: "6px 12px", borderRadius: 6, border: "none", cursor: "pointer", background: tab === t ? color : "#f3f4f6", color: tab === t ? "#fff" : "#374151", fontWeight: tab === t ? 700 : 400 }}>{t}</button>
          ))}
        </div>
        {tab === "apercu" && (
          <div>
            <p style={{ marginBottom: 8 }}>Score composite : <strong>{entity.composite_score}</strong></p>
            <p style={{ marginBottom: 8 }}>Niveau de risque : <strong style={{ color }}>{entity.risk_level}</strong></p>
            <p>Indice estimé : <strong>{entity.estimated_flax_retting_child_labor_rights_index}</strong></p>
          </div>
        )}
        {tab === "indicateurs" && (
          <div>
            <p style={{ color: "#6b7280", fontSize: 14 }}>Indicateurs clés pour {entity.entity} dans le domaine du rouissage de lin.</p>
            <div style={{ marginTop: 12, padding: 12, background: "#f9fafb", borderRadius: 8 }}>
              <p>Score composite : {entity.composite_score}/100</p>
              <p>Indice domaine : {entity.estimated_flax_retting_child_labor_rights_index}/10</p>
            </div>
          </div>
        )}
        {tab === "recommandations" && (
          <div>
            <ul style={{ listStyle: "disc", paddingLeft: 20, color: "#374151", fontSize: 14 }}>
              <li style={{ marginBottom: 8 }}>Renforcer la supervision des chaînes d&apos;approvisionnement en lin</li>
              <li style={{ marginBottom: 8 }}>Mettre en œuvre des programmes de protection de l&apos;enfance</li>
              <li style={{ marginBottom: 8 }}>Auditer régulièrement les fournisseurs à haut risque</li>
              <li>Collaborer avec les ONG locales pour la sensibilisation</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Page() {
  const [data, setData] = useState<ApiData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch(API_URL).then(r => r.json()).then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return <div style={{ padding: 32, textAlign: "center", color: "#6b7280" }}>Chargement...</div>;

  const dist = data.distribution;
  return (
    <div style={{ padding: 32, maxWidth: 1200, margin: "0 auto" }}>
      <h1 style={{ fontSize: 28, fontWeight: 800, color: COLOR, marginBottom: 8 }}>{TITLE}</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Score moyen composite : <strong>{data.avg_composite}</strong></p>
      <div style={{ display: "flex", gap: 12, marginBottom: 32, flexWrap: "wrap" }}>
        {Object.entries(dist).map(([level, count]) => (
          <div key={level} style={{ background: "#f9fafb", border: "1px solid #e5e7eb", borderRadius: 8, padding: "8px 16px" }}>
            <span style={{ fontWeight: 700, color: COLOR }}>{count}</span> <span style={{ color: "#6b7280", fontSize: 14 }}>{level}</span>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: 16 }}>
        {data.entities.map(e => (
          <div key={e.entity} onClick={() => setSelected(e)} style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 20, cursor: "pointer" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 12 }}>
              <GaugeRing value={e.composite_score} color={COLOR} />
              <div>
                <p style={{ fontWeight: 700, fontSize: 14 }}>{e.entity}</p>
                <p style={{ fontSize: 12, color: COLOR, fontWeight: 600 }}>{e.risk_level}</p>
              </div>
            </div>
            <p style={{ fontSize: 12, color: "#6b7280" }}>Indice : {e.estimated_flax_retting_child_labor_rights_index}/10</p>
          </div>
        ))}
      </div>
      {selected && <DetailModal entity={selected} color={COLOR} onClose={() => setSelected(null)} />}
    </div>
  );
}
