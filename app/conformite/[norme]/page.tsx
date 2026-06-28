import Link from "next/link";
import { notFound } from "next/navigation";
import { loadNormes, slugFor, normeBySlug } from "../data";

// Page SEO programmatique : une page par norme, générée au build depuis la base vérifiée.
// Cible une requête à forte intention ("e-facturation obligatoire", "NIS2 suis-je concerné", etc.).

export async function generateStaticParams() {
  return loadNormes().map((n) => ({ norme: slugFor(n) }));
}

export async function generateMetadata({ params }: { params: Promise<{ norme: string }> }) {
  const { norme } = await params;
  const n = normeBySlug(norme);
  if (!n) return { title: "Conformité — Caelum" };
  return {
    title: `${n.norme} — êtes-vous concerné ? | Caelum`,
    description: n.changement.slice(0, 155),
  };
}

export default async function NormePage({ params }: { params: Promise<{ norme: string }> }) {
  const { norme } = await params;
  const n = normeBySlug(norme);
  if (!n) notFound();

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
          <span className="inline-block px-3 py-1 rounded-full bg-red-500/20 border border-red-400/30 text-red-200 text-xs font-medium mb-4">
            {n.echeance}
          </span>
          <h1 className="text-3xl md:text-4xl font-bold">{n.norme}</h1>
          <p className="mt-3 text-slate-300 max-w-2xl">{n.changement}</p>
        </div>
      </section>

      <article className="max-w-4xl mx-auto px-6 py-12 space-y-8">
        <div className="rounded-2xl border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-900">Qui est concerné ?</h2>
          <p className="mt-2 text-slate-700 leading-relaxed">{n.concernes}</p>
        </div>

        <div className="rounded-2xl border border-red-200 bg-red-50 p-6">
          <h2 className="text-lg font-bold text-red-900">⚠️ La sanction</h2>
          <p className="mt-2 text-red-800 leading-relaxed">{n.sanction}</p>
        </div>

        {n.solution_caelum && (
          <div className="rounded-2xl border border-indigo-200 bg-indigo-50 p-6">
            <h2 className="text-lg font-bold text-indigo-900">La solution avec Caelum</h2>
            <p className="mt-2 text-indigo-900/90 leading-relaxed">{n.solution_caelum}</p>
          </div>
        )}

        <p className="text-sm text-slate-500">⚖️ {n.reference_legale}</p>

        {n.sources && n.sources.length > 0 && (
          <div className="text-sm">
            <span className="font-semibold text-slate-600">Sources : </span>
            {n.sources.map((s, i) => (
              <span key={i}>
                {i > 0 ? " · " : ""}
                <a href={s.url} target="_blank" rel="noopener noreferrer" className="text-indigo-700 hover:underline">
                  {s.intitule}
                </a>
                {s.type === "officiel" && <span className="text-emerald-700 font-medium"> [officiel]</span>}
              </span>
            ))}
          </div>
        )}

        {/* CTA */}
        <div className="rounded-2xl bg-indigo-600 text-white p-7 text-center">
          <h2 className="text-xl font-bold">Êtes-vous concerné ? Vérifiez en 1 minute.</h2>
          <p className="text-indigo-100 mt-2 text-sm">
            Notre simulateur vous dit exactement ce qui s&apos;applique à votre entreprise — et on s&apos;occupe de la mise en règle.
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
      </article>
    </main>
  );
}
