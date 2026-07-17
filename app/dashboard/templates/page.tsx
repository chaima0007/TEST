"use client";

import { useEffect, useState } from "react";

interface SubjectVariant {
  variant_key: string;
  subject: string;
}

interface TemplateStats {
  renders: number;
  sends: number;
  opens: number;
  clicks: number;
  replies: number;
  open_rate_pct: number;
  click_rate_pct: number;
  reply_rate_pct: number;
}

interface Template {
  template_id: string;
  name: string;
  channel: "email" | "sms" | "linkedin";
  description: string;
  tags: string[];
  subject_variants: SubjectVariant[];
  required_variables: string[];
  stats: TemplateStats;
}

interface Summary {
  templates_count: number;
  total_sends: number;
  total_opens: number;
  total_clicks: number;
  total_replies: number;
  avg_open_rate_pct: number;
  avg_reply_rate_pct: number;
  top_template: string;
}

interface ApiResponse {
  templates: Template[];
  summary: Summary;
  by_tag: Record<string, number>;
}

const TAG_COLORS: Record<string, string> = {
  cold:         "bg-blue-500/15 text-blue-300 border-blue-500/25",
  warm:         "bg-emerald-500/15 text-emerald-300 border-emerald-500/25",
  post_quote:   "bg-violet-500/15 text-violet-300 border-violet-500/25",
  intro:        "bg-indigo-500/15 text-indigo-300 border-indigo-500/25",
  followup:     "bg-amber-500/15 text-amber-300 border-amber-500/25",
  urgency:      "bg-red-500/15 text-red-300 border-red-500/25",
  social_proof: "bg-teal-500/15 text-teal-300 border-teal-500/25",
  demo:         "bg-cyan-500/15 text-cyan-300 border-cyan-500/25",
  breakup:      "bg-slate-500/15 text-slate-300 border-slate-500/25",
  reactivation: "bg-orange-500/15 text-orange-300 border-orange-500/25",
  objection:    "bg-purple-500/15 text-purple-300 border-purple-500/25",
};

const CHANNEL_COLORS: Record<string, string> = {
  email:    "bg-indigo-500/15 text-indigo-300 border-indigo-500/25",
  sms:      "bg-green-500/15 text-green-300 border-green-500/25",
  linkedin: "bg-blue-500/15 text-blue-300 border-blue-500/25",
};

function TagBadge({ tag }: { tag: string }) {
  const cls = TAG_COLORS[tag] ?? "bg-white/10 text-gray-300 border-white/15";
  return (
    <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded border ${cls}`}>
      {tag}
    </span>
  );
}

function RateBar({ value }: { value: number }) {
  const color =
    value >= 70 ? "bg-emerald-500"
    : value >= 50 ? "bg-blue-500"
    : value >= 30 ? "bg-amber-500"
    : "bg-slate-500";
  return (
    <div className="w-full h-1.5 rounded-full bg-white/10 overflow-hidden">
      <div
        className={`h-full rounded-full transition-all duration-700 ${color}`}
        style={{ width: `${Math.min(100, value)}%` }}
      />
    </div>
  );
}

function StatPill({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <div className={`w-1.5 h-1.5 rounded-full ${color} shrink-0`} />
      <span className="text-[10px] text-gray-400">
        {label} <span className="text-white font-semibold">{value}%</span>
      </span>
    </div>
  );
}

function DetailModal({ template, onClose }: { template: Template; onClose: () => void }) {
  const { stats } = template;
  return (
    <div
      className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06]">
          <div className="flex items-center gap-3 flex-wrap">
            <h2 className="font-bold text-lg text-white">{template.name}</h2>
            <span
              className={`text-xs px-2 py-0.5 rounded-full border ${CHANNEL_COLORS[template.channel]}`}
            >
              {template.channel}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-white text-2xl leading-none ml-4 shrink-0"
          >
            ×
          </button>
        </div>

        <div className="p-5 space-y-5">
          <p className="text-sm text-slate-400">{template.description}</p>

          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Variantes objet</p>
            <div className="space-y-2">
              {template.subject_variants.map((v) => (
                <div
                  key={v.variant_key}
                  className="flex items-start gap-3 bg-white/[0.03] border border-white/[0.06] rounded-lg px-3 py-2"
                >
                  <span className="text-xs font-bold text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 rounded px-1.5 py-0.5 shrink-0">
                    {v.variant_key}
                  </span>
                  <span className="text-xs text-gray-300 leading-relaxed">{v.subject}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">
              Variables requises ({template.required_variables.length})
            </p>
            <div className="flex flex-wrap gap-1.5">
              {template.required_variables.map((v) => (
                <code
                  key={v}
                  className="text-[10px] font-mono bg-white/[0.05] border border-white/[0.08] text-amber-300 px-2 py-0.5 rounded"
                >
                  {"{" + v + "}"}
                </code>
              ))}
            </div>
          </div>

          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Statistiques</p>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-3">
                  <p className="text-xs text-gray-500 mb-0.5">Envois</p>
                  <p className="text-xl font-bold text-white">{stats.sends.toLocaleString("fr-FR")}</p>
                  <p className="text-[10px] text-gray-600">{stats.renders} rendus</p>
                </div>
                <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-3">
                  <p className="text-xs text-gray-500 mb-0.5">Ouvertures</p>
                  <p className="text-xl font-bold text-blue-300">{stats.opens}</p>
                  <p className="text-[10px] text-gray-500">{stats.open_rate_pct}%</p>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400">Ouverture</span>
                  <span className="text-white font-medium">{stats.open_rate_pct}%</span>
                </div>
                <RateBar value={stats.open_rate_pct} />
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400">Clics</span>
                  <span className="text-white font-medium">{stats.click_rate_pct}%</span>
                </div>
                <RateBar value={stats.click_rate_pct} />
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400">Réponses</span>
                  <span className="text-white font-medium">{stats.reply_rate_pct}%</span>
                </div>
                <RateBar value={stats.reply_rate_pct} />
              </div>

              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-3">
                  <p className="text-xs text-gray-500 mb-0.5">Clics</p>
                  <p className="text-xl font-bold text-amber-300">{stats.clicks}</p>
                  <p className="text-[10px] text-gray-500">{stats.click_rate_pct}%</p>
                </div>
                <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-3">
                  <p className="text-xs text-gray-500 mb-0.5">Réponses</p>
                  <p className="text-xl font-bold text-emerald-300">{stats.replies}</p>
                  <p className="text-[10px] text-gray-500">{stats.reply_rate_pct}%</p>
                </div>
              </div>
            </div>
          </div>

          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Tags</p>
            <div className="flex flex-wrap gap-1.5">
              {template.tags.map((tag) => (
                <TagBadge key={tag} tag={tag} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function TemplateCard({
  template,
  onOpen,
}: {
  template: Template;
  onOpen: () => void;
}) {
  const { stats } = template;
  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4 hover:bg-white/[0.05] transition-colors">
      <div className="flex items-start justify-between gap-4 mb-2">
        <div className="flex items-center gap-2 flex-wrap min-w-0">
          <span className="font-semibold text-white text-sm">{template.name}</span>
          <span
            className={`text-[10px] px-2 py-0.5 rounded-full border shrink-0 ${CHANNEL_COLORS[template.channel]}`}
          >
            {template.channel}
          </span>
        </div>
        <button
          onClick={onOpen}
          className="text-xs text-indigo-400 hover:text-indigo-300 border border-indigo-500/30 hover:border-indigo-400/50 px-2.5 py-1 rounded-lg transition-colors shrink-0"
        >
          Voir →
        </button>
      </div>

      <p className="text-xs text-slate-400 mb-3 leading-relaxed">{template.description}</p>

      <div className="flex flex-wrap items-center gap-1.5 mb-3">
        {template.tags.map((tag) => (
          <TagBadge key={tag} tag={tag} />
        ))}
        <span className="text-[10px] text-gray-600 ml-1">
          {template.required_variables.length} variables
        </span>
      </div>

      <div className="space-y-2">
        <div>
          <div className="flex justify-between items-center mb-0.5">
            <StatPill label="Ouverture" value={stats.open_rate_pct} color="bg-blue-400" />
            <span className="text-[10px] text-gray-600">{stats.opens}/{stats.sends}</span>
          </div>
          <RateBar value={stats.open_rate_pct} />
        </div>
        <div>
          <div className="flex justify-between items-center mb-0.5">
            <StatPill label="Clics" value={stats.click_rate_pct} color="bg-amber-400" />
            <span className="text-[10px] text-gray-600">{stats.clicks}/{stats.sends}</span>
          </div>
          <RateBar value={stats.click_rate_pct} />
        </div>
        <div>
          <div className="flex justify-between items-center mb-0.5">
            <StatPill label="Réponses" value={stats.reply_rate_pct} color="bg-emerald-400" />
            <span className="text-[10px] text-gray-600">{stats.replies}/{stats.sends}</span>
          </div>
          <RateBar value={stats.reply_rate_pct} />
        </div>
      </div>
    </div>
  );
}

const TAG_FILTERS = [
  { key: "all",        label: "Tous" },
  { key: "cold",       label: "Cold" },
  { key: "warm",       label: "Warm" },
  { key: "post_quote", label: "Post-devis" },
];

export default function TemplatesPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTag, setActiveTag] = useState("all");
  const [openTemplate, setOpenTemplate] = useState<Template | null>(null);

  useEffect(() => {
    fetch("/api/templates")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!data) {
    return <p className="text-gray-500 p-8">Erreur de chargement.</p>;
  }

  const { templates, summary } = data;

  const filtered =
    activeTag === "all"
      ? templates
      : templates.filter((t) => t.tags.includes(activeTag));

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto">
      {openTemplate && (
        <DetailModal template={openTemplate} onClose={() => setOpenTemplate(null)} />
      )}

      <div>
        <h1 className="text-2xl font-bold text-white">Templates Email</h1>
        <p className="text-sm text-slate-400 mt-1">
          11 templates d'outreach · taux d'ouverture et réponse par template
        </p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Templates</p>
          <p className="text-2xl font-bold text-white">{summary.templates_count}</p>
        </div>
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Total envois</p>
          <p className="text-2xl font-bold text-indigo-300">
            {summary.total_sends.toLocaleString("fr-FR")}
          </p>
        </div>
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Ouverture moy.</p>
          <p className="text-2xl font-bold text-blue-300">{summary.avg_open_rate_pct}%</p>
        </div>
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Réponse moy.</p>
          <p className="text-2xl font-bold text-emerald-300">{summary.avg_reply_rate_pct}%</p>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {TAG_FILTERS.map((f) => (
          <button
            key={f.key}
            onClick={() => setActiveTag(f.key)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
              activeTag === f.key
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"
            }`}
          >
            {f.label}
            {f.key !== "all" && data.by_tag[f.key] != null && (
              <span className="ml-1.5 text-[9px] opacity-60">{data.by_tag[f.key]}</span>
            )}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {filtered.map((t) => (
          <TemplateCard
            key={t.template_id}
            template={t}
            onOpen={() => setOpenTemplate(t)}
          />
        ))}
        {filtered.length === 0 && (
          <p className="text-gray-600 text-sm text-center py-10">Aucun template.</p>
        )}
      </div>
    </div>
  );
}
