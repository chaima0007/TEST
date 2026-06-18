export default function DashboardLoading() {
  return (
    <div className="space-y-5 pb-10 animate-pulse">

      {/* ── Page header skeleton ─────────────────────────────────────────── */}
      <div className="flex items-center justify-between pt-1 pb-1">
        <div>
          <div className="h-7 w-44 bg-slate-200 rounded-lg mb-2" />
          <div className="h-4 w-64 bg-slate-100 rounded" />
        </div>
        <div className="hidden sm:block h-7 w-36 bg-slate-100 rounded-lg" />
      </div>

      {/* ── KPI banner — 5 cards ─────────────────────────────────────────── */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="bg-white rounded-xl border-l-4 border-slate-200 p-4 shadow-sm flex flex-col gap-3"
          >
            <div className="h-3 w-24 bg-slate-100 rounded" />
            <div className="h-8 w-16 bg-slate-200 rounded" />
            <div className="h-3 w-14 bg-slate-100 rounded" />
          </div>
        ))}
      </div>

      {/* ── Main grid ────────────────────────────────────────────────────── */}
      <div className="grid lg:grid-cols-3 gap-5">

        {/* ── Left column (2/3) ──────────────────────────────────────────── */}
        <div className="lg:col-span-2 flex flex-col gap-5">

          {/* Table skeleton — 6 rows */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            {/* Table header */}
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <div className="h-4 w-32 bg-slate-200 rounded mb-1.5" />
                <div className="h-3 w-48 bg-slate-100 rounded" />
              </div>
              <div className="h-4 w-14 bg-slate-100 rounded" />
            </div>
            {/* Column headers */}
            <div className="px-5 py-2.5 bg-slate-50 border-b border-slate-100 flex items-center gap-4">
              <div className="h-3 w-24 bg-slate-100 rounded" />
              <div className="h-3 w-16 bg-slate-100 rounded hidden sm:block" />
              <div className="h-3 w-14 bg-slate-100 rounded" />
              <div className="h-3 w-20 bg-slate-100 rounded hidden md:block ml-auto" />
            </div>
            {/* Rows */}
            <div className="divide-y divide-slate-100">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="flex items-center gap-4 px-5 py-3.5">
                  <div className="w-9 h-9 rounded-xl bg-slate-100 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="h-4 w-28 bg-slate-200 rounded mb-1.5" />
                    <div className="h-3 w-40 bg-slate-100 rounded" />
                  </div>
                  <div className="hidden sm:block h-3 w-16 bg-slate-100 rounded" />
                  <div className="h-5 w-16 bg-slate-100 rounded-full" />
                  <div className="hidden md:flex flex-1 items-center gap-2 max-w-[100px]">
                    <div className="flex-1 h-2 bg-slate-100 rounded-full" />
                    <div className="h-3 w-8 bg-slate-100 rounded" />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Timeline skeleton — 4 items */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <div className="h-4 w-28 bg-slate-200 rounded mb-1.5" />
                <div className="h-3 w-52 bg-slate-100 rounded" />
              </div>
              <div className="h-4 w-14 bg-slate-100 rounded" />
            </div>
            <div className="px-5 py-4">
              <div className="relative">
                {/* Vertical line */}
                <div className="absolute left-3.5 top-0 bottom-0 w-px bg-slate-100" />
                <div className="space-y-5">
                  {[...Array(4)].map((_, i) => (
                    <div key={i} className="flex gap-4">
                      <div className="w-7 h-7 rounded-full bg-slate-200 flex-shrink-0 z-10 relative" />
                      <div
                        className={`flex-1 rounded-lg p-3 ${i === 0 ? "bg-indigo-50/60" : "bg-slate-50"}`}
                      >
                        <div className="h-4 w-4/5 bg-slate-200 rounded mb-2" />
                        <div className="h-3 w-3/5 bg-slate-100 rounded mb-2" />
                        <div className="flex items-center gap-2">
                          <div className="h-4 w-16 bg-slate-200 rounded-full" />
                          <div className="h-3 w-12 bg-slate-100 rounded" />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* ── Right column (1/3) ─────────────────────────────────────────── */}
        <div className="flex flex-col gap-5">

          {/* Donut skeleton */}
          <div className="bg-white rounded-xl shadow-sm p-5">
            <div className="h-4 w-32 bg-slate-200 rounded mb-1.5" />
            <div className="h-3 w-40 bg-slate-100 rounded mb-5" />
            {/* Circle */}
            <div className="flex flex-col items-center gap-4">
              <div className="w-[140px] h-[140px] rounded-full bg-slate-100 ring-[18px] ring-slate-200" />
              {/* Legend lines */}
              <div className="w-full space-y-2">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <div className="w-2.5 h-2.5 rounded-full bg-slate-200" />
                      <div className="h-3 w-14 bg-slate-100 rounded" />
                    </div>
                    <div className="h-3 w-8 bg-slate-200 rounded" />
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Action skeleton cards — 3 items */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <div className="h-4 w-36 bg-slate-200 rounded mb-1.5" />
              <div className="h-3 w-24 bg-slate-100 rounded" />
            </div>
            <div className="divide-y divide-slate-100">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="flex items-center gap-3 px-5 py-3.5">
                  <div className="w-6 h-6 rounded-full bg-slate-200 flex-shrink-0" />
                  <div className="flex-1 h-4 bg-slate-100 rounded" />
                  <div className="w-4 h-4 bg-slate-100 rounded" />
                </div>
              ))}
            </div>
          </div>

          {/* Agents skeleton */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <div className="h-4 w-28 bg-slate-200 rounded mb-1.5" />
              <div className="h-3 w-40 bg-slate-100 rounded" />
            </div>
            <div className="divide-y divide-slate-100">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="flex items-center justify-between px-5 py-2.5">
                  <div className="flex items-center gap-2.5">
                    <div className="w-2 h-2 rounded-full bg-slate-200" />
                    <div>
                      <div className="h-3 w-14 bg-slate-200 rounded mb-1" />
                      <div className="h-2.5 w-20 bg-slate-100 rounded" />
                    </div>
                  </div>
                  <div className="h-5 w-14 bg-slate-100 rounded-full" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
