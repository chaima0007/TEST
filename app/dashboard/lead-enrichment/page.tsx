"use client";

import { useEffect, useState, useCallback, useRef } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type EnrichmentGap = {
  field: string;
  description: string;
  impact_score: number;
};

type Lead = {
  lead_id: string;
  lead_name: string;
  source: string;
  data_quality: string;
  quality_score: number;
  contact_score: number;
  company_score: number;
  intent_score: number;
  engagement_score: number;
  enrichment_priority: string;
  gaps: EnrichmentGap[];
  outreach_ready: boolean;
  quality_signals: string[];
  risk_flags: string[];
  suggested_enrichment_sources: string[];
};

type Summary = {
  total: number;
  quality_counts: Record<string, number>;
  priority_counts: Record<string, number>;
  avg_quality_score: number;
  outreach_ready_count: number;
  needs_enrichment_count: number;
};

// ─── Quality helpers ──────────────────────────────────────────────────────────

const QUALITY_META: Record<string, { label: string; color: string; ring: string; bg: string }> = {
  excellent: { label: "Excellent",   color: "text-emerald-400", ring: "#34d399", bg: "bg-emerald-900/30" },
  good:      { label: "Bon",         color: "text-blue-400",    ring: "#60a5fa", bg: "bg-blue-900/30"    },
  fair:      { label: "Correct",     color: "text-amber-400",   ring: "#fbbf24", bg: "bg-amber-900/30"   },
  poor:      { label: "Pauvre",      color: "text-orange-400",  ring: "#fb923c", bg: "bg-orange-900/30"  },
  incomplete:{ label: "Incomplet",   color: "text-red-400",     ring: "#f87171", bg: "bg-red-900/30"     },
};

const PRIORITY_META: Record<string, { label: string; color: string; dot: string }> = {
  immediate: { label: "Immédiat", color: "text-red-400",     dot: "bg-red-400"     },
  high:      { label: "Haute",    color: "text-orange-400",  dot: "bg-orange-400"  },
  medium:    { label: "Moyenne",  color: "text-amber-400",   dot: "bg-amber-400"   },
  low:       { label: "Faible",   color: "text-blue-400",    dot: "bg-blue-400"    },
  none:      { label: "Aucune",   color: "text-emerald-400", dot: "bg-emerald-400" },
};

const SOURCE_LABELS: Record<string, string> = {
  inbound:  "Entrant",
  outbound: "Sortant",
  referral: "Recommandation",
  event:    "Événement",
  content:  "Contenu",
  paid:     "Payant",
};

const PRIORITY_ORDER = ["all", "immediate", "high", "medium", "low", "none"];

// ─── QualityRing ──────────────────────────────────────────────────────────────

function QualityRing({ score, quality }: { score: number; quality: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const ringColor = QUALITY_META[quality]?.ring ?? "#6366f1";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="36" cy="36" r={r}
        fill="none"
        stroke={ringColor}
        strokeWidth="7"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="40" textAnchor="middle" fill="white" fontSize="13" fontWeight="700">
        {score.toFixed(0)}
      </text>
    </svg>
  );
}

// ─── ScoreBar ─────────────────────────────────────────────────────────────────

function ScoreBar({ label, value, color = "bg-indigo-500" }: { label: string; value: number; color?: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span>
        <span className="text-slate-200">{value.toFixed(0)}%</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

// ─── LeadModal ───────────────────────────────────────────────────────────────

function LeadModal({ lead, onClose }: { lead: Lead; onClose: () => void }) {
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onClose]);

  const qm = QUALITY_META[lead.data_quality] ?? QUALITY_META.incomplete;
  const pm = PRIORITY_META[lead.enrichment_priority] ?? PRIORITY_META.none;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <QualityRing score={lead.quality_score} quality={lead.data_quality} />
            <div>
              <h2 className="text-white font-bold text-lg leading-tight">{lead.lead_name}</h2>
              <div className="flex flex-wrap items-center gap-2 mt-1">
                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${qm.bg} ${qm.color}`}>
                  {qm.label}
                </span>
                <span className="text-slate-400 text-xs">
                  {SOURCE_LABELS[lead.source] ?? lead.source}
                </span>
                {lead.outreach_ready ? (
                  <span className="text-xs text-emerald-400 bg-emerald-900/30 px-2 py-0.5 rounded-full">
                    Prêt à contacter
                  </span>
                ) : (
                  <span className="text-xs text-red-400 bg-red-900/30 px-2 py-0.5 rounded-full">
                    Non prêt
                  </span>
                )}
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors mt-1">
            <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Score breakdown */}
          <div>
            <h3 className="text-slate-300 text-sm font-semibold mb-3">Scores par dimension</h3>
            <div className="space-y-3">
              <ScoreBar label="Contact (35%)" value={lead.contact_score} color="bg-indigo-500" />
              <ScoreBar label="Entreprise (30%)" value={lead.company_score} color="bg-violet-500" />
              <ScoreBar label="Intention (20%)" value={lead.intent_score} color="bg-amber-500" />
              <ScoreBar label="Engagement (15%)" value={lead.engagement_score} color="bg-emerald-500" />
            </div>
          </div>

          {/* Enrichment priority */}
          <div className="flex items-center gap-3 p-3 bg-slate-800/60 rounded-xl">
            <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${pm.dot}`} />
            <div>
              <p className="text-slate-400 text-xs">Priorité d'enrichissement</p>
              <p className={`font-semibold text-sm ${pm.color}`}>{pm.label}</p>
            </div>
          </div>

          {/* Enrichment gaps */}
          {lead.gaps.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">
                Données manquantes ({lead.gaps.length})
              </h3>
              <div className="space-y-2">
                {lead.gaps.map((g) => (
                  <div key={g.field} className="flex items-center justify-between p-2.5 bg-slate-800/60 rounded-lg">
                    <span className="text-slate-300 text-xs">{g.description}</span>
                    <span className="text-red-400 text-xs font-semibold ml-2 flex-shrink-0">
                      -{g.impact_score} pts
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Quality signals */}
          {lead.quality_signals.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Signaux positifs</h3>
              <ul className="space-y-1.5">
                {lead.quality_signals.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk flags */}
          {lead.risk_flags.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Alertes risque</h3>
              <ul className="space-y-1.5">
                {lead.risk_flags.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-orange-300">
                    <span className="text-orange-400 mt-0.5 flex-shrink-0">⚠</span>
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Enrichment sources */}
          {lead.suggested_enrichment_sources.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Sources d'enrichissement recommandées</h3>
              <ul className="space-y-1.5">
                {lead.suggested_enrichment_sources.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-indigo-300">
                    <span className="text-indigo-400 mt-0.5 flex-shrink-0">→</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── LeadCard ─────────────────────────────────────────────────────────────────

function LeadCard({ lead, onClick }: { lead: Lead; onClick: () => void }) {
  const qm = QUALITY_META[lead.data_quality] ?? QUALITY_META.incomplete;
  const pm = PRIORITY_META[lead.enrichment_priority] ?? PRIORITY_META.none;
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 hover:border-indigo-500/50 hover:bg-slate-800 transition-all group"
    >
      <div className="flex items-start gap-4">
        <QualityRing score={lead.quality_score} quality={lead.data_quality} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="text-white font-semibold text-sm group-hover:text-indigo-300 transition-colors truncate">
                {lead.lead_name}
              </p>
              <p className="text-slate-400 text-xs mt-0.5">
                {SOURCE_LABELS[lead.source] ?? lead.source}
              </p>
            </div>
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ${qm.bg} ${qm.color}`}>
              {qm.label}
            </span>
          </div>

          <div className="mt-3 flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-1.5">
              <div className={`w-1.5 h-1.5 rounded-full ${pm.dot}`} />
              <span className={`text-xs ${pm.color}`}>Priorité {pm.label}</span>
            </div>
            {lead.outreach_ready ? (
              <span className="text-xs text-emerald-400">● Prêt</span>
            ) : (
              <span className="text-xs text-red-400">● Non prêt</span>
            )}
            {lead.gaps.length > 0 && (
              <span className="text-xs text-slate-400">
                {lead.gaps.length} champ{lead.gaps.length > 1 ? "s" : ""} manquant{lead.gaps.length > 1 ? "s" : ""}
              </span>
            )}
          </div>

          {/* Dimension mini bars */}
          <div className="mt-3 grid grid-cols-2 gap-x-4 gap-y-1.5">
            {[
              { label: "Contact",    val: lead.contact_score,  color: "bg-indigo-500" },
              { label: "Entreprise", val: lead.company_score,  color: "bg-violet-500" },
              { label: "Intention",  val: lead.intent_score,   color: "bg-amber-500"  },
              { label: "Engagement", val: lead.engagement_score,color: "bg-emerald-500"},
            ].map(({ label, val, color }) => (
              <div key={label}>
                <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
                  <span>{label}</span>
                  <span>{val.toFixed(0)}</span>
                </div>
                <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, val)}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function LeadEnrichmentPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [selected, setSelected] = useState<Lead | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async (priority: string) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (priority !== "all") params.set("priority", priority);
      const res = await fetch(`/api/lead-enrichment?${params}`);
      const data = await res.json();
      setLeads(data.leads ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(priorityFilter); }, [fetchData, priorityFilter]);

  const qc = summary?.quality_counts ?? {};
  const pc = summary?.priority_counts ?? {};

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Enrichissement Leads</h1>
        <p className="text-slate-400 text-sm mt-1">
          Qualité des données leads, gaps identifiés et recommandations d'enrichissement
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Leads analysés",        value: summary?.total ?? "—",                  sub: "total" },
          { label: "Score qualité moyen",   value: summary ? `${summary.avg_quality_score}/100` : "—", sub: "qualité données" },
          { label: "Prêts à contacter",     value: summary?.outreach_ready_count ?? "—",   sub: "leads qualifiés" },
          { label: "Enrichissement urgent", value: summary?.needs_enrichment_count ?? "—", sub: "immédiat + haute priorité" },
        ].map(({ label, value, sub }) => (
          <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5">
            <p className="text-slate-400 text-xs mb-1">{label}</p>
            <p className="text-white text-2xl font-bold">{value}</p>
            <p className="text-slate-500 text-xs mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Quality distribution */}
      {summary && Object.keys(qc).length > 0 && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <h2 className="text-slate-300 text-sm font-semibold mb-4">Répartition qualité des données</h2>
          <div className="flex gap-1 h-5 rounded-full overflow-hidden mb-3">
            {(["excellent","good","fair","poor","incomplete"] as const).map((q) => {
              const count = qc[q] ?? 0;
              const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
              if (pct === 0) return null;
              return (
                <div
                  key={q}
                  style={{ width: `${pct}%`, backgroundColor: QUALITY_META[q].ring }}
                  className="h-full"
                  title={`${QUALITY_META[q].label}: ${count}`}
                />
              );
            })}
          </div>
          <div className="flex flex-wrap gap-3">
            {(["excellent","good","fair","poor","incomplete"] as const).map((q) => {
              const count = qc[q] ?? 0;
              if (!count) return null;
              const m = QUALITY_META[q];
              return (
                <div key={q} className="flex items-center gap-1.5 text-xs">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: m.ring }} />
                  <span className={m.color}>{m.label}</span>
                  <span className="text-slate-500">({count})</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Priority filter tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {PRIORITY_ORDER.map((p) => {
          const isAll = p === "all";
          const count = isAll ? (summary?.total ?? 0) : (pc[p] ?? 0);
          const active = priorityFilter === p;
          const meta = isAll ? null : PRIORITY_META[p];
          return (
            <button
              key={p}
              onClick={() => setPriorityFilter(p)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 ${
                active
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}
            >
              {meta && <div className={`w-2 h-2 rounded-full ${meta.dot}`} />}
              {isAll ? "Tous" : meta?.label}
              <span className={`text-xs px-1.5 py-0.5 rounded-full ${active ? "bg-white/20" : "bg-slate-700"}`}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Lead grid */}
      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : leads.length === 0 ? (
        <div className="text-center py-20 text-slate-500">Aucun lead pour ce filtre</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          {leads.map((lead) => (
            <LeadCard key={lead.lead_id} lead={lead} onClick={() => setSelected(lead)} />
          ))}
        </div>
      )}

      {/* Modal */}
      {selected && <LeadModal lead={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
