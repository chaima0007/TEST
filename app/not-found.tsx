import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-indigo-100 mb-6">
          <span className="text-4xl">🔍</span>
        </div>
        <h1 className="text-6xl font-bold text-slate-900 mb-2">404</h1>
        <h2 className="text-xl font-semibold text-slate-700 mb-3">Page introuvable</h2>
        <p className="text-slate-500 text-sm mb-8 leading-relaxed">
          La page que vous recherchez n&apos;existe pas ou a été déplacée.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link
            href="/dashboard"
            className="bg-indigo-600 text-white px-6 py-2.5 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors"
          >
            Tableau de bord
          </Link>
          <Link
            href="/"
            className="border border-slate-200 text-slate-700 px-6 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-100 transition-colors"
          >
            Accueil
          </Link>
        </div>
      </div>
    </div>
  );
}
