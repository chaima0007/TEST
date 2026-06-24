import Link from "next/link";

export const metadata = { title: "Mentions légales — Caelum" };

export default function MentionsLegales() {
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
        <h1 className="text-3xl font-bold tracking-tight">Mentions légales</h1>
        <div className="mt-6 space-y-5 text-slate-600 leading-relaxed text-sm">
          <p><strong>Éditeur du site</strong> — [Nom de l'entreprise / indépendant], [adresse], Belgique. Numéro d'entreprise (BCE) : [à compléter]. Contact : [email].</p>
          <p><strong>Responsable de la publication</strong> — [Votre nom].</p>
          <p><strong>Hébergement</strong> — Vercel Inc., 340 S Lemon Ave #4133, Walnut, CA 91789, USA — vercel.com.</p>
          <p><strong>Propriété intellectuelle</strong> — L'ensemble du contenu de ce site (textes, visuels, code) est la propriété de Caelum, sauf mention contraire. Toute reproduction sans autorisation est interdite.</p>
          <p><strong>Responsabilité</strong> — Caelum s'efforce de fournir des informations exactes, mais ne saurait être tenu responsable d'erreurs ou d'omissions. Les informations à caractère juridique ou fiscal éventuellement présentes sont fournies à titre informatif et ne constituent pas un conseil professionnel.</p>
        </div>
        <p className="mt-10 text-xs text-slate-400">Dernière mise à jour : 2026. Document à faire valider par un juriste pour une conformité complète.</p>
      </article>
    </main>
  );
}
