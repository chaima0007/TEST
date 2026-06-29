"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Wonen & huur (Vlaanderen) — Nederlandstalige fiche.
// LET OP: huur is een gewestelijke materie. Deze fiche gebruikt het VLAAMS WONINGHUURDECREET
// (decreet van 9 november 2018, voor contracten vanaf 1 januari 2019) — NIET de Waalse of
// Brusselse regels, die verschillen. Officiële bronnen: Vlaanderen.be en codex.vlaanderen.be.

const fiches = [
  {
    title: "De huurwaarborg bedraagt maximaal 3 maanden huur",
    text: "Voor een woninghuurcontract gesloten vanaf 1 januari 2019 mag de huurwaarborg niet meer bedragen dan 3 maanden huur, ongeacht de vorm. U kan kiezen voor een geïndividualiseerde rekening op uw naam, een zakelijke zekerheidstelling of een bankwaarborg via het OCMW.",
    ref: "Vlaams Woninghuurdecreet, art. 37 — huurwaarborg (max. 3 maanden)",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/huren-en-verhuren/huurprijs-en-huurwaarborg/huurwaarborg",
  },
  {
    title: "Een woninghuurcontract duurt in principe 9 jaar",
    text: "De standaardduur is 9 jaar. Wordt het niet tijdig opgezegd (minstens 6 maanden vóór de vervaldag), dan wordt het telkens met 3 jaar verlengd. Een kort contract (3 jaar of minder) is mogelijk, met eigen opzegregels.",
    ref: "Vlaams Woninghuurdecreet, art. 16 — duur van de overeenkomst",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/huren-en-verhuren/einde-en-opzegging-van-het-huurcontract",
  },
  {
    title: "Een omstandige plaatsbeschrijving beschermt u",
    text: "Een tegensprekelijke, gedetailleerde plaatsbeschrijving (bij intrede en uittrede) legt de staat van de woning vast. Ze moet samen met het huurcontract geregistreerd worden. Zonder plaatsbeschrijving is het voor de verhuurder zeer moeilijk om u schade aan te rekenen.",
    ref: "Vlaams Woninghuurdecreet — plaatsbeschrijving; registratie: FOD Financiën",
    url: "https://codex.vlaanderen.be/PrintDocument.ashx?id=1029963&geannoteerd=true",
  },
  {
    title: "U kan altijd opzeggen — let op de vergoeding de eerste 3 jaar",
    text: "Bij een 9-jarig contract kan de huurder op elk moment opzeggen met een opzegtermijn van 3 maanden. Beëindigt u tijdens de eerste 3 jaar, dan is een opzegvergoeding verschuldigd: 3 maanden huur (jaar 1), 2 maanden (jaar 2) of 1 maand (jaar 3). Vanaf het 4de jaar is er geen vergoeding meer.",
    ref: "Vlaams Woninghuurdecreet, art. 20 — opzegging door de huurder",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/huren-en-verhuren/einde-en-opzegging-van-het-huurcontract",
  },
  {
    title: "De huur wordt maar één keer per jaar geïndexeerd",
    text: "De verhuurder mag de huurprijs maximaal één keer per jaar indexeren, ten vroegste op de verjaardag van de inwerkingtreding van het contract, en alleen als het contract schriftelijk is. De indexering volgt de gezondheidsindex.",
    ref: "Vlaams Woninghuurdecreet — indexering van de huurprijs",
    url: "https://codex.vlaanderen.be/PrintDocument.ashx?id=1029963&geannoteerd=true",
  },
  {
    title: "Grote herstellingen zijn voor de verhuurder",
    text: "Het gewone onderhoud en de kleine herstellingen zijn voor de huurder; de grote herstellingen (dak, verwarmingsketel, slijtage door ouderdom of overmacht) zijn voor de verhuurder. Een officiële lijst verduidelijkt wie wat betaalt.",
    ref: "Vlaams Woninghuurdecreet + lijst van herstellingen (B.S. 19/12/2018)",
    url: "https://codex.vlaanderen.be/PrintDocument.ashx?id=1029963&geannoteerd=true",
  },
  {
    title: "Uw huurwoning moet aan kwaliteitsnormen voldoen",
    text: "Een gehuurde woning moet voldoen aan elementaire normen van veiligheid, gezondheid en woningkwaliteit (Vlaamse Codex Wonen). Voldoet de woning niet, dan kan u dit melden bij uw gemeente of Wonen in Vlaanderen.",
    ref: "Vlaamse Codex Wonen / Vlaams Woninghuurdecreet — woningkwaliteitsnormen",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/woningkwaliteit",
  },
  {
    title: "Bij verhuur is een EPC verplicht",
    text: "Wie een woning verhuurt, moet beschikken over een geldig energieprestatiecertificaat (EPC) en het energielabel vermelden in de advertentie. Zo weet u vooraf hoe energiezuinig de woning is.",
    ref: "Vlaams Energiedecreet / Energiebesluit (EPC) — Energiesparen (VEKA)",
    url: "https://www.energiesparen.be/epc-wonen",
  },
];

const readText = `Uw rechten als huurder. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function WonenPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/werk" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Rechten op het werk →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Wonen & huur
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Uw rechten als huurder</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Waarborg, duur, plaatsbeschrijving, opzeg, indexering, herstellingen en woningkwaliteit:
            wat het Vlaams Woninghuurdecreet voorziet, eenvoudig uitgelegd — met de officiële bron erbij.
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
            ⚖️ De huurwetgeving is <strong>geregionaliseerd</strong>: deze fiche beschrijft de <strong>Vlaamse</strong>
            regels (Vlaams Woninghuurdecreet, vanaf 1 januari 2019). In Brussel en Wallonië gelden andere regels.
            Deze fiches geven de grote principes; laat u bij een geschil bijstaan (vrederechter, advocaat,
            juridische bijstand of Wonen in Vlaanderen).
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
