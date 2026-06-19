"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface GeneticEntity {
  entity_id: string;
  data_type: string;
  region: string;
  consent_score: number;
  data_security_score: number;
  discrimination_score: number;
  sovereignty_score: number;
  composite_score: number;
  risk_level: string;
  genetic_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  informed_consent_quality: number;
  indigenous_genetic_sovereignty: number;
}

interface Summary {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_genetic_privacy_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-violet-400",
  high:     "text-violet-300",
  moderate: "text-green-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-violet-500/20 border-violet-500/40",
  high:     "bg-violet-400/20 border-violet-400/40",
  moderate: "bg-green-500/20 border-green-500/40",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  crise_confidentialité_génétique_systémique: "text-violet-400",
  violation_droits_génétiques_majeure:        "text-violet-300",
  risque_discrimination_génétique_structurel: "text-green-400",
  confidentialité_génétique_sous_surveillance:"text-slate-300",
};

const PATTERN_ICON: Record<string, string> = {
  law_enforcement_dna_dragnet:      "🔍",
  insurance_genetic_discrimination: "🏥",
  corporate_biobank_exploitation:   "🏦",
  family_member_privacy_violation:  "👪",
  genetic_colonialism_extraction:   "🌍",
  none:                             "—",
};

const PATTERN_LABEL: Record<string, string> = {
  law_enforcement_dna_dragnet:      "Filet ADN Forces de l'Ordre",
  insurance_genetic_discrimination: "Discrimination Génétique Assurance",
  corporate_biobank_exploitation:   "Exploitation Biobanque Commerciale",
  family_member_privacy_violation:  "Violation Vie Privée Familiale",
  genetic_colonialism_extraction:   "Extraction Coloniale Génétique",
  none:                             "Aucun Schéma Détecté",
};

// ── GaugeRing ────────────────────────────────────────────────────────────────
function GaugeRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={88} height={88} viewBox="0 0 88 88">
        <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx={44} cy={44} r={r} fill="none"
          stroke={color} strokeWidth={8}
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── ScoreBar ─────────────────────────────────────────────────────────────────
function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────
function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-violet-500/30 rounded-xl p-4">
      <div className="text-xs text-slate-400 mb-2">{title}</div>
      <div className="flex gap-1 h-3 rounded-full overflow-hidden">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            className={colors[k] ?? "bg-slate-600"}
            style={{ width: `${(v / total) * 100}%` }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-2 mt-2 text-xs text-slate-500">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k}>{k.replace(/_/g, " ")}: {v}</span>
        ))}
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────
function DetailModal({ entity, onClose }: { entity: GeneticEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"aperçu" | "scores" | "action">("aperçu");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    entity.composite_score >= 60 ? "#7c3aed"
    : entity.composite_score >= 40 ? "#8b5cf6"
    : entity.composite_score >= 20 ? "#22c55e"
    : "#64748b";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-violet-500/30 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <GaugeRing score={entity.composite_score} label="" color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              🧬 {entity.entity_id}
            </h2>
            <p className="text-slate-400 text-sm">{entity.data_type.replace(/_/g, " ")} · {entity.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
                {entity.risk_level} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[entity.severity] ?? "text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["aperçu", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-violet-400 border-b-2 border-violet-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "aperçu" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Schéma Génétique", PATTERN_ICON[entity.genetic_pattern] + " " + (PATTERN_LABEL[entity.genetic_pattern] ?? entity.genetic_pattern.replace(/_/g, " "))],
                  ["Qualité Consentement", (entity.informed_consent_quality * 100).toFixed(0) + "%"],
                  ["Souveraineté Indigène", (entity.indigenous_genetic_sovereignty * 100).toFixed(0) + "%"],
                  ["Score Composite", entity.composite_score.toFixed(1) + " / 100"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal de Confidentialité Génétique</div>
                <div className="text-violet-300 text-sm leading-relaxed">{entity.signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Score Consentement"      value={entity.consent_score}       color="bg-violet-500" />
              <ScoreBar label="Sécurité des Données"    value={entity.data_security_score} color="bg-violet-400" />
              <ScoreBar label="Risque Discrimination"   value={entity.discrimination_score} color="bg-green-500" />
              <ScoreBar label="Souveraineté Génétique"  value={entity.sovereignty_score}   color="bg-green-400" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-violet-500/10 border border-violet-500/30 rounded-xl p-4">
                <div className="text-xs text-violet-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg capitalize">
                  {entity.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {entity.risk_level === "critical" && (
                <div className="bg-violet-500/10 border border-violet-500/30 rounded-xl p-3 text-sm text-violet-300">
                  🔴 Crise critique — intervention immédiate sur la protection des données génétiques requise
                </div>
              )}
              {entity.risk_level === "high" && (
                <div className="bg-violet-400/10 border border-violet-400/30 rounded-xl p-3 text-sm text-violet-300">
                  🟠 Risque élevé — audit des banques ADN et du consentement à déclencher en urgence
                </div>
              )}
              {entity.risk_level === "moderate" && (
                <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-3 text-sm text-green-300">
                  🟡 Risque modéré — renforcement du cadre réglementaire génétique recommandé
                </div>
              )}
              {entity.risk_level === "low" && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ Confidentialité génétique préservée — surveillance continue recommandée
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── EntityCard ────────────────────────────────────────────────────────────────
function EntityCard({ entity, onClick }: { entity: GeneticEntity; onClick: () => void }) {
  const ringColor =
    entity.composite_score >= 60 ? "#7c3aed"
    : entity.composite_score >= 40 ? "#8b5cf6"
    : entity.composite_score >= 20 ? "#22c55e"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-violet-500/30 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <GaugeRing score={entity.composite_score} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            🧬 {entity.entity_id}
          </div>
          <div className="text-slate-400 text-xs">{entity.data_type.replace(/_/g, " ")} · {entity.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
              {entity.risk_level}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold ${RISK_COLOR[entity.risk_level]}`}>
            {entity.composite_score.toFixed(1)}
          </div>
          <div className="text-xs text-slate-500 mt-0.5">/ 100</div>
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[entity.genetic_pattern]} {(PATTERN_LABEL[entity.genetic_pattern] ?? entity.genetic_pattern).replace(/_/g, " ")}
      </div>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────
export default function GeneticPrivacyEnginePage() {
  const [entities, setEntities]   = useState<GeneticEntity[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<GeneticEntity | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterRisk    !== "all") params.set("risk",    filterRisk);
    if (filterPattern !== "all") params.set("pattern", filterPattern);
    fetch(`/api/genetic-privacy-engine?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setEntities(data.entities ?? []);
        setSummary(data.summary ?? null);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [filterRisk, filterPattern]);

  const filteredEntities = entities.filter((e) => {
    if (filterRisk    !== "all" && e.risk_level     !== filterRisk)    return false;
    if (filterPattern !== "all" && e.genetic_pattern !== filterPattern) return false;
    return true;
  });

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    {
      title: "Schémas de Risque Génétique",
      counts: summary?.pattern_distribution ?? {},
      colors: {
        law_enforcement_dna_dragnet:      "bg-violet-600",
        insurance_genetic_discrimination: "bg-violet-500",
        corporate_biobank_exploitation:   "bg-violet-400",
        family_member_privacy_violation:  "bg-green-500",
        genetic_colonialism_extraction:   "bg-green-400",
        none:                             "bg-slate-500",
      },
    },
    {
      title: "Sévérité des Violations",
      counts: summary?.severity_distribution ?? {},
      colors: {
        crise_confidentialité_génétique_systémique: "bg-violet-600",
        violation_droits_génétiques_majeure:        "bg-violet-400",
        risque_discrimination_génétique_structurel: "bg-green-500",
        confidentialité_génétique_sous_surveillance:"bg-slate-400",
      },
    },
    {
      title: "Distribution du Risque",
      counts: summary?.risk_distribution ?? {},
      colors: {
        critical: "bg-violet-600",
        high:     "bg-violet-400",
        moderate: "bg-green-500",
        low:      "bg-slate-500",
      },
    },
    {
      title: "Actions Prescrites",
      counts: summary?.action_distribution ?? {},
      colors: {
        intervention_urgente_protection_données_génétiques: "bg-violet-600",
        audit_immédiat_banques_adn_et_consentement:         "bg-violet-400",
        renforcement_cadre_réglementaire_génétique:         "bg-green-500",
        veille_confidentialité_génétique_continue:          "bg-slate-500",
      },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">
            Confidentialité Génétique &amp; Banques ADN — Module 431
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Moteur d&apos;intelligence sur la confidentialité génétique et les banques de données ADN —
            surveillance des violations de consentement, de la discrimination génétique, de l&apos;exploitation
            commerciale des biobanques et de la souveraineté génétique des peuples autochtones.
          </p>
        </div>

        {/* KPI strip — 6 cards */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Entités Analysées",          value: summary.total },
              { label: "Composite Moyen",             value: summary.avg_composite.toFixed(1),                              color: "text-violet-400" },
              { label: "Cas Critiques",               value: summary.critical,                                              color: "text-violet-500" },
              { label: "Risque Élevé",                value: summary.high,                                                  color: "text-violet-300" },
              { label: "Index Confidentialité ADN",   value: summary.avg_estimated_genetic_privacy_index.toFixed(2) + " /10", color: "text-green-400" },
              { label: "Faible Risque",               value: summary.low,                                                   color: "text-slate-300" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-violet-500/30 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 GaugeRings */}
        {summary && (
          <div className="bg-slate-900 border border-violet-500/30 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Dimensions de la Confidentialité Génétique</div>
            <div className="flex flex-wrap gap-6 justify-around">
              <GaugeRing score={summary.avg_composite * 0.30 * 100 / 100} label="Score Consentement"     color="#7c3aed" />
              <GaugeRing score={summary.avg_composite * 0.25 * 100 / 100} label="Sécurité des Données"   color="#8b5cf6" />
              <GaugeRing score={summary.avg_composite * 0.25 * 100 / 100} label="Risque Discrimination"  color="#22c55e" />
              <GaugeRing score={summary.avg_composite * 0.20 * 100 / 100} label="Souveraineté Génétique" color="#4ade80" />
            </div>
          </div>
        )}

        {/* 4 DistBars */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {distributions.map((d) => (
              <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
            ))}
          </div>
        )}

        {/* filter pills */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "Tous",              val: "all" },
            { label: "🔴 Critique",       val: "critical" },
            { label: "🟠 Élevé",          val: "high" },
            { label: "🟡 Modéré",         val: "moderate" },
            { label: "🟢 Faible",         val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-violet-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterPattern}
            onChange={(e) => setFilterPattern(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">Tous Schémas</option>
            {[
              "law_enforcement_dna_dragnet",
              "insurance_genetic_discrimination",
              "corporate_biobank_exploitation",
              "family_member_privacy_violation",
              "genetic_colonialism_extraction",
              "none",
            ].map((p) => (
              <option key={p} value={p}>{(PATTERN_LABEL[p] ?? p).replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* entity cards grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse de la confidentialité génétique en cours…</div>
        ) : filteredEntities.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune entité ne correspond aux filtres sélectionnés.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredEntities.map((e) => (
              <EntityCard key={e.entity_id} entity={e} onClick={() => setSelected(e)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
