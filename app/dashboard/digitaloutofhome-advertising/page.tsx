"use client";
import { useEffect, useState } from "react";

const COLOR = "#4f46e5";
const DOMAIN = "digitaloutofhome-advertising";
const INDEX_KEY = "estimated_digitaloutofhome_index";
const TITLE = "Digital Out-of-Home Advertising";

const SIGNALS = [
  "Facial recognition consent",
  "Crowd data collection",
  "Location privacy compliance",
  "Sensor data handling",
  "Audience measurement limits",
];

const ACTIONS = [
  "Ban facial recognition ads",
  "Limit crowd data usage",
  "Enforce location privacy",
  "Audit sensor data",
  "Cap audience measurement",
];

type Entity = { name: string; composite_score: number; risk_level: string; [key: string]: number | string };
type DashData = { entities: Entity[]; avg_composite: number; distribution: Record<string, number> };

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

function deriveCerts(score: number) {
  return [
    { id: "ISO-26000", label: "ISO 26000", status: score >= 75 ? "certified" : score >= 50 ? "in-progress" : "not-certified" },
    { id: "SA8000", label: "SA8000", status: score >= 80 ? "certified" : score >= 55 ? "in-progress" : "not-certified" },
    { id: "FAIR-TRADE", label: "Fair Trade", status: score >= 70 ? "certified" : score >= 45 ? "in-progress" : "not-certified" },
    { id: "CSDDD", label: "CSDDD 2024/1760", status: score >= 65 ? "certified" : score >= 40 ? "in-progress" : "not-certified" },
    { id: "ILO-C182", label: "OIT C182", status: score >= 60 ? "certified" : score >= 35 ? "in-progress" : "not-certified" },
  ];
}

function riskColor(level: string) {
  if (level === "critique") return "#dc2626";
  if (level === "élevé") return "#f97316";
  if (level === "modéré") return "#eab308";
  return "#22c55e";
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const score = Number(entity.composite_score);
  const certs = deriveCerts(score);
  const tabs = ["Aperçu", "Signaux", "Actions", "Certifications"];

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 }}>
      <div style={{ background: "#fff", borderRadius: 12, padding: 28, width: 480, maxHeight: "80vh", overflowY: "auto", boxShadow: "0 20px 60px rgba(0,0,0,0.3)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
          <div>
            <h2 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#111" }}>{entity.name}</h2>
            <span style={{ fontSize: 13, color: riskColor(String(entity.risk_level)), fontWeight: 600, textTransform: "capitalize" }}>{entity.risk_level}</span>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 22, cursor: "pointer", color: "#6b7280", lineHeight: 1 }}>×</button>
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 20, borderBottom: "1px solid #e5e7eb", paddingBottom: 12 }}>
          {tabs.map((t, i) => (
            <button key={t} onClick={() => setTab(i)} style={{ padding: "6px 14px", borderRadius: 6, border: "none", cursor: "pointer", fontSize: 13, fontWeight: 600, background: tab === i ? COLOR : "#f3f4f6", color: tab === i ? "#fff" : "#374151" }}>{t}</button>
          ))}
        </div>

        {tab === 0 && (
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 16 }}>
              <GaugeRing value={score} color={COLOR} />
              <div>
                <div style={{ fontSize: 13, color: "#6b7280" }}>Score composite</div>
                <div style={{ fontSize: 28, fontWeight: 800, color: COLOR }}>{score}</div>
                <div style={{ fontSize: 13, color: "#6b7280" }}>Index : {Number(entity[INDEX_KEY] ?? 0).toFixed(2)}</div>
              </div>
            </div>
            <p style={{ fontSize: 14, color: "#374151", lineHeight: 1.6 }}>
              Entité opérant dans le domaine <strong>{TITLE}</strong>. Niveau de risque : <strong>{entity.risk_level}</strong>.
            </p>
          </div>
        )}

        {tab === 1 && (
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {SIGNALS.map((s) => (
              <li key={s} style={{ padding: "10px 0", borderBottom: "1px solid #f3f4f6", fontSize: 14, color: "#374151", display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ width: 8, height: 8, borderRadius: "50%", background: COLOR, display: "inline-block", flexShrink: 0 }} />
                {s}
              </li>
            ))}
          </ul>
        )}

        {tab === 2 && (
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {ACTIONS.map((a, i) => (
              <li key={a} style={{ padding: "10px 0", borderBottom: "1px solid #f3f4f6", fontSize: 14, color: "#374151", display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ width: 22, height: 22, borderRadius: "50%", background: COLOR, color: "#fff", display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, flexShrink: 0 }}>{i + 1}</span>
                {a}
              </li>
            ))}
          </ul>
        )}

        {tab === 3 && (
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {certs.map((c) => (
              <li key={c.id} style={{ padding: "10px 0", borderBottom: "1px solid #f3f4f6", fontSize: 14, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: "#374151", fontWeight: 500 }}>{c.label}</span>
                <span style={{ fontSize: 12, fontWeight: 700, color: c.status === "certified" ? "#16a34a" : c.status === "in-progress" ? "#d97706" : "#dc2626", background: c.status === "certified" ? "#dcfce7" : c.status === "in-progress" ? "#fef3c7" : "#fee2e2", padding: "2px 10px", borderRadius: 20 }}>
                  {c.status === "certified" ? "Certifié" : c.status === "in-progress" ? "En cours" : "Non certifié"}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default function DigitaloutofhomeAdvertisingDashboard() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch(`/api/${DOMAIN}`)
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "60vh", fontSize: 16, color: "#6b7280" }}>Chargement…</div>;
  if (!data) return <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "60vh", fontSize: 16, color: "#dc2626" }}>Erreur de chargement</div>;

  const dist = data.distribution ?? {};

  return (
    <div style={{ padding: 32, maxWidth: 1100, margin: "0 auto", fontFamily: "system-ui, sans-serif" }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div style={{ marginBottom: 28 }}>
        <h1 style={{ margin: 0, fontSize: 26, fontWeight: 800, color: "#111" }}>{TITLE}</h1>
        <p style={{ margin: "6px 0 0", fontSize: 15, color: "#6b7280" }}>Surveillance des droits humains — domaine {DOMAIN}</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 28 }}>
        {[
          { label: "Score moyen", value: data.avg_composite?.toFixed(1) ?? "—", sub: "composite" },
          { label: "Critique", value: dist.critique ?? 0, sub: "entités" },
          { label: "Élevé", value: dist.élevé ?? 0, sub: "entités" },
          { label: "Total entités", value: data.entities?.length ?? 0, sub: "analysées" },
        ].map((card) => (
          <div key={card.label} style={{ background: "#fff", borderRadius: 10, padding: "18px 20px", boxShadow: "0 1px 4px rgba(0,0,0,0.08)", border: "1px solid #f3f4f6" }}>
            <div style={{ fontSize: 13, color: "#6b7280", marginBottom: 6 }}>{card.label}</div>
            <div style={{ fontSize: 28, fontWeight: 800, color: COLOR }}>{card.value}</div>
            <div style={{ fontSize: 12, color: "#9ca3af" }}>{card.sub}</div>
          </div>
        ))}
      </div>

      <div style={{ background: "#fff", borderRadius: 10, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", border: "1px solid #f3f4f6", overflow: "hidden", marginBottom: 28 }}>
        <div style={{ padding: "16px 20px", borderBottom: "1px solid #f3f4f6" }}>
          <h2 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: "#111" }}>Entités surveillées</h2>
        </div>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
            <thead>
              <tr style={{ background: "#f9fafb" }}>
                {["Entité", "Score", "Niveau", "Index", "Détail"].map((h) => (
                  <th key={h} style={{ padding: "10px 16px", textAlign: "left", fontWeight: 600, color: "#374151", borderBottom: "1px solid #e5e7eb" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(data.entities ?? []).map((e, i) => (
                <tr key={i} style={{ borderBottom: "1px solid #f3f4f6" }}>
                  <td style={{ padding: "12px 16px", fontWeight: 500, color: "#111" }}>{e.name}</td>
                  <td style={{ padding: "12px 16px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <div style={{ width: 100, height: 6, background: "#e5e7eb", borderRadius: 3, overflow: "hidden" }}>
                        <div style={{ width: `${e.composite_score}%`, height: "100%", background: COLOR, borderRadius: 3 }} />
                      </div>
                      <span style={{ fontWeight: 700, color: COLOR }}>{e.composite_score}</span>
                    </div>
                  </td>
                  <td style={{ padding: "12px 16px" }}>
                    <span style={{ fontSize: 12, fontWeight: 700, color: riskColor(String(e.risk_level)), background: riskColor(String(e.risk_level)) + "20", padding: "3px 10px", borderRadius: 20, textTransform: "capitalize" }}>{e.risk_level}</span>
                  </td>
                  <td style={{ padding: "12px 16px", color: "#374151" }}>{Number(e[INDEX_KEY] ?? 0).toFixed(2)}</td>
                  <td style={{ padding: "12px 16px" }}>
                    <button onClick={() => setSelected(e)} style={{ background: COLOR, color: "#fff", border: "none", borderRadius: 6, padding: "5px 12px", fontSize: 12, fontWeight: 600, cursor: "pointer" }}>Voir</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div style={{ background: "#fff", borderRadius: 10, padding: 20, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", border: "1px solid #f3f4f6" }}>
          <h3 style={{ margin: "0 0 14px", fontSize: 15, fontWeight: 700, color: "#111" }}>Signaux de risque</h3>
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {SIGNALS.map((s) => (
              <li key={s} style={{ padding: "8px 0", borderBottom: "1px solid #f9fafb", fontSize: 14, color: "#374151", display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ width: 8, height: 8, borderRadius: "50%", background: COLOR, display: "inline-block", flexShrink: 0 }} />{s}
              </li>
            ))}
          </ul>
        </div>
        <div style={{ background: "#fff", borderRadius: 10, padding: 20, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", border: "1px solid #f3f4f6" }}>
          <h3 style={{ margin: "0 0 14px", fontSize: 15, fontWeight: 700, color: "#111" }}>Actions recommandées</h3>
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {ACTIONS.map((a, i) => (
              <li key={a} style={{ padding: "8px 0", borderBottom: "1px solid #f9fafb", fontSize: 14, color: "#374151", display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ width: 22, height: 22, borderRadius: "50%", background: COLOR, color: "#fff", display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, flexShrink: 0 }}>{i + 1}</span>{a}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
