"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Prospect {
  company_id: string;
  name: string;
  sector: string;
  website: string;
  pagespeed_score: number;
  load_time_ms: number;
  priority_score: number;
  tier: "A" | "B" | "C";
  icp_fit: number;
  urgency_label: string;
  estimated_revenue_impact_eur: number;
  contact_email: string;
  company_size: string;
}

interface ProspectsData {
  source: string;
  total: number;
  tier_a: number;
  tier_b: number;
  tier_c: number;
  last_cycle: string;
  prospects: Prospect[];
}

// ── Constants ─────────────────────────────────────────────────────────────────

const TIER_STYLE = {
  A: { bg: "bg-emerald-500/15", text: "text-emerald-300", border: "border-emerald-500/25", label: "Tier A", dot: "bg-emerald-400" },
  B: { bg: "bg-indigo-500/15",  text: "text-indigo-300",  border: "border-indigo-500/25",  label: "Tier B", dot: "bg-indigo-400"  },
  C: { bg: "bg-gray-500/10",    text: "text-gray-400",    border: "border-gray-500/15",    label: "Tier C", dot: "bg-gray-500"   },
};

const URGENCY_COLOR: Record<string, string> = {
  critique:   "text-red-400",
  mauvais:    "text-orange-400",
  moyen:      "text-amber-400",
  acceptable: "text-blue-400",
  bon:        "text-emerald-400",
};

// ── Components ────────────────────────────────────────────────────────────────

function PageSpeedBadge({ score }: { score: number }) {
  const color =
    score < 30 ? "bg-red-500/20 text-red-300 border-red-500/30"
    : score < 50 ? "bg-orange-500/20 text-orange-300 border-orange-500/30"
    : score < 70 ? "bg-amber-500/20 text-amber-300 border-amber-500/30"
    : "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
  return (
    <span className={`text-xs font-mono px-2 py-0.5 rounded-full border ${color}`}>
      {score}/100
    </span>
  );
}

function PriorityBar({ score }: { score: number }) {
  const color = score >= 80 ? "bg-emerald-500" : score >= 50 ? "bg-indigo-500" : "bg-gray-600";
  return (
    <div className="flex items-center gap-2">
      <div className="w-20 h-1.5 bg-white/8 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-xs font-mono text-gray-400">{score}</span>
    </div>
  );
}

function ProspectCard({ p, onEmail }: { p: Prospect; onEmail: (p: Prospect) => void }) {
  const t = TIER_STYLE[p.tier];
  const urgencyColor = URGENCY_COLOR[p.urgency_label] || "text-gray-400";

  return (
    <div className={`border rounded-xl p-4 transition-all hover:scale-[1.01] ${t.bg} ${t.border}`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-0.5">
            <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${t.bg} ${t.border} ${t.text}`}>
              {t.label}
            </span>
            <span className="text-xs text-gray-500 bg-white/5 px-2 py-0.5 rounded">
              {p.company_size}
            </span>
          </div>
          <p className="text-sm font-semibold text-white truncate">{p.name}</p>
          <p className="text-xs text-gray-400">{p.sector}</p>
        </div>
        <PriorityBar score={p.priority_score} />
      </div>

      <div className="grid grid-cols-3 gap-2 mb-3 text-center">
        <div>
          <PageSpeedBadge score={p.pagespeed_score} />
          <p className="text-xs text-gray-600 mt-1">PageSpeed</p>
        </div>
        <div>
          <p className={`text-xs font-semibold ${urgencyColor}`}>
            {p.urgency_label}
          </p>
          <p className="text-xs text-gray-600">{(p.load_time_ms / 1000).toFixed(1)}s</p>
        </div>
        <div>
          <p className="text-xs font-semibold text-amber-300">
            {(p.estimated_revenue_impact_eur / 1000).toFixed(0)}k€
          </p>
          <p className="text-xs text-gray-600">impact/an</p>
        </div>
      </div>

      <div className="flex items-center justify-between gap-2">
        <a
          href={p.website}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-indigo-400 hover:text-indigo-300 truncate max-w-[140px] transition-colors"
        >
          {p.website.replace(/^https?:\/\//, "")}
        </a>
        <button
          onClick={() => onEmail(p)}
          className="text-xs font-medium px-3 py-1.5 rounded-lg bg-indigo-600/20 border border-indigo-500/30 text-indigo-300 hover:bg-indigo-600/30 transition-all shrink-0"
        >
          ✉ Contacter
        </button>
      </div>
    </div>
  );
}

// ── Email modal ───────────────────────────────────────────────────────────────

function EmailModal({ prospect, onClose }: { prospect: Prospect; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-[#141422] border border-white/10 rounded-2xl p-6 max-w-lg w-full">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-semibold">Envoyer un email à {prospect.name}</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-300 text-xl">×</button>
        </div>
        <div className="space-y-3 text-sm">
          <div className="bg-white/5 rounded-xl p-4">
            <p className="text-gray-400 text-xs mb-1">Destinataire</p>
            <p className="text-white">{prospect.contact_email}</p>
          </div>
          <div className="bg-white/5 rounded-xl p-4">
            <p className="text-gray-400 text-xs mb-1">Email généré par Agent 2.1 (Le Factuel)</p>
            <p className="text-gray-300 text-xs leading-relaxed">
              <strong>Objet : Votre site charge en {(prospect.load_time_ms / 1000).toFixed(1)}s — PageSpeed {prospect.pagespeed_score}/100</strong>
              <br /><br />
              Bonjour,<br /><br />
              En analysant {prospect.website.replace(/^https?:\/\//, "")}, j&apos;ai relevé :
              temps de chargement {(prospect.load_time_ms / 1000).toFixed(1)}s, score PageSpeed mobile {prospect.pagespeed_score}/100.
              Ces indicateurs représentent une perte estimée de {Math.round((prospect.estimated_revenue_impact_eur / 1000))}k€/an de revenus mobiles.
              Ces chiffres vous ont-ils déjà été signalés ?
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 rounded-lg border border-white/10 text-gray-400 hover:bg-white/5 text-sm transition-all"
            >
              Annuler
            </button>
            <button
              onClick={() => {
                alert("Email mis en queue — Agent 2.1 l'enverra via SMTP selon le rate limit.");
                onClose();
              }}
              className="flex-1 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-all"
            >
              Envoyer via l&apos;essaim
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function ProspectsPage() {
  const [data, setData] = useState<ProspectsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTier, setActiveTier] = useState<string>("all");
  const [search, setSearch] = useState("");
  const [emailTarget, setEmailTarget] = useState<Prospect | null>(null);

  const fetchProspects = useCallback((tier: string, q: string) => {
    const params = new URLSearchParams();
    if (tier !== "all") params.set("tier", tier);
    if (q) params.set("q", q);
    setLoading(true);
    fetch(`/api/prospects?${params}`)
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    fetchProspects(activeTier, search);
  }, [activeTier, search, fetchProspects]);

  const lastCycle = data
    ? new Date(data.last_cycle).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })
    : "—";

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-5">

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="text-2xl">🎯</span>
            <h1 className="text-2xl font-bold">Prospects</h1>
            {data && (
              <span className={`text-xs px-2.5 py-1 rounded-full border font-medium ${
                data.source === "live"
                  ? "text-emerald-400 bg-emerald-400/10 border-emerald-400/20"
                  : "text-amber-400 bg-amber-400/10 border-amber-400/20"
              }`}>
                {data.source === "live" ? "● Live" : "◎ Demo"}
              </span>
            )}
          </div>
          <p className="text-sm text-gray-400">
            Enrichis par ProspectEnricher — Dernier cycle : {lastCycle}
          </p>
        </div>
        <input
          type="text"
          placeholder="Rechercher…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 w-64"
        />
      </div>

      {/* Stats */}
      {data && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-white/3 border border-white/8 rounded-xl p-4">
            <p className="text-xs text-gray-400 mb-1">Total détectés</p>
            <p className="text-2xl font-bold text-white">{data.total.toLocaleString("fr-FR")}</p>
          </div>
          <div className="bg-emerald-500/5 border border-emerald-500/15 rounded-xl p-4">
            <p className="text-xs text-emerald-400 mb-1">Tier A — Priorité haute</p>
            <p className="text-2xl font-bold text-emerald-300">{data.tier_a}</p>
          </div>
          <div className="bg-indigo-500/5 border border-indigo-500/15 rounded-xl p-4">
            <p className="text-xs text-indigo-400 mb-1">Tier B — Priorité moyenne</p>
            <p className="text-2xl font-bold text-indigo-300">{data.tier_b}</p>
          </div>
          <div className="bg-white/3 border border-white/8 rounded-xl p-4">
            <p className="text-xs text-gray-400 mb-1">Tier C — Faible priorité</p>
            <p className="text-2xl font-bold text-gray-400">{data.tier_c}</p>
          </div>
        </div>
      )}

      {/* Tier filter */}
      <div className="flex gap-2 flex-wrap">
        {["all", "A", "B", "C"].map((tier) => (
          <button
            key={tier}
            onClick={() => setActiveTier(tier)}
            className={`px-4 py-1.5 rounded-lg text-sm font-medium border transition-all ${
              activeTier === tier
                ? "bg-indigo-600/30 border-indigo-500/40 text-indigo-200"
                : "bg-white/3 border-white/8 text-gray-400 hover:bg-white/5"
            }`}
          >
            {tier === "all" ? "Tous" : `Tier ${tier}`}
          </button>
        ))}
      </div>

      {/* Prospect grid */}
      {loading ? (
        <div className="text-center py-16 text-gray-500 text-sm animate-pulse">Chargement des prospects…</div>
      ) : data && data.prospects.length === 0 ? (
        <div className="text-center py-16 text-gray-500 text-sm">Aucun prospect trouvé.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
          {data?.prospects.map((p) => (
            <ProspectCard key={p.company_id} p={p} onEmail={setEmailTarget} />
          ))}
        </div>
      )}

      {emailTarget && (
        <EmailModal prospect={emailTarget} onClose={() => setEmailTarget(null)} />
      )}

    </div>
  );
}
