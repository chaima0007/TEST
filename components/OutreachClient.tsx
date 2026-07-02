"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useToast } from "@/components/Toast";

// ─── Types (contrats API) ────────────────────────────────────────────────────

type ProspectStatus =
  | "new"
  | "qualified"
  | "contacted"
  | "followup"
  | "replied"
  | "won"
  | "lost"
  | "optout";

interface Prospect {
  id: string;
  name: string;
  category: string;
  city: string;
  address?: string | null;
  phone?: string | null;
  email?: string | null;
  score: number;
  status: ProspectStatus;
  _count?: { messages: number };
}

interface OutreachMessage {
  id: string;
  step: number;
  subject: string;
  body: string;
  status: string;
  sentAt?: string | null;
  createdAt: string;
}

interface AgentRun {
  id: string;
  agent: string;
  status: string;
  startedAt: string;
  finishedAt?: string | null;
  output?: string | null;
}

interface StatsData {
  byStatus: Record<string, number>;
  totalProspects: number;
  draftMessages: number;
  sentToday: number;
  dryRun: boolean;
  lastRuns: AgentRun[];
}

interface AgentSummary {
  agent: string;
  processed: number;
  created?: number;
  skipped?: number;
  sent?: number;
  failed?: number;
  details?: string[];
}

interface OrchestratorReport {
  startedAt: string;
  finishedAt: string;
  dryRun: boolean;
  steps: AgentSummary[];
}

// ─── Config statuts / agents ─────────────────────────────────────────────────

const STATUS_ORDER: ProspectStatus[] = [
  "new",
  "qualified",
  "contacted",
  "followup",
  "replied",
  "won",
  "lost",
  "optout",
];

const statusMeta: Record<
  ProspectStatus,
  { label: string; badge: string; dot: string }
> = {
  new: {
    label: "Nouveau",
    badge: "bg-slate-100 text-slate-700 border border-slate-200",
    dot: "bg-slate-400",
  },
  qualified: {
    label: "Qualifié",
    badge: "bg-blue-50 text-blue-700 border border-blue-200",
    dot: "bg-blue-500",
  },
  contacted: {
    label: "Contacté",
    badge: "bg-indigo-50 text-indigo-700 border border-indigo-200",
    dot: "bg-indigo-500",
  },
  followup: {
    label: "Relance",
    badge: "bg-violet-50 text-violet-700 border border-violet-200",
    dot: "bg-violet-500",
  },
  replied: {
    label: "Répondu",
    badge: "bg-emerald-50 text-emerald-700 border border-emerald-200",
    dot: "bg-emerald-500",
  },
  won: {
    label: "Gagné",
    badge: "bg-green-50 text-green-700 border border-green-200",
    dot: "bg-green-500",
  },
  lost: {
    label: "Perdu",
    badge: "bg-gray-100 text-gray-600 border border-gray-200",
    dot: "bg-gray-400",
  },
  optout: {
    label: "Désinscrit",
    badge: "bg-red-50 text-red-700 border border-red-200",
    dot: "bg-red-500",
  },
};

const agentLabels: Record<string, string> = {
  scout: "Scout",
  qualifier: "Qualification",
  copywriter: "Rédaction",
  sequencer: "Séquenceur",
  mailer: "Envoi",
  orchestrator: "Orchestrateur",
};

function agentLabel(agent: string) {
  return agentLabels[agent.toLowerCase()] ?? agent;
}

function stepLabel(step: number) {
  if (step <= 1) return "Email initial";
  return `Relance ${step - 1}`;
}

function formatDateTime(dateStr?: string | null) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleString("fr-FR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

async function readError(res: Response, fallback: string): Promise<string> {
  try {
    const data = (await res.json()) as { error?: string };
    return data.error || fallback;
  } catch {
    return fallback;
  }
}

// ─── Petits composants ───────────────────────────────────────────────────────

function StatusBadge({ status }: { status: ProspectStatus }) {
  const meta = statusMeta[status] ?? statusMeta.new;
  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs font-medium px-2 py-0.5 rounded-full whitespace-nowrap ${meta.badge}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${meta.dot}`} />
      {meta.label}
    </span>
  );
}

function Spinner({ className = "" }: { className?: string }) {
  return (
    <span
      className={`inline-block w-3.5 h-3.5 border-2 border-current/30 border-t-current rounded-full animate-spin ${className}`}
      aria-hidden="true"
    />
  );
}

function ScoreBar({ value }: { value: number }) {
  const pct = Math.max(0, Math.min(100, value));
  const color =
    pct >= 70 ? "bg-emerald-500" : pct >= 40 ? "bg-amber-500" : "bg-slate-300";
  return (
    <div className="flex items-center gap-2 min-w-[70px]">
      <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs font-semibold text-slate-700 tabular-nums w-6 text-right">
        {value}
      </span>
    </div>
  );
}

function AgentReportCard({ summary }: { summary: AgentSummary }) {
  const stats: { label: string; value: number | undefined; cls: string }[] = [
    { label: "traités", value: summary.processed, cls: "text-slate-700" },
    { label: "créés", value: summary.created, cls: "text-blue-700" },
    { label: "ignorés", value: summary.skipped, cls: "text-slate-500" },
    { label: "envoyés", value: summary.sent, cls: "text-emerald-700" },
    { label: "échecs", value: summary.failed, cls: "text-red-600" },
  ];
  return (
    <div className="border border-slate-200 rounded-lg bg-slate-50/60 px-3.5 py-2.5">
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <span className="text-[13px] font-semibold text-slate-900">
          {agentLabel(summary.agent)}
        </span>
        <div className="flex items-center gap-3 flex-wrap">
          {stats
            .filter((s) => s.value !== undefined)
            .map((s) => (
              <span key={s.label} className="text-xs text-slate-500">
                <span className={`font-semibold tabular-nums ${s.cls}`}>{s.value}</span>{" "}
                {s.label}
              </span>
            ))}
        </div>
      </div>
      {summary.details && summary.details.length > 0 && (
        <details className="mt-1.5">
          <summary className="text-xs text-indigo-600 cursor-pointer select-none hover:text-indigo-800 transition-colors">
            Détails ({summary.details.length})
          </summary>
          <ul className="mt-1.5 space-y-1 pl-1">
            {summary.details.map((d, i) => (
              <li key={i} className="text-xs text-slate-600 leading-snug">
                • {d}
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

// ─── Composant principal ─────────────────────────────────────────────────────

export default function OutreachClient() {
  const { toast } = useToast();

  const [stats, setStats] = useState<StatsData | null>(null);
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [loadingProspects, setLoadingProspects] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filtres
  const [statusFilter, setStatusFilter] = useState<ProspectStatus | "all">("all");
  const [search, setSearch] = useState("");

  // Panneau agents
  const [categories, setCategories] = useState("");
  const [cities, setCities] = useState("");
  const [discovering, setDiscovering] = useState(false);
  const [runningPipeline, setRunningPipeline] = useState(false);
  const [report, setReport] = useState<{ title: string; steps: AgentSummary[] } | null>(
    null
  );

  // Édition email inline (id prospect -> valeur saisie)
  const [emailDrafts, setEmailDrafts] = useState<Record<string, string>>({});
  const [savingEmailId, setSavingEmailId] = useState<string | null>(null);
  const [patchingId, setPatchingId] = useState<string | null>(null);

  // Panneau messages
  const [messagesFor, setMessagesFor] = useState<Prospect | null>(null);
  const [messages, setMessages] = useState<OutreachMessage[] | null>(null);
  const [loadingMessages, setLoadingMessages] = useState(false);

  // Formulaire d'ajout
  const [showAddForm, setShowAddForm] = useState(false);
  const [addForm, setAddForm] = useState({
    name: "",
    category: "",
    city: "",
    email: "",
    phone: "",
  });
  const [adding, setAdding] = useState(false);

  const busy = discovering || runningPipeline;

  // ─── Chargement des données ──────────────────────────────────────────────

  const fetchStats = useCallback(async () => {
    try {
      const res = await fetch("/api/outreach/stats");
      if (!res.ok) throw new Error(await readError(res, "Erreur de chargement des statistiques"));
      setStats((await res.json()) as StatsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur de chargement des statistiques");
    }
  }, []);

  const fetchProspects = useCallback(
    async (status: ProspectStatus | "all", q: string) => {
      setLoadingProspects(true);
      try {
        const params = new URLSearchParams();
        if (status !== "all") params.set("status", status);
        if (q.trim()) params.set("q", q.trim());
        const qs = params.toString();
        const res = await fetch(`/api/outreach/prospects${qs ? `?${qs}` : ""}`);
        if (!res.ok) throw new Error(await readError(res, "Erreur de chargement des prospects"));
        setProspects((await res.json()) as Prospect[]);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur de chargement des prospects");
      } finally {
        setLoadingProspects(false);
      }
    },
    []
  );

  const refreshAll = useCallback(() => {
    void fetchStats();
    void fetchProspects(statusFilter, search);
  }, [fetchStats, fetchProspects, statusFilter, search]);

  useEffect(() => {
    // Chargement initial des stats (déféré pour éviter un setState synchrone dans l'effet)
    const t = setTimeout(() => {
      void fetchStats();
    }, 0);
    return () => clearTimeout(t);
  }, [fetchStats]);

  // Prospects : re-fetch quand filtre/recherche changent (recherche debouncée)
  const searchDebounce = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => {
    if (searchDebounce.current) clearTimeout(searchDebounce.current);
    searchDebounce.current = setTimeout(() => {
      void fetchProspects(statusFilter, search);
    }, 300);
    return () => {
      if (searchDebounce.current) clearTimeout(searchDebounce.current);
    };
  }, [statusFilter, search, fetchProspects]);

  // ─── Actions agents ──────────────────────────────────────────────────────

  const handleDiscover = async () => {
    setDiscovering(true);
    setReport(null);
    setError(null);
    try {
      const body = {
        categories: categories.split(",").map((s) => s.trim()).filter(Boolean),
        cities: cities.split(",").map((s) => s.trim()).filter(Boolean),
      };
      const res = await fetch("/api/outreach/discover", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(await readError(res, "La découverte a échoué"));
      const data = (await res.json()) as { scout: AgentSummary; qualifier: AgentSummary };
      setReport({ title: "Rapport de découverte", steps: [data.scout, data.qualifier] });
      toast("Découverte terminée", "success");
      refreshAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : "La découverte a échoué");
    } finally {
      setDiscovering(false);
    }
  };

  const handleRunPipeline = async () => {
    setRunningPipeline(true);
    setReport(null);
    setError(null);
    try {
      const res = await fetch("/api/outreach/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skipDiscovery: true }),
      });
      if (!res.ok) throw new Error(await readError(res, "Le pipeline a échoué"));
      const data = (await res.json()) as OrchestratorReport;
      setReport({
        title: `Rapport du pipeline${data.dryRun ? " (dry-run)" : ""}`,
        steps: data.steps,
      });
      toast("Pipeline terminé", "success");
      refreshAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Le pipeline a échoué");
    } finally {
      setRunningPipeline(false);
    }
  };

  // ─── Actions prospects ───────────────────────────────────────────────────

  const patchProspect = async (
    id: string,
    payload: { status?: ProspectStatus; email?: string },
    successMsg: string
  ) => {
    setError(null);
    try {
      const res = await fetch(`/api/outreach/prospects/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(await readError(res, "La mise à jour a échoué"));
      toast(successMsg, "success");
      refreshAll();
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : "La mise à jour a échoué");
      return false;
    }
  };

  const handleStatusChange = async (id: string, status: ProspectStatus) => {
    setPatchingId(id);
    await patchProspect(id, { status }, `Statut mis à jour : ${statusMeta[status].label}`);
    setPatchingId(null);
  };

  const handleSaveEmail = async (id: string) => {
    const email = (emailDrafts[id] ?? "").trim();
    if (!email) return;
    setSavingEmailId(id);
    const ok = await patchProspect(id, { email }, "Email enregistré");
    if (ok) {
      setEmailDrafts((prev) => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
    }
    setSavingEmailId(null);
  };

  const openMessages = async (p: Prospect) => {
    setMessagesFor(p);
    setMessages(null);
    setLoadingMessages(true);
    try {
      const res = await fetch(`/api/outreach/messages?prospectId=${encodeURIComponent(p.id)}`);
      if (!res.ok) throw new Error(await readError(res, "Erreur de chargement des messages"));
      setMessages((await res.json()) as OutreachMessage[]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur de chargement des messages");
      setMessagesFor(null);
    } finally {
      setLoadingMessages(false);
    }
  };

  const handleAddProspect = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdding(true);
    setError(null);
    try {
      const payload: Record<string, string> = {
        name: addForm.name.trim(),
        category: addForm.category.trim(),
        city: addForm.city.trim(),
      };
      if (addForm.email.trim()) payload.email = addForm.email.trim();
      if (addForm.phone.trim()) payload.phone = addForm.phone.trim();
      const res = await fetch("/api/outreach/prospects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(await readError(res, "L'ajout du prospect a échoué"));
      toast("Prospect ajouté", "success");
      setAddForm({ name: "", category: "", city: "", email: "", phone: "" });
      setShowAddForm(false);
      refreshAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : "L'ajout du prospect a échoué");
    } finally {
      setAdding(false);
    }
  };

  // ─── Données dérivées ────────────────────────────────────────────────────

  const statCards = [
    { label: "Prospects", value: stats?.totalProspects, accent: "text-slate-900" },
    { label: "Qualifiés", value: stats?.byStatus?.qualified ?? 0, accent: "text-blue-600" },
    { label: "Contactés", value: stats?.byStatus?.contacted ?? 0, accent: "text-indigo-600" },
    { label: "Réponses", value: stats?.byStatus?.replied ?? 0, accent: "text-emerald-600" },
    { label: "Brouillons", value: stats?.draftMessages, accent: "text-amber-600" },
    { label: "Envoyés aujourd'hui", value: stats?.sentToday, accent: "text-violet-600" },
  ];

  const runStatusMeta = (status: string) => {
    const s = status.toLowerCase();
    if (s === "success")
      return { label: "Succès", cls: "bg-emerald-50 text-emerald-700 border border-emerald-200" };
    if (s === "error" || s === "failed")
      return { label: "Erreur", cls: "bg-red-50 text-red-700 border border-red-200" };
    if (s === "running")
      return { label: "En cours", cls: "bg-blue-50 text-blue-700 border border-blue-200" };
    return { label: status, cls: "bg-slate-100 text-slate-600 border border-slate-200" };
  };

  const inputCls =
    "w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 bg-white placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow";

  return (
    <div className="space-y-6 pb-8">
      {/* ─── En-tête ─── */}
      <div className="flex items-start justify-between gap-4 flex-wrap pt-1">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Prospection</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Agents orchestrés — entreprises sans site internet
          </p>
        </div>
        {stats &&
          (stats.dryRun ? (
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 flex-shrink-0" />
              DRY-RUN — aucun envoi réel
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full bg-red-50 text-red-700 border border-red-200">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse flex-shrink-0" />
              ENVOI RÉEL ACTIVÉ
            </span>
          ))}
      </div>

      {/* ─── Bannière d'erreur ─── */}
      {error && (
        <div className="flex items-start justify-between gap-3 p-3.5 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center gap-2 text-sm text-red-700">
            <svg
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              className="flex-shrink-0"
            >
              <circle cx="8" cy="8" r="6.5" />
              <line x1="8" y1="5" x2="8" y2="8.5" />
              <circle cx="8" cy="11" r="0.6" fill="currentColor" stroke="none" />
            </svg>
            {error}
          </div>
          <button
            onClick={() => setError(null)}
            className="text-red-400 hover:text-red-700 transition-colors flex-shrink-0 p-0.5"
            aria-label="Fermer l'erreur"
          >
            <svg
              width="12"
              height="12"
              viewBox="0 0 12 12"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            >
              <line x1="1" y1="1" x2="11" y2="11" />
              <line x1="11" y1="1" x2="1" y2="11" />
            </svg>
          </button>
        </div>
      )}

      {/* ─── Cartes stats ─── */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {statCards.map((card) => (
          <div key={card.label} className="bg-white rounded-lg border border-slate-200 p-4">
            {card.value === undefined ? (
              <div className="animate-pulse">
                <div className="h-7 w-10 bg-slate-100 rounded mb-2" />
                <div className="h-3 w-16 bg-slate-100 rounded" />
              </div>
            ) : (
              <>
                <p className={`text-2xl font-bold tabular-nums leading-none ${card.accent}`}>
                  {card.value}
                </p>
                <p className="text-xs text-slate-500 font-medium mt-1.5">{card.label}</p>
              </>
            )}
          </div>
        ))}
      </div>

      {/* ─── Panneau agents orchestrateurs ─── */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <div className="flex items-center gap-2 mb-4">
          <span className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center flex-shrink-0">
            <svg viewBox="0 0 20 20" fill="currentColor" className="w-[18px] h-[18px] text-indigo-600">
              <path d="M17.447 2.553a1 1 0 0 1 .215 1.09l-6 14a1 1 0 0 1-1.85.04L7.6 12.4l-5.283-2.212a1 1 0 0 1 .04-1.85l14-6a1 1 0 0 1 1.09.215zM9.05 11.657l1.507 3.616 4.34-10.126-10.126 4.34 3.616 1.507 3.32-3.32a.75.75 0 0 1 1.06 1.06l-3.32 3.32-.397-.397z" />
            </svg>
          </span>
          <div>
            <h2 className="text-sm font-semibold text-slate-900">Agents orchestrateurs</h2>
            <p className="text-xs text-slate-400">
              Scout → Qualification → Rédaction → Séquenceur → Envoi
            </p>
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-3 mb-4">
          <div>
            <label htmlFor="outreach-categories" className="block text-xs font-medium text-slate-600 mb-1.5">
              Catégories
            </label>
            <input
              id="outreach-categories"
              type="text"
              value={categories}
              onChange={(e) => setCategories(e.target.value)}
              placeholder="plombier, restaurant"
              disabled={busy}
              className={`${inputCls} disabled:opacity-60`}
            />
          </div>
          <div>
            <label htmlFor="outreach-cities" className="block text-xs font-medium text-slate-600 mb-1.5">
              Villes
            </label>
            <input
              id="outreach-cities"
              type="text"
              value={cities}
              onChange={(e) => setCities(e.target.value)}
              placeholder="Lyon, Villeurbanne"
              disabled={busy}
              className={`${inputCls} disabled:opacity-60`}
            />
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={handleDiscover}
            disabled={busy}
            className="inline-flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-700 active:bg-indigo-800 transition-colors shadow-sm disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {discovering ? <Spinner /> : <span aria-hidden="true">🔍</span>}
            Découvrir (Scout + Qualification)
          </button>
          <button
            onClick={handleRunPipeline}
            disabled={busy}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 active:bg-blue-800 transition-colors shadow-sm disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {runningPipeline ? <Spinner /> : <span aria-hidden="true">🚀</span>}
            Lancer le pipeline complet
          </button>
          {busy && (
            <span className="inline-flex items-center gap-2 text-sm text-slate-500">
              <Spinner className="text-indigo-500" />
              Les agents travaillent…
            </span>
          )}
        </div>

        {/* Rapport après run */}
        {report && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2.5">
              {report.title}
            </p>
            {report.steps.length === 0 ? (
              <p className="text-sm text-slate-400">Aucune étape exécutée.</p>
            ) : (
              <div className="space-y-2">
                {report.steps.map((s, i) => (
                  <AgentReportCard key={`${s.agent}-${i}`} summary={s} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ─── Tableau des prospects ─── */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="px-5 pt-4 pb-3 border-b border-slate-100 space-y-3">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <h2 className="text-sm font-semibold text-slate-900">Prospects</h2>
            <button
              onClick={() => setShowAddForm((v) => !v)}
              className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
            >
              {showAddForm ? "− Masquer le formulaire" : "+ Ajouter un prospect"}
            </button>
          </div>

          {/* Formulaire repliable d'ajout */}
          {showAddForm && (
            <form
              onSubmit={handleAddProspect}
              className="bg-slate-50 border border-slate-200 rounded-lg p-4 grid sm:grid-cols-2 lg:grid-cols-5 gap-3 items-end"
            >
              <div>
                <label htmlFor="add-name" className="block text-xs font-medium text-slate-600 mb-1">
                  Nom <span className="text-red-500">*</span>
                </label>
                <input
                  id="add-name"
                  type="text"
                  required
                  value={addForm.name}
                  onChange={(e) => setAddForm((f) => ({ ...f, name: e.target.value }))}
                  placeholder="Plomberie Martin"
                  className={inputCls}
                />
              </div>
              <div>
                <label htmlFor="add-category" className="block text-xs font-medium text-slate-600 mb-1">
                  Catégorie <span className="text-red-500">*</span>
                </label>
                <input
                  id="add-category"
                  type="text"
                  required
                  value={addForm.category}
                  onChange={(e) => setAddForm((f) => ({ ...f, category: e.target.value }))}
                  placeholder="plombier"
                  className={inputCls}
                />
              </div>
              <div>
                <label htmlFor="add-city" className="block text-xs font-medium text-slate-600 mb-1">
                  Ville <span className="text-red-500">*</span>
                </label>
                <input
                  id="add-city"
                  type="text"
                  required
                  value={addForm.city}
                  onChange={(e) => setAddForm((f) => ({ ...f, city: e.target.value }))}
                  placeholder="Lyon"
                  className={inputCls}
                />
              </div>
              <div>
                <label htmlFor="add-email" className="block text-xs font-medium text-slate-600 mb-1">
                  Email
                </label>
                <input
                  id="add-email"
                  type="email"
                  value={addForm.email}
                  onChange={(e) => setAddForm((f) => ({ ...f, email: e.target.value }))}
                  placeholder="contact@exemple.fr"
                  className={inputCls}
                />
              </div>
              <div>
                <label htmlFor="add-phone" className="block text-xs font-medium text-slate-600 mb-1">
                  Téléphone
                </label>
                <input
                  id="add-phone"
                  type="tel"
                  value={addForm.phone}
                  onChange={(e) => setAddForm((f) => ({ ...f, phone: e.target.value }))}
                  placeholder="04 78 00 00 00"
                  className={inputCls}
                />
              </div>
              <div className="sm:col-span-2 lg:col-span-5 flex gap-2">
                <button
                  type="submit"
                  disabled={adding}
                  className="inline-flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-60"
                >
                  {adding && <Spinner />}
                  {adding ? "Ajout en cours…" : "Ajouter"}
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg text-sm font-semibold hover:bg-white transition-colors"
                >
                  Annuler
                </button>
              </div>
            </form>
          )}

          {/* Filtres + recherche */}
          <div className="flex flex-col sm:flex-row gap-3 sm:items-center">
            <div className="relative w-full sm:w-64 flex-shrink-0">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 20 20"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                >
                  <circle cx="9" cy="9" r="6" />
                  <line x1="14.5" y1="14.5" x2="18" y2="18" />
                </svg>
              </span>
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Rechercher un prospect…"
                className={`${inputCls} pl-8`}
              />
            </div>
            <div className="flex items-center gap-1.5 flex-wrap">
              <button
                onClick={() => setStatusFilter("all")}
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium transition-all border ${
                  statusFilter === "all"
                    ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                    : "bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50"
                }`}
              >
                Tous
                <span
                  className={`text-[10px] font-semibold px-1 py-0.5 rounded-full min-w-[16px] text-center ${
                    statusFilter === "all" ? "bg-white/20 text-white" : "bg-slate-100 text-slate-500"
                  }`}
                >
                  {stats?.totalProspects ?? "–"}
                </span>
              </button>
              {STATUS_ORDER.map((s) => {
                const active = statusFilter === s;
                return (
                  <button
                    key={s}
                    onClick={() => setStatusFilter(s)}
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium transition-all border ${
                      active
                        ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                        : "bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50"
                    }`}
                  >
                    <span
                      className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${
                        active ? "bg-white/70" : statusMeta[s].dot
                      }`}
                    />
                    {statusMeta[s].label}
                    <span
                      className={`text-[10px] font-semibold px-1 py-0.5 rounded-full min-w-[16px] text-center ${
                        active ? "bg-white/20 text-white" : "bg-slate-100 text-slate-500"
                      }`}
                    >
                      {stats?.byStatus?.[s] ?? 0}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Table */}
        {loadingProspects ? (
          <div className="divide-y divide-slate-50">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="px-5 py-3.5 flex items-center gap-4 animate-pulse">
                <div className="h-3.5 w-36 bg-slate-100 rounded" />
                <div className="h-3.5 w-20 bg-slate-100 rounded hidden sm:block" />
                <div className="h-3.5 w-24 bg-slate-100 rounded hidden md:block" />
                <div className="h-3.5 flex-1 bg-slate-100 rounded" />
              </div>
            ))}
          </div>
        ) : prospects.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-center px-4">
            <div className="w-12 h-12 rounded-full bg-indigo-50 flex items-center justify-center mb-3">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-6 h-6 text-indigo-400">
                <path d="M17.447 2.553a1 1 0 0 1 .215 1.09l-6 14a1 1 0 0 1-1.85.04L7.6 12.4l-5.283-2.212a1 1 0 0 1 .04-1.85l14-6a1 1 0 0 1 1.09.215z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold text-slate-800 mb-1">
              {statusFilter !== "all" || search
                ? "Aucun prospect ne correspond"
                : "Aucun prospect — lancez le Scout"}
            </h3>
            <p className="text-xs text-slate-400 max-w-xs leading-relaxed">
              {statusFilter !== "all" || search
                ? "Modifiez la recherche ou réinitialisez les filtres."
                : "Renseignez des catégories et des villes puis cliquez sur « Découvrir » pour trouver des entreprises sans site internet."}
            </p>
            {(statusFilter !== "all" || search) && (
              <button
                onClick={() => {
                  setStatusFilter("all");
                  setSearch("");
                }}
                className="mt-4 text-sm text-slate-600 border border-slate-200 px-4 py-2 rounded-lg hover:bg-slate-50 transition-colors"
              >
                Réinitialiser les filtres
              </button>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/70">
                  <th className="text-left px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Nom</th>
                  <th className="text-left px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Catégorie</th>
                  <th className="text-left px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Ville</th>
                  <th className="text-left px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Téléphone</th>
                  <th className="text-left px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Email</th>
                  <th className="text-left px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Score</th>
                  <th className="text-left px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Statut</th>
                  <th className="text-center px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Messages</th>
                  <th className="text-right px-4 py-2.5 text-xs font-semibold text-slate-500 uppercase tracking-wide">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {prospects.map((p) => {
                  const isPatching = patchingId === p.id;
                  return (
                    <tr key={p.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-4 py-3 font-semibold text-slate-900 whitespace-nowrap">{p.name}</td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className="text-xs text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md">{p.category}</span>
                      </td>
                      <td className="px-4 py-3 text-slate-600 whitespace-nowrap">{p.city}</td>
                      <td className="px-4 py-3 text-slate-600 whitespace-nowrap tabular-nums">{p.phone || "—"}</td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        {p.email ? (
                          <span className="text-slate-600">{p.email}</span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5">
                            <input
                              type="email"
                              value={emailDrafts[p.id] ?? ""}
                              onChange={(e) =>
                                setEmailDrafts((prev) => ({ ...prev, [p.id]: e.target.value }))
                              }
                              onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                  e.preventDefault();
                                  void handleSaveEmail(p.id);
                                }
                              }}
                              placeholder="Ajouter un email…"
                              className="w-40 border border-slate-200 rounded-md px-2 py-1 text-xs text-slate-700 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                            <button
                              onClick={() => void handleSaveEmail(p.id)}
                              disabled={savingEmailId === p.id || !(emailDrafts[p.id] ?? "").trim()}
                              className="text-xs font-semibold text-white bg-indigo-600 px-2 py-1 rounded-md hover:bg-indigo-700 transition-colors disabled:opacity-50"
                            >
                              {savingEmailId === p.id ? <Spinner /> : "OK"}
                            </button>
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3">
                        <ScoreBar value={p.score} />
                      </td>
                      <td className="px-4 py-3">
                        <StatusBadge status={p.status} />
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="inline-flex items-center justify-center min-w-[22px] h-[22px] px-1.5 rounded-full bg-slate-100 text-slate-600 text-xs font-semibold tabular-nums">
                          {p._count?.messages ?? 0}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right whitespace-nowrap">
                        <div className="inline-flex items-center gap-1">
                          <button
                            onClick={() => void handleStatusChange(p.id, "replied")}
                            disabled={isPatching}
                            title="Marquer comme répondu"
                            className="text-xs font-medium text-emerald-700 border border-emerald-200 bg-emerald-50 px-2 py-1 rounded-md hover:bg-emerald-100 transition-colors disabled:opacity-50"
                          >
                            Répondu
                          </button>
                          <button
                            onClick={() => void handleStatusChange(p.id, "won")}
                            disabled={isPatching}
                            title="Marquer comme gagné"
                            className="text-xs font-medium text-green-700 border border-green-200 bg-green-50 px-2 py-1 rounded-md hover:bg-green-100 transition-colors disabled:opacity-50"
                          >
                            Gagné
                          </button>
                          <button
                            onClick={() => void handleStatusChange(p.id, "lost")}
                            disabled={isPatching}
                            title="Marquer comme perdu"
                            className="text-xs font-medium text-slate-600 border border-slate-200 bg-slate-50 px-2 py-1 rounded-md hover:bg-slate-100 transition-colors disabled:opacity-50"
                          >
                            Perdu
                          </button>
                          <button
                            onClick={() => void openMessages(p)}
                            title="Voir les emails"
                            className="text-xs font-medium text-indigo-700 border border-indigo-200 bg-indigo-50 px-2 py-1 rounded-md hover:bg-indigo-100 transition-colors"
                          >
                            Emails
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* ─── Journal des agents ─── */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="px-5 py-3.5 border-b border-slate-100">
          <h2 className="text-sm font-semibold text-slate-900">Journal des agents</h2>
        </div>
        {!stats ? (
          <div className="divide-y divide-slate-50">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="px-5 py-3 flex items-center gap-4 animate-pulse">
                <div className="h-3.5 w-24 bg-slate-100 rounded" />
                <div className="h-3.5 w-16 bg-slate-100 rounded" />
                <div className="h-3.5 flex-1 bg-slate-100 rounded" />
              </div>
            ))}
          </div>
        ) : stats.lastRuns.length === 0 ? (
          <p className="px-5 py-8 text-center text-sm text-slate-400">
            Aucune exécution pour le moment — les runs des agents apparaîtront ici.
          </p>
        ) : (
          <div className="divide-y divide-slate-50">
            {stats.lastRuns.map((run) => {
              const meta = runStatusMeta(run.status);
              return (
                <div key={run.id} className="px-5 py-3 flex items-center gap-3 flex-wrap">
                  <span className="text-[13px] font-semibold text-slate-900 w-28 flex-shrink-0">
                    {agentLabel(run.agent)}
                  </span>
                  <span
                    className={`inline-flex items-center text-[11px] font-semibold px-2 py-0.5 rounded-full ${meta.cls}`}
                  >
                    {meta.label}
                  </span>
                  <span className="text-xs text-slate-400 tabular-nums">
                    {formatDateTime(run.startedAt)}
                    {" → "}
                    {run.finishedAt ? formatDateTime(run.finishedAt) : "en cours…"}
                  </span>
                  {run.output && (
                    <span className="text-xs text-slate-500 truncate flex-1 min-w-[120px]" title={run.output}>
                      {run.output}
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ─── Panneau latéral : emails d'un prospect ─── */}
      {messagesFor && (
        <div
          className="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-sm"
          onClick={(e) => {
            if (e.target === e.currentTarget) setMessagesFor(null);
          }}
        >
          <aside className="w-full max-w-lg h-full bg-white shadow-2xl flex flex-col">
            <div className="px-5 py-4 border-b border-slate-100 flex items-start justify-between gap-3">
              <div className="min-w-0">
                <h3 className="font-semibold text-slate-900 truncate">
                  Emails — {messagesFor.name}
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  {messagesFor.category} · {messagesFor.city}
                </p>
              </div>
              <button
                onClick={() => setMessagesFor(null)}
                className="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors flex-shrink-0"
                aria-label="Fermer le panneau"
              >
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 14 14"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                >
                  <line x1="1" y1="1" x2="13" y2="13" />
                  <line x1="13" y1="1" x2="1" y2="13" />
                </svg>
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-5 space-y-4">
              {loadingMessages ? (
                <div className="flex items-center justify-center gap-2 py-12 text-sm text-slate-400">
                  <Spinner className="text-indigo-500" />
                  Chargement des messages…
                </div>
              ) : !messages || messages.length === 0 ? (
                <p className="text-sm text-slate-400 text-center py-12">
                  Aucun message pour ce prospect — le Copywriter n&apos;est pas encore passé.
                </p>
              ) : (
                messages.map((m) => (
                  <div key={m.id} className="border border-slate-200 rounded-lg overflow-hidden">
                    <div className="px-4 py-2.5 bg-slate-50 border-b border-slate-100 flex items-center justify-between gap-2 flex-wrap">
                      <span className="text-[11px] font-semibold text-indigo-700 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-full">
                        {stepLabel(m.step)}
                      </span>
                      <span className="text-[11px] text-slate-400">
                        {m.status === "sent" ? "Envoyé" : m.status === "draft" ? "Brouillon" : m.status}
                        {" · "}
                        {formatDateTime(m.sentAt ?? m.createdAt)}
                      </span>
                    </div>
                    <div className="p-4">
                      <p className="text-sm font-bold text-slate-900 mb-2">{m.subject}</p>
                      <pre className="whitespace-pre-wrap text-[13px] text-slate-600 font-sans leading-relaxed">
                        {m.body}
                      </pre>
                    </div>
                  </div>
                ))
              )}
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
