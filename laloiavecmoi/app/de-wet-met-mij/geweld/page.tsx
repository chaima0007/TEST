"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Geweld & slachtofferhulp (België) — Nederlandstalige fiche.
// Feiten gespiegeld op de reeds geverifieerde Franstalige fiche (violences_conjugales.json),
// met officiële Nederlandstalige bronnen (hulplijn 1712, Vlaanderen.be).

const fiches = [
  {
    title: "U ondervindt geweld: bel 1712 (gratis en anoniem)",
    text: "1712 is de hulplijn voor elke vraag over geweld, misbruik en kindermishandeling. Het nummer is gratis, verschijnt niet op de telefoonrekening en u hoeft niet te zeggen wie u bent. In een levensbedreigende situatie belt u de politie op 101 of de noodcentrale 112.",
    ref: "Hulplijn 1712 (officieel) — gratis en anoniem",
    url: "https://www.1712.be/nl",
  },
  {
    title: "De pleger kan tijdelijk uit de woning worden gezet",
    text: "Bij huiselijk geweld kan een tijdelijk huisverbod worden opgelegd: de persoon die een ernstige bedreiging vormt, mag de gezamenlijke woning gedurende een bepaalde periode niet betreden. Zo kan het slachtoffer in veiligheid blijven.",
    ref: "Wet van 15 mei 2012 betreffende het tijdelijk huisverbod in geval van huiselijk geweld",
    url: "https://www.vlaanderen.be/hulplijn-geweld-misbruik-en-kindermishandeling-1712",
  },
  {
    title: "Uzelf beschermen en een dossier opbouwen",
    text: "Opzettelijke slagen en verwondingen en bedreigingen zijn strafbaar. U kunt klacht indienen bij de politie. Bewaar bewijzen (medische attesten, foto's, berichten, getuigenissen): ze versterken uw dossier.",
    ref: "Strafwetboek — opzettelijke slagen en verwondingen, bedreigingen; klacht bij de politie",
    url: "https://www.1712.be/nl",
  },
  {
    title: "Gratis slachtofferhulp bestaat",
    text: "De Centra voor Algemeen Welzijnswerk (CAW) bieden gratis slachtofferhulp: een luisterend oor, psychosociale ondersteuning en hulp bij administratieve en juridische stappen. 1712 verwijst u door naar de dienst die het best bij u past.",
    ref: "Vlaanderen.be — hulplijn 1712 en slachtofferhulp (CAW)",
    url: "https://www.vlaanderen.be/hulplijn-geweld-misbruik-en-kindermishandeling-1712",
  },
];

const readText = `Geweld en slachtofferhulp. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function GeweldPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/juridische-hulp" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Juridische hulp →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Geweld & slachtofferhulp
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Geweld: u heeft rechten en hulp</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Wie bellen, hoe uzelf beschermen, het tijdelijk huisverbod en gratis slachtofferhulp —
            duidelijk uitgelegd, met de officiële bron erbij.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Alles voorlezen" lang="nl-BE" />
          </div>
        </div>
      </section>

      <section className="px-6 max-w-3xl mx-auto -mt-8 relative z-10">
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 shadow-sm">
          <p className="text-rose-900 text-sm leading-relaxed">
            🆘 <strong>In gevaar?</strong> Bel onmiddellijk de <strong>politie 101</strong> of de <strong>noodcentrale 112</strong>.
            Voor advies en een luisterend oor: <strong>1712</strong> (gratis, anoniem).
          </p>
        </div>
      </section>

      <section className="py-12 px-6 max-w-3xl mx-auto space-y-5">
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
            ⚖️ Deze fiches geven algemene informatie en vervangen geen persoonlijk juridisch advies. Voor een
            dringende of belangrijke situatie verwijzen wij u naar de <strong>politie</strong>, naar <strong>1712</strong>
            of naar een <strong>advocaat</strong>. U bent nooit verantwoordelijk voor het geweld dat u ondergaat.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
