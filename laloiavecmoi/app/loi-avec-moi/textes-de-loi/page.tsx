import Link from "next/link";
import fs from "node:fs";
import path from "node:path";

// Page « Textes de loi » — accès direct aux textes officiels ORIGINAUX (consolidés),
// avec pour chacun : l'année, le pourquoi (contexte historique) et les articles clés.
// Source des liens : data/belgium/_textes_legaux.json (registre vérifié au protocole).

type Texte = {
  cle: string;
  nom: string;
  niveau: string;
  url: string;
  articles_cles: string[];
  annee: number;
  contexte: string;
};

function chargerTextes(): Texte[] {
  const file = path.join(process.cwd(), "data", "belgium", "_textes_legaux.json");
  try {
    const d = JSON.parse(fs.readFileSync(file, "utf-8"));
    return Array.isArray(d?.textes) ? d.textes : [];
  } catch {
    return [];
  }
}

const COULEUR_NIVEAU: Record<string, string> = {
  "Fédéral": "bg-indigo-50 text-indigo-700",
  "Wallonie": "bg-rose-50 text-rose-700",
  "Bruxelles": "bg-violet-50 text-violet-700",
  "Flandre": "bg-amber-50 text-amber-700",
  "Union européenne": "bg-sky-50 text-sky-700",
};

export const dynamic = "force-static";

export const metadata = {
  title: "Les textes de loi officiels — La Loi Avec Moi",
  description:
    "Lisez les grands textes de loi belges à la source : Constitution, codes, décrets. Pour chacun : l'année, pourquoi il a été créé, ses articles clés et le lien officiel.",
};

export default function TextesDeLoiPage() {
  const textes = chargerTextes();

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/base-juridique" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            Base juridique →
          </Link>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-6 pt-12 pb-4">
        <p className="text-sm font-semibold text-indigo-600 uppercase tracking-wide">À la source</p>
        <h1 className="mt-1 text-3xl sm:text-4xl font-bold tracking-tight">Les textes de loi, en version originale</h1>
        <p className="mt-4 max-w-2xl text-slate-600 leading-relaxed">
          Nos fiches expliquent la loi simplement — mais rien ne remplace le texte lui-même. Voici les grands
          textes qui protègent vos droits : pour chacun, <strong>l&apos;année</strong>, <strong>pourquoi il a été
          créé</strong>, ses <strong>articles clés</strong>, et le lien direct vers la <strong>version officielle
          consolidée</strong> (Justel / Moniteur belge, EUR-Lex). Gratuit, comme la loi doit l&apos;être.
        </p>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-8 space-y-5">
        {textes.map((t) => (
          <article key={t.cle} className="rounded-3xl border border-slate-200 p-6 hover:border-indigo-200 transition">
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full ${COULEUR_NIVEAU[t.niveau] ?? "bg-slate-100 text-slate-600"}`}>
                {t.niveau}
              </span>
              <span className="text-[11px] font-medium text-slate-400">depuis {t.annee}</span>
            </div>
            <h2 className="mt-2 text-xl font-bold tracking-tight">{t.nom}</h2>
            <p className="mt-2 text-sm text-slate-600 leading-relaxed">
              <span className="font-semibold text-slate-800">Pourquoi ce texte existe : </span>
              {t.contexte}
            </p>
            {t.articles_cles?.length > 0 && (
              <div className="mt-3">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Articles clés</p>
                <ul className="mt-1.5 flex flex-wrap gap-1.5">
                  {t.articles_cles.map((a) => (
                    <li key={a} className="text-xs bg-slate-50 border border-slate-200 rounded-full px-2.5 py-1 text-slate-700">
                      art. {a}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <a
              href={t.url}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 inline-flex items-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-4 py-2.5 transition-colors"
            >
              📜 Lire le texte officiel original ↗
            </a>
          </article>
        ))}
      </section>

      <section className="max-w-4xl mx-auto px-6 pb-16">
        <div className="rounded-2xl bg-slate-50 border border-slate-200 p-5 text-sm text-slate-600 leading-relaxed">
          <p className="font-semibold text-slate-800">💡 Comment lire un texte de loi ?</p>
          <p className="mt-1">
            Les liens mènent vers la version <strong>consolidée</strong> : le texte tel qu&apos;il s&apos;applique
            aujourd&apos;hui, avec toutes ses modifications intégrées. Cherchez l&apos;article qui vous concerne
            (Ctrl+F), puis revenez lire notre fiche pour l&apos;explication simple. Et pour vous tester en vous
            amusant, essayez le <Link href="/loi-avec-moi/quiz" className="text-indigo-700 font-semibold hover:text-indigo-900">quiz des droits</Link>.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à tous les sujets</Link>
      </footer>
    </main>
  );
}
