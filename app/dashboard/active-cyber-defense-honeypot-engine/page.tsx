"use client";
import { useState, useEffect } from "react";

const ACCENT = "#0a2a3a";

const RC: Record<string, string> = {
  critique: "text-red-400",
  "élevé": "text-orange-400",
  modéré: "text-yellow-400",
  faible: "text-emerald-400",
};
const RB: Record<string, string> = {
  critique: "border-red-500/30 bg-red-500/10",
  "élevé": "border-orange-500/30 bg-orange-500/10",
  modéré: "border-yellow-500/30 bg-yellow-500/10",
  faible: "border-emerald-500/30 bg-emerald-500/10",
};

interface Entity {
  entity_id: string;
  name: string;
  threat_type: string;
  threat_detection_speed: number;
  honeypot_effectiveness: number;
  forensic_evidence_quality: number;
  legal_countermeasure_score: number;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_active_cyber_defense_honeypot_index: number;
}

interface LegalFramework {
  allowed: string[];
  forbidden: string[];
  verdict: string;
}

interface ApiData {
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  avg_estimated_active_cyber_defense_honeypot_index: number;
  legal_framework: LegalFramework;
  entities: Entity[];
  data_sources: string[];
}

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 226.19;
  const offset = circumference - (value / 100) * circumference;
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="8"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">
        {Math.round(value)}
      </text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "signaux" | "tactique">("apercu");
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg">
        <div className="flex items-center justify-between p-5 border-b border-slate-700">
          <div>
            <h2 className="text-white font-bold text-lg">{entity.name}</h2>
            <p className="text-slate-400 text-sm">{entity.threat_type}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl font-bold">×</button>
        </div>
        <div className="flex border-b border-slate-700">
          {(["apercu", "signaux", "tactique"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-sm font-medium capitalize transition-colors ${tab === t ? "border-b-2 border-cyan-400 text-cyan-400" : "text-slate-400 hover:text-white"}`}
            >
              {t === "apercu" ? "Aperçu" : t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        <div className="p-5">
          {tab === "apercu" && (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Score composite</span>
                <span className="text-white font-semibold">{entity.composite_score.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Niveau menace</span>
                <span className={`font-semibold text-sm ${RC[entity.risk_level] || "text-slate-300"}`}>{entity.risk_level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Pattern primaire</span>
                <span className="text-white text-sm text-right max-w-xs">{entity.primary_pattern}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Indice défense active</span>
                <span className="text-cyan-400 font-semibold">{entity.estimated_active_cyber_defense_honeypot_index.toFixed(2)}</span>
              </div>
            </div>
          )}
          {tab === "signaux" && (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Vitesse détection menace</span>
                <span className="text-white font-semibold">{entity.threat_detection_speed.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Efficacité honeypot</span>
                <span className="text-white font-semibold">{entity.honeypot_effectiveness.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Qualité preuves forensiques</span>
                <span className="text-white font-semibold">{entity.forensic_evidence_quality.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Score contre-mesure légale</span>
                <span className="text-white font-semibold">{entity.legal_countermeasure_score.toFixed(2)}</span>
              </div>
            </div>
          )}
          {tab === "tactique" && (
            <div className="space-y-2">
              <p className="text-slate-300 text-sm">Type de menace : <span className="text-cyan-300 font-semibold">{entity.threat_type}</span></p>
              <p className="text-slate-400 text-xs mt-3">Réponse recommandée :</p>
              <ul className="text-slate-300 text-xs space-y-1 list-disc list-inside">
                <li>Honeypot actif — capturer l&apos;attaquant</li>
                <li>Tarpit — ralentir et épuiser la connexion</li>
                <li>Forensics — collecter preuves pour poursuites</li>
                <li>Signalement Europol EC3 sous 24h (NIS2)</li>
              </ul>
            </div>
          )}
        </div>
        <div className="p-4 border-t border-slate-700">
          <button onClick={onClose} className="w-full py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg text-sm font-medium transition-colors">
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ActiveCyberDefenseHoneypotDashboard() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/active-cyber-defense-honeypot-engine")
      .then((r) => r.json())
      .then((d) => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-lg animate-pulse">Analyse cyber-défense en cours…</div>
      </div>
    );
  }
  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400">Erreur de chargement des données.</div>
      </div>
    );
  }

  const sortedEntities = [...data.entities].sort((a, b) => b.composite_score - a.composite_score);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-8" style={{ borderLeft: `4px solid ${ACCENT}`, paddingLeft: "1rem" }}>
        <h1 className="text-3xl font-bold text-white">Défense Cyber Active — Honeypot &amp; Forensics</h1>
        <p className="text-slate-400 mt-1 text-sm">NIS2 · OWASP · Europol EC3 · Belgium Computer Crime Act</p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
          <p className="text-slate-400 text-xs uppercase tracking-wide">Score Défense Moyen</p>
          <p className="text-3xl font-bold text-cyan-400 mt-1">{data.avg_composite.toFixed(1)}</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
          <p className="text-slate-400 text-xs uppercase tracking-wide">Indice Défense Active</p>
          <p className="text-3xl font-bold text-cyan-300 mt-1">{data.avg_estimated_active_cyber_defense_honeypot_index.toFixed(2)}</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
          <p className="text-slate-400 text-xs uppercase tracking-wide">Confiance Analyse</p>
          <p className="text-3xl font-bold text-emerald-400 mt-1">{(data.confidence_score * 100).toFixed(0)}%</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
          <p className="text-slate-400 text-xs uppercase tracking-wide">Menaces Critiques</p>
          <p className="text-3xl font-bold text-red-400 mt-1">{data.risk_distribution["critique"] ?? 0}</p>
        </div>
      </div>

      {/* Legal Framework */}
      {data.legal_framework && (
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 mb-8">
          <h2 className="text-lg font-bold text-white mb-4">Cadre Légal — Défense Active</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-emerald-400 font-semibold text-sm mb-2">Autorisé (légal EU/Belgique)</h3>
              <ul className="space-y-1">
                {data.legal_framework.allowed.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-slate-300 text-xs">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-red-400 font-semibold text-sm mb-2">Interdit (illégal)</h3>
              <ul className="space-y-1">
                {data.legal_framework.forbidden.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-slate-300 text-xs">
                    <span className="text-red-400 mt-0.5">✗</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-4 p-3 bg-cyan-900/30 border border-cyan-500/30 rounded-lg">
                <p className="text-cyan-300 text-xs font-medium">{data.legal_framework.verdict}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Active Tactics */}
      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 mb-8">
        <h2 className="text-lg font-bold text-white mb-4">Tactiques Actives Déployées</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Honeypot", desc: "Piège passif — attire & capture l&apos;attaquant", icon: "🪤", color: "border-cyan-500/30 bg-cyan-500/10" },
            { label: "Tarpit", desc: "Ralentit la connexion — l&apos;attaquant tourne en rond", icon: "⏳", color: "border-blue-500/30 bg-blue-500/10" },
            { label: "Forensics", desc: "Collecte preuves légales — IP, timestamps, vecteur", icon: "🔍", color: "border-purple-500/30 bg-purple-500/10" },
            { label: "Signalement", desc: "Europol EC3 sous 24h — obligation NIS2", icon: "🚨", color: "border-orange-500/30 bg-orange-500/10" },
          ].map((t) => (
            <div key={t.label} className={`rounded-lg p-4 border ${t.color}`}>
              <div className="text-2xl mb-2">{t.icon}</div>
              <p className="text-white font-semibold text-sm">{t.label}</p>
              <p className="text-slate-400 text-xs mt-1" dangerouslySetInnerHTML={{ __html: t.desc }} />
            </div>
          ))}
        </div>
      </div>

      {/* Critical Alerts */}
      {data.critical_alerts && data.critical_alerts.length > 0 && (
        <div className="bg-red-900/20 border border-red-500/30 rounded-xl p-5 mb-8">
          <h2 className="text-red-400 font-bold mb-3">Alertes Critiques Actives</h2>
          <ul className="space-y-1">
            {data.critical_alerts.map((alert, i) => (
              <li key={i} className="text-red-300 text-sm flex items-start gap-2">
                <span className="text-red-500 mt-0.5">▲</span>
                <span>{alert}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Entities Grid */}
      <div className="mb-4">
        <h2 className="text-xl font-bold text-white mb-4">Mécanismes de Défense Analysés</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {sortedEntities.map((entity) => (
            <button
              key={entity.entity_id}
              onClick={() => setSelected(entity)}
              className={`text-left rounded-xl p-5 border transition-all hover:border-cyan-500/50 hover:bg-slate-700 ${RB[entity.risk_level] || "border-slate-700 bg-slate-800"}`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-slate-500 font-mono">{entity.entity_id}</span>
                    <span className={`text-xs font-semibold ${RC[entity.risk_level] || "text-slate-300"}`}>
                      {entity.risk_level.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-white text-sm font-medium leading-snug line-clamp-2">{entity.name}</p>
                  <p className="text-slate-400 text-xs mt-1">{entity.threat_type}</p>
                </div>
                <GaugeRing
                  value={entity.composite_score}
                  color={entity.risk_level === "critique" ? "#f87171" : entity.risk_level === "élevé" ? "#fb923c" : entity.risk_level === "modéré" ? "#facc15" : "#34d399"}
                />
              </div>
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                <div className="text-slate-400">Détection: <span className="text-white">{entity.threat_detection_speed.toFixed(0)}</span></div>
                <div className="text-slate-400">Honeypot: <span className="text-white">{entity.honeypot_effectiveness.toFixed(0)}</span></div>
                <div className="text-slate-400">Forensics: <span className="text-white">{entity.forensic_evidence_quality.toFixed(0)}</span></div>
                <div className="text-slate-400">Légal: <span className="text-white">{entity.legal_countermeasure_score.toFixed(0)}</span></div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Distribution */}
      <div className="bg-slate-800 rounded-xl p-5 border border-slate-700 mt-8">
        <h2 className="text-white font-bold mb-3">Distribution des Menaces</h2>
        <div className="flex gap-4 flex-wrap">
          {Object.entries(data.risk_distribution).map(([level, count]) => (
            <div key={level} className={`px-4 py-2 rounded-lg border ${RB[level] || "border-slate-600 bg-slate-700"}`}>
              <span className={`font-bold ${RC[level] || "text-white"}`}>{count}</span>
              <span className="text-slate-400 text-sm ml-2">{level}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Data Sources */}
      <div className="mt-6 pt-4 border-t border-slate-800">
        <p className="text-slate-500 text-xs">Sources : {data.data_sources.join(" · ")}</p>
      </div>
    </div>
  );
}
