"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Consumentenrecht (België) — Nederlandstalige fiche.
// Feiten gespiegeld op de geverifieerde Franstalige fiche (Wetboek economisch recht, Boek VI).
// Bronnen in het NL: FOD Economie, Belgium.be, Consumentenombudsdienst.

const fiches = [
  {
    title: "Afstandsverkoop: 14 dagen bedenktijd",
    text: "Bij een online aankoop of aankoop op afstand (telefoon, verkoop aan de deur) heeft u 14 dagen om zich te bedenken, zonder reden op te geven. De termijn loopt vanaf de ontvangst van het pakket.",
    ref: "FOD Economie — herroepingsrecht",
    url: "https://economie.fgov.be/nl/themas/consumentenbescherming",
  },
  {
    title: "Wettelijke garantie van 2 jaar",
    text: "Voor elke aankoop door een consument bij een onderneming geldt een wettelijke garantie van 2 jaar op een nieuw product, vanaf de levering. Ze dekt gebreken aan overeenstemming en komt bovenop elke commerciële garantie van de winkel.",
    ref: "FOD Economie — de garantie",
    url: "https://economie.fgov.be/nl/themas/consumentenbescherming",
  },
  {
    title: "Volledige terugbetaling binnen 14 dagen",
    text: "Nadat u uw herroeping heeft gemeld, moet de verkoper u binnen 14 dagen terugbetalen — inclusief de standaard leveringskosten. Hij mag wachten tot hij het goed (of het verzendbewijs) terug heeft.",
    ref: "Belgium.be — consumentenbescherming",
    url: "https://www.belgium.be/nl/economie",
  },
  {
    title: "Niet elke aankoop heeft een herroepingsrecht",
    text: "De termijn van 14 dagen geldt niet voor alles: producten op maat of gepersonaliseerd, bederfbare goederen, gedownloade digitale inhoud (met uw akkoord), kranten, gedateerde tickets (concerten, reizen)… Controleer steeds de uitzonderingen vóór u koopt.",
    ref: "FOD Economie — uitzonderingen",
    url: "https://economie.fgov.be/nl/themas/consumentenbescherming",
  },
  {
    title: "Geschil? De Consumentenombudsdienst helpt gratis",
    text: "Reageert de verkoper niet, dan kan deze federale openbare dienst gratis bemiddelen om een minnelijke oplossing te vinden, of u doorverwijzen. Klaag eerst schriftelijk (e-mail of aangetekend) en bewaar een kopie.",
    ref: "Consumentenombudsdienst",
    url: "https://consumentenombudsdienst.be/nl",
  },
];

const readText = `Uw rechten als consument. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function ConsumentenrechtPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">W</span>
            </div>
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/familie" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Familie & privacy →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Consumentenrecht
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Uw rechten als consument</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Herroepingsrecht, garantie, terugbetaling: wat de wet voorziet, eenvoudig uitgelegd —
            met de officiële bron om indien nodig te tonen.
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
            ⚖️ Deze fiches geven de grote principes van het consumentenrecht. Voor een geschil: klaag eerst
            schriftelijk, schakel daarna de Consumentenombudsdienst in, en in laatste instantie de vrederechter.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
