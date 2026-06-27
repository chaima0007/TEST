import Link from "next/link";
import fs from "node:fs";
import path from "node:path";

// Page "Base juridique vérifiée" — rend les 144 réponses sourcées de data/belgium/*.json.
// Composant serveur : lit les fichiers au build. Source de vérité unique = la base vérifiée.

type Source = { type?: string; url?: string; intitule?: string };
type Contact = { nom?: string; numero?: string; lien?: string; pour?: string; dispo?: string };
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
type Module = { module: string; titre: string; domaine?: string; faits: Fait[] };

function chargerModules(): Module[] {
  const dir = path.join(process.cwd(), "data", "belgium");
  let fichiers: string[] = [];
  try {
    fichiers = fs.readdirSync(dir).filter((f) => f.endsWith(".json") && !f.startsWith("_"));
  } catch {
    return [];
  }
  const mods: Module[] = [];
  for (const f of fichiers.sort()) {
    try {
      const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
      if (d && Array.isArray(d.faits) && d.faits.length) mods.push(d);
    } catch {
      /* ignore fichier illisible */
    }
  }
  return mods.sort((a, b) => (a.titre || "").localeCompare(b.titre || ""));
}

export const metadata = {
  title: "Base juridique vérifiée — La Loi Avec Moi",
  description:
    "Toutes nos réponses juridiques, chacune avec sa source officielle, sa référence légale et sa date de vérification.",
};

export default function BaseJuridiquePage() {
  const modules = chargerModules();
  const totalFaits = modules.reduce((n, m) => n + m.faits.length, 0);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            ← Accueil
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-blue-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Base juridique vérifiée</h1>
          <p className="mt-3 text-blue-100 max-w-2xl">
            {totalFaits} réponses sur {modules.length} domaines — chacune avec sa source officielle,
            sa référence légale et sa date de vérification.
          </p>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-6 py-10">
        <nav aria-label="Domaines" className="flex flex-wrap gap-2 mb-10">
          {modules.map((m) => (
            <a
              key={m.module}
              href={`#${m.module}`}
              className="text-sm px-3 py-1.5 rounded-full border border-slate-200 hover:border-indigo-400 hover:text-indigo-700"
            >
              {m.titre}
            </a>
          ))}
        </nav>

        {modules.map((m) => (
          <section key={m.module} id={m.module} className="mb-12 scroll-mt-20">
            <h2 className="text-2xl font-bold text-blue-900 border-b-2 border-slate-100 pb-2">
              {m.titre}
            </h2>
            <div className="mt-6 grid gap-5">
              {m.faits.map((f) => (
                <article key={f.id} className="rounded-2xl border border-slate-200 p-5 bg-white">
                  <h3 className="font-semibold text-lg text-slate-900">{f.question}</h3>
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

                  {f.reference_legale && (
                    <p className="mt-3 text-sm text-slate-500">⚖️ {f.reference_legale}</p>
                  )}

                  {f.sources && f.sources.length > 0 && (
                    <div className="mt-2 text-sm">
                      <span className="font-semibold text-slate-600">Sources : </span>
                      {f.sources.map((s, i) => (
                        <span key={i}>
                          {i > 0 ? " · " : ""}
                          <a
                            href={s.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-indigo-700 hover:underline"
                          >
                            {s.intitule}
                          </a>
                          {s.type === "officiel" ? (
                            <span className="text-emerald-700 font-medium"> [officiel]</span>
                          ) : (
                            <span className="text-slate-400"> [complément]</span>
                          )}
                        </span>
                      ))}
                    </div>
                  )}

                  {f.date_verification && (
                    <p className="mt-2 text-xs text-slate-400">Vérifié le {f.date_verification}</p>
                  )}
                </article>
              ))}
            </div>
          </section>
        ))}

        <p className="text-xs text-slate-400 mt-10 border-t border-slate-100 pt-4">
          Information juridique générale, à jour à la date indiquée. Ne remplace pas un conseil
          juridique individualisé. Chaque réponse cite ses sources officielles. © La Loi Avec Moi.
        </p>
      </div>
    </main>
  );
}
