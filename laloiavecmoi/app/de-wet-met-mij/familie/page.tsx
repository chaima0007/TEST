"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Familie & privacy (België) — Nederlandstalige fiche.
// Feiten gespiegeld op de geverifieerde Franstalige fiche.
// Bronnen in het NL: Belgium.be, Justitie, Notaris.be, Gegevensbeschermingsautoriteit.

const fiches = [
  {
    title: "Huwelijk, wettelijke en feitelijke samenwoning: drie heel verschillende statuten",
    text: "Feitelijke samenwoning schept geen juridische band: bij overlijden erft de partner niets automatisch. Wettelijke samenwoning (aangifte bij de gemeente) geeft bescherming van de gezinswoning en vruchtgebruik daarvan. Het huwelijk biedt de breedste bescherming: solidariteit, gewaarborgd reservatair deel en vruchtgebruik op de hele nalatenschap.",
    ref: "Belgium.be — koppel en scheiding",
    url: "https://www.belgium.be/nl/familie",
  },
  {
    title: "Een overeenkomst bij de notaris beschermt uw koppel",
    text: "Zonder huwelijkscontract valt u automatisch onder het wettelijk stelsel. Een huwelijkscontract, of een samenlevingscontract bij notariële akte, laat toe inkomsten, gezinskosten, woning en bescherming bij scheiding te regelen. Het beste moment om te beslissen is vóór een conflict.",
    ref: "Notaris.be — relaties en samenleven",
    url: "https://www.notaris.be/",
  },
  {
    title: "Echtscheiding: twee wegen, naargelang u akkoord bent of niet",
    text: "De echtscheiding met onderlinge toestemming veronderstelt een volledig akkoord (goederen, woning, kinderen, onderhoudsgeld) dat bij de familierechtbank wordt neergelegd — dit is het snelst. Zonder akkoord geldt de echtscheiding wegens onherstelbare ontwrichting: gezamenlijk na 6 maanden scheiding, of eenzijdig na 1 jaar.",
    ref: "Justitie — echtscheiding",
    url: "https://justitie.belgium.be/nl",
  },
  {
    title: "Scheiding en kinderen: het ouderlijk gezag blijft gezamenlijk",
    text: "Of u nu samenwoont of niet, het wettelijk principe is dat beide ouders samen het ouderlijk gezag uitoefenen (belangrijke beslissingen: gezondheid, school, religie). Voor het verblijf onderzoekt de familierechtbank bij onenigheid bij voorrang de gelijkmatig verdeelde huisvesting. Bemiddeling wordt aangemoedigd vóór de procedure.",
    ref: "Belgium.be — ouderlijk gezag",
    url: "https://www.belgium.be/nl/familie",
  },
  {
    title: "Erfenis: uw naasten kunnen niet volledig onterfd worden",
    text: "De Belgische wet beschermt bepaalde erfgenamen via een « reservatair deel »: kinderen (en bij huwelijk de langstlevende echtgenoot) kunnen niet volledig uit de erfenis worden gesloten, zelfs niet bij testament. Over een ander deel beschikt u vrij. De notaris is de sleutelfiguur voor een geldig testament of schenking.",
    ref: "Notaris.be",
    url: "https://www.notaris.be/",
  },
  {
    title: "Uw privacy: u heeft GDPR-rechten",
    text: "U kan toegang vragen tot uw gegevens, ze laten verbeteren of wissen, en zich verzetten tegen bepaald gebruik. Een organisatie moet in principe binnen één maand antwoorden. Bij problemen kan u klacht indienen bij de Gegevensbeschermingsautoriteit (GBA).",
    ref: "Gegevensbeschermingsautoriteit (GBA)",
    url: "https://www.gegevensbeschermingsautoriteit.be/burger",
  },
];

const readText = `Familie en privacy. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function FamiliePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/administratie" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Administratieve stappen →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Familie & privacy
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Familie, koppel & privacy</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Samenwonen, huwelijk, scheiding, erfenis en uw GDPR-rechten: wat de wet voorziet, eenvoudig
            uitgelegd — met de officiële bron.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Alles voorlezen" lang="nl-BE" />
          </div>
        </div>
      </section>

      <section className="py-16 px-6 max-w-3xl mx-auto space-y-5">
        {fiches.map((f, i) => (
          <div key={i} className="rounded-2xl border border-slate-200 p-6">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-emerald-600 text-white text-sm font-bold flex items-center justify-center mt-0.5">{i + 1}</span>
              <div>
                <h2 className="text-lg font-bold tracking-tight">{f.title}</h2>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{f.text}</p>
                <a href={f.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 mt-3 bg-emerald-50 border border-emerald-200 hover:bg-emerald-100 rounded-lg px-3 py-2 transition-colors">
                  🔗 Officiële bron: {f.ref}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </a>
              </div>
            </div>
          </div>
        ))}
      </section>

      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Familiezaken zijn gevoelig en persoonlijk. Voor een belangrijke beslissing (huwelijkscontract,
            scheiding, testament) raadpleeg een <strong>notaris</strong> of een <strong>advocaat</strong>;
            de juridische bijstand kan gratis zijn volgens uw inkomen.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
