export default function ReportsLoading() {
  return (
    <div className="space-y-5 pb-10 animate-pulse">

      {/* ── Page header ──────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between">
        <div>
          <div className="h-7 w-40 bg-slate-200 rounded-lg mb-2" />
          <div className="h-4 w-60 bg-slate-100 rounded" />
        </div>
        <div className="h-9 w-40 bg-slate-200 rounded-xl" />
      </div>

      {/* ── Status filter tabs ────────────────────────────────────────────── */}
      <div className="flex gap-2">
        {["Tous", "Prêts", "En cours"].map((label) => (
          <div key={label} className="h-8 w-20 bg-slate-100 rounded-lg" />
        ))}
      </div>

      {/* ── Report cards grid — 6 cards ──────────────────────────────────── */}
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col gap-3"
          >
            {/* Card top: icon + status badge */}
            <div className="flex items-start justify-between">
              <div className="w-11 h-11 bg-slate-100 rounded-xl" />
              <div className="h-5 w-14 bg-slate-100 rounded-full" />
            </div>

            {/* Title + description */}
            <div>
              <div className="h-4 w-52 bg-slate-200 rounded mb-2" />
              <div className="h-3 w-full bg-slate-100 rounded mb-1.5" />
              <div className="h-3 w-3/4 bg-slate-100 rounded" />
            </div>

            {/* Meta: pages + date */}
            <div className="flex items-center gap-3 pt-1">
              <div className="h-3 w-16 bg-slate-100 rounded" />
              <div className="h-3 w-1 bg-slate-100 rounded-full" />
              <div className="h-3 w-24 bg-slate-100 rounded" />
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-2 pt-2 border-t border-slate-50">
              <div className="flex-1 h-8 bg-slate-100 rounded-lg" />
              <div className="h-8 w-8 bg-slate-100 rounded-lg" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
