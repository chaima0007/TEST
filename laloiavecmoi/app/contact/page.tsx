import Link from "next/link";

// Page contact du site indépendant « La Loi Avec Moi ».
// Adresse e-mail à personnaliser (placeholder) — à remplacer par ton adresse définitive.

export default function ContactPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white">
        <div className="relative max-w-3xl mx-auto px-6 py-20 text-center">
          <Link href="/" className="inline-block text-blue-200 hover:text-white text-sm font-medium mb-6">
            ← La Loi Avec Moi
          </Link>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">Nous contacter</h1>
          <p className="mt-5 text-lg text-blue-100 leading-relaxed">
            Une question, une suggestion, un partenariat&nbsp;? Écrivez-nous.
          </p>
        </div>
      </section>

      <section className="px-6 py-16 max-w-2xl mx-auto">
        <div className="rounded-2xl border border-slate-200 p-8 text-center">
          <p className="text-slate-700 leading-relaxed">
            Pour toute demande, contactez-nous par e-mail&nbsp;:
          </p>
          <a
            href="mailto:contact@laloiavecmoi.be"
            className="inline-block mt-4 text-xl font-bold text-blue-700 hover:text-blue-900"
          >
            contact@laloiavecmoi.be
          </a>
          <p className="text-slate-400 text-sm mt-6 leading-relaxed">
            (Adresse à personnaliser une fois ton nom de domaine et ta boîte e-mail configurés.)
          </p>
        </div>

        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 mt-6">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Nous fournissons de l&apos;information générale, pas un conseil juridique personnalisé.
            En cas d&apos;urgence, appelez le <strong>112</strong>.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/" className="hover:text-slate-900">← Accueil</Link>
      </footer>
    </main>
  );
}
