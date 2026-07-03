// État de chargement de la page de suivi (Suspense fallback pendant l'appel
// Admin API / base). Squelette léger, mobile d'abord.
export default function Loading() {
  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto w-full max-w-xl px-4 py-8 sm:py-12" aria-busy="true" aria-live="polite">
        <span className="sr-only">Chargement du suivi de commande…</span>

        {/* En-tête */}
        <div className="mb-6 flex flex-col items-center">
          <div className="mb-4 h-12 w-12 animate-pulse rounded-2xl bg-slate-200" />
          <div className="h-6 w-56 animate-pulse rounded bg-slate-200" />
          <div className="mt-2 h-4 w-28 animate-pulse rounded bg-slate-100" />
        </div>

        {/* Carte statut */}
        <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="space-y-2">
              <div className="h-3 w-20 animate-pulse rounded bg-slate-100" />
              <div className="h-5 w-32 animate-pulse rounded bg-slate-200" />
            </div>
            <div className="space-y-2">
              <div className="h-3 w-24 animate-pulse rounded bg-slate-100" />
              <div className="h-5 w-40 animate-pulse rounded bg-slate-200" />
            </div>
          </div>
        </div>

        {/* Chronologie */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-5 h-4 w-24 animate-pulse rounded bg-slate-200" />
          <div className="space-y-6">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="flex items-center gap-4">
                <div className="h-9 w-9 flex-shrink-0 animate-pulse rounded-full bg-slate-200" />
                <div className="flex-1 space-y-2">
                  <div className="h-4 w-28 animate-pulse rounded bg-slate-200" />
                  <div className="h-3 w-48 animate-pulse rounded bg-slate-100" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
