import Link from "next/link";
import { loadNormes, slugFor } from "./data";
import { SECTEURS } from "./secteurs";

export const metadata = {
  title: "Conformité 2026 des entreprises — toutes les normes | Caelum",
  description:
    "E-facturation, NIS2, RGPD, CSRD, CSDDD, lanceurs d'alerte : ce qui change, qui est concerné, les sanctions. Vérifiez et mettez-vous en règle avec Caelum.",
};

export default function ConformiteHubPage() {
  const normes = loadNormes();

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link
            href="/conformite-2026"
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors"
          >
            Suis-je concerné ?
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Les normes 2026 des entreprises</h1>
          <p className="mt-3 text-slate-300 max-w-2xl">
            Ce qui change, qui est concerné, les sanctions chiffrées et les échéances. Chaque fiche est sourcée
            officiellement. La loi a changé — la solution, c&apos;est nous.
          </p>
        </div>
      </section>

      <section className="max-w-5xl mx-auto px-6 py-12 grid gap-4 sm:grid-cols-2">
        {normes.map((n) => (
          <Link
            key={n.id}
            href={`/conformite/${slugFor(n)}`}
            className="rounded-2xl border border-slate-200 p-6 hover:border-indigo-400 hover:shadow-sm transition-all"
          >
            <div className="flex items-start justify-between gap-3">
              <h2 className="font-bold text-lg text-slate-900">{n.norme}</h2>
              <span className="text-xs whitespace-nowrap px-2 py-1 rounded-full bg-slate-100 text-slate-600">
                {n.echeance}
              </span>
            </div>
            <p className="mt-2 text-sm text-slate-600 line-clamp-3">{n.changement}</p>
            <span className="inline-block mt-3 text-sm font-semibold text-indigo-700">En savoir plus →</span>
          </Link>
        ))}
      </section>

      <section className="max-w-5xl mx-auto px-6 pb-16">
        <h2 className="text-2xl font-bold">Et selon votre secteur ?</h2>
        <p className="text-slate-600 mt-1 mb-5 text-sm">Les obligations qui comptent vraiment pour votre métier.</p>
        <div className="flex flex-wrap gap-2">
          {SECTEURS.map((s) => (
            <Link
              key={s.slug}
              href={`/conformite/secteur/${s.slug}`}
              className="text-sm px-3 py-1.5 rounded-full border border-slate-200 hover:border-indigo-400 hover:text-indigo-700"
            >
              {s.nom}
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
