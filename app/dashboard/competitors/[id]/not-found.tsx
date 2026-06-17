import Link from "next/link";

export default function CompetitorNotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-slate-100 mb-6">
        <span className="text-4xl">🏢</span>
      </div>
      <h2 className="text-2xl font-bold text-slate-900 mb-2">Concurrent introuvable</h2>
      <p className="text-slate-500 text-sm mb-8 max-w-sm leading-relaxed">
        Ce concurrent n&apos;existe pas ou a été supprimé. Retournez à la liste pour voir tous vos concurrents.
      </p>
      <Link
        href="/dashboard/competitors"
        className="bg-indigo-600 text-white px-6 py-2.5 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors"
      >
        ← Retour aux concurrents
      </Link>
    </div>
  );
}
