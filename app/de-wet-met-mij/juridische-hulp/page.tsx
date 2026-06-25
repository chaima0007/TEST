"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Juridische hulp (België) — Nederlandstalige fiche.
// Toegang tot het recht: gratis eerstelijnsbijstand voor iedereen, en tweedelijnsbijstand
// (« pro Deo ») volgens inkomen via het Bureau voor Juridische Bijstand (BJB).
// Bronnen: advocaat.be (Orde van Vlaamse Balies) en justitie.belgium.be.

const fiches = [
  {
    title: "Eerstelijnsbijstand is gratis voor iedereen",
    text: "Een eerste, kort juridisch advies is gratis en zonder inkomensvoorwaarde: men informeert u en oriënteert u. Beschikbaar via de Commissie voor Juridische Bijstand, justitiehuizen en wetswinkels.",
    ref: "Advocaat.be — juridische bijstand",
    url: "https://www.advocaat.be/nl/een-advocaat-nodig/pro-deo-juridische-bijstand",
  },
  {
    title: "Tweedelijnsbijstand (« pro Deo ») volgens uw inkomen",
    text: "Om bijgestaan of vertegenwoordigd te worden door een advocaat, geheel of gedeeltelijk gratis, afhankelijk van uw inkomen. Het Bureau voor Juridische Bijstand (BJB) controleert uw voorwaarden en wijst een advocaat aan.",
    ref: "Advocaat.be — pro Deo",
    url: "https://www.advocaat.be/nl/een-advocaat-nodig/pro-deo-juridische-bijstand",
  },
  {
    title: "Een ereloonovereenkomst beschermt u",
    text: "Vraag aan uw advocaat een duidelijke afspraak over de erelonen en kosten, liefst schriftelijk. Zo vermijdt u verrassingen en weet u vooraf waar u aan toe bent.",
    ref: "Advocaat.be — erelonen",
    url: "https://www.advocaat.be/nl/een-advocaat-nodig",
  },
  {
    title: "Een rechtsbijstandsverzekering kan de kosten dekken",
    text: "Een rechtsbijstandsverzekering (soms gekoppeld aan uw familiale of autoverzekering) kan advocaat- en procedurekosten geheel of gedeeltelijk dekken. Controleer uw polissen.",
    ref: "Belgium.be — justitie",
    url: "https://www.belgium.be/nl/justitie",
  },
];

const readText = `Juridische hulp. ${fiches.map((f) => f.title + ". " + f.text).join(" ")} Als uw inkomen bescheiden is, kan de juridische bijstand geheel of gedeeltelijk gratis zijn via het Bureau voor Juridische Bijstand. Het eerste advies van de eerste lijn is gratis voor iedereen.`;

export default function JuridischeHulpPage() {
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
          <Link href="/de-wet-met-mij/wonen" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Wonen & huur →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Juridische hulp
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Hulp van een advocaat vinden</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Te duur? Dat hoeft niet. Ontdek de gratis eerstelijnsbijstand en de pro-Deo-advocaat
            volgens uw inkomen — met de officiële bronnen.
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

      {/* Twee lijnen */}
      <section className="pb-8 px-6 max-w-3xl mx-auto">
        <div className="grid sm:grid-cols-2 gap-5">
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
            <h3 className="font-bold tracking-tight text-emerald-900">1️⃣ Eerste lijn — gratis voor iedereen</h3>
            <p className="text-emerald-800/90 text-sm mt-2 leading-relaxed">
              Een kort eerste juridisch advies, <strong>zonder inkomensvoorwaarde</strong>: men informeert
              en oriënteert u.
            </p>
          </div>
          <div className="rounded-2xl border border-indigo-200 bg-indigo-50 p-5">
            <h3 className="font-bold tracking-tight text-indigo-900">2️⃣ Tweede lijn (« pro Deo ») — volgens inkomen</h3>
            <p className="text-indigo-800/90 text-sm mt-2 leading-relaxed">
              Bijstand of vertegenwoordiging door een advocaat, <strong>geheel of gedeeltelijk gratis</strong>,
              afhankelijk van uw inkomen. Het <strong>Bureau voor Juridische Bijstand (BJB)</strong> controleert
              uw voorwaarden.
            </p>
          </div>
        </div>
      </section>

      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ De inkomensvoorwaarden voor juridische bijstand worden regelmatig herzien: controleer de
            actuele bedragen bij het Bureau voor Juridische Bijstand of op advocaat.be.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
