import Link from "next/link";

export const metadata = { title: "Politique de confidentialité (RGPD) — Caelum" };

export default function Confidentialite() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-violet-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/" className="text-sm text-slate-500 hover:text-slate-900">← Retour</Link>
        </div>
      </header>
      <article className="max-w-3xl mx-auto px-6 py-14 prose prose-slate">
        <h1 className="text-3xl font-bold tracking-tight">Politique de confidentialité (RGPD)</h1>
        <div className="mt-6 space-y-5 text-slate-600 leading-relaxed text-sm">
          <p>Caelum respecte le Règlement Général sur la Protection des Données (RGPD).</p>
          <p><strong>Données collectées</strong> — Via le formulaire de contact : nom, email, organisation, et le message que vous envoyez. Aucune donnée n'est collectée à votre insu.</p>
          <p><strong>Finalité</strong> — Ces données servent uniquement à vous recontacter au sujet de votre demande. Elles ne sont ni vendues, ni cédées à des tiers.</p>
          <p><strong>Conservation</strong> — Vos données sont conservées le temps nécessaire au traitement de votre demande, puis supprimées sur simple demande.</p>
          <p><strong>Vos droits</strong> — Vous pouvez à tout moment demander l'accès, la rectification ou la suppression de vos données en écrivant à [email]. Vous pouvez aussi introduire une réclamation auprès de l'Autorité de protection des données (Belgique).</p>
          <p><strong>Cookies</strong> — Ce site utilise un minimum de cookies techniques nécessaires à son fonctionnement et à la mesure d'audience.</p>
        </div>
        <p className="mt-10 text-xs text-slate-400">Dernière mise à jour : 2026. Document à faire valider par un juriste pour une conformité complète.</p>
      </article>
    </main>
  );
}
