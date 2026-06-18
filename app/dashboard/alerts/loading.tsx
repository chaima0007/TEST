export default function AlertsLoading() {
  return (
    <div className="space-y-5 pb-10 animate-pulse">

      {/* ── Page header ──────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between">
        <div>
          <div className="h-7 w-36 bg-slate-200 rounded-lg mb-2" />
          <div className="h-4 w-56 bg-slate-100 rounded" />
        </div>
        {/* Unread badge */}
        <div className="h-7 w-24 bg-slate-100 rounded-full" />
      </div>

      {/* ── Type filter pills ─────────────────────────────────────────────── */}
      <div className="flex items-center gap-2 flex-wrap">
        {[...Array(6)].map((_, i) => (
          <div key={i} className={`h-7 bg-slate-100 rounded-full ${i === 0 ? "w-12" : "w-20"}`} />
        ))}
        <div className="ml-auto h-8 w-32 bg-slate-100 rounded-lg" />
      </div>

      {/* ── Alert list — 6 skeleton rows ─────────────────────────────────── */}
      <div className="space-y-3">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="bg-white rounded-xl border border-slate-200 overflow-hidden flex"
          >
            {/* Left accent strip */}
            <div className="w-1 bg-slate-200 flex-shrink-0" />
            <div className="flex-1 p-4">
              <div className="flex items-start gap-3">
                {/* Icon circle */}
                <div className="w-9 h-9 rounded-full bg-slate-100 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  {/* Type + competitor badges */}
                  <div className="flex gap-2 mb-2.5">
                    <div className="h-5 w-20 bg-slate-100 rounded-full" />
                    <div className="h-5 w-16 bg-slate-100 rounded-full" />
                  </div>
                  {/* Message lines */}
                  <div className="h-4 w-full bg-slate-100 rounded mb-1.5" />
                  <div className="h-4 w-4/5 bg-slate-100 rounded mb-2" />
                  {/* Date */}
                  <div className="h-3 w-28 bg-slate-100 rounded" />
                </div>
                {/* Action button */}
                <div className="h-7 w-24 bg-slate-100 rounded-lg flex-shrink-0" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* ── Pagination skeleton ───────────────────────────────────────────── */}
      <div className="flex items-center justify-center gap-2 pt-2">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-8 w-8 bg-slate-100 rounded-lg" />
        ))}
      </div>
    </div>
  );
}
