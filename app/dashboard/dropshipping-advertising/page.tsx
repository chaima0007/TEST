"use client";
import { useEffect, useState } from "react";

const COLOR = "#0ea5e9";

type Entity = {
  name: string;
  composite_score: number;
  risk_level: string;
  estimated_index: number;
};

type Summary = {
  entities: Entity[];
  avg_composite: number;
  generatedAt: string;
  mode?: string;
};

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  modéré: "#f59e0b",
  faible: "#10b981",
};

const RISK_BADGE: Record<string, string> = {
  critique: "bg-red-950 text-red-400 border border-red-700/40",
  "élevé": "bg-orange-950 text-orange-400 border border-orange-700/40",
  modéré: "bg-amber-950 text-amber-400 border border-amber-700/40",
  faible: "bg-emerald-950 text-emerald-400 border border-emerald-700/40",
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - Math.min(value, 100) / 100);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1628" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span style={{ fontSize: 11, color: "#93c5fd", textAlign: "center", lineHeight: 1.2 }}>{label}</span>
    </div>
  );
}

function deriveCerts(entity: Entity): string[] {
  return [
    `Score composite validé : ${entity.composite_score.toFixed(2)} / 100`,
    `Niveau de risque publicitaire Dropshipping : ${entity.risk_level}`,
    `Indice estimé Caelum : ${entity.estimated_index.toFixed(2)} / 10`,
    `Conformité campagne Dropshipping : ${entity.composite_score >= 60 ? "Surveillance active" : "Monitoring standard"}`,
    `Certification Wave 396 — Dropshipping Advertising Intelligence`,
  ];
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "certs" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const certs = deriveCerts(entity);

  return (
    <div
      style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.80)" }}
      onClick={onClose}
    >
      <div
        style={{ background: "#0a0f1e", border: "1px solid rgba(14,165,233,0.3)", borderRadius: 16, width: "100%", maxWidth: 520, padding: 24, boxShadow: "0 25px 50px rgba(0,0,0,0.7)" }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 16 }}>
          <div>
            <div style={{ fontSize: 17, fontWeight: 700, color: "#fff" }}>{entity.name}</div>
            <div style={{ fontSize: 12, color: `${COLOR}99`, marginTop: 2 }}>Dropshipping Advertising · Wave 396</div>
          </div>
          <button onClick={onClose} style={{ color: "#64748b", fontSize: 20, background: "none", border: "none", cursor: "pointer", lineHeight: 1 }}>✕</button>
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {(["scores", "signaux", "certs", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                padding: "4px 12px", borderRadius: 6, fontSize: 12, fontWeight: 500, cursor: "pointer", border: "none",
                background: tab === t ? COLOR : "#1e293b",
                color: tab === t ? "#fff" : "#94a3b8",
              }}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : t === "certs" ? "Certifications" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            {[
              { label: "Score Composite", value: entity.composite_score, color: RISK_COLORS[entity.risk_level] || "#fff" },
              { label: "Index Estimé", value: entity.estimated_index * 10, color: COLOR },
            ].map(({ label, value, color }) => (
              <div key={label} style={{ background: "#1e293b", borderRadius: 10, padding: 14, border: "1px solid rgba(14,165,233,0.2)" }}>
                <div style={{ fontSize: 11, color: "#93c5fd", marginBottom: 4 }}>{label}</div>
                <div style={{ fontSize: 22, fontWeight: 700, color }}>{value.toFixed(2)}</div>
                <div style={{ height: 4, background: "#0f172a", borderRadius: 2, marginTop: 6 }}>
                  <div style={{ height: 4, borderRadius: 2, width: `${Math.min(value, 100)}%`, background: color }} />
                </div>
              </div>
            ))}
            <div style={{ gridColumn: "span 2", background: "#1e293b", borderRadius: 10, padding: 14, border: "1px solid rgba(14,165,233,0.2)" }}>
              <div style={{ fontSize: 11, color: "#93c5fd", marginBottom: 4 }}>Niveau de Risque</div>
              <span style={{ fontSize: 13, fontWeight: 600 }} className={RISK_BADGE[entity.risk_level]}>{entity.risk_level}</span>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {[
              `Score composite ${entity.composite_score.toFixed(1)} — ${entity.risk_level === "critique" ? "surveillance publicitaire Dropshipping urgente" : entity.risk_level === "élevé" ? "monitoring renforcé recommandé" : "suivi standard actif"}`,
              `Indice Caelum Dropshipping Advertising : ${entity.estimated_index.toFixed(2)} / 10`,
              `Campagne Dropshipping en ${entity.risk_level === "faible" ? "zone verte — performance nominale" : "zone d'alerte — optimisation requise"}`,
            ].map((sig, i) => (
              <div key={i} style={{ background: "#1e293b", borderRadius: 8, padding: 12, fontSize: 13, color: "#e2e8f0", border: "1px solid rgba(14,165,233,0.15)", lineHeight: 1.5 }}>
                {sig}
              </div>
            ))}
          </div>
        )}

        {tab === "certs" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {certs.map((cert, i) => (
              <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10, background: "#1e293b", borderRadius: 8, padding: 12, border: "1px solid rgba(14,165,233,0.15)" }}>
                <span style={{ color: COLOR, fontSize: 14, marginTop: 1 }}>✓</span>
                <span style={{ fontSize: 13, color: "#e2e8f0" }}>{cert}</span>
              </div>
            ))}
          </div>
        )}

        {tab === "actions" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 10, fontSize: 13, color: "#cbd5e1" }}>
            <div style={{ background: "#1e293b", borderRadius: 8, padding: 12, border: "1px solid rgba(14,165,233,0.15)" }}>
              <div style={{ fontSize: 11, color: "#93c5fd", marginBottom: 4 }}>Action Prioritaire</div>
              <div>{entity.risk_level === "critique" ? "Audit immédiat des campagnes Dropshipping — conformité réglementaire urgente" : entity.risk_level === "élevé" ? "Révision des stratégies publicitaires Dropshipping — renforcement compliance" : entity.risk_level === "modéré" ? "Optimisation continue des métriques publicitaires Dropshipping" : "Maintien des bonnes pratiques — veille sectorielle Dropshipping"}</div>
            </div>
            <div style={{ background: "#1e293b", borderRadius: 8, padding: 12, border: "1px solid rgba(14,165,233,0.15)" }}>
              <div style={{ fontSize: 11, color: "#93c5fd", marginBottom: 4 }}>Index Caelum</div>
              <div style={{ color: COLOR, fontWeight: 700, fontSize: 18 }}>{entity.estimated_index.toFixed(2)} / 10</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const FILTER_OPTIONS = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];
const FILTER_MAP: Record<string, string> = { Tous: "", Critique: "critique", Élevé: "élevé", Modéré: "modéré", Faible: "faible" };

export default function DropshippingAdvertisingDashboard() {
  const [data, setData] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState("Tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/dropshipping-advertising")
      .then((r) => r.json())
      .then((d) => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setError("Erreur de chargement des données Dropshipping Advertising."); setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", background: "#030712", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff" }}>
        Chargement Dropshipping Advertising&hellip;
      </div>
    );
  }

  if (error || !data) {
    return (
      <div style={{ minHeight: "100vh", background: "#030712", display: "flex", alignItems: "center", justifyContent: "center", color: "#f87171" }}>
        {error || "Données indisponibles"}
      </div>
    );
  }

  const entities = data.entities ?? [];
  const filtered = filter === "Tous" ? entities : entities.filter((e) => e.risk_level === FILTER_MAP[filter]);

  const avgComposite = entities.length > 0
    ? entities.reduce((s, e) => s + e.composite_score, 0) / entities.length
    : 0;
  const avgIndex = entities.length > 0
    ? entities.reduce((s, e) => s + e.estimated_index, 0) / entities.length
    : 0;
  const criticalCount = entities.filter((e) => e.risk_level === "critique").length;
  const elevéCount = entities.filter((e) => e.risk_level === "élevé").length;

  return (
    <div style={{ minHeight: "100vh", background: "#030712", color: "#fff", padding: "32px 24px" }}>
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: COLOR }} />
          <h1 style={{ fontSize: 26, fontWeight: 700, color: "#fff", margin: 0 }}>
            Dropshipping Advertising
          </h1>
        </div>
        <p style={{ fontSize: 13, color: `${COLOR}99`, margin: 0 }}>
          Caelum Partners · Wave 396 · Droits de l&apos;enfant — Secteur dropshipping · {data.generatedAt ? new Date(data.generatedAt).toLocaleDateString("fr-FR") : "2026-06-22"}
          {data.mode === "fallback" && <span style={{ marginLeft: 8, color: "#f59e0b", fontSize: 11 }}>[mode dégradé]</span>}
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 12, marginBottom: 32 }}>
        {[
          { label: "Entités", value: entities.length, color: "#fff" },
          { label: "Critique", value: criticalCount, color: "#ef4444" },
          { label: "Élevé", value: elevéCount, color: "#f97316" },
          { label: "Composite Moyen", value: avgComposite.toFixed(1), color: "#f59e0b" },
          { label: "Index Moyen", value: avgIndex.toFixed(2), color: COLOR },
        ].map(({ label, value, color }) => (
          <div key={label} style={{ background: "#0f172a", border: "1px solid rgba(14,165,233,0.25)", borderRadius: 12, padding: "16px 14px" }}>
            <div style={{ fontSize: 11, color: "#93c5fd99", marginBottom: 4 }}>{label}</div>
            <div style={{ fontSize: 24, fontWeight: 700, color }}>{value}</div>
          </div>
        ))}
      </div>

      <div style={{ background: "#0f172a", border: "1px solid rgba(14,165,233,0.25)", borderRadius: 14, padding: 20, marginBottom: 24 }}>
        <div style={{ fontSize: 12, fontWeight: 600, color: "#93c5fd99", textTransform: "uppercase", letterSpacing: 1, marginBottom: 16 }}>
          Métriques Globales Dropshipping
        </div>
        <div style={{ display: "flex", gap: 24, flexWrap: "wrap", justifyContent: "space-around" }}>
          <GaugeRing value={avgComposite} label="Score Composite" color={COLOR} />
          <GaugeRing value={avgIndex * 10} label="Index Moyen" color="#67e8f9" />
          <GaugeRing value={(criticalCount / Math.max(entities.length, 1)) * 100} label="Taux Critique" color="#ef4444" />
          <GaugeRing value={(elevéCount / Math.max(entities.length, 1)) * 100} label="Taux Élevé" color="#f97316" />
        </div>
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 20 }}>
        {FILTER_OPTIONS.map((opt) => (
          <button
            key={opt}
            onClick={() => setFilter(opt)}
            style={{
              padding: "5px 14px", borderRadius: 20, fontSize: 12, fontWeight: 500, cursor: "pointer",
              border: `1px solid ${filter === opt ? COLOR : "rgba(14,165,233,0.3)"}`,
              background: filter === opt ? COLOR : "#0f172a",
              color: filter === opt ? "#fff" : "#94a3b8",
            }}
          >
            {opt}
          </button>
        ))}
        <span style={{ fontSize: 11, color: "#475569", alignSelf: "center", marginLeft: 4 }}>
          {filtered.length} entité{filtered.length !== 1 ? "s" : ""}
        </span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: 14, marginBottom: 24 }}>
        {filtered.map((entity, i) => (
          <div
            key={i}
            onClick={() => setSelected(entity)}
            style={{
              background: "#0f172a", border: "1px solid rgba(14,165,233,0.25)", borderRadius: 12, padding: 16,
              cursor: "pointer", transition: "border-color 0.2s",
            }}
            onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.borderColor = COLOR; }}
            onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.borderColor = "rgba(14,165,233,0.25)"; }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: "#fff", lineHeight: 1.3, flex: 1, marginRight: 8 }}>{entity.name}</div>
              <span style={{ fontSize: 11, fontWeight: 500, padding: "2px 8px", borderRadius: 4, whiteSpace: "nowrap" }} className={RISK_BADGE[entity.risk_level] || ""}>
                {entity.risk_level}
              </span>
            </div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
              <span style={{ fontSize: 11, color: "#93c5fd99" }}>Composite</span>
              <span style={{ fontSize: 18, fontWeight: 700, color: RISK_COLORS[entity.risk_level] || "#fff" }}>
                {entity.composite_score.toFixed(1)}
              </span>
            </div>

            <div style={{ height: 4, background: "#1e293b", borderRadius: 2, marginBottom: 10 }}>
              <div style={{ height: 4, borderRadius: 2, width: `${Math.min(entity.composite_score, 100)}%`, background: RISK_COLORS[entity.risk_level] || COLOR }} />
            </div>

            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#64748b" }}>
              <span>Index Caelum</span>
              <span style={{ color: COLOR, fontWeight: 600 }}>{entity.estimated_index.toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>

      <div style={{ textAlign: "center", fontSize: 11, color: "#334155" }}>
        Caelum Partners · Dropshipping Advertising Intelligence · Wave 396
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
