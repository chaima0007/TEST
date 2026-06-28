"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Schulden & collectieve schuldenregeling (België) — Nederlandstalige fiche.
// Feiten gespiegeld op de reeds geverifieerde Franstalige fiche (surendettement.json),
// met officiële Nederlandstalige bronnen (FOD Economie, FOD Financiën).

const fiches = [
  {
    title: "De collectieve schuldenregeling: een uitweg onder gerechtelijk toezicht",
    text: "Wie structureel niet meer in staat is zijn schulden te betalen, kan een collectieve schuldenregeling (CSR) aanvragen bij de arbeidsrechtbank. Alle schuldeisers worden samengebracht en dragen, onder toezicht van een rechter, bij tot een oplossing.",
    ref: "Wet van 5 juli 1998 betreffende de collectieve schuldenregeling; Gerechtelijk Wetboek, art. 1675/2 en volgende",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "Voorwaarden om toegelaten te worden",
    text: "De CSR staat open voor een natuurlijke persoon die duurzaam niet in staat is zijn opeisbare schulden te betalen en die zijn onvermogen niet kennelijk zelf heeft georganiseerd. De aanvraag gebeurt via een verzoekschrift bij de arbeidsrechtbank.",
    ref: "Gerechtelijk Wetboek — toelaatbaarheidsvoorwaarden voor de CSR",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "De schuldbemiddelaar en uw leefgeld",
    text: "De rechtbank stelt een schuldbemiddelaar aan die uw inkomsten beheert en de schuldeisers terugbetaalt. U behoudt een leefgeld: een bedrag om menswaardig te leven (huisvesting, voeding, gezin).",
    ref: "Gerechtelijk Wetboek — schuldbemiddeling en leefgeld",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "Gevolgen en duur",
    text: "Zodra de regeling toelaatbaar is, worden de invorderingen en beslagen in principe opgeschort. Op het einde van een aanzuiveringsregeling kan de rechter het saldo van bepaalde schulden kwijtschelden, zodat u opnieuw kunt starten.",
    ref: "Gerechtelijk Wetboek — gevolgen van de CSR en kwijtschelding van het saldo",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "Niet heel uw loon kan in beslag worden genomen",
    text: "Een deel van uw loon is wettelijk beschermd en kan niet in beslag genomen worden. De voor beslag vatbare gedeelten en de drempels worden jaarlijks op 1 januari geïndexeerd en zijn hoger beschermd als u kinderen ten laste heeft.",
    ref: "Gerechtelijk Wetboek, art. 1409 en volgende (voor beslag vatbare gedeelten); jaarlijkse indexering op 1 januari",
    url: "https://werk.belgie.be/nl/themas/loon",
  },
  {
    title: "Eerst proberen: minnelijke schuldbemiddeling",
    text: "Vóór een gerechtelijke procedure kan een minnelijke schuldbemiddeling helpen om met de schuldeisers een afbetalingsplan af te spreken. De FOD Financiën voorziet bovendien eigen oplossingen (zoals een afbetalingsplan) voor schulden bij de fiscus.",
    ref: "FOD Financiën — wettelijke alternatieven bij betalingsmoeilijkheden",
    url: "https://fin.belgium.be/nl/particulieren/betalen-terugkrijgen/moeilijkheden-betalen/alternatieve-mogelijkheden",
  },
];

const readText = `Schulden en collectieve schuldenregeling. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function SchuldenPage() {
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
            Schulden
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Schulden: u staat er niet alleen voor</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Collectieve schuldenregeling, schuldbemiddelaar, leefgeld en bescherming van uw loon —
            eenvoudig uitgelegd, met de officiële bron erbij.
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
            ⚖️ Wacht niet tot de schulden zich opstapelen. Een erkende <strong>schuldbemiddelingsdienst</strong> (vaak
            via het OCMW of een CAW) helpt u gratis of tegen geringe kosten. Deze fiches geven de grote principes en
            vervangen geen persoonlijk juridisch advies.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
