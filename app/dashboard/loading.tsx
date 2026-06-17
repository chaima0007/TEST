export default function DashboardLoading() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Header skeleton */}
      <div>
        <div className="h-8 w-48 bg-slate-200 rounded-lg mb-2"></div>
        <div className="h-4 w-72 bg-slate-100 rounded"></div>
      </div>

      {/* Stats skeleton */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl border border-slate-200 p-5">
            <div className="w-10 h-10 rounded-lg bg-slate-100 mb-3"></div>
            <div className="h-7 w-16 bg-slate-200 rounded mb-1"></div>
            <div className="h-3 w-24 bg-slate-100 rounded"></div>
          </div>
        ))}
      </div>

      {/* Two column skeleton */}
      <div className="grid lg:grid-cols-2 gap-6">
        {[...Array(2)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl border border-slate-200">
            <div className="px-5 py-4 border-b border-slate-100">
              <div className="h-5 w-32 bg-slate-200 rounded"></div>
            </div>
            <div className="divide-y divide-slate-100">
              {[...Array(3)].map((_, j) => (
                <div key={j} className="px-5 py-3.5 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-slate-100 flex-shrink-0"></div>
                  <div className="flex-1">
                    <div className="h-4 w-28 bg-slate-200 rounded mb-1.5"></div>
                    <div className="h-3 w-20 bg-slate-100 rounded"></div>
                  </div>
                  <div className="h-5 w-16 bg-slate-100 rounded-full"></div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
