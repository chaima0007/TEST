"use client";
import { useEffect, useState } from "react";

const ACCENT = "#8b5cf6";

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100);
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={44} cy={44} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={circ * (1 - pct / 100)}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={44} y={48} textAnchor="middle" fill={color} fontSize={16} fontWeight="bold">
        {Math.round(pct)}
      </text>
    </svg>
  );
}

function DetailModal({ entity, onClose, accent }: { entity: any; onClose: () => void; accent: string }) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "sources">("apercu");
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}
      onClick={onClose}>
      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 24, maxWidth: 600, width: "90%", maxHeight: "80vh", overflowY: "auto" }}
        onClick={e => e.stopPropagation()}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
          <h3 style={{ color: "#f1f5f9", fontSize: 16, fontWeight: 600 }}>{entity?.name}</h3>
          <button onClick={onClose} style={{ color: "#94a3b8", background: "none", border: "none", cursor: "pointer", fontSize: 20 }}>×</button>
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {(["apercu", "metriques", "sources"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              style={{ padding: "6px 12px", borderRadius: 6, border: "none", cursor: "pointer",
                background: tab === t ? accent : "#1e293b", color: tab === t ? "#fff" : "#94a3b8" }}>
              {t}
            </button>
          ))}
        </div>
        {tab === "apercu" && (
          <div style={{ color: "#cbd5e1", fontSize: 14, lineHeight: 1.6 }}>
            <div style={{ marginBottom: 8 }}>Score composite: <strong style={{ color: accent }}>{entity?.composite_score}</strong></div>
            <div style={{ marginBottom: 8 }}>Niveau de risque: <strong style={{ color: accent }}>{entity?.risk_level}</strong></div>
            <div>Pays: {entity?.country}</div>
          </div>
        )}
        {tab === "metriques" && (
          <div style={{ color: "#cbd5e1", fontSize: 13 }}>
            {entity && Object.entries(entity).filter(([k]) => k.endsWith("_score") && k !== "composite_score").map(([k, v]) => (
              <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "4px 0", borderBottom: "1px solid #1e293b" }}>
                <span>{k.replace(/_score$/, "").replace(/_/g, " ")}</span>
                <strong style={{ color: accent }}>{String(v)}</strong>
              </div>
            ))}
          </div>
        )}
        {tab === "sources" && (
          <div style={{ color: "#94a3b8", fontSize: 13 }}>
            {(entity?.key_signals || [entity?.primary_pattern]).map((s: string, i: number) => (
              <div key={i} style={{ padding: "6px 0", borderBottom: "1px solid #1e293b" }}>{s}</div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function Page() {
  const [data, setData] = useState<any>(null);
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => {
    fetch("/api/digital-privacy-rights-engine")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return <div style={{ color: "#94a3b8", padding: 40 }}>Chargement...</div>;

  return (
    <div style={{ background: "#020617", minHeight: "100vh", color: "#f1f5f9", fontFamily: "system-ui,sans-serif" }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} accent={ACCENT} />}
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "32px 24px" }}>
        <div style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 28, fontWeight: 700, color: ACCENT }}>Vie Priv&#233;e Num&#233;rique &amp; Surveillance de Masse</h1>
          <div style={{ display: "flex", gap: 24, marginTop: 16 }}>
            <div style={{ background: "#0f172a", borderRadius: 8, padding: 16, flex: 1 }}>
              <GaugeRing value={data.avg_composite} color={ACCENT} />
              <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 8 }}>Score moyen</div>
            </div>
            <div style={{ background: "#0f172a", borderRadius: 8, padding: 16, flex: 1 }}>
              <div style={{ fontSize: 32, fontWeight: 700, color: ACCENT }}>{data.total_entities}</div>
              <div style={{ color: "#94a3b8", fontSize: 12 }}>Entit&#233;s analys&#233;es</div>
            </div>
            <div style={{ background: "#0f172a", borderRadius: 8, padding: 16, flex: 1 }}>
              <div style={{ fontSize: 32, fontWeight: 700, color: "#ef4444" }}>
                {data.risk_distribution?.critique ?? 0}
              </div>
              <div style={{ color: "#94a3b8", fontSize: 12 }}>Niveau critique</div>
            </div>
          </div>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(300px,1fr))", gap: 16 }}>
          {(data.entities ?? []).map((e: any) => (
            <div key={e.entity_id} onClick={() => setSelected(e)}
              style={{ background: "#0f172a", borderRadius: 8, padding: 16, cursor: "pointer",
                border: `1px solid ${e.risk_level === "critique" ? "#ef4444" : e.risk_level === "élevé" ? "#f59e0b" : "#1e293b"}`,
                transition: "border-color 0.2s" }}>
              <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>{e.entity_id}</div>
              <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9", marginBottom: 8, lineHeight: 1.4 }}>{e.name}</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <GaugeRing value={e.composite_score} color={
                  e.risk_level === "critique" ? "#ef4444" : e.risk_level === "élevé" ? "#f59e0b" : e.risk_level === "modéré" ? "#22c55e" : "#3b82f6"
                } />
                <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 4,
                  background: e.risk_level === "critique" ? "#7f1d1d" : e.risk_level === "élevé" ? "#78350f" : e.risk_level === "modéré" ? "#14532d" : "#1e3a5f",
                  color: e.risk_level === "critique" ? "#fca5a5" : e.risk_level === "élevé" ? "#fde68a" : e.risk_level === "modéré" ? "#86efac" : "#93c5fd" }}>
                  {e.risk_level}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
