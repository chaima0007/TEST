import Link from "next/link";
import fs from "node:fs";
import path from "node:path";
import { notFound } from "next/navigation";

// Page SEO par domaine juridique — La Loi Avec Moi. Une URL indexable par domaine,
// générée au build depuis data/belgium (base vérifiée). Moteur d'acquisition organique.

type Source = { type?: string; url?: string; intitule?: string };
type Contact = { nom?: string; numero?: string; lien?: string; pour?: string };
type Fait = {
  id: string;
  question: string;
  reponse: string;
  reference_legale?: string;
  alerte_delai?: string;
  contacts?: Contact[];
  sources?: Source[];
  date_verification?: string;
};
type Module = { module: string; titre: string; faits: Fait[] };

function chargerModules(): Module[] {
  const dir = path.join(process.cwd(), "data", "belgium");
  try {
    return fs
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
    return [];
  }
}

function moduleParSlug(slug: string): Module | undefined {
  return chargerModules().find((m) => m.module === slug);
}

export async function generateStaticParams() {
  return chargerModules().map((m) => ({ domaine: m.module }));
}

export async function generateMetadata({ params }: { params: Promise<{ domaine: string }> }) {
  const { domaine } = await params;
  const m = moduleParSlug(domaine);
  if (!m) return { title: "Domaine juridique — La Loi Avec Moi" };
  return {
    title: `${m.titre} — vos droits expliqués | La Loi Avec Moi`,
    description: `${m.faits.length} réponses claires et sourcées sur : ${m.titre}. Chacune avec sa référence légale et sa source officielle.`,
  };
}

export default async function DomainePage({ params }: { params: Promise<{ domaine: string }> }) {
  const { domaine } = await params;
  const m = moduleParSlug(domaine);
  if (!m) notFound();

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">
            La Loi Avec Moi
          </Link>
          <Link href="/base-juridique" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            Toutes mes réponses →
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-blue-950 to-slate-900 text-white py-14 px-6">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">{m.titre}</h1>
          <p className="mt-3 text-blue-100">
            {m.faits.length} réponses claires — chacune avec sa référence légale et sa source officielle.
          </p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-10 grid gap-5">
        {m.faits.map((f) => (
          <article key={f.id} className="rounded-2xl border border-slate-200 p-5 bg-white">
            <h2 className="font-semibold text-lg text-slate-900">{f.question}</h2>
            <p className="mt-2 text-slate-700 leading-relaxed">{f.reponse}</p>

            {f.alerte_delai && (
              <p className="mt-3 text-sm rounded-lg bg-red-50 border border-red-200 text-red-800 px-3 py-2">
                ⏱ <strong>À ne pas tarder.</strong> {f.alerte_delai}
              </p>
            )}

            {f.contacts && f.contacts.length > 0 && (
              <div className="mt-3 text-sm rounded-lg bg-blue-50 border border-blue-200 px-3 py-2">
                <strong>📞 Qui contacter :</strong>
                <ul className="mt-1 list-disc list-inside text-slate-700">
                  {f.contacts.map((c, i) => (
                    <li key={i}>
                      {c.nom}
                      {c.numero ? ` — ${c.numero}` : ""}
                      {c.pour ? ` (${c.pour})` : ""}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {f.reference_legale && <p className="mt-3 text-sm text-slate-500">⚖️ {f.reference_legale}</p>}

            {f.sources && f.sources.length > 0 && (
              <div className="mt-2 text-sm">
                <span className="font-semibold text-slate-600">Sources : </span>
                {f.sources.map((s, i) => (
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

            {f.date_verification && <p className="mt-2 text-xs text-slate-400">Vérifié le {f.date_verification}</p>}
          </article>
        ))}

        <p className="text-xs text-slate-400 mt-4 border-t border-slate-100 pt-4">
          Information juridique générale, à jour à la date indiquée. Ne remplace pas un conseil juridique
          individualisé. © La Loi Avec Moi.
        </p>
      </div>
    </main>
  );
}
