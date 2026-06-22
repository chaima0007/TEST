"use client";
import { useState, useEffect } from "react";

const ACCENT = "#059669";
const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

interface Entity {
  name: string;
  composite_score: number;
  risk_level: string;
  estimated_index: number;
  [key: string]: unknown;
}

interface DashData {
  entities: Entity[];
  avg_composite: number;
  generatedAt?: string;
  mode?: string;
  [key: string]: unknown;
}

function GaugeRing({ value, label }: { value: number; label: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100) / 100;
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={ACCENT} strokeWidth={8}
          strokeDasharray={circ} strokeDashoffset={circ * (1 - pct)}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
          fill="white" fontSize={13} fontWeight="bold">{value.toFixed(1)}</text>
      </svg>
      <span style={{ fontSize: 11, color: "#94a3b8", textAlign: "center" }}>{label}</span>
    </div>
  );
}

function deriveCerts(score: number) {
  const certs = [
    { id: "ISO-26000", label: "ISO 26000", threshold: 80 },
    { id: "SA8000", label: "SA8000", threshold: 65 },
    { id: "Fair Trade", label: "Fair Trade", threshold: 50 },
    { id: "CSDDD", label: "CSDDD", threshold: 35 },
    { id: "OIT C182", label: "OIT C182", threshold: 20 },
  ];
  return certs.map(c => ({ ...c, obtained: score >= c.threshold }));
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "certifications" | "sources">("apercu");
  const tabs: { key: "apercu" | "metriques" | "certifications" | "sources"; label: string }[] = [
    { key: "apercu", label: "Aperçu" },
    { key: "metriques", label: "Métriques" },
    { key: "certifications", label: "Certifications" },
    { key: "sources", label: "Sources" },
  ];
  const certs = deriveCerts(entity.composite_score);
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", padding: 16 }} onClick={onClose}>
      <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 640, maxHeight: "90vh", overflowY: "auto" }} onClick={e => e.stopPropagation()}>
        <div style={{ padding: 24, borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <span className={`text-xs font-semibold uppercase ${RC[entity.risk_level] ?? "text-slate-400"}`}>{entity.risk_level}</span>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: "white", marginTop: 4 }}>{entity.name}</h2>
            <p style={{ fontSize: 13, color: "#94a3b8", marginTop: 2 }}>Insurtech Advertising Intelligence</p>
          </div>
          <button onClick={onClose} style={{ color: "#64748b", fontSize: 20, background: "none", border: "none", cursor: "pointer" }}>✕</button>
        </div>
        <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
          {tabs.map(t => (
            <button key={t.key} onClick={() => setTab(t.key)}
              style={{ flex: 1, padding: "10px 0", fontSize: 13, fontWeight: 500, background: "none", border: "none", cursor: "pointer", color: tab === t.key ? "white" : "#94a3b8", borderBottom: tab === t.key ? `2px solid ${ACCENT}` : "2px solid transparent" }}>
              {t.label}
            </button>
          ))}
        </div>
        <div style={{ padding: 24 }}>
          {tab === "apercu" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ display: "flex", gap: 12 }}>
                <div style={{ flex: 1, background: "#1e293b", borderRadius: 8, padding: 12 }}>
                  <p style={{ fontSize: 11, color: "#94a3b8" }}>Score Composite</p>
                  <p style={{ fontSize: 22, fontWeight: 700, color: "white" }}>{entity.composite_score.toFixed(2)}</p>
                </div>
                <div style={{ flex: 1, background: "#1e293b", borderRadius: 8, padding: 12 }}>
                  <p style={{ fontSize: 11, color: "#94a3b8" }}>Index Estimé</p>
                  <p style={{ fontSize: 22, fontWeight: 700, color: ACCENT }}>{entity.estimated_index}</p>
                </div>
              </div>
              <p style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6 }}>
                Cet acteur opère dans le secteur de la publicité insurtech. Son score composite reflète
                l&apos;exposition aux risques liés aux pratiques publicitaires des nouvelles technologies
                d&apos;assurance, notamment la transparence algorithmique et la protection des assurés.
              </p>
            </div>
          )}
          {tab === "metriques" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {[
                { label: "Transparence des offres d&apos;assurance", value: entity.composite_score * 0.30 },
                { label: "Conformité ACPR & EIOPA", value: entity.composite_score * 0.25 },
                { label: "Ciblage algorithmique éthique", value: entity.composite_score * 0.25 },
                { label: "Protection données assurés", value: entity.composite_score * 0.20 },
              ].map(m => (
                <div key={m.label} style={{ background: "#1e293b", borderRadius: 8, padding: 12 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ fontSize: 12, color: "#cbd5e1" }} dangerouslySetInnerHTML={{ __html: m.label }} />
                    <span style={{ fontSize: 12, fontWeight: 700, color: "white" }}>{m.value.toFixed(1)}</span>
                  </div>
                  <div style={{ height: 4, background: "#0f172a", borderRadius: 2 }}>
                    <div style={{ height: "100%", width: `${Math.min(m.value, 100)}%`, background: ACCENT, borderRadius: 2 }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "certifications" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {certs.map(c => (
                <div key={c.id} style={{ display: "flex", alignItems: "center", gap: 12, background: "#1e293b", borderRadius: 8, padding: 12 }}>
                  <span style={{ fontSize: 18 }}>{c.obtained ? "✅" : "❌"}</span>
                  <div>
                    <p style={{ fontSize: 13, fontWeight: 600, color: c.obtained ? "#34d399" : "#f87171" }}>{c.label}</p>
                    <p style={{ fontSize: 11, color: "#64748b" }}>Seuil requis : {c.threshold} pts</p>
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "sources" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {["ACPR — Autorité de Contrôle Prudentiel et de Résolution", "EIOPA — European Insurance Regulatory Authority", "FCA UK — Insurance Advertising Standards", "IAIS — International Association of Insurance Supervisors"].map(s => (
                <div key={s} style={{ background: "#1e293b", borderRadius: 8, padding: 12 }}>
                  <p style={{ fontSize: 12, color: "#94a3b8" }}>{s}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function InsurtechAdvertisingDashboard() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/insurtech-advertising")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <p style={{ color: "#94a3b8", fontSize: 14 }}>Chargement Insurtech Advertising…</p>
    </div>
  );

  const entities: Entity[] = data?.entities ?? [];
  const avg = data?.avg_composite ?? 0;

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "white", padding: "32px 16px" }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div style={{ maxWidth: 1100, margin: "0 auto 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", background: ACCENT }} />
          <span style={{ fontSize: 12, color: "#64748b", textTransform: "uppercase", letterSpacing: 2 }}>Wave 379</span>
        </div>
        <h1 style={{ fontSize: 28, fontWeight: 800, color: "white", marginBottom: 4 }}>Insurtech Advertising Intelligence</h1>
        <p style={{ fontSize: 14, color: "#94a3b8" }}>
          Surveillance des pratiques publicitaires dans le secteur insurtech — algorithmes, transparence et droits des assurés
        </p>
      </div>

      {/* KPIs */}
      <div style={{ maxWidth: 1100, margin: "0 auto 32px", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16 }}>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20 }}>
          <GaugeRing value={avg} label="Score Moyen" />
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20, display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <p style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>Entités surveillées</p>
          <p style={{ fontSize: 28, fontWeight: 800, color: "white" }}>{entities.length}</p>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20, display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <p style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>Niveau Critique</p>
          <p style={{ fontSize: 28, fontWeight: 800, color: "#f87171" }}>{entities.filter(e => e.risk_level === "critique").length}</p>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20, display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <p style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>Mode</p>
          <p style={{ fontSize: 13, fontWeight: 600, color: data?.mode === "fallback" ? "#fbbf24" : "#34d399" }}>{data?.mode ?? "live"}</p>
        </div>
      </div>

      {/* Entity Grid */}
      <div style={{ maxWidth: 1100, margin: "0 auto", display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
        {entities.map((e) => (
          <div key={e.name}
            className={`border rounded-xl p-5 cursor-pointer transition-all hover:opacity-90 ${RB[e.risk_level] ?? "border-slate-700 bg-slate-800/40"}`}
            onClick={() => setSelected(e)}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
              <div style={{ flex: 1 }}>
                <p style={{ fontSize: 14, fontWeight: 700, color: "white", marginBottom: 2 }}>{e.name}</p>
                <span className={`text-xs font-semibold uppercase ${RC[e.risk_level] ?? "text-slate-400"}`}>{e.risk_level}</span>
              </div>
              <div style={{ textAlign: "right" }}>
                <p style={{ fontSize: 20, fontWeight: 800, color: ACCENT }}>{e.composite_score.toFixed(1)}</p>
                <p style={{ fontSize: 10, color: "#64748b" }}>composite</p>
              </div>
            </div>
            <div style={{ height: 4, background: "#1e293b", borderRadius: 2 }}>
              <div style={{ height: "100%", width: `${Math.min(e.composite_score, 100)}%`, background: ACCENT, borderRadius: 2 }} />
            </div>
            <p style={{ fontSize: 11, color: "#64748b", marginTop: 8 }}>Index : {e.estimated_index} / 10</p>
          </div>
        ))}
      </div>

      <div style={{ maxWidth: 1100, margin: "24px auto 0", textAlign: "center" }}>
        <p style={{ fontSize: 11, color: "#334155" }}>
          Généré le {data?.generatedAt ? new Date(data.generatedAt).toLocaleString("fr-FR") : "—"} · CaelumSwarm™ Wave 379
        </p>
      </div>
    </div>
  );
}
