"use client";

import { useCallback, useEffect, useState } from "react";

// ─── Types (miroir des réponses API) ─────────────────────────────────────────
interface StepLog { id: string; step: string; status: string; message: string; durationMs: number; }
interface RunSummary {
  id: string; status: string; currentStep: number; startedAt: string; finishedAt: string | null;
  error: string | null; steps: StepLog[]; _count: { matches: number; analyzed: number };
}
interface AnalyzedJob {
  id: string; title: string; status: string; skills: string; budget: number | null;
  durationDays: number | null; location: string | null; reason: string;
}
interface MatchRow {
  id: string; confidence: number; snippet: string; status: string;
  analyzedJob: { title: string }; profile: { name: string };
}
interface RunDetail extends RunSummary {
  analyzed: AnalyzedJob[];
  matches: MatchRow[];
}

const STEP_LABELS: Record<string, string> = {
  ingest: "Ingestion", filter: "Filtrage", match: "Matching", enrich: "Enrichissement", notify: "Notification",
};
const ALL_STEPS = ["ingest", "filter", "match", "enrich", "notify"];

const statusBadge: Record<string, string> = {
  running: "bg-blue-50 text-[#0078D4]",
  completed: "bg-green-50 text-[#107C10]",
  failed: "bg-red-50 text-[#D83B01]",
};

export default function PipelinePage() {
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [threshold, setThreshold] = useState<number | null>(null);
  const [selected, setSelected] = useState<RunDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  const loadRuns = useCallback(async () => {
    const res = await fetch("/api/pipeline/run");
    const data = await res.json();
    setRuns(data.runs);
    setThreshold(data.minBudgetThreshold);
    setLoading(false);
    return data.runs as RunSummary[];
  }, []);

  const loadDetail = useCallback(async (id: string) => {
    const res = await fetch(`/api/pipeline/runs/${id}`);
    if (res.ok) setSelected(await res.json());
  }, []);

  useEffect(() => {
    fetch("/api/pipeline/run")
      .then((r) => r.json())
      .then((data) => { setRuns(data.runs); setThreshold(data.minBudgetThreshold); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const handleRun = async () => {
    setRunning(true);
    try {
      await fetch("/api/pipeline/run", { method: "POST" });
      const fresh = await loadRuns();
      if (fresh[0]) await loadDetail(fresh[0].id);
    } finally {
      setRunning(false);
    }
  };

  const handleResume = async (runId: string) => {
    setRunning(true);
    try {
      await fetch(`/api/pipeline/runs/${runId}/resume`, { method: "POST" });
      await loadRuns();
      await loadDetail(runId);
    } finally {
      setRunning(false);
    }
  };

  const handleMatch = async (matchId: string, action: "approve" | "reject", reason?: string) => {
    await fetch(`/api/pipeline/matches/${matchId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, reason }),
    });
    if (selected) await loadDetail(selected.id);
    await loadRuns(); // le seuil a pu bouger
  };

  return (
    <div className="space-y-6 pb-8">
      {/* Header */}
      <div className="flex items-center justify-between pt-1">
        <div>
          <h1 className="text-[22px] font-semibold text-slate-900 tracking-tight">Pipeline de matching</h1>
          <p className="text-[13px] text-slate-500 mt-0.5">
            Ingestion → Filtrage → Matching → Enrichissement → Notification
          </p>
        </div>
        <div className="flex items-center gap-3">
          {threshold !== null && (
            <span className="hidden sm:inline-flex items-center gap-1.5 text-[12px] text-slate-500 font-medium bg-slate-100 px-3 py-1.5 rounded-md">
              Seuil budget : <span className="font-semibold text-slate-700 tabular-nums">{threshold} €</span>
            </span>
          )}
          <button
            onClick={handleRun}
            disabled={running}
            className="inline-flex items-center gap-2 bg-[#0078D4] text-white text-[13px] font-semibold px-4 py-2 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-60"
          >
            {running ? "Exécution…" : "Lancer un run"}
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-[320px_1fr] gap-5">
        {/* Liste des runs */}
        <div className="bg-white rounded-lg border border-slate-200 overflow-hidden h-fit">
          <div className="px-4 py-3 border-b border-slate-100">
            <h2 className="text-[13px] font-semibold text-slate-900">Historique des runs</h2>
          </div>
          <div className="divide-y divide-slate-100 max-h-[520px] overflow-y-auto">
            {loading ? (
              <p className="px-4 py-6 text-[13px] text-slate-400">Chargement…</p>
            ) : runs.length === 0 ? (
              <p className="px-4 py-6 text-[13px] text-slate-400">Aucun run. Cliquez sur « Lancer un run ».</p>
            ) : (
              runs.map((r) => {
                const done = r.status === "completed" ? ALL_STEPS.length : r.currentStep;
                const isSel = selected?.id === r.id;
                return (
                  <button
                    key={r.id}
                    onClick={() => loadDetail(r.id)}
                    className={`w-full text-left px-4 py-3 transition-colors ${isSel ? "bg-blue-50/60" : "hover:bg-slate-50"}`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${statusBadge[r.status] ?? "bg-slate-100 text-slate-500"}`}>
                        {r.status}
                      </span>
                      <span className="text-[11px] text-slate-400 tabular-nums">
                        {new Date(r.startedAt).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
                      </span>
                    </div>
                    {/* Progress des étapes */}
                    <div className="flex gap-1">
                      {ALL_STEPS.map((_, i) => (
                        <div key={i} className={`h-1.5 flex-1 rounded-full ${i < done ? "bg-[#0078D4]" : r.status === "failed" && i === r.currentStep ? "bg-[#D83B01]" : "bg-slate-200"}`} />
                      ))}
                    </div>
                    <p className="text-[11px] text-slate-400 mt-1.5 tabular-nums">
                      {r._count.analyzed} offre(s) · {r._count.matches} match(s)
                    </p>
                  </button>
                );
              })
            )}
          </div>
        </div>

        {/* Détail du run sélectionné */}
        <div className="space-y-5">
          {!selected ? (
            <div className="bg-white rounded-lg border border-slate-200 p-10 text-center text-[13px] text-slate-400">
              Sélectionnez un run pour voir le détail des étapes et les propositions.
            </div>
          ) : (
            <>
              {/* Timeline des étapes (décisions) */}
              <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                <div className="px-5 py-3.5 border-b border-slate-100">
                  <h2 className="text-[13px] font-semibold text-slate-900">Journal des étapes</h2>
                </div>
                <div className="px-5 py-4 space-y-3">
                  {selected.steps.map((s) => (
                    <div key={s.id} className="flex items-start gap-3">
                      <span className={`mt-1 w-2.5 h-2.5 rounded-full flex-shrink-0 ${s.status === "ok" ? "bg-[#107C10]" : "bg-[#D83B01]"}`} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2">
                          <p className="text-[13px] font-medium text-slate-800">{STEP_LABELS[s.step] ?? s.step}</p>
                          <span className="text-[11px] text-slate-400 tabular-nums">{s.durationMs} ms</span>
                        </div>
                        <p className="text-[12px] text-slate-500">{s.message}</p>
                      </div>
                    </div>
                  ))}
                  {selected.error && (
                    <div className="flex items-center justify-between gap-3 bg-red-50 rounded-md px-3 py-2">
                      <p className="text-[12px] text-[#D83B01]">{selected.error}</p>
                      <button
                        onClick={() => handleResume(selected.id)}
                        disabled={running}
                        className="text-[12px] font-medium px-3 py-1 rounded-md bg-white text-[#D83B01] border border-red-200 hover:bg-red-100 transition-colors disabled:opacity-60 flex-shrink-0"
                      >
                        {running ? "…" : "Reprendre"}
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* Propositions à valider */}
              <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                <div className="px-5 py-3.5 border-b border-slate-100">
                  <h2 className="text-[13px] font-semibold text-slate-900">Propositions ({selected.matches.length})</h2>
                </div>
                <div className="divide-y divide-slate-100">
                  {selected.matches.length === 0 ? (
                    <p className="px-5 py-6 text-[13px] text-slate-400">Aucune proposition pour ce run.</p>
                  ) : (
                    selected.matches.map((m) => (
                      <div key={m.id} className="px-5 py-4">
                        <div className="flex items-start justify-between gap-3">
                          <div className="min-w-0">
                            <p className="text-[13px] font-medium text-slate-900">{m.analyzedJob.title}</p>
                            <p className="text-[12px] text-slate-500">→ {m.profile.name}</p>
                            <p className="text-[12px] text-slate-400 mt-1">{m.snippet}</p>
                          </div>
                          <span className="text-[13px] font-bold text-[#0078D4] tabular-nums flex-shrink-0">
                            {Math.round(m.confidence * 100)}%
                          </span>
                        </div>
                        {m.status === "proposed" ? (
                          <div className="flex gap-2 mt-3">
                            <button onClick={() => handleMatch(m.id, "approve")}
                              className="text-[12px] font-medium px-3 py-1.5 rounded-md bg-green-50 text-[#107C10] hover:bg-green-100 transition-colors">
                              Approuver
                            </button>
                            <button onClick={() => handleMatch(m.id, "reject", "budget")}
                              className="text-[12px] font-medium px-3 py-1.5 rounded-md bg-amber-50 text-amber-700 hover:bg-amber-100 transition-colors">
                              Pas assez cher
                            </button>
                            <button onClick={() => handleMatch(m.id, "reject", "other")}
                              className="text-[12px] font-medium px-3 py-1.5 rounded-md bg-slate-50 text-slate-500 hover:bg-slate-100 transition-colors">
                              Rejeter
                            </button>
                          </div>
                        ) : (
                          <span className={`inline-block mt-2 text-[11px] font-semibold px-2 py-0.5 rounded-full ${m.status === "approved" ? "bg-green-50 text-[#107C10]" : "bg-red-50 text-[#D83B01]"}`}>
                            {m.status === "approved" ? "Approuvé" : "Rejeté"}
                          </span>
                        )}
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Décisions de filtrage (offres rejetées visibles) */}
              <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                <div className="px-5 py-3.5 border-b border-slate-100">
                  <h2 className="text-[13px] font-semibold text-slate-900">Offres analysées ({selected.analyzed.length})</h2>
                </div>
                <div className="divide-y divide-slate-100">
                  {selected.analyzed.map((j) => (
                    <div key={j.id} className="px-5 py-3 flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <p className="text-[13px] text-slate-800">{j.title}</p>
                        <p className="text-[12px] text-slate-400">{j.reason}</p>
                      </div>
                      <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ${j.status === "qualified" ? "bg-green-50 text-[#107C10]" : j.status === "rejected" ? "bg-red-50 text-[#D83B01]" : "bg-slate-100 text-slate-500"}`}>
                        {j.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
