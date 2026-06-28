import Link from "next/link";

export const metadata = {
  title: "Mentions légales — La Loi Avec Moi",
  description: "Informations légales de l'éditeur du site La Loi Avec Moi.",
};

export default function MentionsLegalesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">La Loi Avec Moi</Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">← Accueil</Link>
        </div>
      </header>

      <article className="max-w-3xl mx-auto px-6 py-12 space-y-6">
        <h1 className="text-3xl font-bold">Mentions légales</h1>

        <section>
          <h2 className="text-lg font-bold">Éditeur du site</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            [Nom de l'éditeur / société] · [Forme juridique] · [Adresse]<br />
            Numéro d'entreprise (BCE) : [à compléter] · TVA : [à compléter]<br />
            Contact : contact@laloiavecmoi.be
          </p>
          <p className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 mt-2">
            ⚠️ Champs à compléter par l'éditeur avant la mise en ligne (identité légale réelle).
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Hébergeur</h2>
          <p className="text-slate-700 text-sm mt-2">[Nom et coordonnées de l'hébergeur]</p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Objet du site</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            La Loi Avec Moi fournit une information juridique générale, claire et sourcée, destinée au grand public.
            Elle ne constitue pas un conseil juridique individualisé et ne remplace pas l'avis d'un professionnel
            (avocat, notaire…). Chaque réponse cite ses sources officielles et sa date de vérification.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Propriété intellectuelle</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            Les contenus rédigés par La Loi Avec Moi sont protégés. Les textes légaux et sources officielles
            cités appartiennent à leurs autorités respectives et sont liés vers leur source.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Liens</h2>
          <p className="text-slate-700 text-sm mt-2">
            Voir aussi notre <Link href="/confidentialite" className="text-indigo-700 hover:underline">politique de confidentialité</Link> et
            notre <Link href="/accessibilite" className="text-indigo-700 hover:underline">déclaration d'accessibilité</Link>.
          </p>
        </section>
      </article>
    </main>
  );
}
