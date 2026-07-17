"use client";

import { useEffect, useState, useRef } from "react";

type PersonalizationLevel = "deep" | "strong" | "moderate" | "basic" | "generic";
type OutreachChannel = "email" | "linkedin" | "phone" | "multi";

interface ContactProfile {
  contact_id: string;
  full_name: string;
  title: string;
  company: string;
  industry: string;
  company_size: string;
  linkedin_connections: number;
  website_visits_30d: number;
  emails_opened_30d: number;
  content_downloads: number;
  event_attendances: number;
  has_direct_phone: boolean;
  has_linkedin: boolean;
  has_personal_email: boolean;
  crm_notes_count: number;
  previous_interactions: number;
  triggers: string[];
  trigger_recency_days: number;
  is_decision_maker: boolean;
  budget_authority: boolean;
  pain_score: number;
  icp_score: number;
  preferred_channel: string | null;
  timezone_offset: number;
}

interface PersonalizationPlan {
  contact: ContactProfile;
  personalization_level: PersonalizationLevel;
  recommended_channel: OutreachChannel;
  personalization_score: number;
  profile_richness_score: number;
  engagement_score: number;
  timing_score: number;
  channel_fit_score: number;
  primary_angle: string;
  secondary_angles: string[];
  opening_hook: string;
  call_to_action: string;
  best_send_time: string;
  personalization_tokens: string[];
  do_not_contact: boolean;
  outreach_urgency: number;
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  channel_counts: Record<string, number>;
  avg_personalization_score: number;
  avg_urgency: number;
  hot_count: number;
  dnc_count: number;
}

const LEVEL_META: Record<PersonalizationLevel, { label: string; color: string; bg: string; dot: string }> = {
  deep: { label: "PROFONDE", color: "text-indigo-400", bg: "bg-indigo-500/10 border-indigo-500/30", dot: "bg-indigo-400" },
  strong: { label: "FORTE", color: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/30", dot: "bg-blue-400" },
  moderate: { label: "MODÉRÉE", color: "text-yellow-400", bg: "bg-yellow-500/10 border-yellow-500/30", dot: "bg-yellow-400" },
  basic: { label: "BASIQUE", color: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/30", dot: "bg-orange-400" },
  generic: { label: "GÉNÉRIQUE", color: "text-slate-400", bg: "bg-slate-500/10 border-slate-500/30", dot: "bg-slate-400" },
};

const CHANNEL_META: Record<OutreachChannel, { label: string; icon: string }> = {
  email: { label: "Email", icon: "✉️" },
  linkedin: { label: "LinkedIn", icon: "💼" },
  phone: { label: "Téléphone", icon: "📞" },
  multi: { label: "Multi-canal", icon: "🔀" },
};

const TRIGGER_LABELS: Record<string, string> = {
  job_change: "Prise de poste",
  funding: "Levée de fonds",
  product_launch: "Lancement produit",
  hiring: "Recrutement actif",
  content_published: "Contenu publié",
  event_attended: "Événement",
  website_visit: "Visite site web",
  email_opened: "Email ouvert",
  award: "Distinction/Award",
  expansion: "Expansion",
};

const LEVEL_TABS: { id: PersonalizationLevel | "all"; label: string }[] = [
  { id: "all", label: "Tous" },
  { id: "deep", label: "Profonde" },
  { id: "strong", label: "Forte" },
  { id: "moderate", label: "Modérée" },
  { id: "basic", label: "Basique" },
  { id: "generic", label: "Générique" },
];

function UrgencyRing({ urgency }: { urgency: number }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const offset = circ - (Math.min(100, urgency) / 100) * circ;
  const color = urgency >= 70 ? "#6366f1" : urgency >= 50 ? "#3b82f6" : urgency >= 30 ? "#f59e0b" : "#64748b";
  return (
    <div className="relative flex items-center justify-center w-16 h-16">
      <svg viewBox="0 0 72 72" className="w-16 h-16 -rotate-90">
        <circle cx="36" cy="36" r={r} fill="none" stroke="#334155" strokeWidth="6" />
        <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="6"
          strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
          className="transition-all duration-700" />
      </svg>
      <span className="absolute text-xs font-bold" style={{ color }}>{Math.round(urgency)}</span>
    </div>
  );
}

function ScoreBar({ value, color = "bg-indigo-500" }: { value: number; color?: string }) {
  return (
    <div className="h-1.5 w-full rounded-full bg-slate-700">
      <div className={`h-1.5 rounded-full transition-all ${color}`} style={{ width: `${Math.min(100, value)}%` }} />
    </div>
  );
}

function ContactModal({ plan, onClose }: { plan: PersonalizationPlan; onClose: () => void }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const meta = LEVEL_META[plan.personalization_level];
  const channel = CHANNEL_META[plan.recommended_channel];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    const click = (e: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(e.target as Node)) onClose();
    };
    window.addEventListener("keydown", handler);
    document.addEventListener("mousedown", click);
    return () => { window.removeEventListener("keydown", handler); document.removeEventListener("mousedown", click); };
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div ref={modalRef} className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl bg-slate-900 border border-slate-700 shadow-2xl">
        <div className="sticky top-0 z-10 flex items-start justify-between gap-4 p-6 bg-slate-900 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color}`}>{meta.label}</span>
              <span className="text-xs text-slate-400">{channel.icon} {channel.label}</span>
              {plan.do_not_contact && (
                <span className="text-xs bg-red-500/20 border border-red-500/40 text-red-400 px-2 py-0.5 rounded-full">DNC</span>
              )}
            </div>
            <h2 className="text-xl font-bold text-slate-100">{plan.contact.full_name}</h2>
            <p className="text-sm text-slate-400">{plan.contact.title} · {plan.contact.company}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl leading-none mt-1">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* Contact KPIs */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Urgence", value: `${Math.round(plan.outreach_urgency)}/100`, color: plan.outreach_urgency >= 70 ? "text-indigo-400" : "text-slate-300" },
              { label: "ICP Score", value: `${plan.contact.icp_score}%`, color: plan.contact.icp_score >= 75 ? "text-emerald-400" : "text-yellow-400" },
              { label: "Pain Score", value: `${plan.contact.pain_score}%`, color: plan.contact.pain_score >= 70 ? "text-red-400" : "text-slate-300" },
              { label: "LinkedIn", value: plan.contact.linkedin_connections.toLocaleString("fr-FR"), color: "text-slate-100" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-lg bg-slate-800 border border-slate-700 p-3 text-center">
                <div className={`text-lg font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Personalization dimensions */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Dimensions personnalisation</h3>
            <div className="space-y-2">
              {[
                { label: "Richesse profil", val: plan.profile_richness_score, color: "bg-indigo-500" },
                { label: "Signaux engagement", val: plan.engagement_score, color: "bg-blue-500" },
                { label: "Timing / Triggers", val: plan.timing_score, color: "bg-purple-500" },
                { label: "Fit canal", val: plan.channel_fit_score, color: "bg-emerald-500" },
              ].map((d) => (
                <div key={d.label} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-32 shrink-0">{d.label}</span>
                  <div className="flex-1"><ScoreBar value={d.val} color={d.color} /></div>
                  <span className="text-xs text-slate-300 w-8 text-right">{Math.round(d.val)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Triggers */}
          {plan.contact.triggers.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Signaux déclencheurs</h3>
              <div className="flex flex-wrap gap-2">
                {plan.contact.triggers.map((t) => (
                  <span key={t} className="text-xs bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 px-3 py-1 rounded-full">
                    ⚡ {TRIGGER_LABELS[t] || t}
                    {plan.contact.trigger_recency_days <= 7 && (
                      <span className="ml-1 text-emerald-400">({plan.contact.trigger_recency_days}j)</span>
                    )}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Opening hook */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-2">Accroche d'ouverture</h3>
            <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 text-sm text-slate-200 italic">
              "{plan.opening_hook}"
            </div>
          </div>

          {/* Primary angle */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-2">Angle principal</h3>
            <div className="flex items-start gap-2 text-sm text-slate-300">
              <span className="text-indigo-400 mt-0.5 shrink-0">→</span>
              {plan.primary_angle}
            </div>
            {plan.secondary_angles.length > 0 && (
              <div className="mt-2 space-y-1">
                {plan.secondary_angles.map((a, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-slate-400">
                    <span className="text-slate-600 mt-0.5 shrink-0">→</span>
                    {a}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* CTA */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-2">Call-to-Action recommandé</h3>
            <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-lg p-4 text-sm text-emerald-300">
              {plan.call_to_action}
            </div>
          </div>

          {/* Best send time */}
          <div className="flex items-center gap-3 rounded-lg bg-slate-800 border border-slate-700 p-4">
            <span className="text-xl">🕐</span>
            <div>
              <div className="text-sm font-semibold text-slate-200">Meilleur moment d'envoi</div>
              <div className="text-sm text-slate-400">{plan.best_send_time}</div>
            </div>
          </div>

          {/* Personalization tokens */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Tokens de personnalisation</h3>
            <div className="flex flex-wrap gap-2">
              {plan.personalization_tokens.map((t, i) => (
                <span key={i} className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-2 py-1 rounded-full">
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Contact signals */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Signaux d'activité (30j)</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
              {[
                { label: "Visites site", val: plan.contact.website_visits_30d },
                { label: "Emails ouverts", val: plan.contact.emails_opened_30d },
                { label: "Téléchargements", val: plan.contact.content_downloads },
                { label: "Événements", val: plan.contact.event_attendances },
              ].map((s) => (
                <div key={s.label} className={`rounded-lg border p-2 text-center ${s.val > 0 ? "bg-indigo-500/10 border-indigo-500/30" : "bg-slate-800 border-slate-700"}`}>
                  <div className={`text-lg font-bold ${s.val > 0 ? "text-indigo-300" : "text-slate-500"}`}>{s.val}</div>
                  <div className="text-xs text-slate-400">{s.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Data richness flags */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Données disponibles</h3>
            <div className="flex flex-wrap gap-2">
              {[
                { label: "Tél. direct", ok: plan.contact.has_direct_phone },
                { label: "LinkedIn", ok: plan.contact.has_linkedin },
                { label: "Email perso", ok: plan.contact.has_personal_email },
                { label: "Décideur", ok: plan.contact.is_decision_maker },
                { label: "Budget", ok: plan.contact.budget_authority },
              ].map((f) => (
                <span key={f.label} className={`text-xs px-3 py-1 rounded-full border ${f.ok ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300" : "bg-slate-800 border-slate-700 text-slate-500"}`}>
                  {f.ok ? "✓" : "✗"} {f.label}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ContactCard({ plan, onClick }: { plan: PersonalizationPlan; onClick: () => void }) {
  const meta = LEVEL_META[plan.personalization_level];
  const channel = CHANNEL_META[plan.recommended_channel];
  const isHot = plan.outreach_urgency >= 70;

  return (
    <div
      onClick={onClick}
      className={`cursor-pointer rounded-xl border p-5 transition-all hover:border-slate-600 hover:bg-slate-800/80 ${plan.do_not_contact ? "opacity-40" : meta.bg}`}
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color} flex items-center gap-1`}>
              <span className={`w-1.5 h-1.5 rounded-full ${meta.dot} ${isHot ? "animate-pulse" : ""}`} />
              {meta.label}
            </span>
            {plan.do_not_contact && (
              <span className="text-xs text-red-400 font-bold">DNC</span>
            )}
          </div>
          <h3 className="font-semibold text-slate-100 truncate">{plan.contact.full_name}</h3>
          <p className="text-xs text-slate-400 truncate">{plan.contact.title}</p>
          <p className="text-xs text-slate-500 truncate">{plan.contact.company}</p>
        </div>
        <UrgencyRing urgency={plan.outreach_urgency} />
      </div>

      {/* Channel + triggers */}
      <div className="flex flex-wrap items-center gap-1.5 mb-3">
        <span className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-2 py-0.5 rounded-full">
          {channel.icon} {channel.label}
        </span>
        {plan.contact.triggers.slice(0, 2).map((t) => (
          <span key={t} className="text-xs bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full">
            ⚡ {TRIGGER_LABELS[t]?.split(" ")[0] || t}
          </span>
        ))}
      </div>

      {/* Score bars */}
      <div className="space-y-1.5 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-12 shrink-0">Profil</span>
          <div className="flex-1"><ScoreBar value={plan.profile_richness_score} color="bg-indigo-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(plan.profile_richness_score)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-12 shrink-0">Engage</span>
          <div className="flex-1"><ScoreBar value={plan.engagement_score} color="bg-blue-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(plan.engagement_score)}</span>
        </div>
      </div>

      {/* Angle preview */}
      <p className="text-xs text-slate-400 line-clamp-2 mb-3">{plan.primary_angle}</p>

      {/* Bottom stats */}
      <div className="grid grid-cols-3 gap-2 text-center border-t border-slate-700 pt-3">
        <div>
          <div className="text-sm font-bold text-slate-200">{Math.round(plan.contact.icp_score)}%</div>
          <div className="text-xs text-slate-500">ICP</div>
        </div>
        <div>
          <div className="text-sm font-bold text-slate-200">{Math.round(plan.contact.pain_score)}%</div>
          <div className="text-xs text-slate-500">Pain</div>
        </div>
        <div>
          <div className="text-sm font-bold text-slate-200">{plan.contact.triggers.length}</div>
          <div className="text-xs text-slate-500">Triggers</div>
        </div>
      </div>
    </div>
  );
}

export default function ContactPersonalizerPage() {
  const [contacts, setContacts] = useState<PersonalizationPlan[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<PersonalizationLevel | "all">("all");
  const [selected, setSelected] = useState<PersonalizationPlan | null>(null);

  useEffect(() => {
    fetch("/api/contact-personalizer")
      .then((r) => r.json())
      .then((data) => {
        setContacts(data.contacts ?? []);
        setSummary(data.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = activeTab === "all" ? contacts : contacts.filter((c) => c.personalization_level === activeTab);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Personnalisation Contacts IA</h1>
            <p className="text-sm text-slate-400 mt-1">
              Stratégie d'approche personnalisée — angle, hook, canal recommandé, urgence outreach
            </p>
          </div>
          {summary && summary.hot_count > 0 && (
            <div className="flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/30 rounded-xl px-4 py-2">
              <span className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse" />
              <span className="text-sm font-semibold text-indigo-400">
                {summary.hot_count} contact{summary.hot_count > 1 ? "s" : ""} à contacter maintenant
              </span>
            </div>
          )}
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Contacts analysés", value: summary.total, color: "text-slate-100" },
              { label: "Score perso. moyen", value: `${summary.avg_personalization_score}/100`, color: "text-indigo-400" },
              { label: "Urgence moyenne", value: `${summary.avg_urgency}/100`, color: summary.avg_urgency >= 60 ? "text-indigo-400" : "text-slate-300" },
              { label: "Contacts chauds", value: summary.hot_count, color: "text-emerald-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-xl bg-slate-900 border border-slate-800 p-4">
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-1">{kpi.label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Channel distribution */}
        {summary && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
            <h2 className="text-sm font-semibold text-slate-400 mb-3">Canaux recommandés</h2>
            <div className="flex flex-wrap gap-2">
              {Object.entries(summary.channel_counts).map(([ch, count]) => {
                const c = CHANNEL_META[ch as OutreachChannel];
                if (!c || count === 0) return null;
                return (
                  <span key={ch} className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-full">
                    {c.icon} {c.label}: <span className="font-bold text-slate-100">{count}</span>
                  </span>
                );
              })}
              {summary.dnc_count > 0 && (
                <span className="text-xs bg-red-500/10 border border-red-500/30 text-red-400 px-3 py-1.5 rounded-full">
                  🚫 DNC: {summary.dnc_count}
                </span>
              )}
            </div>
          </div>
        )}

        {/* Level tabs */}
        <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 w-fit flex-wrap">
          {LEVEL_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === tab.id ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab.label}
              {summary && tab.id !== "all" && (
                <span className="ml-1.5 text-xs opacity-70">({summary.level_counts[tab.id] ?? 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Contact grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="rounded-xl bg-slate-900 border border-slate-800 p-5 animate-pulse h-56" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center text-slate-500 py-16">Aucun contact dans cette catégorie</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((plan) => (
              <ContactCard key={plan.contact.contact_id} plan={plan} onClick={() => setSelected(plan)} />
            ))}
          </div>
        )}
      </div>

      {selected && <ContactModal plan={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
