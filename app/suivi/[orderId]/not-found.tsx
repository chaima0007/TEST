import Link from "next/link";

// État « commande introuvable » de la page de suivi (déclenché par notFound()
// quand l'orderId est invalide ou absent côté Admin API).
export default function OrderNotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md text-center">
        <div className="mx-auto mb-6 inline-flex h-20 w-20 items-center justify-center rounded-2xl bg-slate-100">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M3 7l9-4 9 4v10l-9 4-9-4V7z" />
            <path d="M3 7l9 4 9-4M12 21V11" />
            <line x1="8" y1="5" x2="16" y2="9.5" />
          </svg>
        </div>
        <h1 className="mb-2 text-2xl font-bold text-slate-900">Commande introuvable</h1>
        <p className="mb-8 text-sm leading-relaxed text-slate-500">
          Nous n&apos;avons pas trouvé de commande correspondant à ce lien. Vérifiez le lien reçu par
          e-mail, ou contactez-nous : nous vous répondons en moins de 24 h.
        </p>
        <Link
          href="/"
          className="inline-flex items-center justify-center rounded-lg bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-indigo-700"
        >
          Retour à l&apos;accueil
        </Link>
      </div>
    </main>
  );
}
