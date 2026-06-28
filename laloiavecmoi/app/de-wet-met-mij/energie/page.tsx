"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Energie (Vlaanderen) — Nederlandstalige fiche.
// LET OP: energie is een gewestelijke materie. Deze fiche gebruikt de VLAAMSE regels
// (Vlaamse Nutsregulator, Fluvius, LAC) — NIET de Waalse (CWaPE), die anders zijn.
// Officiële bronnen: Vlaanderen.be en Vlaamse Nutsregulator.

const fiches = [
  {
    title: "U kunt uw energiefactuur niet betalen: u wordt niet zomaar afgesloten",
    text: "Bij niet-betaling volgt een vaste procedure: eerst een betalingsherinnering (u heeft 15 dagen), dan een ingebrekestelling. Zegt de leverancier daarna uw contract op, dan moet hij nog minstens 45 kalenderdagen energie blijven leveren. Vindt u geen nieuwe leverancier, dan levert netbeheerder Fluvius verder als sociale leverancier.",
    ref: "Vlaanderen.be — wat als u uw factuur voor elektriciteit en aardgas niet betaalt",
    url: "https://www.vlaanderen.be/wat-als-u-uw-factuur-voor-elektriciteit-en-aardgas-niet-betaalt",
  },
  {
    title: "Beschermde afnemers en het sociaal tarief",
    text: "Wie bepaalde uitkeringen of tegemoetkomingen geniet, is « beschermde afnemer » en heeft recht op het sociaal tarief (sociale maximumprijs) — doorgaans zo'n 30 % goedkoper. Het wordt automatisch toegekend: de FOD Economie geeft de rechthebbenden door aan de leveranciers, u hoeft geen attest meer te bezorgen.",
    ref: "Vlaanderen.be — sociaal tarief voor energie (elektriciteit, aardgas, warmte)",
    url: "https://www.vlaanderen.be/sociaal-tarief-voor-energie-elektriciteit-aardgas-warmte",
  },
  {
    title: "Afsluiten kan enkel via de Lokale Adviescommissie (LAC)",
    text: "De netbeheerder mag u niet zomaar afsluiten: een afsluiting vereist in principe de toestemming van de Lokale Adviescommissie (LAC). Beschermde afnemers genieten bovendien extra waarborgen, zoals een gratis betalingsherinnering en ingebrekestelling.",
    ref: "Vlaamse Nutsregulator — sociaal energiebeleid",
    url: "https://www.vlaamsenutsregulator.be/elektriciteit-en-aardgas/energieprijzen-en-facturen/sociaal-energiebeleid",
  },
  {
    title: "Van energieleverancier veranderen is gratis",
    text: "U mag op elk moment van leverancier veranderen. U tekent gewoon een contract bij een nieuwe leverancier; die regelt de overstap en u hoeft uw oude contract niet zelf op te zeggen. Houd rekening met een opzegtermijn van minstens 3 weken. Met de V-test® van de Vlaamse Nutsregulator vergelijkt u de prijzen.",
    ref: "Vlaanderen.be — energieleveranciers en energiecontracten",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/elektriciteit-en-aardgas/energieleveranciers-en-energiecontracten",
  },
];

const readText = `Energie in Vlaanderen. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function EnergiePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/schulden" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Schulden →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Energie (Vlaanderen)
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Uw rechten rond energie</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Betalingsmoeilijkheden, bescherming tegen afsluiting, sociaal tarief en van leverancier veranderen:
            duidelijk uitgelegd — met de officiële bron erbij.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Alles voorlezen" lang="nl-BE" />
          </div>
        </div>
      </section>

      <section className="px-6 max-w-3xl mx-auto -mt-8 relative z-10">
        <div className="rounded-2xl border border-sky-200 bg-sky-50 p-5 shadow-sm">
          <p className="text-sky-900 text-sm leading-relaxed">
            ℹ️ Energie is een <strong>gewestelijke</strong> bevoegdheid. Deze fiche beschrijft de <strong>Vlaamse</strong>
            regels. In Wallonië en Brussel gelden andere regelaars en procedures.
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
            ⚖️ Bij betalingsmoeilijkheden kunt u een afbetalingsplan vragen aan uw leverancier, het <strong>OCMW</strong>
            of een erkende <strong>schuldbemiddelaar</strong>. Deze fiches geven de grote principes en vervangen geen
            persoonlijk advies.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
