export default function CompetitorsLoading() {
  return (
    <div className="space-y-5 pb-10 animate-pulse">

      {/* ── Page header ──────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between">
        <div>
          <div className="h-7 w-48 bg-slate-200 rounded-lg mb-2" />
          <div className="h-4 w-64 bg-slate-100 rounded" />
        </div>
        <div className="h-9 w-36 bg-slate-200 rounded-xl" />
      </div>

      {/* ── Filter bar + view toggle ──────────────────────────────────────── */}
      <div className="flex items-center gap-3 flex-wrap">
        {/* Search box */}
        <div className="flex-1 min-w-[200px] max-w-sm h-9 bg-slate-100 rounded-xl" />
        {/* Filter pills */}
        <div className="flex gap-2">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-7 w-16 bg-slate-100 rounded-full" />
          ))}
        </div>
        {/* Sort + view toggle */}
        <div className="ml-auto flex items-center gap-2">
          <div className="h-8 w-24 bg-slate-100 rounded-lg" />
          <div className="h-8 w-16 bg-slate-100 rounded-lg" />
        </div>
      </div>

      {/* ── Competitor grid — 6 cards ─────────────────────────────────────── */}
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col gap-4"
          >
            {/* Card header: logo + name + badge */}
            <div className="flex items-start gap-3">
              <div className="w-12 h-12 rounded-xl bg-slate-200 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="h-4 w-28 bg-slate-200 rounded mb-1.5" />
                <div className="h-3 w-20 bg-slate-100 rounded mb-2" />
                <div className="h-5 w-14 bg-slate-100 rounded-full" />
              </div>
              <div className="h-7 w-7 bg-slate-100 rounded-lg flex-shrink-0" />
            </div>

            {/* Description lines */}
            <div className="space-y-1.5">
              <div className="h-3 w-full bg-slate-100 rounded" />
              <div className="h-3 w-5/6 bg-slate-100 rounded" />
              <div className="h-3 w-2/3 bg-slate-100 rounded" />
            </div>

            {/* Market share bar */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <div className="h-3 w-20 bg-slate-100 rounded" />
                <div className="h-3 w-8 bg-slate-200 rounded" />
              </div>
              <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-slate-200 rounded-full"
                  style={{ width: `${30 + i * 10}%` }}
                />
              </div>
            </div>

            {/* Footer: last updated + CTA */}
            <div className="flex items-center justify-between pt-1 border-t border-slate-50">
              <div className="h-3 w-24 bg-slate-100 rounded" />
              <div className="h-7 w-24 bg-slate-100 rounded-lg" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
