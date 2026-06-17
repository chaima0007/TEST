"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

type StepStatus   = "pending" | "sent" | "skipped" | "failed";
type EnrStatus    = "active" | "paused" | "completed" | "stopped";
type StopReason   = "reply_received" | "opt_out" | "max_touches" | "manual" | "converted" | null;

interface Step       { step_index: number; template_id: string; scheduled_at: string; status: StepStatus; sent_at: string | null; opened_at: string | null; clicked_at: string | null; error: string | null; }
interface Enrollment { enrollment_id: string; prospect_id: string; company_name: string; sequence_id: string; sequence_name: string; started_at: string; status: EnrStatus; stop_reason: StopReason; sent_count: number; opened_count: number; clicked_count: number; steps: Step[]; }
interface SequenceDef { sequence_id: string; name: string; description: string; max_touches: number; step_count: number; }
interface Summary { total_enrollments: number; by_status: Record<string, number>; total_sent: number; total_opened: number; total_clicked: number; open_rate_pct: number; click_rate_pct: number; stop_reasons: Record<string, number>; sequences_count: number; }
interface Data { source: string; sequences: SequenceDef[]; enrollments: Enrollment[]; summary: Summary; }

// ── Colour maps ────────────────────────────────────────────────────────────────

const STATUS_COLORS: Record<EnrStatus, string> = {
  active:    "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  paused:    "bg-amber-500/20 text-amber-300 border-amber-500/30",
  completed: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
  stopped:   "bg-red-500/20 text-red-300 border-red-500/30",
};

const STEP_COLORS: Record<StepStatus, string> = {
  pending: "bg-white/[0.04] border-white/[0.08] text-gray-500",
  sent:    "bg-indigo-500/15 border-indigo-500/25 text-indigo-300",
  skipped: "bg-gray-500/10 border-gray-500/20 text-gray-600",
  failed:  "bg-red-500/15 border-red-500/25 text-red-400",
};

const STOP_LABELS: Record<string, string> = {
  reply_received: "Réponse reçue",
  opt_out:        "Désinscription",
  max_touches:    "Max touches",
  manual:         "Arrêt manuel",
  converted:      "Converti",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

function pct(n: number, d: number) { return d === 0 ? "0%" : `${Math.round(n / d * 100)}%`; }
function fmtDate(iso: string | null) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("fr-FR", { day: "2-digit", month: "short" });
}

function StatusBadge({ status }: { status: EnrStatus }) {
  const labels: Record<EnrStatus, string> = { active: "Actif", paused: "Pausé", completed: "Terminé", stopped: "Arrêté" };
  return <span className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_COLORS[status]}`}>{labels[status]}</span>;
}

function StepTimeline({ steps }: { steps: Step[] }) {
  return (
    <div className="flex items-center gap-1 mt-2">
      {steps.map(s => (
        <div key={s.step_index} className="group relative">
          <div className={`w-6 h-6 rounded border flex items-center justify-center text-[9px] font-bold cursor-default ${STEP_COLORS[s.status]}`}>
            {s.status === "sent" ? "✓" : s.status === "skipped" ? "—" : s.status === "failed" ? "✗" : s.step_index + 1}
          </div>
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 bg-[#1a1d2e] border border-white/[0.1] rounded-lg px-2 py-1 text-[10px] text-gray-300 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity z-10 pointer-events-none">
            <span className="block">{s.template_id}</span>
            {s.sent_at && <span className="text-emerald-400 block">Envoyé {fmtDate(s.sent_at)}</span>}
            {s.opened_at && <span className="text-indigo-400 block">Ouvert {fmtDate(s.opened_at)}</span>}
            {s.clicked_at && <span className="text-amber-400 block">Cliqué {fmtDate(s.clicked_at)}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Enrollment modal ───────────────────────────────────────────────────────────

function EnrollmentModal({ e, onClose }: { e: Enrollment; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-xl max-h-[90vh] overflow-y-auto" onClick={ev => ev.stopPropagation()}>
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06]">
          <div>
            <h2 className="font-bold text-lg">{e.company_name}</h2>
            <p className="text-sm text-gray-500">{e.sequence_name} — {e.enrollment_id}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-xl leading-none">×</button>
        </div>
        <div className="p-5 space-y-5">
          <div className="flex flex-wrap gap-2 items-center">
            <StatusBadge status={e.status} />
            {e.stop_reason && <span className="text-xs px-2 py-0.5 rounded-full border bg-gray-500/10 border-gray-500/20 text-gray-400">{STOP_LABELS[e.stop_reason] ?? e.stop_reason}</span>}
          </div>

          <div className="grid grid-cols-3 gap-3 text-center">
            {[["Envoyés", e.sent_count, "text-white"], ["Ouverts", e.opened_count, "text-indigo-400"], ["Cliqués", e.clicked_count, "text-amber-400"]].map(([l, v, c]) => (
              <div key={String(l)} className="bg-white/[0.03] rounded-xl p-3 border border-white/[0.07]">
                <p className="text-xs text-gray-500">{l}</p>
                <p className={`text-xl font-bold mt-0.5 ${c}`}>{v}</p>
              </div>
            ))}
          </div>

          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Étapes</p>
            <div className="space-y-2">
              {e.steps.map(s => (
                <div key={s.step_index} className={`flex items-center gap-3 rounded-xl p-3 border ${STEP_COLORS[s.status]}`}>
                  <div className="w-6 h-6 rounded border flex items-center justify-center text-[9px] font-bold flex-shrink-0 border-current">
                    {s.status === "sent" ? "✓" : s.status === "skipped" ? "—" : s.status === "failed" ? "✗" : s.step_index + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium">{s.template_id}</p>
                    <p className="text-[10px] text-gray-500">Prévu {fmtDate(s.scheduled_at)}</p>
                  </div>
                  <div className="text-right text-[10px] space-y-0.5">
                    {s.opened_at  && <p className="text-indigo-400">Ouvert {fmtDate(s.opened_at)}</p>}
                    {s.clicked_at && <p className="text-amber-400">Cliqué {fmtDate(s.clicked_at)}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Sequence card ──────────────────────────────────────────────────────────────

function SequenceCard({ seq, enrollments }: { seq: SequenceDef; enrollments: Enrollment[] }) {
  const total  = enrollments.length;
  const active = enrollments.filter(e => e.status === "active").length;
  const done   = enrollments.filter(e => e.status === "completed").length;
  const conv   = enrollments.filter(e => e.stop_reason === "converted").length;

  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
      <p className="font-semibold text-sm">{seq.name}</p>
      <p className="text-xs text-gray-500 mt-0.5 mb-3">{seq.description}</p>
      <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-400">
        <span>{seq.step_count} étapes · max {seq.max_touches}</span>
        <span className="text-white">{total} inscrits</span>
        <span className="text-emerald-400">{active} actifs</span>
        <span className="text-indigo-400">{done} terminés</span>
        {conv > 0 && <span className="text-amber-400">{conv} convertis</span>}
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function SequencesPage() {
  const [data, setData]       = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Enrollment | null>(null);
  const [statusFilter, setStatusFilter] = useState("all");
  const [seqFilter, setSeqFilter] = useState("all");

  useEffect(() => {
    fetch("/api/sequences").then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" /></div>;
  if (!data)   return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary, sequences, enrollments } = data;

  const filtered = enrollments.filter(e =>
    (statusFilter === "all" || e.status === statusFilter) &&
    (seqFilter    === "all" || e.sequence_id === seqFilter)
  );

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <EnrollmentModal e={selected} onClose={() => setSelected(null)} />}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Séquences Outreach</h1>
          <p className="text-sm text-gray-500 mt-0.5">Gestion des séquences d'emails multi-touches</p>
        </div>
        {data.source === "mock" && <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">Données démo</span>}
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Total inscrits",    value: String(summary.total_enrollments),   color: "text-white"      },
          { label: "Emails envoyés",    value: String(summary.total_sent),           color: "text-indigo-400" },
          { label: "Taux d'ouverture",  value: `${summary.open_rate_pct}%`,          color: "text-emerald-400"},
          { label: "Taux de clic",      value: `${summary.click_rate_pct}%`,         color: "text-amber-400"  },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      {/* Status breakdown */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {(["active","completed","stopped","paused"] as EnrStatus[]).map(s => (
          <div key={s} className={`rounded-xl p-3 border ${STATUS_COLORS[s]} bg-opacity-10`}>
            <p className="text-xs capitalize">{s === "active" ? "Actifs" : s === "completed" ? "Terminés" : s === "stopped" ? "Arrêtés" : "Pausés"}</p>
            <p className="text-xl font-bold mt-0.5">{summary.by_status[s] ?? 0}</p>
          </div>
        ))}
      </div>

      {/* Sequence cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {sequences.map(s => (
          <SequenceCard key={s.sequence_id} seq={s} enrollments={enrollments.filter(e => e.sequence_id === s.sequence_id)} />
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="flex gap-2 flex-wrap">
          {["all","active","completed","stopped","paused"].map(f => (
            <button key={f} onClick={() => setStatusFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${statusFilter === f ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
              {f === "all" ? "Tous" : f === "active" ? "Actifs" : f === "completed" ? "Terminés" : f === "stopped" ? "Arrêtés" : "Pausés"}
            </button>
          ))}
        </div>
        <select value={seqFilter} onChange={e => setSeqFilter(e.target.value)}
          className="bg-white/[0.03] border border-white/[0.07] rounded-lg px-3 py-1.5 text-xs text-gray-400 focus:outline-none focus:border-indigo-500">
          <option value="all">Toutes les séquences</option>
          {sequences.map(s => <option key={s.sequence_id} value={s.sequence_id}>{s.name}</option>)}
        </select>
      </div>

      {/* Table */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Entreprise", "Séquence", "Statut", "Progression", "Ouvertures", "Clics", "Démarré"].map(h => (
                  <th key={h} className="text-left py-3 px-4 text-xs text-gray-500 uppercase tracking-wider font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={7} className="text-center py-10 text-gray-600 text-sm">Aucune inscription.</td></tr>
              ) : filtered.map(e => (
                <tr key={e.enrollment_id} className="border-b border-white/[0.04] hover:bg-white/[0.02] cursor-pointer" onClick={() => setSelected(e)}>
                  <td className="py-3 px-4">
                    <p className="font-medium text-sm">{e.company_name}</p>
                    <p className="text-xs text-gray-500">{e.enrollment_id}</p>
                    {e.stop_reason && <p className="text-[10px] text-red-400 mt-0.5">{STOP_LABELS[e.stop_reason]}</p>}
                  </td>
                  <td className="py-3 px-4 text-xs text-gray-400">{e.sequence_name}</td>
                  <td className="py-3 px-4"><StatusBadge status={e.status} /></td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
                        <div className="h-full bg-indigo-500 rounded-full" style={{ width: pct(e.sent_count, e.steps.length) }} />
                      </div>
                      <span className="text-xs text-gray-500">{e.sent_count}/{e.steps.length}</span>
                    </div>
                    <StepTimeline steps={e.steps} />
                  </td>
                  <td className="py-3 px-4 text-sm text-center">{e.opened_count > 0 ? <span className="text-indigo-400 font-medium">{e.opened_count}</span> : <span className="text-gray-600">0</span>}</td>
                  <td className="py-3 px-4 text-sm text-center">{e.clicked_count > 0 ? <span className="text-amber-400 font-medium">{e.clicked_count}</span> : <span className="text-gray-600">0</span>}</td>
                  <td className="py-3 px-4 text-xs text-gray-500">{fmtDate(e.started_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <p className="text-xs text-gray-600 text-center">{filtered.length} inscription(s) — Cliquer pour le détail</p>
    </div>
  );
}
