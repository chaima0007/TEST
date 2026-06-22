"use client";
import { useState, useEffect } from "react";

const ACCENT = "#1a0a05";
const ACCENT_LIGHT = "#f97316";
const RC: Record<string, string> = { critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

function GaugeRing({ value }: { value: number }) {
  const r = 36, cx = 44, cy = 44, circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100) / 100;
  return (
    <svg viewBox="0 0 88 88" style={{ width: 96, height: 96 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={ACCENT_LIGHT} strokeWidth={8}
        strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 44 44)" />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={ACCENT_LIGHT} fontSize="14" fontWeight="700">{Math.round(value)}</text>
    </svg>
  );
}

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_arms_trade_rights_index: number;
  [key: string]: unknown;
}

interface DashData {
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  critical_alerts: string[];
  data_sources: string[];
  entities: Entity[];
}

export default function Page() {
  const [data, setData] = useState<DashData | null>(null);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    fetch("/api/arms-trade-rights-engine").then(r => r.json()).then(d => setData(d.payload ?? d)).catch(console.error);
  }, []);

  if (!data) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <p style={{ color: "#94a3b8" }}>Chargement...</p>
    </div>
  );

  const filtered = data.entities.filter(e => filter === "tous" || e.risk_level === filter);

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "#f1f5f9", padding: "24px" }}>
      <div style={{ marginBottom: "32px" }}>
        <h1 style={{ fontSize: "30px", fontWeight: 700, color: ACCENT_LIGHT, margin: 0 }}>Arms Trade Rights Engine</h1>
        <p style={{ color: "#94a3b8", marginTop: "4px" }}>Commerce d&apos;Armes · Droits Humanitaires · Trafic Illicite · ATT Treaty</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "16px", marginBottom: "32px" }}>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
          <p style={{ fontSize: "11px", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: 0 }}>Entités</p>
          <p style={{ fontSize: "28px", fontWeight: 700, color: ACCENT_LIGHT, margin: "4px 0 0" }}>{data.total_entities}</p>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px", display: "flex", flexDirection: "column", alignItems: "center" }}>
          <p style={{ fontSize: "11px", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 8px" }}>Score Moyen</p>
          <GaugeRing value={data.avg_composite} />
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
          <p style={{ fontSize: "11px", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: 0 }}>Critiques</p>
          <p style={{ fontSize: "28px", fontWeight: 700, color: "#ef4444", margin: "4px 0 0" }}>{data.risk_distribution?.critique ?? 0}</p>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
          <p style={{ fontSize: "11px", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: 0 }}>Élevés</p>
          <p style={{ fontSize: "28px", fontWeight: 700, color: "#f97316", margin: "4px 0 0" }}>{data.risk_distribution?.["élevé"] ?? 0}</p>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
          <p style={{ fontSize: "11px", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: 0 }}>Confiance</p>
          <p style={{ fontSize: "28px", fontWeight: 700, color: ACCENT_LIGHT, margin: "4px 0 0" }}>{Math.round((data.confidence_score ?? 0) * 100)}%</p>
        </div>
      </div>

      {data.critical_alerts && data.critical_alerts.length > 0 && (
        <div style={{ background: "#1a0505", border: "1px solid #7f1d1d", borderRadius: "12px", padding: "16px", marginBottom: "24px" }}>
          <p style={{ fontSize: "12px", fontWeight: 600, color: "#ef4444", textTransform: "uppercase", marginBottom: "8px" }}>Alertes Critiques</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {data.critical_alerts.map((a, i) => (
              <span key={i} style={{ background: "#450a0a", border: "1px solid #7f1d1d", borderRadius: "6px", padding: "4px 10px", fontSize: "12px", color: "#fca5a5" }}>{a}</span>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: "flex", gap: "8px", marginBottom: "24px", flexWrap: "wrap" }}>
        {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            padding: "6px 16px", borderRadius: "9999px", fontSize: "13px", fontWeight: 500, cursor: "pointer",
            background: filter === f ? "#431407" : "transparent",
            border: filter === f ? "1px solid #ea580c" : "1px solid #334155",
            color: filter === f ? ACCENT_LIGHT : "#94a3b8",
          }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "16px", marginBottom: "32px" }}>
        {filtered.map(e => (
          <button key={e.id} onClick={() => { setSelected(e); setTab(0); }} style={{
            textAlign: "left", border: "1px solid", borderRadius: "12px", padding: "16px", cursor: "pointer",
            borderColor: e.risk_level === "critique" ? "#7f1d1d" : e.risk_level === "élevé" ? "#7c2d12" : e.risk_level === "modéré" ? "#713f12" : "#14532d",
            background: e.risk_level === "critique" ? "#1a0505" : e.risk_level === "élevé" ? "#1c0a00" : e.risk_level === "modéré" ? "#1a1200" : "#001a0a",
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
              <span style={{ fontSize: "11px", fontFamily: "monospace", color: "#64748b" }}>{e.id}</span>
              <span style={{ fontSize: "11px", fontWeight: 600, textTransform: "uppercase", color: RC[e.risk_level] }}>{e.risk_level}</span>
            </div>
            <p style={{ fontWeight: 600, fontSize: "13px", color: "#f1f5f9", margin: "0 0 6px", lineHeight: 1.4, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>{e.name}</p>
            <p style={{ fontSize: "12px", color: "#64748b", margin: 0 }}>{e.country}</p>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "12px" }}>
              <span style={{ fontSize: "11px", color: "#64748b" }}>Score composite</span>
              <span style={{ fontSize: "20px", fontWeight: 700, color: ACCENT_LIGHT }}>{e.composite_score}</span>
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", padding: "16px" }}
          onClick={() => setSelected(null)}>
          <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: "16px", width: "100%", maxWidth: "600px", maxHeight: "85vh", overflowY: "auto" }}
            onClick={e => e.stopPropagation()}>
            <div style={{ padding: "24px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div>
                <span style={{ fontSize: "11px", fontWeight: 600, textTransform: "uppercase", color: RC[selected.risk_level] }}>{selected.risk_level}</span>
                <h2 style={{ fontSize: "17px", fontWeight: 700, color: "#f1f5f9", margin: "4px 0 0" }}>{selected.name}</h2>
                <p style={{ fontSize: "13px", color: "#64748b", margin: "4px 0 0" }}>{selected.country}</p>
              </div>
              <button onClick={() => setSelected(null)} style={{ background: "none", border: "none", color: "#64748b", fontSize: "20px", cursor: "pointer" }}>✕</button>
            </div>
            <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
              {["Aperçu", "Métriques", "Sources"].map((t, i) => (
                <button key={t} onClick={() => setTab(i)} style={{
                  flex: 1, padding: "12px", fontSize: "13px", fontWeight: 500, cursor: "pointer", background: "none", border: "none",
                  borderBottom: tab === i ? `2px solid ${ACCENT_LIGHT}` : "2px solid transparent",
                  color: tab === i ? ACCENT_LIGHT : "#64748b",
                }}>{t}</button>
              ))}
            </div>
            <div style={{ padding: "24px" }}>
              {tab === 0 && (
                <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span style={{ color: "#94a3b8" }}>Score composite</span>
                    <span style={{ fontSize: "24px", fontWeight: 700, color: ACCENT_LIGHT }}>{selected.composite_score}/100</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: "14px" }}>
                    <span style={{ color: "#94a3b8" }}>Pattern principal</span>
                    <span style={{ color: "#f1f5f9" }}>{String(selected.primary_pattern).replace(/_/g, " ")}</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: "14px" }}>
                    <span style={{ color: "#94a3b8" }}>Indice ATR</span>
                    <span style={{ color: ACCENT_LIGHT, fontWeight: 600 }}>{selected.estimated_arms_trade_rights_index}</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: "14px" }}>
                    <span style={{ color: "#94a3b8" }}>Pays</span>
                    <span style={{ color: "#f1f5f9" }}>{selected.country}</span>
                  </div>
                </div>
              )}
              {tab === 1 && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  <div>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "13px", marginBottom: "4px" }}>
                      <span style={{ color: "#94a3b8" }}>Score composite</span>
                      <span style={{ color: "#f1f5f9" }}>{selected.composite_score}/100</span>
                    </div>
                    <div style={{ height: "6px", background: "#1e293b", borderRadius: "3px", overflow: "hidden" }}>
                      <div style={{ height: "100%", width: `${selected.composite_score}%`, background: ACCENT_LIGHT, borderRadius: "3px" }} />
                    </div>
                  </div>
                  <div>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "13px", marginBottom: "4px" }}>
                      <span style={{ color: "#94a3b8" }}>Indice Droits Commerce Armes</span>
                      <span style={{ color: "#f1f5f9" }}>{Number(selected.estimated_arms_trade_rights_index) * 10}/100</span>
                    </div>
                    <div style={{ height: "6px", background: "#1e293b", borderRadius: "3px", overflow: "hidden" }}>
                      <div style={{ height: "100%", width: `${Number(selected.estimated_arms_trade_rights_index) * 10}%`, background: RC[selected.risk_level], borderRadius: "3px" }} />
                    </div>
                  </div>
                </div>
              )}
              {tab === 2 && (
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  <p style={{ fontSize: "13px", color: "#94a3b8", margin: "0 0 8px" }}>Sources de données utilisées pour cette analyse :</p>
                  {(data.data_sources ?? []).map((s, i) => (
                    <div key={i} style={{ display: "flex", gap: "8px", alignItems: "flex-start", fontSize: "13px" }}>
                      <span style={{ color: ACCENT_LIGHT, marginTop: "2px" }}>▸</span>
                      <span style={{ color: "#cbd5e1" }}>{s.replace(/_/g, " ")}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
