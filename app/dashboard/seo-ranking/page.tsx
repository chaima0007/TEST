"use client";

import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface SEOSite {
  id: string;
  name: string;
  sector: string;
  domain: string;
  avg_position: number;
  organic_traffic_monthly: number;
  keyword_count: number;
  backlink_count: number;
  domain_authority: number;
  page_speed_mobile: number;
  core_web_vitals_score: number;
  indexation_rate: number;
  local_seo_score: number;
  composite_score: number;
  risk_level: string;
}

interface SEOSummary {
  total_sites: number;
  avg_position: number;
  avg_organic_traffic: number;
  avg_domain_authority: number;
  sites_critique: number;
  sites_eleve: number;
  sites_modere: number;
  sites_faible: number;
  top_risk_site: string;
  top_risk_score: number;
  patterns_detected: string[];
  avg_composite: number;
  avg_estimated_seo_index: number;
}

interface APIResponse {
  data: {
    entities: SEOSite[];
    summary: SEOSummary;
  };
}

type RiskFilter = "Tous" | "Critique" | "Élevé" | "Modéré" | "Faible";
type ModalTab = "Scores" | "Signaux" | "Actions";

// ── Risk helpers ──────────────────────────────────────────────────────────────

const RISK_CONFIG: Record<string, { label: string; badge: string; dot: string; bar: string }> = {
  critique: {
    label: "Critique",
    badge: "bg-red-500/15 text-red-400 border border-red-500/25",
    dot: "bg-red-500",
    bar: "bg-red-500",
  },
  "élevé": {
    label: "Élevé",
    badge: "bg-orange-500/15 text-orange-400 border border-orange-500/25",
    dot: "bg-orange-400",
    bar: "bg-orange-400",
  },
  "modéré": {
    label: "Modéré",
    badge: "bg-amber-500/15 text-amber-400 border border-amber-500/25",
    dot: "bg-amber-400",
    bar: "bg-amber-400",
  },
  faible: {
    label: "Faible",
    badge: "bg-emerald-500/15 text-emerald-400 border border-emerald-500/25",
    dot: "bg-emerald-500",
    bar: "bg-emerald-500",
  },
};

const FILTER_TO_RISK: Record<RiskFilter, string | null> = {
  Tous: null,
  Critique: "critique",
  Élevé: "élevé",
  Modéré: "modéré",
  Faible: "faible",
};

const FILTER_PILLS: RiskFilter[] = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];

// ── Score colour ──────────────────────────────────────────────────────────────

function scoreColor(score: number): string {
  if (score >= 70) return "text-emerald-400";
  if (score >= 40) return "text-amber-400";
  if (score >= 20) return "text-orange-400";
  return "text-red-400";
}

function positionColor(pos: number): string {
  if (pos <= 10) return "text-emerald-400";
  if (pos <= 30) return "text-amber-400";
  if (pos <= 60) return "text-orange-400";
  return "text-red-400";
}

// ── Formatters ────────────────────────────────────────────────────────────────

function fmtTraffic(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
  return String(n);
}

// ── GaugeRing ─────────────────────────────────────────────────────────────────

function GaugeRing({
  label,
  value,
  max = 100,
  color,
}: {
  label: string;
  value: number;
  max?: number;
  color: string;
}) {
  const pct = Math.min(Math.max(value / max, 0), 1);
  const r = 38;
  const circ = 2 * Math.PI * r;
  const dash = pct * circ;
  const displayVal = max === 100 ? Math.round(value) : value.toFixed(1);

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="8" />
        <circle
          cx="48"
          cy="48"
          r={r}
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
          className={color}
        />
        <text x="48" y="44" textAnchor="middle" fontSize="15" fontWeight="700" fill="white">
          {displayVal}
        </text>
        <text x="48" y="58" textAnchor="middle" fontSize="9" fill="rgba(255,255,255,0.45)">
          / {max}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

function DistBar({
  label,
  count,
  total,
  barClass,
}: {
  label: string;
  count: number;
  total: number;
  barClass: string;
}) {
  const pct = total > 0 ? (count / total) * 100 : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-16 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-white/6 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${barClass}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-xs font-mono text-slate-300 w-4 text-right">{count}</span>
    </div>
  );
}

// ── KPI Card ──────────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  sub,
  accent,
}: {
  label: string;
  value: string | number;
  sub?: string;
  accent?: string;
}) {
  return (
    <div className="bg-white/3 border border-white/8 rounded-xl p-4">
      <p className="text-xs text-slate-500 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-600 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

const SEO_ACTIONS: Record<string, string[]> = {
  "pénalité détectée": [
    "Auditer les backlinks toxiques via Search Console",
    "Soumettre une demande de désaveu Google",
    "Vérifier les pénalités manuelles dans GSC",
  ],
  "vitesse page insuffisante": [
    "Optimiser et compresser les images (WebP)",
    "Activer la mise en cache navigateur et serveur",
    "Minifier CSS, JS et HTML",
    "Implémenter le lazy-loading des images",
  ],
  "Core Web Vitals échoué": [
    "Améliorer le LCP (Largest Contentful Paint < 2.5s)",
    "Réduire le CLS (Cumulative Layout Shift < 0.1)",
    "Optimiser le FID / INP (< 200ms)",
    "Précharger les ressources critiques",
  ],
  "classement local absent": [
    "Créer/optimiser la fiche Google Business Profile",
    "Uniformiser les NAP sur tous les annuaires",
    "Obtenir des avis clients Google",
    "Ajouter les balises Schema LocalBusiness",
  ],
  "contenu dupliqué": [
    "Implémenter les balises canoniques (rel=canonical)",
    "Fusionner ou rediriger les pages dupliquées (301)",
    "Mettre à jour le fichier robots.txt",
    "Auditer les paramètres d'URL en double",
  ],
};

const PATTERNS_ALL = [
  "pénalité détectée",
  "vitesse page insuffisante",
  "Core Web Vitals échoué",
  "classement local absent",
  "contenu dupliqué",
];

function DetailModal({
  site,
  onClose,
}: {
  site: SEOSite;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<ModalTab>("Scores");
  const cfg = RISK_CONFIG[site.risk_level] ?? RISK_CONFIG.faible;

  // Derive patterns from site composite + scores heuristics for demo
  const sitePatterns = PATTERNS_ALL.filter((p) => {
    if (p === "vitesse page insuffisante" && site.page_speed_mobile < 50) return true;
    if (p === "Core Web Vitals échoué" && site.core_web_vitals_score < 50) return true;
    if (p === "classement local absent" && site.local_seo_score < 35) return true;
    if (p === "contenu dupliqué" && site.indexation_rate < 80) return true;
    if (p === "pénalité détectée" && site.domain_authority < 20) return true;
    return false;
  });

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: "rgba(0,0,0,0.75)" }}
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl bg-[#0f1117] border border-white/10 rounded-2xl overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="px-6 py-4 border-b border-white/8 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${cfg.badge}`}>
                {cfg.label}
              </span>
              <span className="text-xs text-slate-500">{site.sector}</span>
            </div>
            <h2 className="text-lg font-bold text-white">{site.name}</h2>
            <p className="text-xs text-slate-500">{site.domain}</p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white transition-colors mt-1 text-xl leading-none"
          >
            ×
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-white/8">
          {(["Scores", "Signaux", "Actions"] as ModalTab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-400 -mb-px"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6">
          {tab === "Scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: "Score Composite", val: site.composite_score, max: 100 },
                  { label: "Position Moy.", val: site.avg_position, max: 100, inverse: true },
                  { label: "Page Speed Mobile", val: site.page_speed_mobile, max: 100 },
                  { label: "Core Web Vitals", val: site.core_web_vitals_score, max: 100 },
                  { label: "SEO Local", val: site.local_seo_score, max: 100 },
                  { label: "Indexation", val: site.indexation_rate, max: 100 },
                ].map(({ label, val, max }) => (
                  <div key={label}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-400">{label}</span>
                      <span className={`font-mono font-semibold ${scoreColor(val)}`}>
                        {val}
                      </span>
                    </div>
                    <div className="h-1.5 bg-white/6 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${scoreColor(val)
                          .replace("text-", "bg-")}`}
                        style={{ width: `${(val / max) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-3 gap-3 pt-2 border-t border-white/8 text-center">
                <div>
                  <p className="text-lg font-bold text-white">{site.keyword_count}</p>
                  <p className="text-xs text-slate-500">Mots-clés</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-white">{site.backlink_count}</p>
                  <p className="text-xs text-slate-500">Backlinks</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-indigo-400">{site.domain_authority}</p>
                  <p className="text-xs text-slate-500">Domain Auth.</p>
                </div>
              </div>
            </div>
          )}

          {tab === "Signaux" && (
            <div className="space-y-3">
              <p className="text-xs text-slate-500 mb-2">
                Signaux détectés pour ce site ({sitePatterns.length} / 5)
              </p>
              {PATTERNS_ALL.map((pattern) => {
                const active = sitePatterns.includes(pattern);
                return (
                  <div
                    key={pattern}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg border ${
                      active
                        ? "bg-red-500/8 border-red-500/20"
                        : "bg-white/3 border-white/6"
                    }`}
                  >
                    <span
                      className={`w-2 h-2 rounded-full shrink-0 ${
                        active ? "bg-red-500 animate-pulse" : "bg-white/15"
                      }`}
                    />
                    <span
                      className={`text-sm ${
                        active ? "text-red-300 font-medium" : "text-slate-600"
                      }`}
                    >
                      {pattern}
                    </span>
                    {active && (
                      <span className="ml-auto text-xs text-red-500 font-semibold">
                        Actif
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {tab === "Actions" && (
            <div className="space-y-4">
              {sitePatterns.length === 0 && (
                <p className="text-sm text-slate-500 text-center py-4">
                  Aucun signal critique détecté pour ce site.
                </p>
              )}
              {sitePatterns.map((pattern) => (
                <div key={pattern}>
                  <p className="text-xs font-semibold text-red-400 mb-2 uppercase tracking-wide">
                    {pattern}
                  </p>
                  <ul className="space-y-1.5">
                    {(SEO_ACTIONS[pattern] ?? []).map((action) => (
                      <li key={action} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="mt-1.5 w-1 h-1 rounded-full bg-indigo-400 shrink-0" />
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Site Card ─────────────────────────────────────────────────────────────────

function SiteCard({ site, onClick }: { site: SEOSite; onClick: () => void }) {
  const cfg = RISK_CONFIG[site.risk_level] ?? RISK_CONFIG.faible;

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-white/3 border border-white/8 rounded-xl p-4 hover:bg-white/5 hover:border-white/15 transition-all"
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${cfg.badge}`}>
              <span className={`inline-block w-1.5 h-1.5 rounded-full mr-1.5 ${cfg.dot} ${site.risk_level === "critique" ? "animate-pulse" : ""}`} />
              {cfg.label}
            </span>
          </div>
          <p className="text-sm font-semibold text-white truncate">{site.name}</p>
          <p className="text-xs text-slate-500">{site.domain}</p>
        </div>
        <div className="text-right shrink-0">
          <p className={`text-xl font-bold font-mono ${scoreColor(site.composite_score)}`}>
            {site.composite_score}
          </p>
          <p className="text-[10px] text-slate-600">composite</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs mb-3">
        <div>
          <span className="text-slate-500">Position moy.</span>
          <span className={`ml-1.5 font-mono font-semibold ${positionColor(site.avg_position)}`}>
            #{site.avg_position}
          </span>
        </div>
        <div>
          <span className="text-slate-500">Trafic/mois</span>
          <span className="ml-1.5 font-mono text-slate-200">
            {fmtTraffic(site.organic_traffic_monthly)}
          </span>
        </div>
        <div>
          <span className="text-slate-500">Page Speed</span>
          <span className={`ml-1.5 font-mono font-semibold ${scoreColor(site.page_speed_mobile)}`}>
            {site.page_speed_mobile}
          </span>
        </div>
        <div>
          <span className="text-slate-500">DA</span>
          <span className="ml-1.5 font-mono text-indigo-300">{site.domain_authority}</span>
        </div>
      </div>

      <div className="flex items-center gap-1.5">
        <div className="flex-1 h-1 bg-white/6 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${cfg.bar}`}
            style={{ width: `${site.composite_score}%` }}
          />
        </div>
        <span className="text-[10px] text-slate-600">{site.sector}</span>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SEORankingPage() {
  const [entities, setEntities] = useState<SEOSite[]>([]);
  const [summary, setSummary] = useState<SEOSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<RiskFilter>("Tous");
  const [selected, setSelected] = useState<SEOSite | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/seo-ranking")
      .then((r) => r.json())
      .then((payload: APIResponse) => {
        setEntities(payload.data?.entities ?? []);
        setSummary(payload.data?.summary ?? null);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = entities.filter((s) => {
    const risk = FILTER_TO_RISK[filter];
    return risk === null || s.risk_level === risk;
  });

  // Gauge averages
  const avgPageSpeed =
    entities.length > 0
      ? entities.reduce((a, s) => a + s.page_speed_mobile, 0) / entities.length
      : 0;
  const avgCWV =
    entities.length > 0
      ? entities.reduce((a, s) => a + s.core_web_vitals_score, 0) / entities.length
      : 0;
  const avgLocal =
    entities.length > 0
      ? entities.reduce((a, s) => a + s.local_seo_score, 0) / entities.length
      : 0;
  const avgPosition =
    entities.length > 0
      ? entities.reduce((a, s) => a + s.avg_position, 0) / entities.length
      : 0;

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">
            SEO & Positionnement Organique
          </h1>
          <p className="text-sm text-slate-500">
            Moteur de scoring SEO — Analyse composite des 8 sites clients
          </p>
        </div>
        {loading && (
          <span className="text-xs text-slate-500 animate-pulse mt-1">Chargement…</span>
        )}
      </div>

      {/* KPI Cards */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <KpiCard
            label="Total Sites"
            value={summary.total_sites}
            sub="sites clients"
          />
          <KpiCard
            label="Position Moy."
            value={`#${summary.avg_position}`}
            sub="toutes pages"
            accent={positionColor(summary.avg_position)}
          />
          <KpiCard
            label="Trafic Organique"
            value={fmtTraffic(summary.avg_organic_traffic)}
            sub="visites/mois moy."
            accent="text-indigo-300"
          />
          <KpiCard
            label="Autorité Domaine Moy."
            value={summary.avg_domain_authority}
            sub="DA moyen"
            accent="text-violet-400"
          />
          <KpiCard
            label="Sites Critiques"
            value={summary.sites_critique}
            sub="action urgente"
            accent="text-red-400"
          />
          <KpiCard
            label="Score Composite Moy."
            value={summary.avg_composite}
            sub={`indice SEO ${summary.avg_estimated_seo_index}/10`}
            accent={scoreColor(summary.avg_composite)}
          />
        </div>
      )}

      {/* Gauges + Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Gauge Rings */}
        <div className="bg-white/3 border border-white/8 rounded-xl p-5">
          <p className="text-sm font-semibold text-slate-300 mb-4">
            Scores Moyens — Indicateurs Clés
          </p>
          <div className="grid grid-cols-4 gap-2">
            <GaugeRing
              label="Position SEO"
              value={Math.round(100 - avgPosition)}
              max={100}
              color={scoreColor(100 - avgPosition)}
            />
            <GaugeRing
              label="Page Speed"
              value={Math.round(avgPageSpeed)}
              max={100}
              color={scoreColor(avgPageSpeed)}
            />
            <GaugeRing
              label="Core Web Vitals"
              value={Math.round(avgCWV)}
              max={100}
              color={scoreColor(avgCWV)}
            />
            <GaugeRing
              label="SEO Local"
              value={Math.round(avgLocal)}
              max={100}
              color={scoreColor(avgLocal)}
            />
          </div>
        </div>

        {/* Distribution Bars */}
        {summary && (
          <div className="bg-white/3 border border-white/8 rounded-xl p-5">
            <p className="text-sm font-semibold text-slate-300 mb-4">
              Distribution par Niveau de Risque
            </p>
            <div className="space-y-3">
              <DistBar
                label="Critique"
                count={summary.sites_critique}
                total={summary.total_sites}
                barClass="bg-red-500"
              />
              <DistBar
                label="Élevé"
                count={summary.sites_eleve}
                total={summary.total_sites}
                barClass="bg-orange-400"
              />
              <DistBar
                label="Modéré"
                count={summary.sites_modere}
                total={summary.total_sites}
                barClass="bg-amber-400"
              />
              <DistBar
                label="Faible"
                count={summary.sites_faible}
                total={summary.total_sites}
                barClass="bg-emerald-500"
              />
            </div>
            {summary.patterns_detected.length > 0 && (
              <div className="mt-4 pt-4 border-t border-white/8">
                <p className="text-xs text-slate-500 mb-2">Signaux détectés</p>
                <div className="flex flex-wrap gap-1.5">
                  {summary.patterns_detected.map((p) => (
                    <span
                      key={p}
                      className="text-[10px] px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20"
                    >
                      {p}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Filter Pills */}
      <div className="flex items-center gap-2 flex-wrap">
        {FILTER_PILLS.map((pill) => (
          <button
            key={pill}
            onClick={() => setFilter(pill)}
            className={`text-sm px-4 py-1.5 rounded-full border transition-all ${
              filter === pill
                ? "bg-indigo-500/20 border-indigo-500/50 text-indigo-300 font-semibold"
                : "bg-white/3 border-white/10 text-slate-400 hover:text-white hover:border-white/20"
            }`}
          >
            {pill}
            {pill !== "Tous" && (
              <span className="ml-1.5 text-xs opacity-70">
                {entities.filter(
                  (s) => s.risk_level === (FILTER_TO_RISK[pill] ?? "")
                ).length}
              </span>
            )}
          </button>
        ))}
        <span className="text-xs text-slate-600 ml-1">
          {filtered.length} site{filtered.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Entity Cards Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
          {[...Array(8)].map((_, i) => (
            <div
              key={i}
              className="bg-white/3 border border-white/8 rounded-xl p-4 h-40 animate-pulse"
            />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 text-slate-500">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none" className="mb-3">
            <rect x="6" y="8" width="36" height="32" rx="4" fill="rgba(255,255,255,0.05)" />
            <rect x="12" y="16" width="24" height="3" rx="1.5" fill="rgba(255,255,255,0.1)" />
            <rect x="12" y="22" width="18" height="3" rx="1.5" fill="rgba(255,255,255,0.1)" />
            <rect x="12" y="28" width="12" height="3" rx="1.5" fill="rgba(255,255,255,0.1)" />
          </svg>
          <p className="text-sm">Aucun site pour ce filtre</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
          {filtered.map((site) => (
            <SiteCard
              key={site.id}
              site={site}
              onClick={() => setSelected(site)}
            />
          ))}
        </div>
      )}

      {/* Detail Modal */}
      {selected && (
        <DetailModal site={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
