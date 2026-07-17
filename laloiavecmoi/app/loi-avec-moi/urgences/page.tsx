import Link from "next/link";
import fs from "node:fs";
import path from "node:path";

// Page « Urgences & délais » — La Loi Avec Moi. Regroupe automatiquement toutes les réponses
// porteuses d'un délai critique (champ alerte_delai) depuis la base vérifiée + numéros d'urgence.
// Rendu statique (données figées au build).

type Fait = { id: string; question: string; alerte_delai?: string };
type Module = { module: string; titre: string; faits?: Fait[] };

function delaisCritiques(): { module: string; titre: string; id: string; question: string; delai: string }[] {
  const dir = path.join(process.cwd(), "data", "belgium");
  const out: { module: string; titre: string; id: string; question: string; delai: string }[] = [];
  try {
    for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".json") && !x.startsWith("_")).sort()) {
      try {
        const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8")) as Module;
        for (const fait of d.faits || []) {
          if ((fait.alerte_delai || "").trim()) {
            out.push({ module: d.module, titre: d.titre, id: fait.id, question: fait.question, delai: fait.alerte_delai! });
          }
        }
      } catch {
        /* ignore */
      }
    }
  } catch {
    /* ignore */
  }
  return out;
}

const numeros = [
  { n: "112", t: "Urgence vitale (secours, pompiers, ambulance)" },
  { n: "101", t: "Police" },
  { n: "103", t: "Écoute-Enfants" },
  { n: "1712", t: "Violences (conjugales, familiales, maltraitance)" },
  { n: "107", t: "Télé-Accueil (détresse, écoute 24h/24)" },
  { n: "078 170 170", t: "Card Stop (bloquer une carte bancaire)" },
  { n: "00800 2123 2123", t: "DOC STOP (bloquer un document d'identité)" },
];

export const dynamic = "force-static";

export const metadata = {
  title: "Urgences & délais — La Loi Avec Moi",
  description:
    "Les situations où un délai compte (saisie, amende, recours, sinistre…) et les numéros d'urgence. Agissez à temps.",
};

export default function UrgencesPage() {
  const delais = delaisCritiques();

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">
            La Loi Avec Moi
          </Link>
          <Link href="/base-juridique" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            Toutes mes réponses →
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-rose-700 to-rose-900 text-white py-14 px-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Urgences & délais</h1>
          <p className="mt-3 text-rose-100 max-w-2xl">
            Certaines situations n&apos;attendent pas : un délai dépassé peut vous coûter vos droits.
            Voici les numéros d&apos;urgence et toutes les réponses où il faut agir vite.
          </p>
        </div>
      </section>

      {/* Numéros d'urgence */}
      <section className="max-w-4xl mx-auto px-6 -mt-8">
        <div className="grid sm:grid-cols-2 gap-3">
          {numeros.map((x) => (
            <div key={x.n} className="rounded-xl bg-white border-2 border-rose-200 p-4 shadow-sm flex items-baseline gap-3">
              <span className="text-xl font-black text-rose-600 whitespace-nowrap">{x.n}</span>
              <span className="text-sm text-slate-700">{x.t}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Délais critiques */}
      <section className="max-w-4xl mx-auto px-6 py-12">
        <h2 className="text-2xl font-bold">Quand un délai compte ({delais.length})</h2>
        <p className="text-slate-600 text-sm mt-1 mb-6">Cliquez pour voir la réponse complète et les démarches.</p>
        <div className="grid gap-3">
          {delais.map((d) => (
            <Link
              key={`${d.module}-${d.id}`}
              href={`/loi/${d.module}#${d.id}`}
              className="block rounded-xl border border-slate-200 p-4 hover:border-rose-400 hover:shadow-sm transition-all"
            >
              <span className="font-medium text-slate-900">{d.question}</span>
              <span className="block text-sm rounded-lg bg-rose-50 border border-rose-200 text-rose-800 px-3 py-2 mt-2">
                ⏱ {d.delai}
              </span>
              <span className="block text-xs text-slate-500 mt-1">{d.titre} →</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 pb-16">
        <p className="text-xs text-slate-400 border-t border-slate-100 pt-4">
          Information générale, à jour à la date indiquée. En cas de danger immédiat, appelez le 112. © La Loi Avec Moi.
        </p>
      </section>
    </main>
  );
}
