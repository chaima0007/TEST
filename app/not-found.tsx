import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4 relative overflow-hidden">
      {/* Dot texture background */}
      <div
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='2' cy='2' r='1.5' fill='%236366f1' fill-opacity='0.25'/%3E%3C/svg%3E")`,
          backgroundSize: "20px 20px",
        }}
      />

      <div className="relative z-10 text-center max-w-lg">
        {/* Big 404 gradient */}
        <div
          className="text-[9rem] font-black leading-none mb-4 select-none"
          style={{
            background: "linear-gradient(135deg, #4338CA 0%, #7C3AED 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
          }}
        >
          404
        </div>

        {/* Broken magnifier illustration */}
        <div className="flex justify-center mb-6">
          <svg
            width="72"
            height="72"
            viewBox="0 0 72 72"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <circle cx="30" cy="30" r="18" stroke="#6366f1" strokeWidth="4" fill="#EEF2FF" />
            <circle cx="30" cy="30" r="10" stroke="#a5b4fc" strokeWidth="2" fill="none" strokeDasharray="4 3" />
            <line x1="43" y1="43" x2="58" y2="58" stroke="#7C3AED" strokeWidth="4" strokeLinecap="round" />
            {/* Crack lines */}
            <line x1="55" y1="52" x2="60" y2="47" stroke="#c4b5fd" strokeWidth="2" strokeLinecap="round" />
            <line x1="52" y1="58" x2="57" y2="62" stroke="#c4b5fd" strokeWidth="2" strokeLinecap="round" />
            {/* X mark inside circle */}
            <line x1="24" y1="24" x2="36" y2="36" stroke="#818cf8" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="36" y1="24" x2="24" y2="36" stroke="#818cf8" strokeWidth="2.5" strokeLinecap="round" />
          </svg>
        </div>

        {/* Titles */}
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Page introuvable</h1>
        <p className="text-slate-500 text-base mb-8 leading-relaxed">
          Cette page n&apos;existe pas ou a été déplacée.
        </p>

        {/* Quick navigation buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center mb-6">
          <Link
            href="/dashboard"
            className="bg-indigo-600 text-white px-5 py-2.5 rounded-xl text-sm font-semibold shadow-md shadow-indigo-200 hover:bg-indigo-700 hover:shadow-indigo-300 transition-all"
          >
            Tableau de bord
          </Link>
          <Link
            href="/alerts"
            className="border border-indigo-200 text-indigo-700 bg-indigo-50 px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-indigo-100 transition-all"
          >
            Alertes
          </Link>
          <Link
            href="/reports"
            className="border border-indigo-200 text-indigo-700 bg-indigo-50 px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-indigo-100 transition-all"
          >
            Rapports
          </Link>
        </div>

        {/* Back home link */}
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-indigo-600 transition-colors"
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 14 14"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path
              d="M9 2L4 7L9 12"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          Retour à l&apos;accueil
        </Link>
      </div>
    </div>
  );
}
