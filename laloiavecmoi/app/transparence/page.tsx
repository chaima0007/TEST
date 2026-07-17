import Link from "next/link";
import fs from "node:fs";
import path from "node:path";

// Page « Nos sources & méthode » — La Loi Avec Moi. Statistiques calculées au build depuis
// la base vérifiée (data/belgium) + liste des sources officielles (trusted_sources.json).
// But : rendre la fiabilité VISIBLE — la confiance vérifiable est notre différence.

type Fait = { reference_legale?: string; sources?: { type?: string }[]; date_verification?: string };
type Module = { titre?: string; faits?: Fait[] };

function stats() {
  const dir = path.join(process.cwd(), "data", "belgium");
  let modules: Module[] = [];
  try {
    modules = fs
      .readdirSync(dir)
      .filter((f) => f.endsWith(".json") && !f.startsWith("_"))
      .map((f) => {
        try {
          return JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8")) as Module;
        } catch {
          return null;
        }
      })
      .filter((m): m is Module => !!m && Array.isArray(m.faits) && m.faits.length > 0);
  } catch {
    modules = [];
  }

  const faits = modules.flatMap((m) => m.faits || []);
  const total = faits.length;
  const avecLoi = faits.filter((f) => (f.reference_legale || "").trim().length > 0).length;
  const avecSourceOff = faits.filter((f) => (f.sources || []).some((s) => s.type === "officiel")).length;
  const avecDate = faits.filter((f) => (f.date_verification || "").trim().length > 0).length;
  const pct = (n: number) => (total ? Math.round((n / total) * 100) : 0);

  return {
    domaines: modules.length,
    total,
    pctLoi: pct(avecLoi),
    pctSource: pct(avecSourceOff),
    pctDate: pct(avecDate),
  };
}

function sourcesOfficielles(): string[] {
  try {
    const p = path.join(process.cwd(), "data", "governance", "trusted_sources.json");
    const d = JSON.parse(fs.readFileSync(p, "utf-8"));
    return Array.isArray(d.tier1_officiel) ? d.tier1_officiel : [];
  } catch {
    return [];
  }
}

export const metadata = {
  title: "Nos sources & méthode — La Loi Avec Moi",
  description:
    "Comment nous garantissons la fiabilité : chaque réponse cite une loi réelle, une source officielle et une date de vérification.",
};

export default function TransparencePage() {
  const s = stats();
  const sources = sourcesOfficielles();

  const cartes = [
    { v: `${s.domaines}`, l: "domaines couverts" },
    { v: `${s.total}`, l: "réponses vérifiées" },
    { v: `${s.pctLoi}%`, l: "citent une loi réelle" },
    { v: `${s.pctSource}%`, l: "avec source officielle" },
  ];

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

      <section className="bg-gradient-to-b from-blue-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Nos sources & notre méthode</h1>
          <p className="mt-3 text-blue-100 max-w-2xl">
            Ici, rien n&apos;est inventé. Chaque réponse s&apos;appuie sur une loi réelle en vigueur, une source
            officielle et une date de vérification. La confiance, ça se prouve.
          </p>
        </div>
      </section>

      {/* Chiffres */}
      <section className="max-w-4xl mx-auto px-6 -mt-8">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {cartes.map((c) => (
            <div key={c.l} className="rounded-2xl bg-white border border-slate-200 p-5 text-center shadow-sm">
              <div className="text-3xl font-black text-indigo-700">{c.v}</div>
              <div className="text-xs text-slate-600 mt-1">{c.l}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Méthode */}
      <section className="max-w-4xl mx-auto px-6 py-12">
        <h2 className="text-2xl font-bold">Comment on vérifie chaque réponse</h2>
        <ol className="mt-5 space-y-3">
          {[
            "Chaque réponse est reliée à une loi, un code ou un arrêté réellement en vigueur (référence légale).",
            "Chaque réponse cite au moins une source officielle (administration, texte légal, service public).",
            "Chaque réponse porte une date de vérification, pour que vous sachiez de quand elle date.",
            "Un double contrôle automatique vérifie le sourçage AVANT et APRÈS chaque mise à jour.",
            "Quand une information change souvent (montants indexés, dates), on le dit et on renvoie à la source.",
          ].map((t, i) => (
            <li key={i} className="flex items-start gap-3 rounded-xl border border-slate-200 p-4">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-600 text-white text-sm font-bold flex items-center justify-center">
                {i + 1}
              </span>
              <span className="text-slate-700 text-sm leading-relaxed">{t}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* Sources officielles */}
      <section className="max-w-4xl mx-auto px-6 pb-12">
        <h2 className="text-2xl font-bold">Nos sources officielles de confiance</h2>
        <p className="text-slate-600 text-sm mt-1 mb-4">
          {sources.length} domaines officiels figurent dans notre liste blanche (administrations, textes légaux,
          services publics belges et européens).
        </p>
        <div className="flex flex-wrap gap-2">
          {sources.map((d) => (
            <span key={d} className="text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              {d}
            </span>
          ))}
        </div>
      </section>

      {/* Honnêteté */}
      <section className="max-w-4xl mx-auto px-6 pb-16">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h2 className="font-semibold text-amber-900">En toute honnêteté</h2>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            Ce site donne une information juridique générale, claire et sourcée — il ne remplace pas un conseil
            individualisé par un professionnel (avocat, notaire…). Les lois évoluent : l&apos;information est à jour
            à la date indiquée sur chaque réponse, et nous renvoyons toujours à la source officielle pour vérifier.
          </p>
        </div>
      </section>
    </main>
  );
}
