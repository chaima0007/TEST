import Link from "next/link";

// Nederlandstalige ruimte (België) — « De wet met mij ».
// Volwaardige, aparte ruimte (niet vermengd met de Franstalige/Franse versie),
// volgens het principe « rien ne soit mélangé ». Zelfde rigueur, Belgische bronnen in het NL.
// Slogan : « Het recht, toegankelijk voor iedereen » = « Le droit accessible pour tous ».

type Thema = {
  titel: string;
  beschrijving: string;
  href?: string;
  emoji: string;
};

const themas: Thema[] = [
  { titel: "Wonen & huur", beschrijving: "Huurwaarborg, plaatsbeschrijving, opzeg, herstellingen.", href: "/de-wet-met-mij/wonen", emoji: "🏠" },
  { titel: "Werk", beschrijving: "Opzeg, ontslag, C4, minimumloon, verlof.", href: "/de-wet-met-mij/werk", emoji: "💼" },
  { titel: "Juridische hulp", beschrijving: "Gratis eerste advies en pro-Deo-advocaat volgens inkomen.", href: "/de-wet-met-mij/juridische-hulp", emoji: "⚖️" },
  { titel: "Consumentenrecht", beschrijving: "Herroepingsrecht, garantie, aankopen.", emoji: "🛒" },
  { titel: "Familie & privacy", beschrijving: "Samenwonen, scheiding, GDPR-rechten.", emoji: "👪" },
  { titel: "Administratieve stappen", beschrijving: "Beroep, termijnen, ombudsman.", emoji: "📄" },
];

export default function DeWetMetMijPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">W</span>
            </div>
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            🇫🇷 Version française →
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-24 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            De wet met mij · gratis
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Uw rechten en plichten,
            <span className="block bg-gradient-to-r from-emerald-300 to-teal-300 bg-clip-text text-transparent">
              eindelijk eenvoudig uitgelegd
            </span>
          </h1>
          <p className="mt-4 text-base sm:text-lg font-semibold tracking-wide text-emerald-200">
            Het recht, toegankelijk voor iedereen.
          </p>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            De Belgische wet begrijpen zou niet voor elke vraag een advocaat mogen vereisen.
            Wij leggen uw rechten uit in <strong className="text-white">klare taal</strong>, op basis van
            officiële bronnen — gratis.
          </p>
        </div>
      </section>

      {/* Thema's */}
      <section className="py-16 px-6 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Kies een onderwerp</h2>
        <p className="text-slate-500 text-center mt-3">
          Duidelijke informatie, met telkens de officiële bron erbij.
        </p>
        <div className="mt-10 grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {themas.map((t) =>
            t.href ? (
              <Link
                key={t.titel}
                href={t.href}
                className="group rounded-2xl border border-slate-200 p-6 hover:border-emerald-300 hover:shadow-lg hover:shadow-emerald-600/5 transition-all"
              >
                <span className="text-2xl">{t.emoji}</span>
                <h3 className="font-bold tracking-tight mt-3 group-hover:text-emerald-700 transition-colors">
                  {t.titel}
                </h3>
                <p className="text-slate-600 text-sm mt-1.5 leading-relaxed">{t.beschrijving}</p>
                <span className="inline-block mt-3 text-sm font-semibold text-emerald-700">
                  Bekijken →
                </span>
              </Link>
            ) : (
              <div
                key={t.titel}
                className="rounded-2xl border border-dashed border-slate-200 p-6 opacity-80"
              >
                <span className="text-2xl">{t.emoji}</span>
                <h3 className="font-bold tracking-tight mt-3 text-slate-700">{t.titel}</h3>
                <p className="text-slate-500 text-sm mt-1.5 leading-relaxed">{t.beschrijving}</p>
                <span className="inline-block mt-3 text-xs font-semibold text-slate-400 bg-slate-100 rounded-full px-2.5 py-0.5">
                  Binnenkort
                </span>
              </div>
            )
          )}
        </div>
      </section>

      {/* Transparantie */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h3 className="font-semibold text-amber-900">⚖️ In alle eerlijkheid</h3>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            « De wet met mij » geeft <strong>informatie en oriëntatie</strong> om uw rechten te begrijpen —
            het is <strong>geen persoonlijk juridisch advies</strong> (dat is voorbehouden aan erkende
            professionals). Voor een belangrijke beslissing of een geschil verwijzen wij u naar de juiste
            expert (advocaat, notaris, bemiddelaar). Het doel: duidelijkheid, gratis, in alle veiligheid.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-100 py-10 px-6 text-center text-sm text-slate-500">
        <p>« De wet met mij » — algemene informatie, vervangt geen persoonlijk juridisch advies.</p>
        <div className="mt-3 flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
          <Link href="/loi-avec-moi/nos-assistants" className="text-emerald-700 hover:text-emerald-900 font-medium">
            Wie zijn onze assistenten?
          </Link>
          <Link href="/loi-avec-moi" className="text-emerald-700 hover:text-emerald-900 font-medium">
            🇫🇷 Version française →
          </Link>
        </div>
      </footer>
    </main>
  );
}
