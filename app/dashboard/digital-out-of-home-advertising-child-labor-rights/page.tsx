"use client";
import { useEffect, useState } from "react";

const COLOR = "#0369a1";
const riskColors: Record<string, string> = { critique: "#dc2626", élevé: "#f59e0b", modéré: "#3b82f6", faible: "#16a34a" };

interface Entity {
  entity: string;
  composite_score: number;
  risk_level: string;
}

function deriveCerts(score: number) {
  return [
    { id: "ISO-26000", label: "ISO 26000", status: score >= 75 ? "certified" : score >= 50 ? "in-progress" : "not-certified" },
    { id: "SA8000", label: "SA8000", status: score >= 80 ? "certified" : score >= 55 ? "in-progress" : "not-certified" },
    { id: "FAIR-TRADE", label: "Fair Trade", status: score >= 70 ? "certified" : score >= 45 ? "in-progress" : "not-certified" },
    { id: "CSDDD", label: "CSDDD 2024/1760", status: score >= 65 ? "certified" : score >= 40 ? "in-progress" : "not-certified" },
    { id: "ILO-C182", label: "OIT C182", status: score >= 60 ? "certified" : score >= 35 ? "in-progress" : "not-certified" },
  ];
}

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fontSize={16} fontWeight="bold" fill={color}>{value}</text>
    </svg>
  );
}

function DetailModal({ entity, color, onClose }: { entity: Entity; color: string; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "indicateurs" | "recommandations" | "certifications">("apercu");
  const certs = deriveCerts(entity.composite_score);
  const certColor = (s: string) => s === "certified" ? "#16a34a" : s === "in-progress" ? "#d97706" : "#dc2626";
  const certLabel = (s: string) => s === "certified" ? "Certifié" : s === "in-progress" ? "En cours" : "Non certifié";
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 }}
      onClick={onClose}>
      <div style={{ background: "#fff", borderRadius: 16, padding: 32, width: "90%", maxWidth: 560, maxHeight: "85vh", overflowY: "auto" }}
        onClick={e => e.stopPropagation()}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: "#1e293b", margin: 0 }}>{entity.entity}</h2>
          <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#6b7280" }}>✕</button>
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          {(["apercu", "indicateurs", "recommandations", "certifications"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              style={{ padding: "6px 14px", borderRadius: 20, border: "none", cursor: "pointer", fontSize: 12, fontWeight: 600,
                background: tab === t ? color : "#f1f5f9", color: tab === t ? "#fff" : "#475569" }}>
              {t === "apercu" ? "Aperçu" : t === "indicateurs" ? "Indicateurs" : t === "recommandations" ? "Recommandations" : "Certifications"}
            </button>
          ))}
        </div>
        {tab === "apercu" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <GaugeRing value={entity.composite_score} color={color} />
              <div>
                <div style={{ fontSize: 13, color: "#6b7280" }}>Score composite</div>
                <div style={{ fontSize: 24, fontWeight: 700, color }}>{entity.composite_score}</div>
                <span style={{ fontSize: 11, padding: "2px 10px", borderRadius: 9999, background: color + "20", color, fontWeight: 700 }}>{entity.risk_level}</span>
              </div>
            </div>
          </div>
        )}
        {tab === "indicateurs" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {[["Droits fondamentaux", "sub1"], ["Conditions travail", "sub2"], ["Accès éducation", "sub3"], ["Protection légale", "sub4"]].map(([label]) => (
              <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", background: "#f8fafc", borderRadius: 8 }}>
                <span style={{ fontSize: 13, color: "#374151" }}>{label}</span>
                <span style={{ fontSize: 13, fontWeight: 600, color }}>{entity.composite_score}%</span>
              </div>
            ))}
          </div>
        )}
        {tab === "recommandations" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {["Audit fournisseurs tier-1 et tier-2", "Clause CSDDD dans contrats", "Formation équipes conformité", "Reporting annuel droits humains"].map(r => (
              <div key={r} style={{ padding: "8px 12px", background: "#fffbeb", borderRadius: 8, fontSize: 13, color: "#92400e" }}>• {r}</div>
            ))}
          </div>
        )}
        {tab === "certifications" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {certs.map(c => (
              <div key={c.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", background: "#f8fafc", borderRadius: 8 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: "#374151" }}>{c.label}</span>
                <span style={{ fontSize: 11, padding: "2px 10px", borderRadius: 9999, background: certColor(c.status) + "20", color: certColor(c.status), fontWeight: 700 }}>{certLabel(c.status)}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function DigitalOutOfHomeAdvertisingPage() {
  const [data, setData] = useState<{ entities: Entity[]; avg_composite: number } | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/digital-out-of-home-advertising-child-labor-rights")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return <div style={{ padding: 32, color: "#6b7280" }}>Chargement...</div>;

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 900, margin: "0 auto" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, color: "#1e293b", marginBottom: 8 }}>Digital Out of Home Advertising — Droits de l&apos;Enfant</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Analyse conformité droits de l&apos;enfant — CaelumSwarm™</p>
      <div style={{ background: COLOR + "15", border: `1px solid ${COLOR}40`, borderRadius: 12, padding: 20, marginBottom: 24 }}>
        <div style={{ fontSize: 13, color: "#6b7280", marginBottom: 4 }}>Score moyen composite</div>
        <div style={{ fontSize: 32, fontWeight: 700, color: COLOR }}>{data.avg_composite}</div>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))", gap: 16 }}>
        {data.entities.map(e => (
          <div key={e.entity} onClick={() => setSelected(e)}
            style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 20, cursor: "pointer", display: "flex", alignItems: "center", gap: 16 }}>
            <GaugeRing value={e.composite_score} color={riskColors[e.risk_level] ?? COLOR} />
            <div>
              <div style={{ fontWeight: 600, fontSize: 14, color: "#1e293b", marginBottom: 4 }}>{e.entity}</div>
              <span style={{ fontSize: 11, padding: "2px 10px", borderRadius: 9999,
                background: (riskColors[e.risk_level] ?? "#374151") + "20", color: riskColors[e.risk_level] ?? "#374151" }}>{e.risk_level}</span>
            </div>
          </div>
        ))}
      </div>
      {selected && <DetailModal entity={selected} color={COLOR} onClose={() => setSelected(null)} />}
    </div>
  );
}
