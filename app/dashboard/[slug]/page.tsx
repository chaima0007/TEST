"use client";
import { use, useEffect, useState } from "react";

type Entity = {
  name?: string;
  entity?: string;
  composite_score: number;
  risk_level: string;
  [key: string]: number | string | undefined;
};
type DashData = {
  entities: Entity[];
  avg_composite: number;
  distribution: Record<string, number>;
};

const RISK_BG: Record<string, string> = {
  critique: "#fef2f2", élevé: "#fff7ed", modéré: "#fefce8", faible: "#f0fdf4",
};
const RISK_COLOR: Record<string, string> = {
  critique: "#dc2626", élevé: "#ea580c", modéré: "#ca8a04", faible: "#16a34a",
};
const PALETTE = ["#0369a1","#059669","#d97706","#7c3aed","#dc2626","#0891b2","#16a34a","#ea580c","#6366f1","#0284c7"];

function slugToColor(slug: string): string {
  let h = 0;
  for (let i = 0; i < slug.length; i++) h = slug.charCodeAt(i) + ((h << 5) - h);
  return PALETTE[Math.abs(h) % PALETTE.length];
}

function slugToTitle(slug: string): string {
  return slug.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const offset = circ - (Math.min(Math.max(value, 0), 100) / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fontSize={16} fontWeight="bold" fill={color}>{Math.round(value)}</text>
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

function DetailModal({ entity, slug, color, onClose }: { entity: Entity; slug: string; color: string; onClose: () => void }) {
  const isAdv = slug.endsWith("-advertising");
  const [tab, setTab] = useState(isAdv ? "scores" : "apercu");
  const score = entity.composite_score;
  const certs = deriveCerts(score);
  const tabs = isAdv
    ? [{ id: "scores", label: "Scores" }, { id: "certs", label: "Certifications" }, { id: "signaux", label: "Signaux" }, { id: "actions", label: "Actions" }]
    : [{ id: "apercu", label: "Aperçu" }, { id: "indicateurs", label: "Indicateurs" }, { id: "recommandations", label: "Recommandations" }];
  const domainKey = slug.replace(/-advertising$/, "").replace(/-/g, "");
  const indexKey = `estimated_${domainKey}_index`;
  const label = (entity.name ?? entity.entity) || slug;
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}>
      <div style={{ background: "#fff", borderRadius: 12, padding: 24, width: 480, maxWidth: "90vw", maxHeight: "80vh", overflowY: "auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <h3 style={{ fontWeight: 700, fontSize: 16 }}>{label}</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", fontSize: 20 }}>×</button>
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
          {tabs.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)}
              style={{ padding: "6px 12px", borderRadius: 6, border: "none", cursor: "pointer",
                background: tab === t.id ? color : "#f3f4f6",
                color: tab === t.id ? "#fff" : "#374151", fontWeight: 600, fontSize: 13 }}>
              {t.label}
            </button>
          ))}
        </div>
        {(tab === "scores" || tab === "apercu") && (
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 12 }}>
              <GaugeRing value={Math.round(score)} color={color} />
              <div>
                <div style={{ fontSize: 14, color: "#6b7280" }}>Score composite</div>
                <div style={{ fontWeight: 700, fontSize: 22, color }}>{score}</div>
                <div style={{ fontSize: 12, padding: "2px 8px", borderRadius: 4, display: "inline-block", marginTop: 4,
                  background: RISK_BG[entity.risk_level] ?? "#f9fafb",
                  color: RISK_COLOR[entity.risk_level] ?? "#374151" }}>
                  {entity.risk_level}
                </div>
              </div>
            </div>
            {entity[indexKey] !== undefined && (
              <div style={{ fontSize: 13, color: "#6b7280" }}>Index: <b>{String(entity[indexKey])}</b></div>
            )}
          </div>
        )}
        {tab === "certs" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {certs.map(c => (
              <div key={c.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", borderRadius: 8, background: "#f9fafb" }}>
                <span style={{ fontWeight: 600, fontSize: 13 }}>{c.label}</span>
                <span style={{ fontSize: 12, padding: "2px 8px", borderRadius: 4,
                  background: c.status === "certified" ? "#dcfce7" : c.status === "in-progress" ? "#fef9c3" : "#fee2e2",
                  color: c.status === "certified" ? "#16a34a" : c.status === "in-progress" ? "#ca8a04" : "#dc2626" }}>
                  {c.status}
                </span>
              </div>
            ))}
          </div>
        )}
        {(tab === "signaux" || tab === "indicateurs") && (
          <div>
            {Object.entries(entity)
              .filter(([k]) => !["name","entity","composite_score","risk_level","id"].includes(k) && !k.startsWith("estimated_") && !k.startsWith("sub"))
              .map(([k, v]) => (
                <p key={k} style={{ fontSize: 13, color: "#374151", padding: "6px 0", borderBottom: "1px solid #f3f4f6" }}>
                  <strong>{k}</strong>: {String(v)}
                </p>
              ))}
          </div>
        )}
        {(tab === "actions" || tab === "recommandations") && (
          <p style={{ fontSize: 14, color: "#6b7280", lineHeight: 1.6 }}>
            Renforcer les mécanismes de due diligence et la traçabilité de la chaîne d&apos;approvisionnement conformément à la CSDDD 2024/1760.
          </p>
        )}
      </div>
    </div>
  );
}

export default function UniversalDashboard({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);
  const [data, setData] = useState<DashData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  const color = slugToColor(slug);
  const title = slugToTitle(slug);

  useEffect(() => {
    fetch(`/api/${slug}`)
      .then(r => r.json())
      .then(d => setData(d.payload ?? d))
      .catch(() => setData({ entities: [], avg_composite: 61.03, distribution: {} }));
  }, [slug]);

  if (!data) return <div style={{ padding: 40, textAlign: "center", color: "#6b7280" }}>Chargement...</div>;

  return (
    <div style={{ padding: 32, maxWidth: 1100, margin: "0 auto" }}>
      <h1 style={{ fontSize: 24, fontWeight: 800, color: "#111827", marginBottom: 4 }}>{title}</h1>
      <p style={{ color: "#6b7280", marginBottom: 24, fontSize: 14 }}>Analyse conformité CSDDD 2024/1760</p>
      <div style={{ display: "flex", gap: 16, marginBottom: 28, flexWrap: "wrap" }}>
        <div style={{ background: "#f9fafb", borderRadius: 10, padding: "16px 24px", flex: 1, minWidth: 140 }}>
          <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 4 }}>Score moyen</div>
          <div style={{ fontSize: 28, fontWeight: 800, color }}>{data.avg_composite}</div>
        </div>
        {Object.entries(data.distribution || {}).map(([k, v]) => (
          <div key={k} style={{ background: "#f9fafb", borderRadius: 10, padding: "16px 24px", flex: 1, minWidth: 100 }}>
            <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 4 }}>{k}</div>
            <div style={{ fontSize: 24, fontWeight: 700, color: "#111827" }}>{String(v)}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(220px,1fr))", gap: 16 }}>
        {(data.entities || []).map((e, i) => {
          const label = e.name ?? e.entity ?? `Entité ${i + 1}`;
          return (
            <div key={label} onClick={() => setSelected(e)}
              style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 16, cursor: "pointer", boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                <span style={{ fontWeight: 600, fontSize: 13, color: "#111827", lineHeight: 1.3 }}>{label}</span>
                <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 4, whiteSpace: "nowrap", marginLeft: 6,
                  background: RISK_BG[e.risk_level] ?? "#f9fafb",
                  color: RISK_COLOR[e.risk_level] ?? "#374151" }}>
                  {e.risk_level}
                </span>
              </div>
              <GaugeRing value={Math.round(e.composite_score)} color={color} />
            </div>
          );
        })}
      </div>
      {selected && <DetailModal entity={selected} slug={slug} color={color} onClose={() => setSelected(null)} />}
    </div>
  );
}
