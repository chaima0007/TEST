import Link from "next/link";
import { notFound } from "next/navigation";
import { loadNormes, slugFor } from "../../data";
import { SECTEURS, secteurBySlug } from "../../secteurs";

// Page SEO longue traîne : conformité par secteur d'activité.
// Génère une page par secteur, en piochant les normes pertinentes dans la base vérifiée.

export async function generateStaticParams() {
  return SECTEURS.map((s) => ({ secteur: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ secteur: string }> }) {
  const { secteur } = await params;
  const s = secteurBySlug(secteur);
  if (!s) return { title: "Conformité par secteur — Caelum" };
  return {
    title: `Conformité 2026 : ${s.nom} — quelles obligations ? | Caelum`,
    description: s.intro.slice(0, 155),
  };
}

export default async function SecteurPage({ params }: { params: Promise<{ secteur: string }> }) {
  const { secteur } = await params;
  const s = secteurBySlug(secteur);
  if (!s) notFound();

  const toutes = loadNormes();
  const normes = s.normesIds.map((id) => toutes.find((n) => n.id === id)).filter((n) => n !== undefined);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/conformite" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            ← Toutes les normes
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <span className="inline-block px-3 py-1 rounded-full bg-white/10 border border-white/15 text-slate-200 text-xs font-medium mb-4">
            Conformité par secteur
          </span>
          <h1 className="text-3xl md:text-4xl font-bold">{s.nom} : vos obligations 2026</h1>
          <p className="mt-3 text-slate-300 max-w-2xl">{s.intro}</p>
        </div>
      </section>

      <article className="max-w-4xl mx-auto px-6 py-12">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 mb-8">
          <p className="text-amber-900 text-sm">
            <strong>Bon à savoir :</strong> {s.note}
          </p>
        </div>

        <h2 className="text-xl font-bold text-slate-900 mb-4">Les normes qui vous concernent</h2>
        <div className="grid gap-4">
          {normes.map((n) => (
            <Link
              key={n!.id}
              href={`/conformite/${slugFor(n!)}`}
              className="rounded-2xl border border-slate-200 p-5 hover:border-indigo-400 hover:shadow-sm transition-all"
            >
              <div className="flex items-start justify-between gap-3">
                <h3 className="font-semibold text-lg text-slate-900">{n!.norme}</h3>
                <span className="text-xs whitespace-nowrap px-2 py-1 rounded-full bg-slate-100 text-slate-600">
                  {n!.echeance}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-600">{n!.changement}</p>
              <p className="mt-2 text-sm font-medium text-red-700">⚠️ {n!.sanction}</p>
              <span className="inline-block mt-2 text-sm font-semibold text-indigo-700">En savoir plus →</span>
            </Link>
          ))}
        </div>

        <div className="mt-10 rounded-2xl bg-indigo-600 text-white p-7 text-center">
          <h2 className="text-xl font-bold">Vérifiez ce qui s&apos;applique à votre entreprise</h2>
          <p className="text-indigo-100 mt-2 text-sm">
            Notre simulateur vous donne la liste exacte en 1 minute — et on s&apos;occupe de la mise en conformité.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center mt-5">
            <Link
              href="/conformite-2026"
              className="bg-white text-indigo-700 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-50 transition-colors"
            >
              Suis-je concerné ?
            </Link>
            <Link
              href="/offres-conformite"
              className="border border-white/40 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/10 transition-colors"
            >
              Voir les offres
            </Link>
          </div>
        </div>

        {/* Maillage interne SEO : autres secteurs */}
        <div className="mt-10">
          <h2 className="text-sm font-semibold text-slate-500 mb-3">Autres secteurs</h2>
          <div className="flex flex-wrap gap-2">
            {SECTEURS.filter((x) => x.slug !== s.slug).map((x) => (
              <Link
                key={x.slug}
                href={`/conformite/secteur/${x.slug}`}
                className="text-sm px-3 py-1.5 rounded-full border border-slate-200 hover:border-indigo-400 hover:text-indigo-700"
              >
                {x.nom}
              </Link>
            ))}
          </div>
        </div>
      </article>
    </main>
  );
}
